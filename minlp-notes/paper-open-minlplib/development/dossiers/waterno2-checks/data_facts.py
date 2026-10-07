"""Tariff factors, demands and horizon constants read exactly from the OSIL files (dossier check)."""
from fractions import Fraction as F
import osilmini
for T in [6, 9, 12, 18, 24]:
    m = osilmini.read(f'waterno2_{T:02d}.osil')
    V, C, R, NL = m['vars'], m['cons'], m['rows'], m['nonlin']
    kap = set(); dem = []
    for i, c in enumerate(C):
        r = R[i]
        if i not in NL and len(r) == 1 and c['lb'] is not None and c['lb'] == c['ub'] and c['lb'] > 0 and list(r.values())[0] == 1:
            dem.append((c['name'], c['lb']))
        if i not in NL and len(r) == 5 and c['ub'] == 0 and c['lb'] is None:
            neg = [v for v in r.values() if -1 < v < 0]
            if neg: kap.add(-neg[0])
    hor = [i for i in range(len(C)) if i not in NL and C[i]['lb'] is not None and C[i]['lb'] > 0 and C[i]['ub'] is None and len(R[i]) == T]
    print(f'T={T}: tariff factors {sorted(float(k) for k in kap)}; demand rows {len(dem)}; demands min {float(min(d for _, d in dem)):.9f} '
          f'max {float(max(d for _, d in dem)):.9f}; horizon rhs {C[hor[0]]["lb"]} = sum of demands: {C[hor[0]]["lb"] == sum(d for _, d in dem)}')
