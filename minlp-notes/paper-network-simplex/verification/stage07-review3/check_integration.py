from pathlib import Path
import hashlib,json,re,collections
P=Path('paper-network-simplex');E=P/'verification/stage07-review3';S=P/'process/snapshots/stage07-round01';A=P/'process/snapshots/stage06-accepted'
v=json.loads((P/'verification/stage07-validation.json').read_text());print(v.keys())
key='sha256' if 'sha256' in v else 'source_hashes'
for name,digest in v[key].items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
for p in (S/'tables').glob('*.tex'):
 assert p.read_bytes()==(A/'tables'/p.name).read_bytes()
 assert p.read_bytes()==(E/'build/tables'/p.name).read_bytes()
for name in ('02-compression.tex','03-structured-oracles.tex','04-bounded-rank.tex','05-universality.tex'):
 assert (S/'sections'/name).read_bytes()==(A/'sections'/name).read_bytes()
inputs={}
def visit(p):
 assert p.exists() and p not in inputs,p
 text=p.read_text();inputs[p]=text
 for name in re.findall(r'\\input\{([^}]+)\}',text):visit(S/(name+'.tex' if not name.endswith('.tex') else name))
visit(S/'main.tex');source='\n'.join(inputs.values());labels=re.findall(r'\\label\{([^}]+)\}',source)
assert len(labels)==len(set(labels));refs=set()
for group in re.findall(r'\\(?:[cC]ref|eqref|ref)\{([^}]+)\}',source):refs.update(group.split(','))
assert refs<=set(labels)
cover=(P/'process/coverage.md').read_text();loc=set(re.findall(r'\b(?:sec|subsec|thm|lem|prop|cor|ex|rem|tab|fig):[a-z0-9-]+',cover));assert loc<=set(labels)
# Sparse all-label comparison in the new introduction, independently from raw records.
d=json.loads((P/'verification/stage06-benchmarks.json').read_text());c=d['optimization'][2]
assert c['warmup']['full']['stats']['variables']==c['warmup']['global']['stats']['variables']==7215
assert c['warmup']['initial']['stats']['variables']==495 and c['warmup']['eliminated']['stats']['variables']==367
assert round(1000*c['summary']['full']['total_seconds']['median'])==30
assert round(1000*c['summary']['initial']['total_seconds']['median'])==10
out={'source_hashes':len(v[key]),'inputs':len(inputs),'unique_labels':len(labels),'referenced_labels':len(refs),'coverage_locators':len(loc),'tables_unchanged_and_regenerated':5,'intro_experiment_counts_and_rounding':'PASS'}
(E/'integration-checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
