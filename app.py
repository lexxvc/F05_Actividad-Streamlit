"""Aplicación Streamlit para analizar la recompra de clientes de perfumes."""

from pathlib import Path

import pandas as pd
import streamlit as st

from tabs import decisiones, descriptiva, entender, limpiar, predictiva, prescriptiva

st.set_page_config(page_title="Recompra Perfumes", page_icon="🧴", layout="wide")
st.title("Recompra de clientes — Negocio de perfumes")
st.caption(
    "¿Qué clientes tienen mayor probabilidad de volver a comprar y "
    "qué promoción le damos a cada tipo?"
)


@st.cache_data
def cargar() -> pd.DataFrame:
    ruta_datos = Path(__file__).parent / "data" / "clientes_perfumes.csv"
    return pd.read_csv(ruta_datos)


raw = cargar()
tabs = st.tabs(
    [
        "1. Entender",
        "2. Limpiar",
        "3. Describir",
        "4. Predecir",
        "5. Prescribir",
        "6. Decidir",
    ]
)

with tabs[0]:
    entender.render(raw)

with tabs[1]:
    df = limpiar.render(raw)

with tabs[2]:
    descriptiva.render(df)

with tabs[3]:
    df = predictiva.render(df)

with tabs[4]:
    prescriptiva.render(df)

with tabs[5]:
    decisiones.render(df)
