# Branching and structural comparison audit

This audit supports the new B&B complexity manuscript. It reviews the assigned
September 28–30 notes and their recorded reviews, and reads the topic-33 Lean
statements. It does not perform literature research, rerun experiments, inspect
CI, or modify source notes. Mathematical repairs below are authoring material;
new statements should receive the manuscript's independent proof review.

## Main findings and scope corrections

The safe branching spine is complete: exact-gap certificates, optimal tree
size, the one-dimensional minimizer theorem, its information limitations, and
the safety tradeoff. The fixed-factorization decomposition separation is also
sound when stated as a comparison of certificate sizes. Several broader
interpretations would be false or unsupported.

1. **A supremum need not preserve a strict inequality.** The sources define a
   competitive ratio as a supremum. Their instancewise bound
   `T_R < 4 T_opt` establishes a competitive ratio **at most 4**, not strictly
   below 4. The safe intervals are `[11/5, 4]` for the minimizer rule and
   `[5/3, 4]` for the best deterministic I1 rule on the indicated nonanalytic
   class. The sources' `[11/5, 4)` and `[5/3, 4)` are not justified. The
   pointwise strict inequality remains valid.
2. **Higher-dimensional competitiveness remains open.** No full theorem makes
   `omega` constant-competitive for all fixed-dimensional exact-gap instances,
   including separable instances. The phase lemma does not supply the missing
   global accounting. The all-coordinates rule `multi` has a proved growing
   loss even for a separable quadratic.
3. **A germ is a strong oracle.** It distinguishes nonanalytic functions but
   determines a real-analytic objective on a connected box. The germ lower
   bounds therefore do not apply to polynomial or other real-analytic
   classes. A finite jet of order at least a polynomial's degree also
   determines that polynomial. Restricting to a lower-order jet would require
   a different polynomial adversary, which is not constructed here.
4. **The decomposition separation fixes both factorization and relaxation.**
   It does not cover aggregation of the objective, PSD/SDP strengthening,
   arbitrary functional refactorization, or the whole behavior of SCIP.
   Certificate size is not the number of local convex programs or bit
   operations. Its uniform-in-accuracy ratio is a size statement.
5. **The exact-bag covering result is not a relaxed-bag characterization.**
   `covering-upper-half.md` settles separator-cell placement with exact bag
   minima and one-dimensional separators. It does not settle a two-sided
   covering characterization for the decomposition certificate model. The
   static per-bag tolerance allocation has a proved mixed-integer
   counterexample.
6. **Path localization cannot be extended without qualification.** The
   October 2 update inside `adaptive-matching.md` explicitly reports a
   counterexample to unrestricted branching-tree localization `(Loc_T)`.
   GR's proved theorem is for path decompositions and requires
   `grad F(x*) = 0`. A new algorithm linked from that update uses a different
   certificate format and needs a separate audit.
7. **The brief's `research-20260929/theory-single-tree/` directory is absent.**
   The single-tree comparison is in
   `research-20260929/theory-decomposition/decomposition-certificates.md`,
   Section 2.1. The other exact directories are `theory-decomposition/` and
   `theory-consistency/`.

Two smaller repairs matter when copying statements. In the 1D ambiguity pair,
`-37/300` is the minimum of the shifted pruning function, while the objective
relaxation lower bound is `-37/300 - epsilon`. Also, shell counts should use
`max(0, ceil(log2(s0/h)))`; untruncated logarithmic formulas can become
negative for large tolerances. These repairs do not affect the intended
small-tolerance results.

## 1. The model the manuscript should state

For the branching theorems take a compact nondegenerate box
`X0 = product_i [L_i,U_i]`, a continuous objective `f`, no additional
constraints, and a fixed `alpha > 0`. On each box `B`, use the exact bound

```
q_B(y) = sum_i (y_i-l_i)(u_i-y_i),
f_B(y) = f(y) - alpha q_B(y),       LB(B) = min_B f_B.
```

The function `f_B` need not be convex for the 1D minimizer theorem. Convexity
on every box is equivalent to convexity of `f(y)+alpha ||y||_2^2`; it makes
the oracle a convex minimization oracle but is not used in that proof.

Initially fix the incumbent at `f* = min_X0 f`, and let `epsilon > 0`.
Set `m = f-f*+epsilon`. A box is **valid** exactly when
`m(y) >= alpha q_B(y)` at every `y in B`; pruning is then
`LB(B) >= f* - epsilon`. This convention distinguishes `LB` from
`min_B(m-alpha q_B) = LB(B)-f*+epsilon` throughout.

Each invalid node receives one strictly interior coordinate cut and both
children are processed. Count all nodes, equivalently one bound solve per
node in this idealized model. A finished binary tree with `I` internal nodes
and `N` leaves has `T=2I+1=2N-1`. Re-solving a relaxation, finding an
incumbent, evaluating germs, or computing an optimal cut is not charged by
this count. The information model and computational cost must be separate.

Validity is hereditary: if `B' subset B`, then `q_B' <= q_B` on `B'`.
Uniformly small boxes are valid because `q_B <= sum_i width_i(B)^2/4` and
`m >= epsilon`. Consequently finite certificates exist.

Use three different certificate counts consistently:

- `N_part`: the smallest partition of the root into valid boxes, allowing
  non-guillotine partitions.
- `N_guill`: the smallest valid leaf partition obtainable by recursive
  binary coordinate cuts.
- `N_cover`: the smallest cover by valid boxes when the spatial lower-bound
  framework permits overlaps or only covers the feasible set.

The branching notes' `N_opt` is `N_part`. Single-tree lower bounds that
apply to covers also apply to partitions, but that does not make these
benchmarks interchangeable. In one dimension an interval cover can be
converted to a hereditary-valid partition without increasing its size.
In higher dimensions that assertion needs additional work and should not be
assumed.

In 1D, every interval partition has a binary cut tree, so
`T_opt=2 N_part-1`. In higher dimensions,
`T_opt=2 N_guill-1`, with `N_part <= N_guill`. An arbitrary certificate can
be refined along all face positions into a guillotine grid with at most
`(2 N_part-1)^n` cells. Every cell lies in an original box and is valid.
This elementary bound is self-contained. The sharper published BSP bounds
quoted by the notes were inspected only through abstracts; the manuscript
should use the primary-literature evidence supplied by the literature owner
before importing their exact constants and size conventions.

### Information available to a branching rule

Define the rule as a function of explicitly listed data, with the same
oracle convention on the compared instances.

- **Oblivious I0:** the box and depth only. In particular, the fixed-instance
  lower bound in the notes assumes the rule is independent of the tolerance.
  If tolerance-dependent rules are admitted, the adversarial construction
  still gives a bad instance for each tolerance; it no longer automatically
  gives one kink location that works for all tolerances.
- **Relaxation information I1:** the box, `alpha`, tolerance, incumbent,
  bound value, a relaxation minimizer, and the **germ** of `f` at that
  minimizer. Equality of germs means equality on some open neighborhood,
  without granting arbitrary queries over the node. The lower-bound examples
  also agree near the box endpoints in 1D, or near all box corners in the
  coordinate-ambiguity construction. They do not agree on every facet.
- **Full node information:** the entire function on the current box.
  Optimality in this model counts the resulting tree, not the computation
  required to choose its cut.

