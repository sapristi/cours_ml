# TD02 Mono-couche Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construire le TP TD02 mono-couche multi-sorties (3 blobs + piège + bonus lettres 5x5) avec notebook corrigé, version étudiante filtrée et énoncé Obsidian.

**Architecture:** Une seule classe `CoucheMonoCouche` numpy (`W: KxD`, `b: K`, `argmax`), règle Rosenblatt multi-classes `r=0.1`, fonctions de génération blobs/lettres et plots fournies en cellules `# EXPORT`. Le notebook corrigé est la source de vérité, `scripts/filter_notebook.py` produit la version étudiante (`# SKIP` → `# TODO`).

**Tech Stack:** Python 3.12+, numpy, matplotlib, Jupyter notebook JSON, `scripts/filter_notebook.py` existant.

---

## File Structure

- Create: `td_02_mono_couche/mono_couche_corrige.ipynb` — notebook source de vérité (cellules corrigées avec `# EXPORT` / `# SKIP` pour parties à compléter).
- Create: `td_02_mono_couche/TD02-mono-couche.md` — énoncé Obsidian (frontmatter strict, liens wiki, callouts).
- Create: `/tmp/opencode/td02_check_blobs.py` — script de vérification blobs (jetable, pas commité).
- Create: `/tmp/opencode/td02_check_couche.py` — script de vérification classe (jetable).
- Create: `/tmp/opencode/td02_check_lettres.py` — script de vérification lettres (jetable).
- Modify: aucun fichier existant (miroir de `td_01_perceptron/perceptron.ipynb`, ne pas toucher TD01).
- Test: pas de pytest dans `pyproject.toml`, vérification par `python /tmp/opencode/*.py` + `jupyter nbconvert --execute`.

---

### Task 1: Génération blobs 2D séparables + piège

**Files:**
- Create: `td_02_mono_couche/mono_couche_corrige.ipynb` (partiel : cellules 1-4)
- Test: `/tmp/opencode/td02_check_blobs.py`

- [ ] **Step 1: Write the verification script**

```python
# /tmp/opencode/td02_check_blobs.py
import numpy as np
rng = np.random.default_rng(0)
centres = [(-2,-2),(2,-2),(0,2)]
def gen_blobs(n=25, sigma=0.6, seed=0):
    r = np.random.default_rng(seed)
    X, y = [], []
    for k,(cx,cy) in enumerate(centres):
        pts = r.normal(loc=(cx,cy), scale=sigma, size=(n,2))
        X.append(pts); y += [k]*n
    return np.vstack(X), np.array(y)
X, y = gen_blobs()
assert X.shape == (75,2), X.shape
assert set(y.tolist()) == {0,1,2}
# séparabilité grossière : distance inter-centres > 3*sigma
assert np.linalg.norm(np.array([-2,-2])-np.array([2,-2])) > 3*0.6
print("BLOBS OK", X.shape)
```

- [ ] **Step 2: Run verification to verify generation logic works**

Run: `python /tmp/opencode/td02_check_blobs.py`
Expected: `BLOBS OK (75, 2)`

- [ ] **Step 3: Create notebook with generation cells (corrigé source)**

Créer `td_02_mono_couche/mono_couche_corrige.ipynb` avec nbformat 4.5, kernelspec python3, 4 cellules :
Cellule 1 (markdown) : `# TD02 — Réseau mono-couche (3 perceptrons)`
Cellule 2 (code, source exacte) :
```python
# EXPORT
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
```
Cellule 3 (code, source exacte) :
```python
# EXPORT
def gen_blobs(n=25, sigma=0.6, seed=0):
    rng = np.random.default_rng(seed)
    centres = [(-2,-2),(2,-2),(0,2)]
    X_list, y_list = [], []
    for k,(cx,cy) in enumerate(centres):
        pts = rng.normal(loc=(cx,cy), scale=sigma, size=(n,2))
        X_list.append(pts)
        y_list += [k]*n
    return np.vstack(X_list), np.array(y_list)

def gen_piege(n_centre=15, seed=1):
    rng = np.random.default_rng(seed)
    Xc = rng.normal(loc=(0,0), scale=0.6, size=(n_centre,2))
    yc = np.zeros(n_centre, dtype=int)
    return Xc, yc
```
Cellule 4 (code, source exacte) :
```python
# EXPORT
X_train, y_train = gen_blobs()
X_piege, y_piege = gen_piege()
X_dur = np.vstack([X_train, X_piege])
y_dur = np.concatenate([y_train, y_piege])
```

