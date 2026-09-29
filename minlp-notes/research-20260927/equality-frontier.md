# Singular equality certification: two limits on numerical upper bounds

Date: 2026-09-27. Status: verified boundary examples and literature audit, not a
claim of a substantial original contribution. This note investigates the
equality-certification question in
[`open-theory-challenges.md`](../literature/topics/open-theory-challenges.md).
It does not change the convex lower-bound results in
[`paper-certified-minlp`](../paper-certified-minlp/README.md).

Two obstacles must be separated. A singular optimum can disappear under
arbitrarily small perturbations, leaving a fixed gap in any upper bound based
only on uncertain function data. Even when a unique singular root is robust,
the function precision needed for a sharp objective bound can grow
exponentially with the number of variables. Sparse quadratic equations and
Jacobian corank one do not prevent the second obstacle.

The broad robustness theory and exponential polynomial error-bound exponents
are established prior results. The contribution here is a precise pair of
solver-facing examples, including an odd-multiplicity quadratic construction
that keeps root existence robust. These examples are useful safeguards for
future positive theorems, not a reason to claim that the general open problem
has been solved.

## 1. Specify what the numerical data establish

For a compact domain \(K\), equality map \(h\), and objective \(f\), write

\[
v(h)=\min\{f(z):z\in K,\ h(z)=0\}.
\]

Only nonempty feasible sets will be used below. If the available information
allows every map in a family \(\mathcal H\), an upper bound justified by this
information alone must satisfy

\[
U\ge V(\mathcal H):=\sup_{g\in\mathcal H}v(g).
\tag{1}
\]

This is an information requirement: the same reported upper bound must be
valid for every input consistent with the information. It is **not** a lower
bound on all algorithms for an exactly specified rational polynomial. Reading
an exact coefficient or proving a symbolic identity can remove the uncertainty
that defines \(\mathcal H\).

The order of quantifiers in (1) is also important. Every possible equality map
must have some sufficiently good feasible point; the point may depend on the
map. A common feasible point for all maps is not required.

## 2. A fixed upper-bound gap despite vanishing function uncertainty

Let \(K=[-1,2]\), \(f(x)=x\), and

\[
h(x)=x^2(x-1),\qquad
\mathcal H_\delta=\{g\in C(K):\|g-h\|_\infty\le\delta\}.
\]

**Proposition 1.** For \(0<\delta<2\), let \(r_\delta\in(1,2)\) be the
unique solution of \(r_\delta^2(r_\delta-1)=\delta\). Then every member of
\(\mathcal H_\delta\) has a root in \(K\), and

\[
v(h)=0,\qquad V(\mathcal H_\delta)=r_\delta,
\qquad \lim_{\delta\downarrow0}V(\mathcal H_\delta)=1.
\tag{2}
\]

**Proof.** The original roots are 0 and 1. On \([1,2]\), \(h\) is strictly
increasing from 0 to 4, so \(r_\delta\) exists uniquely and converges to 1.
For any permitted \(g\),
\(g(-1)\le-2+\delta<0\) and \(g(r_\delta)\ge0\). The intermediate
value theorem gives a root no greater than \(r_\delta\), hence
\(v(g)\le r_\delta\). Conversely \(g=h-\delta\) belongs to the family.
It is strictly negative on \([-1,1]\) and has exactly the one root
\(r_\delta\) in \((1,2]\). Thus \(v(g)=r_\delta\). ∎

Consequently, a certificate whose only premise is a uniform positive-width
enclosure about this map cannot give \(U<1\), regardless of how small that
width becomes. The original optimum is a zero of even multiplicity; a nearby
simple feasible root does not rescue convergence to the true optimum. Exact
factorization immediately certifies \(x=0\), so this example does not obstruct
symbolic or mixed symbolic/numerical certificates.

This is an explicit optimization consequence of established robust-zero
theory. It must not be presented as a new impossibility theorem for interval
computation.

