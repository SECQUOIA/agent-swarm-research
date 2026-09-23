#!/usr/bin/env python3
"""Choose exact strongest bounds from checked evidence, without new optimization."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import sys


def main():
    p=argparse.ArgumentParser();p.add_argument('--lab',type=Path,required=True);p.add_argument('--paper',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    lab=a.lab.resolve();paper=a.paper.resolve();a.out.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(lab))
    from certify.rational_text import parse_rational_text as Q,format_rational_text as fmt
    sources=[('historical',lab/'results/cert_replay_20260913_complete.jsonl'),('primary',paper/'experiments/uniform-20260913/replay.jsonl'),('producer-repair',paper/'experiments/producer-repair-20260913/replay.jsonl'),('reporting-repair',paper/'experiments/reporting-repair-20260914/replay.jsonl')]
    def portable(path):
        # Frozen records retain original absolute provenance paths. Map those
        # names to the supplement layout without accessing the old filesystem.
        text=str(path)
        for marker,prefix in [('/code/minlp_solver_lab/','lab/'),('/paper-certified-minlp/','')]:
            if marker in text:return prefix+text.split(marker,1)[1]
        path=Path(text)
        if path.is_relative_to(lab):return 'lab/'+str(path.relative_to(lab))
        return str(path.relative_to(paper))
    candidates={};chosen={};cohort_counts={}
    for cohort,path in sources:
        records=[json.loads(x)for x in path.read_text().splitlines()if x.strip()];cohort_counts[cohort]=dict(Counter(r['status']for r in records))
        for r in records:
            if r['status']!='verified':continue
            assert r.get('schema')==1 and r['report']['ok']and r['report']['proof']['ok']
            n=r['instance'];sense=r['sense'];value=Q(r['certified_bound_original_sense']);model=r['artifacts']['instance']['sha256']
            row={'instance':n,'sense':sense,'model_sha256':model,'cohort':cohort,'reporting_target':r.get('reporting_target'),
                 'bound_original_sense':fmt(value),'normalized_lower_bound':fmt(sense*value),
                 'model_path':portable(r['artifacts']['instance']['path']),
                 'lemma_path':portable(r['artifacts']['lemma']['path']),'master_path':portable(r['artifacts']['master']['path']),
                 'proof_path':portable(r['artifacts']['proof']['path']),'proof_sha256':r['artifacts']['proof']['sha256'],'proof_bytes':r['artifacts']['proof']['bytes']}
            if n in chosen:assert (sense,model)==(chosen[n]['sense'],chosen[n]['model_sha256'])
            candidates.setdefault(n,[]).append(row)
            if n not in chosen or sense*value>Q(chosen[n]['normalized_lower_bound']):chosen[n]=row
    for n,rows in candidates.items():assert all(Q(r['normalized_lower_bound'])<=Q(chosen[n]['normalized_lower_bound'])for r in rows)
    selected=[chosen[n]for n in sorted(chosen)]
    report={'selection':'Strongest exact signed-normalized bound per identical model SHA and objective sense; exact ties prefer historical, then primary, producer-repair, reporting-repair in saved record order.',
            'interpretation':'Descriptive merged collection; not a uniform performance experiment. No reference primal or unverified master solution is used.',
            'candidate_verified_records':sum(map(len,candidates.values())),'models':len(chosen),'cohort_statuses':cohort_counts,
            'selected_by_cohort':dict(Counter(r['cohort']for r in selected)),'bounds':selected,'candidates':candidates}
    (a.out/'bound-catalog.json').write_text(json.dumps(report,indent=2)+'\n')
    with(a.out/'bound-catalog.csv').open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=list(selected[0]));w.writeheader();w.writerows(selected)
    (a.out/'bound-catalog-text.tex').write_text(f"The descriptive merged catalogue contains verified bounds for {len(chosen)} distinct loaded models. It chooses the strongest exact normalized lower bound among {sum(map(len,candidates.values()))} accepted records from the historical, primary, producer-repair, and reporting-repair evidence, requiring identical model SHA-256 and objective sense for every comparison. Exact ties use a fixed cohort order. Each entry identifies its original-sense bound, complete proof, source cohort, and hashes. This union is a reusable bound collection; its coverage is not attributed to the uniform search budget.\n")
    print(json.dumps({k:v for k,v in report.items()if k not in('bounds','candidates')},indent=2))

if __name__=='__main__':main()
