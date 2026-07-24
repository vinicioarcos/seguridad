# Diccionario de datos

## Base procesada: `data/processed/indicators.csv`

| Variable | Tipo | Descripción |
|---|---|---|
| `country_code` | texto | Código ISO3 |
| `country` | texto | Nombre oficial devuelto por la fuente |
| `year` | entero | Año de observación |
| `indicator_code` | texto | Código de la serie |
| `indicator` | texto | Nombre de la serie |
| `dimension` | texto | Seguridad o desempeño económico |
| `value` | decimal/nulo | Valor original; no se imputa |
| `unit` | texto | Unidad aprobada en configuración |
| `source_id` | texto | Identificador en `sources.yaml` |
| `retrieved_at` | fecha-hora | Momento UTC de consulta |
| `is_missing` | booleano | Marca de valor faltante |
| `is_outlier` | booleano | Alerta; no implica eliminación |

Actualizar este archivo cuando se incorporen fuentes nacionales o nuevas
variables.
