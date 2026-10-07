# Independent audit of local contraction and stalling

Status: complete analytic audit, with precise replacement statements and proofs. This audit
reads the September theory, its full factorable/boundary proofs, its independent
review, and October foundations. It uses analytic derivations, with no rerun of
numerical experiments and no project-wide verification or CI inspection.

## Material findings already established

1. The interior tangent contraction argument, strict negative face-witness
   stalling argument, termwise quadratic tangent formula, two-variable cube
   eigenvalue, and non-strict row-stall condition are sound under their stated
   whole-relaxation monotonicity and local-domain assumptions.
2. In the two-variable result, an arbitrary box containing a neighborhood of
   zero has widths `Theta(rho(a)^k)` and kth-root rate `rho(a)`. The proof does
   **not** establish convergence of successive width ratios from arbitrary
   boxes. Exact per-round multiplication is proved on eigenvector boxes.
3. Boundary Proposition 11 has a real terminal-case gap, missed in the earlier
   review. Part (b) claims the refined active estimate with `G_0 + eta_k`,
   `eta_k <= delta/2`, even at `k = k_eps = 1`. Its proof does not put the first
   active shape in the small-shape regime when the initial scale is already
   below the cutoff floor. That asserted estimate is false. Keep the coarse
   `G_M` estimate for this case; use the refined estimate only after the
   small-shape induction has started.
4. The phrase “active widths shrink quadratically relative to the free widths”
   must refer to the common geometric **upper scale**, not necessarily to the
   actual free widths. The proof supplies an upper bound. It cannot replace
   this with an equality involving a fictitious enclosing free box.
5. The positive-definite stalling example concerns the termwise relaxation
   with exact convex squares and McCormick bilinear terms. A solver using the
   original convex quadratic as its objective has a different, stronger
   relaxation. The exact rate is attached to the formulation and relaxation.
6. **Additional exact family result:** for
   `f=sum_i x_i^2+a sum_{i<j}x_i x_j`, `n>=3`, the exact cube Jacobi factor is
   `min{1,[sqrt(a^2(n-1)^2+2a n(n-1))-a(n-1)]/2}`. The cube-stall condition
   `a(n-1)(n-2)/2>=1` is necessary and sufficient for this family.
   This derives the archived `n=3,a=1/2` contraction as
   `(sqrt(7)-1)/2`, rather than merely repeating its numerical estimate.

## Explicit counterexample to boundary Proposition 11(b)

Take `f(x,y)=x-x^2+y^2` on
`B_0=[0,1/4] x [-1/4,1/4]`. The global minimizer is `(0,0)`, the active
gradient is `g_x=1`, and the free gradient is zero. For a box
`B=[0,h] x [-r,r]`, keep the convex square `y^2` exact and use the concave
secant of `-x^2`. The projected relaxation is

```
phi_B(x,y) = (1-h)x + y^2.
```

It is valid and monotone under box restriction. Its boundary expansion is
exact, with `Q(d,xi)=-d_x^+ xi_x+xi_y^2`; the reduced free function is
`Q^F=xi_y^2`, and `G_0=0`. Set `u_F=(1,1)`, `delta=1/4`, `lambda=3/4`,
and `M=1`. The reduced map has `Phi_delta^F(u_F)=(1/2,1/2)`, so all the
contraction hypotheses hold. Start at
`B^0=[0,w_0] x [-w_0,w_0]`, and take `epsilon=w_0/2`. For every sufficiently
small positive `w_0`, `k_eps=1`, and both first free boxes stay unchanged.
The active widths are exactly

```
h_1 = epsilon/(1-w_0),
h_2 = epsilon/(1-h_1)
    = epsilon(1-w_0)/(1-w_0-epsilon).
```

Thus

```
(h_2-epsilon)/w_0^2 = 1/(4(1-3w_0/2)) > 1/4.
```

The claimed bound would give `h_2 <= epsilon+(delta/2)w_0^2`, whose coefficient
is `1/8`. It fails for arbitrarily small `w_0`. No numerical solve is needed.

## Immediate repair of the boundary theorem

Keep the old part (a), the initial active estimate, and the old part (c).
Change the refined clause in (b) to apply for
`1 <= k <= k_eps` **only when `k_eps > 1`**. If `k_eps = 1`, use the valid
coarse estimate

```
width_i(B^2) <= width_i(B^1)
               <= (epsilon+(G_M+delta/4)w_0^2)/g_i.
```

This still gives the stated `O(epsilon)` active floor, because in this case
`w_0^2 < 2epsilon/delta`. For `epsilon=0`, replace the equality-looking
statement in (c) by

```
width_i(B^{k+1}) <= (G_0/g_i+o(1)) \hat w_k^2.
```

The precise results below give the complete repairs and the supporting proofs.

## Coverage inventory

The numbers in the first column are the September source's numbering. The
suggested labels are manuscript labels, not assertions of novelty.

| Source result or substantive development | Audit and manuscript treatment |
| --- | --- |
| Setting; projected `phi_B`; R1–R2; exact Jacobi versus sequential rounds | Retain whole-construction validity and monotonicity. Add compactness for attained supports. A full sequential pass inherits upper bounds; partial/selective passes do not. |
| Lemma 1, validity/order/nested-box convergence | Correct. Nested boxes converge to their intersection; do not claim that the intersection is a fixed point without continuity. |
| Proposition 2, sharp minima and second-order error | Correct recurrence; separate zero-cutoff quadratic convergence from positive-cutoff forced recurrence and floor. Handle `tau=0` without division by zero. |
| Proposition 3, quadratic growth | Correct squared recurrence. Its positive-cutoff assertion is an upper envelope and a width floor, not a rate to its actual nonzero limiting box. October foundations states this properly. |
| Assumption T; homogeneity, shape order, `Q(d,0)<=0` | Correct with the feasible minimizer and domain hypotheses. Use continuity or lower semicontinuity in each fixed-shape point variable for attained supports. |
| `Phi_c`; monotonicity, homogeneity, scaling, `Phi(d)<=d` | Correct for nonnegative cutoffs. Avoid a nonnegative-shape convention for negative sublevels that may not contain zero; use pointwise strict witnesses or adjoin zero explicitly. |
| `r*`; robust Collatz–Wielandt upper factor | Correct as an upper factor. Under lower semicontinuity it equals the infimum based on `Phi_0`. General equality with an asymptotic spectral radius is not established. |
| Theorem 4, local tangent contraction | Correct. The enclosing shape is in the relaxation domain. State the result directly in its gauge, including the cutoff threshold. |
| Corollary 5, any admissible factor above `r*` | Correct as a zero-cutoff upper contraction factor and an `O(sqrt(epsilon))` positive-cutoff enclosure. |
| Theorem 6, strict negative face-witness stall | Correct; retain strict slack for nonzero remainder and non-strict witnesses only in exact-homogeneous examples. Stall width is `w max_i(v_i^-+v_i^+)`. |
| Positive eigenvector lower-rate remark | Correct for zero remainder, zero cutoff, and Jacobi rounds. Elementary sandwiching gives an exact kth-root rate for every positive initial shape. |
| Quadratic tangent formula, exact squares, translation/scaling | Correct with `H_ii>=0`. A negative diagonal needs its concave secant and a different tangent formula. |
| Proposition 7, two-variable exact eigenvalue | Formula correct. State `Theta(rho^k)` from arbitrary interior boxes; successive ratios are only proved on eigenvector boxes. |
| Proposition 7, independence of initial box and sign of `a` | Correct by inner/outer cube comparison and coordinate reflection. No nonlinear Perron theorem or `Phi_delta` limit is needed for this proof. |
| Review's asymmetric-square eigenvector observation | Substantive and derivable exactly. The approximate lower range near `0.41` at `a=1` is too broad; the precise condition is supplied below. |
| Proposition 8, complete row-stall condition and rectangular scaling | Correct with `<=`. Proof uses explicit face witnesses, not Theorem 6's strict-slack hypothesis. Zero half-widths are allowed by direct substitution. |
| Strongly convex many-term stall, accumulated gap | Correct. Positive definiteness and ordinary strict row diagonal dominance do not suffice for contraction. Supply exact small examples. |
| Many-term cube contraction at `n=3,a=1/2` and larger-family stalls | The archived factor `0.8229` has the exact value `(sqrt(7)-1)/2`. A complete formula for every uniform positive complete-graph family with `n>=3` is proved below, including the precise stall threshold. |
| Row condition sufficient, not necessary | Correct; replace random-test evidence with the explicit signed three-variable example below. |
| Theorem 12, composite McCormick second-order expansion | Correct, including zero factors, critical points, inflections, and degenerate shapes. Full proof and complete coefficient recursion below. The clipped variant has the same tangent coefficient; finite-box monotonicity remains a separate property. |
| Theorem 12, `C^2` versus Lipschitz second derivative | Correct: uniform `o(w^2)` versus `O(w^3)`. The final objective is `C^{2,1}` in the latter case, so its Taylor remainder is also `O(w^3)`. |
| Theorem 12, auxiliary-variable caveat | Retain: the composite theorem is not a proof for arbitrary lifted reformulations, retained constraints, or changing cuts. Termwise objective-only quadratic lifting is covered. |
| Corollary 9, objective-gap floors | Correct after handling `epsilon=0` by a limiting argument and using monotonicity on degenerate boxes. Sharp case gives `O(epsilon^2)` after entry. |
| Lemma 10, near-optimal hull obstruction | Correct. The objective-gap comparison also uses R2. Several minimizers obstruct singleton collapse; they do not imply that no useful tightening or gap closure is possible. |
| Lemma B1, boundary one-step upper/lower estimates | Correct after a minor negative-right-side convention. Lower estimates are Jacobi statements. The active estimate has a useful exact asymptotic form with a minimum by the old width. |
| Proposition 11, boundary free contraction and active scale | Retain with the terminal-case repair above. The estimate is an upper bound in the chosen scale, not an equality or a proved rate in actual free widths. |
| Boundary strict complementarity and zero-gradient active bounds | State scope locally. A zero-gradient active direction belongs in a one-sided tangent cone; an all-active strictly complementary vertex falls under the sharp-minimum result. |
| Practical observed-ratio rule; branch-and-bound discussion | Heuristic only. Ratios near one may reflect slow contraction, a positive cutoff floor, or stalling; finite observations do not distinguish them. The local theorem has hypotheses, not a universal node-activation guarantee. |
| October foundations' quadratic-growth statement | Correct. Its constants equal the September constants after `mu=gamma/2`. |
| New analytic completion: two-variable positive-cutoff cube floor | Exact formula below. Restrict the equality to symmetric cube starts; no shape-independent positive-cutoff equality was proved. |
| New analytic completion: centered rectangular quadratic support map | Exact formula below, plus an anisotropic three-variable example that changes tightening behavior. |
| New analytic completion: endpoint-tangent square relaxation | Distinguishes the October finite LP square from the exact-square September relaxation; rectangular limits below are exact. |

