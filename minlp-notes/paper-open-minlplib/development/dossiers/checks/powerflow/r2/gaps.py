# Exact gap and display checks (this is the code that was run inline to produce gaps.log)
from fractions import Fraction as Fr
import json
d30=Fr(json.load(open('data/powerflow0030p.sdpcert.json'))['bound_exact'])
d39p=Fr(json.load(open('data/powerflow0039p.bb3t.json'))['LB_exact'])
d39r=Fr(json.load(open('data/powerflow0039r.bb3t.json'))['LB_exact'])
def dec(q,n=22):
    s='-' if q<0 else ''; q=abs(q); i=q.numerator//q.denominator; f=q-i
    return s+str(i)+'.'+str((f*10**n).numerator//(f*10**n).denominator).zfill(n)
rows=[('powerflow0030p',d30,Fr('576.8934122988004'),Fr('576.8934134703742598676684'),Fr('576.8934134704'),Fr('576.8934134703742598676683'),Fr('2.1e-9'),Fr('572.8395847')),
      ('powerflow0039p',d39p,Fr('41869.05148485014'),Fr('41869.0515113202038027683845'),Fr('41869.0515113203'),Fr('41869.0515113202038027683844'),Fr('6.4e-10'),Fr('41818.27916')),
      ('powerflow0039r',d39r,Fr('41869.05148327243'),Fr('41869.0515113209830932768582'),Fr('41869.0515113210'),Fr('41869.0515113209830932768581'),Fr('6.7e-10'),Fr('41804.88153'))]
for n,ex,disp,up,pdisp,lo,relcell,listed in rows:
    print(n)
    print('  exact certificate      ', dec(ex))
    print('  summary dual display   ', dec(disp), ' display <= exact:', disp<=ex, ' exact-display =', float(ex-disp))
    print('  enclosure upper        ', dec(up), ' primal display >= upper:', pdisp>=up, ' display-upper =', float(pdisp-up))
    print('  dual < enclosure lower:', ex<lo)
    g=up-disp; print('  abs gap (upper - display dual) =', float(g), ' rel =', float(g/disp), ' summary cell', float(relcell), 'ok:', g/disp<=relcell)
    g2=up-ex; print('  abs gap (upper - exact cert) =', float(g2), ' rel =', float(g2/ex))
    print('  improvement over best listed dual: abs', float(disp-listed), ' rel to our dual', float((disp-listed)/disp))
print('0039r extension display 41869.05148327244 - exact stored LB =', float(Fr('41869.05148327244')-d39r))
print('0039p extension display 41869.05148485014 <= exact stored LB:', Fr('41869.05148485014')<=d39p, float(d39p-Fr('41869.05148485014')))
print('0030p printed float 576.8934122988005 - exact =', float(Fr('576.8934122988005')-d30))
