import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "var(--color-primary)",
          foreground: "var(--color-on-primary)",
        },
        secondary: {
          DEFAULT: "var(--color-secondary)",
          foreground: "var(--color-on-secondary)",
        },
        accent: {
          DEFAULT: "var(--color-accent)",
          foreground: "var(--color-on-accent)",
        },
        background: "var(--color-background)",
        foreground: "var(--color-foreground)",
        card: {
          DEFAULT: "var(--color-card)",
          foreground: "var(--color-card-foreground)",
        },
        muted: {
          DEFAULT: "var(--color-muted)",
          foreground: "var(--color-muted-foreground)",
        },
        border: "var(--color-border)",
        destructive: {
          DEFAULT: "var(--color-destructive)",
          foreground: "var(--color-on-destructive)",
        },
        ring: "var(--color-ring)",
      },
      fontFamily: {
        sans: ["var(--font-fira-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-fira-code)", "ui-monospace", "monospace"],
      },
      boxShadow: {
        sm: "0 1px 2px rgba(0,0,0,0.05)",
        md: "0 4px 6px rgba(0,0,0,0.1)",
        lg: "0 10px 15px rgba(0,0,0,0.1)",
        xl: "0 20px 25px rgba(0,0,0,0.15)",
      },
      borderRadius: {
        sm: "4px",
        md: "8px",
        lg: "12px",
        xl: "16px",
      },
    },
  },
  plugins: [],
};

export default config;
