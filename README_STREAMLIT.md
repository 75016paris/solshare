# ☀️ Solar Plant Monitoring Dashboard

ML-based monitoring system for HKL GGI solar plant (269.28 kWp) with real-time anomaly detection.

## 🎯 Features

- **Real-time Dashboard**: Monitor daily production, predictions, and performance ratios
- **3-Line Comparison**: Actual vs ML Prediction vs Clear-Sky theoretical maximum
- **Anomaly Detection**: Automatic flagging of underperformance issues
- **Performance Analytics**: Detailed metrics (MAE, RMSE, R², MAPE)
- **Interactive Visualizations**: Plotly-based interactive charts
- **Date Range Selection**: Analyze any time period
- **Alert System**: Configurable thresholds for performance warnings

## 📋 Prerequisites

1. Python 3.8 or higher
2. Trained ML model from `HKL_ML_comparison_v2.ipynb`
3. Exported predictions data

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements_streamlit.txt
```

### Step 2: Export Predictions from Notebook

Open `HKL_ML_comparison_v2.ipynb` and add this code at the end:

```python
# Export predictions for Streamlit app
import pickle
from pathlib import Path

# Create directories
Path('data').mkdir(exist_ok=True)
Path('models').mkdir(exist_ok=True)

# Prepare full dataset with predictions
full_predictions_df = df_hour.copy()

# Add Ridge predictions (using best model)
full_predictions_df['ml_predicted_kwh'] = np.nan
full_predictions_df.loc[test_df.index, 'ml_predicted_kwh'] = predictions_ridge

# For training data, predict as well
if len(train_df) > 0:
    train_features = train_df[feature_columns]
    full_predictions_df.loc[train_df.index, 'ml_predicted_kwh'] = best_ridge_model.predict(train_features)

# Ensure required columns
required_columns = ['generation_kwh', 'ml_predicted_kwh', 'clearsky_expected_kwh']
export_df = full_predictions_df[required_columns].copy()

# Export to parquet
export_df.to_parquet('data/predictions.parquet')
print(f"✅ Exported {len(export_df)} rows to data/predictions.parquet")

# Export the trained model
with open('models/ridge_model.pkl', 'wb') as f:
    pickle.dump(best_ridge_model, f)
print("✅ Exported model to models/ridge_model.pkl")

