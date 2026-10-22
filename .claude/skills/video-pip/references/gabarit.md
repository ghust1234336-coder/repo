# Partie B — Gabarit d'épisode (à remplir à partir du sujet)

> Copier cette partie dans `plan_<slug>_vox.md`, sous un en-tête :
> `# Plan vidéo — « <Titre> » avec Pip (style Vox)`, suivi de la Partie A reprise par référence (« Recette : voir plan_maitre_video.md, Partie A »).

## B0. Fiche d'identité
| Champ | Valeur |
|---|---|
| Sujet | <le sujet retenu (réécrit librement par Claude si c'est mieux)> |
| **Question du titre** | <question concrète, avec « tu » ou « ta », ≤ 8 mots> |
| Titres de secours | <2 autres titres> |
| Réponse en une phrase | <la réponse que donne la scène 5> |
| Ton | <ludique / mystérieux / « beurk-rigolo » / émerveillé…> |
| Variante | `vox` (collage papier) ou `flat` — voir A2 |
| Images d'archive | <photos du domaine public : source, fichier, licence vérifiée, crédit> |
| STRUCTURE | `classique` (A7) ou `chronologie` (variante A7) |
| Étapes (si chronologie) | <3 ou 4 repères, ex. Jour 2 / 1 mois / 3 mois / 1 an> |
| Réactions sociales | <une par étape, de plus en plus forte> |
| Décor principal | <lieu du quotidien où se passe l'accroche> |
| Personnage-sujet | <nom, personnalité, tic visuel, photo ou illustration> ou « aucun » |
| Costume de Pip | <accessoire lié au sujet> |
| Palette thème (8–12) | <codes hex, groupés par rôle> |
| Musique | <BPM, tonalité, ambiance> |
| Mot-choc | <le mot qui a l'effet spécial du titre> |

## B1. Structure
| # | Rôle | Plans | Pip (famille d'interaction) | Durée cible |
|---|---|---|---|---|
| 1 | Accroche | <…> | <…> | ≈ 2,8 s |
| 2 | Déclic | <…> | <…> | ≈ 5,5 s |
| 3 | Mécanisme | <…> | **absent** | ≈ 6,5 s |
| 4 | Rebondissement | <…> | <…> | ≈ 6,5 s |
| 5 | Réponse | <…> | <…> | ≈ 7,5 s |
| 6 | Objection | <…> | <…> | ≈ 7,5 s |
| 7 | Le plus fou / conseil | <…> | <absent ou réagit> | ≈ 6 s |
| 8 | Fin | <retour au décor de l'accroche> | saute sur le bouton | ≈ 2,2 s |

Mots qui arrivent **sur le mot lui-même** : <liste, 2 à 4 mots>.

## B2. Script
| # | Scène | Voix off (une phrase = une synthèse) | Texte à l'écran (bande papier, mot surligné) | Balises / stabilité / vitesse |
|---|---|---|---|---|
| 1 | Accroche | « <…> » | « <…> » | <…> |
| … | … | … | … | … |
| 8 | Fin | « <phrase-boucle> Abonne-toi, y'a plein d'autres secrets ! » | « **Abonne**-toi / pour d'autres **secrets** ! » + bouton « S'ABONNER » et cloche | `[excited]` / 0,3 / 1,10 |

`NOMINAL = [...]` (durées de référence de la chorégraphie, à mettre à l'échelle sur la voix réelle).

**Coût** : environ <N> caractères, balises comprises.

**Si la vidéo approche 60 s**, raccourcir dans cet ordre : <2 phrases désignées à l'avance, jamais dans le hook ni dans la réponse>.

**Glyphes** : <caractères spéciaux du texte à l'écran et police qui les affiche>.

## B3. Exactitude
Pour chaque fait du script :
- ce qui est vrai, en termes scientifiques, **avec un lien vers sa source** (article, organisme officiel, étude) ; un fait sans source est coupé ;
- ce qui est une **image** (comparaison) et pas un terme scientifique ;
- les simplifications assumées ;
- ce que montrent vraiment les photos d'archive ;
- ce qu'on **ne montre pas** (rien de choquant, pas de dose, pas de conseil médical, etc.).

## B4. Mise en scène
Pour chaque scène :
- **Titre de la scène — décor** *(Pip : famille d'interaction, ou absent)* ;
- 2 à 4 puces qui décrivent ce qu'on voit, **calées sur les phrases** (« Sur "<mot>" : … ») ;
- les bruitages de la scène.

Puis la liste des **bruitages propres au sujet** (4 à 8).

## B5. Table `PIP_ACTIONS`
```python
PIP_ACTIONS = {
    1: ("<famille>", "<action>"),
    2: ("<famille>", "<action>"),
    3: None,                       # absent
    # ...
    8: ("agir_corps", "saute sur le bouton S'ABONNER"),
}
```

