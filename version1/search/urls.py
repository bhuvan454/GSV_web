from django.urls import include, path
from django.views.generic import TemplateView

from . import views

app_name="search"

urlpatterns = [
    path('', views.index, name="homepage"),
    path('search/',views.search, name = 'search'),
    path('aboutus/', views.aboutus, name="aboutus"),
]