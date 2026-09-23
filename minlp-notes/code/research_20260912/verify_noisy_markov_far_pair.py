"""Exact checks of a proposed sharper scalar far-residual covariance bound.

This script does not change any certifier. It checks a newly observed identity
against dense rational residual covariance in nonstationary scalar models.
"""

from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import random

from noisy_markov_spacing_bound import spacing_bound
from review_noisy_markov_spacing import dense_solve, enumerated_pair_majorants


class Model:
    def __init__(self, initial, transitions, processes, noises):
        self.n=len(noises)
        self.a,self.q,self.r=transitions,processes,noises
        self.P=[initial]
        for t in range(1,self.n):
            self.P.append(self.a[t]**2*self.P[-1]+self.q[t])
        self.R=tuple(tuple(self.P[min(i,j)]*self.transition(min(i,j),max(i,j))
                           +(self.r[i] if i==j else 0)
                           for j in range(self.n)) for i in range(self.n))

    def transition(self,s,t):
        value=Q(1)
        for j in range(s+1,t+1):
            value*=self.a[j]
        return value

    @lru_cache(None)
    def conditional(self,t,history):
        cross=tuple(self.R[j][t] for j in history)
        coefficients=dense_solve(tuple(tuple(self.R[i][j] for j in history)
                                      for i in history),cross)
        variance=self.R[t][t]-sum((b*c for b,c in zip(coefficients,cross)),Q(0))
        return coefficients,variance

    def update_product(self,history):
        product=Q(1)
        previous=None
        posterior=None
        for t in history:
            prediction=(self.P[t] if previous is None else
                        self.P[t]-self.transition(previous,t)**2*(self.P[previous]-posterior))
            gain=prediction/(prediction+self.r[t])
            product*=1-gain
            posterior=prediction*(1-gain)
            previous=t
        return product

    def check(self,selected,window,counters):
        rows,variances,histories=[],[],[]
        for i,t in enumerate(selected):
            history=tuple(s for s in selected[:i] if t-s<=window)
            b,d=self.conditional(t,history)
            row={t:Q(1),**{s:-coefficient for s,coefficient in zip(history,b)}}
            assert sum((value*self.P[s]*self.transition(s,t)
                        for s,value in row.items()),Q(0))==d-self.r[t]
            rows.append(row);variances.append(d);histories.append(history)
            counters['latent_residual_covariances']+=1
        for i,s in enumerate(selected):
            for j in range(i+1,len(selected)):
                t=selected[j]
                if t-s<=window:
                    continue
                direct=sum((x*y*self.R[u][v] for u,x in rows[i].items()
                            for v,y in rows[j].items()),Q(0))
                predicted=(self.transition(s,t)*(variances[i]-self.r[s])
                           *self.update_product(histories[j]))
                assert direct==predicted
                assert abs(direct)<=max(self.P)*abs(self.transition(s,t))
                counters['far_pair_identities']+=1
        counters['subset_window_models']+=1


def main():
    rng=random.Random(2026091201)
    counters=dict(subset_window_models=0,far_pair_identities=0,
                  latent_residual_covariances=0,nonstationary_models=0)
    transition_choices=[Q(-99,100),Q(-2,3),Q(0),Q(1,4),Q(4,5)]
    process_choices=[Q(0),Q(1,10),Q(1,2)]
    noise_choices=[Q(1,100),Q(1,5),Q(1),Q(3)]
    for n in range(1,8):
        for case in range(5):
            initial=Q(0) if case==0 else Q(case,3)
            a=[Q(0)]+[rng.choice(transition_choices) for _ in range(n-1)]
            q=[Q(0)]+[Q(0) if case==0 else rng.choice(process_choices) for _ in range(n-1)]
            r=[rng.choice(noise_choices) for _ in range(n)]
            model=Model(initial,a,q,r)
            counters['nonstationary_models']+=1
            for k in range(1,n+1):
                for selected in combinations(range(n),k):
                    for window in range(n+1):
                        model.check(selected,window,counters)

    n,window,gap=96,13,2
    rho,latent,nugget=Q('0.6324555320336759'),Q('0.00125'),Q('0.00125')
    old=spacing_bound(n,window,gap,rho,latent,nugget)
    phi=enumerated_pair_majorants(n,window,gap,rho,latent,nugget)
    for h in range(max(gap,window+1),n):
        phi[h]=latent*abs(rho)**h
    best=[Q(0)]*n
    for h in range(gap,n):
        best[h]=max(best[h-1],phi[h]+best[h-gap])
    proposed=max(best[t]+best[n-1-t] for t in range(n))/old['innovation_floor']
    assert proposed<=old['delta']
    result=dict(status='exact_checks_passed_fresh_review_pending',counts=counters,
                n96_spacing_probe=dict(old_delta=float(old['delta']),proposed_delta=float(proposed),
                                       relative_reduction=float(1-proposed/old['delta'])),
                scope='Proposed scalar identity only; no certificate implementation was changed.')
    output=Path(__file__).resolve().parent/'results'/'noisy-markov-far-pair-verification.json'
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    main()