A node-local rule carries no objective-dependent information from other
nodes. Depth or a preassigned random seed may be specified as part of the
model, but stored pseudocosts or learned information from siblings are not.
For randomized lower bounds, use random local maps or fresh independent
local randomization, so that fixing the random input produces an admissible
deterministic node-local rule. The iterated coordinate ambiguity also needs
a coordinate-wise minimizer selection: a separable coordinate minimizer is
selected from its interval and its coordinate function, rather than using
other coordinates to encode information through a tied optimal face.

## 2. A complete safe 1D competitiveness theorem

**Statement.** For continuous `f` under the exact-gap model, split every
invalid interval at any exact minimizer of its relaxation. For every valid
partition with `N>=2` intervals, there are at most `4N-5` splits and at most
`8N-9` nodes. If `N=1`, the root is valid and there is one node. Therefore
the rule is 4-competitive, with the stronger instancewise inequality
`T <= 4T_opt-5` whenever the root is invalid. Ties may be chosen using
arbitrary history; the upper bound does not require node-local tie-breaking.

Here is the full proof suitable for incorporation, without the auxiliary
proximal interpretation.

Let a certificate interval be `J=[s,s']`, of length `lambda`, and let
`phi_B=m-alpha q_B`. An invalid interval has `min phi_B<0`, while its
endpoint values are positive. Every relaxation minimizer is therefore
strictly interior. Two internal nodes never have the same split point:
in nested nodes an ancestor's split is an endpoint of descendants on that
side, and nonnested nodes have disjoint interiors.

A node with its split inside `J` cannot lie in `J`, by hereditary validity.
It must contain `s`, `s'`, or both in its interior. Nodes sharing such an
endpoint are nested. The only algebraic step is the following crossing
lemma.

Suppose `B1` strictly contains `B2`, both contain `s` in their interiors,
and their minimizer splits `y1,y2` both belong to `(s,s')`. The child of
`B1` containing `s` ends at `y1`, so `y2<y1`. Write

```
d = s-l_B1 > 0,   e = u_B1-s > 0,   t_k = y_k-s,
0 < t2 < t1 < min(e,lambda).
```

Optimality of `y1`, invalidity at `y2`, and validity of `J` at `y1` give

```
m(y1) <= m(y2)+alpha[(t1+d)(e-t1)-(t2+d)(e-t2)],
m(y2) < alpha(t2+d)(t1-t2),
m(y1) >= alpha t1(lambda-t1).
```

Combining them yields

```
alpha t1(lambda-t1)
  < alpha(t1-t2)(e-t1)
  < alpha t1(e-t1).
```

Thus `lambda<e`, so `B1` contains `s'` in its interior. Reflection gives
the same lemma for the other endpoint.

Partition the split nodes with splits inside `J` into those crossing only
its left endpoint, only its right endpoint, and both endpoints. The
crossing lemma permits at most one node in each of the first two classes.
There is at most one in the third class because an interior split destroys
the possibility that a child contains both endpoints. Thus each interior
certificate interval contains at most three splits. An end interval has
only one possible crossing class and contains at most one. Interior
certificate breakpoints are split at most once. The total is

```
(N-1) + 2 + 3(N-2) = 4N-5.
```

This also proves termination: every finite partial tree has this bound, so
an infinite run would have a finite partial tree exceeding it. Continuity
on compact intervals supplies a minimizer at every processed node. A
uniform valid partition supplies a finite `N` to which the argument applies.

### Two-interval refinement and exact constants

If `N_part=2`, with certificate breakpoint `s`, the same rule uses at most
five nodes. Suppose by symmetry its first split `y1` lies right of `s`.
The right child is valid. If the left child is invalid, its minimizer
`y2` cannot lie right of `s`: the crossing lemma would put the root's upper
endpoint in the root's interior. If `y2=s`, both children are valid. If
`y2<s`, the leftmost child is valid. The remaining interval
`[y2,y1]` must also be valid. Otherwise a point `z` witnessing invalidity,
combined with optimality of `y2` in `[L,y1]` and validity of `[L,s]`, gives
`z>s`; combined with optimality of `y1` in the root and validity of `[s,U]`,
it gives `z<s`. The identities used are

```
(z-y2)(y1-z)+(y2-L)(y1-y2)-(z-L)(y1-z) = (y2-L)(z-y2),
(z-y2)(y1-z)+(y1-L)(U-y1)-(z-L)(U-z)
  = (y1-z)[(U-y1)-(y2-L)].
```

In the second argument a nonpositive square bracket already contradicts
the positive valid-interval lower bound; otherwise dropping `y2-L>0`
gives `z<s`. This establishes the five-node bound for arbitrary continuous
instances, with no convexity assumption. It is attained on the ambiguity
pair below, so the ratio on the `N_part=2` subclass is exactly `5/3`.

For the full rule, the source review supplies an explicit `N_part=3`,
`T=11` example. It establishes the lower endpoint `11/5`; it does not
establish the exact worst-case ratio. Avoid describing 4 as a sharp global
constant. The per-interval count of three is attained, but that alone does
not prove a ratio tending to four.

### Inexact minimizers and changing incumbents

If a split is strictly interior and its shifted relaxation value is within
`delta` of the true minimum, the safe bound uses an optimal certificate at
tolerance `epsilon-2delta`, with `delta<epsilon/2`. The crossing proof
spends one `delta` in the parent's optimality inequality and one in the
child's witness inequality. A certificate at the tighter tolerance absorbs
both. If every split additionally satisfies `phi_B(y)<0`, only the first
loss is needed, giving tolerance `epsilon-delta` with `delta<epsilon`.
In both versions apply `8N-9` only for `N>=2`; otherwise the root is valid.
The unqualified single-`delta` version is open in the notes.

For incumbents satisfying `f* <= U_t <= f*+g` with `g<epsilon`, every split
node is invalid at tolerance `epsilon-g`. If the minimizer rule is unchanged,
the same argument bounds the run by a certificate at that tolerance.
State this directly; an incumbent of arbitrary quality does not satisfy the
positive-margin hypothesis needed by this argument.

### Formal coverage

The topic-33 package proves the crossing lemmas, pointwise split counts,
`4N-5` and `8N-9`, the single-interval case, leaf-to-certificate conversion,
and comparison with every finished tree. `MinRule` has unconstrained leaves,
so it also covers finite partial trees. The `f` formulation needs only
`fstar <= f`, `epsilon>0`, and the same pruning threshold in the compared
certificate. The recorded axiom audit reports 167 declarations across six
modules, with only standard Lean axioms.

The package does **not** formalize run/minimizer existence, the converse
certificate-to-tree construction, inexact minimizers, information lower
bounds, sharpness, clamps, or higher-dimensional claims. This audit read
the declarations and documentation but did not rerun Lean. Cite recorded
formal verification as provenance, not as a new check in this manuscript.

## 3. Information lower bounds and complete oracle arguments

### The 1D ambiguity pair

Use `alpha=1`, `epsilon=1/10000`, and `f=H-y^2-epsilon` on `[0,1]`.
Write `C_ab(y)=(a+b)y-ab`, and set

```
g_-(y)=143/300+(4/5)(y-3/5),
g_+(y)=143/300+(6/5)(y-3/5),
e_0(y)=epsilon+y/6,
e_1(y)=(5/3)y-2/3+epsilon,
H_A=max(C_(0,1/3),C_(1/3,1),g_-,g_+,e_0,e_1),
H_B=max(C_(0,3/5),C_(3/5,1),g_-,g_+,e_0,e_1).
```

