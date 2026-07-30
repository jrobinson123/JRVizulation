"""Core of jrviz — a black-and-gold, gradient charting layer over matplotlib.

    import jrviz as vz
    vz.bar(["A", "B", "C"], [3, 7, 5], title="Widgets sold")
    vz.line(x, [y1, y2], labels=["north", "south"], title="Revenue")
    ax = vz.bar(["A", "B"], [3, 7], title="Augmented")
    vz.ornament(ax)   # Deus Ex-style faceted backdrop + corner brackets
    vz.show()

The house style is dramatic, not maximally accessible: near-black surfaces,
molten-gold gradients, and engraved display type. Pass ``light=True`` for the
antique-parchment variant.
"""
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib.collections import PolyCollection
from matplotlib.patches import Polygon
from matplotlib.tri import Triangulation

# --- fonts (bundled, SIL OFL — see fonts/LICENSES.md) -------------------------
_FONTS = os.path.join(os.path.dirname(__file__), "fonts")
for _file in ("Cinzel.ttf", "EBGaramond.ttf", "Cormorant.ttf"):
    _path = os.path.join(_FONTS, _file)
    if os.path.exists(_path):
        try:
            _fm.fontManager.addfont(_path)
        except Exception:  # pragma: no cover - font parsing is best effort
            pass
_HAVE = {f.name for f in _fm.fontManager.ttflist}
DISPLAY = "Cinzel" if "Cinzel" in _HAVE else "DejaVu Serif"      # titles
BODY = "EB Garamond" if "EB Garamond" in _HAVE else "DejaVu Serif"  # everything else

# --- palette -----------------------------------------------------------------
# Categorical golds/bronzes/coppers — distinguished by lightness, on purpose.
CATEGORICAL = [
    "#ffd24a", "#c9962b", "#e0a72e", "#b87333",
    "#f4e19c", "#9c7a1e", "#d99a4e", "#7a5a24",
]
# Molten ramp: bronze -> gold -> pale, used for every gradient fill.
GOLD = ["#2a1a06", "#6b4a12", "#b8860b", "#e8bf3c", "#ffe9a8"]
# Sequential (near-black -> gold) for continuous magnitude.
SEQUENTIAL = ["#0b0906", "#3a2708", "#7a5410", "#b8860b", "#e3b83a", "#ffe9a8"]
# Diverging: gold <-> ash <-> patina.
DIVERGING = ["#f0c94b", "#1a1712", "#5f8a86"]

_ONYX = dict(surface="#0b0906", page="#050403", ink="#f3e6c4", ink2="#d0b25a",
             muted="#9a8442", grid="#241d0e", axis="#4a3d1c")
_PARCHMENT = dict(surface="#f4ecd8", page="#ebe1c6", ink="#1a1408", ink2="#7a5c20",
                  muted="#94793a", grid="#dccfa8", axis="#b39a5c")

_GOLD_CMAP = LinearSegmentedColormap.from_list("jrviz_gold", GOLD)


def style(light=False):
    """Apply the jrviz theme to matplotlib rcParams; return its color roles."""
    theme = _PARCHMENT if light else _ONYX
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
        "grid.linestyle": (0, (1, 3)),
        "axes.linewidth": 1.0,
        "axes.axisbelow": True,
        "font.family": "serif",
        "font.serif": [BODY, "DejaVu Serif"],
        "font.size": 12,
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
        ax.set_title(title, fontfamily=DISPLAY, fontsize=16, color=theme["ink"],
                     loc="left", pad=16)
    if xlabel:
        ax.set_xlabel(xlabel, fontfamily=BODY, fontsize=12, labelpad=8)
    if ylabel:
        ax.set_ylabel(ylabel, fontfamily=BODY, fontsize=12, labelpad=8)
    ax.grid(axis="y", zorder=0)
    ax.grid(axis="x", visible=False)
    ax.tick_params(length=0)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(theme["axis"])
    if legend:
        leg = ax.legend(loc="upper left", bbox_to_anchor=(0, -0.14), ncol=4,
                        handlelength=1.4, fontsize=11, labelcolor=theme["ink2"])
        for txt in leg.get_texts():
            txt.set_fontfamily(BODY)
    return ax


