# Focused mathematical review, round 3

Date: 2026-10-05. Scope: the revised `ex:mixing-hull` and
`prop:continue` in `sections/cutoff.tex`, and the numerical-safe-step
paragraph in `sections/certificates.tex`. No manuscript file was edited.
This report supersedes round 2's acceptance of the old mixing-hull
explanation and the unnecessarily restricted continuation result.

**Final disposition:** all three revised arguments are correct, and no
unresolved finding remains in this focused scope. The empty-input
convention is now explicit; see the final verification below.

## Mixing example: accepted

In `cutoff.tex:142`, the frozen relaxation is

```text
R([-1,1]) = {(x,s): -1 <= x <= 1, 2|x|-1 <= s <= 1},  v=s.
```

Mixing `(±1,1)` with `(0,0)` to cutoff `1/4` gives `(±1/4,1/4)`.
On the rebuilt hull `[-1/4,1/4]`, the rows are
`s >= |x|/2 - 1/16` and `s <= 1/16`. At each endpoint the projected
value is `1/16`, so the recomputed lifts `(±1/4,1/16)` prove protection
at cutoff `1/4`. The stored lifts fail only because of their old square
coordinate. The text now distinguishes these two statements correctly.
The frozen cutoff set is `[-5/8,5/8]`, since
`2|x|-1 <= 1/4`; thus the exact decrease is `3/8` per endpoint, while
the mixed points supply the valid upper ceiling `3/4`.

The second construction is a genuine failure of protection. The minimum
of `s` in the stated frozen relaxation is `-1`, attained at `(0,-1)`.
Mixing it with the graph endpoints to cutoff `0` gives coefficient `1/2`
and points `(±1/2,0)`. The frozen cutoff set is exactly `[-1/2,1/2]`.
On its rebuilt hull, the lower envelope is `|x|-1/4` and the secant is
`s <= 1/4`. Hence the projected value at either face is `1/4 > 0`,
regardless of the auxiliary lift. The rebuilt cutoff set is
`[-1/4,1/4]`. All asserted values and inclusions are correct.

## Continuing versus restarting: accepted, with the empty convention

The revised `prop:continue` at `cutoff.tex:297` has the right finite-step
premise. For intermediate boxes `D_0=B_0,...,D_m=C_0` and cutoffs
`V_j >= U'`, soundness and order give

```text
D_(j+1) contains T_(V_j)(D_j), which contains T_(U')(D_j).
```

Induction yields `B'_j` contained in `D_j`, and therefore
`B'_(k+m)` contained in `C_k`. The upper inclusion follows from
`C_0` contained in `B_0`. Both bounding restart sequences have the same
intersection because removing a finite prefix of a nested sequence
does not change its intersection. This argument needs neither
closedness nor `U' >= f*`, and covers `m=0`.

The result requires finitely many relaxation-sound steps for this finite
lag bound. It does not authorize earlier changes of relaxation family,
arbitrary propagation, branching, or steps at a cutoff below `U'`.
The following paragraph correctly reserves the identification of the
common intersection with the greatest fixed box for nonempty iterates
and `eq:closed-family`.

**Convention clarification: resolved.** At the initial reviewed snapshot,
`foundations.tex:123` defined `hull(empty)=empty`, and empty directional
updates were absorbing. The Jacobi operator was not explicitly extended
to empty input, although `prop:continue` allows an empty iterate and
applies further powers of `T`. I requested this sentence beside
`eq:operator`:

```text
We set K_U(emptyset)=T_U(emptyset)=emptyset for every cutoff U.
```

With the now explicit extension, order and both sandwich inclusions hold
after emptiness as well. If a restart iterate is empty, the corresponding
continue iterate is empty; if a continue iterate is empty, the restart
iterate at most `m` indices later is empty. This is a formal definition
clarification, not a false inclusion or a counterexample to the proof.

## Numerical-safe steps: accepted

`certificates.tex:186--194` now ties conservative endpoint movement to
proved support bounds. A certified lower bound `a <= min x_i` permits
the update `ell'_i=max(ell_i,a)`, which remains at most the exact lower
support. A certified lower bound `b <= min(-x_i)` permits
`u'_i=min(u_i,-b)`, which remains at least the exact upper support.
For simultaneous selected endpoints these inequalities imply
`T_U(C)` contained in `C'` contained in `C`; rebuilt sequential updates
apply the same argument at each step.

The cited dual-residual proposition supplies such support bounds when
its verified finite variable box and directed-rounding assumptions hold.
Simply rounding a reported primal optimum outward does not establish
either required inequality. The revised paragraph states this distinction
correctly and does not claim an exact round or a valid upper residual
from conservative numerical movement.

## Snapshot and verification

The reviewed source SHA-256 values were:

```text
a4373749b2d769e600d364c4ae67f173a5fafbc966e95ce89647f71cbcbbb9db  sections/certificates.tex
ca8717986aad87156b02328832adbe13765b973ac98b9acfb3f779a26318e318  sections/cutoff.tex
f26e7f76d4ce48e1bda03711a2f7c42d055f75e162968b00bf518b232524c3fe  sections/residual.tex
```

The residual hash records the current integration snapshot; the structural
move of history examples was outside this focused mathematical check.
I read Opus findings m1/m2, the revised passages, the operator and order
definitions, and the cited dual-residual statement. Targeted source reads
used `nl` and `sed`, including `cutoff.tex:108--182,279--345`,
`certificates.tex:48--125,174--195`, and `foundations.tex:63--151`.
Additional commands actually run were:

```sh
rg -n -C 12 'numerical|safe|sound|rounded' sections/certificates.tex
rg -n -C 7 'empty|varnothing|T_U|directional|sequential' sections/foundations.tex
rg -n -A 51 -B 3 '### m1|### m2' evidence/review-opus-full-r1.md
rg -n -A 75 -B 6 'label\{prop:dual-residual\}' sections/algorithms.tex
sha256sum sections/certificates.tex sections/cutoff.tex sections/residual.tex
```

All example calculations above were checked algebraically. No solver,
experiment, numerical campaign, literature search, LaTeX build,
project-wide verification, or CI inspection was run.

Final follow-up: I read only `foundations.tex:123--127` using
`nl -ba sections/foundations.tex | sed -n '123,127p'` and ran
`sha256sum sections/foundations.tex`. The text now explicitly sets
`K_U(emptyset)=T_U(emptyset)=emptyset` and states that repeated rounds
remain defined after an empty cutoff set. The clarification is fully
resolved. The final checked foundation hash is:

```text
f30184c925375bf1f37300ce465057216656d36aadfdb9bed0c5476d009bb10d  sections/foundations.tex
```
