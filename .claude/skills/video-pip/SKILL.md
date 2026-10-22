---
name: video-pip
description: Écrit le plan complet d'un épisode de la série de vidéos courtes verticales « Comprendre un truc en 60 s » avec Pip (style Vox, collage papier, moteur vox.py, voix ElevenLabs). À utiliser dès que l'utilisateur donne un sujet de vidéo (« Sujet : … »), demande un plan_<slug>_vox.md, un nouvel épisode avec Pip, ou veut réécrire / vérifier le script d'un épisode.
---

# Plan d'épisode « Comprendre un truc en 60 s » avec Pip

Entrée : un **sujet**. Sortie : `plan_<slug>_vox.md`, avec les sections B0 à B5 remplies.

Fichiers de référence (à lire au moment où l'étape en a besoin) :
- `references/recette.md` : la recette commune (Partie A). Leçons, format, style Vox, rythme, voix ElevenLabs, musique, Pip, structure de rétention, vérifications. **Elle ne change pas d'un épisode à l'autre**, sauf la palette thème et les bruitages propres au sujet.
- `references/gabarit.md` : le gabarit à remplir (Partie B, sections B0 à B5).
- `references/fabrication.md` : les fichiers du projet et les commandes (Partie C). Ne le lire que si l'utilisateur passe à la fabrication.

Le fichier de sortie commence par `# Plan vidéo — « <Titre> » avec Pip (style Vox)`, puis la ligne « Recette : voir plan_maitre_video.md, Partie A », puis B0 à B5.

La voix off se fait **toujours avec ElevenLabs** (voix Léo, voir recette A4). Aucun autre service de synthèse vocale.

## Procédure

0. **Réécrire le sujet ou le titre si c'est mieux (autorisé, et même encouragé).** Le sujet est un point de départ. Reformuler, resserrer, changer d'angle ou passer à la variante chronologie si la vidéo est plus forte. Exemples :
   - « que se passe-t-il si on ne prend pas de douche pendant un an » → **« Un an sans douche, il se passe quoi ? »** ;
   - « que se passerait-il si les moustiques disparaissaient ? » → **« Et si tu effaçais tous les moustiques ? »**.

   Pas besoin de se justifier. Garde-fous : garder l'intention (thème, ton, public) ; l'exactitude passe avant le hook.

1. **Trouver la question.** Une question concrète, avec un paradoxe ou un enjeu personnel. *« Le sommeil » → « Pourquoi tu ne peux pas rester éveillé ? »* Proposer 3 titres, en retenir un.
   **Choisir la structure** : si le sujet se raconte dans le temps, prendre la **variante chronologie** (recette A7) avec 3–4 étapes et une réaction sociale par étape.
2. **Écrire la réponse en une phrase.** Si elle n'est pas claire, la question est mal choisie : retour à l'étape 1.
3. **Rassembler 5 à 7 faits vérifiés, chacun avec sa source** (chercher sur le web). Garder seulement ceux qui servent la réponse (R1). Les classer : déclic, mécanisme, idée reçue (rebondissement), objection probable, fait le plus fou / conseil.
4. **Placer les faits dans les 8 rôles** de la recette A7. Chaque transition en « Sauf que / Mais alors / Résultat », jamais « Et aussi ».
5. **Écrire le script** avec les règles d'écriture de A7 : ≤ 12 mots par phrase, une info par phrase, une comparaison par notion abstraite, un chiffre, une boucle ouverte, mot-choc en fin de phrase. **Pas de limite de mots** : écrire ce dont la vidéo a besoin, sans remplissage. Seule limite : la durée estimée (mots ÷ 3,4) reste sous 60 s.
6. **Vérifier le script avant d'aller plus loin** (avant toute génération de voix payante) :
   - compter les mots par phrase, et estimer la durée totale (mots ÷ 3,4 ; sous 60 s) ;
   - aucun mot interdit (« en fait », « donc voilà », « il faut savoir que », « comme on l'a vu ») ;
   - « … » au plus une fois par scène, jamais deux scènes de suite ;
   - chiffres écrits en toutes lettres, pas de « Non ! » ;
   - débit estimé par scène (mots ÷ durée cible) entre 3,2 et 3,6 mots/s, jamais sous 2,8 ;
   - le fil (A8-11) : pour chaque scène, « Cette scène rapproche de la réponse à <question> parce que… ».
   Si une règle casse, corriger le script avant de continuer.
7. **Choisir les visuels** : décor du quotidien pour l'accroche, coupe annotée / schéma / graphique pour le mécanisme, écran partagé ou balance pour l'objection, une vraie photo du domaine public dès qu'elle existe. Un changement visuel toutes les 2 s au plus. Respecter les zones interdites (bas de l'écran, colonne de droite).
8. **Distribuer Pip** : absent d'au moins 2 scènes, familles d'interaction alternées, gags calés sur la phrase en cours. Remplir `PIP_ACTIONS`.
9. **Palette thème, musique, bruitages propres**, et images d'archive du domaine public (NASA, NOAA, CDC, USFWS…) : vérifier la licence (jamais CC BY-SA), noter le crédit.
10. **Écrire la section Exactitude (B3)** avec un lien de source par fait, puis désigner les 2 phrases à couper si la vidéo approche 60 s.
11. **Écrire** `plan_<slug>_vox.md` dans le dossier de travail, sections B0 à B5 remplies.
