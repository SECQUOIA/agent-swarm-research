# Review record: aggregation certificates for a trivial convex hull

Subject: [results/quadratic-aggregation-trivial-hull-certificate.md](../results/quadratic-aggregation-trivial-hull-certificate.md)
(proof of Conjecture 3.3 of Blekherman–Dey–Sun, SIAM J. Optim. 2024).

**Status after the ten-agent corrective audit (2026-09-22).** Independent
rechecks found no error in the main theorem, but found a false claim that
globally convex aggregations recover every valid linear inequality. This has
been replaced by the theorem's existence-only guarantee and a counterexample.
The HHC-versus-stable-convexity example and numerical SDP qualifications were
also corrected. See [the corrective audit](review-minlp-developments-20260922.md).

## Independent adversarial review (2026-09-21, subagent, read-only)

Checked: transcription of Conjecture 3.3 and of Definition 2.1 (HHC) against
the local full text; every step of the proof of Theorem 1 (easy direction,
Lemmas 1–3, Steps 1–3); the three corollaries; the Section 5 example; attempts
at counterexamples.

Verdict: proof correct as written; no fatal or substantive gap. The reviewer
identified the genuinely new content as Steps 2–3 (sweeping the supporting
hyperplane to infinity and the uniform separation constant of Lemma 3), not
found in BDS (whose Section 6 stops at Proposition 2.13) or in Yildiran's
pencil-based `m = 2` argument. Significance assessed as modest but real: a
complete answer to a stated open question, with a weaker hypothesis and no
dimension restriction.

Which hypothesis each step needs (reviewer's summary): hyperplane convexity
near infinity is used in Step 1 (fails in the Section 5 example); `S`
nonempty is used only for `c* < 0` in Step 2 (the single constraint `f_1 = 1`
has `S` empty, `conv(S)` proper, and only the trivial certificate); `conv(S)`
proper is used in Lemma 2's `t = 0` case; finite generation of `P` is used for
closedness in Lemma 3.

Cosmetic corrections requested and applied:

1. Discard indices with `s_k < max(beta, 1)` so that Step 1 never divides by
   `s_k = 0`.
2. Corollary 2 now assumes `n >= 3` (Theorem 2.8 of BDS needs it), with the
   `n = 2` situation stated.
3. Corollary 3 now carries the exact-arithmetic caveat for the SDP decision
   procedure.
4. "separable example" corrected to "example" (the Section 5 example has an
   `x_1 x_2` term).
5. The summary now quotes Theorem 2.8 with its `n >= 3` hypothesis.
6. Remark 3 cites BDS Lemma 5.3 with "cf." (that lemma assumes exactly one
   negative eigenvalue).
7. Lemma 3 stated for closed cones (convexity of `D` unused).

Additional observation from the reviewer, incorporated: the three-constraint
system `x_1^2 - x_2^2 - 1`, `x_2^2 - x_1^2 - 1`, `x_1 x_2 - 1` already shows
that hidden convexity of `f^h` on `R^{n+1}` does not suffice (`x_1 + x_2` is
bounded on `S`, all convex certificates trivial).

## Numerical checks

`code/quadratic_aggregation/check_examples.py` (see its README): example
verification and `m = 2` consistency tests. These exercise only the known
`m = 2` case and the explicit example; they are sanity checks, not evidence
for the general argument.

## Not done

At the time of the original reviews, no Lean formalization had been done.
The second review and subsequent corrective audit are recorded below and
above, respectively. This historical limitation is superseded for Theorem 1
and Lemmas 1–3 by the formal verification record below; the corollaries and
examples remain outside that package.

## Lean verification (2026-09-22)

[Topic 27](../formal/topics/27-quadratic-aggregation/README.md) proves the
main equivalence under asymptotic hyperplane convexity, the HHC
specialization, and all three supporting lemmas. Independent reviews checked
the concrete matrix definitions, quantifiers, source correspondence, cone
closedness, and the final assembly. No unresolved findings remain.

The proof eliminates the constant term using one strict feasible point,
then normalizes the quadratic and linear coefficients and takes one compact
subsequence. This proves the actual existence of a nontrivial certificate
without eigenvalue estimates or an assumed limiting-certificate premise.
The source note now records this alternative as Section 3.4.

The [targeted verification](../formal/topics/27-quadratic-aggregation/VERIFICATION.md)
passed warning-free builds of all 11 modules, an audit of 178 owned
declarations, and every module's kernel replay. Only `propext`,
`Classical.choice`, and `Quot.sound` occur as axiom dependencies.
This does not certify the ancillary corollaries, examples, numerical
software, literature priority, or the developing manuscript as a whole.

## Second independent review (2026-09-22, subagent, read-only): Corollaries 4 and 5

Confirmed: the inclusion `P_SDP ⊆ {f_lambda <= 0}` for convex certificates
(Schur complement, trace of PSD matrices), properness of `{f_lambda <= 0}`,
the perturbation matrices `M_i(s)` of the hyperplanes near infinity, openness
of positive definiteness, the Dines and Polyak citations (Polyak 1998 Theorem
2.1 needs `n >= 3`; the two-variable map `(x_1^2 - x_2^2, 2 x_1 x_2, x_1^2 + x_2^2)`
shows why), the dimension bookkeeping with BDS Corollary 2.6(2), and the
revised scope remark (the lifting `E_0 in span` via a Schur complement).

Error found (low–medium): the parenthetical after Corollary 4 claimed that
`P_SDP` equals the closure of the intersection of convex aggregations. The
intersection is already closed and exact equality fails in general
(`f_1 = 2 x_1 x_2 + 1`, `f_2 = x_1^2`: intersection is a line, `P_SDP` empty).
The correct facts are `P_SDP ⊆ intersection` always and equality of closures
when `S` is nonempty (Fujie–Kojima 1997, Theorem 2.1; Kojima–Tuncel 2000,
Theorem 4.2). The Section 5 claim `P_SDP = R^3` silently used the unproved
direction. Fix adopted: the reviewer's hypothesis-free Lemma 4 (`S` nonempty:
`P_SDP = R^n` iff every convex certificate is trivial), proved by the conic
bipolar theorem and the quadratic midpoint identity; the author verified the
identity `f((a+b)/2) = f(a)/2 + f(b)/2 - g(a-b)/4` and the inclusion
`cl C + int C ⊆ int C`.

