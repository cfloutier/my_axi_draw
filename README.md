# my_axi_draw

Personal GUI tool to control an **AxiDraw** plotter via the official Python API.
Load an SVG file, preview the estimated drawing duration, and control execution (pause, resume, stop, return home) with real-time progress tracking.

---

## Project structure

```
main_ui.py          # Entry point — main window with tabs
plotter.py          # Plotter control logic (state machine, threading)
settings.py         # Settings management (YAML profiles, hardware params)
globals.py          # Shared logger
toggle.py           # Standalone toggle utility

ui/
  trace_page.py         # Main tab: load SVG, run/pause/stop, progress tracking
  pen_page.py           # Pen tab: up/down positions, manual control
  speed_page.py         # Speed tab: speeds, acceleration, raise/lower rates
  trace_options_page.py # Options tab: path reordering, clipping, auto-rotate
  calibration_page.py   # Calibration tab: model, resolution, test SVG generation
  settings_frame.py     # Profile bar (select, save, reset)

settings/
  default.yml       # Default profile
  internal.yml      # App internal state (current file, active profile)
  plotter.yml       # Hardware parameters (model, dimensions, resolution)
  *.yml             # Profiles per pen type (bic, marker, posca…)

tools/
  svg_editor.py     # SVG XML manipulation (editing, test SVG generation)
  nested_dict.py    # Dot-notation access to nested config dicts
  time.py           # Duration formatting (timedelta → human-readable)
  fs.py             # File system utilities
  ctk/              # Reusable CustomTkinter widgets
    base_frame.py       # Base frame with automatic layout
    edit_boxes.py       # Numeric input with validation
    progress_bar.py     # Progress bar with centered text overlay
    separator.py        # Visual separator

AxiDraw_API/        # Local PyAxiDraw API (v3.9.6)
```

---

## Installation

- Install Python
- Install the AxiDraw API: https://axidraw.com/doc/py_api
  - Download and unzip into a local folder `[AXIDRAW_FOLDER]`
  - Follow the included `Installation.txt`

```powershell
# Create the local virtual environment
python -m venv venv

# Activate the environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Go to the API folder and install dependencies
cd [AXIDRAW_FOLDER]
pip install .

# Go back to the project folder and install UI dependencies
cd [PROJECT_FOLDER]
pip install customtkinter coloredlogs
```

**VSCode note**: if the axidraw path is not resolved, add to `.vscode/settings.json`:

```json
{
    "python.analysis.extraPaths": ["C:\\dev\\__tracer\\api\\AxiDraw_API\\AxiDraw_API_396"]
}
```

Set the Python interpreter to `venv/Scripts/python.exe`.

**Windows 11**: install Microsoft Visual C++ 2015 Redistributables if needed.

### Pre-commit (optional)

```powershell
.\venv\Scripts\Activate.ps1
pip install pre-commit
pre-commit install
```

---

## Known limitations

- **Pause/resume on points-only plots (stippling, dots)**: Does not work. `axidrawinternal` tracks resume position via `down_travel_inch`, which stays at `0.0` for vertical pen-down moves with no horizontal displacement (pure dots). As a result, `crop(0)` is a no-op and the plotter always restarts from the beginning after a pause. This is a fundamental limitation of the underlying library.

## Changelog

### 2026-05-10
- **Affichage du temps écoulé** : la barre de progression affiche maintenant simultanément le temps écoulé, le temps restant et le total (`XX.X% - elapsed 01:42 - remaining 03:15 / 04:57`).
- **Format de durée condensé** : `td_format` utilise désormais le format `HH:MM:SS` / `MM:SS` / `Xs` / `Nd HH:MM:SS` selon la magnitude, sans redondance ni unités textuelles.
- **Chrono démarré au premier mouvement** : le compteur de temps démarre maintenant au premier déplacement moteur détecté (stylo haut ou bas), excluant le temps de chargement et de parsing SVG. Pendant cette phase initiale, la barre affiche `"loading..."`.
- **Détection de mouvement générique** : la détection du premier mouvement se base sur `up_travel + down_travel > 0`, couvrant aussi les tracés de points (sans déplacement stylo bas horizontal).
- **Correction dynamique de l'estimation** : le temps total estimé est progressivement corrigé en fonction du rythme réel observé. Transition entre 20% et 60% de progression pour éviter l'instabilité en début de tracé.
- **Affichage du dépassement** : quand le temps estimé est dépassé, affiche `elapsed XX:XX - overtime +MM:SS / total` au lieu d'une valeur négative.

### 2026-05-09
- **Fast resume after pause**: enabled plob cache (`digest=1`) at draw start. The AxiDraw lib stores processed paths as a simplified format (polylines) after the first pass. On resume, the document is recognized as a valid plob and `prepare_document()` is skipped — resuming is near-instant regardless of SVG complexity.
- **Fix crash on resume**: `digest=1` left `document` as `lxml.etree._Element` instead of `ElementTree`, causing a crash on `document.getroot()`. Fixed before each `plot_run()` call on a paused object (`back_home` and `res_plot`).

### Earlier
- Fixed remaining time not adjusted during pauses
- Fixed UI layout issues
- Fixed progress bar text rendering
- Calibration page: added A6/A5/A4/A3/A2 support with precision slider
- Auto-pause feature (configurable timer, useful for refilling pen)
- Resume with pen height changes between runs
