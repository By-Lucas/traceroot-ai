import type { ReactNode } from "react";
export function PageHeader({
  eyebrow,
  title,
  description,
  action,
}: {
  eyebrow: string;
  title: string;
  description: string;
  action?: ReactNode;
}) {
  return (
    <header className="mb-7 flex flex-col justify-between gap-5 md:flex-row md:items-end">
      <div>
        <div className="label mb-2">{eyebrow}</div>
        <h1 className="text-3xl font-semibold tracking-[-.035em] md:text-4xl">
          {title}
        </h1>
        <p className="mt-2 max-w-2xl text-sm leading-6 text-[#8b95aa]">
          {description}
        </p>
      </div>
      {action}
    </header>
  );
}
