"""Recount fixed-domain scans directly from raw logs; no solver runs."""
import ast,re
from pathlib import Path
from fractions import Fraction as Q
p=Path(__file__).resolve().parent
files=['fm_scan.log','master_vbr_b_p4.log','master_vbr_b_p5.log','master_vbr_b_pair2236.log','master_vbr_b_pumps_default.log','p4_smallexcess_vbr_b.log']+[f'seedscan_vbr_b_{m}.log' for m in ['p0','p4','p5','pair2236']]
groups=[]
for name in files:
 buf=[]
 for line in (p/'logs'/name).read_text().splitlines():
  if re.match(r'(?:\S+ )?seed\s+\d+ ',line):buf.append(line)
  if line.startswith('# ') and 'extra=' in line:
   extra=ast.literal_eval(re.search(r'extra=(\{.*?\}):',line)[1])
   if extra.get('constraints/nonlinear/varboundrelax')=='b':
    assert len(buf)==int(re.search(r'of (\d+) seeds',line)[1]);assert all(x.endswith('ok') for x in buf)
    groups.append((name,len(buf)));print(name,'b runs',len(buf),'wrong',0)
   buf=[]
assert sum(n for _,n in groups)==122
# Default matched cases: wheel first ten seeds of p0/p4/p5 plus thirty pair seeds.
wheel=0
for m,n in [('p0',10),('p4',10),('p5',10),('pair2236',30)]:
 lines=[x for x in (p/f'logs/seedscan_{m}.log').read_text().splitlines() if x.startswith('seed ')]
 wheel+=sum(x.endswith('WRONG') for x in lines[:n])
assert wheel==27
fm=[];buf=[]
for line in (p/'logs/fm_scan.log').read_text().splitlines():
 if re.match(r'\S+ seed\s+\d+ ',line):buf.append(line)
 if line.startswith('# ') and 'extra=' in line:
  extra=ast.literal_eval(re.search(r'extra=(\{.*?\}):',line)[1])
  if extra=={} and line.startswith(("# master ","# 10.1.0 ")):fm+=buf
  buf=[]
assert len(fm)==40 and sum(x.endswith('WRONG') for x in fm)==30
# Match every b seed to its raw default master record.
master_wrong=master_n=0
for model in ['p4','p5','pair2236','pumps_default']:
 b_lines=(p/f'logs/master_vbr_b_{model}.log').read_text().splitlines()
 default_lines=(p/f'logs/master_{model}.log').read_text().splitlines()
 selected={int(re.search(r'seed\s+(\d+)',x)[1]) for x in b_lines if x.startswith('master seed')}
 defaults={int(re.search(r'seed\s+(\d+)',x)[1]):x.endswith('WRONG') for x in default_lines if x.startswith('master seed')}
 assert selected<=defaults.keys()
 master_n+=len(selected);master_wrong+=sum(defaults[k] for k in selected)
 print('matched master',model,'wrong',sum(defaults[k] for k in selected),'of',len(selected))
assert (master_wrong,master_n)==(19,20)
print('matched default: wheel 27/60; master 19/20 (selected wrong seeds + p4 seed 5); fm 30/40; small-excess 2/2; total 78/122')
s=(p/'logs/dbgsol_pair2236_seed11.log').read_text();assert 'SCIPBUG' not in s
first=next(l for l in s.splitlines() if 'invalid local lower bound implication' in l);assert '<t_b35>[0] >= 1' in first;print('seed 11:',first)
opt=Q(187,270);assert Q('0.2')+Q('0.614125')>opt and 5*Q('.343')>opt;assert Q('.1')+2*Q(8,27)==opt
# tiny2 b=1 minimum is .2-1.6*sqrt(.8), strictly above -1.337.
assert Q('.8') < ((Q('.2')+Q('1.337'))/Q('1.6'))**2
print('fm336 optimum = 187/270; tiny2 optimum = -1337/1000 (exact case comparisons).')
print('PASS: 0/122; 78 matched-default wrong; uninstrumented seed-11 caveat; exact small-model optima.')
