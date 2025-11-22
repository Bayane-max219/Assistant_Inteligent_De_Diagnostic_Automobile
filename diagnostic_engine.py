# règles + génération d’explicationzany ny IA local tsika eto fa tsy misy API 
# fonction roa avao diagnose pour la décision, generate_explanation pour le texte.”


import unicodedata

def extract_symptoms(selected_symptoms, free_text):
    symptoms = set()
    for name in selected_symptoms:
        symptoms.add(name.lower())

    def normalize(s: str) -> str:
        s = s.lower()
        s = unicodedata.normalize("NFKD", s)
        s = "".join(c for c in s if not unicodedata.combining(c))
        s = s.replace("’", "'")
        return s

    norm_text = normalize(free_text)

    detection_map = {
        # règles existantes
        "fumée noire": ["fumee noire", "fumee noir", "fumee sombre"],
        "consommation élevée": ["consommation elevee", "consommation haute", "mange beaucoup", "consomme beaucoup"],
        "moteur chauffe": ["moteur chauffe", "surchauffe moteur", "chauffe moteur"],
        "fuite liquide": ["fuite liquide", "fuite de liquide", "fuite liquide refroidissement", "fuite de liquide de refroidissement"],
        "démarrage difficile": ["demarrage difficile", "demarrage dur", "difficulte demarrage", "mal demarrer"],
        "batterie faible": ["batterie faible", "batterie dechargee", "batterie hs", "batterie morte"],
        # nouvelle règle injecteur
        "fumée blanche": ["fumee blanche", "fumee blanc", "fumee blanche epaisse", "fumee blanche echappement", "fumee a l echappement blanche"],
        "perte de puissance": ["perte de puissance", "manque de puissance", "plus de puissance", "puissance faible", "n avance pas", "n avance plus", "acceleration faible", "faible reprise"],
        "bruit métallique côté moteur": ["bruit metallique cote moteur", "bruit metallique moteur", "claquement metallique", "cliquetis metallique", "bruit metalique moteur", "toc toc moteur"],
    }

    for canonical, variants in detection_map.items():
        if any(v in norm_text for v in variants):
            symptoms.add(canonical)

    # heuristiques de co‑occurrence robustes
    if "fumee" in norm_text and ("blanch" in norm_text or "blach" in norm_text):
        symptoms.add("fumée blanche")

    has_bruit = "bruit" in norm_text
    has_metal_like = any(t in norm_text for t in ["metal", "metall", "marteau", "marteaux", "fer"])
    has_moteur_area = (
        ("moteur" in norm_text)
        or ("cote moteur" in norm_text)
        or ("du cote moteur" in norm_text)
        or ("cote du moteur" in norm_text)
    )
    if has_bruit and has_metal_like and has_moteur_area:
        symptoms.add("bruit métallique côté moteur")

    return symptoms

# ato amin'ny fonction diagnose toy resaky If/elif reny
# ato avao koa laha te hampilitsy regle diagnostic vaovao mampilitsy bloc elif....avao
# ambany ao avao koa laha te hanova gravité le panne zany 
def diagnose(selected_symptoms, free_text):
    symptoms = extract_symptoms(selected_symptoms, free_text)

    fumee_noire = "fumée noire" in symptoms
    consommation_elevee = "consommation élevée" in symptoms
    moteur_chauffe = "moteur chauffe" in symptoms
    fuite_liquide = "fuite liquide" in symptoms
    demarrage_difficile = "démarrage difficile" in symptoms
    batterie_faible = "batterie faible" in symptoms
    fumee_blanche = "fumée blanche" in symptoms
    perte_puissance = "perte de puissance" in symptoms
    bruit_metallique_moteur = "bruit métallique côté moteur" in symptoms

    diagnostic = "Aucun diagnostic précis"
    gravite = "à confirmer"
    cout_min = 0
    cout_max = 0

    if fumee_blanche and perte_puissance and bruit_metallique_moteur:
        diagnostic = "Injecteur défectueux"
        gravite = "moyen"
        cout_min = 800000
        cout_max = 2000000
    elif fumee_noire and consommation_elevee:
        diagnostic = "Problème d'injection"
        gravite = "moyen"
        cout_min = 700000
        cout_max = 1800000
    elif moteur_chauffe and fuite_liquide:
        diagnostic = "Radiateur défectueux"
        gravite = "critique"
        cout_min = 900000
        cout_max = 2700000
    elif demarrage_difficile and batterie_faible:
        diagnostic = "Panne de batterie"
        gravite = "léger"
        cout_min = 400000
        cout_max = 700000

    return {
        "diagnostic": diagnostic,
        "gravite": gravite,
        "cout_min": cout_min,
        "cout_max": cout_max,
        "symptomes_deduits": sorted(symptoms),
    }

