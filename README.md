# FINAL FANTASY VII REMAKE — Traducción fiel al español (desde el japonés)

Traducción al español de España de **FINAL FANTASY VII REMAKE** y de su episodio **INTERmission**, realizada **directamente desde el japonés**. El español oficial no se usa como fuente: solo como referencia para nombres propios, terminología de menús y subentradas gramaticales.

[![Versión](https://img.shields.io/badge/versi%C3%B3n-1.0-blue)](../../releases/latest)
![Texto](https://img.shields.io/badge/texto-ES%20(Espa%C3%B1a)-red)
![Origen](https://img.shields.io/badge/origen-japon%C3%A9s-lightgrey)

---

## Descarga

El mod se distribuye como **release** de este repositorio:

- **[Descargar la última versión](../../releases/latest)**
- Archivo: `pakchunk99_ES_JP_P.pak`
- Versión: **1.0** (13/11/2026)
- Tamaño: **905.449 bytes**
- SHA-256: `0865C739666D8A7679793CFDC0950AD6A0C28B1E7B09A9EF6C5491096B18986A`

## Qué incluye

La traducción cubre los 21 recursos de texto del juego:

- Historia principal y escenas cinemáticas.
- Diálogos de PNJ, misiones secundarias y conversaciones opcionales.
- Menús, tutoriales, descripciones de objetos, materias y armas.
- Correos, tutoriales y textos del sistema.
- Todo el texto de **INTERmission** (Yuffie).

| Dato | Valor |
|---|---|
| Recursos de texto | 21 |
| Entradas de texto | más de 35.500 |
| Filas con origen japonés revisadas | 29.702 |
| Subentradas gramaticales conservadas | 1.671 (solo en `Resident`) |
| Archivos dentro del pak | 43 (21 `.uasset` + 21 `.uexp` + `modroot.txt`) |

## Criterios de traducción

- **El japonés es la fuente.** Cuando el texto japonés y el español oficial difieren, se traduce el japonés.
- **El español oficial es referencia**, no fuente: se usa para nombres propios, términos de menú y variantes gramaticales de los objetos.
- **Nombres propios sin traducir** y siempre en caja normal: Cloud, Barret, Tifa, Aeris, Sefirot, Shinra, Midgar, Avalancha, TURKS, etc.
- **`SOLDIER` se mantiene** en mayúsculas, igual que en el original.
- **Nombres oficiales en español**: Mireia, Escarlata, Jénova, Madame M, Presidente Shinra.
- **`Jénova Beat` se conserva** como nombre del enemigo porque el japonés es `ジェノバＢｅａｔ`; el español oficial lo llamó «Jénova alfa», pero se ha priorizado el original.
- **Trato**: `tú` dentro del grupo y en contextos cercanos; `usted` en situaciones formales, con Shinra y con personajes de autoridad.
- **Honoríficos adaptados** al español; no se dejan sufijos como `-san` o `-chan`.
- **Profanidad moderada**, equivalente a la del japonés.
- **Latiguillos en inglés** cuando el original japonés los usa en katakana (Jay, Roche). Los títulos de las pistas de la gramola se mantienen en inglés porque son títulos oficiales.
- **Etiquetas y saltos de línea** se conservan y se adaptan al ancho de la caja de diálogo en español.

## Cómo se hizo la traducción

### 1. Extracción

Se partió de los archivos de texto originales del juego (`End/Content/GameContents/Text/`):

- El locale **ES** se usó como **plantilla estructural**: mismos identificadores, mismas subentradas y mismas etiquetas funcionales.
- El locale **JP** se usó como **fuente de significado**.

Ambos se extrajeron de los `.pak` originales con un extractor propio en Python. El texto japonés **no se redistribuye** en este repositorio: cada usuario debe extraerlo de su propia copia legal del juego.

### 2. Volcado a CSV

Cada recurso `.uexp` se convirtió a JSON con `FF7R_text_mod_tools` y después a un CSV de tres columnas:

```csv
id,sub_id,text
$tk_sbil0_50_2750_0020_cld_0,,Ma... a...
```

- Una fila por entrada principal (`sub_id` vacío).
- Una fila por subentrada gramatical (`ARTICLE`, `PLURAL`, `SINGULAR`, `ARTICLE2`) o de actor (`ACTOR`).
- Los saltos de línea internos se guardan como `<br>` durante la edición.

Este formato permite traducir con cualquier editor de texto, hacer búsquedas y comparar líneas de forma sencilla.

### 3. Traducción

- Traducción **fila a fila desde el japonés**, no desde el inglés ni desde el español oficial.
- Cuando el japonés tiene una línea vacía (voz sin subtítulo), la traducción se deja vacía en lugar de inventar texto.
- Se conservan las etiquetas del juego (`<br>`, `<color>`, `<button>`, `<object>`, `<n-objects>`, `<an-object>`, etc.).
- Los saltos de línea se ajustan al ancho de la caja de diálogo en español.

### 4. Control de calidad

Se comprobó, sobre los 21 recursos:

- **0 filas** con texto japonés y traducción vacía.
- **0 caracteres kana/kanji** en la traducción. Solo se conservan signos de puntuación y espaciado japoneses en textos de interfaz y estilo oficial (`【】`, `・`, `＞` y el espacio ideográfico U+3000).
- **Etiquetas alineadas** con el original japonés, normalizando las etiquetas funcionales de objeto del locale ES. Las 34 diferencias de `<count>` son intencionadas.
- **Subentradas gramaticales** de los objetos conservadas (sin ellas, avisos como «Has obtenido…» mostraban el nombre vacío).
- **Round-trip**: cada `.uexp` reconstruido se vuelve a leer y su texto coincide exactamente con el JSON de entrada.
- **Verificación byte a byte** entre los archivos preparados y los extraídos del pak final.

### 5. Empaquetado

1. El CSV traducido se convierte de nuevo a JSON con `herramientas/csv_to_json.py`.
2. El JSON se convierte a `.uexp` con `FF7R_text_mod_tools`, usando el `.uexp` ES original como plantilla.
3. Los 21 recursos se empaquetan con **UnrealPak** en `pakchunk99_ES_JP_P.pak`, con la ruta:

   ```text
   End/Content/GameContents/Text/ES/
   ```

4. El pak se instala en `End/Content/Paks/~mods/`.

## Herramientas utilizadas

| Herramienta | Uso |
|---|---|
| [FF7R_text_mod_tools 1.4.2](https://github.com/matyalatte/FF7R_text_mod_tools) (Matyalatte) | Conversión `.uexp` → JSON y JSON → `.uexp` |
| UnrealPak (Epic Games) | Creación del `.pak` comprimido; flujo de trabajo de FluffyQuack |
| Python 3 | Extractor de pak, conversor CSV ↔ JSON y comprobaciones de calidad |
| PowerShell | Verificación de copias y hashes SHA-256 |

El conversor CSV → JSON utilizado se incluye en [`herramientas/csv_to_json.py`](herramientas/csv_to_json.py).

## Instalación

### Requisitos

- **FINAL FANTASY VII REMAKE** para PC (Steam o Epic Games Store), con **INTERmission** si se quiere jugar el DLC.
- Idioma de texto del juego: **Español (España)**.

### Pasos

1. Cierra el juego.
2. Copia `pakchunk99_ES_JP_P.pak` en la carpeta `~mods`:

   ```text
   <carpeta del juego>\End\Content\Paks\~mods\
   ```

   Si la carpeta `~mods` no existe, créala.

   Ejemplo de Steam:

   ```text
   C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII REMAKE\End\Content\Paks\~mods\
   ```

3. Inicia el juego con el idioma de texto **Español (España)**.

### Comprobar el archivo

En PowerShell, dentro de la carpeta donde esté el pak:

```powershell
Get-FileHash .\pakchunk99_ES_JP_P.pak -Algorithm SHA256
```

Debe devolver:

```text
0865C739666D8A7679793CFDC0950AD6A0C28B1E7B09A9EF6C5491096B18986A
```

### Desinstalación

Borra `pakchunk99_ES_JP_P.pak` de la carpeta `~mods`.

### Problemas frecuentes

- **No se ve la traducción**: comprueba que el idioma de texto sea Español (España) y que el pak esté en `~mods`.
- **Otro mod pisa los textos**: este mod sustituye los 21 recursos de texto del locale ES. Si otro mod carga los mismos archivos, el orden de carga decide cuál se ve.
- **Tras una actualización del juego**: verifica que el pak sigue en `~mods` y que la ruta `End/Content/GameContents/Text/ES/` no ha cambiado.

## Estructura del repositorio

```text
.
├── README.md                  Este documento
├── CHANGELOG.md               Historial de versiones
├── LEEME.txt                  Guía rápida incluida con el mod
├── QA.txt                     Informe de control de calidad
├── LICENSE.md                 Condiciones de uso
├── traduccion/
│   └── csv/                   Texto traducido (21 CSV: id, sub_id, texto)
└── herramientas/
    └── csv_to_json.py         Conversor CSV → JSON para FF7R_text_mod_tools
```

El pak no se guarda en el historial de Git: se adjunta a cada release.

## Limitaciones conocidas

- **664 líneas** tienen el japonés vacío pero texto en el español oficial (interjecciones, voces sin subtítulo y algunas líneas de Sefirot). Se dejan vacías porque no hay texto japonés del que partir; rellenarlas sería inventar diálogo.
- **34 diferencias de `<count>`** respecto al japonés son intencionadas: el español oficial omite el contador cuando el número va implícito en la frase.
- **Puntuación japonesa** conservada en algunos textos de interfaz (`【】`, `・`, `＞`, U+3000), igual que en el locale ES oficial.
- **Solo texto**: el audio y los vídeos no se modifican.
- **No compatible** con otros mods que sustituyan exactamente los mismos 21 recursos de texto.

## Aviso legal

Traducción **personal y sin ánimo de lucro**, realizada por un particular. Esta traducción no está afiliada a Square Enix ni cuenta con su respaldo.

FINAL FANTASY VII REMAKE, sus personajes, textos originales y demás contenido son propiedad de **Square Enix**. Este repositorio no contiene archivos originales del juego ni el texto japonés: solo la traducción, las notas de proceso y las herramientas propias.

Necesitas una copia legal del juego para usar el mod.

## Créditos

- Traducción y control de calidad: **Rob1ts**.
- [FF7R_text_mod_tools](https://github.com/matyalatte/FF7R_text_mod_tools): **Matyalatte**.
- UnrealPak: **Epic Games**; flujo de empaquetado: **FluffyQuack**.
- A la comunidad de modding de FINAL FANTASY VII REMAKE.
