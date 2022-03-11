# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from http.client import PROXY_AUTHENTICATION_REQUIRED
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
import requests
import streetview
from django.shortcuts import render
from data.models import Address_data
from json import dumps

def index(request):
    locations_data = map_data()
    return render(request,'index.html',
    {'locations_data': locations_data})


def aboutus(request):
    return render(request, "aboutus.html", {}) 


def map_data():
    data = Address_data.objects.all().values()
    locations = []
    for address_data in data:
        temp_location = {
            'address':address_data['address'],
            'lat_pin':address_data['latitude_pinpoint'],
            'long_pin':address_data['longitude_pinpoint'],
        }
        locations.append(temp_location)

    return dumps(locations)





############################## image with streetview ##############################################

GOOGLE_API_KEY = 'AIzaSyAzu_20p_S5xKYBAl0aeTjZG_NsI5JKmY4' 
        
api_key = GOOGLE_API_KEY
verbose = False
base_streetview = 'https://maps.googleapis.com/maps/api/streetview?'
base_metadata = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
        
def get_metadata(pano_id):
    _meta_params = dict(key = api_key, pano = pano_id)
    _meta_response = requests.get(base_metadata,params =_meta_params)
    meta_info = _meta_response.json()
    meta_status = meta_info["status"]
    return meta_info,meta_status

def get_image(pano_id,heading,size = '640x640'
                  ,fov ='90',pitch ='0', radius = '20'):

    # initial check for the data
    _ , meta_status = get_metadata(pano_id)
    if meta_status  =='OK':
        image_url = f"{base_streetview}size={size}&pano={pano_id}&fov={fov}&heading={heading}&pitch={pitch}&sourc='outside'&key={api_key}"
        return image_url


####################### Address to Lat,Log fetching #############################


def search(request):
    lat, lng = None, None
    api_key = GOOGLE_API_KEY
    if request.GET.get('address'):
          address = request.GET.get('address')

          #test address = 8122 ChestnutKansas City,MO,64132 --- test case
          base_url = "https://maps.googleapis.com/maps/api/geocode/json"
          endpoint = f"{base_url}?address={address}&key={api_key}"

          print("endpoint is ------------",endpoint)  ## test print

    
          r = requests.get(endpoint)
          if r.status_code not in range(200, 299):
               return None, None
          if r.json()['status'] == 'OK':
              print('yes')
          
          try:
              results = r.json()['results'][0]
              lat = results['geometry']['location']['lat']
              lng = results['geometry']['location']['lng']


            #   print(lat,lng, '*'*20)  ############ check for lat and longitudes


              my_gvs = streetview.panoids(lat, lng)

            #   print(my_gvs, '*'*50)  ############ printing google street view ids 

              final_dict = {} 

                #### parameters
              size = '640x640'
              fov= '35'
              pitch='5'
              heading = 90         ##### we should change this setting
              orient_list = [heading, heading - 15, heading +15]

              final_dict = {}
              years_found = []

              for image in my_gvs:
                if 'year' in image:
                    years_found.append(image['year'])
            
                    ### creating the year list 
                    year_list = []
                    for orient in orient_list:
                        
                        img_url = get_image(pano_id= image['panoid'],size= size,
                                        heading = orient, fov = fov, radius='25', pitch ='5')
                        params = dict(heading = orient, img_url = img_url)

                        year_list.append(params)

                
                    # img_url = get_image(pano_id,heading,size = '640x640'
                    #       ,fov ='90',pitch ='0', radius = '20')
                    final_dict[image['year']] = year_list
                
                years_found.sort()
                user_year = 90000000 # dummy val
                try:
                    if user_year in years_found: 
                        final_images = final_dict[user_year]
                    else: 
                        final_images = final_dict[years_found[0]]
                except:
                    pass
        
                locationData = {}
                locationData['latitude'] = lat
                locationData['longitude'] = lng
                print("years found----------------",years_found)
                
                
                return render(request, "home.html", {'final_data':final_images,'locationData':locationData,'availableYears':years_found})

          except:
              pass
   
    return render(request, "home.html", {'final_data':{}})







