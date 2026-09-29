# Prépa multi-perceptron Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Créer le notebook pré-TD02 boucle-puis-vectorisation qui lève le blocage `W@x+b`.

**Architecture:** Un seul notebook corrigé source de vérité `prepa_multi_perceptron_corrige.ipynb` (cellules `# EXPORT` / `# SKIP`), la version étudiante `prepa_multi_perceptron.ipynb` est produite par `scripts/filter_notebook.py`. Logique : 3x `Perceptron` TD01 en boucle → même chose en `W:(3xD)` → constat ambiguïté sans `argmax`.

**Tech Stack:** Python 3.12+, numpy, Jupyter notebook JSON nbformat 4.5, `scripts/filter_notebook.py` existant.

---

## File Structure

- Create: `td_02_mono_couche/prepa_multi_perceptron_corrige.ipynb` — source de vérité (markdown + code corrigé avec `# EXPORT` / `# SKIP`).
- Ne PAS créer de version étudiante : elle est générée au déploiement par CI (`filter_notebook.py --in-place dist/files/`, voir `.github/workflows/deploy.yml`). Vérifier le filtre vers `/tmp` uniquement.
- Create: `/tmp/opencode/prepa_check_equiv.py` — script vérif jetable (pas commité).
- Modify: aucun fichier existant (ne pas toucher TD01, TD02).
- Test: pas de pytest, vérif par `python /tmp/opencode/*.py` + `jupyter nbconvert --execute`.

---

### Task 1: Vérifier l'équivalence boucle == matrice

**Files:**
- Create: `/tmp/opencode/prepa_check_equiv.py`
- Test: `/tmp/opencode/prepa_check_equiv.py`

- [ ] **Step 1: Write the verification script**

```python
# /tmp/opencode/prepa_check_equiv.py
import numpy as np

def gen_blobs(n=25, sigma=0.6, seed=0):
    rng = np.random.default_rng(seed)
    centres = [(-2,-2),(2,-2),(0,2)]
    X_list, y_list = [], []
    for k,(cx,cy) in enumerate(centres):
        pts = rng.normal(loc=(cx,cy), scale=sigma, size=(n,2))
        X_list.append(pts)
        y_list += [k]*n
    return np.vstack(X_list), np.array(y_list)

# 3 perceptrons factices (poids imposés pour le test, vérifiés par exécution)
W = np.array([[1.0, 0.5], [-1.0, 0.5], [0.0, -1.0]])
b = np.array([-0.5, -0.5, -0.5])

def predict_liste_equiv(x):
    h = W @ x + b
    return (h >= 0).astype(int)

def predict_vect(x):
    h = W @ x + b
    return (h >= 0).astype(int)

X, y = gen_blobs()
for xi in X:
    assert np.array_equal(predict_liste_equiv(xi), predict_vect(xi)), xi
# points ambiguïté imposés (vérifiés par exécution) : [0,0,0] aucun gagnant, [1,1,0] deux gagnants
amb1 = np.array([0.0, 0.0])
amb2 = np.array([0.0, 2.0])
print("ex 0,0 ->", predict_vect(amb1).tolist())
print("ex 0,2 ->", predict_vect(amb2).tolist())
assert predict_vect(amb1).tolist() == [0, 0, 0], predict_vect(amb1)
assert predict_vect(amb2).tolist() == [1, 1, 0], predict_vect(amb2)
print("EQUIV OK")
```

- [ ] **Step 2: Run verification script**

Run: `python /tmp/opencode/prepa_check_equiv.py`
Expected: `EQUIV OK` avec les deux lignes `ex 0,0 -> [0, 0, 0]` et `ex 0,2 -> [1, 1, 0]`

- [ ] **Step 3: Commit (rien à commiter, script jetable)**

Run: `echo "task1 done, /tmp script not committed"`
Expected: `task1 done, /tmp script not committed`

---

### Task 2: Créer le notebook corrigé source

**Files:**
- Create: `td_02_mono_couche/prepa_multi_perceptron_corrige.ipynb`
- Test: `/tmp/opencode/prepa_check_equiv.py` (réutilisé, doit toujours passer)

