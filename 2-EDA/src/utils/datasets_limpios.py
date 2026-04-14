import pandas as pd

import sys
import os
sys.path.append(os.path.abspath("..")) # porque no tengo los archivos en la misma carpeta, así busca en todo "src"
import funciones as fc

# DATASETS ACNUR

# Con Excel: eliminar las hojas que no me interesan y me quedo con T1, T2 y T6 (renombrándolas)
# Con Excel: para T1 y T2, sacar las tablas "UNHCR Bureaus" y "UN major regions" a nuevas hojas
# En funciones.py: sacar cada dataset del libro de Excel y limpiarlos para eliminar los títulos que salen en las hojas de Excel (aún queda eliminar las últimas filas que contienen datos extras)

'''Para las primeras seis hojas, eliminar las columnas “refugees”, “people in refugee-like situations”, “returned refugees”, “returned IDPs”, 
“total population of concern” y “ISO 3 Code”, renombrar las columnas en castellano, pasar de float a int y eliminar la columna de "Total'''

# 1. País acogida
fc.df_ACNUR_pais_acogida.drop(
    index= range(180, 240), 
    columns=["Refugees2", "People in refugee-like situations3", "Returned refugees6", "Returned IDPs8", "Total population of concern", "ISO 3 Code"], 
    inplace=True)
fc.df_ACNUR_pais_acogida.rename(columns={
    "Country/territory of asylum1" : "País/Territorio de asilo",
    "Total refugees and people in refugee-like situations" : "Refugiadas",
    "Asylum-seekers (pending cases)4" : "Solicitantes de asilo (casos pendientes)",
    "Other people in need of international protection5" : "Otras personas que necesitan protección internacional",
    "IDPs of concern to UNHCR7" : "Desplazadas internas",
    "Persons under UNHCR's statelessness mandate9" : "Apátridas",
    "Others of concern to UNHCR10" : "Otras personas de interés"}, 
    inplace=True)
df_ACNUR_pais_acogida = fc.df_ACNUR_pais_acogida
cols = df_ACNUR_pais_acogida.columns.difference(["País/Territorio de asilo"])
df_ACNUR_pais_acogida[cols] = df_ACNUR_pais_acogida[cols].astype(int)
df_ACNUR_pais_acogida = df_ACNUR_pais_acogida[~df_ACNUR_pais_acogida["País/Territorio de asilo"].isin(["Total"])]
df_ACNUR_pais_acogida
# Cambiar los nombres de los países para quitar números y que coincidan con otros datasets
import re
df_ACNUR_pais_acogida["País/Territorio de asilo"] = df_ACNUR_pais_acogida["País/Territorio de asilo"].replace(fc.nombres_países)
df_ACNUR_pais_acogida["País/Territorio de asilo"] = df_ACNUR_pais_acogida["País/Territorio de asilo"].str.replace(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]+', '', regex=True)

# 2. Oficinas ACNUR, país de acogida
fc.df_ACNUR_pais_acogida_UNHCR_bureaus.drop(
    columns=["Refugees2", "People in refugee-like situations3", "Returned refugees6", "Returned IDPs8", "Total population of concern"], 
    inplace=True)
fc.df_ACNUR_pais_acogida_UNHCR_bureaus.rename(columns={
    "UNHCR Bureaus" : "Oficinas ACNUR",
    "Total refugees and people in refugee-like situations" : "Refugiadas",
    "Asylum-seekers (pending cases)4" : "Solicitantes de asilo (casos pendientes)",
    "Other people in need of international protection5" : "Otras personas que necesitan protección internacional",
    "IDPs of concern to UNHCR7" : "Desplazadas internas",
    "Persons under UNHCR's statelessness mandate9" : "Apátridas",
    "Others of concern to UNHCR10" : "Otras personas de interés"}, 
    inplace=True)
df_ACNUR_pais_acogida_UNHCR_bureaus = fc.df_ACNUR_pais_acogida_UNHCR_bureaus
df_ACNUR_pais_acogida_UNHCR_bureaus = df_ACNUR_pais_acogida_UNHCR_bureaus[~df_ACNUR_pais_acogida_UNHCR_bureaus["Oficinas ACNUR"].isin(["Total"])]
df_ACNUR_pais_acogida_UNHCR_bureaus

