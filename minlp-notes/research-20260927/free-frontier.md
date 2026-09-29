# Approximating indicator quadratics through Stieltjes majorants

Date: 2026-09-27. Status: supporting theoretical result; significance is modest
after an independent reviewer supplied a competing coordinate-grid argument.
The square-ratio improvement passed a fresh independent review. The result is an
additive guarantee, not an FPTAS in the usual relative-objective sense. Priority
is provisional; the underlying Stieltjes optimization theorem and the
quadratic majorization identity are established ingredients.

## Motivation and scope

Convex indicator quadratic optimization is polynomially solvable when its
continuous objective is submodular: for a quadratic, all off-diagonal entries
are nonpositive. This includes dense interaction graphs. A few positive
off-diagonal entries destroy that certificate, and branching on their binary
indicators does not remove their continuous interaction when both indicators
are active.

We can approximate such a problem by a finite collection of exactly solvable
Stieltjes problems. The collection changes only diagonal entries and deletes
positive off-diagonal entries. Its size depends exponentially on the number
of positive pairs, while the dependence on the remaining number of variables
and negative interactions is polynomial. The construction gives both a feasible
solution and a global additive error certificate.

## Problem and notation

Let \(Q\in\mathbb Q^{n\times n}\) be symmetric positive definite. Given
rational \(b,c\), and coordinate bounds \(u_i\in\mathbb Q_+\cup\{+\infty\}\),
consider

\[
 v=\min\{x^TQx-2b^Tx+c^Tz:
       0\le x_i\le u_i z_i,\quad z\in\{0,1\}^n\}.       \tag{1}
\]

For \(u_i=+\infty\), the notation means \(x_i\ge0\) and
\(z_i=0\Rightarrow x_i=0\). No additional constraints on \(z\) are
allowed in the theorem. In particular, there is no cardinality constraint.
The entries of \(b,c\) may have either sign. Let a rational certificate
\(\mu>0\) satisfy \(Q\succeq\mu I\), and define

\[
 E_+=\{\{i,j\}:i<j,\ Q_{ij}>0\},\qquad k=|E_+|,
 \qquad d_+=\max_i\sum_{j:Q_{ij}>0,\ j\ne i}Q_{ij}.       \tag{2}
\]

Only off-diagonal entries enter \(d_+\). If \(k=0\), established
submodular optimization solves (1) exactly, and no approximation is needed.

## A finite family of quadratic majorants

For a positive pair \(e=\{i,j\}\) with \(i<j\), write \(\beta_e=Q_{ij}\).
For \(r>0\), let \(D_e(r)\) have entries

\[
 [D_e(r)]_{ii}=\beta_e r,\quad
 [D_e(r)]_{jj}=\beta_e/r,\quad
 [D_e(r)]_{ij}=[D_e(r)]_{ji}=-\beta_e,
\]

and all other entries zero. The identity

\[
 x^TD_e(r)x=\beta_e(\sqrt r\,x_i-x_j/\sqrt r)^2\ge0       \tag{3}
\]

shows that \(D_e(r)\succeq0\). Its matrix entries are rational whenever
\(r\) is rational; square roots are used only to explain positivity.
For a vector \(r=(r_e)_{e\in E_+}\), set

\[
 Q_r=Q+\sum_{e\in E_+}D_e(r_e).                          \tag{4}
\]

Then \(Q_r\succeq Q\succeq\mu I\), and every off-diagonal entry of
\(Q_r\) is nonpositive. Thus \(Q_r\) is Stieltjes.

Fix a rational \(\varepsilon>0\), and choose the integer

\[
 M=\max\{1,\lceil\sqrt{d_+/(\varepsilon\mu)}\rceil\}.
                                                               \tag{5}
\]

The ceiling can be computed by comparisons of rational squares. Construct
the rational square-ratio grid

\[
 \mathcal R_M=\{j^2/M^2,M^2/j^2:1\le j\le M\}.           \tag{6}
\]

It has \(2M-1\) distinct elements, including 1.

**Lemma 1 (pointwise approximation).** For every \(x\ge0\), some
\(r\in\mathcal R_M^{E_+}\) satisfies

