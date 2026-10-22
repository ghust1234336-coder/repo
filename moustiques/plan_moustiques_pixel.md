# Plan vidéo — « Et si tu effaçais tous les moustiques ? » avec Pip (pixel art HD)

Recette : voir `../plan_maitre_video.md`, Partie A (reprise sans changement, sauf la palette thématique et les bruitages ci-dessous).

## B0. Fiche d'identité
| Champ | Valeur |
|---|---|
| Sujet | Que se passerait-il si les moustiques disparaissaient ? (réécrit avec « tu » et une baguette magique : un enjeu personnel au lieu d'une hypothèse abstraite) |
| **Question du titre** | « Et si tu effaçais tous les moustiques ? » (7 mots) |
| Titres de secours | « Un monde sans moustiques, bonne idée ? » / « Tu peux effacer les moustiques. Tu cliques ? » |
| Réponse en une phrase | Pour la nature, presque personne ne les regretterait (sauf dans le Grand Nord), et on sauverait des centaines de milliers de vies par an ; mais les scientifiques préfèrent ne viser que les quelques espèces dangereuses. |
| Ton | ludique, « enquête » avec une pointe d'émerveillement |
| STYLE | `pixel` (moteur `douche/pixel.py`, déjà dans le dépôt). Le personnage-sujet et la chambre de nuit rendent bien en pixel ; les deux chiffres (stades, espèces) se montrent en barres pixel. |
| STRUCTURE | `classique` (A7, 8 scènes). Pas de chronologie : une disparition n'a pas d'étapes datables sans inventer. |
| Décor principal | Chambre de Pip la nuit, lampe de chevet allumée, « bzzz » au-dessus du lit |
| Personnage-sujet | **Zézette**, une femelle moustique effrontée et gourmande (trompe longue, yeux ronds, ailes translucides). Tic : lève ses pattes arrière comme une danseuse. Second rôle : **Bzz**, un mâle doux et rêveur, antennes plumeuses, qui ne pense qu'aux fleurs. |
| Costume de Pip | Chapeau d'explorateur avec voile de moustiquaire (une fleur rose piquée sur le ruban) |
| Palette thème (14) | chambre nuit `#3a3466` · lampe `#ffb347` · draps / neige `#e6f4fa` · moustique `#7a6a58` `#4b3f33` · ailes `#cfe8ff` · trompe `#2a2220` · sang `#c2185b` · parasite `#9be15d` · mare `#2e86ab` · roseaux `#5bbf6a` `#2f7a3f` · fleur / nectar `#ff9ecd` · toundra `#a3845a` |
| Pip (3) | `#5fd4c4` `#2f9c99` `#ff6f91` |
| Musique | 118 BPM, ré mineur → fa majeur à partir de la scène 7, chiptune nocturne « enquête » (basse triangle en pizzicato, mélodie carrée discrète) |
| Mot-choc | **PERSONNE** (les lettres s'envolent une à une comme des moustiques, avec un petit « bzz » chacune) |

## B1. Structure
| # | Rôle | Pip (famille d'interaction) | Durée cible |
|---|---|---|---|
| 1 | Accroche | utiliser_objet (lève sa baguette magique sur Zézette) | ≈ 2,9 s |
| 2 | Déclic | réagir (« ! » et yeux ronds devant le podium) | ≈ 8,2 s |
| 3 | Mécanisme | **absent** | ≈ 8,0 s |
| 4 | Rebondissement | subir (envahi par des mâles qui butinent la fleur de son chapeau) | ≈ 8,8 s |
| 5 | Réponse | réagir (yeux en étoiles) | ≈ 6,2 s |
| 6 | Objection | se_deplacer (glisse en luge sur la toundra) | ≈ 6,8 s |
| 7 | Le plus fou / conseil | **absent** | ≈ 5,0 s |
| 8 | Fin | saute sur le bouton | ≈ 3,8 s |

Mots qui arrivent **sur le mot lui-même** : **MORTEL**, **TAXI**, **PERSONNE**, **MÂLE**.

Le rebondissement commence vers 19 s sur ≈ 51 s, soit ≈ 38 % de la vidéo.

## B2. Script (172 mots, ≈ 51 s à 3,4 mots/s)
| # | Scène | Voix off (une phrase = une synthèse) | Texte à l'écran | Balises / stabilité / vitesse |
|---|---|---|---|---|
| 1 | Accroche | « Et si tu effaçais tous les moustiques de la planète ? » | « Et si tu **EFFAÇAIS** / tous les moustiques ? » | `[curious]` / 0,3 / 1,10 |
| 2 | Déclic | « Bonne idée : c'est l'animal le plus mortel. » · « Rien qu'avec le paludisme, près de six cent mille morts par an. » · « Plus de sept Stades de France pleins, chaque année. » | « Le plus **MORTEL** » · « ≈ 600 000 / an » · « × 7 STADES » | `[surprised]` / 0,3 / 1,08 |
| 3 | Mécanisme | « Mais ce n'est pas la piqûre qui tue : c'est un parasite. » · « La femelle l'aspire chez un malade, puis pique quelqu'un d'autre. » · « Pour les microbes, le moustique est un taxi. » | « **PARASITE** » · « MALADE → TOI » · « **TAXI** » | `[curious]` / 0,45 / 1,06 |
| 4 | Rebondissement | « Sauf que sur trois mille cinq cents espèces, peu nous piquent. » · « Et les mâles ne piquent jamais : ils boivent du nectar. » · « Alors si tu les effaces tous… qui va les regretter ? » | « 3 500 espèces » · « Mâles : **0 PIQÛRE** » · « Qui va les **REGRETTER** ? » | `[whispers]` sur « peu nous piquent » / 0,4 / 1,05 |
| 5 | Réponse | « Réponse des biologistes : presque personne. » · « Oiseaux, poissons et libellules mangeraient d'autres insectes. » · « Et on sauverait des centaines de milliers de vies. » | « Presque **PERSONNE** » · « MENU B : autres insectes » · « + des centaines de milliers de **VIES** » | `[playful]` / 0,5 / 1,05 |
| 6 | Objection | « Mais alors, aucun animal n'en a besoin ? » · « Si : dans le Grand Nord, ils forment des nuages. » · « Là-bas, les poussins d'oiseaux migrateurs s'en régalent. » | « Aucun animal ? » · « **GRAND NORD** » · « Buffet pour **POUSSINS** » | `[mischievously]` / 0,3 / 1,06 |
| 7 | Le plus fou / conseil | « Alors les scientifiques visent seulement les espèces dangereuses. » · « Ils lâchent des mâles modifiés : leurs filles meurent jeunes. » | « On **VISE** juste » · « Mâles modifiés → 0 fille adulte » | `[excited]` / 0,3 / 1,06 |
| 8 | Fin | « Celui-là, tu peux le garder : c'est un mâle. Abonne-toi, y'a plein d'autres secrets ! » | « C'est un **MÂLE** » · « **Abonne**-toi / pour d'autres **secrets** ! » + bouton « S'ABONNER » et cloche | `[excited]` / 0,3 / 1,10 |

Mots par scène : 10 · 28 · 29 · 31 · 21 · 23 · 17 · 13 (aucune scène sous 2,8 mots/s avec les durées cibles).

« … » : une seule fois, scène 4 (suspense avant la réponse). Boucle ouverte : la question de fin de scène 4 (« qui va les regretter ? »), à laquelle la scène 5 répond.

`NOMINAL = [2.9, 8.2, 8.0, 8.8, 6.2, 6.8, 5.0, 3.8]` (≈ 49,7 s + respirations ; mettre à l'échelle sur la voix réelle).

**Coût** : environ 1 150 caractères, balises comprises.

**Si la vidéo dépasse 55 s**, raccourcir dans cet ordre :
1. fusionner les phrases 2 et 3 de la scène 6 en « Si : dans le Grand Nord, les poussins d'oiseaux migrateurs s'en régalent. » ;
2. couper « Plus de sept Stades de France pleins, chaque année. » (le chiffre reste à l'écran sous forme de barre).

## B3. Exactitude
- **« L'animal le plus mortel »** : formule courante (OMS, Fondation Gates). Les maladies transmises par des vecteurs, surtout les moustiques, causent plus de 700 000 morts par an ; les homicides humains environ 400 000 à 500 000, les serpents environ 100 000, les requins quelques-uns.
- **Paludisme, près de 600 000 morts par an** : *World Malaria Report* de l'OMS (2024) : ≈ 597 000 décès en 2023, surtout des enfants de moins de cinq ans en Afrique. **À revérifier dans le dernier rapport avant l'enregistrement** ; « près de six cent mille » reste juste tant que le chiffre est entre 550 000 et 620 000.
- **« Plus de sept Stades de France »** : image. Stade de France ≈ 80 000 places ; 7 × 80 000 = 560 000 < 597 000.
- **Ce n'est pas la piqûre qui tue** : vrai pour le paludisme (parasite *Plasmodium*, transmis par les moustiques *Anopheles*). Le parasite se multiplie dans le moustique puis rejoint ses glandes salivaires (en une à deux semaines), et passe dans la salive injectée à la piqûre suivante. Pour la dengue, le Zika ou le chikungunya (*Aedes*), c'est un virus : d'où le mot générique « microbes » dans la phrase « taxi ».
- **« Taxi à microbes »** : image, pas un terme scientifique (le terme exact est « vecteur »).
- **Seule la femelle pique** : vrai. Elle a besoin de protéines du sang pour ses œufs. Mâles et femelles se nourrissent aussi de nectar ; les mâles n'ont pas de pièces buccales capables de percer la peau.
- **3 500 espèces, peu nous piquent** : environ 3 500 à 3 600 espèces décrites ; « seulement quelques centaines piquent ou dérangent l'humain » (J. Fang, « A world without mosquitoes », *Nature*, 2010). Celles qui transmettent des maladies graves sont encore moins nombreuses (quelques dizaines d'*Anopheles*, *Aedes aegypti*, *Aedes albopictus*, certains *Culex*).
- **« Presque personne » ne les regretterait** : simplification assumée de l'avis recueilli par *Nature* (2010) : la plupart des écologues interrogés pensent que les prédateurs (oiseaux, poissons, libellules, chauves-souris) changeraient de proies et qu'un autre insecte occuperait la place, mais **ce n'est pas une certitude** et certains chercheurs sont plus prudents. D'où « presque » et « réponse des biologistes », pas « la science prouve ».
- **Grand Nord** : dans la toundra arctique, les moustiques forment en été des essaims très denses. Les poussins d'oiseaux limicoles (qui nichent dans l'Arctique) se nourrissent d'insectes, dont les moustiques. Certains chercheurs estiment que leur disparition y aurait un effet notable. « Nuages » est une image.
- **Mâles modifiés, filles qui meurent jeunes** : technique réelle (moustiques *Aedes aegypti* « auto-limitants » d'Oxitec, testés au Brésil, aux îles Caïmans, en Floride) : les mâles relâchés portent un gène qui empêche leurs filles d'atteindre l'âge adulte, ce qui fait baisser la population **localement**. Des projets de « forçage génétique » (Target Malaria) visent les moustiques du paludisme. Simplification assumée : on ne parle pas d'extinction d'espèce, seulement de « viser » les espèces dangereuses.
- **Antennes plumeuses = mâle** : vrai, les mâles ont des antennes très touffues, les femelles des antennes fines. C'est ce qui permet le gag de fin.
- On **ne montre pas** : malade réaliste, sang qui coule, chiffres par pays, conseils médicaux (répulsifs, traitements). Le paludisme est montré par un compteur et des silhouettes de stade, jamais par des personnes malades.

## B4. Mise en scène
1. **Accroche — chambre la nuit** *(Pip : utiliser_objet)*
   - Image déjà en mouvement : Zézette fait des loopings au-dessus du lit ; Pip, sous la couette, sort une baguette magique qui grésille.
   - Titre « Et si tu EFFAÇAIS tous les moustiques ? » avant 0,5 s ; « EFFAÇAIS » clignote comme un bouton prêt à être cliqué.
   - Sur « planète » : coupe sur la Terre en pixel, couverte de petits points qui bourdonnent. Bruitages : bzzz (panoramique gauche-droite), grésillement de baguette.
2. **Déclic — podium des animaux** *(Pip : réagir)*
   - Sur « mortel » : podium pixel ; requin, serpent et humain sur les marches basses, Zézette sur la plus haute, qui lève ses pattes arrière (tic). Titre « Le plus MORTEL » qui tremble ; Pip, au pied du podium, « ! » au-dessus de la tête.
   - Sur « paludisme » : compteur pixel qui défile jusqu'à « ≈ 600 000 / AN ».
   - Sur « Stades » : sept stades pixel qui se remplissent l'un après l'autre (pop à chaque stade). Bruitages : ding de podium, tic-tac de compteur.
3. **Mécanisme — vue loupe, coupe du moustique** *(Pip absent)*
   - Vignette loupe ; sur « parasite » : coupe transparente de Zézette, un petit parasite vert à deux yeux nage dans son ventre.
   - Sur « malade » : Zézette pique un bras à gauche (silhouette grise), le parasite monte vers la tête du moustique ; flèche « MALADE → TOI » ; elle vole vers un bras à droite.
   - Sur « taxi » : le parasite porte une casquette de chauffeur ; Zézette s'allume d'un panneau « TAXI » sur le dos. Titre « TAXI » qui tombe pile sur le mot. Bruitages : slurp, klaxon 8 bits.
4. **Rebondissement — la mare au crépuscule** *(Pip : subir)*
   - Musique en sourdine pendant le chuchotement.
   - Sur « espèces » : une barre de 3 500 petits moustiques en grille, puis seule une fine bande rouge reste allumée (« quelques centaines »), le reste devient gris.
   - Sur « mâles » : des dizaines de Bzz (antennes plumeuses) se posent sur la fleur du chapeau de Pip, qui vacille sous leur poids ; étiquette « Mâles : 0 PIQÛRE ».
   - Sur « regretter » : Pip pointe sa baguette sur la grille ; elle hésite ; titre « Qui va les REGRETTER ? ». Bruitages : sirotage de paille, bzz doux.
5. **Réponse — écran « menu » de l'écosystème** *(Pip : réagir)*
   - Coupure musicale 0,5 s avant « Réponse ».
   - Sur « personne » : les lettres de « PERSONNE » s'envolent une à une (mot-choc).
   - Sur « insectes » : un oiseau, un poisson et une libellule regardent un menu ; la ligne « moustiques » est barrée au feutre rouge, ils pointent « autres insectes ».
   - Sur « vies » : silhouettes qui se rallument par rangées ; Pip, dans un coin, yeux en étoiles. Bruitages : ding, page de menu.
6. **Objection — toundra arctique** *(Pip : se_deplacer)*
   - Sur « besoin » : écran partagé « AILLEURS » (prairie calme) / « GRAND NORD » (toundra) ; la moitié droite s'agrandit et chasse la gauche.
   - Sur « nuages » : nuage noir tramé de moustiques en parallaxe ; Pip, en parka par-dessus son chapeau, traverse l'écran en luge en dessous.
   - Sur « poussins » : trois poussins de limicoles picorent le nuage, étiquette « Buffet pour POUSSINS ». Bruitages : vent, piou-piou, bzz grave.
7. **Le plus fou — le labo** *(Pip absent)*
   - Sur « visent » : réticule de visée qui balaie une étagère de moustiques et ne verrouille que deux espèces (cadre rouge).
   - Sur « mâles modifiés » : une boîte s'ouvre, des Bzz marqués d'un petit « M » s'envolent ; arbre généalogique pixel : leurs filles restent à l'état de larve puis disparaissent (fondu en damier), les fils continuent. Bruitages : bip de labo, boîte qui s'ouvre.
8. **Fin — chambre la nuit (boucle)** *(Pip : agir_corps)*
   - Même cadre que l'accroche : un moustique tourne au-dessus du lit, Pip lève la baguette.
   - Sur « mâle » : loupe sur ses antennes plumeuses, étiquette « MÂLE » ; Pip baisse la baguette, Bzz part sur la fleur du chapeau.
   - Pip saute sur « S'ABONNER », cloche 8 bits.

**Bruitages propres au sujet** : bzzz (aigu pour Zézette, grave et doux pour Bzz, avec panoramique), grésillement de baguette magique, slurp, klaxon 8 bits, sirotage de paille, piou-piou de poussins, vent de toundra, bip de labo.

## B5. Table `PIP_ACTIONS`
```python
PIP_ACTIONS = {
    1: ("utiliser_objet", "lève sa baguette magique sur Zézette"),
    2: ("reagir", "« ! » au pied du podium"),
    3: None,                       # absent (coupe du moustique)
    4: ("subir", "des mâles se posent sur la fleur de son chapeau, il vacille"),
    5: ("reagir", "yeux en étoiles"),
    6: ("se_deplacer", "traverse la toundra en luge"),
    7: None,                       # absent (labo)
    8: ("agir_corps", "saute sur le bouton S'ABONNER"),
}
```
