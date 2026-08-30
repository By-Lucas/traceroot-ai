"use client";

import { useState } from "react";
import { BarChart3, CheckCircle2, FlaskConical, XCircle } from "lucide-react";
import { Shell } from "@/components/shell";
import { PageHeader } from "@/components/page-header";
import { Status } from "@/components/status";
import { api } from "@/lib/api";

type Evaluation = {
  id: string;
  status: string;
  duration_ms: number;
  results: {
    mode?: string;
    error?: string;
    metrics?: {
      cases: number;
      verified_rate: number;
      reproduction_success_rate: number;
      evidence_precision: number;
    };
    cases?: Array<{
      slug: string;
      title: string;
      status: string;
      evidence_found: boolean;
      reproduced: boolean;
      duration_ms: number;
    }>;
  };
};

export default function Evaluations() {
  const [run, setRun] = useState<Evaluation | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  async function execute() {
    setBusy(true);
    setError("");
    try {
      const started = await api<{ id: string }>("/evaluations", {
        method: "POST",
      });
      setRun(await api<Evaluation>(`/evaluations/${started.id}`));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Evaluation failed");
    } finally {
      setBusy(false);
    }
  }
  const metrics = run?.results.metrics;
  return (
    <Shell>
      <PageHeader
        eyebrow="Measured reliability"
        title="Evaluation laboratory"
        description="Executes the checked-in cases inside the same allowlisted repository sandbox used by investigations."
        action={
          <button className="btn btn-primary" disabled={busy} onClick={execute}>
            <FlaskConical size={16} />
            {busy ? "Running cases…" : "Run evaluation"}
          </button>
        }
      />
      {error && (
        <div
          role="alert"
          className="mb-5 rounded-lg border border-[#5d3038] bg-[#261216] p-4 text-sm text-[#f3828d]"
        >
          {error}
        </div>
      )}
      <div className="grid gap-5 lg:grid-cols-3">
        <section className="panel p-6 lg:col-span-2">
          <div className="label">Executed sandbox results</div>
          {!run ? (
            <p className="mt-5 text-sm text-[#808ba0]">
              No hardcoded score is displayed. Run the suite to measure the
              current case files.
            </p>
          ) : run.status === "failed" ? (
            <p className="mt-5 text-sm text-[#f3828d]">
              {run.results.error ?? "Evaluation failed"}
            </p>
          ) : (
            <div className="mt-6 grid grid-cols-3 gap-4">
              {[
                ["Verified", metrics?.verified_rate],
                ["Reproduced", metrics?.reproduction_success_rate],
                ["Evidence found", metrics?.evidence_precision],
              ].map(([label, value]) => (
                <div
                  className="rounded-xl border border-[#293144] bg-[#0c1017] p-5"
                  key={String(label)}
                >
                  <span className="text-sm text-[#8994a9]">{label}</span>
                  <div className="metric mt-3 text-3xl font-semibold">
                    {Math.round(Number(value) * 100)}%
                  </div>
                </div>
              ))}
            </div>
          )}
          {run && (
            <p className="mt-5 text-xs text-[#69758b]">
              {metrics?.cases ?? 0} cases executed in{" "}
              {(run.duration_ms / 1000).toFixed(2)}s. Mode: {run.results.mode}.
            </p>
          )}
        </section>
        <section className="panel p-6">
          <BarChart3 color="#91a5ff" />
          <h2 className="mt-4 text-lg font-semibold">
            Real executions, zero LLM tokens
          </h2>
          <p className="mt-2 text-sm leading-6 text-[#808ba0]">
            Each result comes from reading its declared evidence file and
            running its reproduction script.
          </p>
        </section>
      </div>
      <section className="panel mt-5 p-6">
        <div className="label">Case matrix</div>
        {!run?.results.cases ? (
          <p className="mt-4 text-sm text-[#808ba0]">
            Run the evaluation to populate case-level results.
          </p>
        ) : (
          <div className="mt-4 grid gap-2 md:grid-cols-2">
            {run.results.cases.map((item) => (
              <div
                className="flex items-center gap-3 rounded-lg border border-[#202837] p-3 text-sm"
                key={item.slug}
              >
                {item.status === "VERIFIED" ? (
                  <CheckCircle2 size={15} color="#55d5a1" />
                ) : (
                  <XCircle size={15} color="#f27782" />
                )}
                <div className="min-w-0 flex-1">
                  <div className="truncate">{item.title}</div>
                  <div className="mt-1 text-[10px] text-[#657188]">
                    reproduced={String(item.reproduced)} · evidence=
                    {String(item.evidence_found)} · {item.duration_ms}ms
                  </div>
                </div>
                <Status value={item.status} />
              </div>
            ))}
          </div>
        )}
      </section>
    </Shell>
  );
}
