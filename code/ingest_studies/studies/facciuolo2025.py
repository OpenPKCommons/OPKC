"""
Facciuolo et al 2025 (DOI: 10.1038/s41564-025-01998-6)
https://pubmed.ncbi.nlm.nih.gov/40247094/
======================================================
Paper overview:
----------------
H5N1 challenge study in dairy cattle
    - n=3 with n=2 cows studied long-term, including after re-infection 31 days after initial inoculation
    - third cow was euthanized at day 4 DPI and detailed necropsy was performed
    - H5N1 genotype B3.13
    - viral kinetics = H5N1 RT-qPCR in cows 4 and 11 (longitudinal cows)
        - reported mean of 2 Ct values as values converted to TCID50 by interpolating from a standard curve
    - also measured
        - viral shedding in milk
        - virus-neutralizing antibodies
        - viral RNA in air samples from animal rooms
    - measurement types and frequency are very detailed for the 2-3 animals studied
        - FWIW Eales also appears to be working on ingesting this, as of November 2025
            (https://github.com/Eales96/H5N1_viral_kinetics/tree/main/data)

[Source Data at paper](https://www-nature-com.colorado.idm.oclc.org/articles/s41564-025-01998-6#Sec25)

Data to ingest:
- Figure 4 = RT-qPCR and infectious titers (milk) from cows 4 (b, c), and 11 (d, e)
- Figure 6 = serum and milk (forequarters and hindquarters separated out) antibody responses (h5N1 B3.13 NP gene segment)
    - didn't get to this yet
- eventually may also want to ingest data from Figure 2 = symptoms, more or less
    - a = daily milk yield, b = rectal temperature, c = CMT (California Mastitis Test) results over time
- another eventual possibility is air sampling data from Extended Data Table 2

Ingestion Notes:
- In some cases, data from the 14-day pre-challenge period was reported only as "pre-challenge"
    - Here I artbitrarily decided to assign these to TimeDays = -7
- 1 DPSI = DPI 31, aka the first re-infection day
- VN = virus neutralization assay
- I also assigned IndivIDs and SampleIDs, but these should be edited later once a system across studies is adopted

"""

