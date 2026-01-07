# Open Pathogen Kinetics Commons: the viral kinetics database

This repository contains software to combine data from multiple studies into a single viral kinetics database. 

## Quick start

### Virtual environment setup (once)
This project uses `venv` to manage package versions. After cloning this project to your local machine, navigate to the root directory (`OPKC/`) and run the following from the command line: 

`$ python3 -m venv venv`

Next, activate the virtual environment: 

`source venv/bin/activate`

Install all the required packages from the `requirements.txt` file: 

`pip install -r requirements.txt`

Last (important!!), add `venv/` and `.env` to your `.gitignore` file (create one in your local `gvkl/` directory if you don't have one yet) 

```
# .gitignore
venv/
.env
```

### Virtual environment management (every time you open the code) 

Be sure to re-activate the virtual environment: 

`source venv/bin/activate`

### Data processing 

To ingest the data, format it, and generate the database, run 

```
$ python3 code/ingest_studies/create_schema.py
```

A helper script for testing the ingestion of individual studies before integrating them into the full database is also available: 

```
$ python3 code/ingest_studies/test_import.py
```

## Phase I progress

### Ingesting studies 

```mermaid
graph LR
	inbox[Inbox: 23]
	mayexist[May exist: 45]
	denea[Exists - not easy to access: 18]
	exists[Exists: 9]
	provingest[Provisional ingest: 2]
	ingested[Ingested: 20]
	exists --> provingest --> ingested
```

### Schema

#### Fields and definitions
- StudyID: A unique identifier for the study from which the data comes
- IndivID: A unique individual identifier
- Pathogen: ["SARS2", "Flu", "Dengue", "WestNile"]
    - Prefer shortest cleanest, high-level term
    - Keep track of naming quirks here for consistency
- IndivSpecies: Spcies (corresponding to the individual subject of study) e.g. human, dairy cattle
    - Use naming convention per the paper or simple common name, rather than scientific names
- InfectionID: A unique infection identifier (in case multiple infections in a single person, as needed)
- SampleID: An identifier for the biological sample
- TimeDays: Time in days since the infection's "time 0"
    - or, for challenge studies, time since inoculation
- Symptoms1: Symptom ICD code 1 OR granular symptomatic vs. asymptomatic data depending on the original study's level of detail
- Symptoms2: Symptom ICD code 2
- Symptoms3: Symptom ICD code 3
- Symptoms4: Symptom ICD code 4
- Comorbidity1: Comorbidity ICD code 1
- Comorbidity2: Comorbidity ICD code 2
- Comorbidity3: Comorbidity ICD code 3
- Comorbidity4: Comorbidity ICD code 4
- Treatment1: CPT code of treatment 1
- Treatment2: CPT code of treatment 2
- Treatment3: CPT code of treatment 3
- Treatment4: CPT code of treatment 4
- Hospitalized: Was the patient hospitalized?
- SampleSource: Anatomical source of sample (e.g., saliva, nose/anterior nares, nasopharyngeal), formerly SampleType - e.g. the thing in the tube that goes in analysis machine
	-Note: NP = nasopharyngeal, OP = oropharyngeal, MT = mid-turbinate, AN = anterior nares (all these are different! NP is most invasive, AN is least)
	- reasonable to say nose = anterior nares and throat = OP, but better to use study terminology than to rename
- SampleMethod: Type of sample, medium if relevant (e.g., swab, raw saliva, buffered saliva, VTM)
- AgeRng1: Lower end of the patient's age bracket
- AgeRng2: Upper end of the patient's age bracket
- PathogenSubtype: Pathogen subtype/strain/variant
- AssayType: Analytical test assay or platform type (e.g. RT-qPCR, plaque-forming assay, antibody titer)
- DOI: DOI of the study or data repository
- BiomarkerQuantity: Viral load or other pathogen or immune biomarker quantitation or measurement (most commonly will be log10 viral load - but need to specify!)
    - Formerly "PathogenLoad"
- Units: Pathogen load/biomarker quantity units (e.g., Ct, GE/ml)
- Biomarker: Indicate which biomarker is being measured, if not some form of the pathogen (e.g. an immune marker, gene expression, etc.)
- Ct_max: For Ct values, best practice is to include the maximum number of cycles which papers should report (is often, but not always, 40) - report separately here
- GEml_conversion_intercept: Conversion intercept from viral load units to - GE/ml
- GEml_conversion_slope: Conversion slope from viral load units to GE/ml
- AssayTargets: Assay target(s) e.g. amplification of N1 gene (comma-separated string, not a list)
- ReagentSystem: Refers to assay kit or any reagents used in the lab (e.g. Luna qPCR kit)
    - Formerly recorded in PlatformTech
- ReadoutPlatform: Assay readout manufacturer or machine info (e.g. Roche cobas, Taqpath, BioRad CFX Maestro)
    - Formerly recorded in PlatformTech

#### ID Assignments

TBD

##### StudyID

For v1: firstauthorYear

##### PersonID

For v1: from study

##### InfectionID

Leave blank/TBD

##### SampleID

Leave blank/TBD or from study

## Phase II Work Plan

### Relational Database Structure 

Entity Relationship Diagram

```mermaid
erDiagram
    direction LR
    STUDY ||--|{ SAMPLE : includes
    STUDY ||--|{ INFECTION : includes
    SAMPLE ||--|{ INFECTION : characterizes
    SAMPLE }|--|{ PLATFORM : analyzed
    STUDY {
        string StudyID PK
        string Title
        string FirstAuthor
        string DOI
        date Year
        link DataURL
    }
    SAMPLE {
        string SampleID PK
        string PatientID
        string InfectionID FK
        string PlaformID FK
        string StudyID FK
        string PtSpecies
        int TimeDays
        string SampleSource
        string SampleMethod
        float PathogenLoad
    }
    INFECTION {
        string InfectionID PK
        string PersonID
        string StudyID FK
        string SampleID FK
        string Pathogen
        string Subtype
        int AgeBound1
        int AgeBound2
        string Symptom1
        string Symptom2
        string Symptom3
        string Symptom4
        string Comorbid1
        string Comorbid2
        string Comorbid3
        string Comorbid4
        string Treatment1
        string Treatment2
        string Treatment3
        string Treatment4
        bool Hospitalized
        bool Died
    }
    PLATFORM {
        string PlatformID PK
		string PlatformType
		string PlatformTech
        string Units
        float ConversionIntercept
        float ConversionSlope
        float GEml_conv_int
        float GEml_conv_slope
        float LOD
        string Targets
    }
```

<!--
Here's a provisional entity relationship diagram: 
![An entity relationship diagram for the OpenPKCommons](figures/ERD.png)
-->

### Web app architecture 

