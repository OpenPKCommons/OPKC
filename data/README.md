# Overview
This directory contains data downloaded from the literature. Logged in "main_lit_list.md" are the data sources. As contributors identify literature, they should make sure this list is kept up to date.

## Literature Workflow
In the "Status" column of main_lit_list, collaborators can indicate what stage of the literature worflow a given reference is in, and either add new papers to the list or work on scanning or ingesting already identified papers, and create a github Issue to indicate work in progress.

### 1. **Identify** a candidate paper
- Check main_lit_list for the DOI to ensure that it hasn't already been processed, and if not, add it.
- Recommended avenues of search are:
    - Specific journals (e.g. Epidemics, Human Challenge Studies for Vaccine Development)
    - Authors (e.g. Christopher Chiu, works from senior authors on already identified papers)
    - Methods or topics (e.g. challange studies, epi review papers)

### 2. **Scan** paper for pathogen kinetics data to quickly determine if that data exists or not.
- Annotate in main_lit_list according to the below scheme. (Emojis are for easy labeling in Slack.)
    - DE ✅ = data exists
	- DE-NEA ✳️ = not easily accessible
	    - as in the data is clearly there at individual scale but would need to be extracted or requested
    - DME ❇️ = data may exist, worth following up more in-depth
        - as in would definitely need to request, and figures do not display individual resolution
		- this is more work than DE-NEA
		- * an asterisk denotes that this data seems especially difficult to track down
    - NA ❎ = not applicable, not something we can use for whatever reason
    - MO 🤖 = modeling only
    - DAI = data already included
    	- e.g. data from this source has already been included as part of another dataset
    	- these references are recorded to prevent redundant scanning
	- For other metadata worth flagging (e.g. pathogen, cross-sectional data, meta-analysis, lab data, spatial data, etc.), use tags. Refer to [main_lit_list.md] for tags in use.

### 3. **Ingest** the data from that source by saving it to this directory, then creating a script in ingest_studies/studies that formats it according to our schema.
- Any papers with status Scanned: DE can be immediately ingested. Other designations will need more work.
- A paper is marked as **digested** when this has been done and it has been added to our database with create_schema.py

## Challenges and nuances of note
- identifying empirical vs. modeled data
- want to capture linkages between papers
	- e.g. modeling papers based on empirical data
- papers with many authors can be challenging to identify who the senior author is to seed future searches on