Both objectives have minimum zero at the two endpoints. To see
nonnegativity directly, `e_0-y^2>=epsilon` on `[0,1/6]`,
`e_1-y^2>=epsilon` on `[2/3,1]`, and
`max(g_-,g_+)-y^2>epsilon` on `[1/6,2/3]`, by its endpoint minima
on the two concave quadratic pieces. Their root
relaxation minimizer is uniquely `3/5`, and they agree near it and near
both endpoints. More explicitly they agree on

```
[0,30epsilon/13] union [1/60,27/40] union [1-3epsilon,1].
```

Their shifted root relaxation minima are `-37/300`; their actual node
lower bounds are `-37/300-epsilon`. On A, a two-piece certificate has the
unique breakpoint `1/3`; on B it has the unique breakpoint `3/5`.

The uniqueness check can be written without a script. Each `H` dominates
its two certificate chords. On nonempty intervals adjacent to the ends it
equals each respective chord. Therefore `[0,b]` extending beyond the named
breakpoint violates `H(y)>=b y` at such a left chord point; `[b,1]`
starting below the breakpoint violates `H(y)>=(1+b)y-b` at a right chord
point. Conversely the two named pieces are valid by chord domination.

The same I1 root data force the same deterministic split. At least one
instance then needs an additional internal node and at least five nodes
against an optimum of three. For any randomized split distribution, at
least one of the two wrong-breakpoint events has probability at least one
half, giving expected size at least four. Thus the lower bounds are
`5/3` deterministically and `4/3` in expectation over this **nonanalytic**
function class. Combined with the preceding upper theorem the best
deterministic ratio belongs to `[5/3,4]`.

**Completed smooth extension.** This lower bound also holds for smooth
nonanalytic functions; the notes give only a brief mollification argument.
Extend both maxima of lines to the real line and convolve with the same
symmetric, nonnegative `C-infinity` bump of integral one, supported in
`[-zeta,zeta]`, positive inside its support. Choose `zeta>0` smaller than
all distances from the endpoints, the root point, and the selected tight
chord subintervals to the relevant neighboring breakpoints. These distances
are positive, so such a choice exists.

Convolution preserves convexity and, by Jensen's inequality, lies above
the original `H`. It preserves each affine segment away from the original
knots because the kernel has zero first moment. Thus the new objective
`f_zeta=H_zeta-y^2-epsilon` remains nonnegative and remains zero at both
endpoints. The chord domination and surviving equality subintervals retain
the two distinct unique certificate breakpoints. Around `3/5` the common
function is `y + constant + (1/5)|y-3/5|`. Its symmetric convolution minus
`y` has its unique minimum at `3/5`: the derivative of the smoothed absolute
value is strictly increasing through zero within the kernel support.
Outside that neighborhood convexity excludes another minimizer. Both
instances still agree near the minimizer and endpoints. The same
indistinguishability proof therefore applies. This adds a complete proof,
not an experimental assertion. It cannot be replaced by an analytic
smoothing, which would destroy the agreement on an open interval.

### Full node information

In 1D let `b(l)` be the largest `b<=u` for which `[l,b]` is valid. It exists
because validity is closed in `b`, and nontrivial sufficiently short
intervals are valid. At an invalid node `b(l)<u`; split there, prune the
left child, and continue on the right. The greedy partition is optimal.
If `s_j` are optimal certificate endpoints and `x_j` greedy endpoints, an
induction gives `x_j>=s_j`: either the greedy point already passes `s_j`,
or `[x_{j-1},s_j]` is a subinterval of the corresponding valid certificate
piece. Consequently greedy uses no more than the optimal number of pieces.

In higher dimensions a full node oracle can select the first cut of a
minimum guillotine certificate. Its children must themselves have minimum
guillotine certificates, by replacement of any nonoptimal subtree. This
gives `T_opt`. It does not show that arbitrary certificates have the same
size, nor that computing the optimal cut is efficient.

### Oblivious rules

For I0 on `[0,1]^n`, the source constructs a fixed
`a in [1/3,2/3]^n` for the objective `2alpha ||y-a||_1`. At every split of
the rule's predetermined chain, retain the middle third of the larger
piece of a possible-location interval. Each coordinate's location interval
shrinks by at most a factor six per split in that coordinate and stays at
least its own length from the node endpoints. A nested compact intersection
selects `a`. At depth `k`, some coordinate has at most `k/n` splits, so

```
q_Bk(a) >= 36^(-k/n)/9.
```

These chain nodes are invalid for
`k < n log_36(alpha/(9epsilon))`. Cutting each coordinate at `a_i` gives
a valid guillotine certificate with at most `2^n` leaves. Hence the rule's
ratio is at least

```
[2 ceil(n log_36(alpha/(9epsilon)))+1]/(2^(n+1)-1),
0<epsilon<alpha/9.
```

The fixed bad location is obtained before choosing the tolerance only
because I0 excludes tolerance-dependent cuts. The result is existential
over bad locations, not a bound for every kink position.

### Coordinate ambiguity in dimension n

The separable note's Theorems C and C' are valid under their explicit
parameters. With `epsilon=1/100`, take `c=1/(5n)` in the admissible interval

```
epsilon(2n-1)/(2n(n-1)) < c < (1+2epsilon)/(4n).
```

The `n` instances use one rigid coordinate and `n-1` nonrigid coordinates.
Their root minimizer, root value, incumbent, and objective germs at the
root minimizer and all corners coincide. Cutting the rigid coordinate at
`1/2` gives two valid leaves. Cutting any other coordinate at any point
gives two invalid children. Thus every deterministic I1 rule has ratio at
least `7/3`, and every randomized rule at least `(7-4/n)/3` on some instance.

At a corner node whose rigid coordinate has not yet been cut, all still
possible rigid labels give identical local information. The node remains
invalid because `nc>3epsilon/2`. A cut in a free coordinate yields two
corner descendants; re-cutting a used coordinate yields only one and adds
work. Contracting re-cut chains gives at least `2^d` branching nodes after
`d` free coordinates have been cut. Each is counted for its `n-d` possible
rigid labels. Therefore, writing `N_i` for this count on label `i`,

```
sum_i N_i >= sum_(d=0)^(n-1) 2^d(n-d) = 2^(n+1)-n-2.
```

If coordinate `j` is cut at the root, `N_j=1`, which strengthens the
deterministic averaging bound. The complete analytic lower bounds are

```
max_i T(A_i) >= 2 ceil((2^(n+1)-n-3)/(n-1)) + 1,
max_i E[T(A_i)] >= 2(2^(n+1)-n-2)/n + 1.
```

Divide these by three for tree ratios. They force exponential dependence
on dimension in any prospective constant, but not growth in accuracy at a
fixed dimension. The exact minimax values `G(2..6)=3,5,9,15,25` have recorded
computational provenance; they are not needed for the analytic exponential
bound and should not be made a necessary manuscript proof step.

The iterated result needs node-locality and coordinate-wise minimizer
selection. A method that learns the rigid coordinate from completed
subtrees can finish these examples with `O(n)` nodes. The construction is
piecewise quadratic and nonanalytic; it does not refute full-information
optimality on analytic germ classes.

## 4. Safe clamps: exact statements and their limits

For an interval of width `w`, a `theta`-safe rule chooses a split in
`[l+theta w,u-theta w]`, with `0<theta<1/2`. Every child width is at most
`(1-theta)w`, so every path halves its width after at most
`ceil(log 2 / -log(1-theta))` splits. This is a safeguard against arbitrary
relaxation points at a variable bound; exact-gap 1D minimizers on invalid
nodes are already strictly interior, so these are different assumptions.

