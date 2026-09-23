"""Independent extra atlas-stratum tests and provenance/table checks."""
from pathlib import Path
import sys,json,hashlib,random,subprocess
import sympy as s
HERE=Path(__file__).resolve().parent
REPO=Path('/home/sgusev/repo/minlp-notes')
SNAP=REPO/'paper-structured-bilevel/process/snapshots/stage06-round01'
sys.path.insert(0,str(HERE/'code'))
import original_faces as f
import compressed_solver as c
from check_full_task import data, validate_witness


def compressed_at(atlas,x):
    result=[]
    for p,rs in atlas.points:
        if f.compare(p,x)==0:
            for r in rs:
                assert r.left==r.right
                result.append(tuple(map(s.simplify,r.piece.z(r.left))))
            return set(result)
    for a,b,win in atlas.cells:
        if f.compare(a,x)<0 and f.compare(x,b)<0:
            for i in win:
                branch=atlas.branches[i]
                w=s.sympify(branch.w).subs(c.X,x)
                result.append(tuple(map(s.simplify,branch.piece.z(w))))
            return set(result)
    raise AssertionError('No compressed response')


def random_cases():
    rng=random.Random(66004)
    count=queries=skipped=0
    while count<16:
        n=1+count%3
        d=[s.Rational(rng.randrange(2,7),2) for _ in range(n)]
        u=[rng.choice([-2,-1,0,1,2]) for _ in range(n)]
        lo=[s.Rational(rng.randrange(-3,1),2) for _ in range(n)]
        hi=[v+s.Rational(rng.randrange(0,5),2) for v in lo]
        ins=data(d,[s.Rational(rng.randrange(-5,6),3) for _ in range(n)],u,
                 s.Rational(rng.randrange(0,7),5),gamma=rng.choice([-2,-1,1,2]),lower=lo,upper=hi,L=-2,U=3)
        try: ref=f.build(ins)
        except ValueError as err:
            assert 'Singular principal' in str(err)
            skipped+=1
            continue
        atlas=c.build_atlas(c.Instance(**ins))
        rows=[dict(a=str(rng.choice([-1,0,1])),b=[str(rng.choice([-1,0,1])) for _ in range(n)],rhs=str(rng.choice([-1,0,1,2])))]
        cuts=f.sorted_distinct(ref.cuts+[x for x,rs in atlas.points])
        samples=cuts+[f.interior(a,b) for a,b in zip(cuts,cuts[1:])]
        for x in samples:
            eligible=[face for face in ref.faces if f.compare(face.lo,x)<=0 and f.compare(x,face.hi)<=0]
            values=[f.evaluate(face.cost,x) for face in eligible]
            best=values[0]
            for value in values[1:]:
                if f.compare(value,best)<0:best=value
            expected={tuple(map(s.simplify,face.point(x))) for face,value in zip(eligible,values) if f.compare(value,best)==0}
            assert compressed_at(atlas,x)==expected
            queries+=1
        for semantics in ('optimistic','pessimistic'):
            a=f.optimize(ref,rows,semantics)
            b=c.optimize_tariff(atlas,[c.Constraint(**row) for row in rows],semantics)
            assert (a is None)==(b is None)
            if a is not None:
                assert f.compare(a['value'],b.value)==0 and a['attained']==b.attained
                validate_witness(a,ref,rows,semantics)
                validate_witness(b,ref,rows,semantics)
        count+=1
    return dict(extra_instances=count,union_atlas_stratum_queries=queries,singular_inputs_rejected=skipped)


def provenance():
    result=json.loads((SNAP/'data/stage06-results.json').read_text())
    aliases={
        'paper-structured-bilevel/code/run_experiments.py':REPO/'paper-structured-bilevel/verification/stage06-author/measured-run-experiments.py',
        'paper-structured-bilevel/code/check_full_task.py':REPO/'paper-structured-bilevel/verification/stage06-author/measured-check-full-task.py'}
    for name,digest in result['input_hashes'].items():
        p=aliases.get(name,REPO/name)
        assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,(name,p)
    records=result['records']
    assert len(records)==len({(r['method'],r['name'],r['repetition']) for r in records})==60
    assert all(r['exit_code']==0 for r in records)
    grouped={}
    for r in records:grouped.setdefault((r['method'],r['name']),[]).append(r)
    for group in grouped.values():
        assert sorted(r['repetition'] for r in group)==[0,1,2]
        first=group[0]['result']
        for record in group[1:]:
            other=record['result']
            if 'outputs' in first:
                for sem in ('optimistic','pessimistic'):
                    a,b=first['outputs'][sem],other['outputs'][sem]
                    assert (a is None)==(b is None)
                    if a is not None:assert s.simplify(s.sympify(a['value'])-s.sympify(b['value']))==0 and a['attained']==b['attained']
    for r in records:
        if r['method']=='screening':
            v=r['result'];assert all(v['exact_solution_checks'][k] is True for k in ('exact_box_KKT','exact_upper_feasibility','exact_objective_evaluation'))
            if r['name']=='8':
                assert v['milp_max_linear_violation']>1e-7
                assert abs(v['tighter_tolerance_followup']['primal_minus_exact'])<1e-14
    subprocess.run([sys.executable,str(HERE/'code/summarize_experiments.py')],check=True,cwd=HERE)
    for name in ('table-full-task.tex','table-scaling.tex','table-screening.tex'):
        assert (HERE/'data'/name).read_bytes()==(SNAP/'data'/name).read_bytes()
    subprocess.run([sys.executable,str(HERE/'code/archive_inputs.py')],check=True,cwd=HERE)
    assert (HERE/'data/stage06-convex-screening-inputs.json').read_bytes()==(SNAP/'data/stage06-convex-screening-inputs.json').read_bytes()
    from run_experiments import datasets
    assert datasets()==json.loads((SNAP/'data/stage06-instances.json').read_text())
    return dict(measured_input_hashes_verified=len(result['input_hashes']),recorded_workers=60,three_repetition_groups=len(grouped),tables_reproduced=3,prepared_input_archives_reproduced=2)


if __name__=='__main__':
    result={**random_cases(),**provenance()}
    (HERE/'check_review04.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
