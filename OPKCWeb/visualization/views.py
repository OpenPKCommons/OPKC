# visualization/views.py

from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from io import StringIO # Used to read the CSV content string as a file

# --- SIMULATE GETTING YOUR CSV CONTENT STRING ---
# In a real Django project, 'csv_content' would come from reading the file 
# uploaded by the user, likely a request.FILES object or a file field on a Model.
csv_content = """
StudyID,PersonID,InfectionID,SampleID,TimeDays,Symptoms1,Symptoms2,Symptoms3,Symptoms4,Comorbidity1,Comorbidity2,Comorbidity3,Comorbidity4,Treatment1,Treatment2,Treatment3,Treatment4,Hospitalized,SampleType,AgeRng1,AgeRng2,Subtype,Platform,DOI,Log10VL,Units,GEml_conversion_intercept,GEml_conversion_slope
russell2024,1,<NA>,<NA>,-7,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,1,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,25.031553,Ct,,
russell2024,1,<NA>,<NA>,5,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,18.954472,Ct,,
russell2024,2,<NA>,<NA>,-6,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,50,100,Delta,Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,2,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,50,100,Delta,Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,33.373062,Ct,,
russell2024,2,<NA>,<NA>,13,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,50,100,Delta,Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,24.452152,Ct,,
russell2024,3,<NA>,<NA>,-9,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,35,49,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,3,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,35,49,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,20.044334,Ct,,
russell2024,4,<NA>,<NA>,-8,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,35,49,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,4,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,35,49,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,21.669357,Ct,,
russell2024,5,<NA>,<NA>,-1,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,35,49,Delta,Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,5,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,35,49,Delta,Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,32.067066,Ct,,
russell2024,6,<NA>,<NA>,-5,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,6,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,23.21893,Ct,,
russell2024,7,<NA>,<NA>,-10,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,50,100,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,7,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,50,100,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,31.979,Ct,,
russell2024,8,<NA>,<NA>,-9,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,8,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,16.967419,Ct,,
russell2024,9,<NA>,<NA>,-10,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,35,49,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,9,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,35,49,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,18.680416,Ct,,
russell2024,10,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,35,49,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,16.075422,Ct,,
russell2024,11,<NA>,<NA>,-8,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,50,100,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,11,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,50,100,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,20.749935,Ct,,
russell2024,12,<NA>,<NA>,-10,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,12,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,13.9435215,Ct,,
russell2024,13,<NA>,<NA>,-3,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,13,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,22.371183,Ct,,
russell2024,14,<NA>,<NA>,-6,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,14,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,15.8777685,Ct,,
russell2024,15,<NA>,<NA>,-5,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,35,49,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,15,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,35,49,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,27.107,Ct,,
russell2024,16,<NA>,<NA>,-4,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,16,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.2),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,17.984688,Ct,,
russell2024,17,<NA>,<NA>,-6,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,50,100,Delta,Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,17,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,50,100,Delta,Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,27.148026,Ct,,
russell2024,18,<NA>,<NA>,-7,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,50,100,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,18,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,50,100,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,21.5037,Ct,,
russell2024,19,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,35,49,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,16.331406,Ct,,
russell2024,20,<NA>,<NA>,-4,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,50,100,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,20,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,50,100,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,13.529065,Ct,,
russell2024,21,<NA>,<NA>,-7,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,35,49,Delta,Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,21,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,35,49,Delta,Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,22.55272,Ct,,
russell2024,22,<NA>,<NA>,-6,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,22,<NA>,<NA>,0,symptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,21.447681,Ct,,
russell2024,23,<NA>,<NA>,-8,asymptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,40.0,Ct,,
russell2024,23,<NA>,<NA>,0,asymptomatic,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,<NA>,,nasopharyngeal,20,34,Omicron (BA.1),Crick COVID-19 Consortium (CCC) ORF1ab,10.1371/journal.pbio.3002463,15.648612,Ct,,
"""


# Define the view for the home page
def home_view(request):
    """
    Renders the simple home page template.
    """
    return render(request, 'visualization/home.html', {}) # Note the new template name

def chart_view(request):
    # Use StringIO to treat the content string as a file-like object for pandas
    data_io = StringIO(csv_content)
    
    # 1. Read data using pandas
    # na_values=['<NA>'] handles the placeholder for missing data
    # dtype='str' is used initially for 'TimeDays' to prevent pandas from 
    # making automatic (and possibly incorrect) assumptions about mixed types 
    df = pd.read_csv(data_io, na_values=['<NA>'], dtype={'TimeDays': 'str'})
    
    # 2. Convert 'TimeDays' to numeric and clean the data
    # 'errors="coerce"' turns any non-numeric value into NaN
    df['TimeDays'] = pd.to_numeric(df['TimeDays'], errors='coerce')
    
    # Drop rows where TimeDays is NaN (i.e., couldn't be converted to a number)
    df_clean = df.dropna(subset=['TimeDays'])
    
    # Now convert to integer (since time days are whole numbers)
    df_clean['TimeDays'] = df_clean['TimeDays'].astype(int)

    # 3. Aggregate the data (get counts and sort)
    # value_counts() gives the frequency
    # sort_index() sorts the counts by the TimeDay value (the index), keeping the timeline correct
    frequency_series = df_clean['TimeDays'].value_counts().sort_index()

    # 4. Prepare data for the frontend (Chart.js)
    labels = frequency_series.index.tolist()
    data = frequency_series.values.tolist()
    
    # The processed data you will send to the template:
    context = {
        'chart_labels': labels,
        'chart_data': data,
        'chart_title': "Count of Samples by Time Day",
    }
    
    return render(request, 'visualization/data_chart.html', context)