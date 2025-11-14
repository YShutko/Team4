"""
ETL Pipeline for Spotify Track Analytics
Extracts, transforms, and loads Spotify dataset for analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SpotifyETL:
    """ETL pipeline for Spotify track analytics"""

    def __init__(self, raw_data_path: str = "data/raw/dataset.csv"):
        self.raw_data_path = Path(raw_data_path)
        self.df = None

    def extract(self) -> pd.DataFrame:
        """Extract data from CSV file"""
        logger.info(f"Extracting data from {self.raw_data_path}")

        try:
            self.df = pd.read_csv(self.raw_data_path)
            logger.info(f"Successfully loaded {len(self.df):,} records with {len(self.df.columns)} columns")
            return self.df
        except FileNotFoundError:
            logger.error(f"File not found: {self.raw_data_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def data_quality_report(self) -> dict:
        """Generate comprehensive data quality report"""
        logger.info("Generating data quality report...")

        report = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'columns': list(self.df.columns),
            'duplicates': self.df.duplicated().sum(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'dtypes': self.df.dtypes.astype(str).to_dict(),
            'numeric_columns': self.df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_columns': self.df.select_dtypes(include=['object']).columns.tolist(),
        }

        # Basic statistics
        report['numeric_stats'] = self.df.describe().to_dict()

        # Memory usage
        report['memory_usage_mb'] = self.df.memory_usage(deep=True).sum() / 1024**2

        logger.info(f"Found {report['duplicates']} duplicate rows")
        logger.info(f"Total missing values: {sum(report['missing_values'].values())}")

        return report

    def transform(self) -> pd.DataFrame:
        """Transform and clean the dataset"""
        logger.info("Starting data transformation...")

        # 1. Remove exact duplicates (all columns identical)
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        exact_dups_removed = initial_rows - len(self.df)
        logger.info(f"Removed {exact_dups_removed:,} exact duplicate rows")

        # 2. Remove audio feature duplicates (same track, different metadata)
        audio_dups_removed = self._remove_audio_feature_duplicates()

        # 3. Remove zero-popularity tracks (catalog artifacts)
        zero_pop_removed = self._remove_zero_popularity_tracks()

        # 4. Handle missing values
        missing_before = self.df.isnull().sum().sum()

        # Fill numeric columns with median
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if self.df[col].isnull().sum() > 0:
                self.df[col].fillna(self.df[col].median(), inplace=True)

        # Fill categorical columns with mode
        cat_cols = self.df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            if self.df[col].isnull().sum() > 0:
                self.df[col].fillna(self.df[col].mode()[0], inplace=True)

        missing_after = self.df.isnull().sum().sum()
        logger.info(f"Filled {missing_before - missing_after} missing values")

        # 5. Feature engineering
        self._engineer_features()

        # 6. Data validation
        self._validate_data()

        # 7. Summary of cleaning
        total_removed = exact_dups_removed + audio_dups_removed + zero_pop_removed
        logger.info(f"Total rows removed: {total_removed:,} ({total_removed/initial_rows*100:.2f}%)")
        logger.info(f"Final dataset: {len(self.df):,} tracks")
        logger.info("Data transformation complete")
        return self.df

    def _engineer_features(self):
        """Create derived features"""
        logger.info("Engineering new features...")

        # Duration in minutes (if duration_ms exists)
        if 'duration_ms' in self.df.columns:
            self.df['duration_min'] = self.df['duration_ms'] / 60000
            logger.info("Created 'duration_min' feature")

        # Mood/Energy classification
        if all(col in self.df.columns for col in ['valence', 'energy']):
            self.df['mood_energy'] = self.df.apply(self._classify_mood, axis=1)
            logger.info("Created 'mood_energy' classification")

        # Energy level categories
        if 'energy' in self.df.columns:
            self.df['energy_category'] = pd.cut(
                self.df['energy'],
                bins=[0, 0.33, 0.66, 1.0],
                labels=['Low Energy', 'Medium Energy', 'High Energy'],
                include_lowest=True
            )
            logger.info("Created 'energy_category' feature")

        # Popularity categories
        if 'popularity' in self.df.columns:
            self.df['popularity_category'] = pd.cut(
                self.df['popularity'],
                bins=[0, 33, 66, 100],
                labels=['Low Popularity', 'Medium Popularity', 'High Popularity'],
                include_lowest=True
            )
            logger.info("Created 'popularity_category' feature")

        # Tempo categories (BPM)
        if 'tempo' in self.df.columns:
            self.df['tempo_category'] = pd.cut(
                self.df['tempo'],
                bins=[0, 90, 120, 150, 300],
                labels=['Slow', 'Moderate', 'Fast', 'Very Fast'],
                include_lowest=True
            )
            logger.info("Created 'tempo_category' feature")

    @staticmethod
    def _classify_mood(row) -> str:
        """Classify song mood based on valence and energy"""
        valence = row.get('valence', 0.5)
        energy = row.get('energy', 0.5)

        # Normalize to ensure they're between 0 and 1
        valence = max(0, min(1, valence))
        energy = max(0, min(1, energy))

        if valence > 0.5 and energy > 0.5:
            return "Happy/High Energy"
        elif valence <= 0.5 and energy > 0.5:
            return "Energetic/Sad"
        elif valence > 0.5 and energy <= 0.5:
            return "Chill/Happy"
        else:
            return "Sad/Low Energy"

    def _remove_audio_feature_duplicates(self) -> int:
        """
        Remove tracks with identical audio features (catalog duplicates).
        Keeps the track with highest popularity, or first occurrence if tied.

        Returns:
            Number of duplicates removed
        """
        logger.info("Identifying audio feature duplicates...")

        # Define audio features to check for duplicates
        audio_features = [
            'danceability', 'energy', 'loudness', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'
        ]

        # Only use features that exist in the dataset
        available_features = [f for f in audio_features if f in self.df.columns]

        if not available_features:
            logger.warning("No audio features found for duplicate detection")
            return 0

        initial_rows = len(self.df)

        # Sort by popularity (descending) to keep most popular version
        if 'popularity' in self.df.columns:
            self.df = self.df.sort_values('popularity', ascending=False)

        # Remove duplicates based on audio features, keeping first (most popular)
        self.df = self.df.drop_duplicates(subset=available_features, keep='first')

        duplicates_removed = initial_rows - len(self.df)

        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed:,} audio feature duplicates "
                       f"({duplicates_removed/initial_rows*100:.2f}%)")
            logger.info(f"  Features checked: {', '.join(available_features)}")
        else:
            logger.info("No audio feature duplicates found")

        return duplicates_removed

    def _remove_zero_popularity_tracks(self) -> int:
        """
        Remove tracks with zero popularity (catalog artifacts with no listener data).

        Analysis shows that zero-popularity tracks are primarily:
        - Catalog duplicates (80% are exact audio feature duplicates)
        - Dead catalog entries with no Spotify streaming history
        - Not legitimate "unpopular" tracks

        Returns:
            Number of zero-popularity tracks removed
        """
        if 'popularity' not in self.df.columns:
            logger.warning("Popularity column not found - skipping zero-popularity removal")
            return 0

        logger.info("Analyzing zero-popularity tracks...")

        initial_rows = len(self.df)
        zero_pop_count = (self.df['popularity'] == 0).sum()

        if zero_pop_count == 0:
            logger.info("No zero-popularity tracks found")
            return 0

        # Log statistics before removal
        zero_pop_pct = (zero_pop_count / initial_rows) * 100
        logger.info(f"Found {zero_pop_count:,} zero-popularity tracks ({zero_pop_pct:.2f}%)")

        # Analyze genre distribution
        if 'track_genre' in self.df.columns:
            zero_pop_df = self.df[self.df['popularity'] == 0]
            top_genres = zero_pop_df['track_genre'].value_counts().head(5)
            logger.info(f"  Top affected genres: {', '.join(top_genres.index.tolist())}")

        # Remove zero-popularity tracks
        self.df = self.df[self.df['popularity'] > 0].copy()

        tracks_removed = initial_rows - len(self.df)

        # Log statistics after removal
        if tracks_removed > 0:
            new_mean = self.df['popularity'].mean()
            new_median = self.df['popularity'].median()
            new_std = self.df['popularity'].std()

            logger.info(f"Removed {tracks_removed:,} zero-popularity tracks")
            logger.info(f"  New popularity stats: mean={new_mean:.2f}, "
                       f"median={new_median:.2f}, std={new_std:.2f}")
            logger.info(f"  Rationale: Zero-popularity represents catalog artifacts, "
                       f"not legitimate listener preferences")

        return tracks_removed

    def _validate_data(self):
        """Validate data quality after transformation"""
        logger.info("Validating transformed data...")

        # Check for remaining nulls
        null_counts = self.df.isnull().sum()
        if null_counts.sum() > 0:
            logger.warning(f"Data still contains {null_counts.sum()} null values")
            logger.warning(f"Columns with nulls: {null_counts[null_counts > 0].to_dict()}")

        # Validate numeric ranges
        if 'popularity' in self.df.columns:
            assert self.df['popularity'].between(1, 100).all(), "Popularity out of range [1-100] or contains zeros"
            assert (self.df['popularity'] == 0).sum() == 0, "Dataset should not contain zero-popularity tracks"

        if 'danceability' in self.df.columns:
            assert self.df['danceability'].between(0, 1).all(), "Danceability out of range [0-1]"

        if 'energy' in self.df.columns:
            assert self.df['energy'].between(0, 1).all(), "Energy out of range [0-1]"

        logger.info("Data validation passed")

    def load(self, output_path: str = "data/processed/cleaned_spotify_data.csv"):
        """Save cleaned dataset in both CSV and Parquet formats"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save as CSV
        logger.info(f"Saving cleaned dataset to {output_path}")
        self.df.to_csv(output_path, index=False)
        logger.info(f"Successfully saved CSV: {len(self.df):,} records")

        # Save as Parquet
        parquet_path = output_path.with_suffix('.parquet')
        logger.info(f"Saving Parquet format to {parquet_path}")
        self.df.to_parquet(parquet_path, index=False, compression='snappy')
        logger.info(f"Successfully saved Parquet: {len(self.df):,} records")

        # Save data quality report
        report_path = output_path.parent / "data_quality_report.txt"
        self._save_quality_report(report_path)

        return output_path, parquet_path

    def _save_quality_report(self, report_path: Path):
        """Save data quality report to file"""
        report = self.data_quality_report()

        with open(report_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("SPOTIFY DATASET - DATA QUALITY REPORT\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"Total Rows: {report['total_rows']:,}\n")
            f.write(f"Total Columns: {report['total_columns']}\n")
            f.write(f"Memory Usage: {report['memory_usage_mb']:.2f} MB\n")
            f.write(f"Duplicate Rows: {report['duplicates']}\n\n")

            f.write("COLUMNS:\n")
            f.write("-" * 80 + "\n")
            for col in report['columns']:
                f.write(f"  - {col}\n")

            f.write("\n\nMISSING VALUES:\n")
            f.write("-" * 80 + "\n")
            missing = {k: v for k, v in report['missing_values'].items() if v > 0}
            if missing:
                for col, count in missing.items():
                    f.write(f"  {col}: {count}\n")
            else:
                f.write("  No missing values!\n")

            f.write("\n\nDATA TYPES:\n")
            f.write("-" * 80 + "\n")
            for col, dtype in report['dtypes'].items():
                f.write(f"  {col}: {dtype}\n")

        logger.info(f"Data quality report saved to {report_path}")

    def run(self, output_path: str = "data/processed/cleaned_spotify_data.csv") -> Tuple[pd.DataFrame, Path, Path]:
        """Run complete ETL pipeline"""
        logger.info("=" * 80)
        logger.info("STARTING ETL PIPELINE")
        logger.info("=" * 80)

        # Extract
        self.extract()

        # Generate initial quality report
        initial_report = self.data_quality_report()

        # Transform
        self.transform()

        # Load
        csv_path, parquet_path = self.load(output_path)

        logger.info("=" * 80)
        logger.info("ETL PIPELINE COMPLETE")
        logger.info("=" * 80)

        return self.df, csv_path, parquet_path


if __name__ == "__main__":
    # Run ETL pipeline
    etl = SpotifyETL()
    df_clean, csv_path, parquet_path = etl.run()

    print("\n" + "=" * 80)
    print("ETL PIPELINE SUMMARY")
    print("=" * 80)
    print(f"CSV dataset: {csv_path}")
    print(f"Parquet dataset: {parquet_path}")
    print(f"Total records: {len(df_clean):,}")
    print(f"Total features: {len(df_clean.columns)}")
    print(f"\nNew features created:")
    new_features = ['duration_min', 'mood_energy', 'energy_category', 'popularity_category', 'tempo_category']
    for feat in new_features:
        if feat in df_clean.columns:
            print(f"  ✓ {feat}")
    print("\nFirst few records:")
    print(df_clean.head())
