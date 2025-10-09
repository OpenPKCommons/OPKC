import pandas as pd
from ..schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/wongnak2024.csv")

    # Keep only the columns we need: 
    df = df[['ID', 'Time', 'Trt', 'Swab_ID', 'Age', 'BARCODE', 'Variant', 'log10_viral_load']]

    # Rename columns to match the standard schema:
    df = df.rename(columns={
        "ID": "PersonID",
        "Time": "TimeDays",
        "Trt": "Treatment1",
        "Swab_ID": "SampleType",
        "Age": "AgeRng1",
        "BARCODE": "SampleID", 
        "Variant": "Subtype",
        "log10_viral_load": "Log10VL"
        })

    # Since age is given as a single value, set the upper bound of the age range to be the same
    df['AgeRng2'] = df['AgeRng1']

    # Add additional columns with known but missing information:
    df["StudyID"] = "wongnak2024"
    df["DOI"] = "10.1016/S1473-3099(24)00183-X"
    df["Units"] = "GEml"
    df["Platform"] = "TaqCheckFastPCR"

    df = enforce_schema(df)
    df = coerce_types(df)

    return df