def _grad_rects(ax, lefts, rights, heights, cmap):
    """Fill each [left, right] x [0, height] rectangle with a vertical gradient."""
    grad = np.linspace(0, 1, 256).reshape(-1, 1)
    for lo, hi, h in zip(lefts, rights, heights):
        if h <= 0:
            continue
        ax.imshow(grad, extent=(lo, hi, 0, h), origin="lower", aspect="auto",
                  cmap=cmap, vmin=0, vmax=1, zorder=3)
    ax.set_ylim(0, max(float(np.max(heights)), 1e-9) * 1.16)


def _area_gradient(ax, x, y, color, baseline):
    """Translucent vertical gradient of ``color`` clipped under the y curve."""
    top = float(np.max(y))
    if top <= baseline:
        return
    r, g, b = to_rgb(color)
    ramp = np.zeros((256, 1, 4))
    ramp[..., 0], ramp[..., 1], ramp[..., 2] = r, g, b
    ramp[..., 3] = np.linspace(0.0, 0.5, 256).reshape(-1, 1)
    im = ax.imshow(ramp, extent=(float(np.min(x)), float(np.max(x)), baseline, top),
                   origin="lower", aspect="auto", zorder=2)
    poly = np.column_stack([np.concatenate([x, x[::-1]]),
                            np.concatenate([y, np.full_like(y, baseline)])])
    clip = Polygon(poly, closed=True, facecolor="none", edgecolor="none",
                   transform=ax.transData)
    ax.add_patch(clip)
    im.set_clip_path(clip)


def bar(categories, values, *, ax=None, light=False, title=None, xlabel=None,
         ylabel=None, figsize=(7, 4.2)):
    theme = style(light)
    fig, ax = _canvas(ax, figsize)
    pos = np.arange(len(categories))
    vals = np.asarray(values, dtype=float)
    w = 0.62
    _grad_rects(ax, pos - w / 2, pos + w / 2, vals, _GOLD_CMAP)
    ax.set_xlim(pos[0] - 0.6, pos[-1] + 0.6)
    ax.set_xticks(pos, labels=categories)
    for p, v in zip(pos, vals):
        ax.text(p, v + vals.max() * 0.02, f"{v:g}", ha="center", va="bottom",
                color=theme["ink2"], fontsize=10.5, fontfamily=BODY)
    return _finish(ax, theme, title=title, xlabel=xlabel, ylabel=ylabel)


def line(x, series, *, labels=None, ax=None, light=False, title=None, xlabel=None,
          ylabel=None, figsize=(7, 4.2)):
    theme = style(light)
    fig, ax = _canvas(ax, figsize)
    x = np.asarray(x, dtype=float)
    S = np.atleast_2d(np.asarray(series, dtype=float))
    base = min(0.0, float(S.min()))
    for i, y in enumerate(S):
        c = CATEGORICAL[i % len(CATEGORICAL)]
        _area_gradient(ax, x, y, c, base)
        ax.plot(x, y, color=c, linewidth=7, alpha=0.12, solid_capstyle="round",
                zorder=3)  # glow
        ax.plot(x, y, color=c, linewidth=2.2, marker="o", markersize=5,
                markerfacecolor=c, markeredgecolor=theme["surface"],
                markeredgewidth=0.8, solid_capstyle="round", zorder=4,
                label=labels[i] if labels else None)
    return _finish(ax, theme, title=title, xlabel=xlabel, ylabel=ylabel,
                   legend=bool(labels))


def scatter(x, y, *, ax=None, light=False, title=None, xlabel=None, ylabel=None,
             color=None, size=48, figsize=(7, 4.2)):
    theme = style(light)
    fig, ax = _canvas(ax, figsize)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    ax.scatter(x, y, s=size * 3.4, color="#ffe9a8", alpha=0.10, linewidths=0,
               zorder=3)  # glow
    if color is None:
        ax.scatter(x, y, c=y, cmap=_GOLD_CMAP, s=size, edgecolor=theme["surface"],
                   linewidth=0.5, zorder=4)
    else:
        ax.scatter(x, y, color=color, s=size, edgecolor=theme["surface"],
                   linewidth=0.5, zorder=4)
    return _finish(ax, theme, title=title, xlabel=xlabel, ylabel=ylabel)