# 3. Regiones ONU, país de acogida
fc.df_ACNUR_pais_acogida_UN_regions.drop(
    columns=["Refugees2", "People in refugee-like situations3", "Returned refugees6", "Returned IDPs8", "Total population of concern"], 
    inplace=True)
fc.df_ACNUR_pais_acogida_UN_regions.rename(columns={
    "UN major regions" : "Regiones ONU",
    "Total refugees and people in refugee-like situations" : "Refugiadas",
    "Asylum-seekers (pending cases)4" : "Solicitantes de asilo (casos pendientes)",
    "Other people in need of international protection5" : "Otras personas que necesitan protección internacional",
    "IDPs of concern to UNHCR7" : "Desplazadas internas",
    "Persons under UNHCR's statelessness mandate9" : "Apátridas",
    "Others of concern to UNHCR10" : "Otras personas de interés"}, 
    inplace=True)
df_ACNUR_pais_acogida_UN_regions = fc.df_ACNUR_pais_acogida_UN_regions
df_ACNUR_pais_acogida_UN_regions = df_ACNUR_pais_acogida_UN_regions[~df_ACNUR_pais_acogida_UN_regions["Regiones ONU"].isin(["Total"])]
df_ACNUR_pais_acogida_UN_regions

# 4. País origen
fc.df_ACNUR_pais_origen.drop(
    index= range(206, 224), 
    columns=["Refugees 2", "People in refugee-like situations3", "Returned refugees6", "Returned IDPs8", "Total population of concern", "ISO 3 Code"], 
    inplace=True)
fc.df_ACNUR_pais_origen.rename(columns={
    "Origin1" : "Origen",
    "Total refugees and people in refugee-like situations" : "Refugiadas",
    "Asylum-seekers (pending cases)4" : "Solicitantes de asilo (casos pendientes)",
    "Other people in need of international protection5" : "Otras personas que necesitan protección internacional",
    "IDPs of concern to UNHCR7" : "Desplazadas internas",
    "Persons under UNHCR's statelessness mandate9" : "Apátridas",
    "Others of concern to UNHCR10" : "Otras personas de interés"}, 
    inplace=True)
df_ACNUR_pais_origen = fc.df_ACNUR_pais_origen
cols = df_ACNUR_pais_origen.columns.difference(["Origen"])
df_ACNUR_pais_origen[cols] = df_ACNUR_pais_origen[cols].astype(int)
df_ACNUR_pais_origen = df_ACNUR_pais_origen[~df_ACNUR_pais_origen["Origen"].isin(["Total"])]
df_ACNUR_pais_origen
# Cambiar los nombres de los países para quitar números y que coincidan con otros datasets
import re
df_ACNUR_pais_origen["Origen"] = df_ACNUR_pais_origen["Origen"].replace(fc.nombres_países)
df_ACNUR_pais_origen["Origen"] = df_ACNUR_pais_origen["Origen"].str.replace(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]+', '', regex=True)

# 5. Oficinas ACNUR, país de origen
fc.df_ACNUR_pais_origen_UNHCR_bureaus.drop(
    columns=["Refugees 2", "People in refugee-like situations3", "Returned refugees6", "Returned IDPs8", "Total population of concern"], 
    inplace=True)
fc.df_ACNUR_pais_origen_UNHCR_bureaus.rename(columns={
    "UNHCR Bureaus" : "Oficinas ACNUR",
    "Total refugees and people in refugee-like situations" : "Refugiadas",
    "Asylum-seekers (pending cases)4" : "Solicitantes de asilo (casos pendientes)",
    "Other people in need of international protection5" : "Otras personas que necesitan protección internacional",
    "IDPs of concern to UNHCR7" : "Desplazadas internas",
    "Persons under UNHCR's statelessness mandate9" : "Apátridas",
    "Others of concern to UNHCR10" : "Otras personas de interés"}, 
    inplace=True)