## 3. Exponential precision at a robust singular quadratic root

Fix \(k\ge1\). Use variables \((y_1,\ldots,y_k,x)\in[-1,1]^{k+1}\), set
\(y_0=x\), and consider the parameterized problem

\[
\begin{aligned}
v_k(a)=\min\ &x^2\\
\text{subject to }&y_i-y_{i-1}^2=0 &&(1\le i\le k),\\
&xy_k=a.
\end{aligned}
\tag{3}
\]

Write \(D=2^k+1\), an odd integer.

**Proposition 2.** The following statements hold.

1. For every \(|a|\le1\), (3) has exactly one real feasible point. It is
   \[
   x=\operatorname{sgn}(a)|a|^{1/D},\qquad
   y_i=|a|^{2^i/D},
   \qquad v_k(a)=|a|^{2/D}.
   \tag{4}
   \]
2. At \(a=0\), the root is isolated, the equality Jacobian has rank \(k\),
   and its local Brouwer degree is \(+1\) for the displayed variable and
   equation order. In particular the root persists in every fixed
   neighborhood under sufficiently small arbitrary continuous perturbations
   of all equality components.
3. Every equality is quadratic and involves at most two variables. The
   nonzero coefficients at \(a=0\) belong to \(\{-1,1\}\). The variable
   interaction graph has treewidth at most two.
4. If the information about the last constant is exactly
   \(a\in[-\delta,\delta]\), where \(0\le\delta\le1\), and all other
   equations are known exactly, the smallest uniformly valid objective upper
   bound is
   \[
   U_k(\delta)=\delta^{2/D}.
   \tag{5}
   \]
   This minimum is taken over real-valued bounds. If a checker only accepts
   rational outputs, it is their infimum and is attained exactly when the
   displayed value is rational.
   At the actual input \(a=0\), an upper bound within \(\varepsilon\in(0,1)\)
   of the optimum therefore requires
   \[
   \delta\le\varepsilon^{D/2}.
   \tag{6}
   \]
   For a specified absolute uncertainty radius \(\delta=2^{-p}\), this is
   equivalent to
   \[
   p\ge\frac{2^k+1}{2}\log_2(1/\varepsilon).
   \tag{7}
   \]

**Proof.** The first \(k\) equations imply \(y_i=x^{2^i}\). The last is
therefore \(x^D=a\). An odd power is a bijection on the real line, proving
(4), uniqueness, and the box bounds. At the origin the first \(k\) Jacobian
rows contain an identity matrix in the \(y\) columns and the last row is
zero, proving the rank statement.

For the degree calculation, write the equality map at \(a=0\) as \(F\).
Its only real zero is the origin. A sufficiently small nonzero target
\((0,\ldots,0,a)\) has exactly the point (4) as preimage, and that point
lies in any fixed neighborhood of the origin when \(a\) is sufficiently
small. Eliminating the first \(k\) rows by a Schur complement gives

\[
\det DF(y_1,\ldots,y_k,x)=D x^{D-1}>0
\quad\text{at that preimage}.
\]

Choose a bounded neighborhood with compact boundary disjoint from zero. The
minimum boundary norm of \(F\) is positive. Invariance of degree under a
sufficiently small target translation, followed by the regular-value formula,
gives degree \(+1\). The same boundary margin and homotopy invariance prove
persistence under arbitrary sufficiently small continuous perturbations.
This is qualitative robustness; no dimension-independent margin is asserted.

The graph consists of the path
\(x-y_1-\cdots-y_k\) and the edge \(y_k-x\). For \(k\ge2\), bags
\(\{x,y_i,y_{i+1}\}\), \(1\le i<k\), form a width-two tree decomposition.
For \(k=1\), one bag \(\{x,y_1\}\) has width one. Finally (4) shows that
the supremum of the optimal values over the parameter interval is attained
at either endpoint and equals (5). Rearrangement gives (6) and (7). ∎

