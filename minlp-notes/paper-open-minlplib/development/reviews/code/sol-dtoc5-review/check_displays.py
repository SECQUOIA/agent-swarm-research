"""Check the authored review's displays against independent rational enclosures."""
from fractions import Fraction as F
from pathlib import Path
import json
import os

work = Path(__file__).resolve().parent
result = json.loads((work / 'result.json').read_text())
review = (Path(os.environ['MINLP_REPO_ROOT']) / 'paper-open-minlplib/development/reviews/sol-dtoc5-exact.md').read_text()
safe = result['safe_displays']
enclosures = result['decimal_enclosures']
lower = safe['dual_down_44']
upper = safe['primal_up_44']
assert lower in review and upper in review
assert F(lower) < F(enclosures['dual']['down_100'])
assert F(upper) > F(enclosures['primal']['up_100'])
assert F(upper) - F(lower) == F('7.3e-43')
assert F(enclosures['gap']['down_100']) > F('7.2e-43')
assert F(enclosures['gap']['up_100']) < F('7.205104e-43') < F('7.21e-43')
# The dossier's rounded lower bound also permits 7.21e-43.
primal = F((work / 'primal_exact.txt').read_text())
dossier = F((work / 'dossier_lower_exact.txt').read_text())
assert primal - dossier < F('7.21e-43')
print('PASS: paper endpoints, interval width, and both rounded-up gap displays')
