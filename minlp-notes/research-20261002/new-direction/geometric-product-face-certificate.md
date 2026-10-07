# Sparse growth certificates for an optimal coordinate fiber

Date: 2026-10-02. Status: complete derivation with a
[fresh independent review](../reviews/geometric-product-face-review.md)
and targeted exact checks. No priority claim is made.

A proposed coordinate fiber can be certified as the exact optimal set
of a rational mixed-box QP, with a verified positive growth constant,
without trusting a supplied growth bound or enumerating its
free-coordinate modes. Both active and free coordinates may be
continuous or integer, with arbitrary binary-encoded interval lengths.
Section 5 gives this general result in the original Euclidean metric.
Sections 1--4 first prove the simpler normalized case of continuous
active coordinates fixed at a box face. That proof uses the
relative-rounding argument from the
[strict-copositivity certificate](geometric-copositive-certificate.md),
combined with exact endpoint rounding in directions along the face.

The coordinate fiber is supplied. This does not discover or certify an
arbitrary unknown union of faces, tilted flat manifold, or disconnected
optimal set. Normalizing side lengths changes the conditioning in
Sections 1--4; Section 5 avoids that change by using physical shells.

## 1. Model and checks

Let `m>=1`, and let `Y` be a nonempty bounded rational mixed box.
Integer bounds are rounded inward; fixed coordinates are substituted
out. For each free integer coordinate with exactly two effective
labels `l,u`, replace its square by `(l+u)y_i-lu`. This unary
substitution is exact at both feasible labels. It preserves the
objective on the whole mixed domain, introduces no interaction edge,
and does not change any active diagonal curvature.

After this preprocessing, the domain and objective are

\[
 X=[0,1]^m\times Y,\qquad
 F(x,y)-f_0=a(y)^Tx+x^TAx,\qquad a(y)=c+By,\quad A=A^T.
 \tag{1}
\]

The proposed optimal set is the entire product face

\[
                     S=\{0\}\times Y.                            \tag{2}
\]

For a general input quadratic, (1) is a directly checkable polynomial
identity: subtract its value `f_0` at the proposed face and check that
every term involving only free coordinates vanishes. In particular,
the reduced free-free Hessian block and free linear coefficients are
zero. With the stated preprocessing, this is also a complete test
that the original objective is constant on the proposed mixed face.
Cross coefficients must vanish by differences on two-coordinate
rectangles. Each remaining free quadratic diagonal has either at
least three integer labels or a nondegenerate real interval, so
constancy forces its quadratic and linear coefficients to vanish.
The two-label reductions are necessary: a unary term such as
`y_i(y_i-1)` is zero on a binary domain without being a zero polynomial.

Check also

\[
            \min_{y\in Y} a_i(y)\ge0\qquad(i=1,\ldots,m).        \tag{3}
\]

Each minimum is a scalar affine-box minimization, determined by the
signs of the entries in row `i` of `B`. Integer free coordinates
cause no difficulty: the minimizing bound is feasible. If (3) fails,
the supplied face is not globally optimal, because a sufficiently
small positive change in continuous coordinate `x_i` decreases the
objective. Thus this check loses no instance whose exact optimal
set really is (2).

Let `L>0` be a supplied rational bound for the active diagonal
curvatures, `2A_ii<=L`. A positive upper bound can always be chosen;
the numerical guarantee depends on the one used. Let the supplied
interaction-graph decomposition have `N` bags of size at most `p`,
including both active and free coordinates. Its encoding and the
objective/domain coefficients have total length `I`.

The algorithm is not given a growth constant. For the complexity
analysis, define the true constant

\[
 g=\inf_{x\ne0,\ y\in Y}
          \frac{F(x,y)-f_0}{\|x\|_2^2}
 \tag{4}
\]

and write `kappa=max(1,L/g)` when `g>0`. Then `S` is indeed the
exact optimal set, and `dist((x,y),S)^2=||x||^2`.

Conversely, if `S` is exactly the optimal set, then `g>0`
automatically. The radial inequality proved below makes (4) equal
to the minimum ratio on `max_i x_i=1`, with `y` still in `Y`.
That shell is compact, its denominator is nonzero, and exactness of
the proposed optimal set makes the numerator strictly positive.
Thus termination requires only that the supplied face really be
the exact optimal set; conditioning controls the quantitative bound.

## 2. One sound finite test

For `delta=2^{-r}`, `r>=1`, put

\[
              \eta=\delta/m,\qquad \sigma=L\delta^2/8.
 \tag{5}
\]

For every active coordinate, build `G_delta` from `0,eta` by
multiplying successive positive nodes by `1+delta` and clipping
the final interval at one. Every free coordinate has just its two
feasible endpoints (one label if fixed). Define