\[
 0\le x^T(Q_r-Q)x\le\varepsilon\mu\|x\|_2^2.            \tag{7}
\]

**Proof.** First we establish the scalar grid bound

\[
 \min_{r\in\mathcal R_M}(\sqrt r\,a-b/\sqrt r)^2
       \le\frac{\max\{a^2,b^2\}}{M^2}\qquad(a,b\ge0).   \tag{7a}
\]

When \(a\ge b\) and \(a>0\), put \(t=b/a\in[0,1]\). For
\(0\le t\le1/M^2\), the choice \(r=1/M^2\) gives normalized
error \((1/M-Mt)^2\le1/M^2\). Between adjacent square grid points
\(j^2/M^2\) and \((j+1)^2/M^2\), the corresponding nonnegative error
square roots are

\[
 Mt/j-j/M,\qquad (j+1)/M-Mt/(j+1).
\]

The first increases, the second decreases, and they are equal to \(1/M\)
at \(t=j(j+1)/M^2\). Their minimum is therefore at most \(1/M\).
This proves (7a) for \(a\ge b\). Interchange coordinates and take the
reciprocal grid ratio when \(b>a\). Cases with a zero coordinate are
included; when both vanish, any ratio works.

Choose each edge ratio to satisfy (7a). Summing and using
\(\max\{x_i^2,x_j^2\}\le x_i^2+x_j^2\) gives

\[
 x^T(Q_r-Q)x\le (d_+/M^2)\|x\|^2
                   \le\varepsilon\mu\|x\|^2.
\]

Positive semidefiniteness gives the lower bound. \(\square\)

The lemma is a pointwise selection statement. It does **not** assert that any
one matrix \(Q_r\) approximates \(Q\) uniformly from above in PSD order.

## Optimization theorem

For every tuple \(r\in\mathcal R_M^{E_+}\), solve (1) with \(Q_r\) in
place of \(Q\). Let \(U\) be the least resulting optimal value, and let
\((\widehat x,\widehat z)\) be an optimizer that attains it.

**Theorem 2.** The original objective \(F\) obeys

\[
 v\le F(\widehat x,\widehat z)\le U
       \le v+\varepsilon\|b\|_2^2/\mu.                 \tag{8}
\]

Consequently \([U-\varepsilon\|b\|^2/\mu,\,
F(\widehat x,\widehat z)]\) is a certified interval containing \(v\).
The interval endpoints may be tightened by taking the largest certified lower
bound or smallest original objective obtained elsewhere.

**Proof.** All problems attain minima: there are finitely many indicator
patterns, and the positive definite quadratic makes every nonempty continuous
fiber coercive. Let \((x^*,z^*)\) solve (1). For each \(t\in[0,1]\),
\((t x^*,z^*)\) is feasible. Differentiating its objective in \(t\) at
\(t=1\) from the left gives

\[
 (x^*)^TQx^*\le b^Tx^*.
\]

Thus \(\mu\|x^*\|^2\le\|b\|\|x^*\|\), including the zero case,
and

\[
 \|x^*\|\le\|b\|/\mu.                                 \tag{9}
\]

Lemma 1 supplies one tuple \(r^*\) for which the new objective at
\((x^*,z^*)\) is at most \(v+\varepsilon\mu\|x^*\|^2\), giving
the rightmost inequality in (8). Every modified objective majorizes the
original objective at every point. Hence the chosen solution is feasible for
the original problem and gives the other inequalities. \(\square\)

**Oracle count and encoding.** Directly from (6), the number of solves is

\[
 |\mathcal R_M|^k=(2M-1)^k.                              \tag{10}
\]

Every grid numerator and denominator has bit length \(O(\log(M+1))\);
the remaining encoding growth is polynomial in the input bit length and
\(k\log(M+1)\). Each
Stieltjes indicator problem is polynomially solvable by established reduction
to submodular minimization, using exact rational convex box-QP value oracles.
Thus this is a polynomial-time additive approximation scheme when \(k\) is
fixed and \(d_+/\mu\) is polynomially bounded in the input size. More
explicitly, the nonpolynomial parameter factor is

