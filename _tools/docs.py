"""Documentation des dépôts : README (EN, FR, ES), LICENSE, CREDITS.md, SECURITY.md, .gitignore, .nojekyll, et le README du profil.

python3 docs.py        écrit dans publication/{maison-billot,tafat,atelier-nacre,tiziri,hoshuko.github.io,hoshuko}
"""
import os
from urllib.parse import quote

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du dépôt de travail
ROOT = os.path.join(BASE, 'publication')  # copies locales des dépôts publics
SITE = 'https://hoshuko.github.io/'
M = SITE + 'assets'
GH = 'https://github.com/hoshuko'
YT = 'https://www.youtube.com/@Hosh-uko'
YEAR = 2026
PAGE = {'fr': '', 'en': 'en.html', 'es': 'es.html'}
README = {'en': 'README.md', 'fr': 'README.fr.md', 'es': 'README.es.md'}


def badge(label, message, color, link, alt=None):
    enc = lambda s: quote(s.replace('-', '--').replace('_', '__').replace(' ', '_'), safe='_')
    return f'[![{alt or label}](https://img.shields.io/badge/{enc(label)}-{enc(message)}-{color}?style=for-the-badge)]({link})'


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text.rstrip() + '\n')


# ---------------------------------------------------------------- textes communs
C = {
    'en': {
        'langs': '**English** · [Français](README.fr.md) · [Español](README.es.md)',
        'b_demo': 'Live demo', 'b_video': 'Promo video', 'b_video_msg': '60 s · 3 formats', 'b_langs': 'Languages', 'b_lic': 'License',
        'h_preview': 'Preview', 'preview': 'The site’s signature animation, taken from its 60-second promo video.', 'watch': 'Watch the full promo video →',
        'h_features': 'Highlights', 'h_shots': 'Screenshots', 'desktop': 'Desktop', 'mobile': 'Mobile',
        'h_videos': 'Promo videos',
        'videos': 'Three formats, 60 seconds each, with music and sound effects created from scratch (no copyrighted audio). Click a poster to play the video.',
        'fmt': {'169': 'Landscape · 16:9', '45': 'Feed · 4:5', '916': 'Vertical · 9:16'},
        'use': {'169': 'YouTube, websites', '45': 'Facebook & Instagram feeds', '916': 'Reels, Stories, WhatsApp'},
        'h_langs': 'Languages',
        'langs_text': 'The site ships in French (`index.html`, default), English (`en.html`) and Spanish (`es.html`). Each language is a static page, so search engines and link previews see the right text, and the language switcher sits in the navigation.',
        'h_tech': 'Under the hood',
        'tech': ['Plain HTML, CSS and JavaScript: no framework, no dependency, no build step needed to run it.',
                 'Content and interface text live in one file per language (`{data}`).',
                 'WebP images, self-hosted fonts, `prefers-reduced-motion` support, keyboard navigation and layouts checked from 360 px wide.',
                 'Privacy by design: no cookies, no analytics, no third-party requests, and a strict Content Security Policy.'],
        'h_run': 'Run it locally', 'run': 'Any static web server works. With Python:',
        'run_after': 'Then open <http://localhost:8000>. To publish it, upload the folder to any static host (GitHub Pages, Netlify, Apache, Nginx…).',
        'h_custom': 'Make it yours', 'h_credits': 'Credits',
        'credits': 'Photos come from Unsplash, Pexels and Wikimedia Commons; full attributions are listed in [CREDITS.md](CREDITS.md).{sa} Fonts are under the SIL Open Font License 1.1 ([`assets/fonts/OFL.txt`](assets/fonts/OFL.txt)). All names, addresses, phone numbers, prices and reviews are fictional.',
        'sa': ' Images adapted from CC BY-SA originals remain under that licence.',
        'h_license': 'License',
        'license': 'The code is released under the [PolyForm Noncommercial License 1.0.0](LICENSE). You may use, study and modify it for any non-commercial purpose: personal projects, learning, teaching, charities. Commercial use, such as delivering this template to a paying client, requires a separate licence: open an issue on this repository to ask. Photos and fonts keep their own licences (see above).',
        'h_security': 'Security',
        'security': 'Found a vulnerability? Please report it privately from the repository’s **Security** tab (“Report a vulnerability”) rather than in a public issue. See [SECURITY.md](SECURITY.md).',
        'h_more': 'More templates', 'more': 'Part of **Storefronts in motion**, a series of five scroll-animated website templates:',
        'portfolio': 'Portfolio', 'on_both': '{} on desktop and mobile', 'anim': 'Animated preview of {}', 'on_desk': '{} on desktop', 'on_mob': '{} on mobile',
        'poster': '{} promo video, {}', 'demo': 'Live demo', 'code': 'Code', 'video': 'Promo video',
    },
    'fr': {
        'langs': '[English](README.md) · **Français** · [Español](README.es.md)',
        'b_demo': 'Démo en ligne', 'b_video': 'Vidéo promo', 'b_video_msg': '60 s · 3 formats', 'b_langs': 'Langues', 'b_lic': 'Licence',
        'h_preview': 'Aperçu', 'preview': 'L’animation phare du site, extraite de sa vidéo promo de 60 secondes.', 'watch': 'Voir la vidéo promo en entier →',
        'h_features': 'Points forts', 'h_shots': 'Captures d’écran', 'desktop': 'Ordinateur', 'mobile': 'Mobile',
        'h_videos': 'Vidéos promo',
        'videos': 'Trois formats de 60 secondes, avec une musique et des bruitages créés de toutes pièces (aucun son sous droits). Cliquez sur une affiche pour lancer la vidéo.',
        'fmt': {'169': 'Paysage · 16:9', '45': 'Fil · 4:5', '916': 'Vertical · 9:16'},
        'use': {'169': 'YouTube, sites web', '45': 'Fils Facebook et Instagram', '916': 'Reels, Stories, WhatsApp'},
        'h_langs': 'Langues',
        'langs_text': 'Le site existe en français (`index.html`, par défaut), en anglais (`en.html`) et en espagnol (`es.html`). Chaque langue est une page statique : les moteurs de recherche et les aperçus de liens voient le bon texte, et le sélecteur de langue se trouve dans la navigation.',
        'h_tech': 'Sous le capot',
        'tech': ['HTML, CSS et JavaScript, sans framework ni dépendance : rien à installer ni à compiler pour le lancer.',
                 'Les contenus et les textes de l’interface tiennent dans un fichier par langue (`{data}`).',
                 'Images WebP, polices hébergées avec le site, prise en compte de `prefers-reduced-motion`, navigation au clavier et mise en page vérifiée dès 360 px de large.',
                 'Respect de la vie privée : ni cookies, ni mesure d’audience, ni requête vers un service tiers, et une politique de sécurité du contenu (CSP) stricte.'],
        'h_run': 'Lancer en local', 'run': 'N’importe quel serveur web statique convient. Avec Python :',
        'run_after': 'Ouvrez ensuite <http://localhost:8000>. Pour le mettre en ligne, déposez le dossier chez n’importe quel hébergeur statique (GitHub Pages, Netlify, Apache, Nginx…).',
        'h_custom': 'Personnaliser', 'h_credits': 'Crédits',
        'credits': 'Les photos viennent d’Unsplash, de Pexels et de Wikimedia Commons ; toutes les attributions sont dans [CREDITS.md](CREDITS.md).{sa} Les polices sont sous licence SIL Open Font License 1.1 ([`assets/fonts/OFL.txt`](assets/fonts/OFL.txt)). Les noms, adresses, numéros, prix et avis sont fictifs.',
        'sa': ' Les images adaptées d’originaux sous CC BY-SA restent sous cette licence.',
        'h_license': 'Licence',
        'license': 'Le code est publié sous [licence PolyForm Noncommercial 1.0.0](LICENSE). Vous pouvez l’utiliser, l’étudier et le modifier pour tout usage non commercial : projets personnels, apprentissage, enseignement, associations. Un usage commercial, par exemple livrer cette maquette à un client, demande une licence à part : ouvrez un ticket (issue) sur ce dépôt pour en faire la demande. Les photos et les polices gardent leurs propres licences (voir plus haut).',
        'h_security': 'Sécurité',
        'security': 'Vous avez trouvé une faille ? Signalez-la en privé depuis l’onglet **Security** du dépôt (« Report a vulnerability »), plutôt que dans un ticket public. Voir [SECURITY.md](SECURITY.md).',
        'h_more': 'Autres maquettes', 'more': 'Cette maquette fait partie de **Vitrines en mouvement**, une série de cinq sites animés au défilement :',
        'portfolio': 'Portfolio', 'on_both': '{} sur ordinateur et sur téléphone', 'anim': 'Aperçu animé de {}', 'on_desk': '{} sur ordinateur', 'on_mob': '{} sur téléphone',
        'poster': 'Vidéo promo {}, {}', 'demo': 'Démo', 'code': 'Code', 'video': 'Vidéo promo',
    },
    'es': {
        'langs': '[English](README.md) · [Français](README.fr.md) · **Español**',
        'b_demo': 'Demo en línea', 'b_video': 'Vídeo promocional', 'b_video_msg': '60 s · 3 formatos', 'b_langs': 'Idiomas', 'b_lic': 'Licencia',
        'h_preview': 'Vista previa', 'preview': 'La animación estrella de la web, extraída de su vídeo promocional de 60 segundos.', 'watch': 'Ver el vídeo promocional completo →',
        'h_features': 'Lo más destacado', 'h_shots': 'Capturas de pantalla', 'desktop': 'Ordenador', 'mobile': 'Móvil',
        'h_videos': 'Vídeos promocionales',
        'videos': 'Tres formatos de 60 segundos, con música y efectos de sonido creados desde cero (sin audio sujeto a derechos). Haz clic en un póster para ver el vídeo.',
        'fmt': {'169': 'Horizontal · 16:9', '45': 'Feed · 4:5', '916': 'Vertical · 9:16'},
        'use': {'169': 'YouTube, webs', '45': 'Feed de Facebook e Instagram', '916': 'Reels, Stories, WhatsApp'},
        'h_langs': 'Idiomas',
        'langs_text': 'La web está disponible en francés (`index.html`, por defecto), inglés (`en.html`) y español (`es.html`). Cada idioma es una página estática, así que los buscadores y las vistas previas de enlaces ven el texto correcto; el selector de idioma está en la navegación.',
        'h_tech': 'Por dentro',
        'tech': ['HTML, CSS y JavaScript, sin frameworks ni dependencias: no hay nada que instalar ni compilar para ponerla en marcha.',
                 'Los contenidos y los textos de la interfaz están en un archivo por idioma (`{data}`).',
                 'Imágenes WebP, fuentes alojadas con la web, compatibilidad con `prefers-reduced-motion`, navegación con teclado y diseño comprobado desde 360 px de ancho.',
                 'Privacidad desde el diseño: sin cookies, sin analítica, sin peticiones a terceros y con una política de seguridad de contenido (CSP) estricta.'],
        'h_run': 'Ejecutar en local', 'run': 'Sirve cualquier servidor web estático. Con Python:',
        'run_after': 'Después abre <http://localhost:8000>. Para publicarla, sube la carpeta a cualquier alojamiento estático (GitHub Pages, Netlify, Apache, Nginx…).',
        'h_custom': 'Personalizar', 'h_credits': 'Créditos',
        'credits': 'Las fotos proceden de Unsplash, Pexels y Wikimedia Commons; todas las atribuciones están en [CREDITS.md](CREDITS.md).{sa} Las fuentes tienen licencia SIL Open Font License 1.1 ([`assets/fonts/OFL.txt`](assets/fonts/OFL.txt)). Los nombres, direcciones, teléfonos, precios y opiniones son ficticios.',
        'sa': ' Las imágenes adaptadas de originales con licencia CC BY-SA conservan esa licencia.',
        'h_license': 'Licencia',
        'license': 'El código se publica con la [licencia PolyForm Noncommercial 1.0.0](LICENSE). Puedes usarlo, estudiarlo y modificarlo para cualquier fin no comercial: proyectos personales, aprendizaje, docencia, asociaciones. El uso comercial, por ejemplo entregar esta maqueta a un cliente, requiere una licencia aparte: abre una incidencia (issue) en este repositorio para solicitarla. Las fotos y las fuentes conservan sus propias licencias (ver arriba).',
        'h_security': 'Seguridad',
        'security': '¿Has encontrado una vulnerabilidad? Comunícala de forma privada desde la pestaña **Security** del repositorio («Report a vulnerability»), no en una incidencia pública. Consulta [SECURITY.md](SECURITY.md).',
        'h_more': 'Más maquetas', 'more': 'Forma parte de **Escaparates en movimiento**, una serie de cinco webs animadas al desplazarse:',
        'portfolio': 'Portafolio', 'on_both': '{} en ordenador y en móvil', 'anim': 'Vista previa animada de {}', 'on_desk': '{} en ordenador', 'on_mob': '{} en móvil',
        'poster': 'Vídeo promocional de {}, {}', 'demo': 'Demo', 'code': 'Código', 'video': 'Vídeo',
    },
}

