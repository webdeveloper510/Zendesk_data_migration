from django.shortcuts import render
from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from rest_framework import status
import json
import pandas as pd
import time
import csv
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Tickets, Plant
from base64 import b64encode
import base64
import datetime
import numpy as np
import re   
# Create your views here.

# Zendesk credentials
ZENDESK_API_USERNAME = "nikhil@codenomad.net"
ZENDESK_API_PASSWORD = "Codenomad@2020"
SUBDOMAIN = "z3nhd"

# User create in bulk
def UserCreate(request):
    return process_csv('myapp/files/test.csv', chunk_size=2)

def user_structure(row):
    return {
            "email": row["email"],
            "name": row["name"],
            "role": row["role"],
            "phone": row["phone"],
            "tags": row["tags"],
            "brand":row["brand"]
            }
            
            
ZENDESK_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2/users/create_many"
# BASE_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2/users/create_many"

def create_user_api(user_list):
    payload = json.dumps({"users": user_list})
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.request(
        "POST",
        ZENDESK_URL,
        auth=(ZENDESK_API_USERNAME, ZENDESK_API_PASSWORD),
        headers=headers,
        data=payload
    )
    return response

def process_csv(file_path, chunk_size=2):
    try:
        df = pd.read_csv(file_path)
        total_records = len(df)
        for start_idx in range(0, total_records, chunk_size):
            end_idx = start_idx + chunk_size
            chunk = df[start_idx:end_idx]
            user_list = []
            for _, row in chunk.iterrows():
                user_list.append(user_structure(row))
            response = create_user_api(user_list)
            print("ress",response)
            print(f"Processed {len(user_list)} records. Response: {response.status_code}")
        return JsonResponse({"message":response.json()})
    except Exception as e:
        return JsonResponse({"error": str(e)})
    

# Create ticket in bulk
def Create_ticket(request):
    return process_csv_in_chunks_ticket('myapp/files/test.csv', chunk_size=100)

API_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2/imports/tickets/create_many"

def create_ticket_structure(row):
    return {
            "comments": [
                {
                "value": row['body']
                }
            ],
            "subject": row['subject'],
            "tags": row['tags'],
            "priority": str(row['priority']),
            "type": row['type'],
            "status": row['status']
            }

def ticket_api(ticket_list):
    payload = json.dumps({"tickets": ticket_list})
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        API_URL,
        auth=(ZENDESK_API_USERNAME, ZENDESK_API_PASSWORD),
        headers=headers,
        data=payload
    )
    return response

def process_csv_in_chunks_ticket(file_path, chunk_size=100):
    try:
        df = pd.read_csv(file_path)
        total_records = len(df)
        for start_idx in range(0, total_records, chunk_size):
            end_idx = start_idx + chunk_size
            chunk = df[start_idx:end_idx]
            ticket_list = [create_ticket_structure(row) for _, row in chunk.iterrows()]
            response = ticket_api(ticket_list)
           
           # Get response data
            job_status = response.json().get('job_status', {})
            job_type = job_status.get('job_type')
            url = job_status.get('url')
            status = job_status.get('status')
            # Save the response to the database
            Tickets.objects.create(
                job_type=job_type,
                url=url,
                status =status,
                complete_json = job_status
            )

            print(f"Processed {len(ticket_list)} records. Response: {response.status_code}")
        return JsonResponse({"message":response.json()})
    except Exception as e:
        return JsonResponse({"error": str(e)})

################## Get tickets ######################

class ShowTicket(APIView):
    def get(self,request, *args, **kwargs):
        url = f"https://{SUBDOMAIN}.zendesk.com/api/v2/tickets"
        headers = {
            "Content-Type": "application/json",
        }
        params = {
            'per_page':100,
            'page': 1,   
            'sort_by': 'created_at',
            'sort_order': 'desc'
        }
        response = requests.request(
            "GET",
            url,
            auth=(ZENDESK_API_USERNAME,ZENDESK_API_PASSWORD),
            headers=headers,
            params=params
        )
        response_data = response.json()
        sorted_users = sorted(response_data['tickets'], key=lambda x: x['created_at'], reverse=True)
        return Response({"data":sorted_users})
    

######## Single attach with comment ########

