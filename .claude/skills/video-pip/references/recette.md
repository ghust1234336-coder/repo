# Partie A — Recette commune

## A0. Leçons des épisodes précédents
| Épisode | Ce qui a marché | Ce qui a ralenti |
|---|---|---|
| Anesthésie | Chaque scène répond à la question « pourquoi tu ne sens rien ? ». Le fil ne casse jamais : message → portes → portes bouchées → cerveau en pause → objection → fait fou. | — |
| Mouche | Le hook (tapette + ralenti), le « BEURK », le verdict « NON ! ». | **Scène 2 (« elle goûte avec ses pieds »)** |
| Lune (style Vox) | **Le collage papier** : vraies photos NASA découpées, surligneur jaune, feutre rouge. **Les graphiques tracés au trait** (courbe de marée « ratée », inclinaison de l'axe, barres, balance) rendent un fait chiffré visible en 2 s. Le mot-choc qui disparaît lettre à lettre. | Le « NON ! » crié + grand tampon rouge, trop appuyé (règle A4). Titres placés sous la barre de progression (à garder sous y = 300). |
| Douche (v2) | **La chronologie par étapes** (Jour 2 → 1 mois → 3 mois → 1 an) : le spectateur sait où il en est et attend l'étape suivante. **Une réaction des gens à la fin de chaque étape** (collègues, bus, potes, chat) : gag + enjeu personnel. Tampon plein écran + barre de progression. | v1 sans étapes : bonnes infos mais pas de sensation de progression. |
| Moustiques (style Vox) | **Une vraie photo détourée devenue personnage** (moustique CDC + deux yeux en papier collés). Les chiffres en objets (7 stades qui se remplissent, planche de 3 500 cases). Le mot-choc dont les lettres s'envolent comme des moustiques. La fin en boucle avec une loupe (« c'est un mâle »). | Première prise de voix à 59 s : il a fallu fusionner deux phrases et passer toute la voix à 1,10. **Garder une marge sous 60 s.** Les scènes « réponse » avec une pause dramatique passent sous 2,8 mots/s. |

**Pourquoi la scène des pieds ralentit :**
1. **Elle ne fait pas avancer la question du titre.** « Tu la jettes ? » n'a pas de lien avec le goût des pieds. Le spectateur sent un détour, alors qu'il attend la réponse.
2. **Elle répète une info.** « Elle se pose… et elle sait déjà si c'est bon » redit la phrase précédente. Une deuxième phrase sans info nouvelle sonne comme du remplissage.
3. **Le gag arrive après la voix au lieu d'être en même temps.** Pip qui retire sa chaussure puis grimace demande 2 à 3 s d'action pendant lesquelles rien de neuf n'est appris.
4. **Les points de suspension** (« Elle se pose… ») ajoutent des pauses à un moment où il n'y a pas de suspense à créer.

