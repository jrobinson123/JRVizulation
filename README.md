# jrviz

A **black-and-gold, gradient** charting layer over matplotlib. Molten-gold
gradient fills, near-black surfaces, and engraved display type. The house style
is deliberately dramatic — tuned to be *interesting* rather than maximally
accessible or neutral.

## Install

```bash
pip install -e .
```

Requires Python ≥ 3.9, `matplotlib` ≥ 3.6, and `numpy` ≥ 1.20 (installed
automatically). The **Cinzel** and **EB Garamond** display faces are bundled and
registered on import — no system font setup needed (SIL Open Font License, see
[`jrviz/fonts/LICENSES.md`](jrviz/fonts/LICENSES.md)).

## Quickstart

```python
import jrviz as vz

vz.bar(["A", "B", "C"], [3, 7, 5], title="Widgets sold")
vz.show()          # display, or vz.save("chart.png") to write a PNG
```

## Gallery

Every image below is produced by [`examples/gallery.py`](examples/gallery.py) —
run `python examples/gallery.py` to regenerate them.

| | |
|---|---|
| ![bar](examples/images/bar.png) | ![line](examples/images/line.png) |
| ![scatter](examples/images/scatter.png) | ![hist](examples/images/hist.png) |

![heatmap](examples/images/heatmap.png)

Pass `light=True` for the antique-parchment variant:

![parchment](examples/images/parchment.png)

```python
import numpy as np
import jrviz as vz

# Bar — vertical gold gradient per bar, value labels above
vz.bar(["Q1", "Q2", "Q3", "Q4"], [12, 19, 14, 22], title="Quarterly revenue", ylabel="$M")

# Multi-series line — glowing strokes over gradient area fills
x = np.arange(8)
vz.line(x, [[3, 4, 6, 5, 7, 8, 7, 9], [2, 3, 3, 4, 5, 5, 6, 7]],
        labels=["North", "South"], title="Weekly signups")

# Scatter — points shaded bright-gold→bronze by y-value, with a soft glow
vz.scatter(np.random.randn(120), np.random.randn(120), title="Scatter")

# Histogram — gradient bars
vz.hist(np.random.randn(800), bins=30, title="Distribution", xlabel="value")

# Heatmap — near-black→gold sequential ramp
vz.heatmap(np.random.rand(5, 5), row_labels=list("ABCDE"), col_labels=list("12345"),
           title="Heatmap")

vz.show()
```

### Triangular ornament (Deus Ex look)

`ornament(ax)` layers a faceted low-poly gold backdrop and angular HUD-style
corner brackets onto a finished chart — the *Mankind Divided* treatment.

![ornament](examples/images/ornament.png)

```python
ax = vz.bar(["Q1", "Q2", "Q3", "Q4"], [12, 19, 14, 22], title="Augmented", ylabel="$M")
vz.ornament(ax)    # faceted backdrop + corner brackets, in one call
vz.show()
```

### Composing into subplots

Every chart accepts an existing matplotlib `ax`, so you can build multi-panel
figures:

```python
import matplotlib.pyplot as plt
import jrviz as vz

fig, (left, right) = plt.subplots(1, 2, figsize=(12, 4))
vz.bar(["A", "B", "C"], [3, 7, 5], ax=left, title="Left")
vz.line(range(5), [0, 2, 1, 3, 2], ax=right, title="Right")
plt.show()
```

## API reference

### Common parameters

Every plotting function (`bar`, `line`, `scatter`, `hist`, `heatmap`) accepts
these keyword-only arguments:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ax` | `matplotlib.axes.Axes` | `None` | Draw onto an existing axes instead of creating a new figure. |
| `light` | `bool` | `False` | Use the parchment theme; the default is the onyx (black) theme. |
| `title` | `str` | `None` | Left-aligned engraved (Cinzel) chart title. |
| `figsize` | `(float, float)` | `(7, 4.2)` | Figure size in inches (ignored when `ax` is given). |

`bar`, `line`, `scatter`, and `hist` additionally accept `xlabel` and `ylabel`
(`str`, default `None`) for axis labels. All plotting functions **return the
`Axes`** they drew on.

### `bar(categories, values, **common)`

Vertical bar chart; each bar is filled with a bronze→gold vertical gradient and
gets a value label above it.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `categories` | sequence of `str` | — | X-axis category labels. |
| `values` | sequence of `float` | — | Bar heights, one per category. |

### `line(x, series, *, labels=None, **common)`

One or more line series sharing an x-axis. Each series gets the next gold hue, a
soft glow, a translucent gradient fill down to the baseline, and a marker at
every point.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | sequence | — | Shared x values. |
| `series` | 1-D or 2-D sequence | — | A single series (`[y0, y1, …]`) or a list of series (`[[…], [… ]]`). |
| `labels` | list of `str` | `None` | Legend label per series; a legend is drawn only when given. |

### `scatter(x, y, *, color=None, size=48, **common)`

Scatter plot with a soft glow behind each point.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x`, `y` | sequences | — | Point coordinates (equal length). |
| `color` | color | `None` | A single fill color for all points. When `None`, points are shaded by their `y`-value along the gold ramp. |
| `size` | `float` | `48` | Marker area in points². |

### `hist(values, *, bins=20, **common)`

Histogram of a single distribution, drawn as gradient bars.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `values` | sequence of `float` | — | Values to bin. |
| `bins` | `int` or sequence | `20` | Bin count, or explicit bin edges. |

### `heatmap(matrix, *, row_labels=None, col_labels=None, **common)`

Magnitude grid colored with the near-black→gold sequential ramp, plus a colorbar.
Accepts the common parameters except `xlabel`/`ylabel`.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `matrix` | 2-D array | — | Values to color, shape `(rows, cols)`. |
| `row_labels` | list of `str` | `None` | Y-axis tick labels. |
| `col_labels` | list of `str` | `None` | X-axis tick labels. |

### Helpers

| Function | Description |
|----------|-------------|
| `style(light=False)` | Apply the jrviz theme to matplotlib's global rcParams and return the color-role dict. Called automatically by every chart; use directly to theme your own matplotlib code. |
| `ornament(ax=None, *, light=False, seed=7)` | Add the faceted gold backdrop **and** angular corner brackets in one call. `facets(ax, ...)` and `corners(ax, ...)` are the individual pieces (`facets` accepts `density`, `alpha`, `edges`; both default to the current axes). |
| `show(*args, **kwargs)` | `tight_layout()` then `plt.show()`. |
| `save(path, *args, **kwargs)` | `tight_layout()` then `plt.savefig(path, dpi=180, …)`. |

### Palettes

Three color sequences are exported for building your own marks:

| Name | Purpose |
|------|---------|
| `CATEGORICAL` | 8 gold/bronze/copper hues for categories/series (separated by lightness). |
| `SEQUENTIAL` | Near-black→gold ramp for magnitude (used by `heatmap`). |
| `DIVERGING` | Gold ↔ ash ↔ patina triple for signed data. |
