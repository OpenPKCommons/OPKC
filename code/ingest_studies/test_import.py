from studies import eales2025, hakki2022, jones2021, ke2022, kissler2023, puhach2022, russell2024, savela2022, vuong2024, wagstaffe2024, waickman2022, waickman2024, wongnak2024 #alpha order
from schema import enforce_schema, coerce_types
import pandas as pd

def main():
    df_to_test = vuong2024.load_and_format()

    df_to_test.to_csv("output/test_import.csv", index=False)

if __name__ == "__main__":
    main()
