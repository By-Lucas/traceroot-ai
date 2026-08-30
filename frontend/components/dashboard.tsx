"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import {
  ArrowUpRight,
  CheckCircle2,
  Clock3,
  Plus,
  Radar,
  ShieldCheck,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { Shell } from "@/components/shell";
import { PageHeader } from "@/components/page-header";
import { Status } from "@/components/status";
import { api } from "@/lib/api";
import type { Incident, InvestigationListItem } from "@/lib/domain";

export function Dashboard() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [investigations, setInvestigations] = useState<InvestigationListItem[]>(
    [],
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api<Incident[]>("/incidents"),
      api<InvestigationListItem[]>("/investigations"),
    ])
      .then(([incidentRows, investigationRows]) => {
        setIncidents(incidentRows);
        setInvestigations(investigationRows);
      })
      .catch((reason) =>
        setError(
          reason instanceof Error ? reason.message : "Could not load dashboard",
        ),
      )
      .finally(() => setLoading(false));
  }, []);

  const metrics = useMemo(() => {
    const total = investigations.length;
    const verified = investigations.filter(
      (item) => item.status === "VERIFIED",
    ).length;
    const average = total
      ? investigations.reduce((sum, item) => sum + item.duration_ms, 0) / total
      : 0;
    const withEvidence = investigations.filter(
      (item) => item.evidence_count > 0,
    ).length;
    return [
      {
        label: "Active",
        value: incidents.filter((item) => item.status === "open").length,
        icon: Radar,
        color: "#8ca1fb",
      },
      {
        label: "Verified",
        value: verified,
        icon: ShieldCheck,
        color: "#55d5a1",
      },
      {
        label: "Verification rate",
        value: total ? `${Math.round((verified / total) * 100)}%` : "—",
        icon: CheckCircle2,
        color: "#55d5a1",
      },
      {
        label: "Avg. duration",
        value: total ? `${(average / 1000).toFixed(1)}s` : "—",
        icon: Clock3,
        color: "#eab563",
      },
      {
        label: "Evidence coverage",
        value: total ? `${Math.round((withEvidence / total) * 100)}%` : "—",
        icon: Radar,
        color: "#8ca1fb",
      },
    ] satisfies Array<{
      label: string;
      value: string | number;
      icon: LucideIcon;
      color: string;
    }>;
  }, [incidents, investigations]);

  return (
    <Shell>
      <PageHeader
        eyebrow="Operational intelligence"
        title="Investigation command"
        description="Live metrics calculated from your persisted incidents and investigations."
        action={
          <Link href="/incidents/new" className="btn btn-primary">
            <Plus size={16} />
            New incident
          </Link>
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
      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
        {metrics.map(({ label, value, icon: Icon, color }) => (
          <div className="panel p-5" key={label}>
            <div className="flex items-center justify-between">
              <span className="label">{label}</span>
              <Icon size={16} color={color} />
            </div>
            <div className="metric mt-4 text-3xl font-semibold">
              {loading ? "…" : value}
            </div>
            <div className="mt-2 text-xs text-[#667087]">Current workspace</div>
          </div>
        ))}
      </section>
      <section className="panel mt-6 overflow-hidden">
        <div className="flex items-center justify-between border-b border-[#202735] p-5">
          <div>
            <h2 className="font-semibold">Recent investigations</h2>
            <p className="mt-1 text-xs text-[#747e92]">
              Persisted runs only; no synthetic rows.
            </p>
          </div>
          <Link className="text-sm text-[#98aaff]" href="/incidents">
            View incidents
          </Link>
        </div>
        {loading ? (
          <p className="p-8 text-sm text-[#818ca1]">Loading investigations…</p>
        ) : investigations.length === 0 ? (
          <div className="p-10 text-center">
            <p className="font-medium">No investigation has run yet.</p>
            <Link href="/incidents/new" className="btn mt-4">
              Create the first incident
            </Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[700px] text-left text-sm">
              <thead className="label border-b border-[#202735]">
                <tr>
                  {[
                    "Incident",
                    "Severity",
                    "State",
                    "Confidence",
                    "Duration",
                    "",
                  ].map((item) => (
                    <th className="px-5 py-3 font-medium" key={item}>
                      {item}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {investigations.slice(0, 10).map((item) => (
                  <tr
                    className="border-b border-[#1b212d] last:border-0 hover:bg-[#121721]"
                    key={item.id}
                  >
                    <td className="px-5 py-4 font-medium">
                      {item.incident_title}
                    </td>
                    <td className="px-5 py-4 uppercase text-[#8e98ab]">
                      {item.severity}
                    </td>
                    <td className="px-5 py-4">
                      <Status value={item.status} />
                    </td>
                    <td className="px-5 py-4 font-mono text-xs">
                      {Math.round(item.confidence * 100)}%
                    </td>
                    <td className="px-5 py-4 text-[#8e98ab]">
                      {(item.duration_ms / 1000).toFixed(1)}s
                    </td>
                    <td className="px-5 py-4">
                      <Link
                        aria-label={`Open ${item.incident_title}`}
                        href={`/investigations/${item.id}`}
                      >
                        <ArrowUpRight size={16} />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
      <section className="panel mt-6 p-5">
        <div className="label">Evidence gate</div>
        <p className="mt-4 text-lg font-medium">
          No root cause without evidence.
        </p>
        <p className="mt-2 text-sm leading-6 text-[#8490a4]">
          Runtime, source, controlled reproduction and independent verification
          are required. Missing proof yields{" "}
          <b className="text-[#adb6c8]">UNVERIFIED</b>.
        </p>
      </section>
    </Shell>
  );
}