class attachFile(APIView):
    def post(self, request, *args, **kwargs):
        # Assuming the CSV file has a single column 'file_path'
        csv_file_path = 'myapp/files/files_list.csv'

        # Read file paths from CSV
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            file_paths = [row['file'] for row in reader]
            print("fffffff",file_paths)

        # Zendesk credentials
        auth = ('harjot@codenomad.net', 'harjot@123')

        # Upload files
        upload_tokens = []
        print("uuuuuu",upload_tokens)
        for file_path in file_paths:
            print("111",file_path)
            with open(file_path, 'rb') as f:
                url = 'https://codenomad8499.zendesk.com/api/v2/uploads.json'
                params = {'filename': file_path}
                headers = {'Content-Type': 'pdf/png'}
                response = requests.post(url, params=params,headers=headers ,data=f, auth=auth).json()
                # print("rrrrrrrr",response)
                upload_tokens.append(response['upload']['token'])

        # Attach files to the ticket
        url = 'https://codenomad8499.zendesk.com/api/v2/tickets'
        payload = {
            'ticket': {
                'subject': 'Multiple File Upload',
                'comment': {
                    'body': 'Test multiple file upload',
                    'uploads': upload_tokens
                },
                "tags": "test",
                "type": "task"
            }
        }
        response = requests.post(url, json=payload, auth=auth)
        return Response({"data": response.json()})
    

##### Create ticket with attachment in bulk #######
def Create_ticket_with_attachment(request):
    return process_csv_in_chunks('myapp/files/files_list.csv', chunk_size=10)

ZENDESK_API_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2/tickets/create_many"

def create_ticket_attach_structure(row, upload_token):
    return {
        "comment": {
            "body": row['body'],
            "uploads": upload_token
        },
        "subject": row['subject'],
        "priority": str(row['priority']),
        "tags": row['tags'],
        "type": row['type'],
        "status": row['status']
    }

def attach_tickets(ticket_list):
    payload = json.dumps({"tickets": ticket_list})
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(
        ZENDESK_API_URL,
        auth=(ZENDESK_API_USERNAME,ZENDESK_API_PASSWORD),
        headers=headers,
        data=payload
    )
    return response

def upload_file(file_path):
    with open(file_path, 'rb') as f:
        url = f'https://{SUBDOMAIN}.zendesk.com/api/v2/uploads.json'
        params = {'filename': file_path}
        headers = {'Content-Type': 'image/pdf'}
        response = requests.post(url, params=params, headers=headers, data=f, auth=(ZENDESK_API_USERNAME,ZENDESK_API_PASSWORD)).json()
        # print("resss",response)
        return response['upload']['token']

def process_csv_in_chunks(file_path, chunk_size=10):
    try:
        df = pd.read_csv(file_path)
        total_records = len(df)
        
        for start_idx in range(0, total_records, chunk_size):
            end_idx = start_idx + chunk_size
            chunk = df[start_idx:end_idx]
            
            upload_tokens = [upload_file(row['file']) for _, row in chunk.iterrows()]
            print("uppp",upload_tokens)
            ticket_list = []
            for (_, row), upload_token in zip(chunk.iterrows(), upload_tokens):
                ticket = create_ticket_attach_structure(row, upload_token)
                ticket_list.append(ticket)
            print("gggggg",ticket_list)
            response = attach_tickets(ticket_list)
            print(f"Processed {len(ticket_list)} records. Response: {response.status_code}")
        
        return JsonResponse({"message": response.json()})
    
    except Exception as e:
        return JsonResponse({"error": str(e)})

######## Save excel file in database ########

