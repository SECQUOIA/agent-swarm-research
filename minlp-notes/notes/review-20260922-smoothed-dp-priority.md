# Priority and significance review: smoothed exact indicator messages

Date: 2026-09-22. Independent literature and significance audit of the proposed
algorithm in [the frontier note](research-20260922-next-frontier.md). This is
not a complete independent implementation or proof review of the algorithm.

**Assessment.** The inspected primary sources do not directly imply the proposed
expected polynomial arithmetic-time construction of all exact scalar messages
on block graphs of fixed block size. This is a credible research contribution,
provided the algorithmic proof survives separate review. The strongest claim is
the explicit exact message algorithm under noise only in indicator penalties.
Neither isolation, smoothed polynomial complexity, nor conversion of suitable
approximation algorithms to smoothed exact algorithms is new in general.
The search does not establish priority.

## What needs to be compared

The candidate fixes the continuous quadratic data and support graph. It assumes
strict row diagonal dominance, bounded diagonal and linear coefficients, and
blocks of bounded size meeting at single vertices. Independent real noise with
bounded densities is added only to the indicator penalties. The conclusion is
an expected polynomial number of arithmetic, comparison, and quadratic-root
operations to build exact messages and solve the perturbed problem.

Its useful mechanism has three parts: a deterministic invariant interval for
every support problem; a smoothed bound on the complete scalar lower envelope;
and a construction whose expected work is controlled by independent child
subtrees. The last part is necessary. A small expected representation alone
does not give an algorithm for finding it.

The new statement would already cover chains of triangles, where the repository
has a worst-case hardness construction. It would also cover branching trees of
bounded-size cliques without a bound on vertex degree or volume growth. Trees
themselves are not the new tractability frontier.

## Closest indicator-quadratic results

I inspected the theorem statements and relevant proof sections, not only search
summaries.

