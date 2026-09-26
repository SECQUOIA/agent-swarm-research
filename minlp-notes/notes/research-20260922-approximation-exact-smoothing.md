# Additive approximation and exact smoothed optimization with deterministic offsets

Date: 2026-09-22. Status: complete proofs below; a fresh
[independent review](review-20260922-approximation-exact-oracle.md) found no
substantive gap. This note is a priority check and a broader one-optimizer result, not
a claim that approximation-to-exact smoothed conversion is new.

## Main conclusion and significance

An additive approximation scheme that remains available after fixing arbitrary
binary coordinates can be converted to an exact algorithm with polynomial
expected smoothed running time for

\[
\min_{z\in Z}\{g(z)+\xi^Tz\},\qquad Z\subseteq\{0,1\}^n,
\]

where `Z` is nonempty, even when the deterministic offset `g` is nonlinear
and nonintegral. If the root oracle instead reports an empty feasible set,
the algorithm returns infeasibility immediately. The
conversion needs polynomial-time exact evaluation of a returned support and
an approximation runtime polynomial in inverse additive accuracy. Its
mechanism is the classical higher-winner-gap method, with an elementary
offset extension and a certified partition procedure.

Applied to positive-definite indicator quadratic optimization with polynomial
spectral and coefficient bounds, ordinary finite-domain dynamic programming
supplies the approximation oracle on every fixed-treewidth graph. Thus exact
smoothed optimization of **one perturbed
instance** does not require bounded biconnected block size. The
[exact-message result](../results/smoothed-indicator-block-dp.md) retains a
different conclusion: it constructs complete continuous messages. That
distinction should carry the novelty assessment rather than an assertion
that deterministic nonlinear support costs defeat the established smoothed
methods.

Finite-grid noise also permits an exact expected-polynomial Turing algorithm:
stop the precision loop at a finite threshold and use exhaustive enumeration
on the sufficiently rare remaining cases. This handles exact ties without
pretending discrete noise has a density.

## 1. Higher gaps with arbitrary deterministic offsets

Let independent real random variables `xi_i` have densities bounded by `phi`.
No common bounded support is needed in this section. Put

\[
F_\xi(z)=g(z)+\xi^Tz,\quad v_\xi=\min_{z\in Z}F_\xi(z),\quad
A_\epsilon=\{z:F_\xi(z)\le v_\xi+\epsilon\}.
\]

For a positive integer `r<=n`, set `k_r=2^(r-1)+1`. Then

\[
\Pr\{|A_\epsilon|\ge k_r\}
\le \binom nr\,2^{r(r+1)}(2\phi\epsilon)^r.                 \tag{1}
\]

Constants here are deliberately loose. For fixed `r` they are harmless.

**Proof.** An affine subspace of dimension `d` has an injective projection
onto some `d` coordinate positions. Its intersection with the binary cube
therefore has at most `2^d` points. Consequently `k_r` distinct binary
vectors have affine dimension at least `r`. Choose `r+1` affinely independent
members of `A_epsilon`, and select `r` coordinates `I` on which their
differences have rank `r`. Write their distinct patterns as
`y_0,...,y_r` in `{0,1}^r`.

Fix the coordinates of the noise outside `I`. For every nonempty pattern
class define

\[
a_y=\min_{z\in Z:z_I=y}\left(g(z)+\sum_{j\notin I}\xi_jz_j\right).
\]

Its minimum full cost is `a_y+xi_I^T y`. Each of the selected classes contains
a member of `A_epsilon`; its class minimum consequently belongs to
`[v_xi,v_xi+epsilon]`. Hence, for `j=1,...,r`,

\[
(y_j-y_0)^T\xi_I+(a_{y_j}-a_{y_0})\in[-\epsilon,\epsilon].  \tag{2}
\]

The matrix with rows `y_j-y_0` is a nonsingular integer matrix, so its
determinant has absolute value at least one. The inverse image of the box in
(2) has volume at most `(2 epsilon)^r`. Independence bounds its probability
by `(2 phi epsilon)^r`. This bound holds after any fixing of the other
coordinates. A union over `I` and ordered pattern lists proves (1). Empty
classes need not be considered. The offset `g` enters only the fixed numbers
`a_y`, so neither linearity nor integrality is used. ∎

