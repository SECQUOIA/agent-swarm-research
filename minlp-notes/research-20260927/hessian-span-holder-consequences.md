# Integer slices, short exact penalties, and accurate polyhedral outer models

Date: 2026-09-27. Status: consequences of the independently reviewed
[qualitative Hölder theorem](hessian-span-holder-geometry.md) and the
[quantitative constant argument](hessian-span-holder-height-review.md).
The latter passed a [separate adversarial review](hessian-span-holder-height-adversary.md).
Its [direct number-field refinement](algebraic-coefficient-span-precision.md)
and [independent review](algebraic-coefficient-span-review.md) sharpen the
constant bound to \(\log C\le N^{O(h+1)}\); the current precision and
penalty sizes below use that refinement.
A [separate review of the consequences](hessian-span-holder-consequences-review.md),
with a further independent check of the outer-model argument, found no
substantive gap. All statements retain the qualified novelty status of
the underlying package.

## Uniform error bounds across bounded integer slices

Let \(w=(z,x)\) range over a rational box \(B\), with
\(z\in\mathbb Z^k\). Impose rational affine equalities and inequalities
and rational total-degree-two rows \(q_i(z,x)\le0\). Assume that every
continuous Hessian \(\nabla_{xx}^2q_i\) is positive semidefinite. The
full Hessian in \((z,x)\) may be indefinite. Set
\[
 h=\dim\operatorname{span}\{\nabla_{xx}^2q_i\},
\]
and let \(N\ge2\) be the total explicit binary input length. Write
\(F\ne\varnothing\) for the mixed-integer feasible set. Let \(V\)
be the maximum of zero, all quadratic and affine inequality violations,
and both signs of each affine equality violation.

There is a uniform constant \(C\ge1\) such that
\[
 \operatorname{dist}(w,F)\le C V(w)^{2^{-h}}
 \quad(w\in B,\ z\in\mathbb Z^k),\qquad
 \log_2 C\le N^{O(h+1)}.                             \tag{1}
\]
The integer dimension need not be fixed for this encoding assertion.
There is no Slater assumption on any slice.

To prove (1), fixing a bounded integer vector substitutes integers with
polynomially many bits, so every resulting slice has input length
polynomial in \(N\). If that slice is feasible, the quantitative
continuous theorem gives (1), with a feasible repair in the same integer
slice. Its constant has a bound uniform over all such substitutions.
If the slice is infeasible, minimizing \(V(z,\cdot)\) over its continuous
box is a convex quadratic epigraph program with the same Hessian span.
The [value-separation theorem](hessian-span-reduction.md) gives a uniform
positive lower bound
\[
 \min_x V(z,x)\ge\Delta,
 \qquad \Delta=2^{-N^{O(h+1)}}.
\]
For these slices, use distance to any fixed global feasible point, at
most the full box diameter \(D_B\). A constant
\(D_B\max(1,\Delta^{-2^{-h}})\) suffices. Its logarithm fits (1).
Taking the larger of the feasible-slice and infeasible-slice bounds proves
the result without enumerating integer assignments.

## An exact penalty with exactly \(h\) squaring equations

Let \(f\) be \(L_f\)-Lipschitz on the bounded mixed-integer domain,
using Euclidean distance. For every \(\rho>L_fC\),
\[
 \min_{w\in B,\ z\in\mathbb Z^k}
       \bigl[f(w)+\rho V(w)^{2^{-h}}\bigr]             \tag{2}
\]
has exactly the same minimizers in the original variables as minimizing
\(f\) over \(F\). At any infeasible \(w\), an admissible feasible
repair \(w_F\) from (1) gives
\[
 f(w)+\rho V(w)^{2^{-h}}
 \ge f(w_F)+(\rho-L_fC)V(w)^{2^{-h}}>f(w_F).
\]
At a feasible point the penalty is zero. Compactness and continuity
ensure attainment. If \(f\) is a rational quadratic, with arbitrary
Hessian, a Lipschitz bound with polynomial bit length follows from the
input box. A sufficient integer \(\rho\) therefore has bit length
\(N^{O(h+1)}\), including the objective data in \(N\).

The fractional power has an exact quadratic lift. Choose a rational
\(U\ge\max(1,\max_B V)\), with polynomial bit length. Introduce
\(t_0,\ldots,t_h\in[0,U]\), and impose
\[
 t_{j+1}=t_j^2\quad(0\le j<h),\qquad
 t_h\ge r(w)\quad\text{for every signed residual row }r.
                                                               \tag{3}
\]
Nonnegativity supplies the zero term in \(V\). For fixed \(w\), the
minimum possible \(t_0\) is exactly \(V(w)^{2^{-h}}\), attained by
\(t_j=V(w)^{2^{j-h}}\). All these values lie in \([0,U]\).
Minimizing \(f(w)+\rho t_0\) subject to (3) is therefore exactly (2).
For \(h=0\), the squaring chain is empty and this is the ordinary
linear epigraph of the maximum residual.

