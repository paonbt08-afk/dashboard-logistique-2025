# ============================================================
# 📊 Mini Dashboard Logistique - Taous
# ============================================================

import pandas as pd
import streamlit as st
import plotly.express as px

# ------------------------------------------------------------
# 📥 Charger les données Excel
# ------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("base_logistique_2025.xlsx")
    # Nettoyage des noms de colonnes
    df.columns = df.columns.str.strip()
    # Calculs des indicateurs de coût
    df['cout_t.km'] = df['COUT'] / (df['Qté Facturée'] * df['KM'])
    df['cout_tonne'] = df['COUT'] / df['Qté Facturée']
    return df

df = load_data()

# ------------------------------------------------------------
# 🎛️ Filtres interactifs
# ------------------------------------------------------------
st.sidebar.header("🔍 Filtres")

sites = ["Tous"] + sorted(df['Site de chargement'].dropna().unique().tolist())
transporteurs = ["Tous"] + sorted(df['Transporteur'].dropna().unique().tolist())
periodes = ["Toutes"] + sorted(df['Période'].dropna().unique().tolist())
types_transport = ["Tous"] + sorted(df['Type de transport'].dropna().unique().tolist())

site_sel = st.sidebar.selectbox("🏭 Site de chargement", sites)
trans_sel = st.sidebar.selectbox("🚛 Transporteur", transporteurs)
periode_sel = st.sidebar.selectbox("📅 Période (mois)", periodes)
type_sel = st.sidebar.selectbox("⚙️ Type de transport", types_transport)

# ------------------------------------------------------------
# 📊 Application des filtres
# ------------------------------------------------------------
filtre = df.copy()

if site_sel != "Tous":
    filtre = filtre[filtre["Site de chargement"] == site_sel]
if trans_sel != "Tous":
    filtre = filtre[filtre["Transporteur"] == trans_sel]
if periode_sel != "Toutes":
    filtre = filtre[filtre["Période"] == periode_sel]
if type_sel != "Tous":
    filtre = filtre[filtre["Type de transport"] == type_sel]

# ------------------------------------------------------------
# 📈 KPIs
# ------------------------------------------------------------
st.title("📊 Dashboard Logistique 2025")

col1, col2, col3 = st.columns(3)
col1.metric("Volume transporté (t)", f"{filtre['Qté Facturée'].sum():,.0f}")
col2.metric("Distance totale (km)", f"{filtre['KM'].sum():,.0f}")
col3.metric("Coût total (DZD)", f"{filtre['COUT'].sum():,.0f}")

# ------------------------------------------------------------
# 📉 Graphiques
# ------------------------------------------------------------
# ------------------------------------------------------------
# 📉 Graphiques
# ------------------------------------------------------------
st.subheader("📈 Coût moyen par Wilaya (DZD/t.km)")
if 'Wilaya' in filtre.columns:
    kpi_wilaya = filtre.groupby('Wilaya', as_index=False)['cout_t.km'].mean()
    fig1 = px.bar(
        kpi_wilaya,
        x='Wilaya',
        y='cout_t.km',
        color='cout_t.km',
        title="Coût moyen par Wilaya (DZD/t.km)"
    )
    st.plotly_chart(fig1, use_container_width=True)
