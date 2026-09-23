"""Reproduce the manuscript's finite-volume evidence; no continuum certificate.

Run from any directory with OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1.
Only NumPy, SciPy and Matplotlib are required. Root solvers are imported by
resolved path; output belongs to this manuscript. --plots reuses saved data.
"""
import argparse
import json
import os
from importlib.metadata import version
from pathlib import Path
import platform
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parent / "scripts"))
import numpy as np
import scipy
from numpy.polynomial.legendre import leggauss
from scipy.linalg import solve_banded
from scipy.optimize import minimize
from scipy.special import beta, gamma
from check_robust_design import inverse_integral, adaptive_trial
from check_risk_sensitive_design import graded_design


def circle(budget, order=1., n=32768, nq=48):
    """Midpoint reaction, face conductivities, reflecting half-wall ends.

    Every sampled field is normalized to the SAME discrete mass 2 dx sum D=M.
    The full circle response is twice the half-wall response. Symmetry in c
    gives expectation (1/2) integral_0^2. nq is per subdivision, not total.
    """
    dx = np.pi/n
    faces = np.arange(1, n)*dx
    uniform = np.full(n-1, budget/(2*np.pi))
    if order == 1:
        trial = np.sin(faces)**(-.4)
        radius = budget**(1/7)
    else:
        trial, radius, _ = graded_design(budget, order, faces)
    norm = lambda d: d*(budget/(2*dx*np.sum(d)))
    uniform, trial = norm(uniform), norm(trial)
    breaks = [0, .5, .9, 1, 1.1, 1.5, 2]
    for width in [radius**2, (budget/(4*np.pi))**(1/3), budget**(2/7)]:
        for multiplier in [.1, 1, 10, 100]:
            breaks += [1-width*multiplier, 1+width*multiplier]
    breaks = np.unique(np.clip(breaks, 0, 2))
    nodes, weights = leggauss(nq)
    total = np.zeros(3 if order == 1 else 2)
    for lo, hi in zip(breaks[:-1], breaks[1:]):
        for c, weight in zip((lo+hi)/2+(hi-lo)*nodes/2, weights):
            fields = [uniform, trial]
            if order == 1:
                fields.append(norm(adaptive_trial(c, budget, faces, dx)))
            total += (hi-lo)*weight/4*np.array([
                inverse_integral(c, field, n)**order for field in fields])
    scale = (budget**(order/4) if order < 1.6 else
             budget**.4/np.log(1/budget)**1.4 if order == 1.6 else
             budget**((3*order-2)/7))
    row = dict(M=budget, q=order, cells_half=n, nodes_per_interval=nq,
               quadrature_intervals=len(breaks)-1, breaks=breaks.tolist(),
               uniform=float(total[0]), trial=float(total[1]),
               trial_ratio=float(total[1]/total[0]),
               scaled_trial=float(total[1]*scale))
    if order == 1:
        row.update(adaptive_trial=float(total[2]),
                   adaptive_to_predetermined=float(total[2]/total[1]))
    return row


def center_objective(width, n, nq, extent):
    dx = 2*extent/n
    x = -extent+(np.arange(n)+.5)*dx
    if width:
        z, w = leggauss(nq)
        centers, weights = width*z/2, w/2
        outside = 2/width*np.log((extent+width/2)/(extent-width/2))
    else:
        centers, weights, outside = np.array([0.]), np.array([1.]), 2/extent
    assert extent > width/2
    potentials = [(x-z)**2 for z in centers]

    def objective(masses):
        conductance = masses/dx**3
        band = np.zeros((3, n))
        band[0, 1:] = band[2, :-1] = -conductance
        value, gradient = outside, np.zeros(n-1)
        for potential, weight in zip(potentials, weights):
            band[1] = potential
            band[1, :-1] += conductance
            band[1, 1:] += conductance
            h = solve_banded((1, 1), band, np.ones(n))
            value += weight*dx*np.sum(h)
            gradient -= weight*(np.diff(h)/dx)**2
        return float(value), gradient
    return objective


def center(width, n=400, nq=96, extent=None):
    extent = 6+width/2 if extent is None else extent
    objective = center_objective(width, n, nq, extent)
    start = np.full(n-1, 1/(n-1))
    opt = minimize(objective, start, jac=True, method="SLSQP",
                   bounds=[(0, None)]*(n-1),
                   constraints={"type": "eq", "fun": lambda x: x.sum()-1,
                                "jac": lambda x: np.ones_like(x)},
                   options={"ftol": 2e-9, "maxiter": 600})
    # Project negligible floating feasibility error before the certificate.
    masses = np.maximum(opt.x, 0)
    masses /= masses.sum()
    value, gradient = objective(masses)
    gap = float(gradient@masses-min(gradient))
    validation, _ = center_objective(width, n, max(384, 2*nq), extent)(masses)
    dx = 2*extent/n
    return dict(eta=width, cells=n, nodes=nq if width else 1, extent=extent,
                value=value, lower=value-gap, gap=gap,
                validation_nodes=max(384, 2*nq) if width else 1,
                validation_value=validation,
                quadrature_change=validation/value-1,
                success=bool(opt.success), message=opt.message,
                iterations=opt.nit, mass_error=float(masses.sum()-1),
                positions=(-extent+np.arange(1,n)*dx).tolist(),
                mobility=(masses/dx).tolist())


def save_progress(data):
    (HERE/"data"/"numerical-evidence.json").write_text(json.dumps(data, indent=2)+"\n")


