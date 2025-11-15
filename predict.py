import pickle
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union, Dict, Any
import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer


APP_DIR = Path(__file__).parent
MODEL_PATH = APP_DIR / "xg_model.pkl"
DV_PATH = APP_DIR / "dv.pkl"
CSV_PATH = APP_DIR / "Carbon Emission.csv"


def _load_model(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Model file not found at: {path}")
    with path.open("rb") as f:
        return pickle.load(f)


def _build_or_load_dv(dv_path: Path, csv_path: Path) -> DictVectorizer:
    """Return a DictVectorizer. If a saved dv exists load it; otherwise build it by
    fitting on the CSV's feature dicts (drop the target column). This follows the
    notebook where DictVectorizer was fit on training dicts.
    """
    if dv_path.exists():
        with dv_path.open("rb") as f:
            return pickle.load(f)

    # Build from CSV (must exist in repository as notebook used it)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file for rebuilding DictVectorizer not found at: {csv_path}")

    df = pd.read_csv(csv_path)

    # Notebook normalization: rename columns to lowercase with underscores
    df.columns = ['Body Type', 'Sex', 'Diet', 'Shower', 'Heating', 'Transport', 'Vehicle type', 'Social Activity', 'Monthly Grocery Bill', 'Flight', 'Vehicle Distance', 
                  'Waste Bag Size', 'Waste Weekly', 'TV Daily Hour', 'Clothes Monthly', 'Internet Daily', 'Energy Efficiency', 'Recycling', 'Cooking', 
                  'Carbon Emission']
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    df.replace(np.nan, 'None', inplace=True)

    feature_df = df.drop(columns=['carbon_emission'], errors='ignore')

    dv = DictVectorizer(sparse=True)
    dv.fit(feature_df.to_dict(orient='records'))

    # Persist dv for faster future loads (overwrites if exists)
    with dv_path.open("wb") as f:
        pickle.dump(dv, f)

    return dv


app = FastAPI(title="Carbon Footprint Estimator")


class InputData(BaseModel):
    body_type: str
    sex: str
    diet: str
    shower: str
    heating: str
    transport: str
    vehicle_type: str
    social_activity: str
    monthly_grocery_bill: float
    flight: str
    vehicle_distance: float
    waste_bag_size: str
    waste_weekly: int
    tv_daily_hour: float
    clothes_monthly: int
    internet_daily: float
    energy_efficiency: str
    recycling: Union[List[str], str]
    cooking: Union[List[str], str]


def _normalize_list_field(value: Union[List[str], str]) -> str:
    """Return a string representation that matches the CSV/dataset format used during training.

    Accepts either a list of strings or a string like "['Metal']" or "Metal,Paper".
    """
    if isinstance(value, list):
        return ",".join([str(v).strip() for v in value])
    if isinstance(value, str):
        s = value.strip()
        if s.startswith("[") and s.endswith("]"):
            s = s[1:-1]
        # remove quotes inside
        parts = [p.strip().strip("'\"") for p in s.split(",") if p.strip()]
        return ",".join(parts)
    return str(value)


# Load artifacts at module import. Missing files will raise.
model = _load_model(MODEL_PATH)
dv = _build_or_load_dv(DV_PATH, CSV_PATH)


def _prepare_record(payload: InputData) -> Dict[str, Any]:
    d = payload.dict()

    # Normalize list-like fields to strings (as original dataset appears to have strings)
    d['recycling'] = _normalize_list_field(d.get('recycling', ''))
    d['cooking'] = _normalize_list_field(d.get('cooking', ''))

    # Ensure numeric types are native Python types (not numpy types)
    d['monthly_grocery_bill'] = float(d.get('monthly_grocery_bill', 0.0))
    d['vehicle_distance'] = float(d.get('vehicle_distance', 0.0))
    d['tv_daily_hour'] = float(d.get('tv_daily_hour', 0.0))
    d['internet_daily'] = float(d.get('internet_daily', 0.0))
    d['waste_weekly'] = int(d.get('waste_weekly', 0))
    d['clothes_monthly'] = int(d.get('clothes_monthly', 0))

    return d


@app.post("/predict")
def predict(payload: InputData):
    """Accept InputData JSON, vectorize with DictVectorizer, and return model prediction.

    Returns: {"prediction": float, "units": "kg_co2e"}
    """
    record = _prepare_record(payload)
    X = dv.transform([record])
    pred = model.predict(X)

    if hasattr(pred, '__len__'):
        value = float(pred[0])
    else:
        value = float(pred)

    return {"prediction": value, "input": payload.dict()}


if __name__ == "__main__":
    uvicorn.run("predict:app", host="0.0.0.0", port=9696)