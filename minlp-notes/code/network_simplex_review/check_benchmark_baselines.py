"""Independent support-function and feasibility audit of benchmark baselines.

Run: python code/network_simplex_review/check_benchmark_baselines.py
Uses different seeds, nonzero simplex costs, edge cases in observations and
simplex weights, and checks each recovered optimizer in the full EF.
"""
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'network_simplex_benchmarks'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from baselines import block_chain, full_ef, compressed_ef, full_ef_membership, OriginalLP
from network_simplex_compressed import CompressedNetworkSimplex
from network_simplex.separator import Point


def main():
    count = 0
    max_error = 0.
    for seed in range(901, 931):
        rng = np.random.default_rng(seed)
        m = int(rng.integers(1, 12))
        a = block_chain(seed=seed, blocks=int(rng.integers(1, 4)),
                        paths=int(rng.integers(2, 7)), length=int(rng.integers(1, 5)),
                        states=m, observed_states=seed % (m+1))
        # Cover no observations, bridges, all state labels, and repeated paths.
        if seed % 5 == 0:
            a.observations = []
        elif seed % 5 == 1:
            a.observations = [(e,j) for e in range(a.edge_count) for j in range(m)]
        elif seed % 5 == 2:
            a.observations = sorted(set(a.observations + [(e,0) for e in range(a.edge_count)]))
        E = a.edge_count
        general_model = CompressedNetworkSimplex(a.arcs,(-a.balances).tolist(),m,a.observations)
        for mode in range(4):
            y = None
            if mode == 1:
                y = np.zeros(m)  # residual weight one
            elif mode == 2:
                y = np.zeros(m); y[seed % m] = 1.  # residual weight zero
            elif mode == 3:
                y = rng.dirichlet(np.ones(m+1))[:m]
            c = rng.normal(size=E + m + len(a.observations))
            full = full_ef(a,c,y)
            compact = compressed_ef(a,c,y)
            general = general_model.optimize(c,y_fixed=y)
            mc = OriginalLP(a,y).solve(c)
            assert full.success and compact.success and general.success and mc.success
            err = max(abs(full.fun - compact.fun), abs(full.fun - general.fun))
            max_error = max(max_error,err)
            assert err < 1e-7, (seed,mode,full.fun,compact.fun)
            assert mc.fun <= full.fun + 1e-7
            for result in (full,compact,general):
                p = result.original_point
                assert abs(c @ p - result.fun) < 1e-7
                audit = full_ef_membership(a,p[:E],p[E:E+m],p[E+m:])
                assert audit.success, (seed,mode,audit.message)
                # Membership checks exact domain bounds before its numerical LP.
                # A solver may return cap + 4e-16. Snap only such domain errors,
                # leaving all balance/observation equations to the membership LP.
                snapped = p.copy()
                for i,(lo,hi) in enumerate(general_model.bounds[:len(p)]):
                    if lo is not None and snapped[i] < float(lo):
                        assert float(lo)-snapped[i] < 1e-7
                        snapped[i] = float(lo)
                    if hi is not None and snapped[i] > float(hi):
                        assert snapped[i]-float(hi) < 1e-7
                        snapped[i] = float(hi)
                audit2 = general_model.membership(Point(snapped[:E],snapped[E:E+m],dict(zip(a.observations,snapped[E+m:]))))
                assert audit2.success, (seed,mode,audit2.message)
            expected = sum((len(paths)-1)*len({j for e,j in a.observations
                            if any(e == h for path in paths for h,_ in path)})
                           for paths in a.blocks)
            assert compact.model_stats['auxiliary_variables'] == expected
            count += 1
    print({'support_cases':count, 'full_EF_membership_checks':3*count,
           'general_compressed_membership_checks':3*count,
           'maximum_objective_difference':max_error})


if __name__ == '__main__':
    main()
