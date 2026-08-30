"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { ArrowUpRight, Plus } from "lucide-react";
import { Shell } from "@/components/shell";
import { PageHeader } from "@/components/page-header";
import { Status } from "@/components/status";
import { api } from "@/lib/api";
import type { Incident } from "@/lib/domain";

export default function Incidents() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("");
  const [severity, setSeverity] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api<Incident[]>("/incidents")
      .then(setIncidents)
      .catch((reason) =>
        setError(
          reason instanceof Error ? reason.message : "Could not load incidents",
        ),
      )
      .finally(() => setLoading(false));
  }, []);

  const visible = useMemo(
    () =>
      incidents.filter((item) => {
        const needle = query.toLowerCase();
        return (
          (!needle ||
            `${item.title} ${item.description} ${item.logs}`
              .toLowerCase()
              .includes(needle)) &&
          (!status || item.status === status) &&
          (!severity || item.severity === severity)
        );
      }),
    [incidents, query, severity, status],
  );

  return (
    <Shell>
      <PageHeader
        eyebrow="Incident registry"
        title="Incidents"
        description="Production failures and their persisted investigation state."
        action={
          <Link className="btn btn-primary" href="/incidents/new">
            <Plus size={16} />
            New incident
          </Link>
        }
      />
      <div className="panel overflow-hidden">
        <div className="grid gap-4 border-b border-[#202735] p-5 md:grid-cols-[1fr_auto_auto]">
          <input
            aria-label="Search incidents"
            className="field"
            placeholder="Search title, logs or description…"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
          <select
            aria-label="Filter status"
            className="field"
            value={status}
            onChange={(event) => setStatus(event.target.value)}
          >
            <option value="">All states</option>
            <option value="open">Open</option>
            <option value="investigated">Investigated</option>
          </select>
          <select
            aria-label="Filter severity"
            className="field"
            value={severity}
            onChange={(event) => setSeverity(event.target.value)}
          >
            <option value="">All severities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>
        {loading ? (
          <p className="p-8 text-sm text-[#818ca1]">
            Loading persisted incidents…
          </p>
        ) : error ? (
          <p role="alert" className="p-8 text-sm text-[#f3828d]">
            {error}
          </p>
        ) : visible.length === 0 ? (
          <div className="py-14 text-center">
            <h2 className="text-lg font-semibold">No incidents found</h2>
            <p className="mt-2 text-sm text-[#818ca1]">
              Create an incident or adjust the filters.
            </p>
            <Link className="btn mt-5" href="/incidents/new">
              Open intake
            </Link>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[760px] text-left text-sm">
              <thead className="label border-b border-[#202735]">
                <tr>
                  <th className="px-5 py-3">Incident</th>
                  <th className="px-5 py-3">Severity</th>
                  <th className="px-5 py-3">State</th>
                  <th className="px-5 py-3">Created</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {visible.map((item) => (
                  <tr
                    className="border-b border-[#1b212d] last:border-0"
                    key={item.id}
                  >
                    <td className="px-5 py-4">
                      <div className="font-medium">{item.title}</div>
                      <div className="mt-1 max-w-xl truncate text-xs text-[#788398]">
                        {item.description}
                      </div>
                    </td>
                    <td className="px-5 py-4 uppercase text-[#8e98ab]">
                      {item.severity}
                    </td>
                    <td className="px-5 py-4">
                      <Status value={item.status.toUpperCase()} />
                    </td>
                    <td className="px-5 py-4 text-[#8e98ab]">
                      {new Date(item.created_at).toLocaleString()}
                    </td>
                    <td className="px-5 py-4">
                      <Link
                        aria-label={`Open ${item.title}`}
                        href={`/incidents/${item.id}`}
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
      </div>
    </Shell>
  );
}
