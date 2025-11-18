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

## 📡 API Documentation

### Endpoint: `POST /predict`

**Base URL (Local):** `http://localhost:9696`  
**Base URL (Production):** `https://carbon-footprint-estimator-fcjc.onrender.com`

**Description:** Accepts user lifestyle data and returns predicted annual carbon emissions in kg CO₂e.

#### Request Body

```json
{
  "body_type": "overweight",
  "sex": "female",
  "diet": "pescatarian",
  "shower": "daily",
  "heating": "coal",
  "transport": "public",
  "vehicle_type": "None",
  "social_activity": "often",
  "monthly_grocery_bill": 230,
  "flight": "frequently",
  "vehicle_distance": 210,
  "waste_bag_size": "large",
  "waste_weekly": 4,
  "tv_daily_hour": 7,
  "clothes_monthly": 26,
  "internet_daily": 1,
  "energy_efficiency": "No",
  "recycling": ["Metal"],
  "cooking": ["Stove", "Oven"]
}
```

#### Field Descriptions

| Field | Type | Options | Description |
|-------|------|---------|-------------|
| `body_type` | string | underweight, normal, overweight, obese | User's body classification |
| `sex` | string | male, female, other | User's sex |
| `diet` | string | vegan, vegetarian, pescatarian, omnivore | Diet type |
| `shower` | string | rarely, weekly, daily | Shower frequency |
| `heating` | string | coal, gas, electric, renewable, none | Primary heating source |
| `transport` | string | public, private, walking, cycling | Primary transport mode |
| `vehicle_type` | string | None, electric, hybrid, gasoline, diesel | Vehicle type |
| `social_activity` | string | rarely, sometimes, often | Social activity frequency |
| `monthly_grocery_bill` | float | 0 - ∞ | Monthly grocery spending ($) |
| `flight` | string | never, occasionally, frequently | Flight frequency |
| `vehicle_distance` | float | 0 - ∞ | Weekly driving distance (km) |
| `waste_bag_size` | string | small, medium, large | Typical waste bag size |
| `waste_weekly` | integer | 0 - ∞ | Weekly waste bags count |
| `tv_daily_hour` | float | 0 - 24 | Daily TV/screen time (hours) |
| `clothes_monthly` | integer | 0 - ∞ | Monthly clothing purchases (items) |
| `internet_daily` | float | 0 - 24 | Daily internet usage (hours) |
| `energy_efficiency` | string | Yes, No | Energy-efficient home/appliances |
| `recycling` | array | Metal, Plastic, Paper, Glass, None | Items recycled |
| `cooking` | array | Stove, Oven, Microwave, Grill, None | Cooking methods |

#### Response (Success - 200)

```json
{
  "prediction": 5234.67,
  "input": {
    "body_type": "overweight",
    "sex": "female",
    ...
  }
}
```

#### Response (Validation Error - 422)

```json
{
  "detail": [
    {
      "loc": ["body", "monthly_grocery_bill"],
      "msg": "value must be >= 0",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

#### Example cURL Request

```bash
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{
    "body_type": "normal",
    "sex": "male",
    "diet": "omnivore",
    "shower": "daily",
    "heating": "gas",
    "transport": "private",
    "vehicle_type": "gasoline",
    "social_activity": "sometimes",
    "monthly_grocery_bill": 250,
    "flight": "occasionally",
    "vehicle_distance": 150,
    "waste_bag_size": "medium",
    "waste_weekly": 2,
    "tv_daily_hour": 2,
    "clothes_monthly": 10,
    "internet_daily": 5,
    "energy_efficiency": "No",
    "recycling": ["Paper", "Plastic"],
    "cooking": ["Stove"]
  }'
```

---

## 🎨 Using the Frontend

### Home Page Features

1. **Personal Information Section**
   - Select body type (underweight, normal, overweight, obese)
   - Choose sex
   - Input age (optional)

2. **Diet & Food Section**
   - Select diet type (vegan, vegetarian, pescatarian, omnivore)
   - Enter monthly grocery bill

3. **Daily Habits Section**
   - Set shower frequency
   - Input daily TV/screen time
   - Enter daily internet usage

4. **Transportation Section**
   - Choose primary transport method
   - Select vehicle type
   - Enter weekly vehicle distance

5. **Energy & Utilities Section**
   - Select heating source
   - Indicate energy efficiency

6. **Consumption & Waste Section**
   - Enter monthly clothing purchases
   - Select waste bag size
   - Input weekly waste bag count
   - Select items you recycle

7. **Cooking & Lifestyle Section**
   - Select cooking methods
   - Choose social activity level
   - Select flight frequency

### Prediction Flow

1. **Fill in all fields** on the left panel
2. **Click "🚀 Predict Carbon Emission"** button on the right panel
3. **View results** including:
   - Annual carbon emission in kg CO₂e
   - Emission assessment (Sustainable/Average/High/Very High)
   - Comparison chart vs. typical ranges
   - Emission breakdown by category
   - Personalized tips to reduce footprint
4. **Previous prediction** is stored in session for reference

### Interpretation Guide

- **< 2,000 kg CO₂e/year**: 🟢 Sustainable - Excellent! Below average emissions
- **2,000 - 5,000 kg CO₂e/year**: 🟡 Average - On par with typical consumer
- **5,000 - 8,000 kg CO₂e/year**: 🟠 High - Consider making changes
- **> 8,000 kg CO₂e/year**: 🔴 Very High - Significant reduction opportunities

---

## 🏗️ System Architecture

### Backend Flow

```
User Input (Streamlit)
    ↓
HTTP POST Request to /predict
    ↓
FastAPI validates InputData (Pydantic)
    ↓
_prepare_record() normalizes inputs
    ↓
DictVectorizer transforms record → sparse matrix
    ↓
XGBoost model predicts carbon emission
    ↓
JSON Response with prediction value
    ↓
Streamlit displays result + visualizations
```

### Data Flow for Backend Startup

```
predict.py starts
    ↓
Load xg_model.pkl (trained XGBoost)
    ↓
Check for dv.pkl cache
    ├─ If exists: Load cached DictVectorizer
    └─ If not exists:
        ├─ Read Carbon Emission.csv
        ├─ Normalize column names
        ├─ Fit DictVectorizer on features
        └─ Save dv.pkl for future runs
    ↓
FastAPI app ready to receive requests
```

---
