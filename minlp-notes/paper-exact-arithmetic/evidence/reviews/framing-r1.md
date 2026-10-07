# Framing and model review, round 1

Reviewed on 2026-10-05. This review covers the abstract, introduction, models,
discussion, the formal statement contracts in Sections 02–10, and the framing
and statement contracts in Appendices J/K. It also reads `main.tex`,
`macros.tex`, `evidence/BRIEF.md`, `evidence/authoring/DECISIONS.md`, the vetted
literature review, and the source coverage map. A delegated read-only
crosscheck independently examined the model/output distinctions. This is an
internal editorial and contract review, not external peer review or a fresh
audit of every proof.

The central account is coherent and useful: approximate values, points at a
fixed selector, exact predicates, and exact descriptions need different
ingredients, and the last category depends on its output format. The current
introduction makes those distinctions concrete, credits the prior numerical
and real-algebraic architecture, and does not imply an ordinary polynomial-time
sign algorithm. The technical order is sensible for a comprehensive paper:
point contracts, exact comparisons, constraints and integer search, optimizer
representation, certificate representation, then recourse. The anonymous
author field in `main.tex` is appropriate. The table of contents is useful at
this length.

The findings below distinguish false or materially ambiguous contracts from
optional editing. Files were changing during the review; observations already
repaired are recorded separately. Line numbers refer to the final read before
this report was written and should be refreshed before a repair.

## Remaining contract repairs

1. **Rational minimizer existence does not exclude irrational nonunique
   minimizers.**
   [01-models.tex:282](/workspace/minlp-notes/paper-exact-arithmetic/sections/01-models.tex:282)
   says that degree four is the first degree with irrational optimizers on a
   rational polyhedron, and that a globally convex cubic cannot have one.
   The preceding lemma proves existence of a rational minimizer. For example,
   `f(x,y)=x^2` has the irrational minimizer `(0,sqrt(2))` already at degree two.
   Replace both claims by claims about a **unique** optimizer, or about the
   selected minimum-norm optimizer. A particularly direct first sentence is:
   “Degree four is the first degree at which a globally convex rational
   polynomial on a rational polyhedron can have a unique irrational
   optimizer.”

2. **Joint-field degree lower-bounds dense common-field output, not every
   coordinatewise algebraic output.**
   [J-quadratic-contrast.tex:129](/workspace/minlp-notes/paper-exact-arithmetic/appendices/J-quadratic-contrast.tex:129)
   says that number or field degree bounds the length of “every dense
   algebraic representation.” The immediately preceding paragraph correctly
   explains the distinction: square roots of independent primes each have a
   degree-two coordinate description but their joint field has exponential
   degree. Replace this clause by: “The degree of a scalar bounds its dense
   minimal-polynomial output; the degree of a joint field bounds dense
   common-field output.” The specific lower-bound theorems identify a scalar
   of large degree and are not affected by this wording repair.

3. **Specify the operations or algebraic inputs of circuits for irrational
   coordinates.**
   [06-algebraic.tex:117](/workspace/minlp-notes/paper-exact-arithmetic/sections/06-algebraic.tex:117)
   allows a coordinate to be reported by a “shared arithmetic circuit,” and
   [06-algebraic.tex:403](/workspace/minlp-notes/paper-exact-arithmetic/sections/06-algebraic.tex:403)
   calls the cyclic irrational coordinates short circuit outputs. Section 01
   defines arithmetic circuits with rational constants and rational
   operations, so they cannot output irrational numbers. For the cyclic
   family, say “root circuit or radical expression,” and explicitly allow the
   needed real-root gate with its degree encoded in binary. Alternatively,
   describe a rational circuit acting on an explicitly represented algebraic
   input. The general singleton theorem does not assert radical solvability;
   its general output can remain an implicit polynomial system or an
   algebraic extension tower. At
   [J-quadratic-contrast.tex:132](/workspace/minlp-notes/paper-exact-arithmetic/appendices/J-quadratic-contrast.tex:132)
   and
   [J-quadratic-contrast.tex:1665](/workspace/minlp-notes/paper-exact-arithmetic/appendices/J-quadratic-contrast.tex:1665),
   identify whether the circuit represents a defining polynomial or computes
   from algebraic inputs. A rational circuit that reverses the rational shear
   is valid, but does not by itself specify the irrational starting point.

