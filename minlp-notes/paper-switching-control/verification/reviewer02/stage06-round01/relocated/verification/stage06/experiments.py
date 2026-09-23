"""Reproduce exact tables; all arithmetic certificates use the standard library.

No source data are silently fetched. Pass --fetch or an already downloaded
--data file; the SHA256 check is mandatory in both cases. Timings are descriptive
medians of three calls in this process, with setup and verification excluded.
"""
if not __debug__:
    raise SystemExit('Do not use -O: exact verification requires assertions.')

from fractions import Fraction as F
from pathlib import Path
from itertools import combinations, product
from statistics import median
from time import perf_counter, process_time
import argparse, hashlib, json, platform, sys, urllib.request

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'reference'))
sys.path.insert(0, str(HERE.parent / 'stage05'))
from rounding import optimal_one_switch, optimal_few_switches, schedule_error
from coarsening import uniform_masses, certified_coarsen
URL = 'https://raw.githubusercontent.com/adbuerger/pycombina/6b073fe29984186dccfc7e2108bfba9692a6cc9c/examples/data/mmlotka_nt_12000_400.csv'
SHA = '1ed44f0906dfe71654a2f263d354ee0046ae6211baa1ddfd4b5945293c900883'

def timed(fn, repeats=3):
    wall, cpu = [], []
    answer = None
    for _ in range(repeats):
        w, c = perf_counter(), process_time()
        result = fn()
        wall.append(perf_counter()-w); cpu.append(process_time()-c)
        if answer is None: answer = result
        else: assert result == answer
    return answer, {'wall_median_s': median(wall), 'cpu_median_s': median(cpu),
                    'wall_samples_s': wall, 'cpu_samples_s': cpu}

def prefixes(rows, dt):
    times, sums = [F(0)], [[F(0)]*len(rows[0])]
    for row, width in zip(rows, dt):
        times.append(times[-1]+width)
        sums.append([a+b for a,b in zip(sums[-1],row)])
    return times, sums

def exhaustive(rows, dt, budget):
    """Independent labeled-word enumeration; never calls solver cost helpers."""
    times, A = prefixes(rows, dt)
    n, N = len(rows[0]), len(rows)
    k, best, cases = min(budget+1, N), None, 0
    for interior in combinations(range(1,N), k-1):
        bounds = (0,) + interior + (N,)
        for modes in product(range(n), repeat=k):
            served, error = [F(0)]*n, F(0)
            for label, left, right in zip(modes, bounds, bounds[1:]):
                served[label] += times[right]-times[left]
                error = max(error, *(abs(A[right][i]-served[i]) for i in range(n)))
            best = error if best is None else min(best,error)
            cases += 1
    return best, cases

def continuous_one(rows, dt):
    """All ordered-pair crossings, exact for a piecewise-constant simplex input.

    The first increasing and second decreasing terms of the three-term formula
    meet once; the omitted-mass term is constant. Every pair is considered.
    """
    times,A=prefixes(rows,dt); n=len(rows[0]); T=times[-1]; totals=A[-1]
    records=[]
    for p in range(n):
        for q in range(n):
            if p==q: continue
            for j,width in enumerate(dt):
                g0=2*times[j]-A[j][p]-T+totals[q]
                g1=2*times[j+1]-A[j+1][p]-T+totals[q]
                if g0<=0<=g1:
                    tau=times[j]-g0/(2-rows[j][p]/width)
                    Ap=A[j][p]+(tau-times[j])*rows[j][p]/width
                    value=max([tau-Ap,T-totals[q]-tau]+[totals[i] for i in range(n) if i not in (p,q)])
                    records.append({'p':p,'q':q,'time':str(tau),'error':str(value)})
                    break
            else: raise AssertionError('missing crossing')
    best=min(records,key=lambda r:(F(r['error']),r['p'],r['q']))
    tau=F(best['time']); p,q=best['p'],best['q']; direct=F(0)
    # Independently evaluate every original input knot and the added switch.
    for j,width in enumerate(dt):
        candidates=[times[j+1]]
        if times[j]<=tau<=times[j+1]: candidates.append(tau)
        for t in candidates:
            actual=[A[j][i]+(t-times[j])*rows[j][i]/width for i in range(n)]
            served=[(min(t,tau) if i==p else max(F(0),t-tau) if i==q else F(0)) for i in range(n)]
            direct=max(direct,*(abs(a-b) for a,b in zip(actual,served)))
    assert direct==F(best['error'])
    return {'best':best,'all_pairs':records}

