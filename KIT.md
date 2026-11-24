# Kit de production des maquettes

À lire à la place de tout autre fichier. Objectif : niveau logintec, avec le moins d'écriture et de lectures possible.

## Librairies (ne jamais les coller dans une page)
```html
<script src="../lib/three.min.js"></script>   <!-- three r159, seulement si 3D -->
<script src="../lib/lenis.min.js"></script>   <!-- Lenis 1.1.13 -->
```

## Référence
`logintec/index.html` (≈ 68 Ko, librairies retirées). Ne la lis pas en entier : `grep -n` pour trouver un bloc, puis `sed -n 'a,bp'` sur ce bloc seulement.

## Blocs communs : copie-les par le shell, ne les réécris pas
Avec un petit script python (lecture de logintec, découpe, écriture dans `<slug>/index.html`) :
- section `<aside id="grall-studio">…</aside>` et ses styles `.studio .audit .offers .offer .addons .cta-row` ;
- FAQ (`.faq`), barre mobile (`.mbar`), bandeau maquette (`.proof`), en-tête bulle (`header.site`, règles vers la ligne 205).
Puis modifie seulement : couleurs (variables CSS), nom, les 5 lignes Aujourd'hui / Avec la refonte, la phrase d'introduction, la liste « Immersion », l'ordre des options, le sujet du mailto. Prix et textes d'offres : inchangés.

## Écriture
- Écris la page en UNE fois (Write), puis corrige par petites modifications (Edit). Ne réécris jamais le fichier entier.
- N'affiche jamais un fichier HTML ni une page web complète dans la sortie : `grep`, `head -c`, ou extraits ciblés.

## Contrôle qualité : une seule commande
```
python3 tools/qa.py <slug> --feature "#id-de-la-feature" [--click "sélecteur" ...]
```
Sortie : erreurs de console + une planche JPEG unique `/tmp/qa-<slug>.jpg` (1440 px, 390 px, sans images). Ouvre seulement cette planche avec Read. Maximum 2 tours de correction.
