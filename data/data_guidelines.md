
# Data Guidelines

This document serves as guidelines for identifying and adding future datasets which meet the goals of OPKC. This is actively developing and subject to change.

To be included, **data is required to meet _at least_ the Necessary conditions** listed below. Data should strive to meet some of the relevant conditions in Preferable. Any additional categories listed in Accepted are superfluous but worth including in later steps.

Explicit conditions may not be included in the data structure, but should be extractable from the paper. 

## Necessary

- Pathogen Information
    - Specific Pathogen
    - Measured Pathogen Load (Log10(copies/mL))
    - Units (e.g., Ct, Log10 copies/mL)
    - Platform Type (e.g., RT-qPCR)
    - Time of sample collection (in days, relative to an event)
- Individual Information
    - Identifier
    - Species
- Digital Object Identifier (DOI)


## Preferable 

- Study Identifier
- Infection Identifier
- Conversion to GE/mL (slope/intercept) if not directly measured
- Sample Information
    - Anatomical location (e.g., nose, throat)
    - Collection method (e.g., swab, wash)
- Gene Targets (e.g., N gene, S gene)
- Platform Technology (e.g., Alinity, cobas)

## Accepted

- Age Range
- Symptoms
    - Presence, absence, or description of symptom(s)
- Comorbidities
- Hospitalizations
- Treatments
- Subtype (e.g., H1N1, Omicron)
