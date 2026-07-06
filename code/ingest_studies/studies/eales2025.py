"""
Eales et al. 2025 (DOI: 10.1101/2025.02.01.636082v1)
========================================================
Paper overview::
---------------
This paper pools publicly available data from 3 studies of naturally and experimentally infected cattle with avian influenza H5N1 (clade 2.3.4.4b).

Source papers:
- natural infections
	- Caserta et al Nature 2025 Spillover of highly pathogenic avian influenza H5N1 virus to dairy cattle
- experimental infections
	- Halwe et al Nature 2024 H5N1 clade 2.3.4.4b dynamics in experimentally infected calves and cows
	- Baker et al Nature 2024 Dairy cows inoculated with highly pathogenic avian influenza virus H5N1

Eales et al then developed a Bayesian hierarchical model for quantifying Ct value trajectories, and modeling infectiousness duration.

We will cite here Eales et al as our authoritative source, but references to Baker, Caserta, and Halwe will also be made, and were used to interpret csvs.

Data sources:
------------
Eales et al:
    - https://github.com/Eales96/H5N1_viral_kinetics
    - https://doi.org/10.5281/zenodo.1478844

Baker et al:
    - https://zenodo.org/records/14368006

Notes:
------
Baker et al:
    - data is in "Eales_Baker_Fig.csv" which comes from Figure 1d of Baker (and originally included in Baker supplement)
    - is longitudinal data for two experimentally infected dairy cattle, cows 2112 and 2129
    - viral load reported as Ct values from RT-qPCR testing (max cycles = 40) of milk samples, from milk buckets and other sources ("clinical samples")
        - milk samples were taken every day
        - clinical samples were taken every day for the first 7 days, then every ~2 days thereafter
        - ante-mortem anatomical sources are DIVERSE
        - they also measured VL from milker equiment (claws and buckets pre- and post-decon, which are not ingested here since they're not patient-sourced)
        - here, ingested as:
            SampleSource = original source encoded from Baker, e.g. anatomical source
                - some where ambiguous abbreviations that I (Ellen) took my best guess at - spelled out in Baker_Fig_SampleSourceKey.xlsx
            SampleMethod = ["milk sample", "clinical sample", "antemortem sample"]
    - they also monitored and recorded clinical signs see Baker Extended Data Table 5
        - including body temperature with a thermal microchip, respiratory effort and rate, nasal and ocular discharge, and faecal consistency
        - not ingested here but could be included in v2

Caserta et al:
    - data is in "Eales_Caserta_Fig1a.csv", "Eales_Caserta_Fig1f.csv", and "Eales_Caserta_Fig2b.csv" which are from Eales repo, not from Caserta (which contains more data)
    - Eales also ingested Fig1f and Fig2b data, but the difficult to parse AnimalID naming scheme makes it hard to convert to kinetics
        - I have emailed the Caserta et al authors to ask for clarification (as of 11/17/25) on naming conventions
        - I suspect that the reported data that gets used in Eales et al is only a subset of all the animal data in Caserta et al
            - AND figures in Caserta et al may only show a subset of all animals described in the study
    - for MVP ingestion of Eales et al, decided to only go with data from Fig1a for now
        = mixture of numeric and A-type Animal(?)IDs
        - data is JUST from milk (n = 167) samples collected from cattle from farms 1 to 9 quantified by RT–qPCR targeting the IAV matrix gene

Halwe et al:
    - data is in "Eales_Halwe_Fig.csv" which is from Eales repo, extracted with PlotDigitizer from Halwe Fig 3C
        - H5N1 viral genome load over time in milk samples from 6 experimentally infected lactating cows (Halwe1 to Halwe6)
        - RT-qPCR (max cycles = 38)
        - Eales did not extract antibody level (S/N%) which was also in that figure
    - columns: [x, y, ID]
        - x = time after infection (days)
        - y = viral load, Cq (38 - 10)
        - ID = Halwe1:Halwe6
            - Halwe1-3 are subtype H5N1 B3.13 (US), and Hawe4-6 are H5N1 edDG (EU) according to inoculation groups, my assignment from Halwe text
    
"""
# %%
import pandas as pd
import sys
from pathlib import Path

# Make parent folder importable to import schema.py
import os, sys
THIS_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))  # .../ingest_studies
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from schema import enforce_schema, coerce_types

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
# %%

