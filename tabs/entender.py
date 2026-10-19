"""Exploración inicial de los datos."""

import pandas as pd
import streamlit as st


def render(raw: pd.DataFrame) -> None:
    st.header("1. Entender los datos")
    c1, c2, c3 = st.columns(3)
    c1.metric("Filas (clientes)", raw.shape[0])
    c2.metric("Variables", raw.shape[1])
    c3.metric("Porcentaje de recompra", f"{(raw['recompra_ultima_campana'] == 'Sí').mean():.0%}")

    st.subheader("Vista previa")
    st.dataframe(raw.head(10), width="stretch")

    st.subheader("Variables y tipos de datos")
    info = pd.DataFrame(
        {
            "tipo": raw.dtypes.astype(str),
            "valores_únicos": raw.nunique(),
            "ejemplo": raw.iloc[0].astype(str),
        }
    )
    st.dataframe(info, width="stretch")
    st.info(
        "Variables clave: num_compras, dias_ultima_compra, uso_promocion, "
        "canal_origen. Duda: 'calificacion' es auto-reportada y 'edad' tiene huecos."
    )
