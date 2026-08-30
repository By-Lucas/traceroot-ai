"use client";
import { useEffect, useState } from "react";
import {
  Background,
  Controls,
  Handle,
  Position,
  ReactFlow,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import {
  AlertCircle,
  Check,
  ChevronRight,
  Clock3,
  Code2,
  FileSearch,
  FlaskConical,
  ShieldCheck,
  Terminal,
} from "lucide-react";
import { Shell } from "@/components/shell";
import { PageHeader } from "@/components/page-header";
import { Status } from "@/components/status";
import { api } from "@/lib/api";
type Investigation = {
  id: string;
  status: string;
  confidence: number;
  root_cause: string | null;
  duration_ms: number;
  hypotheses: Array<{
    id: string;
    claim: string;
    confidence: number;
    reason: string;
  }>;
  evidence: Array<{
    id: string;
    type: string;
    location: string;
    content_summary: string;
    supports: string[];
    confidence: number;
    content_hash: string;
  }>;
  report: Record<string, unknown>;
};
const demo: Investigation = {
  id: "demo",
  status: "VERIFIED",
  confidence: 0.96,
  root_cause: "A null handling regression calls strip on an absent promo code",
  duration_ms: 38420,
  hypotheses: [
    {
      id: "H1",
      claim: "Missing null guard in discount normalization",
      confidence: 0.72,
      reason: "Runtime and code path align.",
    },
    {
      id: "H2",
      claim: "Pricing database timeout",
      confidence: 0.28,
      reason: "Retained as an infrastructure alternative.",
    },
  ],
  evidence: [
    {
      id: "e1",
      type: "runtime",
      location: "incident/runtime",
      content_summary:
        "AttributeError: 'NoneType' object has no attribute 'strip'",
      supports: ["H1"],
      confidence: 0.91,
      content_hash: "a51c…9fe2",
    },
    {
      id: "e2",
      type: "source_code",
      location: "checkout_service.py:13",
      content_summary: "return promo_code.strip().upper() — no None guard",
      supports: ["H1"],
      confidence: 0.96,
      content_hash: "ce72…bd30",
    },
  ],
  report: {
    reproduction: {
      command: "python reproduce.py",
      exit_code: 0,
      stdout: "TRACEROOT_REPRODUCED: None promo reaches strip",
    },
    recommended_fix:
      "Normalize a missing promo code before string operations and add a regression test.",
    regression_verification: "REPRODUCTION_CONFIRMED",
    human_approval_requirement: "Required before production deployment.",
  },
};
function GraphNode({ data }: { data: { label: string; kind: string } }) {
  return (
    <div className="min-w-32 rounded-lg border border-[#34415b] bg-[#111722] px-3 py-2 shadow-xl">
      <Handle type="target" position={Position.Left} />
      <div className="text-[9px] uppercase tracking-widest text-[#71809b]">
        {data.kind}
      </div>
      <div className="mt-1 text-xs font-medium">{data.label}</div>
      <Handle type="source" position={Position.Right} />
    </div>
  );
}
const edges = [
  { id: "1", source: "i", target: "h", label: "suggests" },
  { id: "2", source: "e", target: "h", label: "supports" },
  { id: "3", source: "h", target: "r", label: "tested by" },
  { id: "4", source: "r", target: "c", label: "verified by", animated: true },
];
export function InvestigationConsole({ id }: { id: string }) {
  const explicitDemo = id.startsWith("demo");
  const [data, setData] = useState<Investigation | null>(
    explicitDemo ? demo : null,
  );
  const [loading, setLoading] = useState(!explicitDemo);
  const [error, setError] = useState("");
  useEffect(() => {
    if (!explicitDemo) {
      api<Investigation>(`/investigations/${id}`)
        .then(setData)
        .catch((reason) =>
          setError(
            reason instanceof Error
              ? reason.message
              : "Could not load investigation",
          ),
        )
        .finally(() => setLoading(false));
    }
  }, [explicitDemo, id]);

  if (loading)
    return (
      <Shell>
        <PageHeader
          eyebrow={`Investigation / ${id.slice(0, 8)}`}
          title="Assembling evidence…"
          description="Loading the persisted investigation record."
        />
      </Shell>
    );
  if (error || !data)
    return (
      <Shell>
        <PageHeader
          eyebrow={`Investigation / ${id.slice(0, 8)}`}
          title="Investigation unavailable"
          description="No demo fallback was applied."
        />
        <div role="alert" className="panel p-6 text-sm text-[#f3828d]">
          {error || "Investigation not found"}
        </div>
      </Shell>
    );

  const nodes = [
    {
      id: "i",
      position: { x: 0, y: 80 },
      data: {
        label: String(
          (data.report.incident as { title?: string } | undefined)?.title ??
            data.id,
        ).slice(0, 24),
        kind: "incident",
      },
      type: "trace",
    },
    {
      id: "h",
      position: { x: 210, y: 20 },
      data: {
        label: (data.hypotheses[0]?.claim ?? "No hypothesis").slice(0, 24),
        kind: "hypothesis",
      },
      type: "trace",
    },
    {
      id: "e",
      position: { x: 210, y: 145 },
      data: {
        label: (data.evidence[0]?.location ?? "No evidence").slice(0, 24),
        kind: "evidence",
      },
      type: "trace",
    },
    {
      id: "r",
      position: { x: 430, y: 80 },
      data: {
        label:
          data.report.regression_verification === "REPRODUCTION_CONFIRMED"
            ? "Reproduced"
            : "Not reproduced",
        kind: "test",
      },
      type: "trace",
    },
    {
      id: "c",
      position: { x: 640, y: 80 },
      data: {
        label: data.status === "VERIFIED" ? "Verified cause" : data.status,
        kind: "root cause",
      },
      type: "trace",
    },
  ];
  const repro = data.report.reproduction as
    | { command?: string; exit_code?: number; stdout?: string }
    | undefined;
  return (
    <Shell>
      <PageHeader
        eyebrow={`Investigation / ${id.slice(0, 8)}`}
        title={explicitDemo ? "Example root cause review" : "Root cause review"}
        description="A causal record of what the agents observed, executed and independently verified."
        action={<Status value={data.status} />}
      />
      <div className="panel mb-6 overflow-x-auto p-4">
        <div className="flex min-w-[680px] items-center">
          {[
            "Intake",
            "Triage",
            "Evidence",
            "Reproduction",
            "Verification",
            "Final Report",
          ].map((stage, i) => (
            <div className="flex flex-1 items-center" key={stage}>
              <span
                className={`grid h-7 w-7 shrink-0 place-items-center rounded-full border ${i < 6 ? "border-[#3a6c5a] bg-[#143126] text-[#60d3a3]" : "border-[#384256]"}`}
              >
                {i < 6 ? <Check size={13} /> : i + 1}
              </span>
              <span className="ml-2 text-xs text-[#a4adbe]">{stage}</span>
              {i < 5 && (
                <ChevronRight className="ml-auto" size={14} color="#394255" />
              )}
            </div>
          ))}
        </div>
      </div>
      <section className="grid gap-6 xl:grid-cols-[1.25fr_.75fr]">
        <div className="space-y-6">
          <div className="panel p-5">
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="label">Accepted root cause</div>
                <h2 className="mt-3 text-xl font-semibold leading-8">
                  {data.root_cause ??
                    "Evidence is insufficient for a root-cause claim"}
                </h2>
              </div>
              <div className="metric text-3xl font-semibold text-[#61d3a3]">
                {Math.round(data.confidence * 100)}%
              </div>
            </div>
            <div className="mt-5 grid grid-cols-3 gap-3 border-t border-[#202735] pt-4 text-xs">
              <span className="text-[#7f899c]">
                <Clock3 className="mr-1 inline" size={13} />
                {(data.duration_ms / 1000).toFixed(1)}s
              </span>
              <span className="text-[#7f899c]">
                <FileSearch className="mr-1 inline" size={13} />
                {data.evidence.length} evidence items
              </span>
              <span className="text-[#7f899c]">
                <ShieldCheck className="mr-1 inline" size={13} />
                human approval
              </span>
            </div>
          </div>
          <div className="panel overflow-hidden">
            <div className="border-b border-[#202735] p-5">
              <div className="label">Causal evidence graph</div>
              <p className="mt-2 text-sm text-[#808ba0]">
                Every edge has an investigation meaning—not decoration.
              </p>
            </div>
            <div className="h-[330px] bg-[#090c12]">
              <ReactFlow
                nodes={nodes}
                edges={edges}
                nodeTypes={{ trace: GraphNode as never }}
                fitView
                colorMode="dark"
              >
                <Background color="#273044" gap={24} />
                <Controls showInteractive={false} />
              </ReactFlow>
            </div>
          </div>
          <div className="panel overflow-hidden">
            <div className="flex items-center gap-2 border-b border-[#202735] p-4">
              <Terminal size={16} color="#77d5ab" />
              <span className="font-mono text-xs">controlled reproduction</span>
              <span className="ml-auto badge text-[#5ed3a3]">
                <span className="dot" />
                exit {repro?.exit_code ?? 0}
              </span>
            </div>
            <div className="bg-[#080b10] p-5 font-mono text-xs leading-6">
              <div className="text-[#657188]">
                $ {repro?.command ?? "python reproduce.py"}
              </div>
              <div className="mt-2 text-[#7cdbb3]">
                {repro?.stdout ?? "TRACEROOT_REPRODUCED: failure matched H1"}
              </div>
              <div className="mt-3 text-[#657188]">
                Process completed inside approved sandbox.
              </div>
            </div>
          </div>
        </div>
        <aside className="space-y-6">
          <div className="panel p-5">
            <div className="label">Ranked hypotheses</div>
            {data.hypotheses.map((h, i) => (
              <article
                className="mt-4 rounded-lg border border-[#273043] bg-[#0d1119] p-4"
                key={h.id}
              >
                <div className="flex justify-between">
                  <span className="font-mono text-xs text-[#91a5ff]">
                    {h.id}
                  </span>
                  <span className="font-mono text-xs">
                    {Math.round(h.confidence * 100)}%
                  </span>
                </div>
                <p className="mt-2 text-sm font-medium leading-5">{h.claim}</p>
                <p className="mt-2 text-xs leading-5 text-[#768197]">
                  {h.reason}
                </p>
                {i === 0 && (
                  <div className="mt-3 text-[10px] uppercase tracking-widest text-[#55d5a1]">
                    supported
                  </div>
                )}
              </article>
            ))}
          </div>
          <div className="panel p-5">
            <div className="label">Evidence ledger</div>
            {data.evidence.map((e) => (
              <article
                className="mt-4 border-l-2 border-[#596fc9] pl-4"
                key={e.id}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-[#9fb0ff]">
                    {e.type.replace("_", " ")}
                  </span>
                  <span className="font-mono text-[10px] text-[#657087]">
                    {Math.round(e.confidence * 100)}%
                  </span>
                </div>
                <div className="mt-1 font-mono text-[11px] text-[#9ca6b7]">
                  {e.location}
                </div>
                <p className="mt-2 text-xs leading-5 text-[#7f8a9e]">
                  {e.content_summary}
                </p>
                <div className="mt-2 text-[9px] text-[#566075]">
                  SHA-256 {e.content_hash}
                </div>
              </article>
            ))}
          </div>
          <div className="panel border-[#3d3423] p-5">
            <div className="flex gap-2 text-[#e8b45f]">
              <AlertCircle size={17} />
              <b className="text-sm">Human approval required</b>
            </div>
            <p className="mt-2 text-xs leading-5 text-[#8e8a7e]">
              TraceRoot recommends. It never deploys a production change
              autonomously.
            </p>
          </div>
        </aside>
      </section>
      <section className="panel mt-6 p-6">
        <div className="label">Recommended fix</div>
        <p className="mt-3 max-w-3xl text-sm leading-6 text-[#abb3c2]">
          {String(
            data.report.recommended_fix ??
              "Review the verified cause before production changes.",
          )}
        </p>
        <div className="mt-5 flex flex-wrap gap-3">
          <span className="badge text-[#56d4a1]">
            <FlaskConical size={12} />
            Regression confirmed
          </span>
          <span className="badge text-[#9badff]">
            <Code2 size={12} />
            Evidence preserved
          </span>
        </div>
      </section>
    </Shell>
  );
}
