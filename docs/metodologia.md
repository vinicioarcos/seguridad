# Metodología propuesta

## Diseño

Estudio cuantitativo, longitudinal y comparado de Ecuador, Colombia, Perú y
Costa Rica durante 2014–2024. El alcance es descriptivo y correlacional
exploratorio; no se presenta como evaluación de impacto.

## Variables

| Dimensión | Indicador | Unidad | Fuente inicial |
|---|---|---|---|
| Seguridad | Homicidios intencionales | por 100.000 habitantes | WDI/UNODC |
| Crecimiento | Variación del PIB real | % anual | WDI/BM |
| Inversión | Formación bruta de capital fijo | % del PIB | WDI/BM |
| Capital externo | Entradas netas de IED | % del PIB | WDI/BM |

## Estrategia

1. Revisar definiciones y comparabilidad.
2. Describir cobertura, tendencia, dispersión y cambios interanuales.
3. Comparar Ecuador con los tres referentes.
4. Explorar correlaciones contemporáneas y rezagadas.
5. Estimar modelos de panel parsimoniosos con efectos de país, si la muestra lo
   permite.
6. Ejecutar análisis de sensibilidad a años atípicos y rezagos.

## Modelo exploratorio

\[
y_{it}=\alpha_i+\beta\,homicidios_{i,t-k}+\gamma t+\varepsilon_{it}
\]

donde \(y\) representa crecimiento, inversión o IED y \(k\in\{0,1\}\). El
coeficiente \(\beta\) mide asociación condicional, no un efecto causal.

## Riesgos metodológicos

- simultaneidad entre economía y crimen;
- variables omitidas (instituciones, narcotráfico, política fiscal, choques);
- poca muestra y rezagos de publicación;
- cambios de registro y subreporte;
- crisis de 2020 como observación extraordinaria.

Toda decisión definitiva debe quedar en la bitácora.
