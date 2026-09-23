"""Independent exact review of the minimum-gap design certifier.

References use dense rational normal equations and enumerate feasible subsets.
No reference pricing routine uses masks, stages, or the author's Kalman code.
"""

from copy import deepcopy
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from time import perf_counter

import certify_spacing_design as author
from review_noisy_markov_exact import independent_log
from review_noisy_markov_spacing import DenseReference, dense_solve, separated_sets


HERE = Path(__file__).resolve().parent


def inverse(matrix):
    n = len(matrix)
    columns = [dense_solve(matrix, tuple(Q(i == j) for i in range(n)))
               for j in range(n)]
    return tuple(tuple(columns[j][i] for j in range(n)) for i in range(n))


def determinant(matrix):
    rows = [list(row) for row in matrix]
    answer = Q(1)
    for j in range(len(rows)):
        pivot = rows[j][j]
        assert pivot > 0
        answer *= pivot
        for i in range(j+1, len(rows)):
            factor = rows[i][j]/pivot
            for k in range(j+1, len(rows)):
                rows[i][k] -= factor*rows[j][k]
    return answer


def trace_product(A, B):
    return sum((A[i][j]*B[j][i] for i in range(len(A))
                for j in range(len(A))), Q(0))


class Reference(DenseReference):
    def __init__(self, record):
        self.F = tuple(tuple(Q(x) for x in row) for row in record['F'])
        self.prior = tuple(tuple(Q(x) for x in row) for row in record['prior'])
        self.p = len(self.prior)
        super().__init__(len(self.F), *(Q(record[key]) for key in
                         ('rho', 'latent_variance', 'nugget_variance')))

    @lru_cache(None)
    def true(self, selected):
        if not selected:
            return self.prior
        covariance = tuple(tuple(self.R[i][j] for j in selected) for i in selected)
        solutions = [dense_solve(covariance, tuple(self.F[t][j] for t in selected))
                     for j in range(self.p)]
        return tuple(tuple(self.prior[i][j]+sum(
            (self.F[t][i]*solutions[j][s] for s, t in enumerate(selected)), Q(0))
            for j in range(self.p)) for i in range(self.p))

    @lru_cache(None)
    def increment(self, t, history):
        coefficient, variance = self.conditional(tuple(t-j for j in history))
        adjusted = tuple(self.F[t][i]-sum(
            (value*self.F[j][i] for j, value in zip(history, coefficient)), Q(0))
            for i in range(self.p))
        return tuple(tuple(adjusted[i]*adjusted[j]/variance for j in range(self.p))
                     for i in range(self.p))

    def price(self, selected, window, H, grid):
        integer_price = 0
        exact_price = Q(0)
        for i, t in enumerate(selected):
            history = tuple(s for s in selected[:i] if t-s <= window)
            value = trace_product(H, self.increment(t, history))
            assert value >= 0
            scaled = grid*value
            integer_price += (scaled.numerator+scaled.denominator-1)//scaled.denominator
            exact_price += value
        return integer_price, exact_price


def make_record(n, p, k, gap, rho, latent, nugget):
    return dict(F=tuple(tuple(Q(((t+2)*(j+3)) % 11-5, 3+j)
                             for j in range(p)) for t in range(n)),
                prior=tuple(tuple(Q(2) if i == j else Q(1, 5)
                                  for j in range(p)) for i in range(p)),
                rho=rho, latent_variance=latent, nugget_variance=nugget,
                k=k, minimum_gap=gap)


