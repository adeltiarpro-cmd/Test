"use client";

import katex from "katex";

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/\n\n/g, "</p><p>")
    .replace(/\n/g, "<br/>");
}

// Replaces $...$ and $$...$$ with KaTeX HTML; escapes plain text segments.
function renderMathHtml(text: string): string {
  const parts: string[] = [];
  let lastIndex = 0;
  const mathRe = /\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$/g;
  let m: RegExpExecArray | null;

  while ((m = mathRe.exec(text)) !== null) {
    parts.push(escapeHtml(text.slice(lastIndex, m.index)));
    const isDisplay = m[0].startsWith("$$");
    const math = (m[1] ?? m[2]).trim();
    try {
      parts.push(katex.renderToString(math, { displayMode: isDisplay, throwOnError: false }));
    } catch {
      parts.push(`<span class="text-destructive font-mono">${escapeHtml(m[0])}</span>`);
    }
    lastIndex = m.index + m[0].length;
  }

  parts.push(escapeHtml(text.slice(lastIndex)));
  return `<p>${parts.join("")}</p>`;
}

export function MathText({
  children,
  className,
}: {
  children: string;
  className?: string;
}) {
  return (
    <div
      className={className}
      // Safe: KaTeX output is sanitized; plain text is HTML-escaped above.
      dangerouslySetInnerHTML={{ __html: renderMathHtml(children) }}
    />
  );
}
