import Link from "next/link";
import { Plus } from "lucide-react";
import { Shell } from "@/components/shell";
import { PageHeader } from "@/components/page-header";
import { Status } from "@/components/status";
export default function Incidents() {
  return (
    <Shell>
      <PageHeader
        eyebrow="Incident registry"
        title="Incidents"
        description="Production failures and their evidence-backed investigation state."
        action={
          <Link className="btn btn-primary" href="/incidents/new">
            <Plus size={16} />
            New incident
          </Link>
        }
      />
      <div className="panel p-5">
        <div className="grid gap-4 border-b border-[#202735] pb-5 md:grid-cols-[1fr_auto_auto]">
          <input
            aria-label="Search incidents"
            className="field"
            placeholder="Search title, logs or root cause…"
          />
          <select aria-label="Filter status" className="field">
            <option>All states</option>
            <option>Verified</option>
            <option>Unverified</option>
          </select>
          <select aria-label="Filter severity" className="field">
            <option>All severities</option>
            <option>Critical</option>
            <option>High</option>
          </select>
        </div>
        <div className="py-14 text-center">
          <Status value="VERIFIED" />
          <h2 className="mt-4 text-xl font-semibold">Demo registry is ready</h2>
          <p className="mx-auto mt-2 max-w-md text-sm text-[#818ca1]">
            Create an incident or run one of the synthetic cases to populate
            your isolated workspace.
          </p>
          <Link className="btn mt-5" href="/incidents/new">
            Open intake
          </Link>
        </div>
      </div>
    </Shell>
  );
}
