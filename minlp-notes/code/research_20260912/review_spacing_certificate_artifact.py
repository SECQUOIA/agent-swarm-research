"""Independently replay a saved spacing-constrained exact certificate.

Pricing uses a recursive suffix search with tuples of past calendar times.
Local regressions and the incumbent's information use dense rational solves.
The artifact is the only input needed for the mathematical checks.
"""

import argparse
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from noisy_markov_spacing_bound import spacing_bound
from review_certify_spacing_design import Reference, determinant, inverse, trace_product
from review_noisy_markov_exact import independent_log


def exact_data(record):
    result = dict(record)
    for key in ('F','prior'):
        result[key] = tuple(tuple(Q(x) for x in row) for row in record[key])
    for key in ('rho','latent_variance','nugget_variance'):
        result[key] = Q(record[key])
    return result


def bounded_log(value, grid=10**24):
    """Exact enclosure with bounded-size series arguments after range reduction."""
    assert value>0
    scaled=value
    exponent=0
    while scaled>=2:
        scaled/=2
        exponent+=1
    while scaled<1:
        scaled*=2
        exponent-=1
    coordinate=scaled*grid
    lo=Q(coordinate.numerator//coordinate.denominator,grid)
    hi=Q((coordinate.numerator+coordinate.denominator-1)//coordinate.denominator,grid)
    scale=Q(2)**exponent
    return independent_log(lo*scale)[0],independent_log(hi*scale)[1]


def true_dense_information(reference, selected):
    """One elimination with all sensitivity columns as right-hand sides."""
    if not selected:
        return reference.prior
    size, p = len(selected), reference.p
    augmented = [[reference.R[i][j] for j in selected]+list(reference.F[i])
                 for i in selected]
    for j in range(size):
        pivot = augmented[j][j]
        assert pivot > 0
        for k in range(j,size+p):
            augmented[j][k] /= pivot
        for i in range(j+1,size):
            factor = augmented[i][j]
            for k in range(j,size+p):
                augmented[i][k] -= factor*augmented[j][k]
    solved = [[Q(0)]*p for _ in selected]
    for i in reversed(range(size)):
        for c in range(p):
            solved[i][c] = augmented[i][size+c]-sum(
                (augmented[i][j]*solved[j][c] for j in range(i+1,size)),Q(0))
    return tuple(tuple(reference.prior[i][j]+sum(
        (reference.F[t][i]*solved[s][j] for s,t in enumerate(selected)),Q(0))
        for j in range(p)) for i in range(p))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate',type=Path)
    parser.add_argument('output',type=Path)
    args = parser.parse_args()
    started = perf_counter()
    artifact = json.loads(args.certificate.read_text())
    record = exact_data(artifact['problem_data'])
    reference = Reference(record)
    n,p,k,gap,window = (reference.n,reference.p,record['k'],record['minimum_gap'],artifact['L'])
    assert artifact['n']==n and artifact['p']==p and artifact['k']==k
    assert artifact['minimum_gap']==gap and 0<=window<n
    assert 0<=k<=(n+gap-1)//gap
    width=max(window,min(gap-1,n-1))
    assert artifact['state_memory_width']==width
    delta=Q(artifact['delta'])
    # The bound helper itself has a separate independent exhaustive review.
    accepted_bound=spacing_bound(n,window,gap,record['rho'],
                                 record['latent_variance'],record['nugget_variance'])
    assert delta==accepted_bound['delta']<1
    dense_floor=reference.conditional(tuple(range(gap,window+1,gap)))[1]
    assert dense_floor==accepted_bound['innovation_floor']
    N=tuple(tuple(Q(x) for x in row) for row in artifact['tangent_reference'])
    assert len(N)==p and all(len(row)==p for row in N)
    assert all(N[i][j]==N[j][i] for i in range(p) for j in range(p))
    determinant_N=determinant(N)
    inverse_N=inverse(N)
    H=tuple(tuple(x/(1-delta) for x in row) for row in inverse_N)
    grid=artifact['score_grid']
    assert isinstance(grid,int) and grid>0

    def feasible(selected):
        return (len(selected)==k and all(isinstance(t,int) and not isinstance(t,bool)
                                        and 0<=t<n for t in selected)
                and all(b-a>=gap for a,b in zip(selected,selected[1:])))

    selected,priced=tuple(artifact['selected']),tuple(artifact['priced_selection'])
    assert feasible(selected) and feasible(priced)

    @lru_cache(None)
    def arc(t,history):
        coefficients,variance=reference.conditional(tuple(t-s for s in history))
        adjusted=tuple(reference.F[t][i]-sum(
            (coefficient*reference.F[s][i] for s,coefficient in zip(history,coefficients)),Q(0))
            for i in range(p))
        score=sum((H[i][j]*adjusted[i]*adjusted[j]
                   for i in range(p) for j in range(p)),Q(0))/variance
        assert score>=0
        scaled=score*grid
        return (scaled.numerator+scaled.denominator-1)//scaled.denominator

    @lru_cache(None)
    def suffix(t,remaining,history):
        if remaining==0:
            return 0
        earliest=max(t,history[-1]+gap) if history else t
        capacity=0 if earliest>=n else 1+(n-1-earliest)//gap
        if remaining>capacity:
            return None
        retained=tuple(s for s in history if s>=t+1-width)
        values=[]
        skipped=suffix(t+1,remaining,retained)
        if skipped is not None:
            values.append(skipped)
        if t==earliest:
            following=retained+(t,) if width else ()
            tail=suffix(t+1,remaining-1,following)
            if tail is not None:
                local=tuple(s for s in history if t-s<=window)
                values.append(arc(t,local)+tail)
        return max(values) if values else None

    print(json.dumps({'phase':'pricing','n':n,'k':k,'L':window,'minimum_gap':gap}),flush=True)
    maximum=suffix(0,k,())
    assert maximum==artifact['integer_price']
    witness_price=sum(arc(t,tuple(s for s in priced[:i] if t-s<=window))
                      for i,t in enumerate(priced))
    assert witness_price==maximum
    priced_seconds=perf_counter()-started
    print(json.dumps({'phase':'dense_incumbent','integer_price':maximum,
                      'suffix_states':suffix.cache_info().currsize,
                      'priced_arcs':arc.cache_info().currsize,
                      'elapsed_seconds':priced_seconds}),flush=True)
    J=true_dense_information(reference,selected)
    det_J=determinant(J)
    true_log=bounded_log(det_J)
    lower,upper=Q(artifact['lower_bound']),Q(artifact['upper_bound'])
    assert lower<=true_log[0]
    constant=-p+trace_product(inverse_N,reference.prior)+Q(maximum,grid)
    assert upper>=bounded_log(determinant_N)[1]+constant
    assert upper>=true_log[1]
    assert Q(artifact['gap'])==upper-lower>=0
    input_match=None
    if 'input_file' in artifact and Path(artifact['input_file']).exists():
        producer_path=Path(artifact['input_file'])
        assert sha256(producer_path.read_bytes()).hexdigest()==artifact['input_sha256']
        producer=json.loads(producer_path.read_text(),parse_float=str)['results'][artifact['input_case_index']]
        producer_exact=exact_data({key:producer[key] for key in record})
        assert producer_exact==record
        input_match=True
    report=dict(status='passed',n=n,p=p,k=k,L=window,minimum_gap=gap,
                integer_price=maximum,suffix_states=suffix.cache_info().currsize,
                priced_arcs=arc.cache_info().currsize,
                dense_local_conditionals=reference.conditional.cache_info().currsize,
                dense_innovation_floor=str(dense_floor),
                exact_incumbent_determinant_hex_sha256=sha256(
                    (hex(det_J.numerator)+'/'+hex(det_J.denominator)).encode()).hexdigest(),
                exact_incumbent_log_lower=str(true_log[0]),
                exact_incumbent_log_upper=str(true_log[1]),
                certified_gap=str(upper-lower),display_gap=float(upper-lower),
                matching_producer_input=input_match,
                certificate_sha256=sha256(args.certificate.read_bytes()).hexdigest(),
                reviewer_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                pricing_seconds=priced_seconds,elapsed_seconds=perf_counter()-started,
                scope='Independent mathematical replay of the exact artifact; numerical producer not reviewed.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key] for key in
                     ('status','n','L','integer_price','display_gap','elapsed_seconds')}),flush=True)


if __name__=='__main__':
    main()
