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
    