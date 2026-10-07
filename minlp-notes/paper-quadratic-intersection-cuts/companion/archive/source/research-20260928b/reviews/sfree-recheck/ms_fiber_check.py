"""Does MS's output for a fixed point-rule member depend on the transformation?  For L0 random and the boost
B(eta') in the plane of the member's two tangency lines (which fixes the member), compare the MS-modified
normal (in v-coordinates) along the fibre.  Instance 9 of point_rule_check.py (seed 0)."""
import sys
sys.dont_write_bytecode = True
import numpy as np
from point_rule_recheck import case2_instance, sylv, rule_sets, Lmat, J
rng = np.random.default_rng(0)
for i in range(10):
    Q, b, c, sbar, P, w = case2_instance(rng)
W, l = sylv(Q, b, c); us = W @ np.append(sbar, 1.0)
r2 = np.random.default_rng(1)
found = 0
for trial in range(200):
    L0 = Lmat(r2.normal() * 1.5, r2.uniform(0, 2 * np.pi))
    up = L0 @ us; lam = up[:2] / np.linalg.norm(up[:2])
    # boost in the plane spanned by (lam, 1), (lam, -1): generator K with K(lam,0) = (0,1), K(0,1) = (lam,0)
    K = np.zeros((3, 3)); K[:2, 2] = lam; K[2, :2] = lam
    dirs = []; members = []
    for eta in np.linspace(-3, 3, 61):
        Bk = np.eye(3) + np.sinh(eta) * K + (np.cosh(eta) - 1) * K @ K
        assert np.allclose(Bk.T @ J @ Bk, J)
        L = Bk @ L0
        Nms, info = rule_sets(L[None], us, l, True)
        Npl, _ = rule_sets(L[None], us, l, False)
        members.append(np.round(Npl[0] / np.linalg.norm(Npl[0], axis=1, keepdims=True), 8))
        mod = [k for k, npr in enumerate(info['nprime']) if np.all(np.isfinite(npr[0]))]
        if mod:
            n = Nms[0][mod[0]]; dirs.append(tuple(np.round(n / np.linalg.norm(n), 6)))
    same_member = all(np.allclose(m, members[0], atol=1e-6) for m in members)
    if dirs and same_member:
        found += 1
        if found <= 5 or len(set(dirs)) > 1:
            print('trial %3d: member fixed along the fibre: %s; MS modified on %d of 61 fibre points; distinct modified normals: %d'
                  % (trial, same_member, len(dirs), len(set(dirs))))
print('fibres with a modified inequality examined:', found)
