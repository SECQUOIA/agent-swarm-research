"""Analysis of the iterated-OBBT experiment.  Writes CSV tables to ../results and prints summaries."""
import os, sys, json, math, hashlib
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results')
BUDGET = 600.0
RULES = ('r1', 'r5', 'ad0.5', 'ad0.8', 'fp')
pd.set_option('display.width', 250)
pd.set_option('display.max_columns', 40)


def jl(fn):
    p = os.path.join(RES, fn)
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else []


def sgm(x, shift):
    x = np.asarray(x, float)
    return float(np.exp(np.mean(np.log(x + shift))) - shift) if len(x) else float('nan')


def rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


inst = pd.read_csv(os.path.join(RES, 'instances.csv'))
inst = inst[inst.in_scope].set_index('name')
FSTAR = inst.fstar_min.to_dict()
famcap = set(inst.reset_index().sort_values('name').groupby('family').head(3).name)

# ------------------------------------------------------------------ OBBT level
obbt = {(r['name'], r['src']): r for r in jl('obbt.jsonl') if r['status'] == 'ok'}
roots = {(r['name'], r['solver']): r for r in jl('roots.jsonl')}


def gapclosed(LB, LB0, f):
    g = f - LB0
    if not (math.isfinite(LB0) and g > 1e-6 * max(1, abs(f))):
        return float('nan')
    if LB == math.inf:
        return 1.0
    return float(np.clip((LB - LB0) / g, 0, 1))


rows, rnd = [], []
for (name, src), r in obbt.items():
    f = FSTAR[name]
    T = r['trajs']
    full = T['full']
    LB0 = full['LB0']
    d = dict(name=name, src=src, U=r['U'], eps_rel=(r['U'] - f) / max(1, abs(f)), LB0=LB0, fstar=f,
             build=full['build'], nnl=inst.loc[name, 'nnl'])
    for tag, t in T.items():
        H = t['hist']
        for h in H:
            rnd.append(dict(name=name, src=src, traj=tag, **h, gc=gapclosed(h['LB'], LB0, f)))
    for rule in RULES:
        tag = 'restr' if rule.startswith('ad') else 'full'
        s = T[tag]['snaps'][rule]
        h = T[tag]['hist'][s['round'] - 1]
        d['gc_' + rule] = gapclosed(h['LB'], LB0, f)
        d['S_' + rule] = h['S']
        d['t_' + rule] = s['time']
        d['k_' + rule] = s['round']
    d['nlp_full'] = full['nlp']
    d['nlp_restr_ad08'] = sum(h['nlp'] for h in T['restr']['hist'][:T['restr']['snaps']['ad0.8']['round']])
    d['nlp_full_ad08eq'] = sum(h['nlp'] for h in full['hist'][:T['restr']['snaps']['ad0.8']['round']])
    d['fp_capped'] = full['hist'][-1]['capped']
    d['fp_infeasible'] = full['hist'][-1]['infeasible']
    if 'jacobi' in T:
        J = T['jacobi']
        d.update(j_rounds=len(J['hist']), j_nlp=J['nlp'], j_time=J['total'], j_S=J['hist'][-1]['S'],
                 j_gc=gapclosed(J['hist'][-1]['LB'], LB0, f), g_rounds=len(full['hist']), g_nlp=full['nlp'],
                 g_time=full['total'], g_S=full['hist'][-1]['S'],
                 j_S1=J['hist'][0]['S'], g_S1=full['hist'][0]['S'])
    if 'nofilt1' in T:
        N = T['nofilt1']
        d.update(nf_nlp=N['nlp'], nf_time=N['total'], nf_S=N['hist'][0]['S'],
                 f1_nlp=full['hist'][0]['nlp'] + 2, f1_time=full['snaps']['r1']['time'], f1_S=full['hist'][0]['S'],
                 nf_gc=gapclosed(N['hist'][0]['LB'], LB0, f))
    # contraction regime from the full trajectory (rounds 2.. before the last)
    rhos = [h['rho'] for h in full['hist'] if h['nmoved'] > 0]
    d['rounds_fp'] = len(full['hist'])
    d['rho_med_late'] = float(np.median(rhos[2:10])) if len(rhos) >= 4 else float('nan')
    rows.append(d)
OB = pd.DataFrame(rows)
RD = pd.DataFrame(rnd)
OB.to_csv(os.path.join(RES, 'obbt_summary.csv'), index=False)
RD.to_csv(os.path.join(RES, 'obbt_rounds.csv'), index=False)

# ------------------------------------------------------------------ final solves
FIN = {r['key']: r for r in jl('final.jsonl')}


def box_hash(tag):
    f = np.load(os.path.join(RES, 'boxes', tag + '.npz'))
    return hashlib.md5(f['lb'].tobytes() + f['ub'].tobytes()).hexdigest()