## Common assumptions and elementary operator facts

Let `B_0` be a bounded box, `X` the original feasible set, and let
`x* in X cap B_0` attain `f*`. On each relevant subbox `B`, the projected
relaxed objective `phi_B` is valid on `X cap B` and satisfies

```
B' subset B  =>  phi_{B'}(x) >= phi_B(x)  for x in B'.
```

This is a condition on the whole construction, including auxiliary bounds,
relaxed rows, retained cuts, and objective. Compactness of nonempty projected
sublevel sets supplies support attainment. Set

```
K_U(B)={x in B: phi_B(x)<=U},  T_U(B)=box K_U(B),
epsilon=U-f*>=0,  w(B)=max_i(u_i-l_i).
```

**Containment/order lemma** (`lem:order`). Every original feasible point of
objective at most `U` remains in `T_U(B)`. Also `T_U(B) subset B`,
`T_U(B') subset T_U(B)` when `B' subset B`, and
`T_{U'}(B) subset T_U(B)` when `U'<=U`.

**Proof.** Validity gives the first assertion. Box containment gives the
second. For the third, `phi_B<=phi_{B'}` on `B'`, hence
`K_U(B') subset K_U(B)`; take box hulls. The cutoff assertion follows from
sublevel-set inclusion. Thus the exact iterates are nested nonempty compact
boxes, preserve all original `U`-sublevel points, and converge in Hausdorff
distance to their intersection. None of this alone proves
`T_U(B_infinity)=B_infinity`. Endpoints converge monotonically, which proves
the Hausdorff assertion directly. QED.

**Sequential scope.** In a complete sequential pass, each signed endpoint
is optimized at least once, with the relaxation rebuilt on the current
smaller box. Every intermediate cutoff set is contained in the cutoff set
on the starting box. Therefore each updated lower endpoint is at least its
Jacobi value and each updated upper endpoint is at most its Jacobi value.
The completed sequential box is contained in `T_U(B)`. All one-round upper
bounds below transfer, and induction transfers the resulting upper
enclosures. A selective pass that leaves endpoints unprocessed does not have
this inclusion in general. Lower bounds and rate equalities need a separate
argument and remain Jacobi statements here.

**Near-optimal hull lemma** (`lem:sublevel-hull`). Write
`H_U=box{x in X cap B_0:f(x)<=U}`. Every iterate contains `H_U`. In particular,
two distinct global minimizers keep their entire coordinate hull `H` in every
iterate. For `L(B)=inf_{x in B}phi_B(x)`, monotonicity gives

```
H subset B_infinity  =>  L(B_infinity) <= L(H).
```

**Proof.** Preserve each original point by validity and induction, then take
its hull. On `H`, `phi_{B_infinity}<=phi_H`, so
`L(B_infinity)<=inf_H phi_{B_infinity}<=L(H)`. QED.

This obstructs collapse below the near-optimal coordinate hull. It does not
say that a broad near-optimal set prevents all useful bound changes or that
`L(H)<f*` must hold.

## Sharp growth and quadratic growth

**Sharp-growth proposition** (`prop:sharp-growth`). Suppose, for every
relevant box containing `x*` and every point of that box,

```
phi_B(x) >= f* + kappa ||x-x*||_infinity - tau w(B)^2,
kappa>0, tau>=0.
```

Then

```
w(T_U(B)) <= (2/kappa)(epsilon+tau w(B)^2).
```

For `epsilon=0` and `tau>0`, entry into `w(B)<=kappa/(4tau)` guarantees
convergence to `{x*}` with the quadratic upper recurrence
`w_{k+1}<=(2tau/kappa)w_k^2`. For `epsilon>0`, entry guarantees
`w(B_infinity)<=4epsilon/kappa`. If `tau=0`, the one-round bound is
`2epsilon/kappa`, and zero cutoff collapses in one round.

**Proof.** Every retained point satisfies
`||x-x*||_infinity<=(epsilon+tau w(B)^2)/kappa`. The range of each coordinate
is at most twice that radius. In the entry region,
`(2tau/kappa)w_k^2<=w_k/2`; nesting keeps all later widths in that region.
Consequently `w_{k+1}<=w_k/2+2epsilon/kappa`. Take limits to obtain the floor.
At zero cutoff this also proves convergence to zero, and the original
quadratic recurrence then gives the asserted order. QED.

The hypothesis is pointwise on relaxed points. Feasible sharp growth plus
an objective relaxation error on feasible points alone does not imply it.
For a problem with only box constraints, sharp growth on the full box and
`phi_B>=f-tau w(B)^2` do imply it. At a strictly complementary vertex with
all local box directions one-sided, a positive gradient and a second-order
pointwise relaxation error imply the same hypothesis locally after
absorbing the smooth quadratic remainder.

**Quadratic-growth proposition** (`prop:quadratic-growth`). If instead

```
phi_B(x) >= f* + mu ||x-x*||_infinity^2 - tau w(B)^2,
mu>0,
```

then `w_{k+1}^2<=b+q^2 w_k^2`, where
`b=4epsilon/mu`, `q^2=4tau/mu`. If `q<1`,

```
w_k^2 <= q^(2k) w_0^2 + b(1-q^(2k))/(1-q^2),
w(B_infinity) <= 2 sqrt(epsilon/(mu-4tau)).
```

At zero cutoff, `w_{k+1}<=q w_k`. At positive cutoff the displayed scalar
envelope is what is proved; it is not a claim that distance to the actual
limiting box contracts at factor `q`.

**Proof.** Each retained point is at most
`sqrt((epsilon+tau w(B)^2)/mu)` from `x*` in infinity norm. Bound the coordinate
ranges by twice this radius and square. Iterate the affine scalar
recurrence. QED.

October foundations uses `mu=gamma/2`, so its `q^2=8tau/gamma` and
`b=8epsilon/gamma` are identical. For `x^2+y^2+xy`, the best infinity-norm
growth coefficient is `mu=3/4`: on the face `x=1`, minimize in `y` at
`y=-1/2`. The McCormick gap is at most `w(B)^2/4`, so `tau=1/4` gives
`q^2=4/3>1`. Failure of this sufficient estimate does not preclude the exact
contraction proved below.

## Tangent maps and the rigorous rate statements

For `d=(d^-,d^+)>=0`, write `D(d)=prod_i[-d_i^-,d_i^+]`. A local tangent
expansion at a feasible minimizer with no first-order term is

```
phi_{x*+tD(d)}(x*+t xi) = f* + t^2 Q(d,xi) + r_t(d,xi),
sup_{d in K,xi in D(d)} |r_t(d,xi)|/t^2 -> 0
```

for every compact admissible shape set `K`. All comparison boxes must belong
to the relaxation domain. The expansion requires finite relaxed values on
the indicated boxes. It is not a blanket statement for projected constrained
relaxations that take the value `+infinity` off a feasible affine subspace.
For those, an explicitly restricted tangent support construction is needed.

Assume `Q(d,.)` is lower semicontinuous on `D(d)`; continuity follows in the
factorable construction below. For `c>=0`, define `Phi_c(d)` as the signed
endpoint shape of `{xi in D(d):Q(d,xi)<=c}`. Validity at `x*` gives
`Q(d,0)<=0`, so this set is nonempty and its hull contains zero. Write
`Phi=Phi_0`.

**Tangent-map lemma** (`lem:tangent-properties`). The expansion and
monotonicity imply

```
Q(a d,a xi)=a^2 Q(d,xi),
d<=d' => Q(d,xi)>=Q(d',xi)  on D(d),
Phi_c(d)<=d,
d<=d' => Phi_c(d)<=Phi_c(d'),
Phi_c(a d)=a Phi_{c/a^2}(d).
```

**Proof.** The boxes and points represented by `(t,ad,a xi)` and
`(at,d,xi)` coincide. Divide their expansions by `t^2` and let `t` tend to
zero. For nested shape boxes, subtract `f*`, divide the monotonicity
inequality by `t^2`, and take the limit. These two properties give the
sublevel inclusions and the scaling identity. Hulls preserve inclusion. QED.