The same proof works for any deterministic finite `Z`, including fixed-bit
restrictions. The probability bound is used only for the full original
problem; adaptive restrictions in the algorithm do not require independent
conditional noise distributions.

## 2. A certified procedure using an additive oracle

Assume a deterministic oracle is available for every partial binary
assignment `p`. It either certifies that the restricted feasible set `Z_p`
is empty or returns a member `z_p` satisfying

\[
\min_{z\in Z_p}F_\xi(z)\le F_\xi(z_p)
\le \min_{z\in Z_p}F_\xi(z)+\epsilon.                       \tag{3}
\]

Assume exact evaluation of `F_xi(z_p)` is available. An approximate
continuous feasible solution suffices if exact minimization conditional on
its binary support is efficient: replacing its value by the conditional
minimum preserves (3).

For a fixed accuracy `epsilon`, maintain disjoint partial-assignment cells
covering all supports not yet extracted. Each nonempty cell has its cached
candidate `z_p`, exact value `V_p`, and lower bound `L_p=V_p-epsilon`.
Maintain the smallest exact value `U` of every candidate computed so far,
including candidates not yet extracted.

Start with the unrestricted cell. If no cells remain, or every cell has
`L_p>=U`, the candidate attaining `U` is exactly optimal. Otherwise select a
cell of minimum lower bound and extract its candidate `z`. Partition that
cell minus `{z}` into at most `n` new partial-assignment cells: in the ordered
list of previously unfixed coordinates, the first coordinate differing from
`z` determines the cell, earlier coordinates agree with `z`, and later ones
are unrestricted. Query the oracle for each child and continue.

This is the standard first-difference partition used in ranked-solution
enumeration. No claim of novelty is attached to the partition itself.

**Certificate lemma.** If this procedure extracts `k` supports before an
optimality certificate is obtained, those supports are distinct and all
belong to `A_epsilon`. It uses at most `1+kn` oracle calls.

**Proof.** The disjoint partition excludes each extracted support forever.
If some optimal support has not yet been extracted, the cell containing it
has lower bound at most `v_xi`. If an optimal support was already extracted,
then `U=v_xi`; failure of the stopping condition ensures the selected lower
bound is less than `v_xi`. In either case a selected cell has `L_p<=v_xi`.
Its candidate has exact value `V_p=L_p+epsilon<=v_xi+epsilon`. Empty cells
are discarded. The count follows from at most `n` children per extraction. ∎

At accuracy `epsilon`, stop after `k_r` extractions if no certificate was
found. The probability of this failure is bounded by (1), even though the
procedure adaptively chooses its restrictions.

## 3. Expected time from successively finer accuracy

Suppose all restricted oracle calls cost at most

\[
P(N)\,(1+\epsilon^{-a}),\qquad 0<\epsilon\le1,               \tag{4}
\]

for an input parameter `N`, a fixed exponent `a`, and a polynomial `P`.
Polynomial dependence on `log(1/epsilon)` can be absorbed by slightly
increasing `a`. Exact support evaluation is polynomial in `N`. This section
is an arithmetic statement when the noise has arbitrary real values;
Section 5 gives a genuine rational Turing version.

Choose a fixed integer `r>a` and use `k_r` extractions per stage. Run the
procedure afresh with `epsilon_j=2^-j`, `j=0,1,...`, until it certifies an
optimum. The initial stage costs polynomial time. Reaching stage `j>=1`
requires failure at stage `j-1`, whose probability is at most

\[
\binom nr2^{r(r+1)}(2\phi\,2^{-(j-1)})^r.
\]

Thus the expected total cost is bounded by a polynomial in `N,n,phi` times

\[
1+\sum_{j\ge1}2^{aj}2^{-r(j-1)}<\infty.                    \tag{5}
\]

The procedure terminates almost surely and returns an exact optimizer.
This is an expected-time conclusion, not merely a polynomial high-probability
bound. When `n<r`, direct enumeration costs at most `2^(r-1)`, a constant
depending on the fixed exponent, and avoids using (1) outside its range.

## 4. Application to fixed-treewidth indicator quadratic programs