def hist(values, *, bins=20, ax=None, light=False, title=None, xlabel=None,
          ylabel=None, figsize=(7, 4.2)):
    theme = style(light)
    fig, ax = _canvas(ax, figsize)
    counts, edges = np.histogram(np.asarray(values, dtype=float), bins=bins)
    gap = np.diff(edges) * 0.04
    _grad_rects(ax, edges[:-1] + gap, edges[1:] - gap, counts.astype(float), _GOLD_CMAP)
    ax.set_xlim(edges[0], edges[-1])
    return _finish(ax, theme, title=title, xlabel=xlabel, ylabel=ylabel)


# --- triangular ornament (Deus Ex look) --------------------------------------

def ornament(ax=None, *, light=False, seed=7):
    """Apply the full triangular treatment: faceted backdrop + corner brackets.

    The one-call entry point — equivalent to ``facets(ax); corners(ax)``.
    """
    ax = facets(ax, light=light, seed=seed)
    return corners(ax, light=light)


def facets(ax=None, *, light=False, density=110, alpha=0.28, edges=True, seed=7):
    """Draw a faceted, low-poly gold triangulation behind the plotted data.

    Points are Delaunay-triangulated across the axes; each facet is shaded
    along the gold ramp as if lit from the top-left, with per-facet jitter for
    the crystalline "shattered gold" look.
    """
    ax = ax or plt.gca()
    rng = np.random.default_rng(seed)
    pts = rng.random((density, 2))
    frame = np.array([[0, 0], [1, 0], [0, 1], [1, 1],
                      [0.5, 0], [0.5, 1], [0, 0.5], [1, 0.5]])
    P = np.vstack([pts, frame])
    tri = Triangulation(P[:, 0], P[:, 1])
    verts = P[tri.triangles]                      # (ntri, 3, 2), axes coords
    cent = verts.mean(axis=1)                      # facet centroids
    shade = 0.5 * (1 - cent[:, 0]) + 0.5 * cent[:, 1]   # brighter top-left
    shade = np.clip(shade + rng.normal(0, 0.09, shade.shape), 0, 1)
    colors = _GOLD_CMAP(0.12 + 0.72 * shade)

    faces = PolyCollection(verts, facecolors=colors, edgecolors="none",
                           alpha=alpha, transform=ax.transAxes, zorder=-1)
    ax.add_collection(faces, autolim=False)
    if edges:
        wire = PolyCollection(verts, facecolors="none", edgecolors=GOLD[-1],
                              linewidths=0.55, alpha=0.22,
                              transform=ax.transAxes, zorder=-0.9)
        ax.add_collection(wire, autolim=False)
    return ax


def corners(ax=None, *, light=False, size=0.055, color=None):
    """Draw angular gold corner brackets (Deus Ex HUD framing) on the axes."""
    ax = ax or plt.gca()
    theme = _PARCHMENT if light else _ONYX
    c = color or theme["ink2"]
    s = size
    tall = s * 1.7
    tris = [
        [(0, 0), (s, 0), (0, tall)],
        [(1, 0), (1 - s, 0), (1, tall)],
        [(0, 1), (s, 1), (0, 1 - tall)],
        [(1, 1), (1 - s, 1), (1, 1 - tall)],
    ]
    for v in tris:
        ax.add_patch(Polygon(v, closed=True, facecolor=c, edgecolor="none",
                             transform=ax.transAxes, clip_on=False, zorder=6))
    return ax


def show(*args, **kwargs):
    plt.tight_layout()
    plt.show(*args, **kwargs)


def save(path, *args, **kwargs):
    plt.tight_layout()
    plt.savefig(path, dpi=180, *args, **kwargs)
