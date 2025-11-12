from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import make_pipeline
import pickle
import xgboost as xgb
import pandas as pd
import numpy as np


def load_data():
    df = pd.read_csv('Carbon Emission.csv')

    df.columns = ['Body Type', 'Sex', 'Diet', 'Shower', 'Heating', 'Transport', 'Vehicle type', 'Social Activity', 'Monthly Grocery Bill', 'Flight', 'Vehicle Distance', 
                'Waste Bag Size', 'Waste Weekly', 'TV Daily Hour', 'Clothes Monthly', 'Internet Daily', 'Energy Efficiency', 'Recycling', 'Cooking', 
                'Carbon Emission']

    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    df.replace(np.nan, 'None', inplace=True)

    return df


def train_model(df):
    
    numerical = ['monthly_grocery_bill', 'vehicle_distance', 'waste_weekly', 
                'tv_daily_hour', 'clothes_monthly', 'internet_daily']

    categorical = [ 'body_type', 'sex', 'diet', 'shower', 'heating', 'transport',
                   'vehicle_type', 'social_activity', 'flight', 'waste_bag_size',
                   'energy_efficiency', 'recycling', 'cooking'
    ]

    param_xg = {'learning_rate': 0.1, 
                'max_depth': 3, 
                'n_estimators': 200, 
                'subsample': 0.8}

    pipeline = make_pipeline(
        DictVectorizer(),
        xgb.XGBRegressor(**param_xg, objective='reg:squarederror', tree_method='hist', n_jobs=-1, random_state=42)
    )

    train_dict = df[categorical + numerical].to_dict(orient='records')  
    y_train = df.carbon_emission.values 

    pipeline.fit(train_dict, y_train)

    return pipeline

def save_model(filename, model):
    with open(filename, 'wb') as f_out:
        pickle.dump(model, f_out)

    print(f'Model saved to {filename}')

df = load_data()
pipeline = train_model(df)
save_model('xg_model.pkl', pipeline)








