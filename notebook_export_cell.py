"""
COPY-PASTE THIS CELL AT THE END OF HKL_ML_comparison_v2.ipynb
This will export all necessary files for the Streamlit dashboard
"""

# ==================================================================================
# EXPORT FOR STREAMLIT DASHBOARD
# ==================================================================================

import pickle
from pathlib import Path

print("=" * 80)
print("EXPORTING PREDICTIONS FOR STREAMLIT DASHBOARD")
print("=" * 80)

# Create directories
Path('data').mkdir(exist_ok=True)
Path('models').mkdir(exist_ok=True)

# 1. Prepare full dataset with predictions
full_predictions_df = df_hour.copy()

# Initialize ml_predicted_kwh column
full_predictions_df['ml_predicted_kwh'] = np.nan

# Add Ridge predictions to test set
full_predictions_df.loc[test_df.index, 'ml_predicted_kwh'] = predictions_ridge

# Add predictions for training set (optional but recommended for full coverage)
if len(train_df) > 0:
    train_features = train_df[feature_columns]
    train_predictions = best_ridge_model.predict(train_features)
    full_predictions_df.loc[train_df.index, 'ml_predicted_kwh'] = train_predictions
    print(f"✅ Added predictions for {len(train_df)} training samples")

print(f"✅ Added predictions for {len(test_df)} test samples")

# 2. Verify required columns exist
required_columns = ['generation_kwh', 'ml_predicted_kwh', 'clearsky_expected_kwh']

missing_columns = [col for col in required_columns if col not in full_predictions_df.columns]
if missing_columns:
    print(f"❌ ERROR: Missing columns: {missing_columns}")
else:
    print(f"✅ All required columns present: {required_columns}")

# 3. Export to parquet (efficient format for Streamlit)
export_df = full_predictions_df[required_columns].copy()

# Remove any NaN predictions (if any remain)
export_df_clean = export_df.dropna(subset=['ml_predicted_kwh'])

export_df_clean.to_parquet('data/predictions.parquet')
print(f"✅ Exported {len(export_df_clean)} rows to data/predictions.parquet")
print(f"   Date range: {export_df_clean.index.min()} to {export_df_clean.index.max()}")

# 4. Export the trained Ridge model
with open('models/ridge_model.pkl', 'wb') as f:
    pickle.dump(best_ridge_model, f)
print("✅ Exported trained Ridge model to models/ridge_model.pkl")
print(f"   Model parameters: alpha={best_ridge_params['alpha']}")

# 5. Export feature columns for future reference
with open('models/feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_columns, f)
print(f"✅ Exported {len(feature_columns)} feature columns to models/feature_columns.pkl")

# 6. Export model performance metrics
metrics_dict = {
    'model_name': 'Ridge Regression',
    'test_mae': test_mae_ridge,
    'test_rmse': test_rmse_ridge,
    'test_r2': test_r2_ridge,
    'test_mape': test_mape_ridge,
    'best_params': best_ridge_params,
    'num_features': len(feature_columns),
    'train_samples': len(train_df),
    'test_samples': len(test_df),
    'export_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
}

with open('models/model_metrics.pkl', 'wb') as f:
    pickle.dump(metrics_dict, f)
print("✅ Exported model metrics to models/model_metrics.pkl")

print("\n" + "=" * 80)
print("✅ EXPORT COMPLETE - STREAMLIT DASHBOARD IS READY!")
print("=" * 80)
print("\n🚀 To launch the dashboard, run in terminal:")
print("\n   streamlit run app_solar_monitoring.py")
print("\n📖 For detailed instructions, see: README_STREAMLIT.md")
print("=" * 80)