- [ ] **Step 4: Run notebook cells to verify they execute**

Run: `python -c "import json; nb=json.load(open('td_02_mono_couche/mono_couche_corrige.ipynb')); print(len(nb['cells']))"`
Expected: `4`

- [ ] **Step 5: Commit**

```bash
git add td_02_mono_couche/mono_couche_corrige.ipynb
git commit -m "feat(td02): generation blobs + piege"
```

### Task 2: Classe CoucheMonoCouche (predict, learn_one, train)

**Files:**
- Modify: `td_02_mono_couche/mono_couche_corrige.ipynb` (ajout cellules 5-6)
- Test: `/tmp/opencode/td02_check_couche.py`

- [ ] **Step 1: Write the failing verification script**

```python
# /tmp/opencode/td02_check_couche.py
import numpy as np
from dataclasses import dataclass, field

@dataclass
class CoucheMonoCouche:
    W: np.ndarray
    b: np.ndarray
    # SKIP
    def predict(self, x: np.ndarray) -> int:
        h = self.W @ x + self.b
        return int(np.argmax(h))

    def learn_one(self, x: np.ndarray, t: int, r: float = 0.1):
        p = self.predict(x)
        if p != t:
            self.W[t] += r * x
            self.b[t] += r
            self.W[p] -= r * x
            self.b[p] -= r

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 50):
        for _ in range(epochs):
            err = 0
            for xi, ti in zip(X, y):
                p = self.predict(xi)
                if p != int(ti):
                    err += 1
                self.learn_one(xi, int(ti))
            if err == 0:
                break
        return self

c = CoucheMonoCouche(W=np.zeros((3,2)), b=np.zeros(3))
assert c.predict(np.array([1.0,0.0])) == 0
c.learn_one(np.array([2.0,-2.0]), 1)
assert c.predict(np.array([2.0,-2.0])) == 1, "learn_one doit corriger"
rng = np.random.default_rng(0)
X = np.vstack([rng.normal((-2,-2),0.6,size=(25,2)), rng.normal((2,-2),0.6,size=(25,2)), rng.normal((0,2),0.6,size=(25,2))])
y = np.array([0]*25+[1]*25+[2]*25)
c2 = CoucheMonoCouche(W=np.zeros((3,2)), b=np.zeros(3))
c2.train(X, y, epochs=50)
pred = np.array([c2.predict(xi) for xi in X])
acc = (pred==y).mean()
assert acc == 1.0, f"attendu 100%, obtenu {acc}"
print("COUCHE OK acc=1.0")
```

- [ ] **Step 2: Run test to verify reference logic passes (référence pour le notebook)**

Run: `python /tmp/opencode/td02_check_couche.py`
Expected: `COUCHE OK acc=1.0`

- [ ] **Step 3: Append cells to notebook (1 cellule EXPORT utilitaire + 1 cellule SKIP à compléter)**

