"""
Kucirka et al. 2020 (DOI: 10.7326/M20-1495)
========================================================
Paper overview:
---------------
This meta-analysis quantified the false-negative rate of
RT-PCR testing for SARS-CoV-2 as a function of time since
exposure and symptom onset.

Data source:
------------
- https://www.acpjournals.org/doi/10.7326/M20-1495

Notes:
- Species: Human
- Units: Probability of false-negative RT-PCR
- Sampling: Pooled diagnostic respiratory samples
- Platform: RT-qPCR (clinical diagnostics)
- Target: SARS-CoV-2 RNA
- Statistical meta-analysis of multiple cohorts
"""

# Kucirka 2020
# Data source: https://github.com/HopkinsIDD/covidRTPCR/tree/master/data

# Column names of Kucirka 2020 data for reference
# study	, test , day , day_min , day_max , n , test_pos , inconclusive , nqp , pct_pos , notes
# Pulls from 7 different studies providing data on RT-PCR performance by time since symptom onset or SARS-CoV-2 exposure using samples from the upper respiratory tract (n = 1330).
# might be worth splitting this one up...
# Zhao et al. (2020), Liu et al. (2020), Guo et al. (2020), Wölfel et al. (2020), Danis et al. (2020), Kujawski et al. (2020) (nasal only), Kim et al. (2020), and Young et al. (2020) each looked at the sensitivity of the RT-PCR by time since symptom onset.

import pandas as pd
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/kucirka2020.csv")

    # Keep only the columns we need: 
    df = df[['study', 'test', 'day']] # , 'n', 'test_pos', 'nqp', 'pct_pos'
    # PROBLEM: no viral load quantities, only positive or negative and accuracy of testing method...

    # create sub StudyID Kucirka2020_[]
    df['study'] = df['study'].apply(lambda x: 'Kucirka2020_' + str(x))
    # Rename columns to match schema: 
    df = df.rename(columns={
        "study": "StudyID", 
        "test": "AssayType",
        "day": "TimeDays"
        })
    
    # Add additional columns with known but missing information:
    df["StudyID"] = "Kucirka2020"
    df["Pathogen"] = "SARS2"
    df["IndivSpecies"] = "Human"
    df["Units"] = "mixed" # study specific!
    df["DOI"] = "10.7326/M20-1495"
    # df["AssayType"] = "RT-qPCR" # study specific

    # not included or study specific! 
    #df["ReadoutPlatform"] = "Roche cobas 6800"
    #df["AssayTargets"] = "E-gene" 
    
    df = enforce_schema(df)
    df = coerce_types(df)
    return df