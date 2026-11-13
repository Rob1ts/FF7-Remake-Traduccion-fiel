#!/usr/bin/env python3
"""Convierte un CSV de traducción de FF7R al JSON de FF7R_text_mod_tools.

El CSV de entrada debe tener tres columnas: ``id,sub_id,text``.

- Una fila con ``sub_id`` vacío contiene el texto principal de la entrada.
- Una fila con ``sub_id`` no vacío (ARTICLE, PLURAL, SINGULAR, ARTICLE2,
  ACTOR...) contiene una subentrada gramatical o de actor.
- Los saltos de línea internos se escriben como ``<br>`` en el CSV y se
  convierten a saltos CRLF en el JSON.

Ejemplo::

    python herramientas/csv_to_json.py traduccion/csv/140-SBIL0_TxtRes.csv

Genera ``140-SBIL0_TxtRes.json`` junto al CSV. Después se convierte a ``.uexp``
con FF7R_text_mod_tools (modo ``json2uexp``), usando el ``.uexp`` ES original
como plantilla.
"""

import argparse
import csv
import io
import json
import os
from collections import OrderedDict


def simplify(values):
    """Replica el formato de FF7R_text_mod_tools: null / cadena / lista."""
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    return values


def is_not_subtitle(resource, ident):
    """Replica TextUexp.is_not_subtitle() de FF7R_text_mod_tools."""
    if resource[:3].isdecimal():
        return (
            ident[:6] == "$level"
            or (
                ident[-3] != "0"
                and ident[-12:-8] == "_900"
                and ident[-7:-3] == "_cut"
            )
        )
    return not ident.endswith(("chd_0", "art_0", "cld_0"))


def convert(src, dst):
    base = os.path.basename(src)
    resource = base[: -len("_TxtRes.csv")] if base.endswith("_TxtRes.csv") else os.path.splitext(base)[0]

    rows = list(csv.reader(io.open(src, encoding="utf-8-sig", newline="")))
    records = OrderedDict()
    for r in rows[2:]:
        if len(r) < 3:
            continue
        ident, sub_id, text = r[0], r[1], r[2]
        rec = records.setdefault(ident, {"main": None, "subs": []})
        if sub_id == "":
            rec["main"] = text
        else:
            rec["subs"].append(text)

    data = []
    for ident, rec in records.items():
        if rec["main"] is None:
            raise SystemExit(f"Falta la fila principal de {ident}")
        item = {
            "id": ident,
            "text": rec["main"].replace("<br>", "\r\n"),
        }
        subs = [s.replace("<br>", "\r\n") for s in rec["subs"]]
        key = "info" if is_not_subtitle(resource, ident) else "speaker"
        item[key] = simplify(subs)
        data.append(item)

    doc = {
        "data": data,
        "meta": {"tool": "FF7R text mod tools", "version": "1.4.2", "game": "FF7R"},
    }
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    with io.open(dst, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=4)
        f.write("\n")
    print(f"Escrito {dst} ({len(data)} entradas)")


def main():
    ap = argparse.ArgumentParser(
        description="Convierte un CSV de traducción de FF7R al JSON de FF7R_text_mod_tools."
    )
    ap.add_argument("csv", help="CSV de entrada (id, sub_id, text)")
    ap.add_argument(
        "-o",
        "--output",
        help="JSON de salida (por defecto: junto al CSV, con extensión .json)",
    )
    args = ap.parse_args()

    dst = args.output
    if not dst:
        dst = os.path.splitext(args.csv)[0] + ".json"
    convert(args.csv, dst)


if __name__ == "__main__":
    main()