- **Bhathena, Fattahi, Gómez, and Küçükyavuz, trees.**
  [Theorem 3.2 and Lemma 4, arXiv v1](https://arxiv.org/html/2404.08178v1)
  give an exact quadratic arithmetic-time algorithm for positive definite
  quadratic forms whose support is a tree. Their conjugate representation has
  controlled growth without noise or diagonal dominance. The candidate is
  weaker on trees and extends the graph class under additional numerical and
  probabilistic assumptions. Do not describe it as the first exact efficient
  scalar-message algorithm for indicator quadratics.

- **Bhathena, Fattahi, Gómez, and Küçükyavuz, structured graphs.**
  [Definition 5, Lemma 9, and Theorem 1, March 2026 v1](https://arxiv.org/html/2603.02103v1)
  control exact parametric dynamic programming through graph growth,
  conditioning, solution bounds, and a uniform margin condition on nearly
  optimal local supports. This is the closest algorithmic antecedent.
  The candidate replaces that deterministic support condition by a specified
  penalty-noise model on a narrower separator class. It also allows graph
  families lacking a uniform polynomial growth bound. Independent noise does
  not directly supply the paper's uniform margin assumption: its definition
  ranges over bags and local support classes, and its runtime has nonlinear
  dependence on the margin parameters. A pointwise isolation estimate cannot
  simply be inserted into Theorem 1. Their general exact pruning framework,
  rather than a claim of unrelated algorithmic invention, is the appropriate
  context. The inspected arXiv submission history lists v1 dated March 2,
  2026; I found no August revision of this particular paper.

- **Gómez, Han, and Lozano, banded matrices.**
  [Theorem 1 and Section 4.2](https://arxiv.org/html/2405.03051)
  give an additive approximation through truncated decision diagrams, with
  polynomial dependence on inverse accuracy when bandwidth and spectral
  bounds are fixed. The approximation preserves the indicator objective and
  controls errors arising in the continuous quadratic contribution. This is
  a serious antecedent for any claim about bounded-bandwidth instances.
  It does not itself return exact messages or an exact optimizer under
  penalty noise. Block graphs of bounded block size need not have bounded
  bandwidth, so the proposed graph class is not contained in its hypothesis.

- **Choi, Fattahi, Gómez, Han, and Lozano, August 2026.**
  [Theorem 4 and Section 8](https://arxiv.org/html/2608.22815v1)
  bound approximate decision diagrams using volume growth, boundary growth,
  and spectral decay; they allow sparsity of either the Hessian or its inverse.
  Their result is broader in some structural directions and concerns
  approximation. It does not assert the candidate's exact smoothed message
  bound. This August paper has a different author list from the March paper.

## The strongest general smoothed-complexity antecedent

The first audit found a distinction that is valid for an old theorem but is
**not valid for the later literature as a whole**. It must not be used to
inflate the contribution.

[Beier and Vöcking, STOC 2004 version, Theorem 3 and Sections 1.3–1.4](https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/BeierV.pdf)
characterize a weaker smoothed-polynomial notion through randomized
pseudopolynomial optimization. That notion does not by itself bound the first
moment of running time. Their paper explicitly distinguishes it from expected
polynomial time. The coordinate-class isolation argument is also established
there; the local envelope review already attributes it appropriately.

However, [Röglin and Teng, FOCS 2009, Theorem 6.2 and Section 6.2](https://www.roeglin.org/publications/FOCS09.pdf)
**do prove the expected-time version** for binary optimization with a perturbed
linear objective and a randomized pseudopolynomial algorithm. Their method uses
higher winner gaps and several best rounded solutions. Thus the simple
observation that an inverse-gap runtime can have a bad expectation is not a
general novelty argument. The theorem specifies a bit-revelation model and
also discusses discretization. The proposed arithmetic model is different.

[Dughmi and Roughgarden, Proposition II.3 and its footnote](https://www.math.uwaterloo.ca/~cswamy/courses/co759/agt-material/blackbox.pdf)
explicitly state the corresponding black-box conversion from an FPTAS for a
linear binary maximization problem of polynomial dimension to an exact
algorithm with expected polynomial smoothed running time. Their route converts
the FPTAS to a pseudopolynomial exact algorithm and invokes the preceding
theory. Consequently, a bare claim that noise turns an FPTAS into an exact
efficient algorithm would have substantial established precedent.

There is nevertheless a real missing hypothesis when applying these theorems
to the indicator problem. Eliminating the continuous variables gives

```
min_z g(z) + (lambda + xi)^T z,
g(z) = -1/4 c_S^T Q_SS^(-1) c_S,   S={i:z_i=1}.
```

The deterministic support cost `g` is nonlinear and is generally neither an
integer nor an additive function of the bits. Encoding the penalties in unary
does not make this an integer-valued linear-objective problem. In fact the
repository's [unit-penalty hardness construction](../results/indicator-quadratic-treewidth-two-hardness.md)
already has every penalty equal to one, while precise rational continuous data
retain the hardness. Therefore the required pseudopolynomial oracle in the
randomized coefficients has not been supplied. An additive approximation
scheme for this problem cannot be converted to that oracle merely by choosing
accuracy below one half: distinct support values need not differ by an integer.

[Röglin and Vöcking, Section 6.1](https://www.roeglin.org/publications/IPCO05.pdf)
does discuss arbitrary nonlinear adversarial objectives, but in the extension
where linear constraints are perturbed. That statement does not remove this
objective-perturbation mismatch.

This is a failure of a proposed immediate deduction, not proof that the general
smoothed machinery cannot be extended. A higher-gap argument for
`g(z)+xi^T z`, combined with an approximation oracle under fixed-bit
restrictions and a method for finding several nearly best supports, may give
an alternative exact smoothed algorithm. That possibility deserves a separate
investigation. It could reduce the novelty of a one-optimizer conclusion on
bounded-bandwidth graphs. It would not automatically construct all exact
continuous messages, and its graph assumptions would still require checking.

## Pareto and parametric-envelope comparisons

[Beier, Röglin, Rösner, and Vöcking, Theorem 1](https://link.springer.com/article/10.1007/s10107-022-01885-6)
allow one arbitrary deterministic objective and one independent random linear
objective, proving polynomial expected Pareto-set size with explicit density
and expected-magnitude dependence. This already covers important affine
parametric special cases. The candidate's quadratic branch family has varying
curvature, slope, and deterministic intercept. It does not reduce directly to
two fixed objective values with nonnegative scalar weights. A small Pareto set
would also need an enumeration algorithm before it implied the desired DP
runtime.

[Moitra and O'Donnell, Section 2](https://www.cs.cmu.edu/~odonnell/papers/pareto-optima.pdf)
allow several independently perturbed linear objectives and one arbitrary
deterministic objective. The higher-moment literature is relevant to runtime
analysis. One must not treat several deterministic quadratic coefficients as
if all their objective directions had independent perturbations. Noise in the
indicator penalty is only one random linear support objective.

[Applegate et al., Section 6 of the full preprint](https://arxiv.org/html/1805.06420)
provide a direct antecedent in smoothed parametric shortest-path complexity.
Their parameter dependence is affine and their smoothing rotates objective
directions. The inspected result does not state a penalty-only theorem for
arbitrary Lipschitz support costs. The candidate should still acknowledge
smoothed lower-envelope analysis as an established research approach.

## Significance and limits

The plausible substantive contribution is an explicit expected polynomial
algorithm for an exact continuous-discrete problem on a meaningful graph class
containing worst-case hard instances. Its structural insight is that independent
penalty noise controls all scalar support switches, while independent branches
control the expected Cartesian-product work. This is more useful than merely
showing that a typical final optimizer is isolated.

The model is restricted in important ways. It perturbs every indicator capable
of distinguishing competing supports. It fixes the quadratic data before
drawing that noise. A common random shift of all penalties, or randomizing
continuous linear coefficients instead, does not satisfy the same proof.
The graph is a tree of small blocks with one-vertex intersections, not an
arbitrary bounded-treewidth graph. Strong diagonal dominance supplies an
invariant domain; conditioning alone was not shown to replace it.

The algorithm solves the perturbed instance. If deliberately added noise obeys
`|xi_i|<=epsilon`, its output has original objective at most `2n epsilon`
above the original optimum, by comparing the two support penalty sums.
This elementary error estimate is not an exact guarantee for the original
instance. It is a possible route to an approximation algorithm, not evidence
that the original hard problem has become tractable.

An arithmetic-operation theorem under arbitrary continuous noise is not a
finite-input Turing-time theorem. Exact noise samples and comparisons are
idealized. Finite-grid noise, certified root comparisons, and precision costs
need their own analysis. Practical speedup, useful perturbation scales, and
stability of selected supports remain untested.

### Subsequent finite-precision candidate

After this audit, the coordinator supplied a candidate extension using
independent uniform noise on an `N`-point grid, with `N>=4n 2^n`.
Its proposed envelope estimate adds an atom term of order `m 2^m/N`.
Thus a grid with `O(n+log n)` bits per noise coefficient could suffice.
Together with rational Schur-complement coefficients and comparisons of
degree-two algebraic breakpoints, this could strengthen the conclusion to
expected polynomial bit complexity. This extension is undergoing a separate
fresh review; this note does not certify it.

Finite-precision smoothing itself is established: Röglin and Teng's inspected
Section 6.2 explicitly discusses rounding after polynomially many bits as an
alternative to bit-revelation oracles. The potential addition here is a
concrete sufficient precision and a complete expected bit-work proof for the
nonlinear indicator-message algorithm. Merely citing a continuous density
bound would be insufficient for that claim, because discrete grid noise has
atoms. If verified, the extension should replace the arithmetic-only limit in
the final theorem, while retaining the perturbation and graph limitations.

## Verification and search record

The audit inspected the primary sources linked above, including the strongest
expected-time characterization and the explicit FPTAS corollary. Searches also
used combinations of “smoothed,” “indicator quadratic,” “dynamic programming,”
“block graphs,” “winner gap,” and “nonlinear objective.” No exact matching
theorem was found. This is not an exhaustive priority search.

I checked the scope of the reductions and the penalty perturbation comparison
symbolically. I did not run computational experiments, Lean, project-wide
verification, or CI checks. The algorithm needs its separate proof review;
this audit establishes only the source comparisons and qualified significance
assessment above.
