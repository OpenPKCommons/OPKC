import pandas as pd
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/wagstaffe2024.csv")

    # Keep only the columns we need: 
    df = df[['PersonID', 'DaysPostInoculation', 'GEml', 'site']]
    # for each individual we have 1 to 19.5 DaysPostInoculation data points with corresponding GEml (NA if not available)
    # Need to address:
    # 1. are individual IDs same for nose and throat samples or independent?
    # 2. how is GEml measured? What conversions need to be made?
    # 3. how does GEml col get converted?

    # Map the contents of column SampleType to standard names: 
    df["site"] = df["site"].replace({
        "nose": "nasal",
        "throat": "saliva" # need to confirm vs oropharyngeal
        })

    # Rename columns to match schema: 
    df = df.rename(columns={
        "PersonID": "PersonID",
        "DaysPostInoculation": "TimeDays",
        "site": "SampleType"
        })

    # Add additional columns with known but missing information:
    df["StudyID"] = "wagstaffe2024"
    df["DOI"] = "10.1016/S1473-3099(24)00183-X"
    df["Units"] = "GEml"
    # ACTIVATION TIME
        # throat: 1.78 days
        # nose: 2.61 days
    # VIRAL LOAD GROWTH RATE
        # throat: 5.41 days^-1
        # nose: 4.86 days^-1
    # PEAK TIME (ESTIMATED)
        # throat: 3.4 days
        # nose: 5.1 days
    # PEAK VIRAL LOAD
        # throat: 6.96 log_10
        # nose: 8.69 log_10
    # VIRAL LOAD DECAY RATE
        # throat: 0.69 days^-1
        # nose: 1.29 days^-1

    # df["GEml_conversion_intercept"] = df["SampleType"].map({
    #     "saliva": 0.0, # need to find!
    #     "nasal": 0.0, # need to find!
    #     })
    # df["GEml_conversion_slope"] = df["SampleType"].map({
    #     "saliva": 0.0, # need to find!
    #     "nasal": 0.0, # need to find!
    #     })

    df = enforce_schema(df)
    df = coerce_types(df)
    return df