"""Exact finite-N mean-field Potts + kinetic-energy reservoir benchmark.

Enumerates occupation triples modulo color permutations, integrates kinetic
energy analytically, and computes total-energy TV from Gamma/Beta CDFs.
No sampling, histogram, or two-Gaussian approximation enters the calculation.
This mean-field model has no short-range droplet/interface physics.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.special import betaln, gammainc, betainc, gammaln, logsumexp


def canonical_energies(n, beta):
    log_factorial = gammaln(np.arange(n+1)+1)
    energies, log_weights = [], []
    for n1 in range((n+2)//3,n+1):
        n2 = np.arange((n-n1+1)//2,min(n1,n-n1)+1)
        n3 = n-n1-n2
        perm = np.where((n1==n2)&(n2==n3),1,np.where((n1==n2)|(n2==n3),3,6))
        sq = n1*n1+n2*n2+n3*n3
        log_weight = (log_factorial[n]-log_factorial[n1]-log_factorial[n2]
                      -log_factorial[n3]+np.log(perm)+beta*sq/(2*n))
        energies.append(sq)
        log_weights.append(log_weight)
    squared_sum = np.concatenate(energies)
    log_weights = np.concatenate(log_weights)
    log_partition = logsumexp(log_weights)
    weights = np.exp(log_weights-log_partition)
    sq, inverse = np.unique(squared_sum, return_inverse=True)
    weights = np.bincount(inverse,weights=weights,minlength=len(sq))
    keep = weights > 0
    return -sq[keep]/(2*n), weights[keep], float(log_partition), len(squared_sum)


def finite_bath(n, potential, prior, beta, c, kinetic_per_site=.5):
    shape = kinetic_per_site*n
    phase_minus = -n/4+shape/beta
    phase_plus = -n/6+shape/beta
    delta = phase_plus-phase_minus
    bath_at_ref = delta/(-np.expm1(-beta*delta/c))
    total_energy = phase_minus+bath_at_ref
    # Integrate K~Gamma(shape,beta) against exp(h(U+K)-h(E_ref)).
    available = total_energy-potential
    log_z_cond = np.full_like(potential,-np.inf)
    allowed = available > 0
    shift = phase_minus-potential[allowed]
    log_const = shape*np.log(beta*bath_at_ref)+betaln(shape,c+1)-gammaln(shape)
    log_z_cond[allowed] = (-beta*shift+log_const
                          +(shape+c)*np.log1p(shift/bath_at_ref))
    log_post = np.log(prior)+log_z_cond
    log_z = logsumexp(log_post)
    posterior = np.exp(log_post-log_z)
    assert abs(posterior.sum()-1)<2e-9

    def log_ratio(e):
        shift_e = e-phase_minus
        if shift_e >= bath_at_ref:
            return -np.inf
        return beta*shift_e+c*np.log1p(-shift_e/bath_at_ref)-log_z

    maximum = total_energy-c/beta
    assert log_ratio(maximum)>0, (n,c,log_ratio(maximum))
    # Any underflowed canonical orbit has mass below the smallest normal
    # float. Bound its possible revival using the global likelihood maximum.
    log_omitted_posterior_bound = (np.log((n+1)*(n+2)/2)
                                   +np.log(np.finfo(float).tiny)+log_ratio(maximum))
    if log_omitted_posterior_bound > np.log(1e-12):
        raise ValueError("Reweighting may revive underflowed classes; use log-space aggregation.")
    step = delta+20*np.sqrt(n)
    left = maximum-step
    while log_ratio(left)>0:
        step*=2
        left=maximum-step
    # The upper root lies below the finite bath cutoff.
    upper_bracket=maximum+.99*(total_energy-maximum)
    while log_ratio(upper_bracket)>0:
        next_bracket=total_energy-.01*(total_energy-upper_bracket)
        if next_bracket >= total_energy:
            next_bracket=np.nextafter(total_energy,-np.inf)
        if next_bracket <= upper_bracket:
            raise ValueError("Upper likelihood crossing is too close to bath cutoff for float64.")
        upper_bracket=next_bracket
    left_root=brentq(log_ratio,left,maximum,xtol=1e-9)
    right_root=brentq(log_ratio,maximum,upper_bracket,xtol=1e-9)

    def canonical_cdf(e):
        return np.dot(prior,gammainc(shape,beta*np.maximum(e-potential,0)))

    def bath_cdf(e):
        fraction=np.clip((e-potential[allowed])/available[allowed],0,1)
        return np.dot(posterior[allowed],betainc(shape,c+1,fraction))

    tv = ((bath_cdf(right_root)-bath_cdf(left_root))
          -(canonical_cdf(right_root)-canonical_cdf(left_root)))
    assert -2e-8 <= tv <= 1+2e-8
    ordered = potential < (-n/4-n/6)/2
    return {"n":n,"bath_heat_capacity":float(c),"c_over_n_3_2":float(c/n**1.5),
            "total_energy":float(total_energy),"energy_tv":float(tv),
            "config_tv":float(.5*np.sum(np.abs(posterior-prior))),
            "canonical_ordered_probability":float(prior[ordered].sum()),
            "bath_ordered_probability":float(posterior[ordered].sum()),
            "likelihood_interval":[float(left_root),float(right_root)],
            "log_normalization":float(log_z),"kinetic_gamma_shape":float(shape),
            "log_upper_bound_underflowed_posterior_mass":float(log_omitted_posterior_bound)}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--sizes",type=int,nargs="+",default=[300,1000,3000,6000])
    args=parser.parse_args()
    beta=4*np.log(2)
    results=[]
    for n in args.sizes:
        potential,prior,logpart,count=canonical_energies(n,beta)
        print(f"N={n}: {count} occupation orbits, {len(prior)} distinct energies",flush=True)
        for label,c in [("boundary_small",.5*n**1.5),("boundary_large",2*n**1.5),
                        ("faster_bath",n**1.75),("slower_bath",n**1.25)]:
            result=finite_bath(n,potential,prior,beta,c)
            result.update(regime=label,canonical_config_log_partition=logpart)
            results.append(result)
            print(json.dumps(result),flush=True)
    output=Path(__file__).with_name("potts-finite-bath-results.json")
    output.write_text(json.dumps(results,indent=2)+"\n")


if __name__=="__main__":
    main()
