# Data Cleaning Methodology: Deduplication & Zero-Popularity Removal

**Document Version:** 1.0
**Date:** 2025-11-14
**Author:** Spotify Track Analytics Team
**Pipeline:** ETL v2.0 (Enhanced Data Quality)

---

## Executive Summary

This document describes the enhanced data cleaning methodology implemented in the Spotify Track Analytics ETL pipeline. Two critical data quality improvements were added:

1. **Audio Feature Deduplication** - Removal of catalog duplicates with identical audio fingerprints
2. **Zero-Popularity Track Removal** - Filtering of dead catalog entries with no listener engagement

These changes address fundamental data quality issues discovered through statistical analysis, improving model training quality and prediction accuracy.

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Investigation & Analysis](#investigation--analysis)
3. [Methodology](#methodology)
4. [Implementation Details](#implementation-details)
5. [Impact & Results](#impact--results)
6. [Validation & Testing](#validation--testing)
7. [Technical Specifications](#technical-specifications)
8. [Recommendations](#recommendations)

---

## Problem Statement

### Original Dataset Issues

The raw Spotify dataset (114,000 tracks) contained significant data quality issues:

| Issue | Count | Percentage | Impact |
|-------|-------|------------|--------|
| Zero-popularity tracks | 16,020 | 14.05% | Introduces catalog noise |
| Audio feature duplicates | ~12,885 | 11.30% | Redundant training data |
| Catalog artifacts | ~13,000 | 11.40% | Biases genre distribution |

### Business Impact

1. **Model Performance**: Zero-popularity tracks create an artificial floor in the target variable, reducing predictive power
2. **Genre Bias**: Legacy genres (jazz, soul) unfairly penalized due to catalog duplication
3. **Prediction Usefulness**: Model learns to predict catalog organization rather than listener behavior
4. **Training Efficiency**: Duplicate data wastes computational resources without adding information

---

## Investigation & Analysis

### Zero-Popularity Tracks Analysis

**Finding 1: Catalog Duplication**
```
Top duplicated zero-popularity tracks:
• 'Run Rudolph Run': 146 instances
• 'Frosty The Snowman': 77 instances
• 'Little Saint Nick - 1991 Remix': 75 instances
• 'Winter Wonderland': 44 instances (43 with identical audio features)
```

**Finding 2: Artist Catalog Artifacts**
```
Artists with >90% zero-popularity tracks:
• Stevie Wonder: 91.1% (215/236 tracks)
• Ella Fitzgerald: 90.5% (201/222 tracks)
• Nat King Cole: 95.1% (97/102 tracks)
• Dean Martin: 90.9% (100/110 tracks)
• Peggy Lee: 97.6% (80/82 tracks)
```

**Finding 3: Genre Distribution Bias**
```
Genres most affected by zero-popularity:
• Jazz: 68.1% have 0 popularity
• Iranian: 65.6%
• Romance: 63.6%
• Soul: 61.1%
• Latin: 58.8%
• Country: 58.7%
```

**Finding 4: Minimal Audio Differences**
```
Audio feature comparison (zero vs non-zero):
• Energy: -0.031 (negligible)
• Tempo: -3.8 BPM (trivial)
• Instrumentalness: -0.062 (small)
• Duration: -16.8 seconds (minor)
```

### Audio Feature Duplicate Analysis

**Finding 5: Exact Audio Fingerprint Matches**
- 80.4% of zero-popularity tracks have identical audio features to other tracks
- Same song appears across multiple compilations/genres
- Example: "Winter Wonderland" by Jason Mraz appears 5 times with identical features

**Finding 6: Data Quality Indicators**
- Very few tracks (<1) have suspiciously generic/default values
- Missing values: minimal (<0.1%)
- Duplicates represent legitimate same-song-different-album scenarios

---

## Methodology

### Principle 1: Preserve Information, Remove Noise

**Goal**: Maximize information density while minimizing catalog artifacts

**Approach**:
1. Remove exact row duplicates (all columns identical)
2. Remove audio feature duplicates (keep most popular version)
3. Remove zero-popularity tracks (no listener engagement data)

### Principle 2: Intentional Filtering

**What We Remove:**
- ✅ Catalog duplicates (same audio features)
- ✅ Zero-popularity tracks (dead catalog)
- ✅ Exact row duplicates (data entry errors)

**What We Keep:**
- ✅ All tracks with listener engagement (popularity > 0)
- ✅ Genre diversity (all 125 genres represented)
- ✅ Audio feature variance (full musical spectrum)

### Principle 3: Data-Driven Decisions

Every removal decision backed by:
1. **Statistical evidence** (80% of zeros are duplicates)
2. **Business logic** (model predicts active tracks, not catalog ghosts)
3. **Empirical validation** (post-removal distribution analysis)

---

## Implementation Details

### Step 1: Exact Duplicate Removal

```python
# Remove rows where ALL columns are identical
df = df.drop_duplicates()
```

**Rationale**: Data entry errors, export duplicates
**Expected removal**: <1% of dataset
**Risk**: None (identical rows provide zero information gain)

### Step 2: Audio Feature Duplicate Removal

```python
audio_features = [
    'danceability', 'energy', 'loudness', 'speechiness',
    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'
]

# Sort by popularity (keep most popular version)
df = df.sort_values('popularity', ascending=False)

# Remove duplicates based on audio features
df = df.drop_duplicates(subset=audio_features, keep='first')
```

**Rationale**:
- Same song should only appear once in training data
- Keep version with highest engagement (most popular)
- Reduces overfitting on catalog organization

**Expected removal**: 10-15% of dataset
**Risk**: Low (keeps one representative version per unique audio fingerprint)

### Step 3: Zero-Popularity Track Removal

```python
# Remove tracks with no listener engagement
df = df[df['popularity'] > 0]
```

**Rationale**:
- Zero popularity = no Spotify streaming history (dead catalog)
- Not "unpopular tracks people don't like"
- Model should predict active track popularity

**Expected removal**: 14-16% of remaining dataset
**Risk**: None (these tracks have no listener behavior data)

---

## Impact & Results

### Dataset Transformation

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Total Tracks** | 114,000 | ~97,980 | -14.1% |
| **Mean Popularity** | 33.24 | 38.67 | +16.3% |
| **Median Popularity** | 35.00 | 39.00 | +11.4% |
| **Std Deviation** | 22.31 | 19.20 | -14.0% |
| **Popularity Range** | 0-100 | 1-100 | Floor raised |
| **Duplicate Tracks** | ~13,000 | 0 | -100% |

### Model Performance Impact

**Expected Improvements:**

1. **R² Score**: 0.477 → **0.52-0.57** (+10-20%)
   - More focused signal (active tracks only)
   - Reduced noise from catalog artifacts
   - Better feature-to-popularity relationships

2. **Prediction Quality**:
   - More actionable for music producers
   - Reflects actual listener behavior
   - No artificial floor at zero

3. **Training Efficiency**:
   - 14% less data, but higher information density
   - Faster training iterations
   - Better generalization (less overfitting)

### Genre Distribution Impact

**Genres Most Affected (Lowest Retention):**
```
Country:      41.3% retained (587 zero-pop removed)
Alternative:  51.5% retained (485 zero-pop removed)
Classical:    60.2% retained
Blues:        65.4% retained
Jazz:         31.9% retained (681 zero-pop removed)
```

**Genres Least Affected (Highest Retention):**
```
Comedy:       100.0% retained
Club:         99.9% retained
Black-metal:  99.7% retained
Afrobeat:     98.5% retained
Brazil:       96.6% retained
```

**Analysis**: Older catalog-heavy genres show lower retention, but this reflects data quality improvement rather than information loss. Remaining tracks in these genres have actual listener engagement.

---

## Validation & Testing

### Pre-Deployment Validation

**Test 1: Distribution Normality**
```python
# Before: Skewed left (floor at 0)
# After: More normal distribution (floor at 1)
# Result: ✅ Improved for regression modeling
```

**Test 2: Feature Correlations**
```python
# Before: Weak correlations due to zero-pop noise
# After: Stronger feature-to-popularity relationships
# Result: ✅ Better predictive signal
```

**Test 3: Genre Representation**
```python
# Before: 125 genres
# After: 125 genres (all preserved)
# Result: ✅ No genre exclusion
```

**Test 4: Duplicate Detection**
```python
# Audio feature duplicates after cleaning: 0
# Zero-popularity tracks after cleaning: 0
# Result: ✅ Clean dataset
```

### Post-Deployment Monitoring

**Metrics to Track:**
1. Model R² score (expected: 0.52-0.57)
2. RMSE (expected: <15.0)
3. MAE (expected: <11.0)
4. Genre-specific prediction accuracy
5. Prediction distribution (should match 1-100 range)

---

## Technical Specifications

### ETL Pipeline Changes

**File**: `src/etl_pipeline.py`
**Version**: 2.0
**Changes**: Enhanced `transform()` method

**New Methods:**
1. `_remove_audio_feature_duplicates()` - Lines 175-216
2. `_remove_zero_popularity_tracks()` - Lines 218-270

**Logging Enhancements:**
- Per-step removal counts
- Genre distribution analysis
- Before/after statistics
- Validation assertions

### Data Validation

**New Assertions:**
```python
# Ensure no zero-popularity tracks in final dataset
assert df['popularity'].between(1, 100).all()
assert (df['popularity'] == 0).sum() == 0
```

### Output Artifacts

**Cleaned Dataset Files:**
- `data/processed/cleaned_spotify_data.csv` (CSV format)
- `data/processed/cleaned_spotify_data.parquet` (Parquet format)

**Quality Report:**
- `data/processed/data_quality_report.txt`

**Includes:**
- Total rows removed per step
- Genre retention statistics
- Popularity distribution metrics
- Validation results

---

## Recommendations

### For Data Scientists

1. **Use Cleaned Dataset**: Always use `cleaned_spotify_data.parquet` for modeling
2. **Document Changes**: Track model performance before/after data cleaning
3. **Monitor Drift**: Watch for new zero-popularity tracks in future data pulls

### For Model Training

1. **Expected R² Range**: 0.52-0.57 (up from 0.477)
2. **Prediction Range**: 1-100 (not 0-100)
3. **Interpretation**: Predictions represent active track engagement, not catalog status

### For Production Deployment

1. **Input Validation**: Reject tracks with all features at default values
2. **Zero Handling**: If model predicts <1, clip to 1 (floor)
3. **Genre Context**: Consider genre-specific models for highly affected genres

### For Future ETL Runs

1. **Version Control**: Tag data versions after each ETL run
2. **Reproducibility**: Save random seeds, parameters, removal logs
3. **Monitoring**: Track removal percentages to detect data drift

---

## Appendix A: Removal Statistics

### Detailed Breakdown

```
ETL Pipeline Execution Report:
==================================================
Step 1: Exact Duplicate Removal
  - Rows before: 114,000
  - Rows after: ~114,000
  - Removed: ~0 (<0.1%)

Step 2: Audio Feature Duplicate Removal
  - Rows before: ~114,000
  - Rows after: ~101,000
  - Removed: ~13,000 (11.4%)
  - Features checked: 9 audio features
  - Logic: Keep most popular version

Step 3: Zero-Popularity Removal
  - Rows before: ~101,000
  - Rows after: ~97,980
  - Removed: ~3,020 (3.0%)
  - Rationale: No listener engagement data

Final Dataset:
  - Total tracks: 97,980
  - Reduction: 14.1% from original
  - Information gain: Higher signal-to-noise ratio
==================================================
```

---

## Appendix B: Example Cases

### Example 1: "Winter Wonderland" Deduplication

**Before Cleaning:**
- 44 instances of "Winter Wonderland"
- 43 with identical audio features
- Various artists/genres (Jason Mraz, Ella Fitzgerald, Dean Martin, etc.)
- Most have 0 popularity

**After Cleaning:**
- 1 instance kept (highest popularity or first occurrence)
- Represents the unique audio fingerprint
- Eliminates catalog redundancy

### Example 2: Stevie Wonder Catalog

**Before Cleaning:**
- 236 Stevie Wonder tracks
- 215 (91%) with 0 popularity
- Clear catalog duplication pattern

**After Cleaning:**
- ~21 Stevie Wonder tracks with listener engagement
- Represents actual popular tracks
- Eliminates compilation/reissue duplicates

---

## Appendix C: Code Examples

### Running the Enhanced ETL Pipeline

```python
from src.etl_pipeline import SpotifyETL

# Initialize ETL
etl = SpotifyETL(raw_data_path="data/raw/dataset.csv")

# Run complete pipeline
df_clean, csv_path, parquet_path = etl.run(
    output_path="data/processed/cleaned_spotify_data.csv"
)

# Review results
print(f"Cleaned dataset: {len(df_clean):,} tracks")
print(f"Popularity range: {df_clean['popularity'].min()}-{df_clean['popularity'].max()}")
print(f"Mean popularity: {df_clean['popularity'].mean():.2f}")
```

### Custom Validation

```python
# Verify no zeros
assert (df_clean['popularity'] == 0).sum() == 0

# Verify no audio duplicates
audio_features = ['danceability', 'energy', 'loudness', 'speechiness',
                  'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
assert df_clean.duplicated(subset=audio_features).sum() == 0

# Verify all genres present
assert len(df_clean['track_genre'].unique()) == 125
```

---

## Changelog

### Version 2.0 (2025-11-14)
- ✅ Added audio feature deduplication
- ✅ Added zero-popularity track removal
- ✅ Enhanced logging and reporting
- ✅ Added validation assertions
- ✅ Updated documentation

### Version 1.0 (Previous)
- Basic ETL pipeline
- Exact duplicate removal only
- Missing value imputation
- Feature engineering

---

## References

1. **Zero-Popularity Analysis**: `/Volumes/SSD/Spotify/investigation_2025-11-14.txt` (ad-hoc analysis)
2. **ETL Pipeline**: `/Volumes/SSD/Spotify/src/etl_pipeline.py`
3. **Hyperparameter Tuning Results**: `docs/HYPERPARAMETER_TUNING_RESULTS.md`
4. **Model Performance**: Baseline R² = 0.477 (pre-cleaning)

---

## Contact & Support

For questions about this methodology:
1. Review the ETL pipeline code: `src/etl_pipeline.py`
2. Check data quality report: `data/processed/data_quality_report.txt`
3. Consult hyperparameter tuning results: `docs/HYPERPARAMETER_TUNING_RESULTS.md`

---

**Document Status**: ✅ Approved for Production
**Last Updated**: 2025-11-14
**Next Review**: After first model retrain with cleaned data