For fixed `d`, lower semicontinuity and compactness imply
`Phi_c(d) -> Phi_0(d)` componentwise as `c downarrow 0`: for any decreasing
positive `c_j`, the compact nested sets have intersection `{Q<=0}`, and
maximizers have a convergent subsequence in that intersection. This proof
does not require convexity. Convexity is needed only if the support problems
are described as convex programs.

Define the robust upper factor

```
r* = inf{ lambda: some u>>0 and delta>0 satisfy Phi_delta(u)<=lambda u }.
```

It lies in `[0,1]`, because `Phi_delta(u)<=u`. The preceding compactness
argument gives the equivalent infimum based on `Phi_0(u)<=lambda u`:
the robust condition implies the zero-cutoff condition, and any
`lambda'>lambda` admits small positive `delta` when the zero-cutoff condition
holds. Call this a Collatz–Wielandt upper factor. Do not assert a general
nonlinear spectral-radius identity without the additional map hypotheses
and theorem that would establish it.

**Local contraction theorem** (`thm:tangent-contraction`). Suppose
`u>>0`, `delta>0`, and `lambda in (0,1)` satisfy
`Phi_delta(u)<=lambda u`. There is `t_bar>0` such that the comparison boxes
`x*+tD(u)` are admissible for `t<=t_bar` and the following holds. Define

```
g_u(B)=max_i{(x_i*-l_i)/u_i^-, (u_i-x_i*)/u_i^+}
```

for boxes containing `x*`. If `g_u(B)=t<=t_bar` and
`t^2>=2epsilon/delta`, then
`g_u(T_U(B))<=lambda t`. The iterates remain in the neighborhood and satisfy

```
g_u(B_k) <= max{lambda^k g_u(B_0), sqrt(2epsilon/delta)},
B_infinity subset x*+sqrt(2epsilon/delta)D(u).
```

At zero cutoff, they converge to `x*` with an upper one-round contraction
factor `lambda`. Every `lambda in (r*,1)` has such a shape and slack.

**Proof.** Choose `t_bar` so that the remainder on shape `u` is bounded by
`delta t^2/2`. For a retained point in the comparison box, the expansion gives
`Q(u,xi)<=epsilon/t^2+delta/2<=delta`. Thus its hull is contained in
`x*+lambda tD(u)`. Monotonicity transfers the enclosure to the original
smaller box. Below the threshold, nesting preserves its existing enclosure.
Applying these two alternatives inductively gives the stated envelope.
If the initial scale exceeds the positive threshold, finite repeated
contraction crosses it; zero cutoff contracts forever. QED.

**Exact eigenvector rate proposition** (`prop:tangent-eigenrate`). Suppose
the tangent representation has zero remainder at every relevant scale and
`U=f*`. If `Phi(u)=rho u` for `u>>0`, then

```
T_U^k(x*+tD(u))=x*+rho^k tD(u).
```

For any initial shape `d_0>>0`, if all required comparison boxes are
admissible, choose `a,b>0` with `a u<=d_0<=b u`. Monotonicity and homogeneity
give

```
a rho^k u <= Phi^k(d_0) <= b rho^k u.
```

Thus every coordinate extent, and the maximum width, is
`Theta(rho^k)` when `rho>0`, and the kth-root width rate is exactly `rho`.
On the eigenvector box each signed extent has exact per-round ratio `rho`.
For `rho=0`, the upper comparison proves collapse in one round.

**Proof.** Zero remainder identifies `T_U` exactly with `Phi`, and induction
gives the first assertion. Apply the order-preserving homogeneous map to
the two shape inequalities repeatedly to obtain the sandwich. Taking
widths and kth roots proves the rate. QED.

The same assumptions also give `r*=rho`. The upper inequality follows from
`Phi_delta(u) -> Phi(u)` and any `lambda>rho`. For the lower inequality,
if some `v>>0` satisfied `Phi(v)<=lambda v` with `lambda<rho`, a positive
multiple of `u` lies below `v`; iteration would imply a fixed positive
multiple of `rho^k u` lies below `lambda^k v`, an impossibility. This is an
elementary argument and does not require a nonlinear Perron theorem.
Rate lower bounds remain Jacobi statements. A nonzero tangent remainder
does not justify this exact equality by itself.

## Strict stalling and termwise quadratic relaxations

**Strict face-witness stalling theorem** (`thm:local-stall`). Suppose a
nonzero admissible shape `v>=0` has a witness at every positive signed
endpoint, and each witness satisfies `Q(v,xi)<=-delta` for a common
`delta>0`. Then for all sufficiently small positive `t`, and every
`U>=f*`, `T_U(x*+tD(v))=x*+tD(v)`. Every exact Jacobi iterate from a
containing box preserves this box. A complete sequential pass on this box
also changes no endpoint, and every sequential update from a containing
box preserves it.

**Proof.** At each witness, the relaxation value is at most
`f*-delta t^2+o(t^2)<f*<=U`. The origin is retained by validity, so it supplies
each zero one-sided endpoint; entirely degenerate coordinates need no
additional witness. The hull therefore contains every endpoint of the
given box, while containment gives equality. Monotonicity protects the box
inside every Jacobi iterate. In a sequential update, its cutoff set remains
contained in the current box's cutoff set and witnesses its updated
endpoint, so the update cannot cross the protected endpoint. QED.

For a pure quadratic
`f=f*+(1/2)(x-x*)^T H(x-x*)`, retain the diagonal terms exactly when
`H_ii>=0`. Relax each off-diagonal product from below for positive
`H_ij` and from above for negative `H_ij`. Translation and positive scaling
commute with the McCormick planes, so

```
phi_{x*+tD(d)}(x*+t xi)=f*+t^2 Q(d,xi)
```

exactly, where the diagonal contribution is
`sum_i H_ii xi_i^2/2` and the bilinear contribution is its signed envelope.
For example,
`l_j x_i+l_i x_j-l_i l_j` under `x=c+y`, `l=c+l'`, becomes

```
c_i c_j+c_j y_i+c_i y_j+l'_j y_i+l'_i y_j-l'_i l'_j.
```

Every plane receives the same affine translation terms; maxima and minima
therefore commute with translation. Scaling gives the zero remainder.
If `H_ii<0`, a convex relaxation uses the chord

```
(H_ii/2)[(d_i^+-d_i^-)xi_i+d_i^- d_i^+]
```

instead of the concave square. This also scales quadratically but gives a
different `Q`. The row result next assumes `H_ii>=0`.

**Row-stall proposition** (`prop:quadratic-row-stall`). On a centered box
with half-widths `h_i>=0`, let `H'=diag(h) H diag(h)`. If for every
nondegenerate coordinate `k`,

```
H'_{kk}/2 + sum_{j!=k}|H'_{kj}| <= sum_{i<j}|H'_{ij}|,
```

then `T_U(B)=B` for every `U>=f*`.

**Proof.** On the normalized cube, with `s_ij=sign(H'_{ij})`,

```
Q(1,xi)=sum_i H'_{ii}xi_i^2/2
        +sum_{i<j}|H'_{ij}|(|xi_i+s_ij xi_j|-1).
```

At `xi=+e_k` or `-e_k`, every incident pair has envelope contribution zero
and every nonincident pair contributes `-|H'_{ij}|`. Its relaxed value is
exactly the left side of the hypothesis minus the right side. These
nonpositive face witnesses and the origin preserve all box endpoints.
The zero remainder allows `<=0`; no strict-negative-witness theorem is
needed. Scaling back gives the claim. A zero half-width just multiplies the
corresponding rows and products by zero. QED.

**Positive-definite and diagonally dominant stall.** For

```
f=sum_i x_i^2+a sum_{i<j}x_i x_j,
H_ii=2, H_ij=a>0,
```

the eigenvalues of `H` are `2-a` and `2+a(n-1)`, so the objective is strongly
convex for `0<a<2`. The row condition is
`a(n-1)(n-2)/2>=1`. At `a=1/10,n=6`, every face witness has relaxed value
`1-(1/10)10=0`; no coordinate moves at cutoff zero. Moreover
`sum_{j!=i}|H_ij|=1/2<2=H_ii`, so ordinary strict row diagonal dominance
does not prevent this stall. At the origin the relaxed objective is
`-a n(n-1)/2`; the accumulated bilinear envelope gap supplies the mechanism.
For width `w=2h`, that gap is `a n(n-1)w^2/8`.

**Exact uniform-family cube map** (`prop:complete-graph-rate`). For the same
objective, let `n>=3`, `0<a<2`, keep exact squares, and relax each bilinear
term separately. A zero-cutoff cube Jacobi round has exact radius factor

```
rho_n(a)=min{1,
 [sqrt(a^2(n-1)^2+2a n(n-1))-a(n-1)]/2}.
```

The cube stalls if and only if `a(n-1)(n-2)/2>=1`. Below that threshold,
every interior initial box has widths `Theta(rho_n(a)^k)`. At or above it,
every such box preserves a positive centered cube and therefore has a
nonzero limiting width.

**Proof.** Normalize the cube radius to one and fix its first coordinate
at `t>=0`. Let `y_j` be the remaining coordinates and `S=sum_j y_j`.
The sum of absolute values in the relaxed bilinear terms is

```
A=sum_j|t+y_j|+sum_{i<j}|y_i+y_j|.
```

If `S>=0`, its first sum is at least `(n-1)t+S`, hence at least
`(n-1)t`. If `S<=0`, the first sum is at least `(n-1)t+S`, and the second
is at least `-(n-2)S`, because each `y_j` appears in `n-2` nonincident
pairs. Thus `A>=(n-1)t-(n-3)S>=(n-1)t` in this case as well. Therefore
the minimum relaxed objective at fixed `t` is

