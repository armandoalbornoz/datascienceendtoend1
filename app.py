# app.py
import os
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import joblib
from src.datascience.utils.common import dvc_pull_once

# Config


MODEL_PATH = "artifacts/model_trainer/best_model.joblib"

if not Path(MODEL_PATH).exists():
    dvc_pull_once()


DEFAULT_MODEL_PATH = "artifacts/model_trainer/best_model.joblib"
DEFAULT_FEATURES_PATH = "artifacts/model_trainer/feature_names.json"

# Fallback feature order (exactly as in your CSV)
DEFAULT_FEATURES = [
    "surface_pressure_avg",
    "temperature_2m_avg",
    "daily_sunshine",
    "daily_et0_fao_evapotranspiration",
    "relative_humidity_2m_avg",
    "cloud_cover_avg",
    "wind_speed_10m_avg",
    "wind_dir_sin",
    "wind_dir_cos",
]

# -----------------------------
# Helpers
# -----------------------------
@st.cache_resource
def load_model(model_path: str):
    return joblib.load(model_path)

def load_feature_names(path: str | Path) -> list[str]:
    p = Path(path)
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            pass
    return DEFAULT_FEATURES

def compute_wind_components(deg: float) -> tuple[float, float]:
    # Convert meteorological degrees to unit-circle sin/cos (0-360 allowed)
    rad = math.radians(deg % 360.0)
    return math.sin(rad), math.cos(rad)

def predict_once(model, row: dict, features: list[str]):
    # Build single-row DataFrame, coerce numerics, enforce schema & order
    df = pd.DataFrame([row]).apply(pd.to_numeric, errors="coerce")
    df = df.reindex(columns=features, fill_value=0.0)

    # Predict
    y = model.predict(df)[0]
    score = None
    is_prob = False
    if hasattr(model, "predict_proba"):
        score = float(model.predict_proba(df)[:, 1][0])
        is_prob = True
    elif hasattr(model, "decision_function"):
        score = float(model.decision_function(df)[0])
        is_prob = False
    return int(y), score, is_prob, df

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="Rain Prediction", page_icon="🌧️", layout="centered")

st.markdown(
    """
    <style>
      .bubble {border-radius: 14px; padding: 14px 16px; margin: 8px 0;}
      .assistant { background: #f1f5f9; }
      .user { background: #ecfeff; }
      .small { font-size: 0.85rem; color: #57606a; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌧️ Rain Prediction")
st.caption("Expects the same **transformed** features used during training.")

# Paths
model_path = st.sidebar.text_input("Model path", DEFAULT_MODEL_PATH)
features_path = st.sidebar.text_input("Feature names path (optional)", DEFAULT_FEATURES_PATH)

# Load model + features
try:
    model = load_model(model_path)
    st.sidebar.success("Model loaded")
except Exception as e:
    st.sidebar.error(f"Failed to load model: {e}")
    st.stop()

FEATURES = load_feature_names(features_path)


st.markdown('<div class="bubble user">', unsafe_allow_html=True)
st.subheader("Input features")

# Because your model expects already-transformed features (log/standardized),
# we default inputs to 0.0. If you want to feed raw values, you’ll need to
# replicate the exact training transforms here (or serve a Pipeline).
col1, col2 = st.columns(2)

with col1:
    surface_pressure_avg = st.number_input("surface_pressure_avg", value=0.0, step=0.01)
    temperature_2m_avg = st.number_input("temperature_2m_avg", value=0.0, step=0.01)
    daily_sunshine = st.number_input("daily_sunshine", value=0.0, step=0.01,
                                     help="Transformed value used during training")
    daily_et0 = st.number_input("daily_et0_fao_evapotranspiration", value=0.0, step=0.01)

with col2:
    relative_humidity_2m_avg = st.number_input("relative_humidity_2m_avg", value=0.0, step=0.01)
    cloud_cover_avg = st.number_input("cloud_cover_avg", value=0.0, step=0.01)
    wind_speed_10m_avg = st.number_input("wind_speed_10m_avg", value=0.0, step=0.01,
                                         help="Transformed value used during training")
    wind_deg = st.slider("wind_direction (degrees)", min_value=0, max_value=359, value=0)

# Compute sin/cos from degrees for the required features
wind_sin, wind_cos = compute_wind_components(wind_deg)

row = {
    "surface_pressure_avg": surface_pressure_avg,
    "temperature_2m_avg": temperature_2m_avg,
    "daily_sunshine": daily_sunshine,
    "daily_et0_fao_evapotranspiration": daily_et0,
    "relative_humidity_2m_avg": relative_humidity_2m_avg,
    "cloud_cover_avg": cloud_cover_avg,
    "wind_speed_10m_avg": wind_speed_10m_avg,
    "wind_dir_sin": wind_sin,
    "wind_dir_cos": wind_cos,
}

st.markdown("</div>", unsafe_allow_html=True)

with st.expander("Show input row (dict)"):
    st.json(row)

# Predict button
if st.button("Predict"):
    try:
        label, score, is_prob, df_used = predict_once(model, row, FEATURES)

        st.markdown('<div class="bubble assistant">', unsafe_allow_html=True)
        st.markdown(
            f"**Prediction:** {'🌧️ Rain' if int(label)==1 else '🌤️ No rain'}"
        )
        if score is not None:
            if is_prob:
                st.write(f"**Probability of rain:** {100 * score:.2f}%")
            else:
                st.write(f"**Decision score:** {score:.3f}")
        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("Show DataFrame passed to model (enforced order)"):
            st.dataframe(df_used)

    except Exception as e:
        st.error(f"Prediction failed: {e}")

st.markdown(
    '<p class="small">Thanks for using the app :)</p>',
    unsafe_allow_html=True,
)
