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





######## Save customer in excel file in database ########

def save_customer_ticket_excel(request):
    try:
        file_path = "/home/oem/Downloads/testyoko.csv"
        # Specify dtype for multiple columns
        df = pd.read_csv(file_path, dtype={'OUR RECOMMENDATION': str, 'REMAINING TREAD DEPTH (%)': str})
    
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




def deleteuser(request):
    da = Tickets.objects.all().delete()
    return JsonResponse({"msg":da})



#### save customer excel to db ########

def save_customer_data(request):
    try:
        file_path = "myapp/customer_files/Test-new-latest-user.xlsx"
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
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
        return HttpResponse("false")
    

################################## Yokohama api using database maping ############################## 


########## User add in yokohama account ################
class Addcustomer(APIView):
    def post(self, request, *args, **kwargs):
        try:
            process_database_records_in_chunks()
            return JsonResponse({"message": "Processing complete"})
        except Exception as e:
            return JsonResponse({"error": str(e)})

"""For add customer in zendesk"""
def customer_add_api(user_data):
    url = "https://yokohama-atg.zendesk.com/api/v2/imports/tickets/create_many"
    username = "sreevidya@godigitalcx.com"
    password = "4WKO4l4mWhhlSvLkGByJyJ1zu0fmLlnn6Gm3q6gZ"
    auth_string = f"{username}/token:{password}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
    payload = json.dumps(user_data)
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Basic {encoded_auth}'
    }
    response = requests.post(url, data=payload, headers=headers)
    return response

"""For get users record in db"""
def process_database_records_in_chunks(chunk_size=100):
    total_records = UserData.objects.count()
    for start_idx in range(0, total_records, chunk_size):
        end_idx = min(start_idx + chunk_size, total_records)
        records = UserData.objects.all()[start_idx:end_idx]
        user_data = {"users": []}
        
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
                user_data["users"].append({
                    "email": str(record.email),
                    "name": str(record.name),
                    "user_fields": user_fields
                })

            else:
                user_data["users"].append({
                    "name": str(record.name),
                    "user_fields": user_fields
                })

        response = customer_add_api(user_data)
        
        if response.status_code == 200:
            job_status = response.json().get('job_status', {})
            job_type = job_status.get('job_type')
            url = job_status.get('url')
            status = job_status.get('status')

            # Save response in database
            UserResponse.objects.create(
                job_type=job_type,
                url=url,
                status=status,
                complete_json=job_status
            )

            print(f"Processed {len(records)} records. Response: {response.status_code}")
        else:
            print(f"Error processing records. Status code: {response.status_code}")


########## Get user in zendesk ###########
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
            url = data.get('next_page')
            for user in data['users']:
                customer_number = user['user_fields']['distributor_number']
                user_id = user['id']
                user_ids.append(user_id)
                customer_numbers.append(customer_number)

        # Save user_ids and customer_numbers in UserMapping table
        for user_id, customer_number in zip(user_ids, customer_numbers):
            UserMapping.objects.create(user_ids=user_id, customer_number=customer_number)

        return Response({"users": all_users})


############### For save excel data in db ###############
def save_csv_data(request):
    try:
        file_path = "/home/oem/Downloads/mapdefect_code.ods"
        df = pd.read_excel(file_path)
        print("DataFrame:", df)
        for index, row in df.iterrows():
            print("----",row)
            Defect_code.objects.create(
                # mapdesign=row['mapdesign'],
                # excel_design=row['Design'],
                # map_value=row['Mapvalue'],
                # size_value=row['excelsize'],
                # map_li_si_pr=row['map_li_si_pr'],
                # excel_li_si=row['LI /SI /PR'],
                map_defect_code=row['Map defect code'],
                excel_defect_code=row['Defect Code Description'],


            )

        return HttpResponse("save csv data successfully")
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        return HttpResponse(str(e), "false")

