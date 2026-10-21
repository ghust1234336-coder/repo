# Plan vidéo — « Un an sans douche, il se passe quoi ? » avec Pip (pixel art HD)

Recette : voir `plan_maitre_video.md`, Partie A (reprise sans changement, sauf la palette thématique et les bruitages ci-dessous).

## B0. Fiche d'identité
| Champ | Valeur |
|---|---|
| Sujet | Ne pas prendre de douche pendant un an |
| **Question du titre** | « Un an sans douche, il se passe quoi ? » (7 mots) |
| Titres de secours | « Et si tu ne te lavais plus jamais ? » / « Ta peau sans savon pendant 365 jours » |
| Réponse en une phrase | Tu survis, mais ta peau tombe malade (croûte, mycoses, boutons)… et tout le monde te fuit, sauf toi qui ne sens rien. |
| Ton | « beurk-rigolo » |
| STYLE | `pixel` |
| Décor principal | Salle de bain carrelée, douche à l'italienne |
| Personnage-sujet | **Bacto**, une bactérie verte gourmande et effrontée ; tic : se lèche les babines |
| Costume de Pip | Bonnet de douche rose à pois |
| Palette thème (14) | carrelage `#bfe6f5` `#78b8db` · eau `#3f8fd6` · peau `#f5cba7` `#d99a6c` `#a8653f` · croûte `#6e4122` · sébum `#e6c34f` · bactéries `#86d94f` `#3e9442` · odeur `#c7e04a` · champignons `#b56fe0` · savon `#ff8fbf` · gris `#8a8fa8` |
| Pip (3) | `#5fd4c4` `#2f9c99` `#ff6f91` |
| Musique | 120 BPM, la mineur → do majeur à la fin, chiptune sautillant « bêtise » |
| Mot-choc | **PUE** (lettres qui tremblent, nuage vert qui s'échappe) |

## B1. Structure
| # | Rôle | Pip (famille d'interaction) | Durée cible |
|---|---|---|---|
| 1 | Accroche | utiliser_objet : ferme le robinet de la douche | ≈ 2,8 s |
| 2 | Déclic | réagir : se bouche le nez | ≈ 6 s |
| 3 | Mécanisme | **absent** | ≈ 7 s |
| 4 | Rebondissement | subir : envahi par les champignons, se gratte | ≈ 6,5 s |
| 5 | Réponse | réagir : seul, une boule d'herbe passe | ≈ 7 s |
| 6 | Objection | agir_corps : renifle son aisselle, ravi | ≈ 6,5 s |
| 7 | Conseil | **absent** | ≈ 6 s |
| 8 | Fin | agir_corps : saute sur le bouton | ≈ 3 s |

Mots qui arrivent **sur le mot lui-même** : « pue », « champignons », « fuit », « mains ».

## B2. Script
| # | Scène | Voix off | Texte à l'écran | Balises / stab. / vitesse |
|---|---|---|---|---|
| 1 | Accroche | « Tu arrêtes la douche pendant un an. Il se passe quoi ? » | « **UN AN** SANS DOUCHE ? » | `[curious]` / 0,3 / 1,10 |
| 2 | Déclic | « Ta sueur, toute seule, ne sent rien. » · « Ce sont les bactéries qui la mangent qui puent. » · « Ton aisselle devient leur buffet à volonté. » | « 0 ODEUR » → « ÇA **PUE** ! » → panneau « BUFFET » | `[surprised]` / 0,3 / 1,08 |
| 3 | Mécanisme | « Ta peau perd trente mille cellules mortes par minute. » · « Avec le sébum, elles collent comme de la pâte. » · « En quelques semaines, une croûte brune apparaît. » | « 30 000 / MIN » · « J+30 » | `[curious]` / 0,45 / 1,06 |
| 4 | Rebondissement | « Sauf que la croûte, c'est pas le pire. » · « Dans tes plis chauds, poussent des champignons. » · « Ça gratte, ça rougit… et ça s'infecte. » | « **MYCOSES** » | `[whispers]` sur « c'est pas le pire » / 0,4 / 1,05 |
| 5 | Réponse | « Alors, un an sans douche ? Tu survis. » · « Mais ta peau tombe malade, et tout le monde te fuit. » | « TU SURVIS » → « ON TE **FUIT** ! » | `[playful]` / 0,5 / 1,05 |
| 6 | Objection | « Mais alors, toi, tu sentirais ton odeur ? » · « Non ! Ton nez s'habitue en quelques minutes. » · « Tu serais le seul à ne rien sentir. » | « NON ! » · écran partagé « TOI » / « LES AUTRES » | `[mischievously]` / 0,3 / 1,06 |
| 7 | Conseil | « Pas besoin d'une douche par jour. » · « Lave surtout tes aisselles, tes pieds, et tes mains. » | « AISSELLES · PIEDS · **MAINS** » | `[cheerful]` / 0,3 / 1,06 |
| 8 | Fin | « Allez, file sous la douche ! Abonne-toi, y'a plein d'autres secrets ! » | « **Abonne**-toi / pour d'autres **secrets** ! » + bouton « S'ABONNER » et cloche | `[excited]` / 0,3 / 1,10 |

≈ 150 mots. `NOMINAL = [2.8, 6.0, 7.0, 6.5, 7.0, 6.5, 6.0, 3.0]` (mis à l'échelle sur la voix réelle).

**Coût** : environ 1 050 caractères, balises comprises.

**Si la vidéo dépasse 55 s**, couper dans cet ordre : « Ton aisselle devient leur buffet à volonté. » puis « Tu serais le seul à ne rien sentir. »

## B3. Exactitude
- **Sueur inodore** : vrai. La sueur fraîche (eccrine et apocrine) ne sent presque rien ; l'odeur vient de bactéries cutanées (*Corynebacterium*, *Staphylococcus hominis*) qui transforment certains composés en thioalcools et acides gras volatils.
- **« Buffet à volonté »** : image, pas un terme scientifique.
- **30 000 cellules par minute** : ordre de grandeur couramment cité (30 000 à 40 000 cornéocytes par minute). Simplification assumée.
- **« Comme de la pâte »** : image. Le mélange réel est sébum + cornéocytes + sueur + poussière.
- **Croûte brune** : la *dermatite négligée* (dermatitis neglecta) existe ; plaques brunâtres de kératine et de sébum, qui partent au lavage. Délai variable (semaines à mois) : « en quelques semaines » reste prudent.
- **Champignons dans les plis** : les mycoses (intertrigo, candidose, pied d'athlète) sont favorisées par la chaleur et l'humidité des plis. On ne montre pas de photo médicale, seulement des champignons « mignons ».
- **« Tout le monde te fuit »** : effet comique, pas une donnée.
- **Le nez s'habitue** : vrai, adaptation olfactive ; on cesse de percevoir une odeur constante en quelques minutes.
- **Pas de douche quotidienne obligatoire** : avis courant des dermatologues ; lavage ciblé des zones à odeur et lavage des mains (geste clé contre la transmission des microbes).
- On **ne montre pas** : lésions réalistes, parasites, conseils médicaux chiffrés.

## B4. Mise en scène
1. **Accroche — salle de bain** *(Pip : utiliser_objet)*
   - Image déjà en mouvement : la douche coule, Pip (bonnet de douche) ferme le robinet ; les gouttes s'arrêtent net.
   - Titre « UN AN SANS DOUCHE ? » avant 0,5 s, « UN AN » qui tremble.
   - Sur « quoi » : calendrier qui s'emballe (J+1 → J+365). Bruitage : grincement de robinet, plic.
2. **Déclic — vue loupe sur la peau** *(Pip : réagir)*
   - Sur « sueur » : gouttes bleues brillantes + badge « 0 ODEUR ».
   - Sur « bactéries » : Bacto et ses copines arrivent et croquent les gouttes ; sur « puent » : nuages verts, titre « ÇA PUE ! » qui tremble ; Pip, dans le coin, se bouche le nez.
   - Sur « buffet » : panneau « BUFFET » au-dessus des bactéries. Bruitages : slurp, prout-nuage.
3. **Mécanisme — coupe de peau en accéléré** *(Pip absent)*
   - Coupe en couches ; pellicules qui se détachent ; compteur « 30 000 / MIN ».
   - Sur « sébum » : gouttes jaunes qui collent les pellicules.
   - Sur « semaines » : badge ×1000, chrono J+1 → J+30, la couche brune grossit. Bruitage : tic-tac rapide.
4. **Rebondissement — un pli de peau** *(Pip : subir)*
   - Musique en sourdine pendant le chuchotement.
   - Sur « champignons » : champignons violets qui poussent en « pop » successifs, jusque sur le bonnet de Pip.
   - Sur « gratte » : points rouges qui clignotent, Pip se gratte frénétiquement ; titre « MYCOSES ».
5. **Réponse — rue vide** *(Pip : réagir)*
   - Coupure musicale 0,5 s avant « Tu survis » ; ding + titre « TU SURVIS ».
   - Sur « fuit » : silhouettes grises qui détalent hors champ ; une boule d'herbe traverse ; Pip, seul, cligne des yeux.
6. **Objection — écran partagé** *(Pip : agir_corps)*
   - Gauche « TOI » : Pip renifle son aisselle, cœurs. Droite « LES AUTRES » : silhouette avec pince à linge et nuage vert.
   - Sur « Non » : buzzer + « NON ! ». Jauge « nez » qui descend de 100 % à 0 %.
7. **Conseil — liste savon** *(Pip absent)*
   - Une savonnette glisse et coche « AISSELLES », « PIEDS », puis « MAINS » (mot-choc, bulles).
   - Les microbes sur la main éclatent en bulles. Bruitage : pop-bulles.
8. **Fin — salle de bain** *(Pip : agir_corps)*
   - Retour au décor de l'accroche (boucle) : la douche se rallume.
   - Pip saute sur « S'ABONNER », cloche 8 bits.

**Bruitages propres au sujet** : grincement de robinet, plic d'eau, slurp, nuage-prout, pop champignon, gratte-gratte, pop bulles, souffle de vent (boule d'herbe).

## B5. Table `PIP_ACTIONS`
```python
PIP_ACTIONS = {
    1: ("utiliser_objet", "ferme le robinet"),
    2: ("reagir", "se bouche le nez"),
    3: None,
    4: ("subir", "envahi par les champignons, se gratte"),
    5: ("reagir", "seul, cligne, boule d'herbe"),
    6: ("agir_corps", "renifle son aisselle"),
    7: None,
    8: ("agir_corps", "saute sur le bouton S'ABONNER"),
}
```
