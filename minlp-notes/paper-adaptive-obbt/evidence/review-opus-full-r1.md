# Full manuscript review, round 1 (Opus)

Reviewer role: independent full-manuscript reviewer. This review was read-only.
I wrote only this file and edited no manuscript, evidence, or companion file.
I did not run experiments, project-wide verification, or CI, and I did no
literature searching. Source requests for the literature lead are in Section 7.

## Snapshots reviewed

The manuscript changed continuously while I reviewed it. I read every input of
`main.tex` in full at least once, and the core sections twice. I then compared
three local snapshots and reread every change.

| Snapshot (UTC, 2026-10-06) | Content |
| --- | --- |
| 01:2x (first read) | Core sections and the proof appendix, before the front matter existed |
| 01:37 (`snap1`) | Core sections plus the first introduction |
| 01:44 (`snap2`) | All inputs, including abstract, related work, discussion, and both appendices; read in full |
| 01:55 (`snap3`) | Final check of the diffs since `snap2` |

These are the `snap3` SHA-256 prefixes. Line numbers below refer to `snap3`
unless stated otherwise.

```
61662117e180 main.tex               bebd515ea94d abstract.tex
233454b81543 references.bib         8980d76a4a5a sections/algorithms.tex
274823fd9740 sections/certificates  b9a855c6486a sections/constraints.tex
042b81c05557 sections/cutoff.tex    5da4f4725c0c sections/discussion.tex
ca0ba9755fdf sections/effort.tex    b47a48120a9e sections/experiments.tex
825ccbd5c15a sections/foundations   212a9cf8a925 sections/introduction.tex
30a09df4b845 sections/local-rates   8fd759b1e339 sections/related.tex
49703b1836c1 sections/residual.tex  5d764d0cb323 appendices/local-proofs.tex
625d05a78116 appendices/precursor-study.tex
```

All front-matter files exist and are included. The precursor appendix is now
input by `main.tex`. No front-matter file is pending.

## 1. Verdict

**Not yet submission-ready. The mathematics is close to submission quality, but
the literature work and some structure and positioning are not.**

- **Mathematics.** In the final snapshot I found no false theorem,
  proposition, or lemma statement. The audited repairs have been integrated,
  including all 21 items listed in Section 8. Two new mathematical problems
  remain, both small and both repairable here (m1, m2): one worked example
  states a false conclusion, and one proposition carries unnecessary
  hypotheses and a misleading lead-in.
- **Blocking: literature (M1).** The literature audit is still marked
  "preliminary ... in progress". Sixteen of the 29 cited keys are not in the
  literature lead's vetted file (as of 01:58 UTC; see the addendum). Several attributions to specific source
  content therefore lack a completed audit.
- **Required: positioning (M2).** One contribution sentence still overstates
  what the measured policy has to do with the theory. One introduction
  sentence credits the experiments with a conclusion that only the effort
  section establishes.
- **Strongly recommended: structure (M3).** The paper is 91 pages: about 80
  pages of main text and 11 of appendices. Several messages are repeated across
  sections, and some elementary material sits in the main line. A
  consolidation plan is in Section 6. Splitting into separate papers is not
  necessary.

Once M1 and M2 and the minor items in Section 4 are fixed, I would support
submission. M3 would make the paper markedly easier to referee.

## 2. Accepted central results

I checked each proof listed in Section 9 and accept these results under their
stated assumptions in the final snapshot.

1. **Order foundations** (`foundations.tex`).
   - `lem:order`; `lem:sequential` (a)–(c). Part (c), the
     fair-schedule limit, is proved without closedness.
   - `lem:sublevel-hull`; `lem:fixed-persist`.
   - `prop:fixed-limit`, under nonempty iterates plus `eq:closed-family`.
   - `ex:not-fixed`.
   - The exact scalar example after `lem:sequential` replaces the archived
     0.705 attribution. Sequential factor `(9+sqrt17)/32` against Jacobi
     factor `1/2`; I rechecked the recurrence, its validity conditions, and the
     invariant ratio interval `[7/12,3/4]`.
   - The two independent inclusions `H_U ⊆ B_∞` and `P ⊆ B_∞ ⊆ B_k`, with the
     example `φ ≡ 0`.
2. **Local theory** (`local-rates.tex` and Appendix A).
   - Tangent model and map, `lem:tangent-properties`, `lem:cw`,
     `thm:tangent-contraction`, `cor:tangent-rate`.
   - `prop:tangent-eigenrate`, including the `ρ=0` case.
   - `thm:local-stall` with a strict margin; `cor:face-test`, now stated as
     sufficient tests.
   - `ex:critical-scalar`: r*=1, `h_k~2/k`, floor `ε^{1/3}`. It matches
     `proposed-critical-example.tex`, which I verified line by line.
   - The quadratic exact model with `prop:two-variable-rate`,
     `prop:rectangle-map`, `prop:asymmetric-eigenboxes`,
     `prop:two-variable-cutoff-floor`, and `prop:quadratic-rows`. Their
     numerical values all recheck.
   - `ex:many-term`: exact rate and stall threshold `a(n−1)(n−2) ≥ 2`.
     `ex:signed-stall`: value `−1/32` and the row bound. Also
     `ex:shape-change` and `ex:finite-square`.
   - `thm:composite-expansion`, including the upper product rule and the
     complete appendix proof.
   - `lem:boundary-step` and `thm:boundary`: repaired terminal case, upper
     enclosure only, and both counterexamples.
   - `cor:local-gap`.
