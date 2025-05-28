# from studies import study1, study2, study3
from studies import ke2022, kissler2023, russell2024, wagstaffe2024, wongnak2024
from schema import enforce_schema, coerce_types
import pandas as pd

def main():
    df1 = ke2022.load_and_format()
    # df2 = kissler2023.load_and_format()
    # df3 = russell2024.load_and_format()
    # df4 = wagstaffe2024.load_and_format()
    # df5 = wongnak2024.load_and_format()

    # combined_df = pd.concat([df1, df2, df3])
    combined_df = df1
    combined_df.to_csv("output/combined_cleaned_data.csv", index=False)

if __name__ == "__main__":
    main()
