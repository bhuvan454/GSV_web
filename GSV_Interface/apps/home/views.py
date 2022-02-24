# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from csv import reader
from gettext import install
from http.client import PROXY_AUTHENTICATION_REQUIRED
from pdb import lasti2lineno
from urllib import request
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect

# project imports
import os
import glob 
import requests
import urllib.parse
from .forms import PostForm
import numpy as np
import pandas as pd

import streetview
# try: 
#     import streetview
# except:
#     pip install git+https://github.com/robolyst/streetview

import requests
import json
    

import warnings
warnings.filterwarnings('ignore')
#####################string to tuple
import ast

def convert(d):
    return ast.literal_eval(d)




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

# def index(request):
#     return render(request,'home/page-403.html',{})

def index(request):
    lat, lng = None, None
    api_key = GOOGLE_API_KEY
    if request.GET.get('address'):
          address = request.GET.get('address')
          print('address========',address)
          #test address = 8122 ChestnutKansas City,MO,64132
          base_url = "https://maps.googleapis.com/maps/api/geocode/json"
          endpoint = f"{base_url}?address='8122 Chestnut Kansas City,MO,64132'&key={api_key}"
          print("endpoint is ------------",endpoint)
    # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key 
          r = requests.get(endpoint)
          if r.status_code not in range(200, 299):
               return None, None
          if r.json()['status'] == 'OK':
              print('yess 888888888888888888888888888888888888888888888888888888888888888888888888888888888')
          
          try:
              results = r.json()['results'][0]
              lat = results['geometry']['location']['lat']
              lng = results['geometry']['location']['lng']
              print(lat,lng, '*'*20)
              my_gvs = streetview.panoids(lat,lng)
              print(my_gvs, '*'*50)
              final_dict = {} 

                #### parameters
              size = '640x640'
              fov= '35'
              pitch='5'
              heading = 90
              orient_list = [heading, heading - 15, heading +15]

              final_dict = {}
              years_found = []

              for image in my_gvs:
                if 'year' in image:
                    years_found.append(image['year'])

                    print("image ids .........................3333333333",image)
            
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
                print('Image url ...................################',final_images)
                return render(request, "home/index.html", {'final_data':final_images})

          except:
              pass
    return render(request, "home/index.html", {'final_data':{}})
    
  

            