def validate(record, hull, counters, *, score_grid=7, reference_grid=13):
    reference = Reference(record)
    result = author.certify(record, hull, score_grid=score_grid,
                            reference_grid=reference_grid)
    n, gap, k, window = result['n'], record['minimum_gap'], record['k'], result['L']
    feasible = [s for s in separated_sets(n, min(gap, n+1)) if len(s) == k]
    assert result['selected'] in feasible and result['priced_selection'] in feasible
    assert result['state_memory_width'] == max(window, min(gap-1, n-1))
    assert result['visited_states_including_terminal'] <= result['state_count_bound']
    assert result['problem_data'] == {key: record[key] for key in
           ('F', 'prior', 'rho', 'latent_variance', 'nugget_variance', 'k', 'minimum_gap')}
    assert result['delta'] == result['spacing_bound_details']['delta']
    floor = reference.conditional(tuple(range(gap, window+1, gap)))[1]
    assert result['spacing_bound_details']['innovation_floor'] == floor
    N = result['tangent_reference']
    determinant_N = determinant(N)
    inverse_N = inverse(N)
    H = tuple(tuple(x/(1-result['delta']) for x in row) for row in inverse_N)
    prices = {s: reference.price(s, window, H, score_grid) for s in feasible}
    maximum = max(value[0] for value in prices.values())
    assert maximum == result['integer_price']
    assert prices[result['priced_selection']][0] == maximum
    for selected, (rounded, exact) in prices.items():
        assert Q(rounded, score_grid) >= exact
        assert Q(rounded, score_grid)-exact < Q(k, score_grid) or k == 0
        true_det = determinant(reference.true(selected))
        # These enclosures use a separately implemented positive -log series.
        true_upper_log = independent_log(true_det)[1]
        assert result['upper_bound'] >= true_upper_log
        counters['exhaustive_true_objectives'] += 1
        counters['enumerated_integer_prices'] += 1
    constant = -reference.p + trace_product(inverse_N, reference.prior) + Q(maximum, score_grid)
    assert result['upper_bound'] >= independent_log(determinant_N)[1]+constant
    lower_reference = independent_log(determinant(reference.true(result['selected'])))[0]
    assert result['lower_bound'] <= lower_reference
    assert result['gap'] == result['upper_bound']-result['lower_bound'] >= 0
    # The tangent source may be asymmetric or unrelated to a feasible hull.
    # Only the rounded, symmetrized N and its positive definiteness are used.
    grid = Q(reference_grid)
    for i in range(reference.p):
        for j in range(reference.p):
            center = (reference.prior[i][j]
                      + ((Q(hull['hull_information'][i][j])+Q(hull['hull_information'][j][i]))/2
                         - reference.prior[i][j])/(1-result['delta']))
            assert abs(N[i][j]-center) <= 1/(2*grid)
            assert (N[i][j]*reference_grid).denominator == 1
    counters['certificates'] += 1
    if window < gap-1:
        counters['cooldown_certificates'] += 1
    if k == 0:
        counters['empty_design_certificates'] += 1
    return result