3. **Certificates** (`certificates.tex`, `cutoff.tex`, `residual.tex`).
   - Current-round ceilings, `thm:protected`, `prop:fixed-box` (finite and
     rational completeness for a prescribed box), `prop:join`,
     `cor:limit-ceilings`, `cor:objective-ceiling`, `cor:original-points`,
     and `prop:integer-rounding`.
   - `prop:round-check`, now with lifted points (see the note in Section 8),
     and `ex:round-check`.
   - `prop:face-threshold`, `prop:box-threshold`, `prop:mixing`,
     `prop:frontier`, `prop:cutoff-response`, and `ex:frontier`.
   - `thm:residual`: an ordered comparison, no spectral premise, and the
     upper-residual after-round bound. Also `prop:least-majorant`,
     `prop:fixed-point-shift`, `ex:heron`, and `prop:history`.
4. **Constraints** (`constraints.tex`).
   - Dual envelope and cutoff multiplier; exact basis regions, now phrased
     correctly for the gradient of an affine piece.
   - Bracket and no-change threshold, with the endpoint premise now included.
   - Frozen rows, corrected stored dual, and the rebuilt-basis derivative.
   - `thm:cover-con` with `prop:coverage-con`, and `cor:residual-input-con`.
   - `ex:switch-con`; `prop:equality-con`; `prop:restricted-tangent-con`,
     including the `t=0` case and the declared cutoff.
   - `thm:repair-con` and `cor:repair-rate-con`. In `ex:graph-con`, all
     constants recheck: μ=63/64, β=1/4, τ=1/64, L=1/2048, λ0²=43/672, factors
     25/48 and 1/3; tangent variant 9/64, 13/63, 3/4.
5. **Algorithms and effort.**
   - `lem:lp-certificate`; `thm:closure` (a)–(e), including the Heron
     iterates `21523361/21523360`; `prop:row-correction`;
     `prop:dual-residual` with its dual derivation; `lem:enclosure`;
     `prop:sidecar-validity` and its cutoff caveat.
   - `prop:ledger` and its concurrency counterexample; `prop:no-comparison`;
     `thm:interleaving`; `cor:equal-shares`; `prop:rescue`.
6. **Experiments.** All values I could reconstruct from the displayed numbers
   are internally consistent:
   - Mean PAR-2 per arm from the solved-run totals:
     (34.21+520)/40, (39.52+520)/40, (39.88+520)/40.
   - The `tab:work` sums; 20.9% and 18.4%; about 17 ms and 6 ms; "about a third"
     and "more than half".
   - Public gap scores without `bayes2_50`: 0.274, 0.282, 0.289.
   - 117 incumbents, 39 pairs, 78 time-limited runs.
   - Precursor ranges against `tab:precursor-solver`.

   I did not reread raw records; `review-evidence-r1.md` did. The negative
   finding is reported and interpreted honestly. The text never claims a
   statistically established slowdown.

## 3. Major issues

### M1. The literature audit is incomplete (blocking)

`evidence/literature-audit.md` still says "preliminary author guidance while
the targeted source review is in progress". The brief requires related work to
follow that audit. In the final snapshot these points remain open:

1. **Fifteen cited keys are not in `evidence/literature-references.bib`:**
   `badilla2024tradeoffs`, `belotti2012fbbt`, `borrelli2003parametric`,
   `cengil2025learning`, `chmiela2023scheduling`, `coramin2023filters`,
   `gomezcasares2025domain`, `gonzalezdiaz2025lifted`, `hay2012computations`,
   `hendel2018adaptive`, `jachymski2016perov`, `pineda2025sweetspot`,
   `scip2026obbt`, `tarski1955fixpoint`, `walker2011anderson`. I checked this
   by comparing the cited keys with the vetted file.
2. **Several sentences attribute specific content to sources and need
   page-level confirmation:**
   - Caprara–Locatelli: one-variable iteration equals a parametric
     reduction; order independence of cyclic sweeps (`related.tex` 26–31).
   - Caprara–Locatelli–Monaci: two-variable class reached by mixed reduction;
     no-move examples (32–37).
   - Belotti et al.: infinite FBBT iteration and the limit computed by one LP
     (41–46).
   - Gleixner et al.: "a call that tightens nothing can still yield a useful
     dual inequality" (14–16).
   - SCIP: budget tied to root LP effort; genvbound reevaluation (16–18);
     default propagator settings in `experiments.tex` 91–93.
   - Coramin: aggregate-objective filter (19–20).
   - Scott–Stuber–Barton: the exact monotonicity hypotheses (`related.tex`
     80–83; `local-rates.tex` 841–846).
   - Wechsung–Schaber–Barton `K ≤ λ1/8` and Kannan–Barton `τ* ≤ γ/8`
     (`local-rates.tex` 101–109).
