# Symptom-Based Disease Prediction & Health Risk Predictor

A Streamlit web app with two machine-learning tools:

1. **Disease Predictor** – select symptoms and get a ranked list of likely diseases with confidence scores, an urgency level and basic advice (XGBoost).
2. **Health Risk Predictor** – enter lifestyle and body metrics (age, diet, exercise, sleep, stress, BMI, smoking, alcohol) to get a Low / Medium / High risk estimate (Random Forest).

> ⚠️ **Disclaimer:** This is an educational project trained on synthetic data. It is **not** a medical device and must not be used for real diagnosis. Always consult a qualified doctor.

## Project Structure

```
Symptom_Based_Disease_Prediction/
├── Health_risk_predictor.ipynb        # (root copy is empty; real notebook is in project/)
└── project/
    ├── App.py                          # Main Streamlit app (both tabs)
    ├── symptom_predictor.py            # Older, symptom-only version of the app
    ├── train_symptom_model.py          # Trains the XGBoost disease model
    ├── Health_risk_predictor.ipynb     # Trains the health-risk model
    ├── realistic_dataset_no_covid.csv  # Symptom dataset (37,977 rows, 40 symptoms, 19 diseases)
    ├── symptom_disease_model.pkl       # Saved disease model
    ├── symptom_features.pkl            # Ordered list of symptom columns
    ├── disease_label_encoder.pkl       # Disease label encoder
    ├── Health_risk_predictor.pkl       # Saved risk model
    └── label_encoders.pkl              # Encoders for the risk model inputs
```

## Tech Stack

Python 3.11+, pandas, scikit-learn, XGBoost, Streamlit

## Installation

```bash
git clone https://github.com/Devanshbh3108/Symptom_Based_Disease_Prediction.git
cd Symptom_Based_Disease_Prediction/project
pip install pandas scikit-learn xgboost streamlit
```

## Usage

Run the app:

```bash
streamlit run App.py
```

Retrain the disease model (overwrites the `.pkl` files in the current folder):

```bash
python train_symptom_model.py
```

## Datasets & Models

| Model | Algorithm | Input | Output |
|-------|-----------|-------|--------|
| Disease predictor | XGBoost (300 trees, depth 6) | 40 symptom columns | 19 diseases |
| Health risk predictor | Random Forest | age, diet, exercise, sleep, stress, BMI, smoking, alcohol, family history | Low / Medium / High |

The symptom dataset is **synthetic**: each disease has a few "signature" symptoms with high values (3–5) while the rest are random low values (0–1). Because of this, the model reaches ~100% test accuracy, which does **not** reflect real-world performance.

## Known Limitations

- Synthetic data, so accuracy numbers are not meaningful for real patients.
- The app sends symptoms as 0/1, but the dataset uses severity values up to 5. This makes the retrained model give very low confidence.
- Disease descriptions and advice cover only 9–10 diseases; the dataset has 19.
- Models are saved with pickle and sklearn 1.8.0; use the same version to avoid warnings.

## Future Improvements

- Train on a real, clinically validated dataset
- Add a severity slider per symptom
- Add descriptions and advice for all diseases
- Add a `requirements.txt` and a proper root README

## Author

[Devanshbh3108](https://github.com/Devanshbh3108)
