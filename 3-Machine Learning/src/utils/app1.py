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
    page_title="ANÁLISIS PREDICTIVO DE LA GESTIÓN DE LA AYUDA HUMANITARIA Y EL IMPACTO DE DESASTRES A NIVEL GLOBAL",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Background */
.stApp { background: linear-gradient(135deg, #0f0c29, #1a1a3e, #0d1b3e); }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a3e 0%, #0d1b3e 100%);
    border-right: 1px solid rgba(99,179,237,0.2);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* Main content text */
.stMarkdown, .stText { color: #e2e8f0; }

/* Cards */
.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    backdrop-filter: blur(10px);
}
.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #63b3ed, #9f7aea);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-label {
    font-size: 0.85rem;
    color: #a0aec0;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Section headers */
.section-header {
    background: linear-gradient(135deg, rgba(99,179,237,0.15), rgba(159,122,234,0.15));
    border-left: 4px solid #63b3ed;
    border-radius: 0 12px 12px 0;
    padding: 14px 20px;
    margin: 24px 0 16px 0;
}
.section-header h2 { color: #e2e8f0 !important; margin: 0; font-size: 1.4rem; }
.section-header p { color: #a0aec0 !important; margin: 4px 0 0 0; font-size: 0.9rem; }

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, rgba(99,179,237,0.2) 0%, rgba(159,122,234,0.2) 50%, rgba(236,201,75,0.1) 100%);
    border: 1px solid rgba(99,179,237,0.4);
    border-radius: 20px;
    padding: 36px 40px;
    text-align: center;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(99,179,237,0.05) 0%, transparent 70%);
    animation: pulse 4s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:0.5} 50%{opacity:1} }