Use `f_a(y)=2alpha|y-a|` on `[0,1]`. A node containing `a` in its interior
has unique relaxation minimizer `a` and is invalid exactly when
`alpha(a-l)(u-a)>epsilon`; nodes lying on one side of `a` are valid. When
the root is invalid, cutting at `a` gives `N_part=2` and three nodes.

### Persistent clipping and midpoint mixing

For fixed `lambda in [0,1]` and `theta in [0,1/2)`, define the relative
split map

```
pi(p)=clip(lambda p+(1-lambda)/2,theta,1-theta).
```

Unless `(lambda,theta)=(1,0)`, continuity gives a root
`p in (0,1/2)` of `pi(p)=p/(1-p)`: the difference is positive at zero and
negative at one half. Put `kappa=p/(1-p)`. On the fixed kink at `a=p`, the
child containing the kink has width multiplied by `kappa`, and the kink's
relative position alternates between `p` and `1-p`. Therefore the tree has
at least

```
2 ceil(log(alpha p(1-p)/epsilon)/(2 log(1/kappa)))+1
```

nodes. Within this fixed family the pure minimizer rule is the only member
with bounded ratio. This does not say every safe deterministic rule traps.

For the SCIP-style width-dependent formula recorded in the notes, with
global width one,

```
mu=3/4 if w>=1/2, otherwise mu=3w/4,
split=clip(mu mid+(1-mu)y_B,l+w/5,u-w/5),
```

the kink `a=3/238` has first split `45/119`, then a binding clamp at
`9/119`. The kink then sits at relative position `1/6`; later positions
alternate between `1/6` and `5/6`, with width multiplied by `1/5`. This
proves logarithmic growth for the formula inside the idealized oracle
model. The software's absolute distance guards eventually dominate, so
this is not an asymptotic theorem about floating-point SCIP. The numerical
guard threshold is historical evidence in the notes, not reverified here.
The primary source for the current formula/defaults belongs to the
literature/software evidence owner. No claim about current defaults should
be inferred merely from the historical September source check.

### The price of safety

If `a<theta`, define
`J=ceil(log(theta/a)/log(1/theta))`. Along the kink-containing child, the
first `J` allowed cuts must lie to the right of `a`, the left endpoint
remains zero, and width cannot shrink by more than a factor `theta` per
cut. If `epsilon < alpha a^2(1-theta)/theta`, these first `J` chain nodes
are invalid. Thus every safe rule, with any information and with any
randomization, has `T>=2J+1`. A run that ends by actually cutting the kink
needs at least `J+1` splits. Taking
`a=sqrt(2theta epsilon/(alpha(1-theta)))` gives an unbounded worst-case
ratio of logarithmic order. Here the kink changes with the tolerance.

This obstruction is the split restriction, not indistinguishability: even
an oracle that knows the kink is prohibited from cutting it while it is
too near an endpoint. For a fixed kink, safe boundedness as
`epsilon` tends to zero is still possible.

### Recentring: a deterministic repair

For `0<theta<=1/3`, cut at `p` if it is in the safe middle region; below
that region cut at `l+max(theta w,2(p-l))`, with a reflected formula above.
The result stays safe since `2theta<=1-theta`. Writing
`d=min((a-l)/w,(u-a)/w)`, its dynamics are

- `d<theta/2`: ordinary clipping, with new distance `d/theta<1/2`;
- `theta/2<=d<theta`: a recentring cut makes the kink the child's center;
- `d>=theta`: a cut at the kink ends the chain.

If `d0` is the initial distance, put
`J=min{j>=0:d0>=theta^(j+1)}` and
`m=min{j>=0:d0>=theta^(j+1)/2}`. After `m` ordinary clamps the distance is
at least `theta/2`. If it is already at least `theta`, then `m=J` and one
more split suffices. Otherwise `J=m+1` and a recentring split followed by
the exact kink split suffices. Thus the **zero-tolerance chain** hits the
kink in exactly `J+1` splits, which is minimum among safe rules that hit
the kink. At a positive tolerance, pruning may stop earlier; the safe
statement is `T<=2J+3`, with equality for sufficiently small tolerances.
Do not claim split-optimality among all finite-tolerance certificates from
this hitting-time argument.

The midpoint fallback also escapes every kink for `theta<=1/3`, by doubling
its relative distance until it enters the middle region. Consequently the
trap theorem must be limited to **clip schedules whose fallback is the
inner endpoint of the clamp zone**. Schedules may depend on the box path
but not on the hidden point's position within a zone.

For such clip schedules in `[theta0,theta1]`, `theta1<1/2`, nested left/right
zones give an uncountable null trap set. Alternating itineraries have
`rho(1-rho)>=theta0/4`; itineraries with runs of at most two have only
`rho(1-rho)>=theta0^2/4`. Preserve that difference in constants. On the
McCormick kink with x-only selection the bound magnitude is linear in
x-width, not quadratic, so its logarithmic chain constant differs from
the 1D exact-gap constant. The polynomial widest-side lower bound requires
that the x-clamp depend only on its x-interval history and that y-cuts are
safe; these are genuine additional assumptions.

### Randomized clamps and selection

For independent `theta~Uniform[theta0,theta1]`, let
`D=theta1-theta0`, `delta=log(1/theta1)-theta0/D>0`, and
`mu=E log(1/theta)`. The source's proved hitting-time bounds are

```
E[S] <= 1+theta1/(D delta)+log(1/d0)/delta,
E[S] = log(1/d0)/mu + O(1) as d0 tends to zero.
```

These imply fixed-kink bounded expected nodes in 1D and with x-only
selection. The condition `delta>0` must remain; evidence for narrow windows
is not a theorem. Under widest-side selection in the McCormick model,
the expected node count instead has a proved logarithmic lower bound for
kinks in the stated clamp window. Fitted positive power laws are
experimental conjectures. Keying a draw by `(variable,interval)` preserves
pathwise draw distributions and therefore the mean node count; keying by
`interval` alone does not.

The incumbent-coordinate rule has at most one unsafe split per distinct
incumbent coordinate value on a path, since after that split the value is
an endpoint of every descendant interval on that path. It is not a
uniformly safe rule. Its three-node kink behavior needs an optimal
incumbent and, in the McCormick example, selection of x first.

## 5. Higher dimensions and a completed supporting extension

The clean negative example for `multi` is `f(x,z)=x^2` on `[0,1]^2`,
`alpha=1`. Its z-minimizer is the midpoint; its x-minimizer is `(l+u)/4`
when `u>3l`, otherwise the endpoint `l`. The source constructs a valid
guillotine certificate with `O(epsilon^(-1/2))` leaves, while `multi` has
`Omega(epsilon^(-1/2) log(1/epsilon))` internal nodes. Thus splitting at
the correct relaxation point in every available coordinate is not
competitive. Four-way splits are counted as one parent and four children;
`T>=2I+1` is still valid, and replacing them by binary cuts only increases
the counted work. In the source's floor definition of `K`, equality at an
accuracy threshold is harmless because the x-value estimate is strict.

For separable objectives, define
`F_i(J)=min_J(m_i-alpha q_J)` and 1D budget counts `N_i(b)`, with
`min m_i=0`. The correct elementary bracket is

```
max_i N_i(epsilon) <= N_part(epsilon) <= N_guill(epsilon)
  <= min_(sum_i epsilon_i=epsilon) product_i N_i(epsilon_i).
```

