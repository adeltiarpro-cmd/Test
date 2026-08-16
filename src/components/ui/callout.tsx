import { cva, type VariantProps } from "class-variance-authority";
import { type HTMLAttributes } from "react";
import { AlertCircle, CheckCircle2, Info, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/cn";

const calloutVariants = cva("flex gap-3 rounded-lg border p-3 text-sm", {
  variants: {
    variant: {
      info: "border-primary/30 bg-primary/10 text-primary",
      success: "border-green-600/30 bg-green-50 text-green-700",
      warning: "border-amber-600/30 bg-amber-50 text-amber-700",
      error: "border-destructive/30 bg-destructive/10 text-destructive",
    },
  },
  defaultVariants: {
    variant: "info",
  },
});

const ICONS = {
  info: Info,
  success: CheckCircle2,
  warning: AlertTriangle,
  error: AlertCircle,
} as const;

export interface CalloutProps
  extends HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof calloutVariants> {
  title?: string;
}

function Callout({
  className,
  variant = "info",
  title,
  children,
  ...props
}: CalloutProps) {
  const Icon = ICONS[variant ?? "info"];

  return (
    <div
      role="note"
      className={cn(calloutVariants({ variant }), className)}
      {...props}
    >
      <Icon className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
      <div className="flex flex-col gap-0.5">
        {title && <p className="font-semibold">{title}</p>}
        {children && <div className="opacity-90">{children}</div>}
      </div>
    </div>
  );
}

export { Callout };
