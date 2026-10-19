"""Entrenamiento y predicciones del modelo de recompra."""

from typing import NamedTuple

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class ResultadoModelo(NamedTuple):
    exactitud: float
    auc: float
    linea_base: float
    coeficientes: pd.Series
    probabilidades: pd.Series


def entrenar(df: pd.DataFrame) -> ResultadoModelo:
    numericas = [
        "edad",
        "num_compras",
        "ticket_promedio",
        "dias_ultima_compra",
        "calificacion",
    ]
    categoricas = [
        "canal_origen",
        "uso_promocion",
        "familia_olfativa",
        "genero_preferido",
    ]
    variables = pd.get_dummies(
        df[numericas + categoricas],
        columns=categoricas,
        drop_first=True,
    ).astype(float)
    objetivo = df["recompra"]
    x_train, x_test, y_train, y_test = train_test_split(
        variables,
        objetivo,
        test_size=0.25,
        random_state=42,
        stratify=objetivo,
    )
    escalador = StandardScaler().fit(x_train)
    modelo = LogisticRegression(max_iter=1000).fit(
        escalador.transform(x_train), y_train
    )
    probabilidades_test = modelo.predict_proba(escalador.transform(x_test))[:, 1]

    return ResultadoModelo(
        exactitud=float(accuracy_score(y_test, probabilidades_test > 0.5)),
        auc=float(roc_auc_score(y_test, probabilidades_test)),
        linea_base=float(1 - y_test.mean()),
        coeficientes=pd.Series(modelo.coef_[0], index=variables.columns).sort_values(),
        probabilidades=pd.Series(
            modelo.predict_proba(escalador.transform(variables))[:, 1],
            index=df.index,
            name="prob_recompra",
        ),
    )
