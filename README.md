# 🌍 Carbon Footprint Estimator

A comprehensive system for predicting personal carbon emissions based on lifestyle choices. The system consists of a **FastAPI backend** that uses a trained XGBoost model and a **Streamlit frontend** for an interactive user experience.

## 🚀 Live Deployment

**Try the app now:** https://carbon-footprint-estimator-fcjc.onrender.com

Deployed on [Render](https://render.com) with FastAPI backend and Streamlit frontend running in a single Docker container.

## 📋 Table of Contents

- [Live Deployment](#-live-deployment)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Using the Frontend](#using-the-frontend)
- [Docker Deployment](#-docker-deployment)
- [System Architecture](#system-architecture)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### Backend (FastAPI)
- **Machine Learning Model**: XGBoost regressor trained on carbon emission dataset
- **DictVectorizer**: Converts categorical and numerical features into sparse matrices for model input
- **RESTful API**: Easy-to-use `/predict` endpoint for carbon emission predictions
- **Automatic DictVectorizer Management**: Rebuilds from CSV if not cached, saves cache for faster subsequent runs

### Frontend (Streamlit)
- **Interactive User Interface**: Easy-to-use form with dropdown menus and numeric inputs
- **Real-time Predictions**: Instant carbon emission estimates
- **Error Handling**: Comprehensive error messages for network, validation, and server issues
- **Visualizations**: 
  - Comparison chart showing user emissions vs. typical ranges
  - Pie chart showing estimated emission breakdown by category
- **Personalized Recommendations**: Contextual tips to reduce carbon footprint
- **Session Tracking**: Stores last prediction for reference

---

## 📁 Project Structure

```
Carbon-Footprint-Estimator/
├── predict.py                 # FastAPI backend service
├── app.py                      # Streamlit frontend application
├── start.sh                    # Shell script to run both services
├── xg_model.pkl               # Trained XGBoost model (pickled)
├── dv.pkl                      # DictVectorizer cache (auto-generated)
├── Carbon Emission.csv        # Training/reference dataset
├── notebook.ipynb             # Jupyter notebook with ML pipeline
├── train.py                   # Training script (if available)
├── pyproject.toml             # Project dependencies
├── Dockerfile                 # Docker container configuration
├── .dockerignore              # Docker build context exclusions
├── README.md                  # This file
└── __pycache__/               # Python cache files
```

---

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.12+**
- **pip** or **uv** package manager (project uses uv for virtual environment)
- **Git** (to clone the repository)

### Step 1: Clone or Navigate to Repository
```bash
cd c:\\Users\\{your-directory}\\Carbon-Footprint-Estimator
```

### Step 2: Install Dependencies
Using **pip**:
```bash
pip install -r requirements.txt
```

Or using **uv** (if you prefer):
```bash
uv sync
```

Or install from **pyproject.toml**:
```bash
pip install -e .
```

Required packages:
- `fastapi>=0.121.1`
- `uvicorn>=0.38.0`
- `pandas>=2.3.3`
- `scikit-learn>=1.7.2`
- `xgboost>=3.1.1`
- `streamlit>=1.28.0`
- `requests>=2.32.5`
- `plotly` (for visualizations)
- `numpy`, `seaborn`, `matplotlib`

### Step 3: Verify Model Files
Ensure the following files are present in the project root:
- `xg_model.pkl` - Trained XGBoost model
- `Carbon Emission.csv` - Dataset for DictVectorizer initialization
- `dv.pkl` - (Optional) Will be auto-generated on first backend run

---

## 🚀 Running the Application

### Method 1: Run Backend and Frontend Separately (Recommended for Development)

#### Terminal 1: Start the FastAPI Backend

```bash
cd c:\\Users\\{your-dirctory}\\Carbon-Footprint-Estimator
python predict.py
```

Or using uvicorn directly:
```bash
python -m uvicorn predict:app --host 0.0.0.0 --port 9696 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:9696
INFO:     Application startup complete
```

#### Terminal 2: Start the Streamlit Frontend

```bash
cd c:\\Users\\{your-directory}\\Carbon-Footprint-Estimator
streamlit run app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

Open your browser to `http://localhost:8501` to use the application.

---

### Method 2: Run Both Services Together Using `start.sh` (Development & Production)

The `start.sh` script automatically starts both the FastAPI backend and Streamlit frontend in the same process.

#### On Linux/macOS:
```bash
./start.sh
```

#### On Windows (Git Bash or WSL):
```bash
bash start.sh
```

**What `start.sh` does:**
1. Starts FastAPI backend on `http://0.0.0.0:9696` in the background
2. Starts Streamlit frontend on `http://0.0.0.0:8501` in the foreground

Access the app at `http://localhost:8501`.

---

### Method 3: Using Docker (Production)

#### Build the Docker Image
```bash
docker build -t carbon-estimator:latest .
```

#### Run the Container Locally
```bash
docker run --rm -p 9696:9696 -p 8501:8501 carbon-estimator:latest
```

The container automatically executes `start.sh` as the entrypoint, which runs both services simultaneously.

Open your browser to `http://localhost:8501` to access the frontend.

---

## 🐳 Docker Deployment Details

### Overview

The `Dockerfile` uses a **multi-stage build** strategy to minimize image size while keeping both services (backend & frontend) in a single container.

**Optimized for Production:**
- **Multi-stage build**: Separates build dependencies from runtime
- **Slim base image**: `python:3.12.1-slim-bookworm` (reduced size)
- **Image size**: ~600-800 MB (reduced from 2.17 GB with dev dependencies removed)
- **Virtual environment caching**: Compiled dependencies copied from builder stage
- **Minimal cleanup**: Removes `.pyc` files, test directories, and cache to save space
- **Single entrypoint**: `start.sh` runs both FastAPI and Streamlit simultaneously

### How `start.sh` Works

The `start.sh` script is the Docker entrypoint that:
1. Starts the FastAPI backend on port 9696 in the background
2. Starts the Streamlit frontend on port 8501 in the foreground
3. Allows both services to run within a single container

**Development vs. Production:**
- **Production**: Only runtime dependencies (fastapi, streamlit, scikit-learn, xgboost, etc.)
- **Development**: Uncomment `matplotlib`, `plotly`, `seaborn`, `ipykernel` in `pyproject.toml` for local work
- **Update lock file locally**: Run `uv sync` to regenerate `uv.lock` with dev dependencies

---
