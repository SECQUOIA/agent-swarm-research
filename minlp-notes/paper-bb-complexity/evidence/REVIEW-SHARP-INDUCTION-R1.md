# Independent review: the sharp-coordinate induction

Reviewed 2026-10-05. This review covers only the completed induction in
`AUDIT-BRANCHING.md:629–688` and its proof dependencies. It does not review
general higher-dimensional competitiveness, add literature, rerun experiments,
or inspect CI.

## Verdict

**The induction is correct under the intended fixed coordinate-wise oracle
and sharpness assumptions. It can enter the manuscript as a theorem with a
complete proof.** It proves a constant bound for one arbitrary continuous
coordinate and a fixed number of sharp coordinates. The arbitrary coordinate
may be quadratic, nonconvex, or have tied relaxation minima. The result does
not settle competitiveness for arbitrary separable objectives, two arbitrary
coordinates, or the deficit rule with multiple sharp coordinates.

Two clarifications are necessary when stating the theorem:

1. Fix the incumbent at the true minimum, use a positive tolerance, and use
   exact bounds on an unconstrained Cartesian product with a separable
   continuous objective. Fix the minimizer selection as a function of the
   coordinate and its interval. Coordinate-choice ties may be resolved
   arbitrarily.
2. The sentence allowing “any coordinate-wise minimizer selection” at
   `AUDIT-BRANCHING.md:686–688` must mean any such selection **satisfying the
   sharpness assumptions**. Alternatively require the sharpness properties
   for every minimizer, which gives the unqualified selection conclusion.
   Zero gap for a selected one-sided minimizer does not imply zero gap for
   every minimizer of that interval. The standard sharp example has unique
   minimizers and satisfies the stronger version.

The recurrence is conservative, but no smaller constant is needed for the
claim. Its constants are independent of the tolerance, objective, box widths,
kink locations, and positive gaps of the unsplit sharp coordinates. They
depend only on the number of sharp coordinates.

## Source locations and comparison with previous reviews

| Location | Reviewed claim | Finding |
|---|---|---|
| `AUDIT-BRANCHING.md:633–638` | Sharp-coordinate collapse after a kink split | Correct for the selected oracle; every resulting half contains the kink, so its value is exactly zero and its selected gap is zero. |
| `AUDIT-BRANCHING.md:640–647` | Uniform recurrence | Correct: `c_r = r[2r(r+1)+1]`, `A_r = 4(1+c_r)`, `C_0=4`, and `C_r=(A_r+1)+2C_(r-1)(A_r+2)`. |
| `AUDIT-BRANCHING.md:655–663` | Frozen phase and frontier | Correct. Use `kappa=r`, the number of unsplit sharp coordinates, rather than the ambient dimension minus one. Already split sharp coordinates contribute zero. |
| `AUDIT-BRANCHING.md:665–671` | Summed child certificate sizes | Correct. Refining by frontier points gives `sum_j N_Aj(epsilon) <= N+H-1`; this supplies the missing accounting in the original sketch. |
| `AUDIT-BRANCHING.md:673–685` | Induction, termination, and final slice | Correct. Each sharp split removes one unsplit sharp coordinate on both branches, and the slice gives a bound against arbitrary valid box partitions. |
| `separable-omega.md:124–170,172–185` | Model, selection, rules, and benchmarks | These assumptions should accompany the theorem. The manuscript must distinguish valid partitions from guillotine leaf partitions. |
| `separable-omega.md:222–245` | Hereditary bounds and the one-dimensional theorem | Sufficient for the base case and the phase proof. A restricted arbitrary interval need not contain a minimizer of its original coordinate function; nonnegativity is enough. |
| `separable-omega.md:440–508` | Lemma T and Theorem A | The stated constants and both `N>=2` and `N=1` cases check. The proof uses no convexity. |
| `separable-omega.md:602–663` | Definition and two-dimensional theorem | Compatible with the induction. The two-dimensional bound of 56 leaves per one-dimensional certificate is much stronger than the recurrence's first constant. |
| `separable-omega.md:679–690` | Original higher-dimensional sketch | Its budget inequality is correct. State counting alone does not prove the sum bound; the completed recurrence now does. |
| `separable-omega-review.md:75–113,131–178` | Earlier independent review | Confirms the phase lemma and the two-dimensional theorem, but leaves the higher-dimensional summation only indicated. This review supplies the proof of that summation. |

