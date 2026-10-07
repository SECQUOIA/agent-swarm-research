"""Check rounded-copy bounds and source locations; no solvers or main certificates."""
from pathlib import Path
from fractions import Fraction as Q
import subprocess,json
import qplib_camshape_compare as C
p=Path(__file__).resolve().parents[1];s=p/'sources';models=s/'qplib/camshape_copies'
for n,i in [(100,2738),(200,2480),(400,2703),(800,3177)]:
 M=C.parse_gms(models/f'camshape{n}.gms',0);R=C.parse_gms(models/f'QPLIB_{i}.gms',1);nm,nq,unm,w,bd,where=C.compare(M,R)
 assert not unm and nm==2*n+1 and all(v[1] is not None for k,v in M[1].items() if k!='objvar')
 print(n,i,'rows',nm,'coeff',w,'bounds',bd,where)
 if n==400:assert 4.7e-10<bd<4.8e-10
 point=C.read_sol(models/f'QPLIB_{i}.sol',1)
 for label,model in [('MINLPLib',M),('QPLIB',R)]:
  obj,viol,at=C.evaluate(model,point);print('QPLIB point in',label,'objective',float(obj),'max violation',float(viol),at)
for filename in ['waki2004_oo988.pdf','mueller2019_arXiv1912.00356.pdf']:
 text=subprocess.check_output(['pdftotext','-layout',str(s/'papers_rev1'/filename),'-'],text=True)
 pages=text.split('\f');page=33 if filename.startswith('waki') else 40
 body=pages[page-1];print(filename,'PDF page',page);print(body)
 assert ('600' in body and '-1.6e-10' in body) if filename.startswith('waki') else 'camshape100' in body
for i in [3177,2738,2480,2703,8585]:
 text=(s/f'mittelmann_cnconv/logs/QPLIB_{i}.mnt').read_text();print('MINOTAUR',i)
 for line in text.splitlines():
  if any(k in line for k in ['nodes processed =','best bound estimate','best solution value =','gap =','time used =','status of branch-and-bound:']):print(line)
cpp=(s/'QuadHandler_master_r2.cpp').read_text();assert 'defaultLb_ = -100 * defaultLb_' in cpp and 'defaultUb_ = 100 * defaultUb_' in cpp
print('master default rule with sole bound 1 -> [-100,100]; benchmark revision may differ.')
ant=(s/'mittelmann_cnconv/logs/QPLIB_2738.ant').read_text();assert '8.7007237331E-06 (Input point)' in ant
print('CONOPT: column Infeasibility, input point, 8.7007237331E-06 (aggregate; incumbent identity unstated).')
print('PASS: all bounds captured; corrected maximum; Waki/Mueller locations and log wording checked.')
