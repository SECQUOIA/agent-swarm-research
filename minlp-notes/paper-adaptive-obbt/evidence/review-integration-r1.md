# Integration review, round 1

The scientific argument is coherent, and no new body-proof or experimental
transcription blocker was found. The remaining integration work consists of
narrow corrections to summary claims below and the already assigned
foundations/algorithms revision. This is acceptance of the integrated argument
subject to those corrections, not acceptance of the unrevised submission source.

The final source snapshot was read once at **2026-10-06 01:57:51 UTC**. The
active Opus revision had not landed in that snapshot. Findings were sent to the
root as they arose; this report does not wait for or assess that revision.

## Required summary corrections

1. **Fixedness, protection, and the value of a round.** In
   `sections/discussion.tex:7–14`, replace “A round is useless” with “A round
   cannot tighten endpoints” at a fixed box. Related work explicitly notes
   that a call with no movement can still yield useful dual information. Make
   the following distinction explicit: the certificate proves that its box
   `P` is fixed; `P` remains protected in every containing box at cutoffs above
   its threshold. It does not prove that the containing box is fixed.
   Replace “branching that separates the minimizers comes first” with the
   narrower conclusion that collapse to a singleton requires separating or
   otherwise excluding the distinct minimizers. Tightening outside their
   hull can still help, as foundations already explains.

2. **Upper bounds and certificate expiry.** In
   `sections/discussion.tex:54–63`, say that the limit width is bounded by
   `O(sqrt(epsilon))` and the remaining relaxation gap by `O(epsilon)` under
   the contraction hypotheses. “Scales like” suggests matching lower bounds;
   the generic theorem gives those only with its additional feasible-neighborhood
   and growth premises. In `sections/introduction.tex:126–127` and the
   discussion's cutoff paragraph, distinguish expiry of the cached pool's
   proof from loss of fixedness. Suggested wording: “Below the pool's face
   threshold, that pool no longer certifies the stop; the box can remain fixed
   down to its full-relaxation threshold.” This is the distinction already
   proved in `sections/cutoff.tex:91–108`.

3. **Scope of monotonicity and observed histories.** In
   `sections/discussion.tex:100–102`, restrict the monotonicity premise to the
   iteration, rate, and future-round certificate results. The LP validation,
   one-round screening, and numerical policy do not require monotonicity
   between callbacks; the policy itself violates it. The assigned F1/A1
   revision should also identify the box-relative tangent failure, not just
   the retained pool. At discussion lines 46–49, replace “does not certify
   anything” with a finite-history statement about small positive movements.
   An exact round with zero residual proves fixedness, and nesting always
   bounds future movement. Residual lines 349–361 already state these limits
   correctly.

4. **Existence does not imply a required reuse strategy.** At
   `sections/discussion.tex:87–89`, “a net gain requires reusing it” does not
   follow from discovery *sometimes* costing a round. Suggested wording:
   “If finding a certificate costs about as much as a round, reuse across
   rounds, cutoffs, or nodes may be needed to recover that cost.” Cheap
   certificates can pay without this prerequisite. The conclusion that the
   experiments did not assess such reuse is correct.

## Recommended precision edits

- In `sections/introduction.tex:52–58`, state contraction factors
  `lambda in (r*,1)`, stalling at every sufficiently small scale for
  `U >= f*`, and the two-variable rate for `abs(a) < 2`. These are the
  theorem's actual domains; “whatever the cutoff” is too broad.
- In introduction lines 153–156, use “has the same numerical threshold”
  for the relation to no-clustering conditions. The strict contraction
  condition and the cited nonstrict conditions should not be identified.
  The local-rate section already makes this distinction.
- The abstract remains longer than the planned 250-word limit at this
  snapshot. Its shortening is already assigned. Preserve the explicit
  current-round-only experimental scope and the absence of demonstrated
  speedup when shortening it.

## Accepted connections and presentation

