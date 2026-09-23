"""Experiment driver.  Usage:
  python pipeline.py roots  [--procs N]   root-node runs of Gurobi and SCIP (incumbent phase)
  python pipeline.py obbt   [--procs N]   iterated-OBBT trajectories for each cutoff source
  python pipeline.py final  [--procs N] [--arms a,b,...]   final solves (baselines and OBBT boxes)
Results are appended to JSON-lines files in ../results; finished jobs are skipped on restart.
"""
import os, sys, json, math, time, argparse, hashlib, traceback
import numpy as np, pandas as pd
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from qcqp import QCQP

RES = os.path.join(HERE, '..', 'results')
BUDGET = 600.0          # total time per instance and arm, including root run and OBBT
ROOT_LIMIT = 30.0       # time limit of the root-node (incumbent) run: 5% of the budget
FP_CAP = 400.0          # time cap of the full (fixed-point) OBBT trajectories
AD_CAP = 120.0          # adaptive rule: OBBT time cap (20% of the budget)
THETAS = (0.5, 0.8)
SEEDS = (0, 1)

_env = None


def genv():
    global _env
    if _env is None:
        import gurobipy as gp
        _env = gp.Env(params={'OutputFlag': 0})
    return _env


def utol(U):
    return 1e-6 * max(1.0, abs(U))


def instances():
    d = pd.read_csv(os.path.join(RES, 'instances.csv'))
    return d[d.in_scope].sort_values('nvars').reset_index(drop=True)


def fbbt_box(name):
    f = np.load(os.path.join(RES, 'fbbt', name + '.npz'))
    return f['lb'], f['ub']


def done_keys(path):
    keys = set()
    if os.path.exists(path):
        for line in open(path):
            try:
                keys.add(json.loads(line)['key'])
            except Exception:
                pass
    return keys


def append(path, rec):
    with open(path, 'a') as fh:
        fh.write(json.dumps(rec) + '\n')


def run_pool(fn, jobs, procs, path):
    jobs = [j for j in jobs if j['key'] not in done_keys(path)]
    print('%d jobs' % len(jobs), flush=True)
    with Pool(procs, maxtasksperchild=4) as p:
        for rec in p.imap_unordered(fn, jobs, chunksize=1):
            append(path, rec)
            print(rec['key'], rec.get('status', ''), '%.1f' % rec.get('time', 0), flush=True)


# ------------------------------------------------------------------ roots
def root_job(j):
    from solvers import gurobi_run, scip_run
    P = QCQP(j['name'])
    rec = dict(j)
    try:
        if j['solver'] == 'grb':
            o = gurobi_run(P, genv(), time_limit=ROOT_LIMIT, seed=0, params={'NodeLimit': 1}, want_x=True)
        else:
            o = scip_run(P, time_limit=ROOT_LIMIT, seed=0, params={'limits/nodes': 1}, want_x=True)
        x = o.pop('x', None)
        if x is not None:
            os.makedirs(os.path.join(RES, 'roots_x'), exist_ok=True)
            np.save(os.path.join(RES, 'roots_x', '%s__%s.npy' % (j['name'], j['solver'])), np.array(x))
            o['viol'] = P.violation(np.array(x))
        rec.update(o)
    except Exception as e:
        rec.update(status='error', err=str(e)[:300], time=0)
    return rec


def load_roots():
    R = {}
    path = os.path.join(RES, 'roots.jsonl')
    if os.path.exists(path):
        for line in open(path):
            r = json.loads(line)
            R[(r['name'], r['solver'])] = r
    return R


# ------------------------------------------------------------------ OBBT
def cutoff_for(src, row, roots):
    """Cutoff U (minimization form) and the root run record, or (None, rec) if the root run solved it."""
    if src == 'known':
        return row['fstar_min'] + utol(row['fstar_min']), None
    r = roots[(row['name'], src)]
    if r['status'] == 'optimal':
        return None, r
    U = r.get('primal')
    return (math.inf if U is None else U + utol(U)), r


def save_box(name, src, tag, box):
    d = os.path.join(RES, 'boxes')
    os.makedirs(d, exist_ok=True)
    np.savez_compressed(os.path.join(d, '%s__%s__%s.npz' % (name, src, tag)), lb=box[0], ub=box[1])


