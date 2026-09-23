#!/usr/bin/env python3
"""Recreate the separately labeled producer/reporting repair summaries."""
import argparse
from collections import Counter
import json
from pathlib import Path


def rows(path):return [json.loads(x)for x in path.read_text().splitlines()if x.strip()]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--experiments',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    v2=a.experiments/'producer-repair-20260913';v3=a.experiments/'reporting-repair-20260914'
    gen=rows(v2/'generation.jsonl');rep=rows(v2/'replay.jsonl');targets=rows(v3/'replay.jsonl')
    assert len(gen)==len(rep)==12 and len(targets)==2
    assert all(r['status']=='verified'for r in gen+rep+targets)
    tg=json.loads((v2/'timing.json').read_text())['wall_seconds']
    tr=json.loads((v2/'replay-timing.json').read_text())['wall_seconds']
    tt=json.loads((v3/'replay-timing.json').read_text())['wall_seconds']
    summary={'producer_repair':{'generation_statuses':dict(Counter(r['status']for r in gen)),'replay_statuses':dict(Counter(r['status']for r in rep)),'generation_wall_seconds':tg,'replay_wall_seconds':tr},'reporting_repair':{'replay_statuses':dict(Counter(r['status']for r in targets)),'wall_seconds':tt},'final_tests':161}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'repair-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (a.out/'repair-results-text.tex').write_text(f'''All twelve producer-repair runs returned verified output, and all twelve
selected bundles passed separate replay. Generation took {tg:.3f} seconds of
elapsed time and replay took {tr:.3f} seconds. Auditing all nineteen primary
rejections and all secondary attempt reports identified exactly two completed
proofs affected by the subsequent reporting defect, both for \\texttt{{tls12}}.
With the third source version, both passed full replay in a separate
{tt:.3f}-second cohort, without further optimization. The frozen primary replay
counts remain 203 verified and 19 rejected; the corrected reporting layer
accepts one additional primary bundle. The supplement preserves the sources,
records, and completed attempts for each version. These targeted repairs do
not constitute a second uniform experiment or replace its denominator.
''')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
