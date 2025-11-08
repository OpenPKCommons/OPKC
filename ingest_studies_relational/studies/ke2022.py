# ke2022_relational.py
import pandas as pd
import numpy as np

def process_data():
    """
    Loads and processes the Ke et al. 2022 data, returning a dictionary
    of DataFrames for each relational table.
    """
    df = pd.read_csv("data/ke2022.csv")

    # --- Clean up the Ind column ---
    df["Ind"] = df["Ind"].str.replace(r"\s*\*", "", regex=True)

    # --- Pivot the test outcome columns into a single column ---
    df = df.melt(
        id_vars=['Ind', 'Time', 'Lineage', 'Age'],
        value_vars=["Nasal_CN", "Saliva_Ct", "Antigen"],
        var_name="SampleTypeRaw",
        value_name="ViralLoad"
    ).dropna(subset=['ViralLoad'])

    # --- Map the contents of column SampleType to standard names ---
    df.rename(columns={"Ind": "PersonID", "Time": "TimeDays"}, inplace=True)
    df['StudyID'] = 'ke2022'

    # --- 1. Studies Table ---
    studies_df = pd.DataFrame([{
        'StudyID': 'ke2022',
        'Title': 'Daily longitudinal sampling of SARS-CoV-2 infection reveals substantial heterogeneity in infectiousness',
        'DOI': '10.1038/s41564-022-01105-z',
        'Year': 2022,
        'DataURL': 'https://github.com/BROOKELAB/Viral-dynamics-modeling'
    }])

    # --- 2. Platforms Table ---
    platform_map = {
        "Nasal_CN": {
            "PlatformName": "Alinity", "ViralLoadUnits": "Ct",
            "Ct_to_GEml_intercept": 11.35, "Ct_to_GEml_slope": -0.25
        },
        "Saliva_Ct": {
            "PlatformName": "Taqpath", "ViralLoadUnits": "Ct",
            "Ct_to_GEml_intercept": 14.24, "Ct_to_GEml_slope": -0.28
        },
        "Antigen": {
            "PlatformName": "Sofia", "ViralLoadUnits": "binary",
            "Ct_to_GEml_intercept": np.nan, "Ct_to_GEml_slope": np.nan
        }
    }
    platforms_df = pd.DataFrame(platform_map.values())
    platforms_df['PlatformName'] = platforms_df['PlatformName'].astype(str)
    
    # Add platform info to main df for later mapping
    df['PlatformName'] = df['SampleTypeRaw'].map(lambda x: platform_map[x]['PlatformName'])
    df['ViralLoadUnits'] = df['SampleTypeRaw'].map(lambda x: platform_map[x]['ViralLoadUnits'])

    # --- 3. Infections Table ---
    # In this study, each person has one infection event.
    infections_df = df[['StudyID', 'PersonID', 'Age', 'Lineage']].copy()
    infections_df.rename(columns={
        'Age': 'AgeRng1',
        'Lineage': 'Variant'
    }, inplace=True)
    infections_df['AgeRng2'] = infections_df['AgeRng1'] # Age is given as single value
    infections_df['InfectionID'] = infections_df['StudyID'] + '_' + infections_df['PersonID']
    infections_df = infections_df.drop_duplicates(subset=['InfectionID'])

    # --- 4. Samples Table ---
    samples_df = df[['StudyID', 'PersonID', 'TimeDays', 'ViralLoad', 'ViralLoadUnits', 'SampleTypeRaw', 'PlatformName']].copy()
    samples_df['InfectionID'] = samples_df['StudyID'] + '_' + samples_df['PersonID']
    samples_df['SampleID'] = samples_df.index.map(lambda x: f"ke2022_{x}")
    samples_df.rename(columns={'TimeDays': 'Time', 'SampleTypeRaw': 'SampleType'}, inplace=True)
    samples_df['SampleType'] = samples_df['SampleType'].replace({"Nasal_CN": "nasal", "Saliva_Ct": "saliva", "Antigen": "antigen"})
    
    return {
        'studies': studies_df,
        'platforms': platforms_df,
        'infections': infections_df,
        'samples': samples_df
    }