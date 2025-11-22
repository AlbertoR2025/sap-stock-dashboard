import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import unicodedata
import os

st.set_page_config(page_title="Análisis Detallado", page_icon="📈", layout="wide")

# ========================= CSS PREMIUM + FONDO 3D ============================
st.markdown("""
<style>
body, .stApp { background: #14151a !important; }
.block-container {
    background: linear-gradient(135deg, #16171c 0%, #262a34 100%);
    box-shadow: 0 4px 32px 0 #00e5ff55, 0 1.5rem 5rem 0 #000c !important;
    border-radius: 30px !important;
    padding: 3rem 3.5rem !important;
    margin-top: 1rem !important;
    margin-bottom: 3rem !important;
    border: 2px solid rgba(0,229,255,0.19);
    animation: base-glow 3s infinite alternate;
}
@keyframes base-glow {
  0% { box-shadow: 0 0 60px #00e5ff55, 0 8px 40px #000c; border-color: rgba(0,229,255,0.3);}
  100% { box-shadow: 0 0 100px #00e5ffa0, 0 8px 60px #001a; border-color: rgba(0,229,255,0.5);}
}
.graph-title {
    font-family: 'Poppins', sans-serif;
    font-size: 24px;
    font-weight: 700;
    color: white;
    padding: 12px 20px;
    border-left: 5px solid #00E5FF;
    background: rgba(0,229,255,0.05);
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 0 20px rgba(0,229,255,0.15), 0 4px 15px rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    gap: 10px;
    animation: glow-pulse 2s ease-in-out infinite alternate;
}
@keyframes glow-pulse {
    from { box-shadow: 0 0 15px rgba(0,229,255,0.2), 0 4px 15px rgba(0,0,0,0.3);}
    to   { box-shadow: 0 0 30px rgba(0,229,255,0.4), 0 4px 20px rgba(0,0,0,0.4);}
}
.graph-title-icon {
    font-size: 28px;
    filter: drop-shadow(0 0 10px rgba(0,229,255,0.6));
}
.section-title-main {
    background: linear-gradient(135deg, #1a3a3a 0%, #2c5364 100%);
    padding: 20px 30px;
    border-radius: 18px;
    margin: 15px auto 15px auto;
    max-width: 650px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5),
        0 0 0 2px rgba(0,229,255,0.4) inset, 0 0 50px rgba(0,229,255,0.25);
    border: 2px solid rgba(0,229,255,0.5);
    border-left: 6px solid #00E5FF;
    position: relative;
    overflow: hidden;
}
.section-title-main::before {
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 100%; height: 100%;
    background: linear-gradient(90deg,transparent,rgba(0,229,255,0.2),transparent);
    animation: slide-title 3s infinite;
}
@keyframes slide-title {
    0% { left: -100%; }
    50% { left: 100%; }
    100% { left: 100%; }
}
.section-title-main h2 {
    margin: 0; padding: 0;
    font-family: 'Poppins', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    text-shadow: 0 0 15px rgba(0,229,255,0.6), 0 2px 6px rgba(0,0,0,0.4);
    animation: glow-title 2s ease-in-out infinite alternate;
}
.section-title-main h2 span {
    font-size: 34px;
    filter: drop-shadow(0 0 10px rgba(0,229,255,0.7));
}
.main-title, .graph-title { z-index: 10; position: relative; }
</style>
""", unsafe_allow_html=True)

# =================== PORTADA GLOW ANIMADA ==================
st.markdown("""
<div class="section-title-main">
    <h2><span>📈</span> Análisis Detallado de Inventario</h2>
</div>
""", unsafe_allow_html=True)

# =============== PALETA DE COLORES =========================
PRIMARY = "#00E5FF"
ACCENT = "#FF6B6B"
SUCCESS = "#2EE59D"
WARNING = "#FFC861"

# =============== NORMALIZAR CSV ============================
def normalize(col):
    col = col.strip().lower()
    col = ''.join(c for c in unicodedata.normalize('NFD', col) if unicodedata.category(c) != 'Mn')
    col = col.replace(" ", "_")
    return col

@st.cache_data
def load_data():
    ruta = "dashboard/data/inventario_procesado_final.csv"
    df = pd.read_csv(ruta, sep=",")
    df.columns = [normalize(c) for c in df.columns]
    return df

df = load_data()
top_materiales = df.groupby(['material', 'descripcion'], as_index=False).agg({
    'stock': 'sum',
    'cajas': 'sum',
    'pallets': 'sum'
})