\[
 \begin{split}
 M_\delta&=\min_{u\in G_\delta^m,\ \max_i u_i=1,\ v\in V(Y)}
       \bigl[F(u,v)-f_0-2\sigma\|u\|^2\bigr],\\
 b_\delta&=M_\delta-\sigma/m,
 \end{split}                                                    \tag{6}
\]

where `V(Y)` denotes endpoint choices, represented by local labels
in the DP rather than an explicit list of all combinations.

**Soundness.** If the identity (1) and sign check (3) hold, every
trial gives the global inequality

\[
 F(x,y)-f_0\ge
          \sigma\|x\|^2+b_\delta\|x\|_\infty^2
                    \qquad((x,y)\in X).                         \tag{7}
\]

Thus `b_delta>0` certifies exactly the optimal face (2) and the
positive Euclidean growth margin `sigma`. It is valid even if the
growth promise was false or no growth constant was supplied. A
certificate consists of the identity/sign checks, the rational grid,
DP tables proving (6), and the positive rational root bound.

**Proof.** First suppose `max_i x_i=1`. Independently round each
active coordinate to its enclosing grid endpoints with its mean
preserved. Independently round each free coordinate to its original
endpoints, also preserving its mean. Let the results be `U,V`.
An active coordinate originally equal to one remains one.

Every cross term has unchanged expectation. The free diagonal
quadratic terms vanish by (1). Consequently only active-coordinate
variances contribute. As in the copositive-grid argument,

\[
 4\sum_i\operatorname{Var}(U_i)
       \le\delta^2\mathbb E\|U\|^2+m\eta^2.
 \tag{8}
\]

For `R(x,y)=F(x,y)-f_0-sigma||x||^2`, this gives

\[
 \begin{split}
 \mathbb E R(U,V)-R(x,y)
   &=\sum_i(A_{ii}-\sigma)\operatorname{Var}(U_i)\\
   &\le \sigma\mathbb E\|U\|^2+\sigma/m.
 \end{split}                                                    \tag{9}
\]

Hence `R(x,y)>=M_delta-sigma/m=b_delta` on the normalized
active shell. Free-coordinate rounding introduces no error even
when its domain contains exponentially many integer labels.

For a general nonzero `x`, put `t=||x||_infinity` and `u=x/t`.
The sign check (3) implies the radial inequality

\[
 F(tu,y)-f_0
   =t\,a(y)^Tu+t^2u^TAu
   \ge t^2\bigl(F(u,y)-f_0\bigr).
 \tag{10}
\]

Apply the shell bound and multiply by `t^2` to obtain (7).
At `x=0`, the identity (1) gives equality. `□`

## 3. Unknown growth and conditioning

Try `delta=1/2,1/4,1/8,...` and stop at the first `b_delta>0`.
If `g>0`, every feasible grid assignment in (6) satisfies
`||u||^2>=1` and `F(u,v)-f_0>=g||u||^2`. For `sigma<=g/4`,

\[
 M_\delta\ge g-2\sigma,\qquad
 b_\delta\ge g-(2+1/m)\sigma\ge g/4>0.                         \tag{11}
\]

The search therefore terminates. If the successful trial is not the
first, its predecessor had margin parameter `4sigma` and failed,
so `4sigma>g/4`. At the first trial `sigma=L/32`. Therefore

\[
 \sigma\ge\min\{L/32,g/16\},\qquad
          L/\sigma\le32\max\{1,L/g\}=32\kappa.                 \tag{12}
\]

The verified margin need not approximate `g` within a fixed factor:
an arbitrarily large positive affine term can make `g/L` arbitrarily
large. The guarantee is the displayed bound on the *verified
conditioning*. Increasing `L` merely to make it an upper bound on
`g` can lose the intended parameter dependence and is unnecessary.

There are `O(1+log kappa)` trials, and at the last trial
`delta^{-1}<=2sqrt(kappa)`. Thus the active grid has

\[
             K=O\bigl(\sqrt\kappa\log(2m\sqrt\kappa)\bigr)
 \tag{13}
\]

labels. Every free coordinate has at most two labels.

## 4. Sparse DP and rational size

Assign each factor to one bag containing its variables and each
active norm penalty to an owner bag. A message is indexed by its
separator labels and one bit indicating whether an active coordinate
owned in the subtree has value one. Combine bits by OR. Endpoint
choices of free variables contribute ordinary local labels and do
not contribute to the flag.

The root's bit-one minimum is (6). Sequentially combining children
avoids an exponential dependence on node degree. Arithmetic work is
`poly(p) O(N max(K,2)^p)` per trial, plus reading/assigning factors.
Since powers of `log(2m)` can be absorbed into a parameter-dependent
constant times a fixed power of `m`, the total work and certificate
size are `f(p,kappa) poly(I)` with an absolute input exponent.

