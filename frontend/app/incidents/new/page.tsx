"use client";
import { FormEvent, useEffect, useState, useSyncExternalStore } from "react";
import { useRouter } from "next/navigation";
import { AlertTriangle, ArrowRight, FileCode2, Shield } from "lucide-react";
import { Shell } from "@/components/shell";
import { PageHeader } from "@/components/page-header";
import { api, token } from "@/lib/api";
type Incident = { id: string };
type Investigation = { id: string };
export default function NewIncident() {
  const router = useRouter();
  const isClient = useSyncExternalStore(
    () => () => undefined,
    () => true,
    () => false,
  );
  const authenticated = isClient && Boolean(token());
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  useEffect(() => {
    if (isClient && !authenticated) {
      router.replace("/login?next=/incidents/new");
    }
  }, [authenticated, isClient, router]);

  if (!authenticated) {
    return (
      <main className="grid min-h-screen place-items-center text-sm text-[#8b95aa]">
        Checking secure session…
      </main>
    );
  }
  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setBusy(true);
    setError("");
    const data = Object.fromEntries(new FormData(e.currentTarget));
    try {
      const incident = await api<Incident>("/incidents", {
        method: "POST",
        body: JSON.stringify(data),
      });
      const investigation = await api<Investigation>(
        `/incidents/${incident.id}/investigate`,
        { method: "POST" },
      );
      router.push(`/investigations/${investigation.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Investigation failed");
      setBusy(false);
    }
  }
  return (
    <Shell>
      <PageHeader
        eyebrow="Incident intake"
        title="Start with the failure"
        description="Give TraceRoot the raw artifacts. The agents will separate evidence from plausible noise."
      />
      <form onSubmit={submit} className="grid gap-6 xl:grid-cols-[1fr_340px]">
        <section className="panel space-y-5 p-6">
          <div className="grid gap-5 md:grid-cols-[1fr_160px]">
            <label className="text-sm text-[#aeb6c7]">
              Incident title
              <input
                className="field mt-2"
                name="title"
                required
                minLength={3}
                placeholder="Checkout API returns 500"
              />
            </label>
            <label className="text-sm text-[#aeb6c7]">
              Severity
              <select
                className="field mt-2"
                name="severity"
                defaultValue="high"
              >
                <option value="critical">Critical</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </label>
          </div>
          <label className="block text-sm text-[#aeb6c7]">
            What happened?
            <textarea
              className="field mt-2 min-h-28 resize-y"
              name="description"
              required
              minLength={10}
              placeholder="Describe impact, timing and recent changes…"
            />
          </label>
          <label className="block text-sm text-[#aeb6c7]">
            Logs
            <textarea
              className="field mt-2 min-h-36 resize-y font-mono text-xs leading-5"
              name="logs"
              placeholder="Paste relevant log lines…"
            />
          </label>
          <label className="block text-sm text-[#aeb6c7]">
            Stack trace
            <textarea
              className="field mt-2 min-h-28 resize-y font-mono text-xs leading-5"
              name="stack_trace"
              placeholder="Paste the full stack trace…"
            />
          </label>
          <label className="block text-sm text-[#aeb6c7]">
            Controlled demo repository{" "}
            <span className="text-[#6e788c]">
              (optional, demo sandbox only)
            </span>
            <div className="relative mt-2">
              <FileCode2
                className="absolute left-3 top-3"
                size={16}
                color="#788398"
              />
              <select
                className="field pl-10"
                name="repository_path"
                defaultValue="02_null_handling_regression"
              >
                <option value="">No repository — result will be unverified</option>
                <option value="01_missing_environment_variable">Missing environment variable</option>
                <option value="02_null_handling_regression">Null handling regression</option>
                <option value="03_database_migration_bug">Database migration bug</option>
                <option value="04_dependency_version_conflict">Dependency version conflict</option>
                <option value="05_api_payload_contract_regression">API payload regression</option>
                <option value="06_state_or_concurrency_bug">Concurrency bug</option>
                <option value="07_timezone_bug">Timezone bug</option>
                <option value="08_configuration_precedence_bug">Configuration precedence</option>
                <option value="09_auth_token_validation_regression">Auth token regression</option>
                <option value="10_misleading_stacktrace">Misleading stack trace</option>
              </select>
            </div>
          </label>
          {error && (
            <div
              role="alert"
              className="flex gap-2 rounded-lg border border-[#5d3038] bg-[#261216] p-3 text-sm text-[#f3828d]"
            >
              <AlertTriangle size={17} />
              {error}
            </div>
          )}
          <div className="flex justify-end">
            <button className="btn btn-primary" disabled={busy}>
              {busy ? "Agents investigating…" : "Begin investigation"}
              <ArrowRight size={16} />
            </button>
          </div>
        </section>
        <aside className="space-y-4">
          <div className="panel p-5">
            <Shield size={19} color="#62d2a0" />
            <h2 className="mt-4 font-semibold">Controlled by design</h2>
            <p className="mt-2 text-sm leading-6 text-[#828da1]">
              Repository access stays inside the configured sandbox. Only
              allowlisted reproduction commands can execute.
            </p>
          </div>
          <div className="panel p-5">
            <div className="label">Investigation path</div>
            {[
              "Triage hypotheses",
              "Collect provenance",
              "Reproduce safely",
              "Challenge diagnosis",
              "Issue report",
            ].map((x, i) => (
              <div className="mt-4 flex items-center gap-3 text-sm" key={x}>
                <span className="grid h-6 w-6 place-items-center rounded-full border border-[#35415a] text-[10px] text-[#92a6ff]">
                  {i + 1}
                </span>
                {x}
              </div>
            ))}
          </div>
        </aside>
      </form>
    </Shell>
  );
}