**Règles qu'on en tire** (vérifiées en A8) :
- **R1. Chaque scène fait avancer la question du titre.** Un fait amusant qui ne la sert pas est soit relié à la question par une phrase-pont (« …et c'est justement ce qui pose problème »), soit coupé.
- **R2. Une phrase = une info nouvelle.** Pas de reformulation.
- **R3. Les gags se jouent pendant la voix**, jamais après. Un gag dure au plus 1,5 s sans voix.
- **R4. « … » seulement là où on crée du suspense**, une fois par scène au plus, et jamais deux scènes de suite.

## A1. Format
| Élément | Valeur |
|---|---|
| Image finale | vertical 1080×1920, 30 fps, dessinée directement à cette taille (anticrénelée, sans agrandissement) |
| Durée | **60 s maximum**, pas de durée cible |
| Débit de voix | 3,2 à 3,6 mots/s en moyenne, vitesse 1,10 comprise. **Pas de budget de mots** : autant de mots que la vidéo en a besoin, et pas un de plus (R2). Seule limite : la durée estimée (mots ÷ 3,4) reste sous 60 s |
| Outil | moteur Python maison `vox.py` (Pillow + numpy → ffmpeg), rendu sur 4 processus |
| Langue | français, tutoiement |
| Polices (OFL, dans `assets/`) | Work Sans Bold (titres, sous-titres), DM Mono (étiquettes, barre, tampons), Libre Baskerville (journal), Nothing You Could Do (manuscrit) |

## A2. Style visuel — collage papier façon Vox
Le style convient à tous les sujets, et surtout à ceux qui gagnent à montrer de vraies images et des graphiques (science, espace, nature, histoire, chiffres). Le moteur est `lune/vox.py`.

| Élément | Version Vox |
|---|---|
| Fond | papier texturé (crème `#efe8dc` ou bleu nuit `#121a2e` / `#1f2b4a`), généré par bruit basse fréquence + fibres ; **grain de film** à 12 i/s et vignette légère (12 %) posés à la toute fin (`finish()`) |
| Découpages | chaque objet est un `Sprite` : **bord blanc aux ciseaux** (10–12 px) + ombre portée floue décalée (10, 16) ; petit tremblement d'angle (`boil`, ±0,5°, 8 i/s) façon stop motion |
| Vraies images | photos **du domaine public** (NASA, NOAA, CDC, USFWS, archives libres), téléchargées dans `assets/src/`, découpées en disque, en silhouette (fond uni → détourage par couleur, voir `moustiques/make_cutouts.py`) ou en carte photo à bord blanc ; crédit obligatoire dans la description. Jamais d'image sous licence restrictive (CC BY-SA comprise) : à la place, une illustration. |
| Illustrations | aplats simples dessinés en vectoriel (suréchantillonnage ×2–3 puis réduction), sans contour noir ; silhouettes sombres pour la nuit |
| Titres | bande de papier blanc qui tombe avec un rebond (`title()`), légère rotation (±1,5°), **mot-clé passé au surligneur jaune** (`#ffe14d`) qui s'étale de gauche à droite |
| Annotations | **feutre rouge** (`#e8402f`) qui se dessine : cercle à main levée, flèche, croix ; **écriture manuscrite** qui apparaît lettre à lettre |
| Données | **graphiques tracés au trait** (courbe noire = normal, courbe rouge = ce qui change), barres, balance, règle, compteur ; étiquettes en police mono sur fond jaune ; un chiffre abstrait devient des objets (stades, cases, silhouettes) |
| Archives | coupure de journal (titre en serif, colonnes en traits gris) pour une réaction ou une idée reçue |
| Sous-titres | bande blanche, Work Sans Bold 66 px en capitales, **le mot en cours passé au surligneur** (karaoké, comme dans les Shorts à forte rétention) |
| Caméra | zoom lent façon banc-titre (+3,5 % par scène), mouvements continus autorisés |
| Transitions | entre scènes : **volet « papier déchiré »** (0,45 s) ; entre plans : coupes franches (C6) |
| Pip | **découpage papier** (aplats, ombre en croissant, bord blanc) ; le costume se pose par-dessus le découpage (bulle de casque, chapeau…) |
| Glyphes | **vérifier les caractères** : DM Mono n'a pas « → » ni « ⁶ » ; Nothing You Could Do n'a ni « → » ni « ≈ ». Work Sans Bold a les deux. |

- Le **mot-choc** de l'épisode a son propre effet (lettres qui s'envolent, disparaissent, tremblent…).
- **Changement visuel au moins toutes les 2 s** : nouveau plan, nouvel objet, mouvement de caméra, titre, annotation ou réaction de Pip. C'est le principal levier de rétention du format court.

Mise en page (1080×1920) : barre de progression y 40–170, **titres à partir de y = 300**, scène principale y 450–1450, sous-titres y 1526–1626 ; rien d'important sous y = 1650 (interface des Shorts) **ni dans la colonne de droite x > 940 entre y = 900 et 1650** (boutons like / commentaire / partage de TikTok et Reels ; valeur approximative, à vérifier sur une capture). Pip ≤ 15 % de la largeur, jamais dans la zone des sous-titres.

Tampon de chronologie (C3) : écran assombri, **bandeau papier surligné** qui claque (échelle 1,35 → 1), puis sous-titre tapé à la machine en mono (« T + 6 H »). Barre de progression (C4) : règle papier blanche, points rouges par étape, remplissage au surligneur.

### Variante `flat` (sans collage)
Pour un sujet très « abstrait » (maths, cerveau), un **« flat cartoon »** façon Kurzgesagt (formes rondes, aplats, fond sombre avec lueurs) : même moteur `vox.py`, sans texture papier, sans bord blanc ni photos.

