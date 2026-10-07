# Recourse writer handoff

Date: 2026-10-05. Sol continuation of the Opus recourse draft after its
authoring turn was interrupted. Only the authorized recourse files were
changed. No research source, other manuscript section, experiment, CI
record, or git history was changed.

## Completed files

- `sections/06-recourse.tex`: preserved the substantial Opus draft;
  corrected the conditional-matrix row condition from
  `epsilon_bj <= 1-tau` to `epsilon_bj <= tau`, which matches its text
  and degree proof; stated objective membership in the duality proposition;
  added the fixed-grid comparison with every feasible moment family and
  its full quadrature/degree proof; reformatted the grid baseline display.
- `sections/07-regularity.tex`: completed both regularity theorems, their
  proofs, examples, and the qualified parametric-QP comparison.
- `appendices/B-recourse.tex`: supplied the missing full proof that
  omitting private quadratic bounds permits all-order unboundedness.
- `evidence/WRITER-RECOURSE.md`: this record.

Public labels required by the architecture are present: `thm:fixed-recourse`,
`prop:private-bounds-needed`, `prop:convexity-needed`,
`thm:affine-recourse`, `thm:affine-sharp`, `prop:rec-dual`,
`lem:half-degree`, `thm:reg-cheb`, `thm:reg-holder`, `ex:reg-sharp`,
and `ex:strict-convex-insufficient`. New supporting labels include
`cor:rec-grid` and `prop:reg-qp`.

## Mathematical reconstruction and scope

The fixed and affine arguments use the rectangular polynomial space:
shared total degree at most `2r`, private total degree at most two.
The mixed-moment estimate requires objective shared degree `d <= r`.
Fixed fibers use `m=floor(r/w)+1`; affine and regular fibers use
`m=floor((r-1)/w)+1=ceil(r/w)`. The latter gives kernel square degree
at most `r-1-|I|` and covers every shared-dependent row localizer.
The corrected conditional-matrix condition is exactly
`tau >= epsilon_bj`, as its proof requires.

The order-unit proof retains the full polynomial-summation quotient,
the separator equations through `2r`, private quadratic bounds, and
nonempty primal feasibility. It proves compact attained moment minima,
equality with the certificate supremum, and finite real certificates at
every strict level. It asserts neither closedness of the sparse Gram image
nor attainment at the optimal certificate level. The existing direct weak
separation proof for strict levels is valid for a convex cone with nonempty
interior; it does not require that cone to be closed.

The omitted-bound appendix proves scalar shared-preordering closedness
by integration bounds on PSD Gram traces, nonmembership of the homogeneous
Motzkin polynomial by its leading cubic SOS obstruction, and normalized
separation. Moment Cauchy--Schwarz plus monomial bounds make the separating
mass positive already at `r>=3`. Thus the manuscript's stronger range
`r>=3` is justified, although the original main source used `r>=6`.
This does not change the rate theorem's assumption `r>=d=6` for that
objective. The convexity counterexample has an unused shared coordinate,
so its formal model respects the standing convention `w>=1`.

The regularity proof explicitly establishes pointwise KKT existence for
polyhedral fibers and verifies the positive correction
`a^dual(u)^T(U(u)-u h(u))`. It integrates only the regular bounded
projection, without assuming a regular or measurable full-multiplier
selection. The commutator has total degree at most `2r-1`, and every
frequency satisfies `sum_i ceil(alpha_i/2)<=r`. The half-degree lemma
supplies its actual truncated preordering certificate, including odd
frequencies. The adjacent multiplier estimate covers modes just outside
kernel support; in particular `alpha_i=2m-1` can contribute.

For coordinatewise Holder projections, each commutator summand has degree
at most `2m-1`. Its uniform bound transfers to the functional through an
interval certificate of degree `2m<=2r`. Concavity gives exponent
`1+beta`, including `beta=1`; no arbitrary multivariate Lipschitz theorem
or sharpness for intermediate Holder exponents is claimed. A continuous
regularized private optimizer converges to the minimum-norm optimizer,
providing a Borel optimal policy independently of the exhibited KKT pairs.