Consider

\[
\min\left\{x^TQx+c^Tx+(\lambda+\xi)^Tz:
 x_i(1-z_i)=0,\ z\in\{0,1\}^n\right\}.                     \tag{6}
\]

Assume rational input, symmetric `Q`,

\[
0<d\le Q_{ii}\le D,\qquad
\sum_{j\ne i}|Q_{ij}|\le\rho Q_{ii},\qquad 0\le\rho<1,
\qquad |c_i|\le C.
\]

A tree decomposition of the graph with edges `ij` where `Q_ij !=0` is
supplied, with width at most the fixed constant `w` and polynomially many
bags. Put

\[
M=\frac{C}{2d(1-\rho)},\qquad H=D(1+\rho).
\]

If `C=0`, the continuous conditional optimum is `x=0` and all indicators
can be optimized directly; assume `C>0` below. Strict diagonal dominance
implies `Q` and all principal submatrices are positive definite. The
maximum-coordinate argument gives `|x_i|<=M` at every fixed-support
continuous optimum, including every problem with some bits fixed.

For completeness, if `X=max_i|x_i|` on a nonempty support, stationarity at a
maximal coordinate gives

\[
X\le C/(2d)+\rho X,
\]

which proves the bound. Also `||Q||_2<=H` by the symmetric row-sum bound.

Take an even integer `B` with `B>=M sqrt(nH/epsilon)`, and use the grid
`{-M+2Mj/B:j=0,...,B}`, which includes zero. A supported coordinate is
rounded to its nearest grid value, with error at most `M/B`; coordinates
whose bits are zero stay zero. At the exact conditional optimum the linear
term in the rounding error vanishes. Therefore, with rounding vector `e`,

\[
f(x+e,z)-f(x,z)=e^TQe\le H\|e\|_2^2
\le HnM^2/B^2\le\epsilon.                                  \tag{7}
\]

The discrete grid problem has local states `(z_i,x_i)`: one inactive state
`(0,0)` and `B+1` active grid states. Unary costs are
`Q_ii x_i^2+c_i x_i+(lambda_i+xi_i)z_i`; edge costs are
`2Q_ij x_i x_j`. Fixed-bit restrictions simply delete local states. Standard
dynamic programming on the supplied tree decomposition computes its exact
minimum in `O(poly(n)(B+2)^(w+1))` arithmetic operations. One explicit
implementation assigns every unary/edge cost to a bag containing its
variables, and stores for each bag state the least subtree cost. Child
tables are minimized over states with the same separator restriction and
then added. Every factor is counted once.

The returned grid support is within `epsilon` of the unrestricted continuous
optimum for that restriction by (7). Exact conditional minimization returns

\[
x_S=-\tfrac12Q_{SS}^{-1}c_S,\qquad
g(z)=-\tfrac14c_S^TQ_{SS}^{-1}c_S+\lambda^Tz.                \tag{8}
\]

This gives the oracle in Section 2 with accuracy exponent `(w+1)/2`, up to
polynomial logarithmic factors for bit operations. No condition on volume
growth, degree, bandwidth, or biconnected block size was used. Noise affects
only the penalties and may have either sign.

With fixed `w,d,D,C,rho`, Section 3 gives polynomial expected arithmetic time
in the rational data size, `n`, and `phi`. More generally the bound is
polynomial for fixed `w` in the displayed magnitude/conditioning parameters.
It is not polynomial in the logarithms of arbitrarily large bounds or an
arbitrarily small diagonal-dominance margin.

The rational grid can be chosen without irrational arithmetic: find the
least even integer satisfying `B^2 epsilon>=M^2 nH`. Grid costs, table
entries, and the values in (8) have polynomial bit length in the rational
input and `log B`. A sum of polynomially many rational input terms and a
rational principal-system solve suffice; no exact irrational grid is used.

### Diagonal dominance is unnecessary for the one-optimizer conclusion

The same argument works for any rational symmetric matrix satisfying

\[
\mu I\preceq Q\preceq HI,\qquad \mu>0,\quad |c_i|\le C,
\]

with rational certified bounds `mu,H,C`. A principal submatrix has the same
spectral bounds. Therefore every support optimum satisfies

