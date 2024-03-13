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
from .models import *
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
    return process_csv('myapp/customer_files/User-data.csv', chunk_size=2)

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
        file_path = "/home/oem/Downloads/yokohamaTest-ticket.ods"
        df = pd.read_excel(file_path)
        # print("DataFrame:", df)
        for index, row in df.iterrows():
            legacy_claim_no = "legacy_" + str(row['CLAIM NO'])
            unique_data_id = "uid_" + str(row['Unique ID'])
            claim_no_with_migration = "data_migration" + ", " + legacy_claim_no + ", " + unique_data_id
            CustomerTicket.objects.create(
                unique_id=row['Unique ID'],
                date=row['Date'],
                no_of_tyre=row['NO. OF TYRE'],
                size=row['SIZE'],
                design=row['Design'],
                li_si_pr=row['LI /SI /PR'],
                type=row['TYPE'],
                cat_no=row['CAT No.'],
                tyre_serial_no=row['TYRE SERIAL NO.'],
                plant = row['PLANT'],
                claim_no=claim_no_with_migration,
                date_of_invoice=row['DATE OF INVOICE/ SALE/ MOUNTING'],
                invoice_details=row['Invoice details'],
                remaining_tread_depth=row['REMAINING TREAD DEPTH (%)'],
                defect_code_description=row['Defect Code Description'],
                our_recommendation=row['OUR RECOMMENDATION'],
                remarks=row['REMARKS'],
                disposed_by=row['DISPOSED BY'],
                customer_code=row['Customer code'],
                customer_name=row['CUSTOMER NAME'],
                country_working=row['Country-working'],
                region=row['Region'],
                )

        return HttpResponse("save excel data successfully")
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        return HttpResponse(e,"false")

# def data_del(request):
#     us_del =Plant.objects.all().delete()
#     print("dddd",us_del)
#     return HttpResponse("delete all data")
    
############ Yokohama User create in bulk  #############
class CustomerCreate(APIView):
    def post(self, request, *args, **kwargs):
        return process_csv('myapp/customer_files/User-data.xlsx', chunk_size=2)

def customer_structure(row):
    try:
        email = row["email"]
        name = row["Name 1"]
        country = row.get("Country", "")
        region = row.get("Region", "")
        distributor_number = row.get("Customer", "")
        house_number = row.get("House Number", "")
        street = row.get("Street", "")
        street2 = row.get("Street 2", "")
        # street3 = row.get("Street 3", "")

        address = f"{house_number}{street}{street2}"

        return {
            "email": email,
            "name": name,
            "user_fields": {
                "country": country,
                # "region": region,
                "distributor_number": distributor_number,
                "address": address
            }
        }
    except KeyError as e:
        print(f"KeyError: {e}")
        return {}
    except Exception as e:
        print("Error in customer_structure:", e)
        return {}

            
            
def user_excel_api(customer_list):
    url = "https://yokohama-atg.zendesk.com/api/v2/users/create_many"
    Username = "sreevidya@godigitalcx.com"
    Password = "4WKO4l4mWhhlSvLkGByJyJ1zu0fmLlnn6Gm3q6gZ"
    auth_string = f"{Username}/token:{Password}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
    payload = json.dumps({"users": customer_list})
    print("Payload:", payload)
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Basic {encoded_auth}'
    }
    response = requests.post(url, data=payload, headers=headers)
    print("Response:", response.json())  # Debugging statement
    return response

def process_csv(file_path, chunk_size=2):
    try:
        df = pd.read_excel(file_path)
        total_records = len(df)
        for start_idx in range(0, total_records, chunk_size):
            end_idx = start_idx + chunk_size
            chunk = df[start_idx:end_idx]
            chunk['Region'].fillna("nan", inplace=True)
            chunk['Country'].fillna("nan", inplace=True)
            chunk['Customer'].fillna("nan", inplace=True)


            user_list = [customer_structure(row) for _, row in chunk.iterrows()]
            print("==========++++++------",user_list)
            # customer_list = [{
            #     k: v if k != 'user_fields' else {
            #         k2: v2 for k2, v2 in v.items() if v2 is not None
            #     }
            #     for k, v in d.items()
            # } for d in user_list]
            customer_list = []
            for d in user_list:
                cleaned_dict = {}
                for k, v in d.items():
                    if isinstance(v, list):
                        cleaned_values = [i for i in v if not (isinstance(i, str) and i == 'nan')]
                        cleaned_dict[k] = cleaned_values if cleaned_values else None
                    else:
                        cleaned_dict[k] = v if not (isinstance(v, str) and v == 'nan') else None
                cleaned_dict = {k: v for k, v in cleaned_dict.items() if v is not None and not (isinstance(v, str) and v == 'nan')}  # Remove keys with NaN values
                customer_list.append(cleaned_dict)
            print("lllllllll",customer_list)
            response = user_excel_api(customer_list)
            print("==========+++++++++++",response)
            print(f"Processed {len(customer_list)} records. Response: {response.status_code}")
        print(f"Processed {len(response)} records. Response: {response.status_code}")
        return JsonResponse({"message":response.json()})
    except Exception as e:
        return JsonResponse({"error": str(e)})


