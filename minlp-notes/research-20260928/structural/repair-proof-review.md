# Independent proof-review record for feasible repair and separator penalties

Date: 2026-09-28. This records mathematical review, not Lean verification,
publication readiness, or a novelty verdict.

## Review A: sharp repair transfer and terminal obstruction

Author/investigator: `/root/frontier_structural/repair_probe`.
Independent reviewer:
`/root/frontier_structural/repair_probe/terminal_obstruction_review`.

The reviewer received the mathematical statements and proposed proofs in
messages before [repair-probe.md](repair-probe.md) was written. The reviewed
version consisted of these two claims:

1. For a finite tree of nonempty compact metric bag sets, continuous separator
   maps, and nonempty exact-consistency set, the best constant in
   `dist_D(z,F) <= C r(z)^alpha`, `0 < alpha <= 1`, equals the best constant
   in `H(mu) <= C R(mu)^alpha`, using the identical summed bag and separator
   metrics defined in the note.
2. For `f(x)=a x^2` on `[0,1]`, `0<a<1/2`, an `m`-transition path with hard
   final state zero and free first state has repair exponent at most `2^-m`
   despite forward contraction. The local Dirac path from `t` has terminal
   residual `a^(2^m-1)t^(2^m)` and first-stage objective loss `t`.

The reviewer found no substantive error. The response specifically checked
that separator optimal couplings lift to bag couplings by disintegration,
that the edge couplings glue jointly on the tree, and that Dirac laws prove
the reverse inequality for the best constant. It identified the necessary
conditions: compact metric spaces, continuous separator maps, nonempty `F`,
the same metrics and weights in both problems, and `alpha <= 1`. It emphasized
that original integer or action marginal distributions are not preserved.

The reviewer replaced exact measurable nearest-point selection with a simpler
argument: map into a finite epsilon-net of `F`, obtaining repair cost at most
`dist_D(z,F)+epsilon`, then let epsilon tend to zero. This argument appears
in the written proof.

For the contraction example, the reviewer strengthened the proposed lower
example to the sharp bound for arbitrary input laws. With `d=2^m`,
`A=a^(d-1)`, `L=2a`, `mu_m=delta_0`, and
`r_j=W1(f#mu_j,mu_(j+1))`, transport contraction gives

```text
A integral x^d dmu_0 <= sum_j L^(m-1-j) r_j <= R.
```

Jensen gives `integral x dmu_0 <= a^(-1+2^-m) R^(2^-m)`, and the Dirac
example attains its constant. The reviewer checked the fixed-initial-state
version obtained by putting the free variable in the first action. It also
confirmed that this concerns approximate consistency, not exact separator
moment matching, and that globally compatible viable fibers are absent.

The independent reviewer did **not** review the full eventual Markdown file,
the subsequent two transport identities, the finite-union-of-polyhedra
corollary, or the source audit. The parent investigator subsequently reported
an independent reading of the full repair note and found its core proof and
sharp contraction formula sound. The targeted finite computations are recorded
separately in [source-audit.md](source-audit.md).

## Review B: penalty value and bounded separator messages

Proposer: `/root/frontier_structural`.
Independent reviewer: `/root/frontier_structural/repair_probe`.

This review concerns the exact statement sent by the proposer, not a hash of a
later extension file. Assume the compact-tree setting above, continuous local
costs `c_v`, and finite `lambda >= 0`. The reviewed claims are:

1. `min_mu [sum_v integral c_v dmu_v + lambda R(mu)]` equals
   `min_z [sum_v c_v(z_v) + lambda r(z)]`.
2. Their common value equals the attained maximum over anchored
   `lambda`-Lipschitz separator potentials of the sum of local minima of
   `c_v + signed incident potentials`.
3. Exact penalized value for **every** collection of local 1-Lipschitz costs
   holds exactly when `lambda >= Cdet`, where `Cdet` is the sharp linear
   deterministic repair constant. A strict inequality excludes infeasible
   minimizers; equality may allow infeasible tied minimizers.

**Verdict:** the statements are correct with the stated universal-cost
quantifier and finite genuine separator metrics.

For Claim 1, glue edge-optimal couplings to get a joint law whose expected
deterministic penalized cost equals the measure objective. Its expectation
cannot be below the deterministic minimum. Dirac laws prove the reverse
inequality. Nonnegativity of `lambda` is part of the proposed setting.