All relative source-note paths in this table are under
`research-20260928b/bb-complexity/branching-competitiveness/`, except the prior
review, which is under `research-20260928b/reviews/`. The audit is under
`paper-bb-complexity/evidence/`.

## Precise statement suitable for the manuscript

Scale the objective and tolerance by the common gap coefficient so that
`alpha=1`. Let the root be a product of nondegenerate compact intervals and
let

```
f(x,z_1,...,z_r) = f* + m_0(x) + sum_(j=1)^r m_j(z_j),
min m_i = 0,                  epsilon > 0.
```

Each coordinate function is continuous. The incumbent is fixed at `f*`.
For a coordinate interval `J=[l,u]`, write

```
q_J(t) = (t-l)(u-t),
F_i(J) = min_(t in J) [m_i(t)-q_J(t)],
y_i(J) = the selected exact minimizer,
w_i(J) = q_J(y_i(J)).
```

The choice of `y_i(J)` depends only on coordinate `i` and `J`. A box is valid
when `epsilon+sum_i F_i(J_i)>=0`. At an invalid box, `omega` splits a
coordinate of largest `w_i` at its selected minimizer.

For `j>=1`, assume a kink `c_j` in the interior of the original sharp
interval such that `m_j(c_j)=0` and:

- on every interval straddling `c_j`, the selected minimizer is `c_j`;
- on every interval lying on one side of `c_j`, including an interval with
  `c_j` as an endpoint, the selected minimizer has zero gap and the relaxation
  value is nonnegative.

These are conditions on the fixed selection. A stronger statement may
require them for every minimizer and then allow every fixed coordinate-wise
selection. The arbitrary coordinate `m_0` needs no sharpness or convexity.

For `A` in the arbitrary coordinate, let `N_A(epsilon)` be the minimum number
of intervals in a partition of `A` satisfying `F_0(J)>=-epsilon`. Define

```
C_0=4,
c_r=r[2r(r+1)+1],
A_r=4(1+c_r),
C_r=(A_r+1)+2 C_(r-1)(A_r+2),                r>=1.
```

Then the algorithm terminates and has at most `C_r N_A(epsilon)` leaves when
started with arbitrary interval `A`, `r` unsplit sharp intervals, and any
already split sharp halves. In particular, for the original root,

```
T_omega <= 2 C_r N_part(epsilon)-1.
```

Here `N_part` is the minimum number of boxes in any valid box partition; a
guillotine restriction is not needed. A constant ratio against the best
binary cut tree follows. If the root is invalid, `N_part>=2`, and

```
T_omega/T_opt <= (4 C_r-1)/3,
T_opt = 2 N_guill-1,                 N_guill>=N_part.
```

If the root is valid, both trees have one node. A leaf-count factor `C_r`
does not give a node-count ratio `C_r` without this conversion.

## Complete induction proof

First, the assumptions give `m_i>=0`. An invalid box has at least one
positive selected gap: if all gaps were zero, every coordinate relaxation
value would equal the nonnegative value of its objective at an endpoint.
Thus the chosen split is strictly interior. The one-dimensional budget
counts are finite at every positive budget, since an interval of length at
most `2 sqrt(epsilon)` is valid. The minimum count exists because a
nonempty set of positive integer certificate counts has a least element.

If a sharp interval is split at its kink, each half has zero relaxation
value: its value is nonnegative by sharpness, and evaluation at the kink
gives an upper bound of zero. Its selected gap is zero. It cannot be selected
on a later invalid box, so it stays fixed at that half. This fact applies on
both sides and to every sharp coordinate.

