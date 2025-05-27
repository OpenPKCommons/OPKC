from studies import study1, study2, study3
from schema import standardize_headers
import pandas as pd

def main():
    df1 = study1.load_and_format()
    df2 = study2.load_and_format()
    df3 = study3.load_and_format()

    combined_df = pd.concat([df1, df2, df3])
    combined_df.to_csv("combined_cleaned_data.csv", index=False)

if __name__ == "__main__":
    main()
