"""Bounded independent integration review of optional integer arc scoring."""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from time import perf_counter

import certify_spacing_design as author
from integer_interval_scores import IntegerIntervalScores
from review_certify_spacing_design import Reference, determinant, inverse, make_record
from review_noisy_markov_exact import independent_log
from review_noisy_markov_spacing import separated_sets


HERE=Path(__file__).resolve().parent


def reference_prices(reference, result, feasible, coefficient_grid):
    inverse_N=inverse(result['tangent_reference'])
    H=tuple(tuple(x/(1-result['delta']) for x in row) for row in inverse_N)
    exact={s:reference.price(s,result['L'],H,result['score_grid'])[0] for s in feasible}
    if coefficient_grid is None:
        return exact,exact
    scorer=IntegerIntervalScores(reference.F,H,coefficient_grid=coefficient_grid,
                                  score_grid=result['score_grid'])
    interval={}
    for selected in feasible:
        total=0
        for i,t in enumerate(selected):
            history=tuple(s for s in selected[:i] if t-s<=result['L'])
            ages=tuple(t-s for s in history)
            coefficients,variance=reference.conditional(ages)
            # Dense local regressions feed the separately reviewed component.
            pattern=scorer.prepare(ages,coefficients,variance)
            total+=scorer.upper(t,pattern)
        interval[selected]=total
        assert total>=exact[selected]
    return exact,interval


