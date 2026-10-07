# Adversarial review of rebuilt graded certificates

Date: 2026-10-02. Verdict: **accepted with the explicit continuity and
attaining-oracle assumptions now stated in the note.** No unresolved
mathematical or counting defect was found.

I reviewed [note.md](../regridded-certificates/note.md) against Definition
1.2 and Lemmas 1.5, 3.1, and 3.2 of the original
[certificate model](../../research-20260929/theory-decomposition/decomposition-certificates.md).
This review covers the aggregate contraction proof, boundary minimizers,
the finite convex dynamic program, closed touching pairs, clipped shell
partitions, all displayed counts, and the unknown-constant schedules.
A separate delegated audit checked the dynamic program and complexity
claims independently.

The positive result does not use unrestricted tree localization. It
allows individual coordinates to remain far from the current core width
and controls their total squared error instead. Rebuilding partitions
around the preceding consistent point is authorized by the certificate
model. The result is therefore about a different algorithm from nested
refinement GR, as the note correctly states.

## Assumptions and the point addressed during review

The first draft stated the attaining-oracle promise in Section 7 but
opened with only `(QG)`, `(L^{1,1})`, and `(U^q)`. Convexity of a supplied
lower model on a closed box does not by itself guarantee attainment:
upward discontinuities on a boundary face are possible. The current
opening explicitly assumes continuous convex per-factor lower models
and an oracle returning both the minimum value and an attaining point.
It also explains that lower semicontinuity would suffice for attainment.
This addresses the issue. Standard alphaBB and McCormick models satisfy
the added regularity assumption.

With that assumption, every local feasible set is a nonempty compact
box intersection, including lower-dimensional intersections arising from
touching pairs. Its objective is continuous and convex. The minimum
exists. There are only finitely many leaves and cells at each stage,
so maximal intercepts, the root minimum, and a minimizing configuration
all exist.

The proof also imports the original decomposition convention that no
bag is contained in its parent. In particular, separator dimensions are
at most `w`, which is used in the `3^w` oracle-call count. This is already
part of the referenced model; it is not an additional graph restriction.
Without that convention or a normalization step, replace that factor
by `3^(w+1)` when a separator has the full bag dimension.

## Aggregate drift and error estimate

Lemma 1 correctly avoids a branching factor. For one coordinate, the
occurrence subtree has at most `k` bags. A path of length `d` contributes
exactly `2d` distinct width entries to the corresponding matrix row:
one parent-bag width and one separator width per edge. Branching can
repeat a column in different rows, but the squared Frobenius norm still
bounds the squared operator norm. The depth sum is at most
`m_i(m_i-1)/2`. Summing the resulting coordinate inequalities counts a
bag width at most `|V_t|` times and a separator width at most `|S_t|`
times. Thus `E<=k(k-1)p Q` is valid for every configuration.

The edge drift bound applies to the exact closed-box definition:
the separator cell contains the child copy and meets the parent leaf's
projection. Joining the two copies through a point of that intersection
gives drift at most the cell width plus the parent-leaf width. The parent
copy need not lie in the cell. No stronger consistency condition was
silently imposed.

Lemma 2 also has the correct multiplicities. A coordinate occurs in
`m_i` bags and exactly `m_i-1` separators. Copy errors vanish outside a
bag's own separator, so the bag-plus-separator sum of squared copy
errors is exactly `2E`. The preliminary inequality is therefore

```
Q <= 6N h^2 + 3(2k-1) theta^2 ||x-c||^2 + 6theta^2 E.
```

Absorbing the last term under `12 C0 theta^2<=1` gives the stated
`12N h^2+12k theta^2 ||x-c||^2` bound. The zero-coefficient case needs
no division by `C0` and is valid as stated.

The telescoping identity is applied at the actual current center `c`.
Subtree slopes cancel the linear copy terms at that center exactly.
Lipschitz gradients then give

```
|F(x)-Phi| <= M sqrt(k C0) ||x-c|| sqrt(Q) + B0 Q.
```

Substitution of the grading bound produces the coefficients displayed
in Section 5. Young's inequality contributes
`eta ||x-c||^2/2 + 6k C0 M^2 N h^2/eta`; the remaining two restrictions
on `theta` contribute at most another `eta ||x-c||^2/2`. This proves
the uniform configuration estimate with the stated `C`.

No gradient at the true minimizer is set to zero in this argument.
The same cancellation works at a boundary minimizer, and the proof
does not need an upper quadratic bound on `F-f*`. Large linear terms
are canceled by the exact slopes rather than being bounded by `M`.

## Contraction and stopping

A consistent configuration at `x*` is feasible for these finite
partitions and has relaxed value at most `f*`. Thus the minimizing
configuration has `LB_j<=f*`. Combining quadratic growth with the
configuration estimate gives exactly

```
e_j <= e_(j-1)/9 + (10C/(9g)) N h_j^2.
```

For `j>=1`, the induction requires
`4B/9+10C/(9g)<=B`, which follows from `B>=2C/g`.
For stage zero, `n<=pN` and the domain diameter estimate give
`e_(-1)<=pN h_0^2`; this base case is valid independently of the
induction for later stages.

The next distance estimate uses
`||x^(j)-x^(j-1)||^2<=2(e_j+e_(j-1))`, yielding the factor `10B`
for `j>=1` and at most `4B` at stage zero. Consequently

