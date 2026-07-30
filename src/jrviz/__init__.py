"""jrviz — a black-and-gold, gradient charting layer over matplotlib.

    import jrviz as vz
    vz.bar(["A", "B", "C"], [3, 7, 5], title="Widgets sold")
    vz.show()
"""
from .core import (
    bar, line, scatter, hist, style, show, save,
    ornament, facets, corners,
    CATEGORICAL, SEQUENTIAL, DIVERGING,
)

__version__ = "0.1.0"

__all__ = [
    "bar", "line", "scatter", "hist", "style", "show", "save",
    "ornament", "facets", "corners",
    "CATEGORICAL", "SEQUENTIAL", "DIVERGING",
]
