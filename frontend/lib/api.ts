export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";
export function token() {
  return typeof window === "undefined"
    ? null
    : localStorage.getItem("traceroot_access");
}
export async function api<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers);
  headers.set("content-type", "application/json");
  const access = token();
  if (access) headers.set("authorization", `Bearer ${access}`);
  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  const body =
    response.status === 204 ? null : await response.json().catch(() => null);
  if (response.status === 401 && typeof window !== "undefined") {
    localStorage.removeItem("traceroot_access");
    localStorage.removeItem("traceroot_refresh");
    const next = `${window.location.pathname}${window.location.search}`;
    // This transport utility runs outside React, so use a full navigation to clear stale state.
    // eslint-disable-next-line @next/next/no-location-assign-relative-destination
    window.location.href = `/login?next=${encodeURIComponent(next)}`;
  }
  if (!response.ok)
    throw new Error(body?.detail ?? `Request failed (${response.status})`);
  return body as T;
}