4. **The recourse exception needs its running-time qualifier.**
   [10-recourse.tex:29](/workspace/minlp-notes/paper-exact-arithmetic/sections/10-recourse.tex:29)
   says that the quartic obstruction disappears if Square Root Sum and PosSLP
   “have Las Vegas algorithms.” The model definition does not impose a time
   bound on an arbitrary Las Vegas algorithm, and exhaustive exact algorithms
   already exist. Add “with expected polynomial running time,” as the formal
   supporting remark already does.

5. **Restore two hypotheses in the abstract.**
   [abstract.tex:13](/workspace/minlp-notes/paper-exact-arithmetic/sections/abstract.tex:13)
   should say “globally strongly convex” in the exact upper-bound sentence.
   [abstract.tex:17](/workspace/minlp-notes/paper-exact-arithmetic/sections/abstract.tex:17)
   should identify the arbitrary-polyhedron UP/coUP result as one for globally
   strongly convex **quartics**; the formal constrained setting restricts both
   objective and observable to degree at most four. The preceding unary-degree
   unconstrained statement otherwise makes this look like a constrained
   theorem at general unary degree.

6. **Do not label the appendix's specialized quadratic results as imported
   external theorems.**
   [01-models.tex:615](/workspace/minlp-notes/paper-exact-arithmetic/sections/01-models.tex:615)
   lists “Exact algorithms and degree bounds for convex quadratically
   constrained problems with few constraint Hessians” in a table captioned
   “External results used in the proofs.” Appendix J proves those specialized
   span results. Replace this row by its actual imported ingredients, such as
   multihomogeneous Bezout, Hilbert irreducibility, and algebraic-number
   recognition, or distinguish external ingredients from the paper's
   consequences. This matters to the attribution of the original results.

7. **Keep the degree qualifier when describing Hesse's polynomial-time
   result.**
   [00-introduction.tex:39](/workspace/minlp-notes/paper-exact-arithmetic/sections/00-introduction.tex:39)
   and
   [00-introduction.tex:579](/workspace/minlp-notes/paper-exact-arithmetic/sections/00-introduction.tex:579)
   state the prior polynomial-time value result without an encoding/degree
   qualifier, while Section 02 explicitly identifies the imported result as
   one for unary degrees. Add the verified unary-degree premise, or the exact
   numerical-degree dependence supplied by Luna's primary-source contract.
   The abstract and the solver-consequence paragraphs now include this
   qualification.

8. **Retain the sharper meaning of the core curvature parameter.**
   [00-introduction.tex:146](/workspace/minlp-notes/paper-exact-arithmetic/sections/00-introduction.tex:146)
   says that `Lambda` bounds “the second derivatives in the core.” The actual
   product-box hypothesis is the coordinate bound
   `partial^2 f/partial v_i^2 <= Lambda`, not a bound on all mixed derivatives
   or the core Hessian norm. Say “the coordinate second derivatives in the
   core.” This accurately records the weaker proved hypothesis.

The already identified full-exponent-vector input-size repair is still visible
at [02-points.tex:573](/workspace/minlp-notes/paper-exact-arithmetic/sections/02-points.tex:573)
and [02-points.tex:619](/workspace/minlp-notes/paper-exact-arithmetic/sections/02-points.tex:619),
where `L=O(n log n)` is incompatible with printing `O(n)` full exponent
vectors in `n` variables. The proof specialists already own this repair. The
main conclusions still concern polynomial-size inputs and superpolynomial
expanded outputs; only the stated encoding accounting changes. Section 06
now explicitly counts both dense exponent vectors and the full Hessian Gram.

## Repairs observed during review

The author repaired the following after they were reported, and the final
read confirms the changes:

- Section 01 now limits uniqueness from strict convexity to convex feasible
  sets and explicitly permits several mixed-integer optima.
