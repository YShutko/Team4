.PHONY: help setup clean test mlflow-ui mlflow-clean train notebook lint format

# Default target
.DEFAULT_GOAL := help

##@ General

help: ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

setup: ## Install dependencies and setup environment
	@echo "📦 Installing dependencies..."
	@pip install -r requirements.txt
	@echo "✅ Setup complete!"

clean: ## Clean generated files and caches
	@echo "🧹 Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name ".DS_Store" -delete
	@echo "✅ Cleanup complete!"

##@ MLflow

mlflow-ui: ## Start MLflow UI with SQLite backend
	@echo "🚀 Starting MLflow UI..."
	@echo "   Backend: SQLite (mlruns/mlflow.db)"
	@echo "   URL: http://127.0.0.1:5000"
	@echo ""
	@mlflow ui --backend-store-uri sqlite:///mlruns/mlflow.db --port 5000

mlflow-clean: ## Clean all MLflow runs and artifacts
	@echo "⚠️  This will delete all MLflow experiments, runs, and artifacts!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -rf mlruns mlartifacts; \
		echo "✅ MLflow data deleted!"; \
	else \
		echo "❌ Cancelled"; \
	fi

mlflow-export: ## Export MLflow experiments to CSV
	@echo "📊 Exporting MLflow experiments..."
	@mkdir -p exports
	@python -c "import mlflow; import pandas as pd; \
		mlflow.set_tracking_uri('sqlite:///mlruns/mlflow.db'); \
		runs = mlflow.search_runs(); \
		runs.to_csv('exports/mlflow_runs.csv', index=False); \
		print(f'✅ Exported {len(runs)} runs to exports/mlflow_runs.csv')"

mlflow-info: ## Show MLflow tracking information
	@echo "📊 MLflow Information:"
	@echo "   Tracking URI: sqlite:///mlruns/mlflow.db"
	@echo "   Artifacts: ./mlartifacts"
	@echo ""
	@python -c "import mlflow; \
		mlflow.set_tracking_uri('sqlite:///mlruns/mlflow.db'); \
		experiments = mlflow.search_experiments(); \
		print(f'   Total Experiments: {len(experiments)}'); \
		for exp in experiments: \
			runs = mlflow.search_runs([exp.experiment_id]); \
			print(f'   - {exp.name}: {len(runs)} runs');" 2>/dev/null || echo "   No experiments found"

##@ Training

train: ## Run improved ML pipeline
	@echo "🤖 Training model with improved pipeline..."
	@python src/improved_ml_pipeline.py

train-mlflow: ## Run improved ML pipeline with MLflow tracking
	@echo "🤖 Training model with MLflow tracking..."
	@python src/improved_ml_pipeline_mlflow.py

test-pipeline: ## Test pipeline with synthetic data
	@echo "🧪 Testing pipeline with synthetic data..."
	@python src/test_pipeline.py
	@python src/improved_ml_pipeline.py
	@echo "✅ Pipeline test complete!"

##@ Notebooks

notebook: ## Start Jupyter notebook server
	@echo "📓 Starting Jupyter notebook..."
	@jupyter notebook

notebook-improved: ## Open improved ML pipeline notebook
	@echo "📓 Opening improved ML pipeline notebook..."
	@jupyter notebook notebooks/04_Improved_ML_Pipeline.ipynb

##@ Development

lint: ## Run code quality checks
	@echo "🔍 Running linting checks..."
	@python -m flake8 src/ --max-line-length=100 --ignore=E203,W503 || echo "⚠️  Install flake8: pip install flake8"

format: ## Format code with black
	@echo "✨ Formatting code..."
	@python -m black src/ --line-length=100 || echo "⚠️  Install black: pip install black"

##@ Git

git-status: ## Show git status with useful information
	@echo "📊 Git Status:"
	@git status -sb
	@echo ""
	@echo "Recent commits:"
	@git log --oneline -5

git-push: ## Push commits to remote
	@echo "🚀 Pushing to remote..."
	@git push origin main

##@ Outputs

view-plots: ## Open outputs directory to view plots
	@echo "📊 Opening outputs/plots directory..."
	@open outputs/plots/ 2>/dev/null || xdg-open outputs/plots/ 2>/dev/null || echo "Plots location: outputs/plots/"

view-models: ## Show saved models
	@echo "💾 Saved Models:"
	@ls -lh outputs/models/*.joblib 2>/dev/null || echo "No models found"

view-metadata: ## Show model metadata
	@echo "📋 Model Metadata:"
	@ls -lh outputs/metadata/*.json 2>/dev/null || echo "No metadata found"
	@echo ""
	@echo "Latest metadata:"
	@ls -t outputs/metadata/*.json 2>/dev/null | head -1 | xargs cat 2>/dev/null || echo "No metadata found"

##@ Documentation

docs: ## Show project documentation
	@echo "📚 Project Documentation:"
	@echo "   - Full Spec: dev_docs/ML_PIPELINE_IMPROVEMENTS_SPEC.md"
	@echo "   - Implementation Summary: IMPLEMENTATION_SUMMARY.md"
	@echo "   - Quick Start: README_IMPROVEMENTS.md"
	@echo "   - Source Code: src/README.md"

view-spec: ## View ML pipeline improvements specification
	@cat dev_docs/ML_PIPELINE_IMPROVEMENTS_SPEC.md | less

##@ Docker (Optional)

docker-build: ## Build Docker image for the project
	@echo "🐳 Building Docker image..."
	@docker build -t spotify-ml-pipeline .

docker-run: ## Run Docker container
	@echo "🐳 Running Docker container..."
	@docker run -p 5000:5000 -p 8888:8888 -v $(PWD):/app spotify-ml-pipeline

##@ All-in-one

full-pipeline: clean setup train mlflow-ui ## Run full pipeline from scratch
	@echo "✅ Full pipeline complete!"

