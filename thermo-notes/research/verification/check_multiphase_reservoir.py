"""Exact Gaussian-mixture checks for finite-reservoir phase loss.

Deterministic quadrature, not a proof or a molecular-fluid simulation.
Run: python research/verification/check_multiphase_reservoir.py
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import quad
from scipy.special import softmax
from scipy.stats import norm


def transformed(n, kappa, z, weights):
    e = np.array([-1., 0., 1.])
    factor = 1 + kappa*n
    alpha = kappa*n*n/factor
    t = z*factor/n
    means = (n*e+t*n)/factor
    std = np.sqrt(n/factor)
    v = softmax(np.log(weights)+z*e-alpha*e*e/2)
    return means, std, v, alpha


def tv(n, kappa, z, weights):
    means0 = n*np.array([-1., 0., 1.])
    s0 = np.sqrt(n)
    means1, s1, v, alpha = transformed(n, kappa, z, weights)
    intervals = sorted([(m-11*s, m+11*s) for mm, s in [(means0,s0),(means1,s1)] for m in mm])
    merged=[]
    for left,right in intervals:
        if merged and left <= merged[-1][1]:
            merged[-1][1]=max(merged[-1][1],right)
        else:
            merged.append([left,right])
    result=0.
    for left,right in merged:
        center=(left+right)/2
        def integrand(u):
            value=center+s0*u
            p=np.dot(weights,norm.pdf((value-means0)/s0))
            q=np.dot(v,norm.pdf((value-means1)/s1))*s0/s1
            return abs(p-q)/2
        result += quad(integrand,(left-center)/s0,(right-center)/s0,
                       epsabs=2e-9,limit=300)[0]
    invariant=(np.log(v[0]/weights[0])+np.log(v[2]/weights[2])
               -2*np.log(v[1]/weights[1]))
    assert abs(invariant+alpha)<1e-9
    return float(result),v.tolist()


def main():
    results=[]
    for weights in [np.ones(3)/3,np.array([.1,.6,.3])]:
        for n in [1e2,1e4,1e6,1e8,1e10]:
            kappa=n**-1.75
            alpha=kappa*n*n/(1+kappa*n)
            left,left_weights=tv(n,kappa,-alpha/2,weights)
            center,center_weights=tv(n,kappa,0,weights)
            right,right_weights=tv(n,kappa,alpha/2,weights)
            row={"n":n,"kappa":kappa,"alpha":alpha,"reference_weights":weights.tolist(),
                 "balanced_tv":center,"retain_left_pair_tv":left,"retain_right_pair_tv":right,
                 "right_pair_weights":right_weights,
                 "predicted_optimal_limit":float(min(weights[0],weights[2]))}
            results.append(row)
            print(json.dumps(row),flush=True)
    path=Path(__file__).with_name("multiphase-reservoir-results.json")
    path.write_text(json.dumps(results,indent=2)+"\n")


if __name__=="__main__":
    main()
