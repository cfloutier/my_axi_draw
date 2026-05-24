# Bug : pause/resume non fonctionnel pour les tracés points-only (dots/stippling)

**Date de découverte :** mai 2026
**Version axidrawinternal concernée :** 3.9.6
**Statut :** limitation fondamentale de la lib, aucun contournement stable trouvé
**Ticket PR potentiel :** Evil Mad Scientist — axidraw (https://github.com/evil-mad/axidraw)

---

## Symptôme

Lors d'un tracé SVG composé exclusivement de points (chaque chemin SVG est un point isolé —
pen descend, puis remonte immédiatement sans déplacement horizontal), la pause fonctionne
correctement en apparence (le traceur s'arrête), mais **la reprise repart systématiquement
depuis le début du fichier** au lieu de reprendre là où le traceur s'est arrêté.

En pratique, pour un tracé de stippling de 2h, une pause à mi-chemin signifie recommencer
les ~60 premières minutes déjà tracées.

---

## Analyse de la cause racine

### 1. Métrique de position : `down_travel_inch`

`axidrawinternal` encode la position de reprise dans un champ appelé `pause_dist`.
Ce champ est sauvegardé dans le SVG lors d'une pause.

**Fichier :** `axidrawinternal/axidraw.py`, ligne ~948
```python
self.plot_status.resume.new.pause_dist = self.plot_status.stats.down_travel_inch
self.plot_status.resume.new.pause_ref  = self.plot_status.stats.down_travel_inch
```

`down_travel_inch` est la **distance totale parcourue stylo baissé** depuis le début du tracé.
Il est incrémenté dans `plot_status.py`, méthode `add_dist()` :

**Fichier :** `axidrawinternal/plot_status.py`, lignes ~295-300
```python
def add_dist(self, pen_up, distance_inch):
    if pen_up:
        self.up_travel_inch += distance_inch
    else:
        self.down_travel_inch += distance_inch  # ← seule métrique utilisée pour pause_dist
```

### 2. Pourquoi les dots ont `down_travel_inch = 0`

Pour un point SVG (ex. `<circle r="0.1"/>`), après traitement par le digest :

- Le digest crée un `PathItem` avec un seul subpath composé de **deux sommets identiques**
  (ou un seul sommet), représentant le mouvement pen-down : descendre et remonter sur place.
- La méthode `PathItem.length()` calcule la distance euclidienne entre sommets consécutifs :

**Fichier :** `axidrawinternal/path_objects.py`, lignes ~148-165
```python
def length(self):
    subpath = self.subpaths[0]
    total_length = 0
    index = 0
    while index < (vertex_count_less_1):
        d_x = subpath[index+1][0] - subpath[index][0]
        d_y = subpath[index+1][1] - subpath[index][1]
        total_length += sqrt(d_x * d_x + d_y * d_y)  # ← 0 si les deux sommets sont identiques
        index += 1
    return total_length
```

Un point = déplacement nul = `length() == 0.0`. La distance pen-down tracée reste donc `0`
quelle que soit la durée écoulée. `down_travel_inch` ne s'incrémente jamais.

### 3. `crop(0)` est un no-op

Lors de la reprise, la fonction `crop()` est appelée avec `pause_dist = 0.0` :

**Fichier :** `axidrawinternal/axidraw.py`, ligne ~376
```python
if self.options.mode == "res_plot":
    self.digest.crop(self.plot_status.resume.old.pause_dist)  # crop(0.0)
```

**Fichier :** `axidrawinternal/path_objects.py`, lignes ~656-657
```python
def crop(self, distance):
    if distance <= 0:
        return  # ← no-op immédiat, aucun path n'est supprimé
    ...
```

**Résultat :** le digest n'est pas du tout réduit, et la reprise repart du premier path.

---

## Chaîne complète du bug

```
tracé dots  →  PathItem.length() == 0  →  add_dist(pen_up=False, distance=0)
           →  down_travel_inch reste 0  →  pause_dist = 0
           →  crop(0) = no-op           →  reprise depuis le début
```

---

## Piste pour un correctif (PR potentiel)

### Option A — Utiliser `pen_lifts` comme métrique alternative

Chaque point correspond à un pen-lift. La lib comptabilise déjà `pen.status.lifts`
(ou équivalent). On pourrait sauvegarder **le nombre de pen-lifts complétés** dans
`pause_dist` en complément de `down_travel_inch`, et utiliser cette valeur comme
fallback dans `crop()` quand `down_travel_inch == 0`.

Problème : `crop()` travaille sur des distances, pas des indices. Il faudrait étendre
son interface pour accepter optionnellement un index de path.

### Option B — Modifier `crop()` pour supporter un index de path

Ajouter un paramètre `path_index` à `crop()` :
```python
def crop(self, distance, path_index=None):
    if distance <= 0 and path_index is None:
        return
    ...
```

Et enregistrer dans `pause_dist` une métrique composite (distance + index) ou ajouter
un champ `pause_path_index` dans `ResumeData` (`plot_status.py`).

### Option C — Compter les dots via `up_travel_inch`

Le pen-up après chaque dot génère bien un déplacement (`up_travel_inch` > 0 car le
traceur se déplace vers le dot suivant stylo levé). On pourrait utiliser `up_travel_inch`
comme métrique de position **quand `down_travel_inch == 0`**.

Problème : `up_travel_inch` inclut également les déplacements entre lignes dans les
tracés normaux ; cette heuristique n'est pas générale.

### Option D (recommandée) — `pause_path_count` : index de chemins complétés

Ajouter un compteur `pause_path_count` (entier, nombre de PathItems complètement tracés)
aux côtés de `pause_dist` dans `ResumeData`. Lors de la reprise, si `pause_dist == 0`
et `pause_path_count > 0`, utiliser `pause_path_count` pour slicer directement
`layer.paths` dans `crop()`.

Fichiers à modifier :
1. `plot_status.py` — ajouter `pause_path_count` dans `ResumeData.__init__()`, `reset()`, `clean()`
2. `axidraw_control.py` ou `axidraw.py` — incrémenter `pause_path_count` à chaque path complété
3. `path_objects.py` — modifier `crop()` pour utiliser `pause_path_count` quand `distance == 0`
4. `plot_status.py` — lire/écrire `pause_path_count` dans le SVG (méthodes `read_from_svg` / `write_to_svg`)

---

## Fichiers concernés dans axidrawinternal 3.9.6

| Fichier | Lignes clés | Rôle |
|---|---|---|
| `axidraw.py` | 376, 390, 948-949 | Sauvegarde et utilisation de `pause_dist` |
| `path_objects.py` | 148-165, 640-698 | `PathItem.length()` et `DocDigest.crop()` |
| `plot_status.py` | 270-300 | `PlotStats.add_dist()` — incrémentation de `down_travel_inch` |
| `plot_status.py` | 44-63 | `ResumeData` — stockage de `pause_dist` |

---

## Contexte du projet

Ce bug a été découvert lors du développement de `my_axi_draw`, une interface personnalisée
pour l'AxiDraw. Les tracés de stippling (des centaines à milliers de points) peuvent durer
plusieurs heures ; l'impossibilité de faire une pause est une limitation opérationnelle
significative.
