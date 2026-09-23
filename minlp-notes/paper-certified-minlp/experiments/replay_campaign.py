#!/usr/bin/env python3
"""Time a complete, separate kernel replay of a selected campaign view."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import subprocess
import sys
import time


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--lab',type=Path,required=True);ap.add_argument('--campaign',type=Path,required=True);a=ap.parse_args()
    lab=a.lab.resolve();run=a.campaign.resolve();assert(run/'replay-selection.json').exists()
    assert not(run/'replay.jsonl').exists()
    command=[sys.executable,'-m','certify.recheck','--records',str(run/'generation.jsonl'),'--outroot',str(run/'replay-artifacts'),'--instances',str(lab/'instances/py'),'--out',str(run/'replay.jsonl'),'--jobs','6','--timeout','1200']
    start=datetime.now(timezone.utc).isoformat();t=time.monotonic()
    with(run/'replay.log').open('x')as log:r=subprocess.run(command,cwd=lab,stdout=log,stderr=subprocess.STDOUT)
    timing={'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'returncode':r.returncode,'command':command,'external_corroboration':False}
    (run/'replay-timing.json').write_text(json.dumps(timing,indent=2)+'\n')
    assert r.returncode==0,timing
    records=[json.loads(x)for x in(run/'replay.jsonl').read_text().splitlines()]
    names=(run/'names.txt').read_text().split();assert len(records)==len(names)and{r['instance']for r in records}==set(names)
    from collections import Counter
    print(json.dumps({'records':len(records),'statuses':dict(Counter(r['status']for r in records)),**timing},indent=2))

if __name__=='__main__':main()
