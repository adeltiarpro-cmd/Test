-- Liste blanche d'invitations — seul moyen de s'inscrire
CREATE TABLE invitations (
  id         uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  email      text        UNIQUE NOT NULL,
  invited_at timestamptz DEFAULT now(),
  used_at    timestamptz              -- rempli au moment de l'inscription
);

-- Trigger : refuse toute inscription dont l'email n'est pas dans invitations
CREATE OR REPLACE FUNCTION public.check_invitation()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM public.invitations
    WHERE email = NEW.email AND used_at IS NULL
  ) THEN
    RAISE EXCEPTION 'Access denied: email % has not been invited', NEW.email
      USING ERRCODE = 'P0001';
  END IF;

  -- Marque l'invitation comme utilisée
  UPDATE public.invitations
  SET used_at = now()
  WHERE email = NEW.email;

  RETURN NEW;
END;
$$;

CREATE TRIGGER enforce_invitation_on_signup
  BEFORE INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.check_invitation();
