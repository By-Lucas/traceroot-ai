import Link from "next/link";
import {
  ArrowRight,
  GitBranch,
  ShieldCheck,
  TerminalSquare,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

const features: Array<{ icon: LucideIcon; title: string; copy: string }> = [
  {
    icon: GitBranch,
    title: "Deliberate workflow",
    copy: "Four bounded agents with explicit state, budgets and independent verification.",
  },
  {
    icon: TerminalSquare,
    title: "Controlled proof",
    copy: "Allowlisted commands execute only inside the approved evaluation sandbox.",
  },
  {
    icon: ShieldCheck,
    title: "Honest uncertainty",
    copy: "Missing proof returns UNVERIFIED instead of hallucinated certainty.",
  },
];
export default function About() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-16 md:py-24">
      <div className="badge text-[#8fa4ff]">
        <span className="dot" />
        Evidence-first incident AI
      </div>
      <h1 className="mt-8 max-w-4xl text-5xl font-semibold tracking-[-.055em] md:text-7xl">
        From production failure to{" "}
        <span className="text-[#8ea3ff]">verified root cause.</span>
      </h1>
      <p className="mt-6 max-w-2xl text-lg leading-8 text-[#8d97aa]">
        TraceRoot turns logs, source, runtime behavior and controlled
        reproduction into a causal incident record—not another plausible chatbot
        answer.
      </p>
      <div className="mt-9 flex gap-3">
        <Link className="btn btn-primary" href="/register">
          Open command center
          <ArrowRight size={16} />
        </Link>
        <Link className="btn" href="/login">
          Sign in
        </Link>
      </div>
      <section className="mt-20 grid gap-5 md:grid-cols-3">
        {features.map(({ icon: Icon, title, copy }) => (
          <article className="panel p-6" key={title}>
            <Icon color="#91a5ff" />
            <h2 className="mt-5 text-lg font-semibold">{title}</h2>
            <p className="mt-2 text-sm leading-6 text-[#818ca1]">{copy}</p>
          </article>
        ))}
      </section>
    </main>
  );
}
