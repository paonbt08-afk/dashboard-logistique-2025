# ============================================================
# 📊 Mini Dashboard Logistique 2025 - Taous
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
    df.columns = df.columns.str.strip()
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
# 📈 KPI principaux
# ------------------------------------------------------------
st.title("📊 Dashboard Logistique 2025")

col1, col2, col3 = st.columns(3)
col1.metric("Volume transporté (t)", f"{filtre['Qté Facturée'].sum():,.0f}")
col2.metric("Distance totale (km)", f"{filtre['KM'].sum():,.0f}")
col3.metric("Coût total (DZD)", f"{filtre['COUT'].sum():,.0f}")

# ------------------------------------------------------------
# 📉 Coût moyen par Wilaya
# ------------------------------------------------------------
st.subheader("📈 Coût moyen par Wilaya (DZD/t.km)")
if 'Wilaya' in filtre.columns:
    kpi_wilaya = filtre.groupby('Wilaya', as_index=False)['cout_t.km'].mean()
    fig1 = px.bar(
        kpi_wilaya,
        x='Wilaya',
        y='cout_t.km',
        color='cout_t.km',
        title="Coût moyen par Wilaya (DZD/t.km)",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig1, use_container_width=True)

# ------------------------------------------------------------
# 📆 Évolution mensuelle du coût moyen
# ------------------------------------------------------------
st.subheader("📊 Évolution mensuelle du coût moyen (DZD/t.km)")
if 'Période' in filtre.columns:
    evolution = (
        filtre.groupby('Période', as_index=False)['cout_t.km']
        .mean()
        .sort_values('Période')
    )
    fig2 = px.line(
        evolution,
        x='Période',
        y='cout_t.km',
        markers=True,
        title="Évolution du coût moyen par mois",
        line_shape="spline"
    )
    fig2.update_traces(line_color="#1f77b4", marker=dict(size=8, color="#FF4136"))
    st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------------------
# 🗺️ Carte interactive - Coût moyen par Wilaya
# ------------------------------------------------------------
st.subheader("🗺️ Carte interactive - Coût moyen par Wilaya")
if 'Wilaya' in filtre.columns:
    try:
        # Dictionnaire simplifié Wilaya -> coordonnées (approx.)
        coords = {
            'ADRAR': (27.9, -0.3), 'AIN-DEFLA': (36.2, 1.9), 'ALGER': (36.7, 3.1),
            'ANNABA': (36.9, 7.8), 'BATNA': (35.5, 6.2), 'BECHAR': (31.6, -2.2),
            'BEJAIA': (36.75, 5.07), 'BISKRA': (34.85, 5.73), 'BLIDA': (36.48, 2.8),
            'BOUMERDES': (36.75, 3.48), 'CHLEF': (36.16, 1.34), 'CONSTANTINE': (36.35, 6.6),
            'DJELFA': (34.67, 3.25), 'GHARDAIA': (32.48, 3.67), 'MASCARA': (35.4, 0.15),
            'MILA': (36.45, 6.27), 'MOSTAGANEM': (35.94, 0.09), 'ORAN': (35.7, -0.62),
            'OUARGLA': (31.95, 5.33), 'SAIDA': (34.83, 0.15), 'SETIF': (36.18, 5.41),
            'SIDI BEL-ABBES': (35.19, -0.64), 'TAMANRASSET': (22.8, 5.5),
            'TLEMCEN': (34.9, -1.3), 'TIZI-OUZOU': (36.7, 4.05), 'TIARET': (35.37, 1.32)
        }

        map_data = filtre.groupby('Wilaya', as_index=False)['cout_t.km'].mean()
        map_data['lat'] = map_data['Wilaya'].map(lambda w: coords[w][0] if w in coords else None)
        map_data['lon'] = map_data['Wilaya'].map(lambda w: coords[w][1] if w in coords else None)
        map_data = map_data.dropna(subset=['lat', 'lon'])

        fig_map = px.scatter_mapbox(
            map_data,
            lat='lat',
            lon='lon',
            size='cout_t.km',
            color='cout_t.km',
            hover_name='Wilaya',
            color_continuous_scale="YlOrRd",
            size_max=25,
            zoom=4.5,
            title="Carte du coût moyen par Wilaya (DZD/t.km)"
        )
        fig_map.update_layout(mapbox_style="carto-positron")
        st.plotly_chart(fig_map, use_container_width=True)
    except Exception as e:
        st.error(f"Erreur lors du rendu de la carte : {e}")

# ------------------------------------------------------------
# 📋 Données filtrées
# ------------------------------------------------------------
st.subheader("📋 Données filtrées")
st.dataframe(filtre)

st.success("✅ Dashboard chargé avec succès !")
