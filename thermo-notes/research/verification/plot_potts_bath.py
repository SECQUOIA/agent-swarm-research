"""Plot exact finite-N reservoir data and independently derived limits."""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad
from scipy.stats import norm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


HERE=Path(__file__).resolve().parent


def asymptotic_tv(gamma):
    beta=4*np.log(2)
    ratio=np.sqrt(2*(3-beta)/(6-beta))
    weights=np.array([3*ratio,1])/(1+3*ratio)
    variances=np.array([.5/beta**2+1/(6*(3-beta)),.5/beta**2])
    slope=beta**2/(24*gamma)
    shifted_weights=weights*np.exp(slope**2*variances/2)
    shifted_weights/=shifted_weights.sum()
    means=np.array([slope,-slope])*variances
    distance=0.
    for i in range(2):
        distance+=quad(lambda z: .5*abs(weights[i]*norm.pdf(z,scale=np.sqrt(variances[i]))
                         -shifted_weights[i]*norm.pdf(z,loc=means[i],scale=np.sqrt(variances[i]))),
                         -np.inf,np.inf,epsabs=1e-10)[0]
    return distance


def main():
    data=json.loads((HERE/"potts-finite-bath-results.json").read_text())
    fig,ax=plt.subplots(figsize=(6.6,4.3),constrained_layout=True)
    specs=[("slower_bath",r"$c=N^{5/4}$",None),
           ("boundary_small",r"$c=0.5N^{3/2}$",.5),
           ("boundary_large",r"$c=2N^{3/2}$",2),
           ("faster_bath",r"$c=N^{7/4}$",None)]
    for label,legend,gamma in specs:
        rows=sorted([r for r in data if r["regime"]==label],key=lambda r:r["n"])
        line,=ax.loglog([r["n"] for r in rows],[r["energy_tv"] for r in rows],"o-",label=legend)
        if gamma:
            ax.axhline(asymptotic_tv(gamma),color=line.get_color(),linestyle=":",alpha=.65)
    ax.set(xlabel="Number of Potts spins N",ylabel="Total-variation error of subsystem law",
           title="A bath larger than the system can retain a finite error")
    ax.legend(fontsize=9)
    ax.grid(True,which="major",alpha=.15)
    ax.text(.02,.03,"Exact sums; calibrated physical bath\nDotted lines: limits at the boundary scale",
            transform=ax.transAxes,fontsize=8)
    for extension in ("png","pdf"):
        fig.savefig(HERE/f"potts-bath-scaling.{extension}",dpi=200)


if __name__=="__main__":
    main()
