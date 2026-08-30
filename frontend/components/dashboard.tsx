"use client";
import Link from "next/link";
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

const investigations = [
  {
    id: "demo-null",
    title: "Discount API returns 500",
    status: "VERIFIED",
    confidence: 96,
    time: "38s",
    severity: "SEV-2",
  },
  {
    id: "demo-token",
    title: "Expired sessions accepted",
    status: "VERIFIED",
    confidence: 94,
    time: "51s",
    severity: "SEV-1",
  },
  {
    id: "demo-storage",
    title: "Upload timeout spike",
    status: "UNVERIFIED",
    confidence: 35,
    time: "29s",
    severity: "SEV-2",
  },
];
const metrics: Array<{
  label: string;
  value: string | number;
  icon: LucideIcon;
  color: string;
}> = [
  { label: "Active", value: 3, icon: Radar, color: "#8ca1fb" },
  { label: "Verified", value: 24, icon: ShieldCheck, color: "#55d5a1" },
  {
    label: "Verification rate",
    value: "83%",
    icon: CheckCircle2,
    color: "#55d5a1",
  },
  { label: "Avg. duration", value: "44s", icon: Clock3, color: "#eab563" },
  { label: "Evidence coverage", value: "91%", icon: Radar, color: "#8ca1fb" },
];

export function Dashboard() {
  return (
    <Shell>
      <PageHeader
        eyebrow="Operational intelligence"
        title="Investigation command"
        description="TraceRoot correlates runtime, source and reproduction evidence before it accepts a root cause."
        action={
          <Link href="/incidents/new" className="btn btn-primary">
            <Plus size={16} />
            New incident
          </Link>
        }
      />
      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
        {metrics.map(({ label, value, icon: Icon, color }) => (
          <div className="panel p-5" key={label}>
            <div className="flex items-center justify-between">
              <span className="label">{label}</span>
              <Icon size={16} color={color} />
            </div>
            <div className="metric mt-4 text-3xl font-semibold">{value}</div>
            <div className="mt-2 text-xs text-[#667087]">
              Deterministic demo dataset
            </div>
          </div>
        ))}
      </section>
      <section className="panel mt-6 overflow-hidden">
        <div className="flex items-center justify-between border-b border-[#202735] p-5">
          <div>
            <h2 className="font-semibold">Recent investigations</h2>
            <p className="mt-1 text-xs text-[#747e92]">
              Every accepted claim remains linked to its proof.
            </p>
          </div>
          <Link className="text-sm text-[#98aaff]" href="/incidents">
            View all
          </Link>
        </div>
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
                ].map((x) => (
                  <th className="px-5 py-3 font-medium" key={x}>
                    {x}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {investigations.map((item) => (
                <tr
                  className="border-b border-[#1b212d] last:border-0 hover:bg-[#121721]"
                  key={item.id}
                >
                  <td className="px-5 py-4 font-medium">{item.title}</td>
                  <td className="px-5 py-4 text-[#8e98ab]">{item.severity}</td>
                  <td className="px-5 py-4">
                    <Status value={item.status} />
                  </td>
                  <td className="px-5 py-4 font-mono text-xs">
                    {item.confidence}%
                  </td>
                  <td className="px-5 py-4 text-[#8e98ab]">{item.time}</td>
                  <td className="px-5 py-4">
                    <Link
                      aria-label={`Open ${item.title}`}
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
      </section>
      <div className="mt-6 grid gap-6 lg:grid-cols-[1.4fr_1fr]">
        <section className="panel p-5">
          <div className="label">Verification posture</div>
          <div className="mt-6 flex h-24 items-end gap-2">
            {[48, 58, 55, 72, 69, 81, 78, 87, 82, 91, 88, 94].map((n, i) => (
              <div
                key={i}
                className="flex-1 rounded-t bg-[#596fc9]"
                style={{ height: `${n}%`, opacity: 0.35 + i * 0.045 }}
              />
            ))}
          </div>
          <div className="mt-3 flex justify-between text-xs text-[#687286]">
            <span>12 runs ago</span>
            <span>Now</span>
          </div>
        </section>
        <section className="panel p-5">
          <div className="label">Evidence gate</div>
          <p className="mt-4 text-lg font-medium">
            No root cause without evidence.
          </p>
          <p className="mt-2 text-sm leading-6 text-[#8490a4]">
            Runtime + source + reproduction + independent verification. Missing
            proof yields <b className="text-[#adb6c8]">UNVERIFIED</b>, never
            invented certainty.
          </p>
        </section>
      </div>
    </Shell>
  );
}
