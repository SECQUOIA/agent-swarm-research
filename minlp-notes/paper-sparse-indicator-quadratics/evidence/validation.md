# Targeted validation

The following commands were run in `paper-sparse-indicator-quadratics` on
2026-09-27 for the central count, enumeration, and spectral-message text.

```sh
python3 checks/check_enumeration.py
latexmk -C -outdir=build main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
pdftotext -layout build/main.pdf build/main.txt
```

After the localized review fixes, the exact checker passed 2,172 near-optimal
count bounds over 11,830 complete noise outcomes. Of these bounds, 600 are
strictly below the feasible-family cardinality, so the assertions cannot pass
solely from the trivial cardinality bound. The cases contain 2,321 noise
outcomes with multiple optimal supports. Four additional full-cube examples
with `g(z)=sum(z)` and independent noise in `{-1,1}` attain the zero-tolerance
bound `(3/2)^m` exactly, for `m=1,...,4`.

The checker also passed the scalar recovery regression with `Q=1`, `c=0`,
`lambda=-5/6`, and `xi=1`: both supports are retained, and noisy branch values
select the inactive bit, whereas unperturbed constants select the wrong bit.
It passed 46 affine-family dictionary checks with 485
net points and 3,481 oracle calls. The oracle deliberately chooses the worst
allowed approximate candidate. The checker verifies disjoint coverage by
remaining cells after every extraction, inclusion of all near-optimal
supports, the upper gap bound, and the oracle-call bound. Exact affine
activity intervals test completeness over the whole domain; a dedicated
support is optimal only at a single tie point.

The clean LaTeX rebuild completed with 10 pages. The final `build/main.log` has no
warnings, undefined citations or references, or overfull/underfull boxes.
The PDF text was inspected for formulas, cross-references, and the bibliography.

The test cases give distinct finite checks of ties, recovery, and partition
invariants; their raw number is not evidence of a general theorem. The proof
was reconstructed from the source material. The manuscript makes
the tree-decomposition recurrence and factor ownership explicit, separates
the conditional coordinate bound from a root-only bound, and gives a
displayed expected-work bound with numerical parameters. The finite tests
are checks of small cases, not a proof of the general probability or
bit-complexity statements. A complete spectral treewidth implementation has
not been exercised by this checker; the later final-integration section records
the separate complete spectral reference and its checks. No project-wide checks or CI inspection
were performed.

For the hardness, message-size, and star-representation additions, the following
targeted commands were run from the same directory on 2026-09-27:

```sh
python3 checks/check_limits.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
pdftotext -layout build/main.pdf build/main.txt
```

The exact checker passed:

```text
PASS: 1728 hardness support QPs; 36 bounded-noise scaling cases
PASS: 208 message support QPs; 6252 pruning inequalities; 1284 separated-center checks; 252 state-lift supports; 528 short-approximation probes
PASS: 680 star atoms; 30 face inverses; 152 variable orders; 1070 projective residual states
```

The hardness cases include YES and NO inputs for each of the three restrictions,
both `theta=1/10` and `theta=1/20`, every binary support, the normalized scaling
identity, the unit-penalty gap, and state activation. Perturbed scaling is checked
with positive, negative, and alternating bounded noise. The message checker
assembles the original expanded objectives and solves their restricted normal
equations before comparing with the claimed residual formulas. It checks both
prefix-pruning estimates at centers, between centers, and at exterior probes,
as well as the two-piece and one-quadratic approximations for the earlier family.
Those finite probes do not verify an entire continuous interval; the manuscript
proofs establish the uniform estimates.

The star checker directly inverts all principal submatrices for up to eight
leaves. It compares every entry, evaluates the exposing functional and its
off-face atom bound, reconstructs the selected face atoms through the affine
inverse, and checks the Stieltjes sign congruence. For one to four leaves, it
examines every variable order and solves the projection equations in the
independent original factor-row basis. Dividing a nonzero coordinate out of
each residual gives an exact projective signature, so distinct signatures also
exclude equality after row normalization. This specifically tests the stronger
uniform-weight result; Gram matrices alone would not suffice. It does not test
arbitrary alternative decision-diagram state definitions.