The slice uses the whole tolerance; the product uses split tolerances.
Their orders can differ by a logarithm. Dyadic cap functions and quadratics
have `N_i(b)=Theta(log(1/b))`, yet their two-coordinate sums have,
respectively, `Theta(log^2(1/epsilon))` and `Theta(log(1/epsilon))`
certificate counts. This rules out formulas based only on the orders of
the 1D sizes, not every imaginable formula using their exact values.

The phase lemma is sound for `omega`, but the sum of certificate traces
over all phases is not controlled in general. The analogous phase claim
for the deficit rule is explicitly refuted. Grid-restricted optima give
upper bounds on true optimal certificate sizes, so ratios against those
grid optima are **lower bounds** on loss, never certified upper bounds on
competitiveness.

### Completed induction for one arbitrary coordinate and r sharp coordinates

This repairs the sketch after Theorem B of `separable-omega.md`. It is
optional supporting material; its constants are intentionally conservative.
Scale to `alpha=1`. A sharp coordinate at `c` means: on every interval
straddling `c` its relaxation minimizer is `c` with value `-q_J(c)`;
on either side its minimizer has zero gap and nonnegative value. Assume
`m_i(c)=0`. After a split at `c`, each resulting half has value exactly
zero, because it contains `c` and is nonnegative. It has zero minimizer
gap and can never be selected by `omega` on an invalid node.

Let `N_A(epsilon)` be the best 1D budget certificate for an arbitrary
coordinate interval `A`. Put `C0=4`. For `r>=1` define

```
c_r = r[2r(r+1)+1],
A_r = 4(1+c_r),
C_r = (A_r+1)+2 C_(r-1)(A_r+2).
```

**Proposition.** Starting with one arbitrary coordinate on `A` and `r`
unsplit sharp intervals, with all already-cut sharp intervals on one side
of their kink, `omega` finishes with at most `C_r N_A(epsilon)` leaves.
Hence on the full problem
`T_omega <= 2 C_r N_part(epsilon)-1`.

**Proof.** The assertion for `r=0` is the 1D theorem. For `r>=1`, freeze
the sharp coordinates until the first sharp split on each branch. Their
gap values are constants `omega_j>0`; put
`tau=max_j omega_j`, `beta=epsilon-sum_j omega_j`, and
`b=beta+r tau>=epsilon`. The first x-phase is a subtree of
`S(A;beta,tau)` from the phase lemma. If `N=N_A(epsilon)`, monotonicity of
budget counts gives `N_A(b)<=N`, and the phase lemma bounds its internal
nodes by `A_r N`. This includes `N_A(b)=1`, where the bound is `c_r`.
Thus its frontier partitions `A` into `H<= (A_r+1)N` intervals `A_j`.

Refine an optimal budget-epsilon partition of `A` by the `H-1` frontier
breakpoints. At most `H-1` additional intervals are created, and every
piece remains valid. Consequently

```
sum_j N_Aj(epsilon) <= N+H-1 <= (A_r+2)N.
```

A frontier node is either valid or splits one sharp coordinate at its
kink, leaving two problems with `r-1` unsplit sharp coordinates and zero
contribution from the newly split coordinate. Apply the induction bound
to both children. The final number of leaves is at most

```
H+2 C_(r-1) sum_j N_Aj(epsilon)
 <= [(A_r+1)+2 C_(r-1)(A_r+2)] N = C_r N.
```

The frozen phase is finite, and induction proves termination of every
remaining subtree. Finally slice the original certificate at all sharp
kinks to get `N_A(epsilon)<=N_part(epsilon)`. This completes the proof.
It allows either coordinate tie order and any coordinate-wise minimizer
selection. It does not prove the result for arbitrary separable objectives
or for the deficit rule with multiple sharp coordinates.

## 6. The decomposition comparison: complete safe statements

Let a rooted tree decomposition have bags `V_t`, separators
`S_t=V_t intersection V_parent`, width `w=max |V_t|-1`, and assigned bag
objectives `a_t=sum_(factors assigned to t) f_c`. Keep the same factor
assignment and per-factor relaxation on both sides of the comparison.
Let `M` be the number of bags, `k` the maximum number of bags containing a
variable, and `Delta` the maximum number of children. Width alone does
not bound `k` or the constants controlling repeated separator copies.

A decomposition certificate contains separator cell partitions with affine
minorants `ell_(t,D)`, local bag leaf partitions, and convex child functions
`psi_(u,B)` below every child-cell minorant on the intersecting region.
Every leaf relaxation dominates its own cell minorant, with a root
number `ell_r`. Its **size** is local leaves plus separator cells. Validity
follows by induction from the leaves: factor relaxations are below factors,
the children's minorants are below subtree value functions, and the local
inequality gives the parent's minorant. At the root `ell_r<=f*`.

When a single slope `lambda_t` is used on each separator, the maximal
intercepts unfold into a minimum over configurations. A configuration
chooses independent bag copies `z^t` in local leaves and separator cells
meeting the parent leaf. Its value is

```
sum_t sum_(c assigned to t) f_(c,Bt)(z_c^t)
  + sum_(t != root) lambda_t^T(z_parent^t_S - z_t_S).
```

This equality is exact, not a heuristic DP interpretation. The copies need
not agree: intersections of cells with parent leaves control only their
distance. An implicit combination of local members can represent
exponentially many virtual global boxes.

### Existence of small certificates under quadratic growth

Theorem 3.4 of `decomposition-certificates.md` is sound under the following
explicit hypotheses:

- `F-f* >= c_g ||x-x*||_2^2` on the whole root box, with one minimizer;
- every assigned bag objective has `M_a`-Lipschitz gradient on its box;
- every factor relaxation has vertex-vanishing error at most
  `alpha' q_(B_c)`, with `A` an upper bound on the sum of relaxed factor
  arities assigned to a bag;
- bounded `k`, `Delta`, and the admissible shell-width constants below.

For exact center and slopes, a sufficient choice is

```
D_k = sum_(j=1)^(k-1) Delta^j,
K1 = max(1,(k-1)sum_(j=0)^(k-2) Delta^j),
Q = M_a^2 w k/c_g + M_a w/2 + alpha' A,
theta=2^(-mu)<=1/2,
4theta sqrt((k-1)D_k)<=1/2,
theta^2 k[48K1(1+Delta)Q+alpha' A]<=c_g/2,
h^2 <= epsilon/[4M(768K1 Q+3alpha' A)].
```

With separator and bag shell partitions centered at `x*`, and slopes equal
to subtree factor gradients at `x*`, the certificate is valid with
`ell_r>=f*-epsilon` and has size at most

```
2M (4/theta)^(w+1) [1+max(0,ceil(log2(s0/h)))].
```

Using this last count avoids the large-tolerance logarithm defect. For
bounded structural and conditioning parameters it is
`O(M C^(w+1) log(M/epsilon))` in the small-tolerance regime. It is an
existence theorem; it does not assume stationarity and permits a boundary
minimizer.

The mechanism is complete and can be stated compactly in the paper. Define
the consistent point `x_i` from the topmost bag copy containing coordinate
`i`. Running intersection gives the telescoping gradient identity

```
sum_t grad a_t(x*)^T(z^t-x_Vt)
  = sum_(t != root) lambda_t(x*)^T(z^t_S-z_parent^t_S).
```

