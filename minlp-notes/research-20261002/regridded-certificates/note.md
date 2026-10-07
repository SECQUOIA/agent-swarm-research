# Rebuilding graded decomposition certificates gives aggregate contraction

Date: 2026-10-02. Status: complete proof with independent adversarial and
significance reviews; external novelty assessment continues.
The regridding and aggregate-contraction idea was proposed by the root
research agent and developed here independently.

The certificate model, factor assumptions, configuration dynamic program,
shell partitions, and telescoping identity are those of Definition 1.2,
Lemma 1.5, Lemma 3.1, and Lemma 3.2 in
[`decomposition-certificates.md`](../../research-20260929/theory-decomposition/decomposition-certificates.md).
This note does not require the false unrestricted sup-norm localization
property examined in
[`tree-localization/counterexample.md`](../tree-localization/counterexample.md).

## 1. Result and computational scope

Assume `(QG)`, `(L^{1,1})`, and `(U^q)` on a box, continuous convex
per-factor lower models on their boxes, and an exact convex-minimization
oracle returning a value and an attaining point. A new algorithm finds a
certificate and incumbent of absolute gap at most `eps`, without knowing
the minimizer and without a local nonlinear optimization heuristic. It
works on every tree decomposition, including branching trees and boundary
minimizers. It needs neither `(S)` nor monotonicity of successive lower
bounds.

More generally, the proof only needs a continuous convex lower model
`ell_(t,B)` for each bag objective `a_t`, satisfying
`0<=a_t(v)-ell_(t,B)(v)<=A0 width(B)^2/4` throughout `B`.
The original `(U^q)` assumptions imply this bound after summing the
assigned factors. Endpoint or vertex exactness is not otherwise used.
The same proof therefore also permits affine Taylor lower models with
this uniform error bound; such models need not satisfy literal `(U^q)`.

At each stage it builds fresh shell partitions around the previous
consistent point and uses slopes equal to the subtree gradients at that
point. Its proof tracks total squared error rather than the largest bag
error. For suitable constant grading ratio `theta`, let `N=|T|`,
`p=w+1`, and `J=O(log(N/eps))`, with the instance constants displayed below.
Then it has:

| Quantity | Bound |
|---|---:|
| Final leaves plus separator cells | `O(N (4/theta)^p (J+1))` |
| Total leaves and cells created in fresh partitions | `O(N (4/theta)^p (J+1)^2)` |
| Exact local convex-optimization oracle calls | `O(N 3^p (4/theta)^p (J+1)^3)` |

The displayed bound preserves the supplied bags and factor assignment.
A separator can have dimension `p` if adjacent bags coincide. Under the
original convention that no bag is contained in its parent, separator
dimensions are at most `w=p-1`, and `3^p` sharpens to `3^w`. More generally
one can use `3^q` with `q` the largest actual separator dimension. No
bag merging, with its possible change to `M`, is implicit in the bound.

The admissible `theta` depends only on `k`, `w`, `M_a/c_g`, and
`A0/c_g`; no branching parameter is needed. The displayed oracle-call
bound uses a shell-incidence count proved in Section 7. A simpler dense
implementation has more pair-comparison work but the same certified
result. These bounds do not assert polynomial bit complexity or a bound
on the internal cost of the convex-optimization oracle.

Continuity ensures attainment of every local subproblem on its compact
box intersection; it holds for the standard alphaBB and McCormick models.
It is stated explicitly because convexity on a closed box alone does not
exclude an upward boundary discontinuity. More generally, lower
semicontinuity of the models would suffice for attainment.

When applied to the original certificate model, the algorithm uses the
same per-factor relaxations and changes only partitions and slopes.
The generalized width-squared contract also permits a supplied aggregate
bag model. Its partitions may be clipped boxes and are not
required to refine the preceding stage's partitions. Thus it is a
certificate-producing regridding algorithm, not a nested-refinement bound
for algorithm GR.

## 2. Definitions and constants

Write `M=M_a`, `g=c_g`, and assume `g>0`. Under the original factor
assumptions take `A0=alpha' A`; under the generalized contract use its
supplied aggregate error bound `A0`. Set

