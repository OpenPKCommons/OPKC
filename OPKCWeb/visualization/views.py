# visualization/views.py

from django.shortcuts import render
from django.http import HttpResponse
import os
import pandas as pd
import json
import random # <-- 1. IMPORT THE RANDOM MODULE

# Define the absolute path to the base directory of the Django project (OPKCWeb)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construct the full path to the CSV data file
DATA_FILE_PATH = os.path.join(BASE_DIR, 'visualization', 'data', 'combined_cleaned_data.csv')

# --- 2. DEFINE YOUR FEATURED PAPERS ---
# Add as many papers as you like to this list.
# Make sure the 'image_name' matches a file in:
# visualization/static/visualization/images/
FEATURED_PAPERS_LIST = [
    {
        'title': 'Daily longitudinal sampling of SARS-CoV-2 infection reveals substantial heterogeneity in infectiousness',
        'image_name': 'ke2022.png',
        'url': 'https://doi.org/10.1038/s41564-022-01105-z'
    },
    {
        'title': 'Combined analyses of within-host SARS-CoV-2 viral kinetics and information on past exposures to the virus in a human cohort identifies intrinsic differences of Omicron and Delta variants',
        'image_name': 'russell2024.png',
        'url': 'https://doi.org/10.1371/journal.pbio.3002463'
    },
    {
        'title': 'Viral kinetics of sequential SARS-CoV-2 infections',
        'image_name': 'kissler2023.png',
        'url': 'https://doi.org/10.1038/s41467-023-41941-z'
    },
    {
        'title': 'Mucosal and systemic immune correlates of viral control after SARS-CoV-2 infection challenge in seronegative adults',
        'image_name': 'wagstaffe2024.png',
        'url': 'https://doi.org/10.1126/sciimmunol.adj9285'
    },
    {
        'title': 'Viral kinetics of H5N1 infections in dairy cattle',
        'image_name': 'eales2025.png',
        'url': 'https://doi.org/10.1101/2025.02.01.636082'
    },
    # Add another paper screenshot here
    # {
    #     'title': 'Another Great Paper Title',
    #     'image_name': 'another_paper.jpg',
    #     'url': 'https://doi.org/...'
    # },
]


# Define the view for the home page
def home_view(request):
    """
    Renders the simple home page template.
    This view now also calculates stats and selects a random featured paper.
    """
    context = {}
    try:
        # --- "At a Glance" Stats ---
        df = pd.read_csv(DATA_FILE_PATH, na_values=['<NA>'])
        
        # Use new column names
        total_data_points = df['PathogenLoad'].dropna().count()
        total_studies = df['StudyID'].nunique()
        total_pathogens = df['Pathogen'].nunique()

        context['total_data_points'] = f"{total_data_points:,}"
        context['total_studies'] = f"{total_studies:,}"
        context['total_pathogens'] = f"{total_pathogens:,}"
        
    except Exception as e:
        print(f"Error in home_view while reading CSV: {e}")
        context['total_data_points'] = "N/A"
        context['total_studies'] = "N/A"
        context['total_pathogens'] = "N/A"

    # --- 3. "Featured Paper" Logic ---
    try:
        # Select one paper at random from the list
        selected_paper = random.choice(FEATURED_PAPERS_LIST)
        context['featured_paper'] = selected_paper
    except Exception as e:
        print(f"Error selecting featured paper: {e}")
        context['featured_paper'] = None # Handle error gracefully

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
        
        # Use new 'SampleSource' column
        sample_types = df['SampleSource'].dropna().unique().tolist()
        sample_types.sort()

        # --- 3. Prepare ALL Data for JS ---
        # Use new column names
        plot_columns = ['StudyID', 'SampleSource', 'TimeDays', 'PathogenLoad', 'AgeRng1', 'AgeRng2']
        core_plot_cols = ['StudyID', 'SampleSource', 'TimeDays', 'PathogenLoad']
        df_plot = df[plot_columns].dropna(subset=core_plot_cols, how='any')

        # ROBUST FIX for NaN
        df_plot = df_plot.astype(object).where(pd.notnull(df_plot), None)
        
        all_data_list = df_plot.to_dict(orient='records')
        
        context = {
            'chart_title': 'Sample Data Dashboard',
            'study_ids': study_ids,
            'sample_types': sample_types, # This key is used by the JS
            'all_data': all_data_list,
        }

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