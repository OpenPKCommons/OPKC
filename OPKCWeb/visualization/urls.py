# visualization/urls.py

from django.urls import path
from . import views

# The variable 'app_name' is used by Django's template tags
app_name = 'visualization' 

urlpatterns = [
    # Path for your home page
    path('', views.home_view, name='index'),

    # Path for your interactive data chart
    path('time_days/', views.chart_view, name='time_days_bar'),
    
    # --- NEW: Paths for your new static pages ---
    path('data_standard/', views.data_standard_view, name='data_standard'),
    path('docs/', views.docs_view, name='docs'),
    path('why_kinetics/', views.why_kinetics_view, name='why_kinetics'),
    path('add_dataset/', views.add_dataset_view, name='add_dataset'),
    path('fit/', views.fit_view, name='fit_pathogen_load'),
    path('download/', views.download_view, name='download_selection'),
]