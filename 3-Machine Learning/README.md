# Proyecto 3: Machine Learning
## 🌍 Análisis Predictivo de la Gestión de la Ayuda Humanitaria y el Impacto de Desastres a Nivel Global

> Bootcamp Data Science – The Bridge | Bilbao, Febrero-Junio 2026**
> Chiara López Palomino

---

## 📋 Descripción

Este proyecto aplica técnicas de Machine Learning para analizar y predecir patrones en la gestión de desastres naturales y emergencias humanitarias a nivel global. A través de modelos supervisados y no supervisados, se exploran tres objetivos complementarios:

1. **Predicción de la eficiencia de respuesta** — ¿Qué factores determinan una respuesta más eficaz ante una emergencia?
2. **Predicción del tiempo de recuperación** — ¿Cuántos días tardará un país en recuperarse de un desastre?
3. **Segmentación de eventos por perfil de riesgo** — Identificación de grupos naturales de eventos para detectar perfiles diferenciados (alto riesgo / buena gestión / impacto económico severo).

---

## 📦 Dataset

**Enhanced Disaster & Emergency Response Dataset** — versión mejorada del [Global Disaster & Emergency Response Dataset (2018–2024)](https://www.kaggle.com/), obtenido de Kaggle.

| Característica | Detalle |
|---|---|
| Registros | 49.972 eventos únicos |
| Período | 1990–2024 (35 años) |
| Países | 24 |
| Tipos de desastre | 12 (inundaciones, terremotos, tsunamis, ciclones, etc.) |
| Generación | Modelos probabilísticos y distribuciones aleatorias |

> ⚠️ **Nota importante:** Los datos son sintéticos, no recogidos de eventos reales. Las métricas de evaluación son muy elevadas en parte por esta razón. Los patrones aprendidos no reflejan necesariamente la realidad de la gestión de desastres.

---

## 🗂️ Estructura del repositorio

```
📁 3-Machine Learning/
├── 📁 src/
│   ├── 📁 data/
│   ├── 📁 models/
│   │   └── 📁 production/
│   ├── 📁 notebooks/
│   ├── 📁 resources/
│   │   └── 📁 img/
│   ├── 📁 utils/
│   ├── 🐍 app.py
│   └── 📓 main.ipynb
├── 📄 Memoria ML.pdf
├── 📄 Presentación ML.pdf
└── 📄 README.md
```

---

## ⚙️ Pipeline

### 1. Preprocesamiento
- Eliminación del único valor nulo (`economic_loss`)
- Limpieza de columnas monetarias (`economic_loss`, `aid_amount`): eliminación de símbolo `€` y separadores de miles → conversión a `float`
- Corrección de `recovery_days` (eliminación de fila vacía, conversión a `float`)

### 2. EDA
- Análisis de distribuciones: ninguna variable sigue distribución normal; la mayoría presenta asimetría positiva y numerosos outliers
- Mapa de calor de correlaciones: correlación muy alta entre `response_score` y `response_hours` (−0.91), y entre `economic_loss` y `aid_amount` (0.87)
- Análisis por país y tipo de desastre mediante boxplots para ambos targets
- PCA exploratorio (71% varianza explicada) para evaluar la viabilidad del clustering

### 3. Feature Engineering
- **Transformación logarítmica** de las 5 variables con mayor asimetría: `casualties`, `economic_loss`, `aid_amount`, `recovery_days`, `response_hours`
- **One-Hot Encoding** de variables categóricas: `country` (24 categorías) y `disaster_type` (12 categorías) → 36 columnas binarias adicionales
- DataFrame final: **49 columnas**

### 4. Modelado

#### Objetivo 1 — Predicción de `response_score`
- Features excluidas: `response_hours`, `response_hours_log` (data leakage directo)
- Modelos: Regresión Lineal, Lasso, Ridge, ElasticNet, Random Forest, Gradient Boosting, XGBoost (con RandomizedSearchCV)
- División train/test: 80/20 · Estandarización: StandardScaler

| Modelo | R² | RMSE | MAE |
|---|---|---|---|
| **XGBoost** | **0.9923** | **2.4454** | **0.9766** |
| GBM | 0.9920 | 2.4957 | 1.1359 |
| Random Forest | 0.9903 | 2.7486 | 1.0850 |

#### Objetivo 1.2 — Sin `severity_index`
> Al detectar que `casualties_log` y `severity_index` explicaban el 84% de la varianza, se entrenó una versión adicional excluyendo `severity_index`.

| Modelo | R² | RMSE | MAE |
|---|---|---|---|
| **XGBoost** | **0.8515** | **10.7964** | **6.9606** |
| Random Forest | 0.8467 | 10.9691 | 6.8103 |
| GBM | 0.8411 | 11.1659 | 7.3213 |

#### Objetivo 2 — Predicción de `recovery_days_log`
- Features excluidas: `response_score` (leakage temporal)
- Mismos modelos y métricas que Objetivo 1

| Modelo | R² | RMSE | MAE |
|---|---|---|---|
| **XGBoost** | **0.7870** | **84.26** | **42.38** |
| GBM | 0.7857 | 84.18 | 42.53 |
| Random Forest | 0.7808 | 89.02 | 43.51 |

#### Objetivo 3 — Clustering (KMeans, k=3)
- Variables: `casualties_log`, `economic_loss_log`, `response_hours_log`, `recovery_days_log`
- Excluida: `aid_amount_log` (correlación 0.87 con `economic_loss_log`)
- Algoritmos evaluados: KMeans, DBSCAN, HDBSCAN, UMAP
- Métrica: Silhouette Score (k=2: 0.2770 · k=3: 0.2155)
- Selección final: **k=3** por mayor riqueza interpretativa

| Cluster | Perfil |
|---|---|
| 0 | Impacto moderado |
| 1 | Alto impacto humano / mala gestión |
| 2 | Alto daño económico / buena gestión |

---

## 📊 Principales hallazgos del EDA

- **Por país:** el país domina la señal de `recovery_days` más que el tipo de desastre. Se identifican tres grupos claros que se correlacionan con el nivel de desarrollo económico:
  - 🟢 Recuperación rápida (<100 días): Japón, Alemania, EE.UU., España, Francia...
  - 🟡 Recuperación media (100–300 días): India, Brasil, Turquía, Filipinas...
  - 🔴 Recuperación lenta (>300 días): Congo, Nigeria

- **Por tipo de desastre:** los tsunamis presentan la mediana más alta de días de recuperación (~250 días); las erupciones volcánicas, los outliers más extremos (hasta 1.750 días).

- **Respuesta:** el tipo de desastre apenas afecta al `response_score`; todos los tipos tienen medianas entre 70 y 85.

---

## 🔮 Futuros pasos

- Aplicar el mismo enfoque con datasets reales: **EM-DAT**, **OCHA**, **Banco Mundial**
- Incorporar variables contextuales externas: IDH, PIB per cápita, gobernanza e infraestructura
- Explorar en profundidad **HDBSCAN** y **UMAP** para clustering
- Análisis temporal de frecuencia e intensidad de desastres mediante **ARIMA** (especialmente relevante en el contexto del cambio climático)

---

## 🛠️ Tecnologías utilizadas

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-f7931e?logo=scikit-learn)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0-blue)
![pandas](https://img.shields.io/badge/pandas-2.2-150458?logo=pandas)
![matplotlib](https://img.shields.io/badge/matplotlib-3.8-blue)
![seaborn](https://img.shields.io/badge/seaborn-0.13-blue)

---

## 📄 Licencia

Proyecto académico desarrollado en el marco del Bootcamp de Data Science de [The Bridge](https://www.thebridge.tech/) · Bilbao 2026.
