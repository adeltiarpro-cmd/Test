import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
  TableCaption,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Callout } from "@/components/ui/callout";
import { Search, ArrowRight, Trash2 } from "lucide-react";

export const metadata = {
  title: "Style Guide — Prep Platform",
};

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section aria-labelledby={`section-${title.toLowerCase().replace(/\s+/g, "-")}`} className="flex flex-col gap-4">
      <h2
        id={`section-${title.toLowerCase().replace(/\s+/g, "-")}`}
        className="text-base font-semibold text-muted-foreground uppercase tracking-wider border-b border-border pb-2"
      >
        {title}
      </h2>
      {children}
    </section>
  );
}

const PALETTE = [
  { name: "Primary", hex: "#4F46E5", css: "--color-primary", bg: "bg-primary", text: "text-primary-foreground" },
  { name: "Secondary", hex: "#818CF8", css: "--color-secondary", bg: "bg-secondary", text: "text-secondary-foreground" },
  { name: "Accent / CTA", hex: "#EA580C", css: "--color-accent", bg: "bg-accent", text: "text-accent-foreground" },
  { name: "Background", hex: "#EEF2FF", css: "--color-background", bg: "bg-background", text: "text-foreground", border: true },
  { name: "Card", hex: "#FFFFFF", css: "--color-card", bg: "bg-card", text: "text-card-foreground", border: true },
  { name: "Muted", hex: "#EBEEF8", css: "--color-muted", bg: "bg-muted", text: "text-muted-foreground", border: true },
  { name: "Border", hex: "#C7D2FE", css: "--color-border", bg: "bg-border", text: "text-foreground", border: true },
  { name: "Destructive", hex: "#DC2626", css: "--color-destructive", bg: "bg-destructive", text: "text-destructive-foreground" },
];

const SAMPLE_ROWS = [
  { metric: "Sharpe Ratio", q1: "1.42", q2: "1.61", q3: "1.38", status: "On Track" },
  { metric: "Beta", q1: "0.87", q2: "0.91", q3: "0.85", status: "On Track" },
  { metric: "Max Drawdown", q1: "−8.24%", q2: "−6.57%", q3: "−9.01%", status: "Review" },
  { metric: "CAGR", q1: "14.3%", q2: "16.8%", q3: "13.1%", status: "On Track" },
];