# ===================== GRÁFICO 1 (Barras Horizontal) ========================
st.markdown("""
<div class="graph-title">
    <span class="graph-title-icon">📦</span>
    <span>Top 15 Materiales con Mayor Stock</span>
</div>
""", unsafe_allow_html=True)
top_15 = top_materiales.nlargest(15, 'stock')
fig_barras = px.bar(
    top_15, x='stock', y='descripcion', orientation='h',
    title='', color='stock',
    color_continuous_scale=[[0, '#0E1117'], [0.5, PRIMARY], [1, ACCENT]],
    text='stock',
    hover_data={'material': True, 'stock': ':,.0f', 'cajas': ':,.0f', 'pallets': ':,.0f'}
)
fig_barras.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    xaxis_title="Stock Total",
    showlegend=False,
    template='plotly_dark',
    height=500,
    font=dict(size=12, family='Arial, sans-serif'),
    coloraxis_showscale=False,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
fig_barras.update_traces(
    texttemplate='%{text:,.0f}',
    textposition='outside',
    textfont=dict(size=11, color='white'),
    marker_line_color='rgba(0,229,255,0.3)',
    marker_line_width=1
)
st.plotly_chart(fig_barras, use_container_width=True)
st.markdown("---")

# ===================== GRÁFICO 2 (Sunburst Cajas) ========================
st.markdown("""
<div class="graph-title">
    <span class="graph-title-icon">📦</span>
    <span>Top 5 Materiales por Cajas</span>
</div>
""", unsafe_allow_html=True)
top_5_cajas = top_materiales.nlargest(5, 'cajas').copy().reset_index(drop=True)
top_5_cajas['descripcion_corta'] = top_5_cajas['descripcion'].str[:45] + '...'
total_cajas = top_5_cajas['cajas'].sum()
labels_cajas = ['Top 5'] + top_5_cajas['material'].astype(str).tolist()
parents_cajas = [''] + ['Top 5'] * len(top_5_cajas)
values_cajas = [total_cajas] + top_5_cajas['cajas'].tolist()
colors_cajas = ['#0a2342', '#FF6B35', '#F7931E', '#FF5E78', '#FF477E', '#E63946']
texto_centro_cajas = f"Total<br>{total_cajas:,.0f}<br>cajas"
texts_display_cajas = [texto_centro_cajas] + [
    f"{row['material']}<br>{row['cajas']:,.0f}<br>{row['cajas']/total_cajas*100:.0f}%"
    for _, row in top_5_cajas.iterrows()
]
hover_texts_cajas = [f"<b>Total Top 5</b><br>{total_cajas:,.0f} cajas"] + [
    f"<b>Material: {row['material']}</b><br>{row['descripcion']}<br>" +
    f"Cajas: {row['cajas']:,.0f}<br>Stock: {row['stock']:,.0f}<br>Pallets: {row['pallets']:,.0f}<br>" +
    f"Porcentaje: {row['cajas']/total_cajas*100:.1f}%"
    for _, row in top_5_cajas.iterrows()
]
fig_sunburst_cajas = go.Figure(go.Sunburst(
    labels=labels_cajas, parents=parents_cajas, values=values_cajas,
    text=texts_display_cajas, textinfo='text',
    insidetextorientation='auto',
    textfont=dict(size=13, color='white', family='Arial, sans-serif', weight='bold'),
    marker=dict(colors=colors_cajas, line=dict(color='#0E1117', width=2)),
    customdata=hover_texts_cajas, hovertemplate='%{customdata}<extra></extra>',
    branchvalues='total'
))
fig_sunburst_cajas.update_layout(
    template='plotly_dark', height=650, showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        font=dict(size=11, color='white', family='Arial'),
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,229,255,0.3)', borderwidth=1
    ),
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=250, t=20, b=20),
    xaxis=dict(visible=False), yaxis=dict(visible=False)
)
for idx in range(len(top_5_cajas)):
    row = top_5_cajas.iloc[idx]
    fig_sunburst_cajas.add_trace(go.Scatter(
        x=[None], y=[None], mode='markers', marker=dict(size=10, color=colors_cajas[idx+1]),
        legendgroup=str(row['material']), showlegend=True, name=row['descripcion_corta']
    ))
st.plotly_chart(fig_sunburst_cajas, use_container_width=True)
st.markdown("---")