""" Baker import pseudocode

[x] load ../Eales_Baker_Fig.csv
[x] rename columns to schema
    "Animal ID" -> "PatientID"
    "Day post inoculation" -> "TimeDays"
    # "Sample" -> "SampleSource"
    "IAV RT-qPCR Ct" -> "PathogenLoad""
    "VI" == virus isolation (binary) -> could be worth including in v2, analagous to positive culture

[x] You will probably need to create SampleID from PatientID + TimeDays (MVP is milk samples and leave clinical for v2)
    - needs to be unique but can use codes for this so they're not giant - e.g. milk vs clinical vs AM, and the first few letters of SampleSource

[x] Sample Method:
    - check lookup table Baker_Fig_SampleSourceKey.xlsx, "Baker_Sample" column and assign from SampleMethod column

[x] Clean up sample source
    - check lookup table Baker_Fig_SampleSourceKey.xlsx, "OPKC_Sample"
    
# Additional columns
[x] StudyID -> "Eales2025_Baker" # for now _distinguish from other Eales data
[x] Pathogen -> "Influenza"
[x] PtSpecies -> "Dairy cattle"
[x] PlatformType -> "RT-qPCR"
[x] Units -> "Ct (max 40)"
[x] DOI -> "10.1101/2025.02.01.636082v1"
[x] enforce schema
[x] coerce types

"""
# %%
def baker():
    # Load the raw data with relative path
    csv_path = os.path.join(base_dir, "data", "Eales_Baker_Fig.csv")
    df = pd.read_csv(csv_path, usecols=["Animal ID", "Day post inoculation", "Sample", "IAV RT-qPCR Ct"]) # only load needed columns for now

    # Rename columns to match schema:
    df = df.rename(columns={
        "Animal ID": "IndivID",
        "Day post inoculation": "TimeDays",
        "IAV RT-qPCR Ct": "BiomarkerQuantity"
        # "VI": "TBD"  # "viral isolation", may want to include in v2, a la viral culture
    })

    # Load in lookup table from excel
    sample_source_key = pd.read_excel(os.path.join(base_dir, "data", "Baker_Fig_SampleSourceKey.xlsx"), sheet_name="Sheet1")

    # Some entries in Baker_Sample have trailing spaces, so trim first
    sample_source_key["Baker_Sample"] = sample_source_key["Baker_Sample"].str.strip()
    df["Sample"] = df["Sample"].str.strip()

    # Fill in df["SampleMethod"] using lookup table, matching column "Baker_Sample"
    method_map = dict(zip(sample_source_key["Baker_Sample"], sample_source_key["SampleMethod"]))
    df["SampleMethod"] = df["Sample"].map(method_map)

    """
    # are any NaNs? should be none!
    nan_sample_methods = df[df["SampleMethod"].isna()]
    nan_sample_methods
    """

    # Fill in df["SampleSource"] using lookup table, matching column "OPKC_Sample"
    source_map = dict(zip(sample_source_key["Baker_Sample"], sample_source_key["OPKC_Sample"]))
    df["SampleSource"] = df["Sample"].map(source_map)

    # Now can drop "Sample" column from df
    df = df.drop(columns=["Sample"])

    # Add SampleSource_Code to df from lookup table, from OPKC_Sample_ID column, and convert to int ("Int64" to allow for NaNs)
    opkc_id_map = dict(zip(sample_source_key["OPKC_Sample"], sample_source_key["OPKC_SampleSource_Code"])) # but make sure they are integers!!
    df["SampleSource_Code"] = df["SampleSource"].map(opkc_id_map)
    df["SampleSource_Code"] = df["SampleSource_Code"].astype("Int64")

    # Create SampleID from IndivID, TimeDays, first word in SampleMethod, and SampleSource_Code (SampleSource too verbose)
    df["SampleID"] = df["IndivID"].astype(str) + "_" + df["TimeDays"].astype(str) + "_" + df["SampleMethod"].str.split().str[0] + "_" + df["SampleSource_Code"].astype(str)
    # replace _antemorem with _AM for brevity
    df["SampleID"] = df["SampleID"].str.replace("_antemortem", "_AM", regex=False)

    # now can drop SampleSource_Code
    df = df.drop(columns=["SampleSource_Code"])

    # Additional columns with known information:
    df["StudyID"] = "Eales2025_Baker"
    df["Pathogen"] = "Influenza"
    df["PathogenSubtype"] = "H5N1"
    df["IndivSpecies"] = "Dairy cattle"
    df["DOI"] = "10.1101/2025.02.01.636082v1" # Eales et al
    df["Units"] = "Ct"
    df["LOD_max"] = 40
    df["AssayType"] = "RT-qPCR"
    df["Biomarker"] = "pathogen load"

    # Enforce schema and coerce types
    df = enforce_schema(df)
    df = coerce_types(df)

    #df

    return df
# %%

