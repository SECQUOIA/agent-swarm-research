# Core-only noise: what survives with convex residual fibers

Date: 2026-10-02. Status: scoped exploration, with a reviewed restricted
positive theorem and explicit limits on its closure mechanism. This note
does not claim a general expected exact algorithm with arbitrary fibers.

Let `F(v,z)` be a fixed-degree rational polynomial on a product box, with
`k` core coordinates `v`, convex residual slices in `z`, and core diagonal
upper curvature `L`. Only the core receives independent linear noise.
Write `V(v)=min_z F(v,z)`.

## 1. The search bound survives; full-coordinate closure does not follow

Partial minimization preserves coordinate upper curvature. Certified
approximate residual values therefore give the same corrected-corner
search and expected core-cell count as in
[polynomial box recourse](smoothed-polynomial-box-recourse.md). The count
uses only the independent core coefficients. Residual perturbations were
needed later, to obtain a full-coordinate growth and closure event.

Projected point growth can also be handled without a smooth value formula
or a unique residual optimizer. For a proposed margin `epsilon`, its
semialgebraic condition is

\[
 \exists(a,z_0)\ \forall(v,z):\quad
 F(v,z)+\gamma^Tv\ge F(a,z_0)+\gamma^Ta
                         +\epsilon\|v-a\|^2.                 \tag{1}
\]

All quantified points lie in their original boxes. At `v=a`, the
inequality forces `z_0` to be a minimizing completion; minimizing the
other side over `z` gives precisely growth of the value function. Thus
the two-block finite-noise transfer used in the
[strong-recourse theorem](core-only-noise-strong-recourse.md) still applies.
It controls a unique optimal core, not a unique full point.

Consequently one can localize the optimal core while residual optimal
fibers remain large. A strict excluded-region gap cannot then localize
all conditional optimizers around an arbitrary selected completion: an
equally good completion outside that patch makes the required gap zero.
Changing the closure certificate, rather than only its precision, is
necessary.

## 2. Projected growth alone does not imply a convex value neighborhood

For centered core coordinates `u=v_1-1/2`, `w=v_2-1/2` and `z in [0,1]`,
consider

\[
 F(v,z)=(1+z)u^2+(2-z)w^2.
\]

The residual slice is affine and convex, the core diagonal curvature is
at most four, and

\[
 V(v)=\min\{u^2+2w^2,2u^2+w^2\}
      \ge u^2+w^2.
\]

The unique optimal core has a fixed positive growth margin. Nevertheless,
on `u=t+s,w=t-s`,

\[
 V=3t^2+3s^2-2t|s| \quad(t>0).
\]

At `s=0` the value is `3t^2`, whereas the average at `s=+-t/3` is
`8t^2/3`. These feasible triples approach the optimum as `t` tends to
zero. Thus no neighborhood of that core optimum has a convex value.
This is an implication counterexample, not a positive-probability
obstruction under generic core noise: its unperturbed tie need not persist.

## 3. A full-coordinate patch obstruction does persist under core noise

The [rotating-fiber example](core-only-noise-rotating-fiber.md) uses

\[
 F_\gamma(v,z_1,z_2)=(v-1/2)^2+(z_1-vz_2)^2+\gamma v.
\]

For every `|gamma|<1`, the projected value has exact growth one, while
the optimal fiber is `z_1=a_gamma z_2`. The residual Hessian is PSD, but
the full Hessian is indefinite off the residual zero set `z_1=vz_2`.
No full-dimensional jointly convex patch exists around any optimizer.
This persists on an open interval of noise and even with uniform
quadratic growth to the entire optimal set.

The same note gives a strictly convex residual variant with a unique
interior completion on every slice:

\[
 (v-1/2)^2+(z_1-1/2-v(z_2-1/2))^2+(z_2-1/2)^4+\gamma v.
\]

Its full Hessian is still indefinite arbitrarily near the unique
optimizer. Thus uniqueness, qualitative interiority, and strict residual
convexity do not replace a uniform positive residual Hessian modulus.
Both examples have elementary sum-of-squares global certificates and
constant selectors. They obstruct this patch mechanism, not exact
implicit output in general.

## 4. A different certificate can preserve one completion per core

Suppose a rational retained core box `D` is already known to contain all
optimal cores. A supplied feasible selector `s(v)` can certify the exact
value on `D` through residual convexity and the box KKT conditions:
stationarity, nonnegative bound multipliers, and complementary slackness,
uniformly for `v in D`. These are sufficient conditions even if the
conditional optimal fiber is nonunique.

If the resulting value `q(v)=F(v,s(v))` has a verified strong-convexity
certificate on `D`, its unique minimizer gives an exact implicit global
optimizer of the original problem after applying `s`. This certificate
preserves one minimizing completion for every core; it need not contain
all residual optima in a small product box. The constant selectors in
Section 3 satisfy this interface directly.

This is a verification interface, not an efficient discovery theorem.
The [affine-fiber certificate](affine-convex-fiber-certificate.md) develops
a related supplied representation. In particular, a supplied bounded-degree
polynomial selector already permits deterministic algebraic optimization
in the fixed-dimensional core; it is not by itself a new smoothing result.
Selector representation size, uniform feasibility and KKT verification,
value curvature, and precision-efficient evaluation must all be charged.
An explicit polynomial selector with verified polynomial identities and
inequality certificates is one possible format. Merely saying that a
selector is semialgebraic gives none of these quantitative guarantees.

## 5. A completed restricted route and the next open step

The [reviewed strong-recourse theorem](core-only-noise-strong-recourse.md)
does not require an explicit selector. It assumes verified uniform
residual strong convexity and qualitative interiority of every conditional
optimizer. Sensitivity lifts projected growth to full point growth, and
the original free Hessian is then positive definite at the optimizer.
Only core active-gradient events need randomization. No numerical
residual boundary-distance parameter is required.

The separate [boundary-recourse theorem](core-only-noise-boundary-recourse.md)
removes the interiority assumption under the same uniform residual
modulus. Its [small-multiplier lemma](small-residual-multiplier-curvature.md)
allows small active multipliers to remain free on a stable branch;
large ones can be fixed. The
[active-stratum tube estimate](core-noise-active-stratum-tube.md) supplies
a quantitative branch-radius event, including original core faces and
finite-law atoms. These ingredients replace the residual active-gradient
tails used with full ambient noise. The local multiplier lemma alone
would not establish the probability or algorithmic conclusion.

Arbitrary convex fibers remain beyond that route. A useful next mechanism
would discover a compact value or selector certificate without assuming
a nonsingular residual Hessian. Neither generic differentiability nor
projected growth establishes such a mechanism.

## Verification

The value-function counterexample and midpoint inequality were checked
directly. An independent actual-file reading by the author of the
[restricted theorem review](core-only-noise-strong-recourse-independent-review.md)
passed after clarifying that Hessian indefiniteness concerns the residual
zero set, rather than only the optimal fiber. The linked rotating-fiber and restricted-theorem notes contain
their independent reviews and targeted diagnostics. This note adds no
general algorithm or publication-priority claim. No external search,
project-wide checks, CI inspection, or index edits were performed.
