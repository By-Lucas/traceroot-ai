import { KeyRound, LockKeyhole, Server } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { Shell } from "@/components/shell";
import { PageHeader } from "@/components/page-header";
const controls: Array<{ icon: LucideIcon; title: string; value: string }> = [
  {
    icon: Server,
    title: "LLM provider",
    value: "Demo mode — no external calls",
  },
  {
    icon: KeyRound,
    title: "Credentials",
    value: "Environment managed; never shown in the browser",
  },
  {
    icon: LockKeyhole,
    title: "Execution policy",
    value: "Approved sandbox · 20 tool calls max",
  },
];
export default function Settings() {
  return (
    <Shell>
      <PageHeader
        eyebrow="Workspace controls"
        title="Settings"
        description="Provider selection and safety boundaries are configured through environment-backed secrets."
      />
      <section className="panel max-w-3xl divide-y divide-[#202735]">
        {controls.map(({ icon: Icon, title, value }) => (
          <div className="flex items-center gap-4 p-5" key={title}>
            <span className="grid h-10 w-10 place-items-center rounded-lg border border-[#2d374a]">
              <Icon size={17} color="#91a5ff" />
            </span>
            <div>
              <div className="text-sm font-medium">{title}</div>
              <div className="mt-1 text-xs text-[#798499]">{value}</div>
            </div>
          </div>
        ))}
      </section>
    </Shell>
  );
}
