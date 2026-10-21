# Plan maître — vidéos courtes « Comprendre un truc en 50 s » avec Pip

> **À quoi sert ce fichier** : c'est la base commune de toutes les vidéos. Pour un nouvel épisode, tu donnes seulement un **sujet**, et Claude remplit le **gabarit de la Partie B**. Le résultat est un `plan_<sujet>_pixel.md` complet, au même format que les plans « anesthésie » et « mouche ».
>
> **Prompt à utiliser :**
> ```
> Sujet : <ton sujet>
> (Claude peut réécrire le sujet ou le titre s'il trouve mieux : voir Partie D, étape 0.)
> Utilise plan_maitre_video.md pour écrire plan_<slug>_pixel.md (Partie B remplie, Partie A reprise sans changement sauf la palette thématique et les bruitages).
> ```
>
> **Ce qui change par rapport aux plans précédents :**
> 1. **Le script suit une structure de rétention** inspirée des chaînes de vulgarisation courtes (Kurzgesagt, TED-Ed, Dr Nozman, Scilabus, Veritasium Shorts) : une question qui reste ouverte, un enchaînement « mais / donc », une relance au milieu et une réponse nette à la fin.
> 2. **Une règle anti-temps mort**, tirée de la scène « elle goûte avec ses pieds » de la vidéo mouche (voir A0).
> 3. **Le style pixel art HD est conservé** : les deux vidéos ont marché, le moteur `pixel.py` existe déjà, et le style se reconnaît dans le fil. Une option pour faire varier le style est décrite en A2.

- **Partie A** : la recette commune (ne change pas d'un épisode à l'autre).
- **Partie B** : le gabarit d'épisode, à remplir à partir du sujet.
- **Partie C** : les fichiers et la marche à suivre.
- **Partie D** : la procédure que Claude suit pour générer un plan à partir d'un sujet.

---

# Partie A — Recette commune

## A0. Leçons des épisodes précédents
| Épisode | Ce qui a marché | Ce qui a ralenti |
|---|---|---|
| Anesthésie | Chaque scène répond à la question « pourquoi tu ne sens rien ? ». Le fil ne casse jamais : message → portes → portes bouchées → cerveau en pause → objection → fait fou. | — |
| Mouche | Le hook (tapette + ralenti), le « BEURK », le verdict « NON ! ». | **Scène 2 (« elle goûte avec ses pieds »)** |
| Douche (v2) | **La chronologie par étapes** (Jour 2 → 1 mois → 3 mois → 1 an) : le spectateur sait où il en est et attend l'étape suivante. **Une réaction des gens à la fin de chaque étape** (collègues, bus, potes, chat) : gag + enjeu personnel. Tampon plein écran + barre de progression. | v1 sans étapes : bonnes infos mais pas de sensation de progression. |

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
| Image finale | vertical 1080×1920, 30 fps |
| Canevas pixel | **360×640** pixels « art », agrandis ×3 au plus proche voisin (1 pixel art = un bloc 3×3) |
| Durée | ≈ 50 s (cible 42–55 s, **60 s maximum**) |
| Débit de voix | 3,2 à 3,6 mots/s en moyenne, soit environ **150 à 170 mots** pour tout le script |
| Outil | moteur Python maison (Pillow + numpy → ffmpeg). Pas de Manim, qui lisse les bords. |
| Langue | français, tutoiement |
| Police | *Pixelify Sans* (Google Fonts, licence libre), rendue **sans anticrénelage** |

## A2. Style visuel — pixel art HD, version « cartoon »
Règle d'or : **chaque bloc 3×3 de l'image finale a une seule couleur**, et toutes les couleurs viennent de la palette. Pas de flou, pas de dégradé lisse, pas de demi-pixel.

