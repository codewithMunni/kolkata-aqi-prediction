import streamlit as st
import pandas as pd
import altair as alt
import joblib
from pathlib import Path

st.set_page_config(
    page_title="Kolkata AQI Early Warning",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


def html(s: str) -> str:
    """Collapse HTML to one line so Markdown never turns it into a code block."""
    return " ".join(line.strip() for line in s.strip().splitlines())


# ------------------------------------------------------------------ CSS
st.markdown(
    html(
        """
<style>
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {visibility: hidden;}
header {background: transparent;}
.block-container {padding-top: 2.2rem; padding-bottom: 2rem; max-width: 1150px;}

.hero {
    display: flex; align-items: center; gap: 1.2rem;
    background: linear-gradient(120deg, #0b1d26 0%, #14424f 55%, #1f7a8c 100%);
    border: 1px solid rgba(255,255,255,.08);
    padding: 1.8rem 2.2rem; border-radius: 18px; margin-bottom: 1.4rem;
}
.hero-icon {
    flex: 0 0 auto; width: 64px; height: 64px; border-radius: 16px;
    background: rgba(255,255,255,.12); display: flex; align-items: center; justify-content: center;
}
.hero h1 {margin: 0; font-size: 1.9rem; font-weight: 700; color: #ffffff; line-height: 1.2;}
.hero p {margin: .35rem 0 0 0; font-size: .98rem; color: rgba(255,255,255,.82);}
.badge {
    display: inline-block; background: rgba(255,255,255,.14); color: #ffffff;
    padding: 3px 12px; border-radius: 20px; font-size: .76rem; margin: .7rem .4rem 0 0;
}

.card {
    background: #161d27; border: 1px solid #263140; border-radius: 16px;
    padding: 1.5rem 1.7rem; color: #e5e7eb;
}
.card h4 {margin: 0 0 .2rem 0; color: #94a3b8; font-size: .8rem;
          text-transform: uppercase; letter-spacing: .08em; font-weight: 600;}
.big-num {font-size: 4.6rem; font-weight: 800; line-height: 1.05; margin: .2rem 0;}
.cat {font-size: 1.45rem; font-weight: 700; margin-bottom: .5rem;}
.adv {color: #cbd5e1; font-size: .98rem;}

.scale {display: flex; height: 14px; border-radius: 8px; overflow: hidden; margin-top: 1.6rem;}
.scale div {height: 100%;}
.marker-wrap {position: relative; height: 22px;}
.marker {position: absolute; top: 2px; transform: translateX(-50%); font-size: 1.1rem; color: #e5e7eb;}
.scale-labels {display: flex; justify-content: space-between; font-size: .72rem; color: #94a3b8; margin-top: 2px;}

.mini {
    background: #161d27; border: 1px solid #263140; border-radius: 12px;
    padding: .85rem 1.1rem; margin-bottom: .75rem; color: #e5e7eb;
}
.mini span {display: block; font-size: .7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: .06em;}
.mini b {font-size: 1.2rem;}

.note {color: #94a3b8; font-size: .82rem; margin-top: .9rem;}

[data-testid="stExpandSidebarButton"], [data-testid="collapsedControl"] {visibility: visible !important;}

.sec {margin: 1.8rem 0 .8rem 0; font-size: 1.15rem; font-weight: 700; color: #f1f5f9;
      display: flex; align-items: center; gap: .6rem;}
.sec:before {content: ""; width: 5px; height: 1.2rem; background: #2dd4bf; border-radius: 3px;}

.intro {background: linear-gradient(135deg,#161d27 0%,#14313b 100%); border: 1px solid #263140;
        border-radius: 16px; padding: 1.4rem 1.7rem; color: #e5e7eb; font-size: 1rem; line-height: 1.6;}
.intro b {color: #2dd4bf;}

.grid4 {display: grid; grid-template-columns: repeat(4, 1fr); gap: .8rem; margin-top: 1rem;}
.stat {background: #161d27; border: 1px solid #263140; border-radius: 14px; padding: 1rem 1.1rem; text-align: center;}
.stat b {display: block; font-size: 1.9rem; font-weight: 800; color: #2dd4bf; line-height: 1.1;}
.stat span {font-size: .75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: .06em;}

.steps {display: grid; grid-template-columns: repeat(4, 1fr); gap: .8rem;}
.step {background: #161d27; border: 1px solid #263140; border-radius: 14px; padding: 1.1rem 1.1rem 1rem 1.1rem;
       color: #cbd5e1; font-size: .88rem; line-height: 1.5;}
.step .n {display: inline-flex; width: 28px; height: 28px; border-radius: 50%; background: #2dd4bf; color: #0b1d26;
          font-weight: 800; align-items: center; justify-content: center; margin-bottom: .5rem;}
.step h5 {margin: 0 0 .3rem 0; font-size: 1rem; color: #f1f5f9;}

.two {display: grid; grid-template-columns: 1fr 1fr; gap: .8rem;}
.box {background: #161d27; border: 1px solid #263140; border-radius: 14px; padding: 1.1rem 1.3rem;
      color: #cbd5e1; font-size: .92rem; line-height: 1.65;}
.box h5 {margin: 0 0 .5rem 0; font-size: .95rem; color: #f1f5f9;}
.box ul {margin: 0; padding-left: 1.1rem;}

.chips {display: flex; flex-wrap: wrap; gap: .5rem;}
.chip {background: rgba(45,212,191,.12); border: 1px solid rgba(45,212,191,.35); color: #99f6e4;
       padding: 4px 14px; border-radius: 20px; font-size: .82rem;}

.legend {display: grid; grid-template-columns: repeat(6, 1fr); gap: .5rem;}
.lg {border-radius: 10px; padding: .7rem .4rem; text-align: center; color: #0b1d26; font-weight: 700; font-size: .85rem;}
.lg span {display: block; font-weight: 500; font-size: .75rem; opacity: .85;}

@media (max-width: 800px) {
  .grid4, .steps, .two {grid-template-columns: 1fr 1fr;}
  .legend {grid-template-columns: repeat(3, 1fr);}
}
</style>
"""
    ),
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ Model
BASE = Path(__file__).parent
MODEL_PATH = BASE / "model" / "best_model.pkl"
COLS_PATH = BASE / "model" / "columns.pkl"

if not MODEL_PATH.exists() or not COLS_PATH.exists():
    st.error(
        f"Model file not found. Expected at: {MODEL_PATH}\n\n"
        "Run the last cell of the notebook to save the model, "
        "or move the `model` folder next to app.py."
    )
    st.stop()


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH), joblib.load(COLS_PATH)


model, cols = load_model()

# ------------------------------------------------------------------ Helpers
CATEGORIES = [
    (50, "Good", "#00B050", "Air quality is good. Enjoy outdoor activities."),
    (100, "Satisfactory", "#7CC242", "Minor discomfort possible for very sensitive people."),
    (200, "Moderate", "#F5B800", "People with asthma or heart disease should limit outdoor exertion."),
    (300, "Poor", "#FF7C00", "Avoid prolonged outdoor activity. Consider wearing a mask."),
    (400, "Very Poor", "#E53935", "Stay indoors as much as possible. Wear a mask outside."),
    (10_000, "Severe", "#B0173E", "Health emergency. Avoid going outside."),
]


def categorize(v):
    for limit, name, color, advice in CATEGORIES:
        if v <= limit:
            return name, color, advice


def scale_bar(value):
    pos = max(0, min(value, 500)) / 500 * 100
    segs = [(10, "#00B050"), (10, "#7CC242"), (20, "#F5B800"),
            (20, "#FF7C00"), (20, "#E53935"), (20, "#7E0023")]
    bars = "".join(f'<div style="width:{w}%;background:{c}"></div>' for w, c in segs)
    return (
        f'<div class="scale">{bars}</div>'
        f'<div class="marker-wrap"><div class="marker" style="left:{pos}%">▲</div></div>'
        '<div class="scale-labels"><span>0</span><span>50</span><span>100</span>'
        '<span>200</span><span>300</span><span>400</span><span>500+</span></div>'
    )


SEASON_MAP = {12: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

PRESETS = {
    "Clean day": dict(pm25=15.0, pm10=35.0, no=3.0, no2=15.0, nox=18.0, nh3=8.0,
                      co=0.4, so2=4.0, o3=25.0, aqi=45.0, month="Jul", day="Wednesday"),
    "Moderate": dict(pm25=90.0, pm10=165.0, no=30.0, no2=55.0, nox=90.0, nh3=25.0,
                     co=1.1, so2=12.0, o3=38.0, aqi=200.0, month="Nov", day="Friday"),
    "Polluted": dict(pm25=180.0, pm10=300.0, no=60.0, no2=70.0, nox=120.0, nh3=30.0,
                     co=1.8, so2=15.0, o3=25.0, aqi=280.0, month="Jan", day="Monday"),
}


def load_preset(name):
    for k, v in PRESETS[name].items():
        st.session_state[k] = v


for k, v in PRESETS["Moderate"].items():
    st.session_state.setdefault(k, v)

# ------------------------------------------------------------------ Hero
st.markdown(
    html(
        """
<div class="hero">
  <div class="hero-icon">
    <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
      <path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/>
    </svg>
  </div>
  <div>
    <h1>Kolkata AQI Early Warning System</h1>
    <p>Predict tomorrow's Air Quality Index from today's pollutant readings using Machine Learning.</p>
    <span class="badge">Random Forest</span>
    <span class="badge">Next-day forecast</span>
    <span class="badge">Kolkata · 2018–2020 data</span>
  </div>
</div>
"""
    ),
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ Sidebar inputs
with st.sidebar:
    st.header("Today's readings")
    st.caption("Quick examples")
    b1, b2, b3 = st.columns(3)
    b1.button("Clean", on_click=load_preset, args=("Clean day",), use_container_width=True)
    b2.button("Moderate", on_click=load_preset, args=("Moderate",), use_container_width=True)
    b3.button("Polluted", on_click=load_preset, args=("Polluted",), use_container_width=True)

    with st.expander("Particulate matter", expanded=True):
        pm25 = st.number_input("PM2.5 (µg/m³)", 0.0, 500.0, step=1.0, key="pm25")
        pm10 = st.number_input("PM10 (µg/m³)", 0.0, 600.0, step=1.0, key="pm10")

    with st.expander("Gases", expanded=False):
        no = st.number_input("NO", 0.0, 200.0, step=1.0, key="no")
        no2 = st.number_input("NO2", 0.0, 200.0, step=1.0, key="no2")
        nox = st.number_input("NOx", 0.0, 300.0, step=1.0, key="nox")
        nh3 = st.number_input("NH3", 0.0, 100.0, step=1.0, key="nh3")
        co = st.number_input("CO", 0.0, 5.0, step=0.1, key="co")
        so2 = st.number_input("SO2", 0.0, 100.0, step=1.0, key="so2")
        o3 = st.number_input("O3", 0.0, 100.0, step=1.0, key="o3")

    with st.expander("AQI and date", expanded=True):
        aqi = st.number_input("Today's AQI", 0.0, 500.0, step=1.0, key="aqi")
        m_name = st.selectbox("Month", MONTHS, key="month")
        d_name = st.selectbox("Day of week", DAYS, key="day")

    st.caption("Prediction updates automatically when you change a value.")

# ------------------------------------------------------------------ Live prediction
month = MONTHS.index(m_name) + 1
row = {
    "PM2.5": pm25, "PM10": pm10, "NO": no, "NO2": no2, "NOx": nox,
    "NH3": nh3, "CO": co, "SO2": so2, "O3": o3, "AQI": aqi,
    "month": month, "dayofweek": DAYS.index(d_name), "season": SEASON_MAP[month],
}
pred = float(model.predict(pd.DataFrame([row])[cols])[0])

# ------------------------------------------------------------------ Tabs
tab1, tab2, tab3 = st.tabs(["📍 Prediction", "📊 Model performance", "ℹ️ About"])

with tab1:
    name, color, advice = categorize(pred)
    today_name, _, _ = categorize(aqi)
    diff = pred - aqi
    if diff > 5:
        trend, tcolor = "▲ Worsening", "#f87171"
    elif diff < -5:
        trend, tcolor = "▼ Improving", "#4ade80"
    else:
        trend, tcolor = "● Stable", "#94a3b8"

    left, right = st.columns([3, 2])
    with left:
        st.markdown(
            html(
                f"""
<div class="card" style="border-left: 8px solid {color};">
  <h4>Predicted AQI · tomorrow</h4>
  <div class="big-num" style="color:{color};">{pred:.0f}</div>
  <div class="cat" style="color:{color};">{name}</div>
  <div class="adv">{advice}</div>
  {scale_bar(pred)}
  <div class="note">Typical model error: about ±13 AQI points (MAE on test data).</div>
</div>
"""
            ),
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            html(
                f"""
<div class="mini"><span>Today's AQI</span><b>{aqi:.0f} · {today_name}</b></div>
<div class="mini"><span>Change vs today</span>
  <b>{diff:+.0f} &nbsp;<span style="display:inline;color:{tcolor};font-size:1rem;text-transform:none;letter-spacing:0;">{trend}</span></b></div>
<div class="mini"><span>PM2.5 / PM10 input</span><b>{pm25:.0f} / {pm10:.0f}</b></div>
"""
            ),
            unsafe_allow_html=True,
        )

with tab2:
    st.subheader("Model comparison on the test set")
    perf = pd.DataFrame(
        {
            "Model": ["Baseline (Persistence)", "Linear Regression", "Random Forest", "XGBoost"],
            "MAE": [17.393, 14.714, 13.311, 14.800],
            "RMSE": [27.017, 21.197, 18.785, 19.723],
            "R2": [0.841, 0.902, 0.923, 0.915],
        }
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Best model", "Random Forest")
    c2.metric("RMSE", "18.79", delta="-30.5% vs baseline", delta_color="normal")
    c3.metric("R² score", "0.923")

    st.dataframe(perf, use_container_width=True, hide_index=True)

    st.markdown("**RMSE by model (lower is better)**")
    order = alt.Y("Model:N", sort="x", title=None, axis=alt.Axis(labelLimit=250))
    bars = (
        alt.Chart(perf)
        .mark_bar(cornerRadiusEnd=5, size=26)
        .encode(
            x=alt.X("RMSE:Q", title=None),
            y=order,
            color=alt.condition(
                alt.datum.Model == "Random Forest", alt.value("#2dd4bf"), alt.value("#475569")
            ),
            tooltip=["Model", "MAE", "RMSE", "R2"],
        )
    )
    labels = (
        alt.Chart(perf)
        .mark_text(align="left", dx=6, color="#e5e7eb", fontWeight="bold")
        .encode(x="RMSE:Q", y=order, text=alt.Text("RMSE:Q", format=".2f"))
    )
    st.altair_chart((bars + labels).properties(height=190), use_container_width=True)

    st.markdown(
        "The baseline simply assumes tomorrow's AQI equals today's. "
        "Random Forest beats it by about 30% in RMSE and 23% in MAE."
    )

    if hasattr(model, "feature_importances_"):
        st.markdown("**What drives the prediction? (feature importance)**")
        imp = (
            pd.DataFrame({"Feature": cols, "Importance": model.feature_importances_})
            .sort_values("Importance", ascending=False)
            .head(8)
        )
        fy = alt.Y("Feature:N", sort="-x", title=None)
        fbars = (
            alt.Chart(imp)
            .mark_bar(cornerRadiusEnd=5, size=18, color="#2dd4bf")
            .encode(x=alt.X("Importance:Q", title=None), y=fy)
        )
        ftext = (
            alt.Chart(imp)
            .mark_text(align="left", dx=5, color="#e5e7eb")
            .encode(x="Importance:Q", y=fy, text=alt.Text("Importance:Q", format=".2f"))
        )
        st.altair_chart((fbars + ftext).properties(height=260), use_container_width=True)

with tab3:
    st.markdown(
        html(
            """
<div class="intro">
  <b>The problem.</b> Kolkata regularly suffers from poor air quality, especially in winter.
  People usually learn about it only after the air is already bad.
  This project predicts <b>tomorrow's AQI</b> from today's pollutant readings, so schools,
  hospitals and citizens can get an early warning and plan ahead.
</div>
<div class="grid4">
  <div class="stat"><b>814</b><span>Daily records</span></div>
  <div class="stat"><b>4</b><span>Models compared</span></div>
  <div class="stat"><b>0.923</b><span>Best R² score</span></div>
  <div class="stat"><b>30%</b><span>Lower error than baseline</span></div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sec">How it works</div>', unsafe_allow_html=True)
    st.markdown(
        html(
            """
<div class="steps">
  <div class="step"><div class="n">1</div><h5>Collect</h5>
    Daily CPCB air quality readings for Kolkata from the Kaggle dataset.</div>
  <div class="step"><div class="n">2</div><h5>Clean</h5>
    Missing values filled by time interpolation. Month, weekday and season features added.</div>
  <div class="step"><div class="n">3</div><h5>Train</h5>
    Linear Regression, Random Forest and XGBoost trained on the first 80% of days.</div>
  <div class="step"><div class="n">4</div><h5>Predict</h5>
    Best model forecasts tomorrow's AQI and shows a health advisory.</div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sec">AQI categories (CPCB)</div>', unsafe_allow_html=True)
    st.markdown(
        html(
            """
<div class="legend">
  <div class="lg" style="background:#00B050;">Good<span>0 – 50</span></div>
  <div class="lg" style="background:#7CC242;">Satisfactory<span>51 – 100</span></div>
  <div class="lg" style="background:#F5B800;">Moderate<span>101 – 200</span></div>
  <div class="lg" style="background:#FF7C00;">Poor<span>201 – 300</span></div>
  <div class="lg" style="background:#E53935;color:#fff;">Very Poor<span>301 – 400</span></div>
  <div class="lg" style="background:#7E0023;color:#fff;">Severe<span>401+</span></div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sec">Key findings</div>', unsafe_allow_html=True)
    st.markdown(
        html(
            """
<div class="two">
  <div class="box"><h5>Results</h5><ul>
    <li>Random Forest was the best model: MAE 13.3, RMSE 18.8, R² 0.923.</li>
    <li>It cut RMSE by about 30% compared with the naive "tomorrow equals today" baseline.</li>
    <li>Data was split in time order, so the model never sees the future during training.</li>
  </ul></div>
  <div class="box"><h5>Limitations</h5><ul>
    <li>Only Kolkata, mid-2018 to mid-2020. The data includes the 2020 lockdown months.</li>
    <li>City-level readings, not hyperlocal station data.</li>
    <li>No weather inputs such as wind, rain or humidity.</li>
  </ul></div>
</div>
"""
        ),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sec">Tech stack</div>', unsafe_allow_html=True)
    st.markdown(
        html(
            """
<div class="chips">
  <span class="chip">Python</span><span class="chip">pandas</span>
  <span class="chip">scikit-learn</span><span class="chip">XGBoost</span>
  <span class="chip">Altair</span><span class="chip">Streamlit</span>
  <span class="chip">Jupyter</span><span class="chip">GitHub</span>
</div>
"""
        ),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sec">Future work</div>', unsafe_allow_html=True)
    st.markdown(
        html(
            """
<div class="box"><ul>
  <li>Add weather data (wind speed, temperature, humidity) to improve accuracy.</li>
  <li>Use station-level data for truly hyperlocal predictions.</li>
  <li>Forecast several days ahead and try time-series models such as LSTM.</li>
  <li>Deploy publicly on Streamlit Community Cloud.</li>
</ul></div>
"""
        ),
        unsafe_allow_html=True,
    )

    st.caption("For educational use only. Not an official forecast.")