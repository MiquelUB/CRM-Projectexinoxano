--
-- PostgreSQL database dump
--

\restrict 44sexrYUT6xFQcbkGtCnoPzvMXfV1dnslygQVLhnBLRk93CNfX7uNpjC9qpmgGH

-- Dumped from database version 17.6
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: auth; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA auth;


--
-- Name: extensions; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA extensions;


--
-- Name: graphql; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA graphql;


--
-- Name: graphql_public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA graphql_public;


--
-- Name: pgbouncer; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA pgbouncer;


--
-- Name: realtime; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA realtime;


--
-- Name: storage; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA storage;


--
-- Name: vault; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA vault;


--
-- Name: pg_graphql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_graphql WITH SCHEMA graphql;


--
-- Name: EXTENSION pg_graphql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pg_graphql IS 'pg_graphql: GraphQL support';


--
-- Name: pg_stat_statements; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA extensions;


--
-- Name: EXTENSION pg_stat_statements; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pg_stat_statements IS 'track planning and execution statistics of all SQL statements executed';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA extensions;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: supabase_vault; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS supabase_vault WITH SCHEMA vault;


--
-- Name: EXTENSION supabase_vault; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION supabase_vault IS 'Supabase Vault Extension';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA extensions;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: aal_level; Type: TYPE; Schema: auth; Owner: -
--

CREATE TYPE auth.aal_level AS ENUM (
    'aal1',
    'aal2',
    'aal3'
);


--
-- Name: code_challenge_method; Type: TYPE; Schema: auth; Owner: -
--

CREATE TYPE auth.code_challenge_method AS ENUM (
    's256',
    'plain'
);


--
-- Name: factor_status; Type: TYPE; Schema: auth; Owner: -
--

CREATE TYPE auth.factor_status AS ENUM (
    'unverified',
    'verified'
);


--
-- Name: factor_type; Type: TYPE; Schema: auth; Owner: -
--

CREATE TYPE auth.factor_type AS ENUM (
    'totp',
    'webauthn',
    'phone'
);


--
-- Name: oauth_authorization_status; Type: TYPE; Schema: auth; Owner: -
--

CREATE TYPE auth.oauth_authorization_status AS ENUM (
    'pending',
    'approved',
    'denied',
    'expired'
);


--
-- Name: oauth_client_type; Type: TYPE; Schema: auth; Owner: -
--

CREATE TYPE auth.oauth_client_type AS ENUM (
    'public',
    'confidential'
);


--
-- Name: oauth_registration_type; Type: TYPE; Schema: auth; Owner: -
--

CREATE TYPE auth.oauth_registration_type AS ENUM (
    'dynamic',
    'manual'
);


--
-- Name: oauth_response_type; Type: TYPE; Schema: auth; Owner: -
--

CREATE TYPE auth.oauth_response_type AS ENUM (
    'code'
);


--
-- Name: one_time_token_type; Type: TYPE; Schema: auth; Owner: -
--

CREATE TYPE auth.one_time_token_type AS ENUM (
    'confirmation_token',
    'reauthentication_token',
    'recovery_token',
    'email_change_token_new',
    'email_change_token_current',
    'phone_change_token'
);


--
-- Name: actor; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.actor AS ENUM (
    'alcalde',
    'tecnic',
    'cfo'
);


--
-- Name: actor_respuesta; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.actor_respuesta AS ENUM (
    'alcalde',
    'tecnic',
    'cfo'
);


--
-- Name: blocker; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.blocker AS ENUM (
    'alcalde',
    'tecnic',
    'cfo',
    'temporitzacio',
    'cap'
);


--
-- Name: carrec; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.carrec AS ENUM (
    'alcalde',
    'regidor_turisme',
    'tecnic',
    'cfo',
    'regidor_cultura',
    'altre'
);


--
-- Name: estat_draft; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.estat_draft AS ENUM (
    'esborrany',
    'revisat',
    'enviat',
    'programat'
);


--
-- Name: estat_final; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.estat_final AS ENUM (
    'client',
    'perdut',
    'pausa'
);


--
-- Name: estat_sequencia; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.estat_sequencia AS ENUM (
    'pendent',
    'preparant',
    'preparat',
    'programat',
    'enviat',
    'obert',
    'respost',
    'no_obert',
    'cancelat'
);


--
-- Name: etapa_funnel; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.etapa_funnel AS ENUM (
    'research',
    'contacte',
    'demo_pendent',
    'demo_ok',
    'oferta',
    'documentacio',
    'aprovacio',
    'contracte',
    'client',
    'pausa',
    'perdut'
);


--
-- Name: geografia; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.geografia AS ENUM (
    'muntanya',
    'mar',
    'interior',
    'city'
);


--
-- Name: geografia_patro; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.geografia_patro AS ENUM (
    'muntanya',
    'mar',
    'interior',
    'city'
);


--
-- Name: pla; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.pla AS ENUM (
    'Roure',
    'Mirador',
    'Territori'
);


--
-- Name: sentiment; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.sentiment AS ENUM (
    'positiu',
    'neutre',
    'negatiu',
    'confus'
);


--
-- Name: temperatura; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.temperatura AS ENUM (
    'fred',
    'templat',
    'calent',
    'bullent'
);


--
-- Name: temperatura_post; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.temperatura_post AS ENUM (
    'fred',
    'templat',
    'calent',
    'bullent'
);


--
-- Name: tipus_sequencia; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tipus_sequencia AS ENUM (
    'prospeccio',
    'seguiment',
    'nurture',
    'recuperacio'
);


--
-- Name: to_comunicacio; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.to_comunicacio AS ENUM (
    'formal',
    'proxim',
    'tecnic'
);


--
-- Name: action; Type: TYPE; Schema: realtime; Owner: -
--

CREATE TYPE realtime.action AS ENUM (
    'INSERT',
    'UPDATE',
    'DELETE',
    'TRUNCATE',
    'ERROR'
);


--
-- Name: equality_op; Type: TYPE; Schema: realtime; Owner: -
--

CREATE TYPE realtime.equality_op AS ENUM (
    'eq',
    'neq',
    'lt',
    'lte',
    'gt',
    'gte',
    'in'
);


--
-- Name: user_defined_filter; Type: TYPE; Schema: realtime; Owner: -
--

CREATE TYPE realtime.user_defined_filter AS (
	column_name text,
	op realtime.equality_op,
	value text
);


--
-- Name: wal_column; Type: TYPE; Schema: realtime; Owner: -
--

CREATE TYPE realtime.wal_column AS (
	name text,
	type_name text,
	type_oid oid,
	value jsonb,
	is_pkey boolean,
	is_selectable boolean
);


--
-- Name: wal_rls; Type: TYPE; Schema: realtime; Owner: -
--

CREATE TYPE realtime.wal_rls AS (
	wal jsonb,
	is_rls_enabled boolean,
	subscription_ids uuid[],
	errors text[]
);


--
-- Name: buckettype; Type: TYPE; Schema: storage; Owner: -
--

CREATE TYPE storage.buckettype AS ENUM (
    'STANDARD',
    'ANALYTICS',
    'VECTOR'
);


--
-- Name: email(); Type: FUNCTION; Schema: auth; Owner: -
--

CREATE FUNCTION auth.email() RETURNS text
    LANGUAGE sql STABLE
    AS $$
  select 
  coalesce(
    nullif(current_setting('request.jwt.claim.email', true), ''),
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'email')
  )::text
$$;


--
-- Name: FUNCTION email(); Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON FUNCTION auth.email() IS 'Deprecated. Use auth.jwt() -> ''email'' instead.';


--
-- Name: jwt(); Type: FUNCTION; Schema: auth; Owner: -
--

CREATE FUNCTION auth.jwt() RETURNS jsonb
    LANGUAGE sql STABLE
    AS $$
  select 
    coalesce(
        nullif(current_setting('request.jwt.claim', true), ''),
        nullif(current_setting('request.jwt.claims', true), '')
    )::jsonb
$$;


--
-- Name: role(); Type: FUNCTION; Schema: auth; Owner: -
--

CREATE FUNCTION auth.role() RETURNS text
    LANGUAGE sql STABLE
    AS $$
  select 
  coalesce(
    nullif(current_setting('request.jwt.claim.role', true), ''),
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'role')
  )::text
$$;


--
-- Name: FUNCTION role(); Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON FUNCTION auth.role() IS 'Deprecated. Use auth.jwt() -> ''role'' instead.';


--
-- Name: uid(); Type: FUNCTION; Schema: auth; Owner: -
--

CREATE FUNCTION auth.uid() RETURNS uuid
    LANGUAGE sql STABLE
    AS $$
  select 
  coalesce(
    nullif(current_setting('request.jwt.claim.sub', true), ''),
    (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'sub')
  )::uuid
$$;


--
-- Name: FUNCTION uid(); Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON FUNCTION auth.uid() IS 'Deprecated. Use auth.jwt() -> ''sub'' instead.';


--
-- Name: grant_pg_cron_access(); Type: FUNCTION; Schema: extensions; Owner: -
--

CREATE FUNCTION extensions.grant_pg_cron_access() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF EXISTS (
    SELECT
    FROM pg_event_trigger_ddl_commands() AS ev
    JOIN pg_extension AS ext
    ON ev.objid = ext.oid
    WHERE ext.extname = 'pg_cron'
  )
  THEN
    grant usage on schema cron to postgres with grant option;

    alter default privileges in schema cron grant all on tables to postgres with grant option;
    alter default privileges in schema cron grant all on functions to postgres with grant option;
    alter default privileges in schema cron grant all on sequences to postgres with grant option;

    alter default privileges for user supabase_admin in schema cron grant all
        on sequences to postgres with grant option;
    alter default privileges for user supabase_admin in schema cron grant all
        on tables to postgres with grant option;
    alter default privileges for user supabase_admin in schema cron grant all
        on functions to postgres with grant option;

    grant all privileges on all tables in schema cron to postgres with grant option;
    revoke all on table cron.job from postgres;
    grant select on table cron.job to postgres with grant option;
  END IF;
END;
$$;


--
-- Name: FUNCTION grant_pg_cron_access(); Type: COMMENT; Schema: extensions; Owner: -
--

COMMENT ON FUNCTION extensions.grant_pg_cron_access() IS 'Grants access to pg_cron';


--
-- Name: grant_pg_graphql_access(); Type: FUNCTION; Schema: extensions; Owner: -
--

CREATE FUNCTION extensions.grant_pg_graphql_access() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $_$
DECLARE
    func_is_graphql_resolve bool;
BEGIN
    func_is_graphql_resolve = (
        SELECT n.proname = 'resolve'
        FROM pg_event_trigger_ddl_commands() AS ev
        LEFT JOIN pg_catalog.pg_proc AS n
        ON ev.objid = n.oid
    );

    IF func_is_graphql_resolve
    THEN
        -- Update public wrapper to pass all arguments through to the pg_graphql resolve func
        DROP FUNCTION IF EXISTS graphql_public.graphql;
        create or replace function graphql_public.graphql(
            "operationName" text default null,
            query text default null,
            variables jsonb default null,
            extensions jsonb default null
        )
            returns jsonb
            language sql
        as $$
            select graphql.resolve(
                query := query,
                variables := coalesce(variables, '{}'),
                "operationName" := "operationName",
                extensions := extensions
            );
        $$;

        -- This hook executes when `graphql.resolve` is created. That is not necessarily the last
        -- function in the extension so we need to grant permissions on existing entities AND
        -- update default permissions to any others that are created after `graphql.resolve`
        grant usage on schema graphql to postgres, anon, authenticated, service_role;
        grant select on all tables in schema graphql to postgres, anon, authenticated, service_role;
        grant execute on all functions in schema graphql to postgres, anon, authenticated, service_role;
        grant all on all sequences in schema graphql to postgres, anon, authenticated, service_role;
        alter default privileges in schema graphql grant all on tables to postgres, anon, authenticated, service_role;
        alter default privileges in schema graphql grant all on functions to postgres, anon, authenticated, service_role;
        alter default privileges in schema graphql grant all on sequences to postgres, anon, authenticated, service_role;

        -- Allow postgres role to allow granting usage on graphql and graphql_public schemas to custom roles
        grant usage on schema graphql_public to postgres with grant option;
        grant usage on schema graphql to postgres with grant option;
    END IF;

END;
$_$;


--
-- Name: FUNCTION grant_pg_graphql_access(); Type: COMMENT; Schema: extensions; Owner: -
--

COMMENT ON FUNCTION extensions.grant_pg_graphql_access() IS 'Grants access to pg_graphql';


--
-- Name: grant_pg_net_access(); Type: FUNCTION; Schema: extensions; Owner: -
--

CREATE FUNCTION extensions.grant_pg_net_access() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM pg_event_trigger_ddl_commands() AS ev
    JOIN pg_extension AS ext
    ON ev.objid = ext.oid
    WHERE ext.extname = 'pg_net'
  )
  THEN
    IF NOT EXISTS (
      SELECT 1
      FROM pg_roles
      WHERE rolname = 'supabase_functions_admin'
    )
    THEN
      CREATE USER supabase_functions_admin NOINHERIT CREATEROLE LOGIN NOREPLICATION;
    END IF;

    GRANT USAGE ON SCHEMA net TO supabase_functions_admin, postgres, anon, authenticated, service_role;

    IF EXISTS (
      SELECT FROM pg_extension
      WHERE extname = 'pg_net'
      -- all versions in use on existing projects as of 2025-02-20
      -- version 0.12.0 onwards don't need these applied
      AND extversion IN ('0.2', '0.6', '0.7', '0.7.1', '0.8', '0.10.0', '0.11.0')
    ) THEN
      ALTER function net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) SECURITY DEFINER;
      ALTER function net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) SECURITY DEFINER;

      ALTER function net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) SET search_path = net;
      ALTER function net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) SET search_path = net;

      REVOKE ALL ON FUNCTION net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) FROM PUBLIC;
      REVOKE ALL ON FUNCTION net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) FROM PUBLIC;

      GRANT EXECUTE ON FUNCTION net.http_get(url text, params jsonb, headers jsonb, timeout_milliseconds integer) TO supabase_functions_admin, postgres, anon, authenticated, service_role;
      GRANT EXECUTE ON FUNCTION net.http_post(url text, body jsonb, params jsonb, headers jsonb, timeout_milliseconds integer) TO supabase_functions_admin, postgres, anon, authenticated, service_role;
    END IF;
  END IF;
END;
$$;


--
-- Name: FUNCTION grant_pg_net_access(); Type: COMMENT; Schema: extensions; Owner: -
--

COMMENT ON FUNCTION extensions.grant_pg_net_access() IS 'Grants access to pg_net';


--
-- Name: pgrst_ddl_watch(); Type: FUNCTION; Schema: extensions; Owner: -
--

CREATE FUNCTION extensions.pgrst_ddl_watch() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  cmd record;
BEGIN
  FOR cmd IN SELECT * FROM pg_event_trigger_ddl_commands()
  LOOP
    IF cmd.command_tag IN (
      'CREATE SCHEMA', 'ALTER SCHEMA'
    , 'CREATE TABLE', 'CREATE TABLE AS', 'SELECT INTO', 'ALTER TABLE'
    , 'CREATE FOREIGN TABLE', 'ALTER FOREIGN TABLE'
    , 'CREATE VIEW', 'ALTER VIEW'
    , 'CREATE MATERIALIZED VIEW', 'ALTER MATERIALIZED VIEW'
    , 'CREATE FUNCTION', 'ALTER FUNCTION'
    , 'CREATE TRIGGER'
    , 'CREATE TYPE', 'ALTER TYPE'
    , 'CREATE RULE'
    , 'COMMENT'
    )
    -- don't notify in case of CREATE TEMP table or other objects created on pg_temp
    AND cmd.schema_name is distinct from 'pg_temp'
    THEN
      NOTIFY pgrst, 'reload schema';
    END IF;
  END LOOP;
END; $$;


--
-- Name: pgrst_drop_watch(); Type: FUNCTION; Schema: extensions; Owner: -
--

CREATE FUNCTION extensions.pgrst_drop_watch() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  obj record;
BEGIN
  FOR obj IN SELECT * FROM pg_event_trigger_dropped_objects()
  LOOP
    IF obj.object_type IN (
      'schema'
    , 'table'
    , 'foreign table'
    , 'view'
    , 'materialized view'
    , 'function'
    , 'trigger'
    , 'type'
    , 'rule'
    )
    AND obj.is_temporary IS false -- no pg_temp objects
    THEN
      NOTIFY pgrst, 'reload schema';
    END IF;
  END LOOP;
END; $$;


--
-- Name: set_graphql_placeholder(); Type: FUNCTION; Schema: extensions; Owner: -
--

CREATE FUNCTION extensions.set_graphql_placeholder() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $_$
    DECLARE
    graphql_is_dropped bool;
    BEGIN
    graphql_is_dropped = (
        SELECT ev.schema_name = 'graphql_public'
        FROM pg_event_trigger_dropped_objects() AS ev
        WHERE ev.schema_name = 'graphql_public'
    );

    IF graphql_is_dropped
    THEN
        create or replace function graphql_public.graphql(
            "operationName" text default null,
            query text default null,
            variables jsonb default null,
            extensions jsonb default null
        )
            returns jsonb
            language plpgsql
        as $$
            DECLARE
                server_version float;
            BEGIN
                server_version = (SELECT (SPLIT_PART((select version()), ' ', 2))::float);

                IF server_version >= 14 THEN
                    RETURN jsonb_build_object(
                        'errors', jsonb_build_array(
                            jsonb_build_object(
                                'message', 'pg_graphql extension is not enabled.'
                            )
                        )
                    );
                ELSE
                    RETURN jsonb_build_object(
                        'errors', jsonb_build_array(
                            jsonb_build_object(
                                'message', 'pg_graphql is only available on projects running Postgres 14 onwards.'
                            )
                        )
                    );
                END IF;
            END;
        $$;
    END IF;

    END;
$_$;


--
-- Name: FUNCTION set_graphql_placeholder(); Type: COMMENT; Schema: extensions; Owner: -
--

COMMENT ON FUNCTION extensions.set_graphql_placeholder() IS 'Reintroduces placeholder function for graphql_public.graphql';


--
-- Name: get_auth(text); Type: FUNCTION; Schema: pgbouncer; Owner: -
--

CREATE FUNCTION pgbouncer.get_auth(p_usename text) RETURNS TABLE(username text, password text)
    LANGUAGE plpgsql SECURITY DEFINER
    SET search_path TO ''
    AS $_$
  BEGIN
      RAISE DEBUG 'PgBouncer auth request: %', p_usename;

      RETURN QUERY
      SELECT
          rolname::text,
          CASE WHEN rolvaliduntil < now()
              THEN null
              ELSE rolpassword::text
          END
      FROM pg_authid
      WHERE rolname=$1 and rolcanlogin;
  END;
  $_$;


--
-- Name: apply_rls(jsonb, integer); Type: FUNCTION; Schema: realtime; Owner: -
--

CREATE FUNCTION realtime.apply_rls(wal jsonb, max_record_bytes integer DEFAULT (1024 * 1024)) RETURNS SETOF realtime.wal_rls
    LANGUAGE plpgsql
    AS $$
declare
-- Regclass of the table e.g. public.notes
entity_ regclass = (quote_ident(wal ->> 'schema') || '.' || quote_ident(wal ->> 'table'))::regclass;

-- I, U, D, T: insert, update ...
action realtime.action = (
    case wal ->> 'action'
        when 'I' then 'INSERT'
        when 'U' then 'UPDATE'
        when 'D' then 'DELETE'
        else 'ERROR'
    end
);

-- Is row level security enabled for the table
is_rls_enabled bool = relrowsecurity from pg_class where oid = entity_;

subscriptions realtime.subscription[] = array_agg(subs)
    from
        realtime.subscription subs
    where
        subs.entity = entity_
        -- Filter by action early - only get subscriptions interested in this action
        -- action_filter column can be: '*' (all), 'INSERT', 'UPDATE', or 'DELETE'
        and (subs.action_filter = '*' or subs.action_filter = action::text);

-- Subscription vars
roles regrole[] = array_agg(distinct us.claims_role::text)
    from
        unnest(subscriptions) us;

working_role regrole;
claimed_role regrole;
claims jsonb;

subscription_id uuid;
subscription_has_access bool;
visible_to_subscription_ids uuid[] = '{}';

-- structured info for wal's columns
columns realtime.wal_column[];
-- previous identity values for update/delete
old_columns realtime.wal_column[];

error_record_exceeds_max_size boolean = octet_length(wal::text) > max_record_bytes;

-- Primary jsonb output for record
output jsonb;

begin
perform set_config('role', null, true);

columns =
    array_agg(
        (
            x->>'name',
            x->>'type',
            x->>'typeoid',
            realtime.cast(
                (x->'value') #>> '{}',
                coalesce(
                    (x->>'typeoid')::regtype, -- null when wal2json version <= 2.4
                    (x->>'type')::regtype
                )
            ),
            (pks ->> 'name') is not null,
            true
        )::realtime.wal_column
    )
    from
        jsonb_array_elements(wal -> 'columns') x
        left join jsonb_array_elements(wal -> 'pk') pks
            on (x ->> 'name') = (pks ->> 'name');

old_columns =
    array_agg(
        (
            x->>'name',
            x->>'type',
            x->>'typeoid',
            realtime.cast(
                (x->'value') #>> '{}',
                coalesce(
                    (x->>'typeoid')::regtype, -- null when wal2json version <= 2.4
                    (x->>'type')::regtype
                )
            ),
            (pks ->> 'name') is not null,
            true
        )::realtime.wal_column
    )
    from
        jsonb_array_elements(wal -> 'identity') x
        left join jsonb_array_elements(wal -> 'pk') pks
            on (x ->> 'name') = (pks ->> 'name');

for working_role in select * from unnest(roles) loop

    -- Update `is_selectable` for columns and old_columns
    columns =
        array_agg(
            (
                c.name,
                c.type_name,
                c.type_oid,
                c.value,
                c.is_pkey,
                pg_catalog.has_column_privilege(working_role, entity_, c.name, 'SELECT')
            )::realtime.wal_column
        )
        from
            unnest(columns) c;

    old_columns =
            array_agg(
                (
                    c.name,
                    c.type_name,
                    c.type_oid,
                    c.value,
                    c.is_pkey,
                    pg_catalog.has_column_privilege(working_role, entity_, c.name, 'SELECT')
                )::realtime.wal_column
            )
            from
                unnest(old_columns) c;

    if action <> 'DELETE' and count(1) = 0 from unnest(columns) c where c.is_pkey then
        return next (
            jsonb_build_object(
                'schema', wal ->> 'schema',
                'table', wal ->> 'table',
                'type', action
            ),
            is_rls_enabled,
            -- subscriptions is already filtered by entity
            (select array_agg(s.subscription_id) from unnest(subscriptions) as s where claims_role = working_role),
            array['Error 400: Bad Request, no primary key']
        )::realtime.wal_rls;

    -- The claims role does not have SELECT permission to the primary key of entity
    elsif action <> 'DELETE' and sum(c.is_selectable::int) <> count(1) from unnest(columns) c where c.is_pkey then
        return next (
            jsonb_build_object(
                'schema', wal ->> 'schema',
                'table', wal ->> 'table',
                'type', action
            ),
            is_rls_enabled,
            (select array_agg(s.subscription_id) from unnest(subscriptions) as s where claims_role = working_role),
            array['Error 401: Unauthorized']
        )::realtime.wal_rls;

    else
        output = jsonb_build_object(
            'schema', wal ->> 'schema',
            'table', wal ->> 'table',
            'type', action,
            'commit_timestamp', to_char(
                ((wal ->> 'timestamp')::timestamptz at time zone 'utc'),
                'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"'
            ),
            'columns', (
                select
                    jsonb_agg(
                        jsonb_build_object(
                            'name', pa.attname,
                            'type', pt.typname
                        )
                        order by pa.attnum asc
                    )
                from
                    pg_attribute pa
                    join pg_type pt
                        on pa.atttypid = pt.oid
                where
                    attrelid = entity_
                    and attnum > 0
                    and pg_catalog.has_column_privilege(working_role, entity_, pa.attname, 'SELECT')
            )
        )
        -- Add "record" key for insert and update
        || case
            when action in ('INSERT', 'UPDATE') then
                jsonb_build_object(
                    'record',
                    (
                        select
                            jsonb_object_agg(
                                -- if unchanged toast, get column name and value from old record
                                coalesce((c).name, (oc).name),
                                case
                                    when (c).name is null then (oc).value
                                    else (c).value
                                end
                            )
                        from
                            unnest(columns) c
                            full outer join unnest(old_columns) oc
                                on (c).name = (oc).name
                        where
                            coalesce((c).is_selectable, (oc).is_selectable)
                            and ( not error_record_exceeds_max_size or (octet_length((c).value::text) <= 64))
                    )
                )
            else '{}'::jsonb
        end
        -- Add "old_record" key for update and delete
        || case
            when action = 'UPDATE' then
                jsonb_build_object(
                        'old_record',
                        (
                            select jsonb_object_agg((c).name, (c).value)
                            from unnest(old_columns) c
                            where
                                (c).is_selectable
                                and ( not error_record_exceeds_max_size or (octet_length((c).value::text) <= 64))
                        )
                    )
            when action = 'DELETE' then
                jsonb_build_object(
                    'old_record',
                    (
                        select jsonb_object_agg((c).name, (c).value)
                        from unnest(old_columns) c
                        where
                            (c).is_selectable
                            and ( not error_record_exceeds_max_size or (octet_length((c).value::text) <= 64))
                            and ( not is_rls_enabled or (c).is_pkey ) -- if RLS enabled, we can't secure deletes so filter to pkey
                    )
                )
            else '{}'::jsonb
        end;

        -- Create the prepared statement
        if is_rls_enabled and action <> 'DELETE' then
            if (select 1 from pg_prepared_statements where name = 'walrus_rls_stmt' limit 1) > 0 then
                deallocate walrus_rls_stmt;
            end if;
            execute realtime.build_prepared_statement_sql('walrus_rls_stmt', entity_, columns);
        end if;

        visible_to_subscription_ids = '{}';

        for subscription_id, claims in (
                select
                    subs.subscription_id,
                    subs.claims
                from
                    unnest(subscriptions) subs
                where
                    subs.entity = entity_
                    and subs.claims_role = working_role
                    and (
                        realtime.is_visible_through_filters(columns, subs.filters)
                        or (
                          action = 'DELETE'
                          and realtime.is_visible_through_filters(old_columns, subs.filters)
                        )
                    )
        ) loop

            if not is_rls_enabled or action = 'DELETE' then
                visible_to_subscription_ids = visible_to_subscription_ids || subscription_id;
            else
                -- Check if RLS allows the role to see the record
                perform
                    -- Trim leading and trailing quotes from working_role because set_config
                    -- doesn't recognize the role as valid if they are included
                    set_config('role', trim(both '"' from working_role::text), true),
                    set_config('request.jwt.claims', claims::text, true);

                execute 'execute walrus_rls_stmt' into subscription_has_access;

                if subscription_has_access then
                    visible_to_subscription_ids = visible_to_subscription_ids || subscription_id;
                end if;
            end if;
        end loop;

        perform set_config('role', null, true);

        return next (
            output,
            is_rls_enabled,
            visible_to_subscription_ids,
            case
                when error_record_exceeds_max_size then array['Error 413: Payload Too Large']
                else '{}'
            end
        )::realtime.wal_rls;

    end if;
end loop;

perform set_config('role', null, true);
end;
$$;


--
-- Name: broadcast_changes(text, text, text, text, text, record, record, text); Type: FUNCTION; Schema: realtime; Owner: -
--

