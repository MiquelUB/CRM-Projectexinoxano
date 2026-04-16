
import models

def suggest_angle(m: models.Municipi):
    """
    Arbre de decisió d'accions basat en el model unificat.
    """
    angles = []
    
    # 1. Regles Geogràfiques
    if m.geografia == "muntanya":
        angles.append("Turisme Actiu i de Muntanya.")
    elif m.geografia == "mar":
        angles.append("Gestió de Platges i Activitats.")
    elif m.geografia == "interior":
        angles.append("Turisme Rural i Gastronòmic.")

    # 2. Regles de dades
    if not m.web or len(m.web) < 5:
         angles.append("Manca de Web activa. Oportunitat alta.")

    # 3. Regles de temperatura o etapa
    if m.etapa_actual == "research":
         angles.append("Acció: Completar inspecció en mapes.")

    if not angles:
        return "Mantenir calor comercial."

    return " i ".join(angles[:2])
