# Critic: compare the dossier's catmix primal values with the exact enclosure ends saved in
# R/publication/reproduction/cops/logs/v_catmix_model_all.log (100/200) and exact_display_checks.json (400/800).
from fractions import Fraction as F
rows = [  # (instance, exact upper end from saved log, value written in the dossier Section 5.3)
 ('catmix100', '-0.048069432030959562924734533987703146187132711788665927218259922377', '-0.0480694320309595635'),
 ('catmix200', '-0.048059145580114393563745030822862486164614881950414095897713142991', '-0.0480591455801143916'),
 ('catmix400', '-0.048056547756611554855186829086783477043026066787866243854864283091', '-0.048056547756611554855'),
 ('catmix800', '-0.048055901331230800339383491203', '-0.0480559013312308003')]
for n, ex, dv in rows:
    x = F(ex)
    print(f"{n}: float(exact) printed %.20g = {float(x):.20g}; dossier {dv}; dossier - exact = {float(F(dv) - x):+.3e}; "
          f"{'valid upper bound' if F(dv) >= x else 'NOT an upper bound'}")
# hvycrash: objective constant under the decimal reading vs the binary64 reading of 4.37e-3
b = F(4.37e-3)
print('hvycrash: 50*binary64(4.37e-3) - 0.2185 =', float(50 * b - F('0.2185')))
