#!/usr/bin/env python3
"""Present archived SCIP counts; no solver imports or calls. Requires matplotlib."""
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "archive/research-20260928b/bb-complexity/solver-validation/results/runs.jsonl"
FITS = json.loads(SOURCE.with_name("runs_fits.json").read_text())
ROWS = [dict(json.loads(line), source_line=n) for n, line in enumerate(SOURCE.read_text().splitlines(), 1)]
COLORS = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#332288"]
PANELS = [
    ("(a) Optimal sets: model setting", [(i, "model", "-") for i in
        ("ring2", "mccdiag2", "conexp2", "sphere3", "plane3", "conexp4")]),
    ("(b) Flat growth: model setting", [(i, "model", "-") for i in
        ("qflat1", "qflat2a", "qflat2b", "qflat3")]),
    ("(c) Isolated minima: model and default", [(i, s, "-" if s == "model" else "--")
        for i in ("iso2", "iso3", "iso4") for s in ("model", "default")
        if (i, s) != ("iso4", "default")]),
    ("(d) Face alignment: branching settings", [("mccaxis2", s, "-") for s in
        ("lppoint", "xprioexttoy", "exttoy", "default")]),
]


def main():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
        "axes.titlesize": 10, "axes.labelsize": 10, "legend.fontsize": 7.6,
        "pdf.fonttype": 42, "ps.fonttype": 42, "axes.spines.top": False,
        "axes.spines.right": False, "lines.linewidth": 1.4})
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 7.9), constrained_layout=True)
    metadata = dict(source=str(SOURCE.relative_to(HERE)),
        source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        presentation_tools=dict(matplotlib=matplotlib.__version__, numpy=np.__version__),
        presentation="individual archived records; no pooling or averaging",
        plotted_filter="selected exact instance and setting; status != error; includes marked limit and optimal records",
        archived_fit_filter="reject nodelimit/timelimit/error; retain optimal; tail=last five available eps<=1e-3; wide=all eps<=1e-2; minimum three points and 0.99 log10 tolerance span",
        references="arbitrarily normalized theorem rates, not absolute bounds or fitted model curves",
        panels=[])
    for j, (ax, (title, curves)) in enumerate(zip(axes.flat, PANELS)):
        ax.set_title(title, loc="left", pad=57)
        panel = dict(title=title, tolerance_axis="logarithmic, decreasing",
                     node_axis="linear" if j == 2 else "logarithmic", curves=[])
        for k, (inst, setting, linestyle) in enumerate(curves):
            data = sorted([r for r in ROWS if r["inst"] == inst and r["setting"] == setting
                and r["status"] != "error"], key=lambda r: r["eps"], reverse=True)
            color = COLORS[k // 2 if j == 2 else k]
            fit = FITS[f"{inst}|{setting}"]
            if j in (0, 1):
                value = fit["tail"] if fit["tail"] is not None else fit["wide"]
                kind = "tail" if fit["tail"] is not None else "wide"
                label = f"{inst} ({kind} {value:.2f})"
            elif j == 2:
                label = f"{inst}, {setting}"
            else:
                label = {"lppoint": "LP point (clamp 0.2)", "xprioexttoy": "x-priority bisection",
                         "exttoy": "external bisection", "default": "default"}[setting]
            ax.plot([r["eps"] for r in data], [r["nodes"] for r in data], linestyle,
                    color=color, marker="o", markersize=2.8, label=label)
            optimal = [r for r in data if r["status"] == "optimal"]
            limited = [r for r in data if r["status"] in {"nodelimit", "timelimit"}]
            ax.scatter([r["eps"] for r in optimal], [r["nodes"] for r in optimal],
                       facecolors="white", edgecolors=color, marker="s", s=19, linewidths=0.9, zorder=4)
            ax.scatter([r["eps"] for r in limited], [r["nodes"] for r in limited],
                       color=color, marker="^", s=26, zorder=4)
            panel["curves"].append(dict(instance=inst, setting=setting, archived_fit=fit,
                records=[{key:r[key] for key in ("source_line", "eps", "nodes", "status")} for r in data]))
        # Rate guides are separate from all data curves and fit calculations.
        if j == 0:
            ax.plot([1e-2, 1e-5], [100, 100 * 10 ** 1.5], ":", color="0.25", linewidth=1.2)
            ax.text(2e-5, 5200, r"$\varepsilon^{-1/2}$", color="0.25")
            ax.plot([1e-1, 1e-4], [25, 25000], ":", color="0.5", linewidth=1.2)
            ax.text(5e-4, 6000, r"$\varepsilon^{-1}$", color="0.4")
        elif j == 1:
            e = np.logspace(-2, -7, 60)
            ax.plot(e, 13 * (1e-2 / e) ** 0.25, ":", color="0.3", linewidth=1.2)
            ax.text(3e-6, 135, r"$\varepsilon^{-1/4}$", color="0.3")
            ax.plot(e, 230 * (1e-2 / e) ** 0.5, ":", color="0.5", linewidth=1.2)
            ax.text(1e-6, 33000, r"$\varepsilon^{-1/2}$", color="0.4")
        elif j == 2:
            ax.text(0.03, 0.97, r"Theory: $\Theta(\log(1/\varepsilon))$", transform=ax.transAxes,
                    va="top", fontsize=8, color="0.25")
        else:
            ax.text(0.03, 0.97, "Rule-dependent; all curves are mccaxis2", transform=ax.transAxes,
                    va="top", fontsize=7.8, color="0.25")
        ax.set_xscale("log")
        ax.set_yscale("linear" if j == 2 else "log")
        ax.set_xlim(0.13, 7e-8)
        ax.set_xticks([1e-1, 1e-3, 1e-5, 1e-7])
        ax.set_xlabel(r"Absolute-gap tolerance $\varepsilon$ (decreasing)")
        ax.set_ylabel("Processed nodes")
        ax.grid(which="major", color="0.88", linewidth=0.6)
        ax.tick_params(which="minor", length=2)
        ax.legend(loc="lower left", bbox_to_anchor=(0, 1.01), borderaxespad=0,
                  frameon=False, ncol=2)
        if j in (0, 1):ax.set_ylim(1, 2.0e5)
        if j == 2:ax.set_ylim(0, 760)
        if j == 3:ax.set_ylim(1, 3e4)
        metadata["panels"].append(panel)
    fig.suptitle("Archived SCIP 10.0.2 node counts", fontsize=12)
    fig.supxlabel("Open squares: exhausted tree (optimal). Triangles: node limit. Dotted curves: rate guides.",
                  fontsize=8)
    output = HERE / "presentation"
    output.mkdir(exist_ok=True)
    figure_dir = HERE.parent / "figures"
    figure_dir.mkdir(exist_ok=True)
    for suffix in ("pdf", "png"):
        path = output / f"node-scaling.{suffix}"
        kwargs = {"dpi": 300} if suffix == "png" else {"metadata": {"CreationDate": None, "ModDate": None,
            "Title": "Archived SCIP node scaling", "Creator": "plot_node_scaling.py; archived records only"}}
        fig.savefig(path, **kwargs)
        (figure_dir / path.name).write_bytes(path.read_bytes())
    (output / "figure-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    plt.close(fig)
    print("Wrote archived-record node-scaling.pdf, node-scaling.png, and figure-metadata.json")


if __name__ == "__main__":
    main()