def public_input(raw):
    assert hashlib.sha256(raw).hexdigest() == SHA
    data = [[F(x) for x in line.split()] for line in raw.decode().splitlines()[1:]]
    rows, dt, normalization, quantization = [], [], F(0), F(0)
    cum_error = [F(0)]*3; cum_max = F(0)
    for row, following in zip(data,data[1:]):
        width, weights = following[0]-row[0], row[3:]
        assert len(weights)==3 and width>0 and min(weights)>=0 and sum(weights)>0
        norm = [x/sum(weights) for x in weights]
        scaled = [x*10**6 for x in norm]
        counts = [x.numerator//x.denominator for x in scaled]
        order = sorted(range(3), key=lambda i: (-(scaled[i]-counts[i]), i))
        for i in order[:10**6-sum(counts)]: counts[i]+=1
        rates = [F(x,10**6) for x in counts]
        normalization = max(normalization, *(abs(a-b) for a,b in zip(weights,norm)))
        quantization = max(quantization, *(abs(a-b) for a,b in zip(norm,rates)))
        cum_error = [e+width*(a-b) for e,a,b in zip(cum_error,norm,rates)]
        cum_max = max(cum_max, *map(abs,cum_error))
        rows.append(tuple(width*x for x in rates)); dt.append(width)
    assert len(rows)==12000 and sum(dt)==12 and set(dt)=={F(1,1000)}
    assert normalization < F(4959,10**10) and quantization < F(1,10**6)
    assert cum_max < F(12,10**6)
    return rows, dt, {'normalization_max':str(normalization), 'quantization_max':str(quantization),
                     'cumulative_quantization_max':str(cum_max), 'certified_delta':str(F(12,10**6))}

def describe(answer, dt):
    schedule = answer.schedule()
    times, _ = prefixes([[d] for d in dt], dt)
    switches = [j for j in range(1,len(schedule)) if schedule[j]!=schedule[j-1]]
    return {'error':str(answer.error), 'modes':[schedule[0]]+[schedule[j] for j in switches],
            'switch_times':[str(times[j]) for j in switches]}

def solve(rows,dt,budget):
    return optimal_one_switch(rows,dt) if budget==1 else optimal_few_switches(rows,dt,budget)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data',type=Path)
    parser.add_argument('--fetch',action='store_true')
    parser.add_argument('--output',type=Path,default=HERE/'results.json')
    args=parser.parse_args()
    if args.data: raw=args.data.read_bytes()
    elif args.fetch: raw=urllib.request.urlopen(URL,timeout=60).read()
    else: parser.error('pass --fetch or --data PATH; use check_results.py for offline validation')
    rows,dt,errors=public_input(raw)
    cpu_info=Path('/proc/cpuinfo').read_text() if Path('/proc/cpuinfo').exists() else ''
    cpu_name=next((x.split(':',1)[1].strip() for x in cpu_info.splitlines() if x.startswith('model name')),platform.processor())
    result={'provenance':{'url':URL,'sha256':SHA,'quantization_denominator':10**6,**errors},
            'environment':{'python':sys.version,'platform':platform.platform(),'cpu':cpu_name,
                           'repetitions':3,'timing_scope':'solver only; inputs constructed before timing; verification afterward',
                           'concurrency':'shared host; other processes may run; no affinity or frequency control'},
            'public':[],'uniform_convergence':[],'scaling':[],'controlled':[]}
    answer,timing=timed(lambda:optimal_one_switch(rows,dt))
    assert answer.error==F(1889,1000)==schedule_error(rows,dt,answer.schedule())
    independent,cases=exhaustive(rows,dt,1)
    assert independent==answer.error
    result['public_fine']={'n':3,'N':12000,'budget':1,**describe(answer,dt),**timing,'independent_cases':cases}
    result['public_continuous_one']=continuous_one(rows,dt)
    assert F(result['public_continuous_one']['best']['error'])==F(4721469,2500000)
    print('Fine and continuous public one-switch scans verified',flush=True)
    derived=[]
    for M,budgets in [(12,range(4)),(24,range(4)),(48,range(4))]:
        coarse,h=uniform_masses(rows,dt,M); coarse_dt=[h]*M
        derived.append({'N':M,'width':str(h),'masses':[[str(x) for x in row] for row in coarse]})
        for budget in budgets:
            answer,timing=timed(lambda:solve(coarse,coarse_dt,budget))
            expanded=tuple(mode for mode in answer.schedule() for _ in range(12000//M))
            assert schedule_error(rows,dt,expanded)==answer.error
            if M<=24:
                brute,cases=exhaustive(coarse,coarse_dt,budget)
                assert brute==answer.error
            else: cases=None
            lower=max(F(0),answer.error-h)
            result['public'].append({'N':M,'budget':budget,**describe(answer,coarse_dt),**timing,
                'general_lower':str(lower),'lower_strict':answer.error-h>=0,'upper':str(answer.error),
                'independent_cases':cases})
            print(f'Public M={M}, s={budget}: {answer.error}',flush=True)
    certificate=certified_coarsen(rows,dt,2,cells=24)
    assert certificate.exact_error==F(3,2) and certificate.lower==1 and certificate.lower_strict
    result['coarsener_crosscheck']={'N':24,'budget':2,'error':str(certificate.exact_error),
                                    'lower':str(certificate.lower),'lower_strict':certificate.lower_strict}
    for M in [3,4,5,6,8,9,12,16,24]:
        coarse,h=uniform_masses([[F(1,3)]*3],[1],M)
        answer=optimal_few_switches(coarse,[h]*M,2)
        assert max(F(0),answer.error-h)<=F(1,6)<=answer.error
        assert answer.error==schedule_error(coarse,[h]*M,answer.schedule())
        brute,cases=exhaustive(coarse,[h]*M,2)
        assert brute==answer.error
        result['uniform_convergence'].append({'N':M,'error':str(answer.error),
                                              'lower':str(max(F(0),answer.error-h))})
    # Uniform controls isolate mode/grid dependence without instance-generation noise.
    for n,N in [(4,12),(8,12),(16,12),(32,12),(8,8),(8,16),(8,24)]:
        sample=[[F(1,n*N)]*n for _ in range(N)]; widths=[F(1,N)]*N
        answer,timing=timed(lambda:optimal_few_switches(sample,widths,2))
        assert answer.error==schedule_error(sample,widths,answer.schedule())
        result['scaling'].append({'n':n,'N':N,'budget':2,'error':str(answer.error),**timing})
    for n,N,budget in [(3,8,2),(4,8,2),(3,8,3)]:
        sample=[]
        for j in range(N):
            weights=[1+((j+2)*(i+3)+i*i)%11 for i in range(n)]
            sample.append([F(w,N*sum(weights)) for w in weights])
        widths=[F(1,N)]*N
        answer,dp_time=timed(lambda:optimal_few_switches(sample,widths,budget))
        (brute,cases),brute_time=timed(lambda:exhaustive(sample,widths,budget))
        assert answer.error==brute==schedule_error(sample,widths,answer.schedule())
        result['controlled'].append({'n':n,'N':N,'budget':budget,'error':str(brute),'cases':cases,
                                     'subset_dp':dp_time,'word_enumeration':brute_time})
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    (args.output.parent/'derived_public.json').write_text(json.dumps({'source_sha256':SHA,'grids':derived},indent=2)+'\n')
    print(f'Wrote {args.output}',flush=True)

if __name__=='__main__': main()