### Le personnage-sujet (optionnel)
Quand le sujet a un « acteur » (un moustique, un virus, une molécule, une planète…), on lui donne une **petite personnalité** (effronté, paresseux, pressé…) et un tic visuel (lever les pattes, cligner, tourner sur lui-même). Il devient le deuxième personnage, et Pip peut s'effacer dans les scènes où il est la star.
- De préférence **une vraie photo détourée** (la Lune NASA, le moustique CDC), avec au plus une touche cartoon collée par-dessus (deux yeux en papier).
- Petits éléments récurrents (microbes, ions, molécules) : découpages ronds aux couleurs vives, avec deux yeux. **Mignons, jamais effrayants.**

### Palette
| Rôle | Couleurs | Fixe ? |
|---|---|---|
| Papier | `#efe8dc` `#ddd2bf` | fixe |
| Encre | `#1b1b1f` | fixe |
| Nuits | `#121a2e` `#1f2b4a` `#33456e` | fixe |
| Surligneur / feutre | `#ffe14d` `#e8402f` | fixe |
| Pip (**orange**) | `#ff9f1c` (corps) `#ff5e3a` (ombre, bras, pieds) `#ff6f91` (joues) `#fff1d6` (ventre crème) `#ffe14d` (boule d'antenne) | fixe |
| **Thème** | **8 à 12 couleurs** choisies pour le sujet (décor, personnage-sujet, éléments) | **à remplir (B0)** |

Pas de quantification : dégradés, flous et transparences sont permis.

## A3. Rythme et transitions
- Une seule timeline, rendu image par image à partir du temps t (`timeline.py` calé sur `audio/timings.json`).
- `SCENE_GAP` = 0,2 s, respiration entre phrases 0,22 s.
- Volet papier déchiré de 0,45 s centré sur la frontière entre deux scènes.
- Titres en bande de papier qui tombe avec un rebond (0,32 s), surligneur 0,15 s après.
- Le **mot-choc** de chaque scène clé arrive **sur le mot lui-même** (liste dans B1).
- **Le son de transition commence 0,1 s avant la coupe** : l'oreille anticipe, la coupe paraît plus vive.

## A4. Voix off — ElevenLabs
### Branchement
- `.env` à la racine avec `ELEVENLABS_API_KEY` et `ELEVENLABS_VOICE_ID` (dans le `.gitignore`). Dans l'environnement cloud, le proxy injecte la clé.
- Le MCP ElevenLabs sert à **choisir et tester la voix** (voix française, chaleureuse et dynamique). Toujours la même voix sur toute la série (Léo, `jsScnYkNNda9Q1NES5nn`).
- `tts.py` génère avec l'API `with-timestamps`, regroupe les caractères en mots et écrit `audio/timings.json`.

### Modèle
- `eleven_v3` par défaut (balises d'émotion entre crochets).
- Repli automatique sur `eleven_multilingual_v2` (balises retirées, intention passée par `style` 0,3–0,6 et la stabilité).
- Dernier recours : audio v3 sans timings, puis alignement des mots avec faster-whisper.
- `language_code="fr"`, `output_format="mp3_44100_128"`, `apply_text_normalization="on"`.

### Règles de génération
- **Une phrase = une synthèse**, avec `previous_text` / `next_text`.
- Seules les balises, la stabilité et la vitesse changent d'une scène à l'autre.
- Post-traitement : silences de bord 0,03 s, silences internes ≤ 0,25 s, −16 LUFS, de-esser léger. Timings recalés après la coupe.
- Vitesse par `atempo` au post-traitement (±10 % au plus ; 1,10 est la valeur habituelle).
- Cache des prises dans `audio/takes/eleven/<voice_id>/` : une phrase déjà générée n'est pas refacturée.
- Secours gratuit : `--henri` (edge-tts), même sortie.
- **Balises** : 1 par phrase au plus, et **pas de `[laughs]` ni de `[sighs]` en milieu de scène explicative** (ils ajoutent 0,4 à 0,8 s de temps mort). Toute balise prononcée ou qui sonne faux est retirée de `ELEVEN_EXPRESSION`.
- **Le « Non » reste sobre** (retour de l'épisode Lune) : quand une phrase commence par « Non » (réponse à une objection, verdict), il est dit **posément**, sans crier ni appuyer. Pas de « Non ! » avec point d'exclamation dans le script : écrire « Non, … » ou « Non. … ». La phrase qui suit porte l'info, pas le « Non ». À l'écran, pas de grand tampon rouge plein écran : une étiquette ou un mot surligné de taille normale suffit.

### Profils d'expressivité par rôle de scène
| Rôle (voir A7) | Intention | Balises (v3) | Stabilité | Vitesse |
|---|---|---|---|---|
| Accroche | intrigant, punchy | `[curious]` / `[dramatic]` pour rire | 0,3 | 1,10 |
| Déclic | surpris, amusé | `[surprised]` | 0,3 | 1,10 |
| Mécanisme | curieux, posé mais vif | `[curious]` | 0,5 | 1,10 |
| Rebondissement | conspirateur | `[whispers]` | 0,5 | 1,10 |
| Réponse | net, rassurant ou malin | `[playful]` | 0,5 | 1,10 |
| Objection | taquin | `[playful]` / `[mischievously]` | 0,3 | 1,10 |
| Le plus fou / conseil | émerveillé ou complice | `[excited]` / `[cheerful]` | 0,3 | 1,10 |
| Fin | énergique | `[excited]` | 0,3 | 1,10 |

## A5. Musique et bruitages (`sfx.py`)
Tout est synthétisé en numpy (original, libre de droits).
- **Musique « documentaire »** : pad doux + arpège pincé + grosse caisse douce et charleston, 108 à 116 BPM, mineur → majeur sur la fin. Tonalité et ambiance choisies par épisode (B0). −16,5 dB sous la voix.
  - **Coupure musicale** (la musique se tait 0,5 s) juste avant la réponse principale : effet « silence avant la révélation ».
  - **Sourdine** (×0,45) pendant le chuchotement du rebondissement.
- **Communs à tous les épisodes** : sons papier (feuille qui glisse pour les transitions, machine à écrire, coup de tampon, feutre, ciseaux), whoosh (coupes), pop (titres et objets), ding (bonne réponse), buzzer doux, compteur, tic-tac, boing + bonk (Pip qui saute), cloche (« S'ABONNER »).
- **Propres au sujet** : 4 à 8 bruitages listés dans B4, chacun calé sur un moment fort (`timeline.events()`).

## A6. Pip, un personnage qui vit dans la scène
### Le sprite (`pip_vox.py`)
- Découpage papier d'environ 250×300 px : **petite créature ronde orange**, ventre crème, joues roses, antenne à boule jaune, grands yeux, clignement, respiration, ombre en croissant, bord blanc (couleurs : palette A2).
- **Un accessoire de costume par épisode** lié au sujet (casque d'astronaute, chapeau d'explorateur à moustiquaire, blouse, lunettes de plongée…).
- Poses : repos, montrer du doigt, surprise, content, saut, course, perte d'équilibre, tenir un objet ; humeurs : sourire, bouche ouverte, inquiet. Les poses vivent à 12 images/s (stop motion), les déplacements à 30 images/s.

### Catalogue d'interactions
| Famille | Exemples |
|---|---|
| **Se déplacer dans le décor** | courir, glisser en luge, sauter d'un élément à l'autre, être transporté par un flux |
| **Subir la scène** | être emporté, perdre l'équilibre, être envahi, s'endormir |
| **Agir avec le corps** | sauter à pieds joints sur un bouton ou un plateau, pousser, toucher, souffler |
| **Utiliser un objet du décor** | tenir une baguette magique, regarder au télescope, attendre avec une bouée, brandir une loupe |
| **Réagir** | sursaut, « ! » au-dessus de la tête, yeux en étoiles, yeux seuls dans le noir |

### Règles
1. **Pip seulement s'il apporte quelque chose** (compréhension ou gag). Il est **absent d'au moins 2 scènes**, en général le mécanisme et le « plus fou ».
2. **Jamais la même famille d'interaction** dans deux scènes qui se suivent.
3. **Le gag de Pip illustre le fait dit dans la phrase en cours** (règle R3) : il ne crée pas d'action supplémentaire qui demanderait du temps.
4. Pip est toujours **dans le décor**, jamais centré au premier plan devant ce qu'on explique.
5. Il ne recouvre jamais un titre, un sous-titre, le personnage-sujet ou l'élément expliqué.
6. Il occupe au plus 15 % de la largeur de l'écran, sauf pendant les gags où il est en mouvement.

## A7. Structure de rétention (le squelette de tous les épisodes)
Construite sur le principe « **mais / donc** » : chaque scène commence par une raison de continuer (« Sauf que… », « Mais alors… », « Résultat : … »), jamais par « et aussi… ».

| # | Rôle | Ce que la scène doit faire | Pip | Durée cible |
|---|---|---|---|---|
| 1 | **Accroche** | Situation concrète que tout le monde connaît + **question du titre** posée avant 3 s. Image déjà en mouvement. | en action dès la 1re seconde | 2,5–3 s |
| 2 | **Déclic** | Le fait-clé qui change le regard sur la question, en **une image mentale** (comparaison du quotidien). | oui | 5–6 s |
| 3 | **Mécanisme** | Montrer « comment ça marche » en coupe annotée, schéma, loupe ou graphique. L'animation parle seule. | **absent** | 6–7 s |
| 4 | **Rebondissement** (≈ 40 % de la vidéo) | « Sauf que… » : une idée reçue cassée ou un détail inattendu. **Relance** l'attention au milieu. | oui (subit la scène) | 6–7 s |
| 5 | **Réponse** | Réponse **nette** à la question du titre, mot-choc sur le mot. Coupure musicale juste avant. | oui ou absent | 7–8 s |
| 6 | **Objection** | « Mais alors… ? » : la question que le spectateur se pose à ce moment-là, avec une démonstration visuelle (écran partagé, comparaison). Le « Non » de la réponse reste sobre (voir A4). | oui | 7–8 s |
| 7 | **Le plus fou / conseil** | Un fait final qui donne envie de le raconter à quelqu'un, **ou** le conseil pratique qu'on retient. | absent ou réagit | 5–7 s |
| 8 | **Fin** | Phrase courte qui **renvoie à l'accroche** (boucle : la dernière image ressemble à la première, pour le revisionnage) + abonnement en 1,5–2 s. | saute sur le bouton | 2–2,5 s |

Les scènes 6 et 7 peuvent être fusionnées si le sujet est simple (7 scènes au total). On ne descend jamais sous 7 scènes, et on ne dépasse jamais 8.

### Variante « chronologie » (sujets du type « que se passe-t-il si… pendant X ? »)
Validée sur les épisodes douche et Lune. À utiliser dès que le sujet **évolue dans le temps** (un an sans dormir / sans sucre / sans téléphone, un corps dans l'espace, une plante sans eau…).

| # | Rôle | Contenu |
|---|---|---|
| 1 | Accroche | La situation + la question (« Tu arrêtes X pendant un an. Il se passe quoi ? ») |
| 2 | Étape 1 (court terme : heures / jours) | 1 à 2 phrases sur le corps ou l'objet + **1 phrase de réaction sociale** |
| 3 | Étape 2 (≈ 1 mois) | idem — c'est l'étape « mécanisme » (coupe, schéma, graphique) |
| 4 | Étape 3 (≈ 3 mois) | idem — commence par « Sauf qu'à… » (rebondissement, ≈ 40 % de la vidéo) |
| 5 | Étape 4 (fin de la période) | la **réponse nette** au titre (coupure musicale avant) + la réaction sociale la plus forte, en gag final (« même ton chat fait ses valises ») |
| 6 | Objection | « Mais alors… ? » |
| 7 | Conseil | ce qu'on retient |
| 8 | Fin | boucle vers l'accroche + abonnement |

Règles propres à la chronologie :
- **C1. 3 ou 4 étapes**, jamais plus (au-delà, la vidéo dépasse 60 s). Étapes de durée croissante : jours → mois → année.
- **C2. Chaque étape commence par son repère de temps** dit à voix haute, en premier mot (« Jour deux : … », « Un mois : … », « Sauf qu'à trois mois… », « Un an plus tard ? »).
- **C3. Tampon plein écran** sur ce repère (voir A2) : écran assombri, bandeau papier surligné qui claque, sous-titre à la machine à écrire, bruitage « stamp ». Il dure du premier mot du repère jusqu'à 0,25 s après la fin du repère.
- **C4. Barre de progression** en haut de l'écran pendant toutes les étapes (J0 → fin, un repère par étape, remplissage au surligneur), avec le libellé de chaque étape dessous (32 px au moins). Les titres des scènes restent sous y = 300.
- **C5. Une réaction sociale par étape**, en dernière phrase, avec son propre plan du quotidien (bureau, bus, téléphone, rue, coupure de journal…). Elle est **de plus en plus forte** d'une étape à l'autre. Les gens sont des silhouettes grises simples ; leur réaction se lit en un geste (reculer, « ! », fuite, fête).
- **C6. Coupes franches entre les plans d'une même étape**, calées sur le début de la phrase, avec un whoosh 0,08 s avant. Le volet papier déchiré reste réservé aux changements de scène.
- **C7. L'état de Pip empire d'une étape à l'autre** : on voit le temps passer sur lui.
- **C8. Pip joue « toi »** : il peut être présent à chaque étape. Dans ce cas, la règle A6-1 devient « absent d'au moins une scène entière **et** de plusieurs plans ».
- Budget : pas de limite de mots, 60 s maximum. Si ça dépasse, couper d'abord une phrase « corps » secondaire, jamais une réaction sociale ni un repère de temps.

### Règles du hook
1. Pas d'intro : la première image est déjà en mouvement.
2. Titre-question à l'écran avant 0,5 s.
3. Voix à 0,1 s, question posée avant 3 s.
4. Pip visible et en action dans la première seconde.
5. Phrase qui intrigue, et non une phrase qui demande de rester (« reste jusqu'à la fin » est interdit).
6. Le hook contient **un paradoxe ou un enjeu personnel** (« on t'opère et tu ne sens rien », « une mouche sur TA pizza », « tu as une baguette qui efface les moustiques »), jamais une définition.

### Règles d'écriture du script
- Phrases de **12 mots au plus**, vocabulaire de collégien, tutoiement.
- **Une phrase = une info nouvelle** (R2) et une image nouvelle à l'écran.
- **Au moins une comparaison du quotidien** par notion abstraite (« comme des dominos », « un taxi à microbes », « appuie sur les freins »).
- **Au moins un chiffre concret** dans la vidéo (date, nombre, durée), lu en toutes lettres.
- **Boucle ouverte** : la scène 2 ou 4 annonce discrètement qu'il reste quelque chose (« Mais le vrai problème, c'est pas ça. »), sans dire « reste ».
- **Pas de liste** (« premièrement, deuxièmement ») à l'oral : la structure se lit à l'écran.
- Mots interdits : « en fait », « donc voilà », « il faut savoir que », « comme on l'a vu ».
- Le mot-choc de la scène est le **dernier mot** de sa phrase, pour que le titre tombe pile dessus.

## A8. Vérifications (`snap.py`)
1. Plus grand blanc dans la voix ≤ 0,30 s.
2. Hook ≤ 3,0 s.
3. `ffprobe` : 1080×1920, 30 fps, une piste audio, ≤ 60 s.
4. `silencedetect` (−50 dB, 0,3 s) : aucun silence.
5. **Glyphes** : aucun caractère manquant (carré vide) dans les textes à l'écran, police par police.
6. **Poids** : vidéo finale < 100 Mo (limite GitHub ; le grain gonfle le fichier : encoder en `-crf 24 -preset slow`, ≈ 45 Mo pour 56 s).
7. **Placement** : la boîte de Pip ne chevauche jamais un titre, un sous-titre, le personnage-sujet ou l'élément cible ; rien d'important sous y = 1650 ni dans la colonne de droite (x > 940, y 900–1650).
8. **Variété** (table `PIP_ACTIONS` du script d'épisode) :
   - Pip absent d'au moins 2 scènes ;
   - jamais la même famille d'interaction dans deux scènes qui se suivent.
9. **Voix** : aucune balise `[...]` dans les sous-titres ni dans `timings.json`, aucune balise prononcée, chiffres lus en toutes lettres.
10. **Rythme** :
    - aucun plan fixe de plus de 2,0 s sans changement visuel ;
    - aucun gag sans voix de plus de 1,5 s ;
    - débit moyen entre 3,2 et 3,6 mots/s, et aucune scène sous 2,8 mots/s (c'est là que la vidéo mouche ralentissait) ;
    - « … » au plus une fois par scène.
11. **Fil** (relecture humaine) : pour chaque scène, compléter la phrase « Cette scène rapproche de la réponse à *<question du titre>* parce que… ». Si on ne trouve pas, la scène est réécrite ou coupée (R1).
12. **Chronologie** (si variante utilisée) : chaque étape a son repère de temps en premier mot, son tampon, et une réaction sociale en dernière phrase ; la barre de progression est visible de la 1re à la dernière étape.
13. **Images** : chaque photo vient du domaine public, avec son crédit dans `description.md`.

