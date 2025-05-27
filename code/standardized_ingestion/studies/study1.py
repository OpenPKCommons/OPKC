import pandas as pd
from schema import standardize_headers

def load_and_format():
    # Replace with the actual path to your dataset
    df = pd.read_excel("data/study1_data.xlsx")
    df = standardize_headers(df)
    return df