The exponential exponent is not caused by a zero that disappears. The root
has nonzero degree, and the parameterized problems remain uniquely feasible.
It is a conditioning obstruction for objective upper bounds. Degree,
corank, coefficient size, and graph treewidth alone do not control the needed
absolute information accuracy.

All derivatives of positive order of the equality map are independent of
\(a\). Giving a verifier those derivatives exactly does not resolve the
remaining uncertainty in the last constant. Conversely, giving it the exact
statement \(a=0\) does resolve it: the origin itself is an immediate exact
certificate. Equation (7) concerns uncertainty radius, not the mantissa size
of every possible floating-point implementation, symbolic expression length,
or a universal runtime lower bound.

Existence robustness does not mean uniqueness robustness. For example,
replace the first equation by \(y_1-x^2=-\eta\), keep all other right-hand
sides zero, and take \(0<\eta<1\). There are now three distinct real
solutions with \(x=0,\sqrt\eta,-\sqrt\eta\). The first has \(y_1=-\eta\)
and \(y_i=(-\eta)^{2^{i-1}}\) for \(i\ge2\); the other two have all
\(y_i=0\). All belong to the original box and approach the origin as
\(\eta\downarrow0\). The uniqueness in Proposition 2 is specific to
perturbing the final constant alone.

At an arbitrary nonzero actual \(a\), the error of a uniformly valid upper
bound is measured relative to \(|a|^{2/D}\), so (7) is specifically the
sharp statement at the central actual input \(a=0\). For unconstrained
two-sided point estimation, half the value range is the minimax error; that
is a different task from a certified upper bound.

## 4. Prior results and novelty assessment

The following primary sources were examined on 2026-09-27, including an
independent literature search. Local sources were read from the literature
folder; external sources were opened through their public primary pages.
The independent source audit is preserved in
[`equality-frontier-literature-audit-2026-09-27.md`](../notes/equality-frontier-literature-audit-2026-09-27.md).

