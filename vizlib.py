"""vizlib: a tiny, modern-looking charting layer over matplotlib.

    import vizlib as vz
    vz.bar(["A", "B", "C"], [3, 7, 5], title="Widgets sold")
    vz.line(x, [y1, y2], labels=["north", "south"], title="Revenue")
    vz.show()
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Validated categorical order (fixed — never cycle past what you need).
CATEGORICAL = [
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100",
    "#e87ba4", "#008300", "#4a3aa7", "#e34948",
]
# Single-hue sequential ramp (light -> dark) for magnitude encodings.
SEQUENTIAL = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
# Diverging pair (cool -> neutral -> warm) for polarity encodings.
DIVERGING = ["#2a78d6", "#f0efec", "#e34948"]

_LIGHT = dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
              grid="#e1e0d9", axis="#c3c2b7")
_DARK = dict(surface="#1a1a19", ink="#ffffff", ink2="#c3c2b7", muted="#898781",
             grid="#2c2c2a", axis="#383835")


def style(dark=False):
    """Apply the vizlib rcParams theme and return its color roles."""
    theme = _DARK if dark else _LIGHT
    plt.rcParams.update({
        "figure.facecolor": theme["surface"],
        "axes.facecolor": theme["surface"],
        "savefig.facecolor": theme["surface"],
        "axes.edgecolor": theme["axis"],
        "axes.labelcolor": theme["ink2"],
        "text.color": theme["ink"],
        "xtick.color": theme["muted"],
        "ytick.color": theme["muted"],
        "grid.color": theme["grid"],
        "grid.linewidth": 0.8,
        "axes.linewidth": 0.8,
        "axes.axisbelow": True,
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "axes.prop_cycle": plt.cycler(color=CATEGORICAL),
    })
    return theme


def _canvas(ax, figsize):
    if ax is not None:
        return ax.figure, ax
    return plt.subplots(figsize=figsize)


def _finish(ax, theme, *, title=None, xlabel=None, ylabel=None, legend=False):
    if title:
        ax.set_title(title, pad=14)
    if xlabel:
        ax.set_xlabel(xlabel, labelpad=8)
    if ylabel:
        ax.set_ylabel(ylabel, labelpad=8)
    ax.grid(axis="y", zorder=0)
    ax.grid(axis="x", visible=False)
    ax.tick_params(length=0)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(theme["axis"])
    if legend:
        ax.legend(loc="upper left", bbox_to_anchor=(0, -0.14), ncol=4,
                   handlelength=1.2, fontsize=9, labelcolor=theme["ink2"])
    return ax


def bar(categories, values, *, ax=None, dark=False, title=None, xlabel=None,
         ylabel=None, color=None, figsize=(7, 4.2)):
    theme = style(dark)
    fig, ax = _canvas(ax, figsize)
    bars = ax.bar(categories, values, color=color or CATEGORICAL[0], width=0.6,
                   zorder=3, edgecolor=theme["surface"], linewidth=0.6)
    ax.bar_label(bars, padding=3, fontsize=9, color=theme["ink2"])
    return _finish(ax, theme, title=title, xlabel=xlabel, ylabel=ylabel)


def line(x, series, *, labels=None, ax=None, dark=False, title=None, xlabel=None,
          ylabel=None, figsize=(7, 4.2)):
    theme = style(dark)
    fig, ax = _canvas(ax, figsize)
    series = np.atleast_2d(series)
    for i, y in enumerate(series):
        ax.plot(x, y, color=CATEGORICAL[i % len(CATEGORICAL)], linewidth=2.2,
                 label=labels[i] if labels else None, marker="o", markersize=4.5,
                 markeredgecolor=theme["surface"], markeredgewidth=0.6, zorder=3)
    return _finish(ax, theme, title=title, xlabel=xlabel, ylabel=ylabel, legend=bool(labels))


def scatter(x, y, *, ax=None, dark=False, title=None, xlabel=None, ylabel=None,
             color=None, size=45, figsize=(7, 4.2)):
    theme = style(dark)
    fig, ax = _canvas(ax, figsize)
    ax.scatter(x, y, s=size, color=color or CATEGORICAL[0], alpha=0.85,
               edgecolor=theme["surface"], linewidth=0.6, zorder=3)
    return _finish(ax, theme, title=title, xlabel=xlabel, ylabel=ylabel)


def hist(values, *, bins=20, ax=None, dark=False, title=None, xlabel=None,
          ylabel=None, color=None, figsize=(7, 4.2)):
    theme = style(dark)
    fig, ax = _canvas(ax, figsize)
    ax.hist(values, bins=bins, color=color or CATEGORICAL[0], zorder=3,
            edgecolor=theme["surface"], linewidth=0.6)
    return _finish(ax, theme, title=title, xlabel=xlabel, ylabel=ylabel)


def heatmap(matrix, *, row_labels=None, col_labels=None, ax=None, dark=False,
             title=None, figsize=(6, 5)):
    """Magnitude grid on the sequential ramp."""
    theme = style(dark)
    fig, ax = _canvas(ax, figsize)
    cmap = LinearSegmentedColormap.from_list("vizlib_seq", SEQUENTIAL)
    im = ax.imshow(matrix, cmap=cmap, aspect="auto")
    ax.set_xticks(range(len(col_labels or [])), labels=col_labels or [])
    ax.set_yticks(range(len(row_labels or [])), labels=row_labels or [])
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04).outline.set_visible(False)
    if title:
        ax.set_title(title, pad=14)
    return ax


def show(*args, **kwargs):
    plt.tight_layout()
    plt.show(*args, **kwargs)


def save(path, *args, **kwargs):
    plt.tight_layout()
    plt.savefig(path, dpi=180, *args, **kwargs)
