"""
Alahakoon et al. 2025 (DOI: 10.1101/2025.07.02.662782v1)
========================================================
Paper overview:
---------------
This paper develops a multiscale model linking pooled RT-qPCR Ct values from mosquito surveillance to within-mosquito viral kinetics, bird-to-mosquito transmission, and seasonal force of infection for West Nile virus (WNV). 
By integrating pooled surveillance data with laboratory-derived viral growth and decay dynamics, the authors infer temporal patterns of WNV transmission risk in wild bird–mosquito–human systems.

Data source:
------------
- https://www.biorxiv.org/content/10.1101/2025.07.02.662782v1

Notes:
- Species: Mosquitoes (vectors) and birds (hosts, in model)  
- Units: RT-qPCR Ct values (converted to estimated viral loads), model-based estimates of viral titers and force-of-infection  
- Sampling: Pooled mosquito trap samples (RT-qPCR) plus lab-derived kinetics from individual mosquitoes  
- Platform technology: RT-qPCR for Ct measurement; mathematical modeling to link pooled data to viral kinetics and transmission  
- Target: WNV RNA (genomic), using standard RT-qPCR assays  
- Preprint: not yet peer reviewed — raw Ct data appears included as pooled surveillance results; no public raw viral load dataset repository listed.  
"""
# Alahakoon 2025
# Data source: https://github.com/PunyaAlahakoon/west_nile_virus_abm/tree/main

# Data formatted from alahakoon2025_rawfiles
# Column names of combined Alahakoon 2025 data for reference
# surv_year	, disease_week , species , pool_size , WNV , ctval , state

# WORK TO BE DONE/CONSIDERED #
# does WN column only indicate yes West Nile was identified within pool of individuals or that one individual was counted (less likely)?
# how can we incorporate num_count available in SOME of the data? But there is only one viral load data point for each...

import pandas as pd
import os
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    df = pd.read_csv(os.path.join(base_dir, "data", "alahakoon2025.csv"))

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
        "ctval": "BiomarkerQuantity",
        })

    # Add additional columns with known but missing information:
    df["StudyID"] = "alahakoon2025"
    df["Pathogen"] = "West Nile virus"
    df["IndivSpecies"] = "Mosquitoes"
    df["DOI"] = "10.1101/2025.07.02.662782"
    df["Units"] = "Ct"
    lod_max = 40
    df["LOD_max"] = lod_max
    # Raw ctval == 0 is a non-physical sentinel (0 amplification cycles doesn't
    # happen); interpret as "not detected" and canonicalize to LOD_max so the
    # rows sit at the ceiling on the Ct axis instead of at the top of the plot.
    df["BiomarkerQuantity"] = pd.to_numeric(df["BiomarkerQuantity"], errors="coerce")
    df["BelowLOD"] = df["BiomarkerQuantity"].le(0).where(df["BiomarkerQuantity"].notna(), pd.NA)
    df.loc[df["BiomarkerQuantity"].le(0), "BiomarkerQuantity"] = lod_max
    df["AssayType"] = "RT-qPCR" # referred to in the paper as "Real-time PCR with reverse transcription (rRT–PCR)"
    df["ReagentSystem"] = "trioplex RT-qPCR assay"
    df["SampleSource"] = "mosquito"
    df["SampleMethod"] = "CO2 light traps"

    df["Biomarker"] = "pathogen load"
    df = enforce_schema(df)
    df = coerce_types(df)
    return df