Active grid coordinates have the same common-denominator bound as
in the strict-copositivity note. Free endpoint denominators already
have total bit length bounded by `I`. A common denominator for the
rational coefficients, endpoints, grid, and `sigma` gives a common
denominator for all local table values. Every finite DP message is a
sum of assigned factors; its bit length is polynomial in `I` and
the grid encoding, with parameter dependence through `p,kappa`.
No denominator multiplication across bags is needed. Exact table
generation, comparison, and verification therefore satisfy the same
`f_1(p,kappa) poly(I)` bit bound.

These are explicit finite DP certificates. Their significance is
the independently verified margin for a full optimal face with
width-controlled size, not the observation that an arbitrary search
trace can be logged.

## 5. Native mixed-coordinate fibers

The [physical-shell theorem](mixed-shell-certificate.md) gives a
stronger corollary with the same free-coordinate argument. Let
`X_A` and `Y` be bounded rational mixed boxes. Coordinates may lie
on supplied rational lattices; ordinary integers have spacing one.
Let `v` be a proposed feasible point of the active box, and set

\[
       S=\{v\}\times Y,\qquad
       F(v+d,y)-f_0=a(y)^Td+d^TAd.                              \tag{14}
\]

Remove fixed coordinates and apply the free two-label unary
reductions from Section 1. The displayed identity is then exactly
the check that `F(v,y)=f_0` on the entire supplied fiber. If no
active coordinates remain, the identity itself certifies the whole
domain and there is no nonzero distance to bound. Otherwise let
`m>=1` be the number of active coordinates.

For every continuous active coordinate `i` and every available
sign `epsilon` at `v_i`, check

\[
           \min_{y\in Y}\epsilon a_i(y)\ge0.                  \tag{15}
\]

These are affine-box endpoint checks. They are necessary for the
fiber to be globally optimal: failure gives a free endpoint
assignment and a sufficiently small continuous active descent step.
An active interior continuous coordinate requires `a_i(y)=0`
throughout `Y`. No such first-order condition is imposed on active
lattice coordinates.

Let `L>0` be a supplied bound for `2A_ii` on the active coordinates.
Keep the original coordinate units, define

\[
 g=\inf_{d\ne0,\ v+d\in X_A,\ y\in Y}
       \frac{F(v+d,y)-f_0}{\|d\|^2},\qquad
                \kappa=\max\{1,L/g\}\quad(g>0),                \tag{16}
\]

and retain the interaction decomposition of the full quadratic,
including free coordinates. Its bag size is `p` and its total
rational input length, including the proposed fiber, is `I`.

**Mixed-fiber certificate.** A finite rational verifier can certify

\[
              F(x,y)-f_0\ge\sigma\|x-v\|^2
               =\sigma\operatorname{dist}((x,y),S)^2            \tag{17}
\]

with `sigma>0`, without receiving a growth constant. If the
supplied fiber is exactly the optimal set, the certificate search
terminates with

\[
 \sigma\ge\min\{L/32,g/12\},\qquad L/\sigma\le32\kappa,          \tag{18}
\]

using `f(p,kappa) poly(I)` bit work and certificate size, with an
absolute input exponent. This is a physical distance-to-fiber
bound; no side-width factor enters the numerical conditioning.

Here are the full changes to the point-shell proof. Define its
bottom radius using only active coordinates:

\[
 r_0=\min\bigl(
  \{h_i/2:i\text{ is an active lattice coordinate}\}
  \cup\{|e-v_i|:i\text{ is active continuous},\ e\text{ is an endpoint},
                                         \ |e-v_i|>0\}\bigr).
 \tag{19}
\]

Set `D=max_{x in X_A}||x-v||_infinity` and use dyadic radii
`S_j=2^j r_0` through `S_j<=D`. At each radius use exactly the
signed continuous/lattice grids of the physical-shell theorem,
with its coordinate count replaced by `m`. Give every free
coordinate its two feasible endpoints. With `sigma=L delta^2/8`,
compute the DP minimum

\[
 M_{S,\delta}=\min_{u\in G_{S,\delta},\ \|u-v\|_\infty\ge S,
                              \ y\in V(Y)}
       [F(u,y)-f_0-2\sigma\|u-v\|^2].                          \tag{20}
\]

The owned-variable OR flag records only whether an **active**
coordinate has displacement at least `S`. Free endpoint labels
do not affect that flag. Check `M_{S,delta}>=sigma S^2/m` at
every radius.

Indeed, independent rounding of active coordinates has variance
bound
`4 sum_i Var(U_i)<=delta^2 E||U-v||^2+delta^2 S^2/m`.
Independently rounding free coordinates to their endpoints
preserves every affine and active-free bilinear expectation; it
introduces no additional error because the reduced free-free
quadratic block is zero. The same calculation as (9) therefore
gives, throughout that active shell and for every feasible free `y`,

