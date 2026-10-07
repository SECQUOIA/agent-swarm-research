"""Cut-validity check with the debug-solution build (DEBUGSOL=ON): SCIP checks every added cut row against the
MINLPLib solution (sources/sol/INST.p1.sol) and prints '***** debug: row <...> violates debugging solution' if a
cut cuts it off.  Primal heuristics are switched off so that the incumbent reaches the reference value later (SCIP
stops checking once the incumbent is at least as good as the debugging solution).  Symmetry handling is switched
off, because symmetry-breaking cuts and fixings may legitimately exclude the particular debugging solution (seen in
the first run, logs/debugsol_withsym/).

Usage: python3 run_debugsol.py OUTDIR INSTLIST SETTINGS TIMELIMIT NPROC
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import os, sys, subprocess, itertools, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_bench import SETTINGS, OSIL   # noqa: E402

BINARY = (_PUBLIC_HOME + '/build-scip/selection/build-debugsol/bin/scip')
SOL = os.path.join(HERE, '..', 'sources', 'sol')


def run(job):
    inst, setting, tl, outdir = job
    log = os.path.join(outdir, '%s.%s.s0.log' % (inst, setting))
    if os.path.exists(log) and '@@ wallclock' in open(log, errors='replace').read():
        return log, 'skip'
    sol = os.path.abspath(os.path.join(SOL, inst + '.p1.sol'))
    c = ('set misc debugsol %s set heuristics emphasis off set misc usesymmetry 0 set table nlhdlr_quadratic active TRUE '
         'set limits memory 6000 set limits time %d set timing clocktype 1 ' % (sol, tl))
    c += SETTINGS[setting] + 'read %s/%s.osil opt display statistics quit' % (OSIL, inst)
    t0 = time.time()
    with open(log, 'w') as f:
        try:
            rc = subprocess.run([BINARY, '-c', c], stdout=f, stderr=subprocess.STDOUT, timeout=tl * 2 + 120).returncode
        except subprocess.TimeoutExpired:
            rc = 'TIMEOUT'
        f.write('\n@@ wallclock %.2f returncode %s\n' % (time.time() - t0, rc))
    return log, rc


if __name__ == '__main__':
    outdir, instlist, settings, tl, nproc = sys.argv[1:6]
    os.makedirs(outdir, exist_ok=True)
    insts = [l.strip() for l in open(instlist) if l.strip()]
    jobs = [(i, s, int(tl), outdir) for i, s in itertools.product(insts, settings.split(','))
            if os.path.exists(os.path.join(SOL, i + '.p1.sol'))]
    print('jobs', len(jobs), flush=True)
    with ThreadPoolExecutor(int(nproc)) as ex:
        for k, (log, rc) in enumerate(ex.map(run, jobs), 1):
            if rc not in (0, 'skip'):
                print('rc', rc, log, flush=True)
    print('finished', len(jobs), flush=True)
