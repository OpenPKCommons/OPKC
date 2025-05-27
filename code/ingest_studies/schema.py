import pandas as pd

STANDARD_SCHEMA = [
    "StudyID", "PersonID", "InfectionID", "SampleID", "TimeDays",
    "Symptoms1", "Symptoms2", "Symptoms3", "Symptoms4",
    "Comorbidity1", "Comorbidity2", "Comorbidity3", "Comorbidity4",
    "Treatment1", "Treatment2", "Treatment3", "Treatment4",
    "Hospitalized", "SampleType", "AgeRng1", "AgeRng2",
    "Subtype", "Platform", "DOI", "Log10VL", "Units", "GEml_conversion_intercept", "GEml_conversion_slope"
]

def enforce_schema(df):
    """Add missing columns from the schema and return ordered DataFrame."""
    for col in STANDARD_SCHEMA:
        if col not in df.columns:
            df[col] = pd.NA
    return df[STANDARD_SCHEMA]

def coerce_types(df):
    numeric_cols = ["TimeDays", "AgeRng1", "AgeRng2", "GEml_conversion_intercept", "GEml_conversion_slope"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    string_cols = ["StudyID", "PersonID", "InfectionID", "SampleID", "Symptoms1", "Symptoms2", "Symptoms3", "Symptoms4", "Comorbidity1", "Comorbidity2", "Comorbidity3", "Comorbidity4", "Treatment1", "Treatment2", "Treatment3", "Treatment4", "SampleType", "Subtype", "Platform", "DOI", "Units"]
    df[string_cols] = df[string_cols].astype(str)

    return df