################# Ticket create in bulk (Yokohaman) ###############
    
class CustomerData(APIView):
    def post(self, request, *args, **kwargs):
        return process_excel_in_chunks_ticket('myapp/customer_files/new-data-test.xlsx', chunk_size=2)


def create_ticket_structure_excel(row):
   
    return {
            "comments": [
                {
                "body": row['Defect Code Description']
                }
            ],
            "tags": str(row['CLAIM NO']),
            "status": 'closed',
            "requester_id":"23066867293841",
            # "assignee_id":"17459473072145",
            "custom_fields": [{"id": 17459369077521, "value": row['Defect Code Description']},  #Description
                              {"id": 21115540894737, "value": row['CAT No.']},  #Cat Number
                              {"id": 21115518082321, "value": row['TYPE']},     # Type (TT/TL)
                              {"id": 21115488705297, "value": row['Country-working']},  # Country
                              {"id": 21256551170961, "value": row['CUSTOMER NAME']}, #Name
                              {"id": 21145754951697, "value": row['OUR RECOMMENDATION']},#Recommendation for this request
                              {"id": 22364299286289, "value": row['SIZE']}, #tyre size
                              {"id": 21115597806225, "value": row['DATE OF INVOICE/ SALE/ MOUNTING']}, #Invoice Date
                              {"id": 22339841877137, "value": row['LI /SI /PR']}, #P.R/L.I./S.S Rating
                              {"id": 22339398247057, "value": row['Design']},  #Pattern
                              {"id": 21558274008721, "value": row['PLANT']},  #Plant
                              {"id": 21115763616529, "value": row['REMAINING TREAD DEPTH (%)']},  #% RTD
                              {"id": 21115566381201, "value": row['TYRE SERIAL NO.']},  #Tire Serial Number
                              {"id": 22306316700433, "value": row['Region']},  #Construction

                              {"id": 21115676972177, "value": row['REMARKS']}]  #Additional Observation / Remark
                              
                                }


def ticket_excel_api(ticket_list):
    url = "https://yokohama-atg.zendesk.com/api/v2/imports/tickets/create_many"
    Username = "sreevidya@godigitalcx.com"
    Password = "4WKO4l4mWhhlSvLkGByJyJ1zu0fmLlnn6Gm3q6gZ"
    auth_string = f"{Username}/token:{Password}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
    payload = json.dumps({"tickets": ticket_list})
    print("Payload:", payload)  # Debugging statement
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Basic {encoded_auth}'
    }
    response = requests.post(url, data=payload, headers=headers)
    print("Response:", response.json())  # Debugging statement
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
            chunk['DATE OF INVOICE/ SALE/ MOUNTING'] = chunk['DATE OF INVOICE/ SALE/ MOUNTING'].apply(remove_text_date)
            
            chunk['DATE OF INVOICE/ SALE/ MOUNTING'] = chunk['DATE OF INVOICE/ SALE/ MOUNTING'].apply(same_date)
            if not pd.api.types.is_datetime64_any_dtype(chunk['DATE OF INVOICE/ SALE/ MOUNTING']):
                chunk['DATE OF INVOICE/ SALE/ MOUNTING'] = pd.to_datetime(chunk['DATE OF INVOICE/ SALE/ MOUNTING'], format='%d/%m/%Y', errors='coerce')
            chunk['DATE OF INVOICE/ SALE/ MOUNTING'] = chunk['DATE OF INVOICE/ SALE/ MOUNTING'].dt.strftime("%Y-%m-%d").astype(str)
            
            chunk['DATE OF INVOICE/ SALE/ MOUNTING'].fillna("nan", inplace=True)
            chunk['SIZE'].fillna("nan", inplace=True)
            chunk['Country-working'].fillna("nan", inplace=True)
            chunk['LI /SI /PR'].fillna("nan", inplace=True)
            chunk['TYRE SERIAL NO.'].fillna("nan", inplace=True)
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




# class CustomerData(APIView):
#     def post(self, request, *args, **kwargs):
#         return process_excel_in_chunks_ticket('myapp/customer_files/Test_ticket.xlsx', chunk_size=2)