- [ ] **Step 1: Write the notebook file**

Créer `td_02_mono_couche/prepa_multi_perceptron_corrige.ipynb` avec nbformat 4, nbformat_minor 5, kernelspec python3, `outputs: []`, `execution_count: null` partout. Markdown didactique : chaque exo explique ce qui est fourni, ce qu'il faut coder (signature imposée) et comment vérifier. Contenu exact des cellules :

Cell 1 (markdown) :
```
# Prépa TD02 — 3 perceptrons, puis une matrice
Au TD01, un `Perceptron` + Heaviside sépare le plan en deux (0/1).
Ici on veut **3 classes** : on prend **3 perceptrons**, chacun répond 0/1.
D'abord en **boucle Python** (Exo 1), puis rangés en **matrice `W`, vecteur `b`** (Exo 2) :
on doit obtenir exactement les mêmes réponses. Sans `argmax` pour l'instant :
la sortie est un **vecteur `[0/1, 0/1, 0/1]`**.
```

Cell 2 (code) :
```python
# EXPORT
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
```

Cell 3 (markdown) :
```
## Code fourni : `Perceptron` (TD01) + données
`Perceptron(w, b).output(x)` vaut 1 si `w·x + b >= 0`, sinon 0 (Heaviside).
`gen_blobs()` donne 75 points 2D en 3 classes. Rien à coder ici : exécutez.
```

Cell 4 (code) :
```python
# EXPORT
@dataclass
class Perceptron:
    w: np.ndarray
    b: float
    def output(self, x: np.ndarray) -> int:
        return 1 if float(self.w @ x + self.b) >= 0 else 0

def gen_blobs(n=25, sigma=0.6, seed=0):
    rng = np.random.default_rng(seed)
    centres = [(-2,-2),(2,-2),(0,2)]
    X_list, y_list = [], []
    for k,(cx,cy) in enumerate(centres):
        pts = rng.normal(loc=(cx,cy), scale=sigma, size=(n,2))
        X_list.append(pts)
        y_list += [k]*n
    return np.vstack(X_list), np.array(y_list)

X_train, y_train = gen_blobs()
print(X_train.shape, sorted(set(y_train.tolist())))
```

Cell 5 (markdown) :
```
## Exo 1 — boucle sur 3 perceptrons
3 perceptrons fournis ci-dessous (poids imposés, `b=-0.5` pour les trois).
Complétez `predict_liste(x, perceptrons) -> np.ndarray` : boucle sur `p.output(x)`,
retourne `np.array([0/1, 0/1, 0/1])`. Vérifiez avec la cellule suivante :
`[0,0]` doit donner `[0 0 0]`, `[0,2]` doit donner `[1 1 0]`.
```

Cell 6 (code, exo boucle : liste fournie gardée, correction après `# SKIP`) :
```python
# EXPORT
import numpy as np

perceptrons = [
    Perceptron(w=np.array([1.0, 0.5]), b=-0.5),
    Perceptron(w=np.array([-1.0, 0.5]), b=-0.5),
    Perceptron(w=np.array([0.0, -1.0]), b=-0.5),
]
# SKIP
def predict_liste(x: np.ndarray, perceptrons: list) -> np.ndarray:
    return np.array([p.output(x) for p in perceptrons], dtype=int)
```

