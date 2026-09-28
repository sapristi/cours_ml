# Notebook Export Filter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Créer `scripts/filter_notebook.py` qui génère le notebook étudiant depuis le corrigé (EXPORT/SKIP) et filtre au build CI, inspiré de `cours_algo/other/post_treatment.py`.

**Architecture:** Un script stdlib unique avec fonctions pures `source_text/filter/truncate/clear` + CLI double-mode (fichier→fichier en local, `--in-place` sur dossier en CI), réutilisant `insert_clear_button` de cours_algo avec garde anti-doublon.

**Tech Stack:** Python 3.12 (stdlib: `json`, `pathlib`, `argparse`, `sys`), Jupyter nbformat JSON, `uv run`, GitHub Actions existant.

---

## File structure

- Create: `scripts/filter_notebook.py` — tout le filtre (source_text, truncate_skip, filter_cells, clear, bouton, CLI).
- Modify: `.github/workflows/deploy.yml` — ajout étape post-treatment après `jupyter lite build`.
- Test (jetable, pas commité): `/tmp/test_filter_notebook.py` — asserts manuels stdlib.
- Test (jetable): `/tmp/fixture.ipynb` — notebook jouet couvrant tous les cas.
- Source de vérité (lecture seule): `td_01_perceptron/corrige.ipynb`.
- Destination générée: `td_01_perceptron/perceptron.ipynb`.

---

### Task 1: Créer le module de filtre + truncate + clear

**Files:**
- Create: `scripts/filter_notebook.py`

- [ ] **Step 1: Écrire le script de test manuel (failing)**

Créer `/tmp/test_filter_notebook.py` avec :

```python
import sys
sys.path.insert(0, "scripts")
from filter_notebook import source_text, truncate_skip, cell_kept

# source_text gère list et str
assert source_text({"source": ["a\n", "b"]}) == "a\nb"
assert source_text({"source": "a\nb"}) == "a\nb"
# truncate_skip coupe au premier SKIP et ajoute TODO
assert truncate_skip(["x = 1\n", "y = 2  #SKIP\n", "z = 3\n"]) == ["x = 1\n", "# TODO\n"]
assert truncate_skip(["#SKIP tout\n", "z = 3\n"]) == ["# TODO\n"]
assert truncate_skip(["x = 1\n"]) == ["x = 1\n"]
# cell_kept : code sans EXPORT = False, avec = True, markdown = True
assert cell_kept({"cell_type": "code", "source": ["x=1\n"]}) is False
assert cell_kept({"cell_type": "code", "source": ["x=1  # EXPORT\n"]}) is True
assert cell_kept({"cell_type": "markdown", "source": ["# titre"]}) is True
print("OK task1")
```

- [ ] **Step 2: Lancer le test, constater l'échec**

