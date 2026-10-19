# Análisis de recompra de clientes de perfumes

Aplicación interactiva creada con Streamlit para explorar clientes, limpiar datos,
describir segmentos, estimar la probabilidad de recompra y proponer acciones de
marketing. El dataset incluido es sintético y no contiene datos personales.

La pregunta que guía el análisis es:

> ¿Qué clientes tienen mayor probabilidad de volver a comprar y qué promoción
> le damos a cada tipo?

## Contenido

- [Estructura del proyecto](#estructura-del-proyecto)
- [Tecnologías y librerías](#tecnologías-y-librerías)
- [Instalación local](#instalación-local)
- [Ejecución](#ejecución)
- [Cómo funciona la aplicación](#cómo-funciona-la-aplicación)
- [Datos de entrada](#datos-de-entrada)
- [Modelo predictivo](#modelo-predictivo)
- [Despliegue en Streamlit Community Cloud](#despliegue-en-streamlit-community-cloud)
- [Solución de problemas](#solución-de-problemas)
- [Privacidad y limitaciones](#privacidad-y-limitaciones)

## Estructura del proyecto

```text
F05_Actividad Streamlit/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── clientes_perfumes.csv
├── tabs/
│   ├── __init__.py
│   ├── entender.py
│   ├── limpiar.py
│   ├── descriptiva.py
│   ├── predictiva.py
│   ├── prescriptiva.py
│   └── decisiones.py
└── stream_train/
    ├── __init__.py
    └── modelo.py
```

`app.py` es el punto de entrada: lee el CSV desde `data/`, crea las seis pestañas
y pasa los datos a cada módulo de `tabs/`. El paquete `stream_train/` debe
contener la función que entrena el modelo.

> **Requisito pendiente para ejecutar y desplegar:** en la copia del proyecto
> documentada actualmente, `tabs/predictiva.py` importa
> `entrenar` desde `stream_train.modelo`, pero la carpeta `stream_train/` no está
> presente. Además, `.gitignore` contiene una regla que excluye esa carpeta.
> Sin el módulo `stream_train/modelo.py` y su `__init__.py` versionados en el
> repositorio, la aplicación falla al importar la pestaña predictiva. Antes de
> ejecutar o desplegar, agrega esos archivos al proyecto y asegúrate de que
> Git los incluya (retira o ajusta la regla correspondiente en `.gitignore`).

## Tecnologías y librerías

Las dependencias directas se declaran en [`requirements.txt`](requirements.txt):

| Librería | Uso |
|---|---|
| `streamlit` | Interfaz web, pestañas, métricas, tablas y gráficos. |
| `pandas` | Lectura, limpieza, transformación y análisis tabular. |
| `scikit-learn` | Escalado de variables, partición de datos y regresión logística. |

La aplicación también usa módulos de la biblioteca estándar de Python:
`pathlib.Path` para construir una ruta al CSV independiente del directorio actual.

## Instalación local

Se recomienda Python 3.11 o posterior. Ejecuta los comandos desde la carpeta raíz
del proyecto.

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si PowerShell bloquea la activación del entorno, puedes llamar directamente a
sus ejecutables sin cambiar la política de ejecución:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### macOS o Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

El entorno virtual `.venv/` es local: no se debe subir al repositorio. Para
compartir la aplicación, se comparten el código, los datos permitidos y
`requirements.txt`; cada entorno instala sus propias dependencias.

## Ejecución

Desde la raíz del proyecto, activa el entorno virtual y ejecuta:

```bash
streamlit run app.py
```

En Windows PowerShell también puedes usar el ejecutable del entorno:

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

Streamlit mostrará una dirección local (normalmente
`http://localhost:8501`) y abrirá la aplicación en el navegador. Para detener el
servidor, vuelve a la terminal y presiona `Ctrl+C`.

La app busca el archivo de datos en una ruta relativa al propio `app.py`:
`data/clientes_perfumes.csv`. Por eso conviene iniciar Streamlit desde la raíz
del proyecto y conservar la estructura indicada.

## Cómo funciona la aplicación

### 1. Entender

[`tabs/entender.py`](tabs/entender.py) muestra el número de filas y variables, la
tasa inicial de recompra, una vista previa del CSV y el tipo, cardinalidad y un
ejemplo de cada columna.

### 2. Limpiar y segmentar

[`tabs/limpiar.py`](tabs/limpiar.py) trabaja sobre una copia del DataFrame:

1. Cuenta valores nulos y filas duplicadas.
2. Elimina filas completamente duplicadas.
3. Imputa los valores faltantes de `edad` y `calificacion` con la mediana de
   cada columna.
4. Sustituye el valor nulo de `canal_origen` por `"Desconocido"`.
5. Asigna un segmento de cliente según el historial y los días desde la última
   compra:

| Segmento | Regla |
|---|---|
| `Leal activo` | 4 o más compras y 90 días o menos desde la última compra. |
| `Leal dormido` | 4 o más compras, pero más de 90 días desde la última compra. |
| `Nuevo activo` | Menos de 4 compras y 90 días o menos desde la última compra. |
| `En riesgo` | Menos de 4 compras y más de 90 días desde la última compra. |

6. Convierte `recompra_ultima_campana` a una variable binaria llamada
   `recompra`: 1 para `"Sí"` y 0 para cualquier otro valor.

### 3. Describir

[`tabs/descriptiva.py`](tabs/descriptiva.py) presenta la tasa de recompra, el
ticket promedio, la media de compras por cliente y la mediana de días desde la
última compra. También compara clientes, tasa de recompra y ticket por
segmento, y permite explorar la tasa por canal, uso de promociones, familia
olfativa o género preferido.

### 4. Predecir

[`tabs/predictiva.py`](tabs/predictiva.py) muestra exactitud, AUC, una línea base
de clasificación y los coeficientes del modelo. Además, agrega a los datos la
probabilidad estimada (`prob_recompra`) y una categoría (`nivel`):

- Baja: probabilidad de 0 a 0.3.
- Media: mayor que 0.3 y hasta 0.6.
- Alta: mayor que 0.6 y hasta 1.

Esta pestaña depende de `stream_train.modelo.entrenar`, cuyo módulo debe estar
presente para que la aplicación funcione.

### 5. Prescribir

[`tabs/prescriptiva.py`](tabs/prescriptiva.py) resume por segmento la cantidad
de clientes, la probabilidad media y la recompra observada, y presenta la
acción promocional recomendada y su razón.

### 6. Decidir

[`tabs/decisiones.py`](tabs/decisiones.py) permite seleccionar un segmento y
consultar su número de clientes, probabilidad media estimada, canal principal,
acción y mensaje sugeridos. También presenta límites y recomendaciones para
validar el análisis con datos reales.

## Datos de entrada

El archivo esperado es `data/clientes_perfumes.csv`. La aplicación requiere
estas columnas:

| Columna | Descripción / uso |
|---|---|
| `id_cliente` | Identificador del cliente; no se utiliza como predictor. |
| `edad` | Edad; los valores faltantes se imputan con la mediana. |
| `canal_origen` | Canal de adquisición; los faltantes pasan a `"Desconocido"`. |
| `genero_preferido` | Categoría utilizada en el análisis y el modelo. |
| `familia_olfativa` | Categoría utilizada en el análisis y el modelo. |
| `num_compras` | Historial de compras; se utiliza para segmentar y modelar. |
| `ticket_promedio` | Importe medio de compra; predictor y métrica descriptiva. |
| `dias_ultima_compra` | Recencia; se utiliza para segmentar y modelar. |
| `uso_promocion` | Uso de promociones; análisis y predictor. |
| `calificacion` | Calificación del cliente; los faltantes se imputan con la mediana. |
| `recompra_ultima_campana` | Objetivo; se espera `"Sí"` o `"No"`. |

El archivo debe tener encabezados en la primera fila y ser legible por
`pandas.read_csv`. Si el dataset cambia, conserva esos nombres o actualiza los
módulos que dependen de ellos. En especial, el valor afirmativo del objetivo
debe coincidir con `"Sí"` para que la conversión a 0/1 sea correcta.

## Modelo predictivo

La pestaña predictiva espera que `stream_train/modelo.py` implemente
`entrenar(df)` y devuelva un resultado con estos atributos:

- `exactitud`: exactitud medida en el conjunto de prueba.
- `auc`: área bajo la curva ROC en el conjunto de prueba.
- `linea_base`: proporción de la clase negativa en el conjunto de prueba.
- `coeficientes`: `pandas.Series` de coeficientes, indexada por nombre de
  predictor.
- `probabilidades`: `pandas.Series` de probabilidades para las filas recibidas,
  indexada como el DataFrame de entrada.

El flujo de la aplicación presupone regresión logística sobre las variables
numéricas (`edad`, `num_compras`, `ticket_promedio`, `dias_ultima_compra`,
`calificacion`) y categóricas (`canal_origen`, `uso_promocion`,
`familia_olfativa`, `genero_preferido`). Debe codificar las categorías,
escalar usando los datos de entrenamiento y evaluar el modelo en datos no
usados para ajustarlo. No se debe usar `id_cliente` como predictor.

Las probabilidades y coeficientes reflejan asociaciones del dataset; no
demuestran causalidad ni garantizan que una promoción produzca una recompra.
Con datos reales, conviene validar el modelo fuera de muestra y probar las
acciones mediante experimentos controlados.

## Despliegue en Streamlit Community Cloud

### 1. Preparar el repositorio

1. Confirma que el proyecto está completo y que funciona localmente.
2. Añade al repositorio `app.py`, `requirements.txt`, `data/` y `tabs/`.
3. Incluye también `stream_train/__init__.py` y
   `stream_train/modelo.py`. Comprueba que `.gitignore` no excluya
   `stream_train/`.
4. No subas `.venv/`, `rp_env/`, credenciales ni archivos con datos personales.
5. Confirma los cambios y súbelos a GitHub en una rama accesible para
   Streamlit Community Cloud.

### 2. Crear la aplicación

1. Inicia sesión en [Streamlit Community Cloud](https://share.streamlit.io/).
2. Selecciona **Create app** y conecta la cuenta o repositorio de GitHub.
3. Elige el repositorio, la rama que contiene el código y el archivo principal
   `app.py`.
4. Si el panel solicita una versión de Python, elige una compatible con las
   versiones de `streamlit`, `pandas` y `scikit-learn` declaradas en
   `requirements.txt`.
5. Inicia el despliegue y revisa los registros si ocurre un error.

Community Cloud instala las dependencias desde `requirements.txt` y ejecuta
`app.py`. El dataset debe estar dentro del repositorio en
`data/clientes_perfumes.csv`, y la ruta se resuelve en relación con `app.py`.
No configures secretos si la app no utiliza servicios externos que los
requieran.

### 3. Actualizaciones

Para publicar cambios, súbelos a la rama configurada en Streamlit. El servicio
detectará los cambios y volverá a desplegar la aplicación. Si se modifica una
dependencia, actualiza `requirements.txt` y vuelve a desplegar.

## Solución de problemas

| Síntoma | Causa posible y solución |
|---|---|
| `ModuleNotFoundError: No module named 'stream_train'` | Falta `stream_train/modelo.py` o no está incluido en Git. Crea/versiona el módulo requerido y revisa `.gitignore`. |
| `FileNotFoundError` para el CSV | Verifica que exista `data/clientes_perfumes.csv`, que se haya subido al repositorio y que el nombre coincida exactamente. |
| `ModuleNotFoundError` para `streamlit`, `pandas` o `sklearn` | Activa el entorno virtual e instala las dependencias con `pip install -r requirements.txt`. |
| `KeyError` por una columna | El CSV no tiene el encabezado esperado. Comprueba que los nombres coincidan con la sección de datos de entrada. |
| La tasa de recompra aparece como 0 % | Verifica la codificación y el valor de la columna objetivo: el código reconoce `"Sí"` exactamente. |
| No abre la dirección local | Comprueba la terminal donde se ejecuta Streamlit, que el servidor siga activo y que el puerto indicado no esté bloqueado. |
| Falla el despliegue después de cambiar dependencias | Revisa los registros de Community Cloud y confirma que las versiones del entorno sean compatibles con `requirements.txt`. |

## Privacidad y limitaciones

- El CSV suministrado es sintético. Antes de usar datos reales, minimiza los
  datos recopilados y utiliza identificadores anónimos.
- No publiques nombres, teléfonos, correos, credenciales ni otros datos
  personales en el repositorio.
- La imputación de nulos y la eliminación de duplicados se realizan en memoria;
  no modifican el CSV original.
- La segmentación usa umbrales fijos (4 compras y 90 días); revísalos según las
  reglas del negocio y la estacionalidad.
- Las métricas predictivas dependen del dataset y de la partición de prueba.
  No son una garantía de desempeño futuro.
- Valida las promociones propuestas con una prueba A/B antes de escalarlas.