| Effet | Version pixel |
|---|---|
| Fond | Bandes de couleurs de la palette, raccordées par un **tramage de Bayer 4×4** |
| **Effet macro / plongée** | Pour « zoomer », on **change de plan** avec un décor redessiné en grand (pas de zoom continu). Un cercle de vignette noir tramé fait « loupe ». |
| **Ralenti** | Décor à 6 images/s, traînées de mouvement en 3 copies tramées, badge « ×0,1 » dans un coin |
| **Accéléré** | Chrono pixel qui défile, poses tenues 1 image, badge « ×1000 » |
| Glow | Halo tramé de 1 à 2 pixels, à 2 ou 3 teintes |
| Ombres | Ombre d'une seule couleur, décalée de 2 pixels |
| Particules | Poussières de 1 pixel qui scintillent, « lucioles » de 2×2 en parallaxe |
| Contours | Contour sombre de 1 pixel, plus clair côté lumière (*selout*) |
| Caméra vivante | Déplacements par **pas entiers de 1 pixel**, dérive de ±1 pixel |
| Transitions | Volet en mosaïque (blocs de 8 pixels), dissolution en damier, « plongée pixel » (×8 puis reconstruction), ou **l'élément star traverse l'écran** et « essuie » l'ancien plan |

- Poses à **12 images/s**, déplacements et caméra à 30 images/s.
- Titres : 22 à 28 pixels art de haut, contour bleu nuit de 1 pixel, mots-clés en couleur. Le **mot-choc** de l'épisode a son propre effet (goutte qui coule, tremblement, clignotement…).
- Sous-titres : 12 pixels art, blancs avec contour noir de 1 pixel, en groupes de 24 caractères au plus. **Le mot en cours de lecture est surligné** dans la couleur d'accent (style karaoké, comme dans les Shorts à forte rétention).
- **Changement visuel au moins toutes les 2 s** : nouveau plan, nouvel objet, mouvement de caméra, titre, ou réaction de Pip. C'est le principal levier de rétention du format court.

### Option de style (si tu veux varier)
Le pixel art HD reste le style par défaut. Pour un sujet très « abstrait » (cosmos, maths, cerveau), un style **« flat cartoon » vectoriel** façon Kurzgesagt (formes rondes, aplats, ombres en une teinte, fond sombre avec lueurs) peut mieux passer. Le même moteur suffit : on garde la palette et la timeline, mais on dessine à 1080×1920 avec l'anticrénelage de Pillow, et on enlève le test « grille pixel » de A8. À décider au cas par cas dans le plan d'épisode (ligne `STYLE` du tableau B0).

### Le personnage-sujet (optionnel)
Quand le sujet a un « acteur » (une mouche, un virus, une molécule, une planète…), on lui donne une **petite personnalité** (effronté, paresseux, pressé…) et un tic visuel (se frotter les pattes, cligner, tourner sur lui-même). Il devient le deuxième personnage, et Pip peut s'effacer dans les scènes où il est la star.
- Sprite d'environ 20×16 pixels en vue normale, et de 120×100 en vue macro.
- Petits éléments récurrents (microbes, ions, molécules) : boules de 4 à 6 pixels aux couleurs bonbon, avec deux yeux. **Mignons, jamais effrayants.**

### Palette (24 couleurs, tout est quantifié dessus)
| Rôle | Couleurs | Fixe ? |
|---|---|---|
| Neutres | `#ffffff` `#0a0a12` | fixe |
| Nuit / UI / contours | `#1b1838` `#2c2a5a` `#3d4f8f` | fixe |
| Accent titres | `#ffd23f` `#e8333a` | fixe |
| Pip | 3 couleurs au plus, ramenées à la teinte la plus proche | fixe |
| **Thème** | **14 couleurs** choisies pour le sujet (décor, personnage-sujet, éléments) | **à remplir (B0)** |

Un flash-back éventuel utilise une sous-palette de 6 teintes sépia.

## A3. Rythme et transitions
- Une seule timeline, rendu image par image à partir du temps t.
- `SCENE_GAP` = 0,2 s, respiration entre phrases 0,22 s.
- `OVERLAP` = 0,6 s, `TRANSITION_EXTRA` = +0,1 s.
- Titres en rebond par pas de pixel entiers, avec un écrasement de 2 pixels à l'atterrissage.
- Le **mot-choc** de chaque scène clé arrive **sur le mot lui-même** (liste dans B1).
- **Le son de transition (whoosh) commence 0,1 s avant la coupe** : l'oreille anticipe, la coupe paraît plus vive.

