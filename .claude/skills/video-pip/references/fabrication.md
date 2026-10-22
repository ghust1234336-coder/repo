# Partie C — Fichiers et fabrication

| Fichier | Rôle |
|---|---|
| `.env` | `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` (dans le `.gitignore`) |
| `tts.py` | voix off ElevenLabs : `SCRIPT` et `ELEVEN_EXPRESSION` de l'épisode, timings des mots, repli, cache, `--henri` |
| `timeline.py` | calage commun sur `audio/timings.json` : bornes des scènes, `W()` / `S()` pour viser un mot ou une phrase, moments forts sonores (`events()`), coupure musicale et sourdine |
| `sfx.py` | musique documentaire et bruitages papier → `audio/mix.wav` |
| `vox.py` | **moteur** (réutilisé) : papier, grain, `Sprite` découpé, `put()`, surligneur, feutre, écriture manuscrite, trame, `photo_disc()`, volet papier déchiré, caméra, `Writer` ffmpeg. Seule la palette thème change. |
| `pip_vox.py` | Pip en papier découpé, poses, accessoire de costume |
| `decors_<slug>.py` | décors, objets découpés et photos détourées de l'épisode |
| `make_cutouts.py` | (si besoin) détourage des photos d'archive sur fond uni |
| `episode_<slug>.py` | chorégraphie des scènes, table `PIP_ACTIONS`, `title()`, `label()`, `hand()`, sous-titres surlignés, rendu sur 4 processus → `renders/<slug>.mp4` |
| `snap.py` | images fixes de contrôle et tests de A8 |
| `description.md` | titre, description, crédits photo et hashtags pour Shorts / TikTok / Reels |

**Pip est orange** : les dossiers existants (`moustiques/`, `lune/`, `gravite/`) ont encore un Pip turquoise. Après la copie, remplacer dans `vox.py` les couleurs `pip`, `pip_d`, `pip_p` par celles de la recette (A2), et dans `pip_vox.py` dessiner le ventre crème et la boule d'antenne jaune.

Pour un nouvel épisode, copier `moustiques/` (ou `lune/` pour la chronologie : `stage_overlay()` y fait le tampon et la barre de progression) et ne réécrire que `tts.py` (SCRIPT), `timeline.py`, `decors_<slug>.py` et `episode_<slug>.py`. Le script principal s'appelle toujours `episode_<slug>.py`, pour ne jamais entrer en conflit avec le module d'un personnage.

## Commandes
```bash
python tts.py                          # voix off -> audio/voice.wav + timings.json
rm audio/takes/eleven/*/s2_*           # regénérer une scène : les prises sont numérotées à partir de 0, donc s2_* = scène 3 ; supprimer ses prises, puis relancer tts.py
python tts.py --henri                  # secours gratuit edge-tts
python sfx.py                          # musique + bruitages -> audio/mix.wav
python snap.py 1.5 20 36.5             # images de contrôle + tests A8 -> renders/
python episode_<slug>.py --preview     # aperçu 540x960 sans grain
python episode_<slug>.py --final       # final 1080x1920, 30 fps, avec audio/mix.wav (~4 min sur 4 processus)
```

**Note technique :** tout est dessiné en 1080×1920 RGBA. Les éléments statiques (papier, découpages, photos détourées, textes figés) sont préparés une fois et mis en cache (`functools.lru_cache`) ; chaque image ne fait que placer, tourner et composer ces calques. Les formes vectorielles sont dessinées suréchantillonnées (×2 ou ×3) puis réduites. Le grain et la vignette sont posés à la toute fin (`finish()`), puis ffmpeg encode en `libx264 -crf 24 -preset slow`.

