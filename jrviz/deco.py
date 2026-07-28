"""Deus Ex-flavored triangular ornament — an opt-in decorative layer.

    ax = vz.bar(["A", "B", "C"], [3, 7, 5], title="Augmented")
    vz.ornament(ax)   # faceted low-poly gold backdrop + angular HUD corners

``ornament`` is the one-call entry point; ``facets`` and ``corners`` are the
individual pieces it composes. All three draw onto an existing axes (default:
the current one) and return it, so they layer onto any jrviz chart.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
from matplotlib.collections import PolyCollection
from matplotlib.patches import Polygon

from .charts import _GOLD_CMAP, GOLD, _ONYX, _PARCHMENT


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
