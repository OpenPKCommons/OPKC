# Open Pathogen Kinetics Commons: the viral kinetics database

This repository contains software to combine data from multiple studies into a single viral kinetics database. 

## Quick start

To ingest the data, format it, and generate the database, run 

```
$ python3 code/ingest_studies/create_schema.py
```

A helper script for testing the ingestion of individual studies before integrating them into the full database is also available: 

```
$ python3 code/ingest_studies/test_import.py
```