def main():
    started=perf_counter()
    counts=dict(certificates=0,coarse_grid_certificates=0,exact_default_certificates=0,
                enumerated_designs=0,invalid_grid_rejections=0,variance_grid_rejections=0,
                cli_checks=0,large_artifact_comparisons=0)
    source_hash=sha256((HERE/'certify_spacing_design.py').read_bytes()).hexdigest()
    scorer_hash=sha256((HERE/'integer_interval_scores.py').read_bytes()).hexdigest()
    for n,gap,k,window in [(1,10**6,0,0),(1,10**6,1,0),
                           (4,1,0,1),(4,1,2,0),(4,1,3,1),
                           (6,2,3,0),(6,3,2,1),(7,2,3,3),(7,1,4,9)]:
        for rho in (Q(1,4),Q(-2,3)):
            record=make_record(n,2,k,gap,rho,Q(1),Q(2))
            reference=Reference(record)
            feasible=[s for s in separated_sets(n,min(gap,n+1)) if len(s)==k]
            incumbent=feasible[len(feasible)//2]
            hull=dict(L=window,selected=incumbent,hull_information=reference.true(incumbent))
            baseline=None
            for grid in (None,1,3,10,10**12):
                result=author.certify(record,hull,integer_grid=grid,
                                      score_grid=11,reference_grid=17)
                exact,interval=reference_prices(reference,result,feasible,grid)
                assert result['integer_price']==max(interval.values())
                assert interval[result['priced_selection']]==result['integer_price']
                assert result['integer_price']>=max(exact.values())
                assert result['selected']==incumbent
                assert result['integer_coefficient_grid']==grid
                if grid is None:
                    baseline=result
                    assert result['arc_arithmetic']=='exact rational'
                    assert result['integer_feature_grid'] is None
                    assert result['integer_scorer_sha256'] is None
                    counts['exact_default_certificates']+=1
                else:
                    assert result['arc_arithmetic']=='outward integer intervals'
                    assert result['integer_feature_grid']==10**18
                    assert result['integer_scorer_sha256']==scorer_hash
                    for key in ('problem_data','delta','spacing_bound_details','tangent_reference',
                                'lower_bound','selected','state_memory_width','state_count_bound'):
                        assert result[key]==baseline[key]
                    assert result['upper_bound']-baseline['upper_bound']==Q(
                        result['integer_price']-baseline['integer_price'],result['score_grid'])
                    counts['coarse_grid_certificates']+=int(grid<=10)
                for selected in feasible:
                    assert result['upper_bound']>=independent_log(
                        determinant(reference.true(selected)))[1]
                    counts['enumerated_designs']+=1
                counts['certificates']+=1

    record=make_record(4,2,2,2,Q(1,4),Q(1),Q(2))
    hull=dict(L=1,selected=(0,2),hull_information=Reference(record).true((0,2)))
    omitted=author.certify(record,hull)
    explicit_none=author.certify(record,hull,integer_grid=None)
    for key in omitted:
        if key!='wall_seconds':
            assert omitted[key]==explicit_none[key]
    for value in (0,-1,True,False,1.5,'10',Q(10)):
        try:
            author.certify(record,hull,integer_grid=value)
        except ValueError as error:
            assert str(error)=='integer_grid must be a positive integer'
            counts['invalid_grid_rejections']+=1
        else:
            raise AssertionError('Malformed integer grid accepted')
    small=make_record(2,1,1,1,Q(0),Q(0),Q(1,100))
    small_hull=dict(L=0,selected=(0,),hull_information=Reference(small).true((0,)))
    try:
        author.certify(small,small_hull,integer_grid=1)
    except ValueError as error:
        assert str(error)=='Variance grid floor must be positive; increase coefficient_grid'
        counts['variance_grid_rejections']+=1
    else:
        raise AssertionError('Zero rounded variance floor was not rejected')
    author.certify(small,small_hull,integer_grid=100)

    with TemporaryDirectory(prefix='spacing-integer-integration-') as directory:
        input_file=Path(directory)/'input.json'
        output_file=Path(directory)/'output.json'
        json_record=json.loads(json.dumps(record,default=str))
        json_record['hulls']=[hull]
        input_file.write_text(json.dumps({'results':[json_record]},default=str))
        subprocess.run([sys.executable,str(HERE/'certify_spacing_design.py'),str(input_file),
                        str(output_file),'--integer-grid','3'],check=True,capture_output=True)
        saved=json.loads(output_file.read_text())
        expected=author.certify(record,hull,integer_grid=3)
        assert saved['integer_price']==expected['integer_price']
        assert Q(saved['upper_bound'])==expected['upper_bound']
        assert saved['integer_coefficient_grid']==3
        assert saved['integer_feature_grid']==10**18
        assert saved['integer_scorer_sha256']==scorer_hash
        assert saved['source_sha256']==source_hash
        assert saved['input_sha256']==sha256(input_file.read_bytes()).hexdigest()
        counts['cli_checks']+=1
        failed_file=Path(directory)/'refused.json'
        failure=subprocess.run([sys.executable,str(HERE/'certify_spacing_design.py'),str(input_file),
                                str(failed_file),'--integer-grid','0'],capture_output=True)
        assert failure.returncode!=0 and not failed_file.exists()
        counts['cli_checks']+=1

    # Compose the already independent large exact-certificate and component
    # replays with the new integration artifact. Do not repeat their 31,900 arcs.
    base=HERE/'results'
    exact_file=base/'noisy-markov-spacing-kinetics-certificate.json'
    fast_file=base/'noisy-markov-spacing-kinetics-integer-certificate.json'
    exact_saved=json.loads(exact_file.read_text())
    fast_saved=json.loads(fast_file.read_text())
    component=json.loads((base/'integer-interval-scores-independent-review.json').read_text())
    original=json.loads((base/'spacing-design-kinetics-certificate-independent-replay.json').read_text())
    exact_hash=sha256(exact_file.read_bytes()).hexdigest()
    assert component['status']==original['status']=='passed'
    assert component['saved_n96_case']['certificate_sha256']==original['certificate_sha256']==exact_hash
    assert component['component_sha256']==fast_saved['integer_scorer_sha256']==scorer_hash
    assert fast_saved['source_sha256']==source_hash
    allowed_changes={'arc_arithmetic','integer_coefficient_grid','integer_feature_grid',
                     'integer_scorer_sha256','source_sha256','wall_seconds','integer_price',
                     'upper_bound','gap','display_upper_bound','display_gap'}
    for key in set(exact_saved)|set(fast_saved):
        if key not in allowed_changes:
            assert exact_saved.get(key)==fast_saved.get(key),(key,'unexpected artifact change')
    assert fast_saved['integer_coefficient_grid']==10**12 and fast_saved['integer_feature_grid']==10**18
    assert exact_saved['integer_price']==component['saved_n96_case']['exact_price']==original['integer_price']
    assert fast_saved['integer_price']==component['saved_n96_case']['interval_price']
    difference=Q(component['saved_n96_case']['objective_upper_increase'])
    assert Q(fast_saved['upper_bound'])-Q(exact_saved['upper_bound'])==difference==Q(1,10**8)
    assert Q(fast_saved['gap'])-Q(exact_saved['gap'])==difference
    assert Q(fast_saved['gap'])==Q(fast_saved['upper_bound'])-Q(fast_saved['lower_bound'])
    counts['large_artifact_comparisons']+=1
    assert sha256((HERE/'certify_spacing_design.py').read_bytes()).hexdigest()==source_hash
    assert sha256((HERE/'integer_interval_scores.py').read_bytes()).hexdigest()==scorer_hash
    report=dict(status='passed',counts=counts,author_sha256=source_hash,
                scorer_sha256=scorer_hash,reviewer_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                large_fast_certificate_sha256=sha256(fast_file.read_bytes()).hexdigest(),
                large_exact_certificate_sha256=exact_hash,
                large_integer_price=fast_saved['integer_price'],large_price_increase=1,
                large_exact_upper_increase=str(difference),
                large_display_gap=fast_saved['display_gap'],elapsed_seconds=perf_counter()-started,
                scope='Integration checks composed with separately accepted component and exact-artifact reviews.')
    (base/'spacing-integer-integration-independent-review.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)


if __name__=='__main__':
    main()