df_ACNUR_pais_origen_UNHCR_bureaus = fc.df_ACNUR_pais_origen_UNHCR_bureaus
df_ACNUR_pais_origen_UNHCR_bureaus = df_ACNUR_pais_origen_UNHCR_bureaus[~df_ACNUR_pais_origen_UNHCR_bureaus["Oficinas ACNUR"].isin(["Total"])]
df_ACNUR_pais_origen_UNHCR_bureaus

# 6. Regiones ONU, país de origen
fc.df_ACNUR_pais_origen_UN_regions.drop(
    columns=["Refugees 2", "People in refugee-like situations3", "Returned refugees6", "Returned IDPs8", "Total population of concern"], 
    inplace=True)
fc.df_ACNUR_pais_origen_UN_regions.rename(columns={
    "UN major regions" : "Regiones ONU",
    "Total refugees and people in refugee-like situations" : "Refugiadas",
    "Asylum-seekers (pending cases)4" : "Solicitantes de asilo (casos pendientes)",
    "Other people in need of international protection5" : "Otras personas que necesitan protección internacional",
    "IDPs of concern to UNHCR7" : "Desplazadas internas",
    "Persons under UNHCR's statelessness mandate9" : "Apátridas",
    "Others of concern to UNHCR10" : "Otras personas de interés"}, 
    inplace=True)
df_ACNUR_pais_origen_UN_regions = fc.df_ACNUR_pais_origen_UN_regions
df_ACNUR_pais_origen_UN_regions = df_ACNUR_pais_origen_UN_regions[~df_ACNUR_pais_origen_UN_regions["Regiones ONU"].isin(["Total"])]
df_ACNUR_pais_origen_UN_regions

# 7. demografía
'''Eliminar las dos últimas filas con datos extra, las columnas "population for which demographic data is available", “population of concern
to UNHCR end-2023”, “coverage”, “ISO code” y “country/territory of asylum/residence”, y las filas con los datos por cada país'''
fc.df_ACNUR_demografia.drop(
    index= range(9, 578), 
    columns=["Unnamed: 0", "Unnamed: 2", "Unnamed: 19", "Coverage*", "Unnamed: 21", "Unnamed: 22"], 
    inplace=True)
# Poner la primera fila como título de columnas
fc.df_ACNUR_demografia.columns = fc.df_ACNUR_demografia.iloc[0]
fc.df_ACNUR_demografia.drop(index=0, inplace=True)
fc.df_ACNUR_demografia.rename(columns= {"Population type1" : "Edad"}, inplace=True)
# Hacer transposición de la matriz y cambio de nuevo el header de las columnas
df_ACNUR_demografia = fc.df_ACNUR_demografia.T
df_ACNUR_demografia.columns = df_ACNUR_demografia.iloc[0]
df_ACNUR_demografia.drop(index="Edad", inplace=True)
# Añadir una fila para sexo
df_ACNUR_demografia.insert(0, "Sexo", ["M", "M", "M", "M", "M", "M", "M", "M", "H", "H", "H", "H", "H", "H", "H", "H"])
# Incluir índices numéricos y terminar de cambiar los nombres de las columnas
df_ACNUR_demografia.columns.name = None
df_ACNUR_demografia = df_ACNUR_demografia.reset_index()
df_ACNUR_demografia.rename(columns={
    0: "Edad", 
    "Refugees" : "Refugiadas",
    "Asylum-seekers" : "Solicitantes de asilo",
    "Other people in need of international protection" : "Otras personas que necesitan protección internacional",
    "IDPs" : "Desplazadas internas",
    "Stateless persons": "Apátridas",
    "Others of concern" : "Otras personas de interés",
    "Refugee returnees" : "Refugiadas retornadas",
    "IDP Returnees" : "Desplazadas internas retornadas"},
    inplace=True)
# Pasar las celdas de número a int
cols = df_ACNUR_demografia.columns.difference(["Edad", "Sexo"])
df_ACNUR_demografia[cols] = df_ACNUR_demografia[cols].astype(int)
# Quitar las filas "Total" y "0-17"
df_ACNUR_demografia = df_ACNUR_demografia[~df_ACNUR_demografia["Edad"].isin(["Total", "0-17"])] # ~ devuelve True para todo lo que no es "Total" ni "0-17"
df_ACNUR_demografia


