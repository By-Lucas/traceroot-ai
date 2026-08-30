import { InvestigationConsole } from "@/components/investigation-console";
export default async function InvestigationPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <InvestigationConsole id={id} />;
}
