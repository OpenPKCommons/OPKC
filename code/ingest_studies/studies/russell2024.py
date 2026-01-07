"""
Russell et al. 2024 (DOI: 10.1371/journal.pbio.3002463)
========================================================
Paper overview:
---------------
This study integrated viral kinetics, infectiousness modeling,
and immune dynamics to quantify how long individuals remain
infectious with SARS-CoV-2 under different immune histories.

Data source:
------------
- https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3002463

Notes:
- Species: Human
- Units: Viral RNA copies per mL and infectious virus (TCID50)
- Sampling: Longitudinal respiratory sampling
- Platform: RT-qPCR and viral culture
- Target: SARS-CoV-2 genomic RNA
- Model-driven analysis with individual-level trajectories

"""
import pandas as pd
from schema import enforce_schema, coerce_types, split_age_range

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/russell2024.csv")

    # Keep only the columns we need: 
    df = df[['id', 'swab_type', 'VOC', 'symptoms', 'symptom_onset_date', 't', 'age_group', 'ct_type', 'ct_value']]

    # Format the age group column into separate age ranges: 
    df["AgeRng1"] = df["age_group"].map({
        "20-34": 20,
        "35-49": 35,
        "50+": 50
        })
    df["AgeRng2"] = df["age_group"].map({
        "20-34": 34,
        "35-49": 49,
        "50+": 100
        })

    # Convert to numeric
    df["AgeRng1"] = pd.to_numeric(df["AgeRng1"], errors="coerce")
    df["AgeRng2"] = pd.to_numeric(df["AgeRng2"], errors="coerce")

    # Rename columns to match schema: 
    df = df.rename(columns={
        "id": "IndivID",
        "swab_type": "SampleMethod",
        "VOC": "PathogenSubtype",
        "symptoms": "Symptoms1",
        "t": "TimeDays",
        "ct_value": "BiomarkerQuantity"
        })
    
    df["AssayTargets"] = df["ct_type"].map({
        "ct_value": "ORF1a",
        "ct_n_gene": "N",
        "ct_s_gene": "S"
    })

    df["SampleMethod"] = df["SampleMethod"].map({
        "Dry": "dry_swab",
        "VTM": "swab_in_VTM",
        })

    # df = split_age_range(df, col="age_group")

    # Add additional columns with known but missing information:
    df["StudyID"] = "russell2024"
    df["Pathogen"] = "SARS2"
    df["IndivSpecies"] = "Human"
    df["DOI"] = "10.1371/journal.pbio.3002463"
    df["Units"] = "Ct"
    df["SampleSource"] = "nasopharyngeal"
    df["AssayType"] = "RT-qPCR"
    df["ReadoutPlatform"] = "QuantStudio 3"

    df = enforce_schema(df)
    df = coerce_types(df)
    
    return df