```
UBD-LB_j <= (gB/2+C)N h_j^2 <= gBN h_j^2.
```

This is the actual stopping gap because the incumbent includes the
current consistent point. The displayed stopping index `J` follows
without requiring monotone lower bounds. All inequalities hold for every
minimizing configuration, so tie-breaking needs no additional rule.

The constants and their zero-coefficient cases are consistent. In
particular,
`C/g=6C0(M/g)+3(A0/g)+120k C0(M/g)^2`. Thus `B` and the admissible
grading parameter have precisely the stated dependence on the dimension,
occurrence, and relative conditioning parameters. There is no hidden
global depth or maximum branching parameter.

## Dynamic program and finite counts

The local oracles are the convex programs of Lemma 1.5: one program
per intersecting own-separator cell and bag leaf, plus root leaf
minima. Each child contribution is the affine slope term plus the
smallest compatible child intercept. Storing a minimizer and the
selected child cells suffices for backtracking. This does not require a
value-function evaluation oracle or a nonconvex local solve.

At stage `j`, the shell construction has `j+1` levels because
`h_j=s0 2^-j`. Clipping preserves coverage, disjoint interiors, and the
grading inequality. The bound
`2N(4/theta)^p(j+1)` on leaves plus cells follows directly. Summing it
over stages `0,...,J` gives the stated quadratic stage-log count of
created boxes. The final certificate needs only the current partitions;
earlier partitions need not be retained.

The shell-incidence argument covers the dimension and boundary issues.
For each level pair, use the side lengths of the original grid cubes,
before clipping. An interval no longer than a grid spacing meets at most
three grid intervals, including endpoints. If bag cubes are smaller,
charge the at most `3^q` separator choices to each bag cube. If separator
cubes are smaller, charge to each separator cube and then count at most
`m^(d-q)` bag fibers for each projected bag-grid position. Both charges
give `3^q m^d`. Clipping cannot create an intersection between previously
disjoint original cubes. Empty separators have their one cell and satisfy
the separate stated bound.

There are at most `(j+1)^2` level pairs and exactly `N-1` child edges.
Therefore both the own-separator program count and the child-incidence
count are linear in `N` without multiplying by the largest degree.
Summing `(j+1)^2` over the stages gives exactly
`(J+1)(J+2)(2J+3)/6`. Coordinate processing costs the stated additional
factor `O(p)`; this does not turn the oracle-call count into a
bit-complexity or oracle-internal-time bound.

## Unknown constants

I checked the original box-budget schedule and the revised schedule
that budgets all counted operations. Both are valid, and the current
note separates their claims.

Every trial has a valid certificate and stopping test even if its
grading parameter is too large for the analysis. Budgeting before each
counted operation prevents an unsuccessful trial from exceeding its
allowance. A sufficient index `mu*` eventually receives both its
required budget and at least `J+1` stages. The inequality
`r>=J+1-lambda_eps` correctly accounts for stages indexed from zero.

For the work-budget version, shell construction, incidence processing,
convex oracle calls, and the coordinate work fit
`O(p N 3^w m^p(J+1)^3)`. This count treats a bag value or bag gradient
evaluation as one oracle call and excludes its internal evaluation cost.
That interpretation should be explicit: the number of individual factors
assigned to a bag is not bounded by `N` and `p`. If evaluations of those
individual factors are counted separately, their number must enter the
work bound. This qualification concerns the stronger total-work claim,
not the displayed count of convex-minimization calls.

Subtree slopes can be computed by adding child
separator-gradient vectors into each bag gradient and then restricting
to the bag's own separator. Each child edge contributes at most `p`
entries once, so the claimed `O(Np)` arithmetic per stage is valid.

Choose the smallest sufficient round satisfying the displayed maximum.
For fixed instance constants, its stage-allowance requirement is at
most `O(1+log N)` and its other requirements give
`r*=O(log W_work)`, `2^r*=O(W_work)`. Summing the trial budgets then
gives `O(W_work log W_work)`. The analogous statement with `B_work`
applies to the separately described box-budget schedule. The fixed-
constant qualification matters; the note does not claim an additional
uniform bound on the dependence on unknown numerical constants.

## Targeted checks

I ran `PYTHONDONTWRITEBYTECODE=1 python3 -` with an inline check using
integer arithmetic and `fractions.Fraction`. It enumerated all 874
rooted occurrence trees with increasing parent labels through seven
vertices, checked their depth sums, and checked 3,496 nonnegative
width/drift cases. It also checked the exact grading conditions,
stage-zero inequality, induction inequality, and final gap inequality
for 840 parameter choices, including zero coefficients. All checks
passed. These checks support the proof above; they do not replace its
uniform inequalities. No artifact was written.

The independent complexity audit ran a separate exact-rational inline
Python check on six clipped shell examples, with bag dimensions 1–3,
separator dimensions 0–2, and boundary and non-dyadic centers. All 96
level-pair bounds passed over 2,729 actual touching incidences; the
largest count-to-bound ratio was `35/144`. These are checks of the
incidence lemma, not an implementation of the full algorithm.

Neither audit ran project-wide verification, inspected CI, ingested
literature, or used external research. The acceptance is for the stated
exact-oracle theorem and its finite counts. It does not certify an
approximate-oracle implementation, bit complexity, or a complete
executable regridding solver.
