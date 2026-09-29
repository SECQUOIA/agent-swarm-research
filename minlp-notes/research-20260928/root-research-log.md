# Root research and verification log

Date: 2026-09-28. The user renewed the broad research instruction and asked
for continuous work. This continuation does not reopen the previous closing
scope without that renewed authorization.

## Direction selection and current assessment

The initial survey read the repository overview, September 27 closing record,
recent exact-quartic and Hessian-span results, sparse-indicator manuscript
overview, and local literature instructions. Parallel investigators screened
structural relaxations, solver theory, applications, arithmetic, submodularity,
and certificates. The sparse kernel theorem and its fixed quadratic lower
bound currently offer the clearest combination of a precise improvement over
an inspected prior theorem and matching sharpness. Further work is active.

The root independently reconstructed the kernel positivity, local density
and separator consistency argument, moment bounds, and objective estimate.
The root then read the completed finite-quadrature and Slater consequences
and the independent review. The corrected dynamic-programming bound
`O(t N^w)` accounts for child-message aggregation; the table-count bound
alone does not account for that work. This was rechecked without repeating
the author's completed kernel tests.

The root authored the fixed quadratic sharpness proof, including an explicit
high-frequency Fejer signed-measure witness. A fresh reviewer independently
checked the Fourier signs, Jordan normalization, constants, hierarchy
direction, and dense certificate, finding no defect. The independent
coefficient calculation gives `A=10` for the stated affine-transformed
two-bag split. The root independently recomputed it as `4+6=10`, so the
companion upper bound is at most `60/r^2`.

The root read Korda--Magron--Rios-Zertuche's published Theorem 6 and Lemma 10
in the local primary-source extraction. Their degree convention is
coordinatewise; converting to total degree changes width factors, not the
exponent comparison. Their proof first constructs positive polynomial bag
pieces. The current primal rounding proof avoids that step. Independent
source review subsequently found that a rational-separator counterexample
was already Nie--Qu--Tang--Zhang Example 6.7; the source audit now credits
that rediscovery. The sharp quadratic is distinct in degree and in its
quantitative separator-approximation bound; priority is still under audit.

The root also reconstructed the graph-rounding trichotomy, the positive
mass-floor lower bound, the closed-walk apportionment upper bounds, and
the stable diagonal-filter identities from the applications note. No gap
was found. These results have an independent proof review and a bounded
primary-source comparison; the root assessment is a focused theoretical
contribution, not an established broad solver improvement.

The deterministic-to-law repair theorem was read in full. Its tree coupling,
finite-net projection, Dirac converse, cycle counterexample, and terminal
repeated-square obstruction are consistent. Its novelty assessment remains
modest because the transport and error-bound ingredients are classical.

The root read the complete adaptive integer-sign compiler proof and
independently checked the scale recurrence, integer margin, error induction,
and positive-denominator DAG representation. Fresh cross-branch proof and
primary-source reviews are still active because generic adaptive closure
is a stronger complexity claim than its elementary numerical ingredients
might suggest. No current-open-problem claim is justified by an old source's
historical statement. Targeted formal verification is being considered for
the algebraic lemmas, not for the entire compiler theorem.

That fresh review subsequently passed. The deeper audit located the older
extended-basis sign-gate model and verified that a problem-specific
SQRT-SUM many-one reduction already follows from prior PPS results. The
root made binary fan-in and total circuit size explicit; the height bound
was rechecked under these conventions. Local Lean verification now covers
26 named theorems, with a 53-declaration axiom audit. The coverage record
excludes the full compiler, interpreter, size bound, and complexity
conclusion. A separate reference implementation constructs the shared DAG
and distinguishes exact full-schedule tests from reduced diagnostic tests.
These agent-run commands were not redundantly rerun by the root.

The root read the complete ordinary-module kernel draft. Its SOS geometric
normalization, one-generator product inequalities, normalized separator
domination, total-variation repair, and objective normalization identity
were reconstructed independently. The important degree condition is
`R>=wD`, ensuring the combined coefficient-error polynomial has degree
at most `R`. No claim that every intermediate factor in its algebraic
decomposition has that degree is needed. Fresh proof and source reviews
were still underway at this audit point.

The next substantive direction was derived by the root and delegated for
development and review: affine shared-dependent private constraints can
change the sharp exponent from two to one. The proposed lower example has
cost `-xy+z`, with `z>=y,z>=-y`; its separator value is `|y|`.
The proposed upper theorem combines shared-kernel smoothing, conditional
source means, and uniform Hoffman repair under complete recourse. This is
ongoing work, not yet covered by the earlier reviews.

A substantive later literature correction narrowed the leading novelty
assessment. The dedicated Putinar auditor and a separate reader inspected
rendered author slides from July 2025 and February 2026 that explicitly
state the inverse-square two-bag sparse preordering rate. This is an
earlier public assertion, despite its unexplained difference from the
published theorem. The root updated the main note and both indexes and
informed the user. Novelty of the rate itself is no longer asserted. The
fixed quadratic sharpness result, constructive rounding details, ordinary
quadratic-module extension, and constrained-recourse results each need
their own comparison; none inherits novelty from the paper's weaker bound.

The affine-recourse upper and lower notes subsequently passed independent
proof reviews. The root read both completed arguments and reconstructed
the source-mean feasibility, one-degree reserve, squared transport identity,
uniform Hoffman projection, quadrature requirement, Fourier lower witness,
and degree-three dense and branch certificates. No substantive gap was
found. The lower bound uses actual local measures and therefore applies
also to the rectangular shared-degree/private-degree hierarchy. That
hierarchy's inverse-order upper bound is a separate theorem, not a
consequence of the full-preordering example's upper certificate.

