"""Invariant D, Theorem-A bound and rho_par for the adversarial instances of the sfree note
(Section 8.6; logs adversarial_ratio_7.log and adversarial_ratio_8_margin.log), next to the z_A values
recorded there.  Also recomputes z_A with the normalized-frame SDP bisection."""
import json
import os
import numpy as np
import warnings
import rb
from adversarial_ratio import build

warnings.filterwarnings('ignore')
LOG = os.path.join(rb.SFREE, '..', 'logs')
for fn in ('adversarial_ratio_7.log', 'adversarial_ratio_8_margin.log'):
    for line in open(os.path.join(LOG, fn)):
        if not line.startswith('{'):
            continue
        r = json.loads(line)
        sbar, P = build(np.array(r['theta']))
        c = np.ones(3)
        z, lam = rb.zK(sbar, P, c)
        Pt = rb.scaled_rays(P, c, z)
        D = rb.D_inv(sbar, Pt)
        rp, _ = rb.rho_par(sbar, Pt)
        cert, hi, _ = rb.zA_ratio(sbar, Pt, iters=35)
        print('%s restart %d: recorded z_A %.4f | zK %.6f  D %.4g  delta=1/D^2 %.3g  bound(D) %.4g  rho_par %.4g  '
              'z_A (normalized SDP) %.4f / %.4f  cond(P~) %.1f' % (fn, r['restart'], r['final'], z, D, 1 / D ** 2,
                                                                rb.theoremA_bound(D), rp, cert, hi, np.linalg.cond(Pt)), flush=True)
