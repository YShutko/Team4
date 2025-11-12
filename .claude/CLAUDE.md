# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a data science project focused on analyzing Spotify track analytics to predict song popularity. The project uses audio features (danceability, energy, tempo, valence, etc.) from ~114,000 songs across 125 genres to understand key drivers of popularity, classify songs by mood/energy, and support playlist curation.

**Data Source**: [Kaggle Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)

## Development Environment

This project uses a Python virtual environment located at `.venv/`. The virtual environment is already in `.gitignore`.

### Setup Commands

```bash
# Activate virtual environment (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Key Dependencies

- **Data Analysis**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **ML/Statistics**: scikit-learn, xgboost, feature-engine, imbalanced-learn
- **Profiling**: ydata-profiling, ppscore, yellowbrick (can be removed before deployment)
- **Interactive UI**: streamlit (for deployment), gradio (planned)

## Project Structure

```
├── data/                           # Raw datasets (CSV files, zipped data)
│   ├── dataset.csv.zip            # Compressed Spotify dataset
│   └── spotify_dataset.csv        # Uncompressed dataset
├── jupyter_notebooks/             # Early exploration (credit card churn - legacy)
├── notebooks/                     # Main analysis notebooks
│   └── Hackathon2Music.ipynb     # Primary music analytics pipeline
├── docs/                          # Project documentation
├── requirements.txt               # Python dependencies
├── Procfile                       # Heroku deployment config (Streamlit)
├── setup.sh                       # Streamlit configuration script
└── README.md                      # Project overview and business requirements
```

**Note**: `jupyter_notebooks/HackatonProject1.ipynb` contains credit card churn analysis - this appears to be legacy code from a previous project and is not related to the Spotify music analytics focus.

## Running Analysis

### Jupyter Notebooks

The main analysis pipeline is in `notebooks/Hackathon2Music.ipynb`. This notebook:

1. Extracts data from `dataset.csv.zip`
2. Performs data cleaning and feature engineering
3. Standardizes audio features using `StandardScaler`
4. Analyzes popularity drivers via correlation analysis
5. Classifies songs by mood/energy (Happy/High Energy, Sad/Low Energy, etc.)
6. Performs genre-level analysis
7. Generates playlist recommendations
8. Runs hypothesis tests (Spearman correlation for numeric features)
9. Saves cleaned data and EDA visualizations to `eda_outputs/`

```bash
# Launch Jupyter
jupyter notebook notebooks/Hackathon2Music.ipynb
```

### Streamlit Deployment

The project is configured for Heroku deployment with Streamlit (though no `app.py` currently exists in the repo).

```bash
# Expected command (when app.py is created):
streamlit run app.py
```

## Data Processing Pipeline

### Key Column Detection

The notebook dynamically detects column names to handle variations in dataset structure:
- Track name: `track_name`, `track`, `song`, `title`
- Artist: `artist_name`, `artist`, `artists`
- Genre: `genre`, `genres`
- Popularity: `popularity`, `pop`
- Duration: `duration_ms`, `duration`
- Release date: `release_date`, `year`, `release`

### Feature Engineering

1. **Duration conversion**: `duration_ms` → `duration_min` (milliseconds to minutes)
2. **Release year extraction**: Parse `release_date` to extract year
3. **Mood/Energy classification**: Combines valence and energy scores:
   - Happy/High Energy: valence > 0, energy > 0
   - Energetic/Sad: valence ≤ 0, energy > 0
   - Chill/Happy: valence > 0, energy ≤ 0
   - Sad/Low Energy: valence ≤ 0, energy ≤ 0
4. **Audio feature standardization**: StandardScaler applied to `danceability`, `energy`, `loudness`, `acousticness`, `tempo`, `valence`, `instrumentalness`

### Output Artifacts

- **Cleaned dataset**: `cleaned_music_data.csv`
- **Visualizations**: Saved to `eda_outputs/` directory
  - `popularity_drivers_heatmap.png`
  - `mood_energy_distribution.png`
  - `genre_audio_features.png`
  - `popularity_vs_{feature}.png` (multiple)
  - `avg_popularity_per_artist.png`
  - Feature-binned popularity plots

## Business Requirements Context

1. **Key Drivers of Popularity**: Identify which audio features (danceability, energy, tempo, valence) most influence popularity scores
2. **Mood/Energy Classification**: Segment songs into mood categories for user experience
3. **Genre-Level Analysis**: Understand trends across genres (danceability, loudness, acousticness)
4. **Playlist Curation**: Enable smart playlist generation based on shared characteristics
5. **Data-Driven Recommendations**: Foundation for ML-powered music recommendations

## Working with Data

- **Raw data location**: `data/` directory
- **Data format**: CSV (some files are zipped)
- **Size**: ~114,000 tracks, 125 genres
- **Key features**: 17+ audio features including danceability (0-1), energy (0-1), loudness (dB), tempo (BPM), valence (0-1), instrumentalness, acousticness, speechiness, liveness

## Important Notes

- **Legacy content**: The `jupyter_notebooks/` folder contains credit card churn analysis that is unrelated to this Spotify project
- **Development artifacts**: `ydata-profiling`, `ppscore`, `yellowbrick`, and `Pillow` are marked in `requirements.txt` as removable before deployment
- **Deployment ready**: Project includes Heroku configuration (Procfile, setup.sh) but no `app.py` exists yet
- **Interactive UI planned**: README mentions Gradio interface for uploading track features and getting predictions (not yet implemented)
- **Statistical testing**: Notebook includes Spearman correlation tests for numeric features and Kruskal-Wallis tests for categorical features
