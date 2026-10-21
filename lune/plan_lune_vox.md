# Plan vidéo — « La Lune disparaît ce soir. Il se passe quoi ? » avec Pip (style Vox)

Recette : voir `../plan_maitre_video.md`, Partie A, avec **STYLE = flat**, en version « Vox motion » (option A2). Les seuls écarts sont listés en B0bis.

## B0. Fiche d'identité
| Champ | Valeur |
|---|---|
| Sujet | Que se passerait-il si la Lune disparaissait ? |
| **Question du titre** | « La Lune disparaît. Il se passe quoi ? » (7 mots) |
| Titres de secours | « Et si la Lune disparaissait ce soir ? » / « Une nuit sans Lune… pour toujours » |
| Réponse en une phrase | Pas d'apocalypse : la nuit devient noire, les marées rétrécissent et la nature se dérègle. Mais sur des millions d'années, la Terre pourrait se mettre à tanguer, avec des saisons extrêmes. |
| Ton | émerveillé, avec une pointe de « fin du monde, mais pas trop » |
| STYLE | `flat`, version **Vox** (collage papier) |
| STRUCTURE | `chronologie` |
| Étapes | Première nuit / 6 heures / 1 mois / des millions d'années |
| Réactions (une par étape, de plus en plus fortes) | les astronomes font la fête → le Mont-Saint-Michel n'est presque plus une île → les lions chassent mieux dans le noir → même les pingouins sortent la crème solaire |
| Décor principal | ciel de nuit au-dessus d'un village, Pip et son télescope |
| Personnage-sujet | la Lune elle-même (vraie photo NASA en découpage) |
| Costume de Pip | casque d'astronaute (bulle de verre) |
| Palette thème | papier `#efe8dc` `#ddd2bf` · nuit `#121a2e` `#1f2b4a` `#33456e` · océan `#2f7f8f` `#8fc3c8` · sable `#d9b98a` · corail `#ff7a6b` `#ffb3a1` · lune `#d8d4cc` · soleil `#ffb23f` · gris `#8f8a82` `#c9c3b8` |
| Musique | 112 BPM, ré mineur (Dm–B♭–F–C) → fa majeur à la fin ; pad + arpège pincé + pulsation douce, ambiance « documentaire » |
| Mot-choc | **DISPARAÎT** : les lettres s'envolent une à une, dans le désordre |