\[
 F(x,y)-f_0-\sigma\|x-v\|^2
               \ge M_{S,\delta}-\sigma S^2/m.                  \tag{21}
\]

Below `r_0`, all active lattice coordinates stay fixed. Every
remaining nonzero active displacement can be scaled to the bottom
shell on its continuous ray. Hold `y` fixed during that scaling;
(15) makes the linear term nonnegative, so the radial inequality
extends (21) inward. This proves (17).

If the proposed fiber is the exact optimal set, (15) holds, and
the objective gap is strictly positive on the compact region
`||x-v||_infinity>=r_0`. The radial argument makes the growth ratio
at every smaller displacement no less than its value at the
bottom shell with the same `y`. Thus (16) has `g>0` automatically.
All shell tests pass once `sigma<=g/3`; the first-success argument
from the point theorem proves (18).

There are `O(I)` radii. Each active coordinate has
`O(delta^{-1} log(2m/delta))` states, and each free coordinate has
at most two. Running separate shell DPs multiplies work by the
number of radii, not by its `p`th power. The same common-denominator
argument applies to their rational tables and messages. Free
domain widths affect input bit lengths but not their state count.
This proves the stated bit bound.

If every active `A_ii<=0`, use the simpler endpoint branch instead.
Every active coordinate of `v` must be an endpoint, or concavity
gives a different active endpoint with no greater value and the
proposed fiber is not the exact optimal set. Run endpoint DP over
both active and free coordinates, with a flag for an active value
different from `v`. Let `Delta` be its minimum gap above `f_0`.
If `Delta<=0`, the witness disproves the proposed exact optimal
fiber. If `Delta>0`, endpoint rounding gives (17) with

\[
                   \sigma=\Delta/\sum_{i=1}^m w_i^2,            \tag{22}
\]

where `w_i` are active side widths. In detail, for
`t_i=|x_i-v_i|/w_i`, the expected objective gap is at least
`Delta Pr(U_A!=v)>=Delta max_i t_i`, which is at least
`sigma||x-v||^2` with `sigma` from (22). Free endpoint assignments with
`U_A=v` have gap zero by the checked fiber identity. This branch
takes `f(p) poly(I)` work and requires no positive curvature scale.

## 6. Limits and relation to other results

The free coordinates do not have arbitrary nonlinear recourse. The
polynomial identity along the whole supplied face makes their
conditional objective affine; endpoint rounding is exact for that
reason. The method does not enumerate the potentially exponential
number of endpoint combinations, but ordinary tree DP is already
the relevant tool for these finite labels.

The normalized radial argument and necessity of (3) use continuous
active coordinates. Section 5 handles mixed active coordinates by
using physical shells and applying radial scaling only where the
active lattice coordinates are fixed. The example `F(x,y)=(x-y)^2`
with its diagonal optimal segment remains outside this
coordinate-fiber theorem.
Changing coordinates to expose such a segment may turn a box into
coupled inequalities and destroy the sparse box representation.

Most importantly, a proposed coordinate fiber is a compact description
of the full optimal set. The theorem verifies that description; it
does not obtain one when the optimal set is unknown. It does not
remove the need for a supplied growth promise in the existing
general [proximal algorithm](proximal-growth-grid.md).

## 7. Review and targeted verification

The [fresh independent review](../reviews/geometric-product-face-review.md)
found no substantive gap. It includes the two-label reduction,
complete face-constancy check, compact-shell argument for automatic
growth, relative-rounding identity, first-success bound, and sparse
bit complexity. The coordinating researcher independently checked
the core argument as well.

Its native mixed-fiber addendum also checks active-only shell
geometry and flags, uniform continuous first-order conditions,
the physical growth bound, and the nonpositive-diagonal endpoint
branch. The underlying [point-shell theorem](mixed-shell-certificate.md)
has separate independent proof and grid/bit reviews linked there.

The targeted command

```
python3 -B research-20261002/new-direction/check_geometric_product_face.py
```

passed six finite certificates from 208 endpoint-grid entries,
70 exact rounding identities, 280 radially scaled growth checks,
and 18 two-label reductions including 81-bit integer endpoints.
The fixtures include negative active diagonal curvature,
nonconvex active coupling, and a free integer interval with over
one million labels. The native extension passed another 378
mixed-fiber and inner-region cases from 208 endpoint-shell entries;
free coordinates enter the objective and endpoint rounding but not
the active-radius flag. The checker enumerates small tables and
rounding atoms; it is not an implementation of sparse DP.
These finite checks support the identities;
the continuous-domain and complexity claims rest on the proofs.

No project-wide verification or CI inspection was performed.
