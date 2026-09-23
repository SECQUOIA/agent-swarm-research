# Stage 3, round 1: independent review 5

Verdict: pass. No major or minor mathematical, coverage, or exposition issue
requiring correction was identified in this stage. This conclusion concerns
the reviewed stage 3 changes, not the deferred frontier developments or formal
consequences integration.

## Mathematical findings: none requiring correction

Read all of `sections/03-consequences.tex`,
`sections/04-hypotheses-examples.tex`, `appendices/application.tex`, and
`supplement/check_examples.py`. Checked the following boundaries explicitly.

### Closed systems, SDP objectives, and projection

The closed-system equivalence correctly uses strict feasibility through the
accepted theorem and a nonconstant convex aggregate's proper closed sublevel
set. It does not claim the generally stronger equality of the two hulls.
The three-regime statement has the correct separate dimensions for full-image
convexity and the inherited good-aggregation hull theorem; the homogeneous
strict-feasibility equivalence also handles t = 0 by openness.

The normalized multiplier slice is compact, and trace zero on PSD matrices
is the correct replacement for all matrix-coordinate objectives. Both signed
linear-coordinate objectives are needed in the stated test. The empty slice
is handled separately. No unsupported numerical zero or complexity claim is
made.

The cone C = image(PSD) + orthant has precisely the stated dual, even when
not closed. Its interior argument is correct, including the positive scaling
needed for the quadratic mixing identity. The identity's sign is correct:
minus the value at a convex combination equals the convex combination of
negative values plus the positive covariance term. Strict feasibility gives
an interior orthant point. The extrapolation z = 2x - x0 proves actual Shor
membership, not merely membership in its closure, in the whole-space case.
The nontrivial-certificate converse uses a proper sublevel set correctly.

Both nonclosed-projection examples have the exact stated endpoint behavior.
The covariance argument forces its off-diagonal entry to zero when the first
variance vanishes. In the interior, the proposed second variance realizes any
required covariance with determinant zero. In the compact variant, x1 is
bounded away from zero, so the bilinear inequalities also bound x2; the
original feasible set is indeed compact. Its SDP projection nevertheless
has the stated missing endpoint points. The comparison with the historical
closure claim therefore does not overlook original-set compactness.

### Hypotheses and counterexamples

The restricted-matrix perturbation formula has both cross terms and the
correct powers of the sweep parameter. Stable convexity yields AHC for
arbitrary lower-order coefficients. The two-form and definite-three-form
cases use the correct positive dimensions. The Schur-complement explanation
of A-block versus Q-block PDLC correctly uses a nonzero trivial certificate
and its strictly negative constant.

The AHC/HHC and HHC/stable-convexity examples verify opposite nonimplications:
the binary square-cone midpoint and the perturbation midpoint cannot have
preimages. The ordinary-HC example genuinely has a convex full image and
convex image at infinity, while every nonzero level of the selected normal
has a nonconvex image. Deleting its fourth row preserves the injective map;
the separate p,q argument gives a valid proper affine bound despite the
unbounded feasible set. Thus none of these examples inadvertently replaces
HHC by ordinary HC.

The closed-system example has the required full-dimensional interior hull:
the four displayed feasible points have independent planar directions, and
the third coordinate is free. At the origin, strict aggregate validity forces
a negative constant, while the traceless 2-by-2 block supplies another negative
eigenvalue. This proves absence of good closed-system multipliers exactly.
The strip example has the stated interval, origin exclusion, and Shor witness.
Its conclusion distinguishes existence of some bound from exact recovery.

### Application

The validity proposition requires globally active original rows and local
underestimators on the specified box. It correctly distinguishes separation
at an arbitrary expansion point from exclusion of the entire box using a
box minimizer. The first-order condition used for that minimizer is valid
even at the boundary of a possibly lower-dimensional box.

The DD LP's absolute-value lifts and lower affine-minimum lifts give the
claimed exact margin optimization over its sufficient PSD class. Zero box
widths cause no problem. The weighted-square identity proves PSD. Signed
affine equalities are correctly added exactly and normalized jointly with
inequality weights; the example of unbounded equality weights is valid.
Conditional activation requirements are retained.

The rational example's estimators are valid on the smaller box, while the
termwise root lift satisfies all the stated square and McCormick envelopes.
The convex aggregate, tangent, activation witnesses, DD feasible interval,
two margin pieces, and optimum are mutually consistent. The normalization
comparison is correct. Pure-bilinear PSD curvature vanishes by principal
minors, and the full Shor lift implies every convex aggregate and tangent.
The example is therefore not misrepresented as improving the full Shor
relaxation or proving an implemented method's performance.

## Sources, coverage, and formal boundaries

Read the stage author report, updated coverage and literature records,
bibliography, author snapshot, and coordinator closure audit. The source
inventory's stage 3 destinations are all represented. The precise AHC versus
HHC example and compact closure counterexample strengthen the original notes
without introducing unsupported priority claims. The application remains a
bounded appendix of established validity principles and exact calculations.

Checked the local primary Fujie–Kojima extraction at Conditions 1.2 and 1.4
and Theorem 2.1: the closure statement and strict-feasibility sufficient
condition support the manuscript's attribution. Checked the stable-convexity
definition in the local Sheriff extraction. The literature record documents
Polyak's source-access limitations and corroboration through BDS, rather than
claiming a fresh visual inspection that did not occur. No new broad priority
conclusion is drawn in this review. The deferred formal-consequences fragment
does not silently extend the accepted formal account to the new mathematics.

## Targeted checks actually performed

- Ran `python3 supplement/check_examples.py` from the paper directory: PASS.
- Ran a separate SymPy heredoc deriving the tangent directly from the gradient,
  deriving both box-margin pieces by endpoint substitution, and solving all
  four DD inequalities independently. It returned exactly
  `1/5 <= a <= 5/7`; all polynomial identities passed.
- The same independent heredoc checked the covariance determinant symbolically
  for both cross-entry choices, with arbitrary x,y, rather than only the
  script's finite rational witnesses.
- A Python SHA-256 comparison using the snapshot's `files` mapping checked all
  13 saved stage 3 entries: no mismatches. An initial exploratory helper looked
  for the earlier stage's differently named snapshot field and compared no
  entries; the corrected 13-file comparison is the substantive check.
- Inspected the dedicated saved LaTeX log: 17 pages, with no warnings,
  undefined-reference, or overfull/underfull matches. Did not rerun LaTeX.

No project-wide checks, CI inspection, Lean rerun, source edits, or subagents
were used. Did not read other current stage 3 reviewer reports.
