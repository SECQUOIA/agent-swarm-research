# emfl: listed values against the exact lower bounds (audit cert_socp logs, 30-digit rounded down; recheck outward)
from fractions import Fraction as F
L = {'emfl050_3_3': (F('10401752131628136706037811564216e-30'), F('10.4017521318429')),
     'emfl050_5_5': (F('18913632952947218470895064479671e-30'), F('18.9136329557291')),
     'emfl100_3_3': (F('18132653119485885873539965320367e-30'), F('18.1326531242336')),
     'emfl100_5_5': (F('32638190351378666062905969451502e-30'), F('32.6381903545115'))}
vals = {'emfl050_3_3': [('best listed primal p2', '10.40173793'), ('best dual LINDO/SCIP', '10.40173999')],
        'emfl050_5_5': [('best listed primal p6', '18.91165289'), ('best dual', '18.91340776')],
        'emfl100_3_3': [('best listed primal p4', '18.13236088'), ('best dual', '18.13262446')],
        'emfl100_5_5': [('best listed primal p1', '32.63818348'), ('best dual', '32.63818348')]}
for n, (La, Lr) in L.items():
    for lab, s in vals[n]:
        v = F(s); k = len(s.split('.')[1]); half = F(1, 2 * 10**k)
        for nm, Lb in (('audit L', La), ('recheck L', Lr)):
            lit = Lb - v; wid = Lb - (v + half)
            print(f"{n:12s} {lab:22s} {nm:9s} literal {float(lit):.6e} (rel {float(lit/Lb):.6e})  widened {float(wid):.6e} (rel {float(wid/Lb):.6e})")
