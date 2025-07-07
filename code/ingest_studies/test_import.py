from studies import ke2022, kissler2023, russell2024, wagstaffe2024, wongnak2024
from schema import enforce_schema, coerce_types
import pandas as pd

def main():
    df_russell2024 = russell2024.load_and_format()
    
    df_russell2024.to_csv("output/test_import.csv", index=False)

if __name__ == "__main__":
    main()
