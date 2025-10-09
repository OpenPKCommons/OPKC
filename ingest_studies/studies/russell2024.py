import pandas as pd
from ..schema import enforce_schema, coerce_types, split_age_range

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/russell2024.csv")

    # Keep only the columns we need: 
    df = df[['id', 'swab_type', 'VOC', 'symptoms', 'symptom_onset_date', 't', 'age_group', 'ct_type', 'ct_value']]

    # Format the age group column into separate age ranges: 
    df["AgeRng1"] = df["age_group"].map({
        "20-34": 20,
        "35-49": 35,
        "50+": 50
        })
    df["AgeRng2"] = df["age_group"].map({
        "20-34": 34,
        "35-49": 49,
        "50+": 100
        })

    # Convert to numeric
    df["AgeRng1"] = pd.to_numeric(df["AgeRng1"], errors="coerce")
    df["AgeRng2"] = pd.to_numeric(df["AgeRng2"], errors="coerce")

    # Add the platform: 
    df["Platform"] = df["ct_type"].map({
        "ct_value": "Crick COVID-19 Consortium (CCC) ORF1ab",
        "ct_n_gene": "Crick COVID-19 Consortium (CCC) N gene",
        "ct_s_gene": "Crick COVID-19 Consortium (CCC) S gene"
        })

    # Rename columns to match schema: 
    df = df.rename(columns={
        "id": "PersonID",
        # "swab_type": "SampleType",
        "VOC": "Subtype",
        "symptoms": "Symptoms1",
        "t": "TimeDays",
        "ct_value": "Log10VL"
        })

    # df = split_age_range(df, col="age_group")

    # Add additional columns with known but missing information:
    df["StudyID"] = "russell2024"
    df["DOI"] = "10.1371/journal.pbio.3002463"
    df["Units"] = "Ct"
    df["SampleType"] = "nasopharyngeal"
    # df["SampleType"] = "nasopharyngeal"
    # df["Platform"] = df["SampleType"].map({
    #     "saliva": "Taqpath",
    #     "nasal": "Alinity",
    #     "antigen": "Sofia"
    #     })
    # df["GEml_conversion_intercept"] = df["SampleType"].map({
    #     "saliva": 14.24,
    #     "nasal": 11.35,
    #     })
    # df["GEml_conversion_slope"] = df["SampleType"].map({
    #     "saliva": -0.28,
    #     "nasal": -0.25,
    #     })

    df = enforce_schema(df)
    df = coerce_types(df)
    return df