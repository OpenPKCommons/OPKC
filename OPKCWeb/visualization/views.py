# visualization/views.py

from django.shortcuts import render
from django.http import HttpResponse
import os
import pandas as pd
from io import StringIO # Used to read the CSV content string as a file

# Define the absolute path to the base directory of the Django project (OPKCWeb)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construct the full path to the CSV data file
# This assumes your file is in 'visualization/data/test_import.csv' relative to the project root.
DATA_FILE_PATH = os.path.join(BASE_DIR, 'visualization', 'data', 'combined_cleaned_data.csv')

# Define the view for the home page
def home_view(request):
    """
    Renders the simple home page template.
    """
    return render(request, 'visualization/home.html', {}) # Note the new template name

def chart_view(request):
    """
    Renders the bar chart for time days distribution.
    """
    try:
        # 1. Read the CSV file directly from the file path
        df = pd.read_csv(DATA_FILE_PATH, na_values=['<NA>'])

        # 2. (Rest of your existing data processing logic)
        # ... your filtering, grouping, counting, etc. goes here ...
        
        df_clean = df.dropna(subset=['TimeDays']).copy()
        
        frequency_series = df_clean['TimeDays'].value_counts().sort_index()
        labels = frequency_series.index.tolist()
        data = frequency_series.tolist()
        
        # ... (rest of the view function) ...

        context = {
            'chart_title': 'Count of Samples by Time Day',
            'chart_labels': labels,
            'chart_data': data,
        }

        return render(request, 'visualization/data_chart.html', context)
        
    except FileNotFoundError:
        # Handle the case where the data file cannot be found
        return render(request, 'visualization/error.html', {'message': f"Data file not found at: {DATA_FILE_PATH}"})
        
    except Exception as e:
        # Handle other potential errors during processing
        return render(request, 'visualization/error.html', {'message': f"An error occurred during data processing: {e}"})
