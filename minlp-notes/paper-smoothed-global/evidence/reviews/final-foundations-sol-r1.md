# Final foundations review, integrated mathematical draft, round 1

The shared mathematical foundations are sound apart from one missing complexity
premise in the general parameter-dependent uniform-law corollary. That premise
has a concrete repair and does not invalidate the polynomial-precision cases.
The frozen assigned scope is therefore **not yet ready for submission**. After
the repair below and the pending primary-source checks, I find no remaining
substantive defect in the results reviewed here. This is a scope decision, not
approval of the complete paper or its bibliography.

## Scope and independence

I reviewed the actual immutable snapshot
`evidence/snapshots/integrated-mathematical-draft-r1/`, including all of
`sections/02-model.tex`, `sections/03-counting.tex`, and
`appendices/A-finite-noise.tex`. I read the relevant routing passages in
Section 04/Appendix B, Section 07, Section 08/Appendix F, and Section 10,
and the fallback evaluation interfaces at Appendix D:80–89, 690–697,
and 1068–1077.
This report does not certify those other sections' complete proofs.

I used `BRIEF.md`, `independent-review-brief.md`, `integration-contract.md`,
`integration-decisions.md`, `reviews/root-integration-to-final-math.md`, and the
specified earlier findings as task context. Their favorable verdicts were not
treated as proofs of the frozen text.

I previously wrote `author-reports/universal-law-budget-sol.md`. Accordingly,
my assessment of that development is not a fresh independent review of an
unfamiliar argument. I checked its actual integration, its hypotheses, and its
route qualifications in the frozen manuscript. The root separately assigned
a fresh reviewer for the common-root and uniform-law arguments. The root
also relayed that reviewer's concern about the cost of evaluating `F(K)`;
I independently confirm that concern below. My review of the other foundations
is independent of their authorship. I had earlier checked the separate
shared-root development, but did not author it.

All 20 TeX files match their manifest SHA256 hashes. The three principal files
have these hashes:

| Frozen file | SHA256 |
| --- | --- |
| `sections/02-model.tex` | `0a9267cd7a893497d212e5ccb0fbb6433b6428c4784793dd9fc79ec4f4e38a63` |
| `sections/03-counting.tex` | `9818728f37864c878ab2e7d0bb1690bb79e8d53f3a338e2f316e31787692b049` |
| `appendices/A-finite-noise.tex` | `4ff3fe30e76466dcc744389e88deaa9759fc19a2709c1104cba89612379c39cd` |

All line numbers below refer to this snapshot, not to the active manuscript.

## Required finding

**F1 — Moderate: effectiveness of a parameter envelope does not bound its
evaluation work.** Locations: Section 03:689–696, Appendix A:704–709;
model proposition at Section 02:191–210 and its work definition at
Section 02:255–257.

Part (c) assumes only that `F` is effective and nondecreasing. It then specifies
the exact common resolution `M(I,K)=2^{ceil(F(K) P_0(I))}` and promises a work
factor `(1+F(K))^c`. The proof accounts for the lengths of sampled data and for
substitution into the original fixed work polynomial. It does not bound the
deterministic work of computing this resolution. That work is expressly part
of an exact smoothed algorithm's expectation in the model.

This is a missing hypothesis, not a consequence of output length. If `L` is
an arbitrary computable language on the integers, then
`F(K)=2K+1_L(K)` is an effective integer-valued nondecreasing function:
its successive differences are at least one. Its values are `O(K)`, but its
evaluation need not have any fixed polynomial bound in `I+1+F(K)`. Mere
effectiveness therefore does not justify the cost claim for the prescribed
law. Raising the fixed exponent `c` cannot cover an arbitrary computable
evaluation cost.

Concrete repair: require a fixed explicit nondecreasing integer envelope
`F >= 1` whose evaluation at `K` costs at most
`(I+1+F(K))^{c_0}` for a fixed exponent `c_0`, and include that exponent in
the work factor. Alternatively choose an enlarged computable envelope that
dominates both the required budget and its own evaluation cost. The first
version is clearer for this paper. Make the same qualification in
`prop:model:uniform` or state that its existential `F` is chosen with this
property. Fixed integer polynomial envelopes should likewise be the intended
meaning of the effective `P_0` in the construction.