def obbt_job(j):
    import relax
    name, src, U = j['name'], j['src'], j['U']
    P = QCQP(name)
    lb, ub = fbbt_box(name)
    rec = dict(j)
    try:
        trajs = {}
        nl = np.array(P.nlvars)
        w0 = (ub - lb)[nl]
        variants = [('full', dict(mode='GS', restrict=False, time_cap=FP_CAP)),
                    ('restr', dict(mode='GS', restrict=True, time_cap=FP_CAP, stop_when_ad_done=True))]
        if src == 'known':
            variants.append(('jacobi', dict(mode='J', restrict=False, time_cap=FP_CAP)))
            variants.append(('nofilt1', dict(mode='GS', restrict=False, filtering=False, max_rounds=1,
                                             time_cap=FP_CAP)))
        r1box = None
        for tag, kw in variants:
            t = time.time()
            if tag == 'restr':
                # the restricted trajectory shares round 1 with the full one: continue from its box
                R = relax.Relaxation(P, r1box[0], r1box[1], genv(), U)
                F = trajs['full']
                kw['prefix'] = dict(hist=F['hist'][:1], changed=F['changed1'], LB0=F['LB0'])
                tb = time.time() - t + F['build']
            else:
                R = relax.Relaxation(P, lb, ub, genv(), U)
                tb = time.time() - t
            out = relax.iterate(R, thetas=THETAS, theta_cap=AD_CAP, w0=w0, **kw)
            if tag == 'full':
                r1box = out['snaps']['r1']['box']
            snaps = {}
            for s, v in out['snaps'].items():
                keep = (tag == 'full' and s in ('r1', 'r5', 'fp')) or (tag == 'restr' and s.startswith('ad')) \
                    or (tag == 'jacobi' and s == 'fp')
                if keep:
                    save_box(name, src, s if tag != 'jacobi' else 'jfp', v['box'])
                snaps[s] = dict(round=v['round'], time=v['time'] + tb)
            trajs[tag] = dict(build=tb, hist=out['hist'], snaps=snaps, LB0=out['LB0'], nlp=R.nlp,
                              lptime=R.lptime, total=out['total'] + tb, changed1=out['changed1'])
            R.m.dispose()
        rec['trajs'] = trajs
        rec['status'] = 'ok'
        rec['time'] = sum(v['total'] for v in trajs.values())
    except Exception as e:
        rec.update(status='error', err=traceback.format_exc()[-600:], time=0)
    return rec


# ------------------------------------------------------------------ finals
def final_job(j):
    from solvers import gurobi_run, scip_run
    P = QCQP(j['name'])
    rec = dict(j)
    try:
        lb = ub = None
        if j.get('box'):
            f = np.load(os.path.join(RES, 'fbbt', j['box'][5:] + '.npz') if j['box'].startswith('FBBT:')
                        else os.path.join(RES, 'boxes', j['box'] + '.npz'))
            lb, ub = f['lb'], f['ub']
        start = None
        if j.get('start'):
            start = np.load(os.path.join(RES, 'roots_x', j['start'] + '.npy'))
            if lb is not None:
                start = np.clip(start, lb, ub)
        tl = j['tl']
        if tl <= 0.01:
            rec.update(status='nobudget', time=0.0, nodes=0, primal=None, dual=None, root_dual=None)
            return rec
        if j['solver'] == 'grb':
            params = dict(j.get('params') or {})
            if j.get('cutoff') is not None and math.isfinite(j['cutoff']):
                params['Cutoff'] = P.sense * j['cutoff']
            o = gurobi_run(P, genv(), lb, ub, time_limit=tl, seed=j['seed'], params=params, start=start,
                           want_x=j.get('want_x', False))
        else:
            cut = j.get('cutoff')
            o = scip_run(P, lb, ub, time_limit=tl, seed=j['seed'], params=j.get('params'), start=start,
                         objlim=cut if cut is not None and math.isfinite(cut) else None,
                         want_x=j.get('want_x', False))
        x = o.pop('x', None)
        if x is not None:
            os.makedirs(os.path.join(RES, 'final_x'), exist_ok=True)
            np.save(os.path.join(RES, 'final_x', j['key'].replace('/', '_') + '.npy'), np.array(x))
        rec.update(o)
    except Exception as e:
        rec.update(status='error', err=traceback.format_exc()[-600:], time=0)
    return rec


def box_hash(tag):
    f = np.load(os.path.join(RES, 'boxes', tag + '.npz'))
    return hashlib.md5(f['lb'].tobytes() + f['ub'].tobytes()).hexdigest()


