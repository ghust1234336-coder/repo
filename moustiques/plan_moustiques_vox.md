# Plan vidéo — « Et si tu effaçais tous les moustiques ? » avec Pip (style Vox)

Recette : voir `../plan_maitre_video.md`, Partie A, avec **STYLE = vox** (collage papier, moteur `../lune/vox.py`). Même script que la version pixel (`plan_moustiques_pixel.md`) ; seuls changent l'habillage, les plans et le son.

## B0. Fiche d'identité
| Champ | Valeur |
|---|---|
| Sujet | Que se passerait-il si les moustiques disparaissaient ? |
| **Question du titre** | « Et si tu effaçais tous les moustiques ? » (7 mots) |
| Titres de secours | « Un monde sans moustiques, bonne idée ? » / « Tu peux effacer les moustiques. Tu cliques ? » |
| Réponse en une phrase | Pour la nature, presque personne ne les regretterait (sauf dans le Grand Nord), et on sauverait des centaines de milliers de vies par an ; mais les scientifiques préfèrent ne viser que les quelques espèces dangereuses. |
| Ton | ludique, « enquête » avec une pointe d'émerveillement |
| STYLE | `vox` : vraies photos de moustiques en macro (CDC, domaine public), chiffres en graphiques tracés au trait, feutre rouge pour barrer et entourer |
| STRUCTURE | `classique` (A7, 8 scènes) |
| Décor principal | chambre la nuit, papier bleu nuit `#121a2e`, lampe de chevet découpée |
| Personnage-sujet | **Zézette** : la vraie photo d'*Anopheles gambiae* (CDC) détourée en découpage, avec deux yeux ronds en papier collés par-dessus (seule touche « cartoon »). Tic : lève ses pattes arrière (petite rotation du découpage). **Bzz**, le mâle, est une illustration papier (aplats, antennes plumeuses très visibles) : pas de photo du domaine public vérifiée pour l'instant. |
| Costume de Pip | chapeau d'explorateur en papier kraft, voile de moustiquaire en trame transparente, fleur rose sur le ruban |
| Palette thème | papier `#efe8dc` `#ddd2bf` · nuit `#121a2e` `#1f2b4a` · lampe `#ffb347` · sang `#c2185b` · parasite `#9be15d` · mare `#2f7f8f` `#8fc3c8` · roseaux `#5e9f62` · fleur `#ff9ecd` · toundra `#a3845a` · neige `#e6f4fa` · gris `#8f8a82` |
| Fixes Vox | encre `#1b1b1f`, surligneur `#ffe14d`, feutre rouge `#e8402f` |
| Musique | 112 BPM, ré mineur → fa majeur à partir de la scène 7 ; pad doux + arpège pincé + pulsation légère, ambiance documentaire « enquête » |
| Mot-choc | **PERSONNE** : les lettres se détachent de la bande de papier et s'envolent une à une, comme des moustiques (petit « bzz » chacune) |

### Images d'archive (à télécharger dans `moustiques/assets/src/`)
| Usage | Fichier Wikimedia Commons | Licence vérifiée | Crédit à mettre dans la description |
|---|---|---|---|
| Zézette (femelle qui pique), scènes 1, 2, 3, 8 | `Anopheles gambiae mosquito feeding 1354.p lores.jpg` (700×465) | domaine public | CDC / James Gathany |
| Grille des espèces (scène 4), labo (scène 7) | `Aedes aegypti CDC-Gathany.jpg` (700×470) · `Anopheles stephensi.jpeg` (3032×2008) | domaine public | CDC / James Gathany |
| Parasite (scène 3) | `Plasmodium.jpg` (440×473) | domaine public | CDC (via Wikimedia Commons) |
| La planète (scène 1) | `The Earth seen from Apollo 17.jpg` (déjà dans `lune/assets/src/earth_apollo17.jpg`) | domaine public | NASA / Apollo 17 |
| Toundra (scène 6) | prévue : `Caribou herd.jpg` (USFWS, domaine public) ; **non utilisée** (téléchargement refusé par Wikimedia), la toundra est dessinée en papier | — | — |

**Écartées** (licence CC BY-SA, incompatible avec la règle « domaine public seulement ») : `Stade de France.jpg`, `Mosquito larvae.jpg`. Le stade et les larves sont dessinés en illustration papier.

`Plasmodium.jpg` est en basse résolution : on l'utilise petit, dans une loupe, ou on le remplace par un parasite dessiné (forme de croissant vert) si le rendu est flou.

