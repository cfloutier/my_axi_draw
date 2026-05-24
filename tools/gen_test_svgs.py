"""
Generate two pause/resume test SVG files:
  - grid_lines_test.svg   : 10x10 grid (lines only), each line is a sinusoidal polyline
  - grid_mixed_test.svg   : same grid + dots at cell centres, alternating row by row:
                            [10 dots in row i] then [h-line i], repeated,
                            then all 11 vertical lines

Both centred on A4 (210x297 mm), grid area 60x60 mm.
Lines follow a sine oscillation (AMPLITUDE mm, SINE_PERIODS periods) so that
axidrawinternal does not simplify them away.
"""

import math
from pathlib import Path

# ── geometry ──────────────────────────────────────────────────────────────────
X0, X1 = 75.0, 135.0  # horizontal extent (mm)
Y0, Y1 = 118.0, 178.0  # vertical extent  (mm)
COLS = 10  # number of cells horizontally
ROWS = 10  # number of cells vertically
SEGS = 40  # number of sub-segments per grid line (smooth sine)
AMPLITUDE = 3.0  # sine oscillation amplitude in mm
SINE_PERIODS = 2  # number of full sine periods per line

CELL_W = (X1 - X0) / COLS
CELL_H = (Y1 - Y0) / ROWS

LINE_STYLE = "stroke:#000000;stroke-width:0.3;stroke-linecap:round;fill:none"
DOT_STYLE = "stroke:#000000;stroke-width:1;stroke-linecap:round"

SVG_HEADER = """\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="210mm" height="297mm" viewBox="0 0 210 297" version="1.1"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape">
  <g inkscape:label="Layer 1" inkscape:groupmode="layer" id="layer1">"""
SVG_FOOTER = "  </g>\n</svg>"


def dot_elem(x: float, y: float, eid: str) -> str:
    return (
        f'    <line x1="{x:.4f}" y1="{y:.4f}"'
        f' x2="{x+0.0001:.4f}" y2="{y+0.0001:.4f}"'
        f' id="{eid}" style="{DOT_STYLE}"/>'
    )


def h_line_segments(row_idx: int) -> list[str]:
    """Horizontal sinusoidal polyline: x varies linearly, y oscillates."""
    y_base = Y0 + row_idx * CELL_H
    step = (X1 - X0) / SEGS
    pts = " ".join(
        f"{X0 + s * step:.4f},{y_base + AMPLITUDE * math.sin(SINE_PERIODS * 2 * math.pi * s / SEGS):.4f}"
        for s in range(SEGS + 1)
    )
    return [f'    <polyline points="{pts}" id="hl_{row_idx}" style="{LINE_STYLE}"/>']


def v_line_segments(col_idx: int) -> list[str]:
    """Vertical sinusoidal polyline: y varies linearly, x oscillates."""
    x_base = X0 + col_idx * CELL_W
    step = (Y1 - Y0) / SEGS
    pts = " ".join(
        f"{x_base + AMPLITUDE * math.sin(SINE_PERIODS * 2 * math.pi * s / SEGS):.4f},{Y0 + s * step:.4f}"
        for s in range(SEGS + 1)
    )
    return [f'    <polyline points="{pts}" id="vl_{col_idx}" style="{LINE_STYLE}"/>']


# ── SVG 1 : grid lines only ───────────────────────────────────────────────────
def gen_grid_lines(out_path: Path):
    elems = []

    # all horizontal lines (ROWS+1 = 11 lines)
    for r in range(ROWS + 1):
        elems.extend(h_line_segments(r))

    # all vertical lines (COLS+1 = 11 lines)
    for c in range(COLS + 1):
        elems.extend(v_line_segments(c))

    lines = [SVG_HEADER] + elems + [SVG_FOOTER]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {len(elems)} path items -> {out_path}")


# ── SVG 2 : mixed — dots and lines alternated row by row ─────────────────────
def gen_grid_mixed(out_path: Path):
    elems = []
    dot_id = 1

    # For each row of CELLS: first the 10 dots of that row, then the h-line
    for r in range(ROWS):
        # dots at cell centres in row r
        cy = Y0 + (r + 0.5) * CELL_H
        for c in range(COLS):
            cx = X0 + (c + 0.5) * CELL_W
            elems.append(dot_elem(cx, cy, f"dot_{dot_id}"))
            dot_id += 1
        # h-line r (top edge of row r)
        elems.extend(h_line_segments(r))

    # last horizontal line (bottom edge of last row)
    elems.extend(h_line_segments(ROWS))

    # all vertical lines
    for c in range(COLS + 1):
        elems.extend(v_line_segments(c))

    lines = [SVG_HEADER] + elems + [SVG_FOOTER]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    dots = dot_id - 1
    h_paths = ROWS + 1
    v_paths = COLS + 1
    print(
        f"Generated {dots} dots + {h_paths} h-polylines + {v_paths} v-polylines"
        f" = {len(elems)} path items -> {out_path}"
    )


if __name__ == "__main__":
    templates = Path(__file__).parent.parent / "svg_templates"
    gen_grid_lines(templates / "grid_lines_test.svg")
    gen_grid_mixed(templates / "grid_mixed_test.svg")
