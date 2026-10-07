"""Write a slim certificate file: the planning state without the planning data
(SCIP point pool, SCIP evaluations), i.e. cells, leaves, cell slopes and the
rigorous records.  verify_cs.py and crosscheck_cs.py need only these.

usage: python3 export_cert.py state.pkl out.pkl
"""
import pickle
import sys

import cs


def main():
    st = cs.load(sys.argv[1])
    out = cs.State.__new__(cs.State)
    out.__dict__.update(T=st.T, cells=st.cells, leaves=st.leaves, base=st.base, lam=st.lam, recs=st.recs,
                        pts=[[] for _ in range(st.T)], evals={}, scip_inf=set(), log=[])
    with open(sys.argv[2], "wb") as fh:
        pickle.dump(out, fh, protocol=4)


if __name__ == "__main__":
    main()
