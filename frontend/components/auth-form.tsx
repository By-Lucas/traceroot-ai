"use client";
import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AlertTriangle, ArrowRight, Hexagon } from "lucide-react";
import { api } from "@/lib/api";

export function AuthForm({ mode }: { mode: "login" | "register" }) {
  const router = useRouter();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    const data = new FormData(event.currentTarget);
    try {
      const body = await api<{ access_token: string; refresh_token: string }>(
        `/auth/${mode}`,
        { method: "POST", body: JSON.stringify(Object.fromEntries(data)) },
      );
      localStorage.setItem("traceroot_access", body.access_token);
      localStorage.setItem("traceroot_refresh", body.refresh_token);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed");
    } finally {
      setLoading(false);
    }
  }
  return (
    <main className="grid min-h-screen place-items-center p-5">
      <div className="w-full max-w-md">
        <Link
          href="/about"
          className="mb-8 flex items-center justify-center gap-2"
        >
          <Hexagon color="#8ca1fb" />
          <b>TraceRoot</b>
        </Link>
        <section className="panel p-7 md:p-9">
          <div className="label">Secure workspace</div>
          <h1 className="mt-2 text-2xl font-semibold">
            {mode === "login" ? "Return to command" : "Create your workspace"}
          </h1>
          <p className="mt-2 text-sm text-[#8b95aa]">
            {mode === "login"
              ? "Continue an evidence-first investigation."
              : "Move from production failure to verified root cause."}
          </p>
          {error && (
            <div
              role="alert"
              className="mt-5 flex gap-2 rounded-lg border border-[#5d3038] bg-[#261216] p-3 text-sm text-[#f3828d]"
            >
              <AlertTriangle size={17} />
              {error}
            </div>
          )}
          <form className="mt-6 space-y-4" onSubmit={submit}>
            {mode === "register" && (
              <label className="block text-sm text-[#aab2c2]">
                Display name
                <input
                  className="field mt-1.5"
                  name="display_name"
                  required
                  minLength={2}
                  autoComplete="name"
                />
              </label>
            )}
            <label className="block text-sm text-[#aab2c2]">
              Email
              <input
                className="field mt-1.5"
                name="email"
                type="email"
                required
                autoComplete="email"
              />
            </label>
            <label className="block text-sm text-[#aab2c2]">
              Password
              <input
                className="field mt-1.5"
                name="password"
                type="password"
                minLength={10}
                required
                autoComplete={
                  mode === "login" ? "current-password" : "new-password"
                }
              />
            </label>
            <button className="btn btn-primary mt-2 w-full" disabled={loading}>
              {loading
                ? "Securing session…"
                : mode === "login"
                  ? "Enter workspace"
                  : "Create account"}
              <ArrowRight size={16} />
            </button>
          </form>
          <p className="mt-6 text-center text-sm text-[#7f899c]">
            {mode === "login"
              ? "New to TraceRoot? "
              : "Already investigating? "}
            <Link
              className="text-[#9eb0ff] hover:underline"
              href={mode === "login" ? "/register" : "/login"}
            >
              {mode === "login" ? "Create an account" : "Sign in"}
            </Link>
          </p>
        </section>
      </div>
    </main>
  );
}