For `r=0`, all remaining sharp halves have zero value and gap. The algorithm
is exactly the one-dimensional minimizer rule at budget `epsilon`. If
`N_A(epsilon)=1`, the root is valid. Otherwise its number of leaves is at
most `4N_A(epsilon)-4`, and hence at most `C_0 N_A(epsilon)`.

Assume the claim holds with `r-1` unsplit sharp coordinates, and consider a
problem with `r>=1`. Until the first sharp split on a branch, all sharp
intervals are unchanged. For each unsplit coordinate put

```
omega_j=q_Jj(c_j)>0,
tau=max_j omega_j>0,
beta=epsilon-sum_j omega_j,
b=beta+r tau=epsilon+sum_j(tau-omega_j)>=epsilon>0.
```

Every split of the arbitrary coordinate in this initial phase has
`F_0(D)<-beta` and `w_0(D)>=tau`. Therefore this phase is a subtree of the
one-dimensional threshold tree `S(A;beta,tau)` formed by splitting exactly
when those two inequalities hold. Using the fixed coordinate-wise selection
makes this a comparison with the same underlying minimizer tree. An
arbitrary resolution of coordinate-choice ties only removes nodes from that
comparison tree.

The phase lemma with `kappa=r` bounds its internal nodes by

```
4M-5+c_r(4M-4),                     M=N_A(b)>=2,
c_r,                               M=1.
```

Because increasing the budget weakens validity, `M<=N=N_A(epsilon)`. For
`M>=2`, the displayed expression is `A_r M-(5+4c_r)<=A_r N`; for `M=1`,
`c_r<=A_r N`. Hence the initial phase has at most `A_r N` internal nodes.
This also proves it is finite: every finite prefix has that bound.

Stop each branch when it first reaches a valid box or chooses a sharp
coordinate. The resulting finite binary phase tree has a frontier of
`H=I+1` intervals `A_1,...,A_H` that partition `A`, where

```
H<=A_r N+1<=(A_r+1)N.
```

Take a minimum budget-`epsilon` certificate of `A`, with `N` intervals, and
insert the `H-1` interior frontier points. An inserted point creates at most
one additional interval. Validity is hereditary, so every refined piece is
valid at the same budget. Restrict this refined partition to each `A_j`.
These restrictions are certificates, and therefore

```
sum_j N_Aj(epsilon)<=N+H-1<=(A_r+2)N.
```

At a valid frontier box, the final subtree has one leaf. At any other
frontier box, the selected coordinate is sharp and its split at the kink
gives two child problems with exactly `r-1` unsplit sharp coordinates and
the same arbitrary interval `A_j`. The newly split coordinate has zero
value and gap. The induction hypothesis bounds the two subtrees together
by `2 C_(r-1) N_Aj(epsilon)` leaves. Bounding the number of valid frontier
boxes by `H` and summing over all frontier intervals yields

```
L <= H+2 C_(r-1) sum_j N_Aj(epsilon)
  <= [(A_r+1)+2 C_(r-1)(A_r+2)]N
  = C_r N.
```

The induction also proves termination of each remaining child problem.
All estimates use only `r`; no ambient-dimension constant is introduced by
sharp coordinates that have already collapsed.

Finally, intersect any valid box partition of the root with the line on
which all sharp coordinates equal their kinks. A box meeting this line has
`F_j(J_j)<=m_j(c_j)-q_Jj(c_j)<=0` for every sharp coordinate. Its validity
therefore implies `F_0(J_0)>=-epsilon`. Its projections cover `A`. A finite
cover of an interval by hereditary-valid intervals can be converted to a
partition with at most the number of covering intervals: proceed from the
left endpoint, choose a covering interval extending furthest right, and
retain only its previously uncovered suffix. Thus
`N_A(epsilon)<=N_part(epsilon)`. The final binary tree has `T=2L-1`, giving
the claimed node bound.

