from django.db import models
from django.utils.translation import gettext as _ 
# Create your models here.
class Address_data(models.Model):

    property_class = models.CharField(_('property_class'),max_length= 50)	
    property_status	= models.CharField(_('property_status'),max_length= 50)
    address   = models.CharField(_('address'),max_length= 255)
    neighborhood = models.CharField(_('neighborhood'),max_length= 50)
    location = models.CharField(_('neighborhood'),max_length= 150)
    latitude_pinpoint = models.FloatField(_('latitude_pinpoint'))
    longitude_pinpoint	= models.FloatField(_('longitude_pinpoint'))
    year_of_acquisition = models.IntegerField(_('year_of_acquisition'))
    latitude_street	= models.FloatField(_('latitude_street'))
    longitude_street = models.FloatField(_('longitude_street'))
    frontview_heading = models.IntegerField(_('frontview_heading'))
    panoids_years = models.CharField(_('panoids_years'),max_length= 500)

    
