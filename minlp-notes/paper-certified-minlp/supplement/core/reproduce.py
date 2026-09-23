#!/usr/bin/env python3
"""Portable reproduction entry point. Run with the five checker dependencies."""
import argparse
from collections import Counter
from fractions import Fraction
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
LAB=ROOT/'lab'
sys.path.insert(0,str(LAB))


def records(path):return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def small(out):
    from certify.driver import check_certificate
    from certify import audit_solver_discrepancies as audit
    results={}
    for name,model,bundle,target in [
      ('quadratic',LAB/'certify/examples/quadratic/instance.py',LAB/'certify/examples/quadratic','1/4'),
      ('clay0204m',LAB/'instances/py/clay0204m.py',LAB/'results/cert/clay0204m','6545'),
      ('batchdes',LAB/'instances/py/batchdes.py',LAB/'results/cert/batchdes',None),
      ('risk2bpb-regenerated',LAB/'instances/py/risk2bpb.py',LAB/'results/cert_regenerated_20260913/risk2bpb',None)]:
        result=check_certificate(str(model),str(bundle),verbose=False)
        assert result['ok'],(name,result)
        if target is not None:assert Fraction(result['certified_bound_original_sense'])==Fraction(target)
        results[name]=result
    out.mkdir(parents=True,exist_ok=False)
    # Use unchanged evaluator/source comparison on the included portable layout;
    # redirect generated reports so archived evidence remains untouched.
    audit.OUT=out
    original=sys.argv
    try:
        sys.argv=['audit_solver_discrepancies','--verify-certificate']
        audit.main()
    finally:sys.argv=original
    (out/'small-replay.json').write_text(json.dumps(results,indent=2)+'\n')
    steps=ROOT/'evidence/proof-steps'
    if steps.is_dir():
        result=subprocess.run([sys.executable,str(ROOT/'experiments/audit_failed_steps.py'),'--out',str(steps)],check=True,text=True,capture_output=True)
        (out/'proof-step-checks.json').write_text(result.stdout)
    new_checks=[]
    for path in sorted((ROOT/'evidence/new-proof-step-extracts').glob('*.json')):
        record=json.loads(path.read_text());sources=record['antecedents']
        if record['reason']=='lin':
            senses=set();rhs=Fraction(0);coeff={}
            for row,q in zip(sources,map(Fraction,record['multipliers'])):
                if q and row['sense']:senses.add(row['sense']*(1 if q>0 else -1))
                rhs+=q*Fraction(row['rhs'])
                for k,v in row['coefficients'].items():coeff[k]=coeff.get(k,Fraction(0))+q*Fraction(v)
                assert row['coefficients'],'unexpected constant antecedent'
            assert senses=={-1,1} and rhs==Fraction(record['combined_rhs'])
            assert {k:v for k,v in coeff.items()if v}=={k:Fraction(v)for k,v in record['combined_coefficients'].items()}
            result='incompatible_inequality_directions'
        else:
            assert record['reason']=='uns'
            low,high=sources[1],sources[3]
            if low['sense']>0:low,high=high,low
            assert low['sense']==-1 and high['sense']==1
            assert low['coefficients']==high['coefficients']=={'4':'1'}
            assert 4 in record['integer_indices']
            assert Fraction(low['rhs'])==64 and Fraction(high['rhs'])==66
            assert not(Fraction(65)<=Fraction(low['rhs'])or Fraction(65)>=Fraction(high['rhs']))
            result='integer_activity_65_uncovered'
        new_checks.append({'instance':record['instance'],'local_failure':result})
    assert len(new_checks)==3
    (out/'new-proof-step-checks.json').write_text(json.dumps(new_checks,indent=2)+'\n')
    print('Four complete bundles, exact source/primal audits, and fifteen local proof-step extracts passed.')


def summaries(out):
    from certify.summarize import summarize
    with (LAB/'instances/instancedata.csv').open() as stream:
        metadata={r['name']:r for r in csv.DictReader(stream,delimiter=';')}
    baselines={}
    for path in (LAB/'baseline/out').glob('*.txt'):
        instance,solver=path.stem.rsplit('.',1);f=path.read_text().strip().split(',')
        try:baselines.setdefault(instance,{})[solver]={'model_status':int(f[0]),'objective':f[2]}
        except (IndexError,ValueError):pass
    hist=records(LAB/'results/cert_replay_20260913_complete.jsonl')
    result=summarize(hist,metadata,baselines,289)
    assert result['statuses']=={'rejected':92,'verified':188,'missing_artifacts':9}
    assert result['near_recorded_primal_1e4']==52 and result['recorded_primals_beyond_bound']==23
    assert result['proof_bytes_total']==38826726525
    report={'historical':{k:v for k,v in result.items() if k not in ('rows','solver_discrepancies')}}
    fresh=ROOT/'experiments/uniform-20260913/replay.jsonl'
    if fresh.exists():
        q=summarize(records(fresh),metadata,baselines,289)
        report['uniform']={k:v for k,v in q.items() if k not in ('rows','solver_discrepancies')}
    for cohort,count in [('producer-repair-20260913',12),('reporting-repair-20260914',2)]:
        saved=records(ROOT/'experiments'/cohort/'replay.jsonl')
        assert len(saved)==count and all(r['status']=='verified'for r in saved)
        report[cohort]={'saved_verified_records':count}
    report['proof_failure_audit_record_present']=True
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


def replay(cohort,out,jobs):
    if cohort=='historical':
        source=LAB/'results/cert_all.jsonl';artifacts=LAB/'results/cert'
    else:
        source=ROOT/'experiments/uniform-20260913/generation.jsonl'
        artifacts=ROOT/'experiments/uniform-20260913/replay-artifacts'
    assert artifacts.is_dir(),'Extract the bulk certificate archive beside this script first.'
    subprocess.run([sys.executable,'-m','certify.recheck','--records',str(source),
        '--outroot',str(artifacts),'--instances',str(LAB/'instances/py'),'--out',str(out.resolve()),
        '--jobs',str(jobs),'--timeout','1200'],cwd=LAB,check=True)


def verify(include_bulk):
    manifests=['core-manifest.json']+(['bulk-manifest.json']if include_bulk else[])
    count=0
    for name in manifests:
        for item in json.loads((ROOT/name).read_text())['files']:
            p=ROOT/item['path']
            if 'symlink'in item:
                import os
                assert p.is_symlink()and os.readlink(p)==item['symlink'],item['path']
            else:
                assert p.is_file()and p.stat().st_size==item['bytes'],item['path']
                h=hashlib.sha256()
                with p.open('rb')as f:
                    for b in iter(lambda:f.read(1048576),b''):h.update(b)
                assert h.hexdigest()==item['sha256'],item['path']
            count+=1
    print('Verified manifest entries:',count)


def main():
    ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest='command',required=True)
    p=sub.add_parser('verify');p.add_argument('--bulk',action='store_true')
    p=sub.add_parser('small');p.add_argument('--out',type=Path,required=True)
    p=sub.add_parser('summaries');p.add_argument('--out',type=Path,required=True)
    p=sub.add_parser('replay');p.add_argument('cohort',choices=['historical','uniform']);p.add_argument('--out',type=Path,required=True);p.add_argument('--jobs',type=int,default=1)
    args=ap.parse_args()
    if args.command=='verify':verify(args.bulk)
    elif args.command=='small':small(args.out.resolve())
    elif args.command=='summaries':summaries(args.out.resolve())
    else:replay(args.cohort,args.out,args.jobs)

if __name__=='__main__':main()
