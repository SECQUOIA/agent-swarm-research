from pathlib import Path
from fractions import Fraction as Q
import json,sys,importlib.util,tempfile,shutil,decimal
sys.set_int_max_str_digits(0); sys.dont_write_bytecode=True
root=Path(__file__).resolve().parents[2]; sup=root/'supplement'; data=sup/'legacy/results'
def read(n):return json.loads((data/(n+'.json')).read_text())
checks=[]
def record(x):checks.append(x)
# Independently compare printed outward values to exact stored fractions.
mem=['.00270073','.00187230','.00387283','.00183482','.00186234','.00178161','.00190758','.00182972','.00193602','.00194271']
cont=['1.12e-7','6.48e-8','8.39e-8','1.62e-7','6.63e-8','3.54e-7','5.19e-7','6.27e-7','6.64e-7','1.30e-6']
sep=['.04721614','.03593564','.04639027','.03913455','.02276202','.02635127','.10923746','.08378101','.10436604','.08771349']
ms=[read('noisy-markov-extended-certificate-'+str(i)) for i in range(6)]+[read(f'noisy-markov-kinetics-certificate-n{n}-{r}') for n in (48,96) for r in ('fast','slow')]
ds=sum([read(n)['results'] for n in ('dense-design-exact-certificates','dense-design-kinetics-n48-certificates','dense-design-kinetics-n96-certificates')],[])
ss=sum([read(n)['results'] for n in ('dense-all-splits-certificates','dense-all-splits-kinetics-n48-certificates','dense-all-splits-kinetics-n96-certificates')],[])
for i,(m,d,s) in enumerate(zip(ms,ds,ss)):
 assert Q(m['upper_bound'])-Q(m['lower_bound'])==Q(m['gap'])<=Q(mem[i])
 assert Q(d['upper_bound'])-Q(d['continuous_lower_bound'])==Q(d['continuous_certificate_gap'])<=Q(cont[i])
 assert m['problem_data']==d['problem_data']==s['problem_data']
 assert Q(s['all_splits_lower_bound'])-Q(m['upper_bound'])>=Q(sep[i])
record('All 30 scalar table outward bounds and exact common-model arrays checked')
for i,v in enumerate(('.059924','.059732','.060361','.059925')):
 a=read('partial-observation-trace-certificate-'+str(i));assert Q(a['relative_gap'])*100<=Q(v)
record('All four partial trace percentages rounded upward')
for name,vs in [('robust-kinetic-n48-certificate',('-.091701377259','-.083176142020','.008525235239')),('robust-kinetic-n96-certificate',('-.091162249685','-.074519785108','.016642464577')),('robust-kinetic-n96-polished-certificate',('-.086007784227','-.074519785108','.011487999119'))]:
 a=read(name)['standardized'];assert all(Q(a[k])==Q(v) for k,v in zip(('lower_bound','upper_bound','gap'),vs))
record('All robust table endpoints and gaps exactly equal their saved rationals')
for n,b,vs in [(48,8,('14.925507606504','15.005243683880','.079736077376')),(96,12,('14.945662679078','15.051419395187','.105756716109')),(96,16,('14.945662679078','15.025970711361','.080308032283')),(192,12,('14.953046919008','15.139311234872','.186264315864')),(192,16,('14.953046919008','15.110331327215','.157284408207'))]:
 a=read(f'latent-separator-n{n}-b{b}-certificate');assert all(Q(a[k])==Q(v) for k,v in zip(('lower_bound','upper_bound','gap'),vs))
record('All 15 separator table endpoints/gaps exactly match stored rationals')
fresh=json.loads((sup/'results/fresh-all.json').read_text())
for r,lo,hi in zip(fresh['nested']['nested'],('.7747129913','.7837750653','.8352816893','.9008412717'),('.7747130145','.7837754218','.8352816952','.9008414860')):
 assert Q(lo)<=Q(r['lower'])<=Q(r['upper'])<=Q(hi)
record('All nested-anchor interval displays rounded outward')
b=fresh['blocks'];assert Q(b['old_delta'])<=Q('.111957334') and Q(b['sharp_far_delta'])<=Q('.103863638'); assert Q(b['true_lower'])>Q('.90391527')
assert Q(b['old_upper'])<Q('1.01644959') and Q(b['sharp_far_upper'])<Q('1.00735957')
assert 100*Q(b['old_relative_gap'])<=Q('12.4497') and 100*Q(b['sharp_far_relative_gap'])<=Q('11.4441')
record('Fresh block displays and relative gap denominator checked')
# Exponential lower guarantees using a rational alternating series, independent
# of floating exp or the manuscript log-enclosure implementation. All x in [0,1].
def expminus_lower(x):
 total=Q(1);term=Q(1)
 for j in range(1,20):term*=(-x)/j;total+=term
 return total
for name,percent in [('robust-kinetic-n96-polished-certificate','97.1737')]:
 a=read(name)['standardized'];assert 100*expminus_lower(-Q(a['lower_bound'])/3)>Q(percent)
for name,percent in [('robust-kinetic-n96-polished-certificate','99.6177'),('robust-kinetic-n48-certificate','99.7162')]:
 a=read(name)['standardized'];assert 100*expminus_lower(Q(a['gap'])/3)>Q(percent)
assert 100*expminus_lower(Q('.001943')/3)>Q('99.935')
record('All four principal D-efficiency percentage claims proved by rational alternating exp lower bounds')
# Integrity failure behavior in a throwaway copy, with no validation rerun.
spec=importlib.util.spec_from_file_location('validate',sup/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
with tempfile.TemporaryDirectory(dir=Path(__file__).parent/'tmp') as td:
 copy=Path(td)/'s'; shutil.copytree(sup,copy,ignore=shutil.ignore_patterns('.venv','__pycache__','reproduced'))
 counts=v.verify_manifests(copy)
 p=copy/'source_kinetics/kinetics_Q_drop0.csv'; original=p.read_bytes();p.write_bytes(original+b'\n')
 try:v.verify_manifests(copy)
 except ValueError:pass
 else:raise AssertionError('Changed CSV was accepted')
 p.write_bytes(original);p.unlink()
 try:v.verify_manifests(copy)
 except FileNotFoundError:pass
 else:raise AssertionError('Missing CSV was accepted')
record('Both manifest families accepted intact copy and rejected modified/missing public CSV')
output={'status':'passed','checks':checks,'manifest_counts':counts};(Path(__file__).parent/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))
