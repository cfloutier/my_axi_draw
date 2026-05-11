"""Generate a grid_dots.svg test file with 20x20 dots in row-by-row order."""

from pathlib import Path

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
lines.append('<svg width="210mm" height="297mm" viewBox="0 0 210 297" version="1.1"')
lines.append('   xmlns="http://www.w3.org/2000/svg"')
lines.append('   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape">')
lines.append('  <g inkscape:label="Layer 1" inkscape:groupmode="layer" id="layer1">')

cols = 10
rows = 10
# 60x60mm centered on A4 (210x297mm)
x_start, x_end = 75, 135
y_start, y_end = 118, 178

dot_id = 1
for row in range(rows):
    y = y_start + row * (y_end - y_start) / (rows - 1)
    for col in range(cols):
        x = x_start + col * (x_end - x_start) / (cols - 1)
        lines.append(
            f'    <line x1="{x:.4f}" y1="{y:.4f}" x2="{x+0.0001:.4f}" y2="{y+0.0001:.4f}"'
            f' id="dot{dot_id}" style="stroke:#000000;stroke-width:1;stroke-linecap:round"/>'
        )
        dot_id += 1

lines.append("  </g>")
lines.append("</svg>")

out = Path(__file__).parent.parent / "svg_templates" / "grid_dots.svg"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"Generated {dot_id - 1} dots -> {out}")
