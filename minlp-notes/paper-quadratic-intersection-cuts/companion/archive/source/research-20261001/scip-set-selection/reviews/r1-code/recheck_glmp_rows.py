"""Review r1: re-evaluate every intersection row that the debug build reported as violating the supplied
st_glmp_fp2 solution, after giving the OSiL objective helper t_nlobjvar its value x3*x4 at that solution.
Independent of the stream's debugsol_analysis.py. Also checks the supplied point against the OSiL constraints and
records whether each report came before or after the first incumbent."""
import glob, os, re
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'logs', 'debugsol')
# supplied solution (sources/sol/st_glmp_fp2.p1.sol): x1 absent (= 0), x2 = x3 = 5.65, x4 = 1.35
x1, x2, x3, x4 = 0.0, 5.65, 5.65, 1.35
cons = {'e1': 2*x1 + x2 <= 14, 'e2': x1 + x2 <= 10, 'e3': 1.44*x1 + x2 >= 4.89, 'e4': -1.58*x1 + x2 <= 5.65 + 1e-12,
        'e5': -1.03*x1 + x2 <= 5.93, 'e6': x1 + 2*x2 >= 6, 'e7': x1 - x2 <= 3, 'e9': abs(x1 + x2 - x3) < 1e-12,
        'e10': abs(x1 - x2 - x4 + 7) < 1e-12}
print('supplied point feasible for all OSiL constraints:', all(cons.values()), 'objective x3*x4 =', x3 * x4,
      '(minlplib.solu =opt= 7.3445454180)')
NL = x3 * x4
term = re.compile(r'([-+]\d[\d.eE+-]*)<([^>]+)>\[([^\]]+)\]')
tot = 0; minslack = None; negcoef = 0; after_inc = 0; worst = None
for f in sorted(glob.glob(os.path.join(D, 'st_glmp_fp2.*.log'))):
    lines = open(f, errors='replace').read().split('\n')
    incumbent = False
    for k, l in enumerate(lines):
        if re.match(r'^[*a-zA-Z]?\s*\d+\.\d+s\|', l) and not re.search(r'\|\s+--\s+\|', l):
            incumbent = True
        if l.startswith('***** debug: violated row <under_intersection'):
            row = lines[k + 1]
            m = re.match(r'\s*(\S+) <= (\S+)(.*) <= (\S+)\s*$', row)
            lhs, const, body, rhs = float(m.group(1)), float(m.group(2)), m.group(3), float(m.group(4))
            act_logged = const; act = const
            names = []
            for c, v, val in term.findall(body):
                c, val = float(c), float(val)
                names.append(v)
                act_logged += c * val
                if v == 't_nlobjvar':
                    if c < 0:
                        negcoef += 1
                    val = NL
                act += c * val
            assert set(names) <= {'t_x1', 't_x2', 't_nlobjvar'}, names
            slack = min(act - lhs, rhs - act)
            tot += 1
            after_inc += incumbent
            if minslack is None or slack < minslack:
                minslack = slack; worst = (os.path.basename(f), row.strip())
            print('%-28s logged slack %+.6g  corrected slack %+.6g  incumbent known: %s' % (
                os.path.basename(f), min(act_logged - lhs, rhs - act_logged), slack, incumbent))
print('rows:', tot, 'min corrected slack:', minslack, 'rows with negative t_nlobjvar coefficient:', negcoef,
      'reported after an incumbent was known:', after_inc)
print('worst:', worst)
