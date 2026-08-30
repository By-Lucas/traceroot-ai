"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Activity,
  BookOpen,
  CircleGauge,
  FlaskConical,
  GitBranch,
  Hexagon,
  Settings,
} from "lucide-react";
import type { ReactNode } from "react";

const links = [
  ["/dashboard", "Overview", CircleGauge],
  ["/incidents", "Incidents", Activity],
  ["/evaluations", "Evaluations", FlaskConical],
  ["/knowledge", "Knowledge", BookOpen],
  ["/settings", "Settings", Settings],
] as const;

export function Shell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  return (
    <div className="min-h-screen lg:grid lg:grid-cols-[236px_1fr]">
      <aside className="border-b border-[#202633] bg-[#0b0e14]/95 p-5 lg:sticky lg:top-0 lg:h-screen lg:border-b-0 lg:border-r">
        <Link href="/dashboard" className="flex items-center gap-3">
          <span className="grid h-9 w-9 place-items-center rounded-lg border border-[#39435a] bg-[#151b28]">
            <Hexagon size={19} color="#8ca1fb" />
          </span>
          <span>
            <b className="tracking-tight">TraceRoot</b>
            <small className="block text-[10px] tracking-[.18em] text-[#6e7890]">
              INCIDENT INTELLIGENCE
            </small>
          </span>
        </Link>
        <nav className="mt-7 flex gap-2 overflow-x-auto lg:flex-col">
          {links.map(([href, label, Icon]) => (
            <Link
              key={href}
              href={href}
              className={`flex min-w-max items-center gap-3 rounded-lg px-3 py-2.5 text-sm ${pathname.startsWith(href) ? "border border-[#2b354b] bg-[#171d29] text-white" : "text-[#828ba0] hover:text-white"}`}
            >
              <Icon size={16} />
              {label}
            </Link>
          ))}
        </nav>
        <div className="mt-8 hidden rounded-xl border border-[#202a3d] bg-[#111722] p-4 lg:block">
          <div className="label">System posture</div>
          <div className="mt-3 flex items-center gap-2 text-sm text-[#65d5a7]">
            <span className="dot" /> All systems ready
          </div>
          <div className="mt-3 flex items-center gap-2 text-xs text-[#707a90]">
            <GitBranch size={13} /> deterministic demo
          </div>
        </div>
      </aside>
      <main className="min-w-0 p-5 md:p-8 xl:p-10">{children}</main>
    </div>
  );
}