# ---------------------------------------------------------------- projets
P = {
    'billot': {
        'repo': 'maison-billot', 'name': 'Maison Billot', 'color': 'B01F2E', 'color2': '0F2922', 'sa': True,
        'data': 'assets/js/data.fr.js · data.en.js · data.es.js',
        'kind': {'en': 'Artisan butcher · Lyon', 'fr': 'Boucherie artisanale · Lyon', 'es': 'Carnicería artesanal · Lyon'},
        'tagline': {
            'en': 'A scroll-animated website for an artisan butcher: beef explained cut by cut.',
            'fr': 'Le site vitrine animé d’une boucherie artisanale : la découpe du bœuf expliquée pièce par pièce.',
            'es': 'La web animada de una carnicería artesanal: el despiece del vacuno explicado pieza a pieza.'},
        'features': {
            'en': ['**Anatomy on scroll.** The Salers cow splits into 23 photographed cuts, each linked to its exact area on the animal.',
                   '**Cut guide.** Pick a dish (barbecue, pot-au-feu, tartare…) to see the cuts that suit it and where they sit, with instant search.',
                   '**Cut cards.** Tenderness, marbling, flavour, cooking methods, dishes, the butcher’s tip and the price per kilo.',
                   '**House-made, exploded.** The merguez shown ingredient by ingredient, plus pot-au-feu, bourguignon and barbecue kits.',
                   '**Ageing room.** Slide from day 0 to day 60 and watch the rib, the tenderness and the price change.',
                   '**Click & collect.** Build an order, pick a collection slot and get a summary to phone or text in. No payment on the site, and nothing is sent automatically.'],
            'fr': ['**Anatomie au défilement.** La vache Salers se découpe en 23 morceaux photographiés, chacun relié à sa zone exacte sur la bête.',
                   '**Guide des morceaux.** Choisissez un plat (barbecue, pot-au-feu, tartare…) pour voir les morceaux qui conviennent et où ils se trouvent, avec une recherche instantanée.',
                   '**Fiches morceaux.** Tendreté, persillé, goût, cuissons, plats, conseil du boucher et prix au kilo.',
                   '**Le fait maison en vue éclatée.** La merguez montrée ingrédient par ingrédient, et les kits pot-au-feu, bourguignon et barbecue.',
                   '**Cave de maturation.** Faites glisser de J+0 à J+60 et voyez la côte, la tendreté et le prix évoluer.',
                   '**Click & collect.** Composez un colis, choisissez un créneau de retrait et obtenez un récapitulatif à transmettre par téléphone ou par SMS. Aucun paiement sur le site, rien n’est envoyé automatiquement.'],
            'es': ['**Anatomía al desplazarse.** La vaca Salers se divide en 23 piezas fotografiadas, cada una unida a su zona exacta del animal.',
                   '**Guía de piezas.** Elige un plato (barbacoa, cocido, tartar…) para ver las piezas que le van y dónde están, con búsqueda instantánea.',
                   '**Fichas de cada pieza.** Terneza, veteado, sabor, cocciones, platos, el consejo del carnicero y el precio por kilo.',
                   '**Lo de la casa, despiezado.** La merguez ingrediente a ingrediente, y los kits de pot-au-feu, bourguignon y barbacoa.',
                   '**Cámara de maduración.** Desliza del día 0 al día 60 y mira cómo cambian el chuletón, la terneza y el precio.',
                   '**Recogida en tienda.** Prepara un pedido, elige una hora de recogida y obtén un resumen para llamar o enviar por SMS. Sin pagos en la web y sin envíos automáticos.']},
        'tech': {
            'en': 'The 23 areas are SVG polygons traced over the photo and clipped to the animal’s silhouette with a CSS mask; the scroll-driven scenes run on `requestAnimationFrame` with eased progress.',
            'fr': 'Les 23 zones sont des polygones SVG tracés sur la photo et découpés à la silhouette de l’animal par un masque CSS ; les scènes au défilement tournent avec `requestAnimationFrame` et une progression lissée.',
            'es': 'Las 23 zonas son polígonos SVG trazados sobre la foto y recortados a la silueta del animal con una máscara CSS; las escenas al desplazarse funcionan con `requestAnimationFrame` y un avance suavizado.'},
        'custom': {
            'en': 'Everything the shop updates lives in `assets/js/data.fr.js`, `data.en.js` and `data.es.js`: cuts and prices, house-made products, the counter, opening hours, phone number and interface text. Page copy is in `index.html`, `en.html` and `es.html`, and the colours are CSS variables at the top of `assets/css/style.css`.',
            'fr': 'Tout ce que la boutique met à jour se trouve dans `assets/js/data.fr.js`, `data.en.js` et `data.es.js` : morceaux et prix, produits maison, vitrine, horaires, numéro de téléphone et textes de l’interface. Les textes des pages sont dans `index.html`, `en.html` et `es.html`, et les couleurs sont des variables CSS en tête de `assets/css/style.css`.',
            'es': 'Todo lo que la tienda actualiza está en `assets/js/data.fr.js`, `data.en.js` y `data.es.js`: piezas y precios, elaboraciones propias, el mostrador, el horario, el teléfono y los textos de la interfaz. Los textos de las páginas están en `index.html`, `en.html` y `es.html`, y los colores son variables CSS al principio de `assets/css/style.css`.'},
    },
    'tafat': {
        'repo': 'tafat', 'name': 'Tafat', 'color': 'E0A21C', 'color2': '0E4A57', 'sa': True,
        'data': 'assets/js/config.fr.js · config.en.js · config.es.js',
        'kind': {'en': 'Home cleaning · Tigzirt, Kabylia', 'fr': 'Ménage à domicile · Tigzirt, Kabylie', 'es': 'Limpieza a domicilio · Tigzirt, Cabilia'},
        'tagline': {
            'en': 'A website for a women-run home cleaning team on the Kabylian coast: a squeegee wipes the window clean as you scroll.',
            'fr': 'Le site d’une équipe de femmes qui fait le ménage à domicile sur la côte kabyle : au défilement, une raclette nettoie la vitre.',
            'es': 'La web de un equipo de mujeres que limpia casas en la costa de Cabilia: al desplazarte, una rasqueta limpia el cristal.'},
        'features': {
            'en': ['**The window, cleaned on scroll.** A squeegee wipes the dirty picture window stroke by stroke, and the sea appears.',
                   '**Everything fits in a bucket.** An exploded view of the ten products and tools the team brings, from white vinegar to olive-oil soap.',
                   '**Room by room.** A checklist for each room, with hotspots on the photo and the microfibre colour code (green, yellow, red, blue).',
                   '**Quote in 30 seconds.** Home size, service, frequency and extras give a price range and write the WhatsApp message.',
                   '**Summer homes.** A timeline for families who live abroad, plus FAQ, reviews and the service area.',
                   '**Rooted in Kabylia.** Tifinagh touches (ⵜⴰⴼⴰⵜ, “light”) and a warm, local voice.'],
            'fr': ['**La vitre nettoyée au défilement.** Une raclette nettoie la baie vitrée sale, passage après passage, et la mer apparaît.',
                   '**Tout tient dans un seau.** Une vue éclatée des dix produits et outils que l’équipe apporte, du vinaigre blanc au savon à l’huile d’olive.',
                   '**Pièce par pièce.** Une checklist par pièce, avec des points sur la photo et le code couleur des microfibres (vert, jaune, rouge, bleu).',
                   '**Devis en 30 secondes.** Logement, prestation, fréquence et options donnent une fourchette de prix et rédigent le message WhatsApp.',
                   '**Maisons d’été.** Un déroulé pour les familles qui vivent à l’étranger, une FAQ, des avis et la zone d’intervention.',
                   '**Ancré en Kabylie.** Des touches de tifinagh (ⵜⴰⴼⴰⵜ, « la lumière ») et un ton chaleureux et local.'],
            'es': ['**El cristal, limpio al desplazarte.** Una rasqueta limpia el ventanal sucio pasada a pasada y aparece el mar.',
                   '**Todo cabe en un cubo.** Una vista despiezada de los diez productos y herramientas que lleva el equipo, del vinagre blanco al jabón de aceite de oliva.',
                   '**Estancia por estancia.** Una lista para cada estancia, con puntos sobre la foto y el código de colores de las microfibras (verde, amarillo, rojo, azul).',
                   '**Presupuesto en 30 segundos.** Vivienda, servicio, frecuencia y extras dan un rango de precios y redactan el mensaje de WhatsApp.',
                   '**Casas de verano.** Un calendario para las familias que viven fuera, además de preguntas frecuentes, opiniones y zona de servicio.',
                   '**Con raíces en Cabilia.** Detalles en tifinagh (ⵜⴰⴼⴰⵜ, «la luz») y un tono cercano y local.']},
        'tech': {
            'en': 'The dirt on the glass is a canvas layer erased along the squeegee’s path (`destination-out` compositing), and the bucket’s exploded view is built with CSS transforms.',
            'fr': 'La saleté sur la vitre est un calque canvas effacé sur le trajet de la raclette (composition `destination-out`), et la vue éclatée du seau repose sur des transformations CSS.',
            'es': 'La suciedad del cristal es una capa de canvas que se borra por el recorrido de la rasqueta (composición `destination-out`), y la vista despiezada del cubo usa transformaciones CSS.'},
        'custom': {
            'en': 'All the content is in `assets/js/config.fr.js`, `config.en.js` and `config.es.js`: brand, contact details (WhatsApp, phone, Facebook), services, bucket contents, rooms, quote pricing, FAQ and interface text. `demo: true` shows the demo notice and opens WhatsApp without a number; set it to `false` once the real details are in.',
            'fr': 'Tout le contenu est dans `assets/js/config.fr.js`, `config.en.js` et `config.es.js` : marque, coordonnées (WhatsApp, téléphone, Facebook), prestations, contenu du seau, pièces, tarifs du devis, FAQ et textes de l’interface. `demo: true` affiche la mention de démonstration et ouvre WhatsApp sans numéro ; passez-le à `false` une fois les vraies coordonnées renseignées.',
            'es': 'Todo el contenido está en `assets/js/config.fr.js`, `config.en.js` y `config.es.js`: marca, datos de contacto (WhatsApp, teléfono, Facebook), servicios, contenido del cubo, estancias, tarifas del presupuesto, preguntas frecuentes y textos de la interfaz. `demo: true` muestra el aviso de demostración y abre WhatsApp sin número; cámbialo a `false` cuando tengas los datos reales.'},
    },
    'nacre': {
        'repo': 'atelier-nacre', 'name': 'Atelier Nacre', 'color': '5B0E22', 'color2': 'B8924E', 'sa': False,
        'data': 'assets/js/config.fr.js · config.en.js · config.es.js',
        'kind': {'en': 'Nail studio · Bordeaux', 'fr': 'Prothésiste ongulaire · Bordeaux', 'es': 'Estudio de uñas · Burdeos'},
        'tagline': {
            'en': 'A website for a nail studio in Bordeaux: a gel set taken apart layer by layer, a colour try-on and online booking.',
            'fr': 'Le site d’un atelier de prothésiste ongulaire à Bordeaux : une pose démontée couche par couche, un essayage de couleur et la réservation en ligne.',
            'es': 'La web de un estudio de uñas en Burdeos: una manicura desmontada capa a capa, un probador de color y reservas en línea.'},
        'features': {
            'en': ['**Anatomy of a set.** The page zooms in on a nail in the photo, then the gel set comes apart into six 3D layers, each with its timing.',
                   '**Colour try-on.** Twelve shades and four finishes (gloss, matte, chrome, glitter) applied to the photo of a hand, keeping its natural reflections.',
                   '**Which shape?** Square, oval, almond, ballerina and stiletto morph into one another.',
                   '**Gallery and price list.** A filterable gallery with a lightbox, services with durations and prices, and the hygiene protocol.',
                   '**Booking in one line.** The booking buttons point to Planity, Treatwell, Booksy, Calendly or Instagram, as set in the config.'],
            'fr': ['**Anatomie d’une pose.** La page zoome sur l’ongle de la photo, puis la pose en gel se sépare en six couches en 3D, chacune avec sa durée.',
                   '**Essayage de couleur.** Douze teintes et quatre finitions (brillant, mat, chrome, pailleté) appliquées à la photo d’une main, reflets conservés.',
                   '**Quelle forme ?** Carré, ovale, amande, ballerine et stiletto se transforment l’une en l’autre.',
                   '**Galerie et tarifs.** Une galerie filtrable avec visionneuse, les prestations avec durées et prix, et le protocole d’hygiène.',
                   '**Réservation en une ligne.** Les boutons Réserver mènent à Planity, Treatwell, Booksy, Calendly ou Instagram, au choix dans la configuration.'],
            'es': ['**Anatomía de una manicura.** La página se acerca a una uña de la foto y la manicura de gel se separa en seis capas en 3D, cada una con su duración.',
                   '**Probador de color.** Doce tonos y cuatro acabados (brillo, mate, cromado, purpurina) aplicados a la foto de una mano, conservando sus reflejos.',
                   '**¿Qué forma?** Cuadrada, ovalada, almendra, bailarina y stiletto se transforman unas en otras.',
                   '**Galería y precios.** Una galería filtrable con visor, los servicios con duración y precio, y el protocolo de higiene.',
                   '**Reservas en una línea.** Los botones de reserva llevan a Planity, Treatwell, Booksy, Calendly o Instagram, según la configuración.']},
        'tech': {
            'en': 'The six layers are traced from the photo and stacked in CSS 3D; the try-on recolours the nails on a canvas with multiply blending and pixel masks, so highlights stay intact.',
            'fr': 'Les six couches sont tracées à partir de la photo et empilées en 3D CSS ; l’essayage recolore les ongles sur un canvas en mode produit (multiply) avec des masques au pixel près, pour garder les reflets.',
            'es': 'Las seis capas se trazan a partir de la foto y se apilan en 3D con CSS; el probador colorea las uñas en un canvas con fusión multiplicar y máscaras al píxel, para que los brillos se mantengan.'},
        'custom': {
            'en': 'All the content is in `assets/js/config.fr.js`, `config.en.js` and `config.es.js`: brand, address, opening hours, booking platform, layers, shades, shapes, gallery, prices, hygiene, reviews, FAQ and interface text. `demo: true` shows the demo notice and keeps the booking and Instagram buttons from leaving the page; set it to `false` with your real links.',
            'fr': 'Tout le contenu est dans `assets/js/config.fr.js`, `config.en.js` et `config.es.js` : marque, adresse, horaires, plateforme de réservation, couches, teintes, formes, galerie, tarifs, hygiène, avis, FAQ et textes de l’interface. `demo: true` affiche la mention de démonstration et empêche les boutons de réservation et Instagram de quitter la page ; passez-le à `false` avec vos vrais liens.',
            'es': 'Todo el contenido está en `assets/js/config.fr.js`, `config.en.js` y `config.es.js`: marca, dirección, horario, plataforma de reservas, capas, tonos, formas, galería, precios, higiene, opiniones, preguntas frecuentes y textos de la interfaz. `demo: true` muestra el aviso de demostración e impide que los botones de reserva e Instagram salgan de la página; cámbialo a `false` con tus enlaces reales.'},
    },
    'tiziri': {
        'repo': 'tiziri', 'name': 'Tiziri', 'color': 'B4532F', 'color2': '1C1714', 'sa': False, 'videos': True,
        'paths': {'fr': '', 'en': 'en/', 'es': 'es/'}, 'b_langs': 'FR · AR · EN · ES',
        'kind': {'en': 'Fashion boutique · Tigzirt, Kabylia', 'fr': 'Boutique de mode · Tigzirt, Kabylie', 'es': 'Tienda de moda · Tigzirt, Cabilia'},
        'tagline': {
            'en': 'A clothing boutique’s wardrobe online: every piece, photographed in the shop, is worn by a wooden mannequin that comes to life.',
            'fr': 'La garde-robe d’une boutique de vêtements en ligne : chaque pièce, photographiée en magasin, est portée par un mannequin en bois qui prend vie.',
            'es': 'El armario de una tienda de ropa en línea: cada prenda, fotografiada en la tienda, la lleva un maniquí de madera que cobra vida.'},
        'features': {
            'en': ['**A live 3D studio.** On the home page, Elle and Lui, wooden mannequins modelled in code, pose in a sunlit studio and follow the cursor.',
                   '**From shop photo to runway.** Each garment is photographed as it is in the shop, cut out, then worn by Elle or Lui, articulated wooden mannequins that start walking.',
                   '**Fitting room.** Pick a piece and watch the mannequin try it on, pose after pose, then walk.',
                   '**The runway.** The whole shop parades on a pinned, scroll-driven catwalk.',
                   '**Every piece up close.** Worn, ghost mannequin, studio and raw photo: the raw view shows the untouched pixels, and colours are read from the photo.',
                   '**Four languages.** French, Arabic (right to left), English and Spanish.',
                   '**Order on WhatsApp.** Each piece writes its own message: name, price and link; collect in store or cash on delivery.'],
            'fr': ['**Un studio 3D en direct.** Sur l’accueil, Elle et Lui, des mannequins en bois modélisés par le code, prennent la pose dans un studio baigné de soleil et suivent le curseur.',
                   '**De la photo au défilé.** Chaque vêtement est photographié tel quel en boutique, détouré, puis porté par Elle ou Lui, des mannequins articulés en bois qui se mettent en marche.',
                   '**Cabine d’essayage.** Choisissez une pièce : le mannequin l’essaie, pose après pose, puis défile.',
                   '**Le défilé.** Toute la boutique défile sur un podium épinglé, piloté par le défilement.',
                   '**Chaque pièce de près.** Portée, mannequin invisible, studio et photo brute : la vue brute montre les vrais pixels, et les couleurs sont relevées sur la photo.',
                   '**Quatre langues.** Français, arabe (de droite à gauche), anglais et espagnol.',
                   '**Commande sur WhatsApp.** Chaque pièce rédige son message : nom, prix et lien ; retrait en boutique ou paiement à la livraison.'],
            'es': ['**Un estudio 3D en directo.** En la portada, Elle y Lui, maniquíes de madera modelados por código, posan en un estudio bañado de sol y siguen el cursor.',
                   '**De la foto al desfile.** Cada prenda se fotografía tal cual en la tienda, se recorta y la llevan Elle o Lui, maniquíes articulados de madera que echan a andar.',
                   '**Probador.** Elige una prenda: el maniquí se la prueba, pose tras pose, y luego desfila.',
                   '**El desfile.** Toda la tienda desfila en una pasarela fija que avanza al desplazarte.',
                   '**Cada prenda de cerca.** Puesta, maniquí invisible, estudio y foto en bruto: la vista en bruto muestra los píxeles reales y los colores se toman de la foto.',
                   '**Cuatro idiomas.** Francés, árabe (de derecha a izquierda), inglés y español.',
                   '**Pedidos por WhatsApp.** Cada prenda redacta su mensaje: nombre, precio y enlace; recogida en tienda o pago contra reembolso.']},
        'tech': {
            'en': 'Every garment is processed once and kept in a “wardrobe”: a cut-out made on the Mac (Apple Vision), then worn views, a ghost-mannequin shot and an 8-second video generated with Google Flow from the photo. Nothing is generated when the site is built or viewed.',
            'fr': 'Chaque vêtement est traité une seule fois et rangé dans une « garde-robe » : détourage sur le Mac (Apple Vision), puis vues portées, mannequin invisible et vidéo de 8 secondes générés avec Google Flow à partir de la photo. Rien n’est généré à la construction du site ni à la visite.',
            'es': 'Cada prenda se procesa una sola vez y se guarda en un «armario»: recorte en el Mac (Apple Vision) y, a partir de la foto, vistas puestas, maniquí invisible y un vídeo de 8 segundos generados con Google Flow. No se genera nada al construir la web ni al visitarla.'},
        'tech_common': {
            'en': ['Built with Astro (static output): this repository is the published site, ready to serve. GSAP, Lenis and Three.js drive the animations.',
                   'WebP images, self-hosted fonts, `prefers-reduced-motion` support, videos that load only when needed, and layouts checked from 360 px wide.',
                   'Privacy by design: no cookies, no analytics, no third-party requests, and a strict Content Security Policy.'],
            'fr': ['Construit avec Astro (site statique) : ce dépôt est le site publié, prêt à servir. GSAP, Lenis et Three.js animent les pages.',
                   'Images WebP, polices hébergées avec le site, prise en compte de `prefers-reduced-motion`, vidéos chargées seulement quand il le faut, et mise en page vérifiée dès 360 px de large.',
                   'Respect de la vie privée : ni cookies, ni mesure d’audience, ni requête vers un service tiers, et une politique de sécurité du contenu (CSP) stricte.'],
            'es': ['Hecha con Astro (web estática): este repositorio es la web publicada, lista para servir. GSAP, Lenis y Three.js dan vida a las páginas.',
                   'Imágenes WebP, fuentes alojadas con la web, compatibilidad con `prefers-reduced-motion`, vídeos que solo se cargan cuando hace falta y diseño comprobado desde 360 px de ancho.',
                   'Privacidad desde el diseño: sin cookies, sin analítica, sin peticiones a terceros y con una política de seguridad de contenido (CSP) estricta.']},
        'langs_text': {
            'en': 'The site ships in French (root, default), Arabic (`ar/`, right to left), English (`en/`) and Spanish (`es/`). Every page exists in each language as static HTML, so search engines and link previews see the right text, and the language switcher sits in the header.',
            'fr': 'Le site existe en français (à la racine, par défaut), en arabe (`ar/`, de droite à gauche), en anglais (`en/`) et en espagnol (`es/`). Chaque page existe dans chaque langue en HTML statique : les moteurs de recherche et les aperçus de liens voient le bon texte, et le sélecteur de langue se trouve dans l’en-tête.',
            'es': 'La web está disponible en francés (en la raíz, por defecto), árabe (`ar/`, de derecha a izquierda), inglés (`en/`) y español (`es/`). Cada página existe en cada idioma como HTML estático, así que los buscadores y las vistas previas de enlaces ven el texto correcto; el selector de idioma está en la cabecera.'},
        'run': {
            'en': ('The site is built to live at `/tiziri/`, as on GitHub Pages. Serve the folder that contains it with any static server, for example Python:',
                   'Then open <http://localhost:8000/tiziri/>.'),
            'fr': ('Le site est construit pour vivre sous `/tiziri/`, comme sur GitHub Pages. Servez le dossier qui le contient avec n’importe quel serveur statique, par exemple Python :',
                   'Ouvrez ensuite <http://localhost:8000/tiziri/>.'),
            'es': ('La web está preparada para vivir en `/tiziri/`, como en GitHub Pages. Sirve la carpeta que la contiene con cualquier servidor estático, por ejemplo Python:',
                   'Después abre <http://localhost:8000/tiziri/>.')},
        'custom': {
            'en': 'This repository holds the built site. Its source, an Astro project with the wardrobe (one folder per garment: photo, cut-out, views, video and texts in four languages), lives in a private workspace. Shop details (name, WhatsApp number, address, opening hours, delivery) sit in one configuration file; `demo: true` shows the demo notice and opens WhatsApp without a number. Want this site for your shop? Open an issue.',
            'fr': 'Ce dépôt contient le site construit. Sa source, un projet Astro avec la garde-robe (un dossier par vêtement : photo, détourage, vues, vidéo et textes en quatre langues), est dans un espace de travail privé. Les informations de la boutique (nom, numéro WhatsApp, adresse, horaires, livraison) tiennent dans un seul fichier de configuration ; `demo: true` affiche la mention de démonstration et ouvre WhatsApp sans numéro. Vous voulez ce site pour votre boutique ? Ouvrez un ticket (issue).',
            'es': 'Este repositorio contiene la web construida. Su código fuente, un proyecto Astro con el armario (una carpeta por prenda: foto, recorte, vistas, vídeo y textos en cuatro idiomas), está en un espacio de trabajo privado. Los datos de la tienda (nombre, número de WhatsApp, dirección, horario, envíos) están en un único archivo de configuración; `demo: true` muestra el aviso de demostración y abre WhatsApp sin número. ¿Quieres esta web para tu tienda? Abre una incidencia (issue).'},
        'credits': {
            'en': 'Four garments were photographed in a boutique in Tigzirt; the eight demo pieces come from Unsplash photos. Elle and Lui, the wooden mannequins, are modelled in code (Three.js); the worn views, ghost-mannequin shots and videos were generated with Google Flow from their renders and these photos, and are labelled as such on each product page. Full credits are in [CREDITS.md](CREDITS.md). Fonts are under the SIL Open Font License 1.1 ([`assets/fonts/OFL.txt`](assets/fonts/OFL.txt)). The shop name, phone number and prices are fictional.',
            'fr': 'Quatre vêtements ont été photographiés dans une boutique de Tigzirt ; les huit pièces de démonstration viennent de photos Unsplash. Elle et Lui, les mannequins en bois, sont modélisés par le code (Three.js) ; les vues portées, les vues en mannequin invisible et les vidéos ont été générées avec Google Flow à partir de leurs rendus et de ces photos, et sont signalées comme telles sur chaque fiche. Tous les crédits sont dans [CREDITS.md](CREDITS.md). Les polices sont sous licence SIL Open Font License 1.1 ([`assets/fonts/OFL.txt`](assets/fonts/OFL.txt)). Le nom de la boutique, le numéro et les prix sont fictifs.',
            'es': 'Cuatro prendas se fotografiaron en una tienda de Tigzirt; las ocho prendas de demostración proceden de fotos de Unsplash. Elle y Lui, los maniquíes de madera, están modelados por código (Three.js); las vistas puestas, las de maniquí invisible y los vídeos se generaron con Google Flow a partir de sus renders y de esas fotos, y así se indica en cada ficha. Todos los créditos están en [CREDITS.md](CREDITS.md). Las fuentes tienen licencia SIL Open Font License 1.1 ([`assets/fonts/OFL.txt`](assets/fonts/OFL.txt)). El nombre de la tienda, el teléfono y los precios son ficticios.'},
    },
    # Lalla Warda a sa propre documentation en quatre langues (sources/cosmetiques-kenitra/docs.py) : main() n'y écrit rien
    'warda': {
        'repo': 'lalla-warda', 'name': 'Lalla Warda', 'color': 'B23F66', 'color2': '6E1F3A', 'sa': True, 'videos': True, 'own_docs': True,
        'kind': {'en': 'Natural cosmetics · Kenitra, Morocco', 'fr': 'Cosmétiques naturels · Kénitra, Maroc', 'es': 'Cosmética natural · Kenitra, Marruecos'},
        'tagline': {
            'en': 'The website of a natural cosmetics brand from Kenitra: a 3D rose blooms into a serum bottle, and every product shows what it is made of and how it goes on the face and hair.',
            'fr': 'Le site d’une marque de cosmétiques naturels de Kénitra : une rose en 3D s’ouvre sur un flacon de sérum, et chaque soin montre ce qu’il contient et comment il s’applique sur le visage et les cheveux.',
            'es': 'La web de una marca de cosmética natural de Kenitra: una rosa en 3D se abre hasta revelar un frasco de sérum, y cada producto muestra de qué está hecho y cómo se aplica en el rostro y el cabello.'},
    },
}


