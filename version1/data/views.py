from django.shortcuts import render
from .models import Address_data
from django.core import serializers
from json import dumps

def test_data(request):
    data = Address_data.objects.all()[:5].values()

    print('*'*20)
    print(data[0])
    print('/'*20)
    print(data[0]['address'])

    lat_pinpoint = []
    long_pinpoint = []
    lat_street = []
    long_street = []
    address_list = []
    heading_list = []

    for address_data in data:
        lat_pinpoint.append(address_data['latitude_pinpoint'])
        long_pinpoint.append(address_data['longitude_pinpoint'])
        lat_street.append(address_data['latitude_street'])
        long_street.append(address_data['longitude_street'])
        heading_list.append(address_data['frontview_heading'])
        address_list.append(address_data['address'])
    
    pinpoint = zip(lat_pinpoint,long_pinpoint)
    street = zip(lat_street,long_street)
    return render(request,'test.html',
    {'pinpoint':pinpoint,
     'street':street,
     'heading_list':heading_list,
     'address_list':address_list})


# def map_marker_test(request):
#     return render(request, 'map_test.html',{})


def map_marker_test(request):
    data = Address_data.objects.all().values()
    locations = []

    for address_data in data:
        temp_location = {
            'address':address_data['address'],
            'lat_pin':address_data['latitude_pinpoint'],
            'long_pin':address_data['longitude_pinpoint'],
            'lat_street':address_data['latitude_street'],
            'long_street':address_data['longitude_street'],
            'heading':address_data['frontview_heading'],    
        }
        locations.append(temp_location)

    # for address_data in data:
    #     temp_location = [
    #         address_data['address'],
    #         address_data['latitude_pinpoint'],
    #         address_data['longitude_pinpoint'],
    #         address_data['latitude_street'],
    #         address_data['longitude_street'],
    #         address_data['frontview_heading'],    
    #     ]
    #     locations.append(temp_location)


    return render(request,'map_test.html',
    {'locations_data':dumps(locations)})

