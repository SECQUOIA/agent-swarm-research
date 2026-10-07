# Adversarial review of the tree-localization counterexample

Date: 2026-10-02. Verdict: **the stated counterexample is proved; no
substantive gap found.**

I reviewed [counterexample.md](../tree-localization/counterexample.md)
against the exact property `(Loc_T)` in Remark 3.3 and Conjecture 7 of
[adaptive-matching.md](../../research-20260929/theory-decomposition/adaptive-matching.md),
and against Definition 1.2 and Lemmas 1.5 and 3.2 of
[decomposition-certificates.md](../../research-20260929/theory-decomposition/decomposition-certificates.md).
The review includes the actual finite certificate construction, rather
than assuming that an objective perturbation can be realized by a
certificate. No revision is required for mathematical correctness.

The conclusion is precisely the failure of unrestricted `(Loc_T)` with
size-independent constants for bounded branching and fixed conditioning.
Conjecture 7 permits an additional relation between branching and
conditioning, so the counterexample does not refute every version of that
conjecture. The note already states this distinction. It also correctly
avoids claims about partitions reached by GR, certificate-size lower
bounds, or the nonexistence of another adaptive algorithm.

## Quantifiers and admissibility

The construction fixes `k=3`, `w=1`, `Delta=2`, `M_a=3`,
`alpha' A=1/2`, and a strictly positive common `c_g`. Varying depth does
not vary any parameter on which `(Loc_T)` permits its constants to depend.
It is legitimate to use a common quadratic-growth lower bound rather
than the largest possible constant for each finite instance.

All bag gradients vanish at the true minimizer. Consequently the exact
subtree slopes of Lemma 3.2 are zero, and the certificate slopes satisfy
every proposed slope-error bound in `(Loc_T)`, including its dependence
on the proposed localization radius. The entire partition satisfies
`(W_theta)` at `theta=0`; the argument therefore does not depend on how
small a positive `theta_T` is chosen.

The consistent point used in the proof is exactly the prescribed
`x_i=z_i^{top(i)}` rule. Every graph variable first appears in its own
original bag; each dummy variable first appears in its final bag. The
root coordinate of the consistent point is thus the root bag copy.
The conclusion holds for **every** minimizing configuration, so no
selection or tie-breaking rule can avoid the violation.

The decomposition has running intersection and the claimed parameters.
The extra dummy coordinate makes each final bag admissible under the
rule that no bag may be contained in its parent. Its positive quadratic
term preserves the common growth constant and has no relaxation error.

## Factorization and auxiliary minimization

The edge inequality gives `||A_d||_2 <= 2 sqrt(2)`. Thus
`H >= delta_0 I` with the stated strictly positive `delta_0`, uniformly in
depth. Expanding the convex squares gives `H + diag(1_L)` exactly;
subtracting the final unary squares gives the desired `H`. The pivot
interval and all bag Hessian bounds are valid. The final bag function has
Hessian `diag(-1,1)`, which is allowed by `(L^{1,1})`.

The only inexact relaxation is a legitimate per-factor convex envelope:
the chord of `-z^2/2` is affine and has gap
`(z-l)(u-z)/2`. This supplies `(U^q)` with the claimed constants on every
box, not merely the boxes selected for this construction. The remaining
convex factors may be kept exact under the model.

The Schur complement has nonpositive off-diagonal entries and constant
row sums. One useful independent expression for the row sum is

```
q_d = 1 - (a/r_plus) (1-gamma^d)/(1-gamma^(d+1)).
```

It simplifies to the displayed formula in the note. The decomposition
into scalar terms plus
`(1/2) sum_{i<j} (-S_ij)(z_i-z_j)^2` has the correct coefficient.
The scalar gap identity outside `[0,W]` is exact, and the inside identity
is exact as well. These identities prove a unique unrestricted global
minimum, despite the fact that the auxiliary objective need not be
convex across the endpoints of the interval.

The harmonic profile satisfies the root equation, every interior
equation, and the fixed leaf value. Since `a>1/3` implies `r_plus<1`, its
root-to-width ratio diverges. Taking a sufficiently small dyadic `W`
places all coordinates strictly inside the original domain without
changing this ratio. Thus the unrestricted minimization step is valid
for the claimed minimizer on `X0`.

