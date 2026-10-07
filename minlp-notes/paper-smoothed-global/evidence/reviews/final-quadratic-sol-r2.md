# Focused independent quadratic review, frozen round 2

Reviewer: Sol. Date: 2026-10-06. Review target:
`evidence/snapshots/mathematical-revision-r2/`, captured at
`2026-10-06T04:04:44.496806+00:00`. The manifest status is “Complete root
review repairs and verified companion comparisons; final bibliography
pending.” This report reviews the actual frozen repairs and their effect on
the assigned quadratic proofs. It does not inspect or approve mutable live
sources.

**Decision: both quadratic findings from round 1 are resolved.** No new
negative-inertia versus supplied-row-count mismatch, false noise-independence
claim, or changed theorem/count contract was found in the assigned passages.
Section 04 is byte-identical to the fully reviewed R1 version. Appendix B
has exactly one diff hunk, which adds the correct scalar branch to the
sharp-fiber proof; all its other proof blocks are unchanged. The R1
mathematical verdict therefore carries forward, with its two local
corrections now completed.

One minor sign-description correction remains in the changed introduction
body: it says the convex unaries are combined by subtracting a concave term.
The actual model adds the concave term, as the table now correctly says.
This does not affect a theorem or proof.

The assigned internal mathematical scope passes this focused review. Final
primary-source identities and their precise classical theorem contracts
remain pending with Luna. This is not complete-paper submission approval,
a novelty judgment, or a fresh approval of unassigned chapters.

## Provenance and unchanged proof scope

I read `BRIEF.md`, `independent-review-brief.md`, my
`final-quadratic-sol-r1.md`, the original-finding responses in
`author-reports/quadratic-sol-final.md`, the root's
`review-disposition-final-r1.md`, and the actual diff at
`evidence/reviews/mathematical-revision-r2.diff`. I also read the focused
shared-tools repair review. The review reports establish the intended
repairs; the dispositions below use the actual R2 source passages and
direct comparisons between the two immutable snapshots.

All source locators below refer to R2. For compactness, `01:68` means line
68 of `sections/01-introduction.tex`, and `B:768` means line 768 of
`appendices/B-quadratic.tex` in that snapshot.

I checked SHA-256 values and line counts against the R2 manifest for the
same ten assigned/dependency files as in R1. All matched. This is a targeted
ten-file check, not a check of all twenty manifest entries.

| File | Lines | R2 SHA-256 |
|---|---:|---|
| `sections/01-introduction.tex` | 545 | `ff426b32af15073bc6bbe5fa15081600bda1e4b0e05f4c1c6504b0fcdcef8bf8` |
| `sections/02-model.tex` | 569 | `b2ee85b74131bf95659b085dbfe7976e63746acfccfe1500eb060e088891c8ca` |
| `sections/03-counting.tex` | 758 | `28141913b9357189bace34ee2f3e5ee19fd9d04fdfdfcbdaab9edeb375f4c7c8` |
| `sections/04-quadratic.tex` | 909 | `020d70a1f2d3380776aa908dc25a5d9351c126674c0571a74e73a7dab867edd5` |
| `appendices/A-finite-noise.tex` | 829 | `895d4ce273e88a2ab9e9a7a4196b950a619ffdf829a2033536c43dc59295a6d8` |
| `appendices/B-quadratic.tex` | 890 | `29d21acfe56716f49e6098efd1f51cb9cd4babe3f114146891728d94ec6f7e2a` |
| `appendices/G-boundaries.tex` | 481 | `163333352717c3b090f62924f8a8b90eea63cf7c4fc50bf1da0dafd4556f1553` |
| `sections/08-integer.tex` | 777 | `b88b511b7201f75c12a4f51d9e39725d5dee823c80ee8981e8cdf1e5b8d6461c` |
| `appendices/F-integer.tex` | 1131 | `7720acea2407b43cc60844522197094936d3572373ed0759ac2f7611112d69e2` |
| `sections/09-boundaries.tex` | 825 | `fcc8051f9f19582837624ce11d8db5f49b8a2520ed934bf8870f119815c13761` |