export default function StyleGuidePage() {
  return (
    <main className="min-h-screen bg-background px-4 py-8 md:px-8">
      <div className="mx-auto max-w-4xl flex flex-col gap-12">
        <header>
          <h1 className="text-2xl font-semibold text-foreground">
            Style Guide — Prep Platform
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Minimalism &amp; Swiss Style · Fira Sans / Fira Code · Density 8/10
          </p>
        </header>

        {/* ── Color Palette ── */}
        <Section title="Color Palette">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            {PALETTE.map(({ name, hex, css, bg, text, border }) => (
              <div key={name} className="flex flex-col gap-1">
                <div
                  className={`h-12 rounded-md ${bg} ${border ? "border border-border" : ""}`}
                  title={hex}
                />
                <p className="text-xs font-medium text-foreground">{name}</p>
                <p className="text-xs text-muted-foreground font-mono">{hex}</p>
                <p className="text-xs text-muted-foreground font-mono">{css}</p>
              </div>
            ))}
          </div>
        </Section>

        {/* ── Typography ── */}
        <Section title="Typography">
          <div className="flex flex-col gap-3 bg-card rounded-lg border border-border p-4">
            <p className="text-2xl font-bold text-foreground">
              Titre H1 — Fira Sans Bold
            </p>
            <p className="text-xl font-semibold text-foreground">
              Titre H2 — Fira Sans SemiBold
            </p>
            <p className="text-base font-medium text-foreground">
              Corps de texte — Fira Sans Regular 16px
            </p>
            <p className="text-sm text-muted-foreground">
              Texte secondaire — Fira Sans 14px Muted
            </p>
            <p className="font-mono text-sm tabular-nums text-foreground">
              Données financières — Fira Code : 1,234,567.89 € · 42.00% · −8.24%
            </p>
          </div>
        </Section>

        {/* ── Buttons ── */}
        <Section title="Buttons">
          <div className="flex flex-wrap gap-3 items-center">
            <Button variant="primary">Commencer</Button>
            <Button variant="secondary">Explorer</Button>
            <Button variant="outline">En savoir plus</Button>
            <Button variant="ghost">Annuler</Button>
            <Button variant="destructive">Supprimer</Button>
            <Button variant="primary" disabled>Désactivé</Button>
          </div>
          <div className="flex flex-wrap gap-3 items-center">
            <Button variant="primary" size="sm">Petit</Button>
            <Button variant="primary" size="md">Moyen</Button>
            <Button variant="primary" size="lg">Grand</Button>
            <Button variant="outline" size="icon" aria-label="Rechercher">
              <Search className="h-4 w-4" />
            </Button>
            <Button variant="destructive" size="icon" aria-label="Supprimer">
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
          <div className="flex flex-wrap gap-3 items-center">
            <Button variant="primary">
              Continuer <ArrowRight className="h-4 w-4" />
            </Button>
            <Button variant="secondary">
              <Search className="h-4 w-4" /> Recherche
            </Button>
          </div>
        </Section>

        {/* ── Inputs ── */}
        <Section title="Inputs">
          <div className="grid sm:grid-cols-2 gap-4">
            <Input label="Email" type="email" placeholder="nom@exemple.fr" />
            <Input
              label="Recherche"
              placeholder="Taper un concept…"
              startIcon={<Search className="h-4 w-4" />}
            />
            <Input
              label="Mot de passe"
              type="password"
              placeholder="••••••••"
              hint="Minimum 8 caractères"
            />
            <Input
              label="Score GMAT"
              type="number"
              placeholder="550"
              error="Veuillez entrer une valeur entre 200 et 800."
            />
          </div>
        </Section>

        {/* ── Cards ── */}
        <Section title="Cards">
          <div className="grid sm:grid-cols-3 gap-3">
            <Card>
              <CardHeader>
                <CardTitle>Finance de Marché</CardTitle>
                <CardDescription>Options, dérivés, fixed income</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  42 exercices · 3 modules
                </p>
              </CardContent>
              <CardFooter>
                <Badge variant="accent">Actif</Badge>
              </CardFooter>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>GMAT Quantitatif</CardTitle>
                <CardDescription>DS, PS, algèbre, probabilités</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  128 exercices · 8 modules
                </p>
              </CardContent>
              <CardFooter>
                <Badge variant="default">En cours</Badge>
              </CardFooter>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Mathématiques</CardTitle>
                <CardDescription>Calcul stochastique, algèbre linéaire</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  15 exercices · 3 modules
                </p>
              </CardContent>
              <CardFooter>
                <Badge variant="outline">Bientôt</Badge>
              </CardFooter>
            </Card>
          </div>
        </Section>

        {/* ── Badges ── */}
        <Section title="Badges">
          <div className="flex flex-wrap gap-2 items-center">
            <Badge variant="default">Primary</Badge>
            <Badge variant="secondary">Secondary</Badge>
            <Badge variant="accent">CTA / Accent</Badge>
            <Badge variant="muted">Muted</Badge>
            <Badge variant="destructive">Erreur</Badge>
            <Badge variant="outline">Outline</Badge>
          </div>
          <div className="flex flex-wrap gap-2 items-center">
            <Badge variant="default">Difficulté 3</Badge>
            <Badge variant="accent">Nouveau</Badge>
            <Badge variant="muted">MCQ</Badge>
            <Badge variant="outline">Numérique</Badge>
            <Badge variant="destructive">Raté</Badge>
          </div>
        </Section>

        {/* ── Callouts ── */}
        <Section title="Callouts">
          <div className="flex flex-col gap-2">
            <Callout variant="info" title="Conseil">
              Les chiffres tabulaires garantissent l&apos;alignement des colonnes
              dans les états financiers.
            </Callout>
            <Callout variant="success" title="Importation réussie">
              8 exercices chargés — idempotence confirmée.
            </Callout>
            <Callout variant="warning" title="Attention">
              La clé externe doit être unique par lot d&apos;ingestion.
            </Callout>
            <Callout variant="error" title="Erreur de validation">
              Le schéma Zod a rejeté 1 item — vérifiez les champs
              payload.options.
            </Callout>
          </div>
        </Section>

        {/* ── Table ── */}
        <Section title="Table — Tabular Figures">
          <Table>
            <TableCaption>Performance par trimestre (données fictives)</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>Métrique</TableHead>
                <TableHead className="text-right">Q1 2024</TableHead>
                <TableHead className="text-right">Q2 2024</TableHead>
                <TableHead className="text-right">Q3 2024</TableHead>
                <TableHead>Statut</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {SAMPLE_ROWS.map((row) => (
                <TableRow key={row.metric}>
                  <TableCell className="font-medium">{row.metric}</TableCell>
                  <TableCell className="text-right font-mono">{row.q1}</TableCell>
                  <TableCell className="text-right font-mono">{row.q2}</TableCell>
                  <TableCell className="text-right font-mono">{row.q3}</TableCell>
                  <TableCell>
                    <Badge
                      variant={row.status === "On Track" ? "default" : "accent"}
                    >
                      {row.status}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Section>
      </div>
    </main>
  );
}