def outcome(name, solver, arm, seed):
    """Total time, solved flag, nodes, primal, dual, root dual (min form) for one arm and seed."""
    f = FSTAR[name]
    if arm in ('base', 'obbt3'):
        r = FIN.get('%s/%s/%s/%d' % (name, solver, arm, seed))
        if r is None or r['status'] == 'error':
            return None
        return dict(total=min(r['time'], BUDGET), solved=r['status'] == 'optimal' and r['time'] <= BUDGET,
                    nodes=r['nodes'], primal=r['primal'], dual=r['dual'], root_dual=r['root_dual'],
                    t_pre=0.0, status=r['status'])
    kind, rule = arm.split('-', 1)
    if kind == 'pipe':
        rt = roots.get((name, solver))
        if rt is None:
            return None
        if rt['status'] == 'optimal':
            return dict(total=rt['time'], solved=True, nodes=rt['nodes'], primal=rt['primal'], dual=rt['dual'],
                        root_dual=rt['root_dual'], t_pre=rt['time'], status='root-solved')
        if rule == 'none':
            r = FIN.get('%s/%s/pipe-none/%d' % (name, solver, seed))
            t_obbt = 0.0
            U = rt['primal'] + 1e-6 * max(1, abs(rt['primal'])) if rt.get('primal') is not None else math.inf
            o = dict(U=U)
        else:
            o = obbt.get((name, solver))
            if o is None:
                return None
            traj = 'restr' if rule.startswith('ad') else 'full'
            t_obbt = o['trajs'][traj]['snaps'][rule]['time']
            h = box_hash('%s__%s__%s' % (name, solver, rule))
            r = None
            for rr in RULES:
                if box_hash('%s__%s__%s' % (name, solver, rr)) == h:
                    r = FIN.get('%s/%s/pipe-%s/%d' % (name, solver, rr, seed))
                    break
        if r is None:
            return None
        t_pre = rt['time'] + t_obbt
        if r['status'] == 'error':   # solver failure on the tightened box: counts as unsolved
            return dict(total=BUDGET, solved=False, nodes=0, primal=rt['primal'], dual=None, root_dual=None,
                        t_pre=t_pre, status='error')
        U = o['U']
        hasU = math.isfinite(U)
        st = r['status']
        proven = st == 'optimal' or (hasU and st in ('cutoff', 'infeasible'))
        total = t_pre + r['time']
        primal = r['primal']
        if hasU:
            Ui = rt['primal']
            primal = Ui if primal is None else min(primal, Ui)
        dual = r['dual']
        if st in ('cutoff', 'infeasible') and hasU:
            dual = primal
        return dict(total=min(total, BUDGET), solved=proven and total <= BUDGET, nodes=r['nodes'], primal=primal,
                    dual=dual, root_dual=r['root_dual'], t_pre=t_pre, status=st)
    if kind == 'known':
        o = obbt.get((name, 'known'))
        if o is None:
            return None
        t_obbt = o['trajs']['full']['snaps'][rule]['time']
        r = FIN.get('%s/%s/known-%s/%d' % (name, solver, rule, seed))
        if r is None or r['status'] == 'error':
            return None
        total = t_obbt + r['time']
        return dict(total=min(total, BUDGET), solved=r['status'] == 'optimal' and total <= BUDGET,
                    nodes=r['nodes'], primal=r['primal'], dual=r['dual'], root_dual=r['root_dual'],
                    t_pre=t_obbt, status=r['status'])


ARMS = {'grb': ['base', 'obbt3', 'pipe-none'] + ['pipe-' + r for r in RULES] + ['known-fp'],
        'scip': ['base', 'pipe-none'] + ['pipe-' + r for r in RULES] + ['known-fp']}
out = []
for name in inst.index:
    f = FSTAR[name]
    for solver, arms in ARMS.items():
        for arm in arms:
            for seed in (0, 1):
                o = outcome(name, solver, arm, seed)
                if o is None:
                    continue
                P, D = o['primal'], o['dual']
                if P is None:
                    gap = 1.0
                elif D is None:
                    gap = 1.0
                else:
                    gap = min(1.0, max(0.0, (P - D) / max(abs(P), abs(D), 1e-9)))
                o.update(name=name, solver=solver, arm=arm, seed=seed, gap=0.0 if o['solved'] else gap,
                         wrong=bool(o['solved'] and P is not None and P - f > 1e-3 * max(1, abs(f))),
                         better=bool(P is not None and f - P > 1e-4 * max(1, abs(f))))
                out.append(o)
FO = pd.DataFrame(out)
FO.to_csv(os.path.join(RES, 'final_outcomes.csv'), index=False)


