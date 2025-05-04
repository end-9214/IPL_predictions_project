# utils.py
import joblib

def load_models(model_path):
    model = joblib.load(f'{model_path}/winner_model.pkl')
    encoders = joblib.load(f'{model_path}/encoders.pkl')
    return model, encoders

def save_models(model, encoders, save_path):
    joblib.dump(model, f'{save_path}/winner_model.pkl')
    joblib.dump(encoders, f'{save_path}/encoders.pkl')