```
C0 = k(k-1)p,
B0 = M C0/2 + A0/4,
eta = g/20,
C = 12 B0 + 6 k C0 M^2/eta,
B = max(p, 2 C/g).
```

Choose `theta=2^-mu`, `mu>=1`, satisfying

```
12 C0 theta^2 <= 1,
sqrt(12) k sqrt(C0) M theta <= eta/4,
12 k B0 theta^2 <= eta/4.                         (2.1)
```

Terms with zero coefficients impose no restriction. Thus the formulas
cover `k=1`, `M=0`, and `A0=0`. Empty separators have one zero-dimensional
cell, width zero, and zero slope; they contribute no copy drift.

In terms of `kappa=M/g` and `a0=A0/g`, the largest admissible dyadic
`theta` satisfies

```
1/theta = O(1 + sqrt(C0) + k sqrt(C0) kappa
                 + sqrt(k(C0 kappa+a0))).
```

In particular, the grading base is linear in `M/g` when the other
parameters are fixed. `C/g` and `B` are also functions only of `k,w,kappa,a0`.

Let `s0` be the largest side length of the domain and
`h_j=s0 2^-j`. The vacuous zero-dimensional or singleton-domain case can
be solved directly; below `s0>0` and the number of variables is positive.

## 3. Algorithm

Start with any point `x^(-1)` in the box and incumbent
`UBD=F(x^(-1))`. At stages `j=0,1,2,...`:

1. Set the center `c=x^(j-1)` and build fresh partitions
   `L_t=Pi(c_Vt;h_j,theta)` and
   `P_t=Pi(c_St;h_j,theta)` using Lemma 3.1 of the original note.
2. Use slopes `lambda_t(c)` from its Lemma 3.2. Run the bottom-up dynamic
   program of Lemma 1.5 with maximal intercepts, obtaining lower bound
   `LB_j` and a minimizing configuration.
3. Form its consistent point
   `x_i^(j)=z_i^(top(i))`, and update
   `UBD=min(UBD,F(x^(j)))`.
4. If `UBD-LB_j<=eps`, return this certificate and the incumbent.

The definition of `lambda_t(c)` uses gradients of assigned bag functions,
not derivatives of value functions. The only optimization oracles are
the convex subproblems already specified by the certificate model. A
minimizing configuration is recovered by storing minimizers and child
choices during the bottom-up pass and backtracking from a root minimizer.
Every choice among tied minimizing configurations satisfies the analysis.

Every stage supplies a valid certificate, regardless of whether its
grading ratio satisfies (2.1). Consequently the stopping test is always
sound. The restrictions on `theta` establish termination and the size
bound.

## 4. Aggregate copy drift, without a branching factor

Fix one stage, center `c`, and an arbitrary configuration. Write `x` for
its consistent point and set

```
b_t = width(B_t),
d_t = width(D_t)                 (t != root),
Q = sum_t b_t^2 + sum_{t != root} d_t^2,
E = sum_t ||z^t-x_Vt||_2^2,
R = ||x-c||_2.
```

**Lemma 1.** `E <= C0 Q`.

*Proof.* Fix a coordinate `i`. Its occurrence subtree `T_i` has
`m_i<=k` vertices and root `top(i)`. The configuration condition gives,
on each edge of that subtree,

```
|z_i^u-z_i^parent(u)| <= b_parent(u)+d_u.
```

Build a nonnegative matrix with one row for each occurrence `t`, columns
for its occurrence-subtree bag widths and separator widths, and entries
one on the bag and separator widths along the path from `top(i)` to `t`.
Each row has exactly `2 depth_i(t)` ones. It maps the widths to upper
bounds on the absolute coordinate copy errors. Its squared operator norm
is at most its squared Frobenius norm, which is

```
2 sum_{t in T_i} depth_i(t) <= m_i(m_i-1) <= k(k-1).
```

The sum of depths is maximal for a path; alternatively, topologically
order the vertices and bound their depths by `0,1,...,m_i-1`.
Consequently, summing over coordinates,

