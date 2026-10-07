# Prior-art check: a sharp random-tilt tail for global quadratic growth

Date: 2026-10-02. This is a focused comparison, not a completeness or
novelty claim. The mathematical statement and its proximal proof are in
[the accompanying note](../new-direction/proximal-growth-tail.md); this audit
asks whether those results already appear in prior work.

## Candidate statement

For any continuous \(f\) on a nonempty compact set
\(X\subset\mathbb R^n\), let
\(w_i=\max_X x_i-\min_X x_i\). Add independent linear objective
coefficients \(c_i\) with densities bounded by \(\phi_i\). Let \(g_*(c)\)
be the largest global quadratic-growth modulus when the optimizer is unique,
and set it to zero when distinct optimizers exist,
then

\[
 \Pr\{g_*(c)<\varepsilon\}\le
 2\varepsilon\sum_i\phi_iw_i.
\]

The constant is sharp already for a two-point one-dimensional feasible
set. The proof uses the proximal map of a convex conjugate of
\(x\mapsto f(x)-c^Tx-\varepsilon\|x\|^2\), the area formula on the
preimage of the conjugate's nondifferentiability set, and a trace/divergence
bound integrated against the coordinatewise perturbation densities. The
argument does not require convexity or definability of \(f\) or \(X\).

## Closest quantitative predecessor: discrete winner-gap isolation

