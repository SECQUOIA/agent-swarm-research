# Foundations review, round 2

## Scope and snapshot

This focused read-only review checks the developments requested in
`review-opus-foundations-r1.md`, findings F1, F2, and F4: the moving-tangent
example, the greatest fixed box, the revised limit proposition,
decreasing-sequence continuity, joint lower semicontinuity, and independence
of closedness and monotonicity. I also checked the original sublevel-hull
argument, the corrected inclusion chain, and the empty-set convention.
I did not re-review the unchanged local-rate or algorithm material.

The substantive manuscript snapshot was read at 2026-10-06 02:14:08 UTC.
The released notation changes were checked at 02:19:32 UTC.

| File | SHA-256 |
| --- | --- |
| `sections/foundations.tex`, substantive snapshot | `8e9fdef9e3eed75d8244a02a76974e038a8f7c73218f707a1fb3d6afa91a5173` |
| `sections/foundations.tex`, final accepted release | `f30184c925375bf1f37300ce465057216656d36aadfdb9bed0c5476d009bb10d` |
| `evidence/review-opus-foundations-r1.md` | `31ca27b804d59cd12c39188a8ee6aedb3b4eb512d088fa6d8de5074bd271910e` |

Line references in the substantive checks refer to the first snapshot.
The new formal results and proofs pass. The initial notation scope issue
described below is resolved in the accepted release. The requested
empty-input convention was already present in the first snapshot.
There are no remaining mathematical findings within this review's scope.

## Checks of the new developments

### Five-point moving-tangent example: correct

At lines 88–101, minimizing the lift `y` gives exactly
`phi_B(x)=max_k(2 p_k x-p_k^2)`. Each tangent is below `x^2`, and `x^2`
is below the secant on the box, so the lift at that maximum is feasible.
The rows form a compact lifted set on every bounded box.

At `x=0`, the old knots include zero, whereas the new nearest knot is
`-1/8`. The projected values are therefore `0` and `-1/64`, respectively.
This disproves projected monotonicity using a construction determined by
the box alone.

For `U=1/4`, a positive tangent knot gives the upper constraint
`x<=(p^2+1/4)/(2p)`, and a negative knot gives the corresponding lower
constraint. On `[-1,1]`, the knots `p=±1/2` give the endpoints `±1/2`.
On `[-1/2,1]`, the positive-knot upper bounds are `5/8`, `41/80`, and
`5/8`; the negative knots give lower bounds `-1/2` and `-17/16`.
Intersecting with the original interval gives `[-1/2,41/80]`.

At the stated lifted point `(41/80,1/4)`, the five new tangent values are
`-61/80`, `-23/160`, `31/160`, `1/4`, and `1/40`; the new secant is
`121/160`. Every new row holds. The old tangent at `1/2` has value
`21/80>1/4`, so it excludes the point. This establishes the operator
failure as well as the projected failure. The statement about endpoint
tangents alone is correct for the reference square family.

### Original sublevel hull and greatest fixed box: correct

The sublevel-hull proof at lines 242–258 does not need continuity of `f`
or attainment of faces by original sublevel points. With
`S={x in X cap B_0:f(x)<=U}`, validity gives

\[
 S\subseteq K_U(H_U)\subseteq H_U.
\]

Taking closed box hulls gives
`H_U=box S subseteq T_U(H_U) subseteq H_U`. The family is defined on
every subbox of `B_0`, so building it on `H_U` is allowed. The argument
proves fixedness whenever the hull is nonempty; the empty convention
also gives fixedness of the empty set as an operator element.

The arbitrary-family lemma at lines 309–326 is sound. Its hull `Q` is a
nonempty bounded closed box in `B_0`. Monotonicity gives
`P=T_U(P) subseteq T_U(Q)` for every member `P` of the family. Thus the
closed box `T_U(Q)` contains their entire union and its closed box hull
`Q`. Containment supplies the reverse inclusion. This proof handles
infinite families without requiring attainment of the union's extremal
coordinates. Applying it to all nonempty fixed boxes gives the claimed
greatest box, and persistence puts it in every Jacobi iterate.

The lattice statement at lines 330–336 is algebraically correct. Joins
are closed box hulls of unions; meets are intersections, including empty
intersections and empty results. The added absorbing empty element makes
`T_U` a map on this complete lattice. Literature attribution was not
independently searched or reviewed.

The corrected chain at lines 433–437 is correct whenever a fixed box `P`
is under discussion:
`H_U cup P subseteq P_U subseteq B_infty subseteq B_k`.
The example with `f=x^2`, `phi_B=0`, and `U=0` also checks: every subbox
is fixed, `H_U={0}`, `P={1}` is fixed, and the greatest fixed box and the
Jacobi limit both equal the initial interval.

### Closed-limit proposition and decreasing-sequence identity: correct

The proposition at lines 338–370 correctly assumes nonempty Jacobi
iterates, rather than requiring original cutoff points. Its unconditional
conclusions follow from compact nesting, sublevel preservation, the
greatest-fixed-box lemma when applicable, and the fair-schedule sandwich.

For the fixedness conclusion, the coordinate support on `B_k` is attained
because `K_U(B_k)` is nonempty compact. Its witness lies in bounded
`B_0`, so a subsequence converges. Apply the closed-family condition to
that nested subsequence of boxes. The witness coordinate converges to the
corresponding endpoint of `B_infty`; hence every endpoint of the limiting
box is attained in its cutoff set. This proves fixedness and, by
greatestness and persistence, equality with `P_U`.

The identity at lines 373–376 is also correct under the standing
monotonicity assumption. A complete argument covering empty cases is:

1. If any `K_U(C_k)` is empty, monotonicity makes every later cutoff set
   empty and puts `K_U(C)` inside it. Both sides of the claimed identity
   are empty.
