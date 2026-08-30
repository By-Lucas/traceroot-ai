import { BarChart3, CheckCircle2, FlaskConical } from "lucide-react";
import { Shell } from "@/components/shell";
import { PageHeader } from "@/components/page-header";
export default function Evaluations() {
  return (
    <Shell>
      <PageHeader
        eyebrow="Measured reliability"
        title="Evaluation laboratory"
        description="The same ten incidents go to a reasonable single-pass baseline and TraceRoot's evidence gate."
        action={
          <button className="btn btn-primary">
            <FlaskConical size={16} />
            Run evaluation
          </button>
        }
      />
      <div className="grid gap-5 lg:grid-cols-3">
        <section className="panel p-6 lg:col-span-2">
          <div className="label">Verified root cause accuracy</div>
          <div className="mt-6 grid grid-cols-2 gap-5">
            <div className="rounded-xl border border-[#293144] bg-[#0c1017] p-5">
              <span className="text-sm text-[#8994a9]">
                Single-agent baseline
              </span>
              <div className="metric mt-3 text-4xl font-semibold">0%</div>
              <div className="mt-4 h-2 rounded bg-[#232a37]">
                <div
                  className="h-2 rounded bg-[#69758c]"
                  style={{ width: "0%" }}
                />
              </div>
            </div>
            <div className="rounded-xl border border-[#27513f] bg-[#0d1713] p-5">
              <span className="text-sm text-[#8ba89b]">TraceRoot</span>
              <div className="metric mt-3 text-4xl font-semibold text-[#59d3a2]">
                100%
              </div>
              <div className="mt-4 h-2 rounded bg-[#1e332a]">
                <div
                  className="h-2 rounded bg-[#53ca99]"
                  style={{ width: "100%" }}
                />
              </div>
            </div>
          </div>
          <p className="mt-5 text-xs leading-5 text-[#69758b]">
            Offline deterministic demo results. These validate orchestration,
            evidence, reproduction and scoring—not provider-backed LLM quality.
          </p>
        </section>
        <section className="panel p-6">
          <BarChart3 color="#91a5ff" />
          <h2 className="mt-4 text-lg font-semibold">10 / 10 reproduced</h2>
          <p className="mt-2 text-sm leading-6 text-[#808ba0]">
            Each case executes a controlled script and records exit status
            before verification.
          </p>
          <div className="mt-5 space-y-3">
            {[
              "Evidence precision",
              "Reproduction success",
              "False confidence",
            ].map((x, i) => (
              <div className="flex justify-between text-xs" key={x}>
                <span className="text-[#8791a4]">{x}</span>
                <b>{i === 2 ? "0%" : "100%"}</b>
              </div>
            ))}
          </div>
        </section>
      </div>
      <section className="panel mt-5 p-6">
        <div className="label">Case matrix</div>
        <div className="mt-4 grid gap-2 md:grid-cols-2">
          {[
            "Missing environment variable",
            "Null handling regression",
            "Database migration bug",
            "Dependency conflict",
            "Payload contract regression",
            "Concurrency bug",
            "Timezone bug",
            "Configuration precedence",
            "Token validation regression",
            "Misleading stack trace",
          ].map((x, i) => (
            <div
              className="flex items-center gap-3 rounded-lg border border-[#202837] p-3 text-sm"
              key={x}
            >
              <CheckCircle2 size={15} color="#55d5a1" />
              <span className="font-mono text-[10px] text-[#657188]">
                {String(i + 1).padStart(2, "0")}
              </span>
              {x}
            </div>
          ))}
        </div>
      </section>
    </Shell>
  );
}
