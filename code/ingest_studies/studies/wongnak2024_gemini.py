import pandas as pd
from schema import enforce_schema, coerce_types

def load_and_format():
    """
    Loads the Wongnak 2024 dataset, wrangles it into the standard schema,
    and returns a clean DataFrame.
    """
    # Import the raw data:
    # Assuming the data is in a 'data' subdirectory.
    try:
        df = pd.read_csv("wongnak2024.csv")
    except FileNotFoundError:
        df = pd.read_csv("data/wongnak2024.csv")

    # Keep only the columns we need for the final schema:
    df = df[['ID', 'Time', 'Variant', 'Age', 'Trt', 'Swab_ID', 'CT_NS', 'log10_viral_load']]

    # Pivot the two viral load measurement columns (CT and log10) into a single column.
    # This creates a 'MeasurementType' column we can use to assign Units and Platform.
    df = df.melt(
        id_vars=['ID', 'Time', 'Variant', 'Age', 'Trt', 'Swab_ID'],
        value_vars=['CT_NS', 'log10_viral_load'],
        var_name="MeasurementType",
        value_name="Log10VL"
        )

    # Remove rows where the viral load measurement is missing
    df = df.dropna(subset=['Log10VL'])

    # Assign Units and Platform based on the original measurement column
    df['Units'] = df['MeasurementType'].map({
        'CT_NS': 'Ct',
        'log10_viral_load': 'log10_copies_swab'
        })
    df['Platform'] = df['MeasurementType'].map({
        'CT_NS': 'RT-qPCR (NS gene)',
        'log10_viral_load': 'RT-qPCR'
        })

    # Clean up the Swab_ID to create a standardized SampleType
    # e.g., 'Left_tonsil_1' becomes 'tonsil'
    df['SampleType'] = df['Swab_ID'].str.lower().str.replace(r'(_\d+|left_|right_)', '', regex=True)

    # Rename columns to match the standard schema:
    df = df.rename(columns={
        "ID": "PersonID",
        "Time": "TimeDays",
        "Variant": "Subtype",
        "Age": "AgeRng1",
        "Trt": "Treatment1"
        })

    # Since age is given as a single value, set the upper bound of the age range to be the same
    df['AgeRng2'] = df['AgeRng1']

    # Add additional columns with known but missing information:
    df["StudyID"] = "wongnak2024"
    df["DOI"] = "10.1038/s41467-024-47481-z"

    # Coerce data types to match the schema definitions
    df = coerce_types(df)

    # Add any missing columns from the standard schema and ensure correct column order
    df = enforce_schema(df)

    return df

if __name__ == '__main__':
    # This block allows you to run the script directly for testing
    formatted_df = load_and_format()
    print("Successfully formatted Wongnak 2024 data.")
    print(formatted_df.head())
    print("\nDataFrame Info:")
    formatted_df.info()
