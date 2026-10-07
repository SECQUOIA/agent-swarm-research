import gzip
from fractions import Fraction as F
pt={}
for line in gzip.open('dtoc5_point.txt.gz','rt'):
    if line.startswith('#') or not line.strip(): continue
    k,v=line.split(); pt[k]=F(v)
h=F('2e-05'); h4=F('8e-05')
flh=F(float(h)); flh4=F(float(h4))
print('fl(8e-5)==4fl(2e-5):', flh4==4*flh, 'fl(h)!=h:', flh!=h)
u0=pt['x2']; y0=pt.get('x50001',F(1)); y1=pt['x50002']
rb=-h*u0+y0-y1+h4*y0*y0
rc=-flh*u0+y0-y1+flh4*y0*y0
print('reading b residual', rb)
print('reading c residual float', float(rc), 'formula equal', rc==(flh-h)*(4*y0*y0-u0))
print('u0', float(u0), 'y0', y0, 'x50001 in point', 'x50001' in pt)
