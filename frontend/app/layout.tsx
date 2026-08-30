import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = {
  title: { default: "TraceRoot", template: "%s · TraceRoot" },
  description: "From production failure to verified root cause.",
};
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
