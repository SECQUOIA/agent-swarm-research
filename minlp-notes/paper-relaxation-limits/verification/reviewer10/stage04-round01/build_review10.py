import os, subprocess, hashlib, json
from pathlib import Path
out=Path(__file__).resolve().parent
paper=out.parents[2]
snap=paper/'process/snapshots/stage04-round01'
manifest=json.loads((snap/'manifest.json').read_text())
wrong=[p for p,h in manifest.items() if hashlib.sha256((snap/p).read_bytes()).hexdigest()!=h]
assert not wrong,wrong
env=os.environ.copy(); env['TEXINPUTS']=str(snap)+'//:'; env['BIBINPUTS']=str(snap)+':'
commands=[['pdflatex','-interaction=nonstopmode','-halt-on-error',str(snap/'main.tex')],['bibtex','main'],['pdflatex','-interaction=nonstopmode','-halt-on-error',str(snap/'main.tex')],['pdflatex','-interaction=nonstopmode','-halt-on-error',str(snap/'main.tex')]]
for i,cmd in enumerate(commands):
    p=subprocess.run(cmd,cwd=out,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (out/f'build-command-{i+1}.txt').write_text(p.stdout)
    assert p.returncode==0,(cmd,p.stdout[-2000:])
log=(out/'main.log').read_text()
warnings=[line for line in log.splitlines() if any(x in line for x in ['Warning','Overfull','Underfull'])]
report={'manifest_files_verified':len(manifest),'compile_exit':0,'warnings':warnings,'frozen_pdf_sha256':hashlib.sha256((snap/'main.pdf').read_bytes()).hexdigest()}
(out/'build_review10.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
