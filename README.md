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