```
E <= k(k-1)[sum_t |V_t| b_t^2 + sum_{t != root} |S_t| d_t^2]
  <= k(k-1)p Q.
```

No global tree depth or vertex degree occurs in this argument. □

**Lemma 2.** Under the first condition of (2.1),

```
Q <= 12 N h_j^2 + 12 k theta^2 R^2.               (4.1)
```

*Proof.* Shell grading gives
`width(Y)<=h_j+theta dist_inf(Y,c)`. For a bag leaf containing `z^t`,

```
b_t <= h_j + theta ||x_Vt-c_Vt||_2
             + theta ||z^t-x_Vt||_2.
```

The same bound holds for a separator cell with both vectors restricted
to `S_t`. Each variable occurs in at most `k` bags and `k-1` separators.
Moreover, copy errors are zero on `V_t\S_t`, because those variables have
their top bag at `t`. Thus the bag-plus-separator squared center
differences sum to at most `(2k-1)R^2`, and the corresponding squared copy
errors sum to exactly `2E`. Applying
`(u+v+w)^2<=3(u^2+v^2+w^2)` and counting at most `2N-1` boxes gives

```
Q <= 6N h_j^2 + 3(2k-1)theta^2 R^2 + 6theta^2 E.
```

Use Lemma 1 and absorb `6theta^2 C0 Q<=Q/2`. If `C0=0`, the same bound
holds without absorption. □

## 5. The error estimate relative to the current center

The telescoping identity with `x°=c` gives exactly

```
Phi = F(x) + sum_t T_t - sum_t err_t,
T_t = a_t(z^t)-a_t(x_Vt)-grad a_t(c_Vt) dot (z^t-x_Vt),
0 <= err_t <= A0 b_t^2/4.
```

The gradient at `c` need not vanish. The subtree slopes cancel its linear
copy terms exactly. In particular, boundary minimizers cause no remaining
first-order term.

The Lipschitz-gradient assumption gives

```
|T_t| <= M ||x_Vt-c_Vt||_2 ||z^t-x_Vt||_2
          + (M/2)||z^t-x_Vt||_2^2.
```

By Cauchy–Schwarz, coordinate multiplicity, and Lemma 1,

```
|F(x)-Phi| <= M sqrt(k) R sqrt(E) + (M/2)E + (A0/4)Q
           <= M sqrt(k C0) R sqrt(Q) + B0 Q.
```

Using (4.1) and `sqrt(u+v)<=sqrt(u)+sqrt(v)` yields

```
|F(x)-Phi| <= sqrt(12 k C0) M sqrt(N) h_j R
            + [sqrt(12) k sqrt(C0) M theta
                         +12 k B0 theta^2] R^2
            +12 B0 N h_j^2.
```

Young's inequality bounds the first term by
`eta R^2/2 + 6 k C0 M^2 N h_j^2/eta`. The last two restrictions in
(2.1) bound the bracket by `eta/2`. Hence every configuration satisfies

```
|F(x)-Phi| <= eta ||x-c||_2^2 + C N h_j^2.          (5.1)
```

Only the upper bound on `F(x)-Phi` is needed below. The absolute estimate
is available because the factor errors are nonnegative and bounded.

## 6. Contraction, termination, and certificate counts

Write `e_j=||x^(j)-x*||_2^2`. A consistent configuration at the true
minimizer has value at most `f*`, so the minimizing configuration has
`Phi=LB_j<=f*`. Apply (QG) and (5.1):

```
g e_j <= F(x^(j))-f*
      <= F(x^(j))-LB_j
      <= (g/20)||x^(j)-x^(j-1)||_2^2 + C N h_j^2
      <= (g/10)(e_j+e_(j-1)) + C N h_j^2.
```

Therefore

```
e_j <= e_(j-1)/9 + (10 C/(9g)) N h_j^2.            (6.1)
```

Since `h_(j-1)=2h_j`, induction gives

```
e_j <= B N h_j^2.                                 (6.2)
```

For `j>=1`, the induction step uses
`4B/9+10C/(9g)<=B`, which follows from `B>=2C/g`.
For stage zero,
`e_(-1)<=n s0^2<=pN h_0^2<=BN h_0^2`, and the same conclusion follows.