\[
 \left[O\!\left(1+\sqrt{d_+/(\varepsilon\mu)}\right)\right]^k.
                                                               \tag{11}
\]

For variable \(k\), this is an approximation algorithm parameterized by
\(k,d_+/\mu,1/\varepsilon\), with an input-polynomial factor. It is
not an exact fixed-parameter algorithm in \(k\), and it is not polynomial
in the logarithm of \(1/\varepsilon\). A poorly conditioned rational
input can make \(d_+/\mu\) exponentially large. The earlier geometric
ratio grid in this investigation had an extra logarithmic factor and larger
rational coefficients; (6) supersedes it.

## What the result adds and what it does not

### Comparison with ordinary coordinate gridding

An independent reviewer supplied a simpler competing argument. Let \(S\)
be a vertex cover of the positive-edge graph, with \(p=|S|\le k\).
Grid only \(x_S\) in a known bounded region. At a fixed zero coordinate,
choose its indicator to minimize its activation cost; at a positive coordinate,
the indicator is one. Fixing these coordinates leaves a Stieltjes
problem on the other variables. At an optimum of (1), every positive
coordinate below its upper bound has zero partial derivative. Include 0 and
each finite upper bound as exact grid points, so coordinates at their bounds
need not move. If the other selected coordinates move by at most \(h\),
the objective increase at fixed indicators is at most

\[
 \lambda_{\max}(Q_{SS})p h^2.                            \tag{12}
\]

This follows by expanding the quadratic: the linear term vanishes in the
coordinates that move, and \(e^TQe\le\lambda_{\max}(Q_{SS})\|e\|^2\).
Reoptimizing the remaining coordinates can only improve the value. With the
radius from (9), this yields comparable additive approximation by
\(O((1+\sqrt{p\lambda_{\max}(Q_{SS})/(\varepsilon\mu)})^p)\)
conditional Stieltjes solves, with certified rational grid enclosures in the
bit model. If \(b=0\), (9) already fixes every continuous coordinate to
zero at an optimum; if \(p=0\), the original problem is Stieltjes.

Therefore fixed-\(k\) additive tractability is not, by itself, evidence of
a substantial advance. Coordinate gridding can use fewer dimensions and is
often the better construction. The distinction in (11) is its dependence on
the positive off-diagonal row sum, with no direct dependence on large
diagonal or negative curvature. The nonlinear extension below makes this
distinction more precise. Neither algorithm has been implemented as a
practical submodular solver in this investigation.

### Interpretation and limits

The target is a dense attractive interaction system perturbed by a few
repulsive pairs. The theorem gives a global approximation certificate without
requiring small treewidth, small rank, a bound on the number of negative edges,
or generic/random data. The positive-edge count is a sufficient structural
parameter; it need not be a necessary one.

The subproblems retain the full negative interaction graph. Their practical
solution cost and the size of the ratio grid can be large. No computational
speedup has been demonstrated. Adaptive ratio refinement and reuse of
submodular solutions might help, but are not needed for correctness and are
not claimed here.

The scale \(\|b\|^2/\mu\) controls the continuous optimization gain.
Arbitrary activation costs can cancel that gain or shift the optimal value.
Therefore (8) is not a relative-error guarantee for \(v\), even if
\(v\) happens to be nonnegative after adding a constant. Positive lower
bounds on active coordinates also invalidate the scaling proof of (9);
a supplied radius bound could replace (9), but that is a different statement.

## Nonlinear extension with bounded positive interaction

The same argument is not limited to quadratics or bounded full Hessians.
Let \(\phi\) be a continuous convex function on a compact box \([0,u]\).
Let \(0\le\ell_i\le u_i\), and consider the on/off set

\[
 \mathcal F=\{(x,z):z_i=0\Rightarrow x_i=0,\quad
       z_i=1\Rightarrow\ell_i\le x_i\le u_i,\quad
       z\in\{0,1\}^n\}.
\]

Suppose a set \(E\) of \(k\) coordinate pairs and constants
\(\beta_{ij}>0\) are given such that

\[
 \psi(x)=\phi(x)-2\sum_{\{i,j\}\in E}\beta_{ij}x_ix_j
                                                               \tag{13}
\]