def live(p, lang):
    return f"{SITE}{p['repo']}/{p.get('paths', PAGE)[lang]}"


def watch_url(pid, lang):
    return f'{SITE}{PAGE[lang]}#{pid}'


def project_readme(pid, lang):
    p, t = P[pid], C[lang]
    n = p['name']
    others = [q for q in P if q != pid]
    fmts = ('169', '45', '916')
    widths = {'169': 360, '45': 180, '916': 152}
    lines = [
        '<div align="center">', '',
        f'<a href="{live(p, lang)}"><img src="{M}/readme/{pid}-banner-{lang}.jpg" alt="{t["on_both"].format(n)}" width="100%"></a>', '',
        f'# {n}', '',
        f'**{p["tagline"][lang]}**', '',
        t['langs'], '',
        ' '.join([badge(t['b_demo'], 'hoshuko.github.io', p['color'], live(p, lang)),
                  badge(t['b_video'], t['b_video_msg'], p['color2'], watch_url(pid, lang)),
                  badge(t['b_langs'], p.get('b_langs', 'FR · EN · ES'), '555555', f'#{slug(t["h_langs"])}'),
                  badge(t['b_lic'], 'PolyForm Noncommercial', '555555', 'LICENSE')]), '',
        '</div>', '',
        f'## {t["h_preview"]}', '',
        f'<a href="{watch_url(pid, lang)}"><img src="{M}/readme/{pid}-preview-{lang}.webp" alt="{t["anim"].format(n)}" width="100%"></a>', '',
        f'{t["preview"]} [{t["watch"]}]({watch_url(pid, lang)})', '',
        f'## {t["h_features"]}', '',
        *[f'- {f}' for f in p['features'][lang]], '',
        f'## {t["h_shots"]}', '',
        f'| {t["desktop"]} | {t["mobile"]} |', '| :---: | :---: |',
        f'| <img src="{M}/shots/{pid}-desktop-{lang}.webp" alt="{t["on_desk"].format(n)}" width="560"> | <img src="{M}/shots/{pid}-mobile-{lang}.webp" alt="{t["on_mob"].format(n)}" width="200"> |', '',
        f'## {t["h_videos"]}', '',
        t['videos'], '',
        '| ' + ' | '.join(t['fmt'][f] for f in fmts) + ' |', '| :---: | :---: | :---: |',
        '| ' + ' | '.join(f'<a href="{M}/video/{pid}-{f}-{lang}.mp4"><img src="{M}/video/{pid}-{f}-{lang}.jpg" alt="{t["poster"].format(n, t["fmt"][f])}" width="{widths[f]}"></a>' for f in fmts) + ' |',
        '| ' + ' | '.join(f'<sub>{t["use"][f]}</sub>' for f in fmts) + ' |', '',
        f'## {t["h_langs"]}', '',
        p['langs_text'][lang] if 'langs_text' in p else t['langs_text'], '',
        f'## {t["h_tech"]}', '',
        f'- {p["tech"][lang]}',
        *[f'- {x.format(data=p.get("data", ""))}' for x in (p['tech_common'][lang] if 'tech_common' in p else t['tech'])], '',
        f'## {t["h_run"]}', '',
        p['run'][lang][0] if 'run' in p else t['run'], '',
        *(['```bash', f'git clone https://github.com/hoshuko/{p["repo"]}.git', 'python3 -m http.server 8000', '```'] if 'run' in p else
          ['```bash', f'git clone https://github.com/hoshuko/{p["repo"]}.git', f'cd {p["repo"]}', 'python3 -m http.server 8000', '```']), '',
        p['run'][lang][1] if 'run' in p else t['run_after'], '',
        f'## {t["h_custom"]}', '',
        p['custom'][lang], '',
        f'## {t["h_credits"]}', '',
        p['credits'][lang] if 'credits' in p else t['credits'].format(sa=t['sa'] if p['sa'] else ''), '',
        f'## {t["h_license"]}', '',
        t['license'], '',
        f'## {t["h_security"]}', '',
        t['security'], '',
        f'## {t["h_more"]}', '',
        t['more'], '',
        *[f'- **[{P[q]["name"]}]({GH}/{P[q]["repo"]}/blob/main/{README[lang]})**: {P[q]["tagline"][lang]}' for q in others], '',
        f'{t["portfolio"]}: <{SITE}{PAGE[lang]}> · YouTube: <{YT}>',
    ]
    return '\n'.join(lines)


