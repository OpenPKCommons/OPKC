from studies import jones2021, puhach2022
from schema import enforce_schema, coerce_types
import pandas as pd

def main():
    #df_wongnak2024 = wongnak2024.load_and_format()
    df_to_test = puhach2022.load_and_format()
    
    #df_wongnak2024.to_csv("output/test_import.csv", index=False)
    df_to_test.to_csv("output/test_import.csv", index=False)

if __name__ == "__main__":
    main()
