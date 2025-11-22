# 1_Analisis_Detallado.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import unicodedata
import os

st.set_page_config(page_title="Análisis Detallado", page_icon="Chart Increasing", layout="wide")

# ========================= CSS FUTURISTA + NEÓN ============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&display=swap');
    
    body, .stApp {
        background: #0a0e17 !important;
        color: #e0f2fe;
    }
    .block-container {
        background: linear-gradient(145deg, #111827, #1a2332);
        border-radius: 28px;
        padding: 3rem;
        margin: 2rem auto;
        max-width: 95%;
        box-shadow: 
            0 0 60px rgba(0, 255, 255, 0.3),
            0 0 120px rgba(0, 255, 255, 0.15),
            inset 0 0 40px rgba(0, 255, 255, 0.1);
        border: 1px solid rgba(0, 255, 255, 0.4);
    }
    .graph-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 28px;
        font-weight: 900;
        color: #00ffff;
        text-shadow: 0 0 20px #00ffff, 0 0 40px #00ffff;
        padding: 18px 25px;
        background: rgba(0, 255, 255, 0.1);
        border-left: 6px solid #00ffff;
        border-radius: 12px;
        margin: 30px 0 20px;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.4);
        animation: neon-pulse 3s infinite alternate;
    }
    @keyframes neon-pulse {
        from { box-shadow: 0 0 20px #00ffff40, 0 0 40px #00ffff20; }
        to   { box-shadow: 0 0 40px #00ffff80, 0 0 80px #00ffff40; }
    }
    .stPlotlyChart { border-radius: 20px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ========================= NORMALIZAR NOMBRES ============================
def normalize(col):
    col = col.strip().lower()
    col = ''.join(c for c in unicodedata.normalize('NFD', col) if unicodedata.category(c) != 'Mn')
    col = col.replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    return col

# ========================= CARGAR DATOS DESDE GITHUB ============================
@st.cache_data(ttl=60)
def load_data():
    url = "https://raw.githubusercontent.com/AlbertoR2025/sap-stock-dashboard/main/dashboard/data/inventario_procesado_final.csv"
    try:
        df = pd.read_csv(url)
        df.columns = [normalize(c) for c in df.columns]
        return df
    except:
        st.error("No se pudo cargar el inventario desde GitHub")
        st.info("Verifica que el archivo esté en: dashboard/data/inventario_procesado_final.csv")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# ========================= KPIs SUPER VISUALES ============================
st.markdown("<h1 class='graph-title'>Analysis Increasing REPORTE EJECUTIVO - INVENTARIO SAP</h1>", unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.markdown(f"<div style='text-align:center;background:#1e40af;padding:20px;border-radius:15px;box-shadow:0 0 30px #1e40af60;'><h2 style='margin:0;color:#60a5fa;'>Registros</h2><h1 style='margin:5px 0;color:white;'>{len(df):,}</h1></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='text-align:center;background:#7c3aed;padding:20px;border-radius:15px;box-shadow:0 0 30px #7c3aed60;'><h2 style='margin:0;color:#c4b5fd;'>Materiales</h2><h1 style='margin:5px 0;color:white;'>{df['material'].nunique()}</h1></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div style='text-align:center;background:#0891b2;padding:20px;border-radius:15px;box-shadow:0 0 30px #0891b260;'><h2 style='margin:0;color:#a5feca;'>Unidades</h2><h1 style='margin:5px 0;color:white;'>{int(df['stock'].sum()):,}</h1></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div style='text-align:center;background:#dc2626;padding:20px;border-radius:15px;box-shadow:0 0 30px #dc262660;'><h2 style='margin:0;color:#fca5a5;'>Cajas</h2><h1 style='margin:5px 0;color:white;'>{int(df['cajas'].sum()):,}</h1></div>", unsafe_allow_html=True)
with col5:
    st.markdown(f"<div style='text-align:center;background:#f59e0b;padding:20px;border-radius:15px;box-shadow:0 0 30px #f59e0b60;'><h2 style='margin:0;color:#fde68a;'>Pallets</h2><h1 style='margin:5px 0;color:white;'>{df['pallets'].sum():.1f}</h1></div>", unsafe_allow_html=True)
with col6:
    st.markdown(f"<div style='text-align:center;background:#10b981;padding:20px;border-radius:15px;box-shadow:0 0 30px #10b98160;'><h2 style='margin:0;color:#86efac;'>Camiones</h2><h1 style='margin:5px 0;color:white;'>{df['camiones'].sum():.1f}</h1></div>", unsafe_allow_html=True)

# ========================= SUNBURST ULTRA BRILLANTE ============================
st.markdown("<h1 class='graph-title'>Sunburst Chart TOP 10 POR CAJAS - EFECTO NEÓN</h1>", unsafe_allow_html=True)

top10 = df.groupby(['material', 'descripcion'])['cajas'].sum().nlargest(10).reset_index()
top10 = top10.merge(df.groupby('material')['stock'].sum(), on='material')

# Colores NEÓN intensos y únicos
colors = [
    "#00ffff", "#ff00ff", "#ffff00", "#00ff00", "#ff3366",
    "#3366ff", "#ff6600", "#00ffcc", "#ff0066", "#66ff33"
]

labels = ["TOTAL"] + list(top10['descripcion'])
parents = [""] + ["TOTAL"] * len(top10)
values = [top10['cajas'].sum()] + list(top10['cajas'])
hover_texts = ["Todo el inventario"] + [
    f"<b>{row['descripcion']}</b><br>"
    f"Material: {row['material']}<br>"
    f"Cajas: {int(row['cajas']):,}<br>"
    f"Unidades: {int(row['stock']):,}<br>"
    f"{row['cajas']/top10['cajas'].sum()*100:.1f}% del total"
    for _, row in top10.iterrows()
]

fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",
    marker=dict(
        colors=colors,
        line=dict(color="#000", width=3),
        colorscale='electric',
        cmin=values[1:],
        cmax=values[0]
    ),
    hovertemplate="<b>%{label}</b><br>%{customdata}<extra></extra>",
    customdata=hover_texts,
    textinfo="label+percent entry",
    insidetextorientation='radial',
    textfont=dict(size=16, color="white", family="Orbitron")
))

fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=800,
    font=dict(color="#e0f2fe", family="Orbitron"),
    annotations=[dict(
        text="Chart Increasing TOP 10 MATERIALES POR CAJAS",
        x=0.5, y=1.05, xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=20, color="#00ffff"),
        font_family="Orbitron"
    )]
)

