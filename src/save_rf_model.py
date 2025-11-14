"""
Save Tuned Random Forest Model

Quick script to retrain and save the best Random Forest model from Optuna tuning.
Uses the optimal hyperparameters discovered in the tuning phase.
"""

import pandas as pd
import joblib
import json
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np

print("="*80)
print("💾 SAVING TUNED RANDOM FOREST MODEL")
print("="*80)

# Load best parameters from tuning results
results_file = sorted(Path('outputs/metadata').glob('rf_tuning_results_*.json'))[-1]
print(f"Loading parameters from: {results_file}")

with open(results_file, 'r') as f:
    tuning_results = json.load(f)

best_params = tuning_results['optuna']['best_params']
print(f"\nBest parameters:")
for param, value in best_params.items():
    print(f"  {param}: {value}")

# Load data
print("\nLoading dataset...")
df = pd.read_parquet('data/processed/cleaned_spotify_data.parquet')
print(f"✓ Loaded {len(df):,} tracks")

# Prepare features
feature_cols = [
    'danceability', 'energy', 'loudness', 'speechiness',
    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'
]

X = df[feature_cols].copy()
y = df['popularity'].copy()

# Remove NaN values
mask = ~(X.isnull().any(axis=1) | y.isnull())
X, y = X[mask], y[mask]

# Same split as tuning: 70% train, 15% val, 15% test
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, random_state=42
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42
)

print(f"✓ Train: {X_train.shape[0]:,} samples")
print(f"✓ Val: {X_val.shape[0]:,} samples")
print(f"✓ Test: {X_test.shape[0]:,} samples")

# Train model with best parameters
print("\nTraining Random Forest with optimal hyperparameters...")
model = RandomForestRegressor(
    n_estimators=best_params['n_estimators'],
    max_depth=best_params['max_depth'],
    min_samples_split=best_params['min_samples_split'],
    min_samples_leaf=best_params['min_samples_leaf'],
    max_features=best_params['max_features'],
    bootstrap=best_params['bootstrap'],
    random_state=42,
    n_jobs=-1,
    verbose=0
)

model.fit(X_train, y_train)
print("✓ Training complete")

# Evaluate
y_test_pred = model.predict(X_test)
test_r2 = r2_score(y_test, y_test_pred)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_mae = mean_absolute_error(y_test, y_test_pred)

print(f"\nTest Performance:")
print(f"  R² = {test_r2:.4f}")
print(f"  RMSE = {test_rmse:.2f}")
print(f"  MAE = {test_mae:.2f}")

# Save model
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
model_path = Path(f'outputs/models/rf_model_full_{timestamp}.joblib')
model_path.parent.mkdir(parents=True, exist_ok=True)

print(f"\nSaving model...")
joblib.dump(model, model_path)
print(f"✓ Model saved: {model_path}")

# Save metadata
import sklearn

metadata = {
    'timestamp': datetime.now().isoformat(),
    'model_type': 'RandomForestRegressor',
    'sklearn_version': sklearn.__version__,
    'n_samples': len(df),
    'n_features': len(feature_cols),
    'feature_names': feature_cols,
    'hyperparameters': best_params,
    'metrics': {
        'test_r2': test_r2,
        'test_rmse': test_rmse,
        'test_mae': test_mae
    },
    'data_shapes': {
        'train': [X_train.shape[0], X_train.shape[1]],
        'val': [X_val.shape[0], X_val.shape[1]],
        'test': [X_test.shape[0], X_test.shape[1]]
    },
    'feature_importance': [
        {'feature': feat, 'importance': float(imp)}
        for feat, imp in zip(feature_cols, model.feature_importances_)
    ]
}

metadata_path = Path(f'outputs/metadata/rf_metadata_full_{timestamp}.json')
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"✓ Metadata saved: {metadata_path}")

print("\n" + "="*80)
print("✅ RANDOM FOREST MODEL SAVED SUCCESSFULLY")
print("="*80)
print(f"\nModel: {model_path.name}")
print(f"Test R²: {test_r2:.4f}")
print(f"Test RMSE: {test_rmse:.2f}")
print(f"Test MAE: {test_mae:.2f}")
