# Limits of nonlinear depth as an exact-penalty parameter

Date: 2026-09-27. Status: supporting results and limitations, not a claimed
major contribution. The constructions and restricted positive result were
independently checked by a second research agent. The literature status
below records the sources examined; unsuccessful searches are not proof
that a problem remains open.

## Affine dependencies can hide an arbitrarily long squaring chain

For \(n\ge1\), impose

\[
 x_i,t_i\in[0,1],\qquad x_1\ge\tfrac14,\qquad
 t_i\ge x_i^2\quad(1\le i\le n),\qquad
 x_{i+1}\ge t_i\quad(1\le i<n).
\]

Each lower epigraph function \(x_i^2\) is convex and nondecreasing on the
nonnegative interval; its inequality has a rank-one Hessian. The quadratic dependency
arcs \(x_i\to t_i\) are pairwise disjoint. If a proposed depth counts
only these arcs, its value is one. Nevertheless,

\[
 \min t_n=\left(\frac14\right)^{2^n}=2^{-2^{n+1}}.
\]

The lower bound follows inductively, and equality is attained by making
every displayed lower bound tight. The sparse input length is
\(O(n\log(n+1))\), with coefficients from a fixed finite set. Thus
the inverse positive separation has exponentially many bits despite
quadratic-only depth one.

This is an unconditional counterexample to a depth definition that omits
affine dependencies. A usable circuit depth must retain the affine arcs
\(t_i\to x_{i+1}\) with weight zero while counting each squaring gate
with weight one. The corrected depth of this construction is \(n\).

## Independent rank-one quadratics already contain square-root-sum comparison

Take positive integers \(a_1,\ldots,a_n,B\), encoded in binary, and define

\[
 K=\{x\in\mathbb R^n:0\le x_i\le a_i+1,\ x_i^2\le a_i\},
 \qquad r(x)=B-\sum_i x_i.
\]

The native quadratic supports are disjoint. Every Hessian is rank one,
and \(x_i=1/4\) gives nonlinear slack at least \(15/16\).
Since \(K=\prod_i[0,\sqrt{a_i}]\),

\[
 \min_Kr=B-\sum_i\sqrt{a_i},\qquad
 \min_K|r|=\max\left\{0,B-\sum_i\sqrt{a_i}\right\}.
\]

The second identity uses \(B>0\) and the fact that the sum of these
intervals is \([0,\sum_i\sqrt{a_i}]\). Each cap can alternatively be
written as a monotone quadratic epigraph \(t_i\ge x_i^2\) with
\(t_i\le a_i\). These independent epigraphs have nonlinear depth one,
including their affine upper caps. The scalar affine residual couples
their inputs with negative coefficients.

Suppose a theorem supplied a uniform, explicit bound
\(\delta\ge2^{-p(L)2^d}\) for every positive residual separation in
this class, where \(L\) is input length, \(p\) is a fixed polynomial,
and \(d\) is nonlinear depth. At \(d=1\), write the resulting known
lower bound as \(\eta=2^{-2p(L)}\). Approximate
\(S=\sum_i\sqrt{a_i}\) within \(\eta/4\) using rational intervals.
If \(B>S\), then \(B-S\ge\eta\), so
\(B-\widetilde S\ge3\eta/4\). If \(B\le S\), then
\(B-\widetilde S\le\eta/4\). The threshold \(\eta/2\) therefore
decides whether \(S\ge B\) in polynomial time, including equality.

This is an implication to the classical square-root-sum problem, **not**
an unconditional superpolynomial lower bound. The polynomial separation
bound might be true. The implication explains why general affine
residuals make even depth-one systems a substantially harder research
target than forward evaluation of rational circuits.

### Direct exact-penalty version

When \(\delta=B-S>0\), put
\(H=B+\sum_i a_i+2\), \(M=B+H\), and add

\[
 q\in\{0,1\},\quad -H\le y\le H,\quad
 y\ge B-\sum_i x_i-M(1-q).
\]

Minimize \(-q\) subject to these native constraints, \(x\in K\),
and the linking equality \(y=0\). Projection onto \((q,y)\) is

\[
 (\{0\}\times[-H,H])\ \cup\ (\{1\}\times[\delta,H]).
\]

The original optimum is zero. For augmentation \(\rho|y|\), the least
dual-value exact penalty after optimizing the scalar multiplier is
\(1/(2\delta)\). Indeed, the points \((0,-H)\) and
\((1,\delta)\), weighted by \(\delta/(H+\delta)\) and
\(H/(H+\delta)\), cancel the multiplier and give upper bound

\[
 \frac{H(2\rho\delta-1)}{H+\delta}.
\]

It is negative below the claimed threshold. At and above the threshold,
choosing multiplier \(\lambda=\rho\) makes the augmented objective
nonnegative everywhere and zero at a feasible optimum. The native slices
have strict points \(x_i=1/4\), using \(y=0\) for \(q=0\) and
\(y=B+1\) for \(q=1\). The equality-feasible slice is \(q=0\) and
also has such a strict point. Thus the square-root-sum implication is
relevant even when the paper's feasible-slice Slater assumption holds.

## A restricted forward theorem

Let variables \(x_1,\ldots,x_n\) be topologically ordered. Each variable
has rational bounds \(0\le\ell_j\le x_j\le U_j\) and finitely many
lower epigraph constraints

\[
 x_j\ge q_{j,t}(x_1,\ldots,x_{j-1}),
\]

where each \(q_{j,t}\) is rational, has degree at most two, and is
coordinatewise nondecreasing on the nonnegative predecessor box. For the
convex quadratic subclass, additionally require each \(q_{j,t}\) convex.
Other constraints may be nonnegative affine upper rows \(Ax\le b\),
with \(A\ge0\). Suppose the resulting system is feasible.

