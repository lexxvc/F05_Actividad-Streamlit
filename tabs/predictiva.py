"""Entrenamiento y evaluación del modelo de recompra."""

import pandas as pd
import streamlit as st

from stream_train.modelo import entrenar


def render(df: pd.DataFrame) -> pd.DataFrame:
    st.header("4. Estadística predictiva — Regresión logística")
    resultado = entrenar(df)

    c1, c2, c3 = st.columns(3)
    c1.metric("Exactitud (test)", f"{resultado.exactitud:.0%}")
    c2.metric("AUC", f"{resultado.auc:.2f}")
    c3.metric("Línea base (todos 'No')", f"{resultado.linea_base:.0%}")

    st.subheader("Variables que más pesan (coeficientes estandarizados)")
    st.bar_chart(resultado.coeficientes, horizontal=True)
    st.caption("Positivo = aumenta la probabilidad de recompra. Negativo = la reduce.")

    df = df.copy()
    df["prob_recompra"] = resultado.probabilidades
    df["nivel"] = pd.cut(
        df["prob_recompra"],
        [0, 0.3, 0.6, 1],
        labels=["Baja", "Media", "Alta"],
        include_lowest=True,
    )
    st.warning(
        "Alcance: modelo con datos sintéticos y ~320 clientes. "
        "Indica asociación, no causa."
    )
    return df