# DATASET UCDP

''' Eliminar las columnas "side_a", "side_a_id", "side_a_2nd", "side_b", "side_b_id", "side_b_2nd", "cumulative_intensity", 
"type_of_conflict", "start_date","start_prec", "start_date2", "start_prec2", "ep_end", "ep_end_date", "ep_end_prec", "gwno_a", 
"gwno_a_2nd", "gwno_b", "gwno_b_2nd", "gwno_loc" y "version"'''
fc.df_2_conflictos.drop(columns=
    ["side_a", "side_a_id", "side_a_2nd", "side_b", "side_b_id", "side_b_2nd", "cumulative_intensity", "type_of_conflict", 
     "start_date","start_prec", "start_date2", "start_prec2", "ep_end", "ep_end_date", "ep_end_prec", "gwno_a", "gwno_a_2nd", 
     "gwno_b", "gwno_b_2nd", "gwno_loc", "version"],
    inplace=True)
# Pasar los valores numéricos de "incompatibility", "intensity_level" y "region" a lo que hacen referencia en el codebook
fc.df_2_conflictos["incompatibility"] = fc.df_2_conflictos["incompatibility"].apply(lambda x: fc.convertir(x, fc.incompatibilidad))
fc.df_2_conflictos["intensity_level"] = fc.df_2_conflictos["intensity_level"].apply(lambda x: fc.convertir(x, fc.nivel_intensidad))
fc.df_2_conflictos["region"] = fc.df_2_conflictos["region"].apply(lambda x: fc.convertir(x, fc.region))
# Cambiar los nulos por "no aplica"
fc.df_2_conflictos['territory_name'] = fc.df_2_conflictos['territory_name'].fillna('No aplica')
# Renombar las columnas a castellano
fc.df_2_conflictos.rename(columns={
    "conflict_id" : "ID conflicto", 
    "location" : "Ubicación",
    "incompatibility" : "Incompatibilidad",
    "territory_name" : "Nombre territorio",
    "year" : "Año",
    "intensity_level" : "Nivel intensidad",
    "region" : "Región"}, 
    inplace=True)
df_UCDP_conflictos = fc.df_2_conflictos
df_UCDP_conflictos


# DATASET SVAC

# Eliminar las columnas "actor", "type", "gwno", "interm" y "postc"
fc.df_3_violencia_sexual.drop(columns=["actor", "type", "gwnoloc", "gwnoloc2", "interm", "postc"], inplace=True)
# Pasar los valores numéricos de "actor_type", "incomp", "region", "conflictyear", "state_prev", "ai_prev", "hrw_prev", "child_prev" y "form" a lo que hacen referencia en el codebook
fc.df_3_violencia_sexual["actor_type"] = fc.df_3_violencia_sexual["actor_type"].apply(lambda x: fc.convertir(x, fc.tipo_actor))
fc.df_3_violencia_sexual["incomp"] = fc.df_3_violencia_sexual["incomp"].apply(lambda x: fc.convertir(x, fc.incompatibilidad2))
fc.df_3_violencia_sexual["region"] = fc.df_3_violencia_sexual["region"].apply(lambda x: fc.convertir(x, fc.region2))
fc.df_3_violencia_sexual["conflictyear"] = fc.df_3_violencia_sexual["conflictyear"].apply(lambda x: fc.convertir(x, fc.anio_conflicto))
fc.df_3_violencia_sexual["state_prev"] = fc.df_3_violencia_sexual["state_prev"].apply(lambda x: fc.convertir(x, fc.prevalencia))
fc.df_3_violencia_sexual["ai_prev"] = fc.df_3_violencia_sexual["ai_prev"].apply(lambda x: fc.convertir(x, fc.prevalencia))
fc.df_3_violencia_sexual["hrw_prev"] = fc.df_3_violencia_sexual["hrw_prev"].apply(lambda x: fc.convertir(x, fc.prevalencia))
fc.df_3_violencia_sexual["child_prev"] = fc.df_3_violencia_sexual["child_prev"].apply(lambda x: fc.convertir(x, fc.prevalencia))
fc.df_3_violencia_sexual["form"] = fc.df_3_violencia_sexual["form"].apply(lambda x: fc.convertir(x, fc.forma_violencia))
# Pasar "actorid" de float a Int64 (para no perder los NaN)
fc.df_3_violencia_sexual["actorid"] = fc.df_3_violencia_sexual["actorid"].astype("Int64")
# Renombar las columnas a castellano
fc.df_3_violencia_sexual.rename(columns={
    "year" : "Año",
    "conflictid" : "ID conflicto", 
    "actorid" : "ID actor",
    "actor_type" : "Tipo actor",
    "incomp" : "Incompatibilidad",
    "region" : "Región",
    "location" : "Ubicación",
    "conflictyear" : "Conflicto (dummy)",
    "state_prev" : "Datos EEUU",
    "ai_prev" : "Datos Amnistía Internacional",
    "hrw_prev" : "Datos Human Rights Watch",
    "child_prev" : "Datos ¿?",
    "form" : "Forma violencia"}, 
    inplace=True)