The initial stage-2 manuscript built to 19 pages. Its final log had no warnings,
undefined citations or references, or overfull/underfull boxes. The new sections
and bibliography were inspected in the PDF text. The conic lower bounds and
literature comparisons rest on the cited primary results, not these finite
checks. No project-wide verification or CI inspection was performed.

After the localized review fixes, the checker above was rerun without changes
and produced the same three PASS lines. The manuscript was rebuilt with the
same `latexmk` command and the PDF text was extracted again. It now has 20
pages, with no warnings, undefined citations or references, or overfull/underfull
boxes. The displayed regime-3 residual identity, deterministic-message scope,
boundary-cost convention, revised literature comparisons, and new bibliography
entries were inspected in the extracted text. The new scalar projection and
inverse formulas were checked algebraically; no theorem or checker behavior
changed. The lead selected direct verification for these localized fixes as
recorded in `review.md`.

The scoped whitespace check was also run from the repository root:

```sh
git diff --check -- paper-sparse-indicator-quadratics
```

It passed. These are local targeted checks; no CI result is claimed.

For the supporting moment, geometric, and recursive-theory additions, the
following targeted commands were run from this paper directory on 2026-09-27:

```sh
python3 checks/check_extensions.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
pdftotext -layout build/main.pdf build/main.txt
pdfinfo build/main.pdf
git diff --check -- .
```

The new checker produced:

```text
PASS: 276 atomic moment bounds (152 below the trivial cardinality bound); 192 VC tails; 192 affine-rank tails (132 with bound < 1; 45 of these have nonzero event probability); 25792 exact noise outcomes
PASS: 2170 open/closed half-line and 97960 interval discrepancy comparisons
```

The probability checks enumerate all noise outcomes for the stated small
families, compute their near-optimal sets, and compare exact rational moments
of orders one, two, and three with the atomic bound. They separately compute
VC dimensions and higher-gap event frequencies. The 152 nontrivial moment
comparisons exclude success solely from the family-cardinality bound. Of the
192 rank-tail comparisons, 132 have an upper bound below one; 45 of these
also have a nonzero observed event probability. The checker computes these
counts from the enumerated cases. The remaining comparisons are included in
the totals without being treated as evidence of the same strength.
The discrepancy checks use every grid size from 2 through 32, grid points,
between-grid midpoints, exterior points, singletons, and all endpoint
conventions. These checks add finite evidence for the new moment and atomic
transfer statements; they do not establish their general proofs.

The initial integration build caught a mismatched LaTeX delimiter and an
obsolete binomial command; both were corrected. The final manuscript has
34 pages. Its final log has no warnings, undefined references/citations,
or overfull/underfull boxes. A targeted in-memory source scan found 102
unique equation/theorem/section labels with all references and citation keys
resolved, and verified the new appendix headings in the extracted PDF text.
The extracted formulas, proof boundaries, and bibliography were inspected.
The scoped whitespace check passed.

The primary-source passages for sign-condition components, fixed-dimensional
CAD, planar bounded-Hessian levels, DC Hessians, and finite-total-curvature
curves were inspected as recorded in `sources.md`. The finite piecewise
quadratic loop argument explicitly includes interface corners and all
stratum critical values. Both recursive constructions retain full genuine
support quadratics and justify unrestricted elimination separately from
coverage at boundary and tie points. The new subdivision statement retains
all labels, while the recursive formula algorithms use representatives;
their noise-grid and output differences are stated in the manuscript.

A short addition to the star section retains the older dyadic-weight
unnormalized-Gram result and the stronger count when the root is last.
The two residual norm identities follow directly from the displayed residual
vectors; the condition bound uses `sum_i 4^(-i) < 1/3`. This addition does not
extend the Gram claim to row-normalized states.

No CAD implementation, complete spectral dynamic program, or full recursive
solver was added or tested in this increment. The later final-integration
section records the subsequently added spectral reference and its checks.
No finite computation validates
the analytic coarea/curvature proof or the asymptotic algebraic complexity
bounds. The stage-3 independent review round and the lead's decision to
verify its localized fixes directly are recorded in `review.md`. No
project-wide verification or CI inspection was performed.

