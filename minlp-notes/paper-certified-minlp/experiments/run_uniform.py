#!/usr/bin/env python3
"""Frozen paper campaign; observers record timings without changing proof rules."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time


def digest(path):
    path=Path(path)
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1048576),b''):h.update(block)
    return {'path':str(path.resolve()),'bytes':path.stat().st_size,'sha256':h.hexdigest()}


def now():return datetime.now(timezone.utc).isoformat()


def worker(args):
    lab=Path(args.lab).resolve();out=Path(args.out).resolve();case=out/'artifacts'/args.name
    case.mkdir(parents=True,exist_ok=True)
    sys.path.insert(0,str(lab))
    import certify.run_all as producer
    import certify.vipr as kernel
    events=(case/'phase-events.jsonl').open('x',buffering=1)
    ordinal=0
    def emit(**event):
        events.write(json.dumps({'utc':now(),**event},default=str)+'\n');events.flush()
    original_run=subprocess.run
    def timed_run(command,*pos,**kw):
        nonlocal ordinal
        tool=Path(str(command[0])).name if isinstance(command,(list,tuple)) else 'shell'
        if tool not in ('scip','viprcomp','viprchk'):return original_run(command,*pos,**kw)
        command=list(command)
        if tool=='scip':command[1:1]=['-c',f'set load {Path(args.settings).resolve()}']
        ordinal+=1;idx=ordinal;t=time.monotonic()
        emit(event='start',phase=tool,index=idx,command=command)
        try:
            result=original_run(command,*pos,**kw)
            for stream in ('stdout','stderr'):
                value=getattr(result,stream,None)
                if value is not None:(case/f'tool-{idx:03d}-{tool}.{stream}').write_text(value if isinstance(value,str) else value.decode(errors='replace'))
            emit(event='end',phase=tool,index=idx,seconds=time.monotonic()-t,returncode=result.returncode)
            return result
        except BaseException as exc:
            emit(event='end',phase=tool,index=idx,seconds=time.monotonic()-t,error=repr(exc));raise
    original_validate=kernel.validate_vipr
    def timed_validate(path):
        nonlocal ordinal
        ordinal+=1;idx=ordinal;t=time.monotonic();emit(event='start',phase='internal_proof_replay',index=idx)
        try:
            result=original_validate(path)
            emit(event='end',phase='internal_proof_replay',index=idx,seconds=time.monotonic()-t,ok=result.get('ok'))
            return result
        except BaseException as exc:
            emit(event='end',phase='internal_proof_replay',index=idx,seconds=time.monotonic()-t,error=repr(exc));raise
    subprocess.run=timed_run;kernel.validate_vipr=timed_validate
    # run_instance refuses nonempty output folders. Its temporary output is a
    # sibling; move observation files only after the producer starts normally.
    events.close();(case/'phase-events.jsonl').unlink();case.rmdir()
    eventdir=out/'events';eventdir.mkdir(exist_ok=True)
    events=(eventdir/f'{args.name}.jsonl').open('x',buffering=1)
    # Tool output is written once run_instance has created its artifact folder.
    emit(event='start',phase='pipeline')
    t=time.monotonic()
    result=producer.run_instance(args.name,str(out/'artifacts'),30,30,1,
                                 str(Path(args.scip_bin).resolve()),str(lab/'instances/py'))
    emit(event='end',phase='pipeline',seconds=time.monotonic()-t,status=result.get('status'))
    result['observer_events']=str(Path('events')/f'{args.name}.jsonl')
    (out/'worker-reports'/f'{args.name}.json').write_text(json.dumps(result,indent=2,default=str))
    events.close()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--lab',required=True);ap.add_argument('--out',required=True)
    ap.add_argument('--scip-bin',required=True);ap.add_argument('--ipopt',required=True)
    ap.add_argument('--settings',default=str(Path(__file__).with_name('scip-uniform.set')))
    ap.add_argument('--worker',action='store_true');ap.add_argument('--name')
    args=ap.parse_args()
    for v in ('lab','out','scip_bin','ipopt','settings'):setattr(args,v,str(Path(getattr(args,v)).resolve()))
    os.environ['PATH']=str(Path(args.ipopt).parent)+os.pathsep+os.environ.get('PATH','')
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
    if args.worker:worker(args);return
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    for directory in ('artifacts','events','worker-reports','worker-logs'):(out/directory).mkdir()
    lab=Path(args.lab)
    historical=[json.loads(line) for line in (lab/'results/cert_all.jsonl').read_text().splitlines() if line.strip()]
    names=sorted(row['instance'] for row in historical)
    assert len(names)==len(set(names))==289
    (out/'names.txt').write_text(''.join(n+'\n' for n in names))
    sources=sorted((lab/'certify').glob('*.py'))+sorted((lab/'lbesh').glob('*.py'))
    versions={p:importlib.metadata.version(p) for p in ('pyomo','numpy','sympy','mpmath','python-flint','gurobipy')}
    manifest={
      'schema':1,'frozen_utc':now(),'cohort_size':289,'cohort':'all unique historical cert_all.jsonl attempts, lexicographic order',
      'oa_search_seconds':30,'scip_search_seconds_per_attempt':30,'max_scip_attempts':2,
      'requested_threads':1,'workers':6,'outer_worker_cap_seconds':360,'separate_replay_cap_seconds':1200,
      'attempt_policy':'default then conservative fallback after unsuccessful complete checking; unchanged run_all.run_instance',
      'hard_cap_policy':'360 seconds from worker launch; kill entire process group; retain partial artifacts and events; no retries',
      'analysis_policy':'all289 denominator; separate production and independent replay; exact signed reference distances; no solver speed ranking',
      'python':sys.version,'platform':platform.platform(),'cpu':subprocess.run(['lscpu'],capture_output=True,text=True).stdout,
      'memory':Path('/proc/meminfo').read_text(),'package_versions':versions,
      'environment_threads':{k:os.environ[k] for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')},
      'wrapper':digest(__file__),'settings':digest(args.settings),'historical_records':digest(lab/'results/cert_all.jsonl'),
      'model_sources':[digest(lab/'instances/py'/f'{n}.py') for n in names],
      'sources':[digest(p) for p in sources],
      'tools':[digest(Path(args.scip_bin)/n) for n in ('scip','viprcomp','viprchk')]+[digest(args.ipopt)],
      'note':'phase observers time existing subprocess calls and internal proof replay; SCIP loads the documented thread/settings file; proof arithmetic unchanged.'}
    (out/'protocol.json').write_text(json.dumps(manifest,indent=2)+'\n')
    t0=time.monotonic();start=now()
    def run(name):
        t=time.monotonic()
        cmd=[sys.executable,str(Path(__file__).resolve()),'--worker','--name',name,
             '--lab',args.lab,'--out',args.out,'--scip-bin',args.scip_bin,'--ipopt',args.ipopt,'--settings',args.settings]
        with (out/'worker-logs'/f'{name}.log').open('w') as log:
            process=subprocess.Popen(cmd,stdout=log,stderr=log,start_new_session=True)
            status=None
            try:code=process.wait(timeout=360)
            except subprocess.TimeoutExpired:
                status='hard_timeout';os.killpg(process.pid,signal.SIGKILL);code=process.wait()
            finally:
                try:os.killpg(process.pid,signal.SIGKILL)
                except ProcessLookupError:pass
        report=out/'worker-reports'/f'{name}.json'
        if status=='hard_timeout':result={'instance':name,'status':status}
        elif code==0 and report.is_file():result=json.loads(report.read_text())
        else:result={'instance':name,'status':'worker_error','returncode':code}
        result['worker_wall_seconds']=time.monotonic()-t
        return result
    with (out/'generation.jsonl').open('x',buffering=1) as records,ThreadPoolExecutor(max_workers=6) as pool:
        futures={pool.submit(run,name):name for name in names}
        for future in as_completed(futures):
            result=future.result();records.write(json.dumps(result,default=str)+'\n');records.flush()
            print(result['instance'],result['status'],round(result['worker_wall_seconds'],2),flush=True)
    (out/'timing.json').write_text(json.dumps({'started_utc':start,'finished_utc':now(),'wall_seconds':time.monotonic()-t0},indent=2)+'\n')

if __name__=='__main__':main()
