from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re,shutil,subprocess
from statistics import median
root=Path.cwd();paper=root/'paper-network-simplex';out=paper/'verification/stage07-review5';snapshot=paper/'process/snapshots/stage07-round01'
v=json.loads((paper/'verification/stage07-validation.json').read_text())
for path,h in v['sha256'].items():assert hashlib.sha256((root/path).read_bytes()).hexdigest()==h,path
alltex='\n'.join(p.read_text() for p in snapshot.rglob('*.tex'))
labels=re.findall(r'\\label\{([^}]+)\}',alltex);assert len(labels)==len(set(labels))
for group in re.findall(r'\\(?:c|C|eq)?ref\{([^}]+)\}',alltex):
 for label in group.split(','):assert label in labels,label
bib=set(re.findall(r'@\w+\{([^,]+),',(snapshot/'references.bib').read_text()))
for group in re.findall(r'\\cite\w*(?:\[[^]]*\])*\{([^}]+)\}',alltex):
 for key in group.split(','):assert key in bib,key
for path in re.findall(r'\]\(([^)]+)\)',(paper/'README.md').read_text()):
 if '://' not in path:assert (paper/path.split('#')[0]).exists(),path
raw=json.loads((paper/'verification/stage06-benchmarks.json').read_text());summaries=0
for case in raw['flat']+raw['membership']+raw['optimization']:
 for stats in case['summary'].values():summaries+=len(stats)
 for method,stats in case['summary'].items():
  for field,values in stats.items():
   samples=[run['measurements'][method][field] for run in case['runs']]
   assert values==dict(minimum=min(samples),median=median(samples),maximum=max(samples))
control=raw['optimization'][2]
assert [control['warmup'][s]['stats']['variables'] for s in ('full','global','initial','eliminated')]==[7215,7215,495,367]
assert round(1000*control['summary']['full']['total_seconds']['median'])==30
assert round(1000*control['summary']['initial']['total_seconds']['median'])==10
# The author check writes next to itself, so run only a private copy.
shutil.copy(paper/'verification/stage07/integral-hull.py',out/'integral-hull-author-copy.py')
answer=subprocess.run(['/home/sgusev/miniconda3/envs/minlp-notes/bin/python',str(out/'integral-hull-author-copy.py')],capture_output=True,text=True)
assert answer.returncode==0,answer.stderr
(out/'integral-hull-author-copy.txt').write_text(answer.stdout)
print(json.dumps(dict(status='PASS',hashes=len(v['sha256']),labels=len(labels),bibliography_keys=len(bib),timing_summaries=summaries,all_new_intro_metrics=True,author_exact_check=json.loads(answer.stdout)),indent=2))
