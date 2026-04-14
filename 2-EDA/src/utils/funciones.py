import pandas as pd

#DATASETS
 #ACNUR en crudo:
df_1_desplazamiento2023 = pd.read_excel(r"..\data\Annexes_GT_2023.xlsx", sheet_name=None)
#ACNUR por hoja:
df_ACNUR_pais_acogida = pd.read_excel(
    r"..\data\Annexes_GT_2023.xlsx",
    sheet_name='pais_acogida',
    skiprows=7,
    usecols=range(13)
).dropna(how='all').reset_index(drop=True)
df_ACNUR_pais_acogida_UNHCR_bureaus = df_1_desplazamiento2023['pais_acogida_UNHCR_bureaus']
df_ACNUR_pais_acogida_UN_regions = df_1_desplazamiento2023['pais_acogida_UN_regions']

df_ACNUR_pais_origen = pd.read_excel(
    r"..\data\Annexes_GT_2023.xlsx",
    sheet_name='pais_origen',
    skiprows=6, 
    usecols=range(13)
).dropna(how='all').reset_index(drop=True)
df_ACNUR_pais_origen_UNHCR_bureaus = df_1_desplazamiento2023['pais_origen_UNHCR_bureaus']
df_ACNUR_pais_origen_UN_regions = df_1_desplazamiento2023['pais_origen_UN_regions']

df_ACNUR_demografia = pd.read_excel(
    r"..\data\Annexes_GT_2023.xlsx",
    sheet_name='demografia',
    skiprows=7,  
    usecols=range(23)
).dropna(how='all').reset_index(drop=True)

df_2_conflictos = pd.read_excel(r"..\data\UcdpPrioConflict_v25_1.xlsx")
df_3_violencia_sexual = pd.read_excel(r"..\data\SVAC_3.3_complete.xlsx")
df_4_ataques_civiles = pd.read_excel(r"..\data\number_of_events_targeting_civilians_by_country-year_as-of-13Mar2026.xlsx")
df_5_muertes_civiles = pd.read_excel(r"..\data\number_of_reported_civilian_fatalities_by_country-year_as-of-13Mar2026.xlsx")
df_6_muertes_totales = pd.read_excel(r"..\data\number_of_reported_fatalities_by_country-year_as-of-13Mar2026.xlsx")


# DICCIONARIOS
# diccionarios UCDP
incompatibilidad = {1: "Territorio", 2: "Gobierno", 3: "Territorio y gobierno"}
nivel_intensidad = {1: "Menor (25-99 muertes)", 2: "Guerra (>1000 muertes)"}
region = {1: "Europa", 2: "Oriente Próximo", 3: "Asia", 4: "África", 5: "América"}
# diccionarios SVAC
tipo_actor = {1: "Estado/Gobierno", 2: "Estado apoyo Estado", 3: "Rebeldes", 4: "Estado apoyo Rebeldes", 5: "Segundo Estado (interstate)", 6: "Milicias pro-gobierno"}
incompatibilidad2 = {0: "Otro", 1: "Territorio", 2: "Gobierno", 3: "Territorio y gobierno"}
region2 = {1: "Europa", 2: "Oriente Próximo", 3: "Asia", 4: "África", 5: "América"}
anio_conflicto = {1: "Conflicto", 0: "Otro"}
prevalencia = {3: "Masiva", 2: "Numerosa", 1: "Aislada", 0: "Ninguna", -99: "No reporte y No datos"}
forma_violencia = {1: "Violación", 2: "Esclavitud sexual", 3: "Prostitución forzada", 4: "Embarazo forzado", 5: "Esterilización forzada/Aborto", 6: "Mutilación sexual", 7: "Tortura sexual", -99: "No reporte y No datos"}
# nombres países ACNUR y ACLED
nombres_países = {
    "Bolivia (Plurinational State of)" : "Bolivia",
    "Cabo Verde" : "Cape Verde",
    "Central African Rep." : "Central African Republic",
    "Colombia¹¹" : "Colombia",
    "Congo, Republic of" : "Republic of Congo",
    "Czechia" : "Czech Republic",
    "Dem. People's Rep. of Korea" : "North Korea",
    "Dem. Rep. of the Congo" : "Democratic Republic of Congo",
    "DR Congo (Zaire)" : "Democratic Republic of Congo",
    "Dominican Rep." : "Dominican Republic",
    "Iran (Islamic Rep. of)" : "Iran",
    "Iraq¹²" : "Iraq",
    "Serbia and Kosovo: S/RES/1244 (1999)" : "Serbia",
    "Lao People's Dem. Rep." : "Laos",
    "Myanmar (Burma)" : "Myanmar",
    "Netherlands (Kingdom of the)" : "Netherlands",
    "Palestinian¹³" : "Palestine",
    "Rep. of Moldova" : "Moldova",
    "Russian Federation" : "Russia",
    "Russia (Soviet Union), Ukraine" : "Ukraine",
    "Syrian Arab Rep." : "Syria",
    "Türkiye" : "Turkey",
    "Ukraine¹⁴" : "Ukraine",
    "United Rep. of Tanzania" : "Tanzania",
    "United States of America¹⁵" : "United States",
    "Timor-Leste" : "East Timor",
    "Venezuela (Bolivarian Republic of)" : "Venezuela",
    "Viet Nam" : "Vietnam",
    "Yemen (North Yemen)" : "Yemen"}
# países en conflicto para 2023 UCDP
# ', '.join(dt.df_UCDP_conflictos[dt.df_UCDP_conflictos["Año"] == 2023]["Ubicación"].sort_values())
paises_conflicto = [
    "Afghanistan", "Azerbaijan", "Benin", "Burkina Faso", "Burundi", "Cameroon",
    "Central African Republic", "Chad", "Colombia", "Democratic Republic of Congo",
    "Ethiopia", "India", "Indonesia", "Iran", "Israel", "Iraq", "Kenya", "Mali",
    "Mozambique", "Myanmar", "Niger", "Nigeria", "Pakistan", "Philippines", "Russia",
    "Ukraine", "Rwanda", "Somalia", "Sudan", "Syria", "Thailand", "Togo", "Turkey", "Yemen"]
# El de ACNUR acogida tiene los nombres distintos, así que edito los diferentes aquí en lugar de cambiar el dataset de nuevo
paises_conflicto2 = [
    "Afghanistan", "Azerbaijan", "Benin", "Burkina Faso", "Burundi", "Cameroon",
    "Central African Republic", "Chad", "Colombia", "Dem. Rep. of the Congo",
    "Ethiopia", "India", "Indonesia", "Iran", "Israel", "Iraq", "Kenya", "Mali",
    "Mozambique", "Myanmar", "Niger", "Nigeria", "Pakistan", "Philippines", "Russian Federation",
    "Ukraine", "Rwanda", "Somalia", "Sudan", "Syrian Arab Rep.", "Thailand", "Togo", "Turkey", "Yemen"]


# FUNCIONES
# Pasar valores numéricos de las columnas a su equivalente en los codebook (ayuda de la IA)
def convertir(valor, diccionario):
    try:
        if pd.isna(valor):
            return valor
        # Si el valor es NaN, lo devuelve tal cual
        numeros = [int(float(x.strip())) for x in str(valor).split(',')]
        # Quita posibles espacios, convierte el valor a string y lo divide por las comas
        return ', '.join(diccionario[n] for n in numeros)
        # Busca cada número en el diccionario y lo cambia por la palabra del diccionario
    except ValueError:
        return valor
        # Si algo falla en la conversión, devuelve el valor original sin tocar