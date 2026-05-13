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
    0: "🟢 Bajo impacto",
    1: "🔴 Alto impacto humano / Gestión deficiente",
    2: "🟡 Alto daño económico / Respuesta eficiente"
}
CLUSTER_COLORS = {0: "#2d8a4e", 1: "#c0392b", 2: "#c47c2e"}
CLUSTER_DESC = {
    0: "Pocas víctimas, respuesta rápida y recuperación en días. Pérdidas económicas moderadas. Perfil de bajo riesgo y buena gestión.",
    1: "Alta mortalidad y respuesta muy tardía (PC1 alto). Pérdidas económicas elevadas con recuperación prolongada. Requiere intervención prioritaria.",
    2: "Grandes pérdidas económicas pero respuesta muy rápida (PC2 alto). Pocos fallecidos y recuperación acelerada. Típico de países desarrollados ante catástrofes costosas."
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
            HumanidadML
        </div>
        <div style='font-size:0.72rem;color:#a09070;margin-top:4px;letter-spacing:0.06em;text-transform:uppercase;'>
            Gestión de Desastres · IA
        </div>
    </div>
    <div class='sidebar-divider'></div>
    """, unsafe_allow_html=True)

    nav = st.radio("Navegación", [
        "🏠 Inicio",
        "📊 EDA Interactivo",
        "🤖 Predictor: Response Score",
        "📅 Predictor: Días de Recuperación",
        "🔵 Clasificador de Clusters",
        "📋 Comparativa de Modelos"
    ], label_visibility="collapsed")

    st.markdown("""
    <div class='sidebar-divider'></div>
    <div style='font-size:0.72rem;color:#8a7a60;padding:0 4px;line-height:1.8;'>
        <div style='color:#b0a080;font-weight:600;margin-bottom:4px;'>📂 Dataset</div>
        ~50.000 eventos · 24 países · 12 tipos de desastre
        <br><br>
        <div style='color:#b0a080;font-weight:600;margin-bottom:4px;'>🤖 Modelos</div>
        XGBoost · KMeans (k=3) · PCA · UMAP
        <br><br>
        <div style='color:#b0a080;font-weight:600;margin-bottom:4px;'>🎯 Objetivos</div>
        Response Score · Recovery Days · Clustering
    </div>
    """, unsafe_allow_html=True)


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

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("""
        <div class="section-header">
            <h2>🎯 Objetivos del Proyecto</h2>
        </div>
        """, unsafe_allow_html=True)
        for icon, title, desc in [
            ("🔵", "Objetivo 1 — Response Score",
             "Predecir la eficiencia de la respuesta humanitaria (0–100) ante un desastre. "
             "Se entrenan dos versiones: con y sin severity_index para detectar y gestionar el data leakage."),
            ("🟠", "Objetivo 2 — Recovery Days",
             "Estimar cuántos días tardará una región en recuperarse tras el desastre. "
             "La variable objetivo fue transformada con log1p para reducir el sesgo extremo (skewness ≈ 3.1)."),
            ("🟢", "Objetivo 3 — Clustering de Impacto",
             "Segmentar eventos en 3 perfiles de impacto y gestión usando KMeans (k=3) sobre 4 variables clave, "
             "con reducción dimensional PCA y visualización UMAP."),
        ]:
            st.markdown(f"""
            <div class="insight-box">
                <b style="color:#2d4a2d;">{icon} {title}</b>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    with col_r:
        st.markdown("""
        <div class="section-header">
            <h2>🔬 Pipeline del Proyecto</h2>
        </div>
        """, unsafe_allow_html=True)
        for step, desc in [
            ("1️⃣ Limpieza de datos",
             "Eliminación de nulos, corrección de tipos (economic_loss, aid_amount de string €X a float), "
             "detección de outliers y revisión de recovery_days = 0."),
            ("2️⃣ Feature Engineering",
             "Transformación log1p en 5 variables con alta asimetría (casualties: skew 157, economic_loss: 8.2), "
             "One-Hot Encoding de country (24) y disaster_type (12)."),
            ("3️⃣ Modelado supervisado (Obj. 1 y 2)",
             "Comparativa de 7 algoritmos: LinearRegression, Ridge, Lasso, ElasticNet, RandomForest, GBM, XGBoost. "
             "XGBoost lidera en los tres objetivos."),
            ("4️⃣ Clustering (Obj. 3)",
             "KMeans k=3 con PCA previo. Exploración adicional con DBSCAN y HDBSCAN+UMAP. "
             "Silhouette KMeans en UMAP: 0.3208; en espacio original: 0.2155."),
        ]:
            st.markdown(f"""
            <div class="insight-box">
                <b style="color:#8b6914;">{step}</b>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # Feature Engineering details
    st.markdown("""
    <div class="section-header">
        <h2>⚙️ Feature Engineering — Reducción de Skewness</h2>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        skew_data = pd.DataFrame({
            'Variable': ['casualties', 'economic_loss', 'aid_amount', 'recovery_days', 'response_hours'],
            'Skewness original': [157.5, 8.17, 7.33, 3.10, 2.98],
            'Skewness log1p': [0.72, 0.61, 0.52, 0.38, 0.35]
        })
        fig_skew = go.Figure()
        fig_skew.add_bar(name='Skewness original', x=skew_data['Variable'],
                         y=skew_data['Skewness original'],
                         marker_color='rgba(192,57,43,0.75)')
        fig_skew.add_bar(name='Skewness tras log1p', x=skew_data['Variable'],
                         y=skew_data['Skewness log1p'],
                         marker_color='rgba(45,122,78,0.80)')
        fig_skew.update_layout(**PLOTLY_TEMPLATE, title='Reducción de Skewness con log1p (datos reales)',
                               barmode='group', height=300,
                               legend=dict(orientation='h', y=1.1))
        st.plotly_chart(fig_skew, use_container_width=True)
    with col2:
        st.markdown("""
        <div class="insight-box">
            <b>🔄 Transformaciones log1p</b>
            <p>Las 5 variables con distribuciones muy sesgadas fueron transformadas con log1p.
            Destaca <b>casualties</b>, con un skewness de 157.5 (distribución extrema de eventos con muy pocas víctimas
            y rarísimos eventos masivos), que queda en 0.72 tras la transformación.</p>
        </div>
        <div class="insight-box">
            <b>🏷️ Encoding One-Hot</b>
            <p>Las variables categóricas <b>country</b> (24 países) y <b>disaster_type</b> (12 tipos) 
            fueron codificadas con get_dummies, añadiendo 36 columnas binarias adicionales.</p>
        </div>
        <div class="insight-box">
            <b>📏 Estandarización</b>
            <p>StandardScaler aplicado en train y transformado en test por separado para cada objetivo,
            evitando data leakage de escala. Los scalers están guardados como .pkl para reproducibilidad.</p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA: EDA INTERACTIVO (datos reales del CSV)
# ═══════════════════════════════════════════════════════════
elif nav == "📊 EDA Interactivo":
    st.markdown("""
    <div class="section-header">
        <h2>📊 Análisis Exploratorio de Datos (EDA)</h2>
        <p>Basado en los datos reales del dataset — 49.970 eventos, 24 países, 12 tipos de desastre</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Distribuciones", "🌍 Análisis por País",
        "⚡ Por Tipo de Desastre", "🔗 Correlaciones"
    ])

    # ─ Tab 1: Distribuciones ─
    with tab1:
        col_v, col_t = st.columns([2, 1])
        with col_v:
            var = st.selectbox("Variable a visualizar:", [
                'recovery_days', 'response_score', 'casualties',
                'economic_loss', 'response_hours', 'aid_amount', 'severity_index'
            ])
        with col_t:
            chart_type = st.radio("Tipo:", ["Histograma", "Boxplot", "Log-transform"], horizontal=True)

        sample_eda = df_real.sample(min(5000, len(df_real)), random_state=42)

        if chart_type == "Histograma":
            fig = px.histogram(sample_eda, x=var, nbins=60,
                               color_discrete_sequence=['#2d7a4e'],
                               marginal='rug')
        elif chart_type == "Boxplot":
            fig = px.box(sample_eda, y=var, color_discrete_sequence=['#8b6914'])
        else:
            log_vals = np.log1p(sample_eda[var])
            fig = make_subplots(rows=1, cols=2,
                                subplot_titles=[f'{var} (original)', f'{var} (log1p)'])
            fig.add_histogram(x=sample_eda[var], nbinsx=60,
                              marker_color='rgba(192,57,43,0.7)', name='Original', row=1, col=1)
            fig.add_histogram(x=log_vals, nbinsx=60,
                              marker_color='rgba(45,122,78,0.75)', name='Log1p', row=1, col=2)

        skew_orig = df_real[var].skew()
        skew_msg = (
            "Alta asimetría positiva — existen eventos muy extremos pero la mayoría son moderados."
            if skew_orig > 2 else
            "Alta asimetría negativa — la mayoría de valores están cerca del máximo."
            if skew_orig < -2 else
            "Distribución relativamente simétrica."
        )
        fig.update_layout(**PLOTLY_TEMPLATE, height=380,
                          title=f'{var}  ·  Skewness: {skew_orig:.2f}  (n = {len(df_real):,})',
                          showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
        <div class="insight-box">
        <b>💡 Insight — {var}</b>
        <p>Skewness real sobre los 49.970 eventos: <b>{skew_orig:.3f}</b>. {skew_msg}</p>
        </div>
        """, unsafe_allow_html=True)

    # ─ Tab 2: Por País ─
    with tab2:
        metric_pais = st.selectbox("Métrica:", [
            'recovery_days', 'response_score', 'casualties', 'economic_loss', 'response_hours', 'aid_amount'
        ])

        country_stats = df_real.groupby('country')[metric_pais].agg(['median', 'mean', 'std']).reset_index()
        country_stats = country_stats.sort_values('median', ascending=True)

        colorscale = 'RdYlGn_r' if metric_pais in ('recovery_days', 'casualties', 'response_hours') else 'RdYlGn'

        fig_pais = go.Figure()
        fig_pais.add_bar(
            x=country_stats['median'],
            y=country_stats['country'],
            orientation='h',
            marker=dict(
                color=country_stats['median'],
                colorscale=colorscale,
                showscale=True,
                colorbar=dict(title='Mediana', tickfont=dict(color='#3a2e1a'))
            ),
            text=[f"{v:.1f}" for v in country_stats['median']],
            textposition='outside',
        )
        fig_pais.update_layout(**PLOTLY_TEMPLATE, height=680,
                               title=f'Mediana de {metric_pais} por país (datos reales, n=49.970)',
                               xaxis_title=metric_pais, yaxis_title='',
                               margin=dict(l=130, r=90))
        st.plotly_chart(fig_pais, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <b>💡 Tres grupos de países (recovery_days mediana real)</b>
        <p>
        🟢 <b>Recuperación rápida</b> (&lt;40 días): Japón (18), Alemania (26), EE.UU. (33), Nueva Zelanda (33), Australia (34), Canadá (34)<br>
        🟡 <b>Recuperación media</b> (40–200 días): Francia (37), Irlanda (40), Italia (50), México (74), China (75), España (90), Chile (102), Turquía (114), Bangladesh (115), Filipinas (120), Brasil (123), India (128), Grecia (139), Indonesia (150)<br>
        🔴 <b>Recuperación lenta</b> (&gt;200 días): Sudáfrica (259), Perú (298), Nigeria (402), Congo (688)
        </p>
        </div>
        """, unsafe_allow_html=True)

    # ─ Tab 3: Por Tipo de Desastre ─
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            freq = df_real['disaster_type'].value_counts()
            fig_pie = go.Figure(go.Pie(
                labels=freq.index, values=freq.values,
                hole=0.42,
                marker=dict(colors=[
                    '#2d7a4e','#c47c2e','#8b6914','#c0392b',
                    '#2d4a8b','#6d9e4a','#8b2d4a','#4a8b6d',
                    '#8b7a2d','#4a2d8b','#6d4a2d','#2d6d8b'
                ]),
                textinfo='percent+label',
                textfont_size=10
            ))
            fig_pie.update_layout(**PLOTLY_TEMPLATE, title='Distribución de tipos de desastre (real)',
                                  height=400, showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Recovery days mediana por tipo
            disaster_stats = df_real.groupby('disaster_type')['recovery_days'].median().sort_values()
            fig_dis = go.Figure(go.Bar(
                x=disaster_stats.values,
                y=disaster_stats.index,
                orientation='h',
                marker=dict(
                    color=disaster_stats.values,
                    colorscale='RdYlGn_r',
                    showscale=False
                ),
                text=[f"{v:.0f} días" for v in disaster_stats.values],
                textposition='outside',
            ))
            fig_dis.update_layout(**PLOTLY_TEMPLATE, title='Días de recuperación mediana por tipo (real)',
                                  height=400, margin=dict(l=120, r=80))
            st.plotly_chart(fig_dis, use_container_width=True)

        # Response score por tipo de desastre
        fig_box_dis = px.box(df_real, x='disaster_type', y='response_score',
                             color='disaster_type',
                             color_discrete_sequence=[
                                 '#2d7a4e','#c47c2e','#8b6914','#c0392b',
                                 '#2d4a8b','#6d9e4a','#8b2d4a','#4a8b6d',
                                 '#8b7a2d','#4a2d8b','#6d4a2d','#2d6d8b'
                             ])
        fig_box_dis.update_layout(**PLOTLY_TEMPLATE, title='Response Score por tipo de desastre (n=49.970)',
                                  height=380, showlegend=False, xaxis_tickangle=-40)
        st.plotly_chart(fig_box_dis, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <b>💡 El tipo de desastre influye menos que el país</b>
        <p>Los tsunamis (250 días) y sequías (132 días) presentan recuperaciones más largas, mientras que 
        el frío extremo (31 días), ciclones (44 días) y tornados (43 días) son los más cortos. 
        Sin embargo, la varianza intra-tipo es enorme: el factor país domina sobre el tipo de catástrofe.</p>
        </div>
        """, unsafe_allow_html=True)

    # ─ Tab 4: Correlaciones (datos reales) ─
    with tab4:
        num_cols = ['severity_index', 'casualties', 'economic_loss',
                    'response_hours', 'aid_amount', 'response_score', 'recovery_days']
        corr = df_real[num_cols].corr()

        # Annotate with real values
        fig_heat = go.Figure(go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu',
            zmid=0,
            zmin=-1, zmax=1,
            text=corr.values.round(3),
            texttemplate='%{text}',
            textfont_size=11,
            colorbar=dict(title='r', tickfont=dict(color='#3a2e1a'))
        ))
        fig_heat.update_layout(**PLOTLY_TEMPLATE, title='Heatmap de Correlaciones — datos reales (n=49.970)',
                               height=520, margin=dict(l=120, b=120))
        st.plotly_chart(fig_heat, use_container_width=True)

        # Two key scatter plots with real data
        col1, col2 = st.columns(2)
        sample_sc = df_real.sample(1500, random_state=42)
        with col1:
            fig_sc1 = px.scatter(sample_sc, x='response_hours', y='response_score',
                                 trendline='ols', opacity=0.35,
                                 color_discrete_sequence=['#2d4a8b'])
            corr_rh_rs = df_real['response_hours'].corr(df_real['response_score'])
            fig_sc1.update_layout(**PLOTLY_TEMPLATE, height=340,
                                  title=f'response_hours vs response_score · r = {corr_rh_rs:.3f}')
            st.plotly_chart(fig_sc1, use_container_width=True)
        with col2:
            fig_sc2 = px.scatter(sample_sc, x='economic_loss', y='aid_amount',
                                 trendline='ols', opacity=0.35,
                                 color_discrete_sequence=['#8b6914'])
            corr_el_aa = df_real['economic_loss'].corr(df_real['aid_amount'])
            fig_sc2.update_layout(**PLOTLY_TEMPLATE, height=340,
                                  title=f'economic_loss vs aid_amount · r = {corr_el_aa:.3f}')
            st.plotly_chart(fig_sc2, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <b>💡 Las dos correlaciones más fuertes del dataset</b>
        <p>
        📉 <b>response_hours ↔ response_score</b>: Correlación negativa muy fuerte (r = −0.915). 
        Es la relación más potente del dataset: a más horas hasta responder, peor es el score de respuesta. 
        Esto explica por qué response_hours es la variable más importante en los modelos de Obj. 1 y 2.<br><br>
        📈 <b>aid_amount ↔ economic_loss</b>: Correlación positiva fuerte (r = +0.871). 
        A mayor pérdida económica, más ayuda internacional se moviliza. Refleja el mecanismo real de
        asignación de recursos humanitarios.
        </p>
        </div>
        """, unsafe_allow_html=True)

        # Correlation with severity_index
        st.markdown("""
        <div class="insight-box">
        <b>⚠️ severity_index — correlaciones moderadas con economic_loss y aid_amount</b>
        <p>
        severity_index presenta una correlación moderada con economic_loss (r = +0.381) y aid_amount (r = +0.345), 
        lo que explica el leakage detectado en Objetivo 1: al incluir severity_index, el modelo captura
        indirectamente la magnitud económica del desastre, que a su vez está ligada a cómo se generó response_score
        en el dataset.
        </p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA: PREDICTOR RESPONSE SCORE
# ═══════════════════════════════════════════════════════════
elif nav == "🤖 Predictor: Response Score":
    st.markdown("""
    <div class="section-header">
        <h2>🤖 Predictor de Response Score</h2>
        <p>Estima la eficiencia de la respuesta humanitaria (0–100) con XGBoost</p>
    </div>
    """, unsafe_allow_html=True)

    col_info, col_form = st.columns([1, 2])

    with col_info:
        st.markdown("""
        <div class="insight-box">
        <b>ℹ️ ¿Qué es el Response Score?</b>
        <p>Índice de 0 a 100 que mide la eficiencia de la respuesta humanitaria ante un desastre.
        Un score alto indica respuesta rápida, bien coordinada y con recursos adecuados.</p>
        </div>
        <div class="insight-box">
        <b>🔬 Dos versiones del modelo</b>
        <p>
        <b>Con severity_index</b>: R² = 0.9924 — altísima precisión, pero existe leakage confirmado.<br>
        <b>Sin severity_index</b>: R² = 0.8515 — modelo más honesto con el mundo real, sin fuga de información.
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
        <p>Estima cuántos días tardará una región en recuperarse tras un desastre · XGBoost (R² = 0.787 en log)</p>
    </div>
    """, unsafe_allow_html=True)

    col_info, col_form = st.columns([1, 2])
    with col_info:
        st.markdown("""
        <div class="insight-box">
        <b>ℹ️ Variable objetivo</b>
        <p>recovery_days fue transformada con log1p (skewness original: 3.10) para mejorar el ajuste.
        El modelo predice en escala logarítmica y se reconvierte a días reales con expm1.</p>
        </div>
        <div class="insight-box">
        <b>📊 Rendimiento del modelo</b>
        <p>XGBoost: R²(log) = 0.787 · RMSE = 84.3 días · MAE = 42.4 días<br>
        Los modelos lineales se quedan en R² ≈ 0.695, confirmando la no-linealidad del problema.</p>
        </div>
        <div class="insight-box">
        <b>🌍 El país es el factor clave</b>
        <p>Japón: mediana 18 días. Congo: mediana 688 días. 
        Las capacidades institucionales y económicas del país dominan sobre el tipo de catástrofe.</p>
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
        <h2>🔵 Clasificador de Perfil de Impacto · KMeans k=3</h2>
        <p>Asigna un evento a uno de los 3 perfiles de impacto y gestión. Silhouette (UMAP): 0.3208 · (orig.): 0.2155</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    profiles = [
        ("🟢 Cluster 0", "Bajo impacto", CLUSTER_COLORS[0],
         "Pocas víctimas · Pérdidas moderadas · Respuesta rápida · Recuperación en días"),
        ("🔴 Cluster 1", "Alto impacto humano / Gestión deficiente", CLUSTER_COLORS[1],
         "Alta mortalidad · Respuesta muy tardía (domina PC1, loading 0.67 en casualties) · Recuperación prolongada"),
        ("🟡 Cluster 2", "Alto daño económico / Respuesta eficiente", CLUSTER_COLORS[2],
         "Grandes pérdidas económicas · Respuesta rapidísima (PC2: economic_loss +0.81, response_hours −0.55) · Pocos fallecidos"),
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
    <b>PC1</b> (casualties 0.665 · response_hours 0.572 · economic_loss 0.359 · recovery_days 0.318): 
    Separa el Cluster 1 (alto impacto humano, respuesta tardía) hacia la derecha del eje.<br>
    <b>PC2</b> (economic_loss +0.807 · recovery_days +0.200 · response_hours −0.553 · casualties −0.056): 
    Eleva el Cluster 2: mucho daño económico pero respuesta muy rápida.
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
        st.markdown("**Perfiles de ejemplo rápido:**")
        ex_col1, ex_col2, ex_col3 = st.columns(3)
        example_clicked = None
        with ex_col1:
            if st.button("🟢 Bajo impacto"): example_clicked = 0
        with ex_col2:
            if st.button("🔴 Alto impacto"): example_clicked = 1
        with ex_col3:
            if st.button("🟡 Resiliencia"): example_clicked = 2

        predict_btn = st.button("🔵 Clasificar Evento", key="btn_cl")

    with col_result:
        if predict_btn or example_clicked is not None:
            if example_clicked == 0:
                cas, econ, rh, rd = 20, 50_000, 6, 15
            elif example_clicked == 1:
                cas, econ, rh, rd = 5_000, 50_000_000, 200, 600
            elif example_clicked == 2:
                cas, econ, rh, rd = 100, 80_000_000, 8, 30
            else:
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

            # Radar
            categories = ['Víctimas', 'Pérdida Econ.', 'Horas Resp.', 'Días Recup.']
            maxvals = [500_000, 500_000_000, 10_000, 2000]
            vals = [cas/maxvals[0], econ/maxvals[1], rh/maxvals[2], rd/maxvals[3]]
            fig_radar = go.Figure(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor=f"{color}28",
                line_color=color,
                name='Evento'
            ))
            fig_radar.update_layout(**PLOTLY_TEMPLATE, height=300,
                                    polar=dict(
                                        bgcolor='rgba(255,255,255,0.4)',
                                        radialaxis=dict(visible=True, range=[0, 1],
                                                        tickfont=dict(color='#7a6a55', size=9)),
                                        angularaxis=dict(tickfont=dict(color='#3a2e1a'))
                                    ),
                                    title='Perfil del evento', showlegend=False)
            st.plotly_chart(fig_radar, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA: COMPARATIVA DE MODELOS
# ═══════════════════════════════════════════════════════════
elif nav == "📋 Comparativa de Modelos":
    st.markdown("""
    <div class="section-header">
        <h2>📋 Comparativa de Modelos</h2>
        <p>Resultados reales sobre el conjunto de test para los tres objetivos del proyecto</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Objetivo 1 ── (con severity_index)
    st.markdown("### 🎯 Objetivo 1 — Response Score (con severity_index)")
    models_obj1 = pd.DataFrame({
        'Modelo': ['LinearRegression', 'Ridge', 'Lasso', 'ElasticNet', 'RandomForest', 'GBM', 'XGBoost ⭐'],
        'R²': [0.749287, 0.749291, 0.749287, 0.749288, 0.990375, 0.992065, 0.992382],
        'RMSE': [14.028622, 14.028523, 14.028634, 14.028602, 2.748684, 2.495759, 2.445409],
        'MAE': [10.511150, 10.510926, 10.511507, 10.511394, 1.085094, 1.135990, 0.976698],
    })

    colors_m = ['#a0c0a0', '#8aaa8a', '#6d9e6d', '#4a8b4a', '#c47c2e', '#8b6914', '#2d4a2d']
    fig1 = go.Figure()
    for i, row in models_obj1.iterrows():
        fig1.add_bar(name=row['Modelo'],
                     x=['R²', 'RMSE (÷10)', 'MAE (÷10)'],
                     y=[row['R²'], row['RMSE']/10, row['MAE']/10],
                     marker_color=colors_m[i])
    fig1.update_layout(**PLOTLY_TEMPLATE, height=340, barmode='group',
                       title='Objetivo 1 — métricas por modelo (RMSE y MAE divididos ÷10 para escalar con R²)',
                       legend=dict(orientation='h', y=-0.28, font_size=10))
    st.plotly_chart(fig1, use_container_width=True)
    st.dataframe(
        models_obj1.style
        .highlight_max(subset=['R²'], color='rgba(45,122,78,0.25)')
        .highlight_min(subset=['RMSE', 'MAE'], color='rgba(45,122,78,0.25)')
        .format({'R²': '{:.6f}', 'RMSE': '{:.6f}', 'MAE': '{:.6f}'}),
        use_container_width=True, hide_index=True
    )

    # ── Objetivo 1.2 ── (sin severity_index)
    st.markdown("### 🎯 Objetivo 1.2 — Response Score (sin severity_index)")
    models_obj1_2 = pd.DataFrame({
        'Modelo': ['LinearRegression', 'Ridge', 'Lasso', 'ElasticNet', 'RandomForest', 'GBM', 'XGBoost ⭐'],
        'R²': [0.668132, 0.668128, 0.668113, 0.668113, 0.846718, 0.841169, 0.851505],
        'RMSE': [16.140209, 16.140308, 16.140675, 16.140675, 10.969115, 11.165901, 10.796492],
        'MAE': [12.149566, 12.149629, 12.150406, 12.150406, 6.810396, 7.321383, 6.960620],
    })
    st.markdown("""
    <div class="insight-box">
    <b>⚠️ Leakage en Objetivo 1 — severity_index</b>
    <p>Al eliminar severity_index, el R² de XGBoost cae de 0.9924 a 0.8515. 
    Esto confirma que response_score fue generada usando severity_index y casualties como entradas,
    no al revés. El modelo sin severity_index (Obj. 1.2) es más honesto y generalizable al mundo real.</p>
    </div>
    """, unsafe_allow_html=True)

    fig1_2 = go.Figure()
    for i, row in models_obj1_2.iterrows():
        fig1_2.add_bar(name=row['Modelo'],
                       x=['R²', 'RMSE (÷10)', 'MAE (÷10)'],
                       y=[row['R²'], row['RMSE']/10, row['MAE']/10],
                       marker_color=colors_m[i])
    fig1_2.update_layout(**PLOTLY_TEMPLATE, height=320, barmode='group',
                         title='Objetivo 1.2 — sin severity_index',
                         legend=dict(orientation='h', y=-0.28, font_size=10))
    st.plotly_chart(fig1_2, use_container_width=True)
    st.dataframe(
        models_obj1_2.style
        .highlight_max(subset=['R²'], color='rgba(45,122,78,0.25)')
        .highlight_min(subset=['RMSE', 'MAE'], color='rgba(45,122,78,0.25)')
        .format({'R²': '{:.6f}', 'RMSE': '{:.6f}', 'MAE': '{:.6f}'}),
        use_container_width=True, hide_index=True
    )

    # ── Objetivo 2 ──
    st.markdown("### 📅 Objetivo 2 — Recovery Days (escala log)")
    models_obj2 = pd.DataFrame({
        'Modelo': ['LinearRegression', 'Ridge', 'Lasso', 'ElasticNet', 'RandomForest', 'GBM', 'XGBoost ⭐'],
        'R² (log)': [0.694751, 0.694763, 0.694794, 0.694781, 0.780763, 0.785663, 0.786978],
        'RMSE (días)': [115.176844, 115.203126, 115.569513, 115.284092, 89.024764, 84.182923, 84.257597],
        'MAE (días)': [53.103818, 53.108126, 53.167240, 53.121747, 43.514417, 42.530276, 42.382921],
    })
    st.markdown("""
    <div class="insight-box">
    <b>ℹ️ Métricas en escala original (días)</b>
    <p>El R² se calcula en escala log (donde el modelo opera). RMSE y MAE se reportan en días reales
    para facilitar la interpretación. XGBoost logra un MAE de 42.4 días, frente a los 53.1 días
    de los modelos lineales.</p>
    </div>
    """, unsafe_allow_html=True)

    fig2 = go.Figure()
    for i, row in models_obj2.iterrows():
        fig2.add_bar(name=row['Modelo'],
                     x=['R² (log)', 'RMSE ÷100 (días)', 'MAE ÷100 (días)'],
                     y=[row['R² (log)'], row['RMSE (días)']/100, row['MAE (días)']/100],
                     marker_color=colors_m[i])
    fig2.update_layout(**PLOTLY_TEMPLATE, height=320, barmode='group',
                       title='Objetivo 2 — métricas por modelo',
                       legend=dict(orientation='h', y=-0.28, font_size=10))
    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(
        models_obj2.style
        .highlight_max(subset=['R² (log)'], color='rgba(45,122,78,0.25)')
        .highlight_min(subset=['RMSE (días)', 'MAE (días)'], color='rgba(45,122,78,0.25)')
        .format({'R² (log)': '{:.6f}', 'RMSE (días)': '{:.6f}', 'MAE (días)': '{:.6f}'}),
        use_container_width=True, hide_index=True
    )

    # ── Objetivo 3 ──
    st.markdown("### 🔵 Objetivo 3 — Clustering de Impacto")
    col1, col2 = st.columns(2)
    with col1:
        cluster_metrics = pd.DataFrame({
            'Algoritmo': ['KMeans (k=3) ⭐', 'DBSCAN (eps=0.8)', 'HDBSCAN+UMAP'],
            'Silhouette (UMAP)': [0.3208, 0.0054, '—'],
            'Silhouette (orig.)': [0.2155, 0.2843, '—'],
            'Clusters': [3, 'N+ruido', '3+ruido'],
            'Elegido': ['✅ Sí', '❌ No', '❌ No'],
        })
        st.dataframe(cluster_metrics, use_container_width=True, hide_index=True)
        st.markdown("""
        <div class="insight-box">
        <b>💡 ¿Por qué KMeans k=3?</b>
        <p>A pesar del Silhouette moderado (datos con solapamiento inherente), KMeans k=3 ofrece
        la mejor interpretabilidad. Los loadings de PCA confirman la separación:
        <b>PC1</b> (casualties 0.665, response_hours 0.572) separa el cluster rojo.
        <b>PC2</b> (economic_loss +0.807, response_hours −0.553) eleva el cluster amarillo.
        DBSCAN y HDBSCAN se descartaron por menor interpretabilidad.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        cluster_profiles = pd.DataFrame({
            'Cluster': ['Bajo impacto 🟢', 'Alto impacto humano 🔴', 'Alto daño económico 🟡'],
            'Víctimas (med.)': [8, 580, 45],
            'Pérdida (M€)': [0.08, 8.2, 7.5],
            'Horas resp. (med.)': [12, 180, 14],
            'Días recup. (med.)': [18, 520, 35],
        })
        cluster_colors_list = [CLUSTER_COLORS[0], CLUSTER_COLORS[1], CLUSTER_COLORS[2]]
        metrics_cl = ['Víctimas (med.)', 'Pérdida (M€)', 'Horas resp. (med.)', 'Días recup. (med.)']
        fig_prof = go.Figure()
        for i, row in cluster_profiles.iterrows():
            fig_prof.add_bar(
                name=row['Cluster'],
                x=metrics_cl,
                y=[row['Víctimas (med.)']/10, row['Pérdida (M€)'],
                   row['Horas resp. (med.)']/10, row['Días recup. (med.)']/10],
                marker_color=cluster_colors_list[i]
            )
        fig_prof.update_layout(**PLOTLY_TEMPLATE, barmode='group', height=340,
                               title='Perfil medio por cluster (valores normalizados)',
                               legend=dict(orientation='h', y=1.14, font_size=10))
        st.plotly_chart(fig_prof, use_container_width=True)

    # Global summary
    st.markdown("""
    <div class="section-header" style="margin-top:28px;">
        <h2>🏆 Resumen Global del Proyecto</h2>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    for col, (val, lab) in zip([col1, col2, col3, col4], [
        ("0.9924", "R² Obj.1 con severity_index (XGBoost)"),
        ("0.8515", "R² Obj.1.2 sin leakage (XGBoost)"),
        ("0.7870", "R² Obj.2 en log (XGBoost)"),
        ("0.3208", "Silhouette Obj.3 en UMAP (KMeans)"),
    ]):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{lab}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box" style="margin-top:20px;">
    <b>🔮 Futuros pasos</b>
    <p>
    • Probar HDBSCAN con embeddings UMAP para un clustering más robusto y semántico<br>
    • Añadir variables externas: PIB per cápita, Índice de Desarrollo Humano, gobernanza, temperatura<br>
    • Construir un sistema de alerta temprana que combine los 3 objetivos en un pipeline unificado<br>
    • Validar con datos reales (EM-DAT, ReliefWeb, OCHA) para superar las limitaciones del dataset sintético<br>
    • Explorar modelos de series temporales para capturar tendencias históricas por país
    </p>
    </div>
    """, unsafe_allow_html=True)
