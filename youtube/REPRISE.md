# Reprise du travail YouTube (état au 29 septembre 2026)

Note de passation pour la session qui reprend les vidéos YouTube. Lire ce fichier suffit pour savoir où on en est ;
le détail technique est dans les fichiers cités.

## À lire d'abord

1. La mémoire de Claude (`~/.claude/projects/-Users-richard-Developer-github/memory/`, index `MEMORY.md`), surtout
   `gemini-tts-voices.md`, `hoshi-channel-layout.md`, `no-ai-wording-in-titles.md`, `village-trois-moulins-channel.md`,
   `mac-disk-and-ram-tight.md`, `cloud-first-heavy-work.md`, `hoshuko-commit-identity.md`.
2. `youtube/README.md` et `youtube/metadata.json` : titres, descriptions, chapitres et statut de chaque vidéo.
3. `youtube/tools/` : `visit.py` (visite narrée), `gemini_voice.py` (voix Gemini), `narrate.py`, `music.py`, `thumbs.py`.

## Règles fixées par le propriétaire

- **Voix** : Gemini TTS uniquement, `gemini-3.8-flash-tts` (repli `gemini-3.8-flash-lite-tts` si le quota est épuisé),
  jamais `gemini-2.5-pro-preview-tts`, jamais la voix Google Traduction. Choisir les voix soi-même sans demander, en
  variant homme/femme. Vérifier l'audio final par transcription horodatée (`gemini-3.1-flash-lite`).
- **Clé API** : dans `GEMINI_API_KEY` uniquement (jamais écrite dans un fichier ni un commit). Quand le quota est
  atteint (erreur 429), le dire au propriétaire : il fournit une nouvelle clé.
- **Promos sans voix off** : jamais sur YouTube. Elles sont archivées dans `archives/promos-sans-voix/` (dépôt privé,
  exclu du sparse-checkout) et ne restent pas en local.
- **Descriptions YouTube** : aucune mention d'IA (Google Flow, Gemini, voix de synthèse), pas d'« adapté par l'IA »
  dans les titres ; mots-clés que le public recherche, adaptés par langue.
- **Tiziri** : infos fictives en public ; les vraies infos de la boutique restent privées (interrupteur
  `TIZIRI_INFOS_REELLES=1`, voir le commit 903f850). Ne jamais les exposer.
