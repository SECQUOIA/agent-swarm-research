from pathlib import Path
import tempfile, subprocess, json, hashlib, shutil, difflib, re, os
HERE=Path(__file__).resolve().parent
PAPER=HERE.parents[1]
TARGET=Path(tempfile.mkdtemp(prefix='network-simplex-stage3-rebuild-'))
r=subprocess.run(['python',str(PAPER/'delivery/build-packages.py'),'--output',str(TARGET)],capture_output=True,text=True)
(HERE/'rebuild.log').write_text(r.stdout+r.stderr)
assert r.returncode==0
check={}
for name in ['submission.pdf','latex-source.zip','computational-supplement.zip','manifest.json']:
 a=(PAPER/'delivery'/name).read_bytes();b=(TARGET/name).read_bytes();assert a==b,name
 check[name]={'sha256':hashlib.sha256(a).hexdigest(),'bytes':len(a),'byte_equal':True}
shutil.copyfile(PAPER/'delivery/submission.pdf',PAPER/'main.pdf')
assert (PAPER/'main.pdf').read_bytes()==(PAPER/'delivery/submission.pdf').read_bytes()
check['main.pdf']={'equals_delivery_submission':True}
(HERE/'determinism.json').write_text(json.dumps(check,indent=2)+'\n')
accepted=PAPER/'revision-20260909/stage2-round1/paper-network-simplex'
changes=[]
for rel in ['main.tex','sections/08-computation.tex','README.md','PROCESS.md']:
 changes+=difflib.unified_diff((accepted/rel).read_text().splitlines(True),(PAPER/rel).read_text().splitlines(True),fromfile='accepted-stage2/'+rel,tofile='stage3/'+rel)
(HERE/'stage3-source.diff').write_text(''.join(changes))
pattern=r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}[\s\S]*?\\end\{\1\}'
result={}
for path in sorted((PAPER/'sections').glob('*.tex')):
 baseline=(accepted/'sections'/path.name).read_text();current=path.read_text()
 a=[m.group(0) for m in re.finditer(pattern,baseline)];b=[m.group(0) for m in re.finditer(pattern,current)]
 assert a==b,path
 result[path.name]={'formal_environments':len(a),'source_unchanged':baseline==current}
assert (PAPER/'references.bib').read_bytes()==(accepted/'references.bib').read_bytes()
(HERE/'math-preservation.json').write_text(json.dumps(result,indent=2)+'\n')
sandbox=Path((HERE/'sandbox.txt').read_text().strip())/'computational-supplement'
examples=re.findall(r'```python\n(.*?)```',(sandbox/'API.md').read_text(),re.S)
for example in examples:
 subprocess.run(['python','-c',example],cwd=sandbox,env=dict(os.environ,PYTHONPATH=str(sandbox/'code')),check=True)
(HERE/'api-example.json').write_text(json.dumps({'status':'PASS','examples':len(examples)},indent=2)+'\n')
print(json.dumps(check,indent=2))
