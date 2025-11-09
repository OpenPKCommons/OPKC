# visualization/views.py

from django.shortcuts import render
from django.http import HttpResponse
import os
import pandas as pd
import json # <-- 1. IMPORT json

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
    Renders the bar chart for time days distribution
    AND the new scatter plot.
    """
    try:
        # 1. Read the CSV file
        df = pd.read_csv(DATA_FILE_PATH, na_values=['<NA>'])

        # --- 2. Data for Bar Chart (Existing) ---
        df_clean_bar = df.dropna(subset=['TimeDays']).copy()
        frequency_series = df_clean_bar['TimeDays'].value_counts().sort_index()
        labels = frequency_series.index.tolist()
        data = frequency_series.tolist()
        
        context = {
            'chart_title': 'Count of samples by day',
            # --- 2. FIXED: Data must be passed as a JSON string ---
            'chart_labels': json.dumps(labels),
            'chart_data': json.dumps(data),
        }

        # --- 3. Data for Scatter Plot (NEW) ---
        df_clean_scatter = df.dropna(subset=['TimeDays', 'Log10VL']).copy()
        
        scatter_data = {
            'x': df_clean_scatter['TimeDays'].tolist(),
            'y': df_clean_scatter['Log10VL'].tolist()
        }
        
        # Add the new scatter data to the context
        context['scatter_data_json'] = json.dumps(scatter_data)

        return render(request, 'visualization/data_chart.html', context)
        
    except FileNotFoundError:
        # Handle the case where the data file cannot be found
        return HttpResponse(f"Error: Data file not found at: {DATA_FILE_PATH}", status=500)
        
    except Exception as e:
        # Handle other potential errors during processing
        return HttpResponse(f"An error occurred during data processing: {e}", status=500)