Thus first-order copy errors cancel, leaving Taylor errors proportional to
`M_a ||x_Vt-x*_Vt|| Delta_t` and `M_a Delta_t^2`, where `Delta_t` measures
copy drift. A coordinate appears in at most `k` bags, so its drift
telescopes through at most `k-1` edges. Shell widths satisfy
`width <= h+theta distance_to_x*`. If `d_t` is edge drift and `rho_t` is
bag distance, the source's explicit estimates yield

```
sum_t d_t^2 <=48[16M h^2+theta^2(1+Delta)k||x-x*||_2^2],
sum_t Delta_t^2 <= K1 sum_t d_t^2.
```

The first smallness condition bounds the operator that passes drift down
the tree by one half. Young's inequality assigns the mixed Taylor errors
partly to the growth margin; the remaining squared drift and per-factor
errors are absorbed by the second condition. For exact slopes the total
loss is bounded by a strict fraction of `c_g||x-x*||^2` plus
`M h^2(768K1 Q+3alpha' A)`. The prescribed `h` makes the last term at most
`epsilon/4`, proving the root bound. Shell annuli contribute a constant
number of local members at each dyadic scale, which gives the logarithm.
This proof needs neither value-function smoothness nor an unproved
regularity statement near remote kinks.

The source allows an approximate center within `h` in sup norm and slope
errors of order `sqrt(epsilon)` in total Euclidean norm, subject to its
explicit T3 inequalities. Do not replace these by an arbitrary Euclidean
center error of that order: the central mesh must still control
`M h^2`. For a minimal core use the exact-center existence result and
present algorithmic location of that center separately.

### The fixed path family and explicit separation

For `n>=3`, take the root `[-1,1]^n` and

```
F_n=sum_i(x_i^2-0.1x_i^4)+0.8sum_(i=1)^(n-1) x_i x_(i+1).
```

Keep each unary term exact and relax each bilinear term separately by
alphaBB with coefficient `0.4`. Use path bags `{i,i+1}` with the same
assigned factors. The function has `f*=0`, unique nondegenerate minimizer
zero, and global growth `F_n>=0.1||x||_2^2`. It is nonconvex for `n>=3`:
at the all-ones point the Hessian has eigenvalue
`0.8-1.6cos(pi/(n+1))<0`. These facts make the example stronger than a
comparison based on flat or degenerate minima.

Every spatial cover valid for this termwise alphaBB oracle has at least

```
max{0.068 sqrt(n)(2e/pi)^(n/2) log(0.2/(n epsilon)),
    (5/3)^n exp[-(5/9)(1+1.25epsilon)]}
```

members. The first term is useful only for `epsilon<0.2/n` and follows
from the weighted arcsine integral bound. For this path,
`product_i alpha_i=0.8^n/4`; the upper quadratic Hessian is
`H=tridiag(0.8,2,0.8)`, with
`det H <= (4/3)1.6^n` and `lambda_min(H)>=0.4`. Integrating over an
inscribed Hessian ellipsoid yields the first term. The second term is
imported from the face-exact notes; the manuscript should provide that
bound's proof or a proved preceding theorem, not cite an internal note as
if it were a published theorem.

The same oracle admits a path decomposition certificate of size at most

```
U_dec = 3.36e7(n-1)[(1/2)log2(1.96e6(n-1)/epsilon)+2].
```

For this specialization `k=2`, `Delta=1`, `w=1`, `M_a=2.8`, `c_g=0.1`,
`alpha'A=0.8`, `Q=159`, and `theta=2^-10` satisfies the required
inequalities. Slopes are zero because the center is zero. The source also
gives the certificate lower bound
`0.2778(n-1)log(1+0.6/epsilon)` for the fixed path decomposition with
alphaBB.

For every `0<epsilon<=10^-4`, the lower spatial bound divided by `U_dec`
is at least

```
3e-10 (2e/pi)^(n/2)/sqrt(n).
```

One needs both spatial terms to make this ratio uniform in accuracy. If
`epsilon<=0.04/n^2`, the first numerator logarithm controls a fixed
fraction of `log(1/epsilon)` and cancels the denominator logarithm. In
the complementary range `0.04/n^2<epsilon<=10^-4`, the second term covers
the numerator, while `log(n/epsilon)=O(log n)`; its larger exponential
base dominates the remaining polynomial. Keep the exact base
`sqrt(2e/pi)` or round it downward; replacing it by `1.3155` rounds upward
and invalidates a theorem quantified over all `n`.

With termwise McCormick on both sides, the second spatial bound and the
decomposition upper bound still hold, but the alphaBB integral logarithm
and the displayed decomposition lower bound do not transfer. The resulting
safe ratio is
`c(5/3)^n/[n log(n/epsilon)]`, exponential in dimension at each fixed
tolerance, without uniformity as the tolerance tends to zero.

### What the comparison measures

For fixed binary single-tree pruning with no extra reductions,
`N_single` leaves imply `2N_single-1` relaxation solves. A lower bound
for covers also handles the final pruned family of any such tree. If bound
tightening eliminates regions, the source lower bound counts leaves **plus
the certified eliminated pieces**, not automatically just the solver's
displayed node count. Stating a node theorem needs the precise reduction
and accounting assumptions from the general framework.

In the decomposition model, checking an unaligned leaf against each
separator cell it intersects requires a separate convex program. The
source's shell family permits a leaf to meet many cells; this avoids a
product partition of bag leaves but can add a logarithm to the number of
checks. A safe generic upper bound on program count is
`sum_t |Leaves_t||Cells_t|` (with one root program per root leaf), hence
at most a quadratic function of certificate size. With the stated shell
counts and fixed width/conditioning it is at most
`O(M C^(2w+2) log^2(M/epsilon))` per bottom-up pass. No unit-cost statement
about solving those convex programs, and no bit complexity statement,
follows from their number alone.

Thus the exact uniform-in-epsilon separation is a certificate-size
separation. At a fixed tolerance it remains an exponential distinction
after polynomial certification overhead, but a uniform ratio of actual
running times is not proved. The recorded crossovers against computed
certificates are illustrations, not a runtime theorem.

The factorization qualification is substantive. Adding convex unary
curvature to each bilinear factor can remove the stated gap mechanism.
With arbitrary functional splits based on exact conditional margins,
per-factor convex envelopes can certify the root exactly. Those margins
encode globally solved value functions, so this does not give a free
algorithm; it does preclude a lower bound uniform over all factorizations
for such envelopes. It says nothing about every possible fixed algebraic
alphaBB construction.

### Adaptive certificates

The original existence theorem knows `x*`. The subsequent LS theorem,
under monotonicity of factor relaxations as boxes shrink, constructs a
certificate without knowing `x*`, with final size
`O(M(C sqrt(M))^(w+1) log(M/epsilon))`. Its total created boxes and DP
passes carry additional logarithms. The `M^((w+1)/2)` cost is real for LS;
it is not an impossibility theorem for all algorithms.

GR repairs that cost for **path decompositions**, with the extra stationarity
hypothesis `grad F(x*)=0`. It uses a minimizing configuration, gradients at
the preceding consistent point, and graded refinement around each bag
copy. With the source's explicit sufficiently small `theta` and large
`R`, it uses `O(M C^(w+1) log(M/epsilon))` created boxes and logarithmically
many DP passes; unknown constants add a logarithm by capped dovetailing.
The base has worse conditioning dependence than the existence theorem.
Do not infer a useful practical constant from the asymptotic form.