def save_excel_data(request):
    try:
        file_path = "myapp/files/Claim master TN & Dahej(2020).xls"
        df = pd.read_excel(file_path)
        # print("DataFrame:", df)
        for index, row in df.iterrows():
            Plant.objects.create(
                date=row['Date'],
                number_of_tyres=row['No of tyres'],
                size=row['Size'],
                design=row['Design'],
                LI_SI_PR=row['LI /SI /PR'],
                type=row['Type'],
                cat_no=row['CAT No.'],
                tyre_serial_number=row['Tyre serial number'],
                plant = row['PLANT'],
                claim_no=row['CLAIM NO'],
                date_of_mounting=row['Date of mounting'],
                invoice_details=row['Invoice details'],
                remaining_tread_depth=row['REMAINING TREAD DEPTH (%)'],
                defect=row['DEFECT'],
                our_recommendation=row['OUR RECOMMENDATION'],
                remarks=row['REMARKS'],
                dispose_by=row['DISPOSED BY'],
                customer_name=row['Customer Name'],
                country=row['Country'],
                customer_ref_no=row['Customer Ref no.'],
                ND_Used=row['ND/Used'],
                old_ticket_no=row['OLD ticket No.'],)

        return HttpResponse("save excel data successfully")
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        return HttpResponse(e,"false")  # Import failed

# def data_del(request):
#     us_del =Plant.objects.all().delete()
#     print("dddd",us_del)
#     return HttpResponse("delete all data")

################# Ticket create in bulk (Yokohaman) ###############
 
class CustomerData(APIView):
    def post(self, request, *args, **kwargs):
        return process_excel_in_chunks_ticket('myapp/customer_files/Test.xlsx', chunk_size=2)


def create_ticket_structure_excel(row):
    return {
            "comments": [
                {
                "body": row['DEFECT']
                }
            ],
            "tags": row['CLAIM NO'],
            # "status": 'new',
            "requester_id":"22574494361233",
            # "assignee_id":"17459473072145",
            "custom_fields": [{"id": 17459369077521, "value": row['DEFECT']},  #Description
                              {"id": 21115540894737, "value": row['CAT No.']},  #Cat Number
                              {"id": 21115518082321, "value": row['Type']},     # Type (TT/TL)
                              {"id": 21115488705297, "value": row['Country']},  # Country
                              {"id": 21256551170961, "value": row['Customer Name']}, #Name
                              {"id": 21145754951697, "value": row['OUR RECOMMENDATION']},#Recommendation for this request
                              {"id": 21145491038481, "value": row['No of tyres']}, #No of tyres
                              {"id": 21115597806225, "value": row['Date of Invoice']}, #Invoice Date
                              {"id": 21952306937105, "value": row['LI /SI /PR']}, #P.R/L.I./S.S Rating
                              {"id": 21115551933969, "value": row['Design']},  #Pattern
                              {"id": 21558274008721, "value": row['PLANT']},  #Plant
                              {"id": 21115763616529, "value": row['REMAINING TREAD DEPTH (%)']},  #% RTD
                              {"id": 21115566381201, "value": row['Tyre serial number']},  #Tire Serial Number
                              {"id": 21115676972177, "value": row['Remark']},],  #Additional Observation / Remark
                                }


def ticket_excel_api(ticket_list):
    url = "https://yokohamaoff-highwaytires.zendesk.com/api/v2/imports/tickets/create_many"
    Username = "sreevidya@godigitalcx.com"
    Password = "4WKO4l4mWhhlSvLkGByJyJ1zu0fmLlnn6Gm3q6gZ"
    auth_string = f"{Username}/token:{Password}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
    payload = json.dumps({"tickets": ticket_list})
    print("pppppppp",payload)
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Basic {encoded_auth}'
        }
    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers
    )
    return response


