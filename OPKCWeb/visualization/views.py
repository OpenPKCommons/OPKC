# visualization/views.py

from django.shortcuts import render
from django.http import HttpResponse
from functools import lru_cache
import os
import pandas as pd
import json
import random # <-- 1. IMPORT THE RANDOM MODULE

# Define the absolute path to the base directory of the Django project (OPKCWeb)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Repo root is one directory above the Django project
REPO_ROOT = os.path.dirname(BASE_DIR)

# The site reads the *published* CSV in output/. See output/README.md for the
# staged-vs-published workflow.
DATA_FILE_PATH = os.path.join(REPO_ROOT, 'output', 'combined_cleaned_data_published.csv')


# ---------------------------------------------------------------------------
# Data caching
#
# Reading and munging the published CSV on every request is wasteful. Instead,
# we cache the *computed* results (home-page stats + chart context) keyed by
# the CSV's mtime. When the published CSV changes on disk, the mtime changes,
# the cache key changes, and the next request naturally recomputes. No server
# restart needed after publishing new data; no Django cache backend required.
# ---------------------------------------------------------------------------

def _data_mtime():
    """Cache key: the mtime of the published CSV, or 0 if missing."""
    try:
        return os.path.getmtime(DATA_FILE_PATH)
    except OSError:
        return 0


@lru_cache(maxsize=2)
def _compute_home_stats(mtime):
    df = pd.read_csv(DATA_FILE_PATH, na_values=['<NA>'])
    # Count distinct (StudyID, IndivID) pairs so that per-study IDs like "1", "2"
    # don't collide across studies. Rows with no IndivID contribute nothing.
    unique_people = (
        df[['StudyID', 'IndivID']]
        .dropna(subset=['IndivID'])
        .drop_duplicates()
        .shape[0]
    )
    return {
        'total_data_points': f"{len(df):,}",
        'total_studies': f"{df['StudyID'].nunique():,}",
        'total_pathogens': f"{df['Pathogen'].nunique():,}",
        'total_people': f"{unique_people:,}",
    }


def _blod_label(v):
    """Map raw BelowLOD values (True / False / NA, possibly as strings after CSV
    round-trip) to user-facing display labels."""
    if pd.isna(v):
        return 'Unspecified'
    s = str(v).strip().lower()
    if s == 'true':
        return 'Below LOD'
    if s == 'false':
        return 'Detected'
    return 'Unspecified'


@lru_cache(maxsize=2)
def _compute_chart_context(mtime):
    df = pd.read_csv(DATA_FILE_PATH, na_values=['<NA>'])
    df['BelowLOD'] = df['BelowLOD'].apply(_blod_label)

    study_ids = sorted(df['StudyID'].dropna().unique().tolist())
    sample_types = sorted(df['SampleSource'].dropna().unique().tolist())
    pathogens = sorted(df['Pathogen'].dropna().unique().tolist())
    subtypes = sorted(df['PathogenSubtype'].dropna().unique().tolist())
    biomarkers = sorted(df['Biomarker'].dropna().unique().tolist())
    blod_statuses = sorted(df['BelowLOD'].dropna().unique().tolist())

    plot_columns = ['StudyID', 'SampleSource', 'TimeDays', 'BiomarkerQuantity',
                    'AgeRng1', 'AgeRng2', 'Pathogen', 'PathogenSubtype',
                    'Biomarker', 'BelowLOD', 'Units']
    core_plot_cols = ['StudyID', 'SampleSource', 'TimeDays', 'BiomarkerQuantity', 'Pathogen']
    df_plot = df[plot_columns].dropna(subset=core_plot_cols, how='any')
    df_plot = df_plot.astype(object).where(pd.notnull(df_plot), None)

    # Report silently-dropped rows so we notice when a study disappears from the
    # chart (e.g. because an ingest script forgot to set SampleSource). Grouped
    # by study, with a per-column breakdown so the cause is visible at a glance.
    dropped = len(df) - len(df_plot)
    if dropped:
        excluded = df[df[core_plot_cols].isna().any(axis=1)]
        print(f"[chart] dropped {dropped:,} of {len(df):,} rows for missing core columns")
        for study, g in excluded.groupby('StudyID'):
            reasons = {c: int(g[c].isna().sum()) for c in core_plot_cols if g[c].isna().any()}
            print(f"  {study}: {len(g):,} rows dropped -> {reasons}")

    return {
        'study_ids': study_ids,
        'sample_types': sample_types,
        'pathogens': pathogens,
        'subtypes': subtypes,
        'biomarkers': biomarkers,
        'blod_statuses': blod_statuses,
        'all_data': df_plot.to_dict(orient='records'),
    }