```
m_n(t)=t^2+a(n-1)t-a n(n-1)/2,
```

with equality at all `y_j=0`. It is increasing for `t>=0`; solving its
zero gives the displayed root, truncated at the box face. All coordinate
extents coincide by permutation and central-reflection symmetry. Its
value at one is `1-a(n-1)(n-2)/2`, proving the exact stall threshold.
The contracting case follows from the inner/outer cube eigenvector
sandwich. In the stalling case an inner positive cube is itself a fixed
box and is preserved by monotonicity. QED.

At `n=3,a=1/2`, the exact factor is `(sqrt(7)-1)/2`, which rounds to
`0.8229`. The September larger examples `n=5,a=0.3`, `n=10,a=0.1`, and
`n=20,a=0.1` satisfy the exact stall threshold, with left sides
`1.8,3.6,17.1`. These are analytic identities, not reruns of their archived
tangent programs. The proof requires `n>=3`; for two variables, optimization
of the second coordinate gives the different formula in Proposition 7.

**The row condition is not necessary.** Take

```
f=x1^2+x2^2+x3^2+(3/4)(x1*x2+x1*x3-x2*x3)
```

on `[-1,1]^3`. Its Hessian is `2I+(3/4)A`, where
`A=[[0,1,1],[1,0,-1],[1,-1,0]]`. The vectors `(-1,1,1)`, `(0,1,-1)`, and
`(2,1,1)` are an eigenbasis of `A` with eigenvalues `-2,1,1`, respectively.
Thus the Hessian eigenvalues are exactly `1/2,11/4,11/4`. The row condition
fails in every row (`5/2>9/4`). The normalized relaxed objective is

```
Q(x)=x1^2+x2^2+x3^2
     +(3/4)(|x1+x2|+|x1+x3|+|x2-x3|-3).
```

At `z=(1,-3/8,-3/8)`, the squares sum to `41/32`, the two incident product
contributions sum to `-9/16`, and the nonincident product contributes
`-3/4`; hence `Q(z)=41/32-18/32-24/32=-1/32`. The signed permutations
`S_2(x)=(x2,x1,-x3)` and `S_3(x)=(x3,-x2,x1)` preserve the cube and `Q`:
each permutes its three displayed absolute values. They send `z` to
`(-3/8,1,3/8)` and `(-3/8,3/8,1)`, which attain the positive second and
third faces. Since `Q(-x)=Q(x)`, their negatives attain the other three
faces at the same value. The termwise relaxation is therefore a complete
strict stall. This also shows why the sign pattern, not just sums of
absolute off-diagonal coefficients, can matter.

**A rectangular box changes the behavior.** For
`f=x1^2+x2^2+x3^2+x1*x2+x1*x3+x2*x3`, the unit cube stalls (all axis face
witnesses have value zero). On `[-1/4,1/4] x [-1,1]^2`, the first-coordinate
faces remain witnessed by `(+-1/4,0,0)`, whose value is `1/16-1<0`.
At the positive second-coordinate face, writing `t=1/4`, the relaxation is

```
x1^2+1+x3^2+x1+x3+|x1+t x3|-t.
```

Since `x1>=-t`, `x1^2>=0`, `x3^2+x3>=-1/4`, and the absolute value is
nonnegative, it is at least `3/4-2t=1/4>0`. The negative second face follows
by central reflection, and the third-coordinate faces by interchange.
Thus the same strongly convex objective tightens the last two coordinates
on this thin rectangle while it stalls on the cube. Compactness makes the
face exclusion a strict endpoint reduction, rather than merely absence of
one particular witness.

## Exact two-variable rate, rectangular map, and cutoff floor

Consider `f=x^2+y^2+a xy`, `0<a<2`, with the squares exact and the bilinear
term relaxed from below. On `[-h,h]^2`,

```
phi_h(x,y)=x^2+y^2+a h(|x+y|-h).
```

**Two-variable exact-rate proposition** (`prop:two-variable-rate`). At
zero cutoff, a Jacobi round on the cube multiplies its radius by

```
rho(a)=(sqrt(2a^2+4a)-a)/2.
```

Every initial box containing zero in its interior has maximum width
`Theta(rho(a)^k)`, hence kth-root rate `rho(a)`. For negative `a`, replace
`a` by `|a|`; `a=0` collapses in one round. The assertion about arbitrary
boxes is a rate in this geometric sense, not a proof of convergence of
successive width ratios.

**Proof.** Normalize `h=1`, fix the first coordinate `t>=0`, and put
`s=t+y`. Minimizing
`t^2+(s-t)^2+a|s|-a` over the second coordinate gives

```
m_a(t)=2t^2-a,                         0<=t<=a/2,
m_a(t)=t^2+a t-a^2/4-a,               a/2<=t<=1.
```

In the first case the minimizer is `y=-t`; in the second it is `y=-a/2`.
Both are in the box. The formulas meet at `a/2`, and the function is
strictly increasing for `t>0`. Its positive zero is the displayed `rho`.
Since `rho>a/2` exactly when `a<2`, the second formula applies, and
`rho<1`. Coordinate interchange and central reflection give all four
equal extents. Therefore the cube is an eigenvector box, and its iterates
are exactly `[-h rho^k,h rho^k]^2`. Any interior box lies between two
positive centered cubes. The termwise relaxation is defined on all boxes
of `R^2`, so the outer cube is allowed even if it extends beyond the
original box. Monotonicity sandwiches all iterates between those cube
iterates. Reflection `y -> -y` handles negative `a`. Differentiation of
the explicit expression gives `rho'(a)>0`, and its endpoint limits are
zero and one. QED.

For `f=alpha x^2+beta y^2+c xy`, `alpha,beta>0` and
`|c|<2sqrt(alpha beta)`, the change of variables
`z1=sqrt(alpha)x`, `z2=sqrt(beta)y` gives the same rate with
`a=|c|/sqrt(alpha beta)`. In the original variables its centered
eigenvector rectangles have `sqrt(alpha)h_x=sqrt(beta)h_y`.

**Centered rectangular support formula** (`prop:rectangle-support`). On
`[-h,h] x [-k,k]`, set `R=k/h>0`. At zero cutoff the new first-coordinate
half-width is `h r_x(R)`, where

```
r_x(R)=sqrt(a R/(1+R^2)),
    if 4R^3<=a(1+R^2);
r_x(R)=(sqrt(a^2(1+R^2)+4aR)-aR)/2,
    otherwise.
```

The second-coordinate half-width is `k r_x(1/R)`.

**Proof.** With `t=x/h>=0` and `z=y/k`, the objective is

```
h^2 t^2+k^2 z^2+a hk(|t+z|-1).
```

Its minimizing second coordinate is
`z=-min(t,a/(2R))`, which is in `[-1,1]` for `0<=t<=1`. The minimized
objective, divided by `h^2`, is

```
(1+R^2)t^2-aR,                 t<=a/(2R),
t^2+aR t-a^2/4-aR,            t>=a/(2R).
```

The zero of the first formula lies in its branch precisely when
`4R^3<=a(1+R^2)`. Otherwise the positive zero of the second formula gives
the result. The zero is below one because `a<2` and
`1+R^2>aR`; indeed at a physical face the McCormick term becomes the true
product, and the strictly convex quadratic has positive value. Central
reflection gives the negative extent, and coordinate interchange gives
the second formula. QED.

**Asymmetric square eigenvectors** (`prop:asymmetric-eigenboxes`). Let
`c,b>0`, and consider `[-c,b]^2`. Write
`r=1-rho(a)+a/2`. Then the shape is an eigenvector with eigenvalue `rho(a)`
if and only if

```
c>=r b  and  b>=r c.
```

In particular, positive eigenvectors need not be unique.

**Proof.** The bilinear envelope is
`max{-c(x+y)-c^2, b(x+y)-b^2}`, and the two planes meet at `x+y=b-c`.
On the positive face of its zero sublevel, the second plane alone gives
the upper bound `x<=rho b`: after minimizing in `y`,
`x^2+a b x-a^2 b^2/4-a b^2<=0`. Equality requires
`y=-a b/2`. This point belongs to the second-plane region exactly when
`(rho-a/2)b>=b-c`, or `c>=r b`. This condition also implies
`a b/2<c`, because `r>a/2` for `a<2`. If the region condition fails,
the full envelope is strictly larger at the unique minimizing point,
so the positive extent is strictly smaller than `rho b`. The negative
extent similarly equals `rho c` exactly when `b>=r c`. Coordinate
interchange supplies both coordinates. QED.

For the review's normalization `b=1-c`, `a=1`, the interval is exactly

```
r/(1+r) <= c <= 1/(1+r),
r=(4-sqrt(6))/2.
```

Thus its informal lower endpoint near `0.41` should not be repeated as an
exact observation at `a=1`; the exact lower endpoint is about `0.4367`.

**Positive-cutoff cube floor** (`prop:two-variable-cutoff-floor`). For
`epsilon>0` and a symmetric cube start, its radii obey

```
h_{k+1}=min{h_k,
     [sqrt((2a^2+4a)h_k^2+4epsilon)-a h_k]/2}.
```