## A4. Voix off — ElevenLabs
### Branchement
- `.env` à la racine avec `ELEVENLABS_API_KEY` et `ELEVENLABS_VOICE_ID` (dans le `.gitignore`).
- Le MCP ElevenLabs sert à **choisir et tester la voix** (voix française, chaleureuse et dynamique). Toujours la même voix sur toute la série.
- `tts.py` génère avec `text_to_speech.convert_with_timestamps`, regroupe les caractères en mots et écrit `audio/timings.json`.

### Modèle
- `eleven_v3` par défaut (balises d'émotion entre crochets).
- Repli automatique sur `eleven_multilingual_v2` (balises retirées, intention passée par `style` 0,3–0,6 et la stabilité).
- Dernier recours : audio v3 sans timings, puis alignement des mots avec faster-whisper.
- `language_code="fr"`, `output_format="mp3_44100_128"`, `apply_text_normalization="on"`.

### Règles de génération
- **Une phrase = une synthèse**, avec `previous_text` / `next_text`.
- Seules les balises, la stabilité et la vitesse changent d'une scène à l'autre.
- Post-traitement : silences de bord 0,03 s, silences internes ≤ 0,25 s, −16 LUFS, de-esser léger. Timings recalés après la coupe.
- Si `speed` n'est pas accepté : `atempo` au post-traitement (±10 % au plus).
- Cache des prises dans `audio/takes/eleven/<voice_id>/` : une phrase déjà générée n'est pas refacturée.
- Secours gratuit : `--henri` (edge-tts), même sortie.
- **Balises** : 1 par phrase au plus, et **pas de `[laughs]` ni de `[sighs]` en milieu de scène explicative** (ils ajoutent 0,4 à 0,8 s de temps mort). Toute balise prononcée ou qui sonne faux est retirée de `ELEVEN_EXPRESSION`.
- **Le « Non » reste sobre** (retour de l'épisode Lune) : quand une phrase commence par « Non » (réponse à une objection, verdict), il est dit **posément**, sans crier ni appuyer. Pas de « Non ! » avec point d'exclamation dans le script : écrire « Non, … » ou « Non. … ». La phrase qui suit porte l'info, pas le « Non ». À l'écran, pas de grand tampon rouge plein écran : une étiquette ou un mot surligné de taille normale suffit.

### Profils d'expressivité par rôle de scène
| Rôle (voir A7) | Intention | Balises (v3) | Stabilité | Vitesse |
|---|---|---|---|---|
| Accroche | intrigant, punchy | `[curious]` / `[dramatic]` pour rire | 0,3 | 1,10 |
| Déclic | surpris, amusé | `[surprised]` | 0,3 | 1,08 |
| Mécanisme | curieux, posé mais vif | `[curious]` | 0,45 | 1,06 |
| Rebondissement | conspirateur | `[whispers]` sur 2–4 mots | 0,4 | 1,05 |
| Réponse | net, rassurant ou malin | `[playful]` | 0,5 | 1,05 |
| Objection | taquin | `[playful]` / `[mischievously]` | 0,3 | 1,06 |
| Le plus fou / conseil | émerveillé ou complice | `[excited]` / `[cheerful]` | 0,3 | 1,06 |
| Fin | énergique | `[excited]` | 0,3 | 1,10 |

## A5. Musique et bruitages (`sfx.py`), version chiptune
Tout est synthétisé en numpy (original, libre de droits).
- **Musique** : chiptune avec mélodie en onde carrée, basse en triangle et percussions en bruit blanc. 116 à 126 BPM, tonalité et ambiance choisies par épisode (B0). −16,5 dB sous la voix.
  - **Coupure musicale** (la musique se tait 0,5 s) juste avant la réponse principale : effet « silence avant la révélation ».
  - Pendant un **ralenti**, la musique ralentit et baisse d'une octave ; pendant un **accéléré**, elle monte d'une octave.
- **Communs à tous les épisodes** : whoosh (transitions), pop (bulles et titres), ding (bonne réponse), buzzer (mauvaise réponse), tic-tac rapide (accéléré), bonk + boing (Pip qui se cogne), cloche 8 bits (« S'ABONNER »).
- **Propres au sujet** : 4 à 8 bruitages listés dans B4, chacun calé sur un moment fort.

## A6. Pip, un personnage qui vit dans la scène
### Le sprite
- Environ 32×40 pixels art : antenne, grands yeux, clignement, respiration de 1 pixel, antenne qui ondule.
- **Un accessoire de costume par épisode** lié au sujet (tablier, blouse, casque, lunettes de plongée…).
- Poses à 12 images/s : repos, marche, course, saut, glissade, chute, écrasement, surprise, applaudir, bâiller, dormir, grimace, se boucher le nez, se secouer (danse), manger, yeux en étoiles, clin d'œil, s'éventer, se gratter la tête, montrer du doigt.

### Catalogue d'interactions
| Famille | Exemples |
|---|---|
| **Se déplacer dans le décor** | courir, glisser en toboggan, sauter d'un élément à l'autre, être transporté par un flux |
| **Subir la scène** | être emporté, s'écraser contre un obstacle, être envahi, s'endormir, perdre l'équilibre |
| **Agir avec le corps** | sauter à pieds joints sur un bouton, pousser, toucher, goûter, souffler |
| **Utiliser un objet du décor** | tenir une tapette, sonner un réveil, poser une cloche, brandir une loupe |
| **Réagir** | sursaut, « ! » au-dessus de la tête, yeux en étoiles, grimace, s'éventer, se gratter la tête |

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
| 3 | **Mécanisme** | Montrer « comment ça marche » en vue macro, coupe, plongée ou ralenti. L'animation parle seule. | **absent** | 6–7 s |
| 4 | **Rebondissement** (≈ 40 % de la vidéo) | « Sauf que… » : une idée reçue cassée ou un détail inattendu. **Relance** l'attention au milieu. | oui (subit la scène) | 6–7 s |
| 5 | **Réponse** | Réponse **nette** à la question du titre, mot-choc sur le mot (« NON ! », « PAUSE »…). Coupure musicale juste avant. | oui ou absent | 7–8 s |
| 6 | **Objection** | « Mais alors… ? » : la question que le spectateur se pose à ce moment-là, avec une démonstration visuelle (écran partagé, comparaison). Le « Non » de la réponse reste sobre (voir A4). | oui | 7–8 s |
| 7 | **Le plus fou / conseil** | Un fait final qui donne envie de le raconter à quelqu'un, **ou** le conseil pratique qu'on retient. | absent ou réagit | 5–7 s |
| 8 | **Fin** | Phrase courte qui **renvoie à l'accroche** (boucle : la dernière image ressemble à la première, pour le revisionnage) + abonnement en 1,5–2 s. | saute sur le bouton | 2–2,5 s |

Les scènes 6 et 7 peuvent être fusionnées si le sujet est simple (7 scènes au total). On ne descend jamais sous 7 scènes, et on ne dépasse jamais 8.

### Variante « chronologie » (sujets du type « que se passe-t-il si… pendant X ? »)
Validée sur l'épisode douche. À utiliser dès que le sujet **évolue dans le temps** (un an sans dormir / sans sucre / sans téléphone, un corps dans l'espace, une plante sans eau…).

| # | Rôle | Contenu |
|---|---|---|
| 1 | Accroche | La situation + la question (« Tu arrêtes X pendant un an. Il se passe quoi ? ») |
| 2 | Étape 1 (court terme : heures / jours) | 1 à 2 phrases sur le corps ou l'objet + **1 phrase de réaction sociale** |
| 3 | Étape 2 (≈ 1 mois) | idem — c'est l'étape « mécanisme » (coupe, macro, accéléré) |
| 4 | Étape 3 (≈ 3 mois) | idem — commence par « Sauf qu'à… » (rebondissement, ≈ 40 % de la vidéo) |
| 5 | Étape 4 (fin de la période) | la **réponse nette** au titre (coupure musicale avant) + la réaction sociale la plus forte, en gag final (« même ton chat fait ses valises ») |
| 6 | Objection | « Mais alors… ? » |
| 7 | Conseil | ce qu'on retient |
| 8 | Fin | boucle vers l'accroche + abonnement |

Règles propres à la chronologie :
- **C1. 3 ou 4 étapes**, jamais plus (au-delà, la vidéo dépasse 60 s). Étapes de durée croissante : jours → mois → année.
- **C2. Chaque étape commence par son repère de temps** dit à voix haute, en premier mot (« Jour deux : … », « Un mois : … », « Sauf qu'à trois mois… », « Un an plus tard ? »).
- **C3. Tampon plein écran** sur ce repère : fond assombri (tramage noir 10/16), libellé géant 64 px qui tremble, bruitage « stamp ». Il dure du premier mot du repère jusqu'à 0,25 s après la fin du repère.
- **C4. Barre de progression** en haut de l'écran pendant toutes les étapes (J0 → fin, un repère par étape, remplissage jaune animé), avec le **badge de l'étape** dessous (texte 26 px au moins : en dessous, les chiffres « 2 » / « 3 » ressemblent à des « 8 »). Les titres des scènes descendent de 38 px pour laisser la place.
- **C5. Une réaction sociale par étape**, en dernière phrase, avec son propre plan du quotidien (bureau, bus, téléphone, rue…). Elle est **de plus en plus forte** d'une étape à l'autre (reculer d'un pas → place vide → messages ignorés → tout le monde fuit, même l'animal). Les gens sont des silhouettes grises simples ; leur réaction se lit en un geste (reculer, pince à linge, « ! », fuite).
- **C6. Coupes franches entre les plans d'une même étape**, calées sur le début de la phrase, avec un whoosh 0,08 s avant. Le volet mosaïque reste réservé aux changements de scène.
- **C7. L'état de Pip empire d'une étape à l'autre** (taches, croûte, champignon sur le bonnet…) : on voit le temps passer sur lui.
- **C8. Pip joue « toi »** : il peut être présent à chaque étape. Dans ce cas, la règle A6-1 devient « absent d'au moins une scène entière **et** de plusieurs plans » (macro, loupe, téléphone…).
- Budget : 170 à 180 mots, 52 à 58 s. Si ça dépasse, couper d'abord une phrase « corps » secondaire, jamais une réaction sociale ni un repère de temps.

### Règles du hook
1. Pas d'intro : la première image est déjà en mouvement.
2. Titre-question à l'écran avant 0,5 s.
3. Voix à 0,1 s, question posée avant 3 s.
4. Pip visible et en action dans la première seconde.
5. Phrase qui intrigue, et non une phrase qui demande de rester (« reste jusqu'à la fin » est interdit).
6. Le hook contient **un paradoxe ou un enjeu personnel** (« on t'opère et tu ne sens rien », « une mouche sur TA pizza »), jamais une définition.

### Règles d'écriture du script
- Phrases de **12 mots au plus**, vocabulaire de collégien, tutoiement.
- **Une phrase = une info nouvelle** (R2) et une image nouvelle à l'écran.
- **Au moins une comparaison du quotidien** par notion abstraite (« comme des dominos », « comme une éponge-paille », « appuie sur les freins »).
- **Au moins un chiffre concret** dans la vidéo (date, nombre, durée), lu en toutes lettres.
- **Boucle ouverte** : la scène 2 ou 4 annonce discrètement qu'il reste quelque chose (« Mais le vrai problème, c'est pas ça. »), sans dire « reste ».
- **Pas de liste** (« premièrement, deuxièmement ») à l'oral : la structure se lit à l'écran.
- Mots interdits : « en fait », « donc voilà », « il faut savoir que », « comme on l'a vu ».
- Le mot-choc de la scène est le **dernier mot** de sa phrase, pour que le titre tombe pile dessus.

## A8. Vérifications
1. Plus grand blanc dans la voix ≤ 0,30 s.
2. Hook ≤ 3,0 s.
3. `ffprobe` : 1080×1920, 30 fps, une piste audio, ≤ 60 s.
4. `silencedetect` (−50 dB, 0,3 s) : aucun silence.
5. **Grille pixel** : chaque bloc 3×3 est uniforme, y compris pendant les ralentis et les traînées (sauf si `STYLE = flat`).
6. **Palette** : toutes les couleurs sont dans la palette (avant encodage).
7. **Placement** : la boîte de Pip ne chevauche jamais un titre, un sous-titre, le personnage-sujet ou l'élément cible.
8. **Variété** (table `PIP_ACTIONS` du script d'épisode) :
   - Pip absent d'au moins 2 scènes ;
   - jamais la même famille d'interaction dans deux scènes qui se suivent.
9. **Voix** : aucune balise `[...]` dans les sous-titres ni dans `timings.json`, aucune balise prononcée, chiffres lus en toutes lettres.
10. **Rythme** (nouveau) :
    - aucun plan fixe de plus de 2,0 s sans changement visuel ;
    - aucun gag sans voix de plus de 1,5 s ;
    - débit moyen entre 3,2 et 3,6 mots/s, et aucune scène sous 2,8 mots/s (c'est là que la vidéo mouche ralentissait) ;
    - « … » au plus une fois par scène.
11. **Fil** (relecture humaine) : pour chaque scène, compléter la phrase « Cette scène rapproche de la réponse à *<question du titre>* parce que… ». Si on ne trouve pas, la scène est réécrite ou coupée (R1).
12. **Chronologie** (si variante utilisée) : chaque étape a son repère de temps en premier mot, son tampon, et une réaction sociale en dernière phrase ; la barre de progression est visible de la 1re à la dernière étape.

Note : encoder en `-crf 16 -pix_fmt yuv420p` **après** l'agrandissement ×3, jamais avant.

---

# Partie B — Gabarit d'épisode (à remplir à partir du sujet)

> Copier cette partie dans `plan_<slug>_pixel.md`, sous un en-tête :
> `# Plan vidéo — « <Titre> » avec Pip (pixel art HD)`, suivi de la Partie A reprise par référence (« Recette : voir plan_maitre_video.md, Partie A »).

## B0. Fiche d'identité
| Champ | Valeur |
|---|---|
| Sujet | <le sujet retenu (réécrit librement par Claude si c'est mieux)> |
| **Question du titre** | <question concrète, avec « tu » ou « ta », ≤ 8 mots> |
| Titres de secours | <2 autres titres> |
| Réponse en une phrase | <la réponse que donne la scène 5> |
| Ton | <ludique / mystérieux / « beurk-rigolo » / émerveillé…> |
| STYLE | `pixel` (par défaut) ou `flat` |
| STRUCTURE | `classique` (A7) ou `chronologie` (variante A7) |
| Étapes (si chronologie) | <3 ou 4 repères, ex. Jour 2 / 1 mois / 3 mois / 1 an> |
| Réactions sociales | <une par étape, de plus en plus forte> |
| Décor principal | <lieu du quotidien où se passe l'accroche> |
| Personnage-sujet | <nom, personnalité, tic visuel> ou « aucun » |
| Costume de Pip | <accessoire lié au sujet> |
| Palette thème (14) | <codes hex, groupés par rôle> |
| Musique | <BPM, tonalité, ambiance> |
| Mot-choc | <le mot qui a l'effet spécial du titre> |

## B1. Structure
| # | Rôle | Pip (famille d'interaction) | Durée cible |
|---|---|---|---|
| 1 | Accroche | <…> | ≈ 2,8 s |
| 2 | Déclic | <…> | ≈ 5,5 s |
| 3 | Mécanisme | **absent** | ≈ 6,5 s |
| 4 | Rebondissement | <…> | ≈ 6,5 s |
| 5 | Réponse | <…> | ≈ 7,5 s |
| 6 | Objection | <…> | ≈ 7,5 s |
| 7 | Le plus fou / conseil | <absent ou réagit> | ≈ 6 s |
| 8 | Fin | saute sur le bouton | ≈ 2,2 s |

Mots qui arrivent **sur le mot lui-même** : <liste, 2 à 4 mots>.

## B2. Script
| # | Scène | Voix off (une phrase = une synthèse) | Texte à l'écran | Balises / stabilité / vitesse |
|---|---|---|---|---|
| 1 | Accroche | « <…> » | « <…> » | <…> |
| … | … | … | … | … |
| 8 | Fin | « <phrase-boucle> Abonne-toi, y'a plein d'autres secrets ! » | « **Abonne**-toi / pour d'autres **secrets** ! » + bouton « S'ABONNER » et cloche | `[excited]` / 0,3 / 1,10 |

`NOMINAL = [...]` (durées de référence de la chorégraphie, à mettre à l'échelle sur la voix réelle).

**Coût** : environ <N> caractères, balises comprises.

**Si la vidéo dépasse 55 s**, raccourcir dans cet ordre : <2 phrases désignées à l'avance, jamais dans le hook ni dans la réponse>.

## B3. Exactitude
Pour chaque fait du script :
- ce qui est vrai, en termes scientifiques ;
- ce qui est une **image** (comparaison) et pas un terme scientifique ;
- les simplifications assumées ;
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

---

# Partie C — Fichiers et fabrication

| Fichier | Rôle |
|---|---|
| `.env` | `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` (dans le `.gitignore`) |
| `tts.py` | voix off ElevenLabs : `SCRIPT` et `ELEVEN_EXPRESSION` de l'épisode, timings des mots, repli, cache, `--henri` |
| `timeline.py` | calage commun sur `audio/timings.json`. Moments forts déclarés par l'épisode. |
| `sfx.py` | musique chiptune (coupure avant la réponse, effets ralenti / accéléré) et bruitages → `audio/mix.wav` |
| `pixel.py` | **moteur** (réutilisé) : canevas 360×640, palette, Bayer, police, transitions, sous-titres karaoké, modes ralenti / accéléré, vignette loupe, agrandissement ×3, ffmpeg |
| `decors_<slug>.py` | décors et objets de l'épisode |
| `<personnage>.py` | personnage-sujet et petits éléments récurrents (si l'épisode en a) |
| `pip_pixel.py` | sprite de Pip, poses de A6, accessoire de costume |
| `episode_<slug>.py` | chorégraphie des scènes, table `PIP_ACTIONS`, caméra, titres et sous-titres → `renders/<slug>.mp4` |
| `snap.py` | images fixes de contrôle et tests de A8 (dont les tests de rythme) |

Référence : l'épisode `douche/` contient le moteur complet et réutilisable — `stage_overlay()` (tampon + barre + badge), `cut()` (coupes par phrase), décors sociaux (`office`, `bus`, `phone` + `chat_bubble`, `street`, `person`, `cat`), et le correctif de la cédille « Ç » dans `pixel.py`. Pour un nouvel épisode, copier `douche/` et ne réécrire que `tts.py` (SCRIPT), `timeline.py` (événements), `decors_<slug>.py` et `episode_<slug>.py`.

Le script principal s'appelle toujours `episode_<slug>.py`, pour ne jamais entrer en conflit avec le module d'un personnage.

## Commandes
```bash
uv add elevenlabs python-dotenv                     # une seule fois
uv run python tts.py                                # voix off -> audio/voice.wav + timings.json
uv run python tts.py --only 3                       # regénérer une scène (après avoir supprimé ses prises en cache)
uv run python tts.py --henri                        # secours gratuit edge-tts
uv run python sfx.py                                # musique + bruitages -> audio/mix.wav
uv run python snap.py 0 0.5 1.2 5 10 20 30 40 48    # images de contrôle + tests A8 -> renders/
uv run python episode_<slug>.py --preview           # aperçu 360x640
uv run python episode_<slug>.py --final             # final 1080x1920, 30 fps, avec audio/mix.wav
```

**Note technique :** tout est dessiné en 360×640 en indices de palette (numpy `uint8`). Ralenti et accéléré se font **dans la timeline** (temps local de la scène modifié, poses tenues). Ne jamais interpoler entre deux images, ce qui créerait des couleurs hors palette. Les traînées sont des copies tramées décalées d'un nombre entier de pixels. Conversion en couleurs et agrandissement ×3 (`np.repeat`) à la toute fin, puis ffmpeg (`-f rawvideo`, `-crf 16`). Ne jamais redimensionner avec un filtre lissant.

---

# Partie D — Procédure de génération (ce que Claude fait quand tu donnes un sujet)

0. **Réécrire le sujet ou le titre si c'est mieux (autorisé, et même encouragé).** Le sujet ou le titre donné est un point de départ, pas une consigne figée. Claude peut le reformuler, le resserrer, changer d'angle ou de durée, ou passer à la variante chronologie, si ça donne une vidéo plus forte. Exemples :
   - *« que se passe-t-il si on ne prend pas de douche pendant un an »* → **« Un an sans douche, il se passe quoi ? »** (plus court, avec « tu », et la question est posée en moins de 3 s) ;
   - *« le sommeil »* → **« Et si tu ne dormais plus pendant une semaine ? »** (un enjeu personnel et une chronologie possible, au lieu d'une définition).

   Pas besoin de se justifier : Claude prend directement la meilleure version. Garde-fous :
   - **garder l'intention** : même thème, même ton, même public ;
   - l'exactitude passe avant le hook : pas de titre plus accrocheur mais faux.

1. **Trouver la question.** Transformer le sujet en question concrète, avec un paradoxe ou un enjeu personnel. *Sujet « le sommeil » → « Pourquoi tu ne peux pas rester éveillé ? »* Proposer 3 titres et en retenir un.
   **Choisir la structure** : si le sujet se raconte dans le temps (« et si tu… pendant un an ? »), prendre la **variante chronologie** de A7 et fixer les 3–4 étapes + une réaction sociale par étape.
2. **Écrire la réponse en une phrase.** Si elle n'est pas claire, la question est mal choisie : revenir à l'étape 1.
3. **Rassembler 5 à 7 faits vérifiés.** Garder seulement ceux qui servent la réponse (R1). Classer : déclic, mécanisme, idée reçue (rebondissement), objection probable, fait le plus fou / conseil.
4. **Placer les faits dans les 8 rôles de A7.** Écrire chaque transition en « Sauf que / Mais alors / Résultat », jamais « Et aussi ».
5. **Écrire le script** avec les règles d'écriture de A7 (≤ 12 mots, une info par phrase, une comparaison par notion abstraite, un chiffre, une boucle ouverte, mot-choc en fin de phrase). Viser 150 à 170 mots.
6. **Tester le fil** (A8-11) scène par scène, et le débit (A8-10) en comptant les mots par scène.
7. **Choisir les visuels** : un décor du quotidien pour l'accroche, une vue macro / coupe pour le mécanisme, un écran partagé ou un ralenti / accéléré pour l'objection. Un changement visuel toutes les 2 s au plus.
8. **Distribuer Pip** : absent d'au moins 2 scènes, familles alternées, gags calés sur la phrase en cours. Remplir `PIP_ACTIONS`.
9. **Choisir la palette thème (14 couleurs), la musique et les bruitages propres.**
10. **Écrire la section Exactitude**, puis désigner les 2 phrases à couper si la vidéo dépasse 55 s.
11. **Rendre** `plan_<slug>_pixel.md` avec les sections B0 à B5 remplies.