df_SVAC_violencia_sexual = fc.df_3_violencia_sexual
# Eliminar NaNs
df_SVAC_violencia_sexual = df_SVAC_violencia_sexual.dropna(subset=["ID actor", "Datos EEUU", "Datos Amnistía Internacional", "Datos Human Rights Watch", "Datos ¿?", "Forma violencia"])
df_SVAC_violencia_sexual


# DATASET ACLED

# Quedarme solo con las filas de 2023 de los dataset de ACLED
df_4_ataques_civiles = fc.df_4_ataques_civiles[fc.df_4_ataques_civiles["YEAR"] == 2023]
df_5_muertes_civiles = fc.df_5_muertes_civiles[fc.df_5_muertes_civiles["YEAR"] == 2023]
df_6_muertes_totales = fc.df_6_muertes_totales[fc.df_6_muertes_totales["YEAR"] == 2023]

# Cambiar el nombre de las columnas de ataques y muertes para distinguir entre los tres al unirlos
df_4_ataques_civiles.rename(columns={"EVENTS": "Ataques a civiles"}, inplace=True)
df_5_muertes_civiles.rename(columns={"FATALITIES": "Muertes de civiles"}, inplace=True)
df_6_muertes_totales.rename(columns={"FATALITIES": "Muertes totales"}, inplace=True)

# Unir todos los datasets en uno llamado ataques_y_muertes_ACLED, donde todos los países coincidan
# (en df_6_muertes_totales hay celdas en COUNTRY que no hay en el resto, pero no me interesan porque no hacen referencia a países)
df_ACLED_ataques_y_muertes = df_4_ataques_civiles.merge(df_5_muertes_civiles, on="COUNTRY").merge(df_6_muertes_totales, on="COUNTRY")

# Renombrar columnas y obtener dataset final
df_ACLED_ataques_y_muertes.drop(columns=["YEAR_y", "YEAR"], inplace=True)
df_ACLED_ataques_y_muertes.rename(columns={"COUNTRY": "País", "YEAR_x": "Año"}, inplace=True)
df_ACLED_ataques_y_muertes



# NUEVOS DATASETS

# DATASET ACNUR (ORIGEN) Y ACLED
# Cambiar los nombres de los países en ACNUR para que coincidan con los de ACLED
df_ACNUR_pais_origen["Origen"] = df_ACNUR_pais_origen["Origen"].replace(fc.nombres_países)
# Unir los datasets
df_merged_ACNURor_ACLED = df_ACNUR_pais_origen.merge(df_ACLED_ataques_y_muertes, left_on="Origen", right_on="País")
# Eliminar columnas repetidas o irrelevantes
df_merged_ACNURor_ACLED.drop(columns=["País", "Año"], inplace=True)
# Añadir columna de suma de total de personas desplazadas
df_merged_ACNURor_ACLED.insert(7, "Total", df_merged_ACNURor_ACLED[["Refugiadas", "Solicitantes de asilo (casos pendientes)", "Otras personas que necesitan protección internacional", "Desplazadas internas", "Apátridas"]].sum(axis=1))
df_merged_ACNURor_ACLED


# DATASET ACNUR (ORIGEN) y SVAC