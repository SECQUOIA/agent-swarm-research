"""Read saved primary sources and check source attribution; no solvers."""
import json,subprocess,hashlib,re
from pathlib import Path
from fractions import Fraction as Q
p=Path(__file__).resolve().parents[1];s=p/'sources';review=p.parents[1]/'reviews/lit-network-r2'
def extract(name,needles,context=1):
 text=(s/name).read_text();lines=text.splitlines();seen=set()
 print('\nSOURCE',name)
 for i,line in enumerate(lines):
  if any(k in line for k in needles):
   for j in range(max(0,i-context),min(len(lines),i+context+1)):
    if j not in seen:print(lines[j]);seen.add(j)
 return text
rw=extract('schweidtmann2021_dissertation.txt',['Chapter 2 is based on parts','Reprinted from A. M. Schweidtmann','Table 2.8.','4,671,260','6,329,810','10,033,800'])
assert all(x in rw for x in ['4,671,260','2930','6,329,810','444','10,033,800','328'])
ar=extract('schweidtmann2019_arxiv1801.07114.txt',['4,772,133','5,683,103','12,939,508'])
assert all(x in ar for x in ['4,772,133','5,683,103','12,939,508'])
t=extract('oustry_table_of_results.txt',['pglib_opf_case30_as','pglib_opf_case30_ieee','pglib_opf_case39_epri'],0)
assert '803.127' in t and '7896.87' in t and '137254' in t
extract('oustry2022_pscc22.txt',['PGLib-OPF v21.07','conditions (TYP)'])
h=extract('huang2019_dissertation_wayback20240414.txt',['P[0, 1]','P[0, 2]','P[0, 3]','P[0, 5]','P[0, 6]','P[0, 23]'],0)
assert all(x in h for x in ['19.38','39.5','0.000470589','343.41','1.14263'])
for name in ['mueller2020_arxiv1903.05521.txt','goss2026_arxiv2603.16505.txt']:
 extract(name,['waterno2_06','waterno2_09','waterno2_12','waterno2_18','waterno2_24','powerflow0030r','powerflow0039r','powerflow0039p'],0)
suite=p.parent/'control/sources/scip80_suite_arXiv2112.08872v1.pdf'
text=subprocess.check_output(['pdftotext','-layout',str(suite),'-'],text=True)
print('\nSCIP suite 8.0 benchmark rows:')
for i,page in enumerate(text.split('\f'),1):
 for line in page.splitlines():
  if re.search(r'(waterno2[_ ](06|09|12|18|24)|powerflow003[09]r)\s',line):print('PDF page',i,line)
# Exact stored decimal coefficients demonstrate that transport of a rigorous bound is unsafe.
polar=Q('1.86832740213523');rect=2*Q('.934163701067616');assert polar!=rect
print('branch 27-29:',polar,'!=',rect,'absolute difference',float(abs(polar-rect)))
log=(review/'pf_twin_exact_r2.log').read_text();assert log.count('matched exactly 214')==2 and '1.030e-13' in log;print(log)
# Source log explicitly supplies only the time-limit setting, not a changed feasibility tolerance.
logs=list((s/'zenodo_kan/ex').rglob('R3_H1_N4.log'));assert logs
for f in logs:
 text=f.read_text(); print('KAN log',f.relative_to(s))
 for line in text.splitlines():
  if any(x in line for x in ['SCIP version','limits/time','feastol','scip.set']):print(line)
 assert 'limits/time = 7200' in text and 'numerics/feastol =' not in text
meta=json.loads((s/'bibliography_metadata_20261003.json').read_text());print('\nBibliography title evidence:')
for doi,v in meta.items():
 print(doi,v.get('message',{}).get('title','metadata unavailable; use saved paper title'))
print('PASS: version-dependent cumene numbers, nonclosing benchmarks, OPF related models, Huang columns and inferred tolerance checked.')
