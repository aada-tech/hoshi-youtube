# YouTube · vitrines

**[Français](#français)** · **[English](#english)** · **[Español](#español)**

## Français

Tout ce qu'il faut pour publier les vitrines sur la chaîne [@Hosh-uko](https://www.youtube.com/@Hosh-uko) : une vitrine par jour, vidéo commentée à 18 h 00 et Short à 18 h 30 (heure de Paris).

- `metadata.json` : calendrier, titres, descriptions, chapitres, tags, commentaire épinglé et Shorts, en FR, EN, ES (et AR pour Tafat).
- `<projet>/make.py` : visite commentée du site en ligne → `out/<projet>-visite-<langue>.mp4` et sous-titres `.srt`. Exemple : `python3 maison-billot/make.py fr` (ajouter `--test` pour les 15 premières secondes).
- `tools/tour.py` (visite filmée image par image, temps de la page ralenti), `tools/narrate.py` (voix Google, minutage, sous-titres, mixage), `tools/music.py` (musique de fond), `tools/thumbs.py` (miniatures 1280 × 720).
- La vidéo principale est en français, avec les sous-titres EN/ES (`-visite-fr.en.srt`, `.es.srt`) calés sur sa voix ; les versions complètes EN et ES servent de vidéos à part ou de pistes audio.

## English

Everything needed to publish the templates on [@Hosh-uko](https://www.youtube.com/@Hosh-uko): one template a day, the narrated video at 18:00 and the Short at 18:30 (Paris time).

- `metadata.json`: schedule, titles, descriptions, chapters, tags, pinned comment and Shorts, in FR, EN, ES (and AR for Tafat).
- `<project>/make.py`: narrated tour of the live site → `out/<project>-visite-<lang>.mp4` and `.srt` subtitles (`--test` renders the first 15 seconds).
- `tools/`: frame-by-frame site tour, Google voice-over and subtitles, music bed, 1280 × 720 thumbnails.

## Español

Todo lo necesario para publicar las maquetas en [@Hosh-uko](https://www.youtube.com/@Hosh-uko): una maqueta al día, el vídeo comentado a las 18:00 y el Short a las 18:30 (hora de París).

- `metadata.json`: calendario, títulos, descripciones, capítulos, etiquetas, comentario fijado y Shorts, en FR, EN, ES (y AR para Tafat).
- `<proyecto>/make.py`: recorrido comentado de la web en línea → `out/<proyecto>-visite-<idioma>.mp4` y subtítulos `.srt` (`--test` genera los primeros 15 segundos).
- `tools/`: recorrido grabado fotograma a fotograma, voz de Google y subtítulos, música de fondo, miniaturas de 1280 × 720.