\[
\|x_S\|_\infty\le\|x_S\|_2
\le \frac{\|c_S\|_2}{2\mu}
\le\frac{C\sqrt n}{2\mu}
\le\frac{nC}{2\mu}.
\]

Use the rational bound `M=nC/(2mu)` in (7). Every later step is unchanged.
Consequently, for fixed treewidth, the one-optimizer theorem has polynomial
expected complexity in the input size, `C,H,1/mu`, and the smoothing
parameter. In particular, fixed positive spectral bounds and a fixed bound
on the linear coefficients suffice. Diagonal dominance, sign restrictions
on off-diagonal coefficients, and spectral decay of inverse entries are
unnecessary for this conclusion. This does not by itself extend an exact
message-construction theorem, which must control conditional problems over
whole separator domains.

## 5. Finite-grid noise and a Turing algorithm, including ties

Let `xi_i` be independent uniform choices from `N_g` equally spaced rational
points in `[-sigma,sigma]`, where `sigma>0` is rational, `N_g>=2`, and
`phi=1/(2 sigma)`. Here `N_g` denotes the grid cardinality, not input length.

For the certificate matrix `A` in (2), every inverse entry has magnitude at
most `(r-1)!`: its cofactors have that bound by the permutation expansion,
and its nonzero integer determinant has magnitude at least one. The inverse
image of the box in (2) is contained in a coordinate box of side length at
most `2r! epsilon`. A uniform one-dimensional grid gives any interval of
length `ell` probability at most `phi ell+1/N_g`. Independence therefore
replaces (1) with

\[
\Pr\{|A_\epsilon|\ge k_r\}
\le\binom nr2^{r(r+1)}
  (2r!\phi\epsilon+N_g^{-1})^r.                            \tag{9}
\]

This estimate is valid with positive-probability ties. It bounds the number
of distinct supports, not distinct cost values.

Take `N_g=2^n` when `n>=r`; the case `n<r` is enumerated directly. Run the
dyadic stages through the first `J` such that

\[
\epsilon_J\le \min(1,\sigma)/N_g.
\]

If stage `J` still does not certify an optimum, evaluate all `2^n` support
values exactly and return the best. Correctness is unconditional, including
ties. The fallback costs `2^n poly(N)` bit operations for the rational
indicator problem.

For `j<=J`, expand the right side of (9) using
`(a+b)^r<=2^(r-1)(a^r+b^r)`. The continuous part of the expected stage costs
is summable as in (5). The atomic part is bounded by

\[
\operatorname{poly}(N,n)N_g^{-r}\sum_{j=0}^{J}2^{aj}
\le \operatorname{poly}(N,n)
 N_g^{a-r}\max(1,\sigma^{-a}),                              \tag{10}
\]

with a constant depending on `a,r`. Since `r>a`, this is polynomial.
Failure at the last stage has probability at most
`C_r n^r N_g^-r`, because `phi epsilon_J<=1/(2N_g)`.
The expected fallback cost is at most

\[
\operatorname{poly}(N,n)\,2^nN_g^{-r}
\le\operatorname{poly}(N,n).                               \tag{11}
\]

All accuracies, grid points, and noise coordinates have polynomial encoding
length: `J=O(n+log^+(1/sigma))`. In the indicator application the bit cost of
each arithmetic operation is polynomial in these quantities. Taking a
slightly larger fixed `a` absorbs any logarithmic factors, and then taking
`r>a` validates (10). Sampling uses exactly `n` independent fair bits per
noise coordinate, hence `n^2` bits total. This establishes an expected
polynomial Turing algorithm for fixed treewidth and fixed structural bounds,
with polynomial dependence on `1/sigma`.

The exhaustive fallback is a proof device, not evidence of a useful
implementation. Removing it or improving practical constants is a separate
algorithmic question.

## 6. Literature and priority assessment

Sources inspected on 2026-09-22:

