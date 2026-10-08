import csv
import glob
import html
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
REPORT_PATH = os.path.join(OUTPUT_DIR, "results.html")

LABELS = {
    "window_h5": "window (horizon=5)",
    "window_h10": "window (horizon=10)",
    "sentence": "sentence",
}


def label_for(path):
    stem = os.path.splitext(os.path.basename(path))[0]
    for suffix, label in LABELS.items():
        if stem.endswith(suffix):
            return label
    return stem


def read_csv(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    return rows


def build_table(rows):
    if not rows:
        return "<p>No data.</p>"
    header, *body = rows
    parts = ["<table>", "<thead><tr>"]
    parts += [f"<th>{html.escape(c)}</th>" for c in header]
    parts += ["</tr></thead>", "<tbody>"]
    for row in body:
        parts.append("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in row) + "</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)


def main():
    paths = sorted(glob.glob(os.path.join(OUTPUT_DIR, "collocates_*.csv")))
    if not paths:
        raise SystemExit(f"No CSV files found in {OUTPUT_DIR}")

    sections = []
    options = []
    for i, path in enumerate(paths):
        label = label_for(path)
        rows = read_csv(path)
        options.append(
            f'<option value="table{i}">{html.escape(label)}</option>'
        )
        sections.append(
            f'<section id="table{i}" class="table-section" '
            f'style="display:{"block" if i == 0 else "none"}">'
            f"<h2>{html.escape(label)}</h2>{build_table(rows)}</section>"
        )

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Collocate results</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 2rem; }}
  select {{ font-size: 1rem; padding: 0.4rem; margin-bottom: 1rem; }}
  table {{ border-collapse: collapse; font-size: 0.9rem; }}
  th, td {{ border: 1px solid #ccc; padding: 4px 8px; text-align: left; }}
  th {{ background: #f0f0f0; }}
  tbody tr:nth-child(even) {{ background: #fafafa; }}
</style>
</head>
<body>
<h1>Collocate comparison</h1>
<label for="picker">Run: </label>
<select id="picker" onchange="show(this.value)">
{''.join(options)}
</select>
{''.join(sections)}
<script>
function show(id) {{
  document.querySelectorAll('.table-section').forEach(function (s) {{
    s.style.display = (s.id === id) ? 'block' : 'none';
  }});
}}
</script>
</body>
</html>
"""

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(document)

    print(f"Wrote {REPORT_PATH} from {len(paths)} CSV files")


if __name__ == "__main__":
    main()
