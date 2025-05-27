def standardize_headers(df):
    rename_map = {
        "SubjectID": "id",
        "AgeYears": "age",
        "Sex": "gender",
    }
    return df.rename(columns=rename_map)