## Phase-lemma constant check

The completed induction depends on the general integer `kappa` version of
Theorem A, not solely its two-dimensional specialization. I rechecked that
dependence directly.

For a valid interval `ell=[p_0,q_0]` at budget `b=beta+kappa tau`, and a
threshold split interval `D=[p,q]` contained in `ell`, let

```
L=y-p, R=q-y, gL=p-p_0, gR=q_0-q.
```

Validity at `y` and strict invalidity of `D` give

```
L gR+R gL+gL gR < kappa tau <= kappa L R.
```

It follows that `gR<kappa R`, `gL<kappa L`, and
`|D|>|ell|/(kappa+1)`. Along a chain of threshold splits inside `ell`, each
left-child step removes at least `tau/|ell|` from the right, and each
right-child step removes that much from the left. Before a left-child step
whose child is also a split node, the gap inequality gives
`nL L<kappa |ell|`, while that child has length
`L>|ell|/(kappa+1)`. Thus the number of preceding left steps is strictly
less than `kappa(kappa+1)`. There are at most `kappa(kappa+1)` left steps in
the chain, and the same number of right steps. Its number of nodes is at
most `2kappa(kappa+1)+1`.

The terminal split intervals in any finite forest inside `ell` have
disjoint interiors and each has length strictly larger than
`|ell|/(kappa+1)`. There are at most `kappa` of them. The forest is covered
by that many root-to-terminal chains, giving
`c_kappa=kappa[2kappa(kappa+1)+1]` split nodes. The same finite-prefix bound
excludes an infinite forest.

The one-dimensional minimizer tree stopped at budget `b>0` has at most
`4M-5` internal nodes and `4M-4` leaves if `M=N_A(b)>=2`. A threshold-tree
node with `F<-b` is one of those internal nodes, because `F` is
nondecreasing along nested intervals and the selection is the same. Every
other threshold node lies inside a leaf of the budget tree and is charged
by the preceding forest bound. This gives
`4M-5+c_kappa(4M-4)`. If `M=1`, the whole root is valid at budget `b` and
the bound is `c_kappa`. This verifies every phase constant used in the
recurrence.

## Selection caveat: an exact example

The following shows why the final selection sentence needs qualification.
On `[0,1]`, take `c=1/2` and

```
m(t)=t(1/2-t),                  0<=t<=1/2,
m(t)=(t-1/2)(1-t),              1/2<=t<=1.
```

This function is continuous and nonnegative. On every interval straddling
`c`, the relaxation has unique minimizer `c`. Indeed, for `t>c`, the
relaxation difference from its value at `c` is
`(t-c)(3/2-l-u)>0`, and for `t<c` it is
`(c-t)(l+u-1/2)>0`.

On every one-sided interval the relaxation is affine, and an endpoint
selection gives zero gap and nonnegative value, so the coordinate is sharp
for that selection. But on each full half `[0,c]` and `[c,1]` the relaxation
is identically zero. Selecting its midpoint is also an exact
coordinate-wise minimizer and gives gap `1/16`. It violates the second
sharpness condition and invalidates the claimed zero-gap collapse. This is
not a counterexample to the repaired theorem; it demonstrates a mismatch
between selection-dependent hypotheses and an unqualified selection
conclusion.

For the supplied example
`m(t)=sigma|t-c|-(t-c)^2`, with
`sigma>=2(U-L)`, the one-sided relaxation slopes are strictly directed away
from the kink. The minima are unique, so this caveat does not exclude the
sharp-by-quadratic experiments or the advertised family.

## Scope and checks actually performed

I read the assigned audit, the separable source model and proofs, and the
previous review sections identified above. I independently reconstructed
the phase count, refinement inequality, recurrence, collapse, slice, and
termination argument. I also derived the exact selection example above.
Only targeted source-reading commands (`rg`, `nl`, and `sed`) were used;
no computational experiments or formal verification were rerun. No
project-wide verification or CI checks were performed.
