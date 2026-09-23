"""Exact objective certificates for rational noisy-Markov design instances.

Numerical optimization supplies an arbitrary SPD tangent reference and a feasible
selection. All reported objective bounds are recomputed using rational Kalman
conditionals, upward-rounded integer arc scores, exact count/mask pricing, and
rational logarithm enclosures. JSON decimals define exact rational input data.
"""

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
from time import perf_counter

import sympy as sp


def rational(value):
    if isinstance(value,bool) or not isinstance(value,(int,str,Q)):
        raise TypeError("Use exact rational strings, integers or Fractions")
    return Q(value)


def matrix(values):
    rows=tuple(tuple(rational(x) for x in row) for row in values)
    if not rows or not rows[0] or any(len(row)!=len(rows[0]) for row in rows):
        raise ValueError("Nonempty rectangular matrix required")
    return rows


def sympy_matrix(values):
    return sp.Matrix([[sp.Rational(x.numerator,x.denominator) for x in row] for row in values])


def fraction(value):
    return Q(int(value.p),int(value.q))


def require_spd(values):
    n=len(values)
    if any(len(row)!=n for row in values) or any(values[i][j]!=values[j][i] for i in range(n) for j in range(n)):
        raise ValueError("Exact symmetric matrix required")
    m=sympy_matrix(values)
    if any(m[:j,:j].det()<=0 for j in range(1,n+1)):
        raise ValueError("Tangent/prior must be positive definite; increase reference precision")
    return m


