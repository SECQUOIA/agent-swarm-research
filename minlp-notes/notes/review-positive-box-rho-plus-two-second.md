# Second independent audit of the positive-box bound rho plus two

Date: 2026-09-04. Reviewer: `review_fbbt`.

Final canonical proof read in full:
[Positive-box gap bound: aspect ratio plus two](../results/positive-multilinear-positive-box-sharp.md).
Its finite-step induction, common mixture, and explicit affine transfer agree
with the argument audited below. No mathematical correction is needed. The
displayed lower endpoint uses the separately audited lower result; common-aspect
boxes belong to the broader class in the canonical definition, so that transfer
of the lower bound is valid.

The coefficient induction in
[the proof note](positive-box-rho-plus-two-proof.md) is correct. It establishes
the universal bound `tbtgap <= (rho+2) chgap` for every positive multilinear
polynomial on a positive box with coordinate aspect ratios at most `rho>1`.
In particular, four is a valid bound on `[1,2]^n`; this is not a claim that four
is the optimal constant. Novelty and the separate lower family are outside
this mathematical audit.

## Moment definitions and dimension boundaries

Write `C_j,P_j,O_j` for the expected elementary symmetric polynomial of degree
`j` in a rounded binary vector under common-threshold, independent, and
orientation rounding. Since its value is `binom(K,j)`, these agree with the
definitions in the proof. Define degree-zero moments to be one and negative
or above-dimension moments to be zero. The adjacent-cardinality value `V_j`
uses the same conventions.

The cube slab between the two adjacent integer cardinalities is integral:
two fractional coordinates permit an opposite perturbation, and a sole
fractional coordinate either permits a perturbation or contradicts an active
integer sum. Thus any prescribed marginal vector admits an adjacent-cardinality
law. The piecewise linear interpolation of `binom(k,j)` is convex for `j>=2`,
so this law minimizes the corresponding moment. The same argument applies
to `rho^k` for `rho>1`.

For

\[
F_{n,j}=2C_j+V_j-P_j-2O_j+C_{j-1}-P_{j-1},
\]

the degree-zero and degree-one expressions vanish. At `j=n+1` the expression
is exactly `C_n-P_n>=0`, and all higher orders vanish. These cases are
essential because multiplication by `rho=1+t` adds a degree to the physical
polynomial expression.

For degree two, orientation rounding gives each pair's upper and lower
Fréchet intersection probabilities with equal weights. Therefore
`2O_2=C_2+L_2`, where `L_2` is the sum of all pairwise lower bounds. The
identity `F_{n,2}=(C_2-P_2)+(V_2-L_2)` proves the base order: both terms are
nonnegative. The second inequality follows by applying all pairwise lower
bounds to the feasible adjacent-cardinality law. This does not require all
pairwise lower bounds to be simultaneously attained.

## An independent finite-increment proof of the spreading step

This verification avoids any assumption that coordinate partial derivatives
exist along a chosen path. Suppose `3<=j<=n` and all marginals are interior.
Choose distinct coordinates with global minimum `x` and maximum `y`, and
replace them by `x-h,y+h`, with `0<h<=min(x,1-y)`. All other coordinates remain
between them. Put

\[
B=\binom{n-1}{j-1},\qquad D=\binom{n-1}{j-2}.
\]

The sorted-minimum formula for common-threshold moments gives changes
`Delta C_j=-Bh` and `Delta C_{j-1}=-Dh`, including initial ties. The maximum
has zero coefficient in these two moments. The sum of marginals is unchanged,
so `Delta V_j=0`.

Let `E_r` denote the elementary symmetric polynomial in the other `n-2`
marginals. Direct expansion in the chosen two coordinates gives

\[
\Delta(P_j+P_{j-1})
=-h(y-x+h)(E_{j-2}+E_{j-3})\ge-Dh.
\]

Indeed, `0<=y-x+h<=1`, and the two elementary symmetric polynomials are
bounded above by their binomial counts, whose sum is `D`.

Using the same uniform variable and orientation coins, increasing a single
marginal is monotone and changes that binary coordinate on a set of
probability exactly its increment. On that set, the change in `binom(K,j)`
is between zero and `B`. Decreasing the minimum therefore lowers `O_j` by
at most `Bh`; increasing the maximum cannot lower it further. Thus
`Delta O_j>=-Bh`. Combining the four estimates gives

\[
\Delta F_{n,j}\le-2Bh-Dh+Dh+2Bh=0.
\]

Taking `h=min(x,1-y)` reaches a boundary in one step. This proof depends on
choosing the global extrema; it does not assert Schur concavity or monotonicity
under arbitrary pairwise spreading.

## Boundary induction

A zero coordinate is deterministic under every law and can be deleted.
A one coordinate gives Pascal's identity for `C,P,O`. It gives the same
identity for `V`: shifting the sum by one shifts both adjacent cardinalities
by one with the same interpolation weights. Consequently

\[
F_{n,j}(u,0)=F_{n-1,j}(u),\qquad
F_{n,j}(u,1)=F_{n-1,j}(u)+F_{n-1,j-1}(u).
\]

Both formulas respect degree-zero and above-dimension conventions, including
`j=n+1`. Dimension one is immediate. An existing boundary coordinate is
reduced first; otherwise the spread reaches one. Since spreading cannot
increase `F`, its original value is at least the nonnegative boundary value.
The direction of the induction inequality is correct.

## Physical products and arbitrary positive boxes

For `t=rho-1>0`, expand a binary physical product as `(1+t)^K`. Its four
values `C,P,O,V` have coefficients `C_j,P_j,O_j,V_j`, respectively. Thus the
coefficient of `t^j` in

\[
(\rho+1)C+V-\rho P-2O
\]

is exactly `F_{n,j}`. Coefficient nonnegativity implies
`C-V<=rho(C-P)+2(C-O)`, with no missing top-degree coefficient.

Choose independent rounding with probability `rho/(rho+2)` and orientation
rounding with probability `2/(rho+2)`. This is one law on the entire coordinate
set, independent of individual supports and coefficients. Common-threshold
rounding simultaneously maximizes every positive monomial. Summing the
inequalities therefore bounds the termwise gap by `rho+2` times the deficiency
of this law, which is at most the full graph-hull gap.

For unequal coordinate aspect ratios, each original coordinate is a positive
affine function of a physical coordinate in `[1,rho]`. Each original monomial
expands into monomials with nonnegative coefficients. Its exact hull gap is
at most the sum of the expanded monomial gaps, and the full polynomial's hull
gap is unchanged by the affine bijection. The transfer is consequently valid.
Fixed coordinates are first absorbed into coefficients. Constant and affine
terms, endpoint marginals, and zero gaps require no divisions or exceptions.
