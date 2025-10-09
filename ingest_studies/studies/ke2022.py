import pandas as pd
from ..schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/ke2022.csv")

    # Keep only the columns we need: 
    df = df[['Ind', 'Time', 'Lineage', 'Nasal_CN', 'Saliva_Ct', 'Antigen', 'Age']]

    # Clean up the Ind column: 
    df["Ind"] = df["Ind"].str.replace(r"\s*\*", "", regex=True)

    # Pivot the test outcome columns into a single column: 
    df = df.melt(
        id_vars=[col for col in df.columns if col not in ["Nasal_CN", "Saliva_Ct", "Antigen"]],
        value_vars=["Nasal_CN", "Saliva_Ct", "Antigen"],
        var_name="SampleType",
        value_name="Log10VL"
        )

    # Map the contents of column SampleType to standard names: 
    df["SampleType"] = df["SampleType"].replace({
        "Nasal_CN": "nasal",
        "Saliva_Ct": "saliva",
        "Antigen": "antigen"
        })

    # Rename columns to match schema: 
    df = df.rename(columns={
        "Ind": "PersonID",
        "Time": "TimeDays",
        "Lineage": "Subtype",
        "Age": "AgeRng1"
        })

    # Add additional columns with known but missing information:
    df["StudyID"] = "ke2022"
    df["AgeRng2"] = df["AgeRng1"]
    df["DOI"] = "10.1038/s41564-022-01105-z"
    df["Units"] = df["SampleType"].map({
        "saliva": "Ct",
        "nasal": "Ct",
        "antigen": "binary"
        })
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