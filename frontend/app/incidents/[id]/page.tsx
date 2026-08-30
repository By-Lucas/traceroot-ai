import Link from "next/link";
import { Shell } from "@/components/shell";
import { PageHeader } from "@/components/page-header";
export default async function Incident({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return (
    <Shell>
      <PageHeader
        eyebrow={`Incident / ${id.slice(0, 8)}`}
        title="Incident artifacts"
        description="Runtime inputs, source scope and investigations remain bound to this incident."
      />
      <div className="panel p-7">
        <div className="label">Investigation state</div>
        <h2 className="mt-3 text-xl font-semibold">
          Ready for evidence collection
        </h2>
        <p className="mt-2 text-sm text-[#8490a4]">
          Open the latest run to inspect hypotheses, tool calls and the final
          verification gate.
        </p>
        <Link className="btn mt-5" href={`/investigations/${id}`}>
          Open investigation
        </Link>
      </div>
    </Shell>
  );
}
