# Review of regridded certificates: proof and significance

Date: 2026-10-02. Reviewed version: the complete draft of
[regridded certificates](../regridded-certificates/note.md), Sections 1–10,
including its shell-incidence count and the revised all-counted-operations
schedule in Section 8. A follow-up below reviews the abstract recurrence
and scope table in [the synthesis](../SYNTHESIS.md). The coordinate-drift
calculation and abstract recurrence were also checked independently by a
delegated reviewer. No external literature search was performed for this
review.

The core proof checks. This result addresses the repository's original
constructive-center question more directly than geometric-grid DP: it finds
a certificate in the original affine-message model on arbitrary tree
decompositions, with the same linear-logarithm *final certificate size* as
Theorem 3.4, without knowing the minimizer or assuming stationarity. That is
a meaningful theoretical advance over the local September 29 results.
Rebuilding costs an additional logarithmic factor in created boxes and a
further factor in exact convex-optimization calls. It does not establish a
linear-logarithm bound on total construction work, a bound for the original
nested-refinement algorithm GR, or a practical MINLP solver speedup.

The valid conclusion is conditional on the stated original certificate
assumptions and exact oracles. The global growth constant, bounded variable
occurrence, gradient regularity, and quadratic relaxation error are still
substantial requirements. The result also has a stronger oracle requirement
than geometric-grid DP: exact gradients and exact convex minima with
attaining points, not just exact factor values. Those distinctions are
essential when describing its significance.

The main proof steps can be checked without the old sup-norm localization
lemma. Let `b_t` and `d_t` be the selected leaf and separator widths, and
define

```
Q = sum_t b_t^2 + sum_(t != root) d_t^2,
E = sum_t ||z^t-x_Vt||^2,
R = ||x-c||,
C0 = k(k-1)p.
```

Here `x` is reconstructed from the topmost copy of each coordinate and `c`
is the current feasible center. Including both kinds of widths in `Q` is
necessary for the displayed constant. For one coordinate, its occurrence
subtree has at most `k` nodes. Its copy differences are bounded by sums of
leaf and separator widths along paths, with separate width columns. The
path-incidence matrix has squared Frobenius norm

```
2 sum_t depth_i(t) <= k(k-1).
```

Summing over coordinates charges each box at most `p` times and gives
`E<=C0 Q`. This avoids any global tree-depth or branching multiplier. It
does not assume that a separator width is bounded by an adjacent leaf
width, or that the configuration is already consistent.

Shell grading then gives

```
Q <= 6N h^2 + 6k theta^2 R^2 + 6 theta^2 E.
```

Absorbing the last term under `12 C0 theta^2<=1` proves
`Q<=12Nh^2+12k theta^2 R^2`. The sharper `(2k-1)` intermediate coefficient
in the draft is also valid. For `k=1`, copy drift is zero and the condition
written without division handles that case correctly.

The exact slopes at `c` are the decisive choice. The old telescoping
identity gives

```
Phi = F(x)
    + sum_t [a_t(z^t)-a_t(x_Vt)-grad a_t(c_Vt) dot (z^t-x_Vt)]
    - sum_t err_t.
```

Thus no gradient of `F` at either `c` or `x*` has to vanish. Boundary
linear terms cancel through the slopes just as interior linear terms do.
With `M=M_a`, `A0=alpha' A`, and `B0=MC0/2+A0/4`, Lipschitz gradients
and Cauchy–Schwarz give

```
|F(x)-Phi| <= M sqrt(k C0) R sqrt(Q) + B0 Q.
```

Substitution of the mesh bound yields exactly the mixed term and the two
`R^2` terms displayed in Section 5. Under the draft's restrictions on
`theta`, Young's inequality gives

```
|F(x)-Phi| <= eta R^2 + C_eta N h^2,
C_eta = 12B0 + 6kC0 M^2/eta.
```

In particular, `C_eta` depends on `eta`; it is not a fixed constant
multiplied by `eta`. The final draft avoids that possible ambiguity by
calling the chosen coefficient `C`.

For the minimizing configuration, `Phi=LB<=f*`. Taking `eta=g/20`, where
`g=c_g`, gives

```
e_new <= e_old/9 + (10 C_eta/(9g)) N h^2.
```

With `h` halved at each stage and `B=max(p,2C_eta/g)`, the induction is
valid because

```
4B/9 + 10C_eta/(9g) <= B.
```

The initial bound `e_initial<=n s0^2<=pN s0^2` supplies the base case.
The computable gap is bounded by
`(gB/2+C_eta)Nh^2<=gBNh^2`. Consequently the stated stopping stage is
valid for every minimizing configuration, including ties. There is no
need for an upper quadratic bound on `F-F*` or monotonicity of successive
lower bounds.

