"""
Solar Plant Monitoring Dashboard
HKL GGI - 269.28 kWp
ML-based production monitoring and anomaly detection
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pickle
from pathlib import Path
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Solar Plant Monitoring - HKL GGI",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF6B35;
    }
    .alert-box {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Configuration
PLANT_CONFIG = {
    'name': 'HKL GGI',
    'capacity_kwp': 269.28,
    #'latitude': 22.3027,
    'latitude': 24.0223,
    #'longitude': 114.1772,
    'longitude': 90.2957,
    'timezone': 'Asia/Dhaka',
    'alert_threshold_pct': 20  # Alert if actual < predicted by 20%
}


@st.cache_data
def load_data():
    """Load the processed hourly data with predictions"""
    try:
        # Try to load pre-computed predictions
        data_path = Path('/Users/pr/Documents/_PRO/SIGFRID_DATA/SOLroof/data/predictions.parquet')
        if data_path.exists():
            df = pd.read_parquet(data_path)
            df.index = pd.to_datetime(df.index)
            return df
        else:
            st.warning("⚠️ Predictions file not found. Please run the ML notebook first.")
            return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


@st.cache_resource
def load_model():
    """Load the trained Ridge model"""
    try:
        model_path = Path('/Users/pr/Documents/_PRO/SIGFRID_DATA/SOLroof/models/ridge_model.pkl')
        if model_path.exists():
            with open(model_path, 'rb') as f:
                return pickle.load(f)
        else:
            st.warning("⚠️ Model file not found.")
            return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None


def calculate_daily_metrics(df, date):
    """Calculate daily performance metrics"""
    daily_data = df[df.index.date == date]

    if len(daily_data) == 0:
        return None

    metrics = {
        'actual_total': daily_data['generation_kwh'].sum(),
        'predicted_total': daily_data['ml_predicted_kwh'].sum(),
        'clearsky_total': daily_data['clearsky_expected_kwh'].sum(),
        'actual_peak': daily_data['generation_kwh'].max(),
        'predicted_peak': daily_data['ml_predicted_kwh'].max(),
        'num_hours': len(daily_data),
        'residuals': daily_data['generation_kwh'] - daily_data['ml_predicted_kwh']
    }

    # Calculate performance ratio
    if metrics['predicted_total'] > 0:
        metrics['performance_ratio'] = (metrics['actual_total'] / metrics['predicted_total']) * 100
    else:
        metrics['performance_ratio'] = 0

    # Check for anomalies
    threshold = PLANT_CONFIG['alert_threshold_pct']
    metrics['has_anomaly'] = metrics['performance_ratio'] < (100 - threshold)

    return metrics


def plot_three_line_comparison(df, start_date=None, end_date=None):
    """Create 3-line comparison plot (Actual vs ML vs Clear-Sky)"""
    # Convert date to Timestamp and localize to df's timezone
    tz = df.index.tz if df.index.tz else None
    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    if tz is not None:
        start_ts = start_ts.tz_localize(tz)
        end_ts = end_ts.tz_localize(tz)

    mask = (df.index >= start_ts) & (df.index <= end_ts)
    plot_df = df[mask].copy()

    fig = go.Figure()

    # Actual production
    fig.add_trace(go.Scatter(
        x=plot_df.index,
        y=plot_df['generation_kwh'],
        name='Actual Production',
        line=dict(color='#1f77b4', width=2),
        mode='lines'
    ))

    # ML Prediction
    fig.add_trace(go.Scatter(
        x=plot_df.index,
        y=plot_df['ml_predicted_kwh'],
        name='ML Predicted',
        line=dict(color='#2ca02c', width=2),
        mode='lines'
    ))

    # Clear-Sky (theoretical max)
    fig.add_trace(go.Scatter(
        x=plot_df.index,
        y=plot_df['clearsky_expected_kwh'],
        name='Clear-Sky (Theoretical Max)',
        line=dict(color='#d62728', width=2, dash='dash'),
        mode='lines'
    ))

    fig.update_layout(
        title='Production Comparison: Actual vs ML Prediction vs Clear-Sky',
        xaxis_title='Date',
        yaxis_title='Energy Production (kWh)',
        hovermode='x unified',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


def plot_residuals(df, start_date, end_date):
    """Plot residuals (Actual - Predicted) with alert threshold"""
    # Convert date to Timestamp and localize to df's timezone
    tz = df.index.tz if df.index.tz else None
    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    if tz is not None:
        start_ts = start_ts.tz_localize(tz)
        end_ts = end_ts.tz_localize(tz)

    mask = (df.index >= start_ts) & (df.index <= end_ts)
    plot_df = df[mask].copy()

    plot_df['residual'] = plot_df['generation_kwh'] - plot_df['ml_predicted_kwh']

    # Avoid division by zero
    plot_df['residual_pct'] = np.where(
        plot_df['ml_predicted_kwh'] > 0,
        (plot_df['residual'] / plot_df['ml_predicted_kwh']) * 100,
        0
    )

    # Calculate threshold
    threshold_pct = -PLANT_CONFIG['alert_threshold_pct']

    fig = go.Figure()

    # Color residuals based on threshold
    colors = ['red' if x < threshold_pct else 'green' if x > 0 else 'orange'
              for x in plot_df['residual_pct']]

    fig.add_trace(go.Bar(
        x=plot_df.index,
        y=plot_df['residual_pct'],
        name='Residual %',
        marker_color=colors
    ))

    # Add threshold line
    fig.add_hline(
        y=threshold_pct,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Alert Threshold ({threshold_pct}%)"
    )

    fig.add_hline(y=0, line_dash="dash", line_color="gray")

    fig.update_layout(
        title='Residual Analysis (Actual - Predicted)',
        xaxis_title='Date',
        yaxis_title='Residual (%)',
        hovermode='x unified',
        height=400
    )

    return fig


def plot_daily_summary(df, num_days=30):
    """Plot daily summary for recent days"""
    # Get recent dates
    recent_dates = sorted(df.index.date)[-num_days:]

    daily_metrics = []
    for date in recent_dates:
        metrics = calculate_daily_metrics(df, date)
        if metrics:
            daily_metrics.append({
                'date': date,
                'actual': metrics['actual_total'],
                'predicted': metrics['predicted_total'],
                'performance_ratio': metrics['performance_ratio'],
                'has_anomaly': metrics['has_anomaly']
            })

    daily_df = pd.DataFrame(daily_metrics)

    # Create subplots
    fig = go.Figure()

    # Bar chart for production
    fig.add_trace(go.Bar(
        x=daily_df['date'],
        y=daily_df['actual'],
        name='Actual Daily Production',
        marker_color='#1f77b4'
    ))

    fig.add_trace(go.Bar(
        x=daily_df['date'],
        y=daily_df['predicted'],
        name='Predicted Daily Production',
        marker_color='#2ca02c',
        opacity=0.6
    ))

    fig.update_layout(
        title=f'Daily Production Summary (Last {num_days} Days)',
        xaxis_title='Date',
        yaxis_title='Daily Energy (kWh)',
        barmode='overlay',
        height=400,
        hovermode='x unified'
    )

    return fig


def plot_performance_ratio_trend(df, num_days=30):
    """Plot performance ratio trend"""
    recent_dates = sorted(df.index.date)[-num_days:]

    daily_metrics = []
    for date in recent_dates:
        metrics = calculate_daily_metrics(df, date)
        if metrics:
            daily_metrics.append({
                'date': date,
                'performance_ratio': metrics['performance_ratio'],
                'has_anomaly': metrics['has_anomaly']
            })

    daily_df = pd.DataFrame(daily_metrics)

    # Color based on anomaly
    colors = ['red' if x else 'green' for x in daily_df['has_anomaly']]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=daily_df['date'],
        y=daily_df['performance_ratio'],
        mode='lines+markers',
        name='Performance Ratio',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=8, color=colors)
    ))

    # Add reference lines
    fig.add_hline(y=100, line_dash="dash", line_color="green",
                  annotation_text="100% (Perfect Match)")
    fig.add_hline(y=80, line_dash="dash", line_color="orange",
                  annotation_text="80% (Warning)")

    fig.update_layout(
        title='Performance Ratio Trend (Actual / Predicted × 100%)',
        xaxis_title='Date',
        yaxis_title='Performance Ratio (%)',
        height=400,
        hovermode='x unified'
    )

    return fig


def main():
    """Main Streamlit app"""

    # Header
    st.markdown('<p class="main-header">☀️ Solar Plant Monitoring Dashboard</p>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h3>{PLANT_CONFIG['name']} - {PLANT_CONFIG['capacity_kwp']} kWp</h3>
        <p>ML-based Production Monitoring & Anomaly Detection</p>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    with st.spinner('Loading data...'):
        df = load_data()

    if df is None:
        st.error("❌ Unable to load data. Please ensure the ML notebook has been run.")
        st.info("""
        **To generate predictions:**
        1. Run `HKL_ML_comparison_v2.ipynb` notebook
        2. Ensure it saves predictions to `data/predictions.parquet`
        3. Ensure the trained model is saved to `models/ridge_model.pkl`
        """)
        return

    # Sidebar
    st.sidebar.header("⚙️ Configuration")

    # Date range selector
    min_date = df.index.min().date()
    max_date = df.index.max().date()

    st.sidebar.subheader("📅 Date Range")
    date_range = st.sidebar.date_input(
        "Select date range",
        value=(max_date - timedelta(days=7), max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]

    # Alert threshold
    st.sidebar.subheader("🚨 Alert Settings")
    alert_threshold = st.sidebar.slider(
        "Alert threshold (%)",
        min_value=5,
        max_value=50,
        value=PLANT_CONFIG['alert_threshold_pct'],
        help="Alert when actual production is below predicted by this percentage"
    )
    PLANT_CONFIG['alert_threshold_pct'] = alert_threshold

    # Display mode
    st.sidebar.subheader("📊 Display Options")
    show_clearsky = st.sidebar.checkbox("Show Clear-Sky Reference", value=True)
    num_recent_days = st.sidebar.slider("Recent days to analyze", 7, 90, 30)

    # Main content
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "📈 Detailed Analysis",
        "🚨 Anomaly Detection",
        "📉 Model Performance"
    ])

    # TAB 1: OVERVIEW
    with tab1:
        st.header("Daily Overview")

        # Today's metrics (or most recent day)
        latest_date = df.index.max().date()
        today_metrics = calculate_daily_metrics(df, latest_date)

        if today_metrics:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "📅 Latest Date",
                    latest_date.strftime("%Y-%m-%d")
                )

            with col2:
                st.metric(
                    "⚡ Actual Production",
                    f"{today_metrics['actual_total']:.1f} kWh",
                    delta=f"{today_metrics['actual_total'] - today_metrics['predicted_total']:.1f} kWh"
                )

            with col3:
                st.metric(
                    "🎯 Predicted Production",
                    f"{today_metrics['predicted_total']:.1f} kWh"
                )

            with col4:
                delta_color = "normal" if today_metrics['performance_ratio'] >= 80 else "inverse"
                st.metric(
                    "📊 Performance Ratio",
                    f"{today_metrics['performance_ratio']:.1f}%",
                    delta=f"{today_metrics['performance_ratio'] - 100:.1f}%"
                )

            # Alert box
            if today_metrics['has_anomaly']:
                st.markdown(f"""
                <div class="alert-box">
                    <h3>⚠️ Performance Alert</h3>
                    <p>Actual production is <strong>{100 - today_metrics['performance_ratio']:.1f}%</strong> below predicted value.</p>
                    <p>Please check for:</p>
                    <ul>
                        <li>Equipment malfunction</li>
                        <li>Soiling or shading issues</li>
                        <li>Inverter problems</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="success-box">
                    <h3>✅ System Operating Normally</h3>
                    <p>Performance is within expected range.</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # Recent performance trend
        st.subheader(f"📈 Performance Trend (Last {num_recent_days} Days)")
        fig_perf = plot_performance_ratio_trend(df, num_recent_days)
        st.plotly_chart(fig_perf, use_container_width=True)

        # Daily production summary
        st.subheader(f"📊 Daily Production (Last {num_recent_days} Days)")
        fig_daily = plot_daily_summary(df, num_recent_days)
        st.plotly_chart(fig_daily, use_container_width=True)

    # TAB 2: DETAILED ANALYSIS
    with tab2:
        st.header("Detailed Time Series Analysis")

        # Date range summary
        mask = (df.index.date >= start_date) & (df.index.date <= end_date)
        period_df = df[mask]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Actual", f"{period_df['generation_kwh'].sum():.1f} kWh")
        with col2:
            st.metric("Total Predicted", f"{period_df['ml_predicted_kwh'].sum():.1f} kWh")
        with col3:
            perf_ratio = (period_df['generation_kwh'].sum() / period_df['ml_predicted_kwh'].sum()) * 100
            st.metric("Period Performance", f"{perf_ratio:.1f}%")

        # 3-line comparison
        st.subheader("Production Comparison")
        fig_comparison = plot_three_line_comparison(df, start_date, end_date)
        st.plotly_chart(fig_comparison, use_container_width=True)

        # Residuals
        st.subheader("Residual Analysis")
        fig_residuals = plot_residuals(df, start_date, end_date)
        st.plotly_chart(fig_residuals, use_container_width=True)

    # TAB 3: ANOMALY DETECTION
    with tab3:
        st.header("🚨 Anomaly Detection")

        # Find all anomalous days
        all_dates = sorted(set(df.index.date))
        anomalous_days = []

        for date in all_dates:
            metrics = calculate_daily_metrics(df, date)
            if metrics and metrics['has_anomaly']:
                anomalous_days.append({
                    'Date': date,
                    'Actual (kWh)': metrics['actual_total'],
                    'Predicted (kWh)': metrics['predicted_total'],
                    'Performance (%)': metrics['performance_ratio'],
                    'Deficit (kWh)': metrics['predicted_total'] - metrics['actual_total']
                })

        if anomalous_days:
            st.warning(f"⚠️ Found {len(anomalous_days)} anomalous days")

            anomaly_df = pd.DataFrame(anomalous_days)
            anomaly_df = anomaly_df.sort_values('Date', ascending=False)

            # Format display
            st.dataframe(
                anomaly_df.style.format({
                    'Actual (kWh)': '{:.1f}',
                    'Predicted (kWh)': '{:.1f}',
                    'Performance (%)': '{:.1f}',
                    'Deficit (kWh)': '{:.1f}'
                }).background_gradient(subset=['Performance (%)'], cmap='RdYlGn', vmin=50, vmax=100),
                use_container_width=True,
                height=400
            )

            # Summary statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Anomalous Days", len(anomalous_days))
            with col2:
                avg_perf = anomaly_df['Performance (%)'].mean()
                st.metric("Avg Performance", f"{avg_perf:.1f}%")
            with col3:
                total_deficit = anomaly_df['Deficit (kWh)'].sum()
                st.metric("Total Energy Deficit", f"{total_deficit:.1f} kWh")
        else:
            st.success("✅ No anomalies detected in the dataset!")

    # TAB 4: MODEL PERFORMANCE
    with tab4:
        st.header("📉 Model Performance Metrics")

        # Calculate metrics for test set
        test_date = pd.Timestamp('2024-12-31')
        if df.index.tz is not None:
            test_date = test_date.tz_localize(df.index.tz)
        test_mask = df.index >= test_date
        test_df = df[test_mask]

        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

        y_true = test_df['generation_kwh']
        y_pred = test_df['ml_predicted_kwh']

        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)

        # Calculate MAPE avoiding division by zero
        mask_nonzero = y_true > 0
        if mask_nonzero.sum() > 0:
            mape = np.mean(np.abs((y_true[mask_nonzero] - y_pred[mask_nonzero]) / y_true[mask_nonzero])) * 100
        else:
            mape = 0

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("MAE", f"{mae:.2f} kWh")
        with col2:
            st.metric("RMSE", f"{rmse:.2f} kWh")
        with col3:
            st.metric("R² Score", f"{r2:.4f}")
        with col4:
            st.metric("MAPE", f"{mape:.1f}%")

        st.markdown("---")

        # Scatter plot: Predicted vs Actual
        st.subheader("Predicted vs Actual (Test Set)")

        fig_scatter = go.Figure()

        fig_scatter.add_trace(go.Scatter(
            x=y_pred,
            y=y_true,
            mode='markers',
            marker=dict(size=4, color='#1f77b4', opacity=0.6),
            name='Predictions'
        ))

        # Perfect prediction line
        max_val = max(y_true.max(), y_pred.max())
        fig_scatter.add_trace(go.Scatter(
            x=[0, max_val],
            y=[0, max_val],
            mode='lines',
            line=dict(color='red', dash='dash'),
            name='Perfect Prediction'
        ))

        fig_scatter.update_layout(
            xaxis_title='Predicted (kWh)',
            yaxis_title='Actual (kWh)',
            height=500,
            hovermode='closest'
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

        # Error distribution
        st.subheader("Prediction Error Distribution")

        errors = y_true - y_pred

        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=errors,
            nbinsx=50,
            name='Error Distribution',
            marker_color='#1f77b4'
        ))

        fig_hist.update_layout(
            xaxis_title='Prediction Error (kWh)',
            yaxis_title='Frequency',
            height=400
        )

        st.plotly_chart(fig_hist, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Mean Error", f"{errors.mean():.2f} kWh")
        with col2:
            st.metric("Std Error", f"{errors.std():.2f} kWh")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>Solar Plant Monitoring System | Powered by Ridge Regression ML Model</p>
        <p>Data updated: {}</p>
    </div>
    """.format(df.index.max().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