is submodular on the box. Convexity of \(\psi\) is not assumed. Define

\[
 B=\sum_{\{i,j\}\in E}\beta_{ij}\max\{u_i^2,u_j^2\}.    \tag{14}
\]

**Theorem 3 (convex objectives).** For an integer \(M\ge1\), form
\((2M-1)^k\) objectives

\[
 \phi_r(x)=\phi(x)+\sum_{\{i,j\}\in E}
       \beta_{ij}(\sqrt{r_{ij}}x_i-x_j/\sqrt{r_{ij}})^2,
 \qquad r\in\mathcal R_M^E.                            \tag{15}
\]

Each \(\phi_r\) is convex and submodular on the box. If an oracle solves
the resulting indicator problems exactly, the least surrogate optimum
\(U\) and its feasible optimizer obey

\[
 v\le\phi(\widehat x)+c^T\widehat z\le U\le v+B/M^2,
 \quad v=\min_{(x,z)\in\mathcal F}(\phi(x)+c^Tz).        \tag{16}
\]

**Proof.** The added squares preserve convexity. Using (13),

\[
 \phi_r(x)=\psi(x)+\sum_{\{i,j\}\in E}
       \beta_{ij}(r_{ij}x_i^2+x_j^2/r_{ij}),
\]

so \(\phi_r\) is submodular: adding a separable function preserves the
submodular lattice inequality. Compactness and continuity give attainment.
At an original optimizer, apply (7a) to each pair. The total added value is
at most \(B/M^2\). Pointwise majorization and minimization give (16),
exactly as in Theorem 2. \(\square\)

Theorem 3 is an **oracle reduction**. Polynomial exact solution of arbitrary
real-valued convex box subproblems is not assumed without an input model.
The established convex-submodular indicator theorem supplies the reduction
to those convex subproblems. If each surrogate oracle instead returns a
feasible solution within additive \(\tau\) of its global surrogate
minimum, selecting the best surrogate solution gives error at most
\(B/M^2+\tau\), not \(B/M^2+(2M-1)^k\tau\).

If \(\phi\) is twice continuously differentiable on a neighborhood of
the box, an easily stated sufficient condition for (13) is

\[
 \partial_{ij}\phi(x)\le2\beta_{ij}\quad(\{i,j\}\in E),
 \qquad\partial_{ij}\phi(x)\le0\quad(\{i,j\}\notin E),
                                                               \tag{17}
\]

for every \(x\) in the box and every distinct \(i,j\). No upper bound
on pure second derivatives or on the magnitude of negative mixed derivatives
enters (14)–(16). Thus the theorem also covers objectives where ordinary
second-order coordinate-grid estimates have a very large or unavailable
curvature bound. This is the most useful potential distinction, although
its practical importance and novelty remain unestablished.

## Exact one-positive-edge reduction remains open here

For \(x_i,x_j\ge0\), weighted AM–GM gives

\[
 2\beta x_ix_j=\inf_{r>0}\beta(rx_i^2+x_j^2/r).          \tag{18}
\]

When both coordinates are positive, the infimum is attained at
\(r=x_j/x_i\); when exactly one vanishes, it is a limit. Hence, with
one positive pair, the original optimum equals the infimum over a scalar
parameter of exactly solvable Stieltjes indicator problems. This does not
establish polynomial exact optimization of the scalar envelope. No proof
of hardness or exact tractability for that boundary was obtained here.

Scalar parameter dimension alone does not justify a finite polynomial
enumeration of all optimizer supports. Conversely, known large parametric
representations do not rule out another exact optimization algorithm.

## Literature examined and novelty boundary

