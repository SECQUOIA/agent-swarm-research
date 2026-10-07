# Independent early review of the shared foundations

Date: 2026-10-05. Reviewer: Sol. This is a review of the actual frozen partial
snapshot `paper-smoothed-global/evidence/snapshots/early-foundations-r1/`,
not approval of the full manuscript. The assigned scientific scope is
`sections/03-counting.tex` and `appendices/A-finite-noise.tex`;
`sections/02-model.tex` was also read to check their input and output contracts.
Locations below refer to these snapshot files, abbreviated as **03**, **A**,
and **02**. No manuscript or research note was edited.

**Decision.** These foundations are not submission-ready in the frozen
snapshot. The common-root output contract must be integrated, the singleton
case must be removed from a division by zero, and several false scope or size
sentences must be corrected. The substantive counting, pruning, continuous
growth, finite replacement, finite-tail, and scalar-fallback proofs are sound
under their stated substantive hypotheses. In particular, the stronger
lower-semicontinuous version of the sharp growth theorem is proved by the
written appendix. I found no defect that defeats the subject or requires
abandoning these results.

All four snapshot files match the manifest exactly:

| File | SHA-256 |
| --- | --- |
| `macros.tex` | `ac79fc04907f0edc4f964033bbcfa9c1d4d5b07b36428ad0466c72a34d6c8abd` |
| `sections/02-model.tex` | `2a6115404d2d26b9e11cf61c92153dae6da58140d74c85c25c4159599c2eeef9` |
| `sections/03-counting.tex` | `eceb3aa3bd4b9d8e86b32c7f79901d51e2ba2d4ccc9ffdd30bc27f495ba42cbd` |
| `appendices/A-finite-noise.tex` | `05b29ebba8703253ac20498b7c2e10ac362054fe968122267ec7bb25bf9a6644` |

The earlier reports were context. Their conclusions were not substituted for
checking the snapshot proofs. Literature and priority review remain with the
designated Luna lead; I performed no literature research.

## Required repairs

1. **Major: the fallback does not yet meet the manuscript's algebraic output
   contract.** At **03:518–524, 537–544** and **A:426–490**, the algorithm
   returns a separate univariate root representation for each coordinate and
   the value. At **02:260–264**, algebraic output requires one common root
   and rational polynomial maps for the entire optimizer and value.
   Canonical lexicographic selection proves that the scalar coordinates are
   compatible; it does not construct the promised common-root representation.
   The scalar theorem is true, but it is insufficient for the stated model.
   Integrate a common-root conversion into the theorem and proof, and enlarge
   the base-only multiplier before choosing exceptional-event thresholds.
   The new author report
   `paper-smoothed-global/evidence/author-reports/fallback-shared-root-sol.md`
   supplies a sound concrete conversion. I checked its squarefree tensor
   algebra, separation of the full complex Cartesian root set, independent
   coefficient-direction derivatives, selected-real-root recovery from the
   original scalar isolators, and degree/height accounting. Its conversion
   costs a polynomial in the product of the scalar degrees, with absolute
   exponents. Since these degrees have base-only bounds, the product remains
   `2^{poly_d(I)}`. This resolves the mathematical issue after integration;
   its appearance outside the snapshot is not a repair of the snapshot itself.

2. **Major boundary error: the rare budget divides by zero on an allowed
   singleton domain.** At **03:462–472**, `g_0 = rho sigma / S` is defined
   without requiring `S > 0`. A mixed box with no continuous coordinates and
   all integer ranges singletons is allowed by part (d), and has `S = 0`.
   The corresponding proof at **A:414–421** uses the undefined threshold.
   Handle `S = 0` by direct evaluation before selecting thresholds, then state
   part (b) for `S > 0`. This also gives a natural direct treatment of the
   zero-variable case before invoking nonempty quantifier blocks. The growth
   theorem itself already assigns the correct value `g_* = infinity` on a
   singleton.

3. **Moderate false size statement: output length is not bounded by a
   base-only `B` for arbitrary added coefficient length.** At **03:534–535**,
   “The output may have length up to B” contradicts the height dependence
   actually proved at **A:463, 469–490**. For a fixed base domain `{1}` and
   zero base objective, the tilted optimal value is the arbitrary rational
   coefficient `gamma`. A fixed finite length bound cannot encode all these
   values as `b` grows. Replace the sentence by an output-length bound
   `B (I+b+1)^{c_d}`, or an equivalent `B poly_d(I+b)` statement. The rare
   accounting cancels the base multiplier, and retains the polynomial factor.