3. **Bibliography metadata.**
   - `tarski1955fixpoint` points to a third-party copy; use DOI
     10.2140/pjm.1955.5.285.
   - `borrelli2003parametric` and `jachymski2016perov` use personal download
     URLs; use DOI or stable links.
   - `belotti2012fbbt`, `hendel2018adaptive`, and `chmiela2023scheduling` are
     cited as manuscripts or preprints and may have published versions. The
     literature lead should decide which to cite.
4. **Possibly missing prior work and attributions.** These are requests only;
   Section 7 lists them for the literature lead. The literature audit does not
   cover them:
   - Iterated OBBT run to a fixed point in power-systems relaxations.
   - A domain-reduction survey.
   - Safe LP bounds from inexact duals, for `prop:dual-residual`.
   - Nonlinear Perron–Frobenius and Collatz–Wielandt terminology, for `r^*`.
   - McCormick–Taylor convergence order.

Until the literature lead's final audit lands, the qualified contribution
statement (`introduction.tex` 162–171) and the related-work comparisons are
not verified. They are worded cautiously; I found no priority claim.

### M2. Two positioning sentences overstate the link between theory and policy (required)

1. **`introduction.tex` 167–168:** "... and the evaluation of a policy built
   on these ideas." The measured policy uses only established current-round
   screening (Gleixner et al.) plus heuristic triggers and a pilot. Every
   other passage says so (abstract, `algorithms.tex` 592–608,
   `experiments.tex` interpretation). A contribution list is where referees
   look for overclaiming. Replace with:

   > ..., the finite certificate formulations together with their scope, and
   > a prospective evaluation of an adaptive scheduling policy that uses only
   > current-round screening and heuristic triggers, not the all-future
   > certificates.

2. **`introduction.tex` 138–140:** "They do show that the number of auxiliary
   LPs is not a cost measure and that a bound on width or on the remaining
   tightening is not a bound on search time." The experiments show the first
   point. The second is the conceptual result of `prop:no-comparison` and the
   discussion after it; no measured run used a certificate. Replace with:

   > They show that the number of auxiliary LPs is not a cost measure, and
   > Section~\ref{sec:effort} shows why a bound on width or on remaining
   > tightening cannot by itself bound search time.

### M3. Structure and repetition (strongly recommended)

The integrated paper is coherent, but it has three kinds of redundancy.
Section 6 gives the full plan.

1. **The "measured policy does not use the certificates" statement appears
   about eight times:**
   - abstract and introduction;
   - `certificates.tex` 627–633;
   - `residual.tex` 376–378;
   - `constraints.tex` 782 and 1276–1284;
   - `algorithms.tex` 592–608;
   - `experiments.tex` interpretation;
   - discussion.

   The brief asks for this to be stated once clearly and then maintained, and
   warns against repetitive warnings.
2. **"Observed progress cannot certify" is spread over four places:**
   - `local-rates.tex` 1189–1204;
   - `residual.tex` §7.6 (`prop:history`, `ex:ratio`);
   - `constraints.tex` §8.8 (`ex:long-history-con`, `ex:small-ratio-con`);
   - discussion 46–52.

   Cross-references also point to the wrong section:
   `local-rates.tex` 1201 and `discussion.tex` 49–51 cite
   Section~\ref{sec:constraints} for "identical histories", but the general
   result is `prop:history` in Section~\ref{sec:residual}.
3. **A local-rate theorem sits in the constraints section.**
   `rem:linear-equations` (in `local-rates`) and
   `prop:restricted-tangent-con` (in `constraints` §8.6) state the same
   result: one as a remark, the other as a theorem.

## 4. Open minor issues

Each item gives a location and a fix.

### m1. `ex:mixing-hull` states a false conclusion

Location: `cutoff.tex` 139–150 (example and lead-in).

The example is titled "Mixed witnesses do not protect their hull" and shows
only that the stored lifted points `(±1/4,1/4)` fail the rebuilt secant
`s ≤ 1/16`. Under the paper's projected definition of a witness pool,
`def:protected` (`certificates.tex` 194–200), the hull `[-1/4,1/4]` *is*
protected at cutoff `1/4`:

- On `[-1/4,1/4]` the rows are `s ≥ |x|/2 − 1/16` and `s ≤ 1/16`, so
  `φ(±1/4) = 1/16 ≤ 1/4`.
- The recomputed lifts `(±1/4,1/16)` pass the rebuilt check.
- In fact every point of the hull lies in the cutoff set, and the iteration
  limit at cutoff 1/4 is `[-1/2,1/2]`, which contains the hull.

The example therefore shows only that stored auxiliary coordinates cannot be
reused. That is the lifted-reuse point already made by `ex:lambda`; it is not
non-protection. Corrected example, using the same family:

> Relax $s=x^2$ on $[-1,1]$ by $s\ge2|x|-1$ and $s\le1$, with objective
> $v=s$. Mixing the graph points $(\pm1,1)$ with the anchor $(0,0)$ to
> $U'=1/4$ gives the points $(\pm1/4,1/4)$. They bound the frozen round at
> cutoff $1/4$ by $3/4$ per endpoint, whereas the exact round gives
> $[-5/8,5/8]$. Their stored lifts fail the secant $s\le1/16$ rebuilt on
> $[-1/4,1/4]$. Their projections nevertheless lie in $K_{1/4}([-1/4,1/4])$
> with the lifts $(\pm1/4,1/16)$, so the hull is protected once lifts are
> recomputed. A hull of mixed points need not be protected, however. Mixing
> the same graph points with the minimizer $(0,-1)$ of $v$ over $R([-1,1])$ to
> the cutoff $0$ gives $\theta=1/2$ and the points $(\pm1/2,0)$. These are
> exact current-round witnesses (the first round of
> Example~\ref{ex:halving}). On their hull $[-1/2,1/2]$, however,
> $\phi(\pm1/2)=1/4>0$, so the hull is not fixed, and the next round gives
> $[-1/4,1/4]$.

