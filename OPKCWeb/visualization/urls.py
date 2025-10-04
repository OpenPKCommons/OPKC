# visualization/urls.py  <-- THIS IS THE NEW FILE

from django.urls import path
from . import views

# The variable 'app_name' is used by Django's template tags (e.g., {% url 'visualization:time_days_bar' %})
app_name = 'visualization' 

urlpatterns = [
    # Path for your first chart view
    path('time_days/', views.chart_view, name='time_days_bar'),
    
    # If you later add a second chart view called 'viral_load_line_chart'
    # path('viral_load/', views.viral_load_line_chart, name='viral_load_line'),
]