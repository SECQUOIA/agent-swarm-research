# Independent review of the Stieltjes-majorant approximation

Date: 2026-09-27. Reviewed object: [free-frontier.md](free-frontier.md).
Status: the square-ratio construction and the radius argument pass this
review under the assumptions stated below. The main contribution remains a
modest supporting result. Its elementary coordinate-grid comparator must be
reported, and originality is not established by the literature search.

The reviewer first scouted the exact one-positive-edge question, independently
checked the approximation, and delegated a fresh review of the square grid
and smooth extension. Both reviewers obtained the constant-one grid bound
below. This agreement is supporting evidence; the proofs remain the basis
for the claims.

## 1. The square-ratio lemma, with the improved constant

For an integer \(M\ge1\), define

\[
 \mathcal R_M=\{j^2/M^2,M^2/j^2:1\le j\le M\}.
\]

There are exactly \(2M-1\) distinct ratios. Every numerator and denominator
has bit length \(O(\log(M+1))\).

**Lemma.** For every \(a,b\ge0\),

\[
 \min_{r\in\mathcal R_M}
       (\sqrt r\,a-b/\sqrt r)^2
 \le \frac{\max\{a^2,b^2\}}{M^2}
 \le \frac{a^2+b^2}{M^2}.                         \tag{R1}
\]

The first inequality is sharp when exactly one of \(a,b\) is zero.

**Proof.** The zero vector is immediate. Suppose first that \(a>0\) and
\(q=b/a\in[0,1]\). Put \(t_j=j/M\). If \(q\le t_1^2\), choose
\(r=t_1^2\). Then \(0\le t_1-q/t_1\le1/M\).

Otherwise, either \(q=1\), which has zero error at \(r=1\), or some
\(j\in\{1,\ldots,M-1\}\) satisfies
\(t_j^2\le q\le t_{j+1}^2\). If \(q\le t_jt_{j+1}\), choose
\(r=t_j^2\); then

\[
 0\le q/t_j-t_j\le t_{j+1}-t_j=1/M.
\]

If \(q\ge t_jt_{j+1}\), choose \(r=t_{j+1}^2\); then

\[
 0\le t_{j+1}-q/t_{j+1}\le t_{j+1}-t_j=1/M.
\]

Multiplication by \(a^2\) proves the claim for \(a\ge b\). When
\(b>a\), swap the coordinates and invert the chosen ratio. The grid is
closed under reciprocals, and this gives the bound \(b^2/M^2\).
If \(b=0<a\), the minimum is \(a^2/M^2\), since the smallest ratio is
\(M^{-2}\); the other axis is symmetric. \(\square\)

The earlier factor-four ceiling estimate was valid, but R1 supersedes it.
There is no logarithmic grid factor. Square roots occur only in the proof;
the actual matrix entries use rational \(r\) and \(1/r\).

For nonnegative weights \(\beta_{ij}\) on a set \(E\) of unordered pairs,
let

\[
 d=\max_i\sum_{j:\{i,j\}\in E}\beta_{ij}.
\]

Choosing ratios independently in R1 gives, for every fixed \(x\ge0\),

\[
 \sum_{\{i,j\}\in E}\beta_{ij}
       (\sqrt{r_{ij}}x_i-x_j/\sqrt{r_{ij}})^2
 \le \frac{d}{M^2}\|x\|^2.                       \tag{R2}
\]

This is a pointwise choice of a tuple depending on \(x\). It is not one
matrix inequality that holds uniformly for all \(x\) with a fixed tuple.

## 2. General convex objectives and radius assumptions

The cleanest sufficient structural assumption does not require smoothness.
Let \(\phi\) be convex on a nonnegative box containing all feasible
continuous variables. Suppose

\[
 \psi(x)=\phi(x)-2\sum_{\{i,j\}\in E}\beta_{ij}x_ix_j
                                                               \tag{R3}
\]

is continuously submodular on that box. For a tuple of positive ratios set

\[
 \phi_r(x)=\phi(x)+\sum_{\{i,j\}\in E}\beta_{ij}
       (\sqrt{r_{ij}}x_i-x_j/\sqrt{r_{ij}})^2.
                                                               \tag{R4}
\]

Each \(\phi_r\) is convex because R4 adds positive semidefinite quadratic
forms. It is submodular because it equals \(\psi\) plus separable
univariate quadratic functions. This proves the reduction directly.

For \(C^2\) objectives, a sufficient condition for R3 is
\(\partial_{ij}\phi\le2\beta_{ij}\) on pairs in \(E\), and
\(\partial_{ij}\phi\le0\) on every other distinct pair. These bounds
must hold throughout the box used by the continuous optimization oracles.
A certificate only on a Euclidean radius ball is insufficient: the ball is
not generally a lattice, and the oracle can query points outside it.

Suppose the original indicator problem has an optimal pair \((x^*,z^*)\)
with a known bound \(\|x^*\|\le R\). Assume that the surrogate problems
can be minimized by the stated oracle; attainment or an appropriate
approximate-solution convention must be included. Solving R4 over every
tuple in \(\mathcal R_M^E\), and selecting the smallest surrogate value
\(U\), gives a feasible original solution with