The actual flow/TU application supports this repair. Appendix F:754–779
bounds its chart-margin coefficient length using
`Xi'_d(k)=(k+1)^{O_d(k^2)}`; Appendix F:821–832 uses that length in the cap
and grid exponent. A fixed admissible integer exponent gives an explicit
envelope, and finite sums/products of these bounds can be covered by another
explicit integer expression. Computing that expression is polynomial in its
value and the supplied length. No new precision theorem is needed. The
existential model proposition is thus repairable by choosing the correct
envelope; parts (a) and (b) are unaffected.

## Minor precision and writing findings

**F2 — Low: say what the remaining polynomial factor is polynomial in.**
Locations: Section 02:280–281 and 373–375. The statements that the fallback
contributes “only a polynomial term” and that its expected contribution “is
polynomial under the stated law” can be read as a bound polynomial in the base
length alone. The accounting lemma gives a polynomial in the bounded sampled
length, and in `q` when refinement is requested. For nonlinear boundary
flow/TU that length can contain `F(K) poly(I)`. The displayed theorem bounds
already retain this dependence. Repair the prose to say “a polynomial in the
sampled bit length, with the stated parameter factor,” or explicitly write
`poly_d(I+b+q)`. This is not a defect in the accounting lemma.

**F3 — Low: define the empty-retained-set minimum.** Location:
Section 03:210–211. The lower certificate is used even when no cell remains,
but `min_{C retained}` has no stated empty-set convention. Define that minimum
to be `+infinity`, or write the minimum of the set consisting of `U_j` and
the retained bounds. Then it equals `U_j` on exact termination. The proof at
Appendix A:116–120 is otherwise correct.

**F4 — Low: avoid an infinite growth coefficient in the measurability proof.**
Location: Appendix A:239–241. The sentence asserting that the growth inequality
holds at `g=g_*` includes the singleton case, for which the definition sets
`g_*=infinity`; its right side would contain `infinity * 0`. Handle a singleton
first, or restrict that sentence to finite `g_*` and say the argument uses
every finite `epsilon`. The theorem and its tail bound are correct for a
singleton and require no other change.

## Status of every result in the assigned foundations

“Checked” below means that I checked the written statement and proof under the
stated model. Classical-source identity and exact locator checks remain Luna's
work; I did not conduct literature research.

