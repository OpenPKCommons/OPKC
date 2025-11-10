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
        
        sample_types = df['SampleType'].dropna().unique().tolist()
        sample_types.sort()

        # --- 3. Prepare ALL Data for JS ---
        plot_columns = ['StudyID', 'SampleType', 'TimeDays', 'Log10VL', 'AgeRng1', 'AgeRng2']
        
        # We need the core plot columns to be present.
        core_plot_cols = ['StudyID', 'SampleType', 'TimeDays', 'Log10VL']
        df_plot = df[plot_columns].dropna(subset=core_plot_cols, how='any')

        # --- ROBUST FIX for NaN: ---
        # 1. Convert DataFrame to 'object' type. This allows 'None' to be stored.
        # 2. Replace all remaining 'NaN' (and 'NaT') with Python's 'None'.
        # 3. 'json.dumps()' will then correctly serialize 'None' to 'null'.
        df_plot = df_plot.astype(object).where(pd.notnull(df_plot), None)
        
        # Convert the plotting data to a list of dictionaries
        all_data_list = df_plot.to_dict(orient='records')
        
        context = {
            'chart_title': 'Sample Data Dashboard',
            'study_ids_json': json.dumps(study_ids),
            'sample_types_json': json.dumps(sample_types),
            'all_data_json': json.dumps(all_data_list),
        }

        return render(request, 'visualization/data_chart.html', context)
        
    except FileNotFoundError:
        return HttpResponse(f"Error: Data file not found at: {DATA_FILE_PATH}", status=500)
        
    except Exception as e:
        return HttpResponse(f"An error occurred during data processing: {e}", status=500)