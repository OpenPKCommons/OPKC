# Overview
This directory contains data downloaded from the literature. Logged in "../literature/main_lit_list.md" are the data sources. As contributors identify literature, they should make sure that list is kept up to date.

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