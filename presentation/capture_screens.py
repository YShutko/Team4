"""
Capture Screenshots for Spotify Track Popularity Prediction Presentation

This script captures screenshots and copies existing plots for the presentation.
It can optionally capture live screenshots from running services.
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Configuration
BASE_DIR = Path(__file__).parent.parent
PLOTS_DIR = BASE_DIR / "outputs" / "plots"
SCREENS_DIR = Path(__file__).parent / "screens"
METADATA_DIR = BASE_DIR / "outputs" / "metadata"

# Ensure screens directory exists
SCREENS_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print("📸 CAPTURING SCREENSHOTS FOR PRESENTATION")
print("="*80)


def copy_existing_plots() -> List[str]:
    """Copy existing plots from outputs/plots/ to presentation/screens/"""
    print("\n📊 Step 1: Copying Existing Plots")
    print("-" * 80)

    plot_files = [
        "xgboost_learning_curve.png",
        "actual_vs_predicted.png",
        "prediction_density.png",
        "residuals_plot.png",
        "qq_plot_residuals.png",
        "correlation_heatmap.png",
        "feature_importance.png",
        "xgboost_shap_summary_bar.png",
        "xgboost_shap_beeswarm.png",
    ]

    copied_files = []

    for plot_file in plot_files:
        src = PLOTS_DIR / plot_file
        if src.exists():
            # Use numbered prefix for slide ordering
            idx = plot_files.index(plot_file) + 1
            dest_name = f"{idx:02d}_{plot_file}"
            dest = SCREENS_DIR / dest_name
            shutil.copy2(src, dest)
            print(f"  ✅ Copied: {plot_file} → {dest_name}")
            copied_files.append(str(dest))
        else:
            print(f"  ⚠️  Not found: {plot_file}")

    print(f"\n  Total plots copied: {len(copied_files)}")
    return copied_files


def create_title_slide_metadata() -> Dict[str, str]:
    """Extract metadata for title slide"""
    print("\n📋 Step 2: Extracting Metadata")
    print("-" * 80)

    import json

    metadata = {
        "title": "Spotify Track Popularity Prediction",
        "subtitle": "Machine Learning Pipeline with XGBoost & SHAP",
        "date": "2025",
        "features": []
    }

    # Try to load latest model metadata
    if METADATA_DIR.exists():
        metadata_files = sorted(METADATA_DIR.glob("*.json"), reverse=True)
        if metadata_files:
            latest_metadata = metadata_files[0]
            print(f"  📄 Loading metadata from: {latest_metadata.name}")

            with open(latest_metadata, 'r') as f:
                model_meta = json.load(f)

            # Extract key metrics
            if 'metrics' in model_meta:
                metrics = model_meta['metrics']
                metadata['test_r2'] = metrics.get('test_r2', 0)
                metadata['test_rmse'] = metrics.get('test_rmse', 0)
                metadata['test_mae'] = metrics.get('test_mae', 0)

                print(f"  ✅ Test R²: {metadata.get('test_r2', 0):.4f}")
                print(f"  ✅ Test RMSE: {metadata.get('test_rmse', 0):.4f}")
                print(f"  ✅ Test MAE: {metadata.get('test_mae', 0):.4f}")

            # Extract feature names
            if 'feature_names' in model_meta:
                metadata['features'] = model_meta['feature_names']
                print(f"  ✅ Features: {len(metadata['features'])}")

            # Extract git commit
            if 'environment' in model_meta and 'git_commit' in model_meta['environment']:
                metadata['git_commit'] = model_meta['environment']['git_commit']
                print(f"  ✅ Git commit: {metadata['git_commit']}")

    return metadata


def capture_live_screenshots() -> List[str]:
    """
    Capture screenshots from live services (optional)

    This function can be extended to capture screenshots from:
    - Streamlit dashboard (http://localhost:8501)
    - MLflow UI (http://localhost:5000)
    - Gradio dashboard (http://localhost:7860)

    For now, it's a placeholder for future enhancement.
    """
    print("\n🌐 Step 3: Live Screenshots (Optional)")
    print("-" * 80)
    print("  ℹ️  Live screenshot capture not enabled")
    print("  ℹ️  To enable: install playwright and configure URLs")

    return []


def list_captured_screens() -> List[str]:
    """List all captured screenshots"""
    screens = sorted(SCREENS_DIR.glob("*.png"))
    return [str(s) for s in screens]


def main():
    """Main execution"""

    # Step 1: Copy existing plots
    plot_files = copy_existing_plots()

    # Step 2: Extract metadata for title slide
    metadata = create_title_slide_metadata()

    # Save metadata for presentation builder
    metadata_file = SCREENS_DIR / "metadata.json"
    import json
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"\n  ✅ Metadata saved to: {metadata_file.name}")

    # Step 3: Capture live screenshots (optional)
    live_files = capture_live_screenshots()

    # Summary
    print("\n" + "="*80)
    print("✅ SCREENSHOT CAPTURE COMPLETE")
    print("="*80)

    all_screens = list_captured_screens()
    print(f"\n📁 Total screenshots: {len(all_screens)}")
    print(f"   - Plots: {len(plot_files)}")
    print(f"   - Live captures: {len(live_files)}")

    print(f"\n💾 Output directory: {SCREENS_DIR}")
    print(f"\n🎯 Next step: Run 'python presentation/build_pptx.py' to generate presentation")
    print("="*80)

    return all_screens


if __name__ == "__main__":
    main()
