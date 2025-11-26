"""
Export predictions from ML notebook to Streamlit app format
Run this after training the model in HKL_ML_comparison_v2.ipynb
"""

import pandas as pd
import pickle
from pathlib import Path

def export_predictions_for_streamlit():
    """
    Export the test predictions to a format Streamlit can load
    """

    # Paths
    data_dir = Path('data')
    models_dir = Path('models')

    # Create directories if they don't exist
    data_dir.mkdir(exist_ok=True)
    models_dir.mkdir(exist_ok=True)

    print("=" * 80)
    print("EXPORTING PREDICTIONS FOR STREAMLIT")
    print("=" * 80)

    # This should be run from within the Jupyter notebook or after loading the results
    # For now, provide instructions

    print("\n📋 To export predictions, add this code at the end of your notebook:")
    print("\n" + "=" * 80)
    print("""
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

# For training data, use the model to predict (optional)
if len(train_df) > 0:
    train_features = train_df[feature_columns]
    full_predictions_df.loc[train_df.index, 'ml_predicted_kwh'] = best_ridge_model.predict(train_features)

# Ensure required columns exist
required_columns = ['generation_kwh', 'ml_predicted_kwh', 'clearsky_expected_kwh']
export_df = full_predictions_df[required_columns].copy()

# Export to parquet (efficient format)
export_df.to_parquet('data/predictions.parquet')
print(f"✅ Exported {len(export_df)} rows to data/predictions.parquet")

# Export the trained model
with open('models/ridge_model.pkl', 'wb') as f:
    pickle.dump(best_ridge_model, f)
print("✅ Exported trained model to models/ridge_model.pkl")

# Export feature columns for future use
with open('models/feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_columns, f)
print("✅ Exported feature columns to models/feature_columns.pkl")

print("\\n" + "=" * 80)
print("EXPORT COMPLETE - Ready for Streamlit!")
print("=" * 80)
print("\\nRun: streamlit run app_solar_monitoring.py")
    """)
    print("=" * 80)

    # Check if files exist
    print("\n📁 Checking for exported files:")

    pred_file = data_dir / 'predictions.parquet'
    model_file = models_dir / 'ridge_model.pkl'
    features_file = models_dir / 'feature_columns.pkl'

    if pred_file.exists():
        print(f"✅ Predictions file found: {pred_file}")
        df = pd.read_parquet(pred_file)
        print(f"   - Rows: {len(df)}")
        print(f"   - Columns: {list(df.columns)}")
        print(f"   - Date range: {df.index.min()} to {df.index.max()}")
    else:
        print(f"❌ Predictions file not found: {pred_file}")

    if model_file.exists():
        print(f"✅ Model file found: {model_file}")
        with open(model_file, 'rb') as f:
            model = pickle.load(f)
        print(f"   - Model type: {type(model).__name__}")
    else:
        print(f"❌ Model file not found: {model_file}")

    if features_file.exists():
        print(f"✅ Feature columns file found: {features_file}")
    else:
        print(f"❌ Feature columns file not found: {features_file}")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    export_predictions_for_streamlit()