- **Ménage** : dès qu'un fichier est publié ou reproductible, le mettre à la corbeille (disque du Mac presque plein).
- **Commits** : identité hoshuko noreply, sans `Co-Authored-By` ; `git pull --rebase --autostash`, jamais `--force`.
- **Machine** : 8 Go de RAM ; rendus lourds de préférence sur une VM Google Cloud (crédit d'environ 200 $), à supprimer
  après usage.

## Les chaînes

**Hoshi** (@Hosh-uko) : sites vitrines et Uko. Toutes les vidéos sont publiques (le propriétaire les partage pour
avoir des avis). Playlists par thème, toutes langues dedans :
- « Sites vitrines animés pour commerces · gratuits et open source » : Billot kVVHYeQmC9s, Tafat ZPInp08bYq0,
  Nacre OrKFlMC_ekk, Lalla Warda hpVUZweuU0g, Tiziri nobChMGVDVs, Short Tiziri wkbtWiev3-U ;
- « Uko · mascotte animée gratuite pour app et site web · FR, EN, ES » : 7q3UQLEOxqA, Fntj-EfkjvQ, dIn5mROuAIM.
Description de chaîne refaite (sections à émojis, sans liens dans le texte ; les liens sont dans la section Liens).
Chaque nouvelle vidéo va dans la playlist de son thème ; un nouveau projet (ex. SubFlow) aura sa playlist à sa
première vidéo.

**Le Village des Trois Moulins** (@LeVillagedesTroisMoulins) : série pour enfants, projet `~/Developer/series youtube`
(voir son `youtube/README.md` : calendrier, un épisode le mercredi à 10 h dès le 7 octobre 2026). En ligne : épisode 1
en 1080p (3W9aujkq1M0) et bande-annonce 1080p (8FjHEHN16Ug), dans la playlist de la série.

Studio : l'automatisation marche dans le navigateur intégré avec `document.execCommand('insertText')` ; les cases
de playlist sont des `ytcp-checkbox-lit` dont l'état est sur l'enfant `[role=checkbox]`. Les miniatures
personnalisées sont refusées (vérification par téléphone à faire par le propriétaire). Les suppressions et les
changements de visibilité peuvent être bloqués par le mode auto : les laisser au propriétaire.

## À faire

1. **Re-rendre en 3.8 Flash** (nouvelle clé nécessaire) les visites narrées :
   - Lalla Warda ES et AR : `youtube/lalla-warda/make.py` (voix ES Aoede, AR Achird ; FR et EN déjà faites) ;
   - Tiziri EN, ES et AR : `youtube/tiziri/make.py <lang>` (EN Umbriel, ES Callirrhoe, AR Sadaltager). L'arabe de
     l'ancien rendu contient encore les fautes corrigées depuis (duel يرتديانها, « الصورة الأصلية ») : ne pas le publier.
   Puis mettre en ligne sur Hoshi (titres et descriptions dans `metadata.json`), playlist « Sites vitrines ».
2. **Promo arabe de Tiziri** (voix féminine) : les voix sont prêtes (`sources/boutique-tigzirt/promo/voix/ar/`,
   `audio-voix-ar.wav`, 40 lignes « ar: » dans `i18n.txt`) ; il reste à rendre la vidéo avec `render.py`.
   Vérifier aussi si les `tiziri-promo-*-{fr,en,es}.mp4` de ce dossier ont une voix off : sinon, les archiver.
3. **Promo arabe d'Atelier Nacre** avec voix off : dossier `sources/nail-artiste/promo/` (même principe que Tiziri :
   lignes arabes dans `i18n.txt`, voix via `voix.py`/`gemini_voice.py`, rendu `render.py`).
4. **Village** : l'ancienne bande-annonce 720p (4NpZqD00ffg) doit passer en privé ou être supprimée (par le
   propriétaire). Suivre le calendrier des épisodes 2 à 7 avec la session de la série.
5. **Hoshi** : le propriétaire supprime les playlists en trop (Uko EN, Uko ES, Village).
6. **Plus tard** : le kabyle n'est pas pris en charge par Gemini ; pistes Hugging Face : OmniVoice, Matoub-82M,
   MMS-TTS-kab (à tester). Idées d'usage des 200 $ de crédit Google Cloud à rediscuter avec le propriétaire.

## Journal de la session cloud (29 septembre 2026)

- Promo arabe de Tiziri rendue en 16:9, 4:5 et 9:16 : `livrables/tiziri-promo-ar/` (60 s, voix arabe Sulafat déjà générée, musique). Le contrôle de la voix par transcription reste à faire (clé Gemini absente de la session).
- Rendu sous Linux : `render.py` lit `CHROME_BIN` et `FFMPEG_BIN` ; le Chromium d'ici ne lit pas le H.264, donc `sh webm.sh` recode `vid/*.mp4` en `vid/*.webm` et on lance avec `PROMO_VID_EXT=webm`. Ordre : `python3 audio.py --voix ar`, puis `python3 _tools/promo_batch.py sources/boutique-tigzirt/promo tiziri ar 169,45,916`.
- Constat portfolio (hoshuko.github.io) : seules les promos de Tiziri ont une voix off (commit e1d3597) ; Billot, Tafat, Nacre et Lalla Warda sont en musique seule. Le portfolio ouvre toujours sur l'onglet « Paysage » (16:9), sans choix automatique du format sur téléphone (`assets/js/portfolio.js`).

