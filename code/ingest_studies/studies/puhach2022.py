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

import numpy as np
import pandas as pd
import os
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    df = pd.read_csv(os.path.join(base_dir, "data", "puhach2022.csv"))

    # Keep only the columns we need. The paper reports both RNA load (RT-qPCR)
    # and infectious virus (FFU by focus-forming assay); we ingest the RNA load
    # to match AssayType="RT-qPCR" and keep the y-axis scale comparable with
    # other RT-qPCR viral-kinetics studies.
    df = df[['sample number', 'DPOS', 'Variant', 'RNA load/ml', 'Age']]

    # Rename columns to match schema:
    df = df.rename(columns={
        "sample number": "IndivID",
        "DPOS": "TimeDays",
        "RNA load/ml": "BiomarkerQuantity",  # linear copies/mL; log10-transformed below
        "Variant": "PathogenSubtype",
        "Age": "AgeRng1"
        })

    # Log10-transform to match other RT-qPCR studies. Source has no zeros in
    # practice, but flag any source <= 0 as BLOD defensively.
    src = pd.to_numeric(df["BiomarkerQuantity"], errors="coerce")
    df["BelowLOD"] = src.le(0).where(src.notna(), pd.NA)
    df["BiomarkerQuantity"] = np.log10(src.where(src > 0))

    # Add additional columns with known but missing information:
    df["StudyID"] = "Puhach2022"
    df["Pathogen"] = "SARS-CoV-2"
    df["IndivSpecies"] = "Human"
    df["Units"] = "log10(copies/mL)"
    df["DOI"] = "10.1038/s41591-022-01816-0"
    df["AssayType"] = "RT-qPCR"
    df["ReadoutPlatform"] = "Roche cobas 6800"
    df["AssayTargets"] = "E-gene, S-gene"
    df["SampleSource"] = "nasopharynx"
    df["SampleMethod"] = "swab"

    df["Biomarker"] = "pathogen load"
    df = enforce_schema(df)
    df = coerce_types(df)
    
    return df