For `j>=1`, (6.2) gives
`||x^(j)-x^(j-1)||^2<=10BN h_j^2`; at stage zero the stronger factor 4
holds. Thus the actual computable gap satisfies

```
0 <= UBD-LB_j <= F(x^(j))-LB_j
             <= (gB/2+C)N h_j^2
             <= g B N h_j^2.                      (6.3)
```

Consequently the algorithm stops no later than

```
J = max(0, ceil(log2(s0 sqrt(gBN/eps)))).
```

At termination the incumbent is at most `eps` above `f*`, and the lower
bound is at most `eps` below the incumbent. No upper quadratic-growth
bound or stationarity assumption was used.

By the shell-partition lemma, stage `j` has at most

```
S_j = 2N (4/theta)^p (j+1)
```

leaves plus cells. Summing over stages `0,...,J` gives at most

```
N (4/theta)^p (J+1)(J+2)
```

created boxes. The final certificate has size at most
`2N(4/theta)^p(J+1)`. These bounds count the boxes directly constructed
in fresh shell partitions; they do not count repeated refinements of a
retained spatial tree. The previous partition can be discarded once its
consistent point and incumbent are retained.

## 7. Convex subproblems and shell-incidence work

For each bag leaf `B`, the affine child bound requires the minimum
intercept over child cells whose separator box meets `B`'s projection.
For each pair of a bag leaf and its own separator cell that intersect,
the dynamic program solves one convex minimization over their
intersection. This follows directly from Lemma 1.5; it does not replace
the program by a discrete objective table or an unproved value-function
oracle.

Here is a bound that includes touching pairs. Put `m=4/theta`. A shell
partition has `j+1` levels, each contained in a grid with at most `m`
positions per coordinate. Its central level has at most two positions per
coordinate, so it obeys the same bound. Consider a bag of dimension `d`
and a separator of dimension `q<=d`. For one pair of shell levels:

- If the bag-grid side is no larger than the separator-grid side, each
  projected bag cube meets at most `3^q` separator grid cubes. There are
  at most `m^d` bag cubes.
- If the separator-grid side is smaller, each separator cube meets at
  most `3^q` projected bag grid positions. Each such position has at most
  `m^(d-q)` bag-grid fibers, and there are at most `m^q` separator cubes.

Both cases bound the incidences by `3^q m^d` per level pair. Clipping to
the common domain box cannot add intersections between the original
cubes. Thus each bag–separator incidence list has at most

```
3^q m^d (j+1)^2
```

pairs. Empty separators have one cell and obey the bound directly.
Summing own-separator pairs gives at most
`N 3^p m^p (j+1)^2` local convex programs, including root leaf minima.
Summing parent-leaf/child-cell pairs gives at most
`(N-1)3^p m^p(j+1)^2` child incidences, because a tree has `N-1` edges.
No maximum branching factor is needed.

The incidences can be enumerated by shell-level pair and grid indices,
charging to the finer grid in the first case and to the separator grid
plus fibers in the second. This introduces an `O(p)` coordinate-processing
factor. Storing full pair tables is unnecessary: incidence lists can be
streamed and minima accumulated. A naive dense all-pairs implementation
instead performs up to `O(N m^(2p)(j+1)^2)` comparisons, still a
polylogarithmic stage dependence.

Across all stages, the number of exact convex-optimization calls is at
most

```
N 3^p m^p (J+1)(J+2)(2J+3)/6.
```

Each program has dimension at most `p`. The result assumes an exact
convex-minimization oracle returning its value and an attaining point, as
in the original dynamic program. For general supplied convex functions,
these assumptions do not establish a finite bit-complexity bound.
Certified approximate solves require a separate error budget; no such
implementation result is claimed here. Storage for numerical minimizers
and gradients also carries the usual coordinate factor `O(p)` beyond the
count of certificate boxes.

## 8. Unknown conditioning and relaxation constants