The uniform growth bound is sufficient. With
`u=x_I-Bz`, `v=z-t_d 1`, its proof needs the coefficients
`4/delta_0`, `4(2b0^2+1)/q_d`, and `2` for the interior, leaf, and dummy
terms. The stated `C_Q` dominates all three because
`q_d>=lambda_plus`. No dimension factor is missing here.

An independent delegated algebra audit, performed without reading this
review, also found no error in these claims.

## The finite certificate step

The coarse slab can be produced by refining the full domain to width
`W` and then refining exactly the cubes outside the slab to width `h`.
Both scales are dyadic, so this gives finite dyadic cube partitions with
disjoint interiors. Boundary overlaps are permitted because the boxes
are closed. Choosing `h` arbitrarily small after choosing the depth and
`W` is allowed: `(Loc_T)` imposes neither a certificate-size bound nor a
lower bound on leaf width.

The critical model point is valid. A final leaf of width `W` may meet
many cells of its own separator, each of width `h`. Definition 1.2
expressly permits this. Lemma 1.5 requires the final separator copy to
lie in its chosen cell and that cell to meet the original parent bag's
projection. The parent bag has width `h`. Hence the copied coordinate
and the parent coordinate differ by at most `2h`, regardless of the
width of the final leaf. The same estimate applies to original edge
bags, and no longer copy chain occurs for any variable in this
decomposition.

This estimate remains valid for touching pairs: join the two coordinates
through any point in the nonempty intersection of the cell and the
parent projection. Therefore the proof uses Definition 1.2 as written,
including its closed-box configuration constraints.

For an edge factor, changing only its parent copy changes its value by
at most `6 sqrt(2) h < 12h`. For a final factor, the function `phi_W`
is continuous and 1-Lipschitz, including across `0` and `W`. On a coarse
leaf the chord equals `phi_W`; on a fine leaf outside the slab the
additional gap is at most `h^2/8`. Thus its total discrepancy is at most
`2h+h^2/8`. The root and dummy terms have no copy discrepancy.
Summation gives the stated, deliberately loose, `15 n h` bound uniformly
over all configurations.

The maximal intercepts and prescribed affine child bounds consequently
give an actual finite certificate under Lemma 1.5. Its minimum is
attained: the feasible configurations form a finite union of compact
sets, and the objective on each set is continuous. There is a feasible
consistent configuration at the auxiliary minimizer, with each leaf in
its coarse slab, whose value is exactly the auxiliary minimum.

For any minimizing configuration, these facts give

```
G_W(x(c),y(c)) <= Phi(c)+15nh
                <= G_W(xbar,0)+15nh.
```

The global growth bound therefore places every such root copy within
`sqrt(15 C_Q n h)` of `xbar_0`. First choose the depth so that
`xbar_0/W>2K`, then a dyadic `W` to fit the domain, and finally a positive
dyadic divisor `h` of `W` with `15 C_Q n h<xbar_0^2/4`. This sequence
of choices is finite and proves `z_root>K W` for every minimum.
It closes the perturbation-to-certificate gap without a limiting
certificate, an unproved optimizer-continuity claim, or a generic
perturbation assumption.

## Targeted verification

I ran `PYTHONDONTWRITEBYTECODE=1 python3 -` with an inline exact-rational
check using `fractions.Fraction`. It checked 1,044 admissible sampled
final-bag configurations for `W=1/2`, `h=1/8`, including touching pairs,
at interval endpoints and midpoints. All asserted copy and final-factor
bounds passed. The largest copy drift was exactly `1/4=2h`; the largest
final discrepancy was `7/32`, below `129/512=2h+h^2/8`. The same command
checked 65 exact pivot levels, their stated interval condition and Hessian
bound, and sampled edge-factor discrepancies; all passed. These finite
checks support the analytical uniform bounds above and do not replace
them. No test artifact was written.

The delegated algebra audit separately ran an inline NumPy check for
depths 1–7. It reconstructed the Schur complements, harmonic extensions,
and factorization, with maximum residuals respectively `7.8e-16`,
`2.3e-15`, and `2.3e-16`. This was a floating-point check, not a proof.

I read the author's targeted script but did not rerun it or overwrite its
output. Neither audit enumerated the full finite dynamic program. The
argument does not require such an enumeration. No project-wide
verification, CI inspection, external research, or literature ingestion
was performed.