The regular sharp example uses the separator measures for `x_+^2` from
Section 5 with new private lifts `v=z=x_+`. Both affine sharpness cones
are stated and bounded separately. Their shared actual-measure witnesses
do not imply cone inclusion. The QP sensitivity proposition has a full
finite-active-set proof, assumes LICQ on an open feasible neighborhood
of the closed box, and yields the automatic regularity corollary only
for scalar shared bags. Strict convexity alone remains insufficient.

## Sources and literature dependencies

Read the project instructions, manuscript brief and architecture,
`AUDIT-RECOURSE.md`, the accepted independent recourse-duality review,
Sections 2--4 and the relevant Section 5 witness, the four assigned source
notes, and their supplied proof reviews and prior-work notes. Literature
comparison uses only those supplied notes and `LITERATURE-PRELIMINARY.md`.
No web search, primary-paper retrieval, or literature-KB maintenance was
performed.

Canonical citation mapping and final source locators remain assigned to
Luna/root. Section 7 introduces these provisional keys:
`tondel2003-an-algorithm-for-multi-parametric`,
`baotic2016-gradient-value-function`, `lasserre2010-joint-marginal`, and
`qu2024-correlatively-sparse-lagrange`. Section 6's inherited keys also
need final bibliography integration: `hoffman1952-approximate-solutions`,
`lasserre2009-convexity-sdp`, `miller2025-sparse-matrix`,
`nie2026-sparse-tightness`, `pena2018-hoffman-constants`,
`piazzon2018-chebyshev-grids`, `rockafellar1970-convex-analysis`,
`zhang2025-wasserstein-moment`, and `zhong2024-two-stage-polynomial`,
besides the shared Kahl and Guo--Wang keys. These requests were sent to
root. The supplied prior notes support the stated comparisons; publication
priority remains qualified.

## Targeted validation actually run

Read-only inspection used scoped `rg`, `cat`, and `sed` commands.
An inline `python3 - <<'PY'` check on the three owned TeX files verified
final newlines, absence of trailing whitespace, balanced/nested LaTeX
environments, unique owned labels, and existence of every referenced
label in the current manuscript. It passed. A scoped citation-key scan
enumerated the dependencies above.

A temporary LaTeX harness at
`/tmp/sparse-sos-recourse-gxmrkqjt/recourse-check.tex` inputs only the shared
macros and Sections 6--7 plus Appendix B. The targeted command was
`pdflatex -interaction=nonstopmode -halt-on-error -output-directory=/tmp/sparse-sos-recourse-gxmrkqjt /tmp/sparse-sos-recourse-gxmrkqjt/recourse-check.tex`,
run through an inline Python subprocess with the manuscript as working
directory. The first attempt caught an alignment-environment error in
the newly written half-degree identities and a long inherited grid display;
both were repaired. The next two passes succeeded and produced a 22-page
PDF with no overfull-box warning. A final pass after the notation cleanup
also returned exit zero with no overfull warning. The final structure scan
covered all three TeX files and this report, and again passed the owned
environment, unique-label, whitespace, and reference-existence checks.
External references and citations are
undefined in this intentionally isolated harness. This is a syntax and
layout check, not validation of bibliography integration or mathematics.

`git diff --check -- paper-sparse-sos/sections/06-recourse.tex paper-sparse-sos/sections/07-regularity.tex paper-sparse-sos/appendices/B-recourse.tex`
returned exit zero, as did its final repetition including this report.
Because files can be untracked, the direct whitespace
scan provides the relevant coverage for the new files as well.

No experiment, SDP computation, historical source checker, project-wide
verification, or CI inspection was run. Root's independent mathematical
reviews and final bibliography/build integration remain outstanding;
there is no identified unresolved mathematical proof dependency in the
owned recourse text.
