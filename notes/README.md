# 23 May 2025
Our first step is to gather a few viral kinetics databases and try to come up with a schema that accommodates them. 

Here are the ones we'll start with: 

- [**Daily longitudinal sampling of SARS-CoV-2 infection reveals substantial heterogeneity in infectiousness**](https://www.nature.com/articles/s41564-022-01105-z) (Ke *et al.*) [Data](https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-022-01105-z/MediaObjects/41564_2022_1105_MOESM4_ESM.xlsx)
- [**Viral kinetics of sequential SARS-CoV-2 infections**](https://www.nature.com/articles/s41467-023-41941-z) (Kissler *et al.*) [Data](https://github.com/skissler/Ct_SequentialInfections/blob/main/data/ct_dat_refined.csv)
- [**Combined analyses of within-host SARS-CoV-2 viral kinetics and information on past exposures to the virus in a human cohort identifies intrinsic differences of Omicron and Delta variants**](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3002463) (Russell *et al.*) [Data](https://github.com/thimotei/legacy_ct_modelling/tree/main/data_inference)
- [**Kinetics of SARS-CoV-2 Shedding in Nursing Home Residents and Staff**](https://agsjournals.onlinelibrary.wiley.com/doi/full/10.1111/jgs.19499) (Katz *et al.*) [Data](https://data.cms.gov/covid-19/covid-19-nursing-home-data)
- [**Mucosal and systemic immune correlates of viral control after SARS-CoV-2 infection challenge in seronegative adults**](https://www.science.org/doi/10.1126/sciimmunol.adj9285) (Wagstaffe *et al.*) [Data](https://www.science.org/doi/suppl/10.1126/sciimmunol.adj9285/suppl_file/sciimmunol.adj9285_data_file_s1.zip)

Here are the headings we'll start with: 

- **StudyID:** A unique identifier for the study from which the data comes
- **PersonID:** A unique person identifier
- **InfectionID:** A unique infection identifier (in case multiple infections in a single person)
- **SampleID:** An identifier for the biological sample 
- **TimeDays:** Time in days since the infection's "time 0" 
- **Symptoms1:** Symptom ICD code 1
- **Symptoms2:** Symptom ICD code 2
- **Symptoms3:** Symptom ICD code 3
- **Symptoms4:** Symptom ICD code 4
- **Comorbidity1:** Comorbidity ICD code 1
- **Comorbidity2:** Comorbidity ICD code 2
- **Comorbidity3:** Comorbidity ICD code 3
- **Comorbidity4:** Comorbidity ICD code 4
- **Treatment1:** CPT code of treatment 1
- **Treatment2:** CPT code of treatment 2
- **Treatment3:** CPT code of treatment 3
- **Treatment4:** CPT code of treatment 4
- **Hospitalized:** Was the patient hospitalized? 
- **SampleType:** Sample type (*e.g.*, saliva, nasal swab)
- **AgeRng1:** Lower end of the patient's age bracket
- **AgeRng2:** Upper end of the patient's age bracket
- **Subtype:** Pathogen subtype 
- **Platform:** Test platform
- **DOI:** DOI of the study or data repository 
- **VL:** Viral load 
- **Units:** Viral load units (*e.g.*, Ct, GE/ml)
- **GE_ml_conversion:**: Conversion factor from viral load units to GE/ml


# 27 May 2025

I'm working today on building the ingestion code -- something to take in the different studies and create a rough schema based on their contents. 

So far, this is saved as a directory: `code/ingest_studies/`, where the main file is `create_schema.py`. The study-specific ingestion code is in the `studies/` directory/package, and I'm going to develop some code in `shchema.py` to map the original column names to the schema-specific ones. The files within `studies/` will also need to do some re-shaping. 