CREATE FUNCTION realtime.broadcast_changes(topic_name text, event_name text, operation text, table_name text, table_schema text, new record, old record, level text DEFAULT 'ROW'::text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    -- Declare a variable to hold the JSONB representation of the row
    row_data jsonb := '{}'::jsonb;
BEGIN
    IF level = 'STATEMENT' THEN
        RAISE EXCEPTION 'function can only be triggered for each row, not for each statement';
    END IF;
    -- Check the operation type and handle accordingly
    IF operation = 'INSERT' OR operation = 'UPDATE' OR operation = 'DELETE' THEN
        row_data := jsonb_build_object('old_record', OLD, 'record', NEW, 'operation', operation, 'table', table_name, 'schema', table_schema);
        PERFORM realtime.send (row_data, event_name, topic_name);
    ELSE
        RAISE EXCEPTION 'Unexpected operation type: %', operation;
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Failed to process the row: %', SQLERRM;
END;

$$;


--
-- Name: build_prepared_statement_sql(text, regclass, realtime.wal_column[]); Type: FUNCTION; Schema: realtime; Owner: -
--

CREATE FUNCTION realtime.build_prepared_statement_sql(prepared_statement_name text, entity regclass, columns realtime.wal_column[]) RETURNS text
    LANGUAGE sql
    AS $$
      /*
      Builds a sql string that, if executed, creates a prepared statement to
      tests retrive a row from *entity* by its primary key columns.
      Example
          select realtime.build_prepared_statement_sql('public.notes', '{"id"}'::text[], '{"bigint"}'::text[])
      */
          select
      'prepare ' || prepared_statement_name || ' as
          select
              exists(
                  select
                      1
                  from
                      ' || entity || '
                  where
                      ' || string_agg(quote_ident(pkc.name) || '=' || quote_nullable(pkc.value #>> '{}') , ' and ') || '
              )'
          from
              unnest(columns) pkc
          where
              pkc.is_pkey
          group by
              entity
      $$;


--
-- Name: cast(text, regtype); Type: FUNCTION; Schema: realtime; Owner: -
--

CREATE FUNCTION realtime."cast"(val text, type_ regtype) RETURNS jsonb
    LANGUAGE plpgsql IMMUTABLE
    AS $$
declare
  res jsonb;
begin
  if type_::text = 'bytea' then
    return to_jsonb(val);
  end if;
  execute format('select to_jsonb(%L::'|| type_::text || ')', val) into res;
  return res;
end
$$;


--
-- Name: check_equality_op(realtime.equality_op, regtype, text, text); Type: FUNCTION; Schema: realtime; Owner: -
--

CREATE FUNCTION realtime.check_equality_op(op realtime.equality_op, type_ regtype, val_1 text, val_2 text) RETURNS boolean
    LANGUAGE plpgsql IMMUTABLE
    AS $$
      /*
      Casts *val_1* and *val_2* as type *type_* and check the *op* condition for truthiness
      */
      declare
          op_symbol text = (
              case
                  when op = 'eq' then '='
                  when op = 'neq' then '!='
                  when op = 'lt' then '<'
                  when op = 'lte' then '<='
                  when op = 'gt' then '>'
                  when op = 'gte' then '>='
                  when op = 'in' then '= any'
                  else 'UNKNOWN OP'
              end
          );
          res boolean;
      begin
          execute format(
              'select %L::'|| type_::text || ' ' || op_symbol
              || ' ( %L::'
              || (
                  case
                      when op = 'in' then type_::text || '[]'
                      else type_::text end
              )
              || ')', val_1, val_2) into res;
          return res;
      end;
      $$;


--
-- Name: is_visible_through_filters(realtime.wal_column[], realtime.user_defined_filter[]); Type: FUNCTION; Schema: realtime; Owner: -
--

CREATE FUNCTION realtime.is_visible_through_filters(columns realtime.wal_column[], filters realtime.user_defined_filter[]) RETURNS boolean
    LANGUAGE sql IMMUTABLE
    AS $_$
    /*
    Should the record be visible (true) or filtered out (false) after *filters* are applied
    */
        select
            -- Default to allowed when no filters present
            $2 is null -- no filters. this should not happen because subscriptions has a default
            or array_length($2, 1) is null -- array length of an empty array is null
            or bool_and(
                coalesce(
                    realtime.check_equality_op(
                        op:=f.op,
                        type_:=coalesce(
                            col.type_oid::regtype, -- null when wal2json version <= 2.4
                            col.type_name::regtype
                        ),
                        -- cast jsonb to text
                        val_1:=col.value #>> '{}',
                        val_2:=f.value
                    ),
                    false -- if null, filter does not match
                )
            )
        from
            unnest(filters) f
            join unnest(columns) col
                on f.column_name = col.name;
    $_$;


--
-- Name: list_changes(name, name, integer, integer); Type: FUNCTION; Schema: realtime; Owner: -
--

CREATE FUNCTION realtime.list_changes(publication name, slot_name name, max_changes integer, max_record_bytes integer) RETURNS SETOF realtime.wal_rls
    LANGUAGE sql
    SET log_min_messages TO 'fatal'
    AS $$
      with pub as (
        select
          concat_ws(
            ',',
            case when bool_or(pubinsert) then 'insert' else null end,
            case when bool_or(pubupdate) then 'update' else null end,
            case when bool_or(pubdelete) then 'delete' else null end
          ) as w2j_actions,
          coalesce(
            string_agg(
              realtime.quote_wal2json(format('%I.%I', schemaname, tablename)::regclass),
              ','
            ) filter (where ppt.tablename is not null and ppt.tablename not like '% %'),
            ''
          ) w2j_add_tables
        from
          pg_publication pp
          left join pg_publication_tables ppt
            on pp.pubname = ppt.pubname
        where
          pp.pubname = publication
        group by
          pp.pubname
        limit 1
      ),
      w2j as (
        select
          x.*, pub.w2j_add_tables
        from
          pub,
          pg_logical_slot_get_changes(
            slot_name, null, max_changes,
            'include-pk', 'true',
            'include-transaction', 'false',
            'include-timestamp', 'true',
            'include-type-oids', 'true',
            'format-version', '2',
            'actions', pub.w2j_actions,
            'add-tables', pub.w2j_add_tables
          ) x
      )
      select
        xyz.wal,
        xyz.is_rls_enabled,
        xyz.subscription_ids,
        xyz.errors
      from
        w2j,
        realtime.apply_rls(
          wal := w2j.data::jsonb,
          max_record_bytes := max_record_bytes
        ) xyz(wal, is_rls_enabled, subscription_ids, errors)
      where
        w2j.w2j_add_tables <> ''
        and xyz.subscription_ids[1] is not null
    $$;


--
-- Name: quote_wal2json(regclass); Type: FUNCTION; Schema: realtime; Owner: -
--

CREATE FUNCTION realtime.quote_wal2json(entity regclass) RETURNS text
    LANGUAGE sql IMMUTABLE STRICT
    AS $$
      select
        (
          select string_agg('' || ch,'')
          from unnest(string_to_array(nsp.nspname::text, null)) with ordinality x(ch, idx)
          where
            not (x.idx = 1 and x.ch = '"')
            and not (
              x.idx = array_length(string_to_array(nsp.nspname::text, null), 1)
              and x.ch = '"'
            )
        )
        || '.'
        || (
          select string_agg('' || ch,'')
          from unnest(string_to_array(pc.relname::text, null)) with ordinality x(ch, idx)
          where
            not (x.idx = 1 and x.ch = '"')
            and not (
              x.idx = array_length(string_to_array(nsp.nspname::text, null), 1)
              and x.ch = '"'
            )
          )
      from
        pg_class pc
        join pg_namespace nsp
          on pc.relnamespace = nsp.oid
      where
        pc.oid = entity
    $$;


--
-- Name: send(jsonb, text, text, boolean); Type: FUNCTION; Schema: realtime; Owner: -
--

CREATE FUNCTION realtime.send(payload jsonb, event text, topic text, private boolean DEFAULT true) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
  generated_id uuid;
  final_payload jsonb;
BEGIN
  BEGIN
    -- Generate a new UUID for the id
    generated_id := gen_random_uuid();

    -- Check if payload has an 'id' key, if not, add the generated UUID
    IF payload ? 'id' THEN
      final_payload := payload;
    ELSE
      final_payload := jsonb_set(payload, '{id}', to_jsonb(generated_id));
    END IF;

    -- Set the topic configuration
    EXECUTE format('SET LOCAL realtime.topic TO %L', topic);

    -- Attempt to insert the message
    INSERT INTO realtime.messages (id, payload, event, topic, private, extension)
    VALUES (generated_id, final_payload, event, topic, private, 'broadcast');
  EXCEPTION
    WHEN OTHERS THEN
      -- Capture and notify the error
      RAISE WARNING 'ErrorSendingBroadcastMessage: %', SQLERRM;
  END;
END;
$$;


--
-- Name: subscription_check_filters(); Type: FUNCTION; Schema: realtime; Owner: -
--

CREATE FUNCTION realtime.subscription_check_filters() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    /*
    Validates that the user defined filters for a subscription:
    - refer to valid columns that the claimed role may access
    - values are coercable to the correct column type
    */
    declare
        col_names text[] = coalesce(
                array_agg(c.column_name order by c.ordinal_position),
                '{}'::text[]
            )
            from
                information_schema.columns c
            where
                format('%I.%I', c.table_schema, c.table_name)::regclass = new.entity
                and pg_catalog.has_column_privilege(
                    (new.claims ->> 'role'),
                    format('%I.%I', c.table_schema, c.table_name)::regclass,
                    c.column_name,
                    'SELECT'
                );
        filter realtime.user_defined_filter;
        col_type regtype;

        in_val jsonb;
    begin
        for filter in select * from unnest(new.filters) loop
            -- Filtered column is valid
            if not filter.column_name = any(col_names) then
                raise exception 'invalid column for filter %', filter.column_name;
            end if;

            -- Type is sanitized and safe for string interpolation
            col_type = (
                select atttypid::regtype
                from pg_catalog.pg_attribute
                where attrelid = new.entity
                      and attname = filter.column_name
            );
            if col_type is null then
                raise exception 'failed to lookup type for column %', filter.column_name;
            end if;

            -- Set maximum number of entries for in filter
            if filter.op = 'in'::realtime.equality_op then
                in_val = realtime.cast(filter.value, (col_type::text || '[]')::regtype);
                if coalesce(jsonb_array_length(in_val), 0) > 100 then
                    raise exception 'too many values for `in` filter. Maximum 100';
                end if;
            else
                -- raises an exception if value is not coercable to type
                perform realtime.cast(filter.value, col_type);
            end if;

        end loop;

        -- Apply consistent order to filters so the unique constraint on
        -- (subscription_id, entity, filters) can't be tricked by a different filter order
        new.filters = coalesce(
            array_agg(f order by f.column_name, f.op, f.value),
            '{}'
        ) from unnest(new.filters) f;

        return new;
    end;
    $$;


--
-- Name: to_regrole(text); Type: FUNCTION; Schema: realtime; Owner: -
--

CREATE FUNCTION realtime.to_regrole(role_name text) RETURNS regrole
    LANGUAGE sql IMMUTABLE
    AS $$ select role_name::regrole $$;


--
-- Name: topic(); Type: FUNCTION; Schema: realtime; Owner: -
--

CREATE FUNCTION realtime.topic() RETURNS text
    LANGUAGE sql STABLE
    AS $$
select nullif(current_setting('realtime.topic', true), '')::text;
$$;


--
-- Name: can_insert_object(text, text, uuid, jsonb); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.can_insert_object(bucketid text, name text, owner uuid, metadata jsonb) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
  INSERT INTO "storage"."objects" ("bucket_id", "name", "owner", "metadata") VALUES (bucketid, name, owner, metadata);
  -- hack to rollback the successful insert
  RAISE sqlstate 'PT200' using
  message = 'ROLLBACK',
  detail = 'rollback successful insert';
END
$$;


--
-- Name: enforce_bucket_name_length(); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.enforce_bucket_name_length() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
    if length(new.name) > 100 then
        raise exception 'bucket name "%" is too long (% characters). Max is 100.', new.name, length(new.name);
    end if;
    return new;
end;
$$;


--
-- Name: extension(text); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.extension(name text) RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
_parts text[];
_filename text;
BEGIN
	select string_to_array(name, '/') into _parts;
	select _parts[array_length(_parts,1)] into _filename;
	-- @todo return the last part instead of 2
	return reverse(split_part(reverse(_filename), '.', 1));
END
$$;


--
-- Name: filename(text); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.filename(name text) RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
_parts text[];
BEGIN
	select string_to_array(name, '/') into _parts;
	return _parts[array_length(_parts,1)];
END
$$;


--
-- Name: foldername(text); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.foldername(name text) RETURNS text[]
    LANGUAGE plpgsql
    AS $$
DECLARE
_parts text[];
BEGIN
	select string_to_array(name, '/') into _parts;
	return _parts[1:array_length(_parts,1)-1];
END
$$;


--
-- Name: get_common_prefix(text, text, text); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.get_common_prefix(p_key text, p_prefix text, p_delimiter text) RETURNS text
    LANGUAGE sql IMMUTABLE
    AS $$
SELECT CASE
    WHEN position(p_delimiter IN substring(p_key FROM length(p_prefix) + 1)) > 0
    THEN left(p_key, length(p_prefix) + position(p_delimiter IN substring(p_key FROM length(p_prefix) + 1)))
    ELSE NULL
END;
$$;


--
-- Name: get_size_by_bucket(); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.get_size_by_bucket() RETURNS TABLE(size bigint, bucket_id text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    return query
        select sum((metadata->>'size')::int) as size, obj.bucket_id
        from "storage".objects as obj
        group by obj.bucket_id;
END
$$;


--
-- Name: list_multipart_uploads_with_delimiter(text, text, text, integer, text, text); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.list_multipart_uploads_with_delimiter(bucket_id text, prefix_param text, delimiter_param text, max_keys integer DEFAULT 100, next_key_token text DEFAULT ''::text, next_upload_token text DEFAULT ''::text) RETURNS TABLE(key text, id text, created_at timestamp with time zone)
    LANGUAGE plpgsql
    AS $_$
BEGIN
    RETURN QUERY EXECUTE
        'SELECT DISTINCT ON(key COLLATE "C") * from (
            SELECT
                CASE
                    WHEN position($2 IN substring(key from length($1) + 1)) > 0 THEN
                        substring(key from 1 for length($1) + position($2 IN substring(key from length($1) + 1)))
                    ELSE
                        key
                END AS key, id, created_at
            FROM
                storage.s3_multipart_uploads
            WHERE
                bucket_id = $5 AND
                key ILIKE $1 || ''%'' AND
                CASE
                    WHEN $4 != '''' AND $6 = '''' THEN
                        CASE
                            WHEN position($2 IN substring(key from length($1) + 1)) > 0 THEN
                                substring(key from 1 for length($1) + position($2 IN substring(key from length($1) + 1))) COLLATE "C" > $4
                            ELSE
                                key COLLATE "C" > $4
                            END
                    ELSE
                        true
                END AND
                CASE
                    WHEN $6 != '''' THEN
                        id COLLATE "C" > $6
                    ELSE
                        true
                    END
            ORDER BY
                key COLLATE "C" ASC, created_at ASC) as e order by key COLLATE "C" LIMIT $3'
        USING prefix_param, delimiter_param, max_keys, next_key_token, bucket_id, next_upload_token;
END;
$_$;


--
-- Name: list_objects_with_delimiter(text, text, text, integer, text, text, text); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.list_objects_with_delimiter(_bucket_id text, prefix_param text, delimiter_param text, max_keys integer DEFAULT 100, start_after text DEFAULT ''::text, next_token text DEFAULT ''::text, sort_order text DEFAULT 'asc'::text) RETURNS TABLE(name text, id uuid, metadata jsonb, updated_at timestamp with time zone, created_at timestamp with time zone, last_accessed_at timestamp with time zone)
    LANGUAGE plpgsql STABLE
    AS $_$
DECLARE
    v_peek_name TEXT;
    v_current RECORD;
    v_common_prefix TEXT;

    -- Configuration
    v_is_asc BOOLEAN;
    v_prefix TEXT;
    v_start TEXT;
    v_upper_bound TEXT;
    v_file_batch_size INT;

    -- Seek state
    v_next_seek TEXT;
    v_count INT := 0;

    -- Dynamic SQL for batch query only
    v_batch_query TEXT;

BEGIN
    -- ========================================================================
    -- INITIALIZATION
    -- ========================================================================
    v_is_asc := lower(coalesce(sort_order, 'asc')) = 'asc';
    v_prefix := coalesce(prefix_param, '');
    v_start := CASE WHEN coalesce(next_token, '') <> '' THEN next_token ELSE coalesce(start_after, '') END;
    v_file_batch_size := LEAST(GREATEST(max_keys * 2, 100), 1000);

    -- Calculate upper bound for prefix filtering (bytewise, using COLLATE "C")
    IF v_prefix = '' THEN
        v_upper_bound := NULL;
    ELSIF right(v_prefix, 1) = delimiter_param THEN
        v_upper_bound := left(v_prefix, -1) || chr(ascii(delimiter_param) + 1);
    ELSE
        v_upper_bound := left(v_prefix, -1) || chr(ascii(right(v_prefix, 1)) + 1);
    END IF;

    -- Build batch query (dynamic SQL - called infrequently, amortized over many rows)
    IF v_is_asc THEN
        IF v_upper_bound IS NOT NULL THEN
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND o.name COLLATE "C" >= $2 ' ||
                'AND o.name COLLATE "C" < $3 ORDER BY o.name COLLATE "C" ASC LIMIT $4';
        ELSE
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND o.name COLLATE "C" >= $2 ' ||
                'ORDER BY o.name COLLATE "C" ASC LIMIT $4';
        END IF;
    ELSE
        IF v_upper_bound IS NOT NULL THEN
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND o.name COLLATE "C" < $2 ' ||
                'AND o.name COLLATE "C" >= $3 ORDER BY o.name COLLATE "C" DESC LIMIT $4';
        ELSE
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND o.name COLLATE "C" < $2 ' ||
                'ORDER BY o.name COLLATE "C" DESC LIMIT $4';
        END IF;
    END IF;

    -- ========================================================================
    -- SEEK INITIALIZATION: Determine starting position
    -- ========================================================================
    IF v_start = '' THEN
        IF v_is_asc THEN
            v_next_seek := v_prefix;
        ELSE
            -- DESC without cursor: find the last item in range
            IF v_upper_bound IS NOT NULL THEN
                SELECT o.name INTO v_next_seek FROM storage.objects o
                WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" >= v_prefix AND o.name COLLATE "C" < v_upper_bound
                ORDER BY o.name COLLATE "C" DESC LIMIT 1;
            ELSIF v_prefix <> '' THEN
                SELECT o.name INTO v_next_seek FROM storage.objects o
                WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" >= v_prefix
                ORDER BY o.name COLLATE "C" DESC LIMIT 1;
            ELSE
                SELECT o.name INTO v_next_seek FROM storage.objects o
                WHERE o.bucket_id = _bucket_id
                ORDER BY o.name COLLATE "C" DESC LIMIT 1;
            END IF;

            IF v_next_seek IS NOT NULL THEN
                v_next_seek := v_next_seek || delimiter_param;
            ELSE
                RETURN;
            END IF;
        END IF;
    ELSE
        -- Cursor provided: determine if it refers to a folder or leaf
        IF EXISTS (
            SELECT 1 FROM storage.objects o
            WHERE o.bucket_id = _bucket_id
              AND o.name COLLATE "C" LIKE v_start || delimiter_param || '%'
            LIMIT 1
        ) THEN
            -- Cursor refers to a folder
            IF v_is_asc THEN
                v_next_seek := v_start || chr(ascii(delimiter_param) + 1);
            ELSE
                v_next_seek := v_start || delimiter_param;
            END IF;
        ELSE
            -- Cursor refers to a leaf object
            IF v_is_asc THEN
                v_next_seek := v_start || delimiter_param;
            ELSE
                v_next_seek := v_start;
            END IF;
        END IF;
    END IF;

    -- ========================================================================
    -- MAIN LOOP: Hybrid peek-then-batch algorithm
    -- Uses STATIC SQL for peek (hot path) and DYNAMIC SQL for batch
    -- ========================================================================
    LOOP
        EXIT WHEN v_count >= max_keys;

        -- STEP 1: PEEK using STATIC SQL (plan cached, very fast)
        IF v_is_asc THEN
            IF v_upper_bound IS NOT NULL THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" >= v_next_seek AND o.name COLLATE "C" < v_upper_bound
                ORDER BY o.name COLLATE "C" ASC LIMIT 1;
            ELSE
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" >= v_next_seek
                ORDER BY o.name COLLATE "C" ASC LIMIT 1;
            END IF;
        ELSE
            IF v_upper_bound IS NOT NULL THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" < v_next_seek AND o.name COLLATE "C" >= v_prefix
                ORDER BY o.name COLLATE "C" DESC LIMIT 1;
            ELSIF v_prefix <> '' THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" < v_next_seek AND o.name COLLATE "C" >= v_prefix
                ORDER BY o.name COLLATE "C" DESC LIMIT 1;
            ELSE
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = _bucket_id AND o.name COLLATE "C" < v_next_seek
                ORDER BY o.name COLLATE "C" DESC LIMIT 1;
            END IF;
        END IF;

        EXIT WHEN v_peek_name IS NULL;

        -- STEP 2: Check if this is a FOLDER or FILE
        v_common_prefix := storage.get_common_prefix(v_peek_name, v_prefix, delimiter_param);

        IF v_common_prefix IS NOT NULL THEN
            -- FOLDER: Emit and skip to next folder (no heap access needed)
            name := rtrim(v_common_prefix, delimiter_param);
            id := NULL;
            updated_at := NULL;
            created_at := NULL;
            last_accessed_at := NULL;
            metadata := NULL;
            RETURN NEXT;
            v_count := v_count + 1;

            -- Advance seek past the folder range
            IF v_is_asc THEN
                v_next_seek := left(v_common_prefix, -1) || chr(ascii(delimiter_param) + 1);
            ELSE
                v_next_seek := v_common_prefix;
            END IF;
        ELSE
            -- FILE: Batch fetch using DYNAMIC SQL (overhead amortized over many rows)
            -- For ASC: upper_bound is the exclusive upper limit (< condition)
            -- For DESC: prefix is the inclusive lower limit (>= condition)
            FOR v_current IN EXECUTE v_batch_query USING _bucket_id, v_next_seek,
                CASE WHEN v_is_asc THEN COALESCE(v_upper_bound, v_prefix) ELSE v_prefix END, v_file_batch_size
            LOOP
                v_common_prefix := storage.get_common_prefix(v_current.name, v_prefix, delimiter_param);

                IF v_common_prefix IS NOT NULL THEN
                    -- Hit a folder: exit batch, let peek handle it
                    v_next_seek := v_current.name;
                    EXIT;
                END IF;

                -- Emit file
                name := v_current.name;
                id := v_current.id;
                updated_at := v_current.updated_at;
                created_at := v_current.created_at;
                last_accessed_at := v_current.last_accessed_at;
                metadata := v_current.metadata;
                RETURN NEXT;
                v_count := v_count + 1;

                -- Advance seek past this file
                IF v_is_asc THEN
                    v_next_seek := v_current.name || delimiter_param;
                ELSE
                    v_next_seek := v_current.name;
                END IF;

                EXIT WHEN v_count >= max_keys;
            END LOOP;
        END IF;
    END LOOP;
END;
$_$;


--
-- Name: operation(); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.operation() RETURNS text
    LANGUAGE plpgsql STABLE
    AS $$
BEGIN
    RETURN current_setting('storage.operation', true);
END;
$$;


--
-- Name: protect_delete(); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.protect_delete() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Check if storage.allow_delete_query is set to 'true'
    IF COALESCE(current_setting('storage.allow_delete_query', true), 'false') != 'true' THEN
        RAISE EXCEPTION 'Direct deletion from storage tables is not allowed. Use the Storage API instead.'
            USING HINT = 'This prevents accidental data loss from orphaned objects.',
                  ERRCODE = '42501';
    END IF;
    RETURN NULL;
END;
$$;


--
-- Name: search(text, text, integer, integer, integer, text, text, text); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.search(prefix text, bucketname text, limits integer DEFAULT 100, levels integer DEFAULT 1, offsets integer DEFAULT 0, search text DEFAULT ''::text, sortcolumn text DEFAULT 'name'::text, sortorder text DEFAULT 'asc'::text) RETURNS TABLE(name text, id uuid, updated_at timestamp with time zone, created_at timestamp with time zone, last_accessed_at timestamp with time zone, metadata jsonb)
    LANGUAGE plpgsql STABLE
    AS $_$
DECLARE
    v_peek_name TEXT;
    v_current RECORD;
    v_common_prefix TEXT;
    v_delimiter CONSTANT TEXT := '/';

    -- Configuration
    v_limit INT;
    v_prefix TEXT;
    v_prefix_lower TEXT;
    v_is_asc BOOLEAN;
    v_order_by TEXT;
    v_sort_order TEXT;
    v_upper_bound TEXT;
    v_file_batch_size INT;

    -- Dynamic SQL for batch query only
    v_batch_query TEXT;

    -- Seek state
    v_next_seek TEXT;
    v_count INT := 0;
    v_skipped INT := 0;
BEGIN
    -- ========================================================================
    -- INITIALIZATION
    -- ========================================================================
    v_limit := LEAST(coalesce(limits, 100), 1500);
    v_prefix := coalesce(prefix, '') || coalesce(search, '');
    v_prefix_lower := lower(v_prefix);
    v_is_asc := lower(coalesce(sortorder, 'asc')) = 'asc';
    v_file_batch_size := LEAST(GREATEST(v_limit * 2, 100), 1000);

    -- Validate sort column
    CASE lower(coalesce(sortcolumn, 'name'))
        WHEN 'name' THEN v_order_by := 'name';
        WHEN 'updated_at' THEN v_order_by := 'updated_at';
        WHEN 'created_at' THEN v_order_by := 'created_at';
        WHEN 'last_accessed_at' THEN v_order_by := 'last_accessed_at';
        ELSE v_order_by := 'name';
    END CASE;

    v_sort_order := CASE WHEN v_is_asc THEN 'asc' ELSE 'desc' END;

    -- ========================================================================
    -- NON-NAME SORTING: Use path_tokens approach (unchanged)
    -- ========================================================================
    IF v_order_by != 'name' THEN
        RETURN QUERY EXECUTE format(
            $sql$
            WITH folders AS (
                SELECT path_tokens[$1] AS folder
                FROM storage.objects
                WHERE objects.name ILIKE $2 || '%%'
                  AND bucket_id = $3
                  AND array_length(objects.path_tokens, 1) <> $1
                GROUP BY folder
                ORDER BY folder %s
            )
            (SELECT folder AS "name",
                   NULL::uuid AS id,
                   NULL::timestamptz AS updated_at,
                   NULL::timestamptz AS created_at,
                   NULL::timestamptz AS last_accessed_at,
                   NULL::jsonb AS metadata FROM folders)
            UNION ALL
            (SELECT path_tokens[$1] AS "name",
                   id, updated_at, created_at, last_accessed_at, metadata
             FROM storage.objects
             WHERE objects.name ILIKE $2 || '%%'
               AND bucket_id = $3
               AND array_length(objects.path_tokens, 1) = $1
             ORDER BY %I %s)
            LIMIT $4 OFFSET $5
            $sql$, v_sort_order, v_order_by, v_sort_order
        ) USING levels, v_prefix, bucketname, v_limit, offsets;
        RETURN;
    END IF;

    -- ========================================================================
    -- NAME SORTING: Hybrid skip-scan with batch optimization
    -- ========================================================================

    -- Calculate upper bound for prefix filtering
    IF v_prefix_lower = '' THEN
        v_upper_bound := NULL;
    ELSIF right(v_prefix_lower, 1) = v_delimiter THEN
        v_upper_bound := left(v_prefix_lower, -1) || chr(ascii(v_delimiter) + 1);
    ELSE
        v_upper_bound := left(v_prefix_lower, -1) || chr(ascii(right(v_prefix_lower, 1)) + 1);
    END IF;

    -- Build batch query (dynamic SQL - called infrequently, amortized over many rows)
    IF v_is_asc THEN
        IF v_upper_bound IS NOT NULL THEN
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" >= $2 ' ||
                'AND lower(o.name) COLLATE "C" < $3 ORDER BY lower(o.name) COLLATE "C" ASC LIMIT $4';
        ELSE
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" >= $2 ' ||
                'ORDER BY lower(o.name) COLLATE "C" ASC LIMIT $4';
        END IF;
    ELSE
        IF v_upper_bound IS NOT NULL THEN
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" < $2 ' ||
                'AND lower(o.name) COLLATE "C" >= $3 ORDER BY lower(o.name) COLLATE "C" DESC LIMIT $4';
        ELSE
            v_batch_query := 'SELECT o.name, o.id, o.updated_at, o.created_at, o.last_accessed_at, o.metadata ' ||
                'FROM storage.objects o WHERE o.bucket_id = $1 AND lower(o.name) COLLATE "C" < $2 ' ||
                'ORDER BY lower(o.name) COLLATE "C" DESC LIMIT $4';
        END IF;
    END IF;

    -- Initialize seek position
    IF v_is_asc THEN
        v_next_seek := v_prefix_lower;
    ELSE
        -- DESC: find the last item in range first (static SQL)
        IF v_upper_bound IS NOT NULL THEN
            SELECT o.name INTO v_peek_name FROM storage.objects o
            WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" >= v_prefix_lower AND lower(o.name) COLLATE "C" < v_upper_bound
            ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
        ELSIF v_prefix_lower <> '' THEN
            SELECT o.name INTO v_peek_name FROM storage.objects o
            WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" >= v_prefix_lower
            ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
        ELSE
            SELECT o.name INTO v_peek_name FROM storage.objects o
            WHERE o.bucket_id = bucketname
            ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
        END IF;

        IF v_peek_name IS NOT NULL THEN
            v_next_seek := lower(v_peek_name) || v_delimiter;
        ELSE
            RETURN;
        END IF;
    END IF;

    -- ========================================================================
    -- MAIN LOOP: Hybrid peek-then-batch algorithm
    -- Uses STATIC SQL for peek (hot path) and DYNAMIC SQL for batch
    -- ========================================================================
    LOOP
        EXIT WHEN v_count >= v_limit;

        -- STEP 1: PEEK using STATIC SQL (plan cached, very fast)
        IF v_is_asc THEN
            IF v_upper_bound IS NOT NULL THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" >= v_next_seek AND lower(o.name) COLLATE "C" < v_upper_bound
                ORDER BY lower(o.name) COLLATE "C" ASC LIMIT 1;
            ELSE
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" >= v_next_seek
                ORDER BY lower(o.name) COLLATE "C" ASC LIMIT 1;
            END IF;
        ELSE
            IF v_upper_bound IS NOT NULL THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" < v_next_seek AND lower(o.name) COLLATE "C" >= v_prefix_lower
                ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
            ELSIF v_prefix_lower <> '' THEN
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" < v_next_seek AND lower(o.name) COLLATE "C" >= v_prefix_lower
                ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
            ELSE
                SELECT o.name INTO v_peek_name FROM storage.objects o
                WHERE o.bucket_id = bucketname AND lower(o.name) COLLATE "C" < v_next_seek
                ORDER BY lower(o.name) COLLATE "C" DESC LIMIT 1;
            END IF;
        END IF;

        EXIT WHEN v_peek_name IS NULL;

        -- STEP 2: Check if this is a FOLDER or FILE
        v_common_prefix := storage.get_common_prefix(lower(v_peek_name), v_prefix_lower, v_delimiter);

        IF v_common_prefix IS NOT NULL THEN
            -- FOLDER: Handle offset, emit if needed, skip to next folder
            IF v_skipped < offsets THEN
                v_skipped := v_skipped + 1;
            ELSE
                name := split_part(rtrim(storage.get_common_prefix(v_peek_name, v_prefix, v_delimiter), v_delimiter), v_delimiter, levels);
                id := NULL;
                updated_at := NULL;
                created_at := NULL;
                last_accessed_at := NULL;
                metadata := NULL;
                RETURN NEXT;
                v_count := v_count + 1;
            END IF;

            -- Advance seek past the folder range
            IF v_is_asc THEN
                v_next_seek := lower(left(v_common_prefix, -1)) || chr(ascii(v_delimiter) + 1);
            ELSE
                v_next_seek := lower(v_common_prefix);
            END IF;
        ELSE
            -- FILE: Batch fetch using DYNAMIC SQL (overhead amortized over many rows)
            -- For ASC: upper_bound is the exclusive upper limit (< condition)
            -- For DESC: prefix_lower is the inclusive lower limit (>= condition)
            FOR v_current IN EXECUTE v_batch_query
                USING bucketname, v_next_seek,
                    CASE WHEN v_is_asc THEN COALESCE(v_upper_bound, v_prefix_lower) ELSE v_prefix_lower END, v_file_batch_size
            LOOP
                v_common_prefix := storage.get_common_prefix(lower(v_current.name), v_prefix_lower, v_delimiter);

                IF v_common_prefix IS NOT NULL THEN
                    -- Hit a folder: exit batch, let peek handle it
                    v_next_seek := lower(v_current.name);
                    EXIT;
                END IF;

                -- Handle offset skipping
                IF v_skipped < offsets THEN
                    v_skipped := v_skipped + 1;
                ELSE
                    -- Emit file
                    name := split_part(v_current.name, v_delimiter, levels);
                    id := v_current.id;
                    updated_at := v_current.updated_at;
                    created_at := v_current.created_at;
                    last_accessed_at := v_current.last_accessed_at;
                    metadata := v_current.metadata;
                    RETURN NEXT;
                    v_count := v_count + 1;
                END IF;

                -- Advance seek past this file
                IF v_is_asc THEN
                    v_next_seek := lower(v_current.name) || v_delimiter;
                ELSE
                    v_next_seek := lower(v_current.name);
                END IF;

                EXIT WHEN v_count >= v_limit;
            END LOOP;
        END IF;
    END LOOP;
END;
$_$;


--
-- Name: search_by_timestamp(text, text, integer, integer, text, text, text, text); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.search_by_timestamp(p_prefix text, p_bucket_id text, p_limit integer, p_level integer, p_start_after text, p_sort_order text, p_sort_column text, p_sort_column_after text) RETURNS TABLE(key text, name text, id uuid, updated_at timestamp with time zone, created_at timestamp with time zone, last_accessed_at timestamp with time zone, metadata jsonb)
    LANGUAGE plpgsql STABLE
    AS $_$
DECLARE
    v_cursor_op text;
    v_query text;
    v_prefix text;
BEGIN
    v_prefix := coalesce(p_prefix, '');

    IF p_sort_order = 'asc' THEN
        v_cursor_op := '>';
    ELSE
        v_cursor_op := '<';
    END IF;

    v_query := format($sql$
        WITH raw_objects AS (
            SELECT
                o.name AS obj_name,
                o.id AS obj_id,
                o.updated_at AS obj_updated_at,
                o.created_at AS obj_created_at,
                o.last_accessed_at AS obj_last_accessed_at,
                o.metadata AS obj_metadata,
                storage.get_common_prefix(o.name, $1, '/') AS common_prefix
            FROM storage.objects o
            WHERE o.bucket_id = $2
              AND o.name COLLATE "C" LIKE $1 || '%%'
        ),
        -- Aggregate common prefixes (folders)
        -- Both created_at and updated_at use MIN(obj_created_at) to match the old prefixes table behavior
        aggregated_prefixes AS (
            SELECT
                rtrim(common_prefix, '/') AS name,
                NULL::uuid AS id,
                MIN(obj_created_at) AS updated_at,
                MIN(obj_created_at) AS created_at,
                NULL::timestamptz AS last_accessed_at,
                NULL::jsonb AS metadata,
                TRUE AS is_prefix
            FROM raw_objects
            WHERE common_prefix IS NOT NULL
            GROUP BY common_prefix
        ),
        leaf_objects AS (
            SELECT
                obj_name AS name,
                obj_id AS id,
                obj_updated_at AS updated_at,
                obj_created_at AS created_at,
                obj_last_accessed_at AS last_accessed_at,
                obj_metadata AS metadata,
                FALSE AS is_prefix
            FROM raw_objects
            WHERE common_prefix IS NULL
        ),
        combined AS (
            SELECT * FROM aggregated_prefixes
            UNION ALL
            SELECT * FROM leaf_objects
        ),
        filtered AS (
            SELECT *
            FROM combined
            WHERE (
                $5 = ''
                OR ROW(
                    date_trunc('milliseconds', %I),
                    name COLLATE "C"
                ) %s ROW(
                    COALESCE(NULLIF($6, '')::timestamptz, 'epoch'::timestamptz),
                    $5
                )
            )
        )
        SELECT
            split_part(name, '/', $3) AS key,
            name,
            id,
            updated_at,
            created_at,
            last_accessed_at,
            metadata
        FROM filtered
        ORDER BY
            COALESCE(date_trunc('milliseconds', %I), 'epoch'::timestamptz) %s,
            name COLLATE "C" %s
        LIMIT $4
    $sql$,
        p_sort_column,
        v_cursor_op,
        p_sort_column,
        p_sort_order,
        p_sort_order
    );

    RETURN QUERY EXECUTE v_query
    USING v_prefix, p_bucket_id, p_level, p_limit, p_start_after, p_sort_column_after;
END;
$_$;


--
-- Name: search_v2(text, text, integer, integer, text, text, text, text); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.search_v2(prefix text, bucket_name text, limits integer DEFAULT 100, levels integer DEFAULT 1, start_after text DEFAULT ''::text, sort_order text DEFAULT 'asc'::text, sort_column text DEFAULT 'name'::text, sort_column_after text DEFAULT ''::text) RETURNS TABLE(key text, name text, id uuid, updated_at timestamp with time zone, created_at timestamp with time zone, last_accessed_at timestamp with time zone, metadata jsonb)
    LANGUAGE plpgsql STABLE
    AS $$
DECLARE
    v_sort_col text;
    v_sort_ord text;
    v_limit int;
BEGIN
    -- Cap limit to maximum of 1500 records
    v_limit := LEAST(coalesce(limits, 100), 1500);

    -- Validate and normalize sort_order
    v_sort_ord := lower(coalesce(sort_order, 'asc'));
    IF v_sort_ord NOT IN ('asc', 'desc') THEN
        v_sort_ord := 'asc';
    END IF;

    -- Validate and normalize sort_column
    v_sort_col := lower(coalesce(sort_column, 'name'));
    IF v_sort_col NOT IN ('name', 'updated_at', 'created_at') THEN
        v_sort_col := 'name';
    END IF;

    -- Route to appropriate implementation
    IF v_sort_col = 'name' THEN
        -- Use list_objects_with_delimiter for name sorting (most efficient: O(k * log n))
        RETURN QUERY
        SELECT
            split_part(l.name, '/', levels) AS key,
            l.name AS name,
            l.id,
            l.updated_at,
            l.created_at,
            l.last_accessed_at,
            l.metadata
        FROM storage.list_objects_with_delimiter(
            bucket_name,
            coalesce(prefix, ''),
            '/',
            v_limit,
            start_after,
            '',
            v_sort_ord
        ) l;
    ELSE
        -- Use aggregation approach for timestamp sorting
        -- Not efficient for large datasets but supports correct pagination
        RETURN QUERY SELECT * FROM storage.search_by_timestamp(
            prefix, bucket_name, v_limit, levels, start_after,
            v_sort_ord, v_sort_col, sort_column_after
        );
    END IF;
END;
$$;


--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: storage; Owner: -
--

CREATE FUNCTION storage.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW; 
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: audit_log_entries; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.audit_log_entries (
    instance_id uuid,
    id uuid NOT NULL,
    payload json,
    created_at timestamp with time zone,
    ip_address character varying(64) DEFAULT ''::character varying NOT NULL
);


--
-- Name: TABLE audit_log_entries; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.audit_log_entries IS 'Auth: Audit trail for user actions.';


--
-- Name: custom_oauth_providers; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.custom_oauth_providers (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    provider_type text NOT NULL,
    identifier text NOT NULL,
    name text NOT NULL,
    client_id text NOT NULL,
    client_secret text NOT NULL,
    acceptable_client_ids text[] DEFAULT '{}'::text[] NOT NULL,
    scopes text[] DEFAULT '{}'::text[] NOT NULL,
    pkce_enabled boolean DEFAULT true NOT NULL,
    attribute_mapping jsonb DEFAULT '{}'::jsonb NOT NULL,
    authorization_params jsonb DEFAULT '{}'::jsonb NOT NULL,
    enabled boolean DEFAULT true NOT NULL,
    email_optional boolean DEFAULT false NOT NULL,
    issuer text,
    discovery_url text,
    skip_nonce_check boolean DEFAULT false NOT NULL,
    cached_discovery jsonb,
    discovery_cached_at timestamp with time zone,
    authorization_url text,
    token_url text,
    userinfo_url text,
    jwks_uri text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT custom_oauth_providers_authorization_url_https CHECK (((authorization_url IS NULL) OR (authorization_url ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_authorization_url_length CHECK (((authorization_url IS NULL) OR (char_length(authorization_url) <= 2048))),
    CONSTRAINT custom_oauth_providers_client_id_length CHECK (((char_length(client_id) >= 1) AND (char_length(client_id) <= 512))),
    CONSTRAINT custom_oauth_providers_discovery_url_length CHECK (((discovery_url IS NULL) OR (char_length(discovery_url) <= 2048))),
    CONSTRAINT custom_oauth_providers_identifier_format CHECK ((identifier ~ '^[a-z0-9][a-z0-9:-]{0,48}[a-z0-9]$'::text)),
    CONSTRAINT custom_oauth_providers_issuer_length CHECK (((issuer IS NULL) OR ((char_length(issuer) >= 1) AND (char_length(issuer) <= 2048)))),
    CONSTRAINT custom_oauth_providers_jwks_uri_https CHECK (((jwks_uri IS NULL) OR (jwks_uri ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_jwks_uri_length CHECK (((jwks_uri IS NULL) OR (char_length(jwks_uri) <= 2048))),
    CONSTRAINT custom_oauth_providers_name_length CHECK (((char_length(name) >= 1) AND (char_length(name) <= 100))),
    CONSTRAINT custom_oauth_providers_oauth2_requires_endpoints CHECK (((provider_type <> 'oauth2'::text) OR ((authorization_url IS NOT NULL) AND (token_url IS NOT NULL) AND (userinfo_url IS NOT NULL)))),
    CONSTRAINT custom_oauth_providers_oidc_discovery_url_https CHECK (((provider_type <> 'oidc'::text) OR (discovery_url IS NULL) OR (discovery_url ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_oidc_issuer_https CHECK (((provider_type <> 'oidc'::text) OR (issuer IS NULL) OR (issuer ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_oidc_requires_issuer CHECK (((provider_type <> 'oidc'::text) OR (issuer IS NOT NULL))),
    CONSTRAINT custom_oauth_providers_provider_type_check CHECK ((provider_type = ANY (ARRAY['oauth2'::text, 'oidc'::text]))),
    CONSTRAINT custom_oauth_providers_token_url_https CHECK (((token_url IS NULL) OR (token_url ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_token_url_length CHECK (((token_url IS NULL) OR (char_length(token_url) <= 2048))),
    CONSTRAINT custom_oauth_providers_userinfo_url_https CHECK (((userinfo_url IS NULL) OR (userinfo_url ~~ 'https://%'::text))),
    CONSTRAINT custom_oauth_providers_userinfo_url_length CHECK (((userinfo_url IS NULL) OR (char_length(userinfo_url) <= 2048)))
);


--
-- Name: flow_state; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.flow_state (
    id uuid NOT NULL,
    user_id uuid,
    auth_code text,
    code_challenge_method auth.code_challenge_method,
    code_challenge text,
    provider_type text NOT NULL,
    provider_access_token text,
    provider_refresh_token text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    authentication_method text NOT NULL,
    auth_code_issued_at timestamp with time zone,
    invite_token text,
    referrer text,
    oauth_client_state_id uuid,
    linking_target_id uuid,
    email_optional boolean DEFAULT false NOT NULL
);


--
-- Name: TABLE flow_state; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.flow_state IS 'Stores metadata for all OAuth/SSO login flows';


--
-- Name: identities; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.identities (
    provider_id text NOT NULL,
    user_id uuid NOT NULL,
    identity_data jsonb NOT NULL,
    provider text NOT NULL,
    last_sign_in_at timestamp with time zone,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    email text GENERATED ALWAYS AS (lower((identity_data ->> 'email'::text))) STORED,
    id uuid DEFAULT gen_random_uuid() NOT NULL
);


--
-- Name: TABLE identities; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.identities IS 'Auth: Stores identities associated to a user.';


--
-- Name: COLUMN identities.email; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON COLUMN auth.identities.email IS 'Auth: Email is a generated column that references the optional email property in the identity_data';


--
-- Name: instances; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.instances (
    id uuid NOT NULL,
    uuid uuid,
    raw_base_config text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);


--
-- Name: TABLE instances; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.instances IS 'Auth: Manages users across multiple sites.';


--
-- Name: mfa_amr_claims; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.mfa_amr_claims (
    session_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    authentication_method text NOT NULL,
    id uuid NOT NULL
);


--
-- Name: TABLE mfa_amr_claims; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.mfa_amr_claims IS 'auth: stores authenticator method reference claims for multi factor authentication';


--
-- Name: mfa_challenges; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.mfa_challenges (
    id uuid NOT NULL,
    factor_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    verified_at timestamp with time zone,
    ip_address inet NOT NULL,
    otp_code text,
    web_authn_session_data jsonb
);


--
-- Name: TABLE mfa_challenges; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.mfa_challenges IS 'auth: stores metadata about challenge requests made';


--
-- Name: mfa_factors; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.mfa_factors (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    friendly_name text,
    factor_type auth.factor_type NOT NULL,
    status auth.factor_status NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    secret text,
    phone text,
    last_challenged_at timestamp with time zone,
    web_authn_credential jsonb,
    web_authn_aaguid uuid,
    last_webauthn_challenge_data jsonb
);


--
-- Name: TABLE mfa_factors; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.mfa_factors IS 'auth: stores metadata about factors';


--
-- Name: COLUMN mfa_factors.last_webauthn_challenge_data; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON COLUMN auth.mfa_factors.last_webauthn_challenge_data IS 'Stores the latest WebAuthn challenge data including attestation/assertion for customer verification';


--
-- Name: oauth_authorizations; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.oauth_authorizations (
    id uuid NOT NULL,
    authorization_id text NOT NULL,
    client_id uuid NOT NULL,
    user_id uuid,
    redirect_uri text NOT NULL,
    scope text NOT NULL,
    state text,
    resource text,
    code_challenge text,
    code_challenge_method auth.code_challenge_method,
    response_type auth.oauth_response_type DEFAULT 'code'::auth.oauth_response_type NOT NULL,
    status auth.oauth_authorization_status DEFAULT 'pending'::auth.oauth_authorization_status NOT NULL,
    authorization_code text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone DEFAULT (now() + '00:03:00'::interval) NOT NULL,
    approved_at timestamp with time zone,
    nonce text,
    CONSTRAINT oauth_authorizations_authorization_code_length CHECK ((char_length(authorization_code) <= 255)),
    CONSTRAINT oauth_authorizations_code_challenge_length CHECK ((char_length(code_challenge) <= 128)),
    CONSTRAINT oauth_authorizations_expires_at_future CHECK ((expires_at > created_at)),
    CONSTRAINT oauth_authorizations_nonce_length CHECK ((char_length(nonce) <= 255)),
    CONSTRAINT oauth_authorizations_redirect_uri_length CHECK ((char_length(redirect_uri) <= 2048)),
    CONSTRAINT oauth_authorizations_resource_length CHECK ((char_length(resource) <= 2048)),
    CONSTRAINT oauth_authorizations_scope_length CHECK ((char_length(scope) <= 4096)),
    CONSTRAINT oauth_authorizations_state_length CHECK ((char_length(state) <= 4096))
);


--
-- Name: oauth_client_states; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.oauth_client_states (
    id uuid NOT NULL,
    provider_type text NOT NULL,
    code_verifier text,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: TABLE oauth_client_states; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.oauth_client_states IS 'Stores OAuth states for third-party provider authentication flows where Supabase acts as the OAuth client.';


--
-- Name: oauth_clients; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.oauth_clients (
    id uuid NOT NULL,
    client_secret_hash text,
    registration_type auth.oauth_registration_type NOT NULL,
    redirect_uris text NOT NULL,
    grant_types text NOT NULL,
    client_name text,
    client_uri text,
    logo_uri text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    deleted_at timestamp with time zone,
    client_type auth.oauth_client_type DEFAULT 'confidential'::auth.oauth_client_type NOT NULL,
    token_endpoint_auth_method text NOT NULL,
    CONSTRAINT oauth_clients_client_name_length CHECK ((char_length(client_name) <= 1024)),
    CONSTRAINT oauth_clients_client_uri_length CHECK ((char_length(client_uri) <= 2048)),
    CONSTRAINT oauth_clients_logo_uri_length CHECK ((char_length(logo_uri) <= 2048)),
    CONSTRAINT oauth_clients_token_endpoint_auth_method_check CHECK ((token_endpoint_auth_method = ANY (ARRAY['client_secret_basic'::text, 'client_secret_post'::text, 'none'::text])))
);


--
-- Name: oauth_consents; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.oauth_consents (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    client_id uuid NOT NULL,
    scopes text NOT NULL,
    granted_at timestamp with time zone DEFAULT now() NOT NULL,
    revoked_at timestamp with time zone,
    CONSTRAINT oauth_consents_revoked_after_granted CHECK (((revoked_at IS NULL) OR (revoked_at >= granted_at))),
    CONSTRAINT oauth_consents_scopes_length CHECK ((char_length(scopes) <= 2048)),
    CONSTRAINT oauth_consents_scopes_not_empty CHECK ((char_length(TRIM(BOTH FROM scopes)) > 0))
);


--
-- Name: one_time_tokens; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.one_time_tokens (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    token_type auth.one_time_token_type NOT NULL,
    token_hash text NOT NULL,
    relates_to text NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT one_time_tokens_token_hash_check CHECK ((char_length(token_hash) > 0))
);


--
-- Name: refresh_tokens; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.refresh_tokens (
    instance_id uuid,
    id bigint NOT NULL,
    token character varying(255),
    user_id character varying(255),
    revoked boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    parent character varying(255),
    session_id uuid
);


--
-- Name: TABLE refresh_tokens; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.refresh_tokens IS 'Auth: Store of tokens used to refresh JWT tokens once they expire.';


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE; Schema: auth; Owner: -
--

CREATE SEQUENCE auth.refresh_tokens_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: auth; Owner: -
--

ALTER SEQUENCE auth.refresh_tokens_id_seq OWNED BY auth.refresh_tokens.id;


--
-- Name: saml_providers; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.saml_providers (
    id uuid NOT NULL,
    sso_provider_id uuid NOT NULL,
    entity_id text NOT NULL,
    metadata_xml text NOT NULL,
    metadata_url text,
    attribute_mapping jsonb,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    name_id_format text,
    CONSTRAINT "entity_id not empty" CHECK ((char_length(entity_id) > 0)),
    CONSTRAINT "metadata_url not empty" CHECK (((metadata_url = NULL::text) OR (char_length(metadata_url) > 0))),
    CONSTRAINT "metadata_xml not empty" CHECK ((char_length(metadata_xml) > 0))
);


--
-- Name: TABLE saml_providers; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.saml_providers IS 'Auth: Manages SAML Identity Provider connections.';


--
-- Name: saml_relay_states; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.saml_relay_states (
    id uuid NOT NULL,
    sso_provider_id uuid NOT NULL,
    request_id text NOT NULL,
    for_email text,
    redirect_to text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    flow_state_id uuid,
    CONSTRAINT "request_id not empty" CHECK ((char_length(request_id) > 0))
);


--
-- Name: TABLE saml_relay_states; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.saml_relay_states IS 'Auth: Contains SAML Relay State information for each Service Provider initiated login.';


--
-- Name: schema_migrations; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.schema_migrations (
    version character varying(255) NOT NULL
);


--
-- Name: TABLE schema_migrations; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.schema_migrations IS 'Auth: Manages updates to the auth system.';


--
-- Name: sessions; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.sessions (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    factor_id uuid,
    aal auth.aal_level,
    not_after timestamp with time zone,
    refreshed_at timestamp without time zone,
    user_agent text,
    ip inet,
    tag text,
    oauth_client_id uuid,
    refresh_token_hmac_key text,
    refresh_token_counter bigint,
    scopes text,
    CONSTRAINT sessions_scopes_length CHECK ((char_length(scopes) <= 4096))
);


--
-- Name: TABLE sessions; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.sessions IS 'Auth: Stores session data associated to a user.';


--
-- Name: COLUMN sessions.not_after; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON COLUMN auth.sessions.not_after IS 'Auth: Not after is a nullable column that contains a timestamp after which the session should be regarded as expired.';


--
-- Name: COLUMN sessions.refresh_token_hmac_key; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON COLUMN auth.sessions.refresh_token_hmac_key IS 'Holds a HMAC-SHA256 key used to sign refresh tokens for this session.';


--
-- Name: COLUMN sessions.refresh_token_counter; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON COLUMN auth.sessions.refresh_token_counter IS 'Holds the ID (counter) of the last issued refresh token.';


--
-- Name: sso_domains; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.sso_domains (
    id uuid NOT NULL,
    sso_provider_id uuid NOT NULL,
    domain text NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    CONSTRAINT "domain not empty" CHECK ((char_length(domain) > 0))
);


--
-- Name: TABLE sso_domains; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.sso_domains IS 'Auth: Manages SSO email address domain mapping to an SSO Identity Provider.';


--
-- Name: sso_providers; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.sso_providers (
    id uuid NOT NULL,
    resource_id text,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    disabled boolean,
    CONSTRAINT "resource_id not empty" CHECK (((resource_id = NULL::text) OR (char_length(resource_id) > 0)))
);


--
-- Name: TABLE sso_providers; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.sso_providers IS 'Auth: Manages SSO identity provider information; see saml_providers for SAML.';


--
-- Name: COLUMN sso_providers.resource_id; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON COLUMN auth.sso_providers.resource_id IS 'Auth: Uniquely identifies a SSO provider according to a user-chosen resource ID (case insensitive), useful in infrastructure as code.';


--
-- Name: users; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.users (
    instance_id uuid,
    id uuid NOT NULL,
    aud character varying(255),
    role character varying(255),
    email character varying(255),
    encrypted_password character varying(255),
    email_confirmed_at timestamp with time zone,
    invited_at timestamp with time zone,
    confirmation_token character varying(255),
    confirmation_sent_at timestamp with time zone,
    recovery_token character varying(255),
    recovery_sent_at timestamp with time zone,
    email_change_token_new character varying(255),
    email_change character varying(255),
    email_change_sent_at timestamp with time zone,
    last_sign_in_at timestamp with time zone,
    raw_app_meta_data jsonb,
    raw_user_meta_data jsonb,
    is_super_admin boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    phone text DEFAULT NULL::character varying,
    phone_confirmed_at timestamp with time zone,
    phone_change text DEFAULT ''::character varying,
    phone_change_token character varying(255) DEFAULT ''::character varying,
    phone_change_sent_at timestamp with time zone,
    confirmed_at timestamp with time zone GENERATED ALWAYS AS (LEAST(email_confirmed_at, phone_confirmed_at)) STORED,
    email_change_token_current character varying(255) DEFAULT ''::character varying,
    email_change_confirm_status smallint DEFAULT 0,
    banned_until timestamp with time zone,
    reauthentication_token character varying(255) DEFAULT ''::character varying,
    reauthentication_sent_at timestamp with time zone,
    is_sso_user boolean DEFAULT false NOT NULL,
    deleted_at timestamp with time zone,
    is_anonymous boolean DEFAULT false NOT NULL,
    CONSTRAINT users_email_change_confirm_status_check CHECK (((email_change_confirm_status >= 0) AND (email_change_confirm_status <= 2)))
);


--
-- Name: TABLE users; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON TABLE auth.users IS 'Auth: Stores user login data within a secure schema.';


--
-- Name: COLUMN users.is_sso_user; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON COLUMN auth.users.is_sso_user IS 'Auth: Set this column to true when the account comes from SSO. These accounts can have duplicate emails.';


--
-- Name: webauthn_challenges; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.webauthn_challenges (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    challenge_type text NOT NULL,
    session_data jsonb NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    CONSTRAINT webauthn_challenges_challenge_type_check CHECK ((challenge_type = ANY (ARRAY['signup'::text, 'registration'::text, 'authentication'::text])))
);


--
-- Name: webauthn_credentials; Type: TABLE; Schema: auth; Owner: -
--

CREATE TABLE auth.webauthn_credentials (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    credential_id bytea NOT NULL,
    public_key bytea NOT NULL,
    attestation_type text DEFAULT ''::text NOT NULL,
    aaguid uuid,
    sign_count bigint DEFAULT 0 NOT NULL,
    transports jsonb DEFAULT '[]'::jsonb NOT NULL,
    backup_eligible boolean DEFAULT false NOT NULL,
    backed_up boolean DEFAULT false NOT NULL,
    friendly_name text DEFAULT ''::text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    last_used_at timestamp with time zone
);


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: contactes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contactes (
    id uuid NOT NULL,
    municipi_id uuid NOT NULL,
    nom character varying(200) NOT NULL,
    carrec character varying(200),
    email character varying(255),
    telefon character varying(50),
    linkedin character varying(255),
    notes_humanes text,
    actiu boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: contactes_v2; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contactes_v2 (
    id uuid NOT NULL,
    municipi_id uuid NOT NULL,
    nom character varying(100) NOT NULL,
    carrec public.carrec NOT NULL,
    email character varying(100),
    telefon character varying(20),
    actiu boolean,
    principal boolean,
    angles_exitosos jsonb,
    angles_fallits jsonb,
    moment_optimal character varying(10),
    to_preferit public.to_comunicacio,
    data_creacio timestamp with time zone DEFAULT now()
);


--
-- Name: deal_activitats; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.deal_activitats (
    id uuid NOT NULL,
    deal_id uuid NOT NULL,
    tipus character varying(50) NOT NULL,
    descripcio text NOT NULL,
    valor_anterior character varying(255),
    valor_nou character varying(255),
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: deals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.deals (
    id uuid NOT NULL,
    municipi_id uuid NOT NULL,
    contacte_id uuid,
    titol character varying(300) NOT NULL,
    etapa character varying(50) NOT NULL,
    valor_setup numeric(10,2),
    valor_llicencia numeric(10,2),
    prioritat character varying(20),
    notes_humanes text,
    proper_pas text,
    data_seguiment date,
    data_tancament_prev date,
    data_tancament_real date,
    motiu_perdua text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: email_drafts_v2; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_drafts_v2 (
    id uuid NOT NULL,
    municipi_id uuid NOT NULL,
    contacte_id uuid,
    estat public.estat_draft,
    subject character varying(200),
    cos text,
    generat_per_ia boolean,
    prompt_utilitzat text,
    variants_generades jsonb,
    variant_seleccionada integer,
    editat_per_usuari boolean,
    canvis_respecte_ia jsonb,
    data_enviament timestamp with time zone,
    enviat_des_de character varying(100),
    email_enviat_id uuid,
    data_creacio timestamp with time zone DEFAULT now()
);


--
-- Name: email_sequencies_v2; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_sequencies_v2 (
    id uuid NOT NULL,
    municipi_id uuid NOT NULL,
    numero_email integer NOT NULL,
    tipus_sequencia public.tipus_sequencia NOT NULL,
    estat public.estat_sequencia,
    data_programada timestamp with time zone,
    data_enviada timestamp with time zone,
    draft_id uuid,
    obert boolean,
    data_obertura timestamp with time zone,
    respost boolean,
    seguent_accio character varying(50)
);


--
-- Name: emails; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.emails (
    id uuid NOT NULL,
    deal_id uuid,
    contacte_id uuid,
    campanya_id uuid,
    from_address character varying(255) NOT NULL,
    to_address character varying(255) NOT NULL,
    assumpte character varying(500) NOT NULL,
    cos text,
    direccio character varying(3) NOT NULL,
    llegit boolean,
    sincronitzat boolean,
    message_id_extern character varying(500),
    data_email timestamp with time zone NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    tracking_token character varying(100),
    obert boolean,
    data_obertura timestamp with time zone,
    nombre_obertures integer,
    ip_obertura character varying(50)
);


--
-- Name: emails_v2; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.emails_v2 (
    id uuid NOT NULL,
    municipi_id uuid NOT NULL,
    data_enviament timestamp with time zone DEFAULT now(),
    assumpte character varying(200),
    cos text,
    obert boolean,
    data_obertura timestamp with time zone,
    cops_obert integer,
    respost boolean,
    data_resposta timestamp with time zone,
    sentiment_resposta public.sentiment,
    intents_detectats jsonb,
    actor_probable public.actor
);


--
-- Name: llicencies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.llicencies (
    id uuid NOT NULL,
    deal_id uuid NOT NULL,
    data_inici date NOT NULL,
    data_renovacio date NOT NULL,
    estat character varying(50),
    notes text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: memoria_municipis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.memoria_municipis (
    municipi_id uuid NOT NULL,
    ganxos_exitosos jsonb,
    angles_fallits jsonb,
    moment_optimal jsonb,
    llenguatge_preferit jsonb,
    blockers_resolts jsonb,
    data_actualitzacio timestamp with time zone DEFAULT now()
);


--
-- Name: municipis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.municipis (
    id uuid NOT NULL,
    nom character varying(200) NOT NULL,
    tipus character varying(50) NOT NULL,
    provincia character varying(100),
    poblacio character varying(255),
    web character varying(255),
    telefon character varying(50),
    adreca text,
    notes text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    codi_postal character varying(10)
);


--
-- Name: municipis_lifecycle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.municipis_lifecycle (
    id uuid NOT NULL,
    nom character varying(100) NOT NULL,
    comarca character varying(50),
    poblacio integer,
    geografia public.geografia,
    diagnostic_digital jsonb,
    angle_personalitzacio text,
    etapa_actual public.etapa_funnel,
    historial_etapes jsonb,
    blocker_actual public.blocker,
    temperatura public.temperatura,
    dies_etapa_actual integer,
    data_conversio timestamp without time zone,
    pla_contractat public.pla,
    estat_final public.estat_final,
    actor_principal_id uuid,
    data_creacio timestamp with time zone DEFAULT now(),
    data_ultima_accio timestamp with time zone DEFAULT now(),
    usuari_asignat character varying(50)
);


--
-- Name: pagaments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pagaments (
    id uuid NOT NULL,
    llicencia_id uuid NOT NULL,
    import numeric(10,2) NOT NULL,
    tipus character varying(50) NOT NULL,
    estat character varying(50),
    data_emisio date NOT NULL,
    data_limit date,
    data_confirmacio date,
    notes text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: patrons_municipis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.patrons_municipis (
    id uuid NOT NULL,
    rang_poblacio character varying(20),
    tipus_geografia public.geografia_patro,
    context_politic character varying(20),
    probabilitat_conversio double precision,
    temps_mitja_cicle_dies integer,
    etapa_bloqueig_frequent character varying(50),
    estrategia_recomanada text,
    objeccions_frequents jsonb,
    casos_exit_referencia jsonb,
    cops_aplicat integer,
    exitosos integer
);


--
-- Name: reunions_v2; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reunions_v2 (
    id uuid NOT NULL,
    municipi_id uuid NOT NULL,
    data timestamp with time zone,
    tipus character varying(20),
    assistents jsonb,
    aar_completat boolean,
    notes_aar text,
    poi_mes_reaccio character varying(100),
    objeccio_principal character varying(100),
    cta_final character varying(200),
    temperatura_post public.temperatura_post
);


--
-- Name: tasques; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tasques (
    id uuid NOT NULL,
    deal_id uuid,
    contacte_id uuid,
    municipi_id uuid,
    usuari_id uuid,
    titol character varying(300) NOT NULL,
    descripcio text,
    data_venciment date NOT NULL,
    tipus character varying(50),
    prioritat character varying(20),
    estat character varying(20),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: trucades_v2; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.trucades_v2 (
    id uuid NOT NULL,
    municipi_id uuid NOT NULL,
    data timestamp with time zone DEFAULT now(),
    durada_minuts integer,
    qui_va_contestar public.actor_respuesta,
    notes_breus text,
    resum_ia text,
    seguent_accio_sugerida text
);


--
-- Name: usuaris; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuaris (
    id uuid NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    nom character varying(100) NOT NULL,
    rol character varying(50),
    actiu boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


--
-- Name: messages; Type: TABLE; Schema: realtime; Owner: -
--

CREATE TABLE realtime.messages (
    topic text NOT NULL,
    extension text NOT NULL,
    payload jsonb,
    event text,
    private boolean DEFAULT false,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    inserted_at timestamp without time zone DEFAULT now() NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL
)
PARTITION BY RANGE (inserted_at);


--
-- Name: schema_migrations; Type: TABLE; Schema: realtime; Owner: -
--

CREATE TABLE realtime.schema_migrations (
    version bigint NOT NULL,
    inserted_at timestamp(0) without time zone
);


--
-- Name: subscription; Type: TABLE; Schema: realtime; Owner: -
--

CREATE TABLE realtime.subscription (
    id bigint NOT NULL,
    subscription_id uuid NOT NULL,
    entity regclass NOT NULL,
    filters realtime.user_defined_filter[] DEFAULT '{}'::realtime.user_defined_filter[] NOT NULL,
    claims jsonb NOT NULL,
    claims_role regrole GENERATED ALWAYS AS (realtime.to_regrole((claims ->> 'role'::text))) STORED NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    action_filter text DEFAULT '*'::text,
    CONSTRAINT subscription_action_filter_check CHECK ((action_filter = ANY (ARRAY['*'::text, 'INSERT'::text, 'UPDATE'::text, 'DELETE'::text])))
);


--
-- Name: subscription_id_seq; Type: SEQUENCE; Schema: realtime; Owner: -
--

ALTER TABLE realtime.subscription ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME realtime.subscription_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: buckets; Type: TABLE; Schema: storage; Owner: -
--

CREATE TABLE storage.buckets (
    id text NOT NULL,
    name text NOT NULL,
    owner uuid,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    public boolean DEFAULT false,
    avif_autodetection boolean DEFAULT false,
    file_size_limit bigint,
    allowed_mime_types text[],
    owner_id text,
    type storage.buckettype DEFAULT 'STANDARD'::storage.buckettype NOT NULL
);


--
-- Name: COLUMN buckets.owner; Type: COMMENT; Schema: storage; Owner: -
--

COMMENT ON COLUMN storage.buckets.owner IS 'Field is deprecated, use owner_id instead';


--
-- Name: buckets_analytics; Type: TABLE; Schema: storage; Owner: -
--

CREATE TABLE storage.buckets_analytics (
    name text NOT NULL,
    type storage.buckettype DEFAULT 'ANALYTICS'::storage.buckettype NOT NULL,
    format text DEFAULT 'ICEBERG'::text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    deleted_at timestamp with time zone
);


--
-- Name: buckets_vectors; Type: TABLE; Schema: storage; Owner: -
--

CREATE TABLE storage.buckets_vectors (
    id text NOT NULL,
    type storage.buckettype DEFAULT 'VECTOR'::storage.buckettype NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: migrations; Type: TABLE; Schema: storage; Owner: -
--

CREATE TABLE storage.migrations (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    hash character varying(40) NOT NULL,
    executed_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: objects; Type: TABLE; Schema: storage; Owner: -
--

CREATE TABLE storage.objects (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    bucket_id text,
    name text,
    owner uuid,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    last_accessed_at timestamp with time zone DEFAULT now(),
    metadata jsonb,
    path_tokens text[] GENERATED ALWAYS AS (string_to_array(name, '/'::text)) STORED,
    version text,
    owner_id text,
    user_metadata jsonb
);


--
-- Name: COLUMN objects.owner; Type: COMMENT; Schema: storage; Owner: -
--

COMMENT ON COLUMN storage.objects.owner IS 'Field is deprecated, use owner_id instead';


--
-- Name: s3_multipart_uploads; Type: TABLE; Schema: storage; Owner: -
--

CREATE TABLE storage.s3_multipart_uploads (
    id text NOT NULL,
    in_progress_size bigint DEFAULT 0 NOT NULL,
    upload_signature text NOT NULL,
    bucket_id text NOT NULL,
    key text NOT NULL COLLATE pg_catalog."C",
    version text NOT NULL,
    owner_id text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    user_metadata jsonb
);


--
-- Name: s3_multipart_uploads_parts; Type: TABLE; Schema: storage; Owner: -
--

CREATE TABLE storage.s3_multipart_uploads_parts (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    upload_id text NOT NULL,
    size bigint DEFAULT 0 NOT NULL,
    part_number integer NOT NULL,
    bucket_id text NOT NULL,
    key text NOT NULL COLLATE pg_catalog."C",
    etag text NOT NULL,
    owner_id text,
    version text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: vector_indexes; Type: TABLE; Schema: storage; Owner: -
--

CREATE TABLE storage.vector_indexes (
    id text DEFAULT gen_random_uuid() NOT NULL,
    name text NOT NULL COLLATE pg_catalog."C",
    bucket_id text NOT NULL,
    data_type text NOT NULL,
    dimension integer NOT NULL,
    distance_metric text NOT NULL,
    metadata_configuration jsonb,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: refresh_tokens id; Type: DEFAULT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.refresh_tokens ALTER COLUMN id SET DEFAULT nextval('auth.refresh_tokens_id_seq'::regclass);


--
-- Data for Name: audit_log_entries; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.audit_log_entries (instance_id, id, payload, created_at, ip_address) FROM stdin;
\.


--
-- Data for Name: custom_oauth_providers; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.custom_oauth_providers (id, provider_type, identifier, name, client_id, client_secret, acceptable_client_ids, scopes, pkce_enabled, attribute_mapping, authorization_params, enabled, email_optional, issuer, discovery_url, skip_nonce_check, cached_discovery, discovery_cached_at, authorization_url, token_url, userinfo_url, jwks_uri, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.flow_state (id, user_id, auth_code, code_challenge_method, code_challenge, provider_type, provider_access_token, provider_refresh_token, created_at, updated_at, authentication_method, auth_code_issued_at, invite_token, referrer, oauth_client_state_id, linking_target_id, email_optional) FROM stdin;
\.


--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.identities (provider_id, user_id, identity_data, provider, last_sign_in_at, created_at, updated_at, id) FROM stdin;
\.


--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.instances (id, uuid, raw_base_config, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.mfa_amr_claims (session_id, created_at, updated_at, authentication_method, id) FROM stdin;
\.


--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.mfa_challenges (id, factor_id, created_at, verified_at, ip_address, otp_code, web_authn_session_data) FROM stdin;
\.


--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.mfa_factors (id, user_id, friendly_name, factor_type, status, created_at, updated_at, secret, phone, last_challenged_at, web_authn_credential, web_authn_aaguid, last_webauthn_challenge_data) FROM stdin;
\.


--
-- Data for Name: oauth_authorizations; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.oauth_authorizations (id, authorization_id, client_id, user_id, redirect_uri, scope, state, resource, code_challenge, code_challenge_method, response_type, status, authorization_code, created_at, expires_at, approved_at, nonce) FROM stdin;
\.


--
-- Data for Name: oauth_client_states; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.oauth_client_states (id, provider_type, code_verifier, created_at) FROM stdin;
\.


--
-- Data for Name: oauth_clients; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.oauth_clients (id, client_secret_hash, registration_type, redirect_uris, grant_types, client_name, client_uri, logo_uri, created_at, updated_at, deleted_at, client_type, token_endpoint_auth_method) FROM stdin;
\.


--
-- Data for Name: oauth_consents; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.oauth_consents (id, user_id, client_id, scopes, granted_at, revoked_at) FROM stdin;
\.


--
-- Data for Name: one_time_tokens; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.one_time_tokens (id, user_id, token_type, token_hash, relates_to, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.refresh_tokens (instance_id, id, token, user_id, revoked, created_at, updated_at, parent, session_id) FROM stdin;
\.


--
-- Data for Name: saml_providers; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.saml_providers (id, sso_provider_id, entity_id, metadata_xml, metadata_url, attribute_mapping, created_at, updated_at, name_id_format) FROM stdin;
\.


--
-- Data for Name: saml_relay_states; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.saml_relay_states (id, sso_provider_id, request_id, for_email, redirect_to, created_at, updated_at, flow_state_id) FROM stdin;
\.


--
-- Data for Name: schema_migrations; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.schema_migrations (version) FROM stdin;
20171026211738
20171026211808
20171026211834
20180103212743
20180108183307
20180119214651
20180125194653
00
20210710035447
20210722035447
20210730183235
20210909172000
20210927181326
20211122151130
20211124214934
20211202183645
20220114185221
20220114185340
20220224000811
20220323170000
20220429102000
20220531120530
20220614074223
20220811173540
20221003041349
20221003041400
20221011041400
20221020193600
20221021073300
20221021082433
20221027105023
20221114143122
20221114143410
20221125140132
20221208132122
20221215195500
20221215195800
20221215195900
20230116124310
20230116124412
20230131181311
20230322519590
20230402418590
20230411005111
20230508135423
20230523124323
20230818113222
20230914180801
20231027141322
20231114161723
20231117164230
20240115144230
20240214120130
20240306115329
20240314092811
20240427152123
20240612123726
20240729123726
20240802193726
20240806073726
20241009103726
20250717082212
20250731150234
20250804100000
20250901200500
20250903112500
20250904133000
20250925093508
20251007112900
20251104100000
20251111201300
20251201000000
20260115000000
20260121000000
20260219120000
20260302000000
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.sessions (id, user_id, created_at, updated_at, factor_id, aal, not_after, refreshed_at, user_agent, ip, tag, oauth_client_id, refresh_token_hmac_key, refresh_token_counter, scopes) FROM stdin;
\.


--
-- Data for Name: sso_domains; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.sso_domains (id, sso_provider_id, domain, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: sso_providers; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.sso_providers (id, resource_id, created_at, updated_at, disabled) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.users (instance_id, id, aud, role, email, encrypted_password, email_confirmed_at, invited_at, confirmation_token, confirmation_sent_at, recovery_token, recovery_sent_at, email_change_token_new, email_change, email_change_sent_at, last_sign_in_at, raw_app_meta_data, raw_user_meta_data, is_super_admin, created_at, updated_at, phone, phone_confirmed_at, phone_change, phone_change_token, phone_change_sent_at, email_change_token_current, email_change_confirm_status, banned_until, reauthentication_token, reauthentication_sent_at, is_sso_user, deleted_at, is_anonymous) FROM stdin;
\.


--
-- Data for Name: webauthn_challenges; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.webauthn_challenges (id, user_id, challenge_type, session_data, created_at, expires_at) FROM stdin;
\.


--
-- Data for Name: webauthn_credentials; Type: TABLE DATA; Schema: auth; Owner: -
--

COPY auth.webauthn_credentials (id, user_id, credential_id, public_key, attestation_type, aaguid, sign_count, transports, backup_eligible, backed_up, friendly_name, created_at, updated_at, last_used_at) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alembic_version (version_num) FROM stdin;
a3f5e76d049d
\.


--
-- Data for Name: contactes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) FROM stdin;
b5e7c612-dcdc-49ed-9e49-f78edefa741c	b0988c73-01e8-4354-94aa-e4c3795511dc	Josep Maria Tirbió i Civís 	Regidor de Turisme	mia@lapobladesegur.cat	\N	\N	\N	t	2026-03-10 18:55:56.662685+00	2026-03-10 18:55:56.662685+00
53983083-7a16-4591-bfba-7a852a4b1d44	b0988c73-01e8-4354-94aa-e4c3795511dc	 Marc Baró i Bernaduca	Alcalde	alcaldia@lapobladesegur.cat	\N	\N	\N	t	2026-03-10 18:54:45.023885+00	2026-03-10 18:54:45.023885+00
1a433539-031d-44ab-82be-baedf1c17811	78a2343f-dbf5-4707-9e44-5622d03fb5cb	Baldo Farré Serrat 	Alcalde	alcaldia@sort.cat	\N	\N	\N	t	2026-03-12 11:00:17.047496+00	2026-03-12 11:00:17.047496+00
1e022c62-e440-428e-9550-a107e8e50c12	76993a09-1cc4-4288-ae93-c2aed91f5278	 Jordi Alcobé Font	Cònsol Major	comu@canillo.ad	(+376) 751 036	\N	\N	t	2026-03-16 10:56:54.792186+00	2026-03-16 10:56:54.792186+00
c64e9de5-0919-44a5-8e37-5886359b184f	76993a09-1cc4-4288-ae93-c2aed91f5278	 Marc Casal	Cònsol Menor	turisme@canillo.ad	\N	\N	\N	t	2026-03-16 10:57:36.861931+00	2026-03-16 10:57:36.861931+00
d323117a-11e4-448a-badc-9058b3f4bd32	388104f6-3294-4fa6-9fc0-ebca33eec086	 Josep Ramon Fondevila Isus 	Alcalde	ajuntament@soriguera.ddl.net	\N	\N	\N	t	2026-03-16 11:32:43.497594+00	2026-03-16 11:32:43.497594+00
9a77e835-1d42-42e7-b497-2ede3948f73b	388104f6-3294-4fa6-9fc0-ebca33eec086	Ariadna Vidal	lidera les excavacions i el relat científic del jaciment.	info@museudecamins.com	\N	\N	\N	t	2026-03-16 11:37:12.598402+00	2026-03-16 11:37:12.598402+00
3f543baf-2ae0-4513-9a9b-54b8b97b02c1	117d35c3-b4c5-406d-a8d4-8cb58393bf52	Jeannine Abella i Chica	Alcaldessa	ajuntament@isona.ddl.net	973 664 008	\N	\N	t	2026-03-19 17:20:38.173686+00	2026-03-19 17:20:38.173686+00
66dd3892-3736-4bd8-9c0f-ca27d484ae14	af9ca22a-4e96-47e8-b284-1d1fba3f97fa	María Luengo	\N	\N	722652089	\N	\N	t	2026-03-19 17:43:27.481022+00	2026-03-19 17:43:27.481022+00
de4cbf85-800b-4cda-9b1b-3dfece9ae6d3	322a61f2-bddc-45ee-ae31-d79f279cdedf	Iolanda Ferran i Closa	Alcaldessa	ajuntament@elpontdesuert.cat	973 690 005	\N	\N	t	2026-03-19 18:01:08.102013+00	2026-03-19 18:01:08.102013+00
7563ae81-5953-4720-b7e2-0558f127e651	322a61f2-bddc-45ee-ae31-d79f279cdedf	Susanna Garrido i Castro	Regidora de Comunicació i TIC	ajuntament@elpontdesuert.cat	973 690 005	\N	\N	t	2026-03-19 18:03:01.377617+00	2026-03-19 18:03:01.377617+00
779138ee-9918-494a-94ad-2c2de9adb1e2	d47fde40-f1d9-4255-8ad2-9813c5fd8f25	Eva Perisé 	Regidora turisme	eperise@torrecapdella.cat	 973 66 32 62 	\N	\N	t	2026-03-16 09:43:37.372438+00	2026-03-20 11:53:42.617106+00
63e2e3b1-9363-48ac-833d-8b374cad0dc7	d47fde40-f1d9-4255-8ad2-9813c5fd8f25	Josep Maria Dalmau Gil 	Alcalde	jmdalmau@torrecapdella.cat	973 66 30 01 	\N	\N	t	2026-03-16 09:42:09.058303+00	2026-03-20 11:53:57.730706+00
ed326611-e34c-4e5a-a8ad-3ad9af8bbfd7	d47fde40-f1d9-4255-8ad2-9813c5fd8f25	Ramon Jordana	 Regidor de la Torre de Capdela 	rjordana@torrecapdella.cat	\N	\N	\N	t	2026-03-20 11:45:33.724267+00	2026-03-20 11:56:23.201686+00
00efd101-915b-48dd-bb00-8e09526d8bf1	78a2343f-dbf5-4707-9e44-5622d03fb5cb	Gerard Aguado	turisme	turisme@sort.cat	973620010	\N	\N	t	2026-03-12 11:00:48.70712+00	2026-03-23 09:18:12.318517+00
531b277b-ad47-4d95-96f2-a213e09043f7	388104f6-3294-4fa6-9fc0-ebca33eec086	Nuria	Administrativa	ajuntamentdesoriguera@gmail.com	973 62 06 09	\N	\N	t	2026-03-23 09:36:39.139092+00	2026-03-23 09:36:39.139092+00
94e68e67-cb27-4b4d-a3eb-ba26ec5f8817	117d35c3-b4c5-406d-a8d4-8cb58393bf52	Ariadna Roca Melines	Regidora de Turisme i Transf. Digital	ariadnaroca2002@gmail.com	973 664 008	\N	\N	t	2026-03-19 17:21:45.776847+00	2026-03-23 09:55:17.475955+00
1f4435f6-b943-4f04-b391-1eaf77d872ba	78a2343f-dbf5-4707-9e44-5622d03fb5cb	 Pere Báscones Navarro 	| Àrea: Cultura, Educació, Turisme, Sostenibilitat i Noves  Tecnologies. 	pbascones@sort.cat	639 30 30 67 	\N	\N	t	2026-03-23 11:04:17.600403+00	2026-03-23 11:04:17.600403+00
bca93a14-db52-48b2-b801-041730f1edff	322a61f2-bddc-45ee-ae31-d79f279cdedf	Josep M. Rispa i Pifarré	Regidor de Turisme, Cultura i Patrimoni	regidoriacultura@elpontdesuert.cat	973 690 005	\N	\N	t	2026-03-19 18:02:02.018974+00	2026-03-23 11:29:48.344451+00
\.


--
-- Data for Name: contactes_v2; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.contactes_v2 (id, municipi_id, nom, carrec, email, telefon, actiu, principal, angles_exitosos, angles_fallits, moment_optimal, to_preferit, data_creacio) FROM stdin;
779138ee-9918-494a-94ad-2c2de9adb1e2	d47fde40-f1d9-4255-8ad2-9813c5fd8f25	Eva Perisé 	regidor_turisme	admin@vallfosca.net	\N	t	f	[]	[]	\N	formal	2026-03-17 20:06:56.783381+00
63e2e3b1-9363-48ac-833d-8b374cad0dc7	d47fde40-f1d9-4255-8ad2-9813c5fd8f25	Josep Maria Dalmau Gil 	alcalde	admin@vallfosca.net	\N	t	t	[]	[]	\N	formal	2026-03-17 20:06:56.783381+00
1a433539-031d-44ab-82be-baedf1c17811	78a2343f-dbf5-4707-9e44-5622d03fb5cb	Baldo Farré Serrat 	alcalde	alcaldia@sort.cat	\N	t	t	[]	[]	\N	formal	2026-03-17 20:06:56.783381+00
00efd101-915b-48dd-bb00-8e09526d8bf1	78a2343f-dbf5-4707-9e44-5622d03fb5cb	Gerard Aguado	regidor_turisme	turisme@sort.cat	\N	t	f	[]	[]	\N	formal	2026-03-17 20:06:56.783381+00
b5e7c612-dcdc-49ed-9e49-f78edefa741c	b0988c73-01e8-4354-94aa-e4c3795511dc	Josep Maria Tirbió i Civís 	regidor_turisme	mia@lapobladesegur.cat	\N	t	f	[]	[]	\N	formal	2026-03-17 20:06:56.783381+00
53983083-7a16-4591-bfba-7a852a4b1d44	b0988c73-01e8-4354-94aa-e4c3795511dc	 Marc Baró i Bernaduca	alcalde	alcaldia@lapobladesegur.cat	\N	t	t	[]	[]	\N	formal	2026-03-17 20:06:56.783381+00
1e022c62-e440-428e-9550-a107e8e50c12	76993a09-1cc4-4288-ae93-c2aed91f5278	 Jordi Alcobé Font	altre	comu@canillo.ad	(+376) 751 036	t	f	[]	[]	\N	formal	2026-03-17 20:06:56.783381+00
c64e9de5-0919-44a5-8e37-5886359b184f	76993a09-1cc4-4288-ae93-c2aed91f5278	 Marc Casal	altre	turisme@canillo.ad	\N	t	t	[]	[]	\N	formal	2026-03-17 20:06:56.783381+00
d323117a-11e4-448a-badc-9058b3f4bd32	388104f6-3294-4fa6-9fc0-ebca33eec086	 Josep Ramon Fondevila Isus 	alcalde	ajuntament@soriguera.ddl.net	\N	t	t	[]	[]	\N	formal	2026-03-17 20:06:56.783381+00
9a77e835-1d42-42e7-b497-2ede3948f73b	388104f6-3294-4fa6-9fc0-ebca33eec086	Ariadna Vidal	altre	info@museudecamins.com	\N	t	f	[]	[]	\N	formal	2026-03-17 20:06:56.783381+00
\.


--
-- Data for Name: deal_activitats; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.deal_activitats (id, deal_id, tipus, descripcio, valor_anterior, valor_nou, created_at) FROM stdin;
3357f9b4-91bb-4a05-a331-9ebe57771272	b0193e49-c46b-4645-a726-903aad57ab57	canvi_etapa	Canvi d'etapa: de 'prospecte' a 'contacte_inicial'	prospecte	contacte_inicial	2026-03-11 13:34:12.424418+00
77aa4b18-b989-411b-858a-0489da173b1f	d427d8a7-b977-44dc-ad40-dff00d37da3e	canvi_etapa	Canvi d'etapa: de 'prospecte' a 'contacte_inicial'	prospecte	contacte_inicial	2026-03-12 11:07:30.076979+00
6a16fce5-a47c-4657-b7b7-1497a3a058f5	d427d8a7-b977-44dc-ad40-dff00d37da3e	canvi_etapa	Canvi d'etapa: de 'contacte_inicial' a 'prospecte'	contacte_inicial	prospecte	2026-03-12 11:07:31.422685+00
1d1f6f4d-3cd3-406c-9c26-f27cd355cac4	b0193e49-c46b-4645-a726-903aad57ab57	canvi_etapa	Canvi d'etapa: de 'contacte_inicial' a 'prospecte'	contacte_inicial	prospecte	2026-03-12 11:07:38.795705+00
94231caa-675b-41e6-8813-198801db3dd4	b0193e49-c46b-4645-a726-903aad57ab57	canvi_etapa	Canvi d'etapa: de 'prospecte' a 'proposta_enviada'	prospecte	proposta_enviada	2026-03-16 15:40:05.32869+00
17565775-00df-40f3-b7d1-e43906a22438	b0193e49-c46b-4645-a726-903aad57ab57	canvi_etapa	Canvi d'etapa: de 'proposta_enviada' a 'demo_feta'	proposta_enviada	demo_feta	2026-03-16 15:40:09.089593+00
dbe93503-fcff-474c-80ca-1e8a1a59ee92	b0193e49-c46b-4645-a726-903aad57ab57	canvi_etapa	Canvi d'etapa: de 'demo_feta' a 'prospecte'	demo_feta	prospecte	2026-03-16 15:40:11.94375+00
729c0541-c984-4dbd-9daa-06d4c279dfc1	b0193e49-c46b-4645-a726-903aad57ab57	canvi_etapa	Canvi d'etapa: de 'prospecte' a 'contacte_inicial'	prospecte	contacte_inicial	2026-03-16 15:44:16.887268+00
68614cc4-2a7e-4c47-8dc4-9c34a56c5015	484e3468-2ed3-4211-8307-15c7b12af329	email_enviat	Email enviat: Sobre el relat digital del patrimoni del Pont de Suert	\N	\N	2026-03-23 10:52:32.679755+00
6805d227-9faa-4a1e-be9e-931c1b25d927	d427d8a7-b977-44dc-ad40-dff00d37da3e	canvi_etapa	Canvi d'etapa: de 'prospecte' a 'contacte_inicial'	prospecte	contacte_inicial	2026-03-23 12:00:03.056521+00
\.


--
-- Data for Name: deals; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.deals (id, municipi_id, contacte_id, titol, etapa, valor_setup, valor_llicencia, prioritat, notes_humanes, proper_pas, data_seguiment, data_tancament_prev, data_tancament_real, motiu_perdua, created_at, updated_at) FROM stdin;
2e5361cc-6f1d-460f-9872-eaa1dd6a3e80	76993a09-1cc4-4288-ae93-c2aed91f5278	c64e9de5-0919-44a5-8e37-5886359b184f	Projecte ROURE	prospecte	3500.00	2500.00	mitjana	\N	primer email	\N	\N	\N	\N	2026-03-16 11:00:07.729966+00	2026-03-16 11:00:07.729966+00
e4bb29ee-73a3-4cbf-a2cd-9bfb31b0463c	388104f6-3294-4fa6-9fc0-ebca33eec086	d323117a-11e4-448a-badc-9058b3f4bd32	Projecte ROURE	prospecte	3500.00	2500.00	mitjana	\N	\N	\N	\N	\N	\N	2026-03-16 11:43:08.493868+00	2026-03-16 11:43:08.493868+00
b0193e49-c46b-4645-a726-903aad57ab57	b0988c73-01e8-4354-94aa-e4c3795511dc	53983083-7a16-4591-bfba-7a852a4b1d44	ROURE5 - Projecte	contacte_inicial	3500.00	2500.00	alta	Acabar de perfilar els punts de ruta.	demo en persona	2026-03-26	2026-04-10	\N	\N	2026-03-10 19:20:32.405688+00	2026-03-17 20:17:29.107176+00
e4345303-303f-4387-91e8-fd7643b7e99c	d47fde40-f1d9-4255-8ad2-9813c5fd8f25	63e2e3b1-9363-48ac-833d-8b374cad0dc7	Projecte ROURE	prospecte	3500.00	2500.00	mitjana	Enviats segons correus inclos nou contacte Ramon president de Consell Comarcal.\nEva Perise esta de baixa fins el 30/4/26,Contacte amb Sandra de turisme.	eva Perise esta de baixa fins el 30/4/26, Rependre contacte.	2026-04-14	\N	\N	\N	2026-03-16 09:53:56.01049+00	2026-03-23 11:47:50.349917+00
473f02c9-2b4b-4ad0-acec-751463f60247	117d35c3-b4c5-406d-a8d4-8cb58393bf52	\N	Projecte ROURE	prospecte	3500.00	2500.00	mitjana	fet primer contacte amb la Ariadna	enviar segon email	2026-03-27	2026-04-30	\N	\N	2026-03-23 10:01:23.677832+00	2026-03-23 11:48:52.391241+00
484e3468-2ed3-4211-8307-15c7b12af329	5cfe1986-555e-4e28-bc9e-ac500ac0cd4b	bca93a14-db52-48b2-b801-041730f1edff	Projecte ROURE	prospecte	3500.00	2500.00	mitjana		segon email	2026-03-27	2026-04-30	\N	\N	2026-03-23 10:45:39.600903+00	2026-03-23 11:50:47.202115+00
d427d8a7-b977-44dc-ad40-dff00d37da3e	78a2343f-dbf5-4707-9e44-5622d03fb5cb	1a433539-031d-44ab-82be-baedf1c17811	Projecte ROURE	contacte_inicial	3500.00	2500.00	mitjana	Contacte telefonic amb en gerard, enviament correu a Pere Bascones. mPreparar demo per divendres 27/3	trucar en Pere	2026-03-24	2026-03-16	\N	\N	2026-03-12 11:05:27.943955+00	2026-03-23 15:30:53.222816+00
\.


--
-- Data for Name: email_drafts_v2; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.email_drafts_v2 (id, municipi_id, contacte_id, estat, subject, cos, generat_per_ia, prompt_utilitzat, variants_generades, variant_seleccionada, editat_per_usuari, canvis_respecte_ia, data_enviament, enviat_des_de, email_enviat_id, data_creacio) FROM stdin;
b396d2db-ce40-4056-bfcc-57c7b666d501	b0988c73-01e8-4354-94aa-e4c3795511dc	\N	esborrany	La Pobla, el relat que el món llegirà	Alcalde,\n\nVostè ha fet de la Pobla un far de futur; ara cal que el relat sigui seu. Si el municipi no controla la seva veu digital, altres ho faran per vostè.\n\nImagini’s un turista que busca "Pobla de Segur" i troba una història que vostè no ha escrit. Això es vota.\n\nTé 10 minuts demà per decidir qui narra el seu llegat?\n\nRespon SÍ i li explico com.	t	\nActuant per a: Alcalde (Visionari). Vol llegat, visibilitat, guanyar eleccions.\nMissatge-clau: sobirania digital, control del relat, "el teu municipi al mapa".\nRegles: Mai funcionalitats tècniques. Sempre impacte polític i territorial.\nTo: proximitat, "tu", company de trinxera.\n\n\nSituació: Primer contacte. Ganxo patrimoni/digitalització específic.\nRegles: Màxim 120 paraules. Zero enllaços. Zero emojis.\nEstructura: Ganxo personalitzat -> Dolor subtil -> CTA binari.\n	[{"cos": "Alcalde,\\n\\nVostè ha fet de la Pobla un far de futur; ara cal que el relat sigui seu. Si el municipi no controla la seva veu digital, altres ho faran per vostè.\\n\\nImagini’s un turista que busca \\"Pobla de Segur\\" i troba una història que vostè no ha escrit. Això es vota.\\n\\nTé 10 minuts demà per decidir qui narra el seu llegat?\\n\\nRespon SÍ i li explico com.", "angle": "sobirania narrativa", "score": 0.92, "subject": "La Pobla, el relat que el món llegirà"}, {"cos": "Et parla el veí de trenta minuts que vol veure el teu poble protagonista.\\n\\nMentre altres ajuntaments es gasten el pressupost en plataformes que no controlen, la Pobla pot ser el primer municipi de la Vall que tingui titularitat plena de la seva televisió, ràdio i xarxes. Imagina decidir quina imatge surt a l’informatiu, quins projectes es viralitzen i quins emprenedors locals ocupen portada.\\n\\nAquest setembre estem ajudant tres alcaldes a fer-ho sense tocar el pressupost. T’apuntes a la conversa?\\n\\nRespon sí o sí i et truco demà al matí.", "angle": "Lideratge territorial", "score": 0.92, "subject": "Pobla de Segur pot liderar la Catalunya digital"}, {"cos": "Com alcalde, tens el repte de deixar empremta i que el teu poble no sigui una marca blanca al mapa quan et jubilis. La majoria de municipis depenen d’empreses fora del territori per decidir quan i com es parla d’ells: notícies a mitjans aliens, dades a la prestatgeria d’un despatx de Barcelona.\\n\\nAmb el projecte Sobirania Digital pots convertir Pobla de Segur en referent: tu ordines la narrativa, tu esculls què es publica i quan, i acabes legislatura amb la cartera d’actius digitals que et recordarà fins i tot l’oposició.\\n\\nVols que et prepari la proposta pilot per al teu pròxim plenari? Et truco demà al matí?", "angle": "Llegat digital i control del relat", "score": 0.87, "subject": "Pobla de Segur, tens l’oportunitat de pilotar la sobirania digital"}]	0	f	{}	\N	\N	\N	2026-03-17 20:51:55.138594+00
8bca3f64-2cc6-4baa-a532-91b3ceab335a	b0988c73-01e8-4354-94aa-e4c3795511dc	53983083-7a16-4591-bfba-7a852a4b1d44	esborrany	Marc: convertim la Pobla en referent de sobirania digital	Marc, \n\nAvui és dia de posar la Pobla de Segur al mapa i no només de paraula. Imagina controlar tu, des d’aquí, l’impacte que sortim als mitjans, la reputació digital de la Pobla i la narrativa que marcarà el teu llegat. \n\nVull proposar-te una estratègia que converteixi la teva gestió en exemple per la resta del territori i et doni arma electoral clara per al 2027. \n\n15 minuts aquesta setmana n’hi ha prou? \n\nSi vols, dimarts o dimecres al matí?	t	\nActuant per a: Alcalde (Visionari). Vol llegat, visibilitat, guanyar eleccions.\nMissatge-clau: sobirania digital, control del relat, "el teu municipi al mapa".\nRegles: Mai funcionalitats tècniques. Sempre impacte polític i territorial.\nTo: proximitat, "tu", company de trinxera.\n\n\nSituació: Primer contacte. Ganxo patrimoni/digitalització específic.\nRegles: Màxim 120 paraules. Zero enllaços. Zero emojis.\nEstructura: Ganxo personalitzat -> Dolor subtil -> CTA binari.\n	[{"cos": "Marc,\\n\\nHe vist com defensa el teu llegat patrimonial a les xarxes. Imagina que el teu municipi no només el preserva, sinó que el projecta com a referent digital de tot el país.\\n\\nEls rivals polítics ja controlen el relat online. Tu tens 18 mesos per decidir si la Pobla lidera o segueix.\\n\\nEt sona si parlem 10 minuts demà al matí?\\n\\nSalut,\\n\\nJoan", "angle": "Lideratge digital urgent", "score": 0.87, "subject": "Marc, Pobla de Segur pot liderar la Catalunya digital"}, {"cos": "Marc, he vist com has convertit la Pobla en referent de turisme sostenible. Però on és la veu del teu municipi quan TV3 parla del territori? \\n\\nEls grans mitjans acaben decidint la narrativa del Pallars Jussà. I tu, que has lluitat per fer visible la Pobla, et mereixes controlar el relat.\\n\\nEt proposo un cafè a la plaça Major per mostrar-te com podem garantir que la Pobla lideri la conversa digital del territori. \\n\\nDijous a les 10h et va bé?", "angle": "Control narratiu territorial", "score": 0.85, "subject": "Marc, vull compartir-te una idea que podria posar la Pobla al centre del debat nacional"}, {"cos": "Marc, \\n\\nAvui és dia de posar la Pobla de Segur al mapa i no només de paraula. Imagina controlar tu, des d’aquí, l’impacte que sortim als mitjans, la reputació digital de la Pobla i la narrativa que marcarà el teu llegat. \\n\\nVull proposar-te una estratègia que converteixi la teva gestió en exemple per la resta del territori i et doni arma electoral clara per al 2027. \\n\\n15 minuts aquesta setmana n’hi ha prou? \\n\\nSi vols, dimarts o dimecres al matí?", "angle": "ganxo èpic + CTA binari zero ficció", "score": 0.93, "subject": "Marc: convertim la Pobla en referent de sobirania digital"}]	2	f	{}	\N	\N	\N	2026-03-17 21:09:28.105524+00
8be05460-6f21-4991-884a-413e771f5d79	b0988c73-01e8-4354-94aa-e4c3795511dc	53983083-7a16-4591-bfba-7a852a4b1d44	esborrany	Marc, volem posar Pobla de Segur al mapa d’èxits digitals	Ets de pobla i m’agrada parlar-te com a company: el teu llegat es juga ara. Si algú fora controla el relat del que passa al nostre territori, perdem vots i inversió. Però si tu tens la sobirania digital, la Pobla guanya visibilitat, tu guanyes eleccions.\n\nVols que parlem 15 minuts? Sí o no.	t	\nActuant per a: Alcalde (Visionari). Vol llegat, visibilitat, guanyar eleccions.\nMissatge-clau: sobirania digital, control del relat, "el teu municipi al mapa".\nRegles: Mai funcionalitats tècniques. Sempre impacte polític i territorial.\nTo: proximitat, "tu", company de trinxera.\n\n\nSituació: Primer contacte. Ganxo patrimoni/digitalització específic.\nRegles: Màxim 120 paraules. Zero enllaços. Zero emojis.\nEstructura: Ganxo personalitzat -> Dolor subtil -> CTA binari.\n	[{"cos": "Ets l’alcalde que pot posar la Pobla de Segur al centre del mapa de la sobirania digital del país.\\n\\nMentre d’altres esperen subvencions, els municipis que ja han dit \\"sí\\" controlen el relat del seu territori: decideixen què es explica i com, i ho fan des d’una plataforma que és seva, no d’un proveïdor exterior. Guanyen visibilitat, atrauen inversions i deixen empremta per a les pròximes generacions.\\n\\nEt proposo 15 minuts per mostrar-te com la Pobla pot ser el proper cas d’èxit. Dijous o divendres t’aniria bé?", "angle": "Sobirania digital = llegat electoral", "score": 0.92, "subject": "Marc, el teu poble pot liderar la Catalunya digital"}, {"cos": "Marc, quan algú cerca la Pobla, ¿qui controla el que surt? Si ara mateix el relat és Google o la premsa de fora, perds sobirania sobre el territori que has fet créixer.\\n\\nL’alcalde que converteix el seu municipi en referent digital marca el seu llegat. Et proposo 15 minuts per dibuixar com la teva Pobla pot ser l’exemple que tots copiïn.\\n\\nPuc comptar amb tu demà a les 10 o a les 4?", "angle": "Ganxo llegat digital i control del relat per alcalde visionari", "score": 0.93, "subject": "Marc, Pobla de Segur pot liderar el relat digital de la Catalunya interior"}, {"cos": "Ets de pobla i m’agrada parlar-te com a company: el teu llegat es juga ara. Si algú fora controla el relat del que passa al nostre territori, perdem vots i inversió. Però si tu tens la sobirania digital, la Pobla guanya visibilitat, tu guanyes eleccions.\\n\\nVols que parlem 15 minuts? Sí o no.", "angle": "sobirania digital = vots", "score": 0.94, "subject": "Marc, volem posar Pobla de Segur al mapa d’èxits digitals"}]	2	f	{}	\N	\N	\N	2026-03-17 21:09:27.17254+00
\.


--
-- Data for Name: email_sequencies_v2; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.email_sequencies_v2 (id, municipi_id, numero_email, tipus_sequencia, estat, data_programada, data_enviada, draft_id, obert, data_obertura, respost, seguent_accio) FROM stdin;
\.


--
-- Data for Name: emails; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) FROM stdin;
31f06037-3ede-4deb-b924-46876903079a	b0193e49-c46b-4645-a726-903aad57ab57	b5e7c612-dcdc-49ed-9e49-f78edefa741c	\N	miquel@projectexinoxano.cat	mia@lapobladesegur.cat	 La feina de turisme a La Pobla (li acabo de comentar al Marc)	Hola Josep Maria,\nSoc Miquel Utge, de Sort.  Li acabo d'enviar un correu al Marc Baró comentant-li una idea estratègica per recuperar el control digital de La Pobla, però sé perfectament que el dia a dia, les hores de feina i el pes de la promoció turística recauen sobre tu i el teu equip.\nSé la feinada que suposa documentar, mantenir viu i promocionar un patrimoni com el de la baixada dels Raiers, les Falles o el Molí de l'Oli. El problema frustrant que estem veient a molts ajuntaments és que, després de tota la vostra feina de recerca i creació de materials, quan el turista baixa del Tren dels Llacs obre Google Maps i és l'algoritme qui decideix com se li explica el poble. Treballeu a cegues perquè ells es queden les dades.\nHem creat una eina precisament per treure-us aquesta càrrega de feina i fer que el vostre esforç llueixi, recuperant el control. La nostra IA agafa el material històric i els fulletons que ja teniu fets, i us estructura rutes i audioguies web interactives en 15 minuts.\nPerò el més important per al teu dia a dia: la plataforma us genera automàticament informes completíssims amb mapes de calor. Per fi podreu veure de forma visual per quins carrers es mouen exactament els visitants, quant de temps es paren davant de cada actiu i entendre el seu comportament real per justificar qualsevol acció de turisme.\nPerquè vegis que no és teoria, he recollit documentació històrica sobre els Raiers i he preparat una petita maqueta immersiva on podràs veure com donem vida al vostre fons documental i com es recullen aquestes dades.\nCom ho tens per buscar un forat de 10 minuts la setmana entrant i t'ho ensenyo? Sense cap compromís.\nUna abraçada,\nMiquel Utge\n622836542	OUT	t	t	\N	2026-03-11 14:32:46.834563+00	2026-03-11 13:32:46.837388+00	59b95c3e60ec44919f4a49c823d637c0	f	\N	0	\N
750311af-f48c-46f9-b7d9-ddb93cabf3a9	b0193e49-c46b-4645-a726-903aad57ab57	53983083-7a16-4591-bfba-7a852a4b1d44	\N	miquel@projectexinoxano.cat	alcaldia@lapobladesegur.cat	 La història de La Pobla a internet (i qui se'n queda les dades)	Hola Marc,\nSoc Miquel Utge, de Sort. T'escric perquè estem parlant amb diversos ajuntaments que han decidit dir prou a una situació molt frustrant: fer un gran esforç econòmic per mantenir el patrimoni, però dependre totalment de Google Maps i TripAdvisor perquè els visitants el descobreixin.\n\nA La Pobla de Segur teniu un llegat impressionant. Amb la memòria viva de l'ofici als voltants del Museu dels Raiers o la conservació d'espais com el Molí de l'Oli de Sant Josep, heu fet una gran feina de protecció cultural. Però quan el visitant camina pels vostres carrers i obre el mòbil, qui li explica aquesta història? Ara mateix és l'algoritme qui decideix què veuen, i totes les dades d'aquests turistes se les queden les grans plataformes, no l'Ajuntament.\n\nA Projecte xino-xano hem creat una infraestructura pensada justament per a consistoris com el vostre per recuperar aquesta sobirania digital territorial. Sense desenvolupaments complexos: amb la simple introducció de material històric, cultural o natural del vostre arxiu municipal, la nostra tecnologia estructura i prepara rutes interactives i audioguies web en qüestió de minuts. Donem vida al vostre fons documental. Així, el relat oficial el controleu vosaltres i les dades d'ús es queden a La Pobla.\n\nHe recollit documentació històrica sobre la baixada dels raiers i he muntat una petita maqueta perquè vegis com quedaria aquesta experiència immersiva, 100% pròpia i controlada per vosaltres.\n\nCom ho tens per buscar un forat de 10 minuts la setmana entrant i t'ho ensenyo? Sense cap compromís, només perquè vegis com funciona.\n\nUna abraçada,\nMiquel\n622836542	OUT	t	t	\N	2026-03-11 14:29:31.406931+00	2026-03-11 13:29:31.410442+00	12712398383944308ba0093d52c88c48	f	\N	0	\N
098c5ed9-beb9-43f6-89fa-651084631c5c	d427d8a7-b977-44dc-ad40-dff00d37da3e	1a433539-031d-44ab-82be-baedf1c17811	\N	miquel@projectexinoxano.cat	alcaldia@sort.cat	El Castell de Sort a Google / Sobirania territorial	Hola Baldo,\n\nHe vist la bona feina que feu a Sort defensant un model que posa en valor la memòria històrica, com el Castell i la Presó-Museu, i que va molt més enllà del turisme d'estiu.\n\nPerò passa una cosa que veiem sovint: l'Ajuntament inverteix a mantenir aquest patrimoni, però quan el visitant hi arriba, qui li explica el poble és l'algoritme de Google. Ells decideixen què es veu i ells es queden les dades de la vostra gent. Sort posa la feina, ells s'emporten l'or.\n\nHem creat una infraestructura digital sobirana que evita això. La nostra IA agafa els vostres PDFs actuals i crea audioguies 100% vostres en 15 minuts. Com a capital del Pallars, Sort hauria de liderar aquest canvi.\n\nHe fet una prova ràpida amb el PDF de la Vila Closa de Sort. Tens 10 minuts dimarts o dijous al matí per veure-ho funcionant?\n\nUna abraçada,\n\nMiquel Utge\nProjecte Xino Xano\nSobirania Digital Territorial	OUT	t	t	\N	2026-03-12 12:04:36.130699+00	2026-03-12 11:04:39.229483+00	3685337ae8144db5bd4b9e3ea7ca45e7	f	\N	0	\N
e375def5-4a9c-4a18-861a-636c984b45c8	b0193e49-c46b-4645-a726-903aad57ab57	53983083-7a16-4591-bfba-7a852a4b1d44	\N	miquel@projectexinoxano.cat	alcaldia@lapobladesegur.cat	Sobre la Casa Mauri i els fons Next Generation	Hola, Marc,\n\nEt recupero el fil de la setmana passada. He estat analitzant el projecte de turisme sostenible que esteu executant amb els fons NextGen i m’ha sorprès la qualitat del fons documental que teniu a La Pobla, especialment sobre el Conjunt Modernista de la Casa Mauri.\n\nT’escric perquè sovint el problema d'aquestes inversions és que es gasta molt en infraestructura física, però el relat digital queda en mans de tercers. Amb la nostra IA implementada dintre del projecte xino-xano, hem fet una prova interna: hem agafat el vostre fulletó PDF i el sistema l’ha convertit en una audioguia immersiva en menys de 15 minuts.\n\nAixò et permet dues coses clau com a alcalde:\n\nRendibilitat real: No cal contractar agències per fer continguts nous; aprofitem el que ja teniu.\nControl polític: El nom de "La Pobla de Segur" és el que brilla, no el d'una multinacional americana.\n\nCom ho tens per fer un cafè de 10 minuts un matí d'aquesta setmana? T’ensenyaré la maqueta que hem preparat amb el vostre material real.\n\nUna abraçada,\nMiquel Utge\n622836542\n\nProjecte Xino Xano\n\n	OUT	t	t	\N	2026-03-16 10:29:50.680712+00	2026-03-16 09:29:58.648991+00	d2f5782c73a34d2381cb93d557be4d1b	f	\N	0	\N
af9976cf-e48b-4597-8b0b-427f3b719ff5	b0193e49-c46b-4645-a726-903aad57ab57	b5e7c612-dcdc-49ed-9e49-f78edefa741c	\N	miquel@projectexinoxano.cat	mia@lapobladesegur.cat	Una eina per entendre què fan els turistes quan baixen del tren	Hola, Josep Maria,\n\nEspero que la setmana hagi començat bé. T’escric perquè sé que un dels reptes que teniu és mesurar l'impacte real dels visitants que arriben amb el Tren dels Llacs un cop es dispersen pel poble.\n\nA Projecte xino-xano no només digitalitzem el patrimoni (com la baixada dels Raiers o el Molí de l'Oli); el que fem és donar-te dades. La nostra plataforma genera automàticament mapes de calor. Per fi podràs veure, amb dades reals i anònimes:\n\nQuins carrers trepitgen realment.\nOn es detenen més temps.\nQuin contingut els interessa i quins ignoren.\nAixí com els emails dels usuaris registrats per posteriors campanyes d'email màrqueting.\n\nÉs el fi de la "pàgina en blanc". Tu puges el material que ja tens i la infraestructura s’encarrega de la resta, lliurant-te informes que et serviran per justificar qualsevol inversió futura davant de l'ajuntament o la diputació.\n\nT’agradaria veure com funcionen aquests informes amb una demo de 10 minuts? Et podria anar bé un matí  de dimarts a dijous?\n\nSalut,\nMiquel Utge\n622836542\n\nProjecte Xino Xano\n\n	OUT	t	t	\N	2026-03-16 10:34:42.197239+00	2026-03-16 09:34:50.182815+00	037341009d134f289e63627b100519f2	f	\N	0	\N
ee198ee0-0a40-4d59-8eb1-20b1a0459c6f	e4345303-303f-4387-91e8-fd7643b7e99c	63e2e3b1-9363-48ac-833d-8b374cad0dc7	\N	miquel@projectexinoxano.cat	admin@vallfosca.net	Att: Josep Maria Dalmau;  La recuperació de l'Hospital de Cartró i el monopoli de Google	Hola, Josep Maria,\n\n He vist l'esforç tan bèstia que esteu fent des de l'Ajuntament per protegir i consolidar l'històric Hospital de cartó a Torre de Capdella. Heu fet molt bona feina protegint el legat físic de la Vall Fosca. Però analitzant la vall, hi ha una cosa que fa mal: quan el turista arriba al Telefèric o a la Central, qui li explica el poble? L'algoritme de Google Maps o rutes no oficials a Wikiloc. L'Ajuntament posa la feina i les inversions, però Silicon Valey s'emporta l'or (les dades i l'atenció) i decideix el que els visitants veuen. A Projecte Xino-Xano,  estem ajudant els municipis pirinencs, com ja hem fet amb el pilot del Palars Sobirà, a recuperar aquesta sobirania. Construïm infraestructura digital perquè tingueu l'audioguia oficial de la vall activada per GPS, sense embrutar el paisatge amb QRs i recuperant el 100% de les dades dels turistes. \n\nM'agradaria ensenyar-te com quedaria la Val Fosca amb sobirania total. \nTens un matí lliure aquesta setmana de dimarts a dijous?\n\nSalut\nMiquel Utge\n622836542\n\nProjecte xino-xano	OUT	t	t	\N	2026-03-16 11:11:59.84569+00	2026-03-16 10:12:07.948776+00	7e5dbe389e1e43a0b0f6d2c46215c533	f	\N	0	\N
7da7a4a3-e55e-4bff-9954-79959686b66f	e4345303-303f-4387-91e8-fd7643b7e99c	779138ee-9918-494a-94ad-2c2de9adb1e2	\N	miquel@projectexinoxano.cat	ajuntament@torredecapdella.ddl.net	Att: Eva Perisé;  Les rutes de la Val Fosca a Wikiloc vs. el relat del Museu	Hola, Eva, \n\nSegueixo de prop la feina immensa de documentació i difusió que feu des del Museu Hidroelèctric. Sou un referent a tot el Pirineu. \n\nEl motiu del correu és que veig a internet com molts turistes, un cop baixen del Telefèric, acaben guiats per ressenyes desordenades de Google o rutes de Wikiloc que no reflecteixen la precisió ni el relat del vostre arxiu. \n\nA Projecte xino-xano hem desenvolupat la IA Punt d'Or. Bàsicament, li passes un PDF o un tríptic dels que ja teniu publicats a vallfosca.net i, en 15 minuts, et genera una audioguia completa i geolocalitzada, sense que hagis de picar ni una línia de text. Estalvi de temps absolut i, sobretot, el domini i les dades són de l'Ajuntament, no d'una plataforma de tercers. He fet una prova ràpida amb la ruta de l'Antic Carrilet per veure l'efecte que fa.\n\nQuan tens 10 minuts perquè t'ho ensenyi per videotrucada?, un matí de dimarts a dijous?, cap a les 11?\n\nUna abraçada, \nMiquel Utge\n622836542\n\nProjecte xino-xano	OUT	t	t	\N	2026-03-16 11:00:01.966954+00	2026-03-16 10:00:10.02811+00	b43fece1a1d14d6fb26f47a6cbb021c8	t	2026-03-16 11:04:50.220251+00	1	127.0.0.1
7794d463-211a-496b-b011-cde4da9c800a	d427d8a7-b977-44dc-ad40-dff00d37da3e	00efd101-915b-48dd-bb00-8e09526d8bf1	\N	miquel@projectexinoxano.cat	turisme@sort.ca	Els PDFs de la Val d'Àssua i el Batliu / Sobirania a Sort	Hola, Gerard, \n\nHe vist l'esforç brutal que feu des de turisme i Sobirà Dinàmic amb les rutes locals. \n\nTeniu un contingut fantàstic als itineraris del Batliu i la Vall  d'Àssua. Heu fet molt bona feina amb el patrimoni. El problema que estem veient a altres municipis és que l'Ajuntament posa tot l'esforç de creació, però quan el turista arriba a la plaça, qui li explica el poble és l'algoritme de Google Maps. I els que es queden totes les dades.\n\nHem desenvolupat una IA que llegeix els vostres propis PDF municipals i els converteix en audioguies interactives i sobiranes en 15 minuts. Sense argot tècnic ni carregar-te de més feina. He fet una prova ràpida amb el vostre tríptic de la Vila Closa. Tens 10 minuts dimecres al matí i te l'ensenyo? \n\nUna abraçada,\nMiquel Utge\n622836542\n\nProjecte xino-xano	OUT	t	t	\N	2026-03-16 11:04:13.9228+00	2026-03-16 10:04:21.997017+00	4a20de99b6314938b58b04a88025e6a2	t	2026-03-16 11:09:49.221533+00	1	127.0.0.1
0fbe33a7-436e-4f4a-a81d-67e493fb8d4f	e4345303-303f-4387-91e8-fd7643b7e99c	63e2e3b1-9363-48ac-833d-8b374cad0dc7	\N	miquel@projectexinoxano.cat	jmdalmau@torrecapdella.cat	L'Hospital de cartó i el monopoli de Google a la Vall Fosca	Hola, Josep Maria,\n\nHeu fet molt bona feina protegint el llegat físic de la Vall Fosca, com l'esforç brutal per consolidar l'històric Hospital de cartó a la Torre de Capdella.\n\nPerò hi ha una cosa que fa mal: quan el turista arriba al Telefèric, qui li explica el poble? L'algoritme de Google Maps o Wikiloc. L'Ajuntament posa la inversió i la feina, però Silicon Valley s'emporta les dades i decideix què veuen els visitants.\n\nA Projecte Xino Xano estem ajudant els municipis a recuperar aquesta sobirania, com ja hem fet al Pallars Sobirà. Construïm infraestructura digital pròpia perquè tingueu l'audioguia oficial de la vall, sense embrutar el paisatge i recuperant el 100% de les dades.\n\nM'agradaria ensenyar-te com queda el mapa de la Vall Fosca amb sobirania total. El dimarts o el dimecres a les 11h et va bé?\n\nSalut,\n\nMiquel Utge\n622836542\nProjecte Xino Xano	OUT	t	t	\N	2026-03-20 12:57:19.125293+00	2026-03-20 11:57:19.370787+00	3e3ef47585f34d77af805870f7e6b35d	f	\N	0	\N
c30df720-8ea6-4a5f-ae7c-5dbd85dfa311	e4345303-303f-4387-91e8-fd7643b7e99c	63e2e3b1-9363-48ac-833d-8b374cad0dc7	\N	miquel@projectexinoxano.cat	ajuntament@torredecapdella.ddl.net	Att: Josep Maria Dalmau; La recuperació de l'Hospital de Cartró i el monopoli de Google	Hola, Josep Maria,\n\n He vist l'esforç tan bèstia que esteu fent des de l'Ajuntament per protegir i consolidar l'històric Hospital de cartó a Torre de Capdella. Heu fet molt bona feina protegint el legat físic de la Vall Fosca. Però analitzant la vall, hi ha una cosa que fa mal: quan el turista arriba al Telefèric o a la Central, qui li explica el poble? L'algoritme de Google Maps o rutes no oficials a Wikiloc. L'Ajuntament posa la feina i les inversions, però Silicon Valey s'emporta l'or (les dades i l'atenció) i decideix el que els visitants veuen. A Projecte Xino-Xano,  estem ajudant els municipis pirinencs, com ja hem fet amb el pilot del Palars Sobirà, a recuperar aquesta sobirania. Construïm infraestructura digital perquè tingueu l'audioguia oficial de la vall activada per GPS, sense embrutar el paisatge amb QRs i recuperant el 100% de les dades dels turistes. \n\nM'agradaria ensenyar-te com quedaria la Val Fosca amb sobirania total. \nTens un matí lliure aquesta setmana de dimarts a dijous?\n\nSalut\nMiquel Utge\n622836542\n\nProjecte xino-xano	OUT	t	t	\N	2026-03-16 10:52:57.452368+00	2026-03-16 09:53:05.48884+00	5c8f810728f54b2fa7fa4e7c24098306	t	2026-03-16 11:10:16.274919+00	1	127.0.0.1
85f49cf2-7443-44d7-9a44-2defafdcbb15	d427d8a7-b977-44dc-ad40-dff00d37da3e	00efd101-915b-48dd-bb00-8e09526d8bf1	\N	miquel@projectexinoxano.cat	turisme@sort.cat	Sobirania a Sort	Hola, Gerard, \n\nHe vist l'esforç brutal que feu des de turisme i Sobirà Dinàmic amb les rutes locals. \n\nTeniu un contingut fantàstic als itineraris del Batliu i la Vall  d'Àssua. Heu fet molt bona feina amb el patrimoni. El problema que estem veient a altres municipis és que l'Ajuntament posa tot l'esforç de creació, però quan el turista arriba a la plaça, qui li explica el poble és l'algoritme de Google Maps. I els que es queden totes les dades.\n\nHem desenvolupat una IA que llegeix els vostres propis PDF municipals i els converteix en audioguies interactives i sobiranes en 15 minuts. Sense argot tècnic ni carregar-te de més feina. He fet una prova ràpida amb el vostre tríptic de la Vila Closa. Tens 10 minuts dimecres al matí i te l'ensenyo? \n\nUna abraçada,\nMiquel Utge\n622836542\n\nProjecte xino-xano	OUT	t	t	\N	2026-03-16 11:14:31.777948+00	2026-03-16 10:14:39.880123+00	4b1d28385da14112937062b68420f09c	f	\N	0	\N
bb25eed9-c459-4d12-aee4-502d8dc9863c	e4345303-303f-4387-91e8-fd7643b7e99c	779138ee-9918-494a-94ad-2c2de9adb1e2	\N	miquel@projectexinoxano.cat	admin@vallfosca.net	Att: Eva Perisé;  Les rutes de la Val Fosca a Wikiloc vs. el relat del Museu	Hola, Eva, \n\nSegueixo de prop la feina immensa de documentació i difusió que feu des del Museu Hidroelèctric. Sou un referent a tot el Pirineu. \n\nEl motiu del correu és que veig a internet com molts turistes, un cop baixen del Telefèric, acaben guiats per ressenyes desordenades de Google o rutes de Wikiloc que no reflecteixen la precisió ni el relat del vostre arxiu. \n\nA Projecte xino-xano hem desenvolupat la IA Punt d'Or. Bàsicament, li passes un PDF o un tríptic dels que ja teniu publicats a vallfosca.net i, en 15 minuts, et genera una audioguia completa i geolocalitzada, sense que hagis de picar ni una línia de text. Estalvi de temps absolut i, sobretot, el domini i les dades són de l'Ajuntament, no d'una plataforma de tercers. He fet una prova ràpida amb la ruta de l'Antic Carrilet per veure l'efecte que fa.\n\nQuan tens 10 minuts perquè t'ho ensenyi per videotrucada?, un matí de dimarts a dijous?, cap a les 11?\n\nUna abraçada, \nMiquel Utge\n622836542\n\nProjecte xino-xano	OUT	t	t	\N	2026-03-16 11:13:27.40949+00	2026-03-16 10:13:35.508018+00	9bc6e7acd9e041ab8aa6e1c69247cdc0	f	\N	0	\N
fda09688-dba4-426a-8543-b5ece0063d19	2e5361cc-6f1d-460f-9872-eaa1dd6a3e80	c64e9de5-0919-44a5-8e37-5886359b184f	\N	miquel@projectexinoxano.cat	turisme@canillo.ad	Marc, he passat el vostre PDF de senderisme a audioguia interactiva	Hola Marc,\n\nT'escric perquè he estat consultant el portal Visit Canillo i m'ha semblat que la feina de continguts que teniu feta a les guies de senderisme és excel·lent. Tot i això, sé que per al turista actual, descarregar-se un PDF de 5MB i haver de fer zoom amb els dits per llegir sobre el Santuari de Meritxell o la Vall de l'Incles mentre camina, acaba generant una fricció que fa que molta d'aquesta informació es perdi.\n\nHe volgut fer una prova de concepte rigorosa amb el vostre material: he agafat el vostre PDF oficial i l'he processat amb la nostra IA Punt d'Or. En menys de 20 minuts, el sistema ha extret els punts d'interès i ha generat una maqueta d'audioguia geolocalitzada, amb la imatge de Canillo i sense que el visitant hagi de descarregar cap aplicació.\n\nLa meva intenció no és qüestionar la vostra metodologia, sinó ensenyar-te com la tecnologia de Projecte Xino Xano (PXX) pot automatitzar la part més feixuga de la digitalització (el bolcat de dades i la creació d'àudios) perquè us pugueu centrar exclusivament en l'estratègia i el relat de la parròquia.\n\nT'agradaria que et mostrés com ha quedat aquesta prova real de Canillo en un mòbil? Et puc fer una demo de 10 minuts aquesta mateixa setmana, quant et va bé? \nSalut,\nMiquel Utge\n622836542\nProjecte xino-xano	OUT	t	t	\N	2026-03-16 12:14:22.941439+00	2026-03-16 11:14:31.23976+00	f6c4e0a8d7cd4030a2cf216180a8fa51	f	\N	0	\N
7a30be16-5be1-45ce-a7ec-b0c23a5a4001	e4bb29ee-73a3-4cbf-a2cd-9bfb31b0463c	9a77e835-1d42-42e7-b497-2ede3948f73b	\N	miquel@projectexinoxano.cat	info@museudecamins.com	El relat de Llagunes no pot dependre de si el museu està obert	Hola Ariadna,\n\nSegueixo de prop la feina de conservació que feu al jaciment de Santa Creu de Llagunes. Explicar un assentament a 1.600m d'altitud que va de l'Edat de Bronze a la Mitjana és un repte divulgatiu enorme.\n\nT'escric perquè sabem que molts visitants pugen fins al despoblat i, si no coincideixen amb la teva visita guiada, es perden el 90% de la història. Acaben mirant Google Maps, on el relat de Soriguera queda diluït i sense rigor científic.\n\nA PXX hem creat la IA Punt d’Or: una eina que llegeix els teus PDFs i guies actuals i els converteix, en 15 minuts, en una audioguia immersiva per GPS. Sense que tu hagis d'escriure ni una sola paraula de nou.\n\nTinc una mostra de com sona el "teu" museu al mòbil. Et va bé que t'ho ensenyi? Dis-me quant podem quedar.\nUna abraçada,\nMiquel Utge\n622836542\n\nProjecte xino-xano	OUT	t	t	\N	2026-03-16 12:42:18.575513+00	2026-03-16 11:42:26.953753+00	40815ac0315d4c0d971c01b13a89c560	f	\N	0	\N
a561d65a-6bfa-4569-830d-c2a597479634	e4bb29ee-73a3-4cbf-a2cd-9bfb31b0463c	d323117a-11e4-448a-badc-9058b3f4bd32	\N	miquel@projectexinoxano.cat	ajuntament@soriguera.ddl.net	Sobirania digital per als 14 pobles de Soriguera	Hola Josep Ramon,\n\nEnhorabona per la gestió de Soriguera; mantenir un municipi amb 14 nuclis i tanta dispersió és fer política de trinxera real.\n\nT'escric per una preocupació comuna: Actualment, quan un turista busca què fer a Soriguera, és Google qui decideix què veu. Ells es queden les dades i el control, mentre l'ajuntament posa el patrimoni. Silicon Valley s'emporta l'or i vosaltres la feina.\n\nA Pprojecte xino-xano t'oferim infraestructura digital sobirana. No és una "app" més; és una plataforma on l'Ajuntament de Soriguera és l'únic propietari de les dades i del relat.\n\nHe preparat una demo de com apareixeria el vostre patrimoni amb la app de Projecte xino-xano. Quan vols que t'ho ensenyi en 10 minuts?\n\nSalutacions,\nMiquel Utge\n622836542\n\nProjecte xino-xano	OUT	t	t	\N	2026-03-16 12:40:30.110508+00	2026-03-16 11:40:38.482054+00	44a17e53e3874e139967609ed56b45e8	f	\N	0	\N
cdc6eb93-8178-4f84-ac41-e92d4e7463cc	d427d8a7-b977-44dc-ad40-dff00d37da3e	00efd101-915b-48dd-bb00-8e09526d8bf1	\N	miquel@projectexinoxano.cat	turisme@sort.cat	El PDF del Batlliu de Sort convertit en audioguia	Hola Gerard,\n\nFelicitats per la part que et toca del premi de l'alcalde. Sé de sobres que darrere d'aquests reconeixements mediàtics hi ha molta feina invisible des de turisme i Sobirà Dinàmic.\n\nEl problema actual és que l'Ajuntament fa la feina dura de crear les rutes, però és Google qui s'emporta les dades dels turistes quan trepitgen Sort.\n\nPer solucionar això sense carregar-te de més feina, he fet una prova pràctica: he passat el vostre PDF de l'itinerari del Batlliu per la nostra IA Punt d'Or i en només 15 minuts m'ha generat l'audioguia completa i sobirana.\n\nTens 10 minuts aquesta setmana i t'ho ensenyo en viu?\n\nUna abraçada,\n\nMiquel Utge\n622836542\nProjecte Xino Xano	OUT	t	t	\N	2026-03-17 18:40:28.067247+00	2026-03-17 17:40:31.223328+00	7a7bad4d9a604982830bcf182b8805a4	f	\N	0	\N
a704b4f8-6683-4bb4-b944-f877b060704e	d427d8a7-b977-44dc-ad40-dff00d37da3e	1a433539-031d-44ab-82be-baedf1c17811	\N	miquel@projectexinoxano.cat	alcaldia@sort.cat	Premi a la Nit del Dirigent i la sobirania de Sort	\nHola Baldo,\n\nEnhorabona pel reconeixement a la Nit del Dirigent de l'Esport. Aquest lideratge evidencia la gran feina que esteu fent posicionant Sort.\n\nPerò hi ha una fuita important: quan el turista arriba a la Vila Closa, qui li explica el poble? Ara mateix, l'algoritme de Google Maps. Sort inverteix en el patrimoni, i des de Califòrnia s'emporten les dades dels visitants.\n\nHem desenvolupat una infraestructura perquè els ajuntaments recupereu aquesta sobirania digital. He preparat una demo ràpida on pots veure com queda l'escut de Sort controlant el seu propi relat.\n\nTens 10 minuts aquesta setmana i t'ho ensenyo en directe per pantalla?\n\nUna abraçada,\n\nMiquel Utge\n622836542\nProjecte Xino Xano\n	OUT	t	t	\N	2026-03-17 18:38:57.437389+00	2026-03-17 17:39:00.584913+00	61353ce7e62f42c9ac13f47fce4a2b8f	f	\N	0	\N
9ad7856c-65b6-4ded-bbcb-5529179b41c8	e4345303-303f-4387-91e8-fd7643b7e99c	779138ee-9918-494a-94ad-2c2de9adb1e2	\N	miquel@projectexinoxano.cat	eperise@torrecapdella.cat	La ruta de l'Antic Carrilet en audioguia (en 15 minuts)	Hola, Eva,\n\nSegueixo la feina immensa de documentació que feu des del Museu Hidroelèctric. Sou un referent al Pirineu.\n\nVeig que molts turistes que baixen del Telefèric acaben guiats per ressenyes desordenades de Google o Wikiloc que no reflecteixen el rigor del vostre arxiu. La feina la feu vosaltres, però el relat el controlen ells.\n\nA Projecte Xino Xano hem desenvolupat la IA Punt d'Or. Puges un PDF dels que ja teniu a vallfosca.net i et genera una audioguia geolocalitzada en 15 minuts. Sense picar text i amb les dades 100% propietat de l'Ajuntament.\n\nHe fet una prova ràpida amb la ruta de l'Antic Carrilet. Tens 10 minuts dimarts o dimecres al matí i t'ho ensenyo en directe o si prefereixes per video trucada? Soc de Sort puc atançar-me en un moment.\n\nUna abraçada,\n\nMiquel Utge\n622836542\nProjecte Xino Xano	OUT	t	t	\N	2026-03-20 12:56:04.736989+00	2026-03-20 11:56:04.980232+00	6510874960e34e888d60addb29c36388	f	\N	0	\N
892df285-44d5-40aa-8d72-2a8a85af8904	e4345303-303f-4387-91e8-fd7643b7e99c	ed326611-e34c-4e5a-a8ad-3ad9af8bbfd7	\N	miquel@projectexinoxano.cat	rjordana@torrecapdella.cat	El patrimoni de Capdella i el mapa digital del Pallars Jussà	Hola, Ramon,\n\nT'escric per la teva doble visió com a regidor a Capdella i president del Consell Comarcal. Des de les institucions poseu tota la inversió per protegir el patrimoni del territori.\n\nPerò quan el turista arriba a la Vall Fosca, qui li explica la història? L'algoritme de Google Maps o rutes no oficials de Wikiloc. L'esforç és vostre, però Silicon Valley controla el relat i s'emporta les dades.\n\nA Projecte Xino Xano construïm infraestructura digital sobirana des del Pallars. M'agradaria ensenyar-te com Capdella pot tenir la seva audioguia oficial geolocalitzada, i com aquest mateix model pot blindar digitalment tots els municipis del Jussà.\n\nTens 10 minuts dimarts o dimecres al matí i t'ho ensenyo per videotrucada o en persona? Soc de Sort i m´apropo en un moment.\n\nUna abraçada,\n\nMiquel Utge\n622836542\nProjecte Xino Xano	OUT	t	t	\N	2026-03-20 12:59:28.101302+00	2026-03-20 11:59:28.35722+00	22440493ed8544f78ec0975c52081898	f	\N	0	\N
aaab1c5c-a3c6-4aee-ac14-0fbf218f1e2f	e4bb29ee-73a3-4cbf-a2cd-9bfb31b0463c	531b277b-ad47-4d95-96f2-a213e09043f7	\N	miquel@projectexinoxano.cat	ajuntamentdesoriguera@gmail.com	El relat de Soriguera i el patrimoni de Llagunes	Hola Nuria,\n\nHe estat seguint la tasca de gestió que feu a Soriguera amb un territori tan dispers i exigent de mantenir. Amb 14 pobles i actius de la rellevància de Santa Creu de Llagunes, teniu un repte comunicatiu enorme: com explicar la història de la vall quan no hi ha un guia present o el centre d'interpretació està tancat?\n\nSovint, el visitant que arriba a Rubió o a Vilamur acaba consultant fonts digitals genèriques o rutes d'usuaris particulars que no fan justícia a la rigorositat històrica que treballeu des de l'Ajuntament. El relat institucional es perd i la informació queda fragmentada.\n\nA Projecte Xino Xano ajudem els municipis a recuperar el control del seu contingut. Hem creat una infraestructura  que llegeix els vostres fulletons o PDFs oficials i els converteix, en pocs minuts, en audioguies immersives que s'activen per GPS. Això permet que el visitant escolti la vostra veu oficial sense necessitat d'instal·lar cartelleria física ni codis QR que afectin l'entorn natural.\n\nHe preparat una petita demo amb el material de Llagunes perquè veieu com podria sonar el vostre relat oficial en mans dels visitants.\n\nEt truco a final de setmana per veure si podem quadrar la demo.\n\nSalut,\n\nMiquel Utge\n622836542\nProjecte Xino-Xano	OUT	t	t	\N	2026-03-23 10:39:20.387579+00	2026-03-23 09:39:20.770789+00	4314d809f006434791e9100ec69133a9	f	\N	0	\N
baa49ddd-cb57-40ec-a148-7cc3bfea96ce	473f02c9-2b4b-4ad0-acec-751463f60247	94e68e67-cb27-4b4d-a3eb-ba26ec5f8817	\N	miquel@projectexinoxano.cat	ariadnaroca2002@gmail.com	El patrimoni de Isona i la sobirania digital	Hola Ariadna,\n\nEt contacto perquè he vist que gestiones les carteres de Turisme i Transformació Digital, una combinació clau per al futur de municipis amb un patrimoni tan potent com el vostre.\n\nHe estat revisant els actius d'Isona i Conca Dellà, des de la ciutat romana d'Aeso fins a les rutes de la Guerra Civil. Heu fet una feina de conservació magnífica, però quan el visitant arriba al territori, el relat acaba depenent d'algoritmes i plataformes externes que el municipi no controla. L'Ajuntament posa el patrimoni i l'esforç, però la gestió de les dades i de l'experiència queda en mans de tercers.\n\nHem desenvolupat una tecnologia que permet als ajuntaments recuperar aquesta sobirania digital. Podem convertir els vostres PDFs o fulletons en audioguies geolocalitzades en menys de 15 minuts, sense que et tregui temps de la teva agenda ni hagis d'esperar a disposar de més personal tècnic.\n\nT'agradaria veure com quedaria la ruta del Castell de Llordà en aquest format? Dimecres a les 11h o divendres a les 12h et puc ensenyar una prova real en una videotrucada de 10 minuts.\n\nJa em diràs si et va bé.\n\nSalutacions,\n\nMiquel Utge\n622836542\nProjecte Xino Xano	OUT	t	t	\N	2026-03-23 11:00:29.113454+00	2026-03-23 10:00:29.556986+00	bb74c006dc344ad48525d40fd6b6991b	f	\N	0	\N
7293d84f-60fa-4be8-9b97-7a7bb39edcd2	d427d8a7-b977-44dc-ad40-dff00d37da3e	1f4435f6-b943-4f04-b391-1eaf77d872ba	\N	miquel@projectexinoxano.cat	pbascones@sort.cat	Fer visible el valor real de Sort i la Vall d'Àssua	ola Pere,\n\nT'escric perquè des de Projecte Xino Xano estem ajudant els municipis a descentralitzar el turisme. Ens adonem que molts pobles i actius culturals queden amagats, mentre els visitants es concentren només en un parell de punts i es perden el valor real del territori.\n\nHem creat una infraestructura tecnològica sobirana on la nostra IA processa qualsevol dels vostres PDFs turístics (com els de la Ruta del Batlliu) i genera audioguies geolocalitzades en 15 minuts. Així aconseguim guiar el turista cap a aquells pobles que ara passen desapercebuts, retenint-los més temps descobrint la vostra història.\n\nTens 10 minuts dimarts al matí i t'ho ensenyo en directe?\n\nUna abraçada,\n\nMiquel Utge\n622836542\nProjecte xino-xano	OUT	t	t	\N	2026-03-23 12:27:59.650743+00	2026-03-23 11:28:00.36456+00	40c030844bd34e059f723217fff35f7b	f	\N	0	\N
49946ff9-31b7-48fb-9421-8279b95847f9	\N	\N	\N	notifications-noreply@linkedin.com	miquel@projectexinoxano.cat	Siguientes pasos después de añadir una aptitud a tu perfil	<section>\r\n\r\n              <h2 class="heading-large" style="margin: 0; font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', 'Fira Sans', Ubuntu, Oxygen, 'Oxygen Sans', Cantarell, 'Droid Sans', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Lucida Grande', Helvetica, Arial, sans-serif; font-size: 20px; font-weight: 500; line-height: 1.25;">\r\n                Conecta con personas que podrías conocer\r\n              </h2>\r\n                    \r\n        \r\n    <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n      <tbody>\r\n        \r\n          <tr class="w-[400px]" style="width: 400px;">\r\n              <td class="w-1/2 py-1 " style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 50%; padding-top: 8px; padding-bottom: 8px;" width="50%">\r\n                  \r\n      \r\n    \r\n    \r\n    \r\n    \r\n\r\n    \r\n    <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" data-test-id="pymk-entity" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n      <tbody>\r\n        \r\n      <tr>\r\n        <td class="pb-1.5 border-1 border-solid border-system-gray-30 rounded-md\r\n            p-1" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 8px; border-width: 1px; border-style: solid; border-color: #e6e6e6; padding: 8px; padding-bottom: 12px;">\r\n          \r\n    <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n      <tbody>\r\n        \r\n            <tr>\r\n              <td valign="top" align="center" class="h-[170px]" data-test-id="small-view-header" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; height: 170px;" height="170">\r\n                <a href="https://es.linkedin.com/comm/in/solucionsgeografiques?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-pymk_card-0-profile_link&amp;trkEmail=eml-email_skill_add_nba_01-pymk_card-0-profile_link-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;">\r\n                  \r\n    <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n      <tbody>\r\n        \r\n                    <tr>\r\n                      <td align="center" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n                        \r\n    <img class="inline-block relative bg-color-entity-ghost-background clip-path-circle-50 rounded-full w-12 h-12 w-[88px] h-[88px] align-top" src="https://media.licdn.com/dms/image/v2/C5103AQEoz9v0xjJtDA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1516950640817?e=2147483647&amp;v=beta&amp;t=wCjlwNel-zRBOwghc21-eLkjEPGxffGxbd85KSkoV4c" alt="Imagen de perfil de Solucions Geogràfiques" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; position: relative; display: inline-block; height: 88px; width: 88px; border-radius: 9999px; background-color: #eae6df; vertical-align: top; clip-path: circle(50%);" width="88" height="88">\r\n  \r\n                      </td>\r\n                    </tr>\r\n                    <tr>\r\n                      <td align="center" class="pt-0.5" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-top: 4px;">\r\n                        <p class="text-sm leading-regular font-semibold text-system-gray-90" style="margin: 0; font-size: 14px; font-weight: 600; line-height: 1.25; color: #282828;">\r\n                          Solucions Geogràfiques\r\n                        </p>\r\n                      </td>\r\n                    </tr>\r\n                      <tr>\r\n                        <td class="pt-0.5" align="center" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-top: 4px;">\r\n                          <p class="text-sm leading-regular text-system-gray-90" style="margin: 0; font-weight: 400; font-size: 14px; line-height: 1.25; color: #282828;">\r\n                            Solucions GEOINFORMACIÓ I TERRITORI\r\n                          </p>\r\n                        </td>\r\n                      </tr>\r\n                  \r\n      </tbody>\r\n    </table>\r\n  \r\n                </a>\r\n              </td>\r\n            </tr>\r\n\r\n            <tr>\r\n              <td valign="bottom" class="h-[70px]" data-test-id="small-view-bottom" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; height: 70px;" height="70">\r\n                \r\n    <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n      <tbody>\r\n        \r\n                  <tr>\r\n                      <td class="pb-1" align="center" valign="bottom" data-test-id="mutual-connections-small-card" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-bottom: 8px;">\r\n                           \r\n                      </td>\r\n                  </tr>\r\n                  <tr>\r\n                    <td style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n                        \r\n    \r\n    <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="email-button " data-test-id="email-button" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n      <tbody>\r\n        \r\n      <tr>\r\n        <td valign="middle" align="middle" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n          \r\n      <a href="https://www.linkedin.com/mynetwork/send-invite/solucionsgeografiques?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk&amp;trkEmail=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" aria-label="Conectar con Solucions Geogràfiques" class="align-top no-underline " style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; vertical-align: top; text-decoration-line: none;">\r\n        \r\n            \r\n    <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="auto" class="border-separate " style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-collapse: separate;">\r\n      <tbody>\r\n        \r\n              <tr>\r\n                <td class="btn-md\r\n                    btn-secondary-emphasis\r\n                    border-color-brand\r\n                    button-link leading-regular !min-h-[auto] !shadow-none border-1 border-solid" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; height: min-content; border-radius: 24px; padding-top: 12px; padding-bottom: 12px; padding-left: 24px; padding-right: 24px; text-align: center; font-size: 16px; font-weight: 600; cursor: pointer; text-decoration-line: none; background-color: rgba(0, 0, 0, 0); color: #0a66c2; border-width: 1px; border-style: solid; border-color: #0a66c2; line-height: 1.25; min-height: auto !important; box-shadow: 0 0 #0000, 0 0 #0000, 0 0 #0000 !important;">\r\n                  \r\n      <a href="https://www.linkedin.com/mynetwork/send-invite/solucionsgeografiques?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk&amp;trkEmail=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" tabindex="-1" aria-hidden="true" class="no-underline" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; text-decoration-line: none;">\r\n        \r\n                      <span class="no-underline text-color-brand" style="color: #0a66c2; text-decoration-line: none;">\r\n                        Conectar\r\n                      </span>\r\n                                      \r\n      </a>\r\n  \r\n                </td>\r\n              </tr>\r\n            \r\n      </tbody>\r\n    </table>\r\n  \r\n          \r\n      </a>\r\n  \r\n        </td>\r\n      </tr>\r\n    \r\n      </tbody>\r\n    </table>\r\n  \r\n  \r\n                                          </td>\r\n                  </tr>\r\n                \r\n      </tbody>\r\n    </table>\r\n  \r\n              </td>\r\n            </tr>\r\n          \r\n      </tbody>\r\n    </table>\r\n  \r\n        </td>\r\n      </tr>\r\n    \r\n      </tbody>\r\n    </table>\r\n  \r\n  \r\n  \r\n                              </td>\r\n              <td class="w-1/2 py-1 pl-1" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 50%; padding-top: 8px; padding-bottom: 8px; padding-left: 8px;" width="50%">\r\n                  \r\n      \r\n    \r\n    \r\n    \r\n    \r\n\r\n    \r\n    <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" data-test-id="pymk-entity" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n      <tbody>\r\n        \r\n      <tr>\r\n        <td class="pb-1.5 border-1 border-solid border-system-gray-30 rounded-md\r\n            p-1" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 8px; border-width: 1px; border-style: solid; border-color: #e6e6e6; padding: 8px; padding-bottom: 12px;">\r\n          \r\n    <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n      <tbody>\r\n        \r\n            <tr>\r\n              <td valign="top" align="center" class="h-[170px]" data-test-id="small-view-header" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; height: 170px;" height="170">\r\n                <a href="https://es.linkedin.com/comm/in/vicenteluisbenito?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-pymk_card-0-profile_link&amp;trkEmail=eml-email_skill_add_nba_01-pymk_card-0-profile_link-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;">\r\n                  \r\n    <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n      <tbody>\r\n        \r\n                    <tr>\r\n                      <td align="center" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n                        \r\n    <img class="inline-block relative bg-color-entity-ghost-background clip-path-circle-50 rounded-full w-12 h-12 w-[88px] h-[88px] align-top" src="https://media.licdn.com/dms/image/v2/D4D03AQG2ILnHTsVivw/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1669367128833?e=2147483647&amp;v=beta&amp;t=Q4FHO28J5LJnzq7jeZLLGWYy0_KPP5amB4aBa1nX4uw" alt="Imagen de perfil de Vicente L. Benito Molina" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; position: relative; display: inline-block; height: 88px; width: 88px; border-radius: 9999px; background-color: #eae6df; vertical-align: top; clip-path: circle(50%);" width="88" height="88">\r\n  \r\n                      </td>\r\n                    </tr>\r\n                    <tr>\r\n                      <td align="center" class="pt-0.5" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-top: 4px;">\r\n                        <p class="text-sm leading-regular font-semibold text-system-gray-90" style="margin: 0; font-size: 14px; font-weight: 600; line-height: 1.25; color: #282828;">\r\n                          Vicente L. Benito Molina\r\n                        </p>\r\n                      </td>\r\n                    </tr>\r\n                      <tr>\r\n                        <td class="pt-0.5" align="center" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-top: 4px;">\r\n                          <p class="text-sm leading-regular text-system-gray-90" style="margin: 0; font-weight: 400; font-size: 14px; line-height: 1.25; color: #282828;">\r\n                            Consultor especialista en licencias de…\r\n                          </p>\r\n                        </td>\r\n                      </tr>\r\n                  \r\n      </tbody>\r\n    </table>\r\n  \r\n                </a>\r\n              </td>\r\n            </tr>\r\n\r\n            <tr>\r\n              <td valign="bottom" class="h-[70px]" data-test-id="small-view-bottom" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; height: 70px;" height="70">\r\n                \r\n    <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n      <tbody>\r\n        \r\n                  <tr>\r\n                      <td class="pb-1" align="center" valign="bottom" data-test-id="mutual-connections-small-card" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-bottom: 8px;">\r\n                           \r\n                      </td>\r\n                  </tr>\r\n                  <tr>\r\n                    <td style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n                        \r\n    \r\n    <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="email-button " data-test-id="email-button" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n      <tbody>\r\n        \r\n      <tr>\r\n        <td valign="middle" align="middle" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n          \r\n      <a href="https://www.linkedin.com/mynetwork/send-invite/vicenteluisbenito?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk&amp;trkEmail=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" aria-label="Conectar con Vicente L. Benito Molina" class="align-top no-underline " style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; vertical-align: top; text-decoration-line: none;">\r\n        \r\n            \r\n    <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="auto" class="border-separate " style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-collapse: separate;">\r\n      <tbody>\r\n        \r\n              <tr>\r\n                <td class="btn-md\r\n                    btn-secondary-emphasis\r\n                    border-color-brand\r\n                    button-link leading-regular !min-h-[auto] !shadow-none border-1 border-solid" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; height: min-content; border-radius: 24px; padding-top: 12px; padding-bottom: 12px; padding-left: 24px; padding-right: 24px; text-align: center; font-size: 16px; font-weight: 600; cursor: pointer; text-decoration-line: none; background-color: rgba(0, 0, 0, 0); color: #0a66c2; border-width: 1px; border-style: solid; border-color: #0a66c2; line-height: 1.25; min-height: auto !important; box-shadow: 0 0 #0000, 0 0 #0000, 0 0 #0000 !important;">\r\n                  \r\n      <a href="https://www.linkedin.com/mynetwork/send-invite/vicenteluisbenito?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk&amp;trkEmail=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" tabindex="-1" aria-hidden="true" class="no-underline" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; text-decoration-line: none;">\r\n        \r\n                      <span class="no-underline text-color-brand" style="color: #0a66c2; text-decoration-line: none;">\r\n                        Conectar\r\n                      </span>\r\n                                      \r\n      </a>\r\n  \r\n                </td>\r\n              </tr>\r\n            \r\n      </tbody>\r\n    </table>\r\n  \r\n          \r\n      </a>\r\n  \r\n        </td>\r\n      </tr>\r\n    \r\n      </tbody>\r\n    </table>\r\n  \r\n  \r\n                                          </td>\r\n                  </tr>\r\n                \r\n      </tbody>\r\n    </table>\r\n  \r\n              </td>\r\n            </tr>\r\n          \r\n      </tbody>\r\n    </table>\r\n  \r\n        </td>\r\n      </tr>\r\n    \r\n      </tbody>\r\n    </table>\r\n  \r\n  \r\n  \r\n                              </td>\r\n          </tr>   \r\n        \r\n      </tbody>\r\n    </table>\r\n  \r\n          \r\n    \r\n\r\n    <a href="https://www.linkedin.com/comm/search/results/people/?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-pymk-0-null&amp;trkEmail=eml-email_skill_add_nba_01-pymk-0-null-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" class="link-no-visited-state w-[fit-content] mt-1" style="cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-weight: 600; color: #0a66c2; margin-top: 8px; width: fit-content;">\r\n      \r\n    <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;">\r\n      <tbody>\r\n         \r\n        <tr>\r\n          <td class="pr-1" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-right: 8px;"><span class="text-color-text font-bold" style="font-weight: 600; color: rgba(0, 0, 0, 0.9);">Ver más</span></td>\r\n          <td style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"><img class="align-middle" src="https://static.licdn.com/aero-v1/sc/h/6hwnpgjcmcu9mvlpywdqjko83" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; vertical-align: middle;"></td>\r\n        </tr>\r\n      \r\n      </tbody>\r\n    </table>\r\n  \r\n    </a>\r\n  \r\n      </section>\r\n  \r\n\r\n          \r\nDemuestra tu experiencia añadiendo aptitudes relevantes    \r\n\r\n\r\n                Porque añadiste la aptitud Administració pública\r\n                \r\n        \r\n\r\n      \r\n\r\n----------------------------------------\r\n\r\nEste email está dirigido a Miquel Utge (Sobirania Digital per al Territori \r\nSolucions SaaS B2G per a Ajuntaments i Diputacions)\r\nAverigua por qué incluimos esto: https://www.linkedin.com/help/linkedin/answer/4788?lang=es&lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&midToken=AQGmUX0g3NOpOA&midSig=3NkGtUsz57fsc1&trk=eml-email_skill_add_nba_01-SecurityHelp-0-textfooterglimmer&trkEmail=eml-email_skill_add_nba_01-SecurityHelp-0-textfooterglimmer-null-s9x2n0~mn4ffhcr~ll-null-null&eid=s9x2n0-mn4ffhcr-ll\r\nRecibes emails sobre notificaciones de LinkedIn.\r\n\r\nDarse de baja: https://www.linkedin.com/comm/psettings/email-unsubscribe?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&midToken=AQGmUX0g3NOpOA&midSig=3NkGtUsz57fsc1&trk=eml-email_skill_add_nba_01-unsubscribe-0-textfooterglimmer&trkEmail=eml-email_skill_add_nba_01-unsubscribe-0-textfooterglimmer-null-s9x2n0~mn4ffhcr~ll-null-null&eid=s9x2n0-mn4ffhcr-ll&loid=AQFZ71qNMSB9WQAAAZ0fOoSOyQuu041BvPH8vcOT4mGdHcli0aK3ebJLoXsLJtXhkTg2rN1QDnK1jR7qXA1T-SHtl76o8eut3U4vY3DVcKdprlQatF2IIRhKCcWdvSQkZsc\r\nAyuda: https://www.linkedin.com/help/linkedin/answer/67?lang=es&lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&midToken=AQGmUX0g3NOpOA&midSig=3NkGtUsz57fsc1&trk=eml-email_skill_add_nba_01-help-0-textfooterglimmer&trkEmail=eml-email_skill_add_nba_01-help-0-textfooterglimmer-null-s9x2n0~mn4ffhcr~ll-null-null&eid=s9x2n0-mn4ffhcr-ll\r\n\r\n© 2026 LinkedIn Ireland Unlimited Company, Wilton Plaza, Wilton Place, Dublín 2.LinkedIn es un nombre comercial registrado de LinkedIn Ireland Unlimited Company.\r\nLinkedIn y el logotipo de LinkedIn son marcas registradas de LinkedIn.<html xmlns="http://www.w3.org/1999/xhtml" lang="es" xml:lang="es"> <head> <meta http-equiv="Content-Type" content="text/html;charset=utf-8"> <meta name="HandheldFriendly" content="true"> <meta name="viewport" content="width=device-width; initial-scale=0.666667; user-scalable=0"> <meta name="viewport" content="width=device-width"> <title></title> <style>\r\n              @media (max-width: 512px) { .mercado-container { width: 100% !important; } }\r\n            </style> <style>\r\n            @media (max-width: 480px) { .inline-button, .inline-button table { display: none !important; }\r\n            .full-width-button, .full-width-button table { display: table !important; } }\r\n          </style> <style>body {font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue',\r\n            'Fira Sans', Ubuntu, Oxygen, 'Oxygen Sans', Cantarell, 'Droid Sans', 'Apple Color Emoji', 'Segoe UI Emoji',\r\n            'Segoe UI Emoji', 'Segoe UI Symbol', 'Lucida Grande', Helvetica, Arial, sans-serif;}</style> <!--[if mso]><style type="text/css"> </style><![endif]--> <!--[if IE]><style type="text/css"> </style><![endif]--> </head> <body dir="ltr" class="font-sans bg-color-background-canvas w-full m-0 p-0 pt-1" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; margin: 0px; width: 100%; background-color: #f3f2f0; padding: 0px; padding-top: 8px; font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', 'Fira Sans', Ubuntu, Oxygen, 'Oxygen Sans', Cantarell, 'Droid Sans', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Lucida Grande', Helvetica, Arial, sans-serif;"> <div class="h-0 opacity-0 text-transparent invisible overflow-hidden w-0 max-h-[0]" style="visibility: hidden; height: 0px; max-height: 0; width: 0px; overflow: hidden; opacity: 0; mso-hide: all;" data-email-preheader="true">Siguientes pasos en función de la nueva aptitud.</div> <div class="h-0 opacity-0 text-transparent invisible overflow-hidden w-0 max-h-[0]" style="visibility: hidden; height: 0px; max-height: 0; width: 0px; overflow: hidden; opacity: 0; mso-hide: all;"> ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  </div> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="512" align="center" class="mercado-container w-[512px] max-w-[512px] mx-auto my-0 p-0 " style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin-left: auto; margin-right: auto; margin-top: 0px; margin-bottom: 0px; width: 512px; max-width: 512px; padding: 0px;"> <tbody> <tr> <td style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="bg-color-background-container " style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;"> <tbody> <tr> <td class="text-center p-3" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding: 24px; text-align: center;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="min-w-full" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%;"> <tbody> <tr> <td align="left" valign="middle" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <a href="https://www.linkedin.com/comm/feed/?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-header-0-home_glimmer&amp;trkEmail=eml-email_skill_add_nba_01-header-0-home_glimmer-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" class="w-[84px]" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; width: 84px;"> <img alt="LinkedIn" src="https://static.licdn.com/aero-v1/sc/h/9ehe6n39fa07dc5edzv0rla4e" class="h-[21px] w-[84px]" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; height: 21px; width: 84px;" width="84" height="21"> </a> </td> <td valign="middle" align="right" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" data-test-header-profile style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td align="right" valign="middle" class="w-[32px]" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 32px;" width="32"> <a href="https://es.linkedin.com/comm/in/miquel-utge-b906b43b8?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-header-0-profile_glimmer&amp;trkEmail=eml-email_skill_add_nba_01-header-0-profile_glimmer-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;"> <img alt="Miquel Utge" src="https://media.licdn.com/dms/image/v2/D4E03AQEsf5q10C0CoA/profile-displayphoto-scale_200_200/B4EZ0HhEvUHQAg-/0/1773947612042?e=2147483647&amp;v=beta&amp;t=M37ZsROY6hvk60TXYXeQbhdTNn6n5G6pBrkSIZRNVwY" class="rounded-[100%] w-[32px] h-[32px]" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; height: 32px; width: 32px; border-radius: 100%;" width="32" height="32"> </a> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> </tr> <tr> <td class="px-3 pb-3" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-left: 24px; padding-right: 24px; padding-bottom: 24px;"> <div> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <h2 class style="margin: 0; font-weight: 500;">Da estos pasos para abrir la puerta a nuevas oportunidades</h2> </tr> <tr> <td class="pt-2" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-top: 16px;"> <section> <h2 class="heading-large" style="margin: 0; font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', 'Fira Sans', Ubuntu, Oxygen, 'Oxygen Sans', Cantarell, 'Droid Sans', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Lucida Grande', Helvetica, Arial, sans-serif; font-size: 20px; font-weight: 500; line-height: 1.25;"> Conecta con personas que podrías conocer </h2> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr class="w-[400px]" style="width: 400px;"> <td class="w-1/2 py-1 " style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 50%; padding-top: 8px; padding-bottom: 8px;" width="50%"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" data-test-id="pymk-entity" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td class="pb-1.5 border-1 border-solid border-system-gray-30 rounded-md p-1" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 8px; border-width: 1px; border-style: solid; border-color: #e6e6e6; padding: 8px; padding-bottom: 12px;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td valign="top" align="center" class="h-[170px]" data-test-id="small-view-header" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; height: 170px;" height="170"> <a href="https://es.linkedin.com/comm/in/solucionsgeografiques?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-pymk_card-0-profile_link&amp;trkEmail=eml-email_skill_add_nba_01-pymk_card-0-profile_link-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td align="center" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <img class="inline-block relative bg-color-entity-ghost-background clip-path-circle-50 rounded-full w-12 h-12 w-[88px] h-[88px] align-top" src="https://media.licdn.com/dms/image/v2/C5103AQEoz9v0xjJtDA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1516950640817?e=2147483647&amp;v=beta&amp;t=wCjlwNel-zRBOwghc21-eLkjEPGxffGxbd85KSkoV4c" alt="Imagen de perfil de Solucions Geogràfiques" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; position: relative; display: inline-block; height: 88px; width: 88px; border-radius: 9999px; background-color: #eae6df; vertical-align: top; clip-path: circle(50%);" width="88" height="88"> </td> </tr> <tr> <td align="center" class="pt-0.5" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-top: 4px;"> <p class="text-sm leading-regular font-semibold text-system-gray-90" style="margin: 0; font-size: 14px; font-weight: 600; line-height: 1.25; color: #282828;"> Solucions Geogràfiques </p> </td> </tr> <tr> <td class="pt-0.5" align="center" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-top: 4px;"> <p class="text-sm leading-regular text-system-gray-90" style="margin: 0; font-weight: 400; font-size: 14px; line-height: 1.25; color: #282828;"> Solucions GEOINFORMACIÓ I TERRITORI </p> </td> </tr> </tbody> </table> </a> </td> </tr> <tr> <td valign="bottom" class="h-[70px]" data-test-id="small-view-bottom" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; height: 70px;" height="70"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td class="pb-1" align="center" valign="bottom" data-test-id="mutual-connections-small-card" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-bottom: 8px;">   </td> </tr> <tr> <td style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="email-button " data-test-id="email-button" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td valign="middle" align="middle" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <a href="https://www.linkedin.com/mynetwork/send-invite/solucionsgeografiques?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk&amp;trkEmail=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" aria-label="Conectar con Solucions Geogràfiques" class="align-top no-underline " style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; vertical-align: top; text-decoration-line: none;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="auto" class="border-separate " style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-collapse: separate;"> <tbody> <tr> <td class="btn-md btn-secondary-emphasis border-color-brand button-link leading-regular !min-h-[auto] !shadow-none border-1 border-solid" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; height: min-content; border-radius: 24px; padding-top: 12px; padding-bottom: 12px; padding-left: 24px; padding-right: 24px; text-align: center; font-size: 16px; font-weight: 600; cursor: pointer; text-decoration-line: none; background-color: rgba(0, 0, 0, 0); color: #0a66c2; border-width: 1px; border-style: solid; border-color: #0a66c2; line-height: 1.25; min-height: auto !important; box-shadow: 0 0 #0000, 0 0 #0000, 0 0 #0000 !important;"> <a href="https://www.linkedin.com/mynetwork/send-invite/solucionsgeografiques?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk&amp;trkEmail=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" tabindex="-1" aria-hidden="true" class="no-underline" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; text-decoration-line: none;"> <span class="no-underline text-color-brand" style="color: #0a66c2; text-decoration-line: none;"> Conectar </span> </a> </td> </tr> </tbody> </table> </a> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> <td class="w-1/2 py-1 pl-1" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 50%; padding-top: 8px; padding-bottom: 8px; padding-left: 8px;" width="50%"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" data-test-id="pymk-entity" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td class="pb-1.5 border-1 border-solid border-system-gray-30 rounded-md p-1" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-radius: 8px; border-width: 1px; border-style: solid; border-color: #e6e6e6; padding: 8px; padding-bottom: 12px;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td valign="top" align="center" class="h-[170px]" data-test-id="small-view-header" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; height: 170px;" height="170"> <a href="https://es.linkedin.com/comm/in/vicenteluisbenito?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-pymk_card-0-profile_link&amp;trkEmail=eml-email_skill_add_nba_01-pymk_card-0-profile_link-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td align="center" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <img class="inline-block relative bg-color-entity-ghost-background clip-path-circle-50 rounded-full w-12 h-12 w-[88px] h-[88px] align-top" src="https://media.licdn.com/dms/image/v2/D4D03AQG2ILnHTsVivw/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1669367128833?e=2147483647&amp;v=beta&amp;t=Q4FHO28J5LJnzq7jeZLLGWYy0_KPP5amB4aBa1nX4uw" alt="Imagen de perfil de Vicente L. Benito Molina" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; position: relative; display: inline-block; height: 88px; width: 88px; border-radius: 9999px; background-color: #eae6df; vertical-align: top; clip-path: circle(50%);" width="88" height="88"> </td> </tr> <tr> <td align="center" class="pt-0.5" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-top: 4px;"> <p class="text-sm leading-regular font-semibold text-system-gray-90" style="margin: 0; font-size: 14px; font-weight: 600; line-height: 1.25; color: #282828;"> Vicente L. Benito Molina </p> </td> </tr> <tr> <td class="pt-0.5" align="center" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-top: 4px;"> <p class="text-sm leading-regular text-system-gray-90" style="margin: 0; font-weight: 400; font-size: 14px; line-height: 1.25; color: #282828;"> Consultor especialista en licencias de… </p> </td> </tr> </tbody> </table> </a> </td> </tr> <tr> <td valign="bottom" class="h-[70px]" data-test-id="small-view-bottom" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; height: 70px;" height="70"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td class="pb-1" align="center" valign="bottom" data-test-id="mutual-connections-small-card" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-bottom: 8px;">   </td> </tr> <tr> <td style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="email-button " data-test-id="email-button" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td valign="middle" align="middle" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <a href="https://www.linkedin.com/mynetwork/send-invite/vicenteluisbenito?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk&amp;trkEmail=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" aria-label="Conectar con Vicente L. Benito Molina" class="align-top no-underline " style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; vertical-align: top; text-decoration-line: none;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="auto" class="border-separate " style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-collapse: separate;"> <tbody> <tr> <td class="btn-md btn-secondary-emphasis border-color-brand button-link leading-regular !min-h-[auto] !shadow-none border-1 border-solid" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; height: min-content; border-radius: 24px; padding-top: 12px; padding-bottom: 12px; padding-left: 24px; padding-right: 24px; text-align: center; font-size: 16px; font-weight: 600; cursor: pointer; text-decoration-line: none; background-color: rgba(0, 0, 0, 0); color: #0a66c2; border-width: 1px; border-style: solid; border-color: #0a66c2; line-height: 1.25; min-height: auto !important; box-shadow: 0 0 #0000, 0 0 #0000, 0 0 #0000 !important;"> <a href="https://www.linkedin.com/mynetwork/send-invite/vicenteluisbenito?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk&amp;trkEmail=eml-email_skill_add_nba_01-pymk-0-idy_email_pymk-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" tabindex="-1" aria-hidden="true" class="no-underline" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; text-decoration-line: none;"> <span class="no-underline text-color-brand" style="color: #0a66c2; text-decoration-line: none;"> Conectar </span> </a> </td> </tr> </tbody> </table> </a> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> <a href="https://www.linkedin.com/comm/search/results/people/?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-pymk-0-null&amp;trkEmail=eml-email_skill_add_nba_01-pymk-0-null-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" class="link-no-visited-state w-[fit-content] mt-1" style="cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-weight: 600; color: #0a66c2; margin-top: 8px; width: fit-content;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td class="pr-1" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-right: 8px;"><span class="text-color-text font-bold" style="font-weight: 600; color: rgba(0, 0, 0, 0.9);">Ver más</span></td> <td style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"><img class="align-middle" src="https://static.licdn.com/aero-v1/sc/h/6hwnpgjcmcu9mvlpywdqjko83" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; vertical-align: middle;"></td> </tr> </tbody> </table> </a> </section> </td> </tr> <tr> <td class="pt-4" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-top: 32px;"> <section> <h2 class="heading-large" style="margin: 0; font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', 'Fira Sans', Ubuntu, Oxygen, 'Oxygen Sans', Cantarell, 'Droid Sans', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Lucida Grande', Helvetica, Arial, sans-serif; font-size: 20px; font-weight: 500; line-height: 1.25;"> Demuestra tu experiencia añadiendo aptitudes relevantes </h2> <p class="body-small text-color-text-low-emphasis pt-1" style="margin: 0; padding-top: 8px; color: rgba(0, 0, 0, 0.6); font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', 'Fira Sans', Ubuntu, Oxygen, 'Oxygen Sans', Cantarell, 'Droid Sans', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Lucida Grande', Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 1.25;"> Porque añadiste la aptitud Administració pública </p> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td valign="middle" class="font-bold" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 600;">Software de código abierto</td> <td valign="middle" align="right" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <a href="https://www.linkedin.com/comm/in/me/skill-add-edit?skillUrn=urn%3Ali%3Afsd_standardizedSkill%3A3425&amp;lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-profile_prompt-0-null&amp;trkEmail=eml-email_skill_add_nba_01-profile_prompt-0-null-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" class="my-1" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; margin-top: 8px; margin-bottom: 8px;"> <div class="inline-block border-solid border-1 border-system-gray-70 relative rounded-full w-4 h-4" role="button" style="position: relative; display: inline-block; height: 32px; width: 32px; border-radius: 9999px; border-width: 1px; border-style: solid; border-color: #666666;"> <img class="p-1 w-2 h-2" src="https://static.licdn.com/aero-v1/sc/h/a6m61isy235rebhtk2blcd0bl" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; height: 16px; width: 16px; padding: 8px;" width="16" height="16"> </div> </a> </td> </tr> <tr> <td valign="middle" class="font-bold" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 600;">Escalabilidad</td> <td valign="middle" align="right" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <a href="https://www.linkedin.com/comm/in/me/skill-add-edit?skillUrn=urn%3Ali%3Afsd_standardizedSkill%3A1730&amp;lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-profile_prompt-0-null&amp;trkEmail=eml-email_skill_add_nba_01-profile_prompt-0-null-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" class="my-1" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; margin-top: 8px; margin-bottom: 8px;"> <div class="inline-block border-solid border-1 border-system-gray-70 relative rounded-full w-4 h-4" role="button" style="position: relative; display: inline-block; height: 32px; width: 32px; border-radius: 9999px; border-width: 1px; border-style: solid; border-color: #666666;"> <img class="p-1 w-2 h-2" src="https://static.licdn.com/aero-v1/sc/h/a6m61isy235rebhtk2blcd0bl" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; height: 16px; width: 16px; padding: 8px;" width="16" height="16"> </div> </a> </td> </tr> <tr> <td valign="middle" class="font-bold" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 600;">Administración</td> <td valign="middle" align="right" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <a href="https://www.linkedin.com/comm/in/me/skill-add-edit?skillUrn=urn%3Ali%3Afsd_standardizedSkill%3A270&amp;lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-profile_prompt-0-null&amp;trkEmail=eml-email_skill_add_nba_01-profile_prompt-0-null-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" class="my-1" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; margin-top: 8px; margin-bottom: 8px;"> <div class="inline-block border-solid border-1 border-system-gray-70 relative rounded-full w-4 h-4" role="button" style="position: relative; display: inline-block; height: 32px; width: 32px; border-radius: 9999px; border-width: 1px; border-style: solid; border-color: #666666;"> <img class="p-1 w-2 h-2" src="https://static.licdn.com/aero-v1/sc/h/a6m61isy235rebhtk2blcd0bl" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; height: 16px; width: 16px; padding: 8px;" width="16" height="16"> </div> </a> </td> </tr> </tbody> </table> <a href="https://www.linkedin.com/comm/in/me/add-edit/SKILL_AND_ASSOCIATION?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-profile_prompt-0-null&amp;trkEmail=eml-email_skill_add_nba_01-profile_prompt-0-null-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" class="link-no-visited-state w-[fit-content] mt-1" style="cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-weight: 600; color: #0a66c2; margin-top: 8px; width: fit-content;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td class="pr-1" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-right: 8px;"><span class="text-color-text font-bold" style="font-weight: 600; color: rgba(0, 0, 0, 0.9);">Ver más</span></td> <td style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"><img class="align-middle" src="https://static.licdn.com/aero-v1/sc/h/6hwnpgjcmcu9mvlpywdqjko83" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; vertical-align: middle;"></td> </tr> </tbody> </table> </a> </section> </td> </tr> </tbody> </table> </div> </td> </tr> <tr> <td class="bg-color-background-canvas p-3" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f3f2f0; padding: 24px;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="text-xs" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-size: 12px;"> <tbody> <tr> <td class="pb-1 m-0" data-test-id="email-footer__intended" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin: 0px; padding-bottom: 8px;"> Este email está dirigido a Miquel Utge (Sobirania Digital per al Territori Solucions SaaS B2G per a Ajuntaments i Diputacions) </td> </tr> <tr> <td class="pb-1 m-0" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin: 0px; padding-bottom: 8px;"> <a href="https://www.linkedin.com/help/linkedin/answer/4788?lang=es&amp;lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-SecurityHelp-0-footerglimmer&amp;trkEmail=eml-email_skill_add_nba_01-SecurityHelp-0-footerglimmer-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" class="text-inherit underline" style="cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; color: inherit; text-decoration-line: underline;">Consulta por qué informamos sobre esto.</a> </td> </tr> <tr> <td class="pb-1 m-0" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin: 0px; padding-bottom: 8px;">Recibes emails sobre notificaciones de LinkedIn.</td> </tr> <tr> <td class="pb-1 m-0" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin: 0px; padding-bottom: 8px;"> <a href="https://www.linkedin.com/comm/psettings/email-unsubscribe?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-unsubscribe-0-footerGlimmer&amp;trkEmail=eml-email_skill_add_nba_01-unsubscribe-0-footerGlimmer-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll&amp;loid=AQFZ71qNMSB9WQAAAZ0fOoSOyQuu041BvPH8vcOT4mGdHcli0aK3ebJLoXsLJtXhkTg2rN1QDnK1jR7qXA1T-SHtl76o8eut3U4vY3DVcKdprlQatF2IIRhKCcWdvSQkZsc" target="_blank" class="text-inherit underline" style="cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; color: inherit; text-decoration-line: underline;">Darse de baja</a>   ·   <a href="https://www.linkedin.com/help/linkedin/answer/67?lang=es&amp;lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-help-0-footerglimmer&amp;trkEmail=eml-email_skill_add_nba_01-help-0-footerglimmer-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" data-test-help-link class="text-inherit underline" style="cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; color: inherit; text-decoration-line: underline;">Ayuda</a> </td> </tr> <tr> <td class="pb-1" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-bottom: 8px;"> <a href="https://www.linkedin.com/comm/feed/?lipi=urn%3Ali%3Apage%3Aemail_email_skill_add_nba_01%3B1PcfiVRuSgmDkNZ25u5Xvg%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=3NkGtUsz57fsc1&amp;trk=eml-email_skill_add_nba_01-footer-0-logoGlimmer&amp;trkEmail=eml-email_skill_add_nba_01-footer-0-logoGlimmer-null-s9x2n0~mn4ffhcr~ll-null-null&amp;eid=s9x2n0-mn4ffhcr-ll" target="_blank" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;"> <img src="https://static.licdn.com/aero-v1/sc/h/9ehe6n39fa07dc5edzv0rla4e" alt="LinkedIn" class="block h-[14px] w-[56px] image-rendering-crisp" style="outline: none; text-decoration: none; image-rendering: -moz-crisp-edges; image-rendering: -o-crisp-edges; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges; -ms-interpolation-mode: nearest-neighbor; display: block; height: 14px; width: 56px;" width="56" height="14"> </a> </td> </tr> <tr> <td data-test-copyright-text style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> © 2026 LinkedIn Ireland Unlimited Company, Wilton Plaza, Wilton Place, Dublín 2. LinkedIn es un nombre comercial registrado de LinkedIn Ireland Unlimited Company. <span data-test-trademarks-text> LinkedIn y el logotipo de LinkedIn son marcas registradas de LinkedIn. </span> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> <img alt role="presentation" src="https://www.linkedin.com/emimp/ip_Y3psNE1tNHdMVzF1TkdabWFHTnlMV3hzOlpXMWhhV3hmYzJ0cGJHeGZZV1JrWDI1aVlWOHdNUT09Og==.gif" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; width: 1px; height: 1px;" width="1" height="1"> </body> </html>	IN	f	t	<306655367.53066858.1774345423008@lor1-app161585.prod.linkedin.com>	2026-03-24 09:43:43+00	2026-03-24 09:44:18.133907+00	\N	f	\N	0	\N
3660a6c0-0b9b-4182-a13a-130a7bad0a94	484e3468-2ed3-4211-8307-15c7b12af329	bca93a14-db52-48b2-b801-041730f1edff	\N	miquel@projectexinoxano.cat	regidoriacultura@elpontdesuert.cat	Sobre el relat digital del patrimoni del Pont de Suert	Bon dia Josep,\n\nT’escric perquè he estat seguint de prop la feina que feu des de l’àrea de Turisme, especialment amb la preservació del patrimoni de les Falles i l'impuls de les rutes del Romànic a Viu i Irgo. És evident que El Pont de Suert té un relat cultural de primer nivell que cuideu amb molta cura.\n\nL’únic motiu del meu correu és proposar-te una reflexió sobre com arriba avui aquest relat al visitant que camina pel municipi. Sovint, l'Ajuntament fa tota la inversió i la feina de camp, però la "veu" que guia el turista acaba depenent de plataformes externes que no controleu i que es queden amb tota la informació de l'usuari.\n\nLa nostra proposta se centra a retornar-vos el control: que El Pont de Suert tingui una infraestructura digital pròpia. Una eina que us permeti donar veu oficial al vostre patrimoni i, sobretot, que les dades de qui us visita tornin a ser propietat de l’Ajuntament.\n\nTens 10 minuts aquest divendres al matí o dilluns de la setmana entrant i t'ho explico de tu a tu?\n\nSalutacions,\n\nMiquel Utge\n622836542\nProjecte Xino Xano	OUT	t	t	\N	2026-03-23 12:31:50.446913+00	2026-03-23 11:31:51.174507+00	18a6b35938d548b5b613f91506479230	f	\N	0	\N
e133ce60-3dfc-42a7-9f1a-dd2e662a3015	\N	\N	\N	notifications-noreply@linkedin.com	miquel@projectexinoxano.cat	Miquel, tus publicaciones obtuvieron 7 impresiones la semana pasada.	https://www.linkedin.com/comm/feed/?lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&midToken=AQGmUX0g3NOpOA&midSig=0rhKs64i3Wfsc1&trk=eml-email_weekly_analytics_recap_v2-main~module~text-0-visit~linkedin~text&trkEmail=eml-email_weekly_analytics_recap_v2-main~module~text-0-visit~linkedin~text-null-s9x2n0~mn4lnshm~7x-null-null&eid=s9x2n0-mn4lnshm-7x\r\nEtiqueta:https://www.linkedin.com/e/v2?urlhash=TbW-&url=https%3A%2F%2Flinkedinmobileapp%2Ecom&lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&midToken=AQGmUX0g3NOpOA&midSig=0rhKs64i3Wfsc1&ek=email_weekly_analytics_recap_v2&e=s9x2n0-mn4lnshm-7x&eid=s9x2n0-mn4lnshm-7x&m=main-module-text&ts=visit-linkedin-text&li=0&t=plh  \r\n      \r\n\r\n----------------------------------------\r\n\r\nEste email está dirigido a Miquel Utge (Sobirania Digital per al Territori \r\nSolucions SaaS B2G per a Ajuntaments i Diputacions)\r\nAverigua por qué incluimos esto: https://www.linkedin.com/help/linkedin/answer/4788?lang=es&lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&midToken=AQGmUX0g3NOpOA&midSig=0rhKs64i3Wfsc1&trk=eml-email_weekly_analytics_recap_v2-SecurityHelp-0-textfooterglimmer&trkEmail=eml-email_weekly_analytics_recap_v2-SecurityHelp-0-textfooterglimmer-null-s9x2n0~mn4lnshm~7x-null-null&eid=s9x2n0-mn4lnshm-7x\r\nRecibes emails sobre notificaciones de LinkedIn.\r\n\r\n\r\nDarse de baja: https://www.linkedin.com/comm/psettings/email-unsubscribe?lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&midToken=AQGmUX0g3NOpOA&midSig=0rhKs64i3Wfsc1&trk=eml-email_weekly_analytics_recap_v2-unsubscribe-0-textfooterglimmer&trkEmail=eml-email_weekly_analytics_recap_v2-unsubscribe-0-textfooterglimmer-null-s9x2n0~mn4lnshm~7x-null-null&eid=s9x2n0-mn4lnshm-7x&loid=AQEfMwEet-_wWgAAAZ0f3fOly3FaJIQO8iOMdZaEMG25Ym-TjehVhsSED9M5xj3BUHM3Vjp9TZPT_SWzN495f3bhrKAdUU0HadXsd3GYSF1dAAdjYYgZ62-vgSAXZQ\r\nAyuda: https://www.linkedin.com/help/linkedin/answer/67?lang=es&lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&midToken=AQGmUX0g3NOpOA&midSig=0rhKs64i3Wfsc1&trk=eml-email_weekly_analytics_recap_v2-help-0-textfooterglimmer&trkEmail=eml-email_weekly_analytics_recap_v2-help-0-textfooterglimmer-null-s9x2n0~mn4lnshm~7x-null-null&eid=s9x2n0-mn4lnshm-7x\r\n\r\n© 2026 LinkedIn Ireland Unlimited Company, Wilton Plaza, Wilton Place, Dublín 2.LinkedIn es un nombre comercial registrado de LinkedIn Ireland Unlimited Company.\r\nLinkedIn y el logotipo de LinkedIn son marcas registradas de LinkedIn.<html xmlns="http://www.w3.org/1999/xhtml" lang="es" xml:lang="es"> <head> <meta http-equiv="Content-Type" content="text/html;charset=utf-8"> <meta name="HandheldFriendly" content="true"> <meta name="viewport" content="width=device-width; initial-scale=0.666667; user-scalable=0"> <meta name="viewport" content="width=device-width"> <title></title> <style>\r\n              @media (max-width: 512px) { .mercado-container { width: 100% !important; } }\r\n            </style> <style>\r\n            @media (max-width: 480px) { .inline-button, .inline-button table { display: none !important; }\r\n            .full-width-button, .full-width-button table { display: table !important; } }\r\n          </style> <style>body {font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue',\r\n            'Fira Sans', Ubuntu, Oxygen, 'Oxygen Sans', Cantarell, 'Droid Sans', 'Apple Color Emoji', 'Segoe UI Emoji',\r\n            'Segoe UI Emoji', 'Segoe UI Symbol', 'Lucida Grande', Helvetica, Arial, sans-serif;}</style> <!--[if mso]><style type="text/css"> </style><![endif]--> <!--[if IE]><style type="text/css"> </style><![endif]--> </head> <body dir="ltr" class="font-sans bg-color-background-canvas w-full m-0 p-0 pt-1" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; margin: 0px; width: 100%; background-color: #f3f2f0; padding: 0px; padding-top: 8px; font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', 'Fira Sans', Ubuntu, Oxygen, 'Oxygen Sans', Cantarell, 'Droid Sans', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Lucida Grande', Helvetica, Arial, sans-serif;"> <div class="h-0 opacity-0 text-transparent invisible overflow-hidden w-0 max-h-[0]" style="visibility: hidden; height: 0px; max-height: 0; width: 0px; overflow: hidden; opacity: 0; mso-hide: all;" data-email-preheader="true">Rendimiento semanal y consejos para ampliar tu alcance</div> <div class="h-0 opacity-0 text-transparent invisible overflow-hidden w-0 max-h-[0]" style="visibility: hidden; height: 0px; max-height: 0; width: 0px; overflow: hidden; opacity: 0; mso-hide: all;"> ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏  </div> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="512" align="center" class="mercado-container w-[512px] max-w-[512px] mx-auto my-0 p-0 " style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin-left: auto; margin-right: auto; margin-top: 0px; margin-bottom: 0px; width: 512px; max-width: 512px; padding: 0px;"> <tbody> <tr> <td style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="bg-color-background-container " style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;"> <tbody> <tr> <td class="text-center p-3" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding: 24px; text-align: center;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="min-w-full" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%;"> <tbody> <tr> <td align="left" valign="middle" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <a href="https://www.linkedin.com/comm/feed/?lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=0rhKs64i3Wfsc1&amp;trk=eml-email_weekly_analytics_recap_v2-header-0-home_glimmer&amp;trkEmail=eml-email_weekly_analytics_recap_v2-header-0-home_glimmer-null-s9x2n0~mn4lnshm~7x-null-null&amp;eid=s9x2n0-mn4lnshm-7x" target="_blank" class="w-[84px]" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; width: 84px;"> <img alt="LinkedIn" src="https://static.licdn.com/aero-v1/sc/h/9ehe6n39fa07dc5edzv0rla4e" class="h-[21px] w-[84px]" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; height: 21px; width: 84px;" width="84" height="21"> </a> </td> <td valign="middle" align="right" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" data-test-header-profile style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td align="right" valign="middle" class="w-[32px]" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 32px;" width="32"> <a href="https://es.linkedin.com/comm/in/miquel-utge-b906b43b8?lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=0rhKs64i3Wfsc1&amp;trk=eml-email_weekly_analytics_recap_v2-header-0-profile_glimmer&amp;trkEmail=eml-email_weekly_analytics_recap_v2-header-0-profile_glimmer-null-s9x2n0~mn4lnshm~7x-null-null&amp;eid=s9x2n0-mn4lnshm-7x" target="_blank" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;"> <img alt="Miquel Utge" src="https://media.licdn.com/dms/image/v2/D4E03AQEsf5q10C0CoA/profile-displayphoto-scale_200_200/B4EZ0HhEvUHQAg-/0/1773947612042?e=2147483647&amp;v=beta&amp;t=M37ZsROY6hvk60TXYXeQbhdTNn6n5G6pBrkSIZRNVwY" class="rounded-[100%] w-[32px] h-[32px]" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; height: 32px; width: 32px; border-radius: 100%;" width="32" height="32"> </a> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> </tr> <tr> <td class="email-weekly-analytics-recap-v2__body pb-3" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-bottom: 24px; padding: 0 12px !important;"> <div> <div> <div class="bg-color-background-container rounded-sm p-1.5 pb-3" style="border-radius: 4px; background-color: #ffffff; padding: 12px; padding-bottom: 24px;"> <h2 class="text-xl leading-regular font-bold text-system-gray-90 mb-1.5" style="margin: 0; margin-bottom: 12px; font-size: 24px; font-weight: 600; line-height: 1.25; color: #282828;"> Miquel, tus publicaciones han dejado huella en tu público </h2> <p class="text-sm mb-3" style="margin: 0; font-weight: 400; margin-bottom: 24px; font-size: 14px;"> Aquí tienes un resumen de cómo ha rendido tu contenido la semana del <b>03/16 – 03/22</b>. </p> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="mb-1.5" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin-bottom: 12px;"> <tbody> <tr> <td class="pb-1.5" colspan="2" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-bottom: 12px;"> <div class="rounded-sm bg-system-gray-10 py-2 px-1.5" style="border-radius: 4px; background-color: #f7f7f7; padding-left: 12px; padding-right: 12px; padding-top: 16px; padding-bottom: 16px; border-top: 3px solid #01754f; height: 100%;"> <a href="https://www.linkedin.com/comm/analytics/creator/content?startDate=2026-03-16&amp;endDate=2026-03-22&amp;metricType=IMPRESSIONS&amp;timeRange=custom&amp;lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=0rhKs64i3Wfsc1&amp;trk=eml-email_weekly_analytics_recap_v2-milestone~module-0-view~impressions~from~metric~link~impressions&amp;trkEmail=eml-email_weekly_analytics_recap_v2-milestone~module-0-view~impressions~from~metric~link~impressions-null-s9x2n0~mn4lnshm~7x-null-null&amp;eid=s9x2n0-mn4lnshm-7x" target="_blank" style="cursor: pointer; display: inline-block; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; text-decoration: none; color: inherit;"> <p class="font-bold text-lg" style="margin: 0; font-size: 20px; font-weight: 600;">7</p> <p class="text-sm" style="margin: 0; font-weight: 400; font-size: 14px;">Impresiones</p> </a> </div> </td> </tr> <tr> <td class="pr-1.5" width="50%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-right: 12px; vertical-align: top;"> </td> <td width="50%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; vertical-align: top;"> </td> </tr> </tbody> </table> <div> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="email-button " data-test-id="email-button" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td valign="middle" align="left" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <a href="https://www.linkedin.com/comm/analytics/creator/content?startDate=2026-03-16&amp;endDate=2026-03-22&amp;metricType=IMPRESSIONS&amp;timeRange=custom&amp;lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=0rhKs64i3Wfsc1&amp;trk=eml-email_weekly_analytics_recap_v2-milestone~module-0-view~impressions~from~primary~cta&amp;trkEmail=eml-email_weekly_analytics_recap_v2-milestone~module-0-view~impressions~from~primary~cta-null-s9x2n0~mn4lnshm~7x-null-null&amp;eid=s9x2n0-mn4lnshm-7x" target="_blank" aria-label="Ver todos los análisis" class="align-top no-underline " style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; vertical-align: top; text-decoration-line: none;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="auto" class="border-separate " style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-collapse: separate;"> <tbody> <tr> <td class="btn-md btn-primary border-color-brand button-link leading-regular !min-h-[auto] !shadow-none border-1 border-solid" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; height: min-content; border-radius: 24px; padding-top: 12px; padding-bottom: 12px; padding-left: 24px; padding-right: 24px; text-align: center; font-size: 16px; font-weight: 600; cursor: pointer; text-decoration-line: none; background-color: #0a66c2; color: #ffffff; border-width: 1px; border-style: solid; border-color: #0a66c2; line-height: 1.25; min-height: auto !important; box-shadow: 0 0 #0000, 0 0 #0000, 0 0 #0000 !important;"> <a href="https://www.linkedin.com/comm/analytics/creator/content?startDate=2026-03-16&amp;endDate=2026-03-22&amp;metricType=IMPRESSIONS&amp;timeRange=custom&amp;lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=0rhKs64i3Wfsc1&amp;trk=eml-email_weekly_analytics_recap_v2-milestone~module-0-view~impressions~from~primary~cta&amp;trkEmail=eml-email_weekly_analytics_recap_v2-milestone~module-0-view~impressions~from~primary~cta-null-s9x2n0~mn4lnshm~7x-null-null&amp;eid=s9x2n0-mn4lnshm-7x" target="_blank" tabindex="-1" aria-hidden="true" class="no-underline" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; text-decoration-line: none;"> <span class="no-underline text-white" style="color: #ffffff; text-decoration-line: none;"> Ver todos los análisis </span> </a> </td> </tr> </tbody> </table> </a> </td> </tr> </tbody> </table> </div> </div> <div class="bg-color-background-container rounded-sm p-1.5 pb-3" style="border-radius: 4px; background-color: #ffffff; padding: 12px; padding-bottom: 24px;"> <h2 class="text-lg leading-regular font-bold mb-2" style="margin: 0; margin-bottom: 16px; font-size: 20px; font-weight: 600; line-height: 1.25;"> Esto es lo que puedes hacer para ampliar tu alcance: </h2> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="mb-1.5" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin-bottom: 12px;"> <tbody> <tr> <td class="pr-1.5" width="50%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-right: 12px; vertical-align: top;"> <div class="bg-system-gray-10 rounded-sm align-middle text-center p-1.5" style="border-radius: 4px; background-color: #f7f7f7; padding: 12px; text-align: center; vertical-align: middle;"> <img src="https://static.licdn.com/aero-v1/sc/h/ed3zpojsetuc3rng8rkl11bw5" height="48" width="48" alt="Icono de calendario" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic;"> </div> </td> <td width="50%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; vertical-align: top;"> <p class="text-sm text-color-text" style="margin: 0; font-weight: 400; font-size: 14px; color: rgba(0, 0, 0, 0.9);">Si publicas contenido al menos una vez a la semana, podrías multiplicar hasta <b>por cuatro</b> las visualizaciones de tu perfil y <b>duplicar</b> tus seguidores.</p> </td> </tr> </tbody> </table> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="mb-1.5" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin-bottom: 12px;"> <tbody> <tr> <td class="pr-1.5" width="50%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-right: 12px; vertical-align: top;"> <div class="bg-system-gray-10 rounded-sm align-middle text-center p-1.5" style="border-radius: 4px; background-color: #f7f7f7; padding: 12px; text-align: center; vertical-align: middle;"> <img src="https://static.licdn.com/aero-v1/sc/h/1an8e4544xtu5woyuukx0mx2k" height="48" width="48" alt="Icono de mensajes" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic;"> </div> </td> <td width="50%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; vertical-align: top;"> <p class="text-sm text-color-text" style="margin: 0; font-weight: 400; font-size: 14px; color: rgba(0, 0, 0, 0.9);">Si comentas en publicaciones al menos una vez a la semana, podrías <b>triplicar</b> las visualizaciones de tu perfil.</p> </td> </tr> </tbody> </table> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="mb-1.5" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin-bottom: 12px;"> <tbody> <tr> <td class="pr-1.5" width="50%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-right: 12px; vertical-align: top;"> <div class="bg-system-gray-10 rounded-sm align-middle text-center p-1.5" style="border-radius: 4px; background-color: #f7f7f7; padding: 12px; text-align: center; vertical-align: middle;"> <img src="https://static.licdn.com/aero-v1/sc/h/a3zzk04o5x961mc3101webqt" height="48" width="48" alt="Icono de imagen" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic;"> </div> </td> <td width="50%" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; vertical-align: top;"> <p class="text-sm text-color-text" style="margin: 0; font-weight: 400; font-size: 14px; color: rgba(0, 0, 0, 0.9);">Añadir una imagen a tu publicación puede aumentar las reacciones, los comentarios y las veces que comparte hasta en un <b>40 %</b>.</p> </td> </tr> </tbody> </table> <div class="mt-3" style="margin-top: 24px;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="email-button " data-test-id="email-button" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tbody> <tr> <td valign="middle" align="left" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <a href="https://www.linkedin.com/comm/dashboard/share?lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=0rhKs64i3Wfsc1&amp;trk=eml-email_weekly_analytics_recap_v2-tips~module-0-open~sharebox&amp;trkEmail=eml-email_weekly_analytics_recap_v2-tips~module-0-open~sharebox-null-s9x2n0~mn4lnshm~7x-null-null&amp;eid=s9x2n0-mn4lnshm-7x" target="_blank" aria-label="Comienza tu siguiente publicación" class="align-top no-underline " style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; vertical-align: top; text-decoration-line: none;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="auto" class="border-separate " style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-collapse: separate;"> <tbody> <tr> <td class="btn-sm btn-secondary-emphasis border-color-brand button-link leading-regular !min-h-[auto] !shadow-none border-1 border-solid" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; height: min-content; border-radius: 24px; padding-top: 7px; padding-bottom: 7px; padding-left: 16px; padding-right: 16px; text-align: center; font-size: 14px; font-weight: 600; cursor: pointer; text-decoration-line: none; background-color: rgba(0, 0, 0, 0); color: #0a66c2; border-width: 1px; border-style: solid; border-color: #0a66c2; line-height: 1.25; min-height: auto !important; box-shadow: 0 0 #0000, 0 0 #0000, 0 0 #0000 !important;"> <a href="https://www.linkedin.com/comm/dashboard/share?lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=0rhKs64i3Wfsc1&amp;trk=eml-email_weekly_analytics_recap_v2-tips~module-0-open~sharebox&amp;trkEmail=eml-email_weekly_analytics_recap_v2-tips~module-0-open~sharebox-null-s9x2n0~mn4lnshm~7x-null-null&amp;eid=s9x2n0-mn4lnshm-7x" target="_blank" tabindex="-1" aria-hidden="true" class="no-underline" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; text-decoration-line: none;"> <span class="no-underline text-color-brand" style="color: #0a66c2; text-decoration-line: none;"> Comienza tu siguiente publicación </span> </a> </td> </tr> </tbody> </table> </a> </td> </tr> </tbody> </table> </div> </div> </div> </div> </td> </tr> <tr> <td class="bg-color-background-canvas p-3" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f3f2f0; padding: 24px;"> <table role="presentation" valign="top" border="0" cellspacing="0" cellpadding="0" width="100%" class="text-xs" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-size: 12px;"> <tbody> <tr> <td class="pb-1 m-0" data-test-id="email-footer__intended" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin: 0px; padding-bottom: 8px;"> Este email está dirigido a Miquel Utge (Sobirania Digital per al Territori Solucions SaaS B2G per a Ajuntaments i Diputacions) </td> </tr> <tr> <td class="pb-1 m-0" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin: 0px; padding-bottom: 8px;"> <a href="https://www.linkedin.com/help/linkedin/answer/4788?lang=es&amp;lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=0rhKs64i3Wfsc1&amp;trk=eml-email_weekly_analytics_recap_v2-SecurityHelp-0-footerglimmer&amp;trkEmail=eml-email_weekly_analytics_recap_v2-SecurityHelp-0-footerglimmer-null-s9x2n0~mn4lnshm~7x-null-null&amp;eid=s9x2n0-mn4lnshm-7x" target="_blank" class="text-inherit underline" style="cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; color: inherit; text-decoration-line: underline;">Consulta por qué informamos sobre esto.</a> </td> </tr> <tr> <td class="pb-1 m-0" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin: 0px; padding-bottom: 8px;">Recibes emails sobre notificaciones de LinkedIn.</td> </tr> <tr> <td class="pb-1 m-0" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; margin: 0px; padding-bottom: 8px;"> <a href="https://www.linkedin.com/comm/psettings/email-unsubscribe?lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=0rhKs64i3Wfsc1&amp;trk=eml-email_weekly_analytics_recap_v2-unsubscribe-0-footerGlimmer&amp;trkEmail=eml-email_weekly_analytics_recap_v2-unsubscribe-0-footerGlimmer-null-s9x2n0~mn4lnshm~7x-null-null&amp;eid=s9x2n0-mn4lnshm-7x&amp;loid=AQEfMwEet-_wWgAAAZ0f3fOly3FaJIQO8iOMdZaEMG25Ym-TjehVhsSED9M5xj3BUHM3Vjp9TZPT_SWzN495f3bhrKAdUU0HadXsd3GYSF1dAAdjYYgZ62-vgSAXZQ" target="_blank" class="text-inherit underline" style="cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; color: inherit; text-decoration-line: underline;">Darse de baja</a>   ·   <a href="https://www.linkedin.com/help/linkedin/answer/67?lang=es&amp;lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=0rhKs64i3Wfsc1&amp;trk=eml-email_weekly_analytics_recap_v2-help-0-footerglimmer&amp;trkEmail=eml-email_weekly_analytics_recap_v2-help-0-footerglimmer-null-s9x2n0~mn4lnshm~7x-null-null&amp;eid=s9x2n0-mn4lnshm-7x" target="_blank" data-test-help-link class="text-inherit underline" style="cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; color: inherit; text-decoration-line: underline;">Ayuda</a> </td> </tr> <tr> <td class="pb-1" style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt; padding-bottom: 8px;"> <a href="https://www.linkedin.com/comm/feed/?lipi=urn%3Ali%3Apage%3Aemail_email_weekly_analytics_recap_v2%3BZATsLGPHQ4m6UK9C%2B9KsuA%3D%3D&amp;midToken=AQGmUX0g3NOpOA&amp;midSig=0rhKs64i3Wfsc1&amp;trk=eml-email_weekly_analytics_recap_v2-footer-0-logoGlimmer&amp;trkEmail=eml-email_weekly_analytics_recap_v2-footer-0-logoGlimmer-null-s9x2n0~mn4lnshm~7x-null-null&amp;eid=s9x2n0-mn4lnshm-7x" target="_blank" style="color: #0a66c2; cursor: pointer; display: inline-block; text-decoration: none; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;"> <img src="https://static.licdn.com/aero-v1/sc/h/9ehe6n39fa07dc5edzv0rla4e" alt="LinkedIn" class="block h-[14px] w-[56px] image-rendering-crisp" style="outline: none; text-decoration: none; image-rendering: -moz-crisp-edges; image-rendering: -o-crisp-edges; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges; -ms-interpolation-mode: nearest-neighbor; display: block; height: 14px; width: 56px;" width="56" height="14"> </a> </td> </tr> <tr> <td data-test-copyright-text style="-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> © 2026 LinkedIn Ireland Unlimited Company, Wilton Plaza, Wilton Place, Dublín 2. LinkedIn es un nombre comercial registrado de LinkedIn Ireland Unlimited Company. <span data-test-trademarks-text> LinkedIn y el logotipo de LinkedIn son marcas registradas de LinkedIn. </span> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> <img alt role="presentation" src="https://www.linkedin.com/emimp/ip_Y3psNE1tNHdMVzF1Tkd4dWMyaHRMVGQ0OlpXMWhhV3hmZDJWbGEyeDVYMkZ1WVd4NWRHbGpjMTl5WldOaGNGOTJNZz09Og==.gif" style="outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; width: 1px; height: 1px;" width="1" height="1"> </body> </html>	IN	f	t	<88832595.53990730.1774356133154@lor1-app122575.prod.linkedin.com>	2026-03-24 12:42:13+00	2026-03-24 12:46:27.180521+00	\N	f	\N	0	\N
\.


--
-- Data for Name: emails_v2; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.emails_v2 (id, municipi_id, data_enviament, assumpte, cos, obert, data_obertura, cops_obert, respost, data_resposta, sentiment_resposta, intents_detectats, actor_probable) FROM stdin;
\.


--
-- Data for Name: llicencies; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.llicencies (id, deal_id, data_inici, data_renovacio, estat, notes, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: memoria_municipis; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.memoria_municipis (municipi_id, ganxos_exitosos, angles_fallits, moment_optimal, llenguatge_preferit, blockers_resolts, data_actualitzacio) FROM stdin;
\.


--
-- Data for Name: municipis; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.municipis (id, nom, tipus, provincia, poblacio, web, telefon, adreca, notes, created_at, updated_at, codi_postal) FROM stdin;
d47fde40-f1d9-4255-8ad2-9813c5fd8f25	 Torrede de Capdella	ajuntament	Lleida	Torre de Capdella	htpps://www.torredecapdela.org	973663001	\N	\N	2026-03-16 09:38:34.268009+00	2026-03-16 10:40:45.889341+00	\N
78a2343f-dbf5-4707-9e44-5622d03fb5cb	Ajuntament Sort	ajuntament	Lleida	Sort	https://sort.cat/	973620010	Carrer del Dr. Carles Pol i Aleu, 13, 25560 Sort	\N	2026-03-12 10:59:08.042304+00	2026-03-16 10:42:10.811+00	\N
b0988c73-01e8-4354-94aa-e4c3795511dc	Pobla de Segur	ajuntament	Lleida	Pobla de Segur	https://www.lapobladesegur.cat/ca/	 973 680 038	Av. Verdaguer, 35\n25500 La Pobla de Segur	\N	2026-03-10 18:53:52.24095+00	2026-03-16 10:42:35.166655+00	\N
76993a09-1cc4-4288-ae93-c2aed91f5278	Canillo	ajuntament	Lleida	Canillo	https://www.canillo.ad	(+376) 751 036	Pl. Carlemany núm.4,\nEdifici Telecabina .\nAD100 Canillo,\nPRINCIPAT D’ANDORRA	\N	2026-03-16 10:50:38.296184+00	2026-03-16 10:50:38.296184+00	\N
388104f6-3294-4fa6-9fc0-ebca33eec086	Soriguera	ajuntament	Lleida	Soriguera	https://soriguera.ddl.net	973 62 06 09	Plaça Mare de Déu de Medina - 25566 Vilamur | 25566	\N	2026-03-16 11:31:03.581316+00	2026-03-16 11:31:03.581316+00	\N
f3f01788-d8e9-409f-aaf5-c84a5be26fbf	Esterri d´Aneu	ajuntament	Lleida	Esterri d´Aneu	https://www.esterrianeu.cat/	973 626 005	Plaça de la Closa, 1\n25580 Esterri d’Àneu\nPallars Sobirà	\N	2026-03-16 12:18:23.826299+00	2026-03-16 12:18:23.826299+00	\N
117d35c3-b4c5-406d-a8d4-8cb58393bf52	Isona	ajuntament	Lleida	Isona i conca dellà	https://www.isonaiconcadella.cat/	973 664 008	\N	\N	2026-03-19 17:19:42.751755+00	2026-03-19 17:19:42.751755+00	\N
af9ca22a-4e96-47e8-b284-1d1fba3f97fa	Consorsi de Turisme de les Valls d´Aneu	ajuntament	Lleida	Espot	\N	\N	\N	\N	2026-03-19 17:42:32.133326+00	2026-03-19 17:42:32.133326+00	\N
322a61f2-bddc-45ee-ae31-d79f279cdedf	El Pont de Suert	ajuntament	Lleida	Pont de Suert	https://www.elpontdesuert.cat/	973 690 005	\N	\N	2026-03-19 18:00:14.31416+00	2026-03-19 18:00:14.31416+00	\N
5cfe1986-555e-4e28-bc9e-ac500ac0cd4b	El Pont de Suert	ajuntament	Lleida	El Pont de Suert	https://www.elpontdesuert.cat/	 973 690 005	\N	\N	2026-03-23 10:42:30.747236+00	2026-03-23 10:42:30.747236+00	\N
\.


--
-- Data for Name: municipis_lifecycle; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.municipis_lifecycle (id, nom, comarca, poblacio, geografia, diagnostic_digital, angle_personalitzacio, etapa_actual, historial_etapes, blocker_actual, temperatura, dies_etapa_actual, data_conversio, pla_contractat, estat_final, actor_principal_id, data_creacio, data_ultima_accio, usuari_asignat) FROM stdin;
76993a09-1cc4-4288-ae93-c2aed91f5278	Canillo	\N	\N	interior	{"web": "https://www.canillo.ad", "adreca": "Pl. Carlemany núm.4,\\nEdifici Telecabina .\\nAD100 Canillo,\\nPRINCIPAT D’ANDORRA", "notes_v1": null, "telefon_general": "(+376) 751 036"}	Mantenir calor comercial.	research	[]	cap	templat	0	\N	\N	\N	c64e9de5-0919-44a5-8e37-5886359b184f	2026-03-16 10:50:38.296184+00	2026-03-16 10:50:38.296184+00	fundador
388104f6-3294-4fa6-9fc0-ebca33eec086	Soriguera	\N	\N	interior	{"web": "https://soriguera.ddl.net", "adreca": "Plaça Mare de Déu de Medina - 25566 Vilamur | 25566", "notes_v1": null, "telefon_general": "973 62 06 09"}	Mantenir calor comercial.	research	[]	cap	templat	0	\N	\N	\N	d323117a-11e4-448a-badc-9058b3f4bd32	2026-03-16 11:31:03.581316+00	2026-03-16 11:31:03.581316+00	fundador
f3f01788-d8e9-409f-aaf5-c84a5be26fbf	Esterri d´Aneu	\N	\N	interior	{"web": "https://www.esterrianeu.cat/", "adreca": "Plaça de la Closa, 1\\n25580 Esterri d’Àneu\\nPallars Sobirà", "notes_v1": null, "telefon_general": "973 626 005"}	Mantenir calor comercial.	research	[]	cap	fred	0	\N	\N	\N	\N	2026-03-16 12:18:23.826299+00	2026-03-16 12:18:23.826299+00	fundador
b0988c73-01e8-4354-94aa-e4c3795511dc	Pobla de Segur	\N	\N	interior	{"web": "https://www.lapobladesegur.cat/ca/", "adreca": "Av. Verdaguer, 35\\n25500 La Pobla de Segur", "notes_v1": null, "telefon_general": " 973 680 038"}	demo per dijous  26	research	[]	cap	calent	0	\N	\N	\N	53983083-7a16-4591-bfba-7a852a4b1d44	2026-03-10 18:53:52.24095+00	2026-03-16 10:42:35.166655+00	fundador
d47fde40-f1d9-4255-8ad2-9813c5fd8f25	 Torrede de Capdella	\N	\N	interior	{"web": "htpps://www.torredecapdela.org", "adreca": null, "notes_v1": null, "telefon_general": "973663001"}	Baixa de la EVA trucar passat setmana Santa	research	[]	cap	templat	0	\N	\N	\N	63e2e3b1-9363-48ac-833d-8b374cad0dc7	2026-03-16 09:38:34.268009+00	2026-03-16 10:40:45.889341+00	fundador
78a2343f-dbf5-4707-9e44-5622d03fb5cb	Ajuntament Sort	\N	\N	interior	{"web": "https://sort.cat/", "adreca": "Carrer del Dr. Carles Pol i Aleu, 13, 25560 Sort", "notes_v1": null, "telefon_general": "973620010"}	demo per divendres 27	research	[]	cap	templat	0	\N	\N	\N	1a433539-031d-44ab-82be-baedf1c17811	2026-03-12 10:59:08.042304+00	2026-03-16 10:42:10.811+00	fundador
\.


--
-- Data for Name: pagaments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.pagaments (id, llicencia_id, import, tipus, estat, data_emisio, data_limit, data_confirmacio, notes, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: patrons_municipis; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.patrons_municipis (id, rang_poblacio, tipus_geografia, context_politic, probabilitat_conversio, temps_mitja_cicle_dies, etapa_bloqueig_frequent, estrategia_recomanada, objeccions_frequents, casos_exit_referencia, cops_aplicat, exitosos) FROM stdin;
\.


--
-- Data for Name: reunions_v2; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.reunions_v2 (id, municipi_id, data, tipus, assistents, aar_completat, notes_aar, poi_mes_reaccio, objeccio_principal, cta_final, temperatura_post) FROM stdin;
\.


--
-- Data for Name: tasques; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tasques (id, deal_id, contacte_id, municipi_id, usuari_id, titol, descripcio, data_venciment, tipus, prioritat, estat, created_at, updated_at) FROM stdin;
6bdb0db1-f39f-40da-9dce-de2eb7cc5b23	\N	\N	\N	\N	 torre de capdella		2026-03-11	email	mitjana	pendent	2026-03-11 21:07:50.292037+00	2026-03-11 21:07:50.292037+00
c1c08b19-b3a1-4bf7-9b49-b59ef94dac15	b0193e49-c46b-4645-a726-903aad57ab57	\N	\N	\N	Trucada seguiment, Josep Maria Tirbio		2026-03-20	trucada	mitjana	pendent	2026-03-16 10:44:46.19776+00	2026-03-16 10:44:46.19776+00
bf11f915-1bab-45de-8220-48db3e5794f7	2e5361cc-6f1d-460f-9872-eaa1dd6a3e80	\N	\N	\N	segon email		2026-03-20	email	mitjana	pendent	2026-03-16 11:02:21.680844+00	2026-03-16 11:02:21.680844+00
b85df12f-0b62-4a14-a665-4a146cb9b96d	2e5361cc-6f1d-460f-9872-eaa1dd6a3e80	\N	\N	\N	tercer email		2026-03-25	email	mitjana	pendent	2026-03-16 11:02:46.909491+00	2026-03-16 11:02:46.909491+00
0abcbdab-c9bf-4522-8e75-62f02b0d59a4	\N	\N	\N	\N	Trucar Maria Luengo	demanar email, propossar demo	2026-03-20	trucada	mitjana	pendent	2026-03-19 17:44:33.716253+00	2026-03-19 17:44:33.716253+00
384adf86-624b-4d8a-9082-7971750328e4	\N	\N	\N	\N	enviar correus Isona		2026-03-20	trucada	mitjana	pendent	2026-03-19 17:53:53.100034+00	2026-03-19 17:53:53.100034+00
1b3fd192-fa5e-480a-94b8-10ca5ffbb3c3	\N	\N	\N	\N	trucar Nuria de Soriguera		2026-03-27	trucada	mitjana	pendent	2026-03-23 09:40:13.891282+00	2026-03-23 09:40:13.891282+00
\.


--
-- Data for Name: trucades_v2; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trucades_v2 (id, municipi_id, data, durada_minuts, qui_va_contestar, notes_breus, resum_ia, seguent_accio_sugerida) FROM stdin;
\.


--
-- Data for Name: usuaris; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.usuaris (id, email, password_hash, nom, rol, actiu, created_at, updated_at) FROM stdin;
2673fec4-5d12-47a5-af73-810f1f393af8	admin@projectexinoxano.cat	$2b$12$CMYzXn91Y5LRR3f3rj70duKl6c0ZD8KacoiAtbVUTWJ.nR1elY45i	Miquel	admin	t	2026-03-10 16:52:36.952157+00	2026-03-17 16:43:30.840223+00
\.


--
-- Data for Name: schema_migrations; Type: TABLE DATA; Schema: realtime; Owner: -
--

COPY realtime.schema_migrations (version, inserted_at) FROM stdin;
20211116024918	2026-03-12 08:56:00
20211116045059	2026-03-12 08:56:00
20211116050929	2026-03-12 08:56:00
20211116051442	2026-03-12 08:56:00
20211116212300	2026-03-12 08:56:00
20211116213355	2026-03-12 08:56:00
20211116213934	2026-03-12 08:56:00
20211116214523	2026-03-12 08:56:00
20211122062447	2026-03-12 08:56:00
20211124070109	2026-03-12 08:56:00
20211202204204	2026-03-12 08:56:00
20211202204605	2026-03-12 08:56:00
20211210212804	2026-03-12 08:56:00
20211228014915	2026-03-12 08:56:01
20220107221237	2026-03-12 08:56:01
20220228202821	2026-03-12 08:56:01
20220312004840	2026-03-12 08:56:01
20220603231003	2026-03-12 08:56:01
20220603232444	2026-03-12 08:56:01
20220615214548	2026-03-12 08:56:01
20220712093339	2026-03-12 08:56:01
20220908172859	2026-03-12 08:56:01
20220916233421	2026-03-12 08:56:01
20230119133233	2026-03-12 08:56:01
20230128025114	2026-03-12 08:56:01
20230128025212	2026-03-12 08:56:01
20230227211149	2026-03-12 08:56:01
20230228184745	2026-03-12 08:56:01
20230308225145	2026-03-12 08:56:01
20230328144023	2026-03-12 08:56:01
20231018144023	2026-03-12 08:56:02
20231204144023	2026-03-12 08:56:02
20231204144024	2026-03-12 08:56:02
20231204144025	2026-03-12 08:56:02
20240108234812	2026-03-12 08:56:02
20240109165339	2026-03-12 08:56:02
20240227174441	2026-03-12 08:56:02
20240311171622	2026-03-12 08:56:02
20240321100241	2026-03-12 08:56:02
20240401105812	2026-03-12 08:56:02
20240418121054	2026-03-12 08:56:02
20240523004032	2026-03-12 08:56:02
20240618124746	2026-03-12 08:56:02
20240801235015	2026-03-12 08:56:02
20240805133720	2026-03-12 08:56:02
20240827160934	2026-03-12 08:56:02
20240919163303	2026-03-12 08:56:02
20240919163305	2026-03-12 08:56:02
20241019105805	2026-03-12 08:56:02
20241030150047	2026-03-12 08:56:02
20241108114728	2026-03-12 08:56:02
20241121104152	2026-03-12 08:56:02
20241130184212	2026-03-12 08:56:02
20241220035512	2026-03-12 08:56:02
20241220123912	2026-03-12 08:56:02
20241224161212	2026-03-12 08:56:02
20250107150512	2026-03-12 08:56:02
20250110162412	2026-03-12 08:56:02
20250123174212	2026-03-12 08:56:02
20250128220012	2026-03-12 08:56:02
20250506224012	2026-03-12 08:56:02
20250523164012	2026-03-12 08:56:02
20250714121412	2026-03-12 08:56:02
20250905041441	2026-03-12 08:56:02
20251103001201	2026-03-12 08:56:02
20251120212548	2026-03-12 08:56:02
20251120215549	2026-03-12 08:56:02
20260218120000	2026-03-12 08:56:02
\.


--
-- Data for Name: subscription; Type: TABLE DATA; Schema: realtime; Owner: -
--

COPY realtime.subscription (id, subscription_id, entity, filters, claims, created_at, action_filter) FROM stdin;
\.


--
-- Data for Name: buckets; Type: TABLE DATA; Schema: storage; Owner: -
--

COPY storage.buckets (id, name, owner, created_at, updated_at, public, avif_autodetection, file_size_limit, allowed_mime_types, owner_id, type) FROM stdin;
\.


--
-- Data for Name: buckets_analytics; Type: TABLE DATA; Schema: storage; Owner: -
--

COPY storage.buckets_analytics (name, type, format, created_at, updated_at, id, deleted_at) FROM stdin;
\.


--
-- Data for Name: buckets_vectors; Type: TABLE DATA; Schema: storage; Owner: -
--

COPY storage.buckets_vectors (id, type, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: migrations; Type: TABLE DATA; Schema: storage; Owner: -
--

COPY storage.migrations (id, name, hash, executed_at) FROM stdin;
0	create-migrations-table	e18db593bcde2aca2a408c4d1100f6abba2195df	2026-03-12 08:26:10.696968
1	initialmigration	6ab16121fbaa08bbd11b712d05f358f9b555d777	2026-03-12 08:26:10.832889
2	storage-schema	f6a1fa2c93cbcd16d4e487b362e45fca157a8dbd	2026-03-12 08:26:10.83712
3	pathtoken-column	2cb1b0004b817b29d5b0a971af16bafeede4b70d	2026-03-12 08:26:10.886692
4	add-migrations-rls	427c5b63fe1c5937495d9c635c263ee7a5905058	2026-03-12 08:26:11.127183
5	add-size-functions	79e081a1455b63666c1294a440f8ad4b1e6a7f84	2026-03-12 08:26:11.131442
6	change-column-name-in-get-size	ded78e2f1b5d7e616117897e6443a925965b30d2	2026-03-12 08:26:11.136333
7	add-rls-to-buckets	e7e7f86adbc51049f341dfe8d30256c1abca17aa	2026-03-12 08:26:11.147931
8	add-public-to-buckets	fd670db39ed65f9d08b01db09d6202503ca2bab3	2026-03-12 08:26:11.152251
9	fix-search-function	af597a1b590c70519b464a4ab3be54490712796b	2026-03-12 08:26:11.156913
10	search-files-search-function	b595f05e92f7e91211af1bbfe9c6a13bb3391e16	2026-03-12 08:26:11.161995
11	add-trigger-to-auto-update-updated_at-column	7425bdb14366d1739fa8a18c83100636d74dcaa2	2026-03-12 08:26:11.16668
12	add-automatic-avif-detection-flag	8e92e1266eb29518b6a4c5313ab8f29dd0d08df9	2026-03-12 08:26:11.182311
13	add-bucket-custom-limits	cce962054138135cd9a8c4bcd531598684b25e7d	2026-03-12 08:26:11.187243
14	use-bytes-for-max-size	941c41b346f9802b411f06f30e972ad4744dad27	2026-03-12 08:26:11.191821
15	add-can-insert-object-function	934146bc38ead475f4ef4b555c524ee5d66799e5	2026-03-12 08:26:11.247539
16	add-version	76debf38d3fd07dcfc747ca49096457d95b1221b	2026-03-12 08:26:11.252261
17	drop-owner-foreign-key	f1cbb288f1b7a4c1eb8c38504b80ae2a0153d101	2026-03-12 08:26:11.256497
18	add_owner_id_column_deprecate_owner	e7a511b379110b08e2f214be852c35414749fe66	2026-03-12 08:26:11.260505
19	alter-default-value-objects-id	02e5e22a78626187e00d173dc45f58fa66a4f043	2026-03-12 08:26:11.266223
20	list-objects-with-delimiter	cd694ae708e51ba82bf012bba00caf4f3b6393b7	2026-03-12 08:26:11.270704
21	s3-multipart-uploads	8c804d4a566c40cd1e4cc5b3725a664a9303657f	2026-03-12 08:26:11.276044
22	s3-multipart-uploads-big-ints	9737dc258d2397953c9953d9b86920b8be0cdb73	2026-03-12 08:26:11.290739
23	optimize-search-function	9d7e604cddc4b56a5422dc68c9313f4a1b6f132c	2026-03-12 08:26:11.300077
24	operation-function	8312e37c2bf9e76bbe841aa5fda889206d2bf8aa	2026-03-12 08:26:11.304975
25	custom-metadata	d974c6057c3db1c1f847afa0e291e6165693b990	2026-03-12 08:26:11.309509
26	objects-prefixes	215cabcb7f78121892a5a2037a09fedf9a1ae322	2026-03-12 08:26:11.314156
27	search-v2	859ba38092ac96eb3964d83bf53ccc0b141663a6	2026-03-12 08:26:11.318081
28	object-bucket-name-sorting	c73a2b5b5d4041e39705814fd3a1b95502d38ce4	2026-03-12 08:26:11.322007
29	create-prefixes	ad2c1207f76703d11a9f9007f821620017a66c21	2026-03-12 08:26:11.326048
30	update-object-levels	2be814ff05c8252fdfdc7cfb4b7f5c7e17f0bed6	2026-03-12 08:26:11.329875
31	objects-level-index	b40367c14c3440ec75f19bbce2d71e914ddd3da0	2026-03-12 08:26:11.333793
32	backward-compatible-index-on-objects	e0c37182b0f7aee3efd823298fb3c76f1042c0f7	2026-03-12 08:26:11.33815
33	backward-compatible-index-on-prefixes	b480e99ed951e0900f033ec4eb34b5bdcb4e3d49	2026-03-12 08:26:11.342166
34	optimize-search-function-v1	ca80a3dc7bfef894df17108785ce29a7fc8ee456	2026-03-12 08:26:11.346258
35	add-insert-trigger-prefixes	458fe0ffd07ec53f5e3ce9df51bfdf4861929ccc	2026-03-12 08:26:11.350372
36	optimise-existing-functions	6ae5fca6af5c55abe95369cd4f93985d1814ca8f	2026-03-12 08:26:11.354613
37	add-bucket-name-length-trigger	3944135b4e3e8b22d6d4cbb568fe3b0b51df15c1	2026-03-12 08:26:11.358811
38	iceberg-catalog-flag-on-buckets	02716b81ceec9705aed84aa1501657095b32e5c5	2026-03-12 08:26:11.363696
39	add-search-v2-sort-support	6706c5f2928846abee18461279799ad12b279b78	2026-03-12 08:26:11.42807
40	fix-prefix-race-conditions-optimized	7ad69982ae2d372b21f48fc4829ae9752c518f6b	2026-03-12 08:26:11.432486
41	add-object-level-update-trigger	07fcf1a22165849b7a029deed059ffcde08d1ae0	2026-03-12 08:26:11.436474
42	rollback-prefix-triggers	771479077764adc09e2ea2043eb627503c034cd4	2026-03-12 08:26:11.440502
43	fix-object-level	84b35d6caca9d937478ad8a797491f38b8c2979f	2026-03-12 08:26:11.444451
44	vector-bucket-type	99c20c0ffd52bb1ff1f32fb992f3b351e3ef8fb3	2026-03-12 08:26:11.448706
45	vector-buckets	049e27196d77a7cb76497a85afae669d8b230953	2026-03-12 08:26:11.454765
46	buckets-objects-grants	fedeb96d60fefd8e02ab3ded9fbde05632f84aed	2026-03-12 08:26:11.468185
47	iceberg-table-metadata	649df56855c24d8b36dd4cc1aeb8251aa9ad42c2	2026-03-12 08:26:11.47363
48	iceberg-catalog-ids	e0e8b460c609b9999ccd0df9ad14294613eed939	2026-03-12 08:26:11.480065
49	buckets-objects-grants-postgres	072b1195d0d5a2f888af6b2302a1938dd94b8b3d	2026-03-12 08:26:11.514438
50	search-v2-optimised	6323ac4f850aa14e7387eb32102869578b5bd478	2026-03-12 08:26:11.519499
51	index-backward-compatible-search	2ee395d433f76e38bcd3856debaf6e0e5b674011	2026-03-12 08:26:13.323655
52	drop-not-used-indexes-and-functions	5cc44c8696749ac11dd0dc37f2a3802075f3a171	2026-03-12 08:26:13.394139
53	drop-index-lower-name	d0cb18777d9e2a98ebe0bc5cc7a42e57ebe41854	2026-03-12 08:26:13.425556
54	drop-index-object-level	6289e048b1472da17c31a7eba1ded625a6457e67	2026-03-12 08:26:13.428281
55	prevent-direct-deletes	262a4798d5e0f2e7c8970232e03ce8be695d5819	2026-03-12 08:26:13.430048
56	fix-optimized-search-function	cb58526ebc23048049fd5bf2fd148d18b04a2073	2026-03-12 08:26:13.443918
\.


--
-- Data for Name: objects; Type: TABLE DATA; Schema: storage; Owner: -
--

COPY storage.objects (id, bucket_id, name, owner, created_at, updated_at, last_accessed_at, metadata, version, owner_id, user_metadata) FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads; Type: TABLE DATA; Schema: storage; Owner: -
--

COPY storage.s3_multipart_uploads (id, in_progress_size, upload_signature, bucket_id, key, version, owner_id, created_at, user_metadata) FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads_parts; Type: TABLE DATA; Schema: storage; Owner: -
--

COPY storage.s3_multipart_uploads_parts (id, upload_id, size, part_number, bucket_id, key, etag, owner_id, version, created_at) FROM stdin;
\.


--
-- Data for Name: vector_indexes; Type: TABLE DATA; Schema: storage; Owner: -
--

COPY storage.vector_indexes (id, name, bucket_id, data_type, dimension, distance_metric, metadata_configuration, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: secrets; Type: TABLE DATA; Schema: vault; Owner: -
--

COPY vault.secrets (id, name, description, secret, key_id, nonce, created_at, updated_at) FROM stdin;
\.


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: -
--

SELECT pg_catalog.setval('auth.refresh_tokens_id_seq', 1, false);


--
-- Name: subscription_id_seq; Type: SEQUENCE SET; Schema: realtime; Owner: -
--

SELECT pg_catalog.setval('realtime.subscription_id_seq', 1, false);


--
-- Name: mfa_amr_claims amr_id_pk; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.mfa_amr_claims
    ADD CONSTRAINT amr_id_pk PRIMARY KEY (id);


--
-- Name: audit_log_entries audit_log_entries_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.audit_log_entries
    ADD CONSTRAINT audit_log_entries_pkey PRIMARY KEY (id);


--
-- Name: custom_oauth_providers custom_oauth_providers_identifier_key; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.custom_oauth_providers
    ADD CONSTRAINT custom_oauth_providers_identifier_key UNIQUE (identifier);


--
-- Name: custom_oauth_providers custom_oauth_providers_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.custom_oauth_providers
    ADD CONSTRAINT custom_oauth_providers_pkey PRIMARY KEY (id);


--
-- Name: flow_state flow_state_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.flow_state
    ADD CONSTRAINT flow_state_pkey PRIMARY KEY (id);


--
-- Name: identities identities_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.identities
    ADD CONSTRAINT identities_pkey PRIMARY KEY (id);


--
-- Name: identities identities_provider_id_provider_unique; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.identities
    ADD CONSTRAINT identities_provider_id_provider_unique UNIQUE (provider_id, provider);


--
-- Name: instances instances_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.instances
    ADD CONSTRAINT instances_pkey PRIMARY KEY (id);


--
-- Name: mfa_amr_claims mfa_amr_claims_session_id_authentication_method_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.mfa_amr_claims
    ADD CONSTRAINT mfa_amr_claims_session_id_authentication_method_pkey UNIQUE (session_id, authentication_method);


--
-- Name: mfa_challenges mfa_challenges_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.mfa_challenges
    ADD CONSTRAINT mfa_challenges_pkey PRIMARY KEY (id);


--
-- Name: mfa_factors mfa_factors_last_challenged_at_key; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.mfa_factors
    ADD CONSTRAINT mfa_factors_last_challenged_at_key UNIQUE (last_challenged_at);


--
-- Name: mfa_factors mfa_factors_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.mfa_factors
    ADD CONSTRAINT mfa_factors_pkey PRIMARY KEY (id);


--
-- Name: oauth_authorizations oauth_authorizations_authorization_code_key; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_authorization_code_key UNIQUE (authorization_code);


--
-- Name: oauth_authorizations oauth_authorizations_authorization_id_key; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_authorization_id_key UNIQUE (authorization_id);


--
-- Name: oauth_authorizations oauth_authorizations_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_pkey PRIMARY KEY (id);


--
-- Name: oauth_client_states oauth_client_states_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.oauth_client_states
    ADD CONSTRAINT oauth_client_states_pkey PRIMARY KEY (id);


--
-- Name: oauth_clients oauth_clients_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.oauth_clients
    ADD CONSTRAINT oauth_clients_pkey PRIMARY KEY (id);


--
-- Name: oauth_consents oauth_consents_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.oauth_consents
    ADD CONSTRAINT oauth_consents_pkey PRIMARY KEY (id);


--
-- Name: oauth_consents oauth_consents_user_client_unique; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.oauth_consents
    ADD CONSTRAINT oauth_consents_user_client_unique UNIQUE (user_id, client_id);


--
-- Name: one_time_tokens one_time_tokens_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.one_time_tokens
    ADD CONSTRAINT one_time_tokens_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_token_unique; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.refresh_tokens
    ADD CONSTRAINT refresh_tokens_token_unique UNIQUE (token);


--
-- Name: saml_providers saml_providers_entity_id_key; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.saml_providers
    ADD CONSTRAINT saml_providers_entity_id_key UNIQUE (entity_id);


--
-- Name: saml_providers saml_providers_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.saml_providers
    ADD CONSTRAINT saml_providers_pkey PRIMARY KEY (id);


--
-- Name: saml_relay_states saml_relay_states_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.saml_relay_states
    ADD CONSTRAINT saml_relay_states_pkey PRIMARY KEY (id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: sso_domains sso_domains_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.sso_domains
    ADD CONSTRAINT sso_domains_pkey PRIMARY KEY (id);


--
-- Name: sso_providers sso_providers_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.sso_providers
    ADD CONSTRAINT sso_providers_pkey PRIMARY KEY (id);


--
-- Name: users users_phone_key; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.users
    ADD CONSTRAINT users_phone_key UNIQUE (phone);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: webauthn_challenges webauthn_challenges_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.webauthn_challenges
    ADD CONSTRAINT webauthn_challenges_pkey PRIMARY KEY (id);


--
-- Name: webauthn_credentials webauthn_credentials_pkey; Type: CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.webauthn_credentials
    ADD CONSTRAINT webauthn_credentials_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: contactes contactes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contactes
    ADD CONSTRAINT contactes_pkey PRIMARY KEY (id);


--
-- Name: contactes_v2 contactes_v2_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contactes_v2
    ADD CONSTRAINT contactes_v2_pkey PRIMARY KEY (id);


--
-- Name: deal_activitats deal_activitats_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deal_activitats
    ADD CONSTRAINT deal_activitats_pkey PRIMARY KEY (id);


--
-- Name: deals deals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deals
    ADD CONSTRAINT deals_pkey PRIMARY KEY (id);


--
-- Name: email_drafts_v2 email_drafts_v2_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_drafts_v2
    ADD CONSTRAINT email_drafts_v2_pkey PRIMARY KEY (id);


--
-- Name: email_sequencies_v2 email_sequencies_v2_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_sequencies_v2
    ADD CONSTRAINT email_sequencies_v2_pkey PRIMARY KEY (id);


--
-- Name: emails emails_message_id_extern_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emails
    ADD CONSTRAINT emails_message_id_extern_key UNIQUE (message_id_extern);


--
-- Name: emails emails_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emails
    ADD CONSTRAINT emails_pkey PRIMARY KEY (id);


--
-- Name: emails emails_tracking_token_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emails
    ADD CONSTRAINT emails_tracking_token_key UNIQUE (tracking_token);


--
-- Name: emails_v2 emails_v2_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emails_v2
    ADD CONSTRAINT emails_v2_pkey PRIMARY KEY (id);


--
-- Name: llicencies llicencies_deal_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.llicencies
    ADD CONSTRAINT llicencies_deal_id_key UNIQUE (deal_id);


--
-- Name: llicencies llicencies_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.llicencies
    ADD CONSTRAINT llicencies_pkey PRIMARY KEY (id);


--
-- Name: memoria_municipis memoria_municipis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memoria_municipis
    ADD CONSTRAINT memoria_municipis_pkey PRIMARY KEY (municipi_id);


--
-- Name: municipis_lifecycle municipis_lifecycle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipis_lifecycle
    ADD CONSTRAINT municipis_lifecycle_pkey PRIMARY KEY (id);


--
-- Name: municipis municipis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipis
    ADD CONSTRAINT municipis_pkey PRIMARY KEY (id);


--
-- Name: pagaments pagaments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pagaments
    ADD CONSTRAINT pagaments_pkey PRIMARY KEY (id);


--
-- Name: patrons_municipis patrons_municipis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patrons_municipis
    ADD CONSTRAINT patrons_municipis_pkey PRIMARY KEY (id);


--
-- Name: reunions_v2 reunions_v2_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reunions_v2
    ADD CONSTRAINT reunions_v2_pkey PRIMARY KEY (id);


--
-- Name: tasques tasques_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasques
    ADD CONSTRAINT tasques_pkey PRIMARY KEY (id);


--
-- Name: trucades_v2 trucades_v2_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trucades_v2
    ADD CONSTRAINT trucades_v2_pkey PRIMARY KEY (id);


--
-- Name: usuaris usuaris_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuaris
    ADD CONSTRAINT usuaris_email_key UNIQUE (email);


--
-- Name: usuaris usuaris_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuaris
    ADD CONSTRAINT usuaris_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: realtime; Owner: -
--

ALTER TABLE ONLY realtime.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id, inserted_at);


--
-- Name: subscription pk_subscription; Type: CONSTRAINT; Schema: realtime; Owner: -
--

ALTER TABLE ONLY realtime.subscription
    ADD CONSTRAINT pk_subscription PRIMARY KEY (id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: realtime; Owner: -
--

ALTER TABLE ONLY realtime.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: buckets_analytics buckets_analytics_pkey; Type: CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.buckets_analytics
    ADD CONSTRAINT buckets_analytics_pkey PRIMARY KEY (id);


--
-- Name: buckets buckets_pkey; Type: CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.buckets
    ADD CONSTRAINT buckets_pkey PRIMARY KEY (id);


--
-- Name: buckets_vectors buckets_vectors_pkey; Type: CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.buckets_vectors
    ADD CONSTRAINT buckets_vectors_pkey PRIMARY KEY (id);


--
-- Name: migrations migrations_name_key; Type: CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.migrations
    ADD CONSTRAINT migrations_name_key UNIQUE (name);


--
-- Name: migrations migrations_pkey; Type: CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.migrations
    ADD CONSTRAINT migrations_pkey PRIMARY KEY (id);


--
-- Name: objects objects_pkey; Type: CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.objects
    ADD CONSTRAINT objects_pkey PRIMARY KEY (id);


--
-- Name: s3_multipart_uploads_parts s3_multipart_uploads_parts_pkey; Type: CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.s3_multipart_uploads_parts
    ADD CONSTRAINT s3_multipart_uploads_parts_pkey PRIMARY KEY (id);


--
-- Name: s3_multipart_uploads s3_multipart_uploads_pkey; Type: CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.s3_multipart_uploads
    ADD CONSTRAINT s3_multipart_uploads_pkey PRIMARY KEY (id);


--
-- Name: vector_indexes vector_indexes_pkey; Type: CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.vector_indexes
    ADD CONSTRAINT vector_indexes_pkey PRIMARY KEY (id);


--
-- Name: audit_logs_instance_id_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX audit_logs_instance_id_idx ON auth.audit_log_entries USING btree (instance_id);


--
-- Name: confirmation_token_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE UNIQUE INDEX confirmation_token_idx ON auth.users USING btree (confirmation_token) WHERE ((confirmation_token)::text !~ '^[0-9 ]*$'::text);


--
-- Name: custom_oauth_providers_created_at_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX custom_oauth_providers_created_at_idx ON auth.custom_oauth_providers USING btree (created_at);


--
-- Name: custom_oauth_providers_enabled_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX custom_oauth_providers_enabled_idx ON auth.custom_oauth_providers USING btree (enabled);


--
-- Name: custom_oauth_providers_identifier_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX custom_oauth_providers_identifier_idx ON auth.custom_oauth_providers USING btree (identifier);


--
-- Name: custom_oauth_providers_provider_type_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX custom_oauth_providers_provider_type_idx ON auth.custom_oauth_providers USING btree (provider_type);


--
-- Name: email_change_token_current_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE UNIQUE INDEX email_change_token_current_idx ON auth.users USING btree (email_change_token_current) WHERE ((email_change_token_current)::text !~ '^[0-9 ]*$'::text);


--
-- Name: email_change_token_new_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE UNIQUE INDEX email_change_token_new_idx ON auth.users USING btree (email_change_token_new) WHERE ((email_change_token_new)::text !~ '^[0-9 ]*$'::text);


--
-- Name: factor_id_created_at_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX factor_id_created_at_idx ON auth.mfa_factors USING btree (user_id, created_at);


--
-- Name: flow_state_created_at_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX flow_state_created_at_idx ON auth.flow_state USING btree (created_at DESC);


--
-- Name: identities_email_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX identities_email_idx ON auth.identities USING btree (email text_pattern_ops);


--
-- Name: INDEX identities_email_idx; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON INDEX auth.identities_email_idx IS 'Auth: Ensures indexed queries on the email column';


--
-- Name: identities_user_id_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX identities_user_id_idx ON auth.identities USING btree (user_id);


--
-- Name: idx_auth_code; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX idx_auth_code ON auth.flow_state USING btree (auth_code);


--
-- Name: idx_oauth_client_states_created_at; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX idx_oauth_client_states_created_at ON auth.oauth_client_states USING btree (created_at);


--
-- Name: idx_user_id_auth_method; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX idx_user_id_auth_method ON auth.flow_state USING btree (user_id, authentication_method);


--
-- Name: mfa_challenge_created_at_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX mfa_challenge_created_at_idx ON auth.mfa_challenges USING btree (created_at DESC);


--
-- Name: mfa_factors_user_friendly_name_unique; Type: INDEX; Schema: auth; Owner: -
--

CREATE UNIQUE INDEX mfa_factors_user_friendly_name_unique ON auth.mfa_factors USING btree (friendly_name, user_id) WHERE (TRIM(BOTH FROM friendly_name) <> ''::text);


--
-- Name: mfa_factors_user_id_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX mfa_factors_user_id_idx ON auth.mfa_factors USING btree (user_id);


--
-- Name: oauth_auth_pending_exp_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX oauth_auth_pending_exp_idx ON auth.oauth_authorizations USING btree (expires_at) WHERE (status = 'pending'::auth.oauth_authorization_status);


--
-- Name: oauth_clients_deleted_at_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX oauth_clients_deleted_at_idx ON auth.oauth_clients USING btree (deleted_at);


--
-- Name: oauth_consents_active_client_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX oauth_consents_active_client_idx ON auth.oauth_consents USING btree (client_id) WHERE (revoked_at IS NULL);


--
-- Name: oauth_consents_active_user_client_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX oauth_consents_active_user_client_idx ON auth.oauth_consents USING btree (user_id, client_id) WHERE (revoked_at IS NULL);


--
-- Name: oauth_consents_user_order_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX oauth_consents_user_order_idx ON auth.oauth_consents USING btree (user_id, granted_at DESC);


--
-- Name: one_time_tokens_relates_to_hash_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX one_time_tokens_relates_to_hash_idx ON auth.one_time_tokens USING hash (relates_to);


--
-- Name: one_time_tokens_token_hash_hash_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX one_time_tokens_token_hash_hash_idx ON auth.one_time_tokens USING hash (token_hash);


--
-- Name: one_time_tokens_user_id_token_type_key; Type: INDEX; Schema: auth; Owner: -
--

CREATE UNIQUE INDEX one_time_tokens_user_id_token_type_key ON auth.one_time_tokens USING btree (user_id, token_type);


--
-- Name: reauthentication_token_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE UNIQUE INDEX reauthentication_token_idx ON auth.users USING btree (reauthentication_token) WHERE ((reauthentication_token)::text !~ '^[0-9 ]*$'::text);


--
-- Name: recovery_token_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE UNIQUE INDEX recovery_token_idx ON auth.users USING btree (recovery_token) WHERE ((recovery_token)::text !~ '^[0-9 ]*$'::text);


--
-- Name: refresh_tokens_instance_id_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX refresh_tokens_instance_id_idx ON auth.refresh_tokens USING btree (instance_id);


--
-- Name: refresh_tokens_instance_id_user_id_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX refresh_tokens_instance_id_user_id_idx ON auth.refresh_tokens USING btree (instance_id, user_id);


--
-- Name: refresh_tokens_parent_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX refresh_tokens_parent_idx ON auth.refresh_tokens USING btree (parent);


--
-- Name: refresh_tokens_session_id_revoked_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX refresh_tokens_session_id_revoked_idx ON auth.refresh_tokens USING btree (session_id, revoked);


--
-- Name: refresh_tokens_updated_at_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX refresh_tokens_updated_at_idx ON auth.refresh_tokens USING btree (updated_at DESC);


--
-- Name: saml_providers_sso_provider_id_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX saml_providers_sso_provider_id_idx ON auth.saml_providers USING btree (sso_provider_id);


--
-- Name: saml_relay_states_created_at_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX saml_relay_states_created_at_idx ON auth.saml_relay_states USING btree (created_at DESC);


--
-- Name: saml_relay_states_for_email_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX saml_relay_states_for_email_idx ON auth.saml_relay_states USING btree (for_email);


--
-- Name: saml_relay_states_sso_provider_id_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX saml_relay_states_sso_provider_id_idx ON auth.saml_relay_states USING btree (sso_provider_id);


--
-- Name: sessions_not_after_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX sessions_not_after_idx ON auth.sessions USING btree (not_after DESC);


--
-- Name: sessions_oauth_client_id_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX sessions_oauth_client_id_idx ON auth.sessions USING btree (oauth_client_id);


--
-- Name: sessions_user_id_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX sessions_user_id_idx ON auth.sessions USING btree (user_id);


--
-- Name: sso_domains_domain_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE UNIQUE INDEX sso_domains_domain_idx ON auth.sso_domains USING btree (lower(domain));


--
-- Name: sso_domains_sso_provider_id_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX sso_domains_sso_provider_id_idx ON auth.sso_domains USING btree (sso_provider_id);


--
-- Name: sso_providers_resource_id_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE UNIQUE INDEX sso_providers_resource_id_idx ON auth.sso_providers USING btree (lower(resource_id));


--
-- Name: sso_providers_resource_id_pattern_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX sso_providers_resource_id_pattern_idx ON auth.sso_providers USING btree (resource_id text_pattern_ops);


--
-- Name: unique_phone_factor_per_user; Type: INDEX; Schema: auth; Owner: -
--

CREATE UNIQUE INDEX unique_phone_factor_per_user ON auth.mfa_factors USING btree (user_id, phone);


--
-- Name: user_id_created_at_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX user_id_created_at_idx ON auth.sessions USING btree (user_id, created_at);


--
-- Name: users_email_partial_key; Type: INDEX; Schema: auth; Owner: -
--

CREATE UNIQUE INDEX users_email_partial_key ON auth.users USING btree (email) WHERE (is_sso_user = false);


--
-- Name: INDEX users_email_partial_key; Type: COMMENT; Schema: auth; Owner: -
--

COMMENT ON INDEX auth.users_email_partial_key IS 'Auth: A partial unique index that applies only when is_sso_user is false';


--
-- Name: users_instance_id_email_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX users_instance_id_email_idx ON auth.users USING btree (instance_id, lower((email)::text));


--
-- Name: users_instance_id_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX users_instance_id_idx ON auth.users USING btree (instance_id);


--
-- Name: users_is_anonymous_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX users_is_anonymous_idx ON auth.users USING btree (is_anonymous);


--
-- Name: webauthn_challenges_expires_at_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX webauthn_challenges_expires_at_idx ON auth.webauthn_challenges USING btree (expires_at);


--
-- Name: webauthn_challenges_user_id_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX webauthn_challenges_user_id_idx ON auth.webauthn_challenges USING btree (user_id);


--
-- Name: webauthn_credentials_credential_id_key; Type: INDEX; Schema: auth; Owner: -
--

CREATE UNIQUE INDEX webauthn_credentials_credential_id_key ON auth.webauthn_credentials USING btree (credential_id);


--
-- Name: webauthn_credentials_user_id_idx; Type: INDEX; Schema: auth; Owner: -
--

CREATE INDEX webauthn_credentials_user_id_idx ON auth.webauthn_credentials USING btree (user_id);


--
-- Name: ix_municipis_lifecycle_etapa_actual; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_municipis_lifecycle_etapa_actual ON public.municipis_lifecycle USING btree (etapa_actual);


--
-- Name: ix_municipis_lifecycle_nom; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_municipis_lifecycle_nom ON public.municipis_lifecycle USING btree (nom);


--
-- Name: ix_realtime_subscription_entity; Type: INDEX; Schema: realtime; Owner: -
--

CREATE INDEX ix_realtime_subscription_entity ON realtime.subscription USING btree (entity);


--
-- Name: messages_inserted_at_topic_index; Type: INDEX; Schema: realtime; Owner: -
--

CREATE INDEX messages_inserted_at_topic_index ON ONLY realtime.messages USING btree (inserted_at DESC, topic) WHERE ((extension = 'broadcast'::text) AND (private IS TRUE));


--
-- Name: subscription_subscription_id_entity_filters_action_filter_key; Type: INDEX; Schema: realtime; Owner: -
--

CREATE UNIQUE INDEX subscription_subscription_id_entity_filters_action_filter_key ON realtime.subscription USING btree (subscription_id, entity, filters, action_filter);


--
-- Name: bname; Type: INDEX; Schema: storage; Owner: -
--

CREATE UNIQUE INDEX bname ON storage.buckets USING btree (name);


--
-- Name: bucketid_objname; Type: INDEX; Schema: storage; Owner: -
--

CREATE UNIQUE INDEX bucketid_objname ON storage.objects USING btree (bucket_id, name);


--
-- Name: buckets_analytics_unique_name_idx; Type: INDEX; Schema: storage; Owner: -
--

CREATE UNIQUE INDEX buckets_analytics_unique_name_idx ON storage.buckets_analytics USING btree (name) WHERE (deleted_at IS NULL);


--
-- Name: idx_multipart_uploads_list; Type: INDEX; Schema: storage; Owner: -
--

CREATE INDEX idx_multipart_uploads_list ON storage.s3_multipart_uploads USING btree (bucket_id, key, created_at);


--
-- Name: idx_objects_bucket_id_name; Type: INDEX; Schema: storage; Owner: -
--

CREATE INDEX idx_objects_bucket_id_name ON storage.objects USING btree (bucket_id, name COLLATE "C");


--
-- Name: idx_objects_bucket_id_name_lower; Type: INDEX; Schema: storage; Owner: -
--

CREATE INDEX idx_objects_bucket_id_name_lower ON storage.objects USING btree (bucket_id, lower(name) COLLATE "C");


--
-- Name: name_prefix_search; Type: INDEX; Schema: storage; Owner: -
--

CREATE INDEX name_prefix_search ON storage.objects USING btree (name text_pattern_ops);


--
-- Name: vector_indexes_name_bucket_id_idx; Type: INDEX; Schema: storage; Owner: -
--

CREATE UNIQUE INDEX vector_indexes_name_bucket_id_idx ON storage.vector_indexes USING btree (name, bucket_id);


--
-- Name: subscription tr_check_filters; Type: TRIGGER; Schema: realtime; Owner: -
--

CREATE TRIGGER tr_check_filters BEFORE INSERT OR UPDATE ON realtime.subscription FOR EACH ROW EXECUTE FUNCTION realtime.subscription_check_filters();


--
-- Name: buckets enforce_bucket_name_length_trigger; Type: TRIGGER; Schema: storage; Owner: -
--

CREATE TRIGGER enforce_bucket_name_length_trigger BEFORE INSERT OR UPDATE OF name ON storage.buckets FOR EACH ROW EXECUTE FUNCTION storage.enforce_bucket_name_length();


--
-- Name: buckets protect_buckets_delete; Type: TRIGGER; Schema: storage; Owner: -
--

CREATE TRIGGER protect_buckets_delete BEFORE DELETE ON storage.buckets FOR EACH STATEMENT EXECUTE FUNCTION storage.protect_delete();


--
-- Name: objects protect_objects_delete; Type: TRIGGER; Schema: storage; Owner: -
--

CREATE TRIGGER protect_objects_delete BEFORE DELETE ON storage.objects FOR EACH STATEMENT EXECUTE FUNCTION storage.protect_delete();


--
-- Name: objects update_objects_updated_at; Type: TRIGGER; Schema: storage; Owner: -
--

CREATE TRIGGER update_objects_updated_at BEFORE UPDATE ON storage.objects FOR EACH ROW EXECUTE FUNCTION storage.update_updated_at_column();


--
-- Name: identities identities_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.identities
    ADD CONSTRAINT identities_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: mfa_amr_claims mfa_amr_claims_session_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.mfa_amr_claims
    ADD CONSTRAINT mfa_amr_claims_session_id_fkey FOREIGN KEY (session_id) REFERENCES auth.sessions(id) ON DELETE CASCADE;


--
-- Name: mfa_challenges mfa_challenges_auth_factor_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.mfa_challenges
    ADD CONSTRAINT mfa_challenges_auth_factor_id_fkey FOREIGN KEY (factor_id) REFERENCES auth.mfa_factors(id) ON DELETE CASCADE;


--
-- Name: mfa_factors mfa_factors_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.mfa_factors
    ADD CONSTRAINT mfa_factors_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: oauth_authorizations oauth_authorizations_client_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_client_id_fkey FOREIGN KEY (client_id) REFERENCES auth.oauth_clients(id) ON DELETE CASCADE;


--
-- Name: oauth_authorizations oauth_authorizations_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.oauth_authorizations
    ADD CONSTRAINT oauth_authorizations_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: oauth_consents oauth_consents_client_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.oauth_consents
    ADD CONSTRAINT oauth_consents_client_id_fkey FOREIGN KEY (client_id) REFERENCES auth.oauth_clients(id) ON DELETE CASCADE;


--
-- Name: oauth_consents oauth_consents_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.oauth_consents
    ADD CONSTRAINT oauth_consents_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: one_time_tokens one_time_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.one_time_tokens
    ADD CONSTRAINT one_time_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: refresh_tokens refresh_tokens_session_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.refresh_tokens
    ADD CONSTRAINT refresh_tokens_session_id_fkey FOREIGN KEY (session_id) REFERENCES auth.sessions(id) ON DELETE CASCADE;


--
-- Name: saml_providers saml_providers_sso_provider_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.saml_providers
    ADD CONSTRAINT saml_providers_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES auth.sso_providers(id) ON DELETE CASCADE;


--
-- Name: saml_relay_states saml_relay_states_flow_state_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.saml_relay_states
    ADD CONSTRAINT saml_relay_states_flow_state_id_fkey FOREIGN KEY (flow_state_id) REFERENCES auth.flow_state(id) ON DELETE CASCADE;


--
-- Name: saml_relay_states saml_relay_states_sso_provider_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.saml_relay_states
    ADD CONSTRAINT saml_relay_states_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES auth.sso_providers(id) ON DELETE CASCADE;


--
-- Name: sessions sessions_oauth_client_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.sessions
    ADD CONSTRAINT sessions_oauth_client_id_fkey FOREIGN KEY (oauth_client_id) REFERENCES auth.oauth_clients(id) ON DELETE CASCADE;


--
-- Name: sessions sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: sso_domains sso_domains_sso_provider_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.sso_domains
    ADD CONSTRAINT sso_domains_sso_provider_id_fkey FOREIGN KEY (sso_provider_id) REFERENCES auth.sso_providers(id) ON DELETE CASCADE;


--
-- Name: webauthn_challenges webauthn_challenges_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.webauthn_challenges
    ADD CONSTRAINT webauthn_challenges_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: webauthn_credentials webauthn_credentials_user_id_fkey; Type: FK CONSTRAINT; Schema: auth; Owner: -
--

ALTER TABLE ONLY auth.webauthn_credentials
    ADD CONSTRAINT webauthn_credentials_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;


--
-- Name: contactes contactes_municipi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contactes
    ADD CONSTRAINT contactes_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis(id);


--
-- Name: contactes_v2 contactes_v2_municipi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contactes_v2
    ADD CONSTRAINT contactes_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id);


--
-- Name: deal_activitats deal_activitats_deal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deal_activitats
    ADD CONSTRAINT deal_activitats_deal_id_fkey FOREIGN KEY (deal_id) REFERENCES public.deals(id);


--
-- Name: deals deals_contacte_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deals
    ADD CONSTRAINT deals_contacte_id_fkey FOREIGN KEY (contacte_id) REFERENCES public.contactes(id);


--
-- Name: deals deals_municipi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deals
    ADD CONSTRAINT deals_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis(id);


--
-- Name: email_drafts_v2 email_drafts_v2_contacte_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_drafts_v2
    ADD CONSTRAINT email_drafts_v2_contacte_id_fkey FOREIGN KEY (contacte_id) REFERENCES public.contactes_v2(id);


--
-- Name: email_drafts_v2 email_drafts_v2_email_enviat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_drafts_v2
    ADD CONSTRAINT email_drafts_v2_email_enviat_id_fkey FOREIGN KEY (email_enviat_id) REFERENCES public.emails_v2(id);


--
-- Name: email_drafts_v2 email_drafts_v2_municipi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_drafts_v2
    ADD CONSTRAINT email_drafts_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id);


--
-- Name: email_sequencies_v2 email_sequencies_v2_draft_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_sequencies_v2
    ADD CONSTRAINT email_sequencies_v2_draft_id_fkey FOREIGN KEY (draft_id) REFERENCES public.email_drafts_v2(id);


--
-- Name: email_sequencies_v2 email_sequencies_v2_municipi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_sequencies_v2
    ADD CONSTRAINT email_sequencies_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id);


--
-- Name: emails emails_contacte_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emails
    ADD CONSTRAINT emails_contacte_id_fkey FOREIGN KEY (contacte_id) REFERENCES public.contactes(id);


--
-- Name: emails emails_deal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emails
    ADD CONSTRAINT emails_deal_id_fkey FOREIGN KEY (deal_id) REFERENCES public.deals(id);


--
-- Name: emails_v2 emails_v2_municipi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emails_v2
    ADD CONSTRAINT emails_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id);


--
-- Name: municipis_lifecycle fk_municipi_actor_principal; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.municipis_lifecycle
    ADD CONSTRAINT fk_municipi_actor_principal FOREIGN KEY (actor_principal_id) REFERENCES public.contactes_v2(id);


--
-- Name: llicencies llicencies_deal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.llicencies
    ADD CONSTRAINT llicencies_deal_id_fkey FOREIGN KEY (deal_id) REFERENCES public.deals(id);


--
-- Name: memoria_municipis memoria_municipis_municipi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.memoria_municipis
    ADD CONSTRAINT memoria_municipis_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id);


--
-- Name: pagaments pagaments_llicencia_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pagaments
    ADD CONSTRAINT pagaments_llicencia_id_fkey FOREIGN KEY (llicencia_id) REFERENCES public.llicencies(id);


--
-- Name: reunions_v2 reunions_v2_municipi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reunions_v2
    ADD CONSTRAINT reunions_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id);


--
-- Name: tasques tasques_contacte_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasques
    ADD CONSTRAINT tasques_contacte_id_fkey FOREIGN KEY (contacte_id) REFERENCES public.contactes(id);


--
-- Name: tasques tasques_deal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasques
    ADD CONSTRAINT tasques_deal_id_fkey FOREIGN KEY (deal_id) REFERENCES public.deals(id);


--
-- Name: tasques tasques_municipi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasques
    ADD CONSTRAINT tasques_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis(id);


--
-- Name: tasques tasques_usuari_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasques
    ADD CONSTRAINT tasques_usuari_id_fkey FOREIGN KEY (usuari_id) REFERENCES public.usuaris(id);


--
-- Name: trucades_v2 trucades_v2_municipi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trucades_v2
    ADD CONSTRAINT trucades_v2_municipi_id_fkey FOREIGN KEY (municipi_id) REFERENCES public.municipis_lifecycle(id);


--
-- Name: objects objects_bucketId_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.objects
    ADD CONSTRAINT "objects_bucketId_fkey" FOREIGN KEY (bucket_id) REFERENCES storage.buckets(id);


--
-- Name: s3_multipart_uploads s3_multipart_uploads_bucket_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.s3_multipart_uploads
    ADD CONSTRAINT s3_multipart_uploads_bucket_id_fkey FOREIGN KEY (bucket_id) REFERENCES storage.buckets(id);


--
-- Name: s3_multipart_uploads_parts s3_multipart_uploads_parts_bucket_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.s3_multipart_uploads_parts
    ADD CONSTRAINT s3_multipart_uploads_parts_bucket_id_fkey FOREIGN KEY (bucket_id) REFERENCES storage.buckets(id);


--
-- Name: s3_multipart_uploads_parts s3_multipart_uploads_parts_upload_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.s3_multipart_uploads_parts
    ADD CONSTRAINT s3_multipart_uploads_parts_upload_id_fkey FOREIGN KEY (upload_id) REFERENCES storage.s3_multipart_uploads(id) ON DELETE CASCADE;


--
-- Name: vector_indexes vector_indexes_bucket_id_fkey; Type: FK CONSTRAINT; Schema: storage; Owner: -
--

ALTER TABLE ONLY storage.vector_indexes
    ADD CONSTRAINT vector_indexes_bucket_id_fkey FOREIGN KEY (bucket_id) REFERENCES storage.buckets_vectors(id);


--
-- Name: audit_log_entries; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.audit_log_entries ENABLE ROW LEVEL SECURITY;

--
-- Name: flow_state; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.flow_state ENABLE ROW LEVEL SECURITY;

--
-- Name: identities; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.identities ENABLE ROW LEVEL SECURITY;

--
-- Name: instances; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.instances ENABLE ROW LEVEL SECURITY;

--
-- Name: mfa_amr_claims; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.mfa_amr_claims ENABLE ROW LEVEL SECURITY;

--
-- Name: mfa_challenges; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.mfa_challenges ENABLE ROW LEVEL SECURITY;

--
-- Name: mfa_factors; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.mfa_factors ENABLE ROW LEVEL SECURITY;

--
-- Name: one_time_tokens; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.one_time_tokens ENABLE ROW LEVEL SECURITY;

--
-- Name: refresh_tokens; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.refresh_tokens ENABLE ROW LEVEL SECURITY;

--
-- Name: saml_providers; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.saml_providers ENABLE ROW LEVEL SECURITY;

--
-- Name: saml_relay_states; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.saml_relay_states ENABLE ROW LEVEL SECURITY;

--
-- Name: schema_migrations; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.schema_migrations ENABLE ROW LEVEL SECURITY;

--
-- Name: sessions; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.sessions ENABLE ROW LEVEL SECURITY;

--
-- Name: sso_domains; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.sso_domains ENABLE ROW LEVEL SECURITY;

--
-- Name: sso_providers; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.sso_providers ENABLE ROW LEVEL SECURITY;

--
-- Name: users; Type: ROW SECURITY; Schema: auth; Owner: -
--

ALTER TABLE auth.users ENABLE ROW LEVEL SECURITY;

--
-- Name: messages; Type: ROW SECURITY; Schema: realtime; Owner: -
--

ALTER TABLE realtime.messages ENABLE ROW LEVEL SECURITY;

--
-- Name: buckets; Type: ROW SECURITY; Schema: storage; Owner: -
--

ALTER TABLE storage.buckets ENABLE ROW LEVEL SECURITY;

--
-- Name: buckets_analytics; Type: ROW SECURITY; Schema: storage; Owner: -
--

ALTER TABLE storage.buckets_analytics ENABLE ROW LEVEL SECURITY;

--
-- Name: buckets_vectors; Type: ROW SECURITY; Schema: storage; Owner: -
--

ALTER TABLE storage.buckets_vectors ENABLE ROW LEVEL SECURITY;

--
-- Name: migrations; Type: ROW SECURITY; Schema: storage; Owner: -
--

ALTER TABLE storage.migrations ENABLE ROW LEVEL SECURITY;

--
-- Name: objects; Type: ROW SECURITY; Schema: storage; Owner: -
--

ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

--
-- Name: s3_multipart_uploads; Type: ROW SECURITY; Schema: storage; Owner: -
--

ALTER TABLE storage.s3_multipart_uploads ENABLE ROW LEVEL SECURITY;

--
-- Name: s3_multipart_uploads_parts; Type: ROW SECURITY; Schema: storage; Owner: -
--

ALTER TABLE storage.s3_multipart_uploads_parts ENABLE ROW LEVEL SECURITY;

--
-- Name: vector_indexes; Type: ROW SECURITY; Schema: storage; Owner: -
--

ALTER TABLE storage.vector_indexes ENABLE ROW LEVEL SECURITY;

--
-- Name: supabase_realtime; Type: PUBLICATION; Schema: -; Owner: -
--

CREATE PUBLICATION supabase_realtime WITH (publish = 'insert, update, delete, truncate');


--
-- Name: issue_graphql_placeholder; Type: EVENT TRIGGER; Schema: -; Owner: -
--

CREATE EVENT TRIGGER issue_graphql_placeholder ON sql_drop
         WHEN TAG IN ('DROP EXTENSION')
   EXECUTE FUNCTION extensions.set_graphql_placeholder();


--
-- Name: issue_pg_cron_access; Type: EVENT TRIGGER; Schema: -; Owner: -
--

CREATE EVENT TRIGGER issue_pg_cron_access ON ddl_command_end
         WHEN TAG IN ('CREATE EXTENSION')
   EXECUTE FUNCTION extensions.grant_pg_cron_access();


--
-- Name: issue_pg_graphql_access; Type: EVENT TRIGGER; Schema: -; Owner: -
--

CREATE EVENT TRIGGER issue_pg_graphql_access ON ddl_command_end
         WHEN TAG IN ('CREATE FUNCTION')
   EXECUTE FUNCTION extensions.grant_pg_graphql_access();


--
-- Name: issue_pg_net_access; Type: EVENT TRIGGER; Schema: -; Owner: -
--

CREATE EVENT TRIGGER issue_pg_net_access ON ddl_command_end
         WHEN TAG IN ('CREATE EXTENSION')
   EXECUTE FUNCTION extensions.grant_pg_net_access();


--
-- Name: pgrst_ddl_watch; Type: EVENT TRIGGER; Schema: -; Owner: -
--

CREATE EVENT TRIGGER pgrst_ddl_watch ON ddl_command_end
   EXECUTE FUNCTION extensions.pgrst_ddl_watch();


--
-- Name: pgrst_drop_watch; Type: EVENT TRIGGER; Schema: -; Owner: -
--

CREATE EVENT TRIGGER pgrst_drop_watch ON sql_drop
   EXECUTE FUNCTION extensions.pgrst_drop_watch();


--
-- PostgreSQL database dump complete
--

\unrestrict 44sexrYUT6xFQcbkGtCnoPzvMXfV1dnslygQVLhnBLRk93CNfX7uNpjC9qpmgGH

