# Bitácora de agentes y subagentes

| Fecha/hora | Agente | Tarea | Entradas | Salidas | Error/corrección | Validó | Estado |
|---|---|---|---|---|---|---|---|
| 2026-07-24 | coordinador | Crear scaffold | orden de tarea | estructura inicial | No aplica | Pendiente | En revisión |
| 2026-07-24 | coordinador | approve_design | config/project_config.yaml | config/approvals.yaml, config/project_config.yaml | No aplica | Vinicio Arcos | Aprobado |
| 2026-07-24 | source_agent | identify_sources | config/sources.yaml | config/sources.yaml, config/approvals.yaml | URLs de BCE y UNODC estaban obsoletas (redirigían) | Vinicio Arcos | Aprobado |

---

- **Fecha y hora:** 2026-07-24
- **Agente/subagente:** coordinador
- **Responsable humano:** Vinicio Arcos
- **Tarea e identificador:** approve_design (puerta de control humana, config/tasks.yaml)
- **Entradas y fuentes:** config/project_config.yaml (research_design: problema, pregunta, objetivo, países ECU/COL/PER/CRI, periodo 2014-2024, indicadores VC.IHR.PSRC.P5, NY.GDP.MKTP.KD.ZG, NE.GDI.FTOT.ZS, BX.KLT.DINV.WD.GD.ZS, hipótesis H1-H3, alcance interpretativo no causal)
- **Archivos creados/modificados:** config/approvals.yaml (approve_design → approved), config/project_config.yaml (research_design.status → approved)
- **Comandos/pruebas:** No aplica (revisión manual del diseño, sin ejecución de scripts)
- **Resultado:** Diseño de investigación aprobado sin cambios respecto a la propuesta inicial.
- **Errores detectados:** Ninguno.
- **Correcciones:** Ninguna.
- **Limitaciones:** Limitaciones ya declaradas en project_config.yaml (proxy de inseguridad limitado a homicidios, rezagos de publicación, potencia estadística limitada con 4 países/11 años, sin identificación causal).
- **Decisión humana:** aprobado
- **Commit:** pendiente

---

- **Fecha y hora:** 2026-07-24
- **Agente/subagente:** source_agent
- **Responsable humano:** Vinicio Arcos
- **Tarea e identificador:** identify_sources (puerta de control humana, config/tasks.yaml)
- **Entradas y fuentes:** config/sources.yaml (candidatas: world_bank_wdi, bce, inec, unodc, national_security_ecuador)
- **Archivos creados/modificados:** config/sources.yaml (world_bank_wdi → verified; URL de bce y unodc actualizadas por redirección), config/approvals.yaml (identify_sources → approved), docs/checklist_entrega.md
- **Comandos/pruebas:** `curl` en vivo a `https://api.worldbank.org/v2/country/ECU;COL;PER;CRI/indicator/{VC.IHR.PSRC.P5,NY.GDP.MKTP.KD.ZG,NE.GDI.FTOT.ZS,BX.KLT.DINV.WD.GD.ZS}?date=2014:2024`; verificación HTTP de bce.fin.ec, ecuadorencifras.gob.ec y dataunodc.un.org
- **Resultado:** world_bank_wdi confirmada como única fuente que alimenta scripts.download_data: los 4 indicadores responden con la etiqueta y unidad declaradas, cobertura ECU/COL/PER/CRI 2014-2024. BCE y UNODC tenían URLs obsoletas (redirigían de dominio); se actualizaron y quedan `candidate` sin variables mapeadas. national_security_ecuador queda `pending_identification` sin URL, no bloquea el pipeline principal.
- **Errores detectados:** URLs desactualizadas en bce (informacioneconomica/ → estadisticas-economicas/) y unodc (dataunodc.un.org → data.unodc.org).
- **Correcciones:** URLs actualizadas en config/sources.yaml a los dominios vigentes.
- **Limitaciones:** BCE, INEC y la fuente nacional de homicidios siguen sin variables/URL verificadas; si se requieren para robustez o discusión conceptual (homicidio vs. muerte violenta), deben verificarse en una iteración posterior antes de citarlas.
- **Decisión humana:** aprobado
- **Commit:** pendiente

## Formato de nueva entrada

- **Fecha y hora:**
- **Agente/subagente:**
- **Responsable humano:**
- **Tarea e identificador:**
- **Entradas y fuentes:**
- **Archivos creados/modificados:**
- **Comandos/pruebas:**
- **Resultado:**
- **Errores detectados:**
- **Correcciones:**
- **Limitaciones:**
- **Decisión humana:** aprobado / cambios / bloqueado
- **Commit:**

Las ejecuciones automáticas se registran además en
`outputs/logs/agent_runs.jsonl` (no versionado).
