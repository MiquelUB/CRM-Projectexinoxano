--
-- PostgreSQL database dump
--

\restrict YWNcpZEBCZkJl9S5LptsrlBcrRup8Fyx2f71QJNEcW9thjQ9DUci8yelTcm28wv

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
-- Data for Name: audit_log_entries; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: custom_oauth_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: oauth_clients; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: oauth_authorizations; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: oauth_client_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: oauth_consents; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: one_time_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: sso_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: saml_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: saml_relay_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: schema_migrations; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

INSERT INTO auth.schema_migrations (version) VALUES ('20171026211738');
INSERT INTO auth.schema_migrations (version) VALUES ('20171026211808');
INSERT INTO auth.schema_migrations (version) VALUES ('20171026211834');
INSERT INTO auth.schema_migrations (version) VALUES ('20180103212743');
INSERT INTO auth.schema_migrations (version) VALUES ('20180108183307');
INSERT INTO auth.schema_migrations (version) VALUES ('20180119214651');
INSERT INTO auth.schema_migrations (version) VALUES ('20180125194653');
INSERT INTO auth.schema_migrations (version) VALUES ('00');
INSERT INTO auth.schema_migrations (version) VALUES ('20210710035447');
INSERT INTO auth.schema_migrations (version) VALUES ('20210722035447');
INSERT INTO auth.schema_migrations (version) VALUES ('20210730183235');
INSERT INTO auth.schema_migrations (version) VALUES ('20210909172000');
INSERT INTO auth.schema_migrations (version) VALUES ('20210927181326');
INSERT INTO auth.schema_migrations (version) VALUES ('20211122151130');
INSERT INTO auth.schema_migrations (version) VALUES ('20211124214934');
INSERT INTO auth.schema_migrations (version) VALUES ('20211202183645');
INSERT INTO auth.schema_migrations (version) VALUES ('20220114185221');
INSERT INTO auth.schema_migrations (version) VALUES ('20220114185340');
INSERT INTO auth.schema_migrations (version) VALUES ('20220224000811');
INSERT INTO auth.schema_migrations (version) VALUES ('20220323170000');
INSERT INTO auth.schema_migrations (version) VALUES ('20220429102000');
INSERT INTO auth.schema_migrations (version) VALUES ('20220531120530');
INSERT INTO auth.schema_migrations (version) VALUES ('20220614074223');
INSERT INTO auth.schema_migrations (version) VALUES ('20220811173540');
INSERT INTO auth.schema_migrations (version) VALUES ('20221003041349');
INSERT INTO auth.schema_migrations (version) VALUES ('20221003041400');
INSERT INTO auth.schema_migrations (version) VALUES ('20221011041400');
INSERT INTO auth.schema_migrations (version) VALUES ('20221020193600');
INSERT INTO auth.schema_migrations (version) VALUES ('20221021073300');
INSERT INTO auth.schema_migrations (version) VALUES ('20221021082433');
INSERT INTO auth.schema_migrations (version) VALUES ('20221027105023');
INSERT INTO auth.schema_migrations (version) VALUES ('20221114143122');
INSERT INTO auth.schema_migrations (version) VALUES ('20221114143410');
INSERT INTO auth.schema_migrations (version) VALUES ('20221125140132');
INSERT INTO auth.schema_migrations (version) VALUES ('20221208132122');
INSERT INTO auth.schema_migrations (version) VALUES ('20221215195500');
INSERT INTO auth.schema_migrations (version) VALUES ('20221215195800');
INSERT INTO auth.schema_migrations (version) VALUES ('20221215195900');
INSERT INTO auth.schema_migrations (version) VALUES ('20230116124310');
INSERT INTO auth.schema_migrations (version) VALUES ('20230116124412');
INSERT INTO auth.schema_migrations (version) VALUES ('20230131181311');
INSERT INTO auth.schema_migrations (version) VALUES ('20230322519590');
INSERT INTO auth.schema_migrations (version) VALUES ('20230402418590');
INSERT INTO auth.schema_migrations (version) VALUES ('20230411005111');
INSERT INTO auth.schema_migrations (version) VALUES ('20230508135423');
INSERT INTO auth.schema_migrations (version) VALUES ('20230523124323');
INSERT INTO auth.schema_migrations (version) VALUES ('20230818113222');
INSERT INTO auth.schema_migrations (version) VALUES ('20230914180801');
INSERT INTO auth.schema_migrations (version) VALUES ('20231027141322');
INSERT INTO auth.schema_migrations (version) VALUES ('20231114161723');
INSERT INTO auth.schema_migrations (version) VALUES ('20231117164230');
INSERT INTO auth.schema_migrations (version) VALUES ('20240115144230');
INSERT INTO auth.schema_migrations (version) VALUES ('20240214120130');
INSERT INTO auth.schema_migrations (version) VALUES ('20240306115329');
INSERT INTO auth.schema_migrations (version) VALUES ('20240314092811');
INSERT INTO auth.schema_migrations (version) VALUES ('20240427152123');
INSERT INTO auth.schema_migrations (version) VALUES ('20240612123726');
INSERT INTO auth.schema_migrations (version) VALUES ('20240729123726');
INSERT INTO auth.schema_migrations (version) VALUES ('20240802193726');
INSERT INTO auth.schema_migrations (version) VALUES ('20240806073726');
INSERT INTO auth.schema_migrations (version) VALUES ('20241009103726');
INSERT INTO auth.schema_migrations (version) VALUES ('20250717082212');
INSERT INTO auth.schema_migrations (version) VALUES ('20250731150234');
INSERT INTO auth.schema_migrations (version) VALUES ('20250804100000');
INSERT INTO auth.schema_migrations (version) VALUES ('20250901200500');
INSERT INTO auth.schema_migrations (version) VALUES ('20250903112500');
INSERT INTO auth.schema_migrations (version) VALUES ('20250904133000');
INSERT INTO auth.schema_migrations (version) VALUES ('20250925093508');
INSERT INTO auth.schema_migrations (version) VALUES ('20251007112900');
INSERT INTO auth.schema_migrations (version) VALUES ('20251104100000');
INSERT INTO auth.schema_migrations (version) VALUES ('20251111201300');
INSERT INTO auth.schema_migrations (version) VALUES ('20251201000000');
INSERT INTO auth.schema_migrations (version) VALUES ('20260115000000');
INSERT INTO auth.schema_migrations (version) VALUES ('20260121000000');
INSERT INTO auth.schema_migrations (version) VALUES ('20260219120000');
INSERT INTO auth.schema_migrations (version) VALUES ('20260302000000');


--
-- Data for Name: sso_domains; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: webauthn_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: webauthn_credentials; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--



--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.alembic_version (version_num) VALUES ('a3f5e76d049d');


