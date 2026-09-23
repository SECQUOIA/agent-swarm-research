#!/usr/bin/env python3
"""Exact, complete-denominator paper tables from frozen campaign records."""
import argparse
from collections import Counter
import csv
import hashlib
from fractions import Fraction
import json
from pathlib import Path
import statistics
import sys


def rows(path):return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
def dump(path,data):path.write_text(json.dumps(data,indent=2)+'\n')
def failures(record):
    if record['status']!='rejected':return record['status']
    checks=record.get('report',{}).get('checks',[])
    text=' '.join(str(c)for c in checks)
    if any(c[0]=='lemmas' and c[2]=='FAIL'for c in checks)or 'ValueError: cut 'in text:return 'cut'
    if any(c[0]=='vipr_exact_replay' and c[2]=='FAIL'for c in checks):return 'proof_inference'
    if 'uncertified' in text or 'domain' in text:return 'domain_or_curvature'
    return 'other_rejection'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--lab',type=Path,required=True);ap.add_argument('--campaign',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    lab=args.lab.resolve();campaign=args.campaign.resolve();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    inputs=[Path(__file__).resolve(),lab/'certify/summarize.py',lab/'instances/instancedata.csv',lab/'results/cert_replay_20260913_complete.jsonl',campaign/'replay.jsonl',campaign/'generation.jsonl',campaign/'replay-selection.json']+sorted((lab/'baseline/out').glob('*.txt'))
    input_hashes=[{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in inputs]
    sys.path.insert(0,str(lab));from certify.summarize import summarize
    with (lab/'instances/instancedata.csv').open()as f:metadata={r['name']:r for r in csv.DictReader(f,delimiter=';')}
    base={}
    for p in(lab/'baseline/out').glob('*.txt'):
        n,s=p.stem.rsplit('.',1);f=p.read_text().strip().split(',')
        try:base.setdefault(n,{})[s]={'model_status':int(f[0]),'objective':f[2]}
        except(ValueError,IndexError):pass
    hist=rows(lab/'results/cert_replay_20260913_complete.jsonl');fresh=rows(campaign/'replay.jsonl');prod=rows(campaign/'generation.jsonl')
    expected=set((campaign/'names.txt').read_text().split())
    for data in(hist,fresh,prod):assert len(data)==289 and {r['instance']for r in data}==expected
    summaries={key:summarize(data,metadata,base,289)for key,data in [('historical',hist),('uniform',fresh)]}
    for key,data in [('historical',hist),('uniform',fresh)]:
        s=summaries[key];accepted=[r for r in data if r['status']=='verified'];times=[r['checker_seconds']for r in accepted];sizes=[r['artifacts']['proof']['bytes']for r in accepted]
        s['failure_classes']=dict(Counter(failures(r)for r in data))
        s['checker_seconds_all_records']=sum(r.get('checker_seconds',0)for r in data)
        s['checker_seconds_median_accepted']=statistics.median(times)if times else None
        s['proof_bytes_median_accepted']=statistics.median(sizes)if sizes else None
        s['proof_bytes_max_accepted']=max(sizes,default=0)
        s['proof_bytes_all_present']=sum(r.get('artifacts',{}).get('proof',{}).get('bytes',0)for r in data)
        s['derivations_accepted']=sum(r['report']['proof']['derivations']for r in accepted)
        with(out/f'{key}-cases.csv').open('w',newline='')as f:
            cols=['instance','status','failure_class','bound','reference','signed_difference','normalized_difference','checker_seconds','proof_bytes']
            w=csv.DictWriter(f,fieldnames=cols);w.writeheader();look={r['instance']:r for r in s['rows']}
            for r in sorted(data,key=lambda x:x['instance']):
                c=look.get(r['instance'],{}).get('recorded_primal_comparison')or{}
                w.writerow({'instance':r['instance'],'status':r['status'],'failure_class':failures(r),'bound':r.get('certified_bound_original_sense'),
                    'reference':c.get('reference'),'signed_difference':c.get('signed_difference'),'normalized_difference':c.get('normalized_difference'),
                    'checker_seconds':r.get('checker_seconds'),'proof_bytes':r.get('artifacts',{}).get('proof',{}).get('bytes')})
    lookup={r['instance']:r for r in prod};selection=json.loads((campaign/'replay-selection.json').read_text())['records'];sel={r['instance']:r for r in selection}
    completed=[r for r in fresh if r['status']=='verified']
    production={'statuses':dict(Counter(r['status']for r in prod)),
      'worker_wall_seconds_sum':sum(r['worker_wall_seconds']for r in prod),
      'worker_wall_seconds_median':statistics.median(r['worker_wall_seconds']for r in prod),
      'worker_wall_seconds_max':max(r['worker_wall_seconds']for r in prod),
      'generation_timing':json.loads((campaign/'timing.json').read_text()),
      'replay_timing':json.loads((campaign/'replay-timing.json').read_text()),
      'replay_verified_by_generation_status':dict(Counter(lookup[r['instance']]['status']for r in completed)),
      'replay_verified_by_candidate':dict(Counter(sel[r['instance']]['selected']for r in completed)),
      'all_selected_candidates':dict(Counter(str(r['selected'])for r in selection)),
      'scip_attempts':dict(Counter(a['label']for r in prod for a in r.get('scip_attempts',[]))),
      'producer_oa_seconds_sum':sum(r.get('producer',{}).get('oa',{}).get('time',0)for r in prod),
      'producer_master_generation_seconds_sum':sum(r.get('producer',{}).get('time_total',0)for r in prod),
      'phase_seconds_completed_calls':{},'phase_started_calls':{},'phase_ended_calls':{},
      'phase_note':'Only observed completed calls contribute seconds; interrupted calls have starts without ends. Producer OA fields absent from outer-timeout reports are not reconstructed.'}
    phases=Counter();starts=Counter();ends=Counter()
    for p in(campaign/'events').glob('*.jsonl'):
        for e in rows(p):
            if e['event']=='start':starts[e['phase']]+=1
            if e['event']=='end':ends[e['phase']]+=1;phases[e['phase']]+=e.get('seconds',0)
    production.update(phase_seconds_completed_calls=dict(phases),phase_started_calls=dict(starts),phase_ended_calls=dict(ends))
    histv={r['instance']:r for r in hist if r['status']=='verified'};freshv={r['instance']:r for r in completed};overlap=set(histv)&set(freshv);changes=[]
    for n in sorted(overlap):
        h,f=histv[n],freshv[n];assert h['sense']==f['sense'];q=f['sense']*(Fraction(f['certified_bound_original_sense'])-Fraction(h['certified_bound_original_sense']))
        changes.append({'instance':n,'signed_improvement':str(q),'comparison':'stronger'if q>0 else'weaker'if q<0 else'equal'})
    production['historical_overlap']={'both_verified':len(overlap),'only_historical':len(set(histv)-set(freshv)),'only_uniform':len(set(freshv)-set(histv)),'bound_changes':dict(Counter(r['comparison']for r in changes)),'cases':changes}
    dump(out/'production-analysis.json',production)
    for k,v in summaries.items():dump(out/f'{k}-summary.json',v)
    table=['\\begin{table}[tb]','\\centering','\\caption{Complete replay outcomes and exact reference comparisons. Both denominators are 289; generation outcomes are reported separately in the text. Historical replay also used external corroboration. Reference rows count only verified bounds; $d$ is the signed normalized difference from an unverified reference (Section~\\ref{sec:reference-comparison}).}','\\label{tab:campaign-results}','\\begin{tabular}{lrr}','\\toprule','Quantity & Historical archive & Uniform-run artifacts \\\\','\\midrule']
    for label,key in [('Verified','verified'),('Near reference: $0\\le d\\le10^{-4}$','near_recorded_primal_1e4'),('Near reference: $0\\le d\\le10^{-2}$','near_recorded_primal_1e2'),('Negative reference difference','recorded_primals_beyond_bound')]:table.append(f"{label} & {summaries['historical'][key]} & {summaries['uniform'][key]} \\\\")
    for label,key in [('Rejected','rejected'),('Missing complete artifacts','missing_artifacts'),('Timed out during replay','timeout'),('Other replay errors','checker_error')]:table.append(f"{label} & {summaries['historical']['statuses'].get(key,0)} & {summaries['uniform']['statuses'].get(key,0)} \\\\")
    table+=['\\bottomrule','\\end{tabular}','\\end{table}'];(out/'campaign-results.tex').write_text('\n'.join(table)+'\n')
    s=summaries['uniform'];p=production;status=p['statuses'];verified_by=p['replay_verified_by_generation_status'];candidate=p['replay_verified_by_candidate']
    sentence=(f"The uniform generation records {status.get('verified',0)} completed accepted productions, "
      f"{status.get('producer_error',0)} producer errors, {status.get('rejected',0)} unsuccessful completed-check attempts, "
      f"{status.get('hard_timeout',0)} outer timeouts, and {status.get('worker_error',0)} worker errors. "
      f"Its elapsed time is {p['generation_timing']['wall_seconds']:,.3f} seconds. "
      f"Separate replay accepts {s['verified']} bounds, rejects {s['statuses'].get('rejected',0)} bundles, "
      f"and finds {s['statuses'].get('missing_artifacts',0)} incomplete bundles. "
      f"Of its accepted bounds, {verified_by.get('hard_timeout',0)} come from outer-timed-out production, "
      f"{verified_by.get('worker_error',0)} from worker errors, and {verified_by.get('rejected',0)} from producer rejections; "
      f"{sum(v for k,v in candidate.items()if k!='master_complete.vipr')} use a retained failed-attempt completed proof. "
      f"Accepted proofs occupy {s['proof_bytes_total']:,} bytes and contain {s['derivations_accepted']:,} derivations. "
      f"Their summed and median checking costs are {s['checker_seconds_total']:,.3f} and {s['checker_seconds_median_accepted']:.3f} seconds, respectively; "
      f"the maximum is {s['checker_seconds_max']:.3f} seconds. "
      f"All-record checking costs sum to {s['checker_seconds_all_records']:,.3f} seconds and separate replay elapsed time is "
      f"{p['replay_timing']['wall_seconds']:,.3f} seconds. "
      "These observations characterize this fixed protocol, including its unsuccessful attempts; they do not estimate asymptotic coverage or establish superiority over another solver.\n")
    phase_table=['\\begin{table}[tb]','\\centering','\\caption{Observed in-generation calls in the uniform campaign. Sums include completed calls only; starts without ends are interrupted observations. SCIP times cover the process invocation, not just search. These rows are separate from full pipeline and later replay times.}','\\label{tab:generation-phases}','\\begin{tabular}{lrrr}','\\toprule','Phase & Started & Ended & Seconds (sum) \\\\','\\midrule']
    for key,label in [('scip','SCIP process'),('viprcomp','Proof completion'),('viprchk','External proof check'),('internal_proof_replay','Internal proof replay')]:
        phase_table.append(f"{label} & {starts[key]} & {ends[key]} & {phases[key]:,.3f}" + ' ' + chr(92)*2)
    phase_table+=['\\bottomrule','\\end{tabular}','\\end{table}']
    (out/'generation-phases.tex').write_text('\n'.join(phase_table)+'\n')
    (out/'uniform-results-text.tex').write_text(sentence)
    assert all(hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256']for r in input_hashes)
    dump(out/'analysis-inputs.json',{'all_inputs_stable_during_analysis':True,'files':input_hashes})
    print(json.dumps({k:{x:v[x]for x in ('statuses','verified','failure_classes','proof_bytes_total','checker_seconds_total')}for k,v in summaries.items()},indent=2))

if __name__=='__main__':main()