# ===================== GRÁFICO 3 (Sunburst Stock) ========================
st.markdown("""
<div class="graph-title">
    <span class="graph-title-icon">📊</span>
    <span>Top 5 Materiales por Stock</span>
</div>
""", unsafe_allow_html=True)
top_5_stock = top_materiales.nlargest(5, 'stock').copy().reset_index(drop=True)
top_5_stock['descripcion_corta'] = top_5_stock['descripcion'].str[:45] + '...'
total_stock_5 = top_5_stock['stock'].sum()
labels_5 = ['Top 5'] + top_5_stock['material'].astype(str).tolist()
parents_5 = [''] + ['Top 5'] * len(top_5_stock)
values_5 = [total_stock_5] + top_5_stock['stock'].tolist()
colors_premium_5 = ['#0a2342', '#00E5FF', '#FF6B6B', '#0096FF', '#FFC861', '#9D4EDD']
texto_centro_5 = f"Total<br>{total_stock_5:,.0f}<br>unidades"
texts_display_5 = [texto_centro_5] + [
    f"{row['material']}<br>{row['stock']:,.0f}<br>{row['stock']/total_stock_5*100:.0f}%"
    for _, row in top_5_stock.iterrows()
]
hover_texts_5 = [f"<b>Total Top 5</b><br>{total_stock_5:,.0f} unidades"] + [
    f"<b>Material: {row['material']}</b><br>{row['descripcion']}<br>" +
    f"Stock: {row['stock']:,.0f}<br>Porcentaje: {row['stock']/total_stock_5*100:.1f}%"
    for _, row in top_5_stock.iterrows()
]
fig_sunburst_5 = go.Figure(go.Sunburst(
    labels=labels_5, parents=parents_5, values=values_5,
    text=texts_display_5, textinfo='text',
    insidetextorientation='auto',
    textfont=dict(size=13, color='white', family='Arial, sans-serif', weight='bold'),
    marker=dict(colors=colors_premium_5, line=dict(color='#0E1117', width=2)),
    customdata=hover_texts_5, hovertemplate='%{customdata}<extra></extra>',
    branchvalues='total'
))
fig_sunburst_5.update_layout(
    template='plotly_dark', height=650, showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        font=dict(size=11, color='white', family='Arial'),
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,229,255,0.3)', borderwidth=1
    ),
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=250, t=20, b=20),
    xaxis=dict(visible=False), yaxis=dict(visible=False)
)
for idx in range(len(top_5_stock)):
    row = top_5_stock.iloc[idx]
    fig_sunburst_5.add_trace(go.Scatter(
        x=[None], y=[None], mode='markers', marker=dict(size=10, color=colors_premium_5[idx+1]),
        legendgroup=str(row['material']), showlegend=True, name=row['descripcion_corta']
    ))
st.plotly_chart(fig_sunburst_5, use_container_width=True)
st.markdown("---")

# ===================== GRÁFICO 4 (Sunburst Pallets) ========================
st.markdown("""
<div class="graph-title">
    <span class="graph-title-icon">🚛</span>
    <span>Top 5 Materiales por Pallets</span>
</div>
""", unsafe_allow_html=True)
top_5_pallets = top_materiales.nlargest(5, 'pallets').copy().reset_index(drop=True)
top_5_pallets['descripcion_corta'] = top_5_pallets['descripcion'].str[:45] + '...'
total_pallets = top_5_pallets['pallets'].sum()
labels_pallets = ['Top 5'] + top_5_pallets['material'].astype(str).tolist()
parents_pallets = [''] + ['Top 5'] * len(top_5_pallets)
values_pallets = [total_pallets] + top_5_pallets['pallets'].tolist()
colors_pallets = ['#0a2342', '#00E5FF', '#FF6B6B', '#0096FF', '#FFC861', '#9D4EDD']
texto_centro_pallets = f"Total<br>{total_pallets:.0f}"
texts_display_pallets = [texto_centro_pallets] + [
    f"{row['material']}<br>{row['pallets']:.0f}<br>{row['pallets']/total_pallets*100:.0f}%"
    for _, row in top_5_pallets.iterrows()
]
hover_texts_pallets = [f"<b>Total Top 5</b><br>{total_pallets:.0f} pallets"] + [
    f"<b>Material: {row['material']}</b><br>{row['descripcion']}<br>" +
    f"Pallets: {row['pallets']:.0f}<br>Stock: {row['stock']:,.0f}<br>" +
    f"Porcentaje: {row['pallets']/total_pallets*100:.1f}%"
    for _, row in top_5_pallets.iterrows()
]
fig_sunburst_pallets = go.Figure(go.Sunburst(
    labels=labels_pallets, parents=parents_pallets, values=values_pallets,
    text=texts_display_pallets, textinfo='text',
    insidetextorientation='auto',
    textfont=dict(size=13, color='white', family='Arial, sans-serif', weight='bold'),
    marker=dict(colors=colors_pallets, line=dict(color='#0E1117', width=2)),
    customdata=hover_texts_pallets, hovertemplate='%{customdata}<extra></extra>',
    branchvalues='total'
))
fig_sunburst_pallets.update_layout(
    template='plotly_dark', height=650, showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        font=dict(size=11, color='white', family='Arial'),
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,229,255,0.3)', borderwidth=1
    ),
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=250, t=20, b=20),
    xaxis=dict(visible=False), yaxis=dict(visible=False)
)
for idx in range(len(top_5_pallets)):
    row = top_5_pallets.iloc[idx]
    fig_sunburst_pallets.add_trace(go.Scatter(
        x=[None], y=[None], mode='markers', marker=dict(size=10, color=colors_pallets[idx+1]),
        legendgroup=str(row['material']), showlegend=True, name=row['descripcion_corta']
    ))

st.plotly_chart(fig_sunburst_pallets, use_container_width=True)

st.markdown("---")

st.markdown("---")
st.success("🎯 **Análisis visual completado** - Vista integral del inventario SAP")
