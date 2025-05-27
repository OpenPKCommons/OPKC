def standardize_headers(df):
    rename_map = {
        "SubjectID": "id",
        "AgeYears": "age",
        "Sex": "gender",
        # Add all mappings here
    }
    return df.rename(columns=rename_map)