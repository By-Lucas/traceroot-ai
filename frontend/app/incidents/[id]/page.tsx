"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { Shell } from "@/components/shell";
import { PageHeader } from "@/components/page-header";
import { Status } from "@/components/status";
import { api } from "@/lib/api";
import type { Incident, InvestigationListItem } from "@/lib/domain";

export default function IncidentPage() {
  const { id } = useParams<{ id: string }>();
  const [incident, setIncident] = useState<Incident | null>(null);
  const [runs, setRuns] = useState<InvestigationListItem[]>([]);
  const [error, setError] = useState("");
  useEffect(() => {
    Promise.all([
      api<Incident>(`/incidents/${id}`),
      api<InvestigationListItem[]>("/investigations"),
    ])
      .then(([item, allRuns]) => {
        setIncident(item);
        setRuns(allRuns.filter((run) => run.incident_id === id));
      })
      .catch((reason) =>
        setError(
          reason instanceof Error ? reason.message : "Could not load incident",
        ),
      );
  }, [id]);

  return (
    <Shell>
      <PageHeader
        eyebrow={`Incident / ${id.slice(0, 8)}`}
        title={incident?.title ?? "Loading incident…"}
        description="Persisted runtime inputs, source scope and investigation runs."
      />
      {error ? (
        <div role="alert" className="panel p-6 text-[#f3828d]">
          {error}
        </div>
      ) : (
        incident && (
          <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
            <section className="panel space-y-5 p-6">
              <div className="flex items-center justify-between">
                <Status value={incident.status.toUpperCase()} />
                <span className="text-xs uppercase text-[#818ca1]">
                  {incident.severity}
                </span>
              </div>
              <div>
                <div className="label">What happened</div>
                <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-[#aab3c4]">
                  {incident.description}
                </p>
              </div>
              <div>
                <div className="label">Logs</div>
                <pre className="mt-2 overflow-auto rounded-lg bg-[#080b10] p-4 text-xs text-[#8fd8b6]">
                  {incident.logs || "No logs supplied"}
                </pre>
              </div>
              <div>
                <div className="label">Stack trace</div>
                <pre className="mt-2 overflow-auto rounded-lg bg-[#080b10] p-4 text-xs text-[#a7afbe]">
                  {incident.stack_trace || "No stack trace supplied"}
                </pre>
              </div>
            </section>
            <aside className="panel p-5">
              <div className="label">Investigation runs</div>
              {runs.length === 0 ? (
                <p className="mt-4 text-sm text-[#818ca1]">
                  No run was persisted for this incident.
                </p>
              ) : (
                runs.map((run) => (
                  <Link
                    key={run.id}
                    href={`/investigations/${run.id}`}
                    className="mt-4 block rounded-lg border border-[#273043] p-4 hover:bg-[#121721]"
                  >
                    <div className="flex items-center justify-between">
                      <Status value={run.status} />
                      <span className="font-mono text-xs">
                        {Math.round(run.confidence * 100)}%
                      </span>
                    </div>
                    <p className="mt-3 text-sm text-[#aab3c4]">
                      {run.root_cause ?? "No verified root cause"}
                    </p>
                  </Link>
                ))
              )}
            </aside>
          </div>
        )
      )}
    </Shell>
  );
}
