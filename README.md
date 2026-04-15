# Proyecto 2: Exploratory Data Analysis (EDA)
## Análisis del impacto de la violencia armada en el desplazamiento forzado de población civil

**Bootcamp Data Science – The Bridge | Bilbao, Febrero-Junio 2026**
**Autora:** Chiara López Palomino

---

## 📌 Descripción

Este proyecto analiza el impacto humanitario de la violencia armada en la población civil a partir de datos internacionales correspondientes al año 2023. Partiendo de cuatro fuentes de referencia - ACNUR, UCDP, ACLED y SVAC -, se exploran patrones globales de desplazamiento forzado, intensidad del conflicto y violencia dirigida contra civiles. Asimismo, se incorpora un análisis específico sobre violencia sexual en conflictos armados para evaluar su asociación con mayores niveles de desplazamiento.

---

## ❓ Hipótesis

| # | Hipótesis | Resultado |
|---|-----------|-----------|
| H1 | En 2023, los países en conflicto armado reportaron mayores niveles de desplazamiento forzado. | ✅ Confirmada |
| H2 | En 2023, los principales países de acogida de personas desplazadas también experimentaron al menos un conflicto armado activo. | ✅ Confirmada |
| H3 | A mayores ataques dirigidos contra civiles, mayores niveles de desplazamiento forzado. | ⚠️ Confirmada parcialmente |
| H4 | A mayores muertes de civiles o muertes totales, mayores niveles de desplazamiento forzado. | ⚠️ Confirmada parcialmente |
| H5 | A mayor presencia de reportes de violencia sexual en conflictos armados, mayores niveles de desplazamiento forzado. | ❌ No confirmada de forma concluyente |

---

## 📂 Estructura del repositorio

```
2-EDA/
├── Presentación EDA             # Plantilla de Canva para presentar el análisis de datos
├── Memoria EDA                  # Memoria escrita con los pasos de limpieza y análisis de datos
├──src/
│  ├── main.ipynb                 # Notebook principal con el EDA completo
│  ├── utils/
│  │   ├── funciones.py           # Carga de datos, diccionarios, lista de países en conflicto y función convertir()
│  │   └── datasets_limpios.py    # Limpieza y transformación de todos los datasets
│  ├── notebooks/                 # Borradores para probar todo lo incluido en main.ipynb  
│  ├── graphs/                    # Gráficas incluidas en "Presentación EDA"
│  ├── data/                      # Datasets originales
│  ├── codebooks/                 # Codebooks de UCDP y SVAC
```

---

## 📊 Datasets

| Dataset | Fuente | DataFrame(s) |
|---------|--------|--------------|
| [ACNUR – Refugee Statistics 2023](https://www.unhcr.org/refugee-statistics/insights/annexes/trends-annexes.html) | Agencia de la ONU para los Refugiados | `df_ACNUR_pais_acogida`, `df_ACNUR_pais_origen` |
| [UCDP/PRIO Armed Conflict Dataset](https://ucdp.uu.se/downloads/#armedconflict) | Uppsala Conflict Data Program | `df_UCDP_conflictos` |
| [SVAC 3.3](http://www.sexualviolencedata.org/) | Sexual Violence in Armed Conflict | `df_SVAC_violencia_sexual` |
| [ACLED Aggregated Data](https://acleddata.com/conflict-data/download-data-files/aggregated-data) *(a 13 de marzo de 2026)* | Armed Conflict Location & Event Data | `df_ACLED_ataques_y_muertes` |

---

## 🔍 Resultados principales

- **H1 ✅** El 72% de los 25 países con más personas desplazadas en 2023 estaban en conflicto armado activo (18 de 25).
- **H2 ✅** El 76% de los 25 principales países de acogida también experimentaron al menos un conflicto activo (19 de 25).
- **H3 & H4 ⚠️** Existe correlación positiva entre violencia y desplazamiento, pero es moderada (máx. 0.56 en escala normal; 0.68 en escala logarítmica). Palestina, Venezuela o Colombia muestran que otros factores, como el contexto sociopolítico o los desastres naturales, también determinan el desplazamiento.
- **H5 ❌** El coeficiente Phi K es bajo (0.13). La escasez de datos SVAC para 2023 impide confirmar la hipótesis, aunque destaca que el 100% de los conflictos registrados ese año incluía algún nivel de violencia sexual reportada.

---

## ⚠️ Limitaciones

- Disponibilidad limitada de datos sobre violencia sexual (SVAC) para 2023
- Posible infrarregistro en contextos de conflicto
- Diferencias metodológicas entre fuentes (ACNUR, ACLED, UCDP)
- Correlación no implica causalidad

---

## 🛠️ Tecnologías utilizadas

- Python 3
- pandas, numpy
- matplotlib, seaborn, plotly
- phik
- Datawrapper (visualizaciones cartográficas)

---

## ▶️ Cómo ejecutar

1. Clona el repositorio y navega a la carpeta del proyecto:
   ```bash
   git clone https://github.com/chiaralopez/Proyectos-Bootcamp-Data-Science.git
   cd Proyectos-Bootcamp-Data-Science/2-EDA
   ```

2. Instala las dependencias:
   ```bash
   pip install pandas numpy matplotlib seaborn plotly phik openpyxl
   ```

3. Descarga los datasets originales (ver enlaces en la sección **Datasets**) y colócalos en `data/`.

4. Abre y ejecuta el notebook:
   ```bash
   jupyter notebook main.ipynb
   ```