Set `h_epsilon=sqrt(epsilon/(1-a^2/4))`. If `h_0<=h_epsilon`, the first
round stalls. If `h_0>h_epsilon`, radii decrease to exactly `h_epsilon`.
At the limiting cube, the relaxed objective minimum is
`-a h_epsilon^2`, so the objective gap is exactly
`a epsilon/(1-a^2/4)`. More generally the limiting radius is
`min(h_0,h_epsilon)` and its gap is `a min(h_0^2,h_epsilon^2)`.

**Proof.** At nonnegative scaled cutoff, the support root always lies in
the second branch of `m_a`, since its first branch's maximum at `a/2`
is negative. Solving its quadratic at `epsilon/h^2` gives the recurrence.
The radius changes precisely when the face value
`h^2(1-a^2/4)` exceeds `epsilon`. Write the untruncated formula as `g(h)`.
It fixes `h_epsilon`, and is strictly increasing for `h>=h_epsilon`:

```
g'(h)=((2a^2+4a)h/sqrt((2a^2+4a)h^2+4epsilon)-a)/2,
g'(h_epsilon)=a/2>0,
```

and this derivative increases with `h`. Thus
`h_epsilon<g(h)<h` for `h>h_epsilon`. A decreasing radius sequence has a
limit at least `h_epsilon`; continuity and the fixed-point equation force
equality. The relaxed objective is minimized at the origin, because its
two squares and `a h|x+y|` are nonnegative, giving `L=-a h^2`. QED.

For a start above the positive floor, the radius error itself has
successive-ratio limit `a/2`, by the derivative at the fixed point, while
the successive ratios of radii tend to one. This supplies an analytic
example of why a near-one observed width ratio need not mean that the
zero-cutoff rate is near one or that the original minimizer is spread out.
The exact floor equality is not asserted for arbitrary asymmetric initial
boxes. They cannot grow missing sides to a claimed universal cube.

## The finite LP square and a second rectangular example

The October reference family permits `w_ii` with just endpoint tangents
and a secant. This differs from the exact convex square used above. On
`[-h_i,h_i]`, the smallest permitted square value is
`2h_i|x_i|-h_i^2`. For `f=sum_i x_i^2`, and no additional square lower
bound such as `w_ii>=0`, its zero-cutoff projected objective is

```
phi_B(x)=sum_i(2h_i|x_i|-h_i^2).
```

A Jacobi round gives the exact map, for `h_i>0`,

```
h_i' = min{h_i, (sum_j h_j^2)/(2h_i)}.
```

**Proof.** All non-`i` coordinates can be zero, and each has its smallest
square value there. The cutoff requires
`2h_i|x_i|<=sum_j h_j^2`; intersect with the original interval. Conversely,
the endpoint satisfying this inequality is attained with all other
coordinates zero and their square variables at their allowed minima.
The square secants lie above these tangent minima, so the lifted point is
feasible. QED.

In one dimension the half-width halves. On a cube with `n>=2`, every
endpoint stalls, even though the objective is strictly convex and has a
unique minimizer. In two dimensions with `h>=k>0`, the shorter half-width
stays `k`, and the longer one obeys

```
h'=(h^2+k^2)/(2h),
h'-k=(h-k)^2/(2h).
```

It decreases to `k`, giving a limiting square `[-k,k]^2` and a quadratic
error recurrence in its long half-width. If `k=0`, the remaining half-width
halves to zero. This is an exact rectangular example of a finite LP
relaxation's behavior. It does not transfer to a formulation with exact
square epigraphs or with the strengthening rows `w_ii>=0`.

These two rectangular examples and the two-variable rate use different
specified relaxations. The main paper should keep that distinction
explicit; the October lifted LP is not an implementation of the exact
square tangent theorem merely because both contain McCormick rows.

## Objective-gap consequences

**Objective-gap corollary** (`cor:local-gap`). Under the local contraction
theorem let `G=-min_{xi in D(u)}Q(u,xi)>=0`, and use the same `t_bar` whose
remainder is at most `delta t^2/2`. For positive `epsilon` with
`sqrt(2epsilon/delta)<=t_bar`,

```
f*-L(B_infinity) <= (2G/delta+1)epsilon.
```

As `epsilon downarrow 0`, its sharper asymptotic version is
`f*-L(B_infinity)<=(2G/delta)epsilon+o(epsilon)`. At zero cutoff,
`L(B_infinity)=f*`. Under the sharp-growth proposition after entry,

```
f*-L(B_infinity) <= tau(4epsilon/kappa)^2.
```

**Proof.** The limiting box is contained in the comparison box
`C_epsilon=x*+t_epsilon D(u)`, with
`t_epsilon=sqrt(2epsilon/delta)`. Monotonicity gives
`L(B_infinity)>=inf_{C_epsilon}phi_{C_epsilon}`. The tangent expansion bounds
this infimum below by `f*-G t_epsilon^2-delta t_epsilon^2/2`, proving the
finite bound. Its actual uniform remainder is `o(t_epsilon^2)`, proving
the asymptotic version. At zero cutoff the limiting box is `{x*}` and lies
in every sufficiently small comparison box; the same lower bound tends
to `f*`. Validity at `x*` gives the reverse inequality. In the sharp case,
the pointwise hypothesis gives `L(B)>=f*-tau w(B)^2`; insert the proved
limiting width bound. QED.

Monotonicity must include degenerate boxes if `L(B_infinity)` is evaluated
there. If the implementation does not build such relaxations, the valid
claim is the limiting lower bound of the finite-box relaxation values,
which follows from the same enclosing boxes. The rate theorem is an
analytic statement involving `x*`, `f*`, and tangent data; it is not by
itself a computable solver stopping certificate.

## Complete composite McCormick tangent expansion

This is the full September Theorem 12, including the intermediate claim
that makes univariate clipping inactive at second order.

**Construction.** A finite factor sequence contains variables, constants,
sums, signed constant scalings, products of earlier factors (including
repeated factors), and univariate compositions `h(v_a)`. Its last factor
is the objective. Natural interval bounds use endpoint sums, signed
scalings, four corner products, and exact interval images for univariate
functions. Write `cv_a,cc_a` for the convex/concave relaxations of `a`,
and `a^L,a^U` for its interval. With
`s_c(a)=min(c cv_a,c cc_a)` and `t_c(a)=max(c cv_a,c cc_a)`, the product rule is

```
cv_ab=max{s_{b^L}(a)+s_{a^L}(b)-a^L b^L,
          s_{b^U}(a)+s_{a^U}(b)-a^U b^U},
cc_ab=min{t_{b^L}(a)+t_{a^U}(b)-a^U b^L,
          t_{b^U}(a)+t_{a^L}(b)-a^L b^U}.
```

For `h(a)`, on `Z=[a^L,a^U]` use the scalar envelopes and median rules

```
cv_h=h_Z^cv(mid(cv_a,cc_a,z_min)),
cc_h=h_Z^cc(mid(cv_a,cc_a,z_max)),
```

where `z_min` minimizes the convex envelope and `z_max` maximizes the
concave envelope on `Z`. The clipped variant replaces each factor output
by `max(cv,v^L)` and `min(cc,v^U)` before using it later. Here
`phi_B=cv_m`; this is a specified composite relaxation, not an unspecified
lifted projection.

Validity of the scalar bounds follows directly by induction. At a product,
each signed min selection is at most its coefficient times the actual
factor, so the two raw lower planes are at most the bilinear lower planes
evaluated at the actual factors; each such plane is below their product.
The signed max selections and upper planes give the corresponding upper
bound. For a univariate factor, the median is the projection of an
envelope minimizer onto the relaxed argument interval, which contains the
actual argument. It lies between that minimizer and the actual argument
and belongs to the natural argument interval. Convexity implies that the
convex envelope there is at most its value at the actual argument, hence
at most the actual function value. Concavity and an envelope maximizer
give the upper bound. Natural interval bounds contain every actual factor
value; clipping to those bounds preserves the inequalities. Sums and
signed scalings preserve them as well.

Put `a*=v_a(x*)`, `b*=v_b(x*)`,
`p_k(xi)=grad v_k(x*)^T xi`, and
`s^+=max(s,0)`, `s^-=max(-s,0)`. The full tangent recursion is:

- Variables: `[ell_i]=[-d_i^-,d_i^+]`, `E_i^cv=E_i^cc=0`.
- Constants: `[ell]=[0,0]`, `E^cv=E^cc=0`.
- Sums: add interval bounds and corresponding gaps.
- Positive constant scalings: scale both interval bounds and gaps.
- Negative scaling by `c`: swap interval endpoints, and set
  `E^cv=|c|E_a^cc`, `E^cc=|c|E_a^cv`.
- Products: `[ell_ab]=b*[ell_a]+a*[ell_b]` in interval arithmetic, and

```
E_ab^cv=b*^+ E_a^cv+b*^- E_a^cc+a*^+ E_b^cv+a*^- E_b^cc
        +min{(p_a-ell_a^L)(p_b-ell_b^L),
             (ell_a^U-p_a)(ell_b^U-p_b)},
E_ab^cc=b*^+ E_a^cc+b*^- E_a^cv+a*^+ E_b^cc+a*^- E_b^cv
        +min{(ell_a^U-p_a)(p_b-ell_b^L),
             (p_a-ell_a^L)(ell_b^U-p_b)}.
```

- Univariate factors: `[ell_h]=h'(a*)[ell_a]`; if
  `A_a=(p_a-ell_a^L)(ell_a^U-p_a)`, then

```
E_h^cv=(h''(a*)^-/2)A_a+h'(a*)^+ E_a^cv+h'(a*)^- E_a^cc,
E_h^cc=(h''(a*)^+/2)A_a+h'(a*)^+ E_a^cc+h'(a*)^- E_a^cv.
```

