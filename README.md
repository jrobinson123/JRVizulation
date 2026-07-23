# jrviz

A tiny, modern-looking charting layer over matplotlib. Sensible defaults, a
validated colorblind-safe palette, and light/dark themes — in under 150 lines.

## Install

```bash
pip install -e .
```

## Usage

```python
import jrviz as vz
import numpy as np

# Bar chart
vz.bar(["Q1", "Q2", "Q3", "Q4"], [12, 19, 14, 22], title="Quarterly revenue", ylabel="$M")

# Multi-series line chart
x = np.arange(8)
vz.line(x, [[3, 4, 6, 5, 7, 8, 7, 9], [2, 3, 3, 4, 5, 5, 6, 7]],
        labels=["North", "South"], title="Weekly signups")

# Scatter (dark mode)
vz.scatter(np.random.randn(80), np.random.randn(80), title="Scatter demo", dark=True)

# Histogram
vz.hist(np.random.randn(500), bins=30, title="Distribution")

# Heatmap on the sequential ramp
vz.heatmap(np.random.rand(5, 5), row_labels=list("ABCDE"), col_labels=list("12345"),
           title="Heatmap demo")

vz.show()          # or vz.save("chart.png")
```

## API

| Function | Purpose |
|----------|---------|
| `bar(categories, values, ...)` | Vertical bar chart with value labels |
| `line(x, series, labels=..., ...)` | One or more line series |
| `scatter(x, y, ...)` | Scatter plot |
| `hist(values, bins=..., ...)` | Histogram |
| `heatmap(matrix, row_labels=..., col_labels=..., ...)` | Magnitude grid |
| `style(dark=False)` | Apply the theme to the current rcParams |
| `show()` / `save(path)` | Lay out and display / write to disk |

Every chart accepts `dark=True` for dark mode, `title` / `xlabel` / `ylabel`,
and an existing `ax=` so charts compose into matplotlib subplots.

Exposed palettes: `CATEGORICAL`, `SEQUENTIAL`, `DIVERGING`.
