#!/usr/bin/env python3
"""Replay every observed post-proof reporting failure from the frozen campaigns."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from run_uniform import digest


def rows(path):return [json.loads(x)for x in path.read_text().splitlines()if x.strip()]


def main():
    p=argparse.ArgumentParser();p.add_argument('--lab',type=Path,required=True);p.add_argument('--primary',type=Path,required=True);p.add_argument('--secondary',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    lab=a.lab.resolve();primary=a.primary.resolve();secondary=a.secondary.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    audited=[];targets=[]
    for r in rows(primary/'replay.jsonl'):
        if r['status']!='rejected':continue
        affected='integer string conversion' in str(r.get('report',{}).get('checks',[]))
        audited.append({'cohort':'primary','instance':r['instance'],'status':r['status'],'reporting_boundary':affected,'checks':r.get('report',{}).get('checks',[])})
        if affected:
            assert r['report']['proof']['ok']
            targets.append({'id':'primary-'+r['instance'],'instance':r['instance'],'cohort':'primary','directory':primary/'replay-artifacts'/r['instance'],'proof':Path(r['artifacts']['proof']['path'])})
    for r in rows(secondary/'generation.jsonl'):
        for attempt in r.get('scip_attempts',[]):
            affected='integer string conversion' in str(attempt.get('checker_detail',[]))
            audited.append({'cohort':'producer-repair','instance':r['instance'],'attempt':attempt['label'],'status':attempt.get('checker',attempt.get('viprchk')),'reporting_boundary':affected,'checks':attempt.get('checker_detail',[])})
            if affected:
                directory=secondary/'artifacts'/r['instance'];proof=directory/f"master_complete_{attempt['label']}_failed.vipr"
                assert proof.is_file()
                targets.append({'id':'producer-repair-'+attempt['label']+'-'+r['instance'],'instance':r['instance'],'cohort':'producer-repair','directory':directory,'proof':proof})
    assert len([r for r in audited if r['cohort']=='primary'])==19
    assert len(targets)==2 and {r['instance']for r in targets}=={'tls12'}
    sources=sorted((lab/'certify').glob('*.py'))+sorted((lab/'lbesh').glob('*.py'))
    protocol={'frozen_utc':datetime.now(timezone.utc).isoformat(),'purpose':'Complete replays after exact report parse/serialization repair; no numerical generation or performance comparison','target_count':len(targets),'distinct_models':len({r['instance']for r in targets}),'timeout_seconds_per_target':1200,'concurrent_targets':2,
              'selection':'All primary rejected reports and all secondary attempt reports were inspected for the observed integer-string-conversion boundary; every affected completed candidate is replayed.',
              'audited_records':audited,'sources':[digest(p)for p in sources],'wrapper':digest(__file__),
              'targets':[{'id':r['id'],'instance':r['instance'],'cohort':r['cohort'],'proof':digest(r['proof']),'model':digest(lab/'instances/py'/f"{r['instance']}.py")}for r in targets]}
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
    for r in targets:
        target=out/'targets'/r['id'];bundle=target/'artifacts'/r['instance'];bundle.mkdir(parents=True)
        for filename,source in [('lemma.json',r['directory']/'lemma.json'),('master.lp',r['directory']/'master.lp'),('master_complete.vipr',r['proof'])]:
            (bundle/filename).symlink_to(os.path.relpath(source.resolve(),bundle))
        (target/'records.jsonl').write_text(json.dumps({'instance':r['instance'],'status':'post-proof reporting error'})+'\n')
    t=time.monotonic();start=datetime.now(timezone.utc).isoformat()
    def run(r):
        target=out/'targets'/r['id'];command=[sys.executable,'-m','certify.recheck','--records',str(target/'records.jsonl'),'--outroot',str(target/'artifacts'),'--instances',str(lab/'instances/py'),'--out',str(target/'replay.jsonl'),'--jobs','1','--timeout','1200']
        with(target/'replay.log').open('x')as log:result=subprocess.run(command,cwd=lab,stdout=log,stderr=subprocess.STDOUT)
        assert result.returncode==0
        record=rows(target/'replay.jsonl')[0];record['reporting_target']=r['id'];return record
    with ThreadPoolExecutor(max_workers=2)as pool:result=list(pool.map(run,targets))
    for i,r in enumerate(result):r['record_index']=i
    (out/'replay.jsonl').write_text(''.join(json.dumps(r)+'\n'for r in result))
    timing={'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t}
    (out/'replay-timing.json').write_text(json.dumps(timing,indent=2)+'\n')
    assert all(digest(r['path'])['sha256']==r['sha256']for r in protocol['sources'])
    (out/'postreplay-integrity.json').write_text(json.dumps({'all_checker_sources_unchanged_during_replay':True},indent=2)+'\n')
    print(json.dumps({'targets':[{'id':r['reporting_target'],'status':r['status'],'checker_seconds':r['checker_seconds']}for r in result],**timing},indent=2))

if __name__=='__main__':main()