def final_jobs(arms):
    inst = instances()
    roots = load_roots()
    ob = {}
    path = os.path.join(RES, 'obbt.jsonl')
    if os.path.exists(path):
        for line in open(path):
            r = json.loads(line)
            if r['status'] == 'ok':
                ob[(r['name'], r['src'])] = r
    jobs = []
    for row in inst.to_dict('records'):
        name = row['name']
        for seed in SEEDS:
            if 'base' in arms:
                jobs.append(dict(key='%s/grb/base/%d' % (name, seed), name=name, solver='grb', arm='base',
                                 seed=seed, tl=BUDGET, want_x=(seed == 0)))
                jobs.append(dict(key='%s/scip/base/%d' % (name, seed), name=name, solver='scip', arm='base',
                                 seed=seed, tl=BUDGET))
            if 'obbt3' in arms:
                jobs.append(dict(key='%s/grb/obbt3/%d' % (name, seed), name=name, solver='grb', arm='obbt3',
                                 seed=seed, tl=BUDGET, params={'OBBT': 3}))
            for solver in ('grb', 'scip'):
                r = roots.get((name, solver))
                if 'none' in arms and r is not None and r['status'] != 'optimal':
                    # control: root run + incumbent, FBBT box only (no OBBT)
                    U = r['primal'] + utol(r['primal']) if r.get('primal') is not None else math.inf
                    jobs.append(dict(key='%s/%s/pipe-none/%d' % (name, solver, seed), name=name, solver=solver,
                                     arm='pipe-none', seed=seed, box='FBBT:' + name,
                                     start='%s__%s' % (name, solver) if math.isfinite(U) else None,
                                     cutoff=U, t_root=r['time'], t_obbt=0.0, tl=BUDGET - r['time']))
                if 'pipe' in arms:
                    r = roots.get((name, solver))
                    if r is None or r['status'] == 'optimal' or (name, solver) not in ob:
                        continue
                    o = ob[(name, solver)]
                    seen = {}
                    for rule in ('r1', 'r5', 'ad0.5', 'ad0.8', 'fp'):
                        traj = 'restr' if rule.startswith('ad') else 'full'
                        tag = '%s__%s__%s' % (name, solver, rule)
                        h = box_hash(tag)
                        t_obbt = o['trajs'][traj]['snaps'][rule]['time']
                        # identical box: the final run is shared; only the accounted OBBT time differs
                        if h in seen:
                            continue
                        seen[h] = rule
                        U = o['U']
                        jobs.append(dict(key='%s/%s/pipe-%s/%d' % (name, solver, rule, seed), name=name,
                                         solver=solver, arm='pipe-' + rule, seed=seed, box=tag,
                                         start='%s__%s' % (name, solver) if math.isfinite(U) else None,
                                         cutoff=U, t_root=r['time'], t_obbt=t_obbt,
                                         tl=BUDGET - r['time'] - t_obbt))
                if 'known' in arms and (name, 'known') in ob and seed == 0:
                    # reference arm (known optimum as cutoff): fixed-point box only, seed 0 only
                    o = ob[(name, 'known')]
                    seen = set()
                    for rule in ('fp',):
                        tag = '%s__known__%s' % (name, rule)
                        h = box_hash(tag)
                        if h in seen:
                            continue
                        seen.add(h)
                        t_obbt = o['trajs']['full']['snaps'][rule]['time']
                        jobs.append(dict(key='%s/%s/known-%s/%d' % (name, solver, rule, seed), name=name,
                                         solver=solver, arm='known-' + rule, seed=seed, box=tag,
                                         t_obbt=t_obbt, tl=BUDGET - t_obbt))
    return jobs


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('stage')
    ap.add_argument('--procs', type=int, default=18)
    ap.add_argument('--arms', default='base,obbt3,pipe,known')
    ap.add_argument('--names', default=None)
    a = ap.parse_args()
    inst = instances()
    if a.names:
        inst = inst[inst.name.isin(a.names.split(','))]
    if a.stage == 'roots':
        jobs = [dict(key='%s/%s' % (n, s), name=n, solver=s) for n in inst.name for s in ('grb', 'scip')]
        run_pool(root_job, jobs, a.procs, os.path.join(RES, 'roots.jsonl'))
    elif a.stage == 'obbt':
        roots = load_roots()
        jobs = []
        for row in inst.to_dict('records'):
            for src in ('known', 'grb', 'scip'):
                if src != 'known' and (row['name'], src) not in roots:
                    continue
                U, r = cutoff_for(src, row, roots)
                if U is None:
                    continue
                jobs.append(dict(key='%s/%s' % (row['name'], src), name=row['name'], src=src, U=U))
        jobs.sort(key=lambda j: -inst.set_index('name').loc[j['name'], 'nnl'])   # big ones first
        run_pool(obbt_job, jobs, a.procs, os.path.join(RES, 'obbt.jsonl'))
    elif a.stage == 'final':
        jobs = final_jobs(set(a.arms.split(',')))
        if a.names:
            jobs = [j for j in jobs if j['name'] in set(a.names.split(','))]
        run_pool(final_job, jobs, a.procs, os.path.join(RES, 'final.jsonl'))