The interval data come from natural interval arithmetic on the linearized
factor sequence. They need not equal the exact range of the final linear
function, because dependencies can be lost. Induction gives
`p_k(xi) in [ell_k^L,ell_k^U]`, so the displayed gaps are nonnegative.
The interval data are continuous and degree-one homogeneous in `d`; the
gap data are continuous and degree-two homogeneous in `(d,xi)`.

**Factorable expansion theorem** (`thm:factorable-tangent`). If every
univariate factor is `C^2` near its argument's value at `x*`, then, for
every compact shape set `K`, all intervals and relaxations are defined at
sufficiently small scale and, uniformly for `d in K`, `xi in D(d)`,

```
v_k^{L,U}(x*+tD(d))=v_k(x*)+t ell_k^{L,U}(d)+O_K(t^2),
cv_k(x*+t xi)=v_k(x*+t xi)-t^2 E_k^cv(d,xi)+o_K(t^2),
cc_k(x*+t xi)=v_k(x*+t xi)+t^2 E_k^cc(d,xi)+o_K(t^2).
```

The unclipped construction also satisfies

```
(v_k^L-cv_k)^++(cc_k-v_k^U)^+=o_K(t^2).                 (P)
```

The clipped construction has the same tangent data. If the scalar second
derivatives are locally Lipschitz, the `o_K(t^2)` remainders are
`O_K(t^3)`. For both constructions,

```
phi_{x*+tD(d)}(x*+t xi)
 =f(x*)+t grad f(x*)^T xi+t^2 Q(d,xi)+o_K(t^2),
Q(d,xi)=(1/2)xi^T grad^2 f(x*)xi-E_m^cv(d,xi).
```

The result includes boundary points, zero factor values, and degenerate
shapes. It does not imply finite-box monotonicity of the unclipped rule
or cover arbitrary lifted formulations with coupled rows.

**Proof.** All factor functions are `C^2` on a common small neighborhood,
and `{(d,xi):d in K,xi in D(d)}` is compact. Consequently each actual factor
has the uniform expansion
`v_k(x*+t xi)=v_k(x*)+t p_k(xi)+O_K(t^2)`. Inductively, each natural interval
remains within `O_K(t)` of its factor's value at `x*`, so its full argument
interval lies in the univariate smooth domain for small enough `t`.
Products of interval endpoints have first-order coefficient
`b*ell_a^i+a*ell_b^j`; finite min/max are Lipschitz, yielding the claimed
product interval. For univariate intervals, minimize/maximize the uniform
first-order scalar Taylor model. Other interval steps are immediate.

Prove the gap expansions and (P) simultaneously by induction. Variables,
constants, sums, and signed scalings satisfy them immediately. At a product,
the induction implies `cc_a-cv_a=O_K(t^2)`, and endpoint coefficients equal
`b*+O_K(t)` or `a*+O_K(t)`. If `b*!=0`, both `b` endpoints eventually have
its sign, so both convex selections use `cv_a` when positive and `cc_a`
when negative. If `b*=0`, replace either selection by the actual value
`a`; the error is `O_K(t)` times `O_K(t^2)`, hence `O_K(t^3)`.
Do the same for the `b` selections. Thus, to `O_K(t^3)`, the convex output
is the bilinear envelope `M` evaluated at common selected values
`a_tilde,b_tilde`. Algebra gives

```
M(a_tilde,b_tilde)=a_tilde b_tilde
 -min{(a_tilde-a^L)(b_tilde-b^L),
       (a^U-a_tilde)(b^U-b_tilde)}.
```

The product `a_tilde b_tilde` contributes the four signed propagated
`t^2 E` terms. Each endpoint distance is `t(p-ell)+O_K(t^2)`; multiplying
two such distances produces exactly the two displayed product-gap
coefficients, with `O_K(t^3)` errors. Taking a minimum preserves the
uniform error. The upper envelope's gap is the minimum of the two crossed
products, giving the concave formula in the same way.

For (P), the inductively selected pair is at distance `o_K(t^2)` from the
natural interval rectangle. On that rectangle `M` is at least its
minimum corner product: that constant is a convex minorant of the
bilinear function, while `M` is the convex envelope. Its piecewise-affine
formula is `O_K(1)`-Lipschitz, because the endpoint coefficients are
bounded. Moving the pair into the rectangle changes `M` by only
`o_K(t^2)`, so the raw convex output is at least the natural lower bound
minus `o_K(t^2)`. The concave output is similarly at most the maximum
corner product plus `o_K(t^2)`.

For the univariate step, first record two envelope facts with proofs.
A scalar `Lambda`-Lipschitz function on `[L,U]` has convex and concave
envelopes with the same Lipschitz bound. The affine minorants through the
two endpoint values with slopes `+-Lambda` force the convex envelope to
agree with those endpoint values. Convex chord-slope inequalities then
bound every secant slope between `-Lambda` and `Lambda`. Negation proves
the concave assertion. A zero-width interval is trivial.

Next, with `c_2=h''(a*)`, compare `h` on an interval `Z=[L,U]` lying in
`[a*-s,a*+s]` with its quadratic Taylor model. If
`omega(s)=sup_{|y-a*|<=s}|h''(y)-c_2|`, their sup-norm difference is at most
`omega(s)s^2/2`. Envelopes are monotone and commute with added constants,
so their sup-norm difference obeys the same bound. A convex quadratic is
its own convex envelope; a concave quadratic's convex envelope is its
chord. The chord gap is `(c_2^-/2)(y-L)(U-y)`. Hence

```
h(y)-h_Z^cv(y)=(c_2^-/2)(y-L)(U-y)+O(omega(s)s^2),
h_Z^cc(y)-h(y)=(c_2^+/2)(y-L)(U-y)+O(omega(s)s^2).
```

Here `omega(s)->0`; under Lipschitz second derivatives it is `O(s)`.
After subtracting `h'(a*)y`, the scalar function and its envelopes have
Lipschitz constant at most `s sup|h''|`, by the first fact.

Let `a` be the actual argument and `m=mid(cv_a,cc_a,z_min)`. Since
`cv_a<=a<=cc_a`, `a in Z`, and `z_min in Z`, the median belongs to
`[cv_a,cc_a] cap Z`; it is the projection of `z_min` onto `[cv_a,cc_a]`.
Thus `|m-a|=O_K(t^2)`. Decompose the convex output into

```
cv_h=h(a)-[h(a)-h_Z^cv(a)]+[h_Z^cv(m)-h_Z^cv(a)].
```

The first bracket is `t^2(h''(a*)^-/2)A_a+o_K(t^2)`. The second is
`h'(a*)(m-a)+O_K(t^3)`, by the affine-subtracted envelope Lipschitz bound.
If `h'(a*)=0`, the propagated quadratic term vanishes regardless of any
jump in `z_min`. If `h'(a*)>0`, the function is strictly increasing on
the entire interval at small scale. A positive-slope affine minorant
through `h(L)` proves that the convex envelope's unique minimum is at
`L`; thus `m=max(cv_a,L)`. By (P),

```
m-a=(cv_a-a)+(L-cv_a)^+=-t^2 E_a^cv+o_K(t^2).
```

If `h'(a*)<0`, the minimum is at `U`,
`m=min(cc_a,U)`, and `m-a=t^2 E_a^cc+o_K(t^2)`. These cases give the exact
convex gap recursion; the maximizing median gives the concave recursion.
The (P) assertion at this factor is exact: the median is in `Z`, and
`min_Z h_Z^cv=min_Z h` because the latter constant is a convex minorant
and equality is forced at a minimizing point. Therefore
`cv_h>=v_h^L`; similarly `cc_h<=v_h^U`. This closes the induction.

Clipping any factor changes its output by `o_K(t^2)`. All later rules are
uniformly `O_K(1)`-Lipschitz in relaxed inputs: products have bounded
coefficients and finite min/max, medians are 1-Lipschitz, and scalar
envelopes have bounded Lipschitz constants. A finite induction therefore
shows that clipping every output leaves the same quadratic coefficients.
Under Lipschitz second derivatives all error estimates, including (P)
and clipping changes, are `O_K(t^3)`. Taylor expansion of the last actual
factor finishes the objective formula. Its Hessian is locally Lipschitz
in the stronger case, so its own Taylor remainder is also `O_K(t^3)`.
QED.

**Exceptional cases and scope.** A zero first-order interval has actual
width `O(t^2)`; its own scalar envelope gap is `O(t^4)`, while inherited
gaps still occur in the recursion. Zero factor values require no special
sign assumption because their endpoint selection error is `O(t^3)`.
At an inflection `h''(a*)=0`, `C^2` gives `o(t^2)` rather than the sketch's
unqualified `O(t^3)`. At a critical point `h'(a*)=0`, the median can jump
without affecting the quadratic coefficient. No denominator requires
positive interval width. The uniform statement includes all these cases
and degenerate shapes.

An exact univariate square has zero convex gap, whereas representing the
same square as a repeated bilinear product gives convex gap
`min{(p_a-ell_a^L)^2,(ell_a^U-p_a)^2}`. The representation can change `Q`
even for the same objective. The theorem does not supply an expansion for
arbitrary auxiliary-variable relaxations with coupled rows or constraints.

Non-differentiability does not universally imply a first-order relaxation
error: `|x|` can be kept exact. It prevents this smooth Taylor theorem from
applying. Likewise `C^{1,1}` alone does not ensure a second-order Taylor
limit: `h(t)=t^2 sin(log|t|)`, `h(0)=0`, has locally Lipschitz first derivative
but oscillatory `h(t)/t^2`.