4. **Moderate false universal scope: not all exact results use this
   closure-and-rare-fallback architecture.** The assertions at
   **03:249–258** and **03:550–569** conflict with the explicit lattice and
   strong-noise component exceptions at **02:218–222**. The fixed-atom
   example proves a limitation of the specified indefinitely refined
   corrected-corner search. It does not require every exact algorithm to use
   a rare fallback. Qualify the template and preceding explanation as applying
   to the closure-based results, and identify the lattice-spacing and exact
   component routes separately. Retain the necessary every-draw treatment of
   ties and flat optimum sets.

5. **Moderate false computability statement.** At **03:262**, a Turing
   machine is claimed to sample only finite rational laws. A sampler that
   counts fair-bit failures before the first success produces a geometrically
   distributed integer with infinite support and almost-sure finite runtime.
   The present samplers have a prescribed worst-case bound on time and random
   bits, which does imply finite support. State this chosen model directly.
   No finite-law theorem or constructed sampler needs the false general claim.

6. **Minor false intermediate-size estimate in an otherwise sound sampler
   proof.** At **A:207–217**, the Taylor sum is computed as an exact rational
   before rounding. Its numerator and denominator can have quadratic, rather
   than linear, bit length in `b`: powers of the rational `u` already multiply
   its denominator length by `P`. The sentence “All numbers have O(b) bits”
   is therefore false for the written arithmetic. A diagnostic following the
   exact formulas, with `j = 1`, gives `P = 108` at `b = 64` and a reduced
   Taylor denominator of 22,503 bits. Replace the sentence by a polynomial-bit
   intermediate bound, for example `O(b^2 + b log b)`, while retaining `O(b)`
   bits for the rounded weights and output atoms. This preserves the claimed
   worst-case `poly(b)` sampler cost without adding an approximate-arithmetic
   implementation.

7. **Minor evaluation-interface precision.** At **02:283–286**, a `q`-bit
   evaluation requires Euclidean point error at most `2^{-q}`. The fallback
   at **03:522–527** guarantees scalar enclosure widths and an objective gap;
   the proof at **A:496–506** does not assert the Euclidean point bound.
   Coordinate widths do not by themselves give the same Euclidean error in
   dimension `N`. When using these representations to implement the model's
   evaluation contract, refine with an additional
   `ceil(log_2(max{1,N})/2) + O(1)` bits. This change fits the same work bound.
   The separate fallback statements, as presently written, are true.

8. **Minor boundary conventions in the cited elimination theorem.** At
   **A:327–340**, state positive block sizes and at least one free variable,
   the range actually used in the proof, or state a correct convention for
   empty blocks. Also replace small logarithms in
   `L log L log log L` by positive constants. The local mathematical source
   `research-20261002/new-direction/polynomial-exact-fallback.md:158–184`
   explicitly records `ell >= 1` and the small-length convention. The
   snapshot omits both. All nontrivial applications here have one or two
   free variables and positive block sizes; direct evaluation handles the
   empty-dimensional case. This repair does not alter any claimed exponent.

9. **Minor notation mismatch.** The tie example uses `U_{sigma,M}` at
   **02:414**, while the shared tools define `mathcal U_{sigma,M}` at
   **03:94–95, 267–270**. Use the same name throughout.

## Mathematical checks of the written arguments

**Local comparisons and balanced meshes.** The cancellation at **03:59–75**
and **A:8–16** leaves an interval depending on the fixed base function and
grid node, not on the other noise coordinates. Negative endpoint difference
means the event is empty. The independent product bound and tensor-grid sum
at **A:29–43** therefore hold, including discrete atoms. Conditioning is
valid only on an independent random element, as the theorem expressly says.

The nested power-of-two partitions at **03:121–158** and **A:46–70** are
sound. An unrefined coordinate contributes two endpoints and no interior
test. For a refined coordinate, `h_ij > rho_i h_j/2`, so every coordinate's
curvature contribution, including an unrefined coordinate, is at most
`4 c_bal L_i h_ij^2`. This gives the stated bound on the *global* correction
`4 E_j/h_ij`. The uniform-grid atom term is bounded because `M >= m_ij`.
No clipped short final gap or dependence on a minimum original width is
hidden in this argument.

**Rounding and pruning.** The proof at **A:74–91** correctly uses
independent mean-preserving endpoint rounding one coordinate at a time.
Coordinate concavity after subtracting the quadratic is enough; full Hessian
semiconcavity is unnecessary on this box. The total allowance is
`sum_i L_i eta_i^2/8`.