## B1. Structure
| # | Rôle | Plans | Pip | Durée cible |
|---|---|---|---|---|
| 1 | Accroche | chambre de nuit, Zézette (photo) tourne au-dessus du lit → la Terre (photo) couverte de points noirs | utiliser_objet (lève sa baguette) | ≈ 2,9 s |
| 2 | Déclic | podium des animaux en découpages → compteur → 7 stades dessinés qui se remplissent | réagir (« ! ») | ≈ 8,2 s |
| 3 | Mécanisme | coupe annotée de Zézette (photo + feutre) → schéma malade → toi → étiquette TAXI | **absent** | ≈ 8,0 s |
| 4 | Rebondissement | planche d'entomologiste (3 500 cases) → Bzz sur la fleur du chapeau de Pip → coupure de journal | subir (vacille sous les mâles) | ≈ 8,8 s |
| 5 | Réponse | coupure musicale → « Presque PERSONNE » → menu des prédateurs barré au feutre → silhouettes qui se rallument | réagir (yeux en étoiles) | ≈ 6,2 s |
| 6 | Objection | écran partagé prairie / toundra (photo USFWS) → nuage tramé → poussins dessinés | se_deplacer (luge) | ≈ 6,8 s |
| 7 | Le plus fou | réticule sur la planche d'espèces → boîte de mâles modifiés → arbre généalogique tracé au feutre | **absent** | ≈ 5,0 s |
| 8 | Fin | retour à la chambre (boucle), loupe sur les antennes plumeuses, bouton S'ABONNER | agir_corps (saute sur le bouton) | ≈ 3,8 s |

Mots qui arrivent **sur le mot lui-même** : **MORTEL**, **TAXI**, **PERSONNE**, **MÂLE**.

## B2. Script (167 mots, 55,6 s au rendu)
Identique à la version pixel, avec la première coupe prévue appliquée : la première prise durait 59,4 s, donc les deux phrases du Grand Nord sont fusionnées et toutes les scènes passent à la vitesse 1,10 (comme l'épisode Lune). Les balises tiennent compte de la règle A4 (« Non » sobre : le script n'en contient pas).

| # | Voix off | Texte à l'écran (bande papier, mot surligné) | Balise / stabilité / vitesse |
|---|---|---|---|
| 1 | « Et si tu effaçais tous les moustiques de la planète ? » | « Et si tu **effaçais** / tous les moustiques ? » | `[curious]` 0,3 / 1,10 |
| 2 | « Bonne idée : c'est l'animal le plus mortel. » · « Rien qu'avec le paludisme, près de six cent mille morts par an. » · « Plus de sept Stades de France pleins, chaque année. » | « L'animal le plus **mortel** » · étiquette mono « ≈ 600 000 / AN » · « × 7 STADES » | `[surprised]` 0,3 / 1,10 |
| 3 | « Mais ce n'est pas la piqûre qui tue : c'est un parasite. » · « La femelle l'aspire chez un malade, puis pique quelqu'un d'autre. » · « Pour les microbes, le moustique est un taxi. » | « un **parasite** » · « MALADE → TOI » (manuscrit) · « **TAXI** » | `[curious]` 0,5 / 1,10 |
| 4 | « Sauf que sur trois mille cinq cents espèces, peu nous piquent. » · « Et les mâles ne piquent jamais : ils boivent du nectar. » · « Alors si tu les effaces tous… qui va les regretter ? » | « 3 500 espèces » · « mâles : **0 piqûre** » · « Qui va les **regretter** ? » | `[whispers]` 0,5 / 1,10 |
| 5 | « Réponse des biologistes : presque personne. » · « Oiseaux, poissons et libellules mangeraient d'autres insectes. » · « Et on sauverait des centaines de milliers de vies. » | « Presque **personne** » · menu « autres insectes » · « des centaines de milliers de **vies** » | `[playful]` 0,5 / 1,10 |
| 6 | « Mais alors, aucun animal n'en a besoin ? » · « Si : dans le Grand Nord, les poussins d'oiseaux migrateurs s'en régalent. » | « Aucun animal ? » · « **Grand Nord** » · « buffet pour **poussins** » | `[mischievously]` 0,3 / 1,10 |
| 7 | « Alors les scientifiques visent seulement les espèces dangereuses. » · « Ils lâchent des mâles modifiés : leurs filles meurent jeunes. » | « On **vise** juste » · « mâles modifiés → 0 fille adulte » | `[excited]` 0,3 / 1,10 |
| 8 | « Celui-là, tu peux le garder : c'est un mâle. » · « Abonne-toi, y'a plein d'autres secrets ! » | « C'est un **mâle** » · bouton « S'ABONNER » | `[excited]` 0,3 / 1,10 |