# def create_ticket_structure_excel(row):
#     return {
#             "comments": [
#                 {
#                 "body": row['DEFECT']
#                 }
#             ],
#             "tags": row['CLAIM NO'],
#             "status": 'new',
#             "requester_id":"23066867293841",
#             # "assignee_id":"17459473072145",
#             "custom_fields": [{"id": 17459369077521, "value": row['DEFECT']},  #Description
#                               {"id": 21115540894737, "value": row['CAT No.']},  #Cat Number
#                               {"id": 21115518082321, "value": row['Type']},     # Type (TT/TL)
#                               {"id": 21115488705297, "value": row['Country']},  # Country
#                               {"id": 21256551170961, "value": row['Customer Name']}, #Name
#                               {"id": 21145754951697, "value": row['OUR RECOMMENDATION']},#Recommendation for this request
#                               {"id": 21145491038481, "value": row['No of tyres']}, #No of tyres
#                               {"id": 21115597806225, "value": row['Date of Invoice']}, #Invoice Date
#                               {"id": 21952306937105, "value": row['LI /SI /PR']}, #P.R/L.I./S.S Rating
#                               {"id": 21115551933969, "value": row['Design']},  #Pattern
#                               {"id": 21558274008721, "value": row['PLANT']},  #Plant
#                               {"id": 21115763616529, "value": row['REMAINING TREAD DEPTH (%)']},  #% RTD
#                               {"id": 21115566381201, "value": row['Tyre serial number']},  #Tire Serial Number
#                               {"id": 21115676972177, "value": row['Remark']},],  #Additional Observation / Remark
#                                 }


# def ticket_excel_api(ticket_list):
#     url = "https://yokohama-atg.zendesk.com/api/v2/imports/tickets/create_many"
#     Username = "sreevidya@godigitalcx.com"
#     Password = "4WKO4l4mWhhlSvLkGByJyJ1zu0fmLlnn6Gm3q6gZ"
#     auth_string = f"{Username}/token:{Password}"
#     encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
#     payload = json.dumps({"tickets": ticket_list})
#     print("pppppppp",payload)
#     headers = {
#         "Content-Type": "application/json",
#         'Authorization': f'Basic {encoded_auth}'
#         }
#     response = requests.request(
#         "POST",
#         url,
#         data=payload,
#         headers=headers
#     )
#     print("+++++++++++++",response)
#     return response


# def process_excel_in_chunks_ticket(file_path, chunk_size=2):
#     def same_date(date_str):
#         try:
#             date = pd.to_datetime(date_str, errors='raise')
#             return date.strftime('%d/%m/%Y')
#         except (TypeError, ValueError):
#             return np.nan
        
#     def remove_text_date(date_str):
#         if not isinstance(date_str, str):
#             date_str = str(date_str)
#         match = re.search(r'(\d{1,2}[-/\s]\d{1,2}[-/\s]\d{2,4})', date_str)
#         if match:
#             return match.group(1)
#         return date_str
#     try:    
#         df = pd.read_excel(file_path)
#         total_records = len(df)
#         for start_idx in range(0, total_records, chunk_size):
#             end_idx = min(start_idx + chunk_size, total_records)
#             chunk = df.iloc[start_idx:end_idx].copy()
#             chunk['Date of Invoice'] = chunk['Date of Invoice'].apply(remove_text_date)
            
#             chunk['Date of Invoice'] = chunk['Date of Invoice'].apply(same_date)
#             if not pd.api.types.is_datetime64_any_dtype(chunk['Date of Invoice']):
#                 chunk['Date of Invoice'] = pd.to_datetime(chunk['Date of Invoice'], format='%d/%m/%Y', errors='coerce')
#             chunk['Date of Invoice'] = chunk['Date of Invoice'].dt.strftime("%Y-%m-%d").astype(str)
            
#             chunk['Date of Invoice'].fillna("nan", inplace=True)
#             chunk['Size'].fillna("nan", inplace=True)
#             chunk['Country'].fillna("nan", inplace=True)
#             chunk['LI /SI /PR'].fillna("nan", inplace=True)
#             chunk['Tyre serial number'].fillna("nan", inplace=True)
#             cus_ticket_list = [create_ticket_structure_excel(row) for _, row in chunk.iterrows()]
#             ticket_list = [{k: [i for i in v if not (isinstance(i.get('value'), str) and i.get('value') == 'nan')] if k == 'custom_fields' else v for k, v in d.items()} for d in cus_ticket_list]
#             print("lllllllll",ticket_list)
#             response = ticket_excel_api(ticket_list)
            
#            # get response data
#             job_status = response.json().get('job_status', {})
#             job_type = job_status.get('job_type')
#             url = job_status.get('url')
#             status = job_status.get('status')
#             # save the response to the database
#             Tickets.objects.create(
#                 job_type=job_type,
#                 url=url,
#                 status =status,
#                 complete_json = job_status
#             )
            
#             print(f"Processed {len(cus_ticket_list)} records. Response: {response.status_code}")
#         return JsonResponse({"message":response.json()})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}) 


    

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




import numpy as np