def log_enclosure(value, terms=32, grid=10**14):
    """Exact lower/upper rationals for log of a positive rational."""
    value=rational(value)
    if any(isinstance(x,bool) or not isinstance(x,int) or x<1 for x in (terms,grid)):
        raise ValueError("Positive integer logarithm order and grid required")
    if value<=0:
        raise ValueError("Positive logarithm argument required")
    exponent=value.numerator.bit_length()-value.denominator.bit_length()
    scale=Q(2**exponent) if exponent>=0 else Q(1,2**(-exponent))
    z=value/scale
    if z<1:
        exponent-=1
        z*=2
    if z>=2:
        exponent+=1
        z/=2
    assert 1<=z<2
    def series(y):
        t=(y-1)/(y+1)
        result=sum((2*t**(2*i+1)/Q(2*i+1) for i in range(terms)),Q(0))
        tail=2*t**(2*terms+1)/(Q(2*terms+1)*(1-t*t))
        return result,result+tail
    scaled=z*grid
    lo=Q(scaled.numerator//scaled.denominator,grid)
    hi=Q(-((-scaled.numerator)//scaled.denominator),grid)
    lower=series(lo)[0]
    upper=series(hi)[1]
    log2=series(Q(2))
    return (lower+exponent*log2[0 if exponent>=0 else 1],
            upper+exponent*log2[1 if exponent>=0 else 0])


def local_coefficients(history, target, rho, latent, nugget):
    """True local regression coefficients from a fresh exact scalar filter."""
    if not history:
        return (),latent+nugget
    coefficients=[]
    posterior=latent
    previous=None
    for t in history:
        a=Q(1) if previous is None else rho**(t-previous)
        prediction=latent if previous is None else a*a*posterior+latent*(1-a*a)
        predicted=[a*x for x in coefficients]
        gain=prediction/(prediction+nugget)
        coefficients=[(1-gain)*x for x in predicted]+[gain]
        posterior=(1-gain)*prediction
        previous=t
    a=rho**(target-previous)
    return tuple(a*x for x in coefficients),a*a*posterior+latent*(1-a*a)+nugget


def true_information(F,prior,selected,rho,latent,nugget):
    p=len(prior)
    information=[list(row) for row in prior]
    prediction_sensitivity=[Q(0)]*p
    posterior=latent
    previous=None
    for t in selected:
        a=Q(1) if previous is None else rho**(t-previous)
        prediction=latent if previous is None else a*a*posterior+latent*(1-a*a)
        predicted=[a*x for x in prediction_sensitivity]
        adjusted=[x-y for x,y in zip(F[t],predicted)]
        variance=prediction+nugget
        for i in range(p):
            for j in range(p):
                information[i][j]+=adjusted[i]*adjusted[j]/variance
        gain=prediction/variance
        prediction_sensitivity=[x+gain*y for x,y in zip(predicted,adjusted)]
        posterior=(1-gain)*prediction
        previous=t
    return tuple(tuple(row) for row in information)


def full_grid_variance_floor(n,rho,latent,nugget):
    """Conditioning on every past candidate minimizes the innovation variance."""
    prediction=latent
    floor=latent+nugget
    for _ in range(n):
        variance=prediction+nugget
        floor=min(floor,variance)
        posterior=prediction*nugget/variance
        prediction=rho*rho*posterior+latent*(1-rho*rho)
    return floor


def spectral_bound(n,L,rho,latent,nugget):
    """Reviewed gain bound with exact full-calendar innovation normalization."""
    a=abs(rho)
    if a==0 or latent==0 or L>=n-1:
        return Q(0)
    gain=latent/(latent+nugget)
    floor=full_grid_variance_floor(n,rho,latent,nugget)
    return 2*latent/floor*a**(L+1)/(1-a)*(1+gain*a*(1-a**L)/(1-a))


def certify(record,hull,*,score_grid=10**8,reference_grid=10**8,max_states=2_000_000):
    started=perf_counter()
    if any(isinstance(x,bool) or not isinstance(x,int) or x<1 for x in (score_grid,reference_grid,max_states)):
        raise ValueError("Positive integer score/reference grids and state cap required")
    F,prior=matrix(record["F"]),matrix(record["prior"])
    n,p=len(F),len(prior)
    k,L=record["k"],hull["L"]
    if (isinstance(k,bool) or not isinstance(k,int) or not 0<=k<=n
            or isinstance(L,bool) or not isinstance(L,int) or L<0):
        raise ValueError("Invalid cardinality/window")
    L=min(L,n-1)
    masks=1<<L
    if n*(k+1)*masks>max_states:
        raise MemoryError("Exact certificate count/mask state limit exceeded")
    if any(len(row)!=p for row in F):
        raise ValueError("Sensitivity/prior dimensions differ")
    require_spd(prior)
    rho,latent,nugget=map(rational,(record["rho"],record["latent_variance"],record["nugget_variance"]))
    if abs(rho)>=1 or latent<0 or nugget<=0:
        raise ValueError("Invalid stationary covariance data")
    selected=tuple(hull["selected"])
    if (len(selected)!=k or len(set(selected))!=k
            or any(isinstance(t,bool) or not isinstance(t,int) or not 0<=t<n for t in selected)):
        raise ValueError("Incumbent must be a feasible cardinality-k subset")
    selected=tuple(sorted(selected))
    delta=spectral_bound(n,L,rho,latent,nugget)
    if delta>=1:
        raise ValueError("Window is too short for the relative-information certificate")
    M=matrix(hull["hull_information"])
    if len(M)!=p or any(len(row)!=p for row in M):
        raise ValueError("Tangent source dimensions differ")
    reference=tuple(tuple(prior[i][j]+(M[i][j]-prior[i][j])/(1-delta) for j in range(p)) for i in range(p))
    if len(reference)!=p or any(len(row)!=p for row in reference):
        raise ValueError("Tangent reference dimensions differ")
    def nearest(x):
        y=x*reference_grid+Q(1,2)
        return Q(y.numerator//y.denominator,reference_grid)
    N=tuple(tuple(nearest((reference[i][j]+reference[j][i])/2) for j in range(p)) for i in range(p))
    exact_N=require_spd(N)
    inverse=exact_N.inv()
    inverse=tuple(tuple(fraction(inverse[i,j]) for j in range(p)) for i in range(p))
    H=tuple(tuple(x/(1-delta) for x in row) for row in inverse)
    scores={}
    conditional_cache={}
    for t in range(n):
        for mask in range(1<<min(t,L)):
            if mask.bit_count()>=k:
                continue
            ages=tuple(age for age in range(L,0,-1) if mask&(1<<(age-1)))
            if ages not in conditional_cache:
                conditional_cache[ages]=local_coefficients(tuple(-age for age in ages),0,rho,latent,nugget)
            b,d=conditional_cache[ages]
            adjusted=[F[t][j]-sum((coefficient*F[t-age][j] for coefficient,age in zip(b,ages)),Q(0)) for j in range(p)]
            score=sum((H[i][j]*adjusted[i]*adjusted[j] for i in range(p) for j in range(p)),Q(0))/d
            scaled=score*score_grid
            scores[t,mask]=-((-scaled.numerator)//scaled.denominator)
    states={(0,0):(0,())}
    for t in range(n):
        following={}
        for (count,mask),(score,path) in states.items():
            shift=(mask<<1)&(masks-1)
            moves=[]
            if count+n-t-1>=k:
                moves.append(((count,shift),(score,path)))
            if count<k:
                moves.append(((count+1,shift|(1 if L else 0)),(score+scores[t,mask],path+(t,))))
            for state,candidate in moves:
                if state not in following or candidate>following[state]:
                    following[state]=candidate
        states=following
    maximum,priced=max(value for (count,_),value in states.items() if count==k)
    prior_trace=sum((inverse[i][j]*prior[j][i] for i in range(p) for j in range(p)),Q(0))
    logN=log_enclosure(fraction(exact_N.det()))
    upper=logN[1]-p+prior_trace+Q(maximum,score_grid)
    J=true_information(F,prior,selected,rho,latent,nugget)
    lower=log_enclosure(fraction(require_spd(J).det()))[0]
    if upper<lower:
        raise ArithmeticError("Certified upper is below feasible lower")
    return {"status":"certified","n":n,"p":p,"k":k,"L":L,
            "input_interpretation":"JSON decimal numbers are exact rational data",
            "problem_data":{"F":F,"prior":prior,"rho":rho,
                            "latent_variance":latent,"nugget_variance":nugget,"k":k},
            "delta":str(delta),"tangent_reference":N,"score_grid":score_grid,
            "full_grid_innovation_variance_floor":str(full_grid_variance_floor(n,rho,latent,nugget)),
            "reference_grid":reference_grid,"priced_selection":priced,
            "integer_price":maximum,"selected":selected,
            "lower_bound":str(lower),"upper_bound":str(upper),"gap":str(upper-lower),
            "display_lower_bound":float(lower),"display_upper_bound":float(upper),
            "display_gap":float(upper-lower),"conditional_patterns":len(conditional_cache),
            "wall_seconds":perf_counter()-started}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",type=Path)
    parser.add_argument("output",type=Path)
    parser.add_argument("--case",type=int,default=0)
    parser.add_argument("--hull",type=int,default=-1)
    args=parser.parse_args()
    report=json.loads(args.input.read_text(),parse_float=str)
    record=report["results"][args.case]
    result=certify(record,record["hulls"][args.hull])
    result["source_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["input_sha256"]=hashlib.sha256(args.input.read_bytes()).hexdigest()
    result["input_file"]=str(args.input)
    result["input_case_index"]=args.case
    result["input_hull_index"]=args.hull
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({key:result[key] for key in ("status","n","L","display_gap","wall_seconds")}),flush=True)


if __name__=="__main__":
    main()
