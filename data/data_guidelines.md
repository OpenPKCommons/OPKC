
# Data Guidelines

This document serves as guidelines for identifying and adding future datasets which meet the goals of OPKC. This is actively developing and subject to change.

To be included, **data is required to meet _at least_ the Necessary conditions** listed below. Data should strive to meet some of the relevant conditions in Preferable. Any additional categories listed in Accepted are superfluous but worth including in later steps.

Explicit conditions may not be included in the data structure, but should be extractable from the paper. 

## Necessary

- Disease Identification
- Patient Identification
- Timing of each measurement for each patient
    - There should be more than one -> time series data!
- Quantity of viral material (GEml)


## Preferable 

- Conversion to GEml (slope/intercept) if not directly measured
- Sample location 
    - nose, throat, etc.

## Accepted

- Patient Information
    - Age, sex, weight, etc.
- Symptoms
    - symptom onset/timing
- Timeseries from multiple sites
- Vaccination/Booster status
    - Timing of dosages
- Previous infection date(s)
- Testing results
    - Date(s) of test(s)
    - Result(s) of test(s)
- Details of known exposure
- Secondary infections