The shell-incidence calculation also checks. Fix one bag shell level and
one separator level, with dimensions `d` and `q`. If the bag mesh is the
finer one, each projected bag cube intersects at most `3^q` separator
cubes, including touching boundaries. If the separator mesh is finer,
each separator cube meets at most `3^q` projected bag positions, with at
most `m^(d-q)` private-coordinate fibers, where `m=4/theta`. Either case
has at most `3^q m^d` pairs. Clipping cannot create intersections absent
before clipping. This applies both to a bag's own separator and to each
child separator projected into its parent bag.

There are `O((j+1)^2)` pairs of shell levels. Summing own-separator
incidences gives the stated per-stage upper bound
`N 3^w m^p (j+1)^2` on convex programs, with root leaf minima included.
The total over stages is the stated sum of squares. Child choices require
finite minima over intercepted cells; they do not require a product over
child choices or a new value-function oracle. The safe dense-comparison
bound with an extra power of `m` is a possible implementation cost, not
the necessary count of local convex problems.

The resulting comparison is:

| Issue | Regridded certificate result | Qualification |
|---|---|---|
| Unknown optimum | Constructs centers from minimizing configurations | Needs exact convex minimizers and gradients |
| Branching trees | Aggregate drift works on any decomposition | Constants still depend on occurrence bound `k` and width |
| Boundary optimum | Covered with no stationarity assumption | The feasible domain remains a continuous product box |
| Original certificate size | Final size is `O(N C^p log(N/eps))` | Total freshly created boxes have a squared logarithm |
| Convex subproblems | Polynomially many in the stage index | Their internal arithmetic and numerical certification costs are not bounded |
| Unknown constants | The revised dovetail bounds all specified counted operations | Internal oracle costs and bit complexity remain excluded |
| Prior localization conjecture | Not needed | No claim about GR reaching particular partitions or retaining all prior refinements |

The first four rows resolve a real limitation of the earlier repository
work. Theorem 3.4 was a certificate existence result given a sufficiently
accurate center and slopes. The path algorithm made the construction
algorithmic under stationarity, with worse proved conditioning constants.
This construction finds the center with an aggregate contraction, keeps the
original relaxation class, and retains the original final certificate-size
form. Its grading base is linear in `M/g` at fixed other parameters, rather
than the quadratic dependence in the earlier path algorithm's proved base.

It answers the broad earlier question of a construction with
`N C^p polylog(N/eps)` cost measures in this oracle model. It should not be
called an exact match to a literal `N C^p log(N/eps)` cumulative-work
target. Nor does it prove that the old sup-norm localization argument was
repairable: an individual reconstructed coordinate may remain much farther
than `h` from the optimizer while total squared error is `O(Nh^2)`.

Bounded occurrence is a material parameter, not a consequence of bounded
treewidth. A star represented by its edge bags has width one but its center
variable occurs in order `N` bags. Removing the separate branching
parameter does not make the present constants uniform on that family.
The global growth restriction has the same near-tie weakness documented in
[the geometric-DP significance review](significance.md): a remote point of
gap `delta` at distance `D` forces `g<=delta/D^2`. A positive local Hessian
alone gives no useful global separation constant. Multiple global minima
are excluded from the contraction hypothesis.

The exact convex oracle is the main computational caveat. It must return
both the exact value and an attaining point for every relevant leaf-cell
intersection. Convexity alone is not a finite bit-complexity bound for
arbitrary supplied functions. Centers and gradients may become irrational
even when an initial model is described rationally, and expression sizes
can grow across stages. A usable certified implementation needs lower and
upper numerical bounds on the subproblems, a budget for their accumulated
error, and a corresponding approximate-configuration contraction. The draft
correctly leaves those tasks unclaimed.

This also explains why the geometric-grid theorem remains worthwhile. It
has a larger accuracy-logarithm exponent in bag tables but only needs
point-value evaluations and a coordinate upper-curvature bound. It already
covers mixed domains and exact pure integer stopping under its assumptions.
The current regridded proof assumes full Lipschitz bag gradients and the
quadratic factor-relaxation error, and reconstructs a point in the
continuous box. If integer variables are present, local convex minimizers
can be fractional, so the reconstructed point need not be feasible on the
mixed domain. A mixed-integer extension needs a separate argument or a
stronger local optimization oracle. General coupled constraints remain
outside both present contraction results.