# %%
# Caserta MVP = Fig1a per Eales
def caserta():
    #load in data: Eales_Caserta_Fig1a.csv, Eales_Caserta_Fig1f.csv, and Eales_Caserta_Fig2b.csv

    csv_path_fig1a = os.path.join(base_dir, "data", "Eales_Caserta_Fig1a.csv")
    #csv_path_fig1f = os.path.join(base_dir, "data", "Eales_Caserta_Fig1f.csv")
    #csv_path_fig2b = os.path.join(base_dir, "data", "Eales_Caserta_Fig2b.csv")

    df1a = pd.read_csv(csv_path_fig1a)
    #df1f = pd.read_csv(csv_path_fig1f)
    #df2b = pd.read_csv(csv_path_fig2b)

    # %%
    # rename columns per schema
    df1a = df1a.rename(columns={
        "ID": "SampleID",
        "45-Ct": "BiomarkerQuantity"
        })

    # NOTE : I'm making an assumption here that the ID postfixes correspond to TimeDays in a way that makes sense
    # create a column in df1a that extract TimeDays from SampleID - search for the first "-" from the left of the string and take that int
    df1a["TimeDays"] = df1a["SampleID"].str.extract(r'-(\d+)$').astype(int)

    # now create another new column "IndivID"
    ## extract his from SampleID but without the year or TimeDays
    ## if the ID starts with a number, take the first 6 digits
    ## elif it starts with A, take all digits after A24 then up to the first "-"
    def extract_individ(sample_id):
        if sample_id[0].isdigit():
            return sample_id[:6]
        elif sample_id[0] == "A":
            return sample_id.split("-")[0][3:]  # remove "A24", not strictly necessary tbh
        else:
            return sample_id.split("-")[0]  # default case

    df1a["IndivID"] = df1a["SampleID"].apply(extract_individ)

    # %%

    # Additional columns with known information:
    df1a["StudyID"] = "Eales2025_Caserta"
    df1a["Pathogen"] = "Influenza"
    df1a["PathogenSubtype"] = "H5N1"
    df1a["IndivSpecies"] = "Dairy cattle"
    df1a["DOI"] = "10.1101/2025.02.01.636082v1" # Eales et al
    df1a["Units"] = "Ct"
    df1a["LOD_max"] = 45
    df1a["AssayType"] = "RT-qPCR" # referred to in the paper as "Real-time PCR with reverse transcription (rRT–PCR)"
    df1a["ReagentSystem"] = "Path-ID Multiplex One-Step RT-PCR Kit"
    df1a["ReadoutPlatform"] = "Applied Biosystems 7500 Fast PCR"
    df1a["AssayTargets"] = "IAV matrix gene"
    df1a["SampleSource"] = "milk" # raw data from Caserta et al directly does have the other sample types in figure, but Eales didn't ingest these
    df1a["SampleMethod"] = "milk sample"
    df1a["Biomarker"] = "pathogen load"

    # now can enforce schema and coerce types
    df1a = enforce_schema(df1a)
    df1a = coerce_types(df1a)

    return df1a

# Halwe et al is much more straightforward - only thing is that Eales extracted from Figure 3C with PlotDigitizer
# %% 
def halwe():
    csv_path = os.path.join(base_dir, "data", "Eales_Halwe_Fig.csv")
    df = pd.read_csv(csv_path)

    # strip whitespace from column names
    df.columns = df.columns.str.strip()

    #then rename columns according to schema
    df = df.rename(columns={
        "x": "TimeDays",
        "y": "BiomarkerQuantity",
        "ID": "IndivID"
    })

    # Halwe1-3 are subtype H5N1 B3.13 (US), and Hawe4-6 are H5N1 edDG (EU)
    df["PathogenSubtype"] = df["IndivID"].apply(lambda x: "H5N1 B3.13" if x in ["Halwe1", "Halwe2", "Halwe3"] else "H5N1 edDG")

    # Additional columns with known information:
    df["StudyID"] = "Eales2025_Halwe"
    df["Pathogen"] = "Influenza"
    df["IndivSpecies"] = "Dairy cattle"
    df["DOI"] = "10.1101/2025.02.01.636082v1" # Eales et al
    df["Units"] = "Ct WITH PLOTDIGITIZER"
    df['LOD_max'] = 38
    df["AssayType"] = "RT-qPCR"
    df["SampleSource"] = "milk"
    df["SampleMethod"] = "milk sample"
    df["ReagentSystem"] = "AgPath-ID One-Step RT–PCR kit"
    df["ReadoutPlatform"] = "BioRad CFX Maestro 1.1"
    df["Biomarker"] = "pathogen load"

    # Enforce schema and coerce types
    df = enforce_schema(df)
    df = coerce_types(df)

    return df

# %%
def load_and_format():
    # For now, just Baker data
    df_baker = baker()
    df_caserta = caserta() # to be added
    df_halwe = halwe()
    
    # combine all dataframes
    df_eales = pd.concat([df_baker, df_caserta, df_halwe], ignore_index=False)

    return df_eales
# %%