############# Set requster_id in db ################
def requester_id(request):
    user_mapping_numbers = UserMapping.objects.values_list('customer_number', flat=True)
    
    customer_ticket_codes = CustomerTicket.objects.values_list('customer_code', flat=True)
    
    for customer_number in user_mapping_numbers:
        
        if customer_number in customer_ticket_codes:
            user_ids = UserMapping.objects.filter(customer_number=customer_number).values_list('user_ids', flat=True)
            print("User IDs:", list(user_ids))
            
            CustomerTicket.objects.filter(customer_code=customer_number).update(requester_id=user_ids)
    
    return JsonResponse({"message": "done"})


############ Replace tire size mapping #################
def Sizemapping(request):
    size_mapping = ExcelSize.objects.values_list('size_value', flat=True)
    
    customer_size = CustomerTicket.objects.values_list('size', flat=True)
    
    for data in size_mapping:
        
        if data in customer_size:
            size_map = ExcelSize.objects.filter(size_value=data).values_list('map_value', flat=True)
            print("User IDs:", list(size_map))
            
            CustomerTicket.objects.filter(size=data).update(mapsize=size_map)
    
    return JsonResponse({"message": "done"})


########### Replace design mapping #############
def Designmapping(request):
    size_mapping = DesignLISIMAP.objects.values_list('excel_design', flat=True)
    
    customer_size = CustomerTicket.objects.values_list('design', flat=True)
    
    for data in size_mapping:
        # print("------", data)
        if data in customer_size:
            design_ids = DesignLISIMAP.objects.filter(excel_design=data).values_list('mapdesign', flat=True)
            print("Design IDs:", list(design_ids))
            
            CustomerTicket.objects.filter(design=data).update(map_design=design_ids)
    
    return JsonResponse({"message": "done"})


############ Replace excel sheet li_si_pr ################ 
def LI_SImapping(request):
    size_mapping = LI_SI_PRMAP.objects.values_list('excel_li_si', flat=True)
    
    customer_size = CustomerTicket.objects.values_list('li_si_pr', flat=True)
    for data in size_mapping:
        
        if data in customer_size:
            li_si_pr = LI_SI_PRMAP.objects.filter(excel_li_si=data).values_list('map_li_si_pr', flat=True)
            print("Design IDs:", list(li_si_pr))
            
            CustomerTicket.objects.filter(li_si_pr=data).update(map_li_si_pr=li_si_pr)
    
    return JsonResponse({"message": "done"})


########## Replace excel sheet defect code ################# 
def defect_code_mapping(request):
    size_mapping = Defect_code.objects.values_list('excel_defect_code', flat=True)
    
    customer_size = CustomerTicket.objects.values_list('defect_code_description', flat=True)
    for data in size_mapping:
        
        if data in customer_size:
            defect_des = Defect_code.objects.filter(excel_defect_code=data).values_list('map_defect_code', flat=True)
            print("Design IDs:", list(defect_des))
            
            CustomerTicket.objects.filter(defect_code_description=data).update(map_defect_code=defect_des)
    
    return JsonResponse({"message": "done"})