# --- 2. DEFINE YOUR FEATURED PAPERS ---
# (This section is unchanged)
FEATURED_PAPERS_LIST = [
    {
        'title': 'Daily longitudinal sampling of SARS-CoV-2 infection reveals substantial heterogeneity in infectiousness',
        'image_name': 'ke2022.png',
        'url': 'https://doi.org/10.1038/s41564-022-01105-z'
    },
    {
        'title': 'Combined analyses of within-host SARS-CoV-2 viral kinetics and information on past exposures to the virus in a human cohort identifies intrinsic differences of Omicron and Delta variants',
        'image_name': 'russell2024.png',
        'url': 'https://doi.org/10.1371/journal.pbio.3002463'
    },
    {
        'title': 'Viral kinetics of sequential SARS-CoV-2 infections',
        'image_name': 'kissler2023.png',
        'url': 'https://doi.org/10.1038/s41467-023-41941-z'
    },
    {
        'title': 'Mucosal and systemic immune correlates of viral control after SARS-CoV-2 infection challenge in seronegative adults',
        'image_name': 'wagstaffe2024.png',
        'url': 'https://doi.org/10.1126/sciimmunol.adj9285'
    },
    {
        'title': 'Viral kinetics of H5N1 infections in dairy cattle',
        'image_name': 'eales2025.png',
        'url': 'https://doi.org/10.1101/2025.02.01.636082'
    },
    {
        'title': 'Estimating infectiousness throughout SARS-CoV-2 infection course',
        'image_name': 'jones2023.png',
        'url': 'https://doi.org/10.1126/science.abi5273'
    },
    {
        'title': 'Infectious viral load in unvaccinated and vaccinated individuals infected with ancestral, Delta or Omicron SARS-CoV-2',
        'image_name': 'puhach2022.png',
        'url': 'https://doi.org/10.1038/s41591-022-01816-0'
    },
    {
        'title': 'Quantitative SARS-CoV-2 Viral-Load Curves in Paired Saliva Samples and Nasal Swabs Inform Appropriate Respiratory Sampling Site and Analytical Test Sensitivity Required for Earliest Viral Detection',
        'image_name': 'savela2022.png',
        'url': 'https://doi.org/10.1128/JCM.01785-21'
    },
    {
        'title': 'Evolution of inflammation and immunity in a denguevirus 1 human infection model',
        'image_name': 'waickman2022.png',
        'url': 'https://doi.org/10.1126/scitranslmed.abo5019'
    },
    {
        'title': 'Low-dose dengue virus 3 human challenge model: a phase 1 open-label study',
        'image_name': 'waickman2024.png',
        'url': 'https://doi.org/10.1038/s41564-024-01668-z'
    },
]


# Define the view for the home page
def home_view(request):
    """
    Renders the simple home page template.
    This view now also calculates stats and selects a random featured paper.
    """
    context = {}
    try:
        context.update(_compute_home_stats(_data_mtime()))
    except Exception as e:
        print(f"Error in home_view while reading CSV: {e}")
        context['total_data_points'] = "N/A"
        context['total_studies'] = "N/A"
        context['total_pathogens'] = "N/A"
        context['total_people'] = "N/A"

    # --- 3. "Featured Paper" Logic ---
    try:
        # Select one paper at random from the list
        selected_paper = random.choice(FEATURED_PAPERS_LIST)
        context['featured_paper'] = selected_paper
    except Exception as e:
        print(f"Error selecting featured paper: {e}")
        context['featured_paper'] = None # Handle error gracefully

    return render(request, 'visualization/home.html', context)

def chart_view(request):
    """
    Renders the INTERACTIVE dashboard page.
    This view now passes ALL data to the template for client-side filtering.
    """
    try:
        context = {'chart_title': 'Sample Data Dashboard'}
        context.update(_compute_chart_context(_data_mtime()))
        return render(request, 'visualization/data_chart.html', context)

    except FileNotFoundError:
        return HttpResponse(f"Error: Data file not found at: {DATA_FILE_PATH}", status=500)

    except Exception as e:
        return HttpResponse(f"An error occurred during data processing: {e}", status=500)


# --- STUB VIEWS for other pages ---
# (This section is unchanged)

def data_standard_view(request):
    return render(request, 'visualization/data_standard.html', {})

def docs_view(request):
    return render(request, 'visualization/docs.html', {})

def why_kinetics_view(request):
    return render(request, 'visualization/why_kinetics.html', {})

def add_dataset_view(request):
    return render(request, 'visualization/add_dataset.html', {})