def slug(h):
    """Ancre GitHub d'un titre (minuscules, espaces → tirets, ponctuation retirée)."""
    import re
    s = h.strip().lower()
    s = re.sub(r'[^\w\- ]', '', s)
    return s.replace(' ', '-')


# ---------------------------------------------------------------- portfolio
PT = {
    'en': {'title': 'Storefronts in motion',
           'tagline': 'Five scroll-animated website templates for local businesses, each in French, English and Spanish, with promo videos in three formats.',
           'b_site': 'Portfolio', 'h_tpl': 'The templates', 'h_repo': 'About this repository',
           'repo': ['`index.html`, `en.html`, `es.html`: the portfolio in French, English and Spanish. On a first visit, the French home page switches to English or Spanish when that is the browser’s language; a choice made with the language switcher is remembered.',
                    '`assets/video/`: the promo videos (lighter 720p versions) in every format and language, with their posters.',
                    '`assets/shots/` and `assets/readme/`: the screenshots, banners and animated previews shown here and in the templates’ READMEs.'],
           'repo_intro': 'This repository is the portfolio itself, published with GitHub Pages at <https://hoshuko.github.io/>.',
           'tech': 'Static HTML, CSS and JavaScript, self-hosted fonts, no cookies, no analytics, no third-party requests, and a strict Content Security Policy.',
           'credits': 'The screenshots and videos show photos from Unsplash, Pexels and Wikimedia Commons, and photos taken in a shop (Tiziri, with views and videos generated by Google Flow), credited in [CREDITS.md](CREDITS.md) and in each template’s own credits. The music and sound effects of the videos are generated. Fonts: SIL Open Font License 1.1 ([`assets/fonts/OFL.txt`](assets/fonts/OFL.txt)).',
           'license': 'Code under the [PolyForm Noncommercial License 1.0.0](LICENSE).'},
    'fr': {'title': 'Vitrines en mouvement',
           'tagline': 'Cinq maquettes de sites vitrines animés au défilement pour les commerces de proximité, chacune en français, en anglais et en espagnol, avec des vidéos promo en trois formats.',
           'b_site': 'Portfolio', 'h_tpl': 'Les maquettes', 'h_repo': 'À propos de ce dépôt',
           'repo': ['`index.html`, `en.html`, `es.html` : le portfolio en français, en anglais et en espagnol. À la première visite, la page d’accueil en français bascule vers l’anglais ou l’espagnol si c’est la langue du navigateur ; un choix fait avec le sélecteur de langue est mémorisé.',
                    '`assets/video/` : les vidéos promo (versions allégées en 720p) dans chaque format et chaque langue, avec leurs affiches.',
                    '`assets/shots/` et `assets/readme/` : les captures, bannières et aperçus animés affichés ici et dans les README des maquettes.'],
           'repo_intro': 'Ce dépôt est le portfolio lui-même, publié avec GitHub Pages à l’adresse <https://hoshuko.github.io/>.',
           'tech': 'HTML, CSS et JavaScript statiques, polices hébergées avec le site, ni cookies, ni mesure d’audience, ni requête vers un tiers, et une politique de sécurité du contenu (CSP) stricte.',
           'credits': 'Les captures et les vidéos montrent des photos d’Unsplash, de Pexels et de Wikimedia Commons, et des photos prises en boutique (Tiziri, avec des vues et des vidéos générées par Google Flow), créditées dans [CREDITS.md](CREDITS.md) et dans les crédits de chaque maquette. La musique et les bruitages des vidéos sont générés. Polices : SIL Open Font License 1.1 ([`assets/fonts/OFL.txt`](assets/fonts/OFL.txt)).',
           'license': 'Code sous [licence PolyForm Noncommercial 1.0.0](LICENSE).'},
    'es': {'title': 'Escaparates en movimiento',
           'tagline': 'Cinco maquetas de webs escaparate animadas al desplazarse para comercios de barrio, cada una en francés, inglés y español, con vídeos promocionales en tres formatos.',
           'b_site': 'Portafolio', 'h_tpl': 'Las maquetas', 'h_repo': 'Sobre este repositorio',
           'repo': ['`index.html`, `en.html`, `es.html`: el portafolio en francés, inglés y español. En la primera visita, la página de inicio en francés cambia al inglés o al español si ese es el idioma del navegador; la elección hecha con el selector de idioma se recuerda.',
                    '`assets/video/`: los vídeos promocionales (versiones ligeras en 720p) en cada formato e idioma, con sus pósteres.',
                    '`assets/shots/` y `assets/readme/`: las capturas, banners y vistas previas animadas que se muestran aquí y en los README de las maquetas.'],
           'repo_intro': 'Este repositorio es el propio portafolio, publicado con GitHub Pages en <https://hoshuko.github.io/>.',
           'tech': 'HTML, CSS y JavaScript estáticos, fuentes alojadas con la web, sin cookies, sin analítica, sin peticiones a terceros y con una política de seguridad de contenido (CSP) estricta.',
           'credits': 'Las capturas y los vídeos muestran fotos de Unsplash, Pexels y Wikimedia Commons, y fotos hechas en una tienda (Tiziri, con vistas y vídeos generados con Google Flow), acreditadas en [CREDITS.md](CREDITS.md) y en los créditos de cada maqueta. La música y los efectos de sonido de los vídeos son generados. Fuentes: SIL Open Font License 1.1 ([`assets/fonts/OFL.txt`](assets/fonts/OFL.txt)).',
           'license': 'Código con la [licencia PolyForm Noncommercial 1.0.0](LICENSE).'},
}