At **A:93–120**, either the incumbent is already the global optimum, or an
optimizer-containing cell is processed and retained at every level. A closure
at such a cell gives the exact optimum. The incumbent and every retained
lower bound then give the asserted interval of width at most `E_j`.
Retained cells are charged to corners of a deterministic full grid with
gap at most `2 E_j`, and each corner is charged at most `2^k` times. This
avoids conditioning on adaptive survival. The approximation evaluation count
at **A:123–134** includes at most `2^k` children and `2^k` corners per
retained parent, giving the stated `8^k` factor. These box foundations do not
by themselves prove that later bag or constrained searches preserve the same
global rounding allowance; that remains a later-section obligation.

**Product replacement, including atoms.** At **03:277–297** and
**A:139–164**, the telescoping mixed products are correct. Interval
probabilities use distribution functions and their left limits, so open,
closed, half-open, singleton, and unbounded intervals are all covered.
The factor is `2 C sum_i delta_i`. Requiring the scalar-section bound for
every fixed real tuple is essential and is expressly included. An
almost-everywhere continuous-proxy section bound would not suffice.

**Bounded Gaussian-like sampler.** At **A:166–221**, `N` and the common
dyadic denominator use `O(b)` random bits per proposal, and the algorithm
makes a deterministic `O(b^2)` number of proposals. The success probability
is at least `1/(4K)`, hence the failure atom at zero has mass at most `e`.
The normalization, grid integration, and truncation estimates bound the
Kolmogorov error by `14e < 2^{-b}`. The rounded-squaring error recurrence
with the prescribed guard bits gives the stated weight accuracy. All output
atoms lie in the specified interval and have `O(b)` bits. Exact Taylor
arithmetic needs polynomial-size intermediates as noted above; it does not
break the theorem. The sampler's internal proposals define its finite law;
they do not discard or redraw a sampled optimization instance.

**Sharp growth tail and the lower-semicontinuous extension.** At
**03:324–355** and **A:234–321**, finite lower-semicontinuous `f` on compact
`X` is bounded below. Thus `-f` is upper semicontinuous, the maximum defining
`H` is attained, and `H` is finite and convex. Continuity of `f` is not
needed. Lower semicontinuity also gives the closedness of
`{c : g_*(c) >= epsilon}` by taking a convergent subsequence of witnessing
minimizers and passing each inequality to the limit.

The proximal residual lies in the coordinate intervals of lengths
`2 epsilon w_i`. Differentiability of `H` at the proximal point forces the
maximizer to be the residual divided by `2 epsilon`, yielding the exact
global quadratic-growth inequality. The area formula makes `DP` singular
almost everywhere on the containing bad set. Monotonicity gives positive
semidefinite symmetric parts of `DP` and `DQ`; a null vector of `DP` has
Rayleigh quotient one for `DQ`, so the trace bound is valid even without
invoking Hessian symmetry. Independence and bounded coordinate densities
then permit integration of each monotone coordinate section, giving precisely
`2 epsilon sum_i phi_i w_i`. The interval example has
`g_* = |c|/w` and proves sharpness of the constant. The written proof supports
the stronger hypothesis needed by reduced value functions.

**Two-block reduced-value sections.** At **03:387–451** and
**A:347–383**, compactness of `D` and continuity of the polynomial objective
make its reduced value lower semicontinuous on its compact projection.
The displayed formula uses one feasible witness `(x,y)` and one universally
quantified competitor `(x',y')`. Taking competitors with the same `x` forces
the witness's residual value to be optimal; taking a minimizing residual at
every `x'` gives the reduced growth inequality. Conversely that inequality
gives a witness. No third block is needed, even when residual minimizers are
nonunique or feasibility depends on `x`.

The formula has two blocks of size `n+m`, `2s+1` atoms, and degree at most
`max{d,2}` in the quantified variables and free scalar noise coordinate.
The format bound gives at most `H_s^2` polynomial occurrences of degree at
most `H_s`, hence at most `H_s^3` real roots after discarding identically zero
polynomials. Their root points and intervening intervals give the claimed
uniform section bound. All fixed noise values and `epsilon` are real
coefficients, so the argument includes every mixed-product section, not only
generic ones. Binary integer-range encodings can cause exponentially many
atoms, but only their logarithmic count enters the required precision.

