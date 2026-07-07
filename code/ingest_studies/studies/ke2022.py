"""
Ke et al. 2022 (DOI: 10.1038/s41564-022-01105-z)
========================================================
Paper overview:
---------------
This study quantified daily SARS-CoV-2 viral load trajectories
in infected humans to characterize within-host kinetics,
infectiousness, and test sensitivity over time. Dense daily
sampling enabled precise modeling of viral growth and decay.

Data source:
------------
- https://www.nature.com/articles/s41564-022-01105-z

Notes:
- Species: Human
- Units: Viral RNA copies per mL (RT-qPCR)
- Sampling: Daily longitudinal nasal swabs
- Platform: RT-qPCR with viral culture validation
- Target: SARS-CoV-2 N gene
- No standalone public dataset repository
"""
import pandas as pd
import os
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    df = pd.read_csv(os.path.join(base_dir, "data", "ke2022.csv"))

    # Keep only the columns we need: 
    df = df[['Ind', 'Time', 'Lineage', 'Nasal_CN', 'Saliva_Ct', 'Antigen', 'Age']]

    # Clean up the Ind column: 
    df["Ind"] = df["Ind"].str.replace(r"\s*\*", "", regex=True)

    # Pivot the test outcome columns into a single column: 
    df = df.melt(
        id_vars=[col for col in df.columns if col not in ["Nasal_CN", "Saliva_Ct", "Antigen"]],
        value_vars=["Nasal_CN", "Saliva_Ct", "Antigen"],
        var_name="SampleSource",
        value_name="Log10VL"
        )

    # Map the contents of column SampleType to standard names: 
    df["SampleSource"] = df["SampleSource"].replace({
        "Nasal_CN": "nasal",
        "Saliva_Ct": "saliva",
        "Antigen": "nasal antigen"
        })

    # Rename columns to match schema: 
    df = df.rename(columns={
        "Ind": "IndivID",
        "Time": "TimeDays",
        "Lineage": "PathogenSubtype",
        "Age": "AgeRng1",
        "Log10VL": "BiomarkerQuantity"
        })

    # Add additional columns with known but missing information:
    df["StudyID"] = "Ke2022"
    df["Pathogen"] = "SARS-CoV-2"
    df["IndivSpecies"] = "Human"
    df["AgeRng2"] = df["AgeRng1"]
    df["DOI"] = "10.1038/s41564-022-01105-z"
    df["Units"] = df["SampleSource"].map({
        "saliva": "Ct",
        "nasal": "Ct",
        "nasal antigen": "binary"
        })
    df["SampleMethod"] = df["SampleSource"].map({
        "saliva": "raw_saliva",
        "nasal": "flocked_swab_in_VTM",
        "nasal antigen": "dry_swab"
        })
    df["AssayType"] = df["SampleSource"].map({
        "saliva": "RT-qPCR",
        "nasal": "RT-qPCR", #calibrated with ddPCR
        "nasal antigen": "Antigen"
        })
    df["ReadoutPlatform"] = df["SampleSource"].map({
        "saliva": "Taqpath",
        "nasal": "Alinity",
        "nasal antigen": "Sofia"
        })
    df["AssayTargets"] = df["SampleSource"].map({
        "saliva": "ORF1ab, N, S",
        "nasal": "N1",
        })
    df["GEml_conversion_intercept"] = df["SampleSource"].map({
        "saliva": 14.24,
        "nasal": 11.35,
        })
    df["GEml_conversion_slope"] = df["SampleSource"].map({
        "saliva": -0.28,
        "nasal": -0.25,
        })

    df["Biomarker"] = "pathogen load"
    df = enforce_schema(df)
    df = coerce_types(df)
    return df