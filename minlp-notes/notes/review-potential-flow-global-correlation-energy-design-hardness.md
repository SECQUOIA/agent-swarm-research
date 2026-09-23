# Independent review: minimum dissipation and pressure-drop design

Date: 2026-09-05. Reviewer: `benders_property`. Status: PASS.

Reviewed [the full energy-design corollary](potential-flow-global-correlation-energy-design-hardness.md) against the independently reviewed global-correlation total-flow construction. The concave minimization mechanism is classical; this audit verifies its physical objective, exact constants, and complexity scope.

## Bridge correction and physical objective

Replacing each uncertain initial bridge by two series bridges with resistances r_i and 3-r_i is correct. Both remain in [1,2], both carry unit flow, and their total dissipation is identically three. This removes the linear parameter bias that an unpaired bridge would introduce. The original r_i still identifies theta_i uniquely, so the full actual-resistance polytope remains an injective affine image of the cube with bounded integer constraints.

The prefix now has 2n new vertices and edges. The proposed totals `6m+2n` vertices and `8m-1+2n` edges, and cycle rank 2m, follow from the previously checked chain of triangles. Maximum degree three, simplicity, cactus structure, acyclic orientation, and strict positivity of every physical flow are preserved. Only the first and last vertices have nonzero nominations, respectively +1 and -1.

For one triangle, the shared path drop is `2*s*f(s)^2`. Its dissipated power is `2*s*f(s)^3+2*(1-f(s))^3`; equality of the two path drops makes this power equal their common drop times the total through-flow, which is one. This verifies e(s). No factor of 1/3 from the convex energy primitive belongs in the dissipated-power objective.

For the whole network, multiplying the physical edge-drop equations by their signed flows and using conservation gives `sum beta_e*abs(x_e)^3=pi^T*b`. With the prescribed unit source and sink this is exactly their potential difference. Thus this is a specific pairwise pressure-drop objective, not merely a weighted potential surrogate.

## Concavity and exact cut identity

Both displayed derivatives of e are correct, with strict negative second derivative for s>0. The paired function is therefore concave and even in delta. The exact binary values are `A_E=24-16*sqrt(2)` and `B_E=13/2-3*sqrt(3)`. Substitution of the strict rational square bounds gives

    kappa_E > 35/2-16*(283/200)+3*(173/100) = 1/20 > 1/32.

Every initial bridge pair contributes three, every joining bridge contributes two, and there are 2m-1 joining bridges. Hence the constant bridge contribution is `3n+4m-2`, and the full constant C_E is correct. A concave function on a cube has a vertex minimizer by the convex-combination inequality, so

    OPT=C_E-kappa_E*MaxCut(H)

holds exactly. The signs correctly favor larger cuts in this minimization problem.

## Thresholds, encoding, and certificates

Rewrite the half-cut reference value as

    3n+4m-2+(m-K+1/2)*A_E+(K-1/2)*B_E.

The two radical coefficients are nonnegative and O(m). Square-root errors at most w induce errors at most 16w in A_E and 3w in B_E, so the reference error is at most 16mw. The proposed `w=1/[65536*(m+1)]` therefore gives error below 1/4096, more than sufficient for the claimed 1/512 threshold accuracy. A dyadic denominator obtained by rounding up the precision is at most `131072*(m+1)`; including the fixed half factors preserves O(m) denominator size and polynomial numerator magnitude. All reduction data consequently have polynomial unary encoding length.

The cut gap contributes more than 1/64 on either side of the half-cut reference. Deducting threshold error 1/512 leaves the strict 7/512 margin. A yes instance has minimum below tau-7/512, and a no instance has minimum above tau+7/512. This establishes the stated weak upper-threshold reduction and strong hardness without equality ambiguity or numerical scaling.

On this explicit family a binary minimizing parameter is an n-bit certificate. Its value lies in the fixed field Q(sqrt(2),sqrt(3)), and exact comparison with a rational threshold is polynomial. Hence the restricted weak-threshold feasibility claim is NP-complete. This does not assert membership for arbitrary correlated energy-design families.

## Approximation and rational scenario output

Absolute value error 1/256 is below the separation margin. A rational scenario with objective at most OPT+1/256 lies below tau-5/512 in a yes instance, while every no-instance scenario lies above tau+7/512. Approximation of that returned scenario's energy to error 1/512 therefore decides the source.

This evaluation requires only separate quadratic flow-root enclosures and rational arithmetic. For example, on a triangle with s in [1,3] and flow f in [0,1], the power polynomial `2*s*f^3+2*(1-f)^3` has derivative magnitude at most 24. Enclosing each of the 2m triangle flows to an inverse-polynomial absolute width therefore controls the total power error, while all bridge powers are exact rational numbers. Polynomial-time rational output has polynomial encoding length, so no hidden exact radical-sum comparison is needed.

The note correctly makes no fixed relative-error or normalized-objective claim.

## Independent checks

I independently verified five symbolic identities: triangle dissipation equals e(s), both derivatives, and both binary cut constants. Exact rational arithmetic also verified the strict kappa_E lower bound. The graph modification is a subdivision-length change to the separately tested chain construction; the new counts were checked directly above. All checks passed.

No correction was required.
