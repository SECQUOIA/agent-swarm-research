from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[5])

import ast
import glob
import os
import sys
from fractions import Fraction as F
import numpy as np

base='/tmp/sol-eg-audit-review/audit'
sys.path.insert(0,base+'/cert')
import auditor as A
assert F(A.YTINY)==F(1,2**1020)
assert F(A.PLO)==F(1,2**250)
assert F(A.PHI)==F(2**250)
print('Scalar power-derived boundary constants, exact dyadic values: PASS')

a=np.load('/tmp/sol-eg-audit-review/rerun/rec_int.npz')
b=np.load(base+'/out/rec/rec_int.npz')
assert set(a.files)==set(b.files)
differing=[k for k in b.files if not (a[k].dtype==b[k].dtype and a[k].shape==b[k].shape and a[k].tobytes()==b[k].tobytes())]
assert not differing,('regenerated recording',differing)
print('Independently regenerated eg_int_s recording: every saved field byte-identical;',len(a['P_lo']),'processed boxes')

for job in ('int','disc2_p7_c0'):
    a=np.load('/tmp/sol-eg-audit-review/rerun/'+job+'.npz')
    b=np.load(base+'/out/res/'+job+'.npz')
    ignore={'time'}
    differing=[k for k in b.files if k not in ignore and
        not (a[k].dtype==b[k].dtype and a[k].shape==b[k].shape and a[k].tobytes()==b[k].tobytes())]
    assert not differing,(job,differing)
    print(job,'all saved fields except elapsed time: byte-identical;',len(a['sel']),'leaves')

total=0
for f in sorted(glob.glob(base+'/out/res/*.npz')):
    z=np.load(f)
    job=os.path.basename(f)[:-4]
    stats=ast.literal_eval(str(z['stats']))
    counts=ast.literal_eval(str(z['audit_checked']))
    n=stats['pieces']*28*97
    # This adds the power-site multiplicities to compare_audit's exp check.
    assert counts['tau2']==3*n and counts['tau3']==2*n
    assert all(counts[k]==n for k in ('tay_E0','nat_Elo','nat_Ehi','tay_ell','p2','p3','p4'))
    assert counts['s2']>0 and counts['s2']%2==0
    assert len(z['ok'])==len(z['sel']) and z['ok'].all() and not z['abad'].any()
    assert str(z['audit_viol'])=='{}' and str(z['audit_examples'])=='[]'
    total+=sum(counts.values())
    theta='6.4531031529331155' if job=='int' else ('5.760539610694994' if job.startswith('disc_p') else '5.642100574331458')
    log=open(base+'/out/logs/cert_'+job+'.log').read()
    assert 'independent certification vs theta* = '+theta+':' in log
    assert 'failures 0 (by kind [])' in log
    assert str(stats) in log and str(counts) in log
    print(job,'threshold, success, all site multiplicities and zero-violation artifacts: PASS')
assert total==63017129222
print('Recorded audit-result total:',total)

# Independent negative coverage controls on the actual leaf outputs.
os.environ['EG_AUDIT_R']=(_PUBLIC_REPO + '/research-20260929')
sys.path.insert(0,base)
from compare_audit import prove_cover,gms_bounds
z=np.load(base+'/out/res/int.npz')
lo,hi=z['lo'],z['hi']
_,_,ii=gms_bounds('eg_int_s')
ok,_,_=prove_cover(lo,hi,ii,z['root_lo'],z['root_hi'])
assert ok
ok,why,_=prove_cover(lo[1:],hi[1:],ii,z['root_lo'],z['root_hi'])
assert not ok
print('Actual eg_int_s coverage with one leaf dropped: correctly rejected;',why)
print('Independent artifact checks: PASS')