def cards(lang, readme_links=True):
    t = C[lang]
    head = '| ' + ' | '.join(f'<a href="{live(P[q], lang)}"><img src="{M}/readme/{q}-banner-{lang}.jpg" alt="{t["on_both"].format(P[q]["name"])}" width="260"></a>' for q in P) + ' |'
    sep = '|' + ' :---: |' * len(P)
    code = lambda q: f'{GH}/{P[q]["repo"]}/blob/main/{README[lang]}' if readme_links else f'{GH}/{P[q]["repo"]}'
    info = '| ' + ' | '.join(f'**{P[q]["name"]}**<br><sub>{P[q]["kind"][lang]}</sub><br>[{t["demo"]}]({live(P[q], lang)}) · [{t["code"]}]({code(q)}) · [{t["video"]}]({watch_url(q, lang)})' for q in P) + ' |'
    return [head, sep, info]


def portfolio_readme(lang):
    t, c = PT[lang], C[lang]
    return '\n'.join([
        '<div align="center">', '',
        f'<a href="{SITE}{PAGE[lang]}"><img src="{M}/img/og-{lang}.jpg" alt="{t["title"]}" width="100%"></a>', '',
        f'# {t["title"]}', '',
        f'**{t["tagline"]}**', '',
        c['langs'], '',
        ' '.join([badge(t['b_site'], 'hoshuko.github.io', '16181B', SITE + PAGE[lang]), badge('YouTube', '@Hosh-uko', 'C4302B', YT),
                  badge(c['b_lic'], 'PolyForm Noncommercial', '555555', 'LICENSE')]), '',
        '</div>', '',
        f'## {t["h_tpl"]}', '',
        *cards(lang), '',
        f'## {t["h_repo"]}', '',
        t['repo_intro'], '',
        *[f'- {x}' for x in t['repo']], '',
        f'## {c["h_tech"]}', '',
        t['tech'], '',
        f'## {c["h_credits"]}', '',
        t['credits'], '',
        f'## {c["h_license"]}', '',
        t['license'] + ' ' + c['security'],
    ])