For Claim 2, restrict each separator domain to the compact union of its two
bag images. An anchored Lipschitz ball is compact in the uniform topology,
including when the domain is disconnected. The usual Kantorovich--Rubinstein
representation, followed by minimax, gives the proposed dual. The bilinear
function is continuous in each variable, and both the product measure domain
and the product anchored-potential domain are compact convex sets. The dual
objective is continuous in the potentials, so its maximum is attained.
For `lambda=0`, all anchored potentials vanish and the statement reduces to
independent local minimization. Different orientation conventions are valid
as long as each edge potential enters its two incident bags with opposite
signs. Anchoring subtracts edgewise constants, which cancel in the total.

There is also a direct constructive proof of attainment. Root the tree. For
every nonroot vertex `v`, let `p_v` denote its parent-separator map and define
recursively

```text
A_v(x) = c_v(x) + sum_(child w) M_w(p_(v,w)(x)),
M_v(s) = min_(x in K_v) [A_v(x) + lambda d_(parent edge)(p_v(x),s)].
```

At the root, define `A_root` by the same first formula. Ordinary elimination
on the penalized tree gives penalized value `min A_root`. Each `M_v` is
`lambda`-Lipschitz, because it is an infimum of functions sharing that
Lipschitz constant. Put `+M_v` in the parent bag and `-M_v` in bag `v`.
For every nonroot bag,

```text
min_(x in K_v) [A_v(x) - M_v(p_v(x))] = 0.
```

Indeed, the expression is nonnegative by using `x` itself in the message
minimization. At a minimizer `x*` of `A_v`, the message at `p_v(x*)` is also
at least `min A_v`, so equality holds. The sum of local dual minima is thus
`min A_root`. Subtract anchoring constants afterward. This avoids any
possible reliance on unverified infinite-dimensional minimax assumptions.

For Claim 3, `c(z) >= p* - h(z)` for every local 1-Lipschitz objective
collection. Thus `h <= lambda r` implies exact penalized value. Conversely,
if `h(z)>lambda r(z)`, the local costs `c_v(x)=d_v(z_v,x)` have feasible
minimum `h(z)`, but the penalized value at `z` is at most `lambda r(z)`.
This proves necessity and the sharp constant. Individual objectives can be
exact below the threshold; necessity is for the guarantee over all such
objective collections. If `lambda>Cdet`, an infeasible `z` has objective
at least `p*+(lambda-Cdet)r(z)>p*`. The same estimate at law level forces
`R=0` for every minimizing collection of bag laws.

### Explicit discontinuous hard-message example

Take root set `[0,1]`, coordinate `t`, and child set

```text
K_1 = {(s,y): y in {0,1}, 0 <= s <= y}.
```

Use root distance `|t-t'|`, child distance `|s-s'|+|y-y'|`, and separator
equality `t=s`. Then `h=r=|t-s|`, so `Cdet=1`. Repairing `t` to `s`
gives the upper bound; the triangle inequality gives the lower bound.
Choose costs `c_root(t)=-t` and `c_child(s,y)=y`, both local 1-Lipschitz.
The true optimum is zero.

The hard conditional child value is zero at `s=0` and one for every `s>0`;
it is discontinuous. The penalized message is `M_lambda(t)=min(lambda t,1)`.
At the sharp threshold `lambda=1`, the Lipschitz message `M(t)=t` gives
the exact certificate `-t+t=0` at the root and `y-s>=0` at the child.
This supports the proposed interpretation without assuming regularity of
hard conditional value functions.

### Significance and remaining prior comparison

The global error-bound/exact-penalty connection is established. The primary
publisher page for [*The exact penalty principle*](https://www.sciencedirect.com/science/article/abs/pii/S0362546X11001556),
Nonlinear Analysis 75(3), 2012, 1642--1654, explicitly discusses global and
local error bounds and states Clarke's distance-penalty theorem, including
the distinction between equality and strictness at the Lipschitz threshold.
The author's PDF appeared in search results but returned HTTP 404 when opened;
this review relies on the inspected publisher text for that comparison.

Tree elimination, infimal convolution with distance, Kantorovich--Rubinstein
duality, and exact penalty theory are all established. The sharp universal
separator-potential threshold is a useful combined formulation, but this
review does not establish its novelty. No efficient way to calculate `Cdet`
or solve the message minimizations follows from the existence proof.
