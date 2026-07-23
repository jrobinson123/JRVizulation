"""Generate one image per chart type into examples/images/.

Run from anywhere:

    python examples/gallery.py
"""
import os

import numpy as np

import jrviz as vz

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "images")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)


def save(name):
    vz.save(os.path.join(OUT, name))
    print("wrote", os.path.join("examples", "images", name))


# bar -------------------------------------------------------------------------
vz.bar(["Q1", "Q2", "Q3", "Q4"], [12, 19, 14, 22],
       title="Quarterly revenue", ylabel="$M")
save("bar.png")

# line (multi-series) ---------------------------------------------------------
x = np.arange(8)
vz.line(x, [[3, 4, 6, 5, 7, 8, 7, 9], [2, 3, 3, 4, 5, 5, 6, 7]],
        labels=["North", "South"], title="Weekly signups")
save("line.png")

# scatter (dark mode) ---------------------------------------------------------
vz.scatter(rng.normal(size=120), rng.normal(size=120),
           title="Scatter (dark)", dark=True)
save("scatter.png")

# histogram -------------------------------------------------------------------
vz.hist(rng.normal(size=800), bins=30, title="Distribution", xlabel="value")
save("hist.png")

# heatmap ---------------------------------------------------------------------
vz.heatmap(rng.random((5, 5)), row_labels=list("ABCDE"),
           col_labels=list("12345"), title="Heatmap")
save("heatmap.png")

print("done")