"""
Psuedocode planning:

[] Load data from facciuolo2025.xlsx with relative path, KEEPING INDEXES
    - Tabs:
        [x] "Fig_4b" = cow 4 RT-qPCR
        [x] "Fig_4c" = cow 4 titer
        [x] "Fig_4d" = cow 11 RT-qPCR
        [x] "Fig_4e" = cow 11 titer

        [] "Fig_6a" = serum anitbodies by ELISA
        [] "Fig_6b" = serum antibodies by VN

        [] "Fig_6c" = milk forequarters antibodies by ELISA
        [] "Fig_6d" = milk forequarters by VN titer
        [] "Fig_6e" = milk forequarters by HAI titer

        [] "Fig_6f" = milk hindquarters antibodies by ELISA
        [] "Fig_6g" = milk hindquarters by VN titer
        [] "Fig_6h" = milk hindquarters by HAI titer

[x] Write a date-remapping function
    - Rewrite "DAY" (Fig 4) or blank (Fig 6) column 0
        - Rename: "TimeDays"
        - Use indexing to note where "1 DPSI" occurs and set all subsequent days accordingly (Fig 4 only)
        - "Pre-challenge" = -7
        - clean " DPI" from strings
        - convert remaining string to int
        - clean " DPSI" from strings and set dpsi=True
        - convert remainingi string to int+30
        - return cleaned series 

[x] For each tab, reformat data according to schema - may want to assign SampleIDs here
    - 4b
        - "Cow #4 HL" = PathogenLoad
            - "SampleSource" = "left hindquarters"
            - "SampleMethod" = "milk sample"
        - "Cow #4 FL" = PathogenLoad
            - "SampleSource" = "left forequarters"
            - "SampleMethod" = "milk sample"
        - "Cow #4 HR" = PathogenLoad
            - "SampleSource" = "right hindquarters"
            - "SampleMethod" = "milk sample"
        - "Cow #4 FR" = PathogenLoad
            - "SampleSource" = "right forequarters"
            - "SampleMethod" = "milk sample"
        - Units = "TCID50 equivalent/mL"
        - PlatformType = "RT-qPCR"
        - Targets = "Influenza A - M gene"
        - PlatformTech = "Luna qPCR Kit, StepOne Plus Real-Time PCR System"
     - 4c
        - same as 4b
        - Units = "TCID50/mL"
        - PlatformType = "Infectious virus titer"
    - 4d, e = same as 4b , c but for cow 11

[] Additional columns
    [] StudyID = "Facciuolo2025"
    [] Pathogen = "Flu"
    [] Subtype = "H5N1 B3.13"
    [] PtSpecies = "Dairy cattle"
    [] DOI = "10.1038/s41564-025-01998-6"

[] Enforce schema
[] Coerce types

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

def remap_days(day_series, dpsi=False):
    """Remap values from inuptted day_series to TimeDays-compatible integers

    Args:
        day_series (pd.Series): Series of day values (ints or strings) from source data
        dpsi (bool): Indicates whether iterator has already reached DPSI days (not indicated in source data)

    Returns:
        pd.Series: Series of integers representing days post-infection.
    """
    remapped_days = []
    for day in day_series:
        #print("day:", day, " dpsi:", dpsi)

        # convert all to strings for ease
        day = str(day)

        day = day.strip()
        if day == "Pre-challenge":
            remapped_days.append(-7)
        elif "DPI" in day:
            day_num = int(day.replace(" DPI", ""))
            remapped_days.append(day_num)
        elif day.isdigit() and not dpsi:
            day_num = int(day)
            remapped_days.append(day_num)
        elif "DPSI" in day:
            day_num = int(day.replace(" DPSI", ""))
            remapped_days.append(day_num + 30)
            dpsi = True
        elif dpsi and day.isdigit():
            day_num = int(day) + 30
            remapped_days.append(day_num)
        else:
            remapped_days.append(None)  # or handle unexpected format
            print("Warning: unexpected day format:", day)
        
    return pd.Series(remapped_days)

# %%
"""
#Test the remap_days function
test_days = pd.Series(["Pre-challenge", "0 DPI", "1 DPI", "2", "3", "1 DPSI", "2", "3", "4"])
remapped_test_days = remap_days(test_days)
"""

# Function to append raw data to a combined df, by tab and by cow/source - pretty brute force but works for now
def expand_tabs(in_df, col_name, samplesource, samplemethod, units, platformtype, targets, platformtech):
    df_expanded = pd.DataFrame()
    df_expanded["PathogenLoad"] = in_df[col_name].values
    df_expanded["TimeDays"] = in_df["TimeDays"].values
    df_expanded["SampleSource"] = samplesource
    df_expanded["SampleMethod"] = samplemethod
    df_expanded["Units"] = units
    df_expanded["PlatformType"] = platformtype
    df_expanded["Targets"] = targets
    df_expanded["PlatformTech"] = platformtech

    # add an IndivID column based on cow number
    cow_number = col_name.split("#")[1].split(" ")[0]  # extract cow number from "Cow #4 HL"
    df_expanded["IndivID"] = f"cow_{cow_number}"

    # extract HL or FL from col_name
    sample_source = col_name.split(" ")[2]  # e.g., "HL" or "FL"

    # add SampleID column based on cow number, sample_source, and TimeDays (they are all milk)
    df_expanded["SampleID"] = df_expanded.apply(lambda row: f"cow{cow_number}_{sample_source}_milk_{row['TimeDays']}", axis=1)

    return df_expanded
# %%

def load_and_format():
    # Load data
    datapath = Path(base_dir) / "data" / "facciuolo2025.xlsx"

    # Figure 4 data
    df_4b = pd.read_excel(datapath, sheet_name="Fig_4b", index_col=0, header=1)
    df_4c = pd.read_excel(datapath, sheet_name="Fig_4c", index_col=0, header=1)
    df_4d = pd.read_excel(datapath, sheet_name="Fig_4d", index_col=0, header=1)
    df_4e = pd.read_excel(datapath, sheet_name="Fig_4e", index_col=0, header=1)

    # %%
    # Now let's remap DAYS from source data to TimeDays as a new column in each df - can confirm correct mapping
    df_4b["TimeDays"] = remap_days(df_4b.index).values
    df_4c["TimeDays"] = remap_days(df_4c.index).values
    df_4d["TimeDays"] = remap_days(df_4d.index).values
    df_4e["TimeDays"] = remap_days(df_4e.index).values
    # %%

    # %%

    # 4b - Cow 4 HL
    df_4b_HL = expand_tabs(
        df_4b,
        col_name="Cow #4 HL",
        samplesource="left hindquarters",
        samplemethod="milk sample",
        units="TCID50 equivalent/mL",
        platformtype="RT-qPCR",
        targets="Influenza A - M gene",
        platformtech="Luna qPCR Kit, StepOne Plus Real-Time PCR System"
    )

    # %%
    # is it elegant, no? but it works
    df_4b_FL = expand_tabs(
        df_4b,
        col_name="Cow #4 FL",
        samplesource="left forequarters",
        samplemethod="milk sample",
        units="TCID50 equivalent/mL",
        platformtype="RT-qPCR",
        targets="Influenza A - M gene",
        platformtech="Luna qPCR Kit, StepOne Plus Real-Time PCR System"
    )

    df_4b_HR = expand_tabs(
        df_4b,
        col_name="Cow #4 HR",
        samplesource="right hindquarters",
        samplemethod="milk sample",
        units="TCID50 equivalent/mL",
        platformtype="RT-qPCR",
        targets="Influenza A - M gene",
        platformtech="Luna qPCR Kit, StepOne Plus Real-Time PCR System"
    )

    df_4b_FR = expand_tabs(
        df_4b,
        col_name="Cow #4 FR",
        samplesource="right forequarters",
        samplemethod="milk sample",
        units="TCID50 equivalent/mL",
        platformtype="RT-qPCR",
        targets="Influenza A - M gene",
        platformtech="Luna qPCR Kit, StepOne Plus Real-Time PCR System"
    )

    # Now 4c
    df_4c_HL = expand_tabs(
        df_4c,
        col_name="Cow #4 HL",
        samplesource="left hindquarters",
        samplemethod="milk sample",
        units="TCID50/mL",
        platformtype="Infectious virus titer",
        targets="",
        platformtech=""
    )

    df_4c_FL = expand_tabs(
        df_4c,
        col_name="Cow #4 FL",
        samplesource="left forequarters",
        samplemethod="milk sample",
        units="TCID50/mL",
        platformtype="Infectious virus titer",
        targets="",
        platformtech=""
    )

    df_4c_HR = expand_tabs(
        df_4c,
        col_name="Cow #4 HR",
        samplesource="right hindquarters",
        samplemethod="milk sample",
        units="TCID50/mL",
        platformtype="Infectious virus titer",
        targets="",
        platformtech=""
    )

    df_4c_FR = expand_tabs(
        df_4c,
        col_name="Cow #4 FR",
        samplesource="right forequarters",
        samplemethod="milk sample",
        units="TCID50/mL",
        platformtype="Infectious virus titer",
        targets="",
        platformtech=""
    )

    # And Cow 11, 4d
    df_4d_HL = expand_tabs(
        df_4d,
        col_name="Cow #11 HL",
        samplesource="left hindquarters",
        samplemethod="milk sample",
        units="TCID50 equivalent/mL",
        platformtype="RT-qPCR",
        targets="Influenza A - M gene",
        platformtech="Luna qPCR Kit, StepOne Plus Real-Time PCR System"
    )

    df_4d_FL = expand_tabs(
        df_4d,
        col_name="Cow #11 FL",
        samplesource="left forequarters",
        samplemethod="milk sample",
        units="TCID50 equivalent/mL",
        platformtype="RT-qPCR",
        targets="Influenza A - M gene",
        platformtech="Luna qPCR Kit, StepOne Plus Real-Time PCR System"
    )

    df_4d_HR = expand_tabs(
        df_4d,
        col_name="Cow #11 HR",
        samplesource="right hindquarters",
        samplemethod="milk sample",
        units="TCID50 equivalent/mL",
        platformtype="RT-qPCR",
        targets="Influenza A - M gene",
        platformtech="Luna qPCR Kit, StepOne Plus Real-Time PCR System"
    )

    df_4d_FR = expand_tabs(
        df_4d,
        col_name="Cow #11 FR",
        samplesource="right forequarters",
        samplemethod="milk sample",
        units="TCID50 equivalent/mL",
        platformtype="RT-qPCR",
        targets="Influenza A - M gene",
        platformtech="Luna qPCR Kit, StepOne Plus Real-Time PCR System"
    )

    df_4e_HL = expand_tabs(
        df_4e,
        col_name="Cow #11 HL",
        samplesource="left hindquarters",
        samplemethod="milk sample",
        units="TCID50/mL",
        platformtype="Infectious virus titer",
        targets="",
        platformtech=""
    )

    df_4e_FL = expand_tabs(
        df_4e,
        col_name="Cow #11 FL",
        samplesource="left forequarters",
        samplemethod="milk sample",
        units="TCID50/mL",
        platformtype="Infectious virus titer",
        targets="",
        platformtech=""
    )

    df_4e_HR = expand_tabs(
        df_4e,
        col_name="Cow #11 HR",
        samplesource="right hindquarters",
        samplemethod="milk sample",
        units="TCID50/mL",
        platformtype="Infectious virus titer",
        targets="",
        platformtech=""
    )

    df_4e_FR = expand_tabs(
        df_4e,
        col_name="Cow #11 FR",
        samplesource="right forequarters",
        samplemethod="milk sample",
        units="TCID50/mL",
        platformtype="Infectious virus titer",
        targets="",
        platformtech=""
    )

    # Now can concatenate all these dataframes together
    df = pd.concat([
        df_4b_HL, df_4b_FL, df_4b_HR, df_4b_FR,
        df_4c_HL, df_4c_FL, df_4c_HR, df_4c_FR,
        df_4d_HL, df_4d_FL, df_4d_HR, df_4d_FR,
        df_4e_HL, df_4e_FL, df_4e_HR, df_4e_FR
    ], ignore_index=True)
    # %%

    # Figure 6 data
    """
    df_6a = pd.read_excel(datapath, sheet_name="Fig_6a", index_col=0)
    df_6b = pd.read_excel(datapath, sheet_name="Fig_6b", index_col=0)
    df_6c = pd.read_excel(datapath, sheet_name="Fig_6c", index_col=0)
    df_6d = pd.read_excel(datapath, sheet_name="Fig_6d", index_col=0)
    df_6e = pd.read_excel(datapath, sheet_name="Fig_6e", index_col=0)
    df_6f = pd.read_excel(datapath, sheet_name="Fig_6f", index_col=0)
    df_6g = pd.read_excel(datapath, sheet_name="Fig_6g", index_col=0)
    df_6h = pd.read_excel(datapath, sheet_name="Fig_6h", index_col=0)
    """


    # Add additional columns
    df["StudyID"] = "Facciuolo2025"
    df["Pathogen"] = "Flu"
    df["Subtype"] = "H5N1 B3.13"
    df["IndSpecies"] = "Dairy cattle"
    df["DOI"] = "10.1038/s41564-025-01998-6"

    # Enforce schema and coerce types
    df = enforce_schema(df)
    df = coerce_types(df)

    return df
    # %%