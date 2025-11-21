import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análisis Detallado", page_icon="📊", layout="wide")

st.title("Análisis Detallado de Inventario")
st.markdown("---")

@st.cache_data
def cargar_datos():
    try:
        df = pd.read_csv("data/inventario_procesado_final.csv", encoding="utf-8-sig")
        # Mapeo sencillo de nombres de columnas
        columnmapping = {}
        for col in df.columns:
            collower = str(col).lower()
            if "stock" in collower:
                columnmapping[col] = "Stock"
            elif "caja" in collower:
                columnmapping[col] = "Cajas"
            elif "material" in collower:
                columnmapping[col] = "Material"
            elif "descrip" in collower:
                columnmapping[col] = "Descripción"
        df = df.rename(columns=columnmapping)
        # <<< LÍNEA CRÍTICA AGREGADA: elimina duplicados de Material+Descripción >>>
        df = df.drop_duplicates(subset=["Material", "Descripción"])
        # Conversión segura a numérico para evitar incoherencias en gráficos
        if "Stock" in df.columns:
            df["Stock"] = pd.to_numeric(df["Stock"], errors="coerce").fillna(0)
        if "Cajas" in df.columns:
            df["Cajas"] = pd.to_numeric(df["Cajas"], errors="coerce").fillna(0)
        return df
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return pd.DataFrame()

df = cargar_datos()

# KPIs Detallados (puedes personalizar aquí si lo deseas)

st.dataframe(df, use_container_width=True, height=600)

# Ejemplo: Top 15 materiales con mayor stock
if not df.empty and "Stock" in df.columns and "Material" in df.columns:
    top_materiales = (
        df.groupby(["Material", "Descripción"], as_index=False)["Stock"].sum()
        .sort_values(by="Stock", ascending=False)
        .head(15)
    )

    fig1 = px.bar(
        top_materiales,
        x="Stock",
        y="Descripción",
        orientation="h",
        color="Stock",
        title="Top 15 Materiales con Mayor Stock",
        text="Stock",
        height=600
    )
    fig1.update_traces(texttemplate="%{text:,.0f}")
    st.plotly_chart(fig1, use_container_width=True)

# Top 5 materiales por cajas
if not df.empty and "Cajas" in df.columns and "Material" in df.columns:
    top_cajas = (
        df.groupby(["Material", "Descripción"], as_index=False)["Cajas"].sum()
        .sort_values(by="Cajas", ascending=False)
        .head(5)
    )

    fig2 = px.sunburst(
        top_cajas,
        path=["Material", "Descripción"],
        values="Cajas",
        title="Top 5 Materiales por Cajas",
        color="Cajas",
        height=600
    )
    st.plotly_chart(fig2, use_container_width=True)

# Top 5 materiales por stock (sunburst)
if not df.empty and "Stock" in df.columns and "Material" in df.columns:
    top_stock = (
        df.groupby(["Material", "Descripción"], as_index=False)["Stock"].sum()
        .sort_values(by="Stock", ascending=False)
        .head(5)
    )

    fig3 = px.sunburst(
        top_stock,
        path=["Material", "Descripción"],
        values="Stock",
        title="Top 5 Materiales por Stock",
        color="Stock",
        height=600
    )
    st.plotly_chart(fig3, use_container_width=True)