The path localization proof is an exchange on a window with only two
boundary edges. The October 2 note refutes the unrestricted replacement
of that window argument on arbitrary branching trees. The theorem's
stationarity assumption also prevents claiming its incumbent-gap estimate
at arbitrary boundary minimizers.

## 7. Consistency, covering, and the precise structural quantities

The exact-bag split model is useful to explain what separator refinement
must approximate. For bounded bag functions on product boxes, set

```
F_t^phi = F_t + sum_(child edges e) phi_e - phi_parent,
rho(phi)=sum_t inf F_t^phi,        gap(phi)=f*-rho(phi).
```

The split functions telescope on consistent global points, so `gap>=0`.
For edge `e`, let `U_e` be the conditional child-side value function and
`V_e` the parent-side value function. Put `L_e=f*-V_e` and
`w_e=U_e-L_e>=0`. The band of exact one-edge splits is `[L_e,U_e]`.
With compact continuous data, `w_e(s)` is the smallest global objective
margin among points with separator value `s`; consequently its sublevel
sets are projected near-optimal sets.

### One separator: the complete band identity

For a linear class `Phi` containing constants,

```
gap(Phi)=inf_(phi in Phi)[sup(phi-U)+sup(L-phi)]
         =2 dist_inf(Phi,{psi:L<=psi<=U}).
```

The first equality follows from conditioning the two bag infima on the
separator. For the second, every band element `psi` bounds the bracket
above by `osc(phi-psi)`; optimizing a constant shift turns oscillation
into twice a uniform distance. Conversely set
`a=sup(phi-U)`, `b=sup(L-phi)`. Since `inf w=0`, `a+b>=0`. Shift `phi` so
`a,b>=0`, and clip it into the band. Its distance from the clipped function
has range in `[-b,a]`; a further constant centering bounds twice the
distance by `a+b`. This proves both directions without assuming an attained
pinch point. Continuous functions remain continuous under clipping.

The identity concerns approximation to **some band element**, not to a
specified value function. Positive band width can absorb approximation
error away from optimal separator values. In a cellwise class, independent
cell constants balance the two suprema, and the gap is the maximum of
the cell brackets, not their sum.

### Trees: compatibility is essential

For original edge bands and one joint exact split `psi`, the safe bounds
are

```
2max_e dist_inf(Phi_e,Band_e)
 <=gap(Phi)
 <=2 inf_(psi jointly exact) sum_e dist_inf(psi_e,Phi_e)
 <=2sum_e dist_inf(U_e,Phi_e).
```

The upper bound telescopes the oscillations of perturbations of one exact
split. For the lower bound, enlarge all classes except the chosen edge to
all bounded functions; exact DP then merges each side and reduces the
problem to the one-separator identity. Separate infima over the original
edge bands are insufficient. In the three-bag example

```
a(s1)=10(1-s1),
b(s1,s2)=s1+s2-s1s2,
c(s2)=10(1-s2),       s1,s2 in [0,1],
```

both original bands contain zero, but constants on both edges give root
bound zero while `f*=1`. The resulting gap is one.

A minor proof repair: the sequential-band proposition in the notes permits
bounded data without attained minima but appeals to a pinch point. Replace
that appeal by a minimizing sequence. Since
`f* <= V(s)+psi(s) <= U(s)+V(s)` for `L<=psi<=U`, the reduced problem has
infimum `f*`. Along a sequence with `U+V` tending to `f*`,
`0<=U-psi<=w` tends to zero, so the removed leaf has infimum zero. This
proves the same proposition without an attainment assumption.

### Pointwise admissibility

For any chosen split, define reduced child functions and errors

```
U_t^phi(s)=inf_(z_S=s)[F_t(z)+sum_child phi_u(z_Su)],
c_t=inf(U_t^phi-phi_t),
delta_t=U_t^phi-phi_t-c_t>=0.
```

Bottom-up substitution gives the exact identity

```
gap(phi)=sup_x[sum_edges delta_e(x_Se)-(F(x)-f*)].
```

Bag relaxation errors enter the same sum when the reduced functions use
relaxed bags. This identifies the missing coupling: errors are measured
against reduced value functions, which depend on splits farther down the
tree, rather than independently against the original bands.

For decomposition certificates, the chain inequality instead gives the
necessary pointwise budget
`sum_t e_t(x_Vt)<=epsilon+eta` on the near-optimal set `E(eta)`, where
`e_t` is the smallest local leaf gap covering that bag point. Vertices of
those leaves give variable-radius coverings. Retain their Euclidean form
when adding coordinate gaps: a sup-norm description can lose
`w^(Theta(w))` because it forgets that squared coordinate distances add.

The static quantity that first allocates constants
`epsilon_t` with sum `epsilon` and then adds projected bag covering numbers
can overcharge by `M^(d/2)/log M` in the mixed-integer staircase example.
Only one bag is fat at any single optimal point, so its whole tolerance can
be used there. Different bags are fat at different points; a fixed allocation
does not represent this. The counterexample is proved with binary
separators; the continuous-separator modification is a sketch and must
not be promoted to a theorem.

### A safe exact-bag covering theorem

The graded exact split is the sound bridge for trees with at least one
edge. Write `q>=1` for the number of edges, avoiding conflict with the
original variable dimension. A one-bag problem has no separator error.
For each edge let `E_e` be the number of edges strictly below it and put

```
theta_e=(2E_e+1)/(2q),
psi_e=U_e-theta_e w_e,       tau=1/(2q).
```

Then `psi` is jointly exact, and any perturbation `r` satisfies

```
gap(psi+r) <= sum_e[sup(r_e-tau w_e)+sup(-r_e-tau w_e)].
```

For completeness, let `g_t>=0` be the DP margin in bag `t` and let
`W_t` be the conditional global margin with that bag fixed. Running
intersection gives `W_t=w_parent+g_t` and `W_t>=w_e` for every incident
separator. Write the per-bag deficit as a sum of the displayed discounted
perturbations and a residual weighted sum of separator margins minus
`W_t`. The coefficient identity

```
theta_parent=sum_child(theta_e+tau)+tau
```

makes the residual nonpositive at nonroot bags; at the root the child
coefficients add to one. Summing bag deficits proves the inequality. Taking
`r=0` proves exactness. Choosing independent affine pieces and balancing
their cell intercepts bounds the gap by the sum over edges of their worst
discounted cell brackets. Reversing the grading has no such identity and
need not be exact.

Assume every separator is one-dimensional, `U_e` is `M_e`-semiconcave,
`L_e` is `M_e`-semiconvex, and both are `G_e`-Lipschitz. These properties
follow from suitable `C^{1,1}` box data; they are explicit hypotheses,
not a guarantee under arbitrary constraints. Rule R3 dyadically refines
cells using the following bounds, where `r` is cell half-width and
`w_min=min_D w_e`:

```
B(D)=(32q+1/2)M_e r^2-w_min/(2q)
     when dist(D,boundary)>=8q r,
B(D)=2G_e r+(5/2)M_e r^2-w_min/q otherwise.
```

Split while `B(D)>epsilon/q`. On final cells use affine pieces minimizing
the discounted bracket. The complete proved count is

```
|P_e| <=1+(8q+2)J_e N_e+8q J'_e,
N_e=sup_(eta>=0) N_inf(pi_Se E(eta),2sqrt((epsilon+eta)/M_e)),
J_e=max(0,ceil(log2(length(I_e)*sqrt((64q^2+q)M_e/(8epsilon))))),
J'_e=max(0,ceil(log2(length(I_e)/(2rho_e)))),
rho_e=min(epsilon/(4qG_e),sqrt(epsilon/(5qM_e))).
```