# ---------------------------------------------------------------- profil
PROFILE = {
    'en': ('Scroll-animated websites and promo videos for local businesses',
           'Showcase websites for local businesses, each built around one signature scroll animation, available in French, English and Spanish, and delivered with a 60-second promo video in three formats (16:9, 4:5, 9:16).',
           'Everything is open source under the PolyForm Noncommercial licence: have a look at the code, try the demos, watch the videos.'),
    'fr': ('Sites vitrines animés et vidéos promo pour les commerces de proximité',
           'Des sites vitrines pour les commerces de proximité, chacun construit autour d’une animation phare au défilement, en français, en anglais et en espagnol, et livré avec une vidéo promo de 60 secondes en trois formats (16:9, 4:5, 9:16).',
           'Tout le code est ouvert, sous licence PolyForm Noncommercial : parcourez le code, essayez les démos, regardez les vidéos.'),
    'es': ('Webs animadas y vídeos promocionales para comercios de barrio',
           'Webs escaparate para comercios de barrio, cada una construida en torno a una animación estrella al desplazarse, disponibles en francés, inglés y español, y acompañadas de un vídeo promocional de 60 segundos en tres formatos (16:9, 4:5, 9:16).',
           'Todo el código es abierto, con licencia PolyForm Noncommercial: explora el código, prueba las demos y mira los vídeos.'),
}
PROFILE_H = {'en': 'English', 'fr': 'Français', 'es': 'Español'}


def profile_readme():
    out = ['<div align="center">', '',
           f'<a href="{SITE}"><img src="{M}/img/og-en.jpg" alt="Storefronts in motion · hoshuko" width="100%"></a>', '',
           f'**{PROFILE["en"][0]}**', '',
           ' '.join([badge('Portfolio', 'hoshuko.github.io', '16181B', SITE), badge('YouTube', '@Hosh-uko', 'C4302B', YT)]), '',
           '[English](#english) · [Français](#français) · [Español](#español)', '',
           '</div>', '']
    for lang in ('en', 'fr', 'es'):
        title, text, oss = PROFILE[lang]
        out += [f'## {PROFILE_H[lang]}', '', f'**{title}.** {text}', '', *cards(lang), '', oss,
                f'{C[lang]["portfolio"]}: <{SITE}{PAGE[lang]}> · YouTube: <{YT}>', '']
    return '\n'.join(out)


# ---------------------------------------------------------------- licence, crédits, sécurité
def license_text():
    body = open(os.path.join(BASE, '_legal', 'PolyForm-Noncommercial-1.0.0.md'), encoding='utf-8').read()
    return f'Required Notice: Copyright {YEAR} hoshuko (https://github.com/hoshuko)\n\n' + body


CC = {'CC BY-SA 2.0': 'https://creativecommons.org/licenses/by-sa/2.0/', 'CC BY-SA 3.0': 'https://creativecommons.org/licenses/by-sa/3.0/',
      'CC BY-SA 4.0': 'https://creativecommons.org/licenses/by-sa/4.0/', 'CC0 1.0': 'https://creativecommons.org/publicdomain/zero/1.0/'}
