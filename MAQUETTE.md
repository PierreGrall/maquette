# Construire une maquette (sous-agent)

Tu reçois UN prospect (nom, site, ville, métier, email publié, et parfois des notes). Tu le qualifies, puis tu construis sa maquette dans `/home/claude/maquette/<slug>/index.html`. Lis aussi `KIT.md` (court). Ne lis aucun autre fichier en entier. Tu ne commits pas, tu ne crées aucun email.

## 1. Qualifier (arrête-toi dès qu'un critère élimine)
WebFetch : accueil, services/réalisations, contact, mentions légales (4 pages maximum). `places_search` s'il est disponible : note, nombre et contenu des avis, réponses du gérant.
Note sur 100 : panier moyen 30, faiblesse mobile 25, site daté/incohérent/banque d'images 15, aucune conversion 15, bonne réputation 10, email publié 5. Il faut ≥ 60.
Éliminé si : franchise ou réseau, site récent et soigné, WebFetch refusé, aucune photo exploitable. Jamais d'adresse devinée.

## 2. Comprendre (notes courtes, pas de rapport)
(a) L'entreprise : offre réelle, gamme, preuve la plus forte, différence locale, ton, zone, fiche Google (avis sans réponse ? peu d'avis ?). (b) L'acheteur final : qui, budget, moment de décision, désirs, peurs, questions, déclencheur, langue. (c) Conséquences : accroche, ordre des sections, feature phare, questions du configurateur, FAQ, langues, univers visuel, option la plus utile pour lui. Adapte tout à la niche ET à la région (paysage, lumière, vocabulaire, saison, clientèle étrangère éventuelle).

## 3. Maquette (HTML autonome, SES textes réécrits, SES photos en URL absolues, ses coordonnées)
- IMAGES : vraie URL (src réel ou plus grande taille du srcset, jamais un data-src, une miniature ou un pixel transparent), https absolu, `onerror="this.style.visibility='hidden'"`, couleur de fond de repli sur le conteneur (aussi pour les fonds CSS). La page doit rester belle si toutes les photos échouent. Préfère les photos de réalisations.
- ACCROCHE : preuve + désir, 2–3 lignes courtes, chacune sur une ligne (nowrap, tiret insécable), puis une phrase ce qu'il fait / pourquoi lui. Exemple validé : « 2 000 bassins / de Menton à Saint‑Tropez. / Le prochain est chez vous. »
- EN-TÊTE : longue bulle flottante en verre dépoli (999px, blur, bord translucide), jamais de bande blanche ; symbole SVG currentColor + nom complet de l'entreprise ; jamais son logo raster. Bandeau maquette au-dessus (court sur mobile), sans masquer l'en-tête.
- ANIMATION (comme logintec) : ouverture WebGL plein écran écrite à la main, propre à son univers (eau, neige, lumière, matière), réactive au pointeur ; jamais de décor 3D en géométries simples (low-poly) ; titre révélé ligne par ligne ; Lenis ; une seule boucle rAF ; ≥ 3 scènes sticky au défilement (photo phare en clip-path + compteurs ; scène métier SVG construite étape par étape ; galerie horizontale épinglée en parallaxe) ; transform/opacity/clip-path uniquement ; reduced-motion respecté.
- FEATURES (2–3, les plus fortes pour CET acheteur) : piscinistes → bassin 3D three.js qu'on tourne au doigt, jour/nuit avec LED, frise des mois de baignade, compte à rebours avant l'été ; paysagistes → jardin qui pousse, saisons, configurateur adapté au climat local avec eau économisée ; hôtels, chalets, gîtes → réservation directe + prix ici vs plateformes (à valider), météo, neige ou mer en direct (open-meteo, repli silencieux), visite de chambre en profondeur ; stations de ski → enneigement et pistes en direct, comparateur de séjours, réservation de matériel ou de cours en 3 étapes ; restaurants/plages → plan cliquable (transat ou table), carte interactive, bon cadeau en aperçu ; cuisinistes/menuisiers → matières qui changent en direct, avant/après ; immobilier → estimation en 4 questions avec fourchette animée, alerte off-market ; domaines → composeur de coffret, quiz accords, abonnement ; bateaux → carte animée de la côte avec itinéraire et prix. Toujours : aperçu qui réagit à chaque choix, prix animé, pastilles d'étapes, passage automatique, étape calendrier, récapitulatif, envoi WhatsApp prérempli vers son mobile publié (sinon mailto vers son email publié) + lien de projet partageable. Pied de page : petit champ « Recevoir nos réalisations et conseils chaque mois » (démonstration, sans envoi réel, confirmation locale).
- PREUVE : avis mis en scène (grande note, bande défilante, extraits reformulés de ses vrais avis Google + mention « Extraits reformulés de vos avis Google pour la maquette… ») ; sans avis, ses vraies preuves (années, réalisations, labels) sans rien inventer ; FAQ accordéon 7–9 vraies objections dont une urgence réelle ; barre mobile d'action sans doublon, avec un lien `tel:` vers son numéro publié ; langues de sa clientèle étrangère.
- STYLE propre (4–6 couleurs, 1–2 polices Google Fonts + pile système en repli). Interdits : crème + terracotta, noir + vert acide, cartes arrondies identiques avec ombres, dégradés décoratifs, emojis, capitales, flèches dans les boutons, grilles de 3 icônes, banque d'images, images générées, fondus identiques, « Bienvenue », « passionnés », faux avis, faux chiffres (inventé = « à valider avec vous »). `<meta name="robots" content="noindex">`.
- SECTION `id="grall-studio"` : copiée de logintec par le shell (voir KIT.md). Change seulement : l'introduction (nom du gérant, son site), les 5 lignes Aujourd'hui / Avec la refonte (défauts réels ; si sa fiche Google a des avis sans réponse ou peu d'avis, une ligne le dit), la liste Immersion, l'ordre des options (la plus utile pour lui en premier), les exemples dans les textes d'options adaptés à son métier, le sujet du mailto (`Site%20[Entreprise]`), les couleurs. Prix, garantie et paragraphe agence inchangés. Aucune mention de « premiers clients », de lancement ou de réduction. Espace insécable avant « : ; ? ! ».
- TECHNIQUE : librairies par `../lib/` (KIT.md), jamais collées. Dans un ShaderMaterial avec fog, la variable de vue s'appelle `mvPosition` ; n'écris jamais « x-${nombre négatif} » dans un shader. Slug : nom court, minuscules, sans accent, absent du dépôt.

## 4. Contrôle qualité
`python3 tools/qa.py <slug> --feature "#…" --click "…"` puis Read de la planche. Zéro erreur JS ou de shader. Juge en directeur artistique exigeant ET en acheteur final. Deux tours de correction au maximum. Sous le niveau logintec : supprime le dossier et réponds KO.

## 5. Réponse finale (rien d'autre, 8 lignes maximum)
```
OK|KO <slug> — <raison si KO>
entreprise: … | gérant: Monsieur/Madame X ou ? | email: … | tel: …
metier-ville: … | score: …
compliment: <précis et sincère>
defauts: <défaut 1> ; <défaut 2>
feature: <feature phare en quelques mots>
benefice: <bénéfice concret de la feature pour ses clients, une phrase>
google: <conseil précis tiré de sa fiche, pour l'email 3>
```
