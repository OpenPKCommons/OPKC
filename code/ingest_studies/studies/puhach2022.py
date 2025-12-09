"""
Puhach et al. 2022 (DOI: 10.1038/s41591-022-01816-0)
========================================================
Paper overview:
---------------
This study quantified infectious viral load of SARS-CoV-2 in
vaccinated and unvaccinated individuals, linking RNA levels
to culturable virus across variants.

Data source:
------------
- https://www.nature.com/articles/s41591-022-01816-0

Notes:
- Species: Human
- Units: RNA copies per mL and infectious virus (PFU/mL)
- Sampling: Longitudinal nasopharyngeal swabs
- Platform: RT-qPCR + viral culture
- Target: SARS-CoV-2 E gene
- Key study linking PCR to infectiousness
"""
# Puhach 2022
# Data source (supplementary information): https://www-nature-com.colorado.idm.oclc.org/articles/s41591-022-01816-0#Sec19

# Column names of Puhach 2022 data for reference
# sample number , Age , Sex , DPOS , Vaccination status , Number of doses , Days post vac (2nd/3rd dose) , Name of Vaccine Manufacturer , RNA load/ml , FFU/ml , FFU titrated on , Isolation success , Variant
# DPOS - days post onset of symptoms
# Note: RNA load/ml and FFU/ml both in log10, representing RNA viral load and infectious viral loads respectively

import pandas as pd
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/puhach2022.csv")

    # Keep only the columns we need: 
    df = df[['sample number', 'DPOS', 'Variant', 'FFU/ml', 'Age']]

    # Rename columns to match schema: 
    df = df.rename(columns={
        "sample number": "PersonID",
        "DPOS": "TimeDays",
        "FFU/ml": "PathogenLoad", # log10 genome copies per ml for RNA viral loads
        "Variant": "Subtype",
        "Age": "AgeRng1"
        })

    # Add additional columns with known but missing information:
    df["StudyID"] = "puhach2022"
    df["Pathogen"] = "SARS2"
    df["IndSpecies"] = "Human"
    df["Units"] = "GEml (log10VL)"
    df["DOI"] = "10.1038/s41591-022-01816-0"
    df["PlatformType"] = "RT-qPCR"
    df["PlatformTech"] = "Roche cobas 6800/"
    df["Targets"] = "E-gene, S-gene"

    df = enforce_schema(df)
    df = coerce_types(df)
    return df