Retitle the example, for instance "Mixed witnesses at a new cutoff". Keep
"generally not protected" only with the second instance.

### m2. `prop:continue` has unnecessary hypotheses and a misleading lead-in

Location: `cutoff.tex` 280–302. The lead-in says "under the closedness
condition ... both reach the same limit", and the statement assumes
`f* ≤ U'` and `eq:closed-family`. Neither is needed. Corrected statement and
proof:

> **Proposition (Continuing versus restarting).** Let $U'\le U$, let
> $B'_k=T_{U'}^k(B_0)$, and let $C_0\subseteq B_0$ be obtained from $B_0$ by
> $m$ relaxation-sound steps at cutoffs at least $U'$, for example by OBBT at
> the old cutoff $U$. Then $C_k=T_{U'}^k(C_0)$ satisfies
> $B'_{k+m}\subseteq C_k\subseteq B'_k$ for all $k$. In particular,
> $\bigcap_kC_k=\bigcap_kB'_k$.
>
> *Proof.* A relaxation-sound step $C\to C'$ at a cutoff $U''\ge U'$ gives
> $C'\supseteq T_{U''}(C)\supseteq T_{U'}(C)$ by Lemma~\ref{lem:order}(c).
> Induction and monotonicity of $T_{U'}$ give $C_0\supseteq T_{U'}^m(B_0)$,
> hence $C_k\supseteq T_{U'}^{k+m}(B_0)$. The upper inclusion follows from
> $C_0\subseteq B_0$. $\square$

Under `eq:closed-family` and nonempty iterates, the common limit is
additionally the greatest fixed box (`prop:fixed-limit`). The same
sandwich argument is used in `lem:sequential`(c), so the result belongs
naturally beside it.

### m3. The "Starting" paragraph of the discussion overgeneralizes

Location: `discussion.tex` 7–24.

- **(a)** "it remains valid for every larger cutoff and every box that contains
  the certified one" (8–10) conflates two claims. In a containing box the
  certificate no longer proves that a round is useless; it bounds movement.
- **(b)** "Outside such situations, nothing in the results guarantees that a
  first round helps" (21–22) is false if "helps" means "tightens". Several
  results guarantee movement:
  - `prop:box-threshold`: strict movement when `U < τ(P)`;
  - `prop:dual-envelope-con` and `cor:cutoff-multiplier-con`: a guaranteed
    reduction;
  - `thm:tangent-contraction`;
  - `cor:repair-rate-con`: "guaranteed progress".
- **(c)** "branching that separates the minimizers comes first" (14–15) is
  advice rather than a result.

Suggested replacement:

> A round cannot move a box that is already fixed for the given relaxation
> and cutoff, and a finite certificate proves this
> (Section~\ref{sec:certificates}). The certificate remains valid at every
> larger cutoff. In every box that contains the certified box it no longer
> proves a stall but bounds the total movement of all later rounds. Two
> structural situations produce fixed boxes. If a model has several global
> minimizers, for example by symmetry, every iterate contains their hull and
> cannot converge to a point (Lemma~\ref{lem:sublevel-hull}); only branching
> that separates them removes this obstruction. If ... [row-condition
> sentence unchanged]. In other situations some results guarantee movement of
> the operator: the box threshold of Proposition~\ref{prop:box-threshold}, a
> stored dual bound below the current endpoint
> (Corollary~\ref{cor:cutoff-multiplier-con}), or the contraction premises
> of Section~\ref{sec:local-rates}. None guarantees that the movement
> shortens the search, and Section~\ref{sec:effort} shows ...

### m4. "Scales like" overstates upper bounds

Location: `discussion.tex` 54–57 ("The limit box scales like √ε and the
remaining relaxation gap like ε under the contraction hypotheses").
`cor:tangent-rate` and `cor:local-gap` give upper bounds `O(√ε)` and `O(ε)`.
Order exactly `√ε` requires the extra premises of `cor:tangent-rate`. Both
quantities are exact only in `prop:two-variable-cutoff-floor`. Use "is at most
of order", as `local-rates.tex` 1162–1187 now does.

### m5. The ε = 0 stopping discussion omits the natural certificate

Location: `local-rates.tex` 1214–1220; `discussion.tex` 41–45; introduction
121–123.

At `ε=0` the incumbent `x̂` is a global minimizer. Suppose it is the minimizer
`x*` toward which the iterates contract, and it lies in the current box. Then
`{x̂}` is protected (`cor:original-points`) and its ceilings equal the
remaining movement exactly. This is exactly `ex:sharp-halving`, and
`certificates.tex` 609–617 already says so. The three passages name only the
residual certificate. Add one sentence, for example:

> When the optimal incumbent lies in the current box, its protected singleton
> (Corollary~\ref{cor:original-points}) bounds the remaining movement, exactly
> if the iterates converge to it; a residual certificate is needed when no
> such inner box is available.

Also add "These regimes need not cover every relaxation family
(Example~\ref{ex:critical-scalar})" to the discussion's "Stopping" paragraph,
as `local-rates.tex` 1221–1222 already does.

### m6. "Numerically safe OBBT whose computed bounds are rounded outward"

Location: `certificates.tex` 189–192. Rounding a floating-point optimum outward
does not by itself guarantee that an endpoint stays outside its exact support.
The step is relaxation-sound when the bound is proved, for example by
`prop:dual-residual` evaluated with directed rounding. Write:

> ... numerically safe OBBT whose bounds are proved by safe dual bounds
> (Proposition~\ref{prop:dual-residual}), which never move an endpoint past
> its exact support.

`residual.tex` 179 is fine as written.

### m7. The cutoff threshold sentence in the introduction is ambiguous

Location: `introduction.tex` 124–127 ("the cutoff threshold of a certificate
states exactly when a certified stop ceases to be valid"). Two thresholds are
involved:

- `τ_Ŵ(P)` says when the stored witnesses stop covering the faces.
- `τ(P)` says when the box itself stops being fixed.

The same applies to `discussion.tex` 60–63. Name the two thresholds or say
"when the stored witnesses cease to certify the stop".

### m8. Abstract precision

Location: `abstract.tex` 15–16. Replace "Tangent points with negative value on
every face certify stalling" with:

> Points of the tangent model with negative value that attain every face of
> a box shape certify stalling at every sufficiently small scale.

### m9. Dichotomy wording

- `local-rates.tex` 339, "We turn to the opposite regime": write "We now give a
  sufficient condition under which fixed boxes exist at every small scale."
- `local-rates.tex` 714, the title of `ex:many-term` ("An exact dichotomy") is
  accurate only within that family. In a paper that stresses non-exhaustive
  criteria, prefer "A family with an exact stall threshold".

### m10. Make the start-box hypothesis of `cor:local-gap` explicit

Location: `local-rates.tex` 1134–1137. The proof uses
`B_∞ ⊆ x*+t_ε D(u)`. That inclusion needs `g_u(B_0) ≤ t̄` from
`thm:tangent-contraction`(b), not only the hypotheses of part (a). State
"Under the hypotheses of Theorem~\ref{thm:tangent-contraction}(b)".

### m11. Precursor appendix: qualify the Jacobi/sequential and filtering comparisons

Location: `precursor-study.tex` 216–225. `audit-evidence.md` records that some
Gauss–Seidel/Jacobi and filtering comparison counts depend on a tolerance and
on code that is not in the saved analysis script. Add one clause: "these
comparison totals are taken from the archived report; part of their code is
not in the saved analysis script."

### m12. Precursor statement in the discussion

Location: `discussion.tex` 79–81, "mostly on instances that were already
solved in seconds". `precursor-study.tex` 170–172 correctly speaks of the
group means. Write "with the largest mean reductions in groups whose mean
control time was a few seconds".

### m13. The per-callback cost is an allocation

Location: `effort.tex` 36–40. The 17 ms figure is non-LP sidecar time per
admitted callback, including trigger visits that admitted no callback
(`experiments.tex` 311–314). Write "there the non-LP time per admitted
callback was about three times the time of one LP with its validation".

A one-line consistency check is worth adding:

```
ΔL = 453, ΔC = 337
c1·ΔL ≈ 2.7 s,  c0·ΔC ≈ 5.7 s   →  predicted net ≈ 3.0 s
observed sidecar increase: 3.59 s
```

### m14. Terminology and notation

- **"Sidecar"** (`algorithms.tex` 287–289, used 18 times) is an invented
  label, which the brief asks to avoid. Use "the added propagator" throughout,
  as `experiments.tex` mostly does.
- **"Archived"** appears very often in `experiments.tex` and the precursor
  appendix. One sentence on provenance plus "archived records" where needed is
  enough.
- **Start-box notation:** the start box is `B_0` in local-rates and certificates
  but `B_0'` in `prop:restricted-tangent-con` and `cor:repair-rate-con`. Use
  one convention.

### m15. Packaging (outside the manuscript)

`README.md` links `submission-source.zip`, which does not exist yet. `main.pdf`
now exists. This is root packaging, not a manuscript issue.

## 5. Corrected statements and proofs supplied in this review

- Section 4 m1: a corrected `ex:mixing-hull` that keeps the lifted-reuse point
  and adds a genuine non-protected hull.
- Section 4 m2: `prop:continue` without closedness and without `U'≥f*`,
  stated as the sandwich `B'_{k+m} ⊆ C_k ⊆ B'_k`, with a three-line proof.
- Section 4 m3 and m5: replacement text for the discussion and for the ε=0
  stopping passages.
- Section 3 M2: replacement contribution sentence and evidence sentence.

## 6. Structure plan: one coherent large paper, no split

Current page layout from a temporary build: introduction 1–4, related work
4–5, foundations 5–11, local rates 11–27, certificates 27–35, cutoff 35–39,
residual 39–45, constraints 45–61, algorithms 61–70, effort 70–73,
experiments 73–79, discussion 79–81, Appendix A 81–86, Appendix B 86–91.

The paper is long but not too long for its scope. Its main line would be
clearer with these changes. Together they move about 8–10 pages to appendices
and remove about 1–2 pages of repetition.

1. **One statement of what the measured policy implements.**
   - Keep it in the abstract, one introduction sentence, `algorithms.tex`
     §9.4.5 (the authoritative version, with reasons), one sentence in
     `experiments.tex` §11.5, and one in the discussion.
   - Delete the closing disclaimers at `certificates.tex` 627–633,
     `residual.tex` 376–378, `constraints.tex` 782, and `constraints.tex`
     1276–1284. Move the sentence there about SCIP's native OBBT remaining
     active to §11.2.
2. **One home for observed-progress results.**
   - Keep `prop:history` and `ex:ratio` in §7.6. Move
     `ex:long-history-con` and `ex:small-ratio-con` there, or to an appendix,
     since both are instances of the construction in `prop:history`.
   - Keep `ex:switch-con` in §8.5 as the McCormick instance.
   - Point local-rates §4.7 and the discussion to §7.6.
3. **Local-rate theory in the local-rate section.**
   - Turn `rem:linear-equations` into `prop:restricted-tangent-con`, with
     proof, in §4.3.
   - Keep `prop:equality-con` in §8.6 as the worked constrained example, or
     move it too.
   - Section 8 then covers LP information, basis regions, covers, and repair.
4. **Appendix moves that keep statements in the main text:**
   - **Floating-point validation, §9.4.2** (`prop:row-correction`,
     `prop:dual-residual`, `lem:enclosure`, the three-pass evaluation; about
     2.5 pp). Keep `prop:sidecar-validity` and the cutoff caveat in §9.4.
   - **Scheduling guarantees, §10.4–10.5** (`thm:interleaving`,
     `cor:equal-shares`, `prop:rescue`, `ex:history`; about 1.5 pp). These are
     elementary, and the section itself claims no novelty for them. Keep
     §10.1–10.3 and one paragraph pointing to the appendix. `ex:history` can
     become a sentence.
   - **Proofs of `thm:cover-con` and `prop:coverage-con`** (about 1.5 pp).
   - **Proofs of `prop:rectangle-map` and `prop:asymmetric-eigenboxes`**
     (about 1 pp). Optional.
5. **Optional:** fold the `c_0`/`c_1` trade-off of §10.1 into §11.4, where it
   is measured (see m13).

None of these changes alters a result. A split into separate papers is not
needed, and I do not recommend it.

## 7. Source requests for the literature lead

These are requests only; I searched for nothing.

1. **Final audit status.** Complete `literature-audit.md`, then vet or
   replace the 15 unvetted keys listed in M1 (content and metadata),
   including DOIs and published versions.
2. **Page-level confirmation of the attributions listed in M1.2.** This
   includes the exact form and constants of the Wechsung–Schaber–Barton and
   Kannan–Barton no-clustering conditions.
3. **Iterated OBBT to a fixed point in power-systems relaxations.** Check
   whether these should be credited in related work, since "repeat OBBT
   until no change" is standard practice there:
   - Coffrin, Hijazi, and Van Hentenryck (2015), CP;
   - QC-relaxation OBBT papers by Sundar, Nagarajan, and coauthors;
   - Nagarajan et al. (2019), adaptive multivariate partitioning with OBBT.
4. **A domain-reduction survey:** Puranik and Sahinidis (2017),
   *Constraints* 22. Also check whether Ryoo and Sahinidis (1996) or BARON
   papers are the right attribution for optimality-based range reduction.
5. **Safe LP bounds and exact LP**, for `prop:dual-residual`,
   `lem:lp-certificate`, and rational reconstruction:
   - Neumaier and Shcherbina (2004);
   - Jansson (2004);
   - Applegate, Cook, Dash, and Espinoza (2007);
   - Gleixner, Steffy, and Wolter (2016).
6. **Collatz–Wielandt terminology for `r^*`:** nonlinear Perron–Frobenius
   theory, for example Lemmens and Nussbaum (2012), or a Collatz–Wielandt
   formula paper for order-preserving homogeneous maps. The proofs are
   elementary, but the borrowed term should be credited.
7. **Convergence order of McCormick–Taylor models:** Bompadre, Mitsos, and
   Chachuat (2013). This bears on the qualified claim that the
   shape-dependent second-order expansion is new.
8. **Software, data, and metrics:**
   - SCIP 10 report (already in the local KB per `author-algorithms.md`),
     including its OBBT defaults;
   - PySCIPOpt; HiGHS; MINLPLib; OSiL;
   - PAR-2;
   - the shifted geometric mean (Achterberg 2007).
9. **Algorithm portfolios and interleaving**, for `thm:interleaving` and
   `prop:rescue`: Luby, Sinclair, and Zuckerman (1993); Huberman, Lukose, and
   Hogg (1997); Gomes and Selman (2001).

## 8. Status of earlier findings in the final snapshot

All of these are **fixed**. They were integrated during this round, and I
rechecked each one against `snap3`.

**Foundations**

1. The false chain `H_U ⊆ P ⊆ B_∞` is replaced by two independent inclusions
   and an example.
2. The archived 0.705 sequential factor is removed from foundations and local
   rates and replaced by an exact analytic scalar example.
3. Selective rounds now carry a lower enclosure `T_U^m(B) ⊆ C_m`.
4. The fair-schedule limit is proved without closedness.
5. The symmetry wording now says "cannot converge to a single point ...
   tightening can still remove parts outside the hull".
6. A global incumbent outside the node box is handled in foundations,
   certificates, and residual.

**Local rates and appendix**

7. Dichotomy language is gone from foundations §3.4 and local-rates;
   `ex:critical-scalar` is added; the face tests are labeled sufficient; the
   introduction states that the conditions are not exhaustive.
8. The boundary free gauge is an upper enclosure, with a counterexample; `η_k`
   is qualified; appendix (iv) handles a negative numerator; the
   sign-selection case is completed; start-box admissibility is stated.
9. Generic floors are upper bounds; the scope of incumbent improvement is
   corrected; a single minimizer is not enough; `M>0`; the `ρ=0` collapse is
   handled; the round-count bound uses `max(0, ceil)`; the exact interval
   uses `r/(1+r)`; the nonsmooth-factor caution is added.

**Certificates, cutoff, residual**

10. The `−∞` fiber passage is removed, and so are the duplicate limit theorem
    and its `(L1)`/`(L2)` premises.
11. `ex:lambda` has objective `v=s`; `ex:inactive` is defined on every subbox;
    `prop:history` has no negative indices; `ex:heron` has its error identity;
    the rational-solve premise is stated; the empty-cutoff-set case after
    `prop:box-threshold` is handled; frontier pools are nonempty.
12. `prop:round-check` now uses lifted points. The earlier projected version
    was not shown by `ex:round-check`: the projection `x=1/2` lies in
    `K_U(B')` through the lift `(1/2,1/4)`. Fixed in `snap3`.

**Constraints** (`review-constraints-r1` R1–R4)

13. Piece gradient versus support derivative at a shared boundary.
14. An unchanged support versus an unchanged endpoint.
15. The limit of `prop:equality-con` for every starting radius, and "converges
    to" rather than "reaches".
16. `t=0` and the declared cutoff in `prop:restricted-tangent-con`.
17. The crude-estimate wording.
18. The corrected dual restricted to `u∈[1,2]`.

**Evidence** (`review-evidence-r1` items 1–10)

19. Four unbounded public models; the precursor ρ is defined on the moving
    subset; overhead shares are aggregates (the per-run maximum stated as
    1.00501 s); "changed search" is corrected; the probing-node
    interpretation is labeled with its source; rounding 39.52 and 5.23; the
    1 ms LP floor; the pilot gain is measured before integer rounding; the
    discovery cost "can exceed"; control/r5 counts 573/563; trajectory
    classification 97/7 and 22+1; group-mean wording in the appendix.

**Integration**

20. Undefined labels and citations are fixed. The source checker passes
    (Section 10).
21. The introduction paragraph linking rates and certificates no longer says
    a certificate needs positive width.

**Open in `snap3`:** M1–M3 and m1–m14 above. m1 (the mixing example) and m2
(`prop:continue`) are new in this review. Every other open item is a
precision or wording issue.

## 9. Proof coverage actually reviewed

I read and checked every proof in these labels, including every displayed
computation in the worked examples.

- **Foundations:** `lem:order`, `lem:sequential`, `lem:sublevel-hull`,
  `lem:fixed-persist`, `prop:fixed-limit`, the lifted closedness argument,
  `ex:not-fixed`, the scalar Jacobi/sequential example, and the §3.4 example.
- **Local rates:**
  - Scalar bounds and tangent machinery: `prop:sharp-growth`,
    `prop:quadratic-growth`, `lem:tangent-properties`, `lem:cw`,
    `thm:tangent-contraction`, `cor:tangent-rate`, `prop:tangent-eigenrate`,
    `thm:local-stall`, `cor:face-test`, `ex:critical-scalar` (and the
    proposed insertion), `rem:linear-equations`.
  - Quadratic models: `eq:quadratic-Q`, `eq:cube-Q`, `prop:two-variable-rate`
    (with the four decimals), `prop:rectangle-map` (with the example
    factors), `prop:asymmetric-eigenboxes` (with the interval),
    `prop:two-variable-cutoff-floor`, `prop:quadratic-rows`.
  - Quadratic examples: `ex:many-term`, `ex:signed-stall`, `ex:shape-change`,
    `ex:finite-square`.
  - Composite McCormick: the product `cv` and `cc` rules, and
    `thm:composite-expansion` with the full Appendix A.1 (five lemmas;
    product interval, relaxation, and dominance; univariate cases;
    remainder; clipping).
  - Boundary: `lem:boundary-step` and `thm:boundary` with the full Appendix
    A.2, both counterexamples, `ex:boundary`, and `cor:local-gap`.
- **Certificates:**
  - `lem:reference-family`, `ex:lambda`, `prop:current-round`, `ex:halving`,
    `thm:protected`, `prop:fixed-box`, `prop:join`, `cor:limit-ceilings`,
    `ex:sharp-halving`.
  - `cor:objective-ceiling`, `ex:three-variable` (every row of every
    witness), `cor:original-points`, `prop:integer-rounding`, the
    fractional-face and cut examples, `ex:child` (bound 1/2 and its attaining
    lift), `prop:round-check`, `ex:round-check`.
- **Cutoff:** `prop:face-threshold`, `prop:box-threshold`, `prop:mixing`,
  `ex:mixing-hull` (see m1), `prop:frontier`, `prop:cutoff-response`,
  `ex:frontier`, `prop:continue` (see m2).
- **Residual:** `lem:invariant-interval`, `thm:residual`,
  `prop:least-majorant`, `ex:inactive`, `cor:witness-residual`, `ex:heron`,
  `cor:cutoff-tail`, `prop:fixed-point-shift`, `ex:ratio`, `prop:history`.
- **Constraints:**
  - LP duality and basis regions: `prop:dual-envelope-con`,
    `cor:cutoff-multiplier-con`, `prop:basis-region-con` (both directions),
    `ex:cutoff-con`, `prop:bracket-con`, `prop:threshold-con`,
    `ex:cutoff-bracket-con`.
  - Rebuilt rows and covers: `lem:frozen-con`, `ex:rebuilt-dual-con`,
    `prop:corrected-dual-con`, `prop:rebuilt-basis-con`, the McCormick slack
    derivatives, `thm:cover-con`, `prop:coverage-con`,
    `cor:residual-input-con`, `ex:switch-con`.
  - Equality and repair: `prop:equality-con`, `prop:restricted-tangent-con`,
    `thm:repair-con`, `cor:repair-rate-con`, `ex:graph-con` (and the
    tangent variant).
  - Histories: `ex:long-history-con`, `ex:small-ratio-con`.
- **Algorithms:** `lem:lp-certificate`, `thm:closure`, the arithmetic of
  `tab:closure-runs`, `prop:row-correction`, `prop:dual-residual`,
  `lem:enclosure`, the three-pass argument (at the level of rounding-monotone
  steps), `prop:sidecar-validity`.
- **Effort:** `prop:ledger`, the concurrency counterexample,
  `prop:no-comparison`, `thm:interleaving`, `cor:equal-shares` (the
  time-share inequalities), `prop:rescue`, `ex:history`.

**Not independently verified:**

- archived raw records and the saved CSV/JSON (relied on
  `review-evidence-r1.md` and `audit-evidence.md`);
- SCIP source facts;
- every IEEE overflow corner of the three-pass evaluation;
- all source-content attributions (literature-lead scope).

## 10. Verification actually performed

These are targeted, read-only checks. None is a project-wide check or a CI
check. I inspected no CI status or logs.

1. **Reading.** `cat`, `sed -n`, `grep`, `diff`, and the Read tool on:
   - `AGENTS.md` and `evidence/BRIEF.md`;
   - `INTEGRATION-NOTES.md` (before and after its update), `COVERAGE.md`,
     `literature-audit.md`, `literature-references.bib`, `audit-evidence.md`;
   - all five `review-*-r1.md` files, both author reports, and
     `proposed-critical-example.tex`;
   - key sections of the three remaining audits;
   - every manuscript input and `references.bib`.
2. **Snapshots and diffs.** `cp` of the manuscript sources into
   `/tmp/obbt-review/snap{1,2,3}`, followed by `diff` and `sha256sum` between
   snapshots.
3. **Source checker.** `python3 -I verification/check_sources.py`, which only
   reads files. At the first run it reported missing front matter, undefined
   `sec:precursor-details`, and missing keys `caprara2010domain` and
   `gleixner2017enhancements`. At the later run it reported
   `SOURCE_CHECK=ok: 16 TeX files, 237 labels, 28 citations`.
4. **Disposable build.** I copied the sources to `/tmp/obbt-review/build`
   and ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`.
   It exited 0 with 91 pages and no warning, undefined reference, or overfull
   box. The section start pages in Section 6 come from that build's
   `main.aux`.
5. **Citation keys.** A shell comparison of the cited keys with
   `references.bib` (28 entries, 28 cited, none uncited) and with
   `literature-references.bib` (15 unvetted keys, listed in M1).
6. **Analytic checks.** All mathematical checks in Sections 2, 4, and 9 were
   done by hand. I executed no archived solver, analyzer, fixture, or
   numerical experiment.

These are document and analytic checks, distinct from any CI result.

## Addendum (01:58 UTC)

After `snap3`, two files changed. `experiments.tex` 266–274 now cites
release-tagged SCIP 10.0.2 source for the node numbering, instead of the 10.0.3
remark. The labeling of probing nodes is now explicitly an interpretation:
"the logs did not record node types". That resolves the probing-provenance
caveat.

`references.bib` gained `scip1002tree`. It is the 16th cited key not in
`literature-references.bib`, so the M1 list grows by one. It is a software
citation and can be vetted with the other two (`scip2026obbt`,
`coramin2023filters`).

I reran `python3 -I verification/check_sources.py`. It reported
`SOURCE_CHECK=ok: 16 TeX files, 237 labels, 29 citations`. No other open item
in Sections 3–4 changed.
