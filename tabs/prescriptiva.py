"""Recomendaciones promocionales por segmento."""

import pandas as pd
import streamlit as st

ACCIONES = {
    "Leal activo": (
        "Programa VIP: aviso por WhatsApp el día del lanzamiento",
        "Sin descuento: ya compran; proteger margen",
    ),
    "Leal dormido": (
        "Cupón 15 % en su familia olfativa favorita",
        "Alto historial pero mucho tiempo sin comprar",
    ),
    "Nuevo activo": (
        "Muestra/decant gratis en 2.ª compra",
        "Convertir la primera compra en hábito",
    ),
    "En riesgo": (
        "Mensaje de reactivación + 2x1 en decants",
        "Baja probabilidad: acción barata y masiva",
    ),
}


def render(df: pd.DataFrame) -> None:
    st.header("5. Estadística prescriptiva")
    tabla = (
        df.groupby("segmento")
        .agg(
            clientes=("prob_recompra", "size"),
            prob_media=("prob_recompra", "mean"),
            recompra_real=("recompra", "mean"),
        )
        .round(2)
    )
    tabla["acción"] = [ACCIONES[segmento][0] for segmento in tabla.index]
    tabla["razón"] = [ACCIONES[segmento][1] for segmento in tabla.index]
    st.dataframe(tabla.sort_values("prob_media", ascending=False), width="stretch")
    st.subheader("Clientes por nivel de probabilidad")
    st.bar_chart(df["nivel"].value_counts().sort_index())