########## Ticket create for Yokohama #############
class AddTicket(APIView):
    def post(self, request, *args, **kwargs):
        try:
            process_database_records_in_chunks()
            return JsonResponse({"message": "Processing complete"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
        
"""For add ticket in zendesk"""
def ticket_add_api(ticket_data):
    url = "https://yokohama-atg.zendesk.com/api/v2/imports/tickets/create_many"
    username = "sreevidya@godigitalcx.com"
    password = "4WKO4l4mWhhlSvLkGByJyJ1zu0fmLlnn6Gm3q6gZ"
    auth_string = f"{username}/token:{password}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
    payload = json.dumps({"tickets": ticket_data})
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Basic {encoded_auth}'
    }
    response = requests.post(url, data=payload, headers=headers)
    print("rrrrr",response)

    return response

"""For get records in database"""
def process_database_records_in_chunks(chunk_size=2):
    total_records = CustomerTicket.objects.count()
    for start_idx in range(0, total_records, chunk_size):
        end_idx = min(start_idx + chunk_size, total_records)
        records = CustomerTicket.objects.all()[start_idx:end_idx]
        ticket_data_list = [] 
        
        for record in records:
            our_recommendation_value = int(record.our_recommendation) if record.our_recommendation.isdigit() else 0
            our_recommendation_value = our_recommendation_value > 0
            ticket_data = {
                        
                    "comment": {
                        "body": record.defect_code_description
                    },
                    "status": 'closed',
                    "subject":str(record.date),
                    "tags": str(record.claim_no),
                    "requester_id": str(record.requester_id),
                    "custom_fields": [
                        {"id": 21115540894737, "value": record.cat_no},
                        {"id": 17459369077521, "value": record.defect_code_description},
                        {"id": 17459369082641, "value": record.disposed_by},
                        {"id": 17459414176657, "value": record.date},
                        {"id": 21115518082321, "value": record.type},
                        {"id": 21115488705297, "value": record.country_working},
                        {"id": 21256551170961, "value": record.customer_name},
                        {"id": 21145491038481, "value": record.no_of_tyre},
                        {"id": 21145754951697, "value": our_recommendation_value},
                        {"id": 22364299286289, "value": record.mapsize},
                        {"id": 21115597806225, "value": record.date_of_invoice},
                        {"id": 22339841877137, "value": record.map_li_si_pr},
                        {"id": 21115726824849, "value": record.map_defect_code},
                        {"id": 22339398247057, "value": record.map_design},
                        {"id": 21558274008721, "value": record.plant},
                        {"id": 21115763616529, "value": record.remaining_tread_depth},
                        {"id": 21115566381201, "value": record.tyre_serial_no},
                        {"id": 22306316700433, "value": record.region},
                        {"id": 23148917093265, "value": record.remarks},
                        {"id": 24218426495889, "value": record.design},
                        {"id": 24429125347857, "value": record.size},

                    ]
                }
            
            # Filter out dictionaries with value "nan" from custom_fields
            ticket_data["custom_fields"] = [
                field for field in ticket_data["custom_fields"] if field.get("value") != "nan"
            ]
            
            ticket_data_list.append(ticket_data)
        
        response = ticket_add_api(ticket_data_list)
        
        if response.status_code == 200:
            job_status = response.json().get('job_status', {})
            job_type = job_status.get('job_type')
            url = job_status.get('url')
            status = job_status.get('status')

           #save zendesk response in db
            UserResponse.objects.create(
                job_type=job_type,
                url=url,
                status=status,
                complete_json=job_status
            )

            print(f"Processed {len(records)} records. Response: {response.status_code}")
        else:
            print(f"Error processing records. Status code: {response.status_code}")


######### For save ticket ids and claim ids in excel sheet ##############
def ShowYokoTicket(request):
    url = "https://yokohama-atg.zendesk.com/api/v2/tickets"
    username = "sreevidya@godigitalcx.com"
    password = "4WKO4l4mWhhlSvLkGByJyJ1zu0fmLlnn6Gm3q6gZ"
    auth_string = f"{username}/token:{password}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Basic {encoded_auth}'
    }
    all_tickets = []
    ticket_ids = []
    claim = []

    while url:
        response = requests.get(url, headers=headers)
        data = response.json()
        all_tickets.extend(data['tickets'])
        url = data.get('next_page')
        
        for ticket in data['tickets']:
            ticket_id = ticket['id']
            tags = ticket['tags']
            legacy_item = [item for item in tags if item.startswith("legacy_")]
            if legacy_item:
                da = legacy_item[0]
                ticket_id = ticket['id']
                ticket_ids.append(ticket_id)

                claim.append(da)
                # Save ticket_id and claim to the database
                # Ticket_ids.objects.create(ticket_ids=ticket_id, claims=da)
            else:
                print("No item with 'legacy_' found.")
      
    return JsonResponse({"msg":"done"})



def fake_user(request):
    try:
        file_path = "myapp/customer_files/fakeuser.csv"
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            print("----",row)
            Fakeuser.objects.create(
                name=row['name'],
                email=row['email'],
            )

        return HttpResponse("save csv data successfully")
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        return HttpResponse(str(e), "false")