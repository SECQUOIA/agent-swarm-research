#!/usr/bin/env python3
"""Create relative symlink view under frozen deterministic attempt selection."""
from datetime import datetime,timezone
import hashlib,json,os
from pathlib import Path
import sys
p=Path(sys.argv[1]).resolve();view=p/'replay-artifacts';view.mkdir(exist_ok=False)
selection=[]
for name in (p/'names.txt').read_text().split():
    original=p/'artifacts'/name;dest=view/name;dest.mkdir()
    candidates=[f for f in ('master_complete.vipr','master_complete_safe_failed.vipr','master_complete_default_failed.vipr') if (original/f).is_file()]
    selected=candidates[0] if candidates else None
    for target,source in [('lemma.json','lemma.json'),('master.lp','master.lp'),('master_complete.vipr',selected)]:
        if source and (original/source).is_file():(dest/target).symlink_to(os.path.relpath(original/source,dest))
    selection.append({'instance':name,'selected':selected,'other_completed_candidates':candidates[1:]})
(p/'replay-selection.json').write_text(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),
    'policy':'canonical completed proof, else safe failed, else default failed, else absent; no quality selection',
    'records':selection},indent=2)+'\n')
print('Selected',sum(x['selected'] is not None for x in selection),'of',len(selection),'attempts')
