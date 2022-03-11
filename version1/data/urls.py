from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name="data"

urlpatterns = [
    path('data/', views.map_marker_test, name="data"),
    
]