Finite-box monotonicity remains a separate assumption in every rate use.
The standard clipped procedure's monotonicity citation must match that
exact procedure. Omitting clipping is not justified by its locally
vanishing second-order effect. The source verification belongs to the
literature lead; no literature claim in this audit relies on a new search.

## Boundary one-step theorem and complete repaired iteration theorem

Let `A` be the active lower-bound coordinates of `x*`, and `F` its interior
coordinates. Reflect upper-bound coordinates first. Remove fixed coordinates.
Assume `g_i>0` on `A`, `g_i=0` on `F`, and a uniform expansion

```
phi_{x*+tD(d)}(x*+t xi)
 =f*+t sum_{i in A}g_i xi_i+t^2 Q(d,xi)+r_t(d,xi),
sup_{d in K,xi in D(d)}|r_t|/t^2 -> 0,
```

on every compact set in the closed cone `d_A^-=0`. Require `Q` continuous
on this closed shape-point graph, including zero active extents. The
factorable expansion supplies it when the projected objective is that
specified composite construction. Original constraints beyond bounds
must be covered by the actual projected expansion; box KKT conditions
alone do not supply such an expansion.

For a free shape `d_F`, let `iota(d_F)` insert zero active extents and
`Q^F(d_F,xi_F)=Q(iota(d_F),iota(xi_F))`. Define its nonnegative-cutoff
support map `Phi_c^F`, and
`G_F(d_F)=-min_{xi_F in D_F(d_F)}Q^F(d_F,xi_F)>=0`.

**Boundary one-step lemma** (`lem:boundary-step`). Fix a compact set of
free shapes and `delta>0`. For sufficiently small scale and sufficiently
small active shape extents `sigma=||d_A^+||_infinity`, a Jacobi round has:

```
epsilon<=delta t^2/2
  => (T_U(B))_F subset x*_F+tD_F(Phi_delta^F(d_F));

Q^F(d_F,xi_F)<=-delta
  => x*+t iota(xi_F) in K_U(B), for every epsilon>=0;

min{t d_i^+, [epsilon+(G_F(d_F)-delta/2)t^2]^+/g_i}
 <= width_i(T_U(B))
 <= min{t d_i^+, [epsilon+(G_F(d_F)+delta/2)t^2]/g_i}, i in A.
```

Here `[s]^+=max(s,0)` only avoids an empty constructed interval when the
lower numerator is negative. It strengthens the source's harmless but
unproved negative-right-side case to the automatic zero bound.

**Proof.** On a compact shape-point graph with active extents bounded by
some fixed constant, let `omega` be a modulus of continuity of `Q` and
`rho(t)` a uniform normalized remainder bound. Choose the active shape
and scale so that each is at most `delta/4` after applying its modulus.
Replacing `(d,xi)` by `(iota(d_F),iota(xi_F))` moves it at most `sigma`.
For a retained point,

```
t sum_{i in A}g_i xi_i+t^2 Q^F(d_F,xi_F)
 <= epsilon+(delta/2)t^2.                               (B)
```

Dropping the nonnegative active linear term and using the cutoff condition
gives the free support enclosure. If `xi_A=0` and `Q^F<=-delta`, the upper
expansion bound gives relaxation objective at most `f*-(delta/2)t^2`, so
the point is retained. For the active upper bound, use
`g_i xi_i<=sum_A g_j xi_j` in (B), and
`Q^F>=-G_F`. The lower active endpoint stays zero because `x*` is retained;
nesting caps the width by the old width `t d_i^+`.

For the lower bound, let `xi_F` minimize `Q^F`, set all active coordinates
except `i` to zero, and let its `i`th coordinate be `s in [0,d_i^+]`.
The upper objective estimate is
`f*+t g_i s-G_F t^2+(delta/2)t^2`. Any such `s` satisfying the lower
numerator constraint gives a retained point. If that numerator is negative,
the asserted lower bound is zero and follows from the origin. Otherwise
choose the largest of these permitted `s`. QED.

A sharper version uses the actual error
`eta=omega(sigma)+rho(t)` in place of `delta/2` in the two active bounds.
Consequently, along any boxes whose scaled active extents vanish while
`t->0`, uniformly over compact free shape sets and all `epsilon>=0`,

```
width_i(T_U(B))
 =min{width_i(B), (epsilon+G_F(d_F)t^2)/g_i}+o(t^2).       (B-asym)
```

**Justification.** The expression `min{a,max(0,z)/g_i}` is
`1/g_i`-Lipschitz in `z`. The base numerator
`epsilon+G_F t^2` is nonnegative. Both bounds differ from its capped
value by at most `eta t^2/g_i`, which is `o(t^2)`. This gives the equality
on the actual starting box. It does not give an equality after replacing
that box's free shape by a possibly much larger enclosing free shape.
The lower bound and (B-asym) are Jacobi statements; sequential rebuilding
may invalidate the constructed witnesses before the end of a full pass.

**Repaired boundary iteration theorem** (`thm:boundary-rates`). Suppose
`u_F>>0`, `delta>0`, and `lambda in (0,1)` satisfy
`Phi_delta^F(u_F)<=lambda u_F`. Fix `M>=0`, and let

```
G_M=-min{Q(d,xi):d_F=u_F, d_A^-=0,
                0<=d_A^+<=M, xi in D(d)},
G_0=G_F(u_F),  g_min=min_{i in A}g_i.
```

Then `0<=G_0<=G_M`, and there is a small scale `t_bar>0` such that the
following holds. Start from a box `B^0` containing `x*`, with free part
inside `x*_F+t_0D_F(u_F)` and active upper extents at most `M t_0`, where
`0<t_0<=t_bar`. All local comparison boxes must be in the original relaxation
domain. For `k>=1`, set `s_k=lambda^(k-1)t_0`, and let

```
N=min{k>=1:s_k^2<2epsilon/delta},
```

with `N=infinity` when `epsilon=0`. Then:

- The free part of `B^k` is inside `x*_F+s_kD_F(u_F)` for `1<=k<=N`.
- The initial active bound is
  `width_i(B^1)<=[epsilon+(G_M+delta/4)t_0^2]/g_i`.
- If `N>1`, then for `1<=k<=N`,
  `width_i(B^{k+1})<=[epsilon+(G_0+eta_k)s_k^2]/g_i`,
  where `0<=eta_k<=delta/2`, and `eta_k->0` when `s_k->0`.
- If `N=1`, keep the initial coarse active estimate; it also bounds all
  later active widths by nesting. The refined clause is not asserted.
- At zero cutoff, the limiting box is `{x*}`,
  the free widths are `O(lambda^k)`, and
  `width_i(B^{k+1})<=(G_0/g_i+o(1))s_k^2`.
- At positive cutoff,
  `(B_infinity)_F subset x*_F+sqrt(2epsilon/delta)D_F(u_F)` and
  `width_i(B_infinity)<=(2+2G_M/delta)epsilon/g_i`.

Thus the free part has a geometric upper enclosure after one preliminary
step and the active part has its squared-scale upper bound. Any
`lambda in (r*(Phi^F),1)` is admissible after choosing an appropriate
shape and slack. This does not establish actual successive free-width
ratios or a one-round recurrence in their actual gauge.

**Proof.** Use the compact comparison shape set with free part `u_F` and
active extents at most `M'=max(M,1)`. Let `omega` be the modulus of continuity
on its graph and `rho` its normalized remainder bound. Choose
`sigma_bar<=1` with `omega(sigma_bar)<=delta/4`. Put

```
C=(G_M+delta)/(lambda g_min).
```

Choose `t_bar` so that `rho(t)<=delta/4` on smaller scales,
`C t_bar<=sigma_bar`, and all comparison boxes are admissible. In particular,
their free coordinates fit in the interior domain, and their active
coordinates fit above the active lower bounds and below the upper bounds.

Step zero to one preserves the initial free enclosure by nesting.
On the original enclosing shape, nonnegativity of the active linear term
and the definition of `G_M` give the coarse active bound. If `N>1`, then
`epsilon<=delta t_0^2/2`. Relative to `s_1=t_0`, the first active shape is
at most `(G_M+3delta/4)t_0/g_min<=C t_0<=sigma_bar`.

Now assume `1<=k<N` and enclose `B^k` with free shape `u_F` at scale
`s_k`, using its actual active extents divided by `s_k`. Call their maximum
`sigma_k`. The preceding construction starts the induction with
`sigma_k<=sigma_bar`. The one-step lemma applies because
`epsilon<=delta s_k^2/2`. Monotonicity transfers the enclosing box's free
support bound to `B^k`, giving the free enclosure at scale
`s_{k+1}=lambda s_k`. Using the exact continuity/remainder terms gives

```
width_i(B^{k+1})
 <=[epsilon+(G_0+omega(sigma_k)+rho(s_k))s_k^2]/g_i.
```

The normalized active extent at the next scale is at most
`(G_0+delta)s_k/(lambda g_min)<=C s_k<=sigma_bar`, closing the induction.
The active estimate also applies at `k=N` when `N>1`, because that
one-step estimate has no upper restriction on the cutoff. Moreover
`sigma_1<=C t_0` and `sigma_k<=C s_{k-1}` for `k>=2`, so
`eta_k=omega(sigma_k)+rho(s_k)` tends to zero with the scales.

