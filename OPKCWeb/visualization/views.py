# visualization/views.py

from django.shortcuts import render
from django.http import HttpResponse
import os
import pandas as pd
import json


# Define the absolute path to the base directory of the Django project (OPKCWeb)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construct the full path to the CSV data file
DATA_FILE_PATH = os.path.join(BASE_DIR, 'visualization', 'data', 'combined_cleaned_data.csv')

# Define the view for the home page
def home_view(request):
    """
    Renders the simple home page template.
    """
    return render(request, 'visualization/home.html', {})

def chart_view(request):
    """
    Renders the INTERACTIVE dashboard page.
    This view now passes ALL data to the template for client-side filtering.
    """
    try:
        # 1. Read the CSV file
        df = pd.read_csv(DATA_FILE_PATH, na_values=['<NA>'])

        # --- 2. Get Unique IDs for Filters ---
        study_ids = df['StudyID'].dropna().unique().tolist()
        study_ids.sort()
        
        # --- NEW: Get Unique Sample Types for Filters ---
        sample_types = df['SampleType'].dropna().unique().tolist()
        sample_types.sort()

        # --- 3. Prepare ALL Data for JS ---
        # --- UPDATED: Added 'SampleType' to the columns ---
        plot_columns = ['StudyID', 'SampleType', 'TimeDays', 'Log10VL']
        
        # Drop rows where all relevant columns are missing
        df_plot = df[plot_columns].dropna(subset=plot_columns, how='all')

        # --- FIX: Replace pandas NaN with None for valid JSON ---
        # This prevents the "NaN" error during JSON.parse() in the browser
        df_plot = df_plot.where(pd.notnull(df_plot), None)
        
        # Convert the plotting data to a list of dictionaries
        all_data_list = df_plot.to_dict(orient='records')
        
        context = {
            'chart_title': 'Sample Data Dashboard',
            
            # --- We pass data as JSON strings to avoid template errors ---
            
            # Data for Study filters
            'study_ids_json': json.dumps(study_ids),
            
            # --- NEW: Data for SampleType filters ---
            'sample_types_json': json.dumps(sample_types),
            
            # All data for plots
            'all_data_json': json.dumps(all_data_list),
        }

        return render(request, 'visualization/data_chart.html', context)
        
    except FileNotFoundError:
        return HttpResponse(f"Error: Data file not found at: {DATA_FILE_PATH}", status=500)
        
    except Exception as e:
        return HttpResponse(f"An error occurred during data processing: {e}", status=500)