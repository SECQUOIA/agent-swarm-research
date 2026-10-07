"""Copy checked review sources into the owned tracks and save primary metadata."""
import json,hashlib,shutil,urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
p=Path(__file__).resolve().parents[2]; src=p/'literature/network/sources'; entries=[]
review=p/'reviews/lit-network-r2/sources_r2'
copies={
'arxiv1903.05521.pdf':'mueller2020_arxiv1903.05521.pdf',
'arxiv1903.05521.txt':'mueller2020_arxiv1903.05521.txt',
'arxiv2603.16505.pdf':'goss2026_arxiv2603.16505.pdf',
'arxiv2603.16505.txt':'goss2026_arxiv2603.16505.txt',
'oustry2022_pscc22.pdf':'oustry2022_pscc22.pdf',
'oustry_table_of_results.txt':'oustry_table_of_results.txt',
'rwth820314_wayback20260128.pdf':'schweidtmann2021_dissertation.pdf'}
for old,new in copies.items():
 shutil.copyfile(review/old,src/new);entries.append((new,str(review/old)))
# Derived text was already generated for the dissertation.
entries.append(('schweidtmann2021_dissertation.txt','pdftotext -layout of schweidtmann2021_dissertation.pdf'))
shutil.copyfile(p/'reviews/lit-control-r2/web/minotaur/QuadHandler.cpp',p/'literature/control/sources/QuadHandler_master_r2.cpp')
DOIS=['10.1109/TPWRS.2018.2848965','10.1016/j.ejor.2014.12.039','10.1137/16M1069687','10.1109/TPWRS.2015.2390037','10.3934/naco.2012.2.695','10.1109/Allerton.2012.6483274','10.69997/sct.139045','10.69997/sct.195815','10.1109/TPWRS.2015.2402640','10.1109/TPWRS.2011.2160974','10.1109/TPWRS.2014.2372478','10.1007/s10957-018-1396-0','10.18452/16704','10.1007/s10898-022-01228-x','10.1016/j.epsr.2022.108278']
def fetch(url):
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'minor-review-check/1.0'})
  with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
 except Exception as e:return {'error':str(e),'url':url}
with ThreadPoolExecutor(max_workers=4) as pool: meta=dict(zip(DOIS,pool.map(lambda d:fetch('https://api.crossref.org/works/'+d),DOIS)))
f=src/'bibliography_metadata_20261003.json';f.write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n');entries.append((f.name,'Crossref API, fetched 2026-10-03; any errors retained'))
for doi,v in meta.items():
 m=v.get('message');print(doi,m.get('title') if isinstance(m,dict) else v.get('error'))
scip=p/'scip-bug/sources';scip.mkdir(exist_ok=True)
for n in [162,190]:
 for suffix in ['', '/comments']:
  url=f'https://api.github.com/repos/scipopt/scip/issues/{n}'+suffix
  v=fetch(url);f=scip/f'issue_{n}{"_comments" if suffix else ""}_20261003.json';f.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n');print(url,'OK' if 'error' not in v else v['error'])
# Append source entries with copy provenance; PDFs retain the review's original bytes.
with (src/'MANIFEST.md').open('a') as f:
 f.write('\n## Minor-review revision (2026-10-03)\n\nReview sources were copied from the saved r2 files fetched 2026-10-02. Their original URLs and fetch records are in `publication/reviews/lit-network-review-r2.md`, Section 7. Crossref metadata was fetched read-only on 2026-10-03.\n\n| file | origin | bytes | sha256 |\n|---|---|---|---|\n')
 for name,origin in entries:
  f0=src/name;data=f0.read_bytes();f.write(f'| `{name}` | {origin} | {len(data)} | `{hashlib.sha256(data).hexdigest()}` |\n')