def arm_table(FO, solver, names, label, ref='base'):
    sub = FO[(FO.solver == solver) & FO.name.isin(names)]
    base = sub[sub.arm == ref].set_index(['name', 'seed'])
    rows = []
    for arm in ARMS[solver]:
        a = sub[sub.arm == arm].set_index(['name', 'seed'])
        idx = a.index.intersection(base.index)
        if len(idx) == 0:
            continue
        a, b = a.loc[idx], base.loc[idx]
        both = a.solved & b.solved
        # root gap closed relative to base root dual bound
        rg = []
        for (n, s) in idx:
            f = FSTAR[n]
            rb, ra = b.loc[(n, s), 'root_dual'], a.loc[(n, s), 'root_dual']
            if rb is not None and ra is not None and not pd.isna(rb) and not pd.isna(ra) \
                    and f - rb > 1e-6 * max(1, abs(f)):
                rg.append(np.clip((ra - rb) / (f - rb), -1, 1))
        rows.append(dict(set=label, ref=ref, solver=solver, arm=arm, pairs=len(idx),
                         solved=int(a.solved.sum()), solved_base=int(b.solved.sum()),
                         sgm_time=sgm(a.total, 1), sgm_time_base=sgm(b.total, 1),
                         time_ratio=sgm(a.total, 1) / sgm(b.total, 1),
                         both=int(both.sum()),
                         node_ratio=sgm(a.nodes[both], 10) / sgm(b.nodes[both], 10) if both.any() else np.nan,
                         solve_ratio=sgm((a.total - a.t_pre)[both], 1) / sgm((b.total - b.t_pre)[both], 1)
                         if both.any() else np.nan,
                         errors=int((a.status == 'error').sum()),
                         mean_gap=float(a.gap.mean()), mean_gap_base=float(b.gap.mean()),
                         root_gc_mean=float(np.mean(rg)) if rg else np.nan, n_rg=len(rg),
                         wrong=int(a.wrong.sum()), mean_tpre=float(a.t_pre.mean())))
    return pd.DataFrame(rows)


if __name__ == '__main__':
    print('=== OBBT level ===')
    for src in ('known', 'grb', 'scip'):
        s = OB[OB.src == src]
        g = s[s.gc_r1.notna()]
        print('\nsource %s: %d instances, %d with positive relaxation gap' % (src, len(s), len(g)))
        if len(s) == 0:
            continue
        print(' eps_rel median %.2e' % s.eps_rel.median())
        for rule in RULES:
            print('  %-6s gc mean %.3f median %.3f  >=0.5: %3d  full(>=0.999): %3d  time med %.3fs mean %.2fs  rounds med %g'
                  % (rule, g['gc_' + rule].mean(), g['gc_' + rule].median(), (g['gc_' + rule] >= 0.5).sum(),
                     (g['gc_' + rule] >= 0.999).sum(), s['t_' + rule].median(), s['t_' + rule].mean(),
                     s['k_' + rule].median()))
        print('  extra >=10pp after round 1 (fp - r1): %d; ad0.8 - r1 >= 10pp: %d'
              % (((g.gc_fp - g.gc_r1) >= 0.1).sum(), ((g['gc_ad0.8'] - g.gc_r1) >= 0.1).sum()))
    print('\n=== final solves ===')
    allnames = list(inst.index)
    fb = {}
    for n in allnames:
        f = np.load(os.path.join(RES, 'fbbt', n + '.npz'))
        fb[n] = (f['lb'], f['ub'])

    def changed(n, solver):
        p = os.path.join(RES, 'boxes', '%s__%s__fp.npz' % (n, solver))
        if not os.path.exists(p):
            return False
        b = np.load(p)
        return bool((b['lb'] > fb[n][0]).any() or (b['ub'] < fb[n][1]).any())

    tabs = []
    for solver in ('grb', 'scip'):
        base = FO[(FO.solver == solver) & (FO.arm == 'base')]
        hard = set(base[(base.total >= 10) | ~base.solved].name)
        obbt_ran = set(n for n in allnames if (n, solver) in obbt)
        aff = set(n for n in obbt_ran if changed(n, solver))
        sets = (('all', allnames), ('famcap3', [n for n in allnames if n in famcap]),
                ('probe_pool', [n for n in allnames if inst.loc[n, 'in_probe_pool']]),
                ('obbt_ran', sorted(obbt_ran)), ('box_changed', sorted(aff)),
                ('hard', sorted(hard)), ('hard&changed', sorted(hard & aff)))
        for label, names in sets:
            for ref in (('base', 'pipe-none') if label in ('obbt_ran', 'box_changed', 'hard&changed') else ('base',)):
                t = arm_table(FO, solver, names, label, ref)
                t['ninst'] = len(names)
                tabs.append(t)
                print(t.to_string(index=False, float_format='%.3f'))
    pd.concat(tabs).to_csv(os.path.join(RES, 'arm_tables.csv'), index=False)
