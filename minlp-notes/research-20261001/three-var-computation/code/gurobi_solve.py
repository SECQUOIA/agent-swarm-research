"""Solve a box QP instance globally with the Gurobi command line (NonConvex=2).
Usage: python gurobi_solve.py file.lp timelimit threads logfile"""

import os, re, subprocess, sys
env = dict(os.environ, LD_LIBRARY_PATH='/opt/gurobi1302/linux64/lib')
def solve(lp, tl=600, threads=1, log=None, mipgap=1e-6):
    sol = lp + '.sol'
    cmd = ['/opt/gurobi1302/linux64/bin/gurobi_cl', 'NonConvex=2', 'TimeLimit=%g' % tl, 'Threads=%d' % threads,
           'MIPGap=%g' % mipgap, 'MIPGapAbs=1e-6', 'FeasibilityTol=1e-9', 'ResultFile=' + sol]
    if log: cmd.append('LogFile=' + log)
    cmd.append(lp)
    out = subprocess.run(cmd, env=env, capture_output=True, text=True).stdout
    m = re.search(r'Best objective ([-+0-9.e]+), best bound ([-+0-9.e]+), gap ([-+0-9.e]+)%', out)
    status = 'optimal' if 'Optimal solution found' in out else 'other'
    if m:
        return status, float(m.group(1)), float(m.group(2)), out
    return status, None, None, out
if __name__ == '__main__':
    st, ub, lb, out = solve(sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else None)
    print(st, ub, lb)
