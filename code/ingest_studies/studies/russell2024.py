import pandas as pd
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/russell2024.csv")

    # Keep only the columns we need: 
    df = df[['id', 'VOC', 'symptoms', 'symptom_onset_date', 't', 'age_group', 'ct_type', 'ct_value']]

    # Rename columns to match schema: 
    df = df.rename(columns={
        "id": "PersonID",
        "VOC": "Subtype",
        "symptoms": "Symptoms1",
        "t": "TimeDays",
        "ct_type": "Platform",
        "ct_value": "Log10VL"
        })

    # Add additional columns with known but missing information:
    df["StudyID"] = "russell2024"
    df["AgeRng2"] = df["AgeRng1"]
    df["DOI"] = "10.1038/s41564-022-01105-z"
    df["Units"] = "Ct"
    df["SampleType"] = "nasopharyngeal"
    df["Platform"] = df["SampleType"].map({
        "saliva": "Taqpath",
        "nasal": "Alinity",
        "antigen": "Sofia"
        })
    df["GEml_conversion_intercept"] = df["SampleType"].map({
        "saliva": 14.24,
        "nasal": 11.35,
        })
    df["GEml_conversion_slope"] = df["SampleType"].map({
        "saliva": -0.28,
        "nasal": -0.25,
        })

    df = enforce_schema(df)
    df = coerce_types(df)
    return df