# Kolkata AQI Early Warning System

**Next-day Air Quality Index (AQI) prediction for Kolkata using Machine Learning**

Mini-project for the Machine Learning course · Topic: *Hyperlocal Air Pollution Prediction*

---

## Student Information

| | |
|---|---|
| **Name** | SAPAVAT MUNNI |
| **Department** | CSE (AI & ML) |
| **Institute** | Ghani Khan Choudhury Institute of Engineering and Technology (GKCIET), Malda |
| **Subject** | Introduction to Machine Learning |
| **Subject Code** | PCCAIML 502 |
| **Domain** | Machine Learning |
| **Guided by** | Dr. Showmik Bhowmik |

---

## 1. Problem Statement

Kolkata regularly faces poor air quality, especially in winter. People usually find out about it only after the air is already bad. This project builds a Machine Learning model that **predicts tomorrow's AQI from today's pollutant readings**, so that citizens, schools and hospitals can get an early warning and plan ahead.

## 2. Objectives

1. Collect and clean daily air quality data for Kolkata.
2. Explore seasonal and pollutant patterns through EDA.
3. Train and compare at least three ML regression models for next-day AQI prediction.
4. Evaluate the models with MAE, RMSE and R², and compare them against a naive baseline.
5. Build a working web prototype that gives the predicted AQI, its category and a health advisory.

## 3. Dataset

- **Name:** Air Quality Data in India (2015 – 2020)
- **Source:** Kaggle, https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india
- **File used:** `city_day.csv`, filtered to `City == "Kolkata"`
- **Size after filtering:** 814 daily records, from 10 Apr 2018 to 1 Jul 2020
- **Columns used:** PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3 and AQI

The dataset is **not stored in this repository**. See [`data/README.md`](data/README.md) for download instructions.

## 4. Methodology

### 4.1 Preprocessing
- Filtered Kolkata rows and sorted by date.
- Filled missing values using **time-based interpolation**.
- Created calendar features: `month`, `dayofweek`, `season` (Winter, Summer, Monsoon, Post-monsoon).
- Created the target `AQI_next` by shifting AQI one day ahead, so the model forecasts **tomorrow**.

> Same-day AQI is calculated directly from the pollutants, so predicting it gives an unrealistically high score. Predicting the next day makes this a real early-warning task.

### 4.2 Features and target
- **Inputs (13):** PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, today's AQI, month, day of week, season
- **Target:** next day's AQI

### 4.3 Train/test split
**Time-ordered split:** first 80% of days for training, last 20% for testing. A random split is not used, because it would let the model learn from the future.

### 4.4 Models compared

| Model | Settings |
|---|---|
| Baseline (Persistence) | Tomorrow's AQI = today's AQI |
| Linear Regression | Default |
| Random Forest Regressor | 300 trees, max depth 12, random_state 42 |
| XGBoost Regressor | 300 trees, learning rate 0.05, max depth 4, random_state 42 |

### 4.5 Metrics
MAE (Mean Absolute Error), RMSE (Root Mean Squared Error) and R² score.

## 5. Results

| Model | MAE | RMSE | R² |
|---|---|---|---|
| Baseline (Persistence) | 17.393 | 27.017 | 0.841 |
| Linear Regression | 14.714 | 21.197 | 0.902 |
| **Random Forest** | **13.311** | **18.785** | **0.923** |
| XGBoost | 14.800 | 19.723 | 0.915 |

The results are also saved in [`results/model_comparison.csv`](results/model_comparison.csv).

### Observations
- **Random Forest performed best** on all three metrics.
- It reduced RMSE by about **30.5%** and MAE by about **23.5%** compared with the persistence baseline, so the model adds real value beyond "tomorrow equals today".
- Even Linear Regression reached R² of 0.902, which shows that today's AQI is a strong predictor of tomorrow's.
- On average the Random Forest prediction is off by about 13 AQI points.

### Plots

| | |
|---|---|
| ![Trend](images/eda_trend_monthly.png) | ![Correlation](images/eda_correlation.png) |
| AQI trend and monthly average | Correlation heatmap |
| ![Actual vs Predicted](images/actual_vs_predicted.png) | ![Feature importance](images/feature_importance.png) |
| Actual vs predicted AQI | Feature importance (Random Forest) |

## 6. Prototype (Streamlit Web App)

The app takes today's pollutant readings and shows tomorrow's predicted AQI with its CPCB category, a health advisory, a model comparison tab and feature importance.

![App prediction](images/app_prediction.png)
![App model performance](images/app_model_performance.png)

## 7. Project Structure

```
kolkata-aqi-prediction/
├── app.py                         # Streamlit web app
├── requirements.txt
├── README.md
├── .streamlit/config.toml         # App theme
├── data/README.md                 # Dataset download instructions
├── notebooks/
│   └── 01_aqi_prediction.ipynb    # Preprocessing, EDA, training, evaluation
├── model/
│   ├── best_model.pkl             # Trained Random Forest
│   └── columns.pkl                # Feature order used by the model
├── images/                        # EDA plots and app screenshots
└── results/
    └── model_comparison.csv
```

## 8. How to Run

**1. Clone the repository**
```bash
git clone https://github.com/[YOUR-GITHUB-USERNAME]/kolkata-aqi-prediction.git
cd kolkata-aqi-prediction
```

**2. Install the libraries**
```bash
pip install -r requirements.txt
```

**3. Run the web app** (the trained model is already included)
```bash
python -m streamlit run app.py
```
The app opens at `http://localhost:8501`.

**4. (Optional) Re-run the notebook**
Download `city_day.csv` as described in [`data/README.md`](data/README.md), place it in the `data/` folder, then open `notebooks/01_aqi_prediction.ipynb` in Jupyter or VS Code and run all cells.

## 9. Limitations

- Only Kolkata, from mid-2018 to mid-2020. The data includes the 2020 lockdown months, when pollution was unusually low.
- City-level readings, not hyperlocal station-level data.
- No weather inputs such as wind, rain or humidity.
- Only next-day forecasting.

## 10. Future Work

- Add weather data to improve accuracy.
- Use station-level data for truly hyperlocal predictions.
- Multi-day forecasts and time-series models such as LSTM.
- Deploy publicly on Streamlit Community Cloud.

## 11. Tech Stack

Python · pandas · NumPy · scikit-learn · XGBoost · Matplotlib · Seaborn · Altair · Streamlit · Jupyter

---

*Made for educational purposes. Not an official air quality forecast.*