The implemented algorithm only uses `theta`, `h_j`, function and gradient
values, and the convex subproblem oracle. It does not use `g`, `M`, or
`A0` in its operations or stopping test. They are needed to identify a
sufficient `theta` and prove the preceding bound.

A universal version can therefore dovetail the runs
`theta=2^-mu`, `mu=1,2,...`. For rounds `r=1,2,...`, run each
`mu<=r` from the same initial point with at most `r+lambda_eps` stages
and a budget of `2^r` counted operations, where

```
lambda_eps = max(0, ceil(log2(s0/sqrt(eps)))).
```

Count box construction, incidence processing, finite-dimensional
arithmetic, bag-value and bag-gradient oracle evaluations, and exact
convex-optimization oracle calls. The internal cost of each oracle call
remains excluded. If bag functions are given as lists of individual
factors, their input size and evaluation costs must be added; the number
of factors per bag is not bounded by `N` or `p`.
Enforce the budget before each counted operation. Stop at the first run
that passes its own valid gap test. Some sufficiently large `mu` satisfies
(2.1), and a sufficiently large round gives this run both the required
stage allowance and its finite work budget. Thus this procedure
terminates without knowing the problem constants.

More precisely, let `mu*` be a sufficient index and let `J` be its stopping
stage bound. Section 7 gives a total counted-work bound
`W_work=O(p N 3^p (4/theta)^p (J+1)^3)` for that run. Slopes can be
computed by a bottom-up accumulation of the bag gradients, using
`O(Np)` arithmetic per stage, which fits this bound. Any integer

```
r* >= max(1, mu*, ceil(log2 W_work), J+1-lambda_eps)
```

is sufficient. The total counted operations through that round are at
most `sum_{r<=r*} r 2^r <= 2r*2^r*`. For fixed instance constants, this
adds one logarithmic factor to the known-constant counted-work bound.
It still does not bound oracle-internal time or bit complexity.

If only the created-box measure is desired, use the same schedule with
a budget enforced before every box emission instead. Replacing
`W_work` above by
`B_work=N(4/theta)^p(J+1)(J+2)` gives the corresponding one-logarithm
overhead in total created boxes. This latter schedule should not be
reported as the sharper oracle-work bound.

## 9. Relation to the earlier open problem

Theorem 3.4 of the original note constructs small certificates around a
known minimizer. Algorithm GR in `adaptive-matching.md` proves a comparable
algorithmic bound on paths under stationarity by sup-norm localization
and nested refinement. The unrestricted tree version of its localization
property is false.

Rebuilding partitions avoids that requirement. The center may have total
squared error `O(Nh^2)` and individual coordinates much farther than `h`;
the aggregate error estimate still contracts because slopes are evaluated
at that same center. Rebuilding also avoids paying to retain all previous
refinements. The result gives the desired linear-in-`N` certificate count
times logarithms for arbitrary tree decompositions, with a quadratic
stage-log overhead in created boxes and a cubic stage-log bound on exact
convex-optimization calls. It is a different algorithm from GR, and its
count should be reported in that form.

## 10. Verification status

The coordinate-incidence drift bound, grading absorption, and shell-pair
count were derived independently by delegated agents. The shell-pair
argument also received a separate independent check. The completed
[adversarial review](../reviews/regridded-certificates-adversary.md) and
[significance review](../reviews/regridded-certificates-significance.md)
found no blocking mathematical issue after clarifying continuity,
attaining-oracle assumptions, and bag-level oracle accounting.
The targeted command actually run was

```
python research-20261002/regridded-certificates/check_core.py
```

It passed 480 occurrence-subtree drift checks, 500 parameter/constant
checks including the zero-coefficient cases, and 180 valid certificate
configuration checks on branching quadratic families with nonstationary
boundary minima. The maximum telescoping-identity residual was
`1.14e-13`. Details are in `check_core.json`. These floating-point checks
support the algebra; they do not implement or enumerate the full
regridded dynamic program. No project-wide or CI checks were used.

The [inexact-oracle extension](inexact-oracles.md) replaces exact solves
and gradients by certified accuracy requests. It includes feasible
rational reconstruction on touching faces and distinguishes the number
of boxes from the number of serialized local proof objects.