After the stage-3 review fixes, the changed extension checker, targeted
`latexmk` build, PDF text extraction, source/PDF consistency scan, and scoped
`git diff --check -- .` were run again. The checker produced the two PASS
lines above, including the independently computed 132 and 45 rank-tail
counts. The final PDF still has 34 pages, and the final log is clean. The
102 unique labels and all references/citation keys resolve. The extracted
PDF explicitly contains the interior-loop restriction, rational-bound input
convention, planar `M=R` substitution, and tree-algorithm comparison. These
checks support the localized revisions; they add no computational validation
of the analytic geometry or CAD theorems.

## Final integration: spectral reference and cumulative checks

On 2026-09-27, `checks/spectral_reference.py` was added as a standard-library
exact-rational reference of the primary spectral algorithm. It uses the supplied
decomposition for finite-grid optimization, projects child tables at separators,
recovers the grid witness, and continuously reoptimizes its support. It then
performs fixed-threshold partition enumeration at midpoint-net points and builds
each requested subtree message and the global message directly with the same
noise vector. Full noisy Schur coefficients, conditional optimizers, and the
original-objective certificate are returned. The implementation uses the
message-specific coordinate bound proved in the text, which is no larger than
the common bound used in the uniform work estimate. Iterative tree traversals
avoid a Python recursion-depth restriction. Valid Fraction-valued inputs and
supplied spectral bounds/decompositions are explicit preconditions.

The following four targeted checker commands were run from this folder; all
exited successfully. Their complete output is copied below. Logs are in ignored
`build/check-*.log`.

```sh
python3 -B checks/check_enumeration.py
python3 -B checks/check_limits.py
python3 -B checks/check_extensions.py
python3 -B checks/check_spectral.py
```

```text
PASS: 2172 exact count bounds over 11830 noise outcomes (600 bounds below family size; 2321 tied outcomes); 4 tight atomic equalities; noisy-constant recovery regression; 46 affine families, 485 net points, 3481 oracle calls.
PASS: 1728 hardness support QPs; 36 bounded-noise scaling cases
PASS: 208 message support QPs; 6252 pruning inequalities; 1284 separated-center checks; 252 state-lift supports; 528 short-approximation probes
PASS: 680 star atoms; 30 face inverses; 152 variable orders; 1070 projective residual states
PASS: 276 atomic moment bounds (152 below the trivial cardinality bound); 192 VC tails; 192 affine-rank tails (132 with bound < 1; 45 of these have nonzero event probability); 25792 exact noise outcomes
PASS: 2170 open/closed half-line and 97960 interval discrepancy comparisons
PASS: 178 restricted bag-DP/oracle checks against 20197 grid assignments; 37 strictly suboptimal oracle returns; 142 strict reoptimization improvements; 16 witnesses with a nonzero edge term
PASS: 10 enumeration contracts; 17 direct messages; 22 net points; 53 construction oracle calls; 35 finite boundary probes; 56 coefficient checks
PASS: 792 independent support QPs; 7 original-objective certificates; 2 designed tie cases; 8 endpoint/bit-count sampling cases; non-SDD spectral example; 1100-bag path
```

The new checker independently enumerates full grid assignments and calculates
conditional objectives by a matrix double sum. It checks every free/fixed-zero/
fixed-one pattern for each selected grid instance. It independently solves
continuous support problems by Cramer's rule with permutation determinants;
it does not use the reference solver or Schur formula as its comparator.
Branching, disconnected graphs, empty/repeated bags, active zero, signed
penalties, and empty internal/boundary sets are exercised. A three-vertex path
has nonzero contributions from both child-owned edges in its optimal grid
witness. A separate three-vertex matrix has diagonal 1, off-diagonal 3/5,
and known eigenvalues 2/5, 2/5, 11/5; it fails diagonal dominance in every row.

The one-variable example with `Q=1`, `c=-1`, `lambda=-11/8`, `xi=3/2`,
`C=2`, and `epsilon=1/4` gives a genuinely approximate root oracle: the grid
chooses the inactive support with value zero, while the true active optimum
is `-1/8` at `x=1/2`. The fixed-active call improves its grid value `1/8`
to `-1/8`, and enumeration recovers the true optimum. Thus the oracle checks
do not all collapse to exact support selection. Two scalar boundary examples
retain a label optimal only at zero or only at the two endpoints, although
neither type of tie point lies in the chosen midpoint net. Coefficient checks
include cross terms; sampling checks include both endpoints and the exact
number of requested bits. Seven certificates are compared with independently
computed unperturbed optima.

