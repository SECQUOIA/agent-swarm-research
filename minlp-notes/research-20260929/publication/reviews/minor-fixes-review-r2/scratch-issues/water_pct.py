"""Exact check of the water percentage displays from report table values (truncated objectives give lower bounds on gap; add 1e-15 slack upward)."""
from fractions import Fraction as F
rows = {  # name: (objective truncated decimal, dual, displayed percent)
 'waterno2_06': ('282.888037386904807969455615812871', '278.230573774560', '1.674', '1.68'),
 'waterno2_09': ('914.011975237085991', '824.834692454636', '10.82', None),
 'waterno2_12': ('2233.821345608215233', '2089.754565439515', '6.90', None),
 'waterno2_18': ('5023.982760460661871', '4790.820715376162', '4.87', None),
 'waterno2_24': ('6963.795180156419512', '6576.151388415564', '5.90', None),
}
for n, (o, d, p, p2) in rows.items():
    o = F(o); d = F(d)
    hi = o + F(1, 10**15)   # truncated objective: true value < o + 1e-15
    r_lo = (o - d) / d; r_hi = (hi - d) / d
    print(n, 'ratio%% in [%.10f, %.10f]' % (float(100*r_lo), float(100*r_hi)), 'display', p, 'upper:', F(p)/100 >= r_hi, ('display2 %s upper: %s' % (p2, F(p2)/100 >= r_hi)) if p2 else '')
