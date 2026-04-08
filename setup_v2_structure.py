import psycopg2

DB_URL = "postgresql://pxx_admin:b86f95465942a859661e@178.104.83.189:5432/crm_pxx?sslmode=disable"

def setup_v2_structure():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("🛠️ Creant tipus personalitzats (Enums)...")
        enums = {
            "geografia": ["muntanya", "mar", "interior", "city"],
            "etapa_funnel": ["research", "contacte", "demo_pendent", "demo_ok", "oferta", "documentacio", "aprovacio", "contracte", "client", "pausa", "perdut"],
            "blocker": ["alcalde", "tecnic", "cfo", "temporitzacio", "cap"],
            "temperatura": ["fred", "templat", "calent", "bullent"],
            "pla": ["Roure", "Mirador", "Territori"],
            "estat_final": ["client", "perdut", "pausa"],
            "carrec": ["alcalde", "regidor_turisme", "tecnic", "cfo", "regidor_cultura", "altre"],
            "to_comunicacio": ["formal", "proxim", "tecnic"],
            "sentiment": ["positiu", "neutre", "negatiu", "confus"],
            "actor": ["alcalde", "tecnic", "cfo"],
            "actor_respuesta": ["alcalde", "tecnic", "cfo"], # Repetit per consistència amb models
            "estat_draft": ["esborrany", "revisat", "enviat", "programat"],
            "tipus_sequencia": ["prospeccio", "seguiment", "nurture", "recuperacio"],
            "estat_sequencia": ["pendent", "preparant", "preparat", "programat", "enviat", "obert", "respost", "no_obert", "cancelat"],
            "temperatura_post": ["fred", "templat", "calent", "bullent"],
            "geografia_patro": ["muntanya", "mar", "interior", "city"]
        }

        for name, values in enums.items():
            vals_str = ", ".join([f"'{v}'" for v in values])
            cur.execute(f"DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = '{name}') THEN CREATE TYPE {name} AS ENUM ({vals_str}); END IF; END $$;")

        print("🔥 Netejant taules v2 existents (CASCADE)...")
        tables_to_drop = [
            "patrons_municipis", "memoria_municipis", "email_sequencies_v2", 
            "email_drafts_v2", "reunions_v2", "trucades_v2", "emails_v2", 
            "contactes_v2", "municipis_lifecycle"
        ]
        for table in tables_to_drop:
            cur.execute(f"DROP TABLE IF EXISTS public.{table} CASCADE")

        print("🏗️ Creant municipis_lifecycle...")
        cur.execute("""
            CREATE TABLE public.municipis_lifecycle (
              id uuid NOT NULL DEFAULT gen_random_uuid(),
              nom character varying(100) NOT NULL,
              comarca character varying(50),
              poblacio integer,
              geografia geografia,
              diagnostic_digital jsonb DEFAULT '{}',
              angle_personalitzacio text,
              etapa_actual etapa_funnel DEFAULT 'research',
              historial_etapes jsonb DEFAULT '[]',
              blocker_actual blocker DEFAULT 'cap',
              temperatura temperatura DEFAULT 'fred',
              dies_etapa_actual integer DEFAULT 0,
              data_conversio timestamp without time zone,
              pla_contractat pla,
              estat_final estat_final,
              actor_principal_id uuid,
              data_creacio timestamp with time zone DEFAULT now(),
              data_ultima_accio timestamp with time zone DEFAULT now(),
              usuari_asignat character varying(50) DEFAULT 'fundador',
              CONSTRAINT municipis_lifecycle_pkey PRIMARY KEY (id)
            )
        """)

        print("🏗️ Creant contactes_v2...")
        cur.execute("""
            CREATE TABLE public.contactes_v2 (
              id uuid NOT NULL DEFAULT gen_random_uuid(),
              municipi_id uuid NOT NULL,
              nom character varying(100) NOT NULL,
              carrec carrec NOT NULL,
              email character varying(100),
              telefon character varying(20),
              actiu boolean DEFAULT true,
              principal boolean DEFAULT false,
              angles_exitosos jsonb DEFAULT '[]',
              angles_fallits jsonb DEFAULT '[]',
              moment_optimal character varying(10),
              to_preferit to_comunicacio,
              data_creacio timestamp with time zone DEFAULT now(),
              CONSTRAINT contactes_v2_pkey PRIMARY KEY (id),
              CONSTRAINT contactes_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id)
            )
        """)

        # Add FK to municipis_lifecycle now that contactes_v2 exists
        cur.execute("ALTER TABLE public.municipis_lifecycle ADD CONSTRAINT fk_municipi_actor_principal FOREIGN KEY (actor_principal_id) REFERENCES public.contactes_v2(id)")

        print("🏗️ Creant emails_v2...")
        cur.execute("""
            CREATE TABLE public.emails_v2 (
              id uuid NOT NULL DEFAULT gen_random_uuid(),
              municipi_id uuid NOT NULL,
              data_enviament timestamp with time zone DEFAULT now(),
              assumpte character varying(200),
              cos text,
              obert boolean DEFAULT false,
              data_obertura timestamp with time zone,
              cops_obert integer DEFAULT 0,
              respost boolean DEFAULT false,
              data_resposta timestamp with time zone,
              sentiment_resposta sentiment,
              intents_detectats jsonb DEFAULT '[]',
              actor_probable actor,
              CONSTRAINT emails_v2_pkey PRIMARY KEY (id),
              CONSTRAINT emails_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id)
            )
        """)

        print("🏗️ Creant trucades_v2...")
        cur.execute("""
            CREATE TABLE public.trucades_v2 (
              id uuid NOT NULL DEFAULT gen_random_uuid(),
              municipi_id uuid NOT NULL,
              data timestamp with time zone DEFAULT now(),
              durada_minuts integer DEFAULT 0,
              qui_va_contestar actor_respuesta,
              notes_breus text,
              resum_ia text,
              seguent_accio_sugerida text,
              CONSTRAINT trucades_v2_pkey PRIMARY KEY (id),
              CONSTRAINT trucades_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id)
            )
        """)

        print("🏗️ Creant reunions_v2...")
        cur.execute("""
            CREATE TABLE public.reunions_v2 (
              id uuid NOT NULL DEFAULT gen_random_uuid(),
              municipi_id uuid NOT NULL,
              data timestamp with time zone,
              tipus character varying(20),
              assistents jsonb DEFAULT '[]',
              aar_completat boolean DEFAULT false,
              notes_aar text,
              poi_mes_reaccio character varying(100),
              objeccio_principal character varying(100),
              cta_final character varying(200),
              temperatura_post temperatura_post,
              CONSTRAINT reunions_v2_pkey PRIMARY KEY (id),
              CONSTRAINT reunions_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id)
            )
        """)

        print("🏗️ Creant email_drafts_v2...")
        cur.execute("""
            CREATE TABLE public.email_drafts_v2 (
              id uuid NOT NULL DEFAULT gen_random_uuid(),
              municipi_id uuid NOT NULL,
              contacte_id uuid,
              estat estat_draft DEFAULT 'esborrany',
              subject character varying(200),
              cos text,
              generat_per_ia boolean DEFAULT true,
              prompt_utilitzat text,
              variants_generades jsonb DEFAULT '[]',
              variant_seleccionada integer DEFAULT 0,
              editat_per_usuari boolean DEFAULT false,
              canvis_respecte_ia jsonb DEFAULT '{}',
              data_enviament timestamp with time zone,
              enviat_des_de character varying(100),
              email_enviat_id uuid,
              data_creacio timestamp with time zone DEFAULT now(),
              CONSTRAINT email_drafts_v2_pkey PRIMARY KEY (id),
              CONSTRAINT email_drafts_v2_contacte_id_fkey FOREIGN KEY (contacte_id) REFERENCES public.contactes_v2(id),
              CONSTRAINT email_drafts_v2_email_enviat_id_fkey FOREIGN KEY (email_enviat_id) REFERENCES public.emails_v2(id),
              CONSTRAINT email_drafts_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id)
            )
        """)

        print("🏗️ Creant email_sequencies_v2...")
        cur.execute("""
            CREATE TABLE public.email_sequencies_v2 (
              id uuid NOT NULL DEFAULT gen_random_uuid(),
              municipi_id uuid NOT NULL,
              numero_email integer NOT NULL,
              tipus_sequencia tipus_sequencia NOT NULL,
              estat estat_sequencia DEFAULT 'pendent',
              data_programada timestamp with time zone,
              data_enviada timestamp with time zone,
              draft_id uuid,
              obert boolean DEFAULT false,
              data_obertura timestamp with time zone,
              respost boolean DEFAULT false,
              seguent_accio character varying(50),
              CONSTRAINT email_sequencies_v2_pkey PRIMARY KEY (id),
              CONSTRAINT email_sequencies_v2_draft_id_fkey FOREIGN KEY (draft_id) REFERENCES public.email_drafts_v2(id),
              CONSTRAINT email_sequencies_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id)
            )
        """)

        print("🏗️ Creant memoria_municipis...")
        cur.execute("""
            CREATE TABLE public.memoria_municipis (
              municipi_id uuid NOT NULL,
              ganxos_exitosos jsonb DEFAULT '[]',
              angles_fallits jsonb DEFAULT '[]',
              moment_optimal jsonb DEFAULT '{}',
              llenguatge_preferit jsonb DEFAULT '[]',
              blockers_resolts jsonb DEFAULT '[]',
              data_actualitzacio timestamp with time zone DEFAULT now(),
              CONSTRAINT memoria_municipis_pkey PRIMARY KEY (municipi_id),
              CONSTRAINT memoria_municipis_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id)
            )
        """)

        print("🏗️ Creant patrons_municipis...")
        cur.execute("""
            CREATE TABLE public.patrons_municipis (
              id uuid NOT NULL DEFAULT gen_random_uuid(),
              rang_poblacio character varying(20),
              tipus_geografia geografia_patro,
              context_politic character varying(20),
              probabilitat_conversio float DEFAULT 0.0,
              temps_mitja_cicle_dies integer DEFAULT 0,
              etapa_bloqueig_frequent character varying(50),
              estrategia_recomanada text,
              objeccions_frequents jsonb DEFAULT '[]',
              casos_exit_referencia jsonb DEFAULT '[]',
              cops_aplicat integer DEFAULT 0,
              exitosos integer DEFAULT 0,
              CONSTRAINT patrons_municipis_pkey PRIMARY KEY (id)
            )
        """)

        conn.commit()
        print("✨ TOTA L'ESTRUCTURA V2 S'HA CREAT AMB ÈXIT!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    setup_v2_structure()
