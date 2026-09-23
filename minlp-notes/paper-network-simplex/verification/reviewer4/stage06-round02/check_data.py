from pathlib import Path
from statistics import median
import hashlib,json,shutil,subprocess
root=Path.cwd(); paper=root/'paper-network-simplex'; here=Path(__file__).parent
v=json.loads((paper/'verification/stage06-validation.json').read_text())
for p,h in v['sha256'].items(): assert hashlib.sha256((root/p).read_bytes()).hexdigest()==h,p
snap=paper/'process/snapshots/stage06-round02'
for name in ['main.tex','references.bib','README.md']+[str(p.relative_to(snap)) for d in ('sections','tables') for p in (snap/d).glob('*.tex')]:
    assert (snap/name).read_bytes()==(paper/name).read_bytes(),name
new=json.loads((paper/'verification/stage06-benchmarks.json').read_text())
old=json.loads((paper/'verification/stage06-corrections/round1-archive/paper-network-simplex/verification/stage06-benchmarks.json').read_text())
for k in ('flat','membership','cold'): assert old[k]==new[k]
for a,b in zip(old['optimization'],new['optimization']):
    for k in ('edges','states','observations','observed_labels','y','objective_vector','extra_rows','name'): assert a[k]==b[k],k
count=0;runs=0
for kind in ('flat','membership','optimization'):
    for c in new[kind]:
        assert len(c['runs'])==5
        runs+=sum(len(r['measurements']) for r in c['runs'])
        for method,summ in c['summary'].items():
            for key,out in summ.items():
                raw=[r['measurements'][method][key] for r in c['runs']]
                assert out==dict(minimum=min(raw),median=median(raw),maximum=max(raw))
                count+=1
build=here/'build';build.mkdir(exist_ok=True)
for name in ['main.tex','references.bib']:
    shutil.copy2(snap/name,build/name)
for name in ('sections','tables'): shutil.copytree(snap/name,build/name,dirs_exist_ok=True)
section=(snap/'sections/08-computation.tex').read_text()
command=section.split('\\begin{verbatim}\n',1)[1].split('\\end{verbatim}',1)[0]
assert command.splitlines()[0].endswith(' \\') and not command.splitlines()[0].endswith(' \\\\')
# Execute the literal displayed command with a harmless shell function.
proc=subprocess.run(['bash','-c','python() { printf "CALL"; printf " <%s>" "$@"; printf "\\n"; }\n'+command],capture_output=True,text=True)
assert proc.returncode==0 and len(proc.stdout.splitlines())==2
assert '<--output> <paper-network-simplex/verification/stage06-benchmarks.json>' in proc.stdout
(here/'shell-check.txt').write_text(proc.stdout)
# The validator writes only to this private miniature paper directory.
private=here/'tables-check';(private/'verification').mkdir(parents=True,exist_ok=True)
shutil.copy2(paper/'verification/stage06-tables.py',private/'verification/stage06-tables.py')
shutil.copy2(paper/'verification/stage06-benchmarks.json',private/'verification/stage06-benchmarks.json')
proc=subprocess.run(['python',str(private/'verification/stage06-tables.py')],capture_output=True,text=True)
assert proc.returncode==0,proc.stderr
for t in (snap/'tables').glob('*.tex'): assert (private/'tables'/t.name).read_bytes()==t.read_bytes()
result=dict(status='PASS',hashes=len(v['sha256']),timing_summaries=count,timed_method_runs=runs,preserved=['flat','membership','cold'],private_tables=5,displayed_shell_command='PASS')
(here/'data-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