| Result or contract | Frozen locations | Status and reason |
| --- | --- | --- |
| Grid law and interval concentration | 02:85–107; A:18–27, 140–148 | Checked. Endpoint spacing, `1/M`, atom sizes, and bounded fair-bit sampling are correct. |
| Neighbor interval, `lem:count:interval` | 03:62–78; A:8–16 | Checked. The other tilt coefficients cancel and the second difference gives `L_i h+2 delta/h`. An empty reversed interval causes no problem. |
| Local count, `thm:count:local` | 03:104–115; A:29–44 | Checked. Intervals are deterministic after conditioning on independent data; independence multiplies their probabilities. The tensor sum gives two endpoint terms per coordinate. |
| Balanced meshes and level count | 03:125–162; A:46–70 | Checked. Dyadic equal subdivisions are nested; refined gaps are larger than half the nominal scaled gap. The global correction includes every coordinate, including unrefined ones. Row-specific scales are handled correctly. |
| Corrected corners, `lem:count:rounding` | 03:175–182; A:74–91 | Checked. Independent endpoint rounding, successive conditional Jensen inequalities, and variance at most `eta_i^2/4` give the factor `1/8`. |
| Search invariant, `thm:count:cells` | 03:184–217; A:93–122 | Checked subject to F3's convention. Either a minimizing cell remains, or a sound closure has found the exact value. Retained cells have a corner within `2E_j`, and each grid node is charged at most `2^k` times. |
| Approximation count, `cor:count:approx` | 03:223–242; A:124–136 | Checked in the preceding search setting. The cap gives `E_J <= epsilon`; the level work is `2^k+8^k H J`. The finite law depends on the requested accuracy, and exact evaluation bit costs are separately charged. |
| Fixed-atom example | 03:244–270 | Checked. On the atom the tilted objective is constant and all `2^j` cells survive. The text limits this search, not every possible exact algorithm. |
| Product replacement, `lem:count:transfer` | 03:293–315; A:140–165 | Checked. Every scalar section, including degenerate and endpoint intervals, is controlled using CDF values and left limits. Telescoping through mixed products gives `2C sum delta_i`. |
| Bounded Gaussian-like sampler | 03:317–338; A:167–226 | Checked. Worst-case trials and fair bits are bounded; atoms have `O(b)` bits. The error estimates sum to `14*2^{-(b+20)} < 2^{-b}`. Exact Taylor intermediates now have a polynomial, rather than linear, bit bound. |
| Sharp growth tail, `thm:count:growth-tail` | 03:342–395; A:238–325 | Checked for finite lower-semicontinuous `f` on arbitrary nonempty compact `X`, subject only to F4's trivial singleton wording. The written proof supports the strengthened regularity assumption. The factor two is sharp. |
| Renegar format/height theorem | A:331–354 | Applications checked against the stated classical theorem. Positive block sizes, at least one free variable, degree at least two, and small-log conventions are now explicit. Primary identity and exact theorem locator remain pending Luna. |
| Reduced-value section count, finite-tails (a) | 03:404–428; A:356–383 | Checked. The good-growth formula has exactly two blocks of `n+m` variables and one free tilt variable. Reduced-value attainment and lower semicontinuity follow from compactness. The count is uniform over every real conditioning value. |
| Grid/Gaussian growth tails, finite-tails (b)/(c) | 03:429–442; A:385–395 | Checked. The event is open, so measurable; the all-sections format bound makes replacement valid also at atoms. Passing `epsilon` down to zero gives the zero-growth bound. |
| Active-gradient tail, finite-tails (d) | 03:443–452; A:397–421 | Checked. The active coefficient is absent from free stationarity after fixing a face. Positive global growth makes the free Hessian nonsingular. A bounded number of nonsingular roots gives fixed intervals of length `2 tau`. |
| Rare fallback accounting/budget | 03:471–507; A:424–435 | Checked. The multiplier cancels against its probability, but the sampled-length polynomial remains. Grid and Gaussian constants both give at most `3 rho`; `S=0` is handled before division. |
| Shared-root tuple lemma | A:439–562 | Checked. The tensor algebra is reduced after squarefree preprocessing. A moment-curve integer form separates all complex tuples; the characteristic polynomial and coefficient-direction derivative recover coordinates. Original isolators select the designated root. Absolute polynomial work/height bounds are sufficient. |
| Exact fallback, `thm:count:fallback` | 03:511–601; A:564–673 | Checked. Canonical scalar formulas describe the same lexicographic minimizer and value, including continua and singular stationary sets. Shared-root conversion supplies the model output. Degree bounds are base-only, and heights/work have a fixed polynomial dependence on added bits. |
| Feasible rational fallback evaluation | 03:563–565; A:656–672 | Checked at its stated mixed-box scope. Integer labels are recovered exactly; clipping continuous midpoint approximants keeps feasibility. A gradient bound gives the certified gap, and the coordinate precision allowance gives Euclidean error. |
| Closure template | 03:605–640 | Checked as a scope summary. It excludes the lattice and strong-field methods from the rare-fallback template and retains the order of all pre-draw choices. Route-specific closure proofs remain their reviewers' scope. |
| Common grid resolution, universal-law (a) | 03:642–676; A:677–685, 715–768 | Checked under its monotone schedule and effective integer-polynomial envelope. Only the fixed bit polynomial changes; numerical count parameters are retained. Lattice termination requires the stated cap reset. |
| Common Gaussian resolution, universal-law (b) | 03:677–688; A:687–702, 770–790 | Checked. The common `t,b` satisfy both support and precision requirements. The box and cap are recomputed, and the weighted counts use original projected widths. |
| Parameter-dependent resolution, universal-law (c) | 03:689–696; A:704–709, 802–813 | Requires F1. The data-length argument and the `K` qualification are correct, but envelope computation is not bounded by the stated premise. |
| Model uniform-resolution proposition | 02:174–225 | Polynomial-precision parts checked. The nonlinear flow/TU clause needs an explicit efficiently evaluated envelope as in F1. The proposition correctly fixes format constants and the oracle implementation. |
| Exact algorithm and output contracts | 02:242–406 | Checked for the assigned interfaces, subject to F2's wording. One draw, every-draw correctness, global proof versus descriptor, shared-root versus component output, Euclidean evaluation, and the numerical meaning of FPT are distinguished. |
| Original-objective regret proposition | 02:420–454 | Checked. The lower endpoint follows from a lower sampled value and a linear-support upper bound; feasible `y` supplies the upper endpoint. Rational evaluation enclosures add their error and require exact feasibility. |
| Scale calibration and its qualifications | 02:456–516; 10:19–29 | Checked. Widths are in the perturbation coordinates, `W_noise=0` is separate, Gaussian support includes `b+20`, and strong-field lower-scale premises do not permit arbitrary small-error calibration. All other numerical factors remain in work bounds. |
| Model tie example | 02:525–552 | Checked. The equality event has mass `1/M`; the two indicated corners are the only minimizers. Zero point growth forces an atomic tail term. The text does not assert that every exact algorithm needs this fallback. |

