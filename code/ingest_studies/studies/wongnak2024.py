import pandas as pd
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/wongnak2024.csv")

    # Keep only the columns we need: 
    df = df[['ID', 'Time', 'Trt', 'Swab_ID', 'Any_dose', 'Age', 'BARCODE', 'Symptom_onset', 'Variant', 'Variant2', 'CT_NS', 'CT_RNaseP', 'log10_viral_load', 'log10_cens_vl']]

    # I'm pretty sure log10_cens_vl is the limit of detection... but it's not the same for all samples. 

    return df