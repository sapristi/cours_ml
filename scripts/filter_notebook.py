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
