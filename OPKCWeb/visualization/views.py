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
    This view now also calculates stats for the "At a Glance" section.
    """
    context = {}
    try:
        # Read the CSV file to calculate stats
        df = pd.read_csv(DATA_FILE_PATH, na_values=['<NA>'])
        
        # Calculate stats
        # We define "data points" as rows with a valid Log10VL
        total_data_points = df['Log10VL'].dropna().count()
        total_studies = df['StudyID'].nunique()
        total_pathogens = df['Pathogen'].nunique() # Assumes you have a 'Pathogen' column

        # Format numbers with commas
        context['total_data_points'] = f"{total_data_points:,}"
        context['total_studies'] = f"{total_studies:,}"
        context['total_pathogens'] = f"{total_pathogens:,}"
        
    except Exception as e:
        print(f"Error in home_view while reading CSV: {e}")
        # Provide fallback values
        context['total_data_points'] = "N/A"
        context['total_studies'] = "N/A"
        context['total_pathogens'] = "N/A"

    return render(request, 'visualization/home.html', context)

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


# --- STUB VIEWS for other pages ---

def data_standard_view(request):
    return render(request, 'visualization/data_standard.html', {})

def docs_view(request):
    return render(request, 'visualization/docs.html', {})

def why_kinetics_view(request):
    return render(request, 'visualization/why_kinetics.html', {})

def add_dataset_view(request):
    return render(request, 'visualization/add_dataset.html', {})