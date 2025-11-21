import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import cargar_datos
import plotly.express as px
import pandas as pd

df = pd.read_csv("data/inventario_procesado_final.csv", encoding="utf-8-sig")
df.columns = df.columns.astype(str).str.strip().str.upper()


total_stock = df['STOCK'].sum()
total_cajas = df['CAJAS'].sum()
total_pallets = df['PALLETS'].sum()
total_camiones = df['CAMIONES'].sum()


# Configuración de la página
st.set_page_config(
    page_title="Panel de Control",
    page_icon="📦",
    layout="wide"
)

# Cargar datos
df = cargar_datos()

st.markdown("""
<style>
    /* CSS para títulos secundarios estilo Panel de Control */
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
        box-shadow: 
            0 0 20px rgba(0,229,255,0.15),
            0 4px 15px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        gap: 10px;
        animation: glow-pulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow-pulse {
        from {
            box-shadow: 
                0 0 15px rgba(0,229,255,0.2),
                0 4px 15px rgba(0,0,0,0.3);
        }
        to {
            box-shadow: 
                0 0 30px rgba(0,229,255,0.4),
                0 4px 20px rgba(0,0,0,0.4);
        }
    }
    
    .graph-title-icon {
        font-size: 28px;
        filter: drop-shadow(0 0 10px rgba(0,229,255,0.6));
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# BANNER COMPACTO CON EFECTOS Y ANIMACIÓN
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap');
    
    .hero-banner {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 25px 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 
            0 15px 40px rgba(0,0,0,0.5),
            0 0 0 1px rgba(0,255,255,0.2) inset,
            0 0 60px rgba(0,229,255,0.3);
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(0,229,255,0.3);
    }
    
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(0, 229, 255, 0.15) 50%,
            transparent 70%
        );
        animation: shine 6s infinite;
    }
    
    @keyframes shine {
        0% { transform: rotate(0deg) translate(-50%, -50%); }
        100% { transform: rotate(360deg) translate(-50%, -50%); }
    }
    
    .hero-banner::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.2),
            transparent
        );
        animation: slide 3s infinite;
    }
    
    @keyframes slide {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .hero-content {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        position: relative;
        z-index: 1;
    }
    
    .hero-icon {
        font-size: 40px;
        filter: drop-shadow(0 0 15px rgba(0,229,255,0.6));
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    .hero-text-container {
        text-align: left;
    }
    
    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 32px;
        font-weight: 900;
        background: linear-gradient(90deg, #00E5FF 0%, #00f2fe 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 3px;
        margin: 0;
        line-height: 1;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 8px rgba(0,229,255,0.5)); }
        to { filter: drop-shadow(0 0 15px rgba(0,229,255,0.8)); }
    }
    
    .hero-subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 12px;
        color: rgba(255,255,255,0.85);
        margin-top: 5px;
        letter-spacing: 1.5px;
        font-weight: 500;
    }
</style>

<div class="hero-banner">
    <div class="hero-content">
        <div class="hero-icon">📦</div>
        <div class="hero-text-container">
            <h1 class="hero-title">DASHBOARD SAP ULTRA</h1>
            <p class="hero-subtitle">Centro P109 • Inventario en Tiempo Real</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# CSS PARA TARJETAS KPI PREMIUM CON BRILLO Y EFECTOS
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&display=swap');
    
    .kpi-card {
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
        padding: 30px 25px;
        border-radius: 20px;
        box-shadow: 
            0 8px 32px rgba(0,0,0,0.4),
            0 0 0 1px rgba(255,255,255,0.1) inset,
            0 0 40px rgba(var(--glow-color), 0.3);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255,255,255,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
        transform: rotate(45deg);
        transition: all 0.6s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 16px 48px rgba(0,0,0,0.5),
            0 0 0 1px rgba(255,255,255,0.2) inset,
            0 0 60px rgba(var(--glow-color), 0.6);
    }
    
    .kpi-card:hover::before {
        left: 100%;
    }
    
    .kpi-icon {
        font-size: 56px;
        margin-bottom: 12px;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .kpi-title {
        font-size: 13px;
        color: rgba(255,255,255,0.95);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 15px;
        font-family: 'Poppins', sans-serif;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .kpi-value {
        font-size: 48px;
        font-weight: 800;
        color: white;
        margin: 15px 0;
        text-shadow: 
            0 2px 10px rgba(0,0,0,0.3),
            0 0 20px rgba(255,255,255,0.2);
        font-family: 'Poppins', sans-serif;
        line-height: 1;
    }
    
    .kpi-subtitle {
        font-size: 14px;
        color: rgba(255,255,255,0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        font-weight: 600;
        margin-top: 10px;
    }
    
    .kpi-badge {
        display: inline-block;
        padding: 4px 12px;
        background: rgba(255,255,255,0.15);
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
        margin-top: 8px;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# KPIs CON DISEÑO PREMIUM
# ============================================================================

# Calcular KPIs
total_stock = df['Stock'].sum()
total_cajas = df['Cajas'].sum()
total_pallets = df['Pallets'].sum()
total_camiones = df['Camiones'].sum()

# Grid de 4 columnas para KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card" style="--gradient-start: #667eea; --gradient-end: #764ba2; --glow-color: 102, 126, 234;">
        <div class="kpi-icon">📊</div>
        <div class="kpi-title">⚡ Stock Total</div>
        <div class="kpi-value">{total_stock:,.0f}</div>
        <div class="kpi-subtitle">
            <span>▲</span> Unidades Totales
        </div>
        <div class="kpi-badge">INVENTARIO</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card" style="--gradient-start: #f093fb; --gradient-end: #f5576c; --glow-color: 240, 147, 251;">
        <div class="kpi-icon">📦</div>
        <div class="kpi-title">🔥 Stock Cajas</div>
        <div class="kpi-value">{total_cajas:,.0f}</div>
        <div class="kpi-subtitle">
            <span>▲</span> Cajas Disponibles
        </div>
        <div class="kpi-badge">EMPAQUE</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card" style="--gradient-start: #4facfe; --gradient-end: #00f2fe; --glow-color: 79, 172, 254;">
        <div class="kpi-icon">🚛</div>
        <div class="kpi-title">💎 Total Pallets</div>
        <div class="kpi-value">{total_pallets:,.0f}</div>
        <div class="kpi-subtitle">
            <span>●</span> Pallets Activos
        </div>
        <div class="kpi-badge">LOGÍSTICA</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card" style="--gradient-start: #fa709a; --gradient-end: #fee140; --glow-color: 250, 112, 154;">
        <div class="kpi-icon">🚚</div>
        <div class="kpi-title">🌟 Camiones</div>
        <div class="kpi-value">{total_camiones:.0f}</div>
        <div class="kpi-subtitle">
            <span>●</span> Flota Disponible
        </div>
        <div class="kpi-badge">TRANSPORTE</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SEPARACIÓN DESPUÉS DE LOS KPIs
# ============================================================================

st.markdown("<br><br>", unsafe_allow_html=True)


# ============================================================================
import plotly.express as px
import pandas as pd

# ============================================================================
# 📦 TOP MATERIALES POR STOCK
# ============================================================================

# 1. TÍTULO CON FORMATO (DEBE IR PRIMERO)
st.markdown("""
<div class="graph-title">
    <span class="graph-title-icon">📊</span>
    <span>Top 5 Materiales por Stock</span>
</div>
""", unsafe_allow_html=True)

# 2. PREPARAR DATOS
df_grouped = df.groupby('Material', as_index=False)['Stock'].sum()
df_grouped['Material_str'] = df_grouped['Material'].astype(int).astype(str)
top5 = df_grouped.nlargest(5, 'Stock')

# 3. CREAR GRÁFICO
fig = px.bar(
    top5,
    x='Material_str',
    y='Stock',
    text='Stock'
)

# 4. CONFIGURAR GRÁFICO
fig.update_traces(
    marker_color='#00E5FF',
    marker_line_color='#00BFFF',
    marker_line_width=1,
    texttemplate='%{text:,.0f}',
    textposition='outside',
    textfont=dict(size=12, color='white')
)

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white', family='Poppins'),
    xaxis=dict(
        title='Material',
        tickangle=-45,
        tickfont=dict(size=11),
        showgrid=False
    ),
    yaxis=dict(
        title='Stock',
        tickformat=',.0f',
        showgrid=True,
        gridcolor='rgba(0,229,255,0.1)'
    ),
    height=500,
    margin=dict(l=80, r=40, t=40, b=100)
)

# Forzar tipo categoría en eje X
fig.update_xaxes(type='category', tickformat='')

# 5. MOSTRAR GRÁFICO
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
# ============================================================================
# SEPARACIÓN ENTRE GRÁFICO Y MÉTRICAS
# ============================================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