- [Röglin and Teng, *Smoothed Analysis of Multiobjective Optimization*,
  FOCS 2009](https://www.roeglin.org/publications/FOCS09.pdf), Sections 6.1–6.2
  and the appendix proof of Lemma 6.1. Their generalized winner gap and
  expected-time conversion are the direct antecedents. Their stated
  optimization theorem uses a linear objective and a pseudopolynomial
  oracle. Section 1 above gives an affine-rank proof accommodating arbitrary
  deterministic offsets; Sections 2–3 use an additive oracle directly.
  The central conversion strategy is established, and this extension should
  be described as an adaptation unless a deeper novelty audit establishes
  otherwise. Their Section 6.2 also discusses finite precision; finite-bit
  smoothing itself is not new.
- [Dughmi and Roughgarden, *Black-Box Randomized Reductions in Algorithmic
  Mechanism Design*, Proposition II.3](https://www.math.uwaterloo.ca/~cswamy/courses/co759/agt-material/blackbox.pdf)
  explicitly records the FPTAS-to-exact-smoothed conversion for binary
  linear maximization. The direct offset argument here avoids converting
  an additive oracle into an integer-valued pseudopolynomial oracle.
- [Röglin and Vöcking, *Smoothed Analysis of Integer Programming*,
  Section 6.1](https://www.roeglin.org/publications/IPCO05.pdf) extends its
  framework to arbitrary deterministic objective rankings for perturbed
  linear constraints. That is a different stated perturbation model, but
  it reinforces the need for modest novelty claims about offset extensions.
- [Bienstock and Muñoz, *LP Formulations for Polynomial Optimization
  Problems*](https://epubs.siam.org/doi/10.1137/15M1054079), with the
  [open preprint](https://arxiv.org/abs/1501.00288), is an established
  reference for bounded-treewidth mixed-integer polynomial approximation.
  Its publication abstract and accessible preprint material were examined.
  The grid construction in Section 4 is a direct elementary specialization
  and is not asserted to be new.
- [Bhathena, Fattahi, Gómez, and Küçükyavuz, *Solving Convex Quadratic
  Optimization with Indicators Over Structured Graphs*](https://arxiv.org/abs/2603.02103)
  studies exact parametric dynamic programming with treewidth, growth,
  and margin dependence. The present one-optimizer route has a different
  output and uses random penalties. A detailed theorem-by-theorem priority
  comparison for the fixed-treewidth corollary remains necessary.

Searches included combinations of “smoothed”, “arbitrary deterministic
function”, “additive linear perturbation”, “higher winner gap”, “FPTAS”, and
“bounded treewidth” on the same date. They did not establish that the exact
offset conversion or indicator corollary is absent elsewhere. No novelty
claim rests on an unsuccessful search.

## 7. Limits and next checks

- The oracle must survive arbitrary fixed-bit restrictions and certify
  emptiness when relevant. An unrestricted approximation scheme alone is
  insufficient for the stated conversion.
- Polynomial exact evaluation of the eliminated support objective is an
  essential assumption. Arbitrary nonconvex continuous subproblems do not
  meet it automatically.
- The result solves the perturbed problem exactly. It gives no exact
  solution guarantee for the original unperturbed instance.
- It does not construct continuous message envelopes, bound their number
  of connected regions, or provide a practical runtime estimate.
- The finite-grid proof uses a rare exhaustive fallback and loose
  constants exponential in the fixed approximation exponent. It establishes
  expected polynomial complexity, not practical superiority.
- The fresh [independent review](review-20260922-approximation-exact-oracle.md)
  checked the proofs, including the adaptive partition certificate and the
  finite-grid cutoff and expected bit-complexity argument, and found no
  substantive gap.
  No Lean proof has been produced.

## 8. Targeted computational verification

Command actually run:

```
python3 code/research_20260922/check_approximation_exact_smoothing.py
```

Result: 1,080 exact rational stages passed, with 700 optimality certificates,
380 higher-gap failure witnesses, and 5,208 oracle calls. The checker uses
small arbitrary nonintegral support costs, perturbed linear terms,
deliberately unfavorable valid approximate answers, and persistent ties. It
checks disjoint coverage of all unextracted supports, the lower-bound
invariant, exactness of every reported certificate, distinct extractions,
and the implication that stage failure exposes the required number of
near-optimal supports. It does not verify the continuous probability bound,
asymptotic runtime, or an implementation of the indicator grid DP. No
project-wide checks were run.
