"""Read saved data; use exact Fractions for endpoints, gaps and comparisons.
No project module is imported. No optimization or certificate is rerun.
"""
import ast,csv,gzip,hashlib,json,re
from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction as Q
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
checks=[]; gaps={}; sources={}
def read(rel):
    p=BASE/rel; sources[rel]=hashlib.sha256(p.read_bytes()).hexdigest(); return p.read_text()
def J(rel): return json.loads(read(rel))
def check(label,condition):
    assert condition,label
    checks.append(label); print('PASS',label)
def upper_iv(text): return Q(re.fullmatch(r'\[([^,]+),\s*([^]]+)\]',text).group(2))
def emit(name,value,unit,percent=False):
    value=Q(value);unit=Q(unit)
    display=-((-value)//unit)*unit
    check(name+' gap ceiling',value>=0 and display>=value and display-value<unit)
    with localcontext() as ctx:
        ctx.prec=80
        number=Decimal(display.numerator)/Decimal(display.denominator)
        raw=Decimal(value.numerator)/Decimal(value.denominator)
    gaps[name]={'exact_upper':str(value),'decimal_upper':str(raw),'display_value':str(display),'text':(format(number, '.'+str(max(0,-(Decimal(unit.numerator)/Decimal(unit.denominator)).as_tuple().exponent))+'f')+'%' if percent else str(number).lower()),'unit':str(unit)}
    print('GAP',name,raw,'->',gaps[name]['text'])
summary=read('open-instances-summary.md')
rows={}
for line in summary.splitlines():
    if line.startswith('| '):
        columns=line.split('|')
        rows.setdefault(columns[1].strip(),columns) # first occurrence is the numeric table
def shown(name,col): return Q(re.search(r'[−-]?\d+(?:\.\d+)?(?:e[+-]?\d+)?',rows[name][col])[0].replace('−','-'))
# Corrected new primal displays and all closed-table gap cells.
for n in (50,100,200,400):
    name=f'lnts{n}';v=J(f'publication/primal/lnts/points/{name}_point.json')
    enclosure=v['objective_enclosure'];enclosure=ast.literal_eval(enclosure) if isinstance(enclosure,str) else enclosure
    hi=Q(enclosure[1]);check(name+' upward primal',shown(name,4)>=hi)
    L=shown(name,3);emit(name,hi-L,'1e-15')
    v=next(x for x in J('reviews/open-instances-verification/logs/lnts_verify.json') if x['name']==name)
    h=v['cert_1e-12']['h2'];lc=n*(Q(h)-Q(1,10**len(h.split('.')[1])))
    check(name+' displayed dual and verifier gap',L<=lc and hi-lc<=Q('5.55e-13'))
f=Q(read('publication/primal/dtoc5-lukvle10/logs/dtoc5_check_objective_exact.txt').strip())
check('dtoc5 upward primal',shown('dtoc5',4)>=f);emit('dtoc5',f-shown('dtoc5',3),'1e-17')
x=J('publication/primal/dtoc5-lukvle10/logs/lukvle10_enclose.json');hi=Q(x['objective_box'][1])
check('lukvle10 upward primal',shown('lukvle10',4)>=hi);emit('lukvle10',hi-shown('lukvle10',3),'1e-10')
v=J('reviews/bangbang-verification/logs/primal_check.json')['rigorous_primal'];hi=upper_iv(v['J_upper'])
L=Q(J('reviews/bangbang-verification/logs/qcal_exact.json')['bound_str'])/10**20
check('optcdeg2 rounded certificate label and upward primal',shown('optcdeg2',3)<L and shown('optcdeg2',4)>=hi)
emit('optcdeg2',hi-L,'1e-17')
for name in ('ex6_2_5','ex6_2_7'):
    v=J(f'reviews/wave2-small-verification/logs/{name}_bound.json');s=v['own_primal_objective_enclosure'][1]
    hi=Q(s)+Q(1,10**len(s.split('.')[1])) # allow a full unit of last printed digit
    check(name+' upward primal and downward dual',shown(name,4)>=hi and shown(name,3)<=Q(v['dual_bound']))
    emit(name,hi-Q(v['dual_bound']),'1e-16' if name.endswith('5') else '1e-15')
v=J('reviews/wave2-small-verification/logs/etamac.json');hi=upper_iv(v['own_primal']['objective'][1]);L=Q(v['bound']['dual_bound'])
check('etamac displayed dual',shown('etamac',3)<=L);emit('etamac',hi-L,'1e-16')
# pricing's saved primal is only printed at 20 digits. Display subtraction
# is fully exact and conservative; do not assert unretained objective digits.
v=J('reviews/wave2-small-verification/logs/pricing050.json');m=v['multipliers'];U=Q(m['e5'])*-788+Q(m['e6'])*-984-Q(v['certificate']['sum_minF_certified'])+Q('1e-21')
check('pricing050 upward dual',shown('pricing050 (max)',3)>=U)
check('pricing050 downward primal',shown('pricing050 (max)',4)<=Q(v['own_primal']['objective_20'])-Q('1e-16'))
emit('pricing050',shown('pricing050 (max)',3)-shown('pricing050 (max)',4),'1e-16')
for n in (100,200,400,800):
    v=next(x for x in J('reviews/open-instances-verification/logs/camshape_verify.json') if x['n']==n)
    check(f'camshape{n} displayed dual',shown(f'camshape{n}',3)<=Q(v['bound'])-Q(1,10**len(v['bound'].split('.')[1])))
    emit(f'camshape{n}',0,1)
emit('hvycrash',0,1) # exact identity and feasible witness proved in source report
safe={50:'5.0722614939828627',100:'5.0697846107387505',200:'5.0689173417931616',400:'5.068621694604009'}
for n in safe:
    hi=Q(J(f'publication/primal/chain/points/chain{n}_box.json')['objective_enclosure_decimal'][1]);L=Q(J(f'open-instances-wave2/cops/logs/chain{n}_bound.json')['bnb']['bound'])
    check(f'chain{n} safe dual',Q(safe[n])<=L);emit(f'chain{n}',hi-Q(safe[n]),'1e-16')
check('chain compact maximum',max(Q(gaps[f'chain{n}']['exact_upper']) for n in safe)<=Q('1.01e-14'))
# Use exact-point upper ends (not the reviewer's 20-digit Newton display).
cops=J('publication/reproduction/cops/logs/exact_display_checks.json')
for n in (100,200,400,800):
    name=f'catmix{n}';v=next(x for x in cops if x['instance']==name and x['source'].startswith('verifier dual'))
    primal=v['primal_hi'] if n==800 else next(x['primal_hi'] for x in cops if x['instance']==name and x['source'].startswith('author catmix'))
    hi=Q(primal);L=Q(float(v['certified_double']));emit(name,hi-L,{100:'1e-15',200:'1e-13',400:'1e-13',800:'1e-12'}[n])
for name in ('powerflow0030p','powerflow0039p','powerflow0039r'):
    text=read(f'publication/primal/powerflow/logs/certify.{name}.log');lo,hi=map(Q,re.search(r'objective enclosure: \[([^,]+), ([^]]+)\]',text).groups())
    check(name+' upward primal',shown(name,4)>=hi)
    L=Q(J('open-instances-wave3/logs/powerflow0030p.sdpcert.json')['bound_exact']) if name.endswith('0030p') else Q(J(f'open-instances-wave3/powerflow/ext/logs/{name}.bb3t.json')['LB_exact'])
    check(name+' displayed dual',shown(name,3)<=L);emit(name,(hi-L)/abs(L),'1e-10' if name.endswith('0030p') else '1e-11')
text=read('reviews/pindyck-review-checks/logs/primal_check.txt');hi=Q(re.search(r'objective \(min form\) = (\S+)',text)[1])+Q('1e-36')
check('pindyck upward primal',shown('pindyck',4)>=hi);emit('pindyck',hi-shown('pindyck',3),'1e-16')
for name in ('eg_int_s','eg_disc_s','eg_disc2_s'):
    x=dict(line.split() for line in read(f'open-instances-wave3/eg/retry/sol/{name}.retry.sol').splitlines() if line.strip())
    hi=Q(x['objvar']);L=shown(name,3);check(name+' upward primal',shown(name,4)>=hi);emit(name,(hi-L)/L,'1e-11')
for n in ('06','09','12','18','24'):
    name=f'waterno2_{n}';v=J(f'publication/primal/water-ann-kan/points/{name}.exact.json');hi=Q(v['objective'])
    L=Q(J('open-instances-wave2/waterno2/cellslopes/logs/certB_verify.json')['bound_exact']) if n=='06' else Q(J(f'open-instances-wave2/waterno2/logs/cert_{n}_w1_impl.json')['certified_bound_exact'])
    check(name+' upward primal and downward dual',shown(name,4)>=hi and shown(name,3)<=L)
    emit(name,(hi-L)/L*100,'0.01',True)
    if n=='06':
        for label,d in [('separator','272.584700'),('wave2','263.735099')]:emit(name+' '+label,(hi-Q(d))/Q(d)*100,'0.01',True)
v=J('publication/primal/water-ann-kan/points/ann_cumene_tanh.point.json');hi=Q(v['objective_hi']);L=Q(v['dual_bound'])
check('ann upward primal and downward dual',shown('ann_cumene_tanh',4)>=hi and shown('ann_cumene_tanh',3)<=L)
emit('ann',(hi-L)/abs(hi)*100,'0.001',True)
emit('ann dual',(hi-L)/abs(L)*100,'0.001',True)
emit('ann wave3 primal',(hi-Q('-4024.495'))/abs(hi)*100,1,True)
emit('ann wave3 dual',(hi-Q('-4024.495'))/Q('4024.495')*100,'0.1',True)
for name in ('kan_r3_h1_n4','kan_r3_h1_n5','kan_r3_h1_n9','kan_r5_h1_n3','kan_r5_h1_n5','kan_r5_h1_n8'):
    v=J(f'publication/primal/water-ann-kan/points/{name}.point.json');hi=Q(v['objective_hi']);L=Q(v['dual_bound']);emit(name,hi-L,'1e-12' if name!='kan_r5_h1_n3' else '1e-10')
    check(name+' stored gap upper',Q(v['gap_upper'])>=hi-L)
    if name.endswith('n8'):check('KAN n8 upward display 0.0694',Q('0.0694')>=hi>Q('0.0693'))
v=J('bound-audit/logs/cert_socp_emfl050_3_3.json');L=Q(v['lower_bound_30_digits_rounded_down']);p=Q('10.40173793')
check('emfl absolute and relative at-least displays',L-p>=Q('1.42e-5') and (L-p)/L>=Q('1.36e-6') and (L-p)/L<Q('1.4e-6'))
print('EMFL exact relative lower bound',(L-p)/L)
# Campaign: re-count and compare with exact saved source decimals.
reader=csv.DictReader(read('publication/solver-runs/results_table.csv').splitlines());data=list(reader)
check('campaign 43 x 3',len(data)==129 and len({x['instance'] for x in data})==43)
finite=[x for x in data if x['dual'] and x['dual'] not in ('Infinity','-Infinity')]
check('campaign finite and valid counts',len(finite)==109 and sum(x['valid_time_measurement']=='True' for x in data)==126)
check('campaign all finite duals weaker',all((1 if x['sense']=='min' else -1)*(Q(x['certificate_dual'])-Q(x['dual']))>0 for x in finite))
check('campaign zero closures and two BARON claims',sum(x['closes_within_1h']=='True' for x in data)==0 and [x['instance'] for x in data if x['optimality_claim']=='True']==['camshape100','camshape200'])
check('campaign named memory stops', {x['instance'] for x in data if x['valid_time_measurement']=='False'}=={'ex6_2_5','ex6_2_7','pindyck'})
check('campaign disclaimers/overloaded/memory/tightenings',sum(x['globality_warning']=='True' for x in data)==6 and sum(x['loaded_first_batch']=='True' for x in data)==10 and sum(x['valid_time_measurement']=='False' and x['solver']=='SCIP' for x in data)==3 and sum(x['scip_argument_bounds_tightened']=='True' for x in data)==6)
print('COUNTS',dict(Counter(x['solver'] for x in finite)))
# Run G: each chunk's final success/failure total (no expensive certification).
count=0;fail=0;chunks=sorted((BASE/'publication/eg-recheck/logs').glob('cert_p*_c*.log'))
for p in chunks:
    text=read(str(p.relative_to(BASE)));m=re.search(r'certified\s+(\d+)\s*/\s*(\d+).*?failures\s*[:=]?\s*(\d+)',text)
    if not m:
        m=re.search(r'certified\s+(\d+)\s*/\s*(\d+)\s+failed\s+(\d+)',text)
    if m:
        check(p.name+' chunk equality',m[1]==m[2]);count+=int(m[1]);fail+=int(m[3])
    else:
        print('CHUNK FORMAT',p.name,text[-450:]);raise AssertionError('chunk log format')
check('run G total leaves zero failures',len(chunks)==38 and count==1114361 and fail==0)
(OUT/'gap-values.json').write_text(json.dumps(gaps,indent=2)+'\n')
(OUT/'number-checks.json').write_text(json.dumps({'checks':checks,'source_hashes':sources},indent=2)+'\n')
print('ALL CHECKS PASSED',len(checks))
