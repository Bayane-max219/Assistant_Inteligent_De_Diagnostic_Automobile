# Assistant intelligent de diagnostic automobile

Projet Python 3.11 avec interface **Tkinter** qui aide au diagnostic de pannes automobiles
à partir des symptômes saisis par l'utilisateur (cases à cocher + texte libre).

Ce projet a été réalisé dans le cadre d’une épreuve / sujet d’**Intelligence Artificielle**
(système expert simplifié) et sert de mini-assistant pour mécaniciens.

---

## Objectifs pédagogiques

- Mettre en place un **mini système expert** en Python (règles `if / elif`).
- Combiner :
  - des **symptômes structurés** (cases à cocher),
  - et une **saisie en texte libre** avec détection automatique de mots-clés.
- Fournir un **diagnostic**, un **niveau de gravité** et une **estimation de coût**.
- Générer une **explication IA locale** (sans API externe), basée sur les règles du moteur de diagnostic.
- Créer une **interface graphique** professionnelle avec Tkinter (login + interface principale).

---

## Technologies utilisées

- **Langage** : Python 3.11  
- **Interface graphique** : Tkinter  
- **Architecture** : mini système expert à base de règles  
- **Packaging Windows** : PyInstaller (génération d’un `.exe` avec icône personnalisée)  

---

## Fonctionnalités principales

- **Écran de login mécanicien**
  - Thème marron.
  - Saisie e‑mail + mot de passe (validation simple).
  - Petite question de confirmation en français :
    > "Êtes-vous vraiment mécanicien(ne) automobile ?"
  - Affichage de l’e‑mail du mécanicien connecté + bouton **Déconnexion** dans l’interface principale.

- **Interface principale de diagnostic**
  - Bandeau supérieur avec utilisateur connecté + bouton **Déconnexion**.
  - Bandeau titre coloré :  
    *"Assistant intelligent de diagnostic automobile"*.
  - Organisation en **deux colonnes** :
    - Colonne gauche :
      - Cases à cocher pour les symptômes (fumée noire, fumée blanche, perte de puissance, bruit métallique côté moteur, etc.).
      - Zone de **"Description libre des symptômes"**.
      - Bouton **"Diagnostiquer"** bien visible.
    - Colonne droite :
      - Affichage du **diagnostic**.
      - Affichage de la **gravité**.
      - **Estimation du coût** (en Ariary, Ar).
      - Zone de texte "**Explication IA**".

- **Diagnostic automatisé (système expert)**
  - Le moteur de diagnostic applique des règles `if / elif` en combinant :
    - les cases cochées,
    - les symptômes détectés dans le texte libre (avec normalisation + synonymes).

---

## Règles de diagnostic implémentées

Les règles actuelles (simplifiées) incluent notamment :

1. **Injecteur défectueux** (nouvelle règle ajoutée)  
   Déclenchée si :
   - fumée blanche,
   - **perte de puissance**,
   - **bruit métallique côté moteur**.  
   → Gravité : *moyen*  
   → Coût estimatif : **entre 800 000 Ar et 2 000 000 Ar**

2. **Problème d’injection**
   - fumée noire,
   - consommation élevée.  
   → Gravité : *moyen*  
   → Coût estimatif : **entre 700 000 Ar et 1 800 000 Ar**

3. **Radiateur défectueux**
   - moteur chauffe,
   - fuite de liquide.  
   → Gravité : *critique*  
   → Coût estimatif : **entre 900 000 Ar et 2 700 000 Ar**

4. **Panne de batterie**
   - démarrage difficile,
   - batterie faible.  
   → Gravité : *léger*  
   → Coût estimatif : **entre 400 000 Ar et 700 000 Ar**

Chaque diagnostic est accompagné d’une **explication textuelle locale** ("Explication IA")
qui justifie la conclusion (sans utiliser d’API externe payante).

---

## Détection des symptômes en texte libre

Le moteur :
- **normalise** le texte (minuscules, accents, apostrophes),
- utilise une **liste de synonymes / variantes** (par ex. "manque de puissance", "n’avance plus", etc.),
- applique quelques **heuristiques de co‑occurrence** pour détecter des combinaisons comme :
  - fumée blanche,
  - bruit métallique côté moteur,
  - perte de puissance.

Cela rend la saisie plus naturelle pour l’utilisateur tout en restant dans un système expert simple.

---

## Lancement du projet

### 1. Lancer en Python (développement)

Dans un terminal :

```bash
py -3.11 main_app.py
```

- Une fenêtre de **login** s’ouvre d’abord.
- Après connexion, l’**interface de diagnostic** s’affiche.

### 2. Version exécutable Windows

Une configuration **PyInstaller** est prévue pour générer un `.exe` avec icône personnalisée.

Exemple de commande (à adapter) :

```bash
py -3.11 -m PyInstaller --onefile --windowed --icon=icon.ico main_app.py
```

L’exécutable généré apparaît ensuite dans le dossier `dist/`.

---

## Captures d’écran

Les captures suivantes montrent l’interface réelle de l’application, dans l’ordre :

### 01 – Écran de connexion
![01 – Connexion](screenshoots/01-Connexion.png)

### 02 – Confirmation mécanicien
![02 – Confirmation mécanicien](screenshoots/02-Confirmation.png)

### 03 – Interface principale
![03 – Interface principale](screenshoots/03-Interface.png)

### 04 – Test de diagnostic n°1
![04 – Test de diagnostic n°1](screenshoots/04-Test1.png)

### 05 – Test de diagnostic n°2
![05 – Test de diagnostic n°2](screenshoots/05-Test2.png)

### 06 – Test de diagnostic n°3
![06 – Test de diagnostic n°3](screenshoots/06Test3.png)

---

## Limitations et pistes d’amélioration

- Les règles sont **fixes** (pas d’apprentissage automatique).
- Les coûts sont des **estimations simplifiées** en Ariary.
- Possibilité d’ajouter :
  - d’autres règles métier,
  - plus de symptômes,
  - une base de données de cas,
  - une meilleure gestion des historiques de diagnostics.

Ce projet se concentre volontairement sur un **système expert simple + une bonne interface Tkinter**
pour illustrer les concepts d’IA symbolique appliqués au diagnostic automobile.