At zero cutoff this induction never stops; both free and active enclosures
vanish, proving the limiting and rate upper bounds. If `epsilon>0` and
`N>1`, the free enclosure at step `N` has scale below the cutoff threshold,
and nesting preserves it thereafter. The active estimate at this step
gives the tighter floor `(2+2G_0/delta)epsilon/g_i`, hence the stated coarse
floor. If `N=1`, the original free enclosure already lies below the cutoff
threshold; the initial active estimate and `t_0^2<2epsilon/delta` give
`(3/2+2G_M/delta)epsilon/g_i`, which is again at most the stated floor.
This proves every case without the source's invalid refined estimate at
`N=1`. Complete sequential passes inherit the upper enclosures, using their
containment in the Jacobi round at each comparison box. QED.

**Why the actual free gauge need not contract every round.** This distinction
is not just a caution about proof wording. On `x>=0`, take
`f(x,y)=x+y^2`, and the valid monotone convex family

```
phi_B(x,y)=f(x,y)-h_A(B)^2,
```

where `h_A(B)` is the active upper extent from zero. For boxes containing
zero, restricting the box decreases this constant error. Its boundary
expansion is exact, with `Q(d,xi)=xi_y^2-(d_A^+)^2`; the reduced free map
is `Phi_delta^F(u_F)=sqrt(delta)u_F` for `u_F=(1,1)` and `delta<1`.
Start at `[0,t_0] x [-t_0^3,t_0^3]`, `0<t_0<1`, and use zero cutoff.
Its exact map sends active height `h` to `h^2` and free radius `r` to
`min(r,h)`. The first two active heights are `t_0^2,t_0^4`, but both free
radii remain `t_0^3`. Thus the actual free ratio from step one to two is
one, even though any admissible geometric enclosing-scale theorem holds.
The example satisfies all abstract boundary assumptions. A stronger actual
gauge recurrence would need a new assumption relating active extents to
the actual free gauge.

The phrase “quadratically relative to the free widths” should therefore
be written as “bounded by the square of the free geometric enclosing
scale.” The source's equation-like
`width_i=(G_0/g_i+o(1))s_k^2, or smaller` must become the explicit upper
inequality in the repaired theorem. The sharp equality (B-asym) uses the
actual free shape and retains the minimum by the old active width.

If all directions are strictly complementary active bound directions,
the positive linear term and a second-order relaxation error imply the
sharp-growth proposition locally; there is no free part requiring this
theorem. If an active bound has zero gradient, include that coordinate in
the tangent shape with its prohibited endpoint fixed at zero. The interior
gauge proof works on this admissible one-sided cone if a strict contraction
shape dominates all allowed signed extents. Strict complementarity cannot
be silently dropped from the active linear estimate.

## Interpretation and source boundaries

All results above have proofs under their explicitly stated assumptions.
The manuscript can retain the full September mathematics without treating
the following stronger interpretations as established results:

- General identity between `r*` and a nonlinear asymptotic spectral radius.
- Successive-ratio convergence from every asymmetric start.
- A shape-independent exact positive-cutoff floor for every initial box.
- Actual per-round boundary free-gauge contraction under only the enclosing
  box hypotheses.
- An active-width equality based on a larger fictitious free box.
- A convergence rate that depends only on the original objective, regardless
  of its factorization, retained constraints, or relaxation.
- A certificate of eventual stalling inferred from observed near-one ratios.

The archived sequential ratios are numerical illustrations of the formulation
distinction; this audit has not rerun them and does not turn them into proved
exact sequential asymptotic constants. The rigorous transfer is the complete
sequential pass's upper enclosure and the protected-witness stalling result.
Slow zero-cutoff contraction, a nonzero cutoff floor, and an exact stall can
all produce ratios near one. Local rate hypotheses may hold at particular
branch-and-bound nodes, but do not establish a universal activation policy
or a complexity theorem for a solver.

Literature requests sent to the sole lead concern the exact clipped
Scott–Stuber–Barton partition-monotonic procedure; the
Mitsos–Chachuat–Barton product/median rules; Bompadre–Mitsos error-order
conditions; Ryoo–Sahinidis attribution for the elementary sharp-growth
bound; and the Wechsung–Schaber–Barton and Kannan–Barton cluster-prefactor
comparison. The literature lead replied that these are already in the
source ledger/KB and is vetting the packages. No source search was performed
here. The rate proof with a positive eigenvector is elementary and needs
no nonlinear Perron–Frobenius theorem. The earlier limited literature
searches do not establish priority for the full tangent formulation.

The new exact uniform-family formula, signed three-variable example, asymmetric eigenvector
condition, rectangular support formulas, positive-cutoff cube formula,
endpoint-tangent square rectangle, and boundary counterexamples are
analytic developments in this audit. They make no empirical claim and no
priority claim. The examples specify the relaxation that produces them.

## Verification actually performed

Read `AGENTS.md`, the manuscript brief, all substantive mathematical
sections of September `theory.md`, `proofs-12-11.md`, and
`review-theory.md`, and October `document/foundations.tex`. Read the
October reference family's square-relaxation description and its exact
three-variable protected-box example to check formulation consistency.
Commands were targeted `cat`, `sed -n`, and `rg -n` reads of those files.

Two narrow exact-arithmetic commands, each invoked as `python -` with an
inline script importing `fractions.Fraction`, passed:

1. Boundary terminal-case arithmetic at `t_0=1/100`,
   `epsilon=1/200`, `delta=1/4`: computed
   `h_1=1/198`, `h_2=99/19700`, and the false claimed upper value
   `401/80000`. Asserted `h_2` exceeds that value and
   `(h_2-epsilon)/t_0^2=50/197` equals the derived formula.
2. Signed three-variable stall: verified the three displayed eigenvectors
   of `A` with eigenvalues `-2,1,1`; checked all six displayed face witnesses
   have exactly `Q=-1/32`. The Hessian eigenvalues were
   `1/2,11/4,11/4`, while the row quantities were `5/2` and `9/4`.

Also ran `wc -l -w paper-adaptive-obbt/evidence/audit-rates.md` and a targeted
`rg -n` scan of its status, section headings, and unfinished-work markers.
The full mathematical checks are analytic proofs above; no numerical
experiment, solver loop, random-instance check, project-wide verification,
CI-status inspection, or CI-log inspection was run. All writes were confined
to this evidence file.

## Supplemental confirmation of foundations integration points

At the root's request, independently checked the new foundations draft and
its integration notes after completing the rates audit. The checks below
preserve the preceding audit and strengthen the foundations' scope.

**Original sublevel hull and protected boxes are independent enclosures.**
The assertion `H_U subset P` for every fixed or protected box `P` is false.
For a counterexample in which neither contains the other, take
`f(x)=x^2` on `[-1,1]`, cutoff `U=0`, and `phi_B(x)=0` on every box.
This family is valid and monotone, with compact sublevel sets. Then
`H_U={0}`, `P={1}` is a fixed box, and `B_infinity=[-1,1]`.
The valid inclusions are independently

```
H_U subset B_infinity,
P subset B_infinity subset B_k  whenever P subset B_0 is fixed.
```

The protected-box endpoint ceilings use only the second inclusion. For
`P=[a,b] subset B_k=[ell^k,u^k]`, they remain
`ell_i^infinity-ell_i^k<=a_i-ell_i^k` and
`u_i^k-u_i^infinity<=u_i^k-b_i`.

The original sublevel hull is itself fixed when it is nonempty. This does
not require the original sublevel points to attain its faces or require
global continuity of `f`. Write `S_U={x in X cap B_0:f(x)<=U}`. Validity
gives `S_U subset K_U(H_U) subset H_U`. Taking **closed box hulls** gives
`H_U subset T_U(H_U) subset H_U`, hence equality. Compactness of
`K_U(H_U)` supplies relaxed face attainment afterwards.

**Fair directional schedules have the Jacobi limit without closed-family
continuity** (`lem:fair-schedule`). Fix the relaxation family and cutoff.
Let `C_t` be exact directional updates starting at `B_0`, and suppose each
of the finitely many signed directions is selected infinitely often.
Every individual update contains `T_U` on its input, so induction gives
`T_U^t(B_0) subset C_t`. Partition the realized schedule into finite
successive blocks, each containing every signed direction at least once;
fairness permits this even when block lengths are unbounded. Write `t_j`
for the end of block `j`, with `t_0=0`.

Within a block, each support is computed over a smaller cutoff set than
the one on its block-start box. Once a direction has been processed, its
endpoint is therefore at least as tight as the frozen Jacobi endpoint
on that block-start box; later updates never move it outward. Thus

```
C_{t_j} subset T_U(C_{t_{j-1}}) subset T_U^j(B_0),
T_U^{t_j}(B_0) subset C_{t_j} subset T_U^j(B_0).
```

Both `j` and `t_j` tend to infinity. Intersecting these nested, cofinal
sequences proves that the directional and Jacobi intersections are the
same. Neither closed-family continuity nor fixedness was used. They can
have different rates per completed sweep or per support solve.

Closedness along decreasing shape sequences is needed only for the
additional conclusion that the common limit is fixed. Under that
assumption, take an attaining support witness at each time a given
direction is updated, extract a convergent subsequence, and pass to the
limit cutoff set. Its coordinate equals the limiting endpoint. Repeating
for all directions proves face attainment and hence fixedness. This is
the appropriate place for that extra assumption in the foundations.

The supplemental verification used targeted `cat` reads of
`paper-adaptive-obbt/sections/foundations.tex` and
`paper-adaptive-obbt/evidence/INTEGRATION-NOTES.md` and the analytic
arguments above. No other file was edited and no experiment was run.
