# van Kampen 2021
# Data source (source data): https://www-nature-com.colorado.idm.oclc.org/articles/s41467-020-20568-4#Sec12

# Column names of van Kampen 2021 data for reference
# duration of symptoms in days , RNA copies per mL , PRNT titer , virus culture result
# NEED TO ADD individual identification added based on days since infection below (129 indiv from 690 samples!)
# data from respiratory samples

import pandas as pd
from schema import enforce_schema, coerce_types

def load_and_format():
    # Import the raw data:
    df = pd.read_csv("data/vanKampen2021.csv")

    # Keep only the columns we need: 
    df = df[['duration of symptoms in days', 'RNA copies per mL']] # replaced if using code section below
#####################################################################################################################################################
# Implementation of individual identification based on days since infection. There should be 129 individuals but this currently reports 154...
    i = 1
    ##df = df[['duration of symptoms in days', 'RNA copies per mL', 'virus culture result']]
    df['indvID'] = i

    # Identify where the current value is less than the previous value
    condition = df['duration of symptoms in days'] < df['duration of symptoms in days'].shift(1)
    
    # Loop through condition to append indvID
    for j in range(len(df)):
        if condition[j] == True:
            i = i + 1
            df.loc[j, 'indvID'] = i
        elif condition[j] == False:
            df.loc[j, 'indvID'] = i
           next
        else:
          print("ERROR in condition")
        
# code to check if each individual reports a positive result to help resolve 154 > 129 -> unclear if that is an additional requirement...
        # need to include 'virus culture result' if using this section
    # result_lists = (
    #     df.groupby("indvID")["virus culture result"]
    #         .apply(list)
    #         .reset_index(name="culture_result_list")
    # )
    # print(result_lists) # provides every individual and a list of their results
    # pos_summary = (
    #     df.groupby("indvID")["virus culture result"]
    #         .apply(lambda s: pd.Series({
    #             "contains_POS": "POS" in set(s),
    #             "num_POS": (s == "POS").sum()
    #         }))
    #         .reset_index()
    # )
    # print(pos_summary) # provides whether each individual had a positive result in their list and how many
#####################################################################################################################################################

    # Rename columns to match schema: 
    df = df.rename(columns={
        "indvID": "PersonID",
        "duration of symptoms in days": "TimeDays",
        "RNA copies per mL": "PathogenLoad"
        })
    
    # Add additional columns with known but missing information:
    df["StudyID"] = "vanKampen2021"
    df["Pathogen"] = "SARS2"
    df["IndSpecies"] = "Human"
    df["Units"] = "GEml (log10VL)" # RNA copies
    df["DOI"] = "10.1038/s41467-020-20568-4"
    # from sample processing and analysis section
    df["PlatformType"] = "RT-qPCR" 
    df["PlatformTech"] = "Roche cobas 6800/" 
    df["Targets"] = "E-gene" 

    df = enforce_schema(df)
    df = coerce_types(df)
    return df