- Section 01 now gives the correct implication from individual coordinate
  degree to joint-field degree, while explaining that the converse need not
  give a comparable individual degree.
- The abstract and summary table now restrict the matching completeness
  language to order tests; equality remains an upper bound.
- The discussion now states polynomial-time value/point consequences for
  fixed or unary degree.
- The introduction, upper-section motivation, and discussion now avoid
  turning activity at a relaxation optimizer into a valid rule for fixing
  variables of the original MINLP. The discussion explicitly identifies the
  additional application argument that such fixing would require.
- The introduction now says that the dimension-exponential output families
  do not claim exponential growth in total input length.
- The final reread of Section 08 confirms the tower recognition repair:
  stationarity at a zero guarantees the linear-span representation
  `f=r^T S r`; rational SOS membership still requires `S` to be positive
  semidefinite. The earlier wording had conflated these steps and contradicted
  the tower counterexamples.

The high-risk distinctions otherwise survive the statement crosscheck:
Hesse's radius bounds norm rather than coordinate bits; arbitrary singleton
fields are not asserted to be radical-solvable; full Hessian Grams and
polynomial Grams are distinguished; strong convexity and domain convexity
are separate; invalid checked certificates are rejected rather than treated
as promises; candidate lists contain every optimal integer block; fixed-`t`
polynomial reductions are separated from growing-parameter FPT time;
unambiguous, deterministic PosSLP, and randomized oracle classifications
remain distinct; and recourse uses one finite rational draw with a work factor
that controls every precision. The rectangle examples concern printed
endpoint certificates and do not negate distance approximation.

## Optional editing and source follow-up

The new abstract is much tighter than the first version and retains the
central completeness result and the separate representation costs. Aim for
250–300 words if the eventual journal allows it. The two missing hypotheses
above take precedence over an arbitrary word target. The recourse formula is
useful, but the complete active-face/model inventory need not all appear in
the abstract because the introduction table supplies it.

At [00-introduction.tex:185](/workspace/minlp-notes/paper-exact-arithmetic/sections/00-introduction.tex:185),
“every natural restriction imposed” is an unnecessary broad rhetorical
claim. The following exact restrictions are more persuasive by themselves.
At [00-introduction.tex:737](/workspace/minlp-notes/paper-exact-arithmetic/sections/00-introduction.tex:737),
replace “Comparison over arbitrary polyhedra … remains open” by
“Deterministic single-instance comparison over arbitrary polyhedra … remains
open,” since the manuscript establishes unambiguous upper bounds for that
class. The title, main reading order, and output-oriented explanation do not
need structural changes.

At [09-certificates.tex:384](/workspace/minlp-notes/paper-exact-arithmetic/sections/09-certificates.tex:384),
insert “Hessian” before “Gram matrix.” The formal distinction is correct, but
this local adjective avoids momentary ambiguity. Positive definite Grams on
custom polynomial vectors in Section 09 can coexist with zeros because their
vectors may vanish; Section 01's strict-positivity consequence concerns the
full monomial vector containing `1`. An explicit basis qualification in that
model remark would make this apparent conflict easier for readers to dismiss.

Luna should confirm only the outstanding primary contracts; this review did
not search or retrieve external literature. The main request is the exact
degree/encoding premise in Hesse arXiv v1 Theorem 1.1/Corollary 1.2. For the
Balaji comparison at
[00-introduction.tex:629](/workspace/minlp-notes/paper-exact-arithmetic/sections/00-introduction.tex:629),
the vetted report says the thesis full text was unavailable and only indexed
excerpts were checked. If that remains so, describe the comparison with that
limited source basis or omit the detailed source claim. The current related
work avoids a priority claim for the sign compiler, treats Hesse's quartic
questions as version-specific, and does not claim that missing Yang text
lacks a particular exponent theorem.

Only read-only `rg`, `rg --files`, `nl`, `sed`, `head`, `pwd`, and `wc -l`
commands were used for this review, followed by writing this report. No
manuscript file was edited, no mathematical script or experiment was run, and
no build, test, project-wide verification, or CI status/log was inspected.
