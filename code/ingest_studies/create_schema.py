from studies import alahakoon2025
from studies import eales2025
from studies import hakki2022
from studies import jones2021
from studies import ke2022
from studies import kissler2023
from studies import kucirka2020
from studies import puhach2022
from studies import russell2024
from studies import savela2022
from studies import wagstaffe2024
from studies import waickman2022
from studies import waickman2024
from studies import wongnak2024


from schema import enforce_schema, coerce_types
import pandas as pd

def main():
    df_alahakoon2025 = alahakoon2025.load_and_format()
    df_eales2025 = eales2025.load_and_format()
    df_hakki2022 = hakki2022.load_and_format()
    df_jones2021 = jones2021.load_and_format()
    df_ke2022 = ke2022.load_and_format()
    df_kissler2023 = kissler2023.load_and_format()
    df_kucirka2020 = kucirka2020.load_and_format()
    df_puhach2022 = puhach2022.load_and_format()
    df_russell2024 = russell2024.load_and_format()
    df_savela2022 = savela2022.load_and_format()
    df_wagstaffe2024 = wagstaffe2024.load_and_format()
    df_waickman2022 = waickman2022.load_and_format()
    df_waickman2024 = waickman2024.load_and_format()
    df_wongnak2024 = wongnak2024.load_and_format()


    combined_df = pd.concat([
        df_alahakoon2025,
        df_eales2025,
        df_hakki2022,
        df_jones2021,
        df_ke2022,
        df_kissler2023,
        df_kucirka2020,
        df_puhach2022,
        df_russell2024,
        df_savela2022,
        df_wagstaffe2024,
        df_waickman2022,
        df_waickman2024,
        df_wongnak2024
        ])
    combined_df.to_csv("output/combined_cleaned_data.csv", index=False)

if __name__ == "__main__":
    main()