### B0bis. Le style Vox, traduit dans le moteur (`vox.py`)
| Effet Vox | Version moteur |
|---|---|
| Fond papier | texture papier crème ou bleu nuit générée (bruit basse fréquence + fibres), grain de film à 12 i/s, vignette légère |
| Découpages | photos et objets avec **bord blanc aux ciseaux** + ombre portée floue, petit tremblement d'angle façon stop motion |
| Vraies photos d'archive | Terre (Apollo 17, AS17-148-22727) et Lune (LRO, face cachée), NASA, domaine public |
| Surligneur | coup de feutre jaune animé de gauche à droite derrière les mots-clés (titres, tampons, sous-titres karaoké) |
| Annotations | traits de feutre rouge qui se dessinent (cercles à main levée, flèches, croix), écriture manuscrite lettre à lettre |
| Graphiques | courbes dessinées au trait (marée, inclinaison de l'axe), barres, balance, règle |
| Coupure de journal | « Le Petit Astronome », titre en serif |
| Transitions | volet « papier déchiré » entre scènes, coupes franches entre plans (C6), zoom lent façon banc-titre (+3,5 % par scène) |
| Polices | Work Sans Bold (titres, sous-titres), DM Mono (étiquettes, barre de progression), Libre Baskerville (journal), Nothing You Could Do (manuscrit), toutes OFL |
| C3 tampon / C4 barre | tampon = bandeau papier surligné qui claque + sous-titre machine à écrire (« T + 6 H ») ; barre = règle papier en haut, remplie au surligneur |

## B1. Structure (chronologie)
| # | Rôle | Étape | Plans | Pip | Durée réelle |
|---|---|---|---|---|---|
| 1 | Accroche | — | village de nuit, la Lune est découpée aux ciseaux et s'envole | utiliser_objet (télescope) | 2,8 s |
| 2 | Étape 1 | PREMIÈRE NUIT | le ciel passe au noir d'encre → **coupure de journal : les astronomes font la fête** | réagir (on ne voit plus que ses yeux) | 6,7 s |
| 3 | Étape 2 / mécanisme | 6 HEURES | courbe de marée « ratée » → Terre + bosse d'océan tirée par la Lune → barres ÷ 2 à 3 → **Mont-Saint-Michel** | utiliser_objet (bouée) | 12,8 s |
| 4 | Étape 3 / rebondissement | SAUF QU'À 1 MOIS… | calendrier lunaire barré → ponte des coraux → rendez-vous raté → **lions dans la savane noire** | se_deplacer (fuit le lion) | 10,7 s |
| 5 | Étape 4 / réponse | DES MILLIONS D'ANNÉES | la Terre tangue (coupure musicale avant) → toupie + Lune = main → courbe d'inclinaison → **pingouin à la crème solaire** | subir (perd l'équilibre) | 11,9 s |
| 6 | Objection | — | orbite autour du Soleil → « NON ! » + balance Terre / 81 Lunes | agir_corps (saute sur la pile de Lunes) | 5,3 s |
| 7 | Le plus fou | — | la Lune s'éloigne, ruban de mesure + 3,8 cm/an | **absent** | 3,3 s |
| 8 | Fin | — | retour au village du début (boucle), la Lune revient, bouton S'ABONNER | agir_corps (saute sur le bouton) | 4,5 s |

Mots qui arrivent **sur le mot lui-même** : *disparaît* (ciseaux), *noir* (extinction), *tanguer* (roulis), *non* (tampon rouge).

## B2. Script (176 mots selon le décompte de tts.py, 183 en séparant les traits d'union ; 57,9 s)
| # | Voix off | Balise / stabilité / vitesse |
|---|---|---|
| 1 | « Ce soir, la Lune disparaît. Il se passe quoi ? » | `[curious]` 0,3 / 1,10 |
| 2 | « Première nuit : plus de clair de lune, le ciel est noir d'encre. » · « Les astronomes, eux, font la fête. » | `[surprised]` 0,3 / 1,10 |
| 3 | « Six heures plus tard : pas de tsunami, mais la marée rate. » · « La Lune tirait les océans vers elle, comme un aimant. » · « Sans elle, les marées sont deux à trois fois plus petites. » · « Et le Mont-Saint-Michel n'est presque plus jamais une île. » | `[curious]` 0,5 / 1,10 |
| 4 | « Sauf qu'au bout d'un mois, la nature se dérègle. » · « Les coraux pondent tous ensemble, réglés sur la pleine lune. » · « Sans elle, ils ratent leur rendez-vous. » · « Et les lions adorent : ils chassent mieux dans le noir. » | `[whispers]` 0,5 / 1,10 |
| 5 | « Des millions d'années plus tard ? La Terre se met à tanguer. » · « La Lune tenait son axe, comme une main sur une toupie. » · « Sans elle, les saisons pourraient devenir extrêmes. » · « Même les pingouins sortent la crème solaire. » | `[dramatic]` 0,5 / 1,08 |
| 6 | « Mais alors, la Terre quitterait son orbite ? » · « Non ! La Lune est quatre-vingt-une fois plus légère qu'elle. » | `[mischievously]` 0,3 / 1,10 |
| 7 | « Le plus fou ? Elle s'en va déjà : quatre centimètres par an. » | `[excited]` 0,3 / 1,10 |
| 8 | « Alors ce soir, regarde-la bien. » · « Abonne-toi, y'a plein d'autres secrets ! » | `[cheerful]` 0,3 / 1,10 |

**Si la vidéo doit raccourcir** : couper « Sans elle, ils ratent leur rendez-vous. » puis « Pas de tsunami » (la phrase devient « Six heures plus tard : la marée rate. »).

## B3. Exactitude
- **Nuit plus noire** : vrai. Une pleine lune éclaire autour de 0,1 à 0,3 lux, une nuit sans lune sous les étoiles environ 0,001 à 0,002 lux. « ÷ 100 » est un ordre de grandeur. La Lune ne fait que renvoyer la lumière du Soleil.
- **Pas de tsunami** : la marée est une déformation lente, d'une période d'environ 12 h 25. Si la Lune disparaissait, la bosse d'océan se résorberait sur des heures, sans vague géante (les courants côtiers seraient quand même perturbés).
- **« Comme un aimant »** : c'est une **image**, la marée vient de la gravité, pas du magnétisme. On le dit avec « comme ».
- **Marées deux à trois fois plus petites** : la marée solaire vaut environ 46 % de la marée lunaire. Sans Lune, il reste à peu près la moitié de la marée lunaire seule, et environ un tiers des grandes marées actuelles (Lune + Soleil alignés).
- **Mont-Saint-Michel** : il n'est entouré d'eau qu'aux grandes marées. Avec des marées deux à trois fois plus faibles, ce serait très rare. « Presque plus jamais » reste prudent.
- **Coraux** : la ponte synchronisée de la Grande Barrière (une fois par an, quelques nuits après une pleine lune de fin de printemps austral) est réglée en partie par la lumière de la Lune. Sans ce signal, la synchronisation se dégraderait. « Au bout d'un mois » est un raccourci, puisque la ponte n'a lieu qu'une fois par an.
- **Lions** : en Tanzanie, les attaques de lions sont plus fréquentes les nuits sombres qui suivent la pleine lune (Packer et al., 2011). On reste sur « ils chassent mieux dans le noir ».
- **Axe qui tangue** : la Lune stabilise l'inclinaison de la Terre (23,4°, variations de ±1,3°). Sans elle, les simulations donnent des variations bien plus fortes, chaotiques selon Laskar (1993), plus modérées selon Lissauer (2012), et toujours sur des **millions d'années**. D'où « pourraient » dans le texte. La courbe à l'écran est une **illustration** et l'angle affiché qui varie est exagéré.
- **Pingouins et crème solaire** : gag, pas une donnée. Les manchots vivent dans l'hémisphère sud, l'image est comique.
- **81 fois plus légère** : masse de la Terre / masse de la Lune ≈ 81,3. Le centre de gravité Terre-Lune est à l'intérieur de la Terre (≈ 4 700 km du centre), donc l'orbite autour du Soleil ne changerait presque pas.
- **4 cm par an** : la Lune s'éloigne de 3,8 cm/an (mesure laser sur les réflecteurs Apollo), à peu près la vitesse de pousse des ongles.
- **Photos** : la Lune utilisée est la face cachée (LRO), qui se lit comme « la Lune » dans un collage. À remplacer par la face visible si on trouve une image NASA équivalente.
- **Ce qu'on ne montre pas** : pas de catastrophe ni de victime, le lion reste une silhouette et la scène reste comique.

## B4. Mise en scène
**1. Accroche — village de nuit** *(Pip : utiliser_objet)*
- 0,1 s : titre « La **Lune** disparaît. » tombe en bande de papier. La Lune (photo) apparaît en pop au-dessus des toits, Pip montre le ciel près de son télescope.
- Sur « disparaît » : pointillés rouges de ciseaux autour de la Lune, qui s'envole en tournant. Mot-choc : les lettres de « disparaît. » s'envolent une à une, et il ne reste qu'un cercle pointillé blanc avec un « ? » jaune.
- Sur « Il se passe quoi ? » : deuxième bande, « quoi ? » surligné.
- Sons : twinkle, pop, ciseaux, scintillement descendant, feutre.

**2. Première nuit** *(Pip : réagir)*
- Tampon « PREMIÈRE NUIT » + « T + 0 » tapé à la machine. La barre de progression apparaît.
- Sur « noir » : le ciel passe au noir d'encre, des centaines d'étoiles s'allument, les fenêtres s'éteignent. Gag : on ne voit plus que les yeux de Pip qui clignent, et un « ! ». Étiquette « LUMIÈRE LA NUIT : ÷ 100 ».
- Coupe sur « Les astronomes » : coupure de journal « Ciel parfait : les astronomes font la fête », silhouettes en chapeaux pointus qui sautent, confettis, « enfin un ciel noir ! » à la main.

**3. 6 heures** *(Pip : utiliser_objet)*
- Graphique « NIVEAU DE LA MER » : la courbe se dessine. « TSUNAMI ? » barré. Sur « rate », la marée prévue (pointillés) contre la marée réelle (rouge, aplatie), avec « marée ratée ».
- Coupe : la Terre (photo) et sa bosse d'océan étirée vers la Lune, flèches rouges, aimant découpé + « comme un aimant ».
- Coupe : la Lune s'efface, la bosse dégonfle, barres « AVEC LUNE » contre « SOLEIL SEUL », étiquette « ÷ 2 à 3 ».
- Coupe : Mont-Saint-Michel sur la baie, ligne « MARÉE HAUTE D'AVANT » en pointillés rouges. La mer reste basse, Pip attend avec sa bouée, puis le Mont est entouré au feutre sur « île ».

**4. Sauf qu'à 1 mois…** *(Pip : se_deplacer)*
- Calendrier lunaire découpé : les phases sont barrées une à une, le calendrier tremble.
- Coupe sous l'eau : rayons de lumière, la pleine lune brille et trois coraux pondent en même temps (« PONTE GÉANTE »).
- Coupe : plus de Lune, les coraux pondent chacun à un moment différent, « RENDEZ-VOUS RATÉ » barré.
- Coupe : savane de nuit, le lion en silhouette aux yeux jaunes avance, les gazelles fuient et Pip passe en courant. Étiquette « PLUS D'ATTAQUES LES NUITS NOIRES ».

**5. Des millions d'années** *(Pip : subir)*
- Coupure musicale de 0,5 s, puis « La Terre se met à TANGUER » : la Terre roule de ±24° et Pip, debout dessus, perd l'équilibre. L'angle affiché varie.
- Coupe : toupie découpée, avec la Lune posée sur la poignée et « la main » au feutre. Étiquette « AXE STABLE ».
- Coupe : graphique « INCLINAISON DE L'AXE », trait noir sage avec la Lune, trait rouge chaotique sans elle. Un pic est entouré, avec « saisons extrêmes ».
- Coupe : pingouin à lunettes de soleil sur sa banquise, le soleil tourne, la crème SPF 50 gicle sur « crème ».

**6. Objection** *(Pip : agir_corps)*
- Orbite autour du Soleil, la Terre s'échappe avec une flèche rouge et un « ? ».
- Sur « Non ! » : tampon rouge. Balance : la Terre d'un côté, des Lunes qui s'empilent de l'autre (compteur × 0 → × 81) jusqu'à l'équilibre. Pip saute sur la pile. Étiquette « 81 FOIS PLUS LÉGÈRE ».

**7. Le plus fou** *(Pip absent)*
- La Terre et la Lune en photo, ruban de mesure jaune qui s'allonge à mesure que la Lune s'éloigne. Étiquette « + 3,8 cm PAR AN », puis « comme tes ongles qui poussent » à la main.

**8. Fin** *(Pip : agir_corps)*
- Même village qu'en ouverture (boucle), la Lune est revenue. « Regarde-la bien. » Le bouton S'ABONNER arrive en pop et Pip saute dessus (bonk + cloche).

**Bruitages propres au sujet** : ciseaux, scintillement de disparition, extinction des lumières, langue de belle-mère, vague, vidange, élastique, bulles, grognement, roulis, toupie, spray, compteur, règle. Les bruits de transition sont des sons papier (feuille qui glisse, machine à écrire, tampon, feutre).

## B5. Table `PIP_ACTIONS`
```python
PIP_ACTIONS = {
    1: ("utiliser_objet", "regarde la Lune au télescope"),
    2: ("reagir", "seuls ses yeux restent visibles dans le noir"),
    3: ("utiliser_objet", "attend la mer avec sa bouée"),
    4: ("se_deplacer", "fuit le lion dans la savane"),
    5: ("subir", "perd l'équilibre sur la Terre qui tangue"),
    6: ("agir_corps", "saute sur le plateau de la balance"),
    7: None,
    8: ("agir_corps", "saute sur le bouton S'ABONNER"),
}
```
Comme dans l'épisode douche (C8), Pip joue « toi » : il est absent d'une scène entière (7) et de plusieurs plans (journal, graphiques, Terre-aimant, barres, calendrier, coraux, toupie, pingouin, orbite).

## Vérifications (`python snap.py`)
Hook 2,65 s · 1080×1920, 30 i/s, 57,9 s · aucun silence · blanc max dans une phrase 0,12 s · Pip hors des sous-titres · familles alternées · aucune balise · débit 3,20 mots/s, toutes les scènes ≥ 2,78 mots/s. Les tests « grille pixel » et « palette » ne s'appliquent pas (STYLE = flat).

## Fabrication
```bash
python tts.py                 # voix ElevenLabs -> audio/voice.wav + timings.json
python sfx.py                 # musique + bruitages -> audio/mix.wav
python episode_lune.py --final  # 1080x1920 sur 4 processus (~4 min) -> renders/lune.mp4
python snap.py 1.5 20 36.5    # images de contrôle + tests A8
```