`NOMINAL = [2.9, 8.2, 8.0, 8.8, 6.2, 6.8, 5.0, 3.8]`

**Coût** : environ 1 150 caractères, balises comprises.

**Si la vidéo dépasse encore 55 s** (fusion de la scène 6 déjà faite) : couper « Plus de sept Stades de France pleins, chaque année. » (les stades restent à l'écran).

**Glyphes** (vérifiés avec Pillow sur les polices de `lune/assets/`) : « → » n'existe ni en DM Mono ni en Nothing You Could Do, seulement en Work Sans Bold ; « ≈ » existe en DM Mono et en Work Sans, pas en manuscrit. Donc : « MALADE > TOI » en manuscrit (ou une flèche tracée au feutre), « ≈ 600 000 / AN » en mono, « mâles modifiés → 0 fille adulte » en Work Sans Bold.

## B3. Exactitude
Mêmes faits et mêmes sources que `plan_moustiques_pixel.md`, B3 (OMS *World Malaria Report*, Fang 2010 dans *Nature*, Oxitec, Target Malaria). En plus, pour les images :
- **La photo de Zézette est un *Anopheles gambiae*** : c'est bien un moustique du paludisme, cohérent avec la scène 3. Les yeux en papier collés sont un gag assumé.
- **Grille des 3 500 espèces** : on montre des cases identiques (illustration), pas 3 500 vraies photos. La bande rouge « quelques centaines » est une proportion approximative (environ un dixième de la grille au plus).
- **Toundra** : la photo USFWS vient de l'Alaska (refuge arctique) ; elle illustre « le Grand Nord », sans prétendre montrer un essaim réel. Le nuage de moustiques est une trame dessinée.
- **Arbre généalogique** : schéma simplifié du principe « auto-limitant » ; les fils porteurs du gène continuent de vivre, les filles n'atteignent pas l'âge adulte.
- **Ce qu'on ne montre pas** : pas de photo de malade, de sang réel ou de piqûre en gros plan sur la peau ; le bras piqué est une silhouette papier grise.

## B4. Mise en scène
**1. Accroche — chambre de nuit** *(Pip : utiliser_objet)*
- 0,1 s : bande « Et si tu **effaçais** » qui tombe et rebondit ; Zézette (photo détourée, yeux en papier) fait des boucles au-dessus du lit, petite traînée pointillée au feutre derrière elle.
- Pip, assis dans le lit, lève une baguette magique en papier ; étoiles jaunes en découpage à la pointe.
- Sur « planète » : coupe franche sur la Terre (photo Apollo 17) couverte de petits points noirs qui frémissent. Sons : bzzz (panoramique), grésillement de baguette, feuille qui glisse.

**2. Déclic — podium** *(Pip : réagir)*
- Sur « mortel » : podium en carton, découpages requin, serpent et silhouette humaine sur les marches basses ; Zézette sur la plus haute, pattes arrière levées. « mortel » passé au surligneur ; Pip, au pied du podium, « ! » au feutre au-dessus de sa tête.
- Sur « paludisme » : étiquette mono sur fond jaune, compteur qui défile jusqu'à « ≈ 600 000 / AN ».
- Sur « Stades » : sept stades dessinés (vue de dessus, ovale vert et gradins gris) qui se remplissent de points un par un, « × 7 » manuscrit. Sons : tampon, tic-tac de compteur, pop à chaque stade.

**3. Mécanisme — planche annotée** *(Pip absent)*
- Fond crème, Zézette en grand (photo) ; sur « parasite » : loupe circulaire avec le *Plasmodium* (photo ou croissant vert dessiné), flèche rouge vers le ventre.
- Sur « malade » : deux bras en silhouette papier, gauche et droite ; flèche rouge en arc tracée au feutre de l'un à l'autre, « MALADE > TOI » en manuscrit.
- Sur « taxi » : étiquette jaune « TAXI » posée sur le dos de Zézette avec un coup de tampon. Sons : feutre, klaxon doux, tampon.

**4. Rebondissement — planche d'entomologiste** *(Pip : subir)*
- Musique en sourdine pendant le chuchotement.
- Sur « espèces » : planche de collection, cases avec épingles ; la caméra recule pour montrer la grille entière, « 3 500 espèces » à la main. Une fine bande de cases reste en couleur, le reste passe en gris ; la bande est entourée au feutre.
- Sur « mâles » : coupe sur Pip ; une dizaine de Bzz (illustration, antennes plumeuses) se posent sur la fleur de son chapeau, qui penche ; Pip vacille. Étiquette « mâles : 0 piqûre ».
- Sur « regretter » : coupure de journal « Le Petit Naturaliste : FAUT-IL LES EFFACER ? », mot « regretter » surligné. Sons : machine à écrire, sirotage de paille.

**5. Réponse — le menu** *(Pip : réagir)*
- Coupure musicale 0,5 s avant « Réponse ».
- Sur « personne » : bande « Presque **personne** », les lettres de « personne » s'envolent une à une (mot-choc).
- Sur « insectes » : oiseau, poisson et libellule en découpages devant un menu de restaurant en papier ; la ligne « moustiques » est barrée au feutre rouge, « autres insectes » entouré.
- Sur « vies » : rangées de silhouettes grises qui se colorent une à une ; Pip, dans un coin, yeux en étoiles. Sons : ding doux, feutre, page.

**6. Objection — Grand Nord** *(Pip : se_deplacer)*
- Sur « besoin » : écran partagé, prairie dessinée à gauche / toundra (photo USFWS) à droite ; un volet papier déchiré donne tout l'écran à la toundra.
- Sur « nuages » : nuage de moustiques en trame (`halftone`) qui ondule au-dessus de la toundra ; Pip, en parka par-dessus son chapeau, traverse en luge en bas de l'écran.
- Sur « poussins » : trois poussins de limicoles dessinés picorent sous le nuage, étiquette « buffet pour poussins ». Sons : vent, piou-piou, bzz grave.

**7. Le plus fou — labo** *(Pip absent)*
- Retour sur la planche d'espèces ; sur « visent » : réticule rouge tracé au feutre qui ne verrouille que deux cases (photos *Anopheles* et *Aedes*).
- Sur « mâles modifiés » : boîte en carton estampillée « M », des Bzz s'en échappent ; arbre généalogique tracé au trait : les branches « fils » continuent, les branches « filles » sont barrées d'une croix rouge. Sons : boîte qui s'ouvre, feutre, croix.

**8. Fin — chambre de nuit (boucle)** *(Pip : agir_corps)*
- Même cadre que l'accroche : un moustique tourne au-dessus du lit, Pip lève la baguette.
- Sur « mâle » : loupe sur les antennes plumeuses, entourées au feutre, « mâle » surligné ; Pip baisse la baguette, Bzz se pose sur la fleur.
- Bouton « S'ABONNER » en pop, Pip saute dessus (bonk + cloche).

**Bruitages propres au sujet** : bzzz aigu (Zézette, panoramique) et bzz grave et doux (Bzz), grésillement de baguette, klaxon doux, sirotage de paille, piou-piou de poussins, vent de toundra, boîte en carton qui s'ouvre. Transitions et annotations : sons papier du style Vox (feuille qui glisse, machine à écrire, tampon, feutre, ciseaux).

## B5. Table `PIP_ACTIONS`
```python
PIP_ACTIONS = {
    1: ("utiliser_objet", "lève sa baguette magique sur Zézette"),
    2: ("reagir", "« ! » au pied du podium"),
    3: None,                       # absent (planche annotée)
    4: ("subir", "des mâles se posent sur la fleur de son chapeau, il vacille"),
    5: ("reagir", "yeux en étoiles"),
    6: ("se_deplacer", "traverse la toundra en luge"),
    7: None,                       # absent (labo)
    8: ("agir_corps", "saute sur le bouton S'ABONNER"),
}
```

## Fabrication
Copier `../lune/` dans `moustiques/` (moteur `vox.py`, `pip_vox.py`, `sfx.py`, `snap.py`, polices), puis réécrire seulement `tts.py` (SCRIPT ci-dessus), `timeline.py`, `decors_moustiques.py` et `episode_moustiques.py`.

```bash
python tts.py                          # voix ElevenLabs -> audio/voice.wav + timings.json
python sfx.py                          # musique documentaire + bruitages -> audio/mix.wav
python episode_moustiques.py --final   # 1080x1920 sur 4 processus -> renders/moustiques.mp4
python snap.py 1.5 20 36.5             # images de contrôle + tests A8 (vidéo < 100 Mo, aucun glyphe manquant)
```