# ato zany texte local tss api 
# ato le maha IA local azy
# ato avao koa laha te hampilitsy explication IA hafa na hanova
def generate_local_explanation(result, selected_symptoms, free_text):
    diagnostic = result["diagnostic"]
    gravite = result["gravite"]
    cout_min = result["cout_min"]
    cout_max = result["cout_max"]
    symptomes = result["symptomes_deduits"]

    base = "Analyse des symptômes du véhicule.\n\n"

    if symptomes:
        base += "Symptômes pris en compte : " + ", ".join(symptomes) + ".\n\n"
    elif selected_symptoms or free_text.strip():
        base += "Les symptômes saisis ne correspondent pas exactement aux règles, mais ils ont été pris en compte.\n\n"
    else:
        base += "Aucun symptôme n'a été saisi.\n\n"

    if diagnostic == "Problème d'injection":
        explication = (
            "La présence de fumée noire associée à une consommation élevée de carburant "
            "oriente vers un dysfonctionnement du système d'injection. "
            "Les injecteurs peuvent envoyer trop de carburant ou mal pulvériser, "
            "ce qui provoque une combustion incomplète."
        )
    elif diagnostic == "Injecteur défectueux":
        explication = (
            "La combinaison de fumée blanche, d'une perte de puissance et d'un bruit métallique côté moteur "
            "est typique d'un injecteur défectueux. Un injecteur qui fuit ou pulvérise mal provoque une "
            "mauvaise combustion et des irrégularités de fonctionnement. Un contrôle et un test d'étanchéité "
            "des injecteurs sont recommandés."
        )
    elif diagnostic == "Radiateur défectueux":
        explication = (
            "Le moteur qui chauffe accompagné d'une fuite de liquide indique un problème "
            "au niveau du circuit de refroidissement, souvent au niveau du radiateur. "
            "Une fuite empêche le liquide de refroidissement de circuler correctement, "
            "ce qui entraîne une surchauffe du moteur."
        )
    elif diagnostic == "Panne de batterie":
        explication = (
            "Un démarrage difficile combiné à une batterie faible correspond généralement "
            "à une batterie en fin de vie ou insuffisamment chargée. "
            "La batterie ne fournit plus l'énergie nécessaire au démarreur."
        )
    else:
        explication = (
            "Les symptômes fournis ne permettent pas d'identifier clairement une panne précise "
            "parmi les règles définies. Il est recommandé de compléter le diagnostic par des tests "
            "mécaniques plus approfondis."
        )

    if cout_min > 0 or cout_max > 0:
        cout_txt = f"L'estimation du coût de réparation se situe entre {cout_min} Ar et {cout_max} Ar."
    else:
        cout_txt = "Aucune estimation de coût n'est proposée à ce stade."

    gravite_txt = f"Gravité estimée : {gravite}."

    return base + explication + "\n\n" + gravite_txt + " " + cout_txt
# envoie local par défaut (ou en cas d’échec réseau).
def generate_explanation(result, selected_symptoms, free_text):
    """
    Génère l'explication du diagnostic localement, sans appel à une API externe.

    Inputs:
      - result: dict retourné par `diagnose`
      - selected_symptoms: liste de symptômes cochés
      - free_text: description libre

    Retourne:
      - chaîne de caractères explicative en français
    """
    return generate_local_explanation(result, selected_symptoms, free_text)
