import { BookOpen, FileJson2, FileText, Plus } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { Shell } from "@/components/shell";
import { PageHeader } from "@/components/page-header";
const documents: Array<{ title: string; type: string; icon: LucideIcon }> = [
  { title: "Incident response playbook", type: "Markdown", icon: BookOpen },
  { title: "Service architecture", type: "TXT", icon: FileText },
  { title: "Known failure signatures", type: "JSON", icon: FileJson2 },
];
export default function Knowledge() {
  return (
    <Shell>
      <PageHeader
        eyebrow="Engineering memory"
        title="Knowledge base"
        description="Runbooks, architecture notes and known failure modes available to the evidence agent."
        action={
          <button className="btn btn-primary">
            <Plus size={16} />
            Ingest document
          </button>
        }
      />
      <div className="grid gap-5 md:grid-cols-3">
        {documents.map(({ title, type, icon: Icon }) => (
          <article className="panel p-5" key={title}>
            <Icon size={19} color="#91a5ff" />
            <h2 className="mt-5 font-semibold">{title}</h2>
            <div className="mt-2 text-xs text-[#737e92]">
              {type} · provenance indexed
            </div>
            <div className="mt-5 border-t border-[#222a38] pt-4 text-xs text-[#8993a6]">
              Ready for retrieval
            </div>
          </article>
        ))}
      </div>
    </Shell>
  );
}