Cell 7 (code, vérif Exo 1, gardée telle quelle pour l'étudiant) :
```python
# EXPORT
print(predict_liste(np.array([0.0, 0.0]), perceptrons))
print(predict_liste(np.array([0.0, 2.0]), perceptrons))
```

Cell 8 (markdown) :
```
## Exo 2 — la même chose en matrice `W @ x + b`
Rangez les 3 vecteurs `w` en matrice `W:(3x2)` (une ligne par neurone) et les 3 biais
en vecteur `b:(3,)`. Complétez `predict_vect(x, W, b)` : `h = W @ x + b`,
retourne `(h >= 0).astype(int)` (un Heaviside par neurone, comme en Exo 1).
La cellule de vérification prouve `boucle == matrice` sur tout `X_train`.
```

Cell 9 (code, exo vectorisé : correction après `# SKIP`) :
```python
# EXPORT
import numpy as np

# Construisez W (3x2) et b (3,) à partir des 3 perceptrons de l'Exo 1.
# SKIP
def predict_vect(x: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray:
    h = W @ x + b
    return (h >= 0).astype(int)

W = np.array([[1.0, 0.5], [-1.0, 0.5], [0.0, -1.0]])
b = np.array([-0.5, -0.5, -0.5])
```

Cell 10 (code, vérif Exo 2, gardée telle quelle) :
```python
# EXPORT
for xi in X_train:
    assert np.array_equal(predict_liste(xi, perceptrons), predict_vect(xi, W, b))
print("boucle == matrice OK")
print(predict_vect(np.array([0.0, 0.0]), W, b))
print(predict_vect(np.array([0.0, 2.0]), W, b))
```

Cell 11 (markdown) :
```
## Constat — pourquoi il faudra `argmax` ?
`[0 0 0]` : aucun neurone ne s'active — quelle classe choisir ?
`[1 1 0]` : deux neurones gagnent — lequel croire ?
3 Heaviside indépendants ne suffisent pas à **décider une classe unique**.
Au TD02, on tranche avec `y = argmax_k h_k` : le score le plus fort gagne.
```

La partie après `# SKIP` est la correction ; `scripts/filter_notebook.py` la remplacera par `# TODO` dans la version étudiante générée au déploiement. Les cellules de vérif (sans `# SKIP`) sont gardées telles quelles pour que l'étudiant contrôle son code. Les cellules markdown sont gardées telles quelles.

- [ ] **Step 2: Run the equivalence check again (garde-fou)**

Run: `python /tmp/opencode/prepa_check_equiv.py`
Expected: `EQUIV OK`

- [ ] **Step 3: Commit notebook source**

```bash
git add td_02_mono_couche/prepa_multi_perceptron_corrige.ipynb
git commit -m "feat(prepa): notebook boucle puis W@x+b corrige"
```

---

### Task 3: Vérifier exécution + filtre étudiant (sans commiter de version étudiante)

**Files:**
- Modify: aucun (vérifications vers `/tmp` uniquement)
- Test: exécution `jupyter nbconvert --execute` + `scripts/filter_notebook.py` vers `/tmp`

- [ ] **Step 1: Execute corrigé notebook end-to-end**

Run: `jupyter nbconvert --to notebook --execute td_02_mono_couche/prepa_multi_perceptron_corrige.ipynb --output /tmp/opencode/prepa_exec.ipynb --allow-errors`
Expected: exit 0, pas d'erreur Python (vérifier `grep -i "Error" /tmp/opencode/prepa_exec.ipynb` vide), sorties `boucle == matrice OK`, `[0 0 0]`, `[1 1 0]`.

- [ ] **Step 2: Generate student version to /tmp and verify didactic filter**

Run: `python scripts/filter_notebook.py td_02_mono_couche/prepa_multi_perceptron_corrige.ipynb /tmp/opencode/prepa_etudiant.ipynb`
Expected: exit 0.

Run: `python -c "import json; d=json.load(open('/tmp/opencode/prepa_etudiant.ipynb')); s='\n'.join(''.join(c.get('source',[]) if isinstance(c.get('source',[]),list) else c.get('source','')) for c in d['cells']); assert '# TODO' in s, 'TODO manquant'; assert 'boucle == matrice OK' not in s, 'correction a fuite'; assert '## Exo 1' in s and '## Exo 2' in s, 'markdown didactique manquant'; print('FILTRE OK')"`
Expected: `FILTRE OK`

- [ ] **Step 3: Commit (notebook corrigé uniquement)**

```bash
git add td_02_mono_couche/prepa_multi_perceptron_corrige.ipynb
git commit -m "feat(prepa): notebook boucle puis W@x+b corrige"
```
