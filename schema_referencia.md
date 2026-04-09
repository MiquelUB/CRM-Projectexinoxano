# Esquema de Referència Supabase (DDL)

Aquest fitxer conté l'esquema de dades real de Supabase proporcionat per a la referència de relacions i ordres de càrrega.

```sql
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.alembic_version (
  version_num character varying NOT NULL,
  CONSTRAINT alembic_version_pkey PRIMARY KEY (version_num)
);

CREATE TABLE public.contactes (
  id uuid NOT NULL,
  municipi_id uuid NOT NULL,
  nom character varying NOT NULL,
  carrec character varying,
  email character varying,
  telefon character varying,
  linkedin character varying,
  notes_humanes text,
  actiu boolean,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT contactes_pkey PRIMARY KEY (id),
  CONSTRAINT contactes_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis(id)
);

CREATE TABLE public.contactes_v2 (
  id uuid NOT NULL,
  municipi_id uuid NOT NULL,
  nom character varying NOT NULL,
  carrec USER-DEFINED NOT NULL,
  email character varying,
  telefon character varying,
  actiu boolean,
  principal boolean,
  angles_exitosos jsonb,
  angles_fallits jsonb,
  moment_optimal character varying,
  to_preferit USER-DEFINED,
  data_creacio timestamp with time zone DEFAULT now(),
  CONSTRAINT contactes_v2_pkey PRIMARY KEY (id),
  CONSTRAINT contactes_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id)
);

CREATE TABLE public.deal_activitats (
  id uuid NOT NULL,
  deal_id uuid NOT NULL,
  tipus character varying NOT NULL,
  descripcio text NOT NULL,
  valor_anterior character varying,
  valor_nou character varying,
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT deal_activitats_pkey PRIMARY KEY (id),
  CONSTRAINT deal_activitats_deal_id_fkey FOREIGN KEY (deal_id) REFERENCES public.deals(id)
);

CREATE TABLE public.deals (
  id uuid NOT NULL,
  municipi_id uuid NOT NULL,
  contacte_id uuid,
  titol character varying NOT NULL,
  etapa character varying NOT NULL,
  valor_setup numeric,
  valor_llicencia numeric,
  prioritat character varying,
  notes_humanes text,
  proper_pas text,
  data_seguiment date,
  data_tancament_prev date,
  data_tancament_real date,
  motiu_perdua text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT deals_pkey PRIMARY KEY (id),
  CONSTRAINT deals_contacte_id_fkey FOREIGN KEY (contacte_id) REFERENCES public.contactes(id),
  CONSTRAINT deals_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis(id)
);

CREATE TABLE public.email_drafts_v2 (
  id uuid NOT NULL,
  municipi_id uuid NOT NULL,
  contacte_id uuid,
  estat USER-DEFINED,
  subject character varying,
  cos text,
  generat_per_ia boolean,
  prompt_utilitzat text,
  variants_generades jsonb,
  variant_seleccionada integer,
  editat_per_usuari boolean,
  canvis_respecte_ia jsonb,
  data_enviament timestamp with time zone,
  enviat_des_de character varying,
  email_enviat_id uuid,
  data_creacio timestamp with time zone DEFAULT now(),
  CONSTRAINT email_drafts_v2_pkey PRIMARY KEY (id),
  CONSTRAINT email_drafts_v2_contacte_id_fkey FOREIGN KEY (contacte_id) REFERENCES public.contactes_v2(id),
  CONSTRAINT email_drafts_v2_email_enviat_id_fkey FOREIGN KEY (email_enviat_id) REFERENCES public.emails_v2(id),
  CONSTRAINT email_drafts_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id)
);

CREATE TABLE public.email_sequencies_v2 (
  id uuid NOT NULL,
  municipi_id uuid NOT NULL,
  numero_email integer NOT NULL,
  tipus_sequencia USER-DEFINED NOT NULL,
  estat USER-DEFINED,
  data_programada timestamp with time zone,
  data_enviada timestamp with time zone,
  draft_id uuid,
  obert boolean,
  data_obertura timestamp with time zone,
  respost boolean,
  seguent_accio character varying,
  CONSTRAINT email_sequencies_v2_pkey PRIMARY KEY (id),
  CONSTRAINT email_sequencies_v2_draft_id_fkey FOREIGN KEY (draft_id) REFERENCES public.email_drafts_v2(id),
  CONSTRAINT email_sequencies_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id)
);

CREATE TABLE public.emails (
  id uuid NOT NULL,
  deal_id uuid,
  contacte_id uuid,
  campanya_id uuid,
  from_address character varying NOT NULL,
  to_address character varying NOT NULL,
  assumpte character varying NOT NULL,
  cos text,
  direccio character varying NOT NULL,
  llegit boolean,
  sincronitzat boolean,
  message_id_extern character varying UNIQUE,
  data_email timestamp with time zone NOT NULL,
  created_at timestamp with time zone DEFAULT now(),
  tracking_token character varying UNIQUE,
  obert boolean,
  data_obertura timestamp with time zone,
  nombre_obertures integer,
  ip_obertura character varying,
  CONSTRAINT emails_pkey PRIMARY KEY (id),
  CONSTRAINT emails_contacte_id_fkey FOREIGN KEY (contacte_id) REFERENCES public.contactes(id),
  CONSTRAINT emails_deal_id_fkey FOREIGN KEY (deal_id) REFERENCES public.deals(id)
);

CREATE TABLE public.emails_v2 (
  id uuid NOT NULL,
  municipi_id uuid NOT NULL,
  data_enviament timestamp with time zone DEFAULT now(),
  assumpte character varying,
  cos text,
  obert boolean,
  data_obertura timestamp with time zone,
  cops_obert integer,
  respost boolean,
  data_resposta timestamp with time zone,
  sentiment_resposta USER-DEFINED,
  intents_detectats jsonb,
  actor_probable USER-DEFINED,
  CONSTRAINT emails_v2_pkey PRIMARY KEY (id),
  CONSTRAINT emails_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id)
);

CREATE TABLE public.llicencies (
  id uuid NOT NULL,
  deal_id uuid NOT NULL UNIQUE,
  data_inici date NOT NULL,
  data_renovacio date NOT NULL,
  estat character varying,
  notes text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT llicencies_pkey PRIMARY KEY (id),
  CONSTRAINT llicencies_deal_id_fkey FOREIGN KEY (deal_id) REFERENCES public.deals(id)
);

CREATE TABLE public.memoria_municipis (
  municipi_id uuid NOT NULL,
  ganxos_exitosos jsonb,
  angles_fallits jsonb,
  moment_optimal jsonb,
  llenguatge_preferit jsonb,
  blockers_resolts jsonb,
  data_actualitzacio timestamp with time zone DEFAULT now(),
  CONSTRAINT memoria_municipis_pkey PRIMARY KEY (municipi_id),
  CONSTRAINT memoria_municipis_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id)
);

CREATE TABLE public.municipis (
  id uuid NOT NULL,
  nom character varying NOT NULL,
  tipus character varying NOT NULL,
  provincia character varying,
  poblacio character varying,
  web character varying,
  telefon character varying,
  adreca text,
  notes text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  codi_postal character varying,
  CONSTRAINT municipis_pkey PRIMARY KEY (id)
);

CREATE TABLE public.municipis_lifecycle (
  id uuid NOT NULL,
  nom character varying NOT NULL,
  comarca character varying,
  poblacio integer,
  geografia USER-DEFINED,
  diagnostic_digital jsonb,
  angle_personalitzacio text,
  etapa_actual USER-DEFINED,
  historial_etapes jsonb,
  blocker_actual USER-DEFINED,
  temperatura USER-DEFINED,
  dies_etapa_actual integer,
  data_conversio timestamp without time zone,
  pla_contractat USER-DEFINED,
  estat_final USER-DEFINED,
  actor_principal_id uuid,
  data_creacio timestamp with time zone DEFAULT now(),
  data_ultima_accio timestamp with time zone DEFAULT now(),
  usuari_asignat character varying,
  CONSTRAINT municipis_lifecycle_pkey PRIMARY KEY (id),
  CONSTRAINT fk_municipi_actor_principal FOREIGN KEY (actor_principal_id) REFERENCES public.contactes_v2(id)
);

CREATE TABLE public.pagaments (
  id uuid NOT NULL,
  llicencia_id uuid NOT NULL,
  import numeric NOT NULL,
  tipus character varying NOT NULL,
  estat character varying,
  data_emisio date NOT NULL,
  data_limit date,
  data_confirmacio date,
  notes text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT pagaments_pkey PRIMARY KEY (id),
  CONSTRAINT pagaments_llicencia_id_fkey FOREIGN KEY (llicencia_id) REFERENCES public.llicencies(id)
);

CREATE TABLE public.patrons_municipis (
  id uuid NOT NULL,
  rang_poblacio character varying,
  tipus_geografia USER-DEFINED,
  context_politic character varying,
  probabilitat_conversio double precision,
  temps_mitja_cicle_dies integer,
  etapa_bloqueig_frequent character varying,
  estrategia_recomanada text,
  objeccions_frequents jsonb,
  casos_exit_referencia jsonb,
  cops_aplicat integer,
  exitosos integer,
  CONSTRAINT patrons_municipis_pkey PRIMARY KEY (id)
);

CREATE TABLE public.reunions_v2 (
  id uuid NOT NULL,
  municipi_id uuid NOT NULL,
  data timestamp with time zone,
  tipus character varying,
  assistents jsonb,
  aar_completat boolean,
  notes_aar text,
  poi_mes_reaccio character varying,
  objeccio_principal character varying,
  cta_final character varying,
  temperatura_post USER-DEFINED,
  CONSTRAINT reunions_v2_pkey PRIMARY KEY (id),
  CONSTRAINT reunions_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id)
);

CREATE TABLE public.tasques (
  id uuid NOT NULL,
  deal_id uuid,
  contacte_id uuid,
  municipi_id uuid,
  usuari_id uuid,
  titol character varying NOT NULL,
  descripcio text,
  data_venciment date NOT NULL,
  tipus character varying,
  prioritat character varying,
  estat character varying,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT tasques_pkey PRIMARY KEY (id),
  CONSTRAINT tasques_contacte_id_fkey FOREIGN KEY (contacte_id) REFERENCES public.contactes(id),
  CONSTRAINT tasques_deal_id_fkey FOREIGN KEY (deal_id) REFERENCES public.deals(id),
  CONSTRAINT tasques_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis(id),
  CONSTRAINT tasques_usuari_id_fkey FOREIGN KEY (usuari_id) REFERENCES public.usuaris(id)
);

CREATE TABLE public.trucades_v2 (
  id uuid NOT NULL,
  municipi_id uuid NOT NULL,
  data timestamp with time zone DEFAULT now(),
  durada_minuts integer,
  qui_va_contestar USER-DEFINED,
  notes_breus text,
  resum_ia text,
  seguent_accio_sugerida text,
  CONSTRAINT trucades_v2_pkey PRIMARY KEY (id),
  CONSTRAINT trucades_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id)
);

CREATE TABLE public.usuaris (
  id uuid NOT NULL,
  email character varying NOT NULL UNIQUE,
  password_hash character varying NOT NULL,
  nom character varying NOT NULL,
  rol character varying,
  actiu boolean,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT usuaris_pkey PRIMARY KEY (id)
);

CREATE TABLE public.activitats_municipi (
  id uuid NOT NULL,
  municipi_id uuid NOT NULL,
  contacte_id uuid,
  deal_id uuid,
  tipus_activitat character varying NOT NULL, -- ENUM (nota_manual, email_enviat, trucada, etc.)
  data_activitat timestamp with time zone DEFAULT now(),
  contingut jsonb,
  notes_comercial text,
  generat_per_ia boolean DEFAULT false,
  etiquetes text[], -- ARRAY[TEXT]
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT activitats_municipi_pkey PRIMARY KEY (id),
  CONSTRAINT activitats_municipi_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id),
  CONSTRAINT activitats_municipi_contacte_id_fkey FOREIGN KEY (contacte_id) REFERENCES public.contactes_v2(id)
);
```
