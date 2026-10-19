"""Estadística descriptiva de clientes y segmentos."""

import pandas as pd
import streamlit as st


def render(df: pd.DataFrame) -> None:
    st.header("3. Estadística descriptiva")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tasa de recompra", f"{df['recompra'].mean():.0%}")
    c2.metric("Ticket promedio", f"${df['ticket_promedio'].mean():,.0f}")
    c3.metric("Compras por cliente", f"{df['num_compras'].mean():.1f}")
    c4.metric("Días desde última compra", f"{df['dias_ultima_compra'].median():.0f}")

    segmentos = (
        df.groupby("segmento")
        .agg(
            clientes=("recompra", "size"),
            tasa_recompra=("recompra", "mean"),
            ticket=("ticket_promedio", "mean"),
        )
        .round(2)
    )
    st.subheader("Tasa de recompra por segmento")
    st.bar_chart(
        segmentos["tasa_recompra"],
        y_label="Tasa de recompra",
        x_label="Segmento",
    )
    st.dataframe(segmentos, width="stretch")

    columna = st.selectbox(
        "Comparar recompra por:",
        ["canal_origen", "uso_promocion", "familia_olfativa", "genero_preferido"],
    )
    st.bar_chart(df.groupby(columna)["recompra"].mean(), y_label="Tasa de recompra")