Direct byte comparisons establish the following, rather than relying on
an author's statement that the proofs are unchanged:

- Entire Section 04 and Appendix G are unchanged from R1.
- Appendix B before its fiber subsection and after its fiber subsection
  is unchanged; its only diff hunk is the scalar fiber calculation.
- The native-integer low-rank subsection of Section 08, up to its scope
  subsection, and the full low-rank lattice subsection of Appendix F are
  unchanged. Their shifted R2 starting lines are `08:654` and `F:1022`.

Thus this round does not need to repeat the 566-line R1 review of
normalization, witness upper models, face extraction, guarded reconstruction,
mixed conditioned coverage, competing-label certification, tube families,
Gaussian weighted counts, support/precision loops, anisotropic recourse, or
the integer objective lattice. The complete conclusions and qualifications
in that report remain applicable.

## Disposition of the two assigned findings

### Q1: parameter is supplied row count — resolved

Previous severity: moderate summary/parameter-scope defect; the main
theorems were already correct.

The introduction now describes the separable concave term using “k supplied
factor rows” at `01:67–70`. The results-table caption explicitly lists
“supplied factor row count” at `01:133–135`. Its separable and integer
structure cells at `01:159–164` say “plus a concave factor” without asserting
intrinsic rank. The model's structural-parameter paragraph separately lists
negative inertia and the number of rows in a supplied concave factor
(`02:50–61`). These are the actual changes requested by the R1 report.

They agree with the unchanged factor definition at `04:85–99`, which
defines `k` as the number of supplied rows, and with
`thm:qp:aligned` at `04:615–626`, which permits an arbitrary factor with
`k` rows. The aligned separable regime inherits that premise. The pure
native-integer theorem still permits zero or dependent rows (`08:664–665`).
The corrected summaries therefore do not invite replacing the row count
by intrinsic rank while retaining the same aligned finite law.

The intrinsic quadratic regime still uses `k=n_-(A)` and its computed
normalization. This is explicit in `thm:qp:gauss` at `04:559–582` and in
the introduction's opening quadratic explanation at `01:51–60`.
Full-row-rank ambient and anisotropic statements retain their premises,
while the separable Gaussian warning at `04:874–877` retains supplied
curvature and declines to identify a minimum-rank representation. No
new mismatch between these meanings of `k` was found. No theorem bound,
parameter exponent, factor ratio, or sampling law was changed by this
wording repair.

### Q2: scalar fiber calculation — resolved

Previous severity: minor omitted proof branch; the proposition was true.

At `B:768–770`, the joint min/max density calculation is now explicitly
restricted to `n>=2`. At `B:771–772`, the proof separately handles `n=1`:
`A'=B'=U_1`, and the event is `|2U_1-1|<=q`. Since the unchanged proposition
has `0<=ell<=2 sigma m`, its definition
`q=ell/(2 sigma m)` lies in `[0,1]`. For `n=m=1`, the event is the interval

\[
 \frac{1-q}{2}\le U_1\le\frac{1+q}{2},
\]

which has probability `q=1-(1-q)^1`. Hence the stated probability formula
holds also at `q=0` and `q=1`. The variance identity and disjoint-block
product following it remain valid. The formula in
`prop:qp:fiber-sharp` (`04:674–683`) and the dimension dependence are
unchanged. There is no residual use of a singular joint density in the
scalar branch.

### R2-Q3: introductory sign description — minor prose correction

The changed sentence at `01:67–68` says “Convex piecewise-quadratic unaries
with rational breakpoints minus a concave term with k supplied factor rows.”
Taken literally, subtraction of a concave function preserves convexity;
it does not describe the nonconvex model. The actual definition is
`sum_j q_j(x_j) - alpha ||Tx||^2/2` (`04:752–769`): the negative quadratic
is the concave term being added. The corrected table's “plus a concave
factor” at `01:160` has the right sign.

Repair the body to “plus a concave term with k supplied factor rows,” or
“minus a convex quadratic represented by k supplied factor rows.” This is
a minor sign-description error, not a negative-inertia/row-count mismatch,
a missing proof, or a change to any mathematical result. Both R1 findings
remain resolved.

