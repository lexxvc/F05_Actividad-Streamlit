"""Limpieza y segmentación de los datos."""

import pandas as pd
import streamlit as st

TARGET = "recompra_ultima_campana"


def _asignar_segmento(fila: pd.Series) -> str:
    if fila["num_compras"] >= 4 and fila["dias_ultima_compra"] <= 90:
        return "Leal activo"
    if fila["num_compras"] >= 4:
        return "Leal dormido"
    if fila["dias_ultima_compra"] <= 90:
        return "Nuevo activo"
    return "En riesgo"


def render(raw: pd.DataFrame) -> pd.DataFrame:
    st.header("2. Limpiar los datos")
    nulos = raw.isna().sum()
    duplicados = raw.duplicated().sum()
    c1, c2 = st.columns(2)
    c1.metric("Celdas nulas", int(nulos.sum()))
    c2.metric("Filas duplicadas", int(duplicados))
    st.dataframe(nulos[nulos > 0].rename("nulos"), width="stretch")

    df = raw.drop_duplicates().copy()
    df["edad"] = df["edad"].fillna(df["edad"].median())
    df["calificacion"] = df["calificacion"].fillna(df["calificacion"].median())
    df["canal_origen"] = df["canal_origen"].fillna("Desconocido")

    st.markdown(
        """
| Problema | Decisión | Por qué |
|---|---|---|
| Duplicados | Eliminar | Un cliente contado dos veces infla KPIs |
| `edad` nula | Mediana | Robusta a extremos; pocos casos (<5 %) |
| `calificacion` nula | Mediana | Evita perder filas para el modelo |
| `canal_origen` nulo | "Desconocido" | No inventar un canal; se conserva la señal |
"""
    )
    st.success(
        f"Dataset limpio: {df.shape[0]} filas, "
        f"{int(df.isna().sum().sum())} nulos."
    )

    df["segmento"] = df.apply(_asignar_segmento, axis=1)
    df["recompra"] = (df[TARGET] == "Sí").astype(int)
    return df
