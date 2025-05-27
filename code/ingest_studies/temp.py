import pandas as pd
from tabulate import tabulate

df = pd.read_csv("data/ke2022.csv")

print(tabulate(df.head(12), headers="keys"))
print(tabulate(df.tail(12), headers="keys"))

df_long = df.melt(
	id_vars=[col for col in df.columns if col not in ["Nasal_CN", "Saliva_CT", "Antigen"]],
	value_vars=["Nasal_CN", "Saliva_Ct", "Antigen"],
	var_name="SampleType",
	value_name="VL"
	)

df_long["SampleType"] = df_long["SampleType"].replace({
	"Nasal_CN": "nasal",
	"Saliva_Ct": "saliva",
	"Antigen": "antigen"
	})