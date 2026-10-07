"""Count stored certificates only; no leaf re-certification or tree replay."""
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parent; total=side=farkas=split=inf=0
for f in sorted((p/'res').glob('p*_c*.npz')):
 with np.load(f) as v:
  mg=v['mg'];how=v['how'];sel=v['sel']; mask=mg==np.inf
  total+=len(sel); side+=int((mask&(how==1)).sum()); farkas+=int((mask&(how==3)).sum()); split+=int((mask&(how==5)).sum());inf+=int(mask.sum())
assert (total,inf,side,farkas,split)==(1114361,98234,85685,373,12176)
print('leaves',total,'no point with F < theta*',inf,'side-infeasible',side,'Farkas',farkas,'after splitting',split)
print('PASS: semantic correction; no counts or verdict changed.')