Cellule 5 à ajouter (code, squelette étudiant — le `# SKIP` tronquera après filtrage) source exacte :
```python
# EXPORT
from dataclasses import dataclass
import numpy as np

@dataclass
class CoucheMonoCouche:
    W: np.ndarray
    b: np.ndarray
    # SKIP
    def predict(self, x: np.ndarray) -> int:
        h = self.W @ x + self.b
        return int(np.argmax(h))

    def learn_one(self, x: np.ndarray, t: int, r: float = 0.1):
        p = self.predict(x)
        if p != t:
            self.W[t] += r * x
            self.b[t] += r
            self.W[p] -= r * x
            self.b[p] -= r

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 50):
        for _ in range(epochs):
            err = 0
            for xi, ti in zip(X, y):
                if self.predict(xi) != int(ti):
                    err += 1
                self.learn_one(xi, int(ti))
            if err == 0:
                break
        return self
```
Cellule 6 à ajouter (code, non-EXPORT, démo non exportée vers étudiant ? Non : mettre `# EXPORT` pour garder l'entraînement visible) source exacte :
```python
# EXPORT
couche = CoucheMonoCouche(W=np.zeros((3,2)), b=np.zeros(3))
couche.train(X_train, y_train)
pred_train = np.array([couche.predict(x) for x in X_train])
print(f"accuracy train separable: {(pred_train==y_train).mean()*100:.1f}%")
couche_dur = CoucheMonoCouche(W=np.zeros((3,2)), b=np.zeros(3))
couche_dur.train(X_dur, y_dur)
pred_dur = np.array([couche_dur.predict(x) for x in X_dur])
print(f"accuracy avec piege: {(pred_dur==y_dur).mean()*100:.1f}%")
```

- [ ] **Step 4: Run notebook execution to verify accuracy prints**

Run: `jupyter nbconvert --to notebook --execute td_02_mono_couche/mono_couche_corrige.ipynb --output /tmp/opencode/exec1.ipynb --allow-errors 2>&1 | tail -5`
Expected: no `Error`, outputs contiennent `accuracy train separable: 100.0%`

- [ ] **Step 5: Commit**

```bash
git add td_02_mono_couche/mono_couche_corrige.ipynb
git commit -m "feat(td02): classe CoucheMonoCouche Rosenblatt multi-classes"
```

### Task 3: Plots frontières + fond argmax

**Files:**
- Modify: `td_02_mono_couche/mono_couche_corrige.ipynb` (ajout cellules 7-8)
- Test: exécution nbconvert + check png non vide via script

- [ ] **Step 1: Write the verification script**

```python
# /tmp/opencode/td02_check_plot.py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
# mini-fonction identique au notebook pour valider sans notebook
def plot_frontieres(X, y, W, b):
    xx, yy = np.meshgrid(np.linspace(-4,4,50), np.linspace(-4,4,50))
    grid = np.c_[xx.ravel(), yy.ravel()]
    Z = np.argmax(grid @ W.T + b, axis=1).reshape(xx.shape)
    fig, ax = plt.subplots()
    ax.contourf(xx, yy, Z, alpha=0.15)
    ax.scatter(X[:,0], X[:,1], c=y)
    fig.savefig("/tmp/opencode/td02_plot.png")
    print("PLOT OK")
plot_frontieres(np.zeros((3,2)), np.array([0,1,2]), np.zeros((3,2)), np.zeros(3))
```

- [ ] **Step 2: Run test to verify it passes**

Run: `python /tmp/opencode/td02_check_plot.py && ls -lh /tmp/opencode/td02_plot.png`
Expected: `PLOT OK` + fichier png > 1kB

- [ ] **Step 3: Append plot cells to notebook**

Cellule 7 source exacte :
```python
# EXPORT
def plot_frontieres(ax, X, y, couche, lim=(-4,4)):
    xx, yy = np.meshgrid(np.linspace(lim[0],lim[1],300), np.linspace(lim[0],lim[1],300))
    grid = np.c_[xx.ravel(), yy.ravel()]
    Z = np.argmax(grid @ couche.W.T + couche.b, axis=1).reshape(xx.shape)
    ax.contourf(xx, yy, Z, levels=[-0.5,0.5,1.5,2.5], colors=['tab:blue','tab:orange','tab:green'], alpha=0.12)
    for k,c in enumerate(['tab:blue','tab:orange','tab:green']):
        ax.scatter(X[y==k,0], X[y==k,1], c=c, edgecolors='k', s=25, label=f"classe {k}")
    # 3 droites w_k.x + b_k = 0 : on trace via contour de h_k - max autres = 0
    for k in range(3):
        H = (grid @ couche.W[k] + couche.b[k]).reshape(xx.shape)
        ax.contour(xx, yy, H, levels=[0], colors='k', linewidths=1.5, linestyles='--')
    ax.set_aspect('equal'); ax.legend(); ax.grid(True)
```
Cellule 8 source exacte :
```python
# EXPORT
fig, axes = plt.subplots(1, 2, figsize=(11,4.5))
plot_frontieres(axes[0], X_train, y_train, couche)
axes[0].set_title("Separable : 100%")
plot_frontieres(axes[1], X_dur, y_dur, couche_dur)
axes[1].set_title("Avec piege central : <100%")
plt.tight_layout()
plt.show()
```

- [ ] **Step 4: Run notebook execution**

Run: `jupyter nbconvert --to notebook --execute td_02_mono_couche/mono_couche_corrige.ipynb --output /tmp/opencode/exec2.ipynb --allow-errors 2>&1 | tail -3`
Expected: pas d'erreur `Error in ... plot_frontieres`

- [ ] **Step 5: Commit**

```bash
git add td_02_mono_couche/mono_couche_corrige.ipynb
git commit -m "feat(td02): plots frontieres argmax + 3 droites"
```

### Task 4: Bonus lettres 5x5 + visualisation W

**Files:**
- Modify: `td_02_mono_couche/mono_couche_corrige.ipynb` (ajout cellules 9-11)
- Test: `/tmp/opencode/td02_check_lettres.py`

- [ ] **Step 1: Write the failing test**

```python
# /tmp/opencode/td02_check_lettres.py
import numpy as np
A = np.array([0,1,0,1,0, 1,0,1,0,1, 1,1,1,1,1, 1,0,0,0,1, 1,0,0,0,1])
B = np.array([1,1,1,0,0, 1,0,0,1,0, 1,1,1,0,0, 1,0,0,1,0, 1,1,1,0,0])
C = np.array([0,1,1,1,0, 1,0,0,0,0, 1,0,0,0,0, 1,0,0,0,0, 0,1,1,1,0])
for name, v in [("A",A),("B",B),("C",C)]:
    assert v.shape == (25,), name
    assert set(np.unique(v).tolist()) <= {0,1}, name
# encodage +1/-1
def enc(v): return np.where(v==1, 1.0, -1.0)
assert enc(A)[0] == -1.0 and enc(A)[1] == 1.0
# bruit flip 2 px change exactement 2 positions
rng = np.random.default_rng(0)
def bruite(v, n_flip=2, rng=rng):
    w = enc(v).copy()
    idx = rng.choice(25, size=n_flip, replace=False)
    w[idx] *= -1
    return w
assert (bruite(A) != enc(A)).sum() == 2
print("LETTRES OK")
```

- [ ] **Step 2: Run test to verify it passes**

Run: `python /tmp/opencode/td02_check_lettres.py`
Expected: `LETTRES OK`

- [ ] **Step 3: Append lettres cells to notebook**

Cellule 9 source exacte :
```python
# EXPORT
TPL = {
 0: np.array([0,1,0,1,0, 1,0,1,0,1, 1,1,1,1,1, 1,0,0,0,1, 1,0,0,0,1]),
 1: np.array([1,1,1,0,0, 1,0,0,1,0, 1,1,1,0,0, 1,0,0,1,0, 1,1,1,0,0]),
 2: np.array([0,1,1,1,0, 1,0,0,0,0, 1,0,0,0,0, 1,0,0,0,0, 0,1,1,1,0]),
}
def enc(v): return np.where(v==1, 1.0, -1.0)
def gen_lettres(n_per=10, n_flip=2, seed=2):
    rng = np.random.default_rng(seed)
    X, y = [], []
    for k in range(3):
        base = enc(TPL[k])
        for _ in range(n_per):
            w = base.copy()
            idx = rng.choice(25, size=n_flip, replace=False)
            w[idx] *= -1
            X.append(w); y.append(k)
    return np.array(X), np.array(y)
```
Cellule 10 source exacte :
```python
# EXPORT
X_let, y_let = gen_lettres()
c_let = CoucheMonoCouche(W=np.zeros((3,25)), b=np.zeros(3))
c_let.train(X_let, y_let)
pred_let = np.array([c_let.predict(x) for x in X_let])
print(f"accuracy lettres train: {(pred_let==y_let).mean()*100:.1f}%")
X_let_test, y_let_test = gen_lettres(n_per=10, n_flip=5, seed=99)
pred_test = np.array([c_let.predict(x) for x in X_let_test])
print(f"accuracy lettres test flip5: {(pred_test==y_let_test).mean()*100:.1f}%")
```
Cellule 11 source exacte :
```python
# EXPORT
fig, axes = plt.subplots(1, 3, figsize=(8,3))
for k in range(3):
    axes[k].imshow(c_let.W[k].reshape(5,5), cmap="RdBu", vmin=-1, vmax=1)
    axes[k].set_title(f"W classe {k} ({'ABC'[k]})")
    axes[k].axis("off")
plt.tight_layout()
plt.show()
```

- [ ] **Step 4: Run notebook execution**

Run: `jupyter nbconvert --to notebook --execute td_02_mono_couche/mono_couche_corrige.ipynb --output /tmp/opencode/exec3.ipynb --allow-errors 2>&1 | tail -3`
Expected: sortie contient `accuracy lettres train`

- [ ] **Step 5: Commit**

```bash
git add td_02_mono_couche/mono_couche_corrige.ipynb
git commit -m "feat(td02): bonus lettres 5x5 + visu W"
```

### Task 5: Énoncé Obsidian TD02-mono-couche.md

**Files:**
- Create: `td_02_mono_couche/TD02-mono-couche.md`
- Test: vérification frontmatter + liens via grep

- [ ] **Step 1: Write the file**

```markdown
---
titre: TD02 - Reseau mono-couche multi-sorties
cours: "[[Entrypoint]]"
partie: TD02
statut: draft
Contexte: |-
  4e annee post-bac, 50 min + 15 min bonus.
  Suite de [[2 - Perceptron]].
  Prepare [[3- Données non linéairement séparables]].
---

> [!abstract] Objectif
> Passer d'un neurone a une couche de 3 perceptrons : `argmax(W.x+b)`, Rosenblatt multi-classes, visualisation des 3 droites, echec controle, bonus lettres 5x5.

# 1. Couche mono-couche

> [!example] Modele
> `h = W.x + b`, `W:(KxD)`, `y = argmax h`. Si `pred != target` : `W[target]+=r.x`, `W[pred]-=r.x`, idem biais. `r=0.1`.

### [!faq] Exercice 1 — Coder `CoucheMonoCouche`
Completer `predict`, `learn_one`, `train` dans `mono_couche.ipynb` (cellule classe). Verifier 100% sur `X_train`.

# 2. Blobs + piege

### [!faq] Exercice 2 — Succes separable
Entrainer, tracer `plot_frontieres`. Pourquoi regions convexes ?

> [!danger] Exercice 3 — Piege central
> Ajouter `X_dur`. Constater oscillation, <100%. Lien avec XOR du TD01 ? Pourquoi aucun `W` ne marche ?

# 3. Bonus lettres

### [!faq] Exercice 4 — A/B/C en 5x5
Reutiliser la meme classe en 25D. Visualiser `W` en 5x5. Tester flip 5 px. Lien surapprentissage [[3- Données non linéairement séparables]] §4 ?
```

- [ ] **Step 2: Run checks to verify conventions**

Run: `head -8 td_02_mono_couche/TD02-mono-couche.md && grep -c "\[\[" td_02_mono_couche/TD02-mono-couche.md && grep -c "\[!" td_02_mono_couche/TD02-mono-couche.md`
Expected: frontmatter avec `---`, `Contexte: |-`, `[[` >= 3, `[!` >= 3

- [ ] **Step 3: Commit**

```bash
git add td_02_mono_couche/TD02-mono-couche.md
git commit -m "docs(td02): enonce Obsidian mono-couche A+C"
```

### Task 6: Export étudiant + vérification finale

**Files:**
- Create: `td_02_mono_couche/mono_couche.ipynb` (généré, pas édité à la main)
- Test: exécution + filtre

- [ ] **Step 1: Generate student notebook with filter script**

Run: `python scripts/filter_notebook.py td_02_mono_couche/mono_couche_corrige.ipynb td_02_mono_couche/mono_couche.ipynb && python -c "import json; nb=json.load(open('td_02_mono_couche/mono_couche.ipynb')); print([c['cell_type'] for c in nb['cells']]); print('TODO' in open('td_02_mono_couche/mono_couche.ipynb').read())"`
Expected: liste de types, `True` (TODO présent là où `# SKIP` tronquait)

- [ ] **Step 2: Run full execution of corrigé to verify no errors**

Run: `jupyter nbconvert --to notebook --execute td_02_mono_couche/mono_couche_corrige.ipynb --output /tmp/opencode/final.ipynb 2>&1 | tail -3; python -c "import json; nb=json.load(open('/tmp/opencode/final.ipynb')); errs=[c for c in nb['cells'] if 'ename' in str(c.get('outputs',[]))]; print('errors:', len(errs))"`
Expected: `errors: 0`

- [ ] **Step 3: Commit**

```bash
git add td_02_mono_couche/mono_couche.ipynb
git commit -m "feat(td02): notebook etudiant filtre"
```

## Self-Review

1. Spec coverage : §2 architecture → Task 2, §3 blobs+piège → Tasks 1-3, §4 lettres → Task 4, §5 livrables → Tasks 5-6. OK.
2. Placeholder scan : aucun TBD/TODO dans le plan hors `# TODO` généré volontairement par `filter_notebook.py`. Codes complets fournis.
3. Type consistency : `W: (K,D)`, `b: (K,)`, `predict(x)->int`, `learn_one(x,t,r)`, `train(X,y,epochs)`, noms `gen_blobs`, `gen_piege`, `plot_frontieres`, `gen_lettres`, `enc`, `TPL` identiques dans tests et notebook.
