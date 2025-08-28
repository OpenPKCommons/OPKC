# Overview
This directory contains data ingested from the literature. Logged in "main_lit_list.md" are the data sources. As contributors identify literature, they should make sure this list is kept up to date.

## Literature Workflow
In the "Status" column of main_lit_list, users can indicate what stage of the literature worflow a given reference is in, and either add new papers to the list or work on scanning or ingesting already identified papers.

### 1. **Identify** a candidate paper
- Check main_lit_list for the DOI to ensure that it hasn't already been processed, and if not, add it.
- Recommended avenues of search are:
    - Specific journals (e.g. Epidemics, Human Challenge Studies for Vaccine Development)
    - Authors (e.g. Christopher Chiu, works from senior authors on already identified papers)
    - Methods or topics (e.g. challange studies, epi review papers)


### 2. **Scan** paper for pathogen kinetics data to quickly determin if that data exists or not.
- Annotate in main_lit_list according to the below scheme. (Emojis are for easy labeling in Slack.)
    - DE ✅ = data exists
	- DE-NEA ✳️ = not easily accessible
	    - as in the data is clearly there at individual scale but would need to be extracted or requested
    - DME ❇️ = data may exist, worth following up more in-depth
        - as in would definitely need to request, and figures do not display individual resolution
    - NA ❎ = not applicable, not something we can use for whatever reason
    - MO 🤖 = modeling only
- A quick way to find papers with easily accessible data for us is by searching within the paper text for "github", "Zenodo" or "Dryad"
- Other metadata worth noting:
	- pathogen(s), any variant info
    - XS 🌐 = cross-sectional data (may be of use for model parameters, but isn't individual-level empirical data itself)
	- readout(s)
		- symptoms, titers, etc.
        - 🤧 = symptom trajectory information
	- time resolution and duration
		- year(s) data collected?
	- patient/participant population
	- interventions/drugs/treatments
		- e.g. challenge, neutralization, etc.
	- any infection or transmission data?
	- study design/sampling notes
	- first and relevant senior authors

### 3. **Ingest** the data from that source and save it to this directory
- Any papers with status Scanned: DE can be immediately ingested. Other designations will need more work.

## Challenges and nuances of note
- identifying empirical vs. modeled data
- want to capture linkages between papers
	- e.g. modeling papers based on empirical data
- papers with many authors can be challenging to identify who the senior author is to seed future searches on