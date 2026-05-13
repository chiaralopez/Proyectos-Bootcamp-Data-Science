import streamlit as st
import numpy as np
import pandas as pd
import pickle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ANÁLISIS PREDICTIVO — Gestión de Desastres & Ayuda Humanitaria",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background - warm sand/earth tones */
.stApp {
    background-color: #f5f0e8;
    background-image:
        radial-gradient(ellipse at 10% 20%, rgba(210,160,90,0.12) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(180,100,60,0.10) 0%, transparent 50%),
        url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c4a882' fill-opacity='0.06'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

/* Sidebar - warm terracotta / forest green */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #2d4a2d 0%, #1e3a1e 40%, #3d2a1a 100%);
    border-right: none;
    box-shadow: 4px 0 20px rgba(0,0,0,0.15);
}
[data-testid="stSidebar"] * { color: #e8dcc8 !important; }
[data-testid="stSidebar"] .stRadio label { 
    color: #c4b49a !important; 
    font-size: 0.9rem;
    padding: 6px 0;
}

/* Main content text */
.stMarkdown p, .stText { color: #2c2416; }
h1, h2, h3 { font-family: 'Lora', Georgia, serif; color: #1a2e1a; }

/* ── Cards ── */
.metric-card {
    background: rgba(255,255,255,0.75);
    border: 1px solid rgba(180,140,80,0.25);
    border-top: 4px solid #c47c2e;
    border-radius: 12px;
    padding: 20px 16px;
    text-align: center;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 16px rgba(80,50,20,0.08);
}
.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    font-family: 'Lora', serif;
    color: #8b4513;
    line-height: 1.1;
}
.metric-label {
    font-size: 0.78rem;
    color: #7a6a55;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    font-weight: 500;
}

/* ── Section headers ── */
.section-header {
    background: linear-gradient(135deg, rgba(180,130,60,0.12), rgba(100,130,80,0.10));
    border-left: 5px solid #8b6914;
    border-radius: 0 10px 10px 0;
    padding: 14px 22px;
    margin: 28px 0 18px 0;
    box-shadow: 0 2px 10px rgba(80,50,10,0.06);
}
.section-header h2 { 
    color: #2c2416 !important; 
    margin: 0; 
    font-size: 1.35rem;
    font-family: 'Lora', serif;
}
.section-header p { color: #6b5a3e !important; margin: 5px 0 0 0; font-size: 0.88rem; }

/* ── Hero banner ── */
.hero-banner {
    background: 
        linear-gradient(135deg, rgba(45,74,45,0.92) 0%, rgba(139,105,20,0.85) 50%, rgba(139,69,19,0.90) 100%),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='200'%3E%3Cellipse cx='200' cy='100' rx='180' ry='80' fill='%23ffffff08'/%3E%3C/svg%3E");
    border-radius: 18px;
    padding: 40px 48px;
    text-align: center;
    margin-bottom: 36px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(45,74,45,0.25);
}
.hero-banner::before {
    content: '';
    position: absolute;
    inset: 0;
    background: 
        radial-gradient(circle at 20% 50%, rgba(255,200,100,0.12) 0%, transparent 50%),
        radial-gradient(circle at 80% 50%, rgba(100,170,100,0.08) 0%, transparent 50%);
    pointer-events: none;
}
.hero-title { 
    font-size: 2.1rem; 
    font-weight: 700; 
    font-family: 'Lora', serif;
    color: #f5f0e0; 
    margin: 0; 
    line-height: 1.3; 
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.hero-sub { font-size: 1.05rem; color: #d4c8a0; margin: 12px 0 0 0; }
.hero-icon { font-size: 2.5rem; margin-bottom: 12px; display: block; }

/* ── Prediction result box ── */
.pred-box {
    background: linear-gradient(135deg, rgba(72,140,72,0.12), rgba(100,160,60,0.08));
    border: 2px solid rgba(72,140,72,0.45);
    border-radius: 16px;
    padding: 28px 24px;
    text-align: center;
    margin-top: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}
.pred-box.warning {
    background: linear-gradient(135deg, rgba(200,120,30,0.12), rgba(180,90,20,0.08));
    border-color: rgba(200,120,30,0.45);
}
.pred-box.danger {
    background: linear-gradient(135deg, rgba(180,50,40,0.12), rgba(160,30,20,0.08));
    border-color: rgba(180,50,40,0.45);
}
.pred-value { font-size: 3.2rem; font-weight: 700; font-family: 'Lora', serif; color: #2d7a2d; }
.pred-value.warning { color: #c47c2e; }
.pred-value.danger { color: #b03020; }
.pred-label { font-size: 0.95rem; color: #6b5a3e; margin-top: 6px; }

/* ── Insight boxes ── */
.insight-box {
    background: rgba(255,255,255,0.65);
    border: 1px solid rgba(180,140,80,0.2);
    border-radius: 10px;
    padding: 16px 18px;
    margin: 10px 0;
    border-left: 4px solid #8b6914;
    box-shadow: 0 2px 8px rgba(80,50,10,0.06);
}
.insight-box p { color: #4a3c28 !important; margin: 6px 0 0 0; font-size: 0.88rem; line-height: 1.65; }
.insight-box b { color: #2d4a2d; }

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.6);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(180,140,80,0.2);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: #6b5a3e !important;
    font-weight: 500;
    font-size: 0.88rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2d4a2d, #4a6e2a) !important;
    color: white !important;
}

/* ── Buttons ── */
.stButton button {
    background: linear-gradient(135deg, #2d4a2d, #5a7a2d);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
    padding: 10px 28px;
    transition: all 0.25s;
    width: 100%;
    letter-spacing: 0.02em;
}
.stButton button:hover {
    background: linear-gradient(135deg, #3d6a3d, #6a8a3d);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(45,74,45,0.3);
}

/* ── Number inputs / sliders ── */
.stNumberInput input, .stTextInput input {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(180,140,80,0.3) !important;
    border-radius: 8px !important;
    color: #2c2416 !important;
}
.stSelectbox > div { filter: brightness(1.02); }

/* ── Dataframe ── */
.stDataFrame { background: rgba(255,255,255,0.8) !important; border-radius: 10px; }

/* ── Plotly container ── */
.js-plotly-plot { border-radius: 12px; }

/* ── Alert / info ── */
.stAlert { border-radius: 10px; }

/* Sidebar nav radio */
div[data-testid="stSidebar"] .stRadio > label {
    display: block;
    padding: 8px 14px;
    margin: 2px 0;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
}

/* Horizontal rule in sidebar */
.sidebar-divider {
    border: none;
    border-top: 1px solid rgba(200,180,140,0.25);
    margin: 14px 0;
}
</style>
""", unsafe_allow_html=True)

# ── Rutas robustas: funcionan sea cual sea la ubicación de app.py ─────────────
# Sube por el árbol de directorios hasta encontrar la carpeta src/
from pathlib import Path

def _find_src(start: Path) -> Path:
    """Sube por el árbol hasta encontrar src/ o una carpeta que lo contenga."""
    for p in [start, *start.parents]:
        if p.name == "src":
            return p                   # app.py ya está dentro de src/
        if (p / "src").is_dir():
            return p / "src"           # src/ es hija del directorio actual
    return start                       # fallback

_HERE      = Path(__file__).resolve().parent
SRC_DIR    = _find_src(_HERE)
MODELS_DIR = SRC_DIR / "models" / "production"
DATA_DIR   = SRC_DIR / "data"

# ── Load models ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    def _load(name):
        return pickle.load(open(MODELS_DIR / name, "rb"))
    obj1_xgb      = _load("obj1_xgb.pkl")
    obj1_scaler   = _load("obj1_scaler.pkl")
    obj1_2_xgb    = _load("obj1_2_xgb.pkl")
    obj1_2_scaler = _load("obj1_2_scaler.pkl")
    obj2_xgb      = _load("obj2_xgb.pkl")
    obj2_scaler   = _load("obj2_scaler.pkl")
    obj3_kmeans   = _load("obj3_kmeans.pkl")
    obj3_scaler   = _load("obj3_scaler.pkl")
    return obj1_xgb, obj1_scaler, obj1_2_xgb, obj1_2_scaler, obj2_xgb, obj2_scaler, obj3_kmeans, obj3_scaler

obj1_xgb, obj1_scaler, obj1_2_xgb, obj1_2_scaler, obj2_xgb, obj2_scaler, obj3_kmeans, obj3_scaler = load_models()

# ── Load real data ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv(DATA_DIR / "desastres_y_respuestas_limpio.csv")

df_real = load_data()

# ── Constants ─────────────────────────────────────────────────────────────────
COUNTRIES = sorted(df_real['country'].unique().tolist())
DISASTER_TYPES = sorted(df_real['disaster_type'].unique().tolist())

CLUSTER_NAMES = {
    0: "🟢 Impacto moderado",
    1: "🔴 Alto impacto humano / Mala gestión",
    2: "🟡 Alto daño económico / Buena gestión"
}
CLUSTER_COLORS = {0: "#2d8a4e", 1: "#c0392b", 2: "#c47c2e"}
CLUSTER_DESC = {
    0: "Mediana: 44 víctimas, 550k€ pérdida, 18h respuesta, 81 días recuperación",
    1: "Mediana: 40 víctimas, 800k€ pérdida, 19h respuesta, 668 días recuperación",
    2: "Mediana: 7 víctimas, 160k€ pérdida, 8h respuesta, 54 días recuperación"
}

# Plotly template - warm light theme
PLOTLY_TEMPLATE = dict(
    paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='rgba(255,255,255,0.5)',
    font=dict(color='#3a2e1a', family='DM Sans, sans-serif'),
    xaxis=dict(gridcolor='rgba(180,140,80,0.15)', linecolor='rgba(180,140,80,0.3)', zerolinecolor='rgba(180,140,80,0.2)'),
    yaxis=dict(gridcolor='rgba(180,140,80,0.15)', linecolor='rgba(180,140,80,0.3)', zerolinecolor='rgba(180,140,80,0.2)'),
    colorway=['#2d7a4e','#c47c2e','#8b6914','#c0392b','#2d4a8b','#6d9e4a','#8b2d4a'],
)

# ── Helper functions ──────────────────────────────────────────────────────────
def build_feature_vector(features_dict, feature_names):
    row = {f: 0.0 for f in feature_names}
    for k, v in features_dict.items():
        if k in row:
            row[k] = v
    return pd.DataFrame([row])[feature_names]

def predict_response_score(country, disaster_type, year, severity_index,
                            casualties, economic_loss, aid_amount, recovery_days,
                            use_severity=True):
    feats = {
        'year': year,
        'casualties_log': np.log1p(casualties),
        'economic_loss_log': np.log1p(economic_loss),
        'aid_amount_log': np.log1p(aid_amount),
        'recovery_days_log': np.log1p(recovery_days),
        f'country_{country}': 1.0,
        f'disaster_type_{disaster_type}': 1.0,
    }
    if use_severity:
        feats['severity_index'] = severity_index
        model, scaler = obj1_xgb, obj1_scaler
    else:
        model, scaler = obj1_2_xgb, obj1_2_scaler

    X = build_feature_vector(feats, scaler.feature_names_in_)
    X_sc = scaler.transform(X)
    pred = float(model.predict(X_sc)[0])
    return round(np.clip(pred, 0, 100), 2)

def predict_recovery_days(country, disaster_type, year, severity_index,
                           casualties, economic_loss, aid_amount, response_hours):
    feats = {
        'year': year,
        'severity_index': severity_index,
        'casualties_log': np.log1p(casualties),
        'economic_loss_log': np.log1p(economic_loss),
        'aid_amount_log': np.log1p(aid_amount),
        'response_hours_log': np.log1p(response_hours),
        f'country_{country}': 1.0,
        f'disaster_type_{disaster_type}': 1.0,
    }
    X = build_feature_vector(feats, obj2_scaler.feature_names_in_)
    X_sc = obj2_scaler.transform(X)
    pred_log = float(obj2_xgb.predict(X_sc)[0])
    return round(np.expm1(pred_log), 1)

def predict_cluster(casualties, economic_loss, response_hours, recovery_days):
    feats = np.array([[
        np.log1p(casualties),
        np.log1p(economic_loss),
        np.log1p(response_hours),
        np.log1p(recovery_days)
    ]])
    X_sc = obj3_scaler.transform(feats)
    cluster = int(obj3_kmeans.predict(X_sc)[0])
    distances = obj3_kmeans.transform(X_sc)[0]
    return cluster, distances

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 0 12px 0;'>
        <div style='font-size:2.8rem;'>🌍</div>
        <div style='font-size:1.15rem;font-weight:700;color:#d4c8a0;font-family:Lora,serif;margin-top:6px;'>
            ML Gestión de desastres naturales
        </div>
        <div style='font-size:0.72rem;color:#a09070;margin-top:4px;letter-spacing:0.06em;text-transform:uppercase;'>
            Chiara López Palomino
        </div>
    </div>
    <div class='sidebar-divider'></div>
    """, unsafe_allow_html=True)

    nav = st.radio("Navegación", [
        "🏠 Inicio",
        "📊 Predictor: Response Score",
        "📅 Predictor: Días de Recuperación",
        "🔵 Clasificador de Clusters"
    ], label_visibility="collapsed")


# ═══════════════════════════════════════════════════════════
# PÁGINA: INICIO
# ═══════════════════════════════════════════════════════════
if nav == "🏠 Inicio":
    st.markdown("""
    <div class="hero-banner">
        <span class="hero-icon">🌍🆘🤝</span>
        <div class="hero-title">Análisis Predictivo de la Gestión de la<br>Ayuda Humanitaria y el Impacto de Desastres</div>
        <div class="hero-sub">Machine Learning aplicado a la respuesta ante catástrofes naturales a nivel global</div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    kpis = [
        ("~50.000", "Eventos analizados", "📂"),
        ("24", "Países cubiertos", "🗺️"),
        ("12", "Tipos de desastre", "⚡"),
        ("3", "Objetivos ML (XGBoost + KMeans)", "🤖"),
    ]
    for col, (val, lab, icon) in zip([col1, col2, col3, col4], kpis):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:1.8rem">{icon}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-label">{lab}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA: PREDICTOR RESPONSE SCORE
# ═══════════════════════════════════════════════════════════
elif nav == "📊 Predictor: Response Score":
    st.markdown("""
    <div class="section-header">
        <h2>📊 Predictor de Response Score</h2>
        <p>¿Qué factores hacen que una respuesta a emergencias sea más ágil y eficiente?</p>
    </div>
    """, unsafe_allow_html=True)

    col_info, col_form = st.columns([1, 2])

    with col_info:
        st.markdown("""
        <div class="insight-box">
        <b>ℹ️ ¿Qué es el Response Score?</b>
        <p>Índice de 0 a 100 que mide la eficiencia de la respuesta humanitaria ante un desastre. </p>
        </div>
        <div class="insight-box">
        <b>🔬 Dos versiones del modelo</b>
        <p>
        <b>Con severity_index</b>: R² = 0.9924 - altísima precisión, pero existe leakage confirmado.<br>
        <b>Sin severity_index</b>: R² = 0.8515 - modelo más honesto con el mundo real.
        </p>
        </div>
        <div class="insight-box">
        <b>⚠️ Leakage detectado</b>
        <p>severity_index y casualties_log juntas explican la mayor parte de la importancia del modelo,
        sugiriendo que response_score fue calculado a partir de ellas en el proceso de generación del dataset.
        El modelo sin severity_index (R² = 0.8515) es el recomendado para uso real.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        c1, c2 = st.columns(2)
        with c1:
            country = st.selectbox("🗺️ País", COUNTRIES, key="rs_country")
            disaster = st.selectbox("⚡ Tipo de desastre", DISASTER_TYPES, key="rs_disaster")
            year = st.slider("📅 Año", 2000, 2024, 2018, key="rs_year")
        with c2:
            use_sev = st.toggle("Usar severity_index (con leakage)", value=False)
            if use_sev:
                severity = st.slider("🔴 Severity Index", 0.0, 1.0, 0.5, 0.05)
            else:
                severity = 0.5
            casualties = st.number_input("💀 Víctimas", 0, 100_000, 150, step=10, key="rs_cas")
            economic_loss = st.number_input("💸 Pérdida económica (€)", 0, 100_000_000, 500_000, step=10_000)

        c3, c4 = st.columns(2)
        with c3:
            aid_amount = st.number_input("🤝 Ayuda recibida (€)", 0, 100_000_000, 300_000, step=10_000)
        with c4:
            recovery_days_in = st.number_input("📅 Días de recuperación", 0, 2000, 120, step=5)

        if st.button("🚀 Predecir Response Score", key="btn_rs"):
            with st.spinner("Calculando..."):
                pred = predict_response_score(
                    country, disaster, year, severity,
                    casualties, economic_loss, aid_amount, recovery_days_in, use_sev
                )

            if pred >= 75:
                box_cls, val_cls, emoji, label = "", "", "🟢", "Buena respuesta"
            elif pred >= 50:
                box_cls, val_cls, emoji, label = "warning", "warning", "🟡", "Respuesta moderada"
            else:
                box_cls, val_cls, emoji, label = "danger", "danger", "🔴", "Respuesta deficiente"

            st.markdown(f"""
            <div class="pred-box {box_cls}">
                <div class="pred-value {val_cls}">{pred}</div>
                <div class="pred-label">Response Score (0–100)</div>
                <div style="margin-top:12px;font-size:1.2rem;color:#3a2e1a;">{emoji} {label}</div>
                <div style="color:#7a6a55;font-size:0.8rem;margin-top:8px;">
                    Modelo XGBoost · {'Con severity_index (R²=0.9924)' if use_sev else 'Sin severity_index (R²=0.8515)'}
                </div>
            </div>
            """, unsafe_allow_html=True)

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pred,
                domain={'x': [0, 1], 'y': [0, 1]},
                number={'font': {'size': 40, 'color': '#2c2416', 'family': 'Lora,serif'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickfont': {'color': '#6b5a3e'}},
                    'bar': {'color': '#2d7a4e' if pred >= 75 else '#c47c2e' if pred >= 50 else '#c0392b'},
                    'bgcolor': 'rgba(245,240,232,0.5)',
                    'bordercolor': 'rgba(180,140,80,0.3)',
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(192,57,43,0.12)'},
                        {'range': [50, 75], 'color': 'rgba(196,124,46,0.12)'},
                        {'range': [75, 100], 'color': 'rgba(45,122,78,0.12)'},
                    ],
                    'threshold': {'line': {'color': '#8b6914', 'width': 3}, 'value': 70}
                }
            ))
            fig_gauge.update_layout(**PLOTLY_TEMPLATE, height=260, margin=dict(l=30, r=30, t=20, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA: RECOVERY DAYS
# ═══════════════════════════════════════════════════════════
elif nav == "📅 Predictor: Días de Recuperación":
    st.markdown("""
    <div class="section-header">
        <h2>📅 Predictor de Días de Recuperación</h2>
        <p>¿Cuánto tardará un país en recuperarse de un desastre?</p>
    </div>
    """, unsafe_allow_html=True)

    col_info, col_form = st.columns([1, 2])
    with col_info:
        st.markdown("""
        <div class="insight-box">
        <div class="insight-box">
        <b>📊 Rendimiento del modelo</b>
        <p>XGBoost: R²(log) = 0.787 · RMSE = 84.3 días <br></p>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        c1, c2 = st.columns(2)
        with c1:
            country2 = st.selectbox("🗺️ País", COUNTRIES, key="rd_country")
            disaster2 = st.selectbox("⚡ Tipo de desastre", DISASTER_TYPES, key="rd_disaster")
            year2 = st.slider("📅 Año", 2000, 2024, 2018, key="rd_year")
            severity2 = st.slider("🔴 Severity Index", 0.0, 1.0, 0.5, 0.05, key="rd_sev")
        with c2:
            casualties2 = st.number_input("💀 Víctimas", 0, 100_000, 200, step=10, key="rd_cas")
            economic_loss2 = st.number_input("💸 Pérdida económica (€)", 0, 100_000_000, 1_000_000, step=10_000, key="rd_econ")
            aid_amount2 = st.number_input("🤝 Ayuda recibida (€)", 0, 100_000_000, 600_000, step=10_000, key="rd_aid")
            response_hours2 = st.number_input("⏱️ Horas hasta responder", 0, 5000, 24, step=1)

        if st.button("🚀 Predecir Días de Recuperación", key="btn_rd"):
            with st.spinner("Calculando..."):
                pred_days = predict_recovery_days(
                    country2, disaster2, year2, severity2,
                    casualties2, economic_loss2, aid_amount2, response_hours2
                )

            if pred_days < 60:
                box_cls, val_cls, emoji, label = "", "", "🟢", "Recuperación rápida"
            elif pred_days < 200:
                box_cls, val_cls, emoji, label = "warning", "warning", "🟡", "Recuperación media"
            else:
                box_cls, val_cls, emoji, label = "danger", "danger", "🔴", "Recuperación lenta"

            st.markdown(f"""
            <div class="pred-box {box_cls}">
                <div class="pred-value {val_cls}">{pred_days:.0f} días</div>
                <div class="pred-label">Días estimados de recuperación</div>
                <div style="margin-top:12px;font-size:1.2rem;color:#3a2e1a;">{emoji} {label}</div>
                <div style="color:#7a6a55;font-size:0.8rem;margin-top:8px;">
                    ≈ {pred_days/30:.1f} meses · ≈ {pred_days/365:.1f} años
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Real country reference chart
            ref_countries = {
                'Japón (med. real: 18d)': 18, 'Alemania (26d)': 26,
                'EE.UU. (33d)': 33, 'Australia (34d)': 34,
                'Italia (50d)': 50, 'España (90d)': 90,
                'India (128d)': 128, 'Indonesia (150d)': 150,
                'Sudáfrica (259d)': 259, 'Perú (298d)': 298,
                'Nigeria (402d)': 402, 'Congo (688d)': 688
            }
            ref_df = pd.DataFrame({
                'País': list(ref_countries.keys()) + [f'📍 {country2} (predicción)'],
                'Días': list(ref_countries.values()) + [pred_days],
                'Tipo': ['Referencia (mediana real)'] * len(ref_countries) + ['Tu predicción']
            })
            ref_df = ref_df.sort_values('Días')
            fig_bar = px.bar(ref_df, x='Días', y='País', orientation='h',
                             color='Tipo',
                             color_discrete_map={
                                 'Referencia (mediana real)': '#8b9c6a',
                                 'Tu predicción': '#c47c2e'
                             })
            fig_bar.update_layout(**PLOTLY_TEMPLATE, height=440,
                                  title='Comparativa con medianas reales por país',
                                  legend=dict(orientation='h', y=1.06, font_size=11))
            st.plotly_chart(fig_bar, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA: CLUSTERING
# ═══════════════════════════════════════════════════════════
elif nav == "🔵 Clasificador de Clusters":
    st.markdown("""
    <div class="section-header">
        <h2>🔵 Clasificador de Perfil de Impacto</h2>
        <p>Asigna un evento a uno de los 3 perfiles de impacto y gestión. KMeans k=3 | Silhouette: 0.2155</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    profiles = [
        ("🟡 Cluster 0", "Impacto moderado", CLUSTER_COLORS[2],
         "Mediana: 44 víctimas, 550k€ pérdida, 18h respuesta, 81 días recuperación"),
        ("🔴 Cluster 1", "Alto impacto humano / Mala gestión", CLUSTER_COLORS[1],
         "Mediana: 40 víctimas, 800k€ pérdida, 19h respuesta, 668 días recuperación"),
        ("🟢 Cluster 2", "Alto daño económico / Respuesta eficiente", CLUSTER_COLORS[1],
         "Mediana: 7 víctimas, 160k€ pérdida, 8h respuesta, 54 días recuperación"),
    ]

    for col, (badge, name, color, desc) in zip([col1, col2, col3], profiles):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-top-color:{color};">
                <div style="font-size:1.6rem;">{badge.split()[0]}</div>
                <div style="font-weight:700;color:{color};font-size:0.98rem;margin-top:8px;font-family:Lora,serif;">{name}</div>
                <div style="font-size:0.78rem;color:#6b5a3e;margin-top:10px;line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # PCA loadings insight
st.markdown("""
<div class="insight-box">
<b>🔬 Interpretación PCA que separa los clusters</b>
<p>
<b>PC1</b> (casualties 0.665 · response_hours 0.572 · economic_loss 0.359 · recovery_days 0.318)<br>
<b>PC2</b> (economic_loss +0.807 · recovery_days +0.200 · response_hours −0.553 · casualties −0.056)
</p>
</div>
""", unsafe_allow_html=True)

col_form, col_result = st.columns([1, 1])

with col_form:
    st.markdown("#### Introduce los parámetros del evento")
    casualties3 = st.number_input("💀 Víctimas", 0, 500_000, 100, step=10, key="cl_cas")
    economic_loss3 = st.number_input("💸 Pérdida económica (€)", 0, 500_000_000, 1_000_000, step=50_000, key="cl_econ")
    response_hours3 = st.number_input("⏱️ Horas hasta respuesta", 0, 10_000, 48, step=1, key="cl_rh")
    recovery_days3 = st.number_input("📅 Días de recuperación", 0, 2000, 150, step=5, key="cl_rd")

    st.markdown("---")
    predict_btn = st.button("🔵 Clasificar Evento", key="btn_cl")

    with col_result:
        if predict_btn:
            # Leemos los valores de los inputs
            cas, econ, rh, rd = casualties3, economic_loss3, response_hours3, recovery_days3

            cluster, distances = predict_cluster(cas, econ, rh, rd)
            color = CLUSTER_COLORS[cluster]
            name = CLUSTER_NAMES[cluster]
            desc = CLUSTER_DESC[cluster]

            inv_d = 1 / (distances + 1e-6)
            probs = inv_d / inv_d.sum() * 100

            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.7);
                        border:2px solid {color};
                        border-radius:16px;padding:28px;text-align:center;
                        box-shadow:0 4px 20px rgba(0,0,0,0.08);">
                <div style="font-size:2.4rem;font-weight:700;color:{color};font-family:Lora,serif;">{name}</div>
                <div style="color:#6b5a3e;margin-top:14px;font-size:0.9rem;line-height:1.7;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

            # Gráfico de Barras
            fig_prob = go.Figure(go.Bar(
                x=[CLUSTER_NAMES[i].split('·')[0].strip() for i in range(3)],
                y=probs,
                marker_color=[CLUSTER_COLORS[i] for i in range(3)],
                text=[f"{p:.1f}%" for p in probs],
                textposition='outside',
            ))
            fig_prob.update_layout(**PLOTLY_TEMPLATE, height=280,
                                   title='Afinidad con cada cluster (%)',
                                   yaxis_title='%', showlegend=False,
                                   margin=dict(t=50, b=10))
            st.plotly_chart(fig_prob, use_container_width=True)

            # --- CORRECCIÓN AQUÍ ---
            # Convertimos el color Hex a RGBA para que Plotly acepte la transparencia
            # El '28' original (hex) equivale a aproximadamente 0.15 de opacidad decimal
            hex_color = color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            rgba_fill = f"rgba({r}, {g}, {b}, 0.15)"
            # -----------------------)