The recursively defined point

\[
 x_j^*=\max\{\ell_j,\ q_{j,t}(x_1^*,\ldots,x_{j-1}^*)\text{ for all }t\}
\]

is its coordinatewise least feasible point. To prove this, fix any feasible
\(x\). Induction and monotonicity give \(x_j^*\le x_j\), which also
shows that the recursion stays inside every predecessor box. The point
\(x^*\) satisfies its lower epigraphs by construction. Since
\(x^*\le x\), it satisfies all coordinate upper bounds and all
nonnegative affine upper rows. In particular, every affine function
\(r(x)=c^Tx-b_0\), \(c\ge0\), is minimized at \(x^*\).

Let \(Q\) be the product of all positive input denominators and let
\(S\) be their total encoding length. Then \(\log_2Q\le S\).
Retain every affine dependency edge when defining depth. Set the depth
of a node to the maximum depth of its predecessors, adding one if any of
its defining polynomials has a quadratic term. Constant nodes have depth
zero. Let \(d\) be the largest node depth.

Each coordinate denominator divides \(Q^{e_j}\), where one may choose

\[
 e_j=\max\left\{1,\ 1+e_i\text{ for a linear monomial},\
 1+e_i+e_l\text{ for a quadratic monomial}\right\}.
\]

All candidate values in the maximum are rationals with denominators
dividing the same sufficiently high power of \(Q\). Taking their maximum
selects one value and introduces no additional denominator. Induction on
the topological order gives
\(e_j\le j2^{d_j}\). Consequently, for rational input \(c,b_0\),
the denominator of \(r(x^*)\) divides \(Q^{1+n2^d}\). If
\(\delta=r(x^*)>0\), then

\[
 \delta\ge Q^{-(1+n2^d)}\ge2^{-S(1+n2^d)}.
\]

The exponential dependence on depth is necessary up to polynomial
factors, as repeated squaring shows. This positive theorem is an
elementary rational-denominator observation. It requires a least-point
description and a nonnegative residual coefficient vector. It does not
cover the negative sum residual in the preceding section, arbitrary
affine coupling, or the multiplier bounds needed for a general
exact-penalty theorem.

## Literature comparison and status of the square-root-sum question

The following sources were examined on 2026-09-27.

- Allender, Bürgisser, Kjeldgaard-Pedersen and Miltersen, *On the
  complexity of numerical analysis*, SIAM Journal on Computing 38(5)
  (2009), 1987–2006, DOI
  [10.1137/070697926](https://doi.org/10.1137/070697926),
  [open author PDF](https://people.cs.rutgers.edu/~allender/papers/slp.pdf).
  Section 1.4 uses the same integer-versus-positive-sum decision problem
  as above. Corollary 1.5 puts it in the counting hierarchy. The depth-one
  reduction here should not be presented as a new complexity problem.

- Eisenbrand, Haeberle and Singer, *An improved bound on sums of square
  roots via the subspace theorem*, SoCG 2024, 54:1–54:8,
  [official open article](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2024.54),
  [full PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol293-socg2024/LIPIcs.SoCG.2024.54/LIPIcs.SoCG.2024.54.pdf).
  The paper treats signed integer combinations of square roots. Its new
  bound has a nonexplicit constant depending on the radicands, so it does
  not supply a uniform polynomial-precision bound when the radicands are
  part of the input. The paper describes polynomial-time decision as
  open.

- The [Open Problems Project, Problem 33](https://topp.openproblem.net/p33)
  still labels the separation question open in the page examined. Its
  visible revision history ends in 2009, so its current availability alone
  is not evidence of a recent literature audit. Searches including 2025
  and 2026 did not find a resolving primary result. We therefore record
  the question as unresolved in the examined literature, without claiming
  that an unsuccessful search establishes this exhaustively.

- Stewart, Etessami and Yannakakis, *Upper bounds for Newton's method on
  monotone polynomial systems, and P-time model checking of probabilistic
  one-counter automata*, Journal of the ACM 62(4) (2015), Article 30,
  DOI [10.1145/2789208](https://doi.org/10.1145/2789208),
  [open accepted manuscript](https://www.pure.ed.ac.uk/ws/portalfiles/portal/20056266/final_jacm_cav13_jversion.pdf).
  Corollary 4.4 bounds approximation time polynomially in input length,
  \(2^f\), precision, \(\log(1/q_{\min})\), and
  \(\log q_{\max}\). Their \(f\) counts internally nonlinear strongly
  connected components along dependency paths. This differs from counting
  nonlinear gates in an acyclic circuit: an acyclic squaring chain has
  \(f=0\), while its very small least-positive coordinate remains visible
  through \(q_{\min}\). Their Section 4.1 also gives a matching
  exponential-in-\(f\) Newton-iteration example. These are significant
  precedents for depth-sensitive analysis, not a solution of the general
  affine-residual separation question.

## Verification record

The chain, square-root-sum reduction and forward-denominator theorem were
independently reconstructed by a second agent. The penalty projection and
threshold use the same two-witness calculation as
`paper-exact-penalties/sections/03-lower-bound.tex`, with the left interval
length replaced by \(H\). The primary sources above were opened and
their relevant statements inspected. No computational tests or Lean proof
were run; no project-wide checks or CI inspection were performed.
The targeted command
`git diff --no-index --check /dev/null research-20260927/penalty-depth-limitations.md`
produced no whitespace diagnostics; its exit status was 1 because the new
file differs from `/dev/null`.
