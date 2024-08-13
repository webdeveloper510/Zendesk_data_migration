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


##### Create ticket with attachment in bulk #######
def Create_ticket_with_attachment(request):
    return process_csv_in_chunks('myapp/files/files_list.csv', chunk_size=10)

ZENDESK_API_URL = f"https://.zendesk.com/api/v2/tickets/create_many"

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
        # auth=(ZENDESK_API_USERNAME,ZENDESK_API_PASSWORD),
        headers=headers,
        data=payload
    )
    return response

def upload_file(file_path):
    with open(file_path, 'rb') as f:
        url = f'https://.zendesk.com/api/v2/uploads.json'
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
    



################## Get tickets ######################



class ShowTicket(APIView):
    def get(self,request, *args, **kwargs):
        url = f"https://.zendesk.com/api/v2/tickets"
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
            # auth=(ZENDESK_API_USERNAME,ZENDESK_API_PASSWORD),
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
    


    import csv
import pandas as pd

def get_tire_brands(request):

    df = pd.read_csv("size.csv")
    print("df",df)

    for index, row in df.iterrows():
        id_value = str(row['ID']).strip()
        if id_value.endswith('.'):
            id_value = id_value[:-1]
        url = f"https://yokohama-atg.zendesk.com/api/v2/ticket_fields/22364299286289/options/{id_value}"
        username = "support@godigitalcx.com"
        password = "4WKO4l4mWhhlSvLkGByJyJ1zu0fmLlnn6Gm3q6gZ"
        auth_string = f"{username}/token:{password}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_auth}"
        }
        
        response = requests.delete(url, headers=headers)
        print("respnse",response)
        if response.status_code == 200:
            print(f"Successfully deleted record with ID: {id_value}")
        else:
            print(f"Failed to delete record with ID: {id_value}. Status code: {response.status_code}")


def get_tire_brands():
    ids = {
        'pattern': '22339398247057',
        'brand': '22339240830993',
        'size':'22364299286289',
        'construction_r_b_s':'22306316700433',
        'tt_tl':'21115518082321',
        'l_i_rating':'22339841877137',
        'category':'22339929045777'

    }
    extracted_data = {}
    
    for field, id in ids.items():
        url = f"https://yokohama-atg.zendesk.com/api/v2/ticket_fields/{id}/options"
        username = "support@godigitalcx.com"
        password = "4WKO4l4mWhhlSvLkGByJyJ1zu0fmLlnn6Gm3q6gZ"
        auth_string = f"{username}/token:{password}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_auth}"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            custom_field_options = data.get("custom_field_options", [])
            extracted_data[field] = [{"name": option["name"],"id":option["id"]} for option in custom_field_options]
        else:
            print(f"Failed to fetch data for {field} with id {id}: {response.status_code}")
    return extracted_data


def add_custom_field_options(id, missing_values):
    url = f"https://yokohama-atg.zendesk.com/api/v2/ticket_fields/{id}/options"
    username = "support@godigitalcx.com"
    password = "4WKO4l4mWhhlSvLkGByJyJ1zu0fmLlnn6Gm3q6gZ"
    auth_string = f"{username}/token:{password}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_auth}"
    }
    for value in missing_values:
        if not value:
            print(f"Skipping empty value for field {id}")
            continue
        if id == '22364299286289':
            modified_value = value.replace('.', '_').replace('-', '_').replace('x', '_').replace(' ', '_').replace('(', '_').replace(')', '_').lower() + '_tsize'
        elif id == '22339398247057':
            modified_value = value.replace(' ', '_').replace('-', '_').lower()
        elif id == '22339929045777':
            modified_value = value.replace(' ','_').lower()
        elif id == '21115518082321':
            modified_value = value.replace(' ','').lower()
        
        else:
            modified_value = value
        payload = {"custom_field_option": {"name": value, "value": modified_value}}
        print("payloaddd",payload)
        response = requests.post(url, headers=headers, json=payload)
        print("response",response)
        if response.status_code != 201:
            print(f"Failed to add {value} to field {id}: {response.text}")
        else:
            print(f"Successfully added {value} to field {id}")


def my_cron_job(request):
    tire_brands = get_tire_brands()
    missing_patterns = []
    missing_brands = []
    missing_size = []
    missing_const = []
    missing_type = []
    missing_li_si = []
    missing_category = []
    
    existing_patterns = set(Product_PDM.objects.values_list('pattern', flat=True))
    existing_brands = set(Product_PDM.objects.values_list('brand', flat=True))
    existing_size = set(Product_PDM.objects.values_list('size', flat=True))
    existing_constration = set(Product_PDM.objects.values_list('construction_r_b_s', flat=True))
    existing_type = set(Product_PDM.objects.values_list('tt_tl', flat=True))
    existing_li_si = set(Product_PDM.objects.values_list('l_i_rating', flat=True))
    existing_category = set(Product_PDM.objects.values_list('category', flat=True))


    fetched_patterns = {option['name'] for option in tire_brands.get('pattern', [])}
    fetched_brands = {option['name'] for option in tire_brands.get('brand', [])}
    fetched_size = {option['name'] for option in tire_brands.get('size', [])}
    existing_constration = {option['name'] for option in tire_brands.get('construction_r_b_s', [])}
    fetched_type = {option['name'] for option in tire_brands.get('tt_tl', [])}
    fetched_li_si = {option['name'] for option in tire_brands.get('l_i_rating', [])}
    fetched_category = {option['name'] for option in tire_brands.get('category', [])}


    missing_patterns = list(existing_patterns - fetched_patterns)

    missing_brands = list(existing_brands - fetched_brands)
    missing_size = list(existing_size - fetched_size)
    missing_li_si = list(existing_li_si - fetched_li_si)

    missing_const = list(existing_constration - existing_constration)

    missing_type = list(existing_type - fetched_type)

    missing_category = list(existing_category - fetched_category)


    pattern_field_id = '22339398247057'
    brand_field_id = '22339240830993'
    size_field_id = '22364299286289'
    constration_field_id = '22306316700433'
    tt_tl_field_id = '21115518082321'
    li_si_id = '22339841877137'
    category_id = '22339929045777'
    # Add missing data to Zendesk
    add_custom_field_options(pattern_field_id, missing_patterns)
    add_custom_field_options(brand_field_id, missing_brands)
    add_custom_field_options(size_field_id, missing_size)
    add_custom_field_options(constration_field_id, missing_const)
    add_custom_field_options(li_si_id, missing_li_si)
    add_custom_field_options(tt_tl_field_id, missing_type)
    add_custom_field_options(category_id, missing_category)


    return JsonResponse({"missing_patterns": missing_patterns, "missing_brands": missing_brands,"missing_size":missing_size,"missing_const":missing_const,"missing_type":missing_type,"missing_li_si":missing_li_si,"missing_category":missing_category})


