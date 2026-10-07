# Integration review, round 2

**Accepted in the focused integration scope.** The revised front matter closes
all four required r1 correction groups and the recommended factor, parameter,
threshold, and abstract-length edits. No remaining material front-to-body
mismatch was found. This does not clear the pending literature audit or changes
that have not yet been made.

The front snapshot was read at **2026-10-06 02:23:03 UTC**. Its hashes were
confirmed in the subsequent focused check. This review assessed the landed
revision without waiting for the author's release report.

| R1 finding | R2 conclusion |
| --- | --- |
| Fixedness versus protection; value of an unchanged round | Discussion lines 7–17 distinguish fixedness of the certified box from protection inside a containing box, acknowledge useful dual information, and retain tightening outside the minimizers' hull. The unsupported branching prescription is gone. |
| Upper scaling bounds and certificate expiry | Introduction lines 131–137 and discussion lines 69–83 use upper orders, identify the sharp quadratic example separately, and distinguish expiry of the pool's proof from the full-relaxation box threshold. These match the rate/floor and face-threshold statements. |
| Monotonicity and observed histories | Discussion lines 123–129 restrict monotonicity to the iteration, rate, and future-round results and explicitly exclude one-round screens and dual validation. Lines 59–66 preserve nesting's bound and the exact-zero-residual exception. |
| Certificate discovery and reuse | Discussion lines 107–112 recognize cheap certificates and say that reuse *may* be needed when discovery is expensive. The experiments are explicitly separated from these certificates. |
| Strict factors, cutoff and quadratic parameter domains | Introduction lines 52–61 specify `lambda in (r*,1)`, a sufficiently small start, the gauge, `U >= f*`, and `0 < abs(a) < 2`. These agree with the corresponding body results. |
| Strict versus nonstrict thresholds | Introduction lines 168–170 and related-work lines 62–71 distinguish the identical numerical threshold from different strictness and clarify failure of the sufficient scalar condition. |
| Abstract length and experimental scope | The abstract has 248 whitespace tokens when each inline mathematical expression counts as one and the environment commands are omitted. It preserves current-round-only evaluation, no additional solve, and no demonstrated speedup. |

The new singleton discussion is sound. An exactly feasible optimal incumbent
inside the current box supplies a protected singleton, even when iterates reach
it only asymptotically. Its endpoint ceilings are exact when that singleton is
the limit; the text states that qualification and does not equate certificate
existence with finite algorithmic arrival.

The revised contribution paragraph separates the theoretical certificates from
the evaluated scheduling policy. The negative empirical interpretation remains
measured: fewer auxiliary LPs, greater recorded propagator time, no extra solve,
and no demonstrated total speedup. Exact reference checking and conditional
numerical bounds remain distinct. No new broad priority claim was introduced.

The structural moves improve the main text without obscuring the arguments.
`main.tex` includes both new appendices. The introduction's organization
paragraph names them accurately; constraints directs readers to the two moved
parametric proofs; effort retains the assumptions and scope of the scheduling
results and points to their appendix. The appended proofs and scheduling
statements retain their labels and supply the named material. The forthcoming
verbatim relocation of numerical validation was not present and is not covered
by this acceptance.

One optional precision edit remains: in discussion lines 107–109, qualify
“the optima of a completed exact round” with “when they pass the rebuilt-row
check.” The preceding exact-check wording makes the present sentence readable,
but the added words would directly recall that round optima are not
automatically protected witnesses, as the body counterexample shows. This is
not a material blocker.

The pending M1 source audit remains assigned to the sole literature lead. No
independent citation clearance was attempted. Forthcoming vetted predecessor
paragraphs, software metadata, numerical-validation relocation, final typeset
layout, and target-journal formatting lie outside this snapshot. The accepted
body proofs were not re-audited.

Verification consisted of targeted numbered source reads, `rg --files`,
`rg -n` searches for the affected phrases and appendix references, and
`python3 -I -B -` reads for UTC/source identity and the stated abstract count.
The obsolete-phrase search returned no matches. No experiment, solver,
literature research, build, project-wide check, or CI inspection was performed.
Only this report was written.

Reviewed source SHA-256 values:

```text
936850a9957179a5d82b734c92c7bf2916a9d37c26ef42c3a46cbb47739a7b15  main.tex
f75cb5164d64ebc45ae450352fab170a68e99c1199589cc9f369ca02ea4fea4d  abstract.tex
e8ec10762d7a60e00877773204212f8ee8c5d2adf83f5b0464fac22511ec13d4  sections/introduction.tex
3ca85ac3dc8a001ce22b97511f490b82330ece6a3c297cc78c9428afc4dde7ed  sections/related.tex
cb886311c5814ac3f8210f4a0f888a33df81015aaa7a7227ffbe5be99e392cda  sections/discussion.tex
1a75a74507989ac98cddf6815993175d66540e10154dda24916a406117951e82  sections/effort.tex
ae8ad2d7a960904d5b2822b5487ea8d74a706c57892be4cbe51165f166acb9d2  sections/constraints.tex
fb85846b03ea612cec88f1200f96fc7ed786b2abae418108de9897d5d472b956  sections/algorithms.tex
de079f21574486bd3e0fa5f914d857279dc1a328b2c5bfda8f088a1337bfbd75  sections/local-rates.tex
ca8717986aad87156b02328832adbe13765b973ac98b9acfb3f779a26318e318  sections/cutoff.tex
f26e7f76d4ce48e1bda03711a2f7c42d055f75e162968b00bf518b232524c3fe  sections/residual.tex
a4b1c8b1121d170d8ef793884fad0ef1103dae17cbb5c5b2c0a08716d4d1e6b1  appendices/parametric-proofs.tex
03109bf8cf22c3012bd2f60925c36af35a9ecf73e676b4148fa176c42199bf36  appendices/scheduling.tex
```
