"""Run the patched SCIP binary on MINLPLib instances under named settings, in parallel.

Usage:
  python3 run_bench.py OUTDIR INSTLIST SETTINGS SEEDS MODE TIMELIMIT NPROC [BINARY]
    OUTDIR    directory for logs (one log per run: INST.SETTING.sSEED.log)
    INSTLIST  file with one instance name per line
    SETTINGS  comma-separated setting names (see SETTINGS below)
    SEEDS     comma-separated permutation seeds (0 = SCIP default, no permutation)
    MODE      'root' (limits/nodes = 1) or 'full'
    TIMELIMIT seconds
    NPROC     parallel processes
Existing logs that contain a final statistics block are skipped (resumable).
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import os, sys, subprocess, itertools, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
OSIL = os.path.expanduser('~/.cache/minlplib/minlplib/osil')
BINARY = (_PUBLIC_HOME + '/build-scip/selection/build-lapack/bin/scip')

CUTS = 'set nlhdlr quadratic useintersectioncuts TRUE '
STRENGTH = 'set nlhdlr quadratic usestrengthening TRUE '
SETTINGS = {
    'off': '',
    'scip': CUTS,
    'corner': CUTS + 'set nlhdlr quadratic setrule 1 ',
    'eff': CUTS + 'set nlhdlr quadratic setrule 2 ',
    'scipS': CUTS + STRENGTH,
    'cornerS': CUTS + STRENGTH + 'set nlhdlr quadratic setrule 1 ',
    'effS': CUTS + STRENGTH + 'set nlhdlr quadratic setrule 2 ',
}


def command(inst, setting, seed, mode, tl):
    c = 'set table nlhdlr_quadratic active TRUE set limits memory 6000 set limits time %d ' % tl
    c += 'set timing clocktype 1 '          # CPU time (machine is shared with other jobs)
    c += SETTINGS[setting]
    if seed:
        c += 'set randomization permutationseed %d ' % seed
    if mode == 'root':
        c += 'set limits nodes 1 '
    c += 'read %s/%s.osil opt display statistics quit' % (OSIL, inst)
    return c


def run(job):
    inst, setting, seed, mode, tl, outdir, binary = job
    log = os.path.join(outdir, '%s.%s.s%d.log' % (inst, setting, seed))
    if os.path.exists(log):
        with open(log, errors='replace') as f:
            if 'Quadratic SetSel' in f.read():
                return log, 'skip'
    t0 = time.time()
    with open(log, 'w') as f:
        try:
            p = subprocess.run([binary, '-c', command(inst, setting, seed, mode, tl)], stdout=f, stderr=subprocess.STDOUT,
                               timeout=tl * 2 + 120, env=dict(os.environ, OMP_NUM_THREADS='1'))
            rc = p.returncode
        except subprocess.TimeoutExpired:
            rc = 'TIMEOUT'
        f.write('\n@@ wallclock %.2f returncode %s\n' % (time.time() - t0, rc))
    return log, rc


if __name__ == '__main__':
    outdir, instlist, settings, seeds, mode, tl, nproc = sys.argv[1:8]
    binary = sys.argv[8] if len(sys.argv) > 8 else BINARY
    os.makedirs(outdir, exist_ok=True)
    insts = [l.strip() for l in open(instlist) if l.strip() and not l.startswith('#')]
    jobs = [(i, s, int(sd), mode, int(tl), outdir, binary)
            for i, s, sd in itertools.product(insts, settings.split(','), seeds.split(','))]
    print('jobs', len(jobs), flush=True)
    done = 0
    with ThreadPoolExecutor(int(nproc)) as ex:
        for log, rc in ex.map(run, jobs):
            done += 1
            if rc not in (0, 'skip'):
                print('rc', rc, log, flush=True)
            if done % 50 == 0:
                print('done', done, time.strftime('%H:%M:%S'), flush=True)
    print('finished', done, flush=True)
