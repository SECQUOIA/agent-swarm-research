"""Group D: for each log in report Section 5.3, is it instrumented (SCIPBUG lines) and what
precedes the first debug-solution loss (cut off / invalid bound)?"""
import os, re, glob
T = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scip-bug', 'logs'))
logs = ['dbgsol_tiny2', 'dbgsol_pumps_default', 'dbgsol_fm336_v1010', 'dbgsol_sb_pair2236_seed8',
        'dbgsol_expr_pair2236_seed8', 'dbgsol_expr_p4_seed0', 'dbgsol_expr_p5_seed0', 'dbgsol_expr_p5_seed2',
        'dbgsol_expr_p0_seed2', 'mdbg_fm336_s0', 'mdbg_fm318_s0', 'mdbg_pumps_default_s3', 'mdbg_tiny2_hsoff',
        'mdbg_pair2236_s14', 'mdbg_p4_s0', 'mdbg_p5_s3', 'dbgsol_pair2236_seed11', 'dbgsol_pair2236_seed8']
pat = re.compile(r'debugging solution was cut off|invalid (local|global) (lower|upper) bound')
for n in logs:
    L = open(os.path.join(T, n + '.log'), errors='replace').read().splitlines()
    nb = sum('SCIPBUG' in l for l in L)
    i = next((k for k, l in enumerate(L) if pat.search(l)), None)
    prev = None
    if i is not None:
        prev = next((L[k] for k in range(i - 1, -1, -1) if 'SCIPBUG' in L[k]), None)
    print(f'{n}: SCIPBUG lines {nb}; first loss line {i}: {L[i][:110] if i is not None else None}')
    print(f'    last SCIPBUG before it: {prev[:170] if prev else None}')