def main():
    started = perf_counter()
    counts = dict(certificates=0, cooldown_certificates=0,
                  empty_design_certificates=0, exhaustive_true_objectives=0,
                  enumerated_integer_prices=0, expected_delta_rejections=0,
                  malformed_input_rejections=0, state_cap_checks=0,
                  cli_exact_decimal_replays=0)
    covariance_cases = [(Q(1,4), Q(1), Q(2)),
                        (Q(-2,3), Q(2), Q(1)),
                        (Q(99,100), Q(1), Q(1,100)),
                        (Q(0), Q(0), Q(1))]
    for n in (1, 2, 4, 6, 7):
        for gap in sorted({1, 2, 3, n+1, 10**6}):
            for rho, latent, nugget in covariance_cases:
                for k in range((n+gap-1)//gap+1):
                    record = make_record(n, 2, k, gap, rho, latent, nugget)
                    reference = Reference(record)
                    selected = next(s for s in separated_sets(n, min(gap,n+1)) if len(s) == k)
                    M = reference.true(selected)
                    for window in sorted({0, 1, min(3,n-1), n-1, n+1}):
                        hull = dict(L=window, selected=tuple(reversed(selected)), hull_information=M)
                        try:
                            validate(record, hull, counts)
                        except ValueError as error:
                            if str(error) != 'Information window gives no positive relative lower bound':
                                raise
                            counts['expected_delta_rejections'] += 1
        print(json.dumps({'completed_horizon':n, 'counts':counts}), flush=True)

    for p in (1,3):
        record = make_record(6,p,2,2,Q(-1,2),Q(1),Q(2))
        for window in (0,1,3,8):
            M = Reference(record).true((0,4))
            # Add an antisymmetric part: it cannot affect N or bound validity.
            if p > 1:
                M = tuple(tuple(x+(Q(17,3) if (i,j)==(0,1) else
                                  Q(-17,3) if (i,j)==(1,0) else 0)
                                for j,x in enumerate(row)) for i,row in enumerate(M))
            validate(record,dict(L=window,selected=(0,4),hull_information=M),counts,
                     score_grid=10**8, reference_grid=10**8)

    record = make_record(6,2,2,3,Q(1,4),Q(1),Q(2))
    hull = dict(L=0,selected=(0,3),hull_information=Reference(record).true((0,3)))
    bad = []
    for field, value in [('minimum_gap',0),('minimum_gap',True),('minimum_gap',2.0),
                         ('k',3),('k',True),('rho',Q(1)),('rho',.2),
                         ('latent_variance',-1),('nugget_variance',0),
                         ('prior',((1,2),(2,1))),('prior',((1,),)),
                         ('F',((1,),)*6)]:
        item = deepcopy(record); item[field] = value
        bad.append((item,hull,{}))
    for field,value in [('L',-1),('L',True),('L',1.0),('selected',(0,1)),
                        ('selected',(0,0)),('selected',(0,6)),('selected',(False,3)),
                        ('selected',(0,)),('hull_information',((1,),)),
                        ('hull_information',((-100,0),(0,-100)))]:
        item=deepcopy(hull); item[field]=value
        bad.append((record,item,{}))
    for field,value in [('score_grid',0),('reference_grid',True),('max_states',0)]:
        bad.append((record,hull,{field:value}))
    for item,h,kwargs in bad:
        try:
            author.certify(item,h,**kwargs)
        except (TypeError,ValueError):
            counts['malformed_input_rejections'] += 1
        else:
            raise AssertionError('Invalid certificate input accepted')
    nominal = author.certify(record,hull)
    author.certify(record,hull,max_states=nominal['state_count_bound'])
    counts['state_cap_checks'] += 1
    try:
        author.certify(record,hull,max_states=nominal['state_count_bound']-1)
    except MemoryError:
        counts['state_cap_checks'] += 1
    else:
        raise AssertionError('Preflight state cap was ignored')

    # The CLI's decimal interpretation and self-contained artifact are part of
    # the certificate contract; this exercises actual JSON numbers, not strings.
    with TemporaryDirectory(prefix='spacing-certificate-review-') as temporary:
        directory = Path(temporary)
        input_file, output_file = directory/'input.json', directory/'output.json'
        cli_record = dict(F=[[.1,-.3],[.7,.2],[-.9,.4],[.6,-.8]],
                          prior=[[1.0,0],[0,1.0]],rho=-.25,
                          latent_variance=1.0,nugget_variance=2.0,
                          k=2,minimum_gap=2,
                          hulls=[{},dict(L=0,selected=[0,3],hull_information=[[2.0,.1],[.1,2.0]])])
        input_file.write_text(json.dumps({'results':[{},cli_record]}))
        subprocess.run([sys.executable,str(HERE/'certify_spacing_design.py'),
                        str(input_file),str(output_file),'--case','1','--hull','1'],
                       check=True,capture_output=True,text=True)
        artifact = json.loads(output_file.read_text())
        exact_record = artifact['problem_data']
        exact_record['F'] = tuple(tuple(Q(x) for x in row) for row in exact_record['F'])
        exact_record['prior'] = tuple(tuple(Q(x) for x in row) for row in exact_record['prior'])
        for key in ('rho','latent_variance','nugget_variance'):
            exact_record[key] = Q(exact_record[key])
        assert exact_record['F'][0] == (Q(1,10),Q(-3,10))
        assert exact_record['rho'] == Q(-1,4)
        reference = Reference(exact_record)
        N = tuple(tuple(Q(x) for x in row) for row in artifact['tangent_reference'])
        inv_N = inverse(N)
        H = tuple(tuple(x/(1-Q(artifact['delta'])) for x in row) for row in inv_N)
        feasible = [s for s in separated_sets(4,2) if len(s)==2]
        prices = {s: reference.price(s,artifact['L'],H,artifact['score_grid'])[0]
                  for s in feasible}
        assert artifact['integer_price'] == max(prices.values())
        assert prices[tuple(artifact['priced_selection'])] == artifact['integer_price']
        assert Q(artifact['lower_bound']) <= independent_log(
            determinant(reference.true(tuple(artifact['selected']))))[0]
        assert all(Q(artifact['upper_bound']) >= independent_log(
            determinant(reference.true(s)))[1] for s in feasible)
        assert artifact['input_sha256'] == sha256(input_file.read_bytes()).hexdigest()
        assert artifact['source_sha256'] == sha256((HERE/'certify_spacing_design.py').read_bytes()).hexdigest()
        assert artifact['input_case_index'] == artifact['input_hull_index'] == 1
        counts['cli_exact_decimal_replays'] += 1

    report = dict(status='passed',counts=counts,elapsed_seconds=perf_counter()-started,
                  author_sha256=sha256((HERE/'certify_spacing_design.py').read_bytes()).hexdigest(),
                  bound_sha256=sha256((HERE/'noisy_markov_spacing_bound.py').read_bytes()).hexdigest(),
                  primitive_sha256=sha256((HERE/'certify_noisy_markov.py').read_bytes()).hexdigest(),
                  reviewer_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  limitations=['Tests cover the exact certifier; the numerical producer is outside scope.',
                               'The state-count preflight is not a byte or process-memory limit.'])
    (HERE/'results'/'spacing-design-certificate-independent-review.json').write_text(
        json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)


if __name__ == '__main__':
    main()
