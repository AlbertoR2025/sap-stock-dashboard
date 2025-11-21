import streamlit as st
import pandas as pd
from utils.data_loader import cargar_datos
from io import BytesIO  # ← AGREGAR ESTA LÍNEA


# Configuración de la página
st.set_page_config(
    page_title="Datos Fuente",
    page_icon="📊",
    layout="wide"
)

# Cargar datos
df = cargar_datos()

# ============================================================================
# CSS GLOBAL
# ============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@600;700;800&display=swap');
    
    /* Reducir padding superior */
    .main .block-container {
        padding-top: 1rem !important;
    }
    
    /* Banner compacto CENTRADO */
    .hero-banner-small {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 20px 30px;
        border-radius: 18px;
        margin: 0 auto 30px auto;
        max-width: 550px;
        box-shadow: 
            0 15px 40px rgba(0,0,0,0.5),
            0 0 0 1px rgba(0,255,255,0.2) inset,
            0 0 60px rgba(0,229,255,0.3);
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(0,229,255,0.3);
    }
    
    .hero-banner-small::before {
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
    
    .hero-banner-small h2 {
        margin: 0;
        padding: 0;
        font-family: 'Poppins', sans-serif;
        font-size: 24px;
        font-weight: 800;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        text-shadow: 
            0 0 15px rgba(0,229,255,0.6),
            0 2px 6px rgba(0,0,0,0.4);
        position: relative;
        z-index: 1;
    }
    
    .hero-banner-small h2 span {
        font-size: 30px;
        filter: drop-shadow(0 0 10px rgba(0,229,255,0.7));
    }
    
    /* Mini KPIs */
    .mini-kpi {
        background: linear-gradient(135deg, #1a3a3a, #2c5364);
        padding: 15px 20px;
        border-radius: 12px;
        border: 1px solid rgba(0,229,255,0.3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        text-align: center;
    }
    
    .mini-kpi-value {
        font-size: 24px;
        font-weight: 800;
        color: #00E5FF;
        font-family: 'Poppins', sans-serif;
    }
    
    .mini-kpi-label {
        font-size: 11px;
        color: rgba(255,255,255,0.8);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 5px;
    }
    
    /* Tabla estilizada */
    .dataframe {
        background: rgba(0,0,0,0.3) !important;
        border-radius: 10px !important;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #134e5e, #1a6a7c) !important;
        color: white !important;
        font-weight: 700 !important;
        text-align: center !important;
        padding: 12px !important;
        border: 1px solid rgba(0,229,255,0.2) !important;
    }
    
    .dataframe tbody tr {
        background: rgba(26,58,58,0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background: rgba(44,83,100,0.3) !important;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(0,229,255,0.1) !important;
        transform: scale(1.01) !important;
        box-shadow: 0 4px 12px rgba(0,229,255,0.2) !important;
    }
    
    .dataframe tbody tr td {
        color: white !important;
        padding: 10px !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# BANNER CENTRADO
# ============================================================================

st.markdown("""
<div class="hero-banner-small">
    <h2><span>📊</span> Datos Fuente del Inventario</h2>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MINI KPIs
# ============================================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="mini-kpi">
        <div class="mini-kpi-value">{len(df):,}</div>
        <div class="mini-kpi-label">📋 Total Registros</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="mini-kpi">
        <div class="mini-kpi-value">{df['Centro'].nunique()}</div>
        <div class="mini-kpi-label">🏢 Centros</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="mini-kpi">
        <div class="mini-kpi-value">{df['Material'].nunique()}</div>
        <div class="mini-kpi-label">📦 Materiales Únicos</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# FILTROS
# ============================================================================

col_filter1, col_filter2, col_filter3 = st.columns(3)

with col_filter1:
    centros = ['Todos'] + sorted(df['Centro'].unique().tolist())
    centro_seleccionado = st.selectbox('🏢 Centro', centros)

with col_filter2:
    almacenes = ['Todos'] + sorted([str(x) for x in df['Almacén'].dropna().unique() if str(x).lower() != 'nan'])
    almacen_seleccionado = st.selectbox('📦 Almacén', almacenes)

with col_filter3:
    buscar_material = st.text_input('🔍 Buscar Material', '')

# Aplicar filtros
df_filtrado = df.copy()

if centro_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Centro'] == centro_seleccionado]

if almacen_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Almacén'] == almacen_seleccionado]

if buscar_material:
    df_filtrado = df_filtrado[
        df_filtrado['Descripción'].str.contains(buscar_material, case=False, na=False) |
        df_filtrado['Material'].astype(str).str.contains(buscar_material, case=False, na=False)
    ]

# ============================================================================
# TÍTULO DE LA TABLA
# ============================================================================


# ============================================================================
# TABLA DE DATOS
# ============================================================================

st.dataframe(
    df_filtrado,
    use_container_width=True,
    height=600,
    hide_index=True
)

# ============================================================================
# BOTONES DE DESCARGA DEBAJO DE LA TABLA
# ============================================================================

st.markdown("<br>", unsafe_allow_html=True)

col_download1, col_download2, col_spacer = st.columns([1, 1, 3])

with col_download1:
    # Descargar CSV
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name=f"inventario_sap_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col_download2:
    # Descargar Excel
    from io import BytesIO
    
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_filtrado.to_excel(writer, index=False, sheet_name='Inventario')
    
    st.download_button(
        label="📊 Descargar xlsx",
        data=buffer.getvalue(),
        file_name=f"inventario_sap_{pd.Timestamp.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