## Checks of the delicate proof steps

The sharp tail does not use continuity of `f`. Lower semicontinuity makes the
maximum defining `H` attain its value, and finite `f` on compact `X` makes
`H` finite. The limiting minimizer argument makes `{g_* >= epsilon}` closed.
The nondifferentiability set can be enlarged to a Borel null set, whose
preimage under the Lipschitz proximal map is measurable. Applying the area
formula on bounded pieces makes `DP` singular almost everywhere on that
preimage. Monotonicity gives positive semidefinite symmetric parts for both
`DP` and `DQ`; a kernel vector of `DP` yields trace `DQ >= 1`. Independent
bounded densities and the absolutely continuous monotone sections of `Q_i`
then give total variation `2 epsilon w_i`. These steps justify the stated
tail without a definability or smoothness assumption on the original problem.

For the finite-law tails, I checked the distinction between coefficient space
and the reduced feasible variables. The quantified good-growth formula chooses
an attaining `(x,y)` and compares it to all feasible `(x',y')`; setting `x'=x`
also proves that the witness has the reduced optimal value. There is no extra
quantified fiber-minimization block. Discarding constant/zero output
polynomials leaves at most `H_s^3` roots and at most `2H_s^3+1` point/interval
pieces. This bound holds for all real fixed tilt coefficients, which is the
condition needed when finite and continuous marginals are mixed.

For active gradients, the union ranges over native integer labels, original
box faces, and active coordinates. It counts nonsingular free stationary
solutions, not an arbitrary possibly positive-dimensional stationary set.
The Taylor argument from positive global growth supplies exactly the required
nonsingularity. Faces with no free coordinate contribute one candidate; a
linear objective cannot have a nonsingular positive-dimensional free system.

For the fallback, each scalar singleton has degree bounded by
`A_0=2^{poly_d(I)}` independently of `b`. There are `N+1` scalars, with
`N <= poly(I)`, so the product degree is still `2^{poly_d(I)}`. The shared-root
lemma has absolute polynomial exponents in that product degree and the scalar
heights. Consequently powers of `b` and `q` do not depend on `N`. The enlarged
base multiplier includes elimination, univariate recovery, and conversion
before the failure budget or law is chosen. It is not asserted to bound the
whole output length independently of `b`.

The shared-root construction also keeps the value contract honest: its source
isolators select `(x^lex,f^*)`, so the value identity holds at the selected
root. It need not hold modulo the polynomial at extraneous Cartesian tuples.
The text now says this explicitly. Integer coordinates are extracted exactly,
and the Euclidean allowance costs only additional `O(log(N+1))` scalar bits.

