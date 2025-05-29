from studies import ke2022, kissler2023, russell2024, wagstaffe2024, wongnak2024
from schema import enforce_schema, coerce_types
import pandas as pd

def main():
    df_ke2022 = ke2022.load_and_format()
    df_kissler2023 = kissler2023.load_and_format()
    # df_russell2024 = russell2024.load_and_format()
    # df_wagstaffe2024 = wagstaffe2024.load_and_format()
    # df_wongnak2024 = wongnak2024.load_and_format()

    # combined_df = pd.concat([df_ke2022, df_kissler2023, df_russell2024, df_wagstaffe2024, df_wongnak2024])
    # combined_df = df_ke2022
    combined_df = pd.concat([df_ke2022, df_kissler2023])
    combined_df.to_csv("output/combined_cleaned_data.csv", index=False)

if __name__ == "__main__":
    main()
