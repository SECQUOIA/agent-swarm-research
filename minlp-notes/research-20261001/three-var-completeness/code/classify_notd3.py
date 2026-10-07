import json, glob, collections, sys
import numpy as np
from cube3 import *
from zero_pattern import zeros

def canon_pattern(pvec, tol=1e-5):
    z = zeros(pvec, tol)
    faces = []
    for st, x in z:
        faces.append(tuple(st))
    # canonical form under the 48 symmetries: map face status tuples
    best = None
    for perm, flips in GROUP:
        img = []
        for st in faces:
            new = [None] * 3
            for i in range(3):
                s = st[perm[i]]
                if s != -1 and flips[i]: s = 1 - s
                new[i] = s
            img.append(tuple(new))
        img = tuple(sorted(img))
        if best is None or img < best: best = img
    return best

files = sys.argv[1:]
cnt = collections.Counter(); ex = {}
for f in files:
    for o in json.load(open(f)):
        if o.get('r0', 0) < -1e-6:
            p = np.array(o['p']); key = canon_pattern(p)
            cnt[key] += 1; ex.setdefault(key, (o.get('r0'), o.get('r1'), np.round(p, 4).tolist()))
for k, v in cnt.most_common():
    print(v, k, ex[k][:2])