The three limits organize the paper well: the original sublevel hull is a
problem property, fixed boxes depend on the relaxation, and rates depend on
the iteration. The body distinguishes Jacobi and sequential rounds, projected
and lifted monotonicity, and closedness needed to identify the iteration limit
as a fixed box. The contracting and stall conditions are sufficient tests,
not an exhaustive dichotomy; the critical scalar example supports that claim.
Singleton certificates and asymptotic convergence are handled consistently.

The certificates correctly concern remaining movement rather than a new
search domain. They separate a frozen-round screen from witnesses checked on
their own rebuilt hull, give the scope under rounding/cuts/branching, and
separate checking from discovery. The constrained region-cover result provides
the uniform sensitivity premise that the residual theorem needs; a current
basis or an observed ratio does not supply it. The exact closure algorithm and
the numerical solver policy have distinct contracts, including the conditional
validity of numerical incumbent cutoffs.

The experimental interpretation is reliable and useful. The 120-run comparison
reports fewer LPs and greater recorded propagator time, unchanged solved sets,
and no demonstrated overall speedup. It confines these conclusions to the
selected cohort, short limits, and shared machine, without asserting a
statistically established slowdown. The measured policy does not test the
protected-box or matrix-tail machinery. The precursor study remains separate,
with numerical stopping distinguished from exact fixedness and corrected solved
counts distinguished from unchanged archived timing summaries. The discussion's
final-solve sentence agrees with the experimental section. The cost-accounting
section explains why fewer LPs and movement bounds do not predict search time.

Attribution consistently assigns classical filtering, duality, parametric LP,
fixed-point reasoning, and contraction ingredients to prior work. The claimed
contributions are the specified OBBT tangent formulations, exact model rates
and stall conditions, coefficient expansion, certificate formulations and
scope, and empirical evaluation. No broad priority claim was found. This review
does not independently clear source attribution: the sole literature lead's
final audit and the already requested algorithm citations remain separate work.
The literature audit read here still has its preliminary status note.

An expert can follow the section motivations before the formal definitions
and results. The long constraints section has a useful contract table, and the
algorithm contract table prevents confusion about exact and numerical claims.
No TODO, placeholder, agent/process prose, or private-path proof substitute was
found in the included manuscript sources. The entry point is anonymous, and
the supplementary archive and companion documentation exist. Length alone is
not a scientific blocker under the user's accepted large-paper scope; target
journal style, page limits, and final typeset layout remain submission matters.

## Scope, checks, and source identity

Read `AGENTS.md`, `evidence/BRIEF.md`, `main.tex`, the complete front matter and
discussion, substantial body statements and connecting explanations, the four
accepted r2 scope reports, and `review-opus-foundations-r1.md`. Also inspected
the supplied literature audit and companion documentation. This is an
integration review, not another proof-by-proof audit or an independent source
search.

Targeted commands actually run were `rg --files`, `rg -n`, `cat`, numbered
`sed -n` reads, and one `python3 -I -B -` source read that recorded UTC time,
line counts, and SHA-256 hashes from the same in-memory source bytes. All were
read-only. No experiment, solver, archived analyzer, LaTeX build, project-wide
verification, CI status/log inspection, or literature research was performed.
Only this report was written.

The live files directly involved in the remaining summary/revision work had
these SHA-256 values at the final snapshot:

```text
61662117e1809bd20016c0e00cd88d1698b03720424d104fdc4ad2cb5bd4bbca  main.tex
bebd515ea94db952b1b47099a33678b2032d38ad0923641a503e9b5f4291e9e0  abstract.tex
212a9cf8a9258e21a6805ca62109c74453eef221979b5bd98c2fa6af3bded1ba  sections/introduction.tex
8fd759b1e339e427003eb346fdc3ba2533bc8c96c5b951b5e868a52eed0a98d9  sections/related.tex
5da4f4725c0cd0e25896d625da9047b79e2e3e9704f8ff1697bf72504e203fc5  sections/discussion.tex
825ccbd5c15a5ef19cc06eb27a9d25112e446f57d32273a3d4f35ae51418d58b  sections/foundations.tex
8980d76a4a5af79fcedb2dfe77e5ca75ee4f67bfd4a62bce18060383918d2cff  sections/algorithms.tex
```
