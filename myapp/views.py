from django.shortcuts import render
from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from django.db.models import Case, When, Value
import json
import pandas as pd
import time
import csv
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from base64 import b64encode
import base64
import numpy as np
import re   
# Create your views here.



######## Save customer in excel file in database ########

def save_customer_ticket_excel(request):
    try:
        file_path = "/home/codenomad/Downloads/Data for Migration from 1st Jan-24 to 31st Jul-24 - Final.xlsx"
        # Specify dtype for multiple columns
        df = pd.read_excel(file_path, dtype={'OUR RECOMMENDATION': str, 'REMAINING TREAD DEPTH (%)': str})
    
        for index, row in df.iterrows():
            legacy_claim_no = "legacy_" + str(row['CLAIM NO'])
            unique_data_id = "uid_" + str(row['Unique ID'])
            claim_no_with_migration = "data_migration" + ", " + legacy_claim_no + ", " + unique_data_id
            print("dddddddd", row['Customer code'])

          
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
                plant=row['PLANT'],
                claim_no=claim_no_with_migration,
                date_of_invoice=row['DATE OF INVOICE/ SALE/ MOUNTING'],
                invoice_details=row['Invoice details'],
                remaining_tread_depth=row['REMAINING TREAD DEPTH (%)'],
                defect_code_description=row['Defect Code Description'],
                our_recommendation=row['OUR RECOMMENDATION'],
                remarks=row['REMARKS'],
                disposed_by=row['DISPOSED BY'],
                customer_code=row['Customer code'],
                # map_li_si_pr=row['map_li_si_pr'],
                customer_name=row['CUSTOMER NAME'],
                country_working=row['Country-working'],
                region=row['Region'],
            )

        return HttpResponse("save excel data successfully")
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        return HttpResponse(f"Error importing data: {str(e)}", status=500)


    


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
    username = "support@godigitalcx.com"
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
class AddUserCustomerCode(APIView):
    def get(self, request, *args, **kwargs):

        url = "https://yokohama-atg.zendesk.com/api/v2/users"
        username = "support@godigitalcx.com"
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
def save_mapping_data(request):
    try:
        file_path = "/home/codenomad/Downloads/backup-download/mapdesign.ods"
        df = pd.read_excel(file_path)
        print("DataFrame:", df)
        for index, row in df.iterrows():
            print("----",row)
            DesignLISIMAP.objects.create(
                mapdesign=row['mapdesign'],
                excel_design=row['Design'],
                # map_value=row['Mapvalue'],
                # size_value=row['excelsize'],
                # map_li_si_pr=row['map_li_si_pr'],
                # excel_li_si=row['LI /SI /PR'],
                # map_defect_code=row['Map defect code'],
                # excel_defect_code=row['Defect Code Description'],


            )

        return HttpResponse("save csv data successfully")
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        return HttpResponse(str(e), "false")



############# Set requster_id in db ################
def requester_id(request):
    user_mapping_numbers = UserMapping.objects.values_list('customer_number', flat=True)
    customer_ticket_codes = CustomerTicket.objects.values_list('customer_code', flat=True)
    
    # Check if customer_ticket_codes is empty
    for customer_number in user_mapping_numbers:

        if customer_number in customer_ticket_codes:
            if customer_number:
                user_ids = UserMapping.objects.filter(customer_number=customer_number).values_list('user_ids', flat=True)
            
                if user_ids:
                    # Assuming you want to pick the first user_id for the update
                    # first_user_id = user_ids[0]
                    CustomerTicket.objects.filter(customer_code=customer_number).update(requester_id=user_ids)
            # if not customer_ticket_codes:
            #     # Update all requester_id to null if customer_ticket_codes is empty
            #     CustomerTicket.objects.all().update(requester_id=None)
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
        if data in customer_size:
            design_ids = DesignLISIMAP.objects.filter(excel_design=data).values_list('mapdesign', flat=True)
            if design_ids:
                CustomerTicket.objects.filter(design=data).update(map_design=design_ids[0])

    return JsonResponse({"message": "done"})


########## Replace excel sheet li_si_pr  ################# 

def LI_SImapping(request):
    mappings = LI_SI_PRMAP.objects.values('excel_li_si', 'map_li_si_pr')

    # Create a list of conditions for Case-When
    conditions = [
        When(li_si_pr=mapping['excel_li_si'], then=Value(mapping['map_li_si_pr']))
        for mapping in mappings
    ]

    if conditions:
        CustomerTicket.objects.update(
            map_li_si_pr=Case(
                *conditions,
                default=Value(None),
            )
        )

    return JsonResponse({"message": "done"})



########## Replace excel sheet defect code ################# 
def defect_code_mapping(request):
    size_mapping = Defect_code.objects.values('excel_defect_code', 'map_defect_code')


    conditions = [
        When(defect_code_description=mapping['excel_defect_code'], then=Value(mapping['map_defect_code']))
        for mapping in size_mapping
    ]

    if conditions:
        CustomerTicket.objects.update(
            map_defect_code=Case(
                *conditions,
                default=Value(None),
            )
        )

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
    username = "support@godigitalcx.com"
    password = "4WKO4l4mWhhlSvLkGByJyJ1zu0fmLlnn6Gm3q6gZ"
    auth_string = f"{username}/token:{password}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode('utf-8')
    payload = json.dumps({"tickets": ticket_data})
    # print("payloadddddd",payload)
    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Basic {encoded_auth}'
    }
    response = requests.post(url, data=payload, headers=headers)
    print("rrrrr",response)

    return response

"""For get records in database"""
def process_database_records_in_chunks(chunk_size=100):
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
                    # "requester_id": str(record.requester_id),
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
            if record.requester_id is not None:
                ticket_data["requester_id"] = str(record.requester_id)
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
    username = "support@godigitalcx.com"
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
    
    # Create a CSV file with ticket_ids and claim columns
    with open('tickets.csv', 'w', newline='') as csvfile:
        fieldnames = ['ticket_ids', 'claim']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for t_id, cl in zip(ticket_ids, claim):
            writer.writerow({'ticket_ids': t_id, 'claim': cl})

    return JsonResponse({"msg": "done"})


