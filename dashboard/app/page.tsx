"use client";

import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useMemo, useState } from "react";
import rawDataset from "../public/data/indicators.json";

type Datum = {
  countryCode: string;
  country: string;
  year: number;
  indicatorCode: string;
  indicator: string;
  dimension: string;
  value: number | null;
  unit: string;
  sourceId: string;
};

type Dataset = {
  meta: {
    status: string;
    generatedAt: string | null;
    title: string;
    period: number[];
    source: string;
    validationCoverage: number | null;
    interpretationScope: string;
  };
  countries: { code: string; name: string }[];
  indicators: { code: string; label: string; unit: string; dimension: string }[];
  kpis: { indicatorCode: string; label: string; value: number; unit: string; year: number }[];
  data: Datum[];
  interpretation: string;
};

const dataset = rawDataset as Dataset;
const palette: Record<string, string> = {
  ECU: "#f5a524",
  COL: "#42b7a5",
  PER: "#ef6f6c",
  CRI: "#78a6ff",
};

function formatValue(value: number | null | undefined) {
  return value == null ? "Sin dato" : new Intl.NumberFormat("es-EC", { maximumFractionDigits: 2 }).format(value);
}

export default function Home() {
  const [indicator, setIndicator] = useState(
    dataset.indicators[0]?.code ?? "VC.IHR.PSRC.P5",
  );
  const selected = dataset.indicators.find((item) => item.code === indicator);

  const chartData = useMemo(() => {
    const rows = dataset.data.filter((item) => item.indicatorCode === indicator);
    const years = [...new Set(rows.map((item) => item.year))].sort((a, b) => a - b);
    return years.map((year) => {
      const point: Record<string, number | string | null> = { year };
      for (const row of rows.filter((item) => item.year === year)) {
        point[row.countryCode] = row.value;
      }
      return point;
    });
  }, [indicator]);

  const latestRows = useMemo(() => {
    return dataset.countries.map((country) => {
      const rows = dataset.data
        .filter(
          (item) =>
            item.countryCode === country.code &&
            item.indicatorCode === indicator &&
            item.value != null,
        )
        .sort((a, b) => b.year - a.year);
      return { country: country.name, code: country.code, datum: rows[0] };
    });
  }, [indicator]);

  const ready = dataset.meta.status === "human_validated" && dataset.data.length > 0;

  return (
    <main>
      <header className="hero">
        <nav>
          <span className="brand">CONTEXTO / ECONOMÍA</span>
          <div className="navLinks">
            <a href="#datos">Datos</a>
            <a href="#metodo">Método</a>
            <a href={process.env.NEXT_PUBLIC_REPOSITORY_URL || "#"}>GitHub</a>
          </div>
        </nav>
        <div className="heroGrid">
          <div>
            <span className="eyebrow">Ecuador · Colombia · Perú · Costa Rica</span>
            <h1>Seguridad y<br />desempeño económico</h1>
            <p className="lead">
              Una lectura comparada de violencia, crecimiento, inversión e IED
              durante 2014–2024.
            </p>
          </div>
          <aside className="questionCard">
            <span>Pregunta central</span>
            <p>
              ¿Cómo se relaciona la evolución de la inseguridad con el desempeño
              económico de Ecuador frente a tres economías latinoamericanas?
            </p>
          </aside>
        </div>
      </header>

      <section className={`status ${ready ? "ready" : "pending"}`}>
        <strong>{ready ? "Datos validados" : "Datos pendientes de validación humana"}</strong>
        <span>
          {ready
            ? `Actualizado: ${dataset.meta.generatedAt}`
            : "El dashboard no mostrará cifras hasta completar las puertas de calidad."}
        </span>
      </section>

      <section className="content" id="datos">
        <div className="sectionHeader">
          <div>
            <span className="eyebrow dark">Indicadores</span>
            <h2>La evidencia, antes que el relato</h2>
          </div>
          <label>
            Indicador
            <select value={indicator} onChange={(event) => setIndicator(event.target.value)}>
              {dataset.indicators.map((item) => (
                <option key={item.code} value={item.code}>{item.label}</option>
              ))}
            </select>
          </label>
        </div>

        {dataset.kpis.length > 0 && (
          <div className="kpiGrid">
            {dataset.kpis.map((kpi) => (
              <article className="kpi" key={kpi.indicatorCode}>
                <span>{kpi.label} · Ecuador</span>
                <strong>{formatValue(kpi.value)}</strong>
                <small>{kpi.unit} · {kpi.year}</small>
              </article>
            ))}
          </div>
        )}

        <div className="panel">
          <div className="panelTitle">
            <div>
              <h3>{selected?.label ?? "Indicador"}</h3>
              <p>{selected?.unit ?? ""}</p>
            </div>
            <span className="source">Fuente: {dataset.meta.source}</span>
          </div>
          {ready ? (
            <div className="chart">
              <ResponsiveContainer width="100%" height={390}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#253349" />
                  <XAxis dataKey="year" stroke="#9bacbf" />
                  <YAxis stroke="#9bacbf" />
                  <Tooltip
                    contentStyle={{ background: "#111c2d", border: "1px solid #314158" }}
                    formatter={(value) => formatValue(Number(value))}
                  />
                  <Legend />
                  {dataset.countries.map((country) => (
                    <Line
                      key={country.code}
                      type="monotone"
                      dataKey={country.code}
                      name={country.name}
                      stroke={palette[country.code]}
                      strokeWidth={country.code === "ECU" ? 3 : 2}
                      connectNulls={false}
                    />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="empty">
              <span>∅</span>
              <h3>No hay cifras publicables todavía</h3>
              <p>Ejecute el pipeline, revise faltantes y apruebe la validación.</p>
            </div>
          )}
        </div>

        <div className="analysisGrid">
          <article className="interpretation">
            <span className="eyebrow dark">Lectura económica</span>
            <h3>Interpretación prudente</h3>
            <p>{dataset.interpretation}</p>
          </article>
          <article className="interpretation accent">
            <span className="eyebrow">Advertencia</span>
            <h3>Asociación ≠ causalidad</h3>
            <p>
              El crimen y la economía pueden afectarse mutuamente y responder a
              instituciones, choques externos o políticas omitidas.
            </p>
          </article>
        </div>

        <div className="panel tablePanel">
          <div className="panelTitle"><h3>Última observación disponible</h3></div>
          <div className="tableWrap">
            <table>
              <thead>
                <tr><th>País</th><th>Año</th><th>Valor</th><th>Unidad</th></tr>
              </thead>
              <tbody>
                {latestRows.map((row) => (
                  <tr key={row.code}>
                    <td>{row.country}</td>
                    <td>{row.datum?.year ?? "—"}</td>
                    <td>{formatValue(row.datum?.value)}</td>
                    <td>{row.datum?.unit ?? selected?.unit ?? "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section className="method" id="metodo">
        <span className="eyebrow">Método</span>
        <h2>Panel comparado, trazabilidad completa</h2>
        <div className="steps">
          {["Fuentes oficiales", "Validación", "Análisis exploratorio", "Auditoría humana"].map(
            (step, index) => (
              <div key={step}><b>0{index + 1}</b><span>{step}</span></div>
            ),
          )}
        </div>
        <p>
          Los modelos incorporan efectos de país y tendencia temporal cuando la
          cobertura lo permite. Sus coeficientes se reportan como asociaciones
          exploratorias.
        </p>
      </section>

      <footer>
        <span>Proyecto académico reproducible · 2026</span>
        <div>
          <a href={process.env.NEXT_PUBLIC_REPORT_URL || "#"}>Descargar informe</a>
          <a href={process.env.NEXT_PUBLIC_REPOSITORY_URL || "#"}>Ver código</a>
        </div>
      </footer>
    </main>
  );
}