\[
 v\le F(\widehat x,\widehat z)\le U
       \le v+dR^2/M^2.                            \tag{R5}
\]

Indeed, R2 applies to \(x^*\), while every surrogate majorizes the original
objective. This radius-based statement allows arbitrary nonnegative active
intervals \(\ell_i z_i\le x_i\le u_i z_i\). Compact intervals supply
\(R=\|u\|\) and attainment for continuous objectives. Strong convexity
supplies coercivity and a sharper radius in the zero-lower-bound case.

Specifically, suppose \(\phi\) is differentiable and \(\alpha\)-strongly
convex in the standard convention, and \(0\le x_i\le u_i z_i\).
At an optimum with its indicator vector fixed, radial feasibility gives

\[
 \nabla\phi(x^*)^Tx^*\le0.
\]

Strong monotonicity of the gradient therefore implies

\[
 \alpha\|x^*\|^2
 \le -\nabla\phi(0)^Tx^*
 \le \|[-\nabla\phi(0)]_+\|\,\|x^*\|.
\]

Thus \(R=\|[-\nabla\phi(0)]_+\|/\alpha\) is valid. The full gradient
norm also gives a valid, weaker bound. Arbitrary activation costs do not
affect this argument because \(z\) stays fixed during scaling.

For the main note's normalization \(\phi(x)=x^TQx-2b^Tx\) with
\(Q\succeq\mu I\), take \(\alpha=2\mu\). This yields
\(R=\|b_+\|/\mu\le\|b\|/\mu\), and

\[
 M=\max\{1,\lceil\sqrt{d/(\varepsilon\mu)}\rceil\}
\]

suffices for error \(\varepsilon\|b\|^2/\mu\). There is no missing
factor of two under this normalization. For an objective
\(x^TQx/2-b^Tx\), the corresponding majorant penalty is half as large.

The zero lower bounds are essential for the gradient-derived radius. For
\(\phi(x)=x^2/2\), \(x=z\), and activation cost \(-1\), the optimum
has \(x=z=1\), although \(\nabla\phi(0)=0\). The radius-based theorem
itself survives when another valid radius is supplied.

## 3. Elementary coordinate gridding is a material comparator

Consider the main note's quadratic normalization with zero lower activation
bounds. Let \(S\) be a set of \(p\ge1\) coordinates such that deleting
\(S\) leaves a Stieltjes principal
matrix. Write \(L_S=\lambda_{\max}(Q_{SS})\) and
\(R=\|b\|/\mu\). If \(S\) covers the positive-edge graph, this
condition holds; selecting one endpoint per positive edge gives \(p\le k\).
If \(p=0\), the original problem is already Stieltjes and can be solved
exactly without a grid.

Grid each selected coordinate over \([0,\min\{u_i,R\}]\), using mesh
at most \(h\) and including both endpoints. Fix a global optimum and its
indicator vector. Coordinates at actual interval bounds can be preserved
exactly. Every coordinate changed by rounding is interior to its original
continuous interval, so its partial derivative vanishes. Rounding only
selected coordinates therefore gives

\[
 F(x^*+e,z^*)-F(x^*,z^*)
 =e_S^TQ_{SS}e_S\le L_Sp h^2.                      \tag{R6}
\]

This includes coordinates at the artificial radius endpoint: if that endpoint
is not an actual bound, the coordinate is interior and has zero derivative.
If \(R=0\), there is no grid to build: all continuous variables are zero.

For each grid point, the remaining problem is a conditional Stieltjes
indicator problem, with altered linear coefficients. A selected positive
coordinate forces its indicator to one. At a selected zero coordinate,
choose its indicator optimally from its activation cost; no extra binary
enumeration is needed because there are no other indicator constraints.

Taking \(h=R\sqrt{\varepsilon\mu/(pL_S)}\) yields additive error
\(\varepsilon\|b\|^2/\mu\), with

\[
 \left[O\!\left(1+\sqrt{pL_S/(\varepsilon\mu)}\right)\right]^p
                                                               \tag{R7}
\]

conditional solves. Thus a fixed-number-of-exceptional-coordinates additive
scheme follows from an elementary argument. The square-ratio result should
not be sold merely as fixed-\(k\) approximate tractability.

R7 is a solve-count comparison. The displayed norm and eigenvalue may be
irrational; an implementation in the rational bit model should use certified
rational upper bounds for \(R,L_S\) and a rational mesh no larger than the
required one.

The square-ratio construction's stronger distinction is its dependence only
on positive mixed curvature. It does not require an upper bound on diagonal
curvature. The smooth extension can therefore be preferable when separable
curvature is large or unbounded, while positive mixed derivatives remain
bounded. This is a theoretical distinction, not a demonstrated solver speedup.

## 4. Oracle, encoding, and significance qualifications

- \((2M-1)^k\) counts complete surrogate indicator minimizations. Each
  invokes the established submodular reduction and its continuous box-value
  oracles; it is not one continuous convex solve per tuple.
- General smooth strong convexity does not imply exact polynomial-time
  continuous minimization. State the smooth result in an oracle model.
  Rational quadratic data support the intended bit-complexity specialization.
