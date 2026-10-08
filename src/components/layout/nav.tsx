"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/cn";

const LINKS = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/session", label: "Entraînement" },
  { href: "/sections", label: "Sections" },
  { href: "/consulting", label: "Consulting" },
  { href: "/math", label: "Maths" },
] as const;

export function Nav() {
  const pathname = usePathname();
  if (pathname.startsWith("/login") || pathname.startsWith("/style-guide")) return null;

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <nav className="mx-auto max-w-5xl flex items-center gap-1 px-4 h-12">
        <span className="text-sm font-bold text-foreground mr-4 shrink-0">Prep</span>
        {LINKS.map(({ href, label }) => (
          <Link
            key={href}
            href={href}
            className={cn(
              "px-3 py-1.5 rounded text-sm font-medium transition-colors",
              pathname.startsWith(href)
                ? "bg-primary/10 text-primary"
                : "text-muted-foreground hover:text-foreground hover:bg-muted"
            )}
          >
            {label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