The revised unknown-constant schedule in Section 8 is sound as stated.
Its primary version now budgets box construction, incidence processing,
finite-dimensional arithmetic, function and gradient evaluations, and
exact convex calls together. The cap is enforced before each counted
operation. Thus an incomplete stage cannot overshoot the run's budget.
Slopes can be accumulated in `O(Np)` arithmetic per stage, and the stated
known-parameter work bound accommodates these operations.

For a sufficient trial `mu*`, let `W_work>=1` bound its entire counted
cost through stopping stage `J`. A round satisfying

```
r* >= max(1, mu*, ceil(log2 W_work), J+1-lambda_eps)
```

admits that trial and gives it both enough stages and enough work. Since
round `r` has `r` trials, the total counted work is at most

```
sum_(r=1)^r* r 2^r = (r*-1)2^(r*+1)+2 <= 2r*2^r*.
```

Every completed trial has a valid certificate regardless of its parameter
admissibility, so stopping in an earlier trial remains sound. At fixed
instance constants this gives the stated additional logarithmic factor.
Internal oracle costs and bit complexity are excluded throughout. The
separate box-emission schedule remains valid for the created-box measure;
it must not be used to claim the primary schedule's stronger work bound.

The synthesis's abstract recurrence also checks after adding the explicit
conditions `g,N,h_0>0`, `0<=a<g/10`, and `b>=0`. If

```
LB <= f* <= F(x) <= UB,
UB-LB <= a ||x-z||^2 + b N h^2,
```

then quadratic growth and the squared triangle inequality imply

```
(g-2a)e_j <= 2a e_(j-1) + b N h_j^2.
```

For halving widths, the inductive right side is at most
`(8aB+b)Nh_j^2`. The condition `B>=b/(g-10a)` gives the desired
`e_j<=BNh_j^2`; the assumed initial bound is stronger than the preceding
stage bound required at stage zero. The gap is at most
`(10aB+b)Nh_j^2<=gBNh_j^2`. If `B=0`, the assumptions force the exact
zero-error case, so no positive-radius argument is needed.

The initial synthesis statement omitted `a>=0`; that condition was
necessary and has been added by the author and rechecked. For example,
`F(x)=x^2`, `g=b=N=h_0=1`, `a=-1`, `z=0`, `x=7/10`, `LB=0`,
`UB=49/100`, and `B=1/11` satisfy the earlier written gap and initial
conditions but violate its claimed distance bound. The new condition
licenses the inequality direction used in the proof and excludes this
example.

There is no hidden identification of ambient dimension with bag count.
In the abstract recurrence `N` can be any fixed positive normalization for
which its residual bound holds. One can use the ambient coordinate count
for the grid construction or the bag count for rebuilt certificates, or
absorb their ratio into `b`. Changing that normalization also changes the
initial-error condition; it does not change the argument.

For application to a retained incumbent, keep the newly reconstructed
point separate from the best earlier point. The abstract `UB` must bound
`F(x)` for the point appearing in its distance term and used as the next
center. For the exact regridded argument, take `UB=F(x)`; the actual
stopping gap using a better incumbent is no larger. A retained best value
can be smaller than `F(x)` and should not be substituted into the abstract
inequality `F(x)<=UB` without changing the point as well.

The synthesis's two main comparison rows preserve the important scope
differences: continuous convex-relaxation certificates versus mixed
coordinate grids; gradient and attaining convex-minimizer oracles versus
point evaluation; and final certificate size versus table-work count.
The arithmetic-extension row inherits the underlying grid theorem's
structural hypotheses. Rational-polynomial input alone does not imply its
conditioned accuracy or polynomial bit bound. This review confirms that
scope distinction; it does not independently re-prove the separate
arithmetic-extension theorem.

No blocking mathematical issue was found in the reviewed draft. Its
strongest honest claim is an algorithmic construction of the original small
continuous-box decomposition certificates, with explicit polylogarithmic
construction overhead, in the original exact convex-oracle setting. That
claim is more consequential for the repository's original question than
the alternate finite-grid representation alone. External originality and
practical competitiveness remain unestablished.

Verification for this review: the displayed inequalities and constants were
checked algebraically against the current draft and the original Lemmas
1.5, 3.1, and 3.2, read with `cat` and `sed`. A delegated reviewer separately
derived the aggregate drift and current-center error bounds. The revised
Section 8 and corrected synthesis assumptions were freshly read and
checked algebraically, with a delegated second check of the recurrence and
budget. An inline `python3` check confirmed that the review's three local
Markdown links resolve. No numerical experiment or project-wide
verification was run, and no CI status or logs were inspected.
