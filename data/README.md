# Overview
This directory contains data downloaded from the literature. Logged in "../literature/main_lit_list.md" are the data sources. As contributors identify literature, they should make sure that list is kept up to date.

Below are guidelines for selecting data to include, as well as a step-by-step workflow for ingesting data from identified sources.

# Data Guidelines

These guidelines are for adding future datasets which meet the goals of OPKC, written for OPKC contributors adding data to the OPKC repo. This is actively developing and subject to change.

Study authors may consult the necessary conditions for reference here when submitting their datasets, but please refer to the [Data Standard](https://openpkcommons.org/charts/data_standard/).

To be included, **data is required to meet _at least_ the Necessary conditions** listed below. Data should strive to meet some of the relevant conditions in Preferable. Any additional categories listed in Accepted are superfluous but worth including in later ingestion steps.

Explicit conditions may not be included in the data structure, but should be extractable from the paper.

OPKC contributors should note in main_lit_list where additional data types are available from the source paper, but may not have been initially ingested.

## Necessary

- Pathogen
- Time of sample collection (in days, relative to onset or day 0)
    - May require re-mapping from original study
    - If samples were collected from multiple individuals, some way to disambiguate different samples from different individuals needs to be clear from the source paper
- Measured Pathogen Load (in units below)
- Units (e.g., Ct, Log10 copies/mL)
- Platform Type (e.g., RT-qPCR)
- Paper Digital Object Identifier (DOI), or we will assign a study identifier
- Individual (Patient) Information
    - Identifier ID (or we will assign)
    - Species

## Preferable

- Study Identifier (or we will assign)
- Infection Identifier (e.g. to differentiate multiple infection events)
- Conversion to GE/mL (slope/intercept) if not directly measured
- Sample Information
    - Anatomical source location (e.g., nose, throat)
    - Collection method (e.g., swab, wash)
- Gene Targets (e.g., N gene, S gene)
- Platform Technology (e.g., Alinity, cobas)

## Accepted

- Age (range)
- Symptoms
    - Presence, absence, or description of symptom(s)
- Comorbidities
- Hospitalized (yes/no)
- Treatments
- Pathogen Variant or Subtype (e.g., H1N1, Omicron)

# Ingestion Workflow
Once a good source paper has been identified, OPKC team members may use the below workflow to "ingest" the data.

1. open workspace of choice (e.g. VScode)
2. set up git
	- create or checkout to your own separate ingestion branch
	- git pull from main or branch depending on recent work in branch
3. check DE paper queue in literature/main_lit_list.md 
	- choose a paper from DE category to ingest
	- to communicate to others that you're working on this ingestion and prevent duplicated efforts:
		- 1. update markdown file
		- 2. open a GitHub Issue ('Task')
4. review the paper text
	- access the paper from DOI link or shared Zotero collection: https://www.zotero.org/groups/open-pk-commons 
	- skim paper to get a sense of:
		- pathogen and subtype
		- scale of study: individuals tested over what time resolution and overall duration
		- pathogen measurement methodology: one or multiple? are conversions necessary?
		- which figure(s) is the most useful data likely to come from?
		- note if the paper references other sources we could use
			- REF tag
		- be cognizant of other tags to add - see literature README
			- XS 🌐 = cross-sectional data (may be of use for model parameters, but isn't individual-level empirical data itself)
			- sx 🤧 = symptom trajectory information
			- MA ♻️ = meta-analysis or review that combines other original data sources
			- REF = paper has references that should be scanned for data availability
			- LAB, LOD, SEQ, Ab = paper has lab data that may be useful (e.g. culture, LOD, genetic sequencing, antibodies)
			- BIN = infection status is binary, positive/negative
			- MOSP = mobility or spatial data
			- PACK = package
			- VAX = vaccination data
5. access the kinetics data
	- the bare minimum, most important things to get clear on are:
		- pathogen load or biomarker units
		- whatever assignment system is used for individual and/or sample IDs
		- time measurement
			- may need to convert to schema format of TimeDays = time in days since an infection's "time 0", or time since inoculation for challenge studies
	- then search the data and the paper for all other schema fields and fill in
	- save data in original format to OPKC/data clearly labeled with papernamestring as filename or directory name as needed
6. write your ingestion script ("papernamestring.py") in OPKC/code/ingest_studies/studies
	- make sure to include clear comments
		- paper overview
		- function definitions
		- data available in paper that may be useful for future versions of the schema but not ingested yet
			- also note this in the last column of the digested papers table in main_lit_list
	- import necessary packages (e.g. pandas, sys, Path from pathlib)
	- load raw data
	- rename, remap, calculate raw kinetics data as needed to fit our schema definitions
		- refer to repo README for updated definitions
	- assign unassigned ID fields as needed (e.g. StudyID
	- fill in other schema fields e.g. Pathogen, IndivSpecies, DOI, AssayType, Units are the most important
		- but fill in everything else you can that is known from the paper and methods text
		- check repo README for consistent formatting (e.g. for IndivSpecies, AssayType, etc.)
	- enforce schema and coerce types
	- make sure to include your own unit tests and check intermediate dataframes for correctness along the way (e.g. # %%)
7. validate your ingestion script
	- once your ingestion script correctly returns a dataframe that you think is properly formatted, add it as the df_to_test in OPKC/code/ingest_studies/test_import.py and run
	- inspect OPKC/output/test_import.csv and confirm correct schema formatting
	- edit as needed
8. once validated, add your work to the combined dataset
	- once test_import looks good, add your script to OPKC/code/ingest_studies/create_schema.py and run
	- inspect OPKC/output/combined_cleaned_data.csv and confirm correct schema formatting relative to other studies
9. update main_lit_list and repo README as needed
10. git commit
11. submit a pull request
	- if desired, have another team member look over your PR to validate ingestion
12. merge PR to main
13. close the relevant GitHub Issue 🎉 
