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
    df['cout_t.km'] = df['COUT'] / (df['Qté Facturée'] * df['KM'])
    df['cout_tonne'] = df['COUT'] / df['Qté Facturée']
    return df

df = load_data()
st.write("🧾 Colonnes disponibles :", list(df.columns))
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

# Appliquer les filtres
filtre = df.copy