st.plotly_chart(fig, use_container_width=True)

# ========================= SUNBURST PALLETS - MEGA BRILLANTE ============================
st.markdown("<h1 class='graph-title'>Sunburst Chart DISTRIBUCIÓN POR PALLETS</h1>", unsafe_allow_html=True)

top_pallets = df.groupby(['material', 'descripcion'])['pallets'].sum().nlargest(8).reset_index()

colors_p = [
    "#ff006e", "#00f5ff", "#ffea00", "#00ff85", "#ff2a6d",
    "#05d9e8", "#ff9a00", "#d400ff"
]

labels_p = ["TOTAL"] + list(top_pallets['descripcion'])
parents_p = [""] + ["TOTAL"] * len(top_pallets)
values_p = [top_pallets['pallets'].sum()] + list(top_pallets['pallets'])

hover_p = ["Inventario completo"] + [
    f"<b>{row['descripcion']}</b><br>Pallets: {row['pallets']:.1f}<br>Unidades: {int(row['stock']):,}"
    for _, row in top_pallets.iterrows()
]

fig_p = go.Figure(go.Sunburst(
    labels=labels_p,
    parents=parents_p,
    values=values_p,
    marker=dict(colors=colors_p, line=dict(color="black", width=2)),
    hovertemplate="%{customdata}<extra></extra>",
    customdata=hover_p,
    textinfo="label+percent entry",
    textfont=dict(size=15, color="white", family="Orbitron")
))

fig_p.update_layout(
    margin=dict(t=40, l=0, r=0, b=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=700
)

st.plotly_chart(fig_p, use_container_width=True)

st.success("Analysis Increasing **Análisis completado** — Datos actualizados al {datetime.now().strftime('%d/%m/%Y %H:%M')}")

st.markdown("<p style='text-align:center;color:#64748b;margin-top:50px;'>Sistema automático • Nutrisco • Dashboard en vivo</p>", unsafe_allow_html=True)