The root also reconstructed the exact-consistency ordinary-module
strengthening. The weighted Cauchy--Schwarz calculation needs the full
moment order: its largest degree is `(v+j)D<=2R`, whereas the coefficient
moment estimates use degree at most `R`. Adding the same constant density
in every bag preserves exact separator consistency. The final choice
`N=2ceil(max(3/2,(w+1)/4)log2(s))` makes the correction lower order without
an extra bag-count factor. The author and independent reviewers completed
targeted exact checks; a further fresh root-requested adversarial audit is
underway. Conservative finite-order constants preclude an immediate
computational-speedup claim.

The current research emphasis has shifted accordingly: the ordinary-module
transfer and sharp recourse boundary are stronger candidates than claiming
a new full-preordering exponent. New investigations consider general hard
constraints and active-region branching. Rational certificate construction
is retained as a useful consequence of established methods, with its
expanded-SDP complexity and slack promise stated explicitly.

## Targeted command actually run by the root

```
python3 -B research-20260928/solver/check_quadratic_sharpness.py
```

Result: PASS. The checker verifies the quadratic and dense preordering
identities, nine independently integrated odd Fourier coefficients, 128
exact rational lower-bound cases, and sixteen independent Fourier
convolutions. The all-degree proof, measure duality, and asymptotic claims
remain mathematical arguments; this finite check does not establish them
or publication priority.

An earlier inline SymPy exploration integrated the first six odd Chebyshev
coefficients of the truncated quadratic. Those values motivated, but did
not replace, the general product-to-sum derivation and retained checker.

Each agent's other targeted commands are recorded in its topic's verification
or review note. They are not represented as commands rerun by the root.
No project-wide verification or CI status/log inspection was performed.

## Final scope and completed checks

The user subsequently required completion of the current ideas and no new
directions. The continuation is closed at that scope. The
[closing record](closing-research-results.md) is the final synthesis; earlier
entries above preserve the chronology and are not current assignments.

The final ordinary-module audit passed. The root read it and independently
rechecked the common-shift identity, full-order weighted Cauchy--Schwarz,
smaller normalization parameter, and finite dual-attainment argument. The
root also read the rational-certificate construction, including its known
ellipsoid radii, rational separation, coefficient right inverse, and the
corrected denominator bound. Those are complete scoped consequences, not
claims of practical numerical conditioning.

The two last mathematical branches are complete. For regular affine
recourse, the root independently derived the projected-multiplier KKT
inequality, the Chebyshev multiplier-difference estimate, and the scalar
commutator bound. An initial total-degree shortcut would have been
insufficient: the commutator can have degree greater than `r`. The final
proof instead uses the certificate for `1+-T_alpha` when
`sum ceil(alpha_i/2)<=r`. The root and a fresh reviewer independently
rechecked this repair. Both stated regularity variants and the sharp
regular example passed their proof review and targeted exact checks.

For polynomial constraints, the root read the completed proof and fresh
review, independently reconstructing conditional violation control,
the `2/s` squared-Fejer displacement estimate, the degree-preserving
ordinary-module certificate for polynomial differences, and the product
mass estimate. These justify the sharpened ordinary rate
`O((log R/R)^alpha)`. The global geometric bound and primal-only scope
remain explicit. The source comparison distinguishes this logarithmic
refinement from the weaker bound obtained by composing earlier lifting
and box theorems.

A documentation audit identified a missing fresh noncontributor review
of the full joint Hessian-Gram refinement in binary extraction. That
review is now complete, including exact symbolic and rational matrix
checks, with no mathematical correction needed. The main note and prior
review link it. The root also read the curvature atlas and disjoint-well
proofs and their existing reviews; the bounded literature comparison was
completed separately without adding a new theorem.

Older summaries now credit the July 2025 and February 2026 sparse-rate
slides. The Guo--Wang matrix-Jensen reference is corrected to Proposition
27, with Theorem 29 reserved for convergence. The private-block,
finite-state, ordinary-module, affine-recourse, and exact finite-order
notes link their completed reviews. Important modest and negative results
are reachable from the continuation index and closing record.

The final scope audit also found one subsidiary three-variable submodularity
counterexample whose original note still requested independent review.
The auditor checked its exact minors, stationarity equations, feasible
minimizers, values, and defect by hand. The root independently rechecked
the full stationary point, determinant `2117/100`, and submodularity defect
`-7/116`; the review is now recorded in that note. The closing synthesis
also distinguishes the quadratic example's order-one truncated moment
witness from its order-two actual local measures. These were completion
and presentation corrections within the existing work.

Agent-run verification commands and their exact coverage are retained in
each verification or review note. The root did not redundantly rerun
completed numerical, symbolic, or Lean checks. The new checks concern the
already active results, not new research directions. Unresolved broader
questions are exclusions from the completed claims; no proof or review
task remains assigned after closure.

Final documentation commands actually run by the root:

```text
python3 - [inline pathlib/re scan of the 18 root-edited Markdown files]
git diff --check -- README.md
```

Both passed. The inline scan checked final newlines, trailing whitespace,
and 392 local file links in the specified files; external URLs and
renderer-specific anchors were not checked. The `git diff` check covers
the tracked root README only. The inline scan explicitly included the
new untracked topic files, which a normal `git diff --check` would omit.
These are documentation checks, not mathematical verification. The
separate [closure audit](closure-audit.md) records its own path and status
checks and the corrections they prompted.