This lift uses \(h\) squaring equalities and \(h+1\) continuous
variables. It is nonconvex. The theorem gives an encoding bound and
minimizer-set exactness, not an improvement in the difficulty of solving
the penalized problem. The exponent cannot be increased uniformly as a
function of \(h\), by the classical power-chain example in the
qualitative note.

## Polyhedral outer models with a distance guarantee in every integer slice

For this part impose the stronger assumption that every full quadratic
Hessian in \((z,x)\) is positive semidefinite. This is needed for the
polyhedral square approximation used in
[the MILP projection theorem](mixed-integer-span-frontier.md), rather
than for (1). Keep all affine constraints and box bounds exactly.

That construction replaces each quadratic by a continuous polyhedral
lift of a lower approximation \(\underline q_i\) satisfying
\[
 q_i-\varepsilon\le\underline q_i\le q_i
 \quad\text{throughout }B.
\]
The dyadic square lift has size polynomial in input length and
\(\log(1/\varepsilon)\). No extra integer variables are introduced.
Let \(O_z\) be the continuous projection of its fiber at an integer
assignment \(z\), and let \(F_z\) be the original feasible fiber.

Fix a requested distance tolerance \(\tau=2^{-p}\), \(p\in\mathbb Z_{\ge0}\).
Let \(\overline C=2^{N^{O(h+1)}}\) bound all feasible-slice
constants, and choose
\[
 0<\varepsilon\le
 \min\{\Delta/2,(\tau/\overline C)^{2^h}\}.          \tag{4}
\]
Then
\[
 O_z=\varnothing\quad\Longleftrightarrow\quad F_z=\varnothing,
 \qquad
 F_z\subseteq O_z\subseteq F_z+\tau\mathbb B_2
 \quad\text{for every feasible integer slice}.       \tag{5}
\]
The first statement is the positive violation-gap argument. For the
second, every original feasible point lifts, while every point of
\(O_z\) has true maximum residual at most \(\varepsilon\). Applying
the feasible-slice version of (1) and (4) gives a repair in the same
integer slice at distance at most \(\tau\). Since the fibers are
compact and one contains the other, their Hausdorff distance is at most
\(\tau\).

A dyadic \(\varepsilon\) satisfying (4) needs at most
\[
 N^{O(h+1)}+O(2^h p)
\]
fractional bits after enlarging the universal constants. Thus, for
fixed \(h\), the outer formulation has polynomial size in \(N+p\).
It preserves feasible integer assignments exactly and approximates each
nonempty continuous fiber to any prescribed distance, even when the
original fiber has empty interior or consists entirely of irrational
points.

For an affine objective \(c_z^Tz+c_x^Tx\), let \(v\) be the original
optimum and \(v_O\) the outer MILP optimum. Compactness and (5) give
\[
 v-\|c_x\|_2\tau\le v_O\le v.                       \tag{6}
\]
An outer optimizer's integer assignment admits an exactly feasible
continuous repair within \(\tau\), whose objective is at most
\(v_O+\|c_x\|_2\tau\). This is an existence statement about the
repair, not an assertion that the rational MILP continuous output itself
is feasible. If desired, the canonical-point construction in the
[algebraic-witness theorem](algebraic-witness-recovery.md), applied after
a rational translation by the MILP output, returns the nearest feasible
point in that integer slice as algebraic coordinates. Its native Hessian
span remains \(h\).

## Significance and limits

Fractional exact penalties, quadratic lifts of fractional powers, and
polyhedral approximation of convex quadratic epigraphs are established
ideas. The [later source comparison](hessian-span-holder-original-source-audit.md)
also gives a [conic derivation of the qualitative exponent](hessian-span-holder-hu-li-comparison.md)
from established results and a short Hessian-span argument. That exponent
is therefore a modest structural corollary. The potential addition here
is uniform encoding and precision control through the matrix-span
parameter, including slices without strict feasible points. The
[prior audit](hessian-span-holder-prior.md) and its follow-up record the
remaining source-comparison gaps; neither establishes priority for the
arithmetic bound or these deductions.

These consequences do not establish a practical universal penalty
coefficient, a numerically stable algebraic repair implementation, or a
polynomial-time algorithm with arbitrarily many integer variables.
The estimates are worst-case bounds with large unspecified effective
constants. Their solver relevance is the existence of finite-precision
outer formulations and admissible repairs under a structural hypothesis
that allows many variables, many constraints, and degeneracy.

## Verification

These deductions were independently reviewed, including the infeasible-slice
case, the zero-length squaring chain, residuals larger than one, the
precision-bit count, and nearest-point recovery after translation. The
proof author reread the complete saved review. No numerical experiment or
formal proof assistant is claimed. A targeted inline Python command
checked the eight files in this Hölder package for valid relative links,
paired math delimiters, trailing whitespace, control characters, and final
newlines. These document checks do not verify the mathematics. No
project-wide checks or CI inspection were performed.

After the reviewed arithmetic refinement, the author read its complete
proof and independent review and propagated the stronger constant bound
through (1)–(4) and the precision-bit count. The exponent and all repair
arguments are unchanged. A new targeted inline Python command checked
only this consequences note and the geometry note for the same document
properties, and confirmed that neither retained a superseded quadratic
exponent in its current constant or size claims.
