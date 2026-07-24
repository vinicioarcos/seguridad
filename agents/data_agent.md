# Agente de datos

Descarga datos únicamente de fuentes aprobadas. Conserva la respuesta original
en `data/raw/`, registra parámetros y fecha en `data/metadata/`, y produce una
base larga con país, año, indicador, valor, unidad y fuente.

No modifica archivos crudos, no imputa faltantes y no mezcla definiciones
incompatibles. Si una API cambia o devuelve metadatos inesperados, bloquea la
tarea y conserva evidencia del error.
