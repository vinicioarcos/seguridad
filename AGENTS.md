# Protocolo operativo para agentes

## Misión

Construir un análisis económico reproducible del contexto ecuatoriano y global
sin inventar datos, referencias, resultados ni validaciones.

## Fuente de verdad

1. `config/project_config.yaml`: alcance aprobado.
2. `config/sources.yaml`: fuentes autorizadas.
3. `config/tasks.yaml`: dependencias y entregables.
4. `config/agents.yaml`: roles y límites.
5. `docs/bitacora_agentes.md`: evidencia y validación humana.

Si dos archivos se contradicen, detenerse y solicitar decisión humana.

## Reglas no negociables

- No cambiar el problema, países, periodo o método sin registrar la decisión.
- No usar una cifra si no puede trazarse hasta su fuente y fecha de consulta.
- No convertir datos faltantes en cero.
- No imputar, eliminar atípicos o transformar unidades silenciosamente.
- No afirmar causalidad a partir de correlaciones o regresiones descriptivas.
- No citar documentos que no hayan sido localizados y verificados.
- No colocar claves en código, prompts, bitácoras o commits.
- No publicar una salida hasta que el agente auditor y un humano la aprueben.
- Mantener separados `data/raw/` (inmutable) y `data/processed/` (reproducible).

## Ciclo obligatorio de una tarea

1. Leer configuración y contrato del agente.
2. Declarar entradas, salida esperada y criterio de aceptación.
3. Ejecutar una tarea acotada.
4. Validar el resultado.
5. Registrar archivos, errores y correcciones.
6. Solicitar la puerta de control humana indicada en `tasks.yaml`.
7. Hacer un commit descriptivo.

## Trabajo con subagentes

El coordinador puede delegar solo tareas independientes y acotadas. Cada
subagente devuelve: fuentes consultadas, archivos creados/modificados,
supuestos, pruebas realizadas, limitaciones y estado (`aprobable` o
`bloqueado`). El coordinador integra; no copia respuestas sin revisión.

## Definición de terminado

Una tarea está terminada cuando existe el archivo de salida, pasan sus pruebas,
la bitácora conserva trazabilidad y el responsable humano registra su
validación. “La IA dijo que funciona” no es una prueba.