The generic dictionary comparisons use 35 finite boundary probes. They do not
verify an entire continuous parameter box by computation. The earlier
enumeration checker uses an exhaustive approximate oracle; the new reference
uses bag DP. These tests supplement the proofs and provide no asymptotic timing
claim or practical performance benchmark. No CAD or complete recursive SDD
solver was added, and the analytic geometry statements remain proof-based.

The final manuscript was rebuilt from clean generated files with:

```sh
latexmk -C -outdir=build main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
pdftotext -layout build/main.pdf build/main.txt
cp build/main.pdf paper.pdf
git diff --check -- .
```

The PDF has 34 pages. The final LaTeX log contains no warnings, undefined
references/citations, or overfull/underfull boxes. An in-memory source scan
checked 102 unique labels, 146 reference uses, and 28 used bibliography keys;
all resolve. The extracted PDF contains the short reproducibility statement,
and `paper.pdf` is byte-for-byte identical to `build/main.pdf`. The scoped
whitespace check passed. Title, oracle-proof, geometry, recursive-proof, and
last-reference pages were rendered with `pdftoppm` and visually inspected;
their ignored previews are `build/preview-{title,oracle-proof,geometry,recursive,references}.png`.

The cumulative independent review and the lead's disposition of its localized
findings are recorded in [review.md](review.md). No
project-wide checks or CI inspection were performed, and all generated files
and edits stayed inside this paper folder.

## Localized fixes after cumulative review

The cumulative review recorded in [review.md](review.md) led to attribution,
assumption clarity, and test-coverage changes only. The reference algorithm
and theorem statements are unchanged. The manuscript names the reference
file and its message-specific bounds, and identifies the lifted message's
separator and translated boundary subinterval. Beier–Vöcking's conference
Lemma 5 and Beier–Röglin–Rösner–Vöcking's journal Theorem 1 were inspected;
their methods and outputs are distinguished from this paper's count and
dictionary statements in [sources.md](sources.md).

The changed spectral checker now independently asserts the displayed `M_k`
and `L_k` formulas. Its non-SDD example also uses a two-dimensional boundary
box with radius `1/50`: the bounds are `M=103/400`, `L=1133/1000`, and
`epsilon=1/30`. The exact midpoint net has nine points, the Cartesian square
of `{-1/75, 0, 1/75}`. The checker asserts those points and their count, runs
the message construction on that box, and checks each net-point value by
independent support solves. The prior three checkers were unchanged; their
successful cumulative results are recorded above and were not rerun.

The following targeted commands were run after the changes:

```sh
python3 -B checks/check_spectral.py
latexmk -C -outdir=build main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
pdftotext -layout build/main.pdf build/main.txt
cp build/main.pdf paper.pdf
git diff --check -- .
```

The spectral checker passed with this updated output:

```text
PASS: 178 restricted bag-DP/oracle checks against 20197 grid assignments; 37 strictly suboptimal oracle returns; 142 strict reoptimization improvements; 16 witnesses with a nonzero edge term
PASS: 10 enumeration contracts; 17 direct messages; 30 net points; 69 construction oracle calls; 35 finite boundary probes; 56 coefficient checks
PASS: 810 independent support QPs; 7 original-objective certificates; 2 designed tie cases; 8 endpoint/bit-count sampling cases; 9 two-dimensional net probes; non-SDD spectral example; 1100-bag path
```

The updated PDF has 35 pages, including the two added bibliography entries.
Its final log has no warnings, undefined references/citations, or overfull/
underfull boxes. The source scan resolves all 102 unique labels, 147 reference
uses, and 30 used bibliography keys. `paper.pdf` matches the clean build.
The changed prose and bibliography pages (3, 5, 10, 14, 22, 33, and 35) were
rendered with `pdftoppm` and visually inspected. Updated ignored previews are
`build/preview-{prior-work,count,spectral-reference,lift,scalar,new-references,references}.png`;
the earlier representative previews were refreshed too. The scoped whitespace
check passed. All validation remains targeted and non-formal; finite parameter
probes do not prove completeness over the continuous box. No project-wide
checks, CI inspection, or changes outside the paper folder were performed.