def save_customer_data(request):
    try:
        file_path = "myapp/customer_files/Test-new-latest-user.xlsx"
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            # Convert each value to string and handle NaN values
            address_parts = [
                str(row['House Number']),
                str(row['Street']),
                str(row['Street 2']),
                str(row['Street 3']),
                str(row['Street 4']),
                str(row['Street 5']),
                str(row['City']),
                str(row['Postal Code'])
            ]
            # Filter out empty strings and NaN values and join them with a comma
            address = ", ".join(filter(lambda x: x != 'nan', address_parts))
            UserData.objects.create(
                account_group=row['Account group'],
                customer=row['Customer'],
                name=row['Name 1'],
                search_term=row['Search term'],
                address=address,
                country=row['Country'],
                region=row['Region'],
                email=row['email'],
                branch=row['Branch ']
            )
        return HttpResponse("save excel data successfully")
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        return HttpResponse("false")  # Import failed
    

class Addcustomer(APIView):
    def post(self, request, *args, **kwargs):
        try:
            process_database_records_in_chunks()
            return JsonResponse({"message": "Processing complete"})
        except Exception as e:
            return JsonResponse({"error": str(e)})

def customer_add_api(ticket_data):
    url = "https://yokohama-atg.zendesk.com/api/v2/users/create_many"
    username = "sreevidya@godigitalcx.com"
    password = "4WKO4l4mWhhlSvLkGByJyJ1zu0fmLlnn6Gm3q6gZ"
    auth_string = f"{username}/token:{password}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
    payload = json.dumps(ticket_data)
    print("payyyyyyyyy",payload)
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Basic {encoded_auth}'
    }
    response = requests.post(url, data=payload, headers=headers)
    return response

def process_database_records_in_chunks(chunk_size=100):
    total_records = UserData.objects.count()  # Count total records in the database
    for start_idx in range(0, total_records, chunk_size):
        end_idx = min(start_idx + chunk_size, total_records)
        records = UserData.objects.all()[start_idx:end_idx]
        print("rrrrrrr",records)
        ticket_data = {"users": []}
        
        for record in records:
            user_fields = {
                "country": str(record.country),
                "address": str(record.address),
                "distributor_number": record.customer
            }
            
            # Add region to user_fields if it's not NaN
            if record.region and record.region.lower() != 'nan':
                user_fields["region"] = str(record.region)

             # Add email only if it's not NaN
            if record.email and str(record.email).lower() != 'nan':
                ticket_data["users"].append({
                    "email": str(record.email),
                    "name": str(record.name),
                    "user_fields": user_fields
                })

            else:
                ticket_data["users"].append({
                    "name": str(record.name),
                    "user_fields": user_fields
                })


        response = customer_add_api(ticket_data)
        
        # Handle response
        if response.status_code == 200:
            job_status = response.json().get('job_status', {})
            job_type = job_status.get('job_type')
            url = job_status.get('url')
            print("url====",url)
            status = job_status.get('status')

            # Save response to the database or log it as required
            UserResponse.objects.create(
                job_type=job_type,
                url=url,
                status=status,
                complete_json=job_status
            )

            print(f"Processed {len(records)} records. Response: {response.status_code}")
        else:
            print(f"Error processing records. Status code: {response.status_code}")

class ShowUser(APIView):
    def get(self, request, *args, **kwargs):

        url = "https://yokohama-atg.zendesk.com/api/v2/users"
        username = "sreevidya@godigitalcx.com"
        password = "4WKO4l4mWhhlSvLkGByJyJ1zu0fmLlnn6Gm3q6gZ"
        auth_string = f"{username}/token:{password}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
        headers = {
            "Content-Type": "application/json",
            'Authorization': f'Basic {encoded_auth}'
        }
        all_users = []
        user_ids = []
        customer_numbers = []

        # Fetch data from all pages
        while url:
            response = requests.get(url, headers=headers)
            data = response.json()
            all_users.extend(data['users'])
            url = data.get('next_page')  # Use .get() to avoid KeyError if 'next_page' doesn't exist
            for user in data['users']:
                customer_number = user['user_fields']['distributor_number']
                user_id = user['id']
                user_ids.append(user_id)
                customer_numbers.append(customer_number)

        # Save user_ids and customer_numbers in UserMapping table
        for user_id, customer_number in zip(user_ids, customer_numbers):
            UserMapping.objects.create(user_ids=user_id, customer_number=customer_number)

        return Response({"users": all_users})



def save_csv_data(request):
    try:
        file_path = "/home/oem/Downloads/mapsize.ods"
        df = pd.read_excel(file_path)
        print("DataFrame:", df)
        for index, row in df.iterrows():
            print("----",row)
            ExcelSize.objects.create(
                map_value=row['Mapvalue'],  # Access row data using string index
                size_value=row['excelsize'],
            )

        return HttpResponse("save csv data successfully")
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        return HttpResponse(str(e), "false")  # Import failed, returning error message
