#!/usr/bin/env python3
"""Verify frozen producer inputs after a campaign; no optimization calls."""
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
import sys

def recorded_path(value, root):
    """Bind a public repository path to the checkout used for this check."""
    path=Path(value)
    try:
        relative=path.relative_to('/workspace/minlp-notes')
    except ValueError:
        return path
    return root/relative


root=Path(__file__).resolve().parent.parent.parent
p=Path(sys.argv[1]);protocol=json.loads((p/'protocol.json').read_text())
items=[protocol['wrapper'],protocol['settings'],protocol['historical_records']]+protocol['sources']+protocol['model_sources']+protocol['tools']
results=[]
for item in items:
    path=recorded_path(item['path'],root);h=hashlib.sha256()
    with path.open('rb') as stream:
        for b in iter(lambda:stream.read(1048576),b''):h.update(b)
    results.append({'path':item['path'],'sha256':h.hexdigest(),'matches':h.hexdigest()==item['sha256'] and path.stat().st_size==item['bytes']})
r={'checked_utc':datetime.now(timezone.utc).isoformat(),'all_frozen_bytes_unchanged':all(i['matches'] for i in results),'files':results}
(p/'postgeneration-integrity.json').write_text(json.dumps(r,indent=2)+'\n')
assert r['all_frozen_bytes_unchanged']
print('Unchanged frozen files:',len(results))
