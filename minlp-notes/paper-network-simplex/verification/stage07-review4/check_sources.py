from pathlib import Path
import json,hashlib,shutil
from statistics import median
root=Path.cwd();paper=root/'paper-network-simplex';here=Path(__file__).parent
manifest=json.loads((paper/'verification/stage07-validation.json').read_text())
for p,h in manifest['sha256'].items():assert hashlib.sha256((root/p).read_bytes()).hexdigest()==h,p
snap=paper/'process/snapshots/stage07-round01'
for folder in ['sections','tables','figures']:
    for p in (snap/folder).glob('*.tex'):assert p.read_bytes()==(paper/folder/p.name).read_bytes()
for name in ['main.tex','README.md','references.bib']:assert (snap/name).read_bytes()==(paper/name).read_bytes()
bench=json.loads((paper/'verification/stage06-benchmarks.json').read_text())
count=0
for kind in ('flat','membership','optimization'):
    for case in bench[kind]:
        for method,summary in case['summary'].items():
            for key,out in summary.items():
                raw=[r['measurements'][method][key] for r in case['runs']]
                assert out==dict(minimum=min(raw),median=median(raw),maximum=max(raw));count+=1
local=bench['optimization'][2]
for method,number in [('full',7215),('global',7215),('initial',495),('eliminated',367)]: assert local['warmup'][method]['stats']['variables']==number
assert 29<1000*local['summary']['full']['total_seconds']['median']<31
assert 9<1000*local['summary']['initial']['total_seconds']['median']<11
assert local['summary']['initial']['total_seconds']['median']<local['summary']['eliminated']['total_seconds']['median']
build=here/'build';build.mkdir(exist_ok=True)
for name in ['main.tex','references.bib']:shutil.copy2(snap/name,build/name)
for name in ['sections','tables','figures']:shutil.copytree(snap/name,build/name,dirs_exist_ok=True)
out=dict(status='PASS',hashes=len(manifest['sha256']),timing_summaries=count,introduction_counts_and_times='PASS')
(here/'sources.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