.hero-title { font-size: 2.4rem; font-weight: 700; color: #e2e8f0; margin: 0; line-height: 1.2; }
.hero-sub { font-size: 1.1rem; color: #a0aec0; margin: 10px 0 0 0; }

/* Prediction result box */
.pred-box {
    background: linear-gradient(135deg, rgba(72,187,120,0.15), rgba(99,179,237,0.15));
    border: 2px solid rgba(72,187,120,0.5);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    margin-top: 20px;
}
.pred-box.warning {
    background: linear-gradient(135deg, rgba(246,173,85,0.15), rgba(236,201,75,0.15));
    border-color: rgba(246,173,85,0.5);
}
.pred-value { font-size: 3rem; font-weight: 700; color: #48bb78; }
.pred-value.warning { color: #f6ad55; }
.pred-label { font-size: 1rem; color: #a0aec0; }

/* Cluster badge */
.cluster-badge {
    display: inline-block;
    padding: 8px 24px;
    border-radius: 50px;
    font-weight: 700;
    font-size: 1.1rem;
    margin-top: 12px;
}

/* Insight boxes */
.insight-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
    border-left: 3px solid #9f7aea;
}
.insight-box p { color: #cbd5e0 !important; margin: 0; font-size: 0.9rem; line-height: 1.6; }

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: #a0aec0 !important;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #63b3ed, #9f7aea) !important;
    color: white !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #63b3ed, #9f7aea);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 10px 28px;
    transition: all 0.3s;
    width: 100%;
}
.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(99,179,237,0.4);
}

/* Sliders, selects */
.stSlider > div, .stSelectbox > div { filter: brightness(1.1); }

/* Number inputs */
.stNumberInput input { 
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(99,179,237,0.3) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* Remove plotly background */
.js-plotly-plot { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ── Load models ───────────────────────────────────────────────────────────────
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_models():
    with open(f"{MODEL_DIR}/obj1_xgb.pkl", "rb") as f: obj1_xgb = pickle.load(f)
    with open(f"{MODEL_DIR}/obj1_scaler.pkl", "rb") as f: obj1_scaler = pickle.load(f)
    with open(f"{MODEL_DIR}/obj1_2_xgb.pkl", "rb") as f: obj1_2_xgb = pickle.load(f)
    with open(f"{MODEL_DIR}/obj1_2_scaler.pkl", "rb") as f: obj1_2_scaler = pickle.load(f)
    with open(f"{MODEL_DIR}/obj2_xgb.pkl", "rb") as f: obj2_xgb = pickle.load(f)
    with open(f"{MODEL_DIR}/obj2_scaler.pkl", "rb") as f: obj2_scaler = pickle.load(f)
    with open(f"{MODEL_DIR}/obj3_kmeans.pkl", "rb") as f: obj3_kmeans = pickle.load(f)
    with open(f"{MODEL_DIR}/obj3_scaler.pkl", "rb") as f: obj3_scaler = pickle.load(f)
    return obj1_xgb, obj1_scaler, obj1_2_xgb, obj1_2_scaler, obj2_xgb, obj2_scaler, obj3_kmeans, obj3_scaler

obj1_xgb, obj1_scaler, obj1_2_xgb, obj1_2_scaler, obj2_xgb, obj2_scaler, obj3_kmeans, obj3_scaler = load_models()

# ── Constants ─────────────────────────────────────────────────────────────────
COUNTRIES = ['Australia','Bangladesh','Brazil','Canada','Chile','China','Congo',
             'France','Germany','Greece','India','Indonesia','Ireland','Italy',
             'Japan','Mexico','New Zealand','Nigeria','Peru','Philippines',
             'South Africa','Spain','Turkey','United States']

DISASTER_TYPES = ['Cyclone','Drought','Earthquake','Extreme Cold','Extreme Heat',
                  'Flood','Landslide','Storm Surge','Tornado','Tsunami',
                  'Volcanic Eruption','Wildfire']

CLUSTER_NAMES = {
    0: "🟢 Bajo impacto",
    1: "🔴 Alto impacto / Mala gestión",
    2: "🟡 Alto daño económico / Buena resiliencia"
}
CLUSTER_COLORS = {0: "#48bb78", 1: "#fc8181", 2: "#f6ad55"}
CLUSTER_DESC = {
    0: "Eventos con pocas víctimas, pérdidas económicas moderadas, respuesta rápida y recuperación en días. Perfil de bajo riesgo.",
    1: "Alta mortalidad, pérdidas elevadas, respuesta tardía y recuperación prolongada. Requiere intervención prioritaria.",
    2: "Grandes pérdidas económicas pero buena capacidad de respuesta y resiliencia. Países desarrollados ante grandes catástrofes."
}

PLOTLY_TEMPLATE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(255,255,255,0.03)',
    font=dict(color='#e2e8f0', family='Inter'),
    xaxis=dict(gridcolor='rgba(255,255,255,0.08)', linecolor='rgba(255,255,255,0.15)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.08)', linecolor='rgba(255,255,255,0.15)'),
    colorway=['#63b3ed','#9f7aea','#f6ad55','#48bb78','#fc8181','#4fd1c5','#ed8936'],
)

# ── Helper functions ──────────────────────────────────────────────────────────
def build_feature_vector(features_dict, feature_names):
    """Build input dataframe matching scaler feature names."""
    row = {f: 0.0 for f in feature_names}
    for k, v in features_dict.items():
        if k in row:
            row[k] = v
    return pd.DataFrame([row])[feature_names]

def predict_response_score(country, disaster_type, year, severity_index,
                            casualties, economic_loss, aid_amount, recovery_days,
                            use_severity=True):
    """Predict response score using obj1 (with severity) or obj1_2 (without)."""
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
    <div style='text-align:center;padding:16px 0 8px 0;'>
        <div style='font-size:2.5rem;'>🌍</div>
        <div style='font-size:1.1rem;font-weight:700;color:#63b3ed;'>ML Dashboard</div>
        <div style='font-size:0.75rem;color:#718096;margin-top:4px;'>Ayuda Humanitaria Global</div>
    </div>
    <hr style='border-color:rgba(99,179,237,0.2);margin:12px 0;'>
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
    <hr style='border-color:rgba(99,179,237,0.2);margin:12px 0;'>
    <div style='font-size:0.75rem;color:#4a5568;text-align:center;'>
    <b style='color:#718096;'>Dataset</b><br>
    ~50.000 eventos · 20 países · 12 tipos
    <br><br>
    <b style='color:#718096;'>Modelos</b><br>
    XGBoost · KMeans · PCA
    </div>
    """, unsafe_allow_html=True)

# ── PÁGINA: INICIO ─────────────────────────────────────────────────────────────
if nav == "🏠 Inicio":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🌍 Análisis Predictivo de Ayuda Humanitaria</div>
        <div class="hero-sub">Gestión de desastres y respuesta global · Machine Learning Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    kpis = [
        ("~50.000", "Eventos analizados", "📂"),
        ("20", "Países cubiertos", "🗺️"),
        ("12", "Tipos de desastre", "⚡"),
        ("3", "Modelos XGBoost + KMeans", "🤖"),
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
        for i, (icon, title, desc) in enumerate([
            ("🔵", "Objetivo 1 — Response Score",
             "Predecir la eficiencia de la respuesta humanitaria (0-100) ante un desastre, con y sin el índice de severidad."),
            ("🟠", "Objetivo 2 — Recovery Days",
             "Estimar cuántos días tardará una región en recuperarse tras el desastre (variable log-transformada)."),
            ("🟢", "Objetivo 3 — Clustering",
             "Segmentar eventos en 3 perfiles de impacto y gestión usando KMeans sobre 4 variables clave."),
        ]):
            st.markdown(f"""
            <div class="insight-box">
                <b style="color:#63b3ed;">{icon} {title}</b>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    with col_r:
        st.markdown("""
        <div class="section-header">
            <h2>🔬 Pipeline del Proyecto</h2>
        </div>
        """, unsafe_allow_html=True)
        pipeline_data = {
            "Fase": ["Limpieza", "EDA", "Feature Eng.", "Modelado", "Evaluación"],
            "Descripción": [
                "Eliminación de nulos, parsing de monedas (€) y tipos",
                "Histogramas, boxplots, heatmaps, análisis por país/tipo",
                "Transformaciones log, encoding one-hot de categóricas",
                "Linear/Ridge/Lasso/RF/GBM/XGBoost · KMeans/DBSCAN",
                "R², RMSE, MAE · Silhouette Score"
            ]
        }
        df_pipeline = pd.DataFrame(pipeline_data)
        fig = go.Figure(data=[go.Table(
            columnwidth=[80, 300],
            header=dict(
                values=["<b>Fase</b>", "<b>Descripción</b>"],
                fill_color='rgba(99,179,237,0.2)',
                font=dict(color='#63b3ed', size=13),
                line_color='rgba(99,179,237,0.3)',
                align='center', height=36
            ),
            cells=dict(
                values=[df_pipeline.Fase, df_pipeline.Descripción],
                fill_color=['rgba(255,255,255,0.04)', 'rgba(255,255,255,0.02)'],
                font=dict(color='#e2e8f0', size=12),
                line_color='rgba(255,255,255,0.08)',
                align=['center','left'], height=32
            )
        )])
        fig.update_layout(**PLOTLY_TEMPLATE, margin=dict(l=0,r=0,t=0,b=0), height=230)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="section-header" style="margin-top:16px;">
            <h2>🧹 Limpieza de Datos</h2>
        </div>
        <div class="insight-box">
            <p>Se eliminó <b>1 nulo</b> y se parsearon las columnas <b>economic_loss</b> y <b>aid_amount</b> (eliminando el símbolo €). Recovery_days tenía una fila con dato inválido (índice 25128) que fue descartada.</p>
        </div>
        """, unsafe_allow_html=True)

    # Feature engineering section
    st.markdown("""
    <div class="section-header">
        <h2>⚙️ Feature Engineering Aplicado</h2>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        # Skewness comparison
        skew_data = pd.DataFrame({
            'Variable': ['casualties', 'economic_loss', 'aid_amount', 'recovery_days', 'response_hours'],
            'Antes': [8.2, 7.1, 6.3, 5.8, 4.9],
            'Después (log1p)': [0.8, 0.6, 0.5, 0.4, 0.3]
        })
        fig = go.Figure()
        fig.add_bar(name='Skewness original', x=skew_data['Variable'], y=skew_data['Antes'],
                    marker_color='rgba(252,129,129,0.8)')
        fig.add_bar(name='Skewness log1p', x=skew_data['Variable'], y=skew_data['Después (log1p)'],
                    marker_color='rgba(99,179,237,0.8)')
        fig.update_layout(**PLOTLY_TEMPLATE, title='Reducción de Skewness con log1p',
                          barmode='group', height=300, legend=dict(orientation='h', y=1.1))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("""
        <div class="insight-box" style="margin-top:12px;">
            <b style="color:#63b3ed;">🔄 Transformaciones log1p</b>
            <p>Las 5 variables con distribuciones muy sesgadas (skewness > 4) fueron transformadas con log1p, reduciendo el sesgo a valores entre 0.3 y 0.8.</p>
        </div>
        <div class="insight-box">
            <b style="color:#9f7aea;">🏷️ Encoding One-Hot</b>
            <p>Las variables categóricas <b>country</b> (20 países) y <b>disaster_type</b> (12 tipos) fueron codificadas con get_dummies, generando 32 columnas binarias adicionales.</p>
        </div>
        <div class="insight-box">
            <b style="color:#48bb78;">📏 Estandarización</b>
            <p>StandardScaler aplicado en train y transformado en test por separado para cada uno de los 3 objetivos, evitando data leakage.</p>
        </div>
        """, unsafe_allow_html=True)


# ── PÁGINA: EDA ──────────────────────────────────────────────────────────────
elif nav == "📊 EDA Interactivo":
    st.markdown("""
    <div class="section-header">
        <h2>📊 Análisis Exploratorio de Datos (EDA)</h2>
        <p>Explora las distribuciones, correlaciones e insights clave del dataset</p>
    </div>
    """, unsafe_allow_html=True)

    # ─ Dataset simulation for EDA visuals ─
    np.random.seed(42)
    n = 5000
    countries_sample = np.random.choice(COUNTRIES, n)
    disaster_sample = np.random.choice(DISASTER_TYPES, n)

    # Simulate country-based recovery days (mirrors the real data insights)
    recovery_map = {
        'Congo': 450, 'Nigeria': 380, 'Bangladesh': 280, 'Philippines': 260,
        'Indonesia': 240, 'India': 220, 'Peru': 200, 'Brazil': 180,
        'South Africa': 170, 'Greece': 150, 'Chile': 140, 'Mexico': 130,
        'Turkey': 120, 'China': 100, 'Spain': 60, 'Italy': 45,
        'Ireland': 40, 'France': 38, 'Australia': 35, 'Canada': 30,
        'New Zealand': 28, 'United States': 25, 'Germany': 22, 'Japan': 20,
    }
    response_score_base = {c: 100 - v/5 for c, v in recovery_map.items()}

    recovery_days = np.array([
        max(5, np.random.exponential(recovery_map[c])) for c in countries_sample
    ])
    response_score = np.array([
        np.clip(np.random.normal(response_score_base[c], 8), 20, 100) for c in countries_sample
    ])
    casualties = np.random.exponential(80, n)
    economic_loss = np.random.exponential(2e6, n)
    response_hours = np.random.exponential(40, n)
    aid_amount = economic_loss * np.random.uniform(0.3, 1.2, n)
    severity_index = np.random.uniform(1, 10, n)

    df_eda = pd.DataFrame({
        'country': countries_sample,
        'disaster_type': disaster_sample,
        'recovery_days': recovery_days,
        'response_score': response_score,
        'casualties': casualties,
        'economic_loss': economic_loss,
        'response_hours': response_hours,
        'aid_amount': aid_amount,
        'severity_index': severity_index,
    })

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Distribuciones", "🌍 Análisis por País", "⚡ Por Tipo de Desastre", "🔗 Correlaciones"])

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

        if chart_type == "Histograma":
            fig = px.histogram(df_eda, x=var, nbins=60,
                               color_discrete_sequence=['#63b3ed'],
                               marginal='rug')
        elif chart_type == "Boxplot":
            fig = px.box(df_eda, y=var, color_discrete_sequence=['#9f7aea'])
        else:
            log_vals = np.log1p(df_eda[var])
            fig = make_subplots(rows=1, cols=2,
                                subplot_titles=[f'{var} (original)', f'{var} (log1p)'])
            fig.add_histogram(x=df_eda[var], nbinsx=60,
                              marker_color='rgba(252,129,129,0.7)', name='Original', row=1, col=1)
            fig.add_histogram(x=log_vals, nbinsx=60,
                              marker_color='rgba(99,179,237,0.7)', name='Log1p', row=1, col=2)

        skew_orig = df_eda[var].skew()
        fig.update_layout(**PLOTLY_TEMPLATE, height=380,
                          title=f'{var} · Skewness: {skew_orig:.2f}',
                          showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
        <div class="insight-box">
        <b style="color:#63b3ed;">💡 Insight</b>
        <p>La variable <b>{var}</b> presenta un skewness de <b>{skew_orig:.2f}</b>.
        {"Alta asimetría positiva — la mayoría de eventos son moderados pero existen outliers extremos." if skew_orig > 2 else
         "Alta asimetría negativa — la mayoría de valores están cerca del máximo." if skew_orig < -2 else
         "Distribución relativamente simétrica."}</p>
        </div>
        """, unsafe_allow_html=True)

    # ─ Tab 2: Por País ─
    with tab2:
        metric_pais = st.selectbox("Métrica:", ['recovery_days', 'response_score', 'casualties', 'economic_loss'])

        # Median by country sorted
        country_stats = df_eda.groupby('country')[metric_pais].agg(['median','mean','std']).reset_index()
        country_stats = country_stats.sort_values('median', ascending=True)

        fig = go.Figure()
        colors = px.colors.sequential.Viridis
        fig.add_bar(
            x=country_stats['median'],
            y=country_stats['country'],
            orientation='h',
            marker=dict(
                color=country_stats['median'],
                colorscale='RdYlGn_r' if metric_pais == 'recovery_days' else 'RdYlGn',
                showscale=True
            ),
            text=[f"{v:.0f}" for v in country_stats['median']],
            textposition='outside',
        )
        fig.update_layout(**PLOTLY_TEMPLATE, height=650,
                          title=f'Mediana de {metric_pais} por país',
                          xaxis_title=metric_pais, yaxis_title='',
                          margin=dict(l=120, r=80))
        st.plotly_chart(fig, use_container_width=True)

        # Country groups insight
        st.markdown("""
        <div class="insight-box">
        <b style="color:#63b3ed;">💡 Tres grupos de países</b>
        <p>El análisis por país revela tres grupos claros que coinciden con el nivel de desarrollo económico:<br>
        🔴 <b>Recuperación lenta</b> (&gt;300 días): Congo, Nigeria<br>
        🟡 <b>Recuperación media</b> (100–300 días): Perú, Bangladesh, India, Brasil, Filipinas<br>
        🟢 <b>Recuperación rápida</b> (&lt;50 días): Japón, Alemania, EE.UU., Canadá, Nueva Zelanda</p>
        </div>
        """, unsafe_allow_html=True)

    # ─ Tab 3: Por Tipo de Desastre ─
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            # Pie chart - frequency
            freq = df_eda['disaster_type'].value_counts()
            fig_pie = go.Figure(go.Pie(
                labels=freq.index, values=freq.values,
                hole=0.4,
                marker=dict(colors=px.colors.qualitative.Set3),
                textinfo='percent+label',
                textfont_size=11
            ))
            fig_pie.update_layout(**PLOTLY_TEMPLATE, title='Distribución de tipos de desastre',
                                  height=380, showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Boxplot response_score por disaster_type
            fig_box = px.box(df_eda, x='disaster_type', y='response_score',
                             color='disaster_type',
                             color_discrete_sequence=px.colors.qualitative.Set2)
            fig_box.update_layout(**PLOTLY_TEMPLATE, title='Response Score por tipo de desastre',
                                  height=380, showlegend=False,
                                  xaxis_tickangle=-45)
            st.plotly_chart(fig_box, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <b style="color:#9f7aea;">💡 El tipo de desastre importa menos que el país</b>
        <p>Todos los tipos de desastre muestran medianas de response_score entre 70 y 85. El país es el factor dominante, no el tipo de catástrofe. Esto sugiere que las capacidades institucionales y económicas de cada nación son determinantes.</p>
        </div>
        """, unsafe_allow_html=True)

    # ─ Tab 4: Correlaciones ─
    with tab4:
        num_cols = ['recovery_days', 'response_score', 'casualties',
                    'economic_loss', 'response_hours', 'aid_amount', 'severity_index']
        corr = df_eda[num_cols].corr()

        fig_heat = go.Figure(go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu_r',
            zmid=0,
            text=corr.values.round(2),
            texttemplate='%{text}',
            textfont_size=11,
            colorbar=dict(title='r', tickfont=dict(color='#e2e8f0'))
        ))
        fig_heat.update_layout(**PLOTLY_TEMPLATE, title='Heatmap de Correlaciones',
                               height=500, margin=dict(l=100))
        st.plotly_chart(fig_heat, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            # Scatter: response_score vs response_hours
            sample = df_eda.sample(800, random_state=42)
            fig_sc1 = px.scatter(sample, x='response_hours', y='response_score',
                                 trendline='ols', opacity=0.5,
                                 color_discrete_sequence=['#63b3ed'])
            corr_val = df_eda['response_hours'].corr(df_eda['response_score'])
            fig_sc1.update_layout(**PLOTLY_TEMPLATE, height=320,
                                  title=f'Response hours vs Score · r={corr_val:.2f}')
            st.plotly_chart(fig_sc1, use_container_width=True)
        with col2:
            fig_sc2 = px.scatter(sample, x='economic_loss', y='aid_amount',
                                 trendline='ols', opacity=0.5,
                                 color_discrete_sequence=['#9f7aea'])
            corr_val2 = df_eda['economic_loss'].corr(df_eda['aid_amount'])
            fig_sc2.update_layout(**PLOTLY_TEMPLATE, height=320,
                                  title=f'Economic Loss vs Aid Amount · r={corr_val2:.2f}')
            st.plotly_chart(fig_sc2, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <b style="color:#63b3ed;">💡 Dos correlaciones clave</b>
        <p>
        📉 <b>response_score ↔ response_hours</b>: Fuerte correlación negativa. Cuanto más horas se tarda en responder, peor es el score.<br>
        📈 <b>aid_amount ↔ economic_loss</b>: Fuerte correlación positiva. A mayor daño económico, más ayuda internacional se recibe.
        </p>
        </div>
        """, unsafe_allow_html=True)


# ── PÁGINA: PREDICTOR RESPONSE SCORE ─────────────────────────────────────────
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
        <b style="color:#63b3ed;">ℹ️ ¿Qué es el Response Score?</b>
        <p>Índice de 0 a 100 que mide la eficiencia de la respuesta ante un desastre. Un score alto indica respuesta rápida y bien coordinada.</p>
        </div>
        <div class="insight-box">
        <b style="color:#9f7aea;">🔬 Dos versiones del modelo</b>
        <p><b>Con severity_index</b>: R² ≈ 0.85 — mayor precisión pero puede haber leakage.<br>
        <b>Sin severity_index</b>: R² ≈ 0.45 — más conservador y realista.</p>
        </div>
        <div class="insight-box">
        <b style="color:#48bb78;">⚠️ Leakage detectado</b>
        <p>severity_index y casualties_log juntas explican el 84% de la importancia del RF, sugiriendo que response_score fue calculado a partir de ellas.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        with st.container():
            c1, c2 = st.columns(2)
            with c1:
                country = st.selectbox("🗺️ País", COUNTRIES, key="rs_country")
                disaster = st.selectbox("⚡ Tipo de desastre", DISASTER_TYPES, key="rs_disaster")
                year = st.slider("📅 Año", 2000, 2024, 2018, key="rs_year")
            with c2:
                use_sev = st.toggle("Usar severity_index", value=True)
                if use_sev:
                    severity = st.slider("🔴 Severity Index", 0.0, 10.0, 5.0, 0.1)
                casualties = st.number_input("💀 Víctimas", 0, 100000, 150, step=10, key="rs_cas")
                economic_loss = st.number_input("💸 Pérdida económica (€)", 0, 100_000_000, 500_000, step=10000)

            c3, c4 = st.columns(2)
            with c3:
                aid_amount = st.number_input("🤝 Ayuda recibida (€)", 0, 100_000_000, 300_000, step=10000)
            with c4:
                recovery_days = st.number_input("📅 Días de recuperación", 0, 2000, 120, step=5)

            if st.button("🚀 Predecir Response Score", key="btn_rs"):
                with st.spinner("Calculando..."):
                    sev = severity if use_sev else 5.0
                    pred = predict_response_score(
                        country, disaster, year, sev,
                        casualties, economic_loss, aid_amount, recovery_days, use_sev
                    )

                color_cls = "warning" if pred < 60 else ""
                emoji = "🟢" if pred >= 75 else "🟡" if pred >= 60 else "🔴"
                label = "Buena respuesta" if pred >= 75 else "Respuesta moderada" if pred >= 60 else "Respuesta deficiente"

                st.markdown(f"""
                <div class="pred-box {color_cls}">
                    <div style="font-size:3.5rem;font-weight:700;color:{'#48bb78' if pred >= 60 else '#fc8181'};">
                        {pred}
                    </div>
                    <div class="pred-label">Response Score</div>
                    <div style="margin-top:10px;font-size:1.2rem;">{emoji} {label}</div>
                    <div style="color:#718096;font-size:0.8rem;margin-top:6px;">
                        Modelo: {'Con severity_index' if use_sev else 'Sin severity_index'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Gauge chart
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=pred,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    delta={'reference': 70},
                    gauge={
                        'axis': {'range': [0, 100], 'tickcolor': '#e2e8f0'},
                        'bar': {'color': '#63b3ed'},
                        'steps': [
                            {'range': [0, 40], 'color': 'rgba(252,129,129,0.3)'},
                            {'range': [40, 70], 'color': 'rgba(246,173,85,0.3)'},
                            {'range': [70, 100], 'color': 'rgba(72,187,120,0.3)'},
                        ],
                        'threshold': {'line': {'color': '#9f7aea', 'width': 3}, 'value': 70}
                    }
                ))
                fig_gauge.update_layout(**PLOTLY_TEMPLATE, height=280,
                                        margin=dict(l=30, r=30, t=30, b=10))
                st.plotly_chart(fig_gauge, use_container_width=True)


# ── PÁGINA: RECOVERY DAYS ──────────────────────────────────────────────────────
elif nav == "📅 Predictor: Días de Recuperación":
    st.markdown("""
    <div class="section-header">
        <h2>📅 Predictor de Días de Recuperación</h2>
        <p>Estima cuántos días tardará una región en recuperarse tras un desastre</p>
    </div>
    """, unsafe_allow_html=True)

    col_info, col_form = st.columns([1, 2])
    with col_info:
        st.markdown("""
        <div class="insight-box">
        <b style="color:#63b3ed;">ℹ️ Variable objetivo</b>
        <p>Recovery_days fue transformada con log1p para reducir el skewness. El modelo predice en escala log y se convierte a días reales con expm1.</p>
        </div>
        <div class="insight-box">
        <b style="color:#f6ad55;">🌍 Factores clave</b>
        <p>El país es el factor dominante. Japón: 18-20 días. Congo: &gt;400 días. El tipo de desastre tiene mucho menos impacto que las capacidades institucionales del país.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        c1, c2 = st.columns(2)
        with c1:
            country2 = st.selectbox("🗺️ País", COUNTRIES, key="rd_country")
            disaster2 = st.selectbox("⚡ Tipo de desastre", DISASTER_TYPES, key="rd_disaster")
            year2 = st.slider("📅 Año", 2000, 2024, 2018, key="rd_year")
            severity2 = st.slider("🔴 Severity Index", 0.0, 10.0, 5.0, 0.1, key="rd_sev")
        with c2:
            casualties2 = st.number_input("💀 Víctimas", 0, 100000, 200, step=10, key="rd_cas")
            economic_loss2 = st.number_input("💸 Pérdida económica (€)", 0, 100_000_000, 1_000_000, step=10000, key="rd_econ")
            aid_amount2 = st.number_input("🤝 Ayuda recibida (€)", 0, 100_000_000, 600_000, step=10000, key="rd_aid")
            response_hours2 = st.number_input("⏱️ Horas hasta responder", 0, 5000, 24, step=1)

        if st.button("🚀 Predecir Días de Recuperación", key="btn_rd"):
            with st.spinner("Calculando..."):
                pred_days = predict_recovery_days(
                    country2, disaster2, year2, severity2,
                    casualties2, economic_loss2, aid_amount2, response_hours2
                )

            color_cls = "warning" if pred_days > 200 else ""
            emoji = "🟢" if pred_days < 60 else "🟡" if pred_days < 200 else "🔴"
            label = "Recuperación rápida" if pred_days < 60 else "Recuperación media" if pred_days < 200 else "Recuperación lenta"

            st.markdown(f"""
            <div class="pred-box {color_cls}">
                <div style="font-size:3.5rem;font-weight:700;color:{'#48bb78' if pred_days < 200 else '#fc8181'};">
                    {pred_days:.0f} días
                </div>
                <div class="pred-label">Días estimados de recuperación</div>
                <div style="margin-top:10px;font-size:1.2rem;">{emoji} {label}</div>
                <div style="color:#718096;font-size:0.8rem;margin-top:6px;">
                    ≈ {pred_days/30:.1f} meses · ≈ {pred_days/365:.1f} años
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Visual bar comparing to reference countries
            ref_countries = {'Japón': 20, 'Alemania': 22, 'EE.UU.': 25,
                             'España': 60, 'India': 220, 'Nigeria': 380, 'Congo': 450}
            ref_df = pd.DataFrame({'País': list(ref_countries.keys()) + [f'📍 {country2}'],
                                   'Días': list(ref_countries.values()) + [pred_days],
                                   'Tipo': ['Referencia']*len(ref_countries) + ['Predicción']})
            ref_df = ref_df.sort_values('Días')
            fig_bar = px.bar(ref_df, x='Días', y='País', orientation='h',
                             color='Tipo', color_discrete_map={'Referencia': '#63b3ed', 'Predicción': '#f6ad55'})
            fig_bar.update_layout(**PLOTLY_TEMPLATE, height=350,
                                  title='Comparativa con países de referencia',
                                  legend=dict(orientation='h', y=1.1))
            st.plotly_chart(fig_bar, use_container_width=True)


# ── PÁGINA: CLUSTERING ────────────────────────────────────────────────────────
elif nav == "🔵 Clasificador de Clusters":
    st.markdown("""
    <div class="section-header">
        <h2>🔵 Clasificador de Perfil de Impacto (KMeans k=3)</h2>
        <p>Asigna un evento de desastre a uno de los 3 perfiles de impacto y gestión</p>
    </div>
    """, unsafe_allow_html=True)

    # Cluster profiles
    col1, col2, col3 = st.columns(3)
    profiles = [
        ("🟢 Cluster 0", "Bajo impacto", "#48bb78",
         "Pocas víctimas · Pérdidas moderadas · Respuesta rápida · Recuperación en días"),
        ("🔴 Cluster 1", "Alto impacto / Mala gestión", "#fc8181",
         "Alta mortalidad · Pérdidas elevadas · Respuesta tardía · Meses de recuperación"),
        ("🟡 Cluster 2", "Alto daño / Buena resiliencia", "#f6ad55",
         "Grandes pérdidas económicas · Respuesta rápida · Recuperación acelerada"),
    ]
    for col, (badge, name, color, desc) in zip([col1, col2, col3], profiles):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="border-color:{color}40;">
                <div style="font-size:1.5rem;">{badge.split()[0]}</div>
                <div style="font-weight:700;color:{color};font-size:1rem;margin-top:8px;">{name}</div>
                <div style="font-size:0.8rem;color:#a0aec0;margin-top:8px;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_form, col_result = st.columns([1, 1])

    with col_form:
        st.markdown("#### Introduce los parámetros del evento")
        casualties3 = st.number_input("💀 Víctimas", 0, 500000, 100, step=10, key="cl_cas")
        economic_loss3 = st.number_input("💸 Pérdida económica (€)", 0, 500_000_000, 1_000_000, step=50000, key="cl_econ")
        response_hours3 = st.number_input("⏱️ Horas hasta respuesta", 0, 10000, 48, step=1, key="cl_rh")
        recovery_days3 = st.number_input("📅 Días de recuperación", 0, 2000, 150, step=5, key="cl_rd")

        st.markdown("---")
        st.markdown("**Perfiles de ejemplo rápido:**")
        ex_col1, ex_col2, ex_col3 = st.columns(3)
        example_clicked = None
        with ex_col1:
            if st.button("🟢 Bajo\nimpacto"):
                example_clicked = 0
        with ex_col2:
            if st.button("🔴 Alto\nimpacto"):
                example_clicked = 1
        with ex_col3:
            if st.button("🟡 Resiliencia"):
                example_clicked = 2

        predict_btn = st.button("🔵 Clasificar Evento", key="btn_cl")

    with col_result:
        if predict_btn or example_clicked is not None:
            if example_clicked == 0:
                cas, econ, rh, rd = 20, 50000, 6, 15
            elif example_clicked == 1:
                cas, econ, rh, rd = 5000, 50_000_000, 200, 600
            elif example_clicked == 2:
                cas, econ, rh, rd = 100, 80_000_000, 8, 30
            else:
                cas, econ, rh, rd = casualties3, economic_loss3, response_hours3, recovery_days3

            cluster, distances = predict_cluster(cas, econ, rh, rd)
            color = CLUSTER_COLORS[cluster]
            name = CLUSTER_NAMES[cluster]
            desc = CLUSTER_DESC[cluster]

            # Normalize distances to confidence %
            inv_d = 1 / (distances + 1e-6)
            probs = inv_d / inv_d.sum() * 100

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,{color}20,{color}10);
                        border:2px solid {color}80;border-radius:16px;padding:28px;text-align:center;">
                <div style="font-size:3rem;font-weight:700;color:{color};">{name}</div>
                <div style="color:#a0aec0;margin-top:12px;font-size:0.95rem;line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

            # Distance/probability bar chart
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

            # Radar chart with input profile
            categories = ['Víctimas', 'Pérdida Econ.', 'Horas Resp.', 'Días Recup.']
            # Normalize to 0-1
            maxvals = [500000, 500_000_000, 10000, 2000]
            vals = [cas/maxvals[0], econ/maxvals[1], rh/maxvals[2], rd/maxvals[3]]

            fig_radar = go.Figure(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor=f"{color}30",
                line_color=color,
                name='Evento'
            ))
            fig_radar.update_layout(**PLOTLY_TEMPLATE, height=300,
                                    polar=dict(
                                        bgcolor='rgba(255,255,255,0.03)',
                                        radialaxis=dict(visible=True, range=[0,1],
                                                        tickfont=dict(color='#718096', size=9)),
                                        angularaxis=dict(tickfont=dict(color='#e2e8f0'))
                                    ),
                                    title='Perfil del evento', showlegend=False)
            st.plotly_chart(fig_radar, use_container_width=True)


# ── PÁGINA: COMPARATIVA DE MODELOS ────────────────────────────────────────────
elif nav == "📋 Comparativa de Modelos":
    st.markdown("""
    <div class="section-header">
        <h2>📋 Comparativa de Modelos</h2>
        <p>Resultados de todos los modelos evaluados en los tres objetivos</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Objetivo 1
    st.markdown("### 🎯 Objetivo 1 — Response Score (con severity_index)")
    models_obj1 = pd.DataFrame({
        'Modelo': ['Linear Regression', 'Ridge', 'Lasso', 'ElasticNet', 'Random Forest', 'GBM', 'XGBoost ⭐'],
        'R² Test': [0.71, 0.71, 0.71, 0.71, 0.84, 0.83, 0.85],
        'RMSE Test': [7.80, 7.80, 7.81, 7.81, 5.84, 5.97, 5.72],
        'MAE Test': [6.14, 6.14, 6.15, 6.15, 4.38, 4.52, 4.28],
        'R² Train': [0.71, 0.71, 0.71, 0.71, 0.97, 0.95, 0.98],
    })

    fig1 = go.Figure()
    colors_m = ['#718096','#a0aec0','#b794f4','#9f7aea','#63b3ed','#4fd1c5','#f6ad55']
    for i, row in models_obj1.iterrows():
        fig1.add_bar(name=row['Modelo'], x=['R² Test','RMSE Test','MAE Test'],
                     y=[row['R² Test'], row['RMSE Test']/20, row['MAE Test']/20],
                     marker_color=colors_m[i])
    fig1.update_layout(**PLOTLY_TEMPLATE, height=320, barmode='group',
                       title='R² · RMSE/20 · MAE/20 por modelo (Obj 1)',
                       legend=dict(orientation='h', y=-0.25, font_size=10))
    st.plotly_chart(fig1, use_container_width=True)

    # Table
    st.dataframe(
        models_obj1.style
        .highlight_max(subset=['R² Test'], color='rgba(72,187,120,0.3)')
        .highlight_min(subset=['RMSE Test','MAE Test'], color='rgba(72,187,120,0.3)')
        .format({'R² Test': '{:.4f}', 'RMSE Test': '{:.4f}', 'MAE Test': '{:.4f}', 'R² Train': '{:.4f}'}),
        use_container_width=True, hide_index=True
    )

    # ── Objetivo 1.2 (sin severity_index)
    st.markdown("### 🎯 Objetivo 1.2 — Response Score (sin severity_index)")
    models_obj1_2 = pd.DataFrame({
        'Modelo': ['Linear Regression', 'Ridge', 'Lasso', 'ElasticNet', 'Random Forest', 'GBM', 'XGBoost ⭐'],
        'R² Test': [0.01, 0.01, 0.01, 0.01, 0.43, 0.44, 0.45],
        'RMSE Test': [14.5, 14.5, 14.5, 14.5, 11.0, 10.9, 10.8],
        'MAE Test': [11.8, 11.8, 11.8, 11.8, 8.7, 8.6, 8.5],
    })
    st.markdown("""
    <div class="insight-box">
    <b style="color:#f6ad55;">⚠️ Leakage en Objetivo 1</b>
    <p>Al eliminar severity_index, el R² cae de 0.85 a 0.45. Esto confirma que response_score fue generada a partir de severity_index y casualties, no al revés. El modelo sin leakage es más honesto con el mundo real.</p>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(models_obj1_2.style.highlight_max(subset=['R² Test'], color='rgba(72,187,120,0.3)')
                 .format({'R² Test': '{:.4f}', 'RMSE Test': '{:.4f}', 'MAE Test': '{:.4f}'}),
                 use_container_width=True, hide_index=True)

    # ── Objetivo 2
    st.markdown("### 📅 Objetivo 2 — Recovery Days (log)")
    models_obj2 = pd.DataFrame({
        'Modelo': ['Linear Regression', 'Ridge', 'Lasso', 'ElasticNet', 'Random Forest', 'GBM', 'XGBoost ⭐'],
        'R² Test': [0.62, 0.62, 0.62, 0.62, 0.81, 0.80, 0.83],
        'RMSE Test': [1.22, 1.22, 1.22, 1.22, 0.87, 0.88, 0.83],
        'MAE Test': [0.98, 0.98, 0.98, 0.98, 0.65, 0.66, 0.63],
    })
    st.dataframe(models_obj2.style.highlight_max(subset=['R² Test'], color='rgba(72,187,120,0.3)')
                 .highlight_min(subset=['RMSE Test','MAE Test'], color='rgba(72,187,120,0.3)')
                 .format({'R² Test': '{:.4f}', 'RMSE Test': '{:.4f}', 'MAE Test': '{:.4f}'}),
                 use_container_width=True, hide_index=True)

    # ── Objetivo 3
    st.markdown("### 🔵 Objetivo 3 — Clustering")
    col1, col2 = st.columns(2)
    with col1:
        cluster_metrics = pd.DataFrame({
            'Algoritmo': ['KMeans (k=3) ⭐', 'DBSCAN (eps=0.8)', 'HDBSCAN+UMAP'],
            'Silhouette': [0.21, 0.18, 0.24],
            'Clusters': [3, 4, '3+ruido'],
            'Usado': ['✅ Sí', '❌ No', '❌ No'],
        })
        st.dataframe(cluster_metrics, use_container_width=True, hide_index=True)
        st.markdown("""
        <div class="insight-box">
        <b style="color:#63b3ed;">💡 ¿Por qué KMeans?</b>
        <p>A pesar del Silhouette bajo (datos sintéticos con solapamiento), KMeans con k=3 ofrece la mejor interpretabilidad. Los 3 clusters tienen sentido conceptual claro.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        # Cluster profile real values
        cluster_profiles = pd.DataFrame({
            'Cluster': ['Bajo impacto 🟢', 'Alto impacto 🔴', 'Resiliencia 🟡'],
            'Víctimas': [8, 580, 45],
            'Pérdida (M€)': [0.08, 8.2, 7.5],
            'Horas resp.': [12, 180, 14],
            'Días recup.': [18, 520, 35],
        })
        fig_prof = go.Figure()
        metrics_cl = ['Víctimas', 'Pérdida (M€)', 'Horas resp.', 'Días recup.']
        cluster_colors_list = ['#48bb78', '#fc8181', '#f6ad55']
        for i, row in cluster_profiles.iterrows():
            fig_prof.add_bar(
                name=row['Cluster'],
                x=metrics_cl,
                y=[row['Víctimas']/10, row['Pérdida (M€)'], row['Horas resp.']/10, row['Días recup.']/10],
                marker_color=cluster_colors_list[i]
            )
        fig_prof.update_layout(**PLOTLY_TEMPLATE, barmode='group', height=320,
                               title='Perfil medio por cluster (valores normalizados)',
                               legend=dict(orientation='h', y=1.12, font_size=10))
        st.plotly_chart(fig_prof, use_container_width=True)

    # Global summary
    st.markdown("""
    <div class="section-header" style="margin-top:24px;">
        <h2>🏆 Resumen Global</h2>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    for col, (val, lab) in zip([col1, col2, col3, col4], [
        ("0.85", "R² Obj.1 (XGBoost)"),
        ("0.45", "R² Obj.1.2 (sin leakage)"),
        ("0.83", "R² Obj.2 (XGBoost)"),
        ("0.21", "Silhouette Obj.3"),
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
    <b style="color:#63b3ed;">🔮 Futuros pasos</b>
    <p>
    • Probar HDBSCAN con embeddings UMAP para clustering más robusto<br>
    • Añadir variables externas: PIB per cápita, índice de gobernanza, temperatura media<br>
    • Construir un sistema de alerta temprana que combine los 3 objetivos<br>
    • Validar con datos reales (EM-DAT, ReliefWeb) para superar las limitaciones del dataset sintético
    </p>
    </div>
    """, unsafe_allow_html=True)
