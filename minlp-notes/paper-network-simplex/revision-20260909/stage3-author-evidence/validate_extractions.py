"""Private Stage 3 extraction validation; reports do not enter either package."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib, json, os, re, shutil, subprocess, sys, tempfile, time, zipfile
HERE=Path(__file__).resolve().parent
PAPER=HERE.parents[1]
DELIVERY=PAPER/'delivery'
SANDBOX=Path(tempfile.mkdtemp(prefix='network-simplex-stage3-extraction-'))
(HERE/'sandbox.txt').write_text(str(SANDBOX)+'\n')
for name in ['latex-source','computational-supplement']:
 with zipfile.ZipFile(DELIVERY/f'{name}.zip') as z:
  assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
  z.extractall(SANDBOX)
SOURCE=SANDBOX/'latex-source';SUPP=SANDBOX/'computational-supplement'
RESULTS={}
def run(name,command,cwd=SUPP,extra=None):
 env=dict(os.environ,PYTHONPATH=str(cwd/'code'))
 if extra:env.update(extra)
 start=time.monotonic()
 result=subprocess.run(command,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (HERE/f'{name}.log').write_text(result.stdout)
 out=dict(command=command,cwd=str(cwd),returncode=result.returncode,elapsed_seconds=time.monotonic()-start)
 print(name,result.returncode,round(out['elapsed_seconds'],2),flush=True)
 return name,out

tasks=[('source-manifest',['sha256sum','-c','MANIFEST.sha256'],SOURCE),
 ('supplement-manifest',['sha256sum','-c','MANIFEST.sha256'],SUPP),
 ('principal-tests',[sys.executable,'-m','unittest','network_simplex.test_separator','network_simplex.test_flat_chain','network_simplex_benchmarks.test_strong_baselines','-v'],SUPP),
 ('flat-audit',[sys.executable,'code/network_simplex_review/verify_flat_chain_implementation.py'],SUPP),
 ('compressed-audit',[sys.executable,'-m','network_simplex_compressed.verify'],SUPP),
 ('compressed-integration',[sys.executable,'-m','network_simplex_compressed.integration'],SUPP),
 ('benchmark-smoke',[sys.executable,'-m','network_simplex_benchmarks.paper_stage06','--quick','--repetitions','1','--output','smoke-benchmarks.json'],SUPP),
 ('table-regeneration',[sys.executable,'paper-network-simplex/verification/stage06-tables.py'],SUPP)]
for path in ['stage02-exact.py','stage03-exact.py','stage04-recovery.py','stage05-padding.py','stage05-profile.py','stage07/integral-hull.py']:
 tasks.append((Path(path).stem,[sys.executable,'paper-network-simplex/verification/'+path],SUPP))
for path in sorted((SUPP/'checks').glob('*.py')):
 tasks.append((path.stem,[sys.executable,'checks/'+path.name],SUPP))
with ThreadPoolExecutor(max_workers=4) as pool:
 futures=[pool.submit(run,*args) for args in tasks]
 futures.append(pool.submit(run,'latex-build',['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','main.tex'],SOURCE,dict(SOURCE_DATE_EPOCH='946684800',FORCE_SOURCE_DATE='1',TZ='UTC')))
 for future in as_completed(futures):
  name,out=future.result();RESULTS[name]=out
  (HERE/'extraction-results.json').write_text(json.dumps(RESULTS,indent=2)+'\n')
assert all(r['returncode']==0 for r in RESULTS.values()),RESULTS
name,out=run('supplement-manifest-after',['sha256sum','-c','MANIFEST.sha256']);assert out['returncode']==0
RESULTS[name]=out
pdf=(SOURCE/'main.pdf').read_bytes();assert pdf==(DELIVERY/'submission.pdf').read_bytes()
log=(SOURCE/'main.log').read_text()
assert not re.search(r'(LaTeX Warning:|Package natbib Warning:|Overfull|Underfull)',log)
shutil.copyfile(SOURCE/'main.log',HERE/'clean-main.log')
shutil.copyfile(SOURCE/'main.blg',HERE/'clean-main.blg')
for filename in ['main.pdf','main.fls']:
 shutil.copyfile(SOURCE/filename,HERE/filename)
info=subprocess.check_output(['pdfinfo',SOURCE/'main.pdf'],text=True);(HERE/'pdfinfo.txt').write_text(info)
text=subprocess.check_output(['pdftotext','-layout',SOURCE/'main.pdf','-'],text=True);(HERE/'manuscript.txt').write_text(text)
assert 'Author:' not in info or re.search(r'^Author:\s*$',info,re.M)
assert not re.search(r'(/home/|/tmp/|@)',info)
assert not re.search(r'(/home/|/tmp/)',text)
# Verify every archive input is anonymously named and has no private paths.
scanned=0
for folder in [SOURCE,SUPP]:
 for row in (folder/'MANIFEST.sha256').read_text().splitlines():
  digest,name=row.split('  ',1);p=folder/name
  assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
  if p.suffix in ['.md','.tex','.bib','.py','.json','.txt']:
   body=p.read_text();assert not re.search(r'(/home/|/Users/)',body),name
   scanned+=1
# Check the document's explicit inputs and bibliography exist in the source archive.
refs=[]
for p in SOURCE.rglob('*.tex'):
 for command,ref in re.findall(r'\\(input|bibliography|includegraphics)(?:\[[^]]*\])?\{([^}]+)\}',p.read_text()):
  target=SOURCE/ref
  if not target.suffix:target=target.with_suffix('.bib' if command=='bibliography' else '.tex')
  assert target.is_file(),(p,command,ref)
  refs.append(str(target.relative_to(SOURCE)))
smoke=json.loads((SUPP/'smoke-benchmarks.json').read_text())
assert smoke['quick'] and smoke['repetitions']==1
assert [len(smoke[k]) for k in ['flat','membership','optimization']]==[4,1,1]
shutil.copyfile(SUPP/'smoke-benchmarks.json',HERE/'smoke-benchmarks.json')
for path in (SUPP/'checks').glob('*.json'):
 shutil.copyfile(path,HERE/path.name)
RESULTS['summary']=dict(status='PASS',pdf_byte_equal=True,private_path_scan_files=scanned,latex_input_references=refs,smoke_case_counts=[4,1,1])
(HERE/'extraction-results.json').write_text(json.dumps(RESULTS,indent=2)+'\n')
print('ALL PASS',flush=True)