Counterexample attempts against Corollary 5(2) were blocked for the reason
given in the scope remark. Significance assessment: the corollaries are
presentational (checkable hypotheses, connection to relaxation strength), the
mathematical content being Theorem 1.

## Author's addition after the reviews (2026-09-22)

The closed-system example `T = {x_1 x_2 = 1, |x_1| <= |x_2|}` in `R^3` (strict
system empty, hull proper with interior, HHC, only trivial certificates, no
good aggregation) shows that Corollary 1 needs the strict system to be feasible
and that the hypothesis `Q_lambda != 0` of BDS Theorem 2.23 cannot be dropped.
Numerical check: `code/quadratic_aggregation/check_closed_example.py`. Not yet
independently reviewed.

## Verified consequences and boundary examples (2026-09-22)

[Topic 28](../formal/topics/28-quadratic-aggregation-consequences/README.md)
now proves Corollaries 1, 3 and 4, Lemma 4, and the closed-system and strip
counterexamples with actual HHC. Its 10 new modules passed warning-free
builds, an audit of 158 owned declarations, and all kernel replays.
Independent reviews found no unresolved mathematical or statement issues.

The formal proof of Lemma 4 separates the affine PSD image directly from
the strict negative orthant and constructs strict covariance slacks at
every point. It does not assume closedness of a PSD image or projection.
The finite SDP tests include exact optimum attainment and infeasibility,
not numerical solver certification. Corollaries 2 and 5 and other examples
remain outside these packages. See the [verification record](../formal/topics/28-quadratic-aggregation-consequences/VERIFICATION.md).

## Recommended infinite-aggregation follow-up

[Topic 29](../formal/topics/29-infinite-aggregation/README.md) is also complete.
It proves actual HHC for the explicit three-inequality system in every
`2r` variables with `r≥2`, classifies good multipliers using genuine
homogeneous eigenvalue counts, and verifies the strict-ray and finite
closed-hull obstructions. Eighteen modules, 248 audited declarations and
all kernel replays passed, with independent semantic reviews. Its
[verification record](../formal/topics/29-infinite-aggregation/VERIFICATION.md)
and [paper supplement](../paper-quadratic-aggregation/formal-infinite-aggregation.tex)
state the exact scope. This does not formalize the external full hull theorem,
exact hull formula, arbitrary-quadratic obstruction, or quantitative claims.

## Exact hull and accuracy follow-ups

The user-selected [topic 30](../formal/topics/30-infinite-aggregation-hull/README.md)
and [topic 31](../formal/topics/31-aggregation-accuracy/README.md) are complete.
Together they add 25 modules and 325 audited declarations, with independent
semantic reviews and all targeted builds and kernel replays passing. The
first proves the exact hull and SDP lifts by a direct two-point argument
for every `r≥2`; the second proves the uniform Hausdorff bounds, rational
cut construction, coefficient sizes and actual tolerance budgets. The
arbitrary-quadratic obstruction, general Gram-map theorem and separate
single-objective proposition remain outside these packages.