## Related changed interfaces

The introduction's independence paragraph now identifies the factor
coefficients and residual noise as the generally dependent quantities under
uniform ambient noise (`01:242–245`). It then restricts independence to the
continuous Gaussian proxy (`01:246–247`). This agrees with
`04:713–743`: independence of the projected factor and residual holds for
the real Gaussian proxy, while the actual finite law is handled by
axis-section transfer. It does not assert independence of correlated
factor coordinates, or independence for the actual finite Gaussian-like
law. The adaptive-count explanation immediately preceding it still sums
over a deterministic grid fixed before sampling.

At `01:308–316`, expected proof-record length is now tied to the
corresponding structural and numerical work bound. This removes the
unqualified polynomial-in-input interpretation. It is consistent with the
quadratic distinction between polynomial-height rational output and a
possibly large search trace (`04:499–507`), and with the retained numerical
ratios in the theorem bounds. The changed canonical-selector qualification
does not alter the quadratic algorithm's output contract.

`thm:count:cells` now gives an explicit empty-set minimum convention
(`03:210–212`). At exact termination this makes the lower certificate equal
to the incumbent, which already equals the global minimum by part (ii).
This is consistent with both guarded value reconstruction and the immediate
no-retained-cell branch in `B:209–229`. No pruning or count bound changed.

The growth-tail measurability proof now uses a finite positive threshold
`epsilon` and treats a singleton vacuously (`A:238–249`). Taking limits of
admissible finite coefficients justifies the closed superlevel set without
forming `infinity times zero`. The rest of the growth-tail proof is
unchanged. This preserves the tail used by the two-negative-direction
theorem; it does not change its finite-law residual or capped moment.

The universal-law parameter-envelope premise at `03:690–700`, its charged
evaluation at `A:706–714`, and the matching model wording at `02:192–200`
have the explicit computation contract already accepted by the focused
shared-tools review. The encoded supplied bound contributes to `I`, so

\[
 (1+\operatorname{size}(K)+F(K))^{c_F}
 \le (1+I)^{c_F}(1+F(K))^{c_F}.
\]

Thus evaluation before sampling fits the retained parameter factor. The
flow/TU envelope paragraph at `A:807–820` makes its application explicit.
The adjusted model fallback wording (`02:277–286`, `02:378–389`) correctly
retains sampled-height and sampling-parameter costs after rare-event
cancellation. These changes do not enlarge an uncharged cost in the
quadratic proofs: their selected `b` or grid bit length is already
polynomial in `I`, and the same-draw fallback and absolute exponent
contracts are unchanged.

## Remaining scope and checks performed

No assigned theorem/proof blocker remains; the minor introduction sign
wording should be corrected before publication. The final literature
audit must still confirm the exact classical primitives and locators
listed in R1, particularly singular/lower-dimensional exact rational
convex QP, exact convex MIQP with `f(n_z)L^c` and an absolute exponent,
rational LP/vertex extraction, reconstruction, rational Jacobi arithmetic,
and the convex-analysis/measure facts used in the growth proof. I did not
perform literature research, validate the new companion comparison prose
against its primary sources, or make a priority claim. Bibliography and
whole-paper readiness remain separate work. Table typesetting is also
outside this mathematical review; no build was run.

Checks actually performed: targeted `cat`, `rg`, `nl`, and `sed` reads of
the requested evidence and frozen changed source passages; Python
SHA-256/line-count comparisons for the ten listed files; direct immutable
R1/R2 byte comparisons and diff-hunk checks for the assigned proof blocks;
and a report-only format check. An initial attempt located the diff at the
wrong evidence path; `rg --files` found its actual location under
`evidence/reviews/`, which was then read. Initial low-rank block marker
checks used headings that did not match the source; checking the actual
headings produced the successful unchanged-block assertions reported above.
These were file-location checks, not failed mathematical tests.

Only this report was written. No live TeX, historical note, bibliography,
or other report was edited. No experiment, delegation, build, project-wide
check, or CI inspection was performed. The focused review stops here.
