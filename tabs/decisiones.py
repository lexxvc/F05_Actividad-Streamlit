"""Decisiones y mensajes recomendados por segmento."""

import pandas as pd
import streamlit as st

from tabs.prescriptiva import ACCIONES

MENSAJES = {
    "Leal activo": (
        "«Eres de nuestros clientes favoritos: prueba antes que nadie "
        "el nuevo lanzamiento.»"
    ),
    "Leal dormido": (
        "«Te extrañamos 🧴 Tu aroma favorito tiene 15 % de descuento esta semana.»"
    ),
    "Nuevo activo": (
        "«¿Te gustó tu perfume? En tu próxima compra te regalamos una muestra.»"
    ),
    "En riesgo": "«Vuelve a descubrir tu aroma: 2x1 en decants solo por 72 horas.»",
}


def render(df: pd.DataFrame) -> None:
    st.header("6. Toma de decisiones")
    segmento = st.selectbox("Elige un segmento", list(ACCIONES))
    clientes = df[df["segmento"] == segmento]
    c1, c2, c3 = st.columns(3)
    c1.metric("Clientes", len(clientes))
    c2.metric("Prob. media de recompra", f"{clientes['prob_recompra'].mean():.0%}")
    c3.metric("Canal principal", clientes["canal_origen"].mode()[0])

    st.markdown(f"**Acción:** {ACCIONES[segmento][0]}")
    st.markdown(f"**Mensaje:** {MENSAJES[segmento]}")
    st.markdown(
        f"**Justificación:** {ACCIONES[segmento][1]}. "
        f"Recompra real del segmento: {clientes['recompra'].mean():.0%} "
        f"vs {df['recompra'].mean():.0%} general."
    )
    with st.expander("Límites y siguiente paso con datos reales"):
        st.markdown(
            """
- **Calidad:** datos sintéticos; con ventas reales validar fechas y duplicados por teléfono.
- **Sesgo:** clientes de WhatsApp sobrerrepresentados; balancear canales.
- **Privacidad:** usar ID anónimo, nunca nombre/teléfono en el repositorio.
- **Validar:** prueba A/B de la promoción antes de escalarla.
"""
        )
