# Alahakoon 2025
# Data source: https://github.com/PunyaAlahakoon/west_nile_virus_abm/tree/main

# Data formatted from alahakoon2025_rawfiles
# Column names of combined Alahakoon 2025 data for reference
# surv_year	, disease_week , species , pool_size , WNV , ctval , state


import pandas as pd
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/alahakoon2025.csv")

    # Keep only the columns we need: 
    df = df[['disease_week', 'species', 'ctval']]
    # add ID for each individual
    df['mosqID'] = df.index + 1

    # translate weeks to days -> shift for minimum week data
    df['disease_week'] = (df['disease_week'] - 22) * 7

    # Rename columns to match schema: 
    df = df.rename(columns={
        "mosqID": "IndivID",
        "disease_week": "TimeDays",
        "ctval": "PathogenLoad"
        })

    # Add additional columns with known but missing information:
    df["StudyID"] = "alahakoon2025"
    df["Pathogen"] = "WestNile"
    df["IndSpecies"] = "Mosquitoes"
    df["DOI"] = "10.1101/2025.07.02.662782"
    df["Units"] = "Ct (max 40)"
    df["PlatformType"] = "RT-qPCR" # referred to in the paper as "Real-time PCR with reverse transcription (rRT–PCR)"
    df["PlatformTech"] = "trioplex RT-qPCR assay"
    df["SampleMethod"] = "CO2 light traps"

    df = enforce_schema(df)
    df = coerce_types(df)
    return df