enc_url = lambda u: u.replace('(', '%28').replace(')', '%29')
COMMONS = {
    'billot': [('assets/img/cow.webp', 'SalersBreed YoungCow.JPG', 'https://commons.wikimedia.org/wiki/File:SalersBreed_YoungCow.JPG', 'B.navez', 'CC BY-SA 3.0', 'background removed, resized, WebP'),
               ('assets/img/bavette.webp', 'Flank Steak piece of meat.jpg', 'https://commons.wikimedia.org/wiki/File:Flank_Steak_piece_of_meat.jpg', 'Bortz60', 'CC BY-SA 3.0', 'background removed, resized, WebP'),
               ('assets/img/queue.webp', 'Raw oxtail-01.jpg', 'https://commons.wikimedia.org/wiki/File:Raw_oxtail-01.jpg', 'FotoosVanRobin', 'CC BY-SA 2.0', 'background removed, resized, WebP'),
               ('assets/img/merguez.webp', 'Merguez in Bratpfanne roh.jpg', 'https://commons.wikimedia.org/wiki/File:Merguez_in_Bratpfanne_roh.jpg', 'Stanislaus der Lausige', 'CC BY-SA 4.0', 'background removed, resized, WebP'),
               ('assets/img/harissa.webp', 'Harissa Sauce.JPG', 'https://commons.wikimedia.org/wiki/File:Harissa_Sauce.JPG', 'Miansari66', 'CC0 1.0', 'background removed, resized, WebP')],
    'tafat': [('assets/img/tigzirt-ville.webp', 'Tigzirt - Tizi Ouzou Province (Algeria).jpg', 'https://commons.wikimedia.org/wiki/File:Tigzirt_-_Tizi_Ouzou_Province_(Algeria).jpg', 'Fayeqalnatour', 'CC BY-SA 4.0', 'resized, WebP'),
              ('assets/img/tigzirt-plage.webp', 'Wiki Loves Earth 2014dz8 tamda ouguemoun tizi-ouzou.JPG', 'https://commons.wikimedia.org/wiki/File:Wiki_Loves_Earth_2014dz8_tamda_ouguemoun_tizi-ouzou.JPG', 'Yazid Leharani', 'CC BY-SA 3.0', 'cropped, resized, WebP'),
              ('assets/img/tigzirt-ruines.webp', 'Tigzirt roman ruins 02.jpg', 'https://commons.wikimedia.org/wiki/File:Tigzirt_roman_ruins_02.jpg', 'MohAdm', 'CC BY-SA 4.0', 'resized, WebP')],
    'nacre': [],
    'tiziri': [],
    'warda': [('assets/img/i-rose.webp', 'Rosa Damascena kelaa Mgouna.jpg', 'https://commons.wikimedia.org/wiki/File:Rosa_Damascena_kelaa_Mgouna.jpg', 'Nabil Talibi', 'CC BY-SA 4.0', 'background removed, resized, WebP'),
              ('assets/img/i-argan.webp', 'Argania spinosa MHNT.BOT.2010.12.2.jpg', 'https://commons.wikimedia.org/wiki/File:Argania_spinosa_MHNT.BOT.2010.12.2.jpg', 'Roger Culos', 'CC BY-SA 3.0', 'one kernel cut out, resized, WebP'),
              ('assets/img/i-figue.webp', 'Fruit of Indian fig opuntia (Opuntia ficus-indica), Agios Sostis, Tinos, Greece julesvernex2.jpg',
               'https://commons.wikimedia.org/wiki/File:Fruit_of_Indian_fig_opuntia_(Opuntia_ficus-indica),_Agios_Sostis,_Tinos,_Greece_julesvernex2.jpg', 'Jules Verne Times Two', 'CC BY-SA 4.0', 'background removed, resized, WebP')],
}
STOCK = {
    'billot': [('Unsplash', 'Alexander Van Steenberge, Eiliv Aceron, David Foodphototasty, Sergey Kotenev, Kelsey Todd, Anastasia Malysh, hyun-su Jung, Jakob Trost, Studio Crevettes, Sally Cox, Wesual Click, Marcos Paulo Prado, Skyler Ewing, Paras Kapoor, Olivier Amyot, Kyle Mackie, Manjunath Kammar, Katrina Wright, Mockup Graphics',
                'cuts of beef, lamb and spices (backgrounds removed)')],
    'tafat': [('Unsplash', 'Gábor Szűts (hero window, dirt effect added), Vitaly Gariev, PuroClean, Antonio Sessa, Zac Cain, Suzanne Fell, Phil Hearing, Paolo Bendandi, Francesca Tosolini, SYKS, Patrick Lalonde, Galen Crout, Artem Makarov, Kenny, Maria Kovalets, nemo, Precious Plastic Melbourne, Scurtu Corina, Annie Spratt, JESHOOTS.COM, Mike Hindle',
               'services, rooms, summer home, products'),
              ('Pexels', 'Blissful Place Cleaning (squeegee), Margo Evardson (rugs in the sun), Ksenia Chernaya (after building work), Srattha Nualsate (green spray bottle), Karolina Grabowska (Kaboompics), Polina Tankilevitch (soap, microfibre cloths)',
               'bucket contents and services')],
    'nacre': [('Unsplash', 'Ellie Eshaghi, Chelson Tamares (hand in the try-on and anatomy sections); Jodene Isakowitz, Margarita Yutsaytis, de Aura, zain ali, Konstantin Shmatov, Tainara Paixão, Divaris Shirichena, 한별 정, Noel Oviedo (gallery); Daniel, Ondrej Supitar, pure julia, H&CO, Karolina De Costa, Daria Trofimova, Tasha Kostyuk, Katie Harp, Kristina Tochilko, Logan Voss (studio, tools and textures)',
               'try-on, anatomy, gallery, studio'),
              ('Pexels', 'Roman Titov, Anna McDonald, honggyu kim, Leeloo The First, Artem Podrez, cottonbro studio', 'gallery and studio')],
    'tiziri': [('Unsplash', 'Mavi Atlas, Derick McKinney, Tobias Tullius, Nikola Tasic, Léa Ochel, Lisanto, Alessandra Caretto, H&CO',
                'the eight demo pieces (see the table below)')],
}
# Tiziri : d'où vient chaque pièce de démonstration (photo Unsplash), et ce qui est généré par IA.
TIZIRI_DEMO = [('robe-brodee-velours', 'cAOxU0nLheI', 'Mavi Atlas'), ('blouson-cuir-marron', '3OFBcQQTN64', 'Derick McKinney'),
               ('bomber-terracotta', 'Fg15LdqpWrs', 'Tobias Tullius'), ('veste-laine-brune', 'gJtwWqMiyUw', 'Nikola Tasic'),
               ('perfecto-noir', 'nsRBbE6-YLs', 'Léa Ochel'), ('chemise-blanche', 've2dwNxZ5Rg', 'Lisanto'),
               ('robe-bustier-blanche', 'pHA6KL_HpoE', 'Alessandra Caretto'), ('top-noir-sans-manches', 'cp-VMJ-mdKs', 'H&CO')]
TIZIRI_NOTES = ['## Tiziri: photos taken in the shop · photos prises en boutique · fotos hechas en la tienda', '',
                '`pull-leopard`, `robe-maille-grise`, `gilet-long-beige`, `pantalon-gris`: photographed in a clothing boutique in Tigzirt. '
                'Photographiées dans une boutique de vêtements de Tigzirt. Fotografiadas en una tienda de ropa de Tigzirt.', '',
                '## AI-generated images and videos · Images et vidéos générées par IA · Imágenes y vídeos generados con IA', '',
                'Elle and Lui, the wooden mannequins, are modelled in code (Three.js). The worn views, the ghost-mannequin shots and the 8-second videos were generated with Google Flow '
                '(Nano Banana Pro for images, Omni Flash for videos) from their renders and the photos above. The studio and raw-photo views keep the real pixels.  ',
                'Elle et Lui, les mannequins en bois, sont modélisés par le code (Three.js). Les vues portées, les vues en mannequin invisible et les vidéos de 8 secondes ont été générées avec Google Flow '
                '(Nano Banana Pro pour les images, Omni Flash pour les vidéos) à partir de leurs rendus et de ces photos. Les vues studio et photo brute gardent les vrais pixels.  ',
                'Elle y Lui, los maniquíes de madera, están modelados por código (Three.js). Las vistas puestas, las de maniquí invisible y los vídeos de 8 segundos se generaron con Google Flow '
                '(Nano Banana Pro para las imágenes, Omni Flash para los vídeos) a partir de sus renders y de esas fotos. Las vistas de estudio y de foto en bruto conservan los píxeles reales.', '']
LIC_URL = {'Unsplash': 'https://unsplash.com/license', 'Pexels': 'https://www.pexels.com/license/'}
FONTS = {'billot': 'Bodoni Moda, IBM Plex Mono, Instrument Sans', 'tafat': 'Bricolage Grotesque, Figtree, Noto Sans Tifinagh',
         'nacre': 'Gloock, Hanken Grotesk, DM Mono', 'tiziri': 'Instrument Serif, Geist, Amiri, IBM Plex Sans Arabic',
         'portfolio': 'Syne, Onest, JetBrains Mono, Bodoni Moda, Bricolage Grotesque, Gloock, Instrument Serif'}


