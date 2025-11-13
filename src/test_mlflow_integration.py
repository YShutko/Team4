"""
Test MLflow Integration with Synthetic Data
"""
import os
import sys
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.mlflow_tracker import MLflowTracker
from src.ml_utils import adjusted_r2, load_config

print("="*80)
print("🧪 TESTING MLFLOW INTEGRATION")
print("="*80)

np.random.seed(42)
n_samples = 1000

print("\n📊 Generating synthetic data...")
data = {
    'danceability': np.random.randn(n_samples),
    'energy': np.random.randn(n_samples),
    'loudness': np.random.randn(n_samples),
    'acousticness': np.random.randn(n_samples),
    'tempo': np.random.randn(n_samples),
    'valence': np.random.randn(n_samples),
    'instrumentalness': np.random.randn(n_samples),
}

popularity = (
    10 * data['energy'] +
    8 * data['danceability'] +
    5 * data['valence'] +
    np.random.randn(n_samples) * 5 +
    50
)
popularity = np.clip(popularity, 0, 100)

df = pd.DataFrame(data)
df['popularity'] = popularity

X = df.drop('popularity', axis=1)
y = df['popularity']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"✅ Data ready: {X_train.shape[0]} train, {X_test.shape[0]} test\n")

tracker = MLflowTracker(
    experiment_name="spotify_popularity_prediction",
    tracking_uri="sqlite:///mlruns/mlflow.db"
)

try:
    params = load_config('config/xgboost_params.json')
except:
    params = {
        'max_depth': 6,
        'learning_rate': 0.1,
        'n_estimators': 100,
        'random_state': 42
    }

run = tracker.start_run(
    run_name="test_mlflow_integration",
    tags={
        'dataset': 'synthetic',
        'model_type': 'xgboost',
        'pipeline_version': 'improved_v1.0'
    }
)

print("\n🤖 Training model...")
tracker.log_params(params)

model = XGBRegressor(**params)
model.fit(X_train, y_train)

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
train_mae = mean_absolute_error(y_train, y_train_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)
test_adj_r2 = adjusted_r2(test_r2, len(y_test), X_test.shape[1])

metrics = {
    'train_rmse': train_rmse,
    'test_rmse': test_rmse,
    'train_mae': train_mae,
    'test_mae': test_mae,
    'train_r2': train_r2,
    'test_r2': test_r2,
    'test_adjusted_r2': test_adj_r2
}

print("\n📊 Logging metrics to MLflow...")
tracker.log_metrics(metrics)

print("\n💾 Logging model to MLflow...")
tracker.log_model(model, registered_model_name="spotify_xgboost_model")

tracker.log_dict({
    'n_samples': len(X),
    'n_features': X.shape[1],
    'feature_names': list(X.columns),
    'train_size': len(X_train),
    'test_size': len(X_test)
}, 'data_info.json')

tracker.end_run(status="FINISHED")

print("\n" + "="*80)
print("✅ MLFLOW INTEGRATION TEST COMPLETE!")
print("="*80)
print(f"\n📊 Test Results:")
print(f"   Test R²:          {test_r2:.4f}")
print(f"   Test Adjusted R²: {test_adj_r2:.4f}")
print(f"   Test RMSE:        {test_rmse:.4f}")
print(f"   Test MAE:         {test_mae:.4f}")

print(f"\n🔍 View results in MLflow UI:")
print(f"   Run: make mlflow-ui")
print(f"   Or:  mlflow ui --backend-store-uri sqlite:///mlruns/mlflow.db")
print("\n" + "="*80)
