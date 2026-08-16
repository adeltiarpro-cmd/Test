-- Sources de contenu (livres, PDFs, vidéos...)
CREATE TABLE sources (
  id           uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  kind         text        NOT NULL,        -- 'book' | 'pdf' | 'video' | 'internal'
  title        text        NOT NULL,
  storage_path text,                        -- chemin dans Supabase Storage (nullable)
  meta         jsonb       NOT NULL DEFAULT '{}',
  created_at   timestamptz DEFAULT now()
);