For Gaussian uniformization, the written calculation is
`b+20 <= H+4H log_2 H <= H+4H^2 <= H^4 <= 2^t`, with `2^t <= 2H^4`.
The cap is computed on that very trial box before sampling. Appendix B:675–688
gives `J(t) <= J(0)+t`, and its deterministic node budget has logarithm bounded
by a polynomial base term plus a polynomial multiple of `t`. Enforcing
`h_J <= 1` keeps the mixed-label gap constant independent of support.
The separable schedule at B:878–887 has the same affine precision envelope.
These are sufficient for the common `A,D` construction.

The model's Gaussian original-objective calibration chooses the least
adequate dyadic scale. Its failed previous trial implies
`1/sigma < 4R(P(I_0+t)+20)` when `t >= 1`, while `t=0` has
`1/sigma=1 <= R`. Thus the full support factor is included without silently
introducing an exponential precision cost. The prescribed-error consequence
retains curvature, width, and coupling ratios as numerical factors.

## Integrated qualifications retained correctly

- Bounded worst-case random bits, not Turing samplability alone, imply finite
  support. The manuscript now gives the countably supported counterexample.
- Singletons and zero-coordinate cases are handled before mesh widths,
  threshold divisions, or positive-block elimination are used. Implicit point
  charts still require evaluation of their dependent roots.
- Feasible rational approximants are promised on mixed boxes, rational
  polyhedral domains, and explicit rational polynomial graphs. An implicit
  graph may need an exact algebraic dependent lift and may contain no full
  rational feasible point.
- Fixed degree bounds format/degree logarithms, not every geometric quantity.
  The repeated-squaring compact domain is a correct counterexample to a
  generic polynomial logarithmic width inference. Actual polynomial-bit routes
  use their narrower domains and supplied brackets/certificates.
- All supplied scales, numerical bounds, matrices, and certificates are
  charged in base length. The fixed oracle must cover every required rational
  query in the new coefficient support. Its costs and certificate checks are
  not removed by uniformization.
- Nonlinear boundary flow/TU keeps a supplied `k <= K` and parameter-dependent
  sampled lengths. Taking `K=I` does not preserve the actual small-core work
  bound. The text claims a limitation of this proof, not an impossibility.
- Strong-field interval probabilities are recomputed for the new grid. The
  two-grid example shows why arbitrary distribution-dependent subcriticality
  is not monotone; the explicit sufficient strong-noise regime is preserved.
- The common law is a normalized scalar family, rescaled by supplied noise
  scales in the theorem's perturbation coordinates. It does not switch law
  families or assert one identical vector measure for different instances.
- Arbitrary-precision evaluation refines the same exact descriptor and draw.
  It does not continue raw-grid refinement forever under a fixed atomic law.

## Targeted checks and unresolved work

I read all assigned statements and proofs with `nl -ba ... | sed -n ...`.
Targeted searches used `rg --files` for the immutable snapshot and `rg -n`
or `rg -n -F` for result labels, sampling/precision passages, support schedules,
margin bounds, and output contracts. A few initial locator searches failed
because of guessed filenames or an unescaped regular expression; I corrected
them using the actual file catalog and literal patterns. Those failures were
not mathematical or verification failures.

I ran a local Python SHA256 comparison of every file listed in
`manifest.json`; it returned `PASS: all 20 manifest SHA256 hashes match
immutable snapshot`. I also checked the written constants, exceptional
probability sums, dimensions of quantified blocks, refinement allowances,
and absolute polynomial exponents by hand. A targeted Python check confirmed
the report's final newline and absence of trailing whitespace. No optimization or sampling
experiment was run. No project-wide tests, CI checks, compilation, literature
research, source-note edit, or manuscript edit was performed.

The remaining assigned-scope action is F1's explicit envelope-computation
premise, with the minor precision repairs F2–F4. Luna must finish the primary
identities/locators and applicability checks for Renegar, the measure/convex
facts, nonsingular-root counting, and univariate isolation/refinement.
This report does not infer those checks from successful typesetting or from
earlier reviews. A new immutable capture can be checked for the exact repairs;
the frozen files reviewed here must remain unchanged.