- If a complete surrogate oracle returns a feasible solution within additive
  \(\tau\) of its minimum, R5 gains only \(\tau\). This does not by itself
  justify replacing the underlying submodular value oracle by approximate
  values: those values need not remain submodular.
- The ratio \(d/\mu\) can be exponential in input bit length. The claim is
  neither an exact fixed-parameter algorithm in \(k\), nor an unconditional
  fixed-\(k\) FPTAS. Arbitrary activation costs also prevent conversion of
  the stated additive bound to a relative-objective guarantee.
- Negative activation costs are allowed, but the active indicator set need
  not equal the nonzero support: \(z_i=1,x_i=0\) remains possible.
- The nonnegativity assumption is substantive. The squared majorant need
  not approach zero at a pair of coordinates with opposite signs.

## 5. Literature checked and unresolved questions

[Han and Gómez, arXiv:2209.13161v2](https://arxiv.org/html/2209.13161v2)
is the canonical source. It establishes the convex-submodular indicator
reduction, including arbitrary activation intervals and sign-switchable
quadratics. The arXiv:2507.00442 withdrawal identifies a duplicate submission,
not a retraction of the mathematics. Polynomiality is conditional on the
continuous box optimization oracle. The square-ratio note uses this theorem
and does not replace it.

Their contracted-sign graph condition requires retaining positive self-loops:
a positive edge internal to a connected negative-edge component obstructs
sign switching. Removing those loops would incorrectly broaden the condition.

Additional comparisons examined during this scout:

- [Mittal and Schulz, low-rank optimization](https://optimization-online.org/wp-content/uploads/2011/09/3152.pdf)
  concerns a low-rank objective with positivity, monotonicity, and scaling
  conditions over a polytope with a separation oracle. Those hypotheses do
  not directly cover a dense Stieltjes objective with indicators.
- [Iyer and Bilmes, 2019](https://proceedings.mlr.press/v89/iyer19a/iyer19a.pdf)
  studies fixed sums of monotone concave-over-modular terms. Enumerating
  approximating linear pieces is methodological precedent, not an identified
  theorem for the present continuous indicator model.
- [Han, Gómez, and Atamtürk, two-variable convexifications](https://link.springer.com/article/10.1007/s10107-023-01924-w)
  treats positive-cross-term convexification, rather than the present
  few-positive-pairs approximation statement.
- [Goemans, Gupta, and Jaillet, IPCO 2017, Section 5](https://web.mit.edu/jaillet/www/general/ggj-ipco-17.pdf)
  distinguishes polynomial discrete Newton line search from enumeration of
  all signed-modular parametric breakpoints. It does not justify exact
  polynomial minimization of the ratio envelope here.
- [Allman, Lo, and McCormick](https://arxiv.org/abs/2107.09743) establish
  exponential two-parameter minimum-cut complexity. This blocks a naive
  inference from fixed parameter dimension to few solution regions, but
  does not settle a particular reciprocal curve of parameters.
- [Bhathena, Fattahi, Gómez, and Küçükyavuz, 2026](https://arxiv.org/abs/2603.02103)
  develops structured-graph algorithms with additional parameters. The
  results examined do not settle unconditional exact complexity with one
  frustrated positive edge.

The AM–GM identity and finite covering argument are elementary. No equivalent
specialized theorem was identified in this limited search, which does not
establish novelty. Exact complexity with one frustrated positive edge remains
unresolved by this scout. Neither the generic binary branching argument nor
the approximation theorem answers it.

## 6. Reproducible targeted verification

The following command was run from the repository root. It uses exact
rational arithmetic to evaluate the penalty without floating-point square
roots. It checks 9,984 finite cases and the grid cardinality; it does not
prove the universal inequality, verify an optimizer implementation, or test
the Han–Gómez reduction.

```sh
python - <<'PY'
from fractions import Fraction as F
worst = F(0)
arg = None
checks = 0
for M in range(1, 17):
    grid = ({F(j*j, M*M) for j in range(1, M+1)}
            | {F(M*M, j*j) for j in range(1, M+1)})
    assert len(grid) == 2*M - 1
    for a in range(25):
        for b in range(25):
            if not (a or b):
                continue
            err = min(r*a*a - 2*a*b + F(b*b, 1)/r for r in grid)
            ratio = err*M*M/F(a*a+b*b, 1)
            assert ratio <= 1, (M, a, b, ratio)
            if ratio > worst:
                worst, arg = ratio, (M, a, b)
            checks += 1
print({'exact_rational_cases': checks,
       'maximum_sampled_normalized_error': str(worst),
       'maximizer': arg, 'bound': 1})
PY
```

The initial run asserted the weaker bound 4 and reported a maximum of 1.
The displayed strengthened command was then rerun and passed, with output:

```text
{'exact_rational_cases': 9984, 'maximum_sampled_normalized_error': '1', 'maximizer': (1, 0, 1), 'bound': 1}
```

A fresh reviewer independently checked the constant-one lemma, radius proof,
and oracle assumptions. No Lean formalization was attempted: the short
inequality proof and independent checks were the relevant verification here.
No project-wide verification or CI inspection was run.
