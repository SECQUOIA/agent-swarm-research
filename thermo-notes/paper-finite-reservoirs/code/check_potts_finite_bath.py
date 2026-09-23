"""Independent checks: explicit spin enumeration and direct energy quadrature."""
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.integrate import quad
from scipy.special import gammaln, logsumexp
from scipy.stats import gamma, beta as beta_distribution
from potts_finite_bath import canonical_energies, finite_bath
from potts_phase_statistics import phase_statistics


def explicit_spin_checks():
    beta=4*np.log(2)
    rows=[]
    for n in range(1,9):
        # Enumerate all 3^N labeled spin states, not occupation orbits.
        energies=[]
        ordered_states=[]
        # Six times each minimum makes squared Voronoi distances integral.
        minima=np.array([[2,2,2],[4,1,1],[1,4,1],[1,1,4]])
        for spins in product(range(3),repeat=n):
            occupation=np.bincount(spins,minlength=3)
            energies.append(-np.dot(occupation,occupation)/(2*n))
            distances=np.sum((6*occupation-n*minima)**2,axis=1)
            ordered_states.append(distances[1:].min()<=distances[0])
        energies=np.asarray(energies)
        exact_logz=logsumexp(-beta*energies)
        spins_prior=np.exp(-beta*energies-exact_logz)
        potential,prior,logz,orbits=canonical_energies(n,beta)
        error=max(abs(weight-spins_prior[energies==energy].sum())
                  for energy,weight in zip(potential,prior))
        assert error<2e-13 and abs(logz-exact_logz)<2e-13
        # Check Voronoi statistics independently of the maximum-occupation rule.
        ordered_states=np.asarray(ordered_states)
        ordered_probability=spins_prior[ordered_states].sum()
        conditional=spins_prior[ordered_states]/ordered_probability
        phase_energies=energies[ordered_states]
        phase_mean=np.dot(conditional,phase_energies)
        variance_per_spin=np.dot(conditional,(phase_energies-phase_mean)**2)/n
        statistics=phase_statistics(n)
        probability_error=abs(statistics['ordered_probability']-ordered_probability)
        variance_error=abs(statistics['ordered_variance_per_spin']-variance_per_spin)
        assert probability_error<2e-13 and variance_error<2e-13
        # Independent beta-integral configuration weights for the physical bath.
        c=10*n**1.5
        result=finite_bath(n,potential,prior,beta,c)
        shape=n/2
        spin_post=np.exp((shape+c)*np.log(result['total_energy']-energies)
                         -logsumexp((shape+c)*np.log(result['total_energy']-energies)))
        expected_tv=.5*abs(spin_post-spins_prior).sum()
        expected_ordered=spin_post[energies<(-n/4-n/6)/2].sum()
        assert abs(expected_tv-result['config_tv'])<2e-12
        assert abs(expected_ordered-result['bath_ordered_probability'])<2e-12
        rows.append(dict(n=n,labeled_states=3**n,orbits=orbits,max_energy_mass_error=float(error),
                         voronoi_probability_error=float(probability_error),
                         voronoi_variance_per_spin_error=float(variance_error)))
    return rows


def direct_density_check(n=12,shape=12.,capacity=50.):
    beta=4*np.log(2)
    # Enumerate all labeled-color occupation triples without orbit reduction.
    ns=np.asarray([(i,j,n-i-j) for i in range(n+1) for j in range(n-i+1)])
    U=-np.sum(ns**2,axis=1)/(2*n)
    log_m=gammaln(n+1)-np.sum(gammaln(ns+1),axis=1)
    em=-n/4+shape/beta; ep=-n/6+shape/beta
    total=em+(ep-em)/(-np.expm1(-beta*(ep-em)/capacity))
    available=total-U
    logzc=logsumexp(log_m-beta*U)
    logzf=logsumexp(log_m+(shape+capacity)*np.log(available))
    prior=np.exp(log_m-beta*U-logzc)
    posterior=np.exp(log_m+(shape+capacity)*np.log(available)-logzf)
    logM=(gammaln(capacity+1)-gammaln(shape+capacity+1)
          +logzf-logzc+shape*np.log(beta))
    def p_density(E):
        return np.dot(prior,gamma.pdf(E-U,a=shape,scale=1/beta))
    def q_density(E):
        return np.dot(posterior,beta_distribution.pdf((E-U)/available,shape,capacity+1)/available)
    potential,code_prior,_,_=canonical_energies(n,beta)
    calculated=finite_bath(n,potential,code_prior,beta,capacity,kinetic_per_site=shape/n)
    left,right=calculated['likelihood_interval']
    quad_tv=(quad(lambda E:abs(q_density(E)-p_density(E)),U.min(),total,
                  points=[left,right],epsabs=1e-10,limit=200)[0]
             +np.dot(prior,gamma.sf(total-U,a=shape,scale=1/beta)))/2
    ratio_error=max(abs(q_density(E)/p_density(E)-np.exp(beta*E+capacity*np.log(total-E)-logM))
                    for E in np.linspace(em-.5,ep+.5,20))
    logz_relative=logM-beta*em-capacity*np.log(total-em)
    assert abs(quad_tv-calculated['energy_tv'])<1e-9
    assert ratio_error<1e-10
    assert abs(logz_relative-calculated['log_normalization'])<1e-10
    return dict(n=n,kinetic_shape=shape,bath_capacity=capacity,
                tv_from_direct_density_quadrature=float(quad_tv),
                tv_from_code_cdfs=calculated['energy_tv'],
                likelihood_ratio_max_abs_error=float(ratio_error),
                independently_computed_relative_log_normalization=float(logz_relative),
                code_relative_log_normalization=calculated['log_normalization'])


if __name__=='__main__':
    results={'explicit_spin_checks':explicit_spin_checks(),
             'direct_density_checks':[direct_density_check(shape=6.),direct_density_check(shape=12.)]}
    (Path(__file__).resolve().parents[1]/'data'/'potts-independent-check-results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