Use positive upper bounds `M_e,G_e` if either minimal regularity constant
is zero, or state the obvious limiting zero-error cases separately.
Refining ends at finite depth because both brackets tend to at most zero.
Each split interior cell meets a projected near-optimal sublevel set at
its scale, and each covering interval meets at most `8q+2` dyadic cells.
At most `8q` cells per scale lie near the two endpoints. This supplies the
count, with logarithms from the number of scales. The local affine-error
estimate follows from the sharp one-dimensional slope-variation bound

```
Delta_U([c-h/2,c+h/2])+Delta_L([c-h/2,c+h/2])
 <=4 w(c)/h+4M_e h,
```

proved by setting `phi=L+M_e(s-c)^2/2-[U-M_e(s-c)^2/2]`, using its
convex chord-slope inequalities on the two exterior half-intervals, and
`phi(c-h/2)+phi(c+h/2)>=2phi(c)`. R3 deliberately uses the weaker
constants eight. The notes' sharper R3 constants are a short algebraic
extension, but using the already reviewed version avoids a needless new
algorithm statement.

This theorem is self-contained in the **exact-bag model**, where bag
infima may themselves be hard global problems. It counts separator cells;
it does not pay for approximating those infima. The relaxed-bag extension
requires aligned leaves and suitable affine slopes, and only gives a
sufficient condition. General pointwise tolerance allocation for relaxed
bags remains unresolved. The proposed `C^{1,1}` band insertion argument in
the consistency note also has explicit unresolved extension/localization
steps; it is unnecessary for the proved 1D-separator theorem and should
remain a sketch if mentioned.

## 8. Minimal manuscript core and overlap advice

A coherent core for these topics can use the following sequence:

1. Fix the relaxation oracle, incumbent convention, and certificate/tree
   counting model. Distinguish arbitrary covers, partitions, and guillotine
   trees.
2. Present the 1D minimizer theorem with its crossing proof. Give the
   five-node two-piece refinement and the exact meaning of 4-competitive.
3. Contrast relaxation information, full information, oblivious cuts, and
   persistent safeguards. Include the nonanalytic ambiguity pair and the
   complete recentring tradeoff; explain analyticity explicitly.
4. Use `multi` and coordinate ambiguity to demonstrate why dimension and
   coordinate selection add structure. Leave general `omega` competitiveness
   open. The completed sharp-coordinate induction is optional.
5. Define decomposition certificates, prove validity/unfolding, and give
   the fixed path separation with size and checking costs stated separately.
   Present the growth-based existence proof as the main mechanism, then the
   narrower adaptive path theorem if needed.
6. Use the band identity, incompatibility example, and pointwise
   admissibility to explain separator accuracy. Present graded covering only
   if the manuscript can keep the exact-bag/relaxed-bag distinction visible.

`paper-relaxation-limits` already treats termwise relaxation gaps, spatial
certificate lower bounds, and representation dependence. Attribute overlap
there; the competitiveness and safe-clamp analysis studies selection of a
tree relative to its certificates and is a distinct question.
`paper-decomposition-aware` now uses certified coordinate grids, corrected
DP, growth-dependent algorithms, bit complexity for rational quadratic
models, recourse, and structural limits. Its grid/path certificates are
different objects from the unaligned affine-cell certificates audited here.
Do not use its later algorithmic conclusions as if they were proofs of the
September certificate model, and do not present a repeated growth/sparsity
message as a separately new discovery. Cross-reference its stronger
algorithmic results where appropriate, while the present comparison fixes
the termwise oracle and analyzes the source of its tree-size obstruction.

The source notes identify a 1991 minimizer-rule precedent and older
decomposition bound-validity/approximate-DP precedents. This audit has not
checked those primary sources. Novelty language must come from the assigned
literature evidence, with theorem-level hypotheses compared, not from the
notes' unsuccessful searches. No result here proves practical solver speedup.

## 9. Evidence and verification record

Primary source locations inspected:

- `research-20260928b/bb-complexity/branching-competitiveness/competitive-branching.md`:
  model, Sections 3–6, and revised scope.
- `research-20260928b/bb-complexity/branching-competitiveness/n-dimensional.md`:
  radius failure, `multi`, guillotine refinement, and separable brackets.
- `research-20260928b/bb-complexity/branching-competitiveness/separable-omega.md`:
  coordinate-wise selection, phase lemma, sharp theorem, dyadic caps, and
  coordinate-ambiguity proof including the closing correction.
- `research-20260928b/bb-complexity/robust-branching-points/robust-branching.md`:
  rules, safety, trap sets, randomization, recentring, and revised scopes.
- `formal/topics/33-competitive-branching/{CLAIMS,VERIFICATION,README}.md`,
  its statement review, and `formal/Formal/CompetitiveBranching/` model,
  pruning, counting, and final theorem declarations.
- `research-20260929/theory-decomposition/{decomposition-certificates,extension-adaptive,adaptive-matching,covering-upper-half}.md`:
  models, relevant proof sections, status tables, and revisions.
- `research-20260929/theory-consistency/consistency-relaxations.md`:
  split model, band proof, tree sandwich, counterexample, and incomplete
  insertion argument.
- The matching competitive, separable, robust, decomposition, consistency,
  adaptive, and covering reviews and confirmations; the September 28
  closing audit; the October 2 correction embedded in adaptive matching.
- `paper-decomposition-aware/{main,sections/abstract,sections/intro,sections/limits}.tex`
  and relevant framing in `paper-relaxation-limits/main.tex` for overlap.

Targeted mathematical verification actually run in this audit:

```
python3 - <<'PY'
import sympy as s
from fractions import Fraction as F
l,u,y1,y2,z,ss,lam,d,e,t1,t2 = s.symbols('l u y1 y2 z ss lam d e t1 t2')
checks = {
 'minimizer_chain_identity': (t1+d)*(e-t1)-(t2+d)*(e-t2)+(t2+d)*(t1-t2)-(t1-t2)*(e-t1),
 'two_interval_left_identity': (z-y2)*(y1-z)+(y2-l)*(y1-y2)-(z-l)*(y1-z)-(y2-l)*(z-y2),
 'two_interval_right_identity': (z-y2)*(y1-z)+(y1-l)*(u-y1)-(z-l)*(u-z)-(y1-z)*((u-y1)-(y2-l)),
}
for label, expr in checks.items():
 assert s.expand(expr)==0, label
 print(label + ': PASS')
a=F(3,238); root_split=F(3,8)+a/F(4); width1=root_split; mu1=F(3,4)*width1
assert root_split==F(45,119)
assert mu1*width1/F(2)+(1-mu1)*a < width1/F(5)
assert a/(width1/F(5))==F(1,6)
print('SCIP-formula transient identities: PASS')
Q=F(28,10)**2*2/F(1,10)+F(28,10)/2+F(8,10)
assert Q==159
th=F(1,1024)
assert 4*th<=F(1,2)
assert th**2*2*(96*Q+F(8,10))<=F(1,20)
assert 2*(4/th)**2 < 33_600_000
print('path decomposition constants: PASS')
PY
```

Result: exit zero; all five printed checks passed. These are new algebraic
identity and rational-constant checks, not reruns of experiments. The source
proofs were reviewed by hand as described above. No full-project check,
experiment script, Lean build, software-default query, or CI check was run.
