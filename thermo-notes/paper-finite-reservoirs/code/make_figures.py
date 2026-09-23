"""Regenerate manuscript figures from archived exact sums and proved formulas."""
from pathlib import Path
import json
import numpy as np
from scipy.special import ndtr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/"figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,
                     "pdf.fonttype":42,"ps.fonttype":42})

def phase_tv(weights, variances, slope):
    scores=.5*slope*slope*np.asarray(variances)
    shifted=np.asarray(weights)*np.exp(scores-scores.max())
    shifted/=shifted.sum()
    value=0.
    for w,r,v in zip(weights,shifted,variances):
        d=abs(slope)*np.sqrt(v)
        if d==0:
            value+=max(r-w,0)
        else:
            a=np.log(r/w)/d
            value+=r*ndtr(a+d/2)-w*ndtr(a-d/2)
    return float(value)

def main():
    data=json.loads((ROOT/"data"/"potts-finite-bath-results.json").read_text())
    beta=4*np.log(2)
    ratio=np.sqrt(2*(3-beta)/(6-beta))
    weights=np.array([3*ratio,1])/(1+3*ratio)
    variances=np.array([.5/beta**2+1/(6*(3-beta)),.5/beta**2])
    fig,ax=plt.subplots(figsize=(6.7,3.7),layout="constrained")
    specs=[("slower_bath",r"$c=N^{5/4}$",None,"#AA3377"),
           ("boundary_small",r"$c=0.5N^{3/2}$",.5,"#EE7733"),
           ("boundary_large",r"$c=2N^{3/2}$",2.,"#0077BB"),
           ("faster_bath",r"$c=N^{7/4}$",None,"#009988")]
    limits={}
    for regime,label,gamma,color in specs:
        rows=sorted((r for r in data if r["regime"]==regime),key=lambda r:r["n"])
        ax.loglog([r["n"] for r in rows],[r["energy_tv"] for r in rows],
                  "o-",label=label,color=color,ms=4)
        if gamma is not None:
            limit=phase_tv(weights,variances,beta**2/(24*gamma))
            limits[str(gamma)]=limit
            ax.axhline(limit,color=color,linestyle=":",linewidth=1.3)
    ax.set(xlabel=r"Number of spins $N$",ylabel="Full-state total-variation error")
    ax.grid(True,which="major",alpha=.2)
    ax.legend(ncol=4,fontsize=9,loc="lower left",bbox_to_anchor=(0,1.01),frameon=False,handlelength=1.5,columnspacing=1)
    fig.savefig(FIG/"potts-scaling.pdf")
    fig.savefig(FIG/"potts-scaling.png",dpi=180)
    plt.close(fig)

    x=np.linspace(0,4,801)
    balanced=2*ndtr(x/2)-1
    optimized=np.minimum(balanced,.5)
    fig,ax=plt.subplots(figsize=(6.7,3.25),layout="constrained")
    ax.plot(x,balanced,label="Retain both phase weights",color="#0077BB",linewidth=2)
    ax.plot(x,optimized,label="Optimize over composite energy",color="#EE7733",
            linewidth=2,linestyle="--")
    ax.axhline(.5,color=".5",linewidth=.8,linestyle=":")
    crossing=1.3489795003921634
    ax.axvline(crossing,color=".6",linewidth=.8,linestyle=":")
    ax.text(crossing+.07,.07,r"$\lambda_*=2\Phi^{-1}(3/4)$",fontsize=9)
    ax.set(xlabel=r"Standardized boundary tilt $\lambda=b\sqrt{v}$",
           ylabel="Limiting full-state TV",xlim=(0,4),ylim=(0,1))
    ax.legend(fontsize=9,loc="lower right")
    ax.grid(True,alpha=.15)
    fig.savefig(FIG/"boundary-optimization.pdf")
    fig.savefig(FIG/"boundary-optimization.png",dpi=180)
    plt.close(fig)
    (ROOT/"data"/"figure-derived-values.json").write_text(
        json.dumps({"mean_field_beta":beta,"mean_field_weights":weights.tolist(),
                    "mean_field_variances":variances.tolist(),
                    "secant_boundary_tv_limits":limits,
                    "balanced_boundary_optimizer_crossing":crossing},indent=2)+"\n")
    np.savetxt(ROOT/"data"/"boundary-optimization.csv",
               np.column_stack((x,balanced,optimized)),delimiter=",",
               header="standardized_tilt,retained_weights_tv,optimized_tv",comments="")
    print(json.dumps(limits,indent=2))

if __name__=="__main__":
    main()