def credits_md(pid):
    out = ['# Credits · Crédits · Créditos', '',
           'Photos keep their own licences and are not covered by the code licence (PolyForm Noncommercial).  ',
           'Les photos gardent leurs propres licences : elles ne relèvent pas de la licence du code.  ',
           'Las fotos conservan sus propias licencias y no están cubiertas por la licencia del código.', '']
    rows = COMMONS.get(pid, [])
    if rows:
        out += ['## Wikimedia Commons', '', '| File · Fichier · Archivo | Original | Author · Auteur · Autor | Licence | Changes · Modifications · Cambios |',
                '| --- | --- | --- | --- | --- |']
        out += [f'| `{f}` | [{title}]({enc_url(url)}) | {author} | [{lic}]({CC[lic]}) | {chg} |' for f, title, url, author, lic, chg in rows]
        out += ['', 'Files adapted from CC BY-SA originals are shared under the same CC BY-SA licence.  ',
                'Les fichiers adaptés d’originaux sous CC BY-SA sont diffusés sous la même licence CC BY-SA.  ',
                'Los archivos adaptados de originales con CC BY-SA se comparten con la misma licencia CC BY-SA.', '']
    for src, names, use in STOCK.get(pid, []):
        out += [f'## {src}', '', f'Photos: {names}.', '', f'Used for · Utilisées pour · Usadas para: {use}. Licence: [{src} License]({LIC_URL[src]}).', '']
    if pid == 'tiziri':
        out += ['| Piece · Pièce · Prenda | Photo | Author · Auteur · Autor |', '| --- | --- | --- |']
        out += [f'| `{piece}` | [unsplash.com/photos/{ph}](https://unsplash.com/photos/{ph}) | {who} |' for piece, ph, who in TIZIRI_DEMO]
        out += [''] + TIZIRI_NOTES
    out += ['## Fonts · Polices · Fuentes', '', f'{FONTS[pid]}: SIL Open Font License 1.1, see [`assets/fonts/OFL.txt`](assets/fonts/OFL.txt).', '',
            '## Demo content · Contenu de démonstration · Contenido de demostración', '']
    if pid == 'tiziri':
        out += ['The shop name, phone number and prices are fictional; in demo mode the WhatsApp button opens without a number.  ',
                'Le nom de la boutique, le numéro et les prix sont fictifs ; en mode démonstration, le bouton WhatsApp s’ouvre sans numéro.  ',
                'El nombre de la tienda, el teléfono y los precios son ficticios; en modo demostración, el botón de WhatsApp se abre sin número.']
    else:
        out += ['All names, addresses, phone numbers, prices and reviews are fictional. French phone numbers use ranges that ARCEP reserves for fiction.  ',
                'Les noms, adresses, numéros, prix et avis sont fictifs. Les numéros français appartiennent aux plages réservées à la fiction par l’ARCEP.  ',
                'Los nombres, direcciones, teléfonos, precios y opiniones son ficticios. Los números franceses pertenecen a los rangos que la ARCEP reserva para la ficción.']
    return '\n'.join(out)


def credits_portfolio():
    out = ['# Credits · Crédits · Créditos', '',
           'The screenshots and promo videos in this repository show the five templates, including their photos. Full credits: '
           + ', '.join(f'[{P[q]["name"]}]({GH}/{P[q]["repo"]}/blob/main/CREDITS.md)' for q in P) + '.  ',
           'Les captures et vidéos promo de ce dépôt montrent les cinq maquettes et leurs photos. Crédits complets : voir les liens ci-dessus.  ',
           'Las capturas y los vídeos promocionales de este repositorio muestran las cinco maquetas y sus fotos. Créditos completos: ver los enlaces anteriores.', '',
           '## Wikimedia Commons (CC BY-SA)', '', 'These works appear in the screenshots and videos · Ces œuvres apparaissent dans les captures et les vidéos · Estas obras aparecen en las capturas y los vídeos:', '']
    for q in ('billot', 'tafat', 'warda'):
        for f, title, url, author, lic, chg in COMMONS[q]:
            if lic.startswith('CC BY-SA'):
                out.append(f'- [{title}]({enc_url(url)}), {author}, [{lic}]({CC[lic]}) ({P[q]["name"]})')
    out += ['', '## Unsplash · Pexels', '', f'Photos under the [Unsplash License]({LIC_URL["Unsplash"]}) and the [Pexels License]({LIC_URL["Pexels"]}); photographers are listed in each template’s CREDITS.md.', '',
            '## Tiziri', '', 'Four garments were photographed in a boutique in Tigzirt; the worn views and videos were generated with Google Flow (the wooden mannequins are modelled in code). '
            'Quatre vêtements photographiés dans une boutique de Tigzirt ; vues portées et vidéos générées avec Google Flow (les mannequins en bois sont modélisés par le code). '
            'Cuatro prendas fotografiadas en una tienda de Tigzirt; vistas puestas y vídeos generados con Google Flow (los maniquíes de madera están modelados por código).', '',
            '## Music & sound · Musique et sons · Música y sonido', '', 'The music and sound effects of the promo videos are synthesised for these videos: no samples, no copyrighted audio.  ',
            'La musique et les bruitages des vidéos promo sont synthétisés pour ces vidéos : aucun échantillon, aucun son sous droits.  ',
            'La música y los efectos de sonido de los vídeos promocionales se han sintetizado para ellos: sin muestras ni audio con derechos.', '',
            '## Fonts · Polices · Fuentes', '', f'{FONTS["portfolio"]}: SIL Open Font License 1.1, see [`assets/fonts/OFL.txt`](assets/fonts/OFL.txt).']
    return '\n'.join(out)


SECURITY = """# Security policy · Politique de sécurité · Política de seguridad

## English

This repository is a static website: HTML, CSS, JavaScript, images, fonts{videos}. There is no server, no database, no account, no cookie, no analytics and no form that sends data anywhere. Pages are served by GitHub Pages with a strict Content Security Policy: scripts from the site only, no inline scripts, no third-party requests.

If you find a security issue, for example a way to inject content or script, please report it privately: open the **Security** tab of this repository and choose **Report a vulnerability**. Please do not open a public issue for it. Include the page, the steps to reproduce and the browser you used.

## Français

Ce dépôt est un site web statique : HTML, CSS, JavaScript, images, polices{videos_fr}. Il n’y a ni serveur, ni base de données, ni compte, ni cookie, ni mesure d’audience, ni formulaire qui envoie des données. Les pages sont servies par GitHub Pages avec une politique de sécurité du contenu stricte : scripts du site uniquement, aucun script en ligne, aucune requête vers un tiers.

Si vous trouvez une faille, par exemple un moyen d’injecter du contenu ou du script, signalez-la en privé : ouvrez l’onglet **Security** de ce dépôt et choisissez **Report a vulnerability**. N’ouvrez pas de ticket public à ce sujet. Indiquez la page, les étapes pour reproduire le problème et le navigateur utilisé.

## Español

Este repositorio es una web estática: HTML, CSS, JavaScript, imágenes, fuentes{videos_es}. No hay servidor, base de datos, cuentas, cookies, analítica ni formularios que envíen datos. GitHub Pages sirve las páginas con una política de seguridad de contenido estricta: solo scripts de la propia web, sin scripts en línea y sin peticiones a terceros.

Si encuentras una vulnerabilidad, por ejemplo una forma de inyectar contenido o scripts, comunícala de forma privada: abre la pestaña **Security** de este repositorio y elige **Report a vulnerability**. No abras una incidencia pública. Indica la página, los pasos para reproducirla y el navegador que usaste.
"""

GITIGNORE = '.DS_Store\nThumbs.db\ndesktop.ini\n'


def main():
    for pid, p in P.items():
        if p.get('own_docs'):
            continue
        d = os.path.join(ROOT, p['repo'])
        for lang in ('en', 'fr', 'es'):
            write(os.path.join(d, README[lang]), project_readme(pid, lang))
        write(os.path.join(d, 'LICENSE'), license_text())
        write(os.path.join(d, 'CREDITS.md'), credits_md(pid))
        v = p.get('videos')
        write(os.path.join(d, 'SECURITY.md'), SECURITY.format(videos=' and videos' if v else '', videos_fr=' et vidéos' if v else '', videos_es=' y vídeos' if v else ''))
        write(os.path.join(d, '.gitignore'), GITIGNORE)
        open(os.path.join(d, '.nojekyll'), 'w').close()
    d = os.path.join(ROOT, 'hoshuko.github.io')
    for lang in ('en', 'fr', 'es'):
        write(os.path.join(d, README[lang]), portfolio_readme(lang))
    write(os.path.join(d, 'LICENSE'), license_text())
    write(os.path.join(d, 'CREDITS.md'), credits_portfolio())
    write(os.path.join(d, 'SECURITY.md'), SECURITY.format(videos=' and videos', videos_fr=' et vidéos', videos_es=' y vídeos'))
    write(os.path.join(d, '.gitignore'), GITIGNORE)
    open(os.path.join(d, '.nojekyll'), 'w').close()
    write(os.path.join(ROOT, 'hoshuko', 'README.md'), profile_readme())
    print('documentation écrite')


if __name__ == '__main__':
    main()