Beier and Vöcking, [“Typical Properties of Winners and Losers in Discrete
Optimization”](https://doi.org/10.1145/1007352.1007409), *Proceedings of the
36th ACM Symposium on Theory of Computing* (STOC 2004), Lemma 5, prove that
for a fixed feasible set
\(S\subseteq\{0,1\}^n\) and independent continuous linear-objective
coefficients with density bounds \(\phi_i\), the density of the gap between
the best and second-best feasible solutions is at most
\(2\sum_i\phi_i\). They state that this density bound is tight. This is the
closest quantitative comparison: it has the same sharp factor and the same
sum of coordinate density bounds, with unit coordinate widths.

The measured quantity is different. Their gap compares only the best and
second-best *values* in a finite binary feasible set. It does not divide a
value gap by squared distance, does not control the objective throughout a
continuous feasible set, and does not allow an arbitrary continuous fixed
base objective \(f\). A winner-gap bound alone can lose a factor equal to
the squared diameter when converted to a global quadratic-growth bound.
Thus Lemma 5 is strong prior art for isolation of discrete objective values,
but it does not state the candidate theorem.

## Qualitative a.e. growth from Alexandrov's theorem

There is a classical route to the qualitative conclusion for arbitrary
continuous data, without a semialgebraic assumption. Define the convex
conjugate-like support function

\[
 h(c)=\max_{x\in X}\{c^Tx-f(x)\}.
\]

Because \(X\) is compact and \(f\) is continuous, \(h\) is finite and
convex on \(\mathbb R^n\). Alexandrov's theorem says that a finite convex
function has a second-order Taylor expansion at almost every point; see
Theorem 1.1 in Azagra, Cappello, and Hajłasz,
[“A geometric approach to second-order differentiability of convex
functions”](https://arxiv.org/abs/2303.06265). At such a point \(c\),
\(h\) is differentiable, so its maximizer \(x^*\) is unique. The local
quadratic upper expansion of \(h\), combined with
\(h(c+d)\ge (c+d)^Ty-f(y)\) for every \(y\in X\), gives a local
quadratic lower bound for \(f(y)-c^Ty-(f(x^*)-c^Tx^*)\): take \(d\) to be
a sufficiently small fixed multiple of \(y-x^*\). Compactness and
uniqueness then extend that local bound to a positive global quadratic
growth modulus. This is a direct corollary of Alexandrov's theorem and
convex duality, not a theorem explicitly stated in the cited paper.

Thus any absolutely continuous random linear tilt has, almost surely, a
unique global minimizer and some positive global quadratic-growth
constant, even for arbitrary continuous \(f\) on compact \(X\). This
qualitative conclusion gives no explicit tail or useful lower bound on the
modulus. The candidate theorem strengthens it with a sharp quantitative
probability estimate in terms of coordinate widths and coefficient
densities.

## Other qualitative predecessors: generic quadratic growth

Lee and Phạm, [“Stability and Genericity for Semi-Algebraic Compact
Programs”](https://doi.org/10.1007/s10957-016-0910-5), *Journal of
Optimization Theory and Applications* 169(2) (2016), Theorem 6.1, establish
that almost every objective perturbation in their polynomial
semi-algebraic class has a unique global minimizer with some positive global
quadratic-growth constant. Their paper includes a fixed polynomial objective
plus a linear perturbation. Lee and Phạm, [“Generic Properties for
Semialgebraic Programs”](https://doi.org/10.1137/16M1068992), *SIAM Journal
on Optimization* 27(3) (2017), Theorem A, give a related generic result for
regular closed semialgebraic feasible sets. These establish the qualitative
genericity phenomenon, but no explicit probability tail or density/width/
failure-probability dependence. They require semialgebraic structure, while
the candidate statement is for arbitrary continuous data on compact sets.

Drusvyatskiy and Lewis, [“Tilt Stability, Uniform Quadratic Growth, and
Strong Metric Regularity of the Subdifferential”](https://optimization-online.org/wp-content/uploads/2012/05/3459.pdf),
*SIAM Journal on Optimization* 23 (2013), 256–267, give deterministic local
equivalences between tilt stability, uniform local quadratic growth, and
strong metric regularity. This supplies local sensitivity background, not a
random-tilt distributional bound or global compact-domain theorem.

## Proximal and measure-theoretic ingredients

The candidate proof uses standard proximal facts for finite convex
functions: the proximal map is firmly nonexpansive, is the gradient of a
convex continuously differentiable potential, and has symmetric Jacobian
with eigenvalues in \([0,1]\) almost everywhere. It also uses the Lipschitz
area formula. The proof's particular inference is that the preimage of the
convex conjugate's nondifferentiability set has zero proximal Jacobian
determinant, so the indicator of bad growth is bounded by the trace of the
proximal residual Jacobian. Integrating that trace costs only
\(2\varepsilon\sum_i\phi_iw_i\), with no dimension logarithm.

The focused search found no prior theorem packaging these standard facts
into this sharp, global random-growth tail for arbitrary compact feasible
sets and continuous base objectives. This is a scoped negative result, not
evidence that the combination is new. It is safer to describe the result as
a quantitative strengthening of known genericity and winner-gap isolation,
subject to a broader search, than to claim a new isolation principle.

## Sources and comparison boundary

- Beier and Vöcking (2004), Lemma 5 and Theorem 1; the local full-text
  extraction was checked. The lemma is about the top-two score gap over a
  fixed binary feasible set. Their separate 2006 journal-version record
  (DOI [10.1137/S0097539705447268](https://doi.org/10.1137/S0097539705447268))
  is metadata-only in the KB and was not used to support claims here.
- Lee and Phạm (2016), Theorem 6.1; author-hosted full text and the existing
  project audit were checked. The result is qualitative genericity for
  semialgebraic polynomial programs.
- Lee and Phạm (2017), Theorem A; author-hosted full text and the existing
  project audit were checked. The result is qualitative and assumes a
  regular closed semialgebraic feasible set.
- Drusvyatskiy and Lewis (2013); author-hosted full text and the existing
  project audit were checked. The result is local deterministic stability.
- Azagra, Cappello, and Hajłasz (2023), Theorem 1.1; arXiv HTML full text
  checked. The theorem is Alexandrov's a.e. second-order differentiability
  result for convex functions. The arbitrary-compact-set, a.e. global-QG
  conclusion above is our deduction from that theorem and convex duality,
  not a result they state.

Targeted terminology searches included “random linear perturbation
quadratic growth,” “continuous isolation lemma,” “quantitative strong
exposure,” “proximal mapping area formula,” “convex conjugate random tilt,”
and “global quadratic growth random objective.” They returned the sources
above and standard proximal/genericity material, but no direct match for the
candidate tail. This check did not search every adjacent field or every
equivalent formulation.
