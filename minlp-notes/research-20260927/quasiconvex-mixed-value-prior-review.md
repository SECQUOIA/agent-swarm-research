# Review of the quasiconvex mixed-integer prior-results note

Date: 2026-09-28. Scope: an independent, focused check of
[the prior-results note](quasiconvex-mixed-value-prior.md), limited to
Hildebrand--Köppe, Espinoza--Fukasawa--Goycoolea, the boundary example,
and the stated Westerlund--Pörn assumptions. No substantive correction
is required within this scope. This review does not establish novelty.

1. **The pure-integer distinction is correct.** Equation (1) of
   [Hildebrand--Köppe](https://arxiv.org/pdf/1006.4661) requires all
   coordinates to be integral and uses an integer-coefficient polynomial
   objective. Theorem 1.1(b), p. 2, explicitly gives output complexity
   \(l d^{O(n)}\), independent of the number of constraints. The proof on
   p. 25 invokes a bounded-size ball containing a minimizer when one exists,
   bounds its objective value, and refers to Heinz's Theorem 5.1. A nonempty
   set of integer objective values with finite infimum has a minimum, so
   this theorem does not directly address a free real, unattained value.

2. **The fractional predecessor is represented accurately.**
   [Espinoza--Fukasawa--Goycoolea](https://mgoycool.github.io/papers/10espinoza_orl.pdf),
   Theorem 2.3(5), p. 2, gives a point or ray certificate when the algorithm
   reaches its finite-value exit. The p. 3 termination statement has the
   finite-oracle-output condition recorded in the note. Section 5,
   pp. 5--6, handles denominator signs and asymptotic values. The rational
   mixed-integer hull gives rationality: validity of the relevant affine
   inequality on that hull reduces to finitely many rational linear
   conditions on the scalar parameter. This is a mathematical consequence,
   not a quantitative theorem quoted from the paper. A coefficient-size
   bound still needs a separate quantitative argument.

   The continuous domain must include the positive-denominator
   restriction: positivity only on mixed-integer feasible points need not
   imply positivity throughout the relaxation. The note now states this
   restriction explicitly. The restricted strict sublevels and their
   projections are convex.

3. **The boundary example is correct.** For
   \(E=(\mathbb R^k\times(0,\infty))\cup(S\times\{0\})\), upward closure
   follows directly. The strict projected level is empty for
   \(\tau\le0\), and is \(\mathbb R^k\) for \(\tau>0\). The lattice
   point \(0\) with arbitrary positive threshold proves the infimum is
   zero; zero is attained precisely when \(S\) contains a lattice point.
   Thus arbitrary boundary feasibility is compatible with convex strict
   levels. The note correctly refrains from treating this as a
   counterexample to a value bound. Its proposed additional boundary
   hypotheses remain conditions to investigate, not a proved sufficiency
   claim.

4. **The bounded-domain comparison is supported.** The local full text of
   [Westerlund--Pörn](https://users.abo.fi/twesterl/some-selected-papers/40.%20OPTE-TW-RP-2002.pdf),
   printed pp. 255--256, states differentiable pseudoconvex functions,
   compact \(X\), finite bounded integer domain \(Y\), and nonempty
   feasibility. Printed p. 258 expressly uses compactness and finiteness
   in its convergence discussion.

Verification used `cat research-20260927/quasiconvex-mixed-value-prior.md`,
targeted `rg -n` searches and `sed -n` excerpts of the local
Hildebrand--Köppe and Westerlund--Pörn source texts, and the linked
Hildebrand--Köppe and Espinoza et al. primary PDFs. The boundary example
was checked directly. The targeted command
`git diff --check -- research-20260927/quasiconvex-mixed-value-prior-review.md`
returned success; the newly created file was also read back. No
project-wide verification or CI inspection was performed. The main note
was not edited.
