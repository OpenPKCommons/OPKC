# 23 May 2025
Our first step is to gather a few viral kinetics databases and try to come up with a schema that accommodates them. 

Here are the ones we'll start with: 

- [**Daily longitudinal sampling of SARS-CoV-2 infection reveals substantial heterogeneity in infectiousness**](https://www.nature.com/articles/s41564-022-01105-z) (Ke *et al.* 2022) [Data](https://static-content.springer.com/esm/art%3A10.1038%2Fs41564-022-01105-z/MediaObjects/41564_2022_1105_MOESM4_ESM.xlsx)
- [**Viral kinetics of sequential SARS-CoV-2 infections**](https://www.nature.com/articles/s41467-023-41941-z) (Kissler *et al.* 2023) [Data](https://github.com/skissler/Ct_SequentialInfections/blob/main/data/ct_dat_refined.csv)
- [**Combined analyses of within-host SARS-CoV-2 viral kinetics and information on past exposures to the virus in a human cohort identifies intrinsic differences of Omicron and Delta variants**](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3002463) (Russell *et al.* 2024) [Data](https://github.com/thimotei/legacy_ct_modelling/tree/main/data_inference)
- [**Temporal changes in SARS-CoV-2 clearance kinetics and the optimal design of antiviral pharmacodynamic studies: an individual patient data meta-analysis of a randomised, controlled, adaptive platform study (PLATCOV)**](https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(24)00183-X/fulltext) (Wongnak *et al.* 2024) [Data](https://github.com/jwatowatson/Determinants-viral-clearance)
- [**Mucosal and systemic immune correlates of viral control after SARS-CoV-2 infection challenge in seronegative adults**](https://www.science.org/doi/10.1126/sciimmunol.adj9285) (Wagstaffe *et al.* 2024) [Data](https://www.science.org/doi/suppl/10.1126/sciimmunol.adj9285/suppl_file/sciimmunol.adj9285_data_file_s1.zip)

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
- **VL:** log10 Viral load 
- **Units:** Viral load units (*e.g.*, Ct, GE/ml)
- **GEml_conversion_intercept:** Conversion intercept from viral load units to GE/ml
- **GEml_conversion_slope:** Conversion slope from viral load units to GE/ml


# 27 May 2025

I'm working today on building the ingestion code -- something to take in the different studies and create a rough schema based on their contents. 

So far, this is saved as a directory: `code/ingest_studies/`, where the main file is `create_schema.py`. The study-specific ingestion code is in the `studies/` directory/package, and I'm going to develop some code in `shchema.py` to map the original column names to the schema-specific ones. The files within `studies/` will also need to do some re-shaping. 

A note -- I've replaced the Katz study with Wongnak2024 (the PLATCOV study). I was having trouble finding a public release of the nursing home data from Katz (the epidemiological data is there, but the viral kinetics data doesn't seem to be linked); and I think there may be value in including data that comes from a clinical trial. 

# 29 May 2025 

I've gotten some code running to ingest the Ke2022 study. Right now, the ingestion code for the remaining studies are copies of this one. Next, I want to ingest the code from our "sequential infections" study (Kissler2023). 

(Also -- I've created a Streamlit app to visualize the viral kinetics data, and it's working ok. That's in a separate directory right now, but I'll likely merge it over into this one soon.) 

Here are the headers in the raw data: 

- PersonID
- InfectionEvent
- TestDateIndex
- CtT1
- AgeGrp
- VaccinationStatus
- BoosterStatus
- InterveningDose
- LineageBroad
- InfNum
- NInf
- PrevLineageBroad
- NextLineageBroad
- RowID
- InPairedAnalysis

That's in; now I'm going to work on bringing in the dataset from Russell2024. 

Here are the headings: 

- id
- infection_id
- swab_date
- swab_type
- ct_unadjusted
- result
- VOC
- symptoms
- symptom_onset_date
- total_infections
- no_vaccines
- date_dose_1
- date_dose_2
- date_dose_3
- date_dose_4
- uncensored
- no_pos_results
- first_pos_test_date
- t_since_first_pos
- t
- onset_time
- no_exposures
- age_group
- ct_type
- ct_value
- t_since_last_dose
- t_first_inf_by_id
- t_first_inf_to_cur_inf
- t_since_last_exposure
- t_first_test
- data_id
- swab_type_num


# 7 July 2025

To create the schema: 

`$ python3 code/ingest_studies/create_schema.py`

Working more now on getting russell imported: 

I think we need the following columns: 


| russell              | schema            |
|----------------------|-------------------|
| id                   | PersonID          |
| ct_value             | Log10VL           |
| VOC                  | Subtype           |
| symptoms             | Symptoms          |
| symptom_onset_date   | Symptoms          |
| t                    | TimeDays          |
| age_group            | AgeRng1, AgeRng2  |
| ct_type              | Platform          |
| swab_type            | SampleType        |

I need to figure out exactly how the ct_value is calculated (from ct_unadjusted); it removes the na values, but also has some proper numerical adjustments to the ct values for the n- and s-gene targets. 

For symptoms, I'll have to extract the timing. I also need to think about how to deal with 'symptomatic' as a category, without any specification of the actual symptoms. 

We'll want to create 'SampleID' as a new index column. It's unclear, though, whether we're dealing with the same sample run in multiple ways (dry vs vtm, overall vs s vs n targets) or with different samples. I think probably the same sample. 

More broadly: we need to specify which are the index columns. It seems like we could get some conflicts: we might have the same swab run on multiple targets, or different swabs on different targets but on the same day; or different swabs run on the same target. This needs some thought. 





