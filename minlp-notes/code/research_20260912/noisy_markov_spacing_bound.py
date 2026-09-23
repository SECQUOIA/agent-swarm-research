"""Exact finite-horizon error majorant for observations with a minimum gap.

This extends the stationary scalar noisy-Markov window bound. It prices a
nonnegative residual-pair majorant over separated calendar distances; it does
not optimize the observation design or certify a floating-point solve.
"""

from fractions import Fraction as Q
from math import comb

from certify_noisy_markov import full_grid_variance_floor, rational


def spacing_bound(n, L, gap, rho, latent, nugget, *, refined_pairs=False):
    """Return an exact uniform bound on ||C_L(S)-I|| for gap-separated S."""
    if not isinstance(refined_pairs, bool):
        raise TypeError("refined_pairs must be a boolean")
    if any(isinstance(x, bool) or not isinstance(x, int) for x in (n, L, gap)):
        raise TypeError("Integer horizon, window and minimum gap required")
    if n < 1 or L < 0 or gap < 1:
        raise ValueError("Require n>=1, L>=0 and gap>=1")
    rho, latent, nugget = map(rational, (rho, latent, nugget))
    if abs(rho) >= 1 or latent < 0 or nugget <= 0:
        raise ValueError("Invalid stationary scalar covariance")
    a = abs(rho)
    L = min(L, n-1)
    # At most floor(L/gap) previous observations enter a local conditional.
    m = L//gap
    floor = (latent+nugget if m == 0 else
             full_grid_variance_floor(m+1, a**gap, latent, nugget))
    if not a or not latent or L >= n-1 or gap >= n:
        return {"delta": Q(0), "innovation_floor": floor,
                "row_majorant": Q(0), "worst_anchor": 0}
    gain = latent/(latent+nugget)
    far_coefficient = latent*(1+gain*sum(
        (a**(2*gap*j) for j in range(1, L//gap+1)), Q(0)))
    near_coefficient = latent*gain
    if refined_pairs:
        # Exact fresh-filter propagation removes the far regression factor.
        # Constant latent/nugget variances give a first gain of P/(P+r).
        far_coefficient = latent
        near_coefficient *= 1-gain
    phi = [Q(0)]*n
    for h in range(gap, n):
        if h > L:
            phi[h] = far_coefficient*a**h
        else:
            first = max(gap, L+1-h)
            phi[h] = near_coefficient*a**h*sum(
                (a**(2*d) for d in range(first, L+1, gap)), Q(0))
    best = [Q(0)]*n
    for h in range(gap, n):
        best[h] = max(best[h-1], phi[h]+best[h-gap])
    anchor = max(range(n), key=lambda t: best[t]+best[n-1-t])
    row = best[anchor]+best[n-1-anchor]
    return {"delta": row/floor, "innovation_floor": floor,
            "row_majorant": row, "worst_anchor": anchor}


def spacing_mask_count(L, gap):
    """Number of L-bit strings whose set bits are at least gap apart."""
    if (any(isinstance(x, bool) or not isinstance(x, int) for x in (L, gap))
            or L < 0 or gap < 1):
        raise ValueError("Require an integer L>=0 and integer gap>=1")
    return 1+sum(comb(L-(gap-1)*(q-1), q)
                 for q in range(1, (L+gap-1)//gap+1))