- Atamtürk and Gómez, *Strong Formulations for Quadratic Optimization with
  M-matrices and Indicator Variables*, Mathematical Programming 170 (2018),
  141–176, [arXiv:1804.05284](https://arxiv.org/abs/1804.05284). This supplies
  the established Stieltjes/submodular algorithmic baseline.
- Han and Gómez, *Convex Submodular Minimization with Indicator Variables*,
  [canonical arXiv:2209.13161](https://arxiv.org/abs/2209.13161). The inspected
  recent version treats general continuous convex submodular objectives and
  sign-switchable quadratic patterns. The duplicate arXiv:2507.00442 record
  redirects to this canonical submission. Its reduction, not a new oracle
  theorem here, justifies the general signed \(b,c\) and box-bound scope.
- Gorelick and coauthors, *Submodularization for Quadratic Pseudo-Boolean
  Optimization*, [arXiv:1311.1856](https://arxiv.org/abs/1311.1856), is a close
  algorithmic predecessor. The inspected version's Section 2.2 constructs
  submodular auxiliary upper bounds for binary pairwise energies and proves
  objective descent for its iterative method. The present claim concerns a
  finite family of convex quadratic majorants with a prescribed additive
  global guarantee for continuous on/off variables. Merely replacing
  non-submodular terms by an upper bound is therefore established practice.
- El Halabi and Jegelka, *Optimal approximation for unconstrained
  non-submodular minimization*, ICML 2020,
  [primary paper](https://proceedings.mlr.press/v119/halabi20a/halabi20a.pdf).
  Section 3, Theorem 1 and Corollary 1 concern a value-oracle set function
  expressed as a difference of functions satisfying weak diminishing-returns
  assumptions. Their guarantee uses multiplicative distortion parameters
  for those components plus algorithmic tolerance. Equations (13)–(16)
  instead assume an explicit continuous bilinear correction and bound the
  absolute error by its coefficients and coordinate bounds. No equivalence
  or separation between these parameterizations has been proved here.
- The repository's [signed low-rank exploration](../research-20260925/integer-structure-exploration.md)
  gives a separate fixed-rank negative-update algorithm and positive-update
  hardness. Its assumptions differ: here the Stieltjes part may have full
  rank and dense support, and the positive perturbation is measured by pairs.

The exact ratio identity is weighted AM–GM and is not claimed as original.
The proposed contribution is its finite, rational, uniformly certified
approximation family combined with the Stieltjes indicator optimization
oracle. Literature comparison and independent adversarial review remain
necessary before making a publication-priority claim.

## Separate parametric obstruction scouted

Allman, Lo and McCormick, *Complexity of Source-Sink Monotone 2-Parameter
Min Cut*, Operations Research Letters 50 (2022), 84–90,
[arXiv:2107.09743](https://arxiv.org/abs/2107.09743), prove that all
\(2^n\) cuts can occur as unique optima under two monotone parameters.
Their construction uses very large coefficients; the paper explicitly
records doubly exponential growth. It cannot be cited for an exponential
lower bound in binary input length.

A small quadratic perturbation can transfer finitely many strict cut optima
to near-diagonal Stieltjes indicator QPs, suggesting a useful obstacle to
exact two-parameter warm-start dictionaries. This transfer is not developed
as a theorem here: the positive approximation result above is the more useful
direction. A failed search for a short exact dictionary is not evidence of
novelty, and the known min-cut result already supplies the central phenomenon.

## Verification status

An independent agent proposed the underlying one-positive-edge identity and
checked the initial geometric-grid estimate, the maximum positive row-sum
refinement, and the need for rational grids and downward-scalable continuous
fibers. A fresh reviewer independently checked the replacement square grid
and supplied the sharp constant-one scalar estimate (7a). The nonlinear
extension and the competing coordinate-grid argument also received independent
adversarial checks. The written [review](free-frontier-review.md) records the
scope and remaining novelty limits.

Targeted command actually run:

```sh
python research-20260927/check_stieltjes_majorants.py
```

It passed 24 exact small optimization instances, 314 Stieltjes problems solved
by exhaustive support enumeration, and 960 rational square-grid checks. Grid
sizes ranged from 1 to 11; the samples include zero coordinates, very unequal
coordinate ratios, signed linear terms and signed activation penalties.
The checker uses only Python's standard library and rational arithmetic. It
does not implement the polynomial submodular oracle, test practical runtime
on large inputs, or certify the general nonlinear theorem. No project-wide
checks or CI inspection have been run. Lean formalization was not used.
The independent review additionally records a separate exact scalar-grid check
with 9,984 cases, including sharpness on the coordinate axes.
