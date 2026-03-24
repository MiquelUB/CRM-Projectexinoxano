from models_v2 import MunicipiLifecycle, GeografiaEnum

def suggest_angle(m: MunicipiLifecycle):
    """
    Arbre de decisió d'accions.
    Retorna un angle comercial o temes recomanats de comunicació basat en el Diagnòstic.
    """
    angles = []
    diag = m.diagnostic_digital if m.diagnostic_digital else {}

    # 1. Regles Geogràfiques
    if m.geografia == GeografiaEnum.muntanya:
        angles.append("Turisme Actiu i de Muntanya (Excursionisme/BTT).")
    elif m.geografia == GeografiaEnum.mar:
        angles.append("Gestió de Platges i Activitats Acuàtiques.")
    elif m.geografia == GeografiaEnum.interior:
        angles.append("Turisme Rural i Gastronòmic.")

    # 2. Regles de Diagnòstic
    v1_notes = diag.get("notes_v1") or ""
    if "patrimoni" in v1_notes.lower():
         angles.append("Destacar itineraris de Patrimoni Històric.")

    web = diag.get("web")
    if not web or len(web) < 5:
         angles.append("Buit Digital: Manca de Web activa o obsoleta. Oportunitat alta.")

    # 3. Regles de temperatura o etapa
    if m.etapa_actual == "research":
         angles.append("Acció: Completar inspecció en mapes per trobar 3 POIs forts.")

    if not angles:
        return "Mantenir calor comercial i demanar feedback general."

    # Return a formatted string or top-1
    return " i ".join(angles[:2])  # Combinem els 2 primers
