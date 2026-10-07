"""Prépare les notebooks pour la diffusion (jupyterlite).

Retire les solutions (blocs # BEGIN/# END → # TODO + pass), vide les outputs
et insère le bouton « Clear notebook ».

Les commentaires écrits juste après ``# BEGIN`` deviennent le corps du TODO :
``# code`` est dé-commenté (devient du code), ``## indice`` garde un ``#``.
Sans commentaire, le script émet ``# TODO`` + ``pass`` comme avant.

Aperçu:  python scripts/prepare_notebooks.py corrige.ipynb apercu.ipynb
CI:      python scripts/prepare_notebooks.py --in-place dist/files/
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
BEGIN_MARKER = "# BEGIN"
END_MARKER = "# END"
TODO = "# TODO"
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
def uncomment_line(line: str) -> tuple[str, bool]:
    """Transforme une ligne de commentaire du corps du TODO.

    ``# code`` → ``code`` (dé-commenté, devient du code) ; ``## indice`` →
    ``# indice`` (conserve un ``#``). Renvoie ``(ligne, est_du_code)``.
    """
    indent = line[: len(line) - len(line.lstrip())]
    content = line[len(indent):]
    if content.startswith("##"):
        return indent + content[1:], False
    body = content[1:]
    if body.startswith(" "):
        body = body[1:]
    return indent + body, True


def truncate_blocks(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if BEGIN_MARKER not in line:
            out.append(line)
            i += 1
            continue
        indent = line[: len(line) - len(line.lstrip())]
        newline = "\n" if line.endswith("\n") else ""
        out.append(indent + TODO + newline)
        i += 1
        has_code = False
        while i < len(lines):
            nxt = lines[i]
            if not nxt.lstrip().startswith("#") or END_MARKER in nxt:
                break
            emitted, is_code = uncomment_line(nxt)
            out.append(emitted)
            has_code = has_code or is_code
            i += 1
        if not has_code:
            out.append(indent + "pass" + newline)
        while i < len(lines) and END_MARKER not in lines[i]:
            i += 1
        if i < len(lines):
            i += 1
    return out


def clear_cell(cell: dict) -> None:
    cell["outputs"] = []
    if "execution_count" in cell:
        cell["execution_count"] = None
def filter_cells(cells: list[dict]) -> list[dict]:
    kept: list[dict] = []
    for cell in cells:
        if cell.get("cell_type") == "code":
            cell["source"] = truncate_blocks(as_lines(cell))
            clear_cell(cell)
        kept.append(cell)
    return kept


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
        f'console.log("Deleted {notebook_rel} state in " + tablename + " (" + e.target.result + ")");}}}};'
        f'for (let tablename of tables) {{ clearNotenook(tablename); }}'
        f'}}}}}};</script>'
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
    if with_button and has_clear_button(nb):
        # déjà traité : ne pas refiltrer (idempotence) ni réinsérer le bouton.
        return nb
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
    p = argparse.ArgumentParser(description="Prépare les notebooks pour la diffusion (BEGIN/END → TODO + clear outputs).")
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