2. Otherwise the cutoff sets are nested nonempty compact subsets of
   bounded `C_0`. Monotonicity and the closed-family condition imply
   `K_U(C)=intersection_k K_U(C_k)`: apply the condition to a constant
   point sequence for the nontrivial inclusion.
3. For each coordinate, choose minima and maxima on these sets. Compactness
   supplies cluster points in their intersection that attain the limits
   of the monotone support values. Taking closed box hulls therefore
   commutes with this decreasing intersection.

If one of the input boxes is empty, step 1 applies directly through the
explicit convention. Consequently
`T_U(intersection_k C_k)=intersection_k T_U(C_k)` holds in all cases
covered by the stated domain.

### Joint lower semicontinuity and independence: correct

At lines 377–382, joint lower semicontinuity is understood on the domain
`{(x,ell,u):ell<=x<=u}` with admissible box endpoints. The endpoint limits
of nonempty nested bounded boxes define their intersection. Thus the
displayed liminf argument proves closedness, including extended projected
values and degenerate limiting boxes. No continuity of the original
objective is needed. The objective-only termwise quadratic construction
in item (a) is jointly continuous because its envelope planes have
continuous endpoint coefficients.

The compact lifted argument at lines 384–391 is sound and uses the
attainment assumed earlier. A common compact set is essential for the
subsequence of lifts; it is stated explicitly here.

For the independence claim, the moving-tangent projected objective is the
maximum of five continuous functions of `(x,ell,u)`, so it is jointly
continuous and satisfies closedness, although it is not monotone. The
next example is monotone but fails closedness: take its iteration boxes
`C_k=[0,s_k]` and points `x_k=g(s_k)`. Then `x_k in K_0(C_k)` and
`x_k ->1/2`, but the limiting cutoff set is `[0,1/8]`.
The added conclusions `P_U=H_U={0}` and the second infinite sequence
`[0,1/8],[0,1/32],...` are correct.

### Empty-box convention: present and sufficient

Lines 124–126 explicitly set `K_U(emptyset)=T_U(emptyset)=emptyset`.
Lines 148–149 make directional updates absorbing at the empty set.
Support optimization is defined only when the cutoff set is nonempty.
These conventions cover the order lemma, repeated operator powers,
fair schedules, the lattice statement, and the decreasing-sequence
identity. There is no remaining empty-input gap in the reviewed snapshot.

## Resolved notation scope clarification

Summary item (ii), lines 425–429, refers to “the greatest of them,
`P_U`” without repeating the existence condition. The new lemma defines
`P_U` only if a nonempty fixed box exists, and the enlarged limit
proposition correctly retains that condition. Nonempty iterates alone
do not ensure that a nonempty fixed box exists without closedness.

For example, let `B_0=[0,1]`, `X={0}`, `f=0`, and `U=-1`. On a
positive-width box `[r,s]`, set the projected value to `-1` when
`x<=s/2` and to `0` otherwise; on every singleton set it to `0`.
The family is valid, monotone, and lower semicontinuous on each box.
Every positive-width cutoff set is `[r,s] cap [0,s/2]`, so no such box
is fixed, and every singleton has an empty cutoff set. Nevertheless,
Jacobi from `[0,1]` produces the nonempty boxes `[0,2^{-k}]`.
Here `H_U` is empty and there is no nonempty `P_U`.

The main setting `U>=f^*` avoids this issue, because the nonempty original
sublevel hull is fixed. The accepted release resolves the broader notation
scope by defining `P_U=emptyset` when there is no nonempty fixed box.

### Released-sentence confirmation

At 2026-10-06 02:19:32 UTC I checked only the changed lemma, its empty-case
proof sentences, the simplified limit statement and proof introduction,
and the summary inclusions. These correspond to release lines 309–377
and 428–445. The accepted digest is
`f30184c925375bf1f37300ce465057216656d36aadfdb9bed0c5476d009bb10d`.

- The lemma defines `P_U` for the empty family and calls it the greatest
  fixed box only when nonempty. Its proof applies persistence only in
  that case and treats empty containment directly. The assertion
  `H_U subseteq P_U` also holds for empty `H_U`.
- On the augmented lattice, the empty case is a fixed point because
  `T_U(emptyset)=emptyset`; if no nonempty fixed box exists, it is the
  greatest fixed point. The lattice paragraph now states this correctly
  without an existence qualifier.
- The limit proposition can now state `P_U subseteq B_infty`
  unconditionally. Closedness proves that the nonempty limit is itself
  a fixed box, so its equality with `P_U` remains valid.
- The summary's empty-iterate parenthesis is correct: persistence would
  prevent an empty iterate if a nonempty fixed box existed. Thus an empty
  iterate implies `P_U=B_infty=emptyset`.

The revised definition preserves the manuscript's definition of a fixed
box as nonempty and supports every unconditional summary inclusion.
The released notation change is accepted; no proof change is needed.

## Verification performed

Only this report was authored. I used `cat
evidence/review-opus-foundations-r1.md`, `nl -ba
sections/foundations.tex`, and `sha256sum sections/foundations.tex
evidence/review-opus-foundations-r1.md`. A targeted Python read computed
the manuscript digest and printed lines 1–155, 309–396, and 400–438 from
the same byte snapshot. All displayed exact fractions and proof steps
were checked analytically.

After the later digest change, the only additional source reads were
`sed -n '119,150p' sections/foundations.tex` and
`sed -n '422,437p' sections/foundations.tex`, followed by the requested
released-sentence Python read of lines 309–377 and 428–445 with its digest
computed from the same bytes.

No computational experiments, solver runs, literature searches, manuscript
builds, project-wide verification, or CI status/log checks were performed.
