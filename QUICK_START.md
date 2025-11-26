# 🚀 Quick Start Guide - Solar Monitoring Dashboard

## 📋 3 Simple Steps to Launch

### Step 1: Install Dependencies (2 minutes)

```bash
pip install -r requirements_streamlit.txt
```

### Step 2: Export Data from Notebook (1 minute)

**Option A - Easy Copy-Paste:**
1. Open `HKL_ML_comparison_v2.ipynb`
2. Create a new cell at the end
3. Copy ALL code from `notebook_export_cell.py`
4. Paste into the new cell
5. Run the cell

**Option B - Manual Check:**
```bash
python export_predictions.py
```
This shows you what code to add and verifies your exports.

### Step 3: Launch Dashboard (10 seconds)

```bash
streamlit run app_solar_monitoring.py
```

**Done! 🎉** The dashboard opens at `http://localhost:8501`

---

## ✅ Verification Checklist

Before running Streamlit, verify these files exist:

```bash
ls data/predictions.parquet          # ✅ Should exist
ls models/ridge_model.pkl            # ✅ Should exist
ls models/feature_columns.pkl        # ✅ Should exist
```

If any are missing, go back to Step 2.

---

## 🎯 What You'll See

### Tab 1: Overview
- Daily production metrics
- Performance alerts (if any)
- 30-day trend chart
- Daily production comparison

### Tab 2: Detailed Analysis
- 3-line comparison (Actual vs ML vs Clear-Sky)
- Residual analysis with alert zones
- Custom date range selection

### Tab 3: Anomaly Detection
- Table of all underperforming days
- Color-coded performance ratios
- Energy deficit calculations

### Tab 4: Model Performance
- MAE, RMSE, R², MAPE metrics
- Predicted vs Actual scatter plot
- Error distribution histogram

---

## 🎨 First-Time Setup Tips

1. **Set Alert Threshold**: Start with 20% (default), adjust based on your plant's typical variation

2. **Choose Date Range**: Try last 7 days first to see recent performance

3. **Analyze Anomalies**: Check Tab 3 to identify problematic days

4. **Verify Accuracy**: Compare ML predictions to Clear-Sky in Tab 2

---

## 🐛 Common Issues

### "Unable to load data"
```bash
# Run this to check:
python export_predictions.py
# Then re-run Step 2 if files are missing
```

### "Module not found"
```bash
# Re-install dependencies:
pip install -r requirements_streamlit.txt
```

### Dashboard is slow
- Reduce date range in sidebar
- Decrease "Recent days to analyze" slider

---

## 📱 Daily Usage Workflow

1. **Morning Check** (1 minute):
   - Open dashboard
   - Check Overview tab for yesterday's performance
   - Look for red alerts

2. **Weekly Review** (5 minutes):
   - Tab 2: Review 7-day trend
   - Tab 3: Investigate any anomalies
   - Adjust alert threshold if needed

3. **Monthly Analysis** (15 minutes):
   - Tab 2: Set date range to last 30 days
   - Tab 3: Export anomaly list for maintenance planning
   - Tab 4: Verify model accuracy

---

## 💡 Pro Tips

### Custom Alert Threshold
Sidebar → "Alert threshold (%)" → Adjust based on:
- **15%**: Strict monitoring (more alerts)
- **20%**: Balanced (recommended)
- **30%**: Relaxed (fewer alerts)

### Best Date Ranges
- **Last 7 days**: Daily monitoring
- **Last 30 days**: Monthly reports
- **Last 90 days**: Seasonal analysis
- **Custom**: Investigate specific events

### Export Data
From any chart, click the Plotly toolbar:
- 📷 Download as PNG
- 🔍 Zoom and pan
- 📊 Hover for exact values

---

## 🔄 Updating Data

When new data arrives:

1. Re-run `HKL_ML_comparison_v2.ipynb` with new data
2. Re-run the export cell (from `notebook_export_cell.py`)
3. Refresh Streamlit browser tab (press R)

**No need to restart Streamlit!**

---

## 📞 Need Help?

Check in order:
1. This guide
2. `README_STREAMLIT.md` (detailed documentation)
3. Run `python export_predictions.py` (diagnostics)
4. Check terminal for Streamlit error messages

---

## 🎓 Understanding the Metrics

### Performance Ratio
```
Performance Ratio = (Actual / ML Predicted) × 100%

- 100%: Perfect match
- >100%: Better than expected (good weather)
- <80%: Potential issue (check equipment)
```

### Anomaly Detection
```
Anomaly = Performance Ratio < (100% - Alert Threshold)

Example (20% threshold):
- 85% ratio: OK (15% below)
- 75% ratio: ANOMALY (25% below)
```

### Model Accuracy (Tab 4)
```
- MAE: Average error in kWh (lower is better)
- RMSE: Emphasizes large errors (lower is better)
- R²: How well model fits data (higher is better, max 1.0)
- MAPE: Average error percentage (lower is better)
```

---

**Ready to monitor your solar plant! ☀️**