def process_excel_in_chunks_ticket(file_path, chunk_size=2):
    def same_date(date_str):
        try:
            date = pd.to_datetime(date_str, errors='raise')
            return date.strftime('%d/%m/%Y')
        except (TypeError, ValueError):
            return np.nan
        
    def remove_text_date(date_str):
        if not isinstance(date_str, str):
            date_str = str(date_str)
        match = re.search(r'(\d{1,2}[-/\s]\d{1,2}[-/\s]\d{2,4})', date_str)
        if match:
            return match.group(1)
        return date_str
    try:    
        df = pd.read_excel(file_path)
        total_records = len(df)
        for start_idx in range(0, total_records, chunk_size):
            end_idx = min(start_idx + chunk_size, total_records)
            chunk = df.iloc[start_idx:end_idx].copy()
            chunk['Date of Invoice'] = chunk['Date of Invoice'].apply(remove_text_date)
            
            chunk['Date of Invoice'] = chunk['Date of Invoice'].apply(same_date)
            if not pd.api.types.is_datetime64_any_dtype(chunk['Date of Invoice']):
                chunk['Date of Invoice'] = pd.to_datetime(chunk['Date of Invoice'], format='%d/%m/%Y', errors='coerce')
            chunk['Date of Invoice'] = chunk['Date of Invoice'].dt.strftime("%Y-%m-%d").astype(str)
            
            chunk['Date of Invoice'].fillna("nan", inplace=True)
            chunk['Size'].fillna("nan", inplace=True)
            chunk['Country'].fillna("nan", inplace=True)
            chunk['LI /SI /PR'].fillna("nan", inplace=True)
            chunk['Tyre serial number'].fillna("nan", inplace=True)
            cus_ticket_list = [create_ticket_structure_excel(row) for _, row in chunk.iterrows()]
            ticket_list = [{k: [i for i in v if not (isinstance(i.get('value'), str) and i.get('value') == 'nan')] if k == 'custom_fields' else v for k, v in d.items()} for d in cus_ticket_list]
            print("lllllllll",ticket_list)
            response = ticket_excel_api(ticket_list)
            
           # get response data
            job_status = response.json().get('job_status', {})
            job_type = job_status.get('job_type')
            url = job_status.get('url')
            status = job_status.get('status')
            # save the response to the database
            Tickets.objects.create(
                job_type=job_type,
                url=url,
                status =status,
                complete_json = job_status
            )
            
            print(f"Processed {len(cus_ticket_list)} records. Response: {response.status_code}")
        return JsonResponse({"message":response.json()})
    except Exception as e:
        return JsonResponse({"error": str(e)})
    

def deleteuser(request):
    da = Tickets.objects.all().delete()
    return JsonResponse({"msg":da})





# class attachFile(APIView):
#     def post(self, request, *args, **kwargs):
#         local_filename = 'myapp/files/comment.csv'
#         attachment_filename = local_filename

#         auth=('harjot@codenomad.net', 'harjot@123')

#         # upload file
#         url = 'https://codenomad8499.zendesk.com/api/v2/uploads.json'
#         params = {'filename': attachment_filename}
#         # headers = {'Content-Type': 'image/png'}
#         with open(local_filename, 'rb') as f:
#             response = requests.post(url, params=params, data=f, auth=auth).json()
#         upload_token = response['upload']['token']

#         # attach file
#         url = 'https://codenomad8499.zendesk.com/api/v2/tickets'
#         payload = {
#             'ticket': {
#                 'subject': 'File upload',
#                 'comment': {
#                     'body': 'Test file',
#                     'uploads': [upload_token]
#                 },
#                 "tags" : "test",
#                 "type" : "task"
#             }
#         }
#         response = requests.post(url, json=payload, auth=auth)
#         return Response({"data":response.json()})




# # Create ticket in bulk
# def Create_ticket(request):
#     return process_csv_in_chunks_ticket('myapp/files/comment.csv', chunk_size=100)

# API_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2/tickets/create_many"

# def create_ticket_structure(row):
#     return {
#         "comment": {
#             "body": row['body']
#         },
#         "subject": row['subject'],
#         "priority": str(row['priority']),
#         "tags": row['tags'],
#         "description":row['description'],
#         "type": row['type'],
#         "status": row['status']
#     }

# def ticket_api(ticket_list):
#     payload = json.dumps({"tickets": ticket_list})
#     headers = {
#         "Content-Type": "application/json",
#     }
#     response = requests.post(
#         API_URL,
#         auth=(ZENDESK_API_USERNAME, ZENDESK_API_PASSWORD),
#         headers=headers,
#         data=payload
#     )
#     return response

# def process_csv_in_chunks_ticket(file_path, chunk_size=2):
#     try:
#         df = pd.read_csv(file_path)
#         total_records = len(df)
#         for start_idx in range(0, total_records, chunk_size):
#             end_idx = start_idx + chunk_size
#             chunk = df[start_idx:end_idx]
#             ticket_list = [create_ticket_structure(row) for _, row in chunk.iterrows()]
#             response = ticket_api(ticket_list)
#             print(f"Processed {len(ticket_list)} records. Response: {response.status_code}")
#         return JsonResponse({"message":response.json()})
#     except Exception as e:
#         return JsonResponse({"error": str(e)})