Run: `uv run python /tmp/test_filter_notebook.py`
Expected: FAIL avec `ModuleNotFoundError: No module named 'filter_notebook'` (le fichier n'existe pas encore).

- [ ] **Step 3: Implémenter le minimal (fonctions pures + squelette)**

Créer `scripts/filter_notebook.py` avec le contenu complet suivant :

```python
"""Filtre EXPORT/SKIP pour notebooks étudiants.

Local:  python scripts/filter_notebook.py corrige.ipynb perceptron.ipynb
CI:     python scripts/filter_notebook.py --in-place dist/files/
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EXPORT_MARKER = "EXPORT"
SKIP_MARKER = "SKIP"
TODO_LINE = "# TODO\n"


def source_text(cell: dict) -> str:
    src = cell.get("source", "")
    if isinstance(src, list):
        return "".join(src)
    return src


def as_lines(cell: dict) -> list[str]:
    src = cell.get("source", "")
    if isinstance(src, list):
        return list(src)
    return src.splitlines(keepends=True)


def cell_kept(cell: dict) -> bool:
    if cell.get("cell_type") != "code":
        return True
    return EXPORT_MARKER in source_text(cell)


def truncate_skip(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        if SKIP_MARKER in line:
            out.append(TODO_LINE)
            break
        out.append(line)
    else:
        return out
    return out


def clear_cell(cell: dict) -> None:
    cell["outputs"] = []
    if "execution_count" in cell:
        cell["execution_count"] = None


def filter_cells(cells: list[dict]) -> list[dict]:
    kept: list[dict] = []
    for cell in cells:
        if not cell_kept(cell):
            continue
        if cell.get("cell_type") == "code":
            cell["source"] = truncate_skip(as_lines(cell))
            clear_cell(cell)
        kept.append(cell)
    return kept
```

- [ ] **Step 4: Relancer le test, constater le succès**

Run: `uv run python /tmp/test_filter_notebook.py`
Expected: PASS, affiche `OK task1`.

- [ ] **Step 5: Commit**

```bash
git add scripts/filter_notebook.py
git commit -m "feat: ajoute filtre EXPORT/SKIP (fonctions pures)"
```

---

### Task 2: Ajouter treat + bouton Clear + CLI double-mode

**Files:**
- Modify: `scripts/filter_notebook.py`

- [ ] **Step 1: Écrire le test CLI (failing)**

Créer `/tmp/fixture.ipynb` (généré par script, pas à la main) via :

```python
import json
nb = {
 "cells": [
  {"cell_type": "markdown", "source": ["# Titre\n"], "metadata": {}},
  {"cell_type": "code", "source": ["x = 1  # EXPORT\n", "y = 2  #SKIP\n", "z = 3\n"], "metadata": {}, "outputs": [{"a": 1}], "execution_count": 5},
  {"cell_type": "code", "source": ["secret = 1\n"], "metadata": {}, "outputs": [], "execution_count": 1},
 ],
 "metadata": {}, "nbformat": 4, "nbformat_minor": 5,
}
Path("/tmp/fixture.ipynb").write_text(json.dumps(nb), encoding="utf-8")
```

Puis test `/tmp/test_cli.py` :

```python
import json, subprocess, sys
from pathlib import Path
r = subprocess.run([sys.executable, "scripts/filter_notebook.py", "/tmp/fixture.ipynb", "/tmp/out.ipynb"], capture_output=True, text=True)
assert r.returncode == 0, r.stderr
data = json.loads(Path("/tmp/out.ipynb").read_text(encoding="utf-8"))
assert len(data["cells"]) == 2, data
code = data["cells"][1]
assert "".join(code["source"]) == "x = 1  # EXPORT\n# TODO\n"
assert code["outputs"] == [] and code["execution_count"] is None
print("OK task2")
```

- [ ] **Step 2: Lancer, constater l'échec**

Run: `uv run python /tmp/test_cli.py`
Expected: FAIL (pas de CLI `source dest`, `SystemExit != 0` ou fichier absent).

- [ ] **Step 3: Implémenter treat + bouton + main**

Ajouter à la fin de `scripts/filter_notebook.py` :

```python
def has_clear_button(nb: dict) -> bool:
    cells = nb.get("cells", [])
    if not cells:
        return False
    return "button_for_indexeddb" in source_text(cells[0])


def insert_clear_button(nb: dict, notebook_rel: str) -> None:
    if has_clear_button(nb):
        return
    html = (
        f'<button type="button" id="button_for_indexeddb">Clear notebook {notebook_rel}</button>'
        f'<script>window.button_for_indexeddb.onclick = function(e) {{'
        f'window.indexedDB.open(\'JupyterLite Storage\').onsuccess = function(e) {{'
        f'let tables = ["checkpoints", "files"];'
        f'let t = e.target.result.transaction(tables, "readwrite");'
        f'function clearNotenook(tablename) {{'
        f't.objectStore(tablename).delete(\'{notebook_rel}\').onsuccess = function(e) {{'
        f'console.log("Deleted {notebook_rel} state in " + tablename);}}}};}}}};</script>'
    )
    cell_source = (
        "from IPython.display import display, HTML\n"
        f"display(HTML(\"\"\"{html}\"\"\"))"
    )
    nb["cells"].insert(0, {
        "cell_type": "code",
        "source": cell_source,
        "metadata": {},
        "outputs": [],
        "execution_count": None,
    })


def treat_data(nb: dict, rel: str | None, with_button: bool) -> dict:
    nb["cells"] = filter_cells(nb.get("cells", []))
    if with_button and rel is not None:
        insert_clear_button(nb, rel)
    return nb


def treat_file(path: Path, root: Path, with_button: bool) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    rel = str(path.relative_to(root)) if with_button else None
    treat_data(data, rel, with_button)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def iter_notebooks(root: Path):
    for nb in root.glob("**/*.ipynb"):
        if ".ipynb_checkpoints" in nb.parts:
            continue
        yield nb


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Filtre EXPORT/SKIP + clear outputs.")
    p.add_argument("src", nargs="?", help="notebook source (mode fichier)")
    p.add_argument("dst", nargs="?", help="notebook destination (mode fichier)")
    p.add_argument("--in-place", dest="in_place", default=None, help="dossier à traiter sur place (CI)")
    args = p.parse_args(argv)
    if args.in_place:
        root = Path(args.in_place)
        if not root.is_dir():
            print(f"dossier introuvable: {root}", file=sys.stderr)
            return 2
        for nb in iter_notebooks(root):
            print(f"treating notebook {nb}")
            treat_file(nb, root, with_button=True)
        return 0
    if not args.src or not args.dst:
        p.print_usage(sys.stderr)
        return 2
    src, dst = Path(args.src), Path(args.dst)
    if not src.is_file():
        print(f"source introuvable: {src}", file=sys.stderr)
        return 2
    data = json.loads(src.read_text(encoding="utf-8"))
    treat_data(data, None, with_button=False)
    dst.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Relancer, constater le succès**

Run: `uv run python /tmp/test_cli.py`
Expected: PASS, affiche `OK task2`. Vérifier aussi `--help` : `uv run python scripts/filter_notebook.py --help` affiche les 3 args.

- [ ] **Step 5: Commit**

```bash
git add scripts/filter_notebook.py
git commit -m "feat: ajoute CLI fichier et --in-place + bouton Clear"
```

---

### Task 3: Intégrer au workflow CI (deploy.yml)

**Files:**
- Modify: `.github/workflows/deploy.yml`

- [ ] **Step 1: Relire le fichier actuel**

Contenu actuel pertinent (lignes ~24-28) :

```yaml
      - name: Build the JupyterLite site
        run: |
          uv run jupyter lite build --output-dir dist
```

- [ ] **Step 2: Ajouter l'étape post-treatment**

Remplacer par :

```yaml
      - name: Build the JupyterLite site
        run: |
          uv run jupyter lite build --output-dir dist
      - name: post-treatment
        run: |
          uv run python scripts/filter_notebook.py --in-place dist/files/
```

Si `dist/files/` n'existe pas au premier build local (à valider Task 4 : lister `dist/` et ajuster en `dist/` si besoin — le glob `**/*.ipynb` couvre les sous-dossiers, donc `dist` marche aussi ; préférer `dist/files` pour coller à cours_algo, fallback `dist`).

- [ ] **Step 3: Valider YAML**

Run: `python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/deploy.yml')); print('YAML OK')"`
Si `pyyaml` absent : `uv run --with pyyaml python -c "import yaml; yaml.safe_load(open('.github/workflows/deploy.yml')); print('YAML OK')"`
Expected: `YAML OK`.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/deploy.yml
git commit -m "ci: filtre EXPORT/SKIP au build JupyterLite"
```

---

### Task 4: Vérification bout-en-bout sur copies réelles

**Files:** aucun commité (travail en `/tmp` uniquement).

- [ ] **Step 1: Générer depuis le corrigé réel**

Run: `uv run python scripts/filter_notebook.py td_01_perceptron/corrige.ipynb /tmp/perceptron_test.ipynb && python3 -c "import json; d=json.load(open('/tmp/perceptron_test.ipynb')); print('cells:', len(d['cells'])); print(''.join(d['cells'][0]['source'])[:300])"`
Expected: `cells:` <= 21 (seules les cellules avec EXPORT survivent ; aujourd'hui corrige n'a aucun EXPORT donc 0 code + markdown restants — c'est normal avant d'annoter le corrigé).

- [ ] **Step 2: Test bouton + idempotence en mode in-place**

Run: `mkdir -p /tmp/inplace && cp /tmp/fixture.ipynb /tmp/inplace/nb.ipynb && uv run python scripts/filter_notebook.py --in-place /tmp/inplace/ && uv run python scripts/filter_notebook.py --in-place /tmp/inplace/ && python3 -c "import json; d=json.load(open('/tmp/inplace/nb.ipynb')); print('cells:', len(d['cells'])); print('boutons:', ''.join(d['cells'][0]['source']).count('button_for_indexeddb'))"`
Expected: `boutons: 1` (pas de doublon au 2e run), `cells: 3` (bouton + markdown + code filtré).

- [ ] **Step 3: py_compile + nettoyage**

Run: `python3 -m py_compile scripts/filter_notebook.py && echo COMPILE_OK && rm -f /tmp/out.ipynb /tmp/perceptron_test.ipynb && rm -rf /tmp/inplace`
Expected: `COMPILE_OK`.

- [ ] **Step 4: Commit final si ajustements** (seulement si Task 4 a forcé un fix, ex. chemin `dist` vs `dist/files`)

```bash
git status --short
# si diff: git add -A && git commit -m "fix: ajustement chemin post-treatment"
```

---

## Self-review

- Spec §4 (substring EXPORT code-only, suppression, SKIP→TODO, source list/str, outputs vidés) : couvert Task 1 Steps 1-4.
- Spec §3 (bouton repris cours_algo + anti-doublon, CLI local sans bouton / CI avec bouton) : couvert Task 2.
- Spec §5 (local corrige→perceptron, CI après build, config inchangée) : couvert Tasks 2-3.
- Spec §6 (erreurs exit 2, checkpoints ignorés, idempotence, utf-8/ensure_ascii) : couvert Task 2 code + Task 4 Step 2.
- Spec §7 (jouet, py_compile, diff, build) : couvert Task 4.
- Pas de placeholders : tous les blocs de code sont complets et copiables.
- Cohérence types : `source_text(cell)->str`, `as_lines->list[str]`, `truncate_skip(list)->list`, `filter_cells(list)->list`, `treat_data(nb, rel|None, bool)->dict` — mêmes noms/signatures dans Tasks 1-2.