| Source | Relevant established result | Consequence for this note |
|---|---|---|
| Füllner, Kirst, Stein (2021), [local summary](../literature/papers/fullner2021-convergent-upper-bounds-in-global/paper.md) and [full text](../literature/papers/fullner2021-convergent-upper-bounds-in-global/fulltext.md) | Miranda verification gives convergent upper bounds under LICQ and interior assumptions. | It does not claim a uniform certification guarantee for the singular examples above. |
| Füllner, Kirst, Otto, Rebennack (2024), [full text](../literature/papers/fullner2024-feasibility-verification-and-upper-bound/fulltext.md) | Approximate active sets extend the framework to inequalities; the authors explain rank and active-set limitations. | Merely adding inequalities or a different box test would not be a new general result. |
| Kirst et al. (2025), [full text](../literature/papers/kirst2025-on-the-use-of-restriction/fulltext.md) | Restricted right-hand-side methods address valid upper bounds under their stated regularity conditions. | The unresolved target must specify which degeneracies and uncertainty models it handles. |
| Franek, Ratschan, Zgliczynski, [Quasi-decidability of a Fragment of the First-order Theory of Real Numbers](https://arxiv.org/html/1309.6280), Theorem 6 and Lemma 8 | Nonzero degree on a subregion characterizes robust zeros in their square-system setting. A padded interval-oracle argument prevents universal termination on nonrobust inputs. | The broad robustness barrier and finite-transcript obstruction are already known. Proposition 1 is a concrete objective-value example. |
| Franek, Krčál, [Robust Satisfiability of Systems of Equations](https://arxiv.org/abs/1402.0858) | Robust satisfiability is related to sphere-extension problems, with algorithms and undecidability boundaries beyond ordinary degree tests. | A proposal to replace Miranda by general topology must compare against this stronger theory. |
| Kollár (1999), [An Effective Łojasiewicz Inequality for Real Polynomials](https://arxiv.org/html/math/9904161), Example 1 | A power chain of degree \(d\) in \(n\) variables has exact error-bound exponent \(d^n\), already on a path graph. | Exponential conditioning at fixed degree and small graph width is established. Our degree-two odd-closing variant preserves a robust real root and gives the exact objective-information formula. Its broader originality is unestablished. |
| Akoglu, Hauenstein, Szanto, [Certifying solutions to overdetermined and singular polynomial systems over Q](https://arxiv.org/html/1408.2721), introduction | A quadratic repeated-squaring chain exhibits a doubly exponentially small residual for an inconsistent system; exact rational univariate representations support certification. | Small residuals versus exact certification, and the repeated-squaring mechanism, are established. Exact rational input falls outside our uncertainty obstruction. |
| Basu, Mohammad-Nezhad (2024), [Improved effective Łojasiewicz inequality and applications](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/022BF859F5714FDA8050F6DC1992E48B), Example 2.4 and Theorem 2.11 | Effective semialgebraic error bounds and power-chain lower examples continue this literature. | Old open questions about optimal real exponents are not asserted to remain open here. |
| Mantzaflaris, Mourrain, [Deflation and Certified Isolation of Singular Zeros of Polynomial Systems](https://arxiv.org/abs/1101.3140); Li, Zhi, [Verified Error Bounds for Isolated Singular Solutions of Polynomial Systems](https://doi.org/10.1137/120902914) | Their stated verified conclusions involve appropriately perturbed systems and multiplicity information. | A perturbed-system certificate must not silently become a certificate for the original MINLP. Other exact symbolic methods can certify original systems; deflation as a whole is not ruled out. |

An unsuccessful search is not evidence of novelty. The small additional
combination in Proposition 2 is not presently a convincing basis for a
standalone research paper. The most useful outcome is to prevent an overly
broad positive claim and to make uncertainty assumptions explicit.

## 5. Verification and limits

An independent adversarial reviewer checked the algebra, local degree,
treewidth, and information interpretation. The reviewer required explicit
wording that the output is an **upper bound**, that accuracy is measured at
the actual central input \(a=0\), and that two-sided estimation has a
different factor of two. Those distinctions are included above. The parent
author independently rechecked them from (4)–(7).

A second independent adversarial reviewer checked Proposition 1, including
attainment of the worst-case value and the uncertainty-model caveat. The
reviewer found no substantive correction. That review used direct mathematical
reasoning and did not independently check the literature or computation.

A targeted exact SymPy calculation was run with `python3` through a here
document. For each \(k=1,\ldots,6\), it substituted
\(y_i=x^{2^i}\), verified the eliminated polynomial \(x^{2^k+1}\), checked
Jacobian rank \(k\) at zero, and checked the determinant identity
\((2^k+1)x^{2^k}\) on the solution curve. All six cases passed. This is an
exact finite-instance check; the proof above establishes the result for all
\(k\). No Lean proof, numerical solver benchmark, project-wide verification,
or CI check was performed or claimed.

For a durable rerun, the exact targeted command is:

```bash
python3 research-20260927/check_equality_precision.py
```

That durable command was also run and all six checks passed.

## 6. What a stronger positive contribution would need

A useful certification theorem should combine explicit structural identities
with numerical information, rather than assume that all equalities are opaque
and independently perturbable. It should report separately: an original-model
feasible point, existence of an original-model feasible point in a region,
existence for a perturbed model, and a bound that holds uniformly over specified
data uncertainty.

The examples leave a concrete possible direction: find a checkable structural
parameter that controls the objective's sensitivity to equality uncertainty.
Treewidth, polynomial degree, and Jacobian corank are insufficient. Along the
chain in (3), composition depth and vanishing order carry the missing
information. A theorem that computes useful objective-specific sensitivity
bounds for broad factorable models, without expanding an exponentially high
degree polynomial, could support adaptive precision and certified incumbent
selection. That capability remains a research target; it has not been proved
here, and practical speedup is speculative.
