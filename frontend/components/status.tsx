const colors: Record<string, string> = {
  VERIFIED: "text-[#55d5a1] border-[#275843] bg-[#10251d]",
  PARTIALLY_VERIFIED: "text-[#e9b767] border-[#5a4525] bg-[#261d10]",
  UNVERIFIED: "text-[#a5afc2]",
  REJECTED: "text-[#f27782] border-[#603039] bg-[#291216]",
};
export function Status({ value }: { value: string }) {
  return (
    <span className={`badge ${colors[value] ?? "text-[#9ba5b8]"}`}>
      <span className="dot" />
      {value.replaceAll("_", " ")}
    </span>
  );
}
