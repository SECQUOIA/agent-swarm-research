"""Fresh exact checks for integration-review facts; saved evidence only."""
import json
import re
from fractions import Fraction as Q
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[1]
results = {}
def read(rel):
    return (BASE/rel).read_text()
def check(name, condition, value):
    assert condition, (name, value)
    results[name] = str(value)
    print('PASS', name, value)

target = Q('5.760539610694994')
excess = target-Q(float(target))
check('eg_disc_s display above binary64 by about 2.4e-16',
      Q('2.35e-16') < excess < Q('2.45e-16'), excess)
leaves = []
for part in (0,1):
    text = read(f'reviews/eg-retry-review-checks/logs/verify_disc_p{part}.log')
    m = re.search(r'independent certification vs theta\* = (\S+): certified (\d+)/(\d+); failures (\d+)', text)
    check(f'eg_disc_s exact decimal target, part {part}', Q(m[1]) == target and m[2] == m[3] and int(m[4]) == 0, m[0])
    leaves.append(int(m[2]))
check('eg_disc_s leaves in two parts', leaves == [46223,40573], sum(leaves))
check('retry reviewer parses target without float conversion',
      'self.theta = Fr(theta)' in read('reviews/eg-retry-review-checks/indep_cert.py') and
      'path, name, theta = sys.argv[1], sys.argv[2], sys.argv[3]' in read('reviews/eg-retry-review-checks/verify_tree.py'), 'command-line string -> Fraction')

# Closeness uses the listed dual and the attained camshape optimum / lnts enclosure.
import csv
refs = list(csv.DictReader(read('publication/solver-runs/references.csv').splitlines()))
c = next(r for r in refs if r['instance'] == 'camshape100')
data = json.loads(read('reviews/open-instances-verification/logs/camshape_verify.json'))
lo = Q(next(x for x in data if x['n'] == 100)['envelope_exact']['obj'])
gap = (lo-Q(c['listed_dual']))/abs(lo)
check('camshape100 historical closeness rounds to 1.2e-6', Q('1.15e-6') < gap < Q('1.25e-6'), gap)
lhi = Q(json.loads(read('publication/primal/lnts/points/lnts50_point.json'))['objective_enclosure'][1])
lgap = (lhi-Q('0.55464755'))/lhi
check('lnts50 historical closeness rounds to 3.8e-5', Q('3.75e-5') < lgap < Q('3.85e-5'), lgap)
pointlog = read('publication/solver-runs/point_checks.log')
m = re.search(r'camshape100__SCIP objective (\S+) max violation (\S+)', pointlog)
deficit = lo-Q(m[1])
check('campaign camshape100 SCIP deficit rounds to 1.5e-7', Q('1.45e-7') < deficit < Q('1.55e-7'), deficit)
check('campaign row violation rounds to 7.7e-10', Q('7.65e-10') < Q(m[2]) < Q('7.75e-10'), m[2])

spring = re.search(r'spring\s+spring.p3.exact.sol.*exact: feasible, obj (\S+).*feasible, obj (\S+),', read('publication/audit-ir/logs/xcheck_scip.log'))
check('spring accepted objective difference', Q(spring[1])-Q(spring[2]) == Q('1e-9'), Q(spring[1])-Q(spring[2]))
pages = json.loads(read('bound-audit/pages.json'))
meth = next(p for p in pages if p['name'] == 'methanol50')
entry = next(x for x in meth['duals'] if x['value'] == '0.00802826')
print('methanol50 saved entry',entry)
check('methanol50 has six significant digits and eight decimals',
      entry['solver'] == 'LINDO' and entry['date'] == '15 Feb 2022' and
      len('00802826'.lstrip('0')) == 6 and len(entry['value'].split('.')[1]) == 8, entry)

# Read only scalar timing fields from npz, without pickle or project imports.
files = sorted((BASE/'publication/eg-recheck/res').glob('p*_c*.npz'))
elapsed = Q(0)
for p in files:
    with np.load(p, allow_pickle=False) as x:
        elapsed += Q(float(x['time']))
check('all-leaf saved timing fields, 38 chunks', len(files) == 38, len(files))
rounded = (2*elapsed.numerator+elapsed.denominator)//(2*elapsed.denominator)
check('aggregate chunk wall time rounds to 41162 seconds', rounded == 41162, elapsed)
printed = sum(int(re.search(r'; time (\d+)s', p.read_text())[1])
              for p in (BASE/'publication/eg-recheck/logs').glob('cert_p*_c*.log'))
check('sum of individually printed whole-second chunk times', printed == 41151, printed)
check('eg timing measures elapsed wall time', 'time=time.time() - t0' in read('publication/eg-recheck/recheck_leaves.py'), 'time.time(), not process_time()')
check('eg scheduler elapsed wall seconds', 'all jobs finished after 5372s' in read('publication/eg-recheck/logs/run_cert.out'), 5372)

history = read('publication/minlplib-status/report.md').split('More on the table:')[0]
no_pre = [line.split('|')[1].strip() for line in history.splitlines() if '| none (added ' in line]
group_sizes = [len(names.split(', ')) for names in no_pre]
check('nine instances have no pre-bound copy', group_sizes == [4,1,4] and sum(group_sizes) == 9,
      str(group_sizes)+': '+str(no_pre))
progress = json.loads(read('publication/reviews/solver-campaign-r2/PROGRESS.json'))
check('campaign review r2 did not complete', progress['done'] == [], progress['done'])
check('PARA printed percentage half-unit', Q('0.01')/2 == Q('0.005'), Q('0.01')/2)
pdftext = (OUT/'goess2026-r1.txt').read_text()
for n,gap in ((100,'0.00'),(200,'0.00'),(400,'0.01')):
    row = next(line for line in pdftext.splitlines() if re.match(rf'\s*lnts{n}\s+min\s+PARA',line))
    check(f'PARA lnts{n} printed gap', row.split()[-2] == gap, row.strip())
check('Martin spelling in source paper', 'Alexander Martin' in pdftext, 'Alexander Martin')
analysis = read('publication/reviews/solver-analysis-review-r1.md')
issues = re.findall(r'^### \d+\. (major|minor):',analysis,re.M)
check('solver analysis review r1 issue counts', issues.count('major') == 2 and issues.count('minor') == 4, issues)
minor = read('publication/reviews/minor-fixes-review-r2.md')
check('minor-fixes independent r2 counts', 'There are no blockers, 1 major issue and 10 minor issues.' in minor, '1 major, 10 minor')
env = json.loads((OUT/'environment-r1.json').read_text())
check('host core count and GiB conversion', env['physical_cores'] == 18 and env['logical_cpus'] == 36 and
      Q(env['mem_total_kib'])/1048576 == Q(env['mem_total_gib_exact']), env['mem_total_gib_exact'])
requirements = dict(line.split('==') for line in read('publication/reproduction/requirements.txt').splitlines() if line.strip())
check('all pinned package versions agree with requirements', requirements == env['pinned_reproduction']['packages'], requirements)
for solver,version in (('BARON','26.5.27'),('GUROBI','13.0.2'),('SCIP','10.0.3')):
    text = read(f'publication/solver-runs/runs/camshape100__{solver}/gams.log')
    check(f'campaign {solver} and GAMS versions', version in text and 'GAMS 54.3.1' in text, version)
(OUT/'review-r1-evidence.json').write_text(json.dumps(results, indent=2)+'\n')