--
-- Data for Name: municipis; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.municipis (id, nom, tipus, provincia, poblacio, web, telefon, adreca, notes, created_at, updated_at, codi_postal) VALUES ('d47fde40-f1d9-4255-8ad2-9813c5fd8f25', ' Torrede de Capdella', 'ajuntament', 'Lleida', 'Torre de Capdella', 'htpps://www.torredecapdela.org', '973663001', NULL, NULL, '2026-03-16 09:38:34.268009+00', '2026-03-16 10:40:45.889341+00', NULL);
INSERT INTO public.municipis (id, nom, tipus, provincia, poblacio, web, telefon, adreca, notes, created_at, updated_at, codi_postal) VALUES ('78a2343f-dbf5-4707-9e44-5622d03fb5cb', 'Ajuntament Sort', 'ajuntament', 'Lleida', 'Sort', 'https://sort.cat/', '973620010', 'Carrer del Dr. Carles Pol i Aleu, 13, 25560 Sort', NULL, '2026-03-12 10:59:08.042304+00', '2026-03-16 10:42:10.811+00', NULL);
INSERT INTO public.municipis (id, nom, tipus, provincia, poblacio, web, telefon, adreca, notes, created_at, updated_at, codi_postal) VALUES ('b0988c73-01e8-4354-94aa-e4c3795511dc', 'Pobla de Segur', 'ajuntament', 'Lleida', 'Pobla de Segur', 'https://www.lapobladesegur.cat/ca/', ' 973 680 038', 'Av. Verdaguer, 35
25500 La Pobla de Segur', NULL, '2026-03-10 18:53:52.24095+00', '2026-03-16 10:42:35.166655+00', NULL);
INSERT INTO public.municipis (id, nom, tipus, provincia, poblacio, web, telefon, adreca, notes, created_at, updated_at, codi_postal) VALUES ('76993a09-1cc4-4288-ae93-c2aed91f5278', 'Canillo', 'ajuntament', 'Lleida', 'Canillo', 'https://www.canillo.ad', '(+376) 751 036', 'Pl. Carlemany núm.4,
Edifici Telecabina .
AD100 Canillo,
PRINCIPAT D’ANDORRA', NULL, '2026-03-16 10:50:38.296184+00', '2026-03-16 10:50:38.296184+00', NULL);
INSERT INTO public.municipis (id, nom, tipus, provincia, poblacio, web, telefon, adreca, notes, created_at, updated_at, codi_postal) VALUES ('388104f6-3294-4fa6-9fc0-ebca33eec086', 'Soriguera', 'ajuntament', 'Lleida', 'Soriguera', 'https://soriguera.ddl.net', '973 62 06 09', 'Plaça Mare de Déu de Medina - 25566 Vilamur | 25566', NULL, '2026-03-16 11:31:03.581316+00', '2026-03-16 11:31:03.581316+00', NULL);
INSERT INTO public.municipis (id, nom, tipus, provincia, poblacio, web, telefon, adreca, notes, created_at, updated_at, codi_postal) VALUES ('f3f01788-d8e9-409f-aaf5-c84a5be26fbf', 'Esterri d´Aneu', 'ajuntament', 'Lleida', 'Esterri d´Aneu', 'https://www.esterrianeu.cat/', '973 626 005', 'Plaça de la Closa, 1
25580 Esterri d’Àneu
Pallars Sobirà', NULL, '2026-03-16 12:18:23.826299+00', '2026-03-16 12:18:23.826299+00', NULL);
INSERT INTO public.municipis (id, nom, tipus, provincia, poblacio, web, telefon, adreca, notes, created_at, updated_at, codi_postal) VALUES ('117d35c3-b4c5-406d-a8d4-8cb58393bf52', 'Isona', 'ajuntament', 'Lleida', 'Isona i conca dellà', 'https://www.isonaiconcadella.cat/', '973 664 008', NULL, NULL, '2026-03-19 17:19:42.751755+00', '2026-03-19 17:19:42.751755+00', NULL);
INSERT INTO public.municipis (id, nom, tipus, provincia, poblacio, web, telefon, adreca, notes, created_at, updated_at, codi_postal) VALUES ('af9ca22a-4e96-47e8-b284-1d1fba3f97fa', 'Consorsi de Turisme de les Valls d´Aneu', 'ajuntament', 'Lleida', 'Espot', NULL, NULL, NULL, NULL, '2026-03-19 17:42:32.133326+00', '2026-03-19 17:42:32.133326+00', NULL);
INSERT INTO public.municipis (id, nom, tipus, provincia, poblacio, web, telefon, adreca, notes, created_at, updated_at, codi_postal) VALUES ('322a61f2-bddc-45ee-ae31-d79f279cdedf', 'El Pont de Suert', 'ajuntament', 'Lleida', 'Pont de Suert', 'https://www.elpontdesuert.cat/', '973 690 005', NULL, NULL, '2026-03-19 18:00:14.31416+00', '2026-03-19 18:00:14.31416+00', NULL);
INSERT INTO public.municipis (id, nom, tipus, provincia, poblacio, web, telefon, adreca, notes, created_at, updated_at, codi_postal) VALUES ('5cfe1986-555e-4e28-bc9e-ac500ac0cd4b', 'El Pont de Suert', 'ajuntament', 'Lleida', 'El Pont de Suert', 'https://www.elpontdesuert.cat/', ' 973 690 005', NULL, NULL, '2026-03-23 10:42:30.747236+00', '2026-03-23 10:42:30.747236+00', NULL);


--
-- Data for Name: contactes; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('b5e7c612-dcdc-49ed-9e49-f78edefa741c', 'b0988c73-01e8-4354-94aa-e4c3795511dc', 'Josep Maria Tirbió i Civís ', 'Regidor de Turisme', 'mia@lapobladesegur.cat', NULL, NULL, NULL, true, '2026-03-10 18:55:56.662685+00', '2026-03-10 18:55:56.662685+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('53983083-7a16-4591-bfba-7a852a4b1d44', 'b0988c73-01e8-4354-94aa-e4c3795511dc', ' Marc Baró i Bernaduca', 'Alcalde', 'alcaldia@lapobladesegur.cat', NULL, NULL, NULL, true, '2026-03-10 18:54:45.023885+00', '2026-03-10 18:54:45.023885+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('1a433539-031d-44ab-82be-baedf1c17811', '78a2343f-dbf5-4707-9e44-5622d03fb5cb', 'Baldo Farré Serrat ', 'Alcalde', 'alcaldia@sort.cat', NULL, NULL, NULL, true, '2026-03-12 11:00:17.047496+00', '2026-03-12 11:00:17.047496+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('1e022c62-e440-428e-9550-a107e8e50c12', '76993a09-1cc4-4288-ae93-c2aed91f5278', ' Jordi Alcobé Font', 'Cònsol Major', 'comu@canillo.ad', '(+376) 751 036', NULL, NULL, true, '2026-03-16 10:56:54.792186+00', '2026-03-16 10:56:54.792186+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('c64e9de5-0919-44a5-8e37-5886359b184f', '76993a09-1cc4-4288-ae93-c2aed91f5278', ' Marc Casal', 'Cònsol Menor', 'turisme@canillo.ad', NULL, NULL, NULL, true, '2026-03-16 10:57:36.861931+00', '2026-03-16 10:57:36.861931+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('d323117a-11e4-448a-badc-9058b3f4bd32', '388104f6-3294-4fa6-9fc0-ebca33eec086', ' Josep Ramon Fondevila Isus ', 'Alcalde', 'ajuntament@soriguera.ddl.net', NULL, NULL, NULL, true, '2026-03-16 11:32:43.497594+00', '2026-03-16 11:32:43.497594+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('9a77e835-1d42-42e7-b497-2ede3948f73b', '388104f6-3294-4fa6-9fc0-ebca33eec086', 'Ariadna Vidal', 'lidera les excavacions i el relat científic del jaciment.', 'info@museudecamins.com', NULL, NULL, NULL, true, '2026-03-16 11:37:12.598402+00', '2026-03-16 11:37:12.598402+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('3f543baf-2ae0-4513-9a9b-54b8b97b02c1', '117d35c3-b4c5-406d-a8d4-8cb58393bf52', 'Jeannine Abella i Chica', 'Alcaldessa', 'ajuntament@isona.ddl.net', '973 664 008', NULL, NULL, true, '2026-03-19 17:20:38.173686+00', '2026-03-19 17:20:38.173686+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('66dd3892-3736-4bd8-9c0f-ca27d484ae14', 'af9ca22a-4e96-47e8-b284-1d1fba3f97fa', 'María Luengo', NULL, NULL, '722652089', NULL, NULL, true, '2026-03-19 17:43:27.481022+00', '2026-03-19 17:43:27.481022+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('de4cbf85-800b-4cda-9b1b-3dfece9ae6d3', '322a61f2-bddc-45ee-ae31-d79f279cdedf', 'Iolanda Ferran i Closa', 'Alcaldessa', 'ajuntament@elpontdesuert.cat', '973 690 005', NULL, NULL, true, '2026-03-19 18:01:08.102013+00', '2026-03-19 18:01:08.102013+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('7563ae81-5953-4720-b7e2-0558f127e651', '322a61f2-bddc-45ee-ae31-d79f279cdedf', 'Susanna Garrido i Castro', 'Regidora de Comunicació i TIC', 'ajuntament@elpontdesuert.cat', '973 690 005', NULL, NULL, true, '2026-03-19 18:03:01.377617+00', '2026-03-19 18:03:01.377617+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('779138ee-9918-494a-94ad-2c2de9adb1e2', 'd47fde40-f1d9-4255-8ad2-9813c5fd8f25', 'Eva Perisé ', 'Regidora turisme', 'eperise@torrecapdella.cat', ' 973 66 32 62 ', NULL, NULL, true, '2026-03-16 09:43:37.372438+00', '2026-03-20 11:53:42.617106+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('63e2e3b1-9363-48ac-833d-8b374cad0dc7', 'd47fde40-f1d9-4255-8ad2-9813c5fd8f25', 'Josep Maria Dalmau Gil ', 'Alcalde', 'jmdalmau@torrecapdella.cat', '973 66 30 01 ', NULL, NULL, true, '2026-03-16 09:42:09.058303+00', '2026-03-20 11:53:57.730706+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('ed326611-e34c-4e5a-a8ad-3ad9af8bbfd7', 'd47fde40-f1d9-4255-8ad2-9813c5fd8f25', 'Ramon Jordana', ' Regidor de la Torre de Capdela ', 'rjordana@torrecapdella.cat', NULL, NULL, NULL, true, '2026-03-20 11:45:33.724267+00', '2026-03-20 11:56:23.201686+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('00efd101-915b-48dd-bb00-8e09526d8bf1', '78a2343f-dbf5-4707-9e44-5622d03fb5cb', 'Gerard Aguado', 'turisme', 'turisme@sort.cat', '973620010', NULL, NULL, true, '2026-03-12 11:00:48.70712+00', '2026-03-23 09:18:12.318517+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('531b277b-ad47-4d95-96f2-a213e09043f7', '388104f6-3294-4fa6-9fc0-ebca33eec086', 'Nuria', 'Administrativa', 'ajuntamentdesoriguera@gmail.com', '973 62 06 09', NULL, NULL, true, '2026-03-23 09:36:39.139092+00', '2026-03-23 09:36:39.139092+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('94e68e67-cb27-4b4d-a3eb-ba26ec5f8817', '117d35c3-b4c5-406d-a8d4-8cb58393bf52', 'Ariadna Roca Melines', 'Regidora de Turisme i Transf. Digital', 'ariadnaroca2002@gmail.com', '973 664 008', NULL, NULL, true, '2026-03-19 17:21:45.776847+00', '2026-03-23 09:55:17.475955+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('1f4435f6-b943-4f04-b391-1eaf77d872ba', '78a2343f-dbf5-4707-9e44-5622d03fb5cb', ' Pere Báscones Navarro ', '| Àrea: Cultura, Educació, Turisme, Sostenibilitat i Noves  Tecnologies. ', 'pbascones@sort.cat', '639 30 30 67 ', NULL, NULL, true, '2026-03-23 11:04:17.600403+00', '2026-03-23 11:04:17.600403+00');
INSERT INTO public.contactes (id, municipi_id, nom, carrec, email, telefon, linkedin, notes_humanes, actiu, created_at, updated_at) VALUES ('bca93a14-db52-48b2-b801-041730f1edff', '322a61f2-bddc-45ee-ae31-d79f279cdedf', 'Josep M. Rispa i Pifarré', 'Regidor de Turisme, Cultura i Patrimoni', 'regidoriacultura@elpontdesuert.cat', '973 690 005', NULL, NULL, true, '2026-03-19 18:02:02.018974+00', '2026-03-23 11:29:48.344451+00');


--
-- Data for Name: municipis_lifecycle; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.municipis_lifecycle (id, nom, comarca, poblacio, geografia, diagnostic_digital, angle_personalitzacio, etapa_actual, historial_etapes, blocker_actual, temperatura, dies_etapa_actual, data_conversio, pla_contractat, estat_final, actor_principal_id, data_creacio, data_ultima_accio, usuari_asignat) VALUES ('76993a09-1cc4-4288-ae93-c2aed91f5278', 'Canillo', NULL, NULL, 'interior', '{"web": "https://www.canillo.ad", "adreca": "Pl. Carlemany núm.4,\nEdifici Telecabina .\nAD100 Canillo,\nPRINCIPAT D’ANDORRA", "notes_v1": null, "telefon_general": "(+376) 751 036"}', 'Mantenir calor comercial.', 'research', '[]', 'cap', 'templat', 0, NULL, NULL, NULL, 'c64e9de5-0919-44a5-8e37-5886359b184f', '2026-03-16 10:50:38.296184+00', '2026-03-16 10:50:38.296184+00', 'fundador');
INSERT INTO public.municipis_lifecycle (id, nom, comarca, poblacio, geografia, diagnostic_digital, angle_personalitzacio, etapa_actual, historial_etapes, blocker_actual, temperatura, dies_etapa_actual, data_conversio, pla_contractat, estat_final, actor_principal_id, data_creacio, data_ultima_accio, usuari_asignat) VALUES ('388104f6-3294-4fa6-9fc0-ebca33eec086', 'Soriguera', NULL, NULL, 'interior', '{"web": "https://soriguera.ddl.net", "adreca": "Plaça Mare de Déu de Medina - 25566 Vilamur | 25566", "notes_v1": null, "telefon_general": "973 62 06 09"}', 'Mantenir calor comercial.', 'research', '[]', 'cap', 'templat', 0, NULL, NULL, NULL, 'd323117a-11e4-448a-badc-9058b3f4bd32', '2026-03-16 11:31:03.581316+00', '2026-03-16 11:31:03.581316+00', 'fundador');
INSERT INTO public.municipis_lifecycle (id, nom, comarca, poblacio, geografia, diagnostic_digital, angle_personalitzacio, etapa_actual, historial_etapes, blocker_actual, temperatura, dies_etapa_actual, data_conversio, pla_contractat, estat_final, actor_principal_id, data_creacio, data_ultima_accio, usuari_asignat) VALUES ('f3f01788-d8e9-409f-aaf5-c84a5be26fbf', 'Esterri d´Aneu', NULL, NULL, 'interior', '{"web": "https://www.esterrianeu.cat/", "adreca": "Plaça de la Closa, 1\n25580 Esterri d’Àneu\nPallars Sobirà", "notes_v1": null, "telefon_general": "973 626 005"}', 'Mantenir calor comercial.', 'research', '[]', 'cap', 'fred', 0, NULL, NULL, NULL, NULL, '2026-03-16 12:18:23.826299+00', '2026-03-16 12:18:23.826299+00', 'fundador');
INSERT INTO public.municipis_lifecycle (id, nom, comarca, poblacio, geografia, diagnostic_digital, angle_personalitzacio, etapa_actual, historial_etapes, blocker_actual, temperatura, dies_etapa_actual, data_conversio, pla_contractat, estat_final, actor_principal_id, data_creacio, data_ultima_accio, usuari_asignat) VALUES ('b0988c73-01e8-4354-94aa-e4c3795511dc', 'Pobla de Segur', NULL, NULL, 'interior', '{"web": "https://www.lapobladesegur.cat/ca/", "adreca": "Av. Verdaguer, 35\n25500 La Pobla de Segur", "notes_v1": null, "telefon_general": " 973 680 038"}', 'demo per dijous  26', 'research', '[]', 'cap', 'calent', 0, NULL, NULL, NULL, '53983083-7a16-4591-bfba-7a852a4b1d44', '2026-03-10 18:53:52.24095+00', '2026-03-16 10:42:35.166655+00', 'fundador');
INSERT INTO public.municipis_lifecycle (id, nom, comarca, poblacio, geografia, diagnostic_digital, angle_personalitzacio, etapa_actual, historial_etapes, blocker_actual, temperatura, dies_etapa_actual, data_conversio, pla_contractat, estat_final, actor_principal_id, data_creacio, data_ultima_accio, usuari_asignat) VALUES ('d47fde40-f1d9-4255-8ad2-9813c5fd8f25', ' Torrede de Capdella', NULL, NULL, 'interior', '{"web": "htpps://www.torredecapdela.org", "adreca": null, "notes_v1": null, "telefon_general": "973663001"}', 'Baixa de la EVA trucar passat setmana Santa', 'research', '[]', 'cap', 'templat', 0, NULL, NULL, NULL, '63e2e3b1-9363-48ac-833d-8b374cad0dc7', '2026-03-16 09:38:34.268009+00', '2026-03-16 10:40:45.889341+00', 'fundador');
INSERT INTO public.municipis_lifecycle (id, nom, comarca, poblacio, geografia, diagnostic_digital, angle_personalitzacio, etapa_actual, historial_etapes, blocker_actual, temperatura, dies_etapa_actual, data_conversio, pla_contractat, estat_final, actor_principal_id, data_creacio, data_ultima_accio, usuari_asignat) VALUES ('78a2343f-dbf5-4707-9e44-5622d03fb5cb', 'Ajuntament Sort', NULL, NULL, 'interior', '{"web": "https://sort.cat/", "adreca": "Carrer del Dr. Carles Pol i Aleu, 13, 25560 Sort", "notes_v1": null, "telefon_general": "973620010"}', 'demo per divendres 27', 'research', '[]', 'cap', 'templat', 0, NULL, NULL, NULL, '1a433539-031d-44ab-82be-baedf1c17811', '2026-03-12 10:59:08.042304+00', '2026-03-16 10:42:10.811+00', 'fundador');


--
-- Data for Name: contactes_v2; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.contactes_v2 (id, municipi_id, nom, carrec, email, telefon, actiu, principal, angles_exitosos, angles_fallits, moment_optimal, to_preferit, data_creacio) VALUES ('779138ee-9918-494a-94ad-2c2de9adb1e2', 'd47fde40-f1d9-4255-8ad2-9813c5fd8f25', 'Eva Perisé ', 'regidor_turisme', 'admin@vallfosca.net', NULL, true, false, '[]', '[]', NULL, 'formal', '2026-03-17 20:06:56.783381+00');
INSERT INTO public.contactes_v2 (id, municipi_id, nom, carrec, email, telefon, actiu, principal, angles_exitosos, angles_fallits, moment_optimal, to_preferit, data_creacio) VALUES ('63e2e3b1-9363-48ac-833d-8b374cad0dc7', 'd47fde40-f1d9-4255-8ad2-9813c5fd8f25', 'Josep Maria Dalmau Gil ', 'alcalde', 'admin@vallfosca.net', NULL, true, true, '[]', '[]', NULL, 'formal', '2026-03-17 20:06:56.783381+00');
INSERT INTO public.contactes_v2 (id, municipi_id, nom, carrec, email, telefon, actiu, principal, angles_exitosos, angles_fallits, moment_optimal, to_preferit, data_creacio) VALUES ('1a433539-031d-44ab-82be-baedf1c17811', '78a2343f-dbf5-4707-9e44-5622d03fb5cb', 'Baldo Farré Serrat ', 'alcalde', 'alcaldia@sort.cat', NULL, true, true, '[]', '[]', NULL, 'formal', '2026-03-17 20:06:56.783381+00');
INSERT INTO public.contactes_v2 (id, municipi_id, nom, carrec, email, telefon, actiu, principal, angles_exitosos, angles_fallits, moment_optimal, to_preferit, data_creacio) VALUES ('00efd101-915b-48dd-bb00-8e09526d8bf1', '78a2343f-dbf5-4707-9e44-5622d03fb5cb', 'Gerard Aguado', 'regidor_turisme', 'turisme@sort.cat', NULL, true, false, '[]', '[]', NULL, 'formal', '2026-03-17 20:06:56.783381+00');
INSERT INTO public.contactes_v2 (id, municipi_id, nom, carrec, email, telefon, actiu, principal, angles_exitosos, angles_fallits, moment_optimal, to_preferit, data_creacio) VALUES ('b5e7c612-dcdc-49ed-9e49-f78edefa741c', 'b0988c73-01e8-4354-94aa-e4c3795511dc', 'Josep Maria Tirbió i Civís ', 'regidor_turisme', 'mia@lapobladesegur.cat', NULL, true, false, '[]', '[]', NULL, 'formal', '2026-03-17 20:06:56.783381+00');
INSERT INTO public.contactes_v2 (id, municipi_id, nom, carrec, email, telefon, actiu, principal, angles_exitosos, angles_fallits, moment_optimal, to_preferit, data_creacio) VALUES ('53983083-7a16-4591-bfba-7a852a4b1d44', 'b0988c73-01e8-4354-94aa-e4c3795511dc', ' Marc Baró i Bernaduca', 'alcalde', 'alcaldia@lapobladesegur.cat', NULL, true, true, '[]', '[]', NULL, 'formal', '2026-03-17 20:06:56.783381+00');
INSERT INTO public.contactes_v2 (id, municipi_id, nom, carrec, email, telefon, actiu, principal, angles_exitosos, angles_fallits, moment_optimal, to_preferit, data_creacio) VALUES ('1e022c62-e440-428e-9550-a107e8e50c12', '76993a09-1cc4-4288-ae93-c2aed91f5278', ' Jordi Alcobé Font', 'altre', 'comu@canillo.ad', '(+376) 751 036', true, false, '[]', '[]', NULL, 'formal', '2026-03-17 20:06:56.783381+00');
INSERT INTO public.contactes_v2 (id, municipi_id, nom, carrec, email, telefon, actiu, principal, angles_exitosos, angles_fallits, moment_optimal, to_preferit, data_creacio) VALUES ('c64e9de5-0919-44a5-8e37-5886359b184f', '76993a09-1cc4-4288-ae93-c2aed91f5278', ' Marc Casal', 'altre', 'turisme@canillo.ad', NULL, true, true, '[]', '[]', NULL, 'formal', '2026-03-17 20:06:56.783381+00');
INSERT INTO public.contactes_v2 (id, municipi_id, nom, carrec, email, telefon, actiu, principal, angles_exitosos, angles_fallits, moment_optimal, to_preferit, data_creacio) VALUES ('d323117a-11e4-448a-badc-9058b3f4bd32', '388104f6-3294-4fa6-9fc0-ebca33eec086', ' Josep Ramon Fondevila Isus ', 'alcalde', 'ajuntament@soriguera.ddl.net', NULL, true, true, '[]', '[]', NULL, 'formal', '2026-03-17 20:06:56.783381+00');
INSERT INTO public.contactes_v2 (id, municipi_id, nom, carrec, email, telefon, actiu, principal, angles_exitosos, angles_fallits, moment_optimal, to_preferit, data_creacio) VALUES ('9a77e835-1d42-42e7-b497-2ede3948f73b', '388104f6-3294-4fa6-9fc0-ebca33eec086', 'Ariadna Vidal', 'altre', 'info@museudecamins.com', NULL, true, false, '[]', '[]', NULL, 'formal', '2026-03-17 20:06:56.783381+00');


--
-- Data for Name: deals; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.deals (id, municipi_id, contacte_id, titol, etapa, valor_setup, valor_llicencia, prioritat, notes_humanes, proper_pas, data_seguiment, data_tancament_prev, data_tancament_real, motiu_perdua, created_at, updated_at) VALUES ('2e5361cc-6f1d-460f-9872-eaa1dd6a3e80', '76993a09-1cc4-4288-ae93-c2aed91f5278', 'c64e9de5-0919-44a5-8e37-5886359b184f', 'Projecte ROURE', 'prospecte', 3500.00, 2500.00, 'mitjana', NULL, 'primer email', NULL, NULL, NULL, NULL, '2026-03-16 11:00:07.729966+00', '2026-03-16 11:00:07.729966+00');
INSERT INTO public.deals (id, municipi_id, contacte_id, titol, etapa, valor_setup, valor_llicencia, prioritat, notes_humanes, proper_pas, data_seguiment, data_tancament_prev, data_tancament_real, motiu_perdua, created_at, updated_at) VALUES ('e4bb29ee-73a3-4cbf-a2cd-9bfb31b0463c', '388104f6-3294-4fa6-9fc0-ebca33eec086', 'd323117a-11e4-448a-badc-9058b3f4bd32', 'Projecte ROURE', 'prospecte', 3500.00, 2500.00, 'mitjana', NULL, NULL, NULL, NULL, NULL, NULL, '2026-03-16 11:43:08.493868+00', '2026-03-16 11:43:08.493868+00');
INSERT INTO public.deals (id, municipi_id, contacte_id, titol, etapa, valor_setup, valor_llicencia, prioritat, notes_humanes, proper_pas, data_seguiment, data_tancament_prev, data_tancament_real, motiu_perdua, created_at, updated_at) VALUES ('b0193e49-c46b-4645-a726-903aad57ab57', 'b0988c73-01e8-4354-94aa-e4c3795511dc', '53983083-7a16-4591-bfba-7a852a4b1d44', 'ROURE5 - Projecte', 'contacte_inicial', 3500.00, 2500.00, 'alta', 'Acabar de perfilar els punts de ruta.', 'demo en persona', '2026-03-26', '2026-04-10', NULL, NULL, '2026-03-10 19:20:32.405688+00', '2026-03-17 20:17:29.107176+00');
INSERT INTO public.deals (id, municipi_id, contacte_id, titol, etapa, valor_setup, valor_llicencia, prioritat, notes_humanes, proper_pas, data_seguiment, data_tancament_prev, data_tancament_real, motiu_perdua, created_at, updated_at) VALUES ('e4345303-303f-4387-91e8-fd7643b7e99c', 'd47fde40-f1d9-4255-8ad2-9813c5fd8f25', '63e2e3b1-9363-48ac-833d-8b374cad0dc7', 'Projecte ROURE', 'prospecte', 3500.00, 2500.00, 'mitjana', 'Enviats segons correus inclos nou contacte Ramon president de Consell Comarcal.
Eva Perise esta de baixa fins el 30/4/26,Contacte amb Sandra de turisme.', 'eva Perise esta de baixa fins el 30/4/26, Rependre contacte.', '2026-04-14', NULL, NULL, NULL, '2026-03-16 09:53:56.01049+00', '2026-03-23 11:47:50.349917+00');
INSERT INTO public.deals (id, municipi_id, contacte_id, titol, etapa, valor_setup, valor_llicencia, prioritat, notes_humanes, proper_pas, data_seguiment, data_tancament_prev, data_tancament_real, motiu_perdua, created_at, updated_at) VALUES ('473f02c9-2b4b-4ad0-acec-751463f60247', '117d35c3-b4c5-406d-a8d4-8cb58393bf52', NULL, 'Projecte ROURE', 'prospecte', 3500.00, 2500.00, 'mitjana', 'fet primer contacte amb la Ariadna', 'enviar segon email', '2026-03-27', '2026-04-30', NULL, NULL, '2026-03-23 10:01:23.677832+00', '2026-03-23 11:48:52.391241+00');
INSERT INTO public.deals (id, municipi_id, contacte_id, titol, etapa, valor_setup, valor_llicencia, prioritat, notes_humanes, proper_pas, data_seguiment, data_tancament_prev, data_tancament_real, motiu_perdua, created_at, updated_at) VALUES ('484e3468-2ed3-4211-8307-15c7b12af329', '5cfe1986-555e-4e28-bc9e-ac500ac0cd4b', 'bca93a14-db52-48b2-b801-041730f1edff', 'Projecte ROURE', 'prospecte', 3500.00, 2500.00, 'mitjana', '', 'segon email', '2026-03-27', '2026-04-30', NULL, NULL, '2026-03-23 10:45:39.600903+00', '2026-03-23 11:50:47.202115+00');
INSERT INTO public.deals (id, municipi_id, contacte_id, titol, etapa, valor_setup, valor_llicencia, prioritat, notes_humanes, proper_pas, data_seguiment, data_tancament_prev, data_tancament_real, motiu_perdua, created_at, updated_at) VALUES ('d427d8a7-b977-44dc-ad40-dff00d37da3e', '78a2343f-dbf5-4707-9e44-5622d03fb5cb', '1a433539-031d-44ab-82be-baedf1c17811', 'Projecte ROURE', 'contacte_inicial', 3500.00, 2500.00, 'mitjana', 'Contacte telefonic amb en gerard, enviament correu a Pere Bascones. mPreparar demo per divendres 27/3', 'trucar en Pere', '2026-03-24', '2026-03-16', NULL, NULL, '2026-03-12 11:05:27.943955+00', '2026-03-23 15:30:53.222816+00');


--
-- Data for Name: deal_activitats; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.deal_activitats (id, deal_id, tipus, descripcio, valor_anterior, valor_nou, created_at) VALUES ('3357f9b4-91bb-4a05-a331-9ebe57771272', 'b0193e49-c46b-4645-a726-903aad57ab57', 'canvi_etapa', 'Canvi d''etapa: de ''prospecte'' a ''contacte_inicial''', 'prospecte', 'contacte_inicial', '2026-03-11 13:34:12.424418+00');
INSERT INTO public.deal_activitats (id, deal_id, tipus, descripcio, valor_anterior, valor_nou, created_at) VALUES ('77aa4b18-b989-411b-858a-0489da173b1f', 'd427d8a7-b977-44dc-ad40-dff00d37da3e', 'canvi_etapa', 'Canvi d''etapa: de ''prospecte'' a ''contacte_inicial''', 'prospecte', 'contacte_inicial', '2026-03-12 11:07:30.076979+00');
INSERT INTO public.deal_activitats (id, deal_id, tipus, descripcio, valor_anterior, valor_nou, created_at) VALUES ('6a16fce5-a47c-4657-b7b7-1497a3a058f5', 'd427d8a7-b977-44dc-ad40-dff00d37da3e', 'canvi_etapa', 'Canvi d''etapa: de ''contacte_inicial'' a ''prospecte''', 'contacte_inicial', 'prospecte', '2026-03-12 11:07:31.422685+00');
INSERT INTO public.deal_activitats (id, deal_id, tipus, descripcio, valor_anterior, valor_nou, created_at) VALUES ('1d1f6f4d-3cd3-406c-9c26-f27cd355cac4', 'b0193e49-c46b-4645-a726-903aad57ab57', 'canvi_etapa', 'Canvi d''etapa: de ''contacte_inicial'' a ''prospecte''', 'contacte_inicial', 'prospecte', '2026-03-12 11:07:38.795705+00');
INSERT INTO public.deal_activitats (id, deal_id, tipus, descripcio, valor_anterior, valor_nou, created_at) VALUES ('94231caa-675b-41e6-8813-198801db3dd4', 'b0193e49-c46b-4645-a726-903aad57ab57', 'canvi_etapa', 'Canvi d''etapa: de ''prospecte'' a ''proposta_enviada''', 'prospecte', 'proposta_enviada', '2026-03-16 15:40:05.32869+00');
INSERT INTO public.deal_activitats (id, deal_id, tipus, descripcio, valor_anterior, valor_nou, created_at) VALUES ('17565775-00df-40f3-b7d1-e43906a22438', 'b0193e49-c46b-4645-a726-903aad57ab57', 'canvi_etapa', 'Canvi d''etapa: de ''proposta_enviada'' a ''demo_feta''', 'proposta_enviada', 'demo_feta', '2026-03-16 15:40:09.089593+00');
INSERT INTO public.deal_activitats (id, deal_id, tipus, descripcio, valor_anterior, valor_nou, created_at) VALUES ('dbe93503-fcff-474c-80ca-1e8a1a59ee92', 'b0193e49-c46b-4645-a726-903aad57ab57', 'canvi_etapa', 'Canvi d''etapa: de ''demo_feta'' a ''prospecte''', 'demo_feta', 'prospecte', '2026-03-16 15:40:11.94375+00');
INSERT INTO public.deal_activitats (id, deal_id, tipus, descripcio, valor_anterior, valor_nou, created_at) VALUES ('729c0541-c984-4dbd-9daa-06d4c279dfc1', 'b0193e49-c46b-4645-a726-903aad57ab57', 'canvi_etapa', 'Canvi d''etapa: de ''prospecte'' a ''contacte_inicial''', 'prospecte', 'contacte_inicial', '2026-03-16 15:44:16.887268+00');
INSERT INTO public.deal_activitats (id, deal_id, tipus, descripcio, valor_anterior, valor_nou, created_at) VALUES ('68614cc4-2a7e-4c47-8dc4-9c34a56c5015', '484e3468-2ed3-4211-8307-15c7b12af329', 'email_enviat', 'Email enviat: Sobre el relat digital del patrimoni del Pont de Suert', NULL, NULL, '2026-03-23 10:52:32.679755+00');
INSERT INTO public.deal_activitats (id, deal_id, tipus, descripcio, valor_anterior, valor_nou, created_at) VALUES ('6805d227-9faa-4a1e-be9e-931c1b25d927', 'd427d8a7-b977-44dc-ad40-dff00d37da3e', 'canvi_etapa', 'Canvi d''etapa: de ''prospecte'' a ''contacte_inicial''', 'prospecte', 'contacte_inicial', '2026-03-23 12:00:03.056521+00');


--
-- Data for Name: emails_v2; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: email_drafts_v2; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.email_drafts_v2 (id, municipi_id, contacte_id, estat, subject, cos, generat_per_ia, prompt_utilitzat, variants_generades, variant_seleccionada, editat_per_usuari, canvis_respecte_ia, data_enviament, enviat_des_de, email_enviat_id, data_creacio) VALUES ('b396d2db-ce40-4056-bfcc-57c7b666d501', 'b0988c73-01e8-4354-94aa-e4c3795511dc', NULL, 'esborrany', 'La Pobla, el relat que el món llegirà', 'Alcalde,

Vostè ha fet de la Pobla un far de futur; ara cal que el relat sigui seu. Si el municipi no controla la seva veu digital, altres ho faran per vostè.

Imagini’s un turista que busca "Pobla de Segur" i troba una història que vostè no ha escrit. Això es vota.

Té 10 minuts demà per decidir qui narra el seu llegat?

Respon SÍ i li explico com.', true, '
Actuant per a: Alcalde (Visionari). Vol llegat, visibilitat, guanyar eleccions.
Missatge-clau: sobirania digital, control del relat, "el teu municipi al mapa".
Regles: Mai funcionalitats tècniques. Sempre impacte polític i territorial.
To: proximitat, "tu", company de trinxera.


Situació: Primer contacte. Ganxo patrimoni/digitalització específic.
Regles: Màxim 120 paraules. Zero enllaços. Zero emojis.
Estructura: Ganxo personalitzat -> Dolor subtil -> CTA binari.
', '[{"cos": "Alcalde,\n\nVostè ha fet de la Pobla un far de futur; ara cal que el relat sigui seu. Si el municipi no controla la seva veu digital, altres ho faran per vostè.\n\nImagini’s un turista que busca \"Pobla de Segur\" i troba una història que vostè no ha escrit. Això es vota.\n\nTé 10 minuts demà per decidir qui narra el seu llegat?\n\nRespon SÍ i li explico com.", "angle": "sobirania narrativa", "score": 0.92, "subject": "La Pobla, el relat que el món llegirà"}, {"cos": "Et parla el veí de trenta minuts que vol veure el teu poble protagonista.\n\nMentre altres ajuntaments es gasten el pressupost en plataformes que no controlen, la Pobla pot ser el primer municipi de la Vall que tingui titularitat plena de la seva televisió, ràdio i xarxes. Imagina decidir quina imatge surt a l’informatiu, quins projectes es viralitzen i quins emprenedors locals ocupen portada.\n\nAquest setembre estem ajudant tres alcaldes a fer-ho sense tocar el pressupost. T’apuntes a la conversa?\n\nRespon sí o sí i et truco demà al matí.", "angle": "Lideratge territorial", "score": 0.92, "subject": "Pobla de Segur pot liderar la Catalunya digital"}, {"cos": "Com alcalde, tens el repte de deixar empremta i que el teu poble no sigui una marca blanca al mapa quan et jubilis. La majoria de municipis depenen d’empreses fora del territori per decidir quan i com es parla d’ells: notícies a mitjans aliens, dades a la prestatgeria d’un despatx de Barcelona.\n\nAmb el projecte Sobirania Digital pots convertir Pobla de Segur en referent: tu ordines la narrativa, tu esculls què es publica i quan, i acabes legislatura amb la cartera d’actius digitals que et recordarà fins i tot l’oposició.\n\nVols que et prepari la proposta pilot per al teu pròxim plenari? Et truco demà al matí?", "angle": "Llegat digital i control del relat", "score": 0.87, "subject": "Pobla de Segur, tens l’oportunitat de pilotar la sobirania digital"}]', 0, false, '{}', NULL, NULL, NULL, '2026-03-17 20:51:55.138594+00');
INSERT INTO public.email_drafts_v2 (id, municipi_id, contacte_id, estat, subject, cos, generat_per_ia, prompt_utilitzat, variants_generades, variant_seleccionada, editat_per_usuari, canvis_respecte_ia, data_enviament, enviat_des_de, email_enviat_id, data_creacio) VALUES ('8bca3f64-2cc6-4baa-a532-91b3ceab335a', 'b0988c73-01e8-4354-94aa-e4c3795511dc', '53983083-7a16-4591-bfba-7a852a4b1d44', 'esborrany', 'Marc: convertim la Pobla en referent de sobirania digital', 'Marc, 

Avui és dia de posar la Pobla de Segur al mapa i no només de paraula. Imagina controlar tu, des d’aquí, l’impacte que sortim als mitjans, la reputació digital de la Pobla i la narrativa que marcarà el teu llegat. 

Vull proposar-te una estratègia que converteixi la teva gestió en exemple per la resta del territori i et doni arma electoral clara per al 2027. 

15 minuts aquesta setmana n’hi ha prou? 

Si vols, dimarts o dimecres al matí?', true, '
Actuant per a: Alcalde (Visionari). Vol llegat, visibilitat, guanyar eleccions.
Missatge-clau: sobirania digital, control del relat, "el teu municipi al mapa".
Regles: Mai funcionalitats tècniques. Sempre impacte polític i territorial.
To: proximitat, "tu", company de trinxera.


Situació: Primer contacte. Ganxo patrimoni/digitalització específic.
Regles: Màxim 120 paraules. Zero enllaços. Zero emojis.
Estructura: Ganxo personalitzat -> Dolor subtil -> CTA binari.
', '[{"cos": "Marc,\n\nHe vist com defensa el teu llegat patrimonial a les xarxes. Imagina que el teu municipi no només el preserva, sinó que el projecta com a referent digital de tot el país.\n\nEls rivals polítics ja controlen el relat online. Tu tens 18 mesos per decidir si la Pobla lidera o segueix.\n\nEt sona si parlem 10 minuts demà al matí?\n\nSalut,\n\nJoan", "angle": "Lideratge digital urgent", "score": 0.87, "subject": "Marc, Pobla de Segur pot liderar la Catalunya digital"}, {"cos": "Marc, he vist com has convertit la Pobla en referent de turisme sostenible. Però on és la veu del teu municipi quan TV3 parla del territori? \n\nEls grans mitjans acaben decidint la narrativa del Pallars Jussà. I tu, que has lluitat per fer visible la Pobla, et mereixes controlar el relat.\n\nEt proposo un cafè a la plaça Major per mostrar-te com podem garantir que la Pobla lideri la conversa digital del territori. \n\nDijous a les 10h et va bé?", "angle": "Control narratiu territorial", "score": 0.85, "subject": "Marc, vull compartir-te una idea que podria posar la Pobla al centre del debat nacional"}, {"cos": "Marc, \n\nAvui és dia de posar la Pobla de Segur al mapa i no només de paraula. Imagina controlar tu, des d’aquí, l’impacte que sortim als mitjans, la reputació digital de la Pobla i la narrativa que marcarà el teu llegat. \n\nVull proposar-te una estratègia que converteixi la teva gestió en exemple per la resta del territori i et doni arma electoral clara per al 2027. \n\n15 minuts aquesta setmana n’hi ha prou? \n\nSi vols, dimarts o dimecres al matí?", "angle": "ganxo èpic + CTA binari zero ficció", "score": 0.93, "subject": "Marc: convertim la Pobla en referent de sobirania digital"}]', 2, false, '{}', NULL, NULL, NULL, '2026-03-17 21:09:28.105524+00');
INSERT INTO public.email_drafts_v2 (id, municipi_id, contacte_id, estat, subject, cos, generat_per_ia, prompt_utilitzat, variants_generades, variant_seleccionada, editat_per_usuari, canvis_respecte_ia, data_enviament, enviat_des_de, email_enviat_id, data_creacio) VALUES ('8be05460-6f21-4991-884a-413e771f5d79', 'b0988c73-01e8-4354-94aa-e4c3795511dc', '53983083-7a16-4591-bfba-7a852a4b1d44', 'esborrany', 'Marc, volem posar Pobla de Segur al mapa d’èxits digitals', 'Ets de pobla i m’agrada parlar-te com a company: el teu llegat es juga ara. Si algú fora controla el relat del que passa al nostre territori, perdem vots i inversió. Però si tu tens la sobirania digital, la Pobla guanya visibilitat, tu guanyes eleccions.

Vols que parlem 15 minuts? Sí o no.', true, '
Actuant per a: Alcalde (Visionari). Vol llegat, visibilitat, guanyar eleccions.
Missatge-clau: sobirania digital, control del relat, "el teu municipi al mapa".
Regles: Mai funcionalitats tècniques. Sempre impacte polític i territorial.
To: proximitat, "tu", company de trinxera.


Situació: Primer contacte. Ganxo patrimoni/digitalització específic.
Regles: Màxim 120 paraules. Zero enllaços. Zero emojis.
Estructura: Ganxo personalitzat -> Dolor subtil -> CTA binari.
', '[{"cos": "Ets l’alcalde que pot posar la Pobla de Segur al centre del mapa de la sobirania digital del país.\n\nMentre d’altres esperen subvencions, els municipis que ja han dit \"sí\" controlen el relat del seu territori: decideixen què es explica i com, i ho fan des d’una plataforma que és seva, no d’un proveïdor exterior. Guanyen visibilitat, atrauen inversions i deixen empremta per a les pròximes generacions.\n\nEt proposo 15 minuts per mostrar-te com la Pobla pot ser el proper cas d’èxit. Dijous o divendres t’aniria bé?", "angle": "Sobirania digital = llegat electoral", "score": 0.92, "subject": "Marc, el teu poble pot liderar la Catalunya digital"}, {"cos": "Marc, quan algú cerca la Pobla, ¿qui controla el que surt? Si ara mateix el relat és Google o la premsa de fora, perds sobirania sobre el territori que has fet créixer.\n\nL’alcalde que converteix el seu municipi en referent digital marca el seu llegat. Et proposo 15 minuts per dibuixar com la teva Pobla pot ser l’exemple que tots copiïn.\n\nPuc comptar amb tu demà a les 10 o a les 4?", "angle": "Ganxo llegat digital i control del relat per alcalde visionari", "score": 0.93, "subject": "Marc, Pobla de Segur pot liderar el relat digital de la Catalunya interior"}, {"cos": "Ets de pobla i m’agrada parlar-te com a company: el teu llegat es juga ara. Si algú fora controla el relat del que passa al nostre territori, perdem vots i inversió. Però si tu tens la sobirania digital, la Pobla guanya visibilitat, tu guanyes eleccions.\n\nVols que parlem 15 minuts? Sí o no.", "angle": "sobirania digital = vots", "score": 0.94, "subject": "Marc, volem posar Pobla de Segur al mapa d’èxits digitals"}]', 2, false, '{}', NULL, NULL, NULL, '2026-03-17 21:09:27.17254+00');


--
-- Data for Name: email_sequencies_v2; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: emails; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('31f06037-3ede-4deb-b924-46876903079a', 'b0193e49-c46b-4645-a726-903aad57ab57', 'b5e7c612-dcdc-49ed-9e49-f78edefa741c', NULL, 'miquel@projectexinoxano.cat', 'mia@lapobladesegur.cat', ' La feina de turisme a La Pobla (li acabo de comentar al Marc)', 'Hola Josep Maria,
Soc Miquel Utge, de Sort.  Li acabo d''enviar un correu al Marc Baró comentant-li una idea estratègica per recuperar el control digital de La Pobla, però sé perfectament que el dia a dia, les hores de feina i el pes de la promoció turística recauen sobre tu i el teu equip.
Sé la feinada que suposa documentar, mantenir viu i promocionar un patrimoni com el de la baixada dels Raiers, les Falles o el Molí de l''Oli. El problema frustrant que estem veient a molts ajuntaments és que, després de tota la vostra feina de recerca i creació de materials, quan el turista baixa del Tren dels Llacs obre Google Maps i és l''algoritme qui decideix com se li explica el poble. Treballeu a cegues perquè ells es queden les dades.
Hem creat una eina precisament per treure-us aquesta càrrega de feina i fer que el vostre esforç llueixi, recuperant el control. La nostra IA agafa el material històric i els fulletons que ja teniu fets, i us estructura rutes i audioguies web interactives en 15 minuts.
Però el més important per al teu dia a dia: la plataforma us genera automàticament informes completíssims amb mapes de calor. Per fi podreu veure de forma visual per quins carrers es mouen exactament els visitants, quant de temps es paren davant de cada actiu i entendre el seu comportament real per justificar qualsevol acció de turisme.
Perquè vegis que no és teoria, he recollit documentació històrica sobre els Raiers i he preparat una petita maqueta immersiva on podràs veure com donem vida al vostre fons documental i com es recullen aquestes dades.
Com ho tens per buscar un forat de 10 minuts la setmana entrant i t''ho ensenyo? Sense cap compromís.
Una abraçada,
Miquel Utge
622836542', 'OUT', true, true, NULL, '2026-03-11 14:32:46.834563+00', '2026-03-11 13:32:46.837388+00', '59b95c3e60ec44919f4a49c823d637c0', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('750311af-f48c-46f9-b7d9-ddb93cabf3a9', 'b0193e49-c46b-4645-a726-903aad57ab57', '53983083-7a16-4591-bfba-7a852a4b1d44', NULL, 'miquel@projectexinoxano.cat', 'alcaldia@lapobladesegur.cat', ' La història de La Pobla a internet (i qui se''n queda les dades)', 'Hola Marc,
Soc Miquel Utge, de Sort. T''escric perquè estem parlant amb diversos ajuntaments que han decidit dir prou a una situació molt frustrant: fer un gran esforç econòmic per mantenir el patrimoni, però dependre totalment de Google Maps i TripAdvisor perquè els visitants el descobreixin.

A La Pobla de Segur teniu un llegat impressionant. Amb la memòria viva de l''ofici als voltants del Museu dels Raiers o la conservació d''espais com el Molí de l''Oli de Sant Josep, heu fet una gran feina de protecció cultural. Però quan el visitant camina pels vostres carrers i obre el mòbil, qui li explica aquesta història? Ara mateix és l''algoritme qui decideix què veuen, i totes les dades d''aquests turistes se les queden les grans plataformes, no l''Ajuntament.

A Projecte xino-xano hem creat una infraestructura pensada justament per a consistoris com el vostre per recuperar aquesta sobirania digital territorial. Sense desenvolupaments complexos: amb la simple introducció de material històric, cultural o natural del vostre arxiu municipal, la nostra tecnologia estructura i prepara rutes interactives i audioguies web en qüestió de minuts. Donem vida al vostre fons documental. Així, el relat oficial el controleu vosaltres i les dades d''ús es queden a La Pobla.

He recollit documentació històrica sobre la baixada dels raiers i he muntat una petita maqueta perquè vegis com quedaria aquesta experiència immersiva, 100% pròpia i controlada per vosaltres.

Com ho tens per buscar un forat de 10 minuts la setmana entrant i t''ho ensenyo? Sense cap compromís, només perquè vegis com funciona.

Una abraçada,
Miquel
622836542', 'OUT', true, true, NULL, '2026-03-11 14:29:31.406931+00', '2026-03-11 13:29:31.410442+00', '12712398383944308ba0093d52c88c48', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('098c5ed9-beb9-43f6-89fa-651084631c5c', 'd427d8a7-b977-44dc-ad40-dff00d37da3e', '1a433539-031d-44ab-82be-baedf1c17811', NULL, 'miquel@projectexinoxano.cat', 'alcaldia@sort.cat', 'El Castell de Sort a Google / Sobirania territorial', 'Hola Baldo,

He vist la bona feina que feu a Sort defensant un model que posa en valor la memòria històrica, com el Castell i la Presó-Museu, i que va molt més enllà del turisme d''estiu.

Però passa una cosa que veiem sovint: l''Ajuntament inverteix a mantenir aquest patrimoni, però quan el visitant hi arriba, qui li explica el poble és l''algoritme de Google. Ells decideixen què es veu i ells es queden les dades de la vostra gent. Sort posa la feina, ells s''emporten l''or.

Hem creat una infraestructura digital sobirana que evita això. La nostra IA agafa els vostres PDFs actuals i crea audioguies 100% vostres en 15 minuts. Com a capital del Pallars, Sort hauria de liderar aquest canvi.

He fet una prova ràpida amb el PDF de la Vila Closa de Sort. Tens 10 minuts dimarts o dijous al matí per veure-ho funcionant?

Una abraçada,

Miquel Utge
Projecte Xino Xano
Sobirania Digital Territorial', 'OUT', true, true, NULL, '2026-03-12 12:04:36.130699+00', '2026-03-12 11:04:39.229483+00', '3685337ae8144db5bd4b9e3ea7ca45e7', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('e375def5-4a9c-4a18-861a-636c984b45c8', 'b0193e49-c46b-4645-a726-903aad57ab57', '53983083-7a16-4591-bfba-7a852a4b1d44', NULL, 'miquel@projectexinoxano.cat', 'alcaldia@lapobladesegur.cat', 'Sobre la Casa Mauri i els fons Next Generation', 'Hola, Marc,

Et recupero el fil de la setmana passada. He estat analitzant el projecte de turisme sostenible que esteu executant amb els fons NextGen i m’ha sorprès la qualitat del fons documental que teniu a La Pobla, especialment sobre el Conjunt Modernista de la Casa Mauri.

T’escric perquè sovint el problema d''aquestes inversions és que es gasta molt en infraestructura física, però el relat digital queda en mans de tercers. Amb la nostra IA implementada dintre del projecte xino-xano, hem fet una prova interna: hem agafat el vostre fulletó PDF i el sistema l’ha convertit en una audioguia immersiva en menys de 15 minuts.

Això et permet dues coses clau com a alcalde:

Rendibilitat real: No cal contractar agències per fer continguts nous; aprofitem el que ja teniu.
Control polític: El nom de "La Pobla de Segur" és el que brilla, no el d''una multinacional americana.

Com ho tens per fer un cafè de 10 minuts un matí d''aquesta setmana? T’ensenyaré la maqueta que hem preparat amb el vostre material real.

Una abraçada,
Miquel Utge
622836542

Projecte Xino Xano

', 'OUT', true, true, NULL, '2026-03-16 10:29:50.680712+00', '2026-03-16 09:29:58.648991+00', 'd2f5782c73a34d2381cb93d557be4d1b', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('af9976cf-e48b-4597-8b0b-427f3b719ff5', 'b0193e49-c46b-4645-a726-903aad57ab57', 'b5e7c612-dcdc-49ed-9e49-f78edefa741c', NULL, 'miquel@projectexinoxano.cat', 'mia@lapobladesegur.cat', 'Una eina per entendre què fan els turistes quan baixen del tren', 'Hola, Josep Maria,

Espero que la setmana hagi començat bé. T’escric perquè sé que un dels reptes que teniu és mesurar l''impacte real dels visitants que arriben amb el Tren dels Llacs un cop es dispersen pel poble.

A Projecte xino-xano no només digitalitzem el patrimoni (com la baixada dels Raiers o el Molí de l''Oli); el que fem és donar-te dades. La nostra plataforma genera automàticament mapes de calor. Per fi podràs veure, amb dades reals i anònimes:

Quins carrers trepitgen realment.
On es detenen més temps.
Quin contingut els interessa i quins ignoren.
Així com els emails dels usuaris registrats per posteriors campanyes d''email màrqueting.

És el fi de la "pàgina en blanc". Tu puges el material que ja tens i la infraestructura s’encarrega de la resta, lliurant-te informes que et serviran per justificar qualsevol inversió futura davant de l''ajuntament o la diputació.

T’agradaria veure com funcionen aquests informes amb una demo de 10 minuts? Et podria anar bé un matí  de dimarts a dijous?

Salut,
Miquel Utge
622836542

Projecte Xino Xano

', 'OUT', true, true, NULL, '2026-03-16 10:34:42.197239+00', '2026-03-16 09:34:50.182815+00', '037341009d134f289e63627b100519f2', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('ee198ee0-0a40-4d59-8eb1-20b1a0459c6f', 'e4345303-303f-4387-91e8-fd7643b7e99c', '63e2e3b1-9363-48ac-833d-8b374cad0dc7', NULL, 'miquel@projectexinoxano.cat', 'admin@vallfosca.net', 'Att: Josep Maria Dalmau;  La recuperació de l''Hospital de Cartró i el monopoli de Google', 'Hola, Josep Maria,

 He vist l''esforç tan bèstia que esteu fent des de l''Ajuntament per protegir i consolidar l''històric Hospital de cartó a Torre de Capdella. Heu fet molt bona feina protegint el legat físic de la Vall Fosca. Però analitzant la vall, hi ha una cosa que fa mal: quan el turista arriba al Telefèric o a la Central, qui li explica el poble? L''algoritme de Google Maps o rutes no oficials a Wikiloc. L''Ajuntament posa la feina i les inversions, però Silicon Valey s''emporta l''or (les dades i l''atenció) i decideix el que els visitants veuen. A Projecte Xino-Xano,  estem ajudant els municipis pirinencs, com ja hem fet amb el pilot del Palars Sobirà, a recuperar aquesta sobirania. Construïm infraestructura digital perquè tingueu l''audioguia oficial de la vall activada per GPS, sense embrutar el paisatge amb QRs i recuperant el 100% de les dades dels turistes. 

M''agradaria ensenyar-te com quedaria la Val Fosca amb sobirania total. 
Tens un matí lliure aquesta setmana de dimarts a dijous?

Salut
Miquel Utge
622836542

Projecte xino-xano', 'OUT', true, true, NULL, '2026-03-16 11:11:59.84569+00', '2026-03-16 10:12:07.948776+00', '7e5dbe389e1e43a0b0f6d2c46215c533', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('7da7a4a3-e55e-4bff-9954-79959686b66f', 'e4345303-303f-4387-91e8-fd7643b7e99c', '779138ee-9918-494a-94ad-2c2de9adb1e2', NULL, 'miquel@projectexinoxano.cat', 'ajuntament@torredecapdella.ddl.net', 'Att: Eva Perisé;  Les rutes de la Val Fosca a Wikiloc vs. el relat del Museu', 'Hola, Eva, 

Segueixo de prop la feina immensa de documentació i difusió que feu des del Museu Hidroelèctric. Sou un referent a tot el Pirineu. 

El motiu del correu és que veig a internet com molts turistes, un cop baixen del Telefèric, acaben guiats per ressenyes desordenades de Google o rutes de Wikiloc que no reflecteixen la precisió ni el relat del vostre arxiu. 

A Projecte xino-xano hem desenvolupat la IA Punt d''Or. Bàsicament, li passes un PDF o un tríptic dels que ja teniu publicats a vallfosca.net i, en 15 minuts, et genera una audioguia completa i geolocalitzada, sense que hagis de picar ni una línia de text. Estalvi de temps absolut i, sobretot, el domini i les dades són de l''Ajuntament, no d''una plataforma de tercers. He fet una prova ràpida amb la ruta de l''Antic Carrilet per veure l''efecte que fa.

Quan tens 10 minuts perquè t''ho ensenyi per videotrucada?, un matí de dimarts a dijous?, cap a les 11?

Una abraçada, 
Miquel Utge
622836542

Projecte xino-xano', 'OUT', true, true, NULL, '2026-03-16 11:00:01.966954+00', '2026-03-16 10:00:10.02811+00', 'b43fece1a1d14d6fb26f47a6cbb021c8', true, '2026-03-16 11:04:50.220251+00', 1, '127.0.0.1');
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('7794d463-211a-496b-b011-cde4da9c800a', 'd427d8a7-b977-44dc-ad40-dff00d37da3e', '00efd101-915b-48dd-bb00-8e09526d8bf1', NULL, 'miquel@projectexinoxano.cat', 'turisme@sort.ca', 'Els PDFs de la Val d''Àssua i el Batliu / Sobirania a Sort', 'Hola, Gerard, 

He vist l''esforç brutal que feu des de turisme i Sobirà Dinàmic amb les rutes locals. 

Teniu un contingut fantàstic als itineraris del Batliu i la Vall  d''Àssua. Heu fet molt bona feina amb el patrimoni. El problema que estem veient a altres municipis és que l''Ajuntament posa tot l''esforç de creació, però quan el turista arriba a la plaça, qui li explica el poble és l''algoritme de Google Maps. I els que es queden totes les dades.

Hem desenvolupat una IA que llegeix els vostres propis PDF municipals i els converteix en audioguies interactives i sobiranes en 15 minuts. Sense argot tècnic ni carregar-te de més feina. He fet una prova ràpida amb el vostre tríptic de la Vila Closa. Tens 10 minuts dimecres al matí i te l''ensenyo? 

Una abraçada,
Miquel Utge
622836542

Projecte xino-xano', 'OUT', true, true, NULL, '2026-03-16 11:04:13.9228+00', '2026-03-16 10:04:21.997017+00', '4a20de99b6314938b58b04a88025e6a2', true, '2026-03-16 11:09:49.221533+00', 1, '127.0.0.1');
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('0fbe33a7-436e-4f4a-a81d-67e493fb8d4f', 'e4345303-303f-4387-91e8-fd7643b7e99c', '63e2e3b1-9363-48ac-833d-8b374cad0dc7', NULL, 'miquel@projectexinoxano.cat', 'jmdalmau@torrecapdella.cat', 'L''Hospital de cartó i el monopoli de Google a la Vall Fosca', 'Hola, Josep Maria,

Heu fet molt bona feina protegint el llegat físic de la Vall Fosca, com l''esforç brutal per consolidar l''històric Hospital de cartó a la Torre de Capdella.

Però hi ha una cosa que fa mal: quan el turista arriba al Telefèric, qui li explica el poble? L''algoritme de Google Maps o Wikiloc. L''Ajuntament posa la inversió i la feina, però Silicon Valley s''emporta les dades i decideix què veuen els visitants.

A Projecte Xino Xano estem ajudant els municipis a recuperar aquesta sobirania, com ja hem fet al Pallars Sobirà. Construïm infraestructura digital pròpia perquè tingueu l''audioguia oficial de la vall, sense embrutar el paisatge i recuperant el 100% de les dades.

M''agradaria ensenyar-te com queda el mapa de la Vall Fosca amb sobirania total. El dimarts o el dimecres a les 11h et va bé?

Salut,

Miquel Utge
622836542
Projecte Xino Xano', 'OUT', true, true, NULL, '2026-03-20 12:57:19.125293+00', '2026-03-20 11:57:19.370787+00', '3e3ef47585f34d77af805870f7e6b35d', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('c30df720-8ea6-4a5f-ae7c-5dbd85dfa311', 'e4345303-303f-4387-91e8-fd7643b7e99c', '63e2e3b1-9363-48ac-833d-8b374cad0dc7', NULL, 'miquel@projectexinoxano.cat', 'ajuntament@torredecapdella.ddl.net', 'Att: Josep Maria Dalmau; La recuperació de l''Hospital de Cartró i el monopoli de Google', 'Hola, Josep Maria,

 He vist l''esforç tan bèstia que esteu fent des de l''Ajuntament per protegir i consolidar l''històric Hospital de cartó a Torre de Capdella. Heu fet molt bona feina protegint el legat físic de la Vall Fosca. Però analitzant la vall, hi ha una cosa que fa mal: quan el turista arriba al Telefèric o a la Central, qui li explica el poble? L''algoritme de Google Maps o rutes no oficials a Wikiloc. L''Ajuntament posa la feina i les inversions, però Silicon Valey s''emporta l''or (les dades i l''atenció) i decideix el que els visitants veuen. A Projecte Xino-Xano,  estem ajudant els municipis pirinencs, com ja hem fet amb el pilot del Palars Sobirà, a recuperar aquesta sobirania. Construïm infraestructura digital perquè tingueu l''audioguia oficial de la vall activada per GPS, sense embrutar el paisatge amb QRs i recuperant el 100% de les dades dels turistes. 

M''agradaria ensenyar-te com quedaria la Val Fosca amb sobirania total. 
Tens un matí lliure aquesta setmana de dimarts a dijous?

Salut
Miquel Utge
622836542

Projecte xino-xano', 'OUT', true, true, NULL, '2026-03-16 10:52:57.452368+00', '2026-03-16 09:53:05.48884+00', '5c8f810728f54b2fa7fa4e7c24098306', true, '2026-03-16 11:10:16.274919+00', 1, '127.0.0.1');
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('85f49cf2-7443-44d7-9a44-2defafdcbb15', 'd427d8a7-b977-44dc-ad40-dff00d37da3e', '00efd101-915b-48dd-bb00-8e09526d8bf1', NULL, 'miquel@projectexinoxano.cat', 'turisme@sort.cat', 'Sobirania a Sort', 'Hola, Gerard, 

He vist l''esforç brutal que feu des de turisme i Sobirà Dinàmic amb les rutes locals. 

Teniu un contingut fantàstic als itineraris del Batliu i la Vall  d''Àssua. Heu fet molt bona feina amb el patrimoni. El problema que estem veient a altres municipis és que l''Ajuntament posa tot l''esforç de creació, però quan el turista arriba a la plaça, qui li explica el poble és l''algoritme de Google Maps. I els que es queden totes les dades.

Hem desenvolupat una IA que llegeix els vostres propis PDF municipals i els converteix en audioguies interactives i sobiranes en 15 minuts. Sense argot tècnic ni carregar-te de més feina. He fet una prova ràpida amb el vostre tríptic de la Vila Closa. Tens 10 minuts dimecres al matí i te l''ensenyo? 

Una abraçada,
Miquel Utge
622836542

Projecte xino-xano', 'OUT', true, true, NULL, '2026-03-16 11:14:31.777948+00', '2026-03-16 10:14:39.880123+00', '4b1d28385da14112937062b68420f09c', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('bb25eed9-c459-4d12-aee4-502d8dc9863c', 'e4345303-303f-4387-91e8-fd7643b7e99c', '779138ee-9918-494a-94ad-2c2de9adb1e2', NULL, 'miquel@projectexinoxano.cat', 'admin@vallfosca.net', 'Att: Eva Perisé;  Les rutes de la Val Fosca a Wikiloc vs. el relat del Museu', 'Hola, Eva, 

Segueixo de prop la feina immensa de documentació i difusió que feu des del Museu Hidroelèctric. Sou un referent a tot el Pirineu. 

El motiu del correu és que veig a internet com molts turistes, un cop baixen del Telefèric, acaben guiats per ressenyes desordenades de Google o rutes de Wikiloc que no reflecteixen la precisió ni el relat del vostre arxiu. 

A Projecte xino-xano hem desenvolupat la IA Punt d''Or. Bàsicament, li passes un PDF o un tríptic dels que ja teniu publicats a vallfosca.net i, en 15 minuts, et genera una audioguia completa i geolocalitzada, sense que hagis de picar ni una línia de text. Estalvi de temps absolut i, sobretot, el domini i les dades són de l''Ajuntament, no d''una plataforma de tercers. He fet una prova ràpida amb la ruta de l''Antic Carrilet per veure l''efecte que fa.

Quan tens 10 minuts perquè t''ho ensenyi per videotrucada?, un matí de dimarts a dijous?, cap a les 11?

Una abraçada, 
Miquel Utge
622836542

Projecte xino-xano', 'OUT', true, true, NULL, '2026-03-16 11:13:27.40949+00', '2026-03-16 10:13:35.508018+00', '9bc6e7acd9e041ab8aa6e1c69247cdc0', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('fda09688-dba4-426a-8543-b5ece0063d19', '2e5361cc-6f1d-460f-9872-eaa1dd6a3e80', 'c64e9de5-0919-44a5-8e37-5886359b184f', NULL, 'miquel@projectexinoxano.cat', 'turisme@canillo.ad', 'Marc, he passat el vostre PDF de senderisme a audioguia interactiva', 'Hola Marc,

T''escric perquè he estat consultant el portal Visit Canillo i m''ha semblat que la feina de continguts que teniu feta a les guies de senderisme és excel·lent. Tot i això, sé que per al turista actual, descarregar-se un PDF de 5MB i haver de fer zoom amb els dits per llegir sobre el Santuari de Meritxell o la Vall de l''Incles mentre camina, acaba generant una fricció que fa que molta d''aquesta informació es perdi.

He volgut fer una prova de concepte rigorosa amb el vostre material: he agafat el vostre PDF oficial i l''he processat amb la nostra IA Punt d''Or. En menys de 20 minuts, el sistema ha extret els punts d''interès i ha generat una maqueta d''audioguia geolocalitzada, amb la imatge de Canillo i sense que el visitant hagi de descarregar cap aplicació.

La meva intenció no és qüestionar la vostra metodologia, sinó ensenyar-te com la tecnologia de Projecte Xino Xano (PXX) pot automatitzar la part més feixuga de la digitalització (el bolcat de dades i la creació d''àudios) perquè us pugueu centrar exclusivament en l''estratègia i el relat de la parròquia.

T''agradaria que et mostrés com ha quedat aquesta prova real de Canillo en un mòbil? Et puc fer una demo de 10 minuts aquesta mateixa setmana, quant et va bé? 
Salut,
Miquel Utge
622836542
Projecte xino-xano', 'OUT', true, true, NULL, '2026-03-16 12:14:22.941439+00', '2026-03-16 11:14:31.23976+00', 'f6c4e0a8d7cd4030a2cf216180a8fa51', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('7a30be16-5be1-45ce-a7ec-b0c23a5a4001', 'e4bb29ee-73a3-4cbf-a2cd-9bfb31b0463c', '9a77e835-1d42-42e7-b497-2ede3948f73b', NULL, 'miquel@projectexinoxano.cat', 'info@museudecamins.com', 'El relat de Llagunes no pot dependre de si el museu està obert', 'Hola Ariadna,

Segueixo de prop la feina de conservació que feu al jaciment de Santa Creu de Llagunes. Explicar un assentament a 1.600m d''altitud que va de l''Edat de Bronze a la Mitjana és un repte divulgatiu enorme.

T''escric perquè sabem que molts visitants pugen fins al despoblat i, si no coincideixen amb la teva visita guiada, es perden el 90% de la història. Acaben mirant Google Maps, on el relat de Soriguera queda diluït i sense rigor científic.

A PXX hem creat la IA Punt d’Or: una eina que llegeix els teus PDFs i guies actuals i els converteix, en 15 minuts, en una audioguia immersiva per GPS. Sense que tu hagis d''escriure ni una sola paraula de nou.

Tinc una mostra de com sona el "teu" museu al mòbil. Et va bé que t''ho ensenyi? Dis-me quant podem quedar.
Una abraçada,
Miquel Utge
622836542

Projecte xino-xano', 'OUT', true, true, NULL, '2026-03-16 12:42:18.575513+00', '2026-03-16 11:42:26.953753+00', '40815ac0315d4c0d971c01b13a89c560', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('a561d65a-6bfa-4569-830d-c2a597479634', 'e4bb29ee-73a3-4cbf-a2cd-9bfb31b0463c', 'd323117a-11e4-448a-badc-9058b3f4bd32', NULL, 'miquel@projectexinoxano.cat', 'ajuntament@soriguera.ddl.net', 'Sobirania digital per als 14 pobles de Soriguera', 'Hola Josep Ramon,

Enhorabona per la gestió de Soriguera; mantenir un municipi amb 14 nuclis i tanta dispersió és fer política de trinxera real.

T''escric per una preocupació comuna: Actualment, quan un turista busca què fer a Soriguera, és Google qui decideix què veu. Ells es queden les dades i el control, mentre l''ajuntament posa el patrimoni. Silicon Valley s''emporta l''or i vosaltres la feina.

A Pprojecte xino-xano t''oferim infraestructura digital sobirana. No és una "app" més; és una plataforma on l''Ajuntament de Soriguera és l''únic propietari de les dades i del relat.

He preparat una demo de com apareixeria el vostre patrimoni amb la app de Projecte xino-xano. Quan vols que t''ho ensenyi en 10 minuts?

Salutacions,
Miquel Utge
622836542

Projecte xino-xano', 'OUT', true, true, NULL, '2026-03-16 12:40:30.110508+00', '2026-03-16 11:40:38.482054+00', '44a17e53e3874e139967609ed56b45e8', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('cdc6eb93-8178-4f84-ac41-e92d4e7463cc', 'd427d8a7-b977-44dc-ad40-dff00d37da3e', '00efd101-915b-48dd-bb00-8e09526d8bf1', NULL, 'miquel@projectexinoxano.cat', 'turisme@sort.cat', 'El PDF del Batlliu de Sort convertit en audioguia', 'Hola Gerard,

Felicitats per la part que et toca del premi de l''alcalde. Sé de sobres que darrere d''aquests reconeixements mediàtics hi ha molta feina invisible des de turisme i Sobirà Dinàmic.

El problema actual és que l''Ajuntament fa la feina dura de crear les rutes, però és Google qui s''emporta les dades dels turistes quan trepitgen Sort.

Per solucionar això sense carregar-te de més feina, he fet una prova pràctica: he passat el vostre PDF de l''itinerari del Batlliu per la nostra IA Punt d''Or i en només 15 minuts m''ha generat l''audioguia completa i sobirana.

Tens 10 minuts aquesta setmana i t''ho ensenyo en viu?

Una abraçada,

Miquel Utge
622836542
Projecte Xino Xano', 'OUT', true, true, NULL, '2026-03-17 18:40:28.067247+00', '2026-03-17 17:40:31.223328+00', '7a7bad4d9a604982830bcf182b8805a4', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('a704b4f8-6683-4bb4-b944-f877b060704e', 'd427d8a7-b977-44dc-ad40-dff00d37da3e', '1a433539-031d-44ab-82be-baedf1c17811', NULL, 'miquel@projectexinoxano.cat', 'alcaldia@sort.cat', 'Premi a la Nit del Dirigent i la sobirania de Sort', '
Hola Baldo,

Enhorabona pel reconeixement a la Nit del Dirigent de l''Esport. Aquest lideratge evidencia la gran feina que esteu fent posicionant Sort.

Però hi ha una fuita important: quan el turista arriba a la Vila Closa, qui li explica el poble? Ara mateix, l''algoritme de Google Maps. Sort inverteix en el patrimoni, i des de Califòrnia s''emporten les dades dels visitants.

Hem desenvolupat una infraestructura perquè els ajuntaments recupereu aquesta sobirania digital. He preparat una demo ràpida on pots veure com queda l''escut de Sort controlant el seu propi relat.

Tens 10 minuts aquesta setmana i t''ho ensenyo en directe per pantalla?

Una abraçada,

Miquel Utge
622836542
Projecte Xino Xano
', 'OUT', true, true, NULL, '2026-03-17 18:38:57.437389+00', '2026-03-17 17:39:00.584913+00', '61353ce7e62f42c9ac13f47fce4a2b8f', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('9ad7856c-65b6-4ded-bbcb-5529179b41c8', 'e4345303-303f-4387-91e8-fd7643b7e99c', '779138ee-9918-494a-94ad-2c2de9adb1e2', NULL, 'miquel@projectexinoxano.cat', 'eperise@torrecapdella.cat', 'La ruta de l''Antic Carrilet en audioguia (en 15 minuts)', 'Hola, Eva,

Segueixo la feina immensa de documentació que feu des del Museu Hidroelèctric. Sou un referent al Pirineu.

Veig que molts turistes que baixen del Telefèric acaben guiats per ressenyes desordenades de Google o Wikiloc que no reflecteixen el rigor del vostre arxiu. La feina la feu vosaltres, però el relat el controlen ells.

A Projecte Xino Xano hem desenvolupat la IA Punt d''Or. Puges un PDF dels que ja teniu a vallfosca.net i et genera una audioguia geolocalitzada en 15 minuts. Sense picar text i amb les dades 100% propietat de l''Ajuntament.

He fet una prova ràpida amb la ruta de l''Antic Carrilet. Tens 10 minuts dimarts o dimecres al matí i t''ho ensenyo en directe o si prefereixes per video trucada? Soc de Sort puc atançar-me en un moment.

Una abraçada,

Miquel Utge
622836542
Projecte Xino Xano', 'OUT', true, true, NULL, '2026-03-20 12:56:04.736989+00', '2026-03-20 11:56:04.980232+00', '6510874960e34e888d60addb29c36388', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('892df285-44d5-40aa-8d72-2a8a85af8904', 'e4345303-303f-4387-91e8-fd7643b7e99c', 'ed326611-e34c-4e5a-a8ad-3ad9af8bbfd7', NULL, 'miquel@projectexinoxano.cat', 'rjordana@torrecapdella.cat', 'El patrimoni de Capdella i el mapa digital del Pallars Jussà', 'Hola, Ramon,

T''escric per la teva doble visió com a regidor a Capdella i president del Consell Comarcal. Des de les institucions poseu tota la inversió per protegir el patrimoni del territori.

Però quan el turista arriba a la Vall Fosca, qui li explica la història? L''algoritme de Google Maps o rutes no oficials de Wikiloc. L''esforç és vostre, però Silicon Valley controla el relat i s''emporta les dades.

A Projecte Xino Xano construïm infraestructura digital sobirana des del Pallars. M''agradaria ensenyar-te com Capdella pot tenir la seva audioguia oficial geolocalitzada, i com aquest mateix model pot blindar digitalment tots els municipis del Jussà.

Tens 10 minuts dimarts o dimecres al matí i t''ho ensenyo per videotrucada o en persona? Soc de Sort i m´apropo en un moment.

Una abraçada,

Miquel Utge
622836542
Projecte Xino Xano', 'OUT', true, true, NULL, '2026-03-20 12:59:28.101302+00', '2026-03-20 11:59:28.35722+00', '22440493ed8544f78ec0975c52081898', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('aaab1c5c-a3c6-4aee-ac14-0fbf218f1e2f', 'e4bb29ee-73a3-4cbf-a2cd-9bfb31b0463c', '531b277b-ad47-4d95-96f2-a213e09043f7', NULL, 'miquel@projectexinoxano.cat', 'ajuntamentdesoriguera@gmail.com', 'El relat de Soriguera i el patrimoni de Llagunes', 'Hola Nuria,

He estat seguint la tasca de gestió que feu a Soriguera amb un territori tan dispers i exigent de mantenir. Amb 14 pobles i actius de la rellevància de Santa Creu de Llagunes, teniu un repte comunicatiu enorme: com explicar la història de la vall quan no hi ha un guia present o el centre d''interpretació està tancat?

Sovint, el visitant que arriba a Rubió o a Vilamur acaba consultant fonts digitals genèriques o rutes d''usuaris particulars que no fan justícia a la rigorositat històrica que treballeu des de l''Ajuntament. El relat institucional es perd i la informació queda fragmentada.

A Projecte Xino Xano ajudem els municipis a recuperar el control del seu contingut. Hem creat una infraestructura  que llegeix els vostres fulletons o PDFs oficials i els converteix, en pocs minuts, en audioguies immersives que s''activen per GPS. Això permet que el visitant escolti la vostra veu oficial sense necessitat d''instal·lar cartelleria física ni codis QR que afectin l''entorn natural.

He preparat una petita demo amb el material de Llagunes perquè veieu com podria sonar el vostre relat oficial en mans dels visitants.

Et truco a final de setmana per veure si podem quadrar la demo.

Salut,

Miquel Utge
622836542
Projecte Xino-Xano', 'OUT', true, true, NULL, '2026-03-23 10:39:20.387579+00', '2026-03-23 09:39:20.770789+00', '4314d809f006434791e9100ec69133a9', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('baa49ddd-cb57-40ec-a148-7cc3bfea96ce', '473f02c9-2b4b-4ad0-acec-751463f60247', '94e68e67-cb27-4b4d-a3eb-ba26ec5f8817', NULL, 'miquel@projectexinoxano.cat', 'ariadnaroca2002@gmail.com', 'El patrimoni de Isona i la sobirania digital', 'Hola Ariadna,

Et contacto perquè he vist que gestiones les carteres de Turisme i Transformació Digital, una combinació clau per al futur de municipis amb un patrimoni tan potent com el vostre.

He estat revisant els actius d''Isona i Conca Dellà, des de la ciutat romana d''Aeso fins a les rutes de la Guerra Civil. Heu fet una feina de conservació magnífica, però quan el visitant arriba al territori, el relat acaba depenent d''algoritmes i plataformes externes que el municipi no controla. L''Ajuntament posa el patrimoni i l''esforç, però la gestió de les dades i de l''experiència queda en mans de tercers.

Hem desenvolupat una tecnologia que permet als ajuntaments recuperar aquesta sobirania digital. Podem convertir els vostres PDFs o fulletons en audioguies geolocalitzades en menys de 15 minuts, sense que et tregui temps de la teva agenda ni hagis d''esperar a disposar de més personal tècnic.

T''agradaria veure com quedaria la ruta del Castell de Llordà en aquest format? Dimecres a les 11h o divendres a les 12h et puc ensenyar una prova real en una videotrucada de 10 minuts.

Ja em diràs si et va bé.

Salutacions,

Miquel Utge
622836542
Projecte Xino Xano', 'OUT', true, true, NULL, '2026-03-23 11:00:29.113454+00', '2026-03-23 10:00:29.556986+00', 'bb74c006dc344ad48525d40fd6b6991b', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('7293d84f-60fa-4be8-9b97-7a7bb39edcd2', 'd427d8a7-b977-44dc-ad40-dff00d37da3e', '1f4435f6-b943-4f04-b391-1eaf77d872ba', NULL, 'miquel@projectexinoxano.cat', 'pbascones@sort.cat', 'Fer visible el valor real de Sort i la Vall d''Àssua', 'ola Pere,

T''escric perquè des de Projecte Xino Xano estem ajudant els municipis a descentralitzar el turisme. Ens adonem que molts pobles i actius culturals queden amagats, mentre els visitants es concentren només en un parell de punts i es perden el valor real del territori.

Hem creat una infraestructura tecnològica sobirana on la nostra IA processa qualsevol dels vostres PDFs turístics (com els de la Ruta del Batlliu) i genera audioguies geolocalitzades en 15 minuts. Així aconseguim guiar el turista cap a aquells pobles que ara passen desapercebuts, retenint-los més temps descobrint la vostra història.

Tens 10 minuts dimarts al matí i t''ho ensenyo en directe?

Una abraçada,

Miquel Utge
622836542
Projecte xino-xano', 'OUT', true, true, NULL, '2026-03-23 12:27:59.650743+00', '2026-03-23 11:28:00.36456+00', '40c030844bd34e059f723217fff35f7b', false, NULL, 0, NULL);
INSERT INTO public.emails (id, deal_id, contacte_id, campanya_id, from_address, to_address, assumpte, cos, direccio, llegit, sincronitzat, message_id_extern, data_email, created_at, tracking_token, obert, data_obertura, nombre_obertures, ip_obertura) VALUES ('3660a6c0-0b9b-4182-a13a-130a7bad0a94', '484e3468-2ed3-4211-8307-15c7b12af329', 'bca93a14-db52-48b2-b801-041730f1edff', NULL, 'miquel@projectexinoxano.cat', 'regidoriacultura@elpontdesuert.cat', 'Sobre el relat digital del patrimoni del Pont de Suert', 'Bon dia Josep,

T’escric perquè he estat seguint de prop la feina que feu des de l’àrea de Turisme, especialment amb la preservació del patrimoni de les Falles i l''impuls de les rutes del Romànic a Viu i Irgo. És evident que El Pont de Suert té un relat cultural de primer nivell que cuideu amb molta cura.

L’únic motiu del meu correu és proposar-te una reflexió sobre com arriba avui aquest relat al visitant que camina pel municipi. Sovint, l''Ajuntament fa tota la inversió i la feina de camp, però la "veu" que guia el turista acaba depenent de plataformes externes que no controleu i que es queden amb tota la informació de l''usuari.

La nostra proposta se centra a retornar-vos el control: que El Pont de Suert tingui una infraestructura digital pròpia. Una eina que us permeti donar veu oficial al vostre patrimoni i, sobretot, que les dades de qui us visita tornin a ser propietat de l’Ajuntament.

Tens 10 minuts aquest divendres al matí o dilluns de la setmana entrant i t''ho explico de tu a tu?

Salutacions,

Miquel Utge
622836542
Projecte Xino Xano', 'OUT', true, true, NULL, '2026-03-23 12:31:50.446913+00', '2026-03-23 11:31:51.174507+00', '18a6b35938d548b5b613f91506479230', false, NULL, 0, NULL);


--
-- Data for Name: llicencies; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: memoria_municipis; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: pagaments; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: patrons_municipis; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: reunions_v2; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: usuaris; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.usuaris (id, email, password_hash, nom, rol, actiu, created_at, updated_at) VALUES ('2673fec4-5d12-47a5-af73-810f1f393af8', 'admin@projectexinoxano.cat', '$2b$12$CMYzXn91Y5LRR3f3rj70duKl6c0ZD8KacoiAtbVUTWJ.nR1elY45i', 'Miquel', 'admin', true, '2026-03-10 16:52:36.952157+00', '2026-03-17 16:43:30.840223+00');


--
-- Data for Name: tasques; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tasques (id, deal_id, contacte_id, municipi_id, usuari_id, titol, descripcio, data_venciment, tipus, prioritat, estat, created_at, updated_at) VALUES ('6bdb0db1-f39f-40da-9dce-de2eb7cc5b23', NULL, NULL, NULL, NULL, ' torre de capdella', '', '2026-03-11', 'email', 'mitjana', 'pendent', '2026-03-11 21:07:50.292037+00', '2026-03-11 21:07:50.292037+00');
INSERT INTO public.tasques (id, deal_id, contacte_id, municipi_id, usuari_id, titol, descripcio, data_venciment, tipus, prioritat, estat, created_at, updated_at) VALUES ('c1c08b19-b3a1-4bf7-9b49-b59ef94dac15', 'b0193e49-c46b-4645-a726-903aad57ab57', NULL, NULL, NULL, 'Trucada seguiment, Josep Maria Tirbio', '', '2026-03-20', 'trucada', 'mitjana', 'pendent', '2026-03-16 10:44:46.19776+00', '2026-03-16 10:44:46.19776+00');
INSERT INTO public.tasques (id, deal_id, contacte_id, municipi_id, usuari_id, titol, descripcio, data_venciment, tipus, prioritat, estat, created_at, updated_at) VALUES ('bf11f915-1bab-45de-8220-48db3e5794f7', '2e5361cc-6f1d-460f-9872-eaa1dd6a3e80', NULL, NULL, NULL, 'segon email', '', '2026-03-20', 'email', 'mitjana', 'pendent', '2026-03-16 11:02:21.680844+00', '2026-03-16 11:02:21.680844+00');
INSERT INTO public.tasques (id, deal_id, contacte_id, municipi_id, usuari_id, titol, descripcio, data_venciment, tipus, prioritat, estat, created_at, updated_at) VALUES ('b85df12f-0b62-4a14-a665-4a146cb9b96d', '2e5361cc-6f1d-460f-9872-eaa1dd6a3e80', NULL, NULL, NULL, 'tercer email', '', '2026-03-25', 'email', 'mitjana', 'pendent', '2026-03-16 11:02:46.909491+00', '2026-03-16 11:02:46.909491+00');
INSERT INTO public.tasques (id, deal_id, contacte_id, municipi_id, usuari_id, titol, descripcio, data_venciment, tipus, prioritat, estat, created_at, updated_at) VALUES ('0abcbdab-c9bf-4522-8e75-62f02b0d59a4', NULL, NULL, NULL, NULL, 'Trucar Maria Luengo', 'demanar email, propossar demo', '2026-03-20', 'trucada', 'mitjana', 'pendent', '2026-03-19 17:44:33.716253+00', '2026-03-19 17:44:33.716253+00');
INSERT INTO public.tasques (id, deal_id, contacte_id, municipi_id, usuari_id, titol, descripcio, data_venciment, tipus, prioritat, estat, created_at, updated_at) VALUES ('384adf86-624b-4d8a-9082-7971750328e4', NULL, NULL, NULL, NULL, 'enviar correus Isona', '', '2026-03-20', 'trucada', 'mitjana', 'pendent', '2026-03-19 17:53:53.100034+00', '2026-03-19 17:53:53.100034+00');
INSERT INTO public.tasques (id, deal_id, contacte_id, municipi_id, usuari_id, titol, descripcio, data_venciment, tipus, prioritat, estat, created_at, updated_at) VALUES ('1b3fd192-fa5e-480a-94b8-10ca5ffbb3c3', NULL, NULL, NULL, NULL, 'trucar Nuria de Soriguera', '', '2026-03-27', 'trucada', 'mitjana', 'pendent', '2026-03-23 09:40:13.891282+00', '2026-03-23 09:40:13.891282+00');


--
-- Data for Name: trucades_v2; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: schema_migrations; Type: TABLE DATA; Schema: realtime; Owner: supabase_admin
--

INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20211116024918, '2026-03-12 08:56:00');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20211116045059, '2026-03-12 08:56:00');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20211116050929, '2026-03-12 08:56:00');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20211116051442, '2026-03-12 08:56:00');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20211116212300, '2026-03-12 08:56:00');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20211116213355, '2026-03-12 08:56:00');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20211116213934, '2026-03-12 08:56:00');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20211116214523, '2026-03-12 08:56:00');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20211122062447, '2026-03-12 08:56:00');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20211124070109, '2026-03-12 08:56:00');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20211202204204, '2026-03-12 08:56:00');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20211202204605, '2026-03-12 08:56:00');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20211210212804, '2026-03-12 08:56:00');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20211228014915, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20220107221237, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20220228202821, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20220312004840, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20220603231003, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20220603232444, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20220615214548, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20220712093339, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20220908172859, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20220916233421, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20230119133233, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20230128025114, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20230128025212, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20230227211149, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20230228184745, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20230308225145, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20230328144023, '2026-03-12 08:56:01');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20231018144023, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20231204144023, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20231204144024, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20231204144025, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20240108234812, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20240109165339, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20240227174441, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20240311171622, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20240321100241, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20240401105812, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20240418121054, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20240523004032, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20240618124746, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20240801235015, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20240805133720, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20240827160934, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20240919163303, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20240919163305, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20241019105805, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20241030150047, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20241108114728, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20241121104152, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20241130184212, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20241220035512, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20241220123912, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20241224161212, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20250107150512, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20250110162412, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20250123174212, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20250128220012, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20250506224012, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20250523164012, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20250714121412, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20250905041441, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20251103001201, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20251120212548, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20251120215549, '2026-03-12 08:56:02');
INSERT INTO realtime.schema_migrations (version, inserted_at) VALUES (20260218120000, '2026-03-12 08:56:02');


--
-- Data for Name: subscription; Type: TABLE DATA; Schema: realtime; Owner: supabase_admin
--



--
-- Data for Name: buckets; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: buckets_analytics; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: buckets_vectors; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: migrations; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (0, 'create-migrations-table', 'e18db593bcde2aca2a408c4d1100f6abba2195df', '2026-03-12 08:26:10.696968');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (1, 'initialmigration', '6ab16121fbaa08bbd11b712d05f358f9b555d777', '2026-03-12 08:26:10.832889');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (2, 'storage-schema', 'f6a1fa2c93cbcd16d4e487b362e45fca157a8dbd', '2026-03-12 08:26:10.83712');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (3, 'pathtoken-column', '2cb1b0004b817b29d5b0a971af16bafeede4b70d', '2026-03-12 08:26:10.886692');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (4, 'add-migrations-rls', '427c5b63fe1c5937495d9c635c263ee7a5905058', '2026-03-12 08:26:11.127183');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (5, 'add-size-functions', '79e081a1455b63666c1294a440f8ad4b1e6a7f84', '2026-03-12 08:26:11.131442');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (6, 'change-column-name-in-get-size', 'ded78e2f1b5d7e616117897e6443a925965b30d2', '2026-03-12 08:26:11.136333');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (7, 'add-rls-to-buckets', 'e7e7f86adbc51049f341dfe8d30256c1abca17aa', '2026-03-12 08:26:11.147931');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (8, 'add-public-to-buckets', 'fd670db39ed65f9d08b01db09d6202503ca2bab3', '2026-03-12 08:26:11.152251');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (9, 'fix-search-function', 'af597a1b590c70519b464a4ab3be54490712796b', '2026-03-12 08:26:11.156913');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (10, 'search-files-search-function', 'b595f05e92f7e91211af1bbfe9c6a13bb3391e16', '2026-03-12 08:26:11.161995');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (11, 'add-trigger-to-auto-update-updated_at-column', '7425bdb14366d1739fa8a18c83100636d74dcaa2', '2026-03-12 08:26:11.16668');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (12, 'add-automatic-avif-detection-flag', '8e92e1266eb29518b6a4c5313ab8f29dd0d08df9', '2026-03-12 08:26:11.182311');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (13, 'add-bucket-custom-limits', 'cce962054138135cd9a8c4bcd531598684b25e7d', '2026-03-12 08:26:11.187243');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (14, 'use-bytes-for-max-size', '941c41b346f9802b411f06f30e972ad4744dad27', '2026-03-12 08:26:11.191821');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (15, 'add-can-insert-object-function', '934146bc38ead475f4ef4b555c524ee5d66799e5', '2026-03-12 08:26:11.247539');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (16, 'add-version', '76debf38d3fd07dcfc747ca49096457d95b1221b', '2026-03-12 08:26:11.252261');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (17, 'drop-owner-foreign-key', 'f1cbb288f1b7a4c1eb8c38504b80ae2a0153d101', '2026-03-12 08:26:11.256497');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (18, 'add_owner_id_column_deprecate_owner', 'e7a511b379110b08e2f214be852c35414749fe66', '2026-03-12 08:26:11.260505');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (19, 'alter-default-value-objects-id', '02e5e22a78626187e00d173dc45f58fa66a4f043', '2026-03-12 08:26:11.266223');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (20, 'list-objects-with-delimiter', 'cd694ae708e51ba82bf012bba00caf4f3b6393b7', '2026-03-12 08:26:11.270704');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (21, 's3-multipart-uploads', '8c804d4a566c40cd1e4cc5b3725a664a9303657f', '2026-03-12 08:26:11.276044');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (22, 's3-multipart-uploads-big-ints', '9737dc258d2397953c9953d9b86920b8be0cdb73', '2026-03-12 08:26:11.290739');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (23, 'optimize-search-function', '9d7e604cddc4b56a5422dc68c9313f4a1b6f132c', '2026-03-12 08:26:11.300077');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (24, 'operation-function', '8312e37c2bf9e76bbe841aa5fda889206d2bf8aa', '2026-03-12 08:26:11.304975');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (25, 'custom-metadata', 'd974c6057c3db1c1f847afa0e291e6165693b990', '2026-03-12 08:26:11.309509');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (26, 'objects-prefixes', '215cabcb7f78121892a5a2037a09fedf9a1ae322', '2026-03-12 08:26:11.314156');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (27, 'search-v2', '859ba38092ac96eb3964d83bf53ccc0b141663a6', '2026-03-12 08:26:11.318081');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (28, 'object-bucket-name-sorting', 'c73a2b5b5d4041e39705814fd3a1b95502d38ce4', '2026-03-12 08:26:11.322007');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (29, 'create-prefixes', 'ad2c1207f76703d11a9f9007f821620017a66c21', '2026-03-12 08:26:11.326048');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (30, 'update-object-levels', '2be814ff05c8252fdfdc7cfb4b7f5c7e17f0bed6', '2026-03-12 08:26:11.329875');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (31, 'objects-level-index', 'b40367c14c3440ec75f19bbce2d71e914ddd3da0', '2026-03-12 08:26:11.333793');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (32, 'backward-compatible-index-on-objects', 'e0c37182b0f7aee3efd823298fb3c76f1042c0f7', '2026-03-12 08:26:11.33815');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (33, 'backward-compatible-index-on-prefixes', 'b480e99ed951e0900f033ec4eb34b5bdcb4e3d49', '2026-03-12 08:26:11.342166');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (34, 'optimize-search-function-v1', 'ca80a3dc7bfef894df17108785ce29a7fc8ee456', '2026-03-12 08:26:11.346258');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (35, 'add-insert-trigger-prefixes', '458fe0ffd07ec53f5e3ce9df51bfdf4861929ccc', '2026-03-12 08:26:11.350372');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (36, 'optimise-existing-functions', '6ae5fca6af5c55abe95369cd4f93985d1814ca8f', '2026-03-12 08:26:11.354613');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (37, 'add-bucket-name-length-trigger', '3944135b4e3e8b22d6d4cbb568fe3b0b51df15c1', '2026-03-12 08:26:11.358811');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (38, 'iceberg-catalog-flag-on-buckets', '02716b81ceec9705aed84aa1501657095b32e5c5', '2026-03-12 08:26:11.363696');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (39, 'add-search-v2-sort-support', '6706c5f2928846abee18461279799ad12b279b78', '2026-03-12 08:26:11.42807');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (40, 'fix-prefix-race-conditions-optimized', '7ad69982ae2d372b21f48fc4829ae9752c518f6b', '2026-03-12 08:26:11.432486');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (41, 'add-object-level-update-trigger', '07fcf1a22165849b7a029deed059ffcde08d1ae0', '2026-03-12 08:26:11.436474');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (42, 'rollback-prefix-triggers', '771479077764adc09e2ea2043eb627503c034cd4', '2026-03-12 08:26:11.440502');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (43, 'fix-object-level', '84b35d6caca9d937478ad8a797491f38b8c2979f', '2026-03-12 08:26:11.444451');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (44, 'vector-bucket-type', '99c20c0ffd52bb1ff1f32fb992f3b351e3ef8fb3', '2026-03-12 08:26:11.448706');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (45, 'vector-buckets', '049e27196d77a7cb76497a85afae669d8b230953', '2026-03-12 08:26:11.454765');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (46, 'buckets-objects-grants', 'fedeb96d60fefd8e02ab3ded9fbde05632f84aed', '2026-03-12 08:26:11.468185');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (47, 'iceberg-table-metadata', '649df56855c24d8b36dd4cc1aeb8251aa9ad42c2', '2026-03-12 08:26:11.47363');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (48, 'iceberg-catalog-ids', 'e0e8b460c609b9999ccd0df9ad14294613eed939', '2026-03-12 08:26:11.480065');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (49, 'buckets-objects-grants-postgres', '072b1195d0d5a2f888af6b2302a1938dd94b8b3d', '2026-03-12 08:26:11.514438');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (50, 'search-v2-optimised', '6323ac4f850aa14e7387eb32102869578b5bd478', '2026-03-12 08:26:11.519499');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (51, 'index-backward-compatible-search', '2ee395d433f76e38bcd3856debaf6e0e5b674011', '2026-03-12 08:26:13.323655');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (52, 'drop-not-used-indexes-and-functions', '5cc44c8696749ac11dd0dc37f2a3802075f3a171', '2026-03-12 08:26:13.394139');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (53, 'drop-index-lower-name', 'd0cb18777d9e2a98ebe0bc5cc7a42e57ebe41854', '2026-03-12 08:26:13.425556');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (54, 'drop-index-object-level', '6289e048b1472da17c31a7eba1ded625a6457e67', '2026-03-12 08:26:13.428281');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (55, 'prevent-direct-deletes', '262a4798d5e0f2e7c8970232e03ce8be695d5819', '2026-03-12 08:26:13.430048');
INSERT INTO storage.migrations (id, name, hash, executed_at) VALUES (56, 'fix-optimized-search-function', 'cb58526ebc23048049fd5bf2fd148d18b04a2073', '2026-03-12 08:26:13.443918');


--
-- Data for Name: objects; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: s3_multipart_uploads; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: s3_multipart_uploads_parts; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: vector_indexes; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--



--
-- Data for Name: secrets; Type: TABLE DATA; Schema: vault; Owner: supabase_admin
--



--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('auth.refresh_tokens_id_seq', 1, false);


--
-- Name: subscription_id_seq; Type: SEQUENCE SET; Schema: realtime; Owner: supabase_admin
--

SELECT pg_catalog.setval('realtime.subscription_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict YWNcpZEBCZkJl9S5LptsrlBcrRup8Fyx2f71QJNEcW9thjQ9DUci8yelTcm28wv