# Export feature columns
with open('models/feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_columns, f)
print("✅ Exported feature columns")
```

**Or run the helper script:**

```bash
python export_predictions.py
```

This will show you the code to add to your notebook and verify the exported files.

### Step 3: Run the Streamlit App

```bash
streamlit run app_solar_monitoring.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 📊 Dashboard Tabs

### 1. 📊 Overview
- **Daily Metrics**: Latest production, predictions, performance ratio
- **Alert System**: Visual warnings for underperformance
- **Performance Trend**: Last 30 days performance ratio
- **Daily Production**: Bar chart comparison

### 2. 📈 Detailed Analysis
- **3-Line Comparison**: Actual vs ML vs Clear-Sky
- **Residual Analysis**: Error visualization with alert thresholds
- **Period Statistics**: Total production for selected date range

### 3. 🚨 Anomaly Detection
- **Anomalous Days Table**: All days with significant underperformance
- **Color-coded Performance**: Red (poor), orange (warning), green (good)
- **Deficit Calculation**: Energy loss on anomalous days

### 4. 📉 Model Performance
- **Test Set Metrics**: MAE, RMSE, R², MAPE
- **Scatter Plot**: Predicted vs Actual
- **Error Distribution**: Histogram of prediction errors

## ⚙️ Configuration

### Sidebar Settings

- **Date Range**: Select time period to analyze
- **Alert Threshold**: Set percentage threshold for anomaly detection (default: 20%)
- **Recent Days**: Number of days to show in trend analysis (7-90 days)
- **Show Clear-Sky**: Toggle clear-sky reference line

### Plant Configuration

Edit `PLANT_CONFIG` in `app_solar_monitoring.py`:

```python
PLANT_CONFIG = {
    'name': 'HKL GGI',
    'capacity_kwp': 269.28,
    'latitude': 22.3027,
    'longitude': 114.1772,
    'timezone': 'Asia/Hong_Kong',
    'alert_threshold_pct': 20  # Alert if actual < predicted by 20%
}
```

## 📁 Required File Structure

```
SOLroof/
├── app_solar_monitoring.py       # Main Streamlit app
├── export_predictions.py         # Helper script
├── requirements_streamlit.txt    # Dependencies
├── data/
│   └── predictions.parquet       # Exported predictions (required)
└── models/
    ├── ridge_model.pkl           # Trained model (optional)
    └── feature_columns.pkl       # Feature list (optional)
```

## 🔍 How It Works

### ML Prediction vs Clear-Sky

**Traditional Method (Not Used):**
- Compare actual production to theoretical clear-sky maximum
- Problem: Flags normal cloudy days as failures

**ML Method (Used in this app):**
- Train model on historical data with actual weather conditions
- Predict expected production based on current weather
- Only flag deviations that indicate real problems (equipment failure, soiling)

### Anomaly Detection Logic

```python
# Performance ratio
performance_ratio = (actual_production / ml_predicted_production) × 100%

# Anomaly if:
performance_ratio < (100% - alert_threshold)

# Example with 20% threshold:
# - Actual: 80 kWh, Predicted: 100 kWh → 80% ratio → ANOMALY (20% below)
# - Actual: 85 kWh, Predicted: 100 kWh → 85% ratio → OK (15% below)
```

## 🎨 Customization

### Change Color Scheme

Edit the CSS in `app_solar_monitoring.py`:

```python
st.markdown("""
    <style>
    .main-header {
        color: #FF6B35;  # Change header color
    }
    .metric-card {
        border-left: 4px solid #FF6B35;  # Change accent color
    }
    </style>
""", unsafe_allow_html=True)
```

### Add New Metrics

Example: Add capacity factor calculation

```python
# In calculate_daily_metrics function
metrics['capacity_factor'] = (
    metrics['actual_total'] / (PLANT_CONFIG['capacity_kwp'] * 24)
) * 100
```

### Export Reports

Add export functionality to any tab:

```python
# Add download button for anomaly report
if st.button("📥 Download Anomaly Report"):
    anomaly_df.to_csv('anomaly_report.csv', index=False)
    st.success("Report downloaded!")
```

## 🐛 Troubleshooting

### App shows "Unable to load data"
- **Solution**: Run Step 2 to export predictions from the notebook
- **Check**: Verify `data/predictions.parquet` exists and contains data

### "Module not found" error
- **Solution**: Install dependencies with `pip install -r requirements_streamlit.txt`

### Charts not displaying
- **Solution**: Ensure Plotly is installed: `pip install plotly`

### Performance is slow
- **Solution**: Reduce `num_recent_days` in sidebar
- **Solution**: Add `@st.cache_data` decorator to expensive functions

## 📈 Performance Tips

1. **Limit date ranges**: Analyzing 30 days is much faster than 365 days
2. **Use parquet format**: Much faster than CSV for large datasets
3. **Enable caching**: Functions with `@st.cache_data` are cached automatically

## 🔐 Security Note

This dashboard is designed for **local use**. Before deploying to production:

1. Add authentication (e.g., `streamlit-authenticator`)
2. Restrict file access
3. Use environment variables for sensitive config
4. Enable HTTPS

## 📞 Support

For issues or questions:
1. Check `export_predictions.py` output for file verification
2. Verify notebook has been run completely
3. Check Streamlit logs in terminal

## 📄 License

Internal use - Solar plant monitoring system

---

**Built with:**
- Streamlit for the web interface
- Plotly for interactive visualizations
- Scikit-learn Ridge Regression for ML predictions
- Pandas for data processing