**Active gradients.** At **A:385–408**, fix the integer labels, a continuous
face, and an active coordinate `i`, and condition on all other coefficients.
The free stationarity system is independent of `gamma_i`. Its nonsingular
complex solutions bound the real candidates by `D^{k'}`; only real candidates
are needed for the intervals. Positive point growth forces the free Hessian
at the actual optimizer to dominate `2g_* I`, so that optimizer is among the
counted nonsingular candidates. This does not assume that all stationary
points are nonsingular. Each candidate confines `gamma_i` to an interval of
length `2 tau`; the union over labels, faces, and active coordinates gives
the stated `K_act`. The zero-free-coordinate and degree-one cases are covered.

**Canonical fallback and bit separation.** The compact optimum set admits
the successive-coordinate minimizations at **A:427–433**. The two-block
singleton formulas at **A:435–455** select precisely that point and its value;
they remain valid with ties, singular stationary sets, and a continuum of
minimizers. Root recovery from the squarefree product at **A:473–490** is
sound: a singleton satisfying a univariate sign formula must be a root of a
nonconstant atom polynomial, and signs at all isolated roots select exactly
one root.

Crucially, **A:469–471** gives polynomial *degree* bounds depending only on
the base atom count, degree, and dimensions. Added coefficient bits occur
in the height bound through `L_c`, not in those degrees. Forming the product,
taking its squarefree part, and doing root isolation preserve a base-only
`2^{poly_d(I)}` degree bound and a coefficient-height bound of that factor
times a fixed polynomial in `I+b`. Thus arbitrary-precision refinement has
a fixed exponent in `I+b+q`; the proof does not merely infer degree bounds
from a total runtime bound. These are exactly the bounds needed by the
common-root repair.

**Feasible approximations and accounting.** At **A:492–506**, clipping the
continuous rational approximations and extracting the integer labels is
valid on a mixed box. The derivative bound has polynomial logarithmic size,
and the objective and value errors sum to the requested gap. No such claim
is made for an arbitrary semialgebraic domain, which can have no rational
feasible point. The model at **02:289–296, 374–378** correctly distinguishes
rational free coordinates with an exact implicit algebraic lift from a
coordinatewise rational approximation that may be infeasible.

The rare-budget inequalities at **A:411–421** are correct once `S > 0` is
enforced. Uniform noise gives two contributions of at most `rho` plus an
atomic contribution at most `rho`. Gaussian proxy noise gives two
`sqrt{2/pi} rho` terms plus at most `rho`, still below `3rho`. The accounting
lemma pays only for the base multiplier and retains the sampled-input
polynomial. The law must be selected after the multiplier, thresholds, and
depth are bounded from base data; the final algorithm must use the same draw
for the fast route and fallback. Enlarging `B` for common-root conversion
must precede this choice.

## Checks performed and remaining scope

I read `AGENTS.md`, `evidence/BRIEF.md`, and
`evidence/independent-review-brief.md`; read the frozen scientific files with
`nl -ba` and scoped `sed`; and used scoped `rg --files` and `rg -n` to locate
the relevant local mathematical notes and author report. I read the root
early reports and prewriting low-rank and sparse reports as context. The
targeted mathematical source reads were the proximal growth note, the
polynomial fallback note, and the common-root conversion report. I rederived
the inequalities, quantified formulas, root counts, and base/height
separation from the snapshot text.

Two inline Python diagnostics were run:

- A SHA-256 check using `hashlib` and the snapshot's `manifest.json` passed
  for all four files, with the hashes printed above.
- An exact `fractions.Fraction` Taylor-sum calculation used the sampler's
  prescribed `K`, `N`, `s`, and `P`, and `j=1`, for `b` in `{1,4,16,64}`.
  The reduced numerator/denominator bit lengths were respectively
  `2931/2932`, `3390/3390`, `5861/5861`, and `22503/22503`; the rounded-weight
  precisions were `39`, `43`, `57`, and `108`. This verifies the specific
  intermediate-size correction. It did not sample a law or solve an
  optimization problem.

A report-only final-newline, trailing-whitespace, paired-fence, and named-path
check was also run after writing this review. It passed. These are targeted
local document and proof diagnostics. No optimization experiment was rerun;
no project-wide check, CI status, or CI log was inspected.

The unresolved issues in this snapshot are the required repairs above.
After integration they need a check against the new written text, especially
the enlarged pre-draw fallback factor. The later low-rank, sparse, recourse,
component, and constrained closure theorems, their stopping events and
evaluation oracles, manuscript-wide coherence, and literature attribution
are outside this early assigned scope. This report grants no approval for
those sections or for the complete paper.
