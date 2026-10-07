"""Group C: waterno2 gap ratios from stored exact objectives and the r1 reviewer's dual values."""
import json
from fractions import Fraction as F
from pathlib import Path
P = Path(__file__).resolve().parents[3] / 'primal/water-ann-kan/points'
duals = {'06': F(39157472136693483, 140737488355328), '09': F(824.8346924546364), '12': F(2089.7545654395158),
         '18': F(4790.820715376162), '24': F(6576.151388415564)}
shown = {'06': ('1.674%', '1.674e-2', '1.647e-2'), '09': ('10.82%', '1.082e-1', '9.757e-2'),
         '12': ('6.89%', '6.894e-2', '6.450e-2'), '18': ('4.87%', '4.867e-2', '4.641e-2'),
         '24': ('5.90%', '5.895e-2', '5.567e-2')}
for n, d in duals.items():
    f = F(json.loads((P / f'waterno2_{n}.exact.json').read_text())['objective'])
    g = f - d
    rd, rp = g / abs(d), g / abs(f)
    t = shown[n]
    print(f"{n}: gap {float(g):.10g} gap/dual {float(rd):.7e} gap/primal {float(rp):.7e}; shown text {t[0]} "
          f"({'>=' if F(t[0][:-1])/100 >= rd else 'BELOW'} exact), table dual {t[1]} ({'>=' if F(t[1]) >= rd else 'BELOW'}), "
          f"table primal {t[2]} ({'>=' if F(t[2]) >= rp else 'BELOW'})")
