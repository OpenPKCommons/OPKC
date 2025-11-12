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
        df_plot = df_plot.astype(object).where(pd.notnull(df_plot), None)
        
        # Convert the plotting data to a list of dictionaries
        all_data_list = df_plot.to_dict(orient='records')
        
        # --- FIX: Pass the raw Python objects, NOT JSON strings ---
        context = {
            'chart_title': 'Sample Data Dashboard',
            'study_ids': study_ids,       # No more '_json'
            'sample_types': sample_types, # No more '_json'
            'all_data': all_data_list,  # No more '_json'
        }
        # --- END FIX ---

        return render(request, 'visualization/data_chart.html', context)
        
    except FileNotFoundError:
        return HttpResponse(f"Error: Data file not found at: {DATA_FILE_PATH}", status=500)
        
    except Exception as e:
        return HttpResponse(f"An error occurred during data processing: {e}", status=500)

# --- NEW: Stub views for your new pages ---

def data_standard_view(request):
    """
    Renders the data standard page.
    """
    return render(request, 'visualization/data_standard.html', {})

def docs_view(request):
    """
    Renders the docs page.
    """
    return render(request, 'visualization/docs.html', {})

def why_kinetics_view(request):
    """
    Renders the 'Why Kinetics' page.
    """
    return render(request, 'visualization/why_kinetics.html', {})

def add_dataset_view(request):
    """
    Renders the 'Add Dataset' page.
    """
    return render(request, 'visualization/add_dataset.html', {})