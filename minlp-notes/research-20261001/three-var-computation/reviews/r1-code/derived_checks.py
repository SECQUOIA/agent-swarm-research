"""Reviewer r1: per-instance details for two derived Section 4.5 claims (KA shortfall; XF/F time)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import tables_recompute as T
for d in ('chain', 'cactus'):
    for tag, r in T.method_rows(d).items():
        sstar = max(r[m]['safe'] for m in r if isinstance(r[m], dict) and 'safe' in r[m] and m != 'B')
        trip = lambda m: (r[m]['safe'] - r['B_safe']) / (sstar - r['B_safe'])
        print('%-22s F-KA %.2fpp KAF-KA %.2fpp (U-closure); F-KA %.2fpp (triple closure); XF/F time %.2f (XF %.2f s, F %.2f s)' % (
            tag, 100 * (r['F']['closed'] - r['KA']['closed']), 100 * (r['KAF']['closed'] - r['KA']['closed']),
            100 * (trip('F') - trip('KA')), r['XF']['time'] / r['F']['time'], r['XF']['time'], r['F']['time']))
