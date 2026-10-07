"""Shortfall decomposition on the large paths (E5 default and E5V feastol)."""
import sys
from scip_shortfall_cause import run
which = sys.argv[1]
if which == 'a':
    run('path', 128, 101)
else:
    run('path', 32, 101, feastol=1e-9)
