# database_schema.py

# Define the columns for each of the four tables in the relational database.

STUDIES_COLS = [
    'StudyID', 'Title', 'DOI', 'Year', 'DataURL'
]

INFECTIONS_COLS = [
    'InfectionID', 'PersonID', 'StudyID', 'AgeRng1', 'AgeRng2',
    'Symptom1', 'Symptom1Start', 'Symptom1End', 
    'Symptom2', 'Symptom2Start', 'Symptom2End', 
    'Symptom3', 'Symptom3Start', 'Symptom3End', 
    'Symptom4', 'Symptom4Start', 'Symptom4End', 
    'Comorbidity1', 'Comorbidity2', 'Comorbidity3', 'Comorbidity4',
    'Treatment1', 'Treatment2', 'Treatment3', 'Treatment4', 
    'Variant', 'Hospitalized', 'Died'
]

SAMPLES_COLS = [
    'SampleID', 'PersonID', 'InfectionID', 'PlatformID', 'StudyID',
    'Time', 'GeoLocation', 'ViralLoad', 'ViralLoadUnits', 
    'AnatomicalSite', 'CollectionMethod', 'Medium'
]

PLATFORMS_COLS = [
    'PlatformID', 'PlatformName', 
    'Ct_to_GEml_slope', 'Ct_to_GEml_intercept', 'LimitOfDetection'
]