def run():
    data = dict(versions=dict(python=platform.python_version(), numpy=np.__version__,
                             scipy=scipy.__version__, matplotlib=version("matplotlib")), circle=[], refinements=[],
                center=[], center_refinements=[])
    for q in [1., 1.6, 3.]:
        for m in ([1e-3, 1e-6, 1e-9] if q == 1 else [1e-3,1e-6,1e-9,1e-12]):
            row = circle(m, q)
            data["circle"].append(row)
            save_progress(data)
            print(json.dumps(row), flush=True)
    for q, m in [(1.,1e-9),(1.6,1e-12),(3.,1e-12)]:
        for n,nq in [(65536,48),(32768,96),(65536,96)]:
            row = circle(m,q,n,nq)
            data["refinements"].append(row)
            save_progress(data)
            print(json.dumps(row), flush=True)
    for eta in [0.,2.,8.,32.]:
        row = center(eta,400,192 if eta == 32 else 96)
        data["center"].append(row)
        save_progress(data)
        print(json.dumps({k:v for k,v in row.items() if k not in ["positions","mobility"]}),flush=True)
    for args in [(0.,200,96,None),(2.,200,96,None),(32.,200,192,None),
                 (32.,600,192,33.),(32.,200,24,None)]:
        row = center(*args)
        data["center_refinements"].append(row)
        save_progress(data)
        print(json.dumps({k:v for k,v in row.items() if k not in ["positions","mobility"]}),flush=True)
    return data


def plots(data):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
    c0=np.pi/2*gamma(.25)/gamma(.75)
    cpl=12*(3/80)**.2
    kcrit=(2*c0)**1.6/8*(4/7)**1.4
    kuniform=c0*c0/np.sqrt(np.pi)*(2*np.pi)**.25
    kblind=2**(-2)*c0*(2*beta(.3,.5))**1.25
    fig=plt.figure(figsize=(7.2,5.3),layout="constrained")
    grid=fig.add_gridspec(2,2)
    ax=[fig.add_subplot(grid[0,0]),fig.add_subplot(grid[0,1]),fig.add_subplot(grid[1,:])]
    rows=[r for r in data["circle"] if r["q"]==1]
    ax[0].semilogx([r["M"] for r in rows],[r["trial_ratio"] for r in rows],"o-",label="Predetermined trial / uniform")
    ax[0].axhline(1,color=".7",ls=":")
    ax[0].axhline(kblind/kuniform,color=".4",ls="--",label="Asymptotic optimum ratio")
    ax[0].set(title="(a) Mean: a small asymptotic gain",ylabel="Mean response ratio")
    rows=[r for r in data["circle"] if r["q"]==3]
    ax[1].loglog([r["M"] for r in rows],[r["trial_ratio"] for r in rows],"o-",color="#34845d",label="Graded trial / uniform")
    ax[1].set(title="(b) Third moment",ylabel="Third-moment ratio")
    rows=[r for r in data["circle"] if r["q"]==1.6]
    ax[2].semilogx([r["M"] for r in rows],[r["scaled_trial"] for r in rows],"o-",color="#7a5195",label="Explicit critical trial")
    ax[2].axhline(kcrit,color=".4",ls="--",label="Proved optimal coefficient")
    ax[2].set(title="(c) Slow critical convergence",ylabel=r"$M^{2/5}\,\mathbb{E}J^{8/5}/[\log(1/M)]^{7/5}$")
    for a in ax:
        a.set_xlabel("Dimensionless budget $M$"); a.invert_xaxis();a.grid(alpha=.15);a.legend(fontsize=8,frameon=False)
    fig.savefig(HERE/"figures"/"moment-designs.pdf")
    plt.close(fig)
    fig,ax=plt.subplots(1,2,figsize=(9,3.6),layout="constrained")
    rows=data["center"]
    for r in rows:
        if r["eta"] in [0.,2.,8.]:
            ax[0].plot(r["positions"],r["mobility"],label=rf"$\eta={r['eta']:g}$")
    ax[0].set(xlim=(-7,7),xlabel="Local position $x$",ylabel="Face mobility density",title="(a) Discrete optimized profiles")
    eta=np.linspace(0,32,300)
    ax[1].plot(eta,np.maximum(cpl,c0*eta**.25),"--",color=".4",label="Proved continuum lower bound")
    ax[1].plot([r["eta"] for r in rows],[r["value"] for r in rows],"o",label="400-cell discrete values")
    ax[1].set(xlabel=r"Center uncertainty width $\eta$",ylabel="Local response",title="(b) Local uncertain-center value")
    for a in ax:a.grid(alpha=.15);a.legend(frameon=False,fontsize=8)
    fig.savefig(HERE/"figures"/"uncertain-center.pdf")
    plt.close(fig)
    center_lines = []
    for r in data["center"]:
        center_lines.append(f"{r['eta']:g} & {r['value']:.6f} & {r['lower']:.6f} & {r['gap']:.2g} " + r"\\")
    (HERE/"data"/"center-table.tex").write_text("\n".join(center_lines)+"\n"+r"\bottomrule"+"\n")
    mean_lines = []
    for r in data["circle"]:
        if r["q"] == 1:
            power=int(round(np.log10(r["M"])))
            mean_lines.append(f"$10^{{{power}}}$ & {r['trial_ratio']:.4f} & {r['adaptive_to_predetermined']:.4f} " + r"\\")
    (HERE/"data"/"mean-table.tex").write_text("\n".join(mean_lines)+"\n"+r"\bottomrule"+"\n")


if __name__ == "__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--plots",action="store_true")
    args=parser.parse_args()
    data=json.loads((HERE/"data"/"numerical-evidence.json").read_text()) if args.plots else run()
    plots(data)
