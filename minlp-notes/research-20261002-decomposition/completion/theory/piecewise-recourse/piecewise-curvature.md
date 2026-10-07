# Curvature cancellation across changing convex responses

Date: 2026-10-03. Status: theorem and exact scalar-attachment implementation;
[independent review](review.md) and [diagnostic results](check-results.json).

This extends the existing globally affine recourse reduction to **locally
certified piecewise-affine responses**. The useful bound is the largest
coordinate curvature of the reduced pieces. It can remain bounded while
the direct retained-coordinate curvature diverges and the response changes
active set. Local partitions remain local: the algorithm neither constructs
their global overlay nor increases their attachment scopes.

The pieces are an explicit input to the complexity bound. Finding a short
partition in general is not claimed. Parametric-QP critical regions are
classical; the contribution here is their verified curvature composition
with the existing sparse filtered-grid theorem, including nonsmooth and
singular cases, and a separating family.

## 1. Model and coverage certificate

Use the model of [affine convex recourse](../../../negative-curvature/affine-convex-recourse.md):

\[
 F(z,y)=q_0(z)+\sum_t f_t(y_t,E_tz),\qquad
 f_t(y,v)=\tfrac12y^TC_ty+y^TD_tv+c_t^Ty
          +\tfrac12v^TA_tv+d_t^Tv+e_t,                 \tag{1}
\]

where all data are rational, `C_t` is PSD, `z` lies in a product box,
and private blocks `y_t` lie in independent product boxes. Each `E_t`
selects distinct retained coordinates. Substitute
fixed coordinates first. Attachment scopes and every quadratic factor of
`q0` must fit in bags of a supplied retained-variable tree decomposition.
Private feasible sets do not depend on the retained variables.

For each attachment box, supply a rational binary space partition (BSP).
Its root is the entire attachment box. An internal node labelled by
`a^T v <= b` has the two closed children obtained by intersecting its
parent with `a^T v <= b` and `a^T v >= b`. Accept a split only when both
children have nonempty full-dimensional interior, and keep their closures.
The closed full-dimensional leaves cover the root, including every
interface. Constant-scope blocks need a single ordinary convex-QP certificate.

Each leaf polytope `P={v:Gv<=h}` carries rational affine maps

\[
 \bar y(v)=a+Bv,\qquad \lambda(v)=r+Rv,\qquad
 \mu(v)=s+Sv                                             \tag{2}
\]

with the following identities and inequalities on `P`:

\[
 \begin{split}
 &l\le\bar y(v)\le u,\quad \lambda(v),\mu(v)\ge0,\\
 &C\bar y(v)+Dv+c=\lambda(v)-\mu(v),\\
 &\lambda_i(v)(\bar y_i(v)-l_i)=0,
 \quad\mu_i(v)(u_i-\bar y_i(v))=0.                    \tag{3}
 \end{split}
\]

PSD, stationarity, and complementarity are exact rational algebra checks.
Since `P` has interior, complementarity is a polynomial coefficient
identity. Every affine sign or feasibility condition is checked by LP.
It can instead be replayed from rational dual multipliers: to establish
`c0+c^T v>=0` on nonempty bounded `Gv<=h`, supply `w>=0` with
`G^T w=-c` and `h^T w<=c0`. Rational LP duality guarantees such a witness
whenever the inequality holds. Thus numerical LP success is not accepted
as a certificate. Rational strict-interior points certify the full
dimensionality of the nodes that are retained.

The BSP itself proves coverage. Shared boundary points can occur in both
leaves; this is harmless. The KKT conditions certify both responses there,
so both quadratic values agree. Responses themselves need not agree when
`C` is singular. A collection of sampled KKT points or an arbitrary list
of polyhedra without a coverage proof does not meet this contract.

Let `S` denote the total bit length of the problem, decomposition, trees,
affine maps, and LP witnesses. Verification is polynomial in `S`. No
claim bounds `S` polynomially in the original problem encoding.

## 2. Piecewise reduced curvature is a global bound

On leaf `r`, substitution in (1) gives a quadratic `q_tr(v)` with Hessian

\[
 H_{tr}=A_t+B_{tr}^TC_tB_{tr}+B_{tr}^TD_t+D_t^TB_{tr}.    \tag{4}
\]

The usual KKT identity proves, for every `v` in that leaf and feasible `y`,

\[
 f_t(y,v)-q_{tr}(v)=\tfrac12(y-\bar y)^TC_t(y-\bar y)
           +\lambda(v)^T(y-l)+\mu(v)^T(u-y)\ge0.        \tag{5}
\]

Equality holds at `bar y`. The continuous value function
`phi_t(v)=min_y f_t(y,v)` therefore equals these certified pieces.

For local attachment coordinate `j`, define

\[
 \ell_{tj}=\max_r (H_{tr})_{jj}.                         \tag{6}
\]

These numbers may be negative. **For every fixed choice of the other
attachment coordinates, `phi_t(v)-ell_tj v_j^2/2` is concave as a
function of `v_j`.**

Proof: write `phi_t(v)=v^T A_t v/2+d_t^Tv+e_t+psi_t(v)`.
The function `psi_t` is an infimum of affine functions of `v`, hence is
concave. Along a coordinate line, the finite polyhedral partition makes
`phi_t` continuous and piecewise quadratic. Each open segment has second
derivative at most `ell_tj`. At each joining point, concavity of `psi_t`
gives a nonpositive jump in its one-sided derivative. The added quadratic
has no derivative jump, and neither does the subtracted quadratic
`ell_tj v_j^2/2`. Thus the derivative of the resulting piecewise quadratic
is nonincreasing both within segments and at their joins, which proves
concavity. If the line lies in a leaf boundary, its subsegments are
covered by leaf closures; the restrictions of any two pieces there agree
as univariate polynomials. The same argument applies. This proof permits
singular `C_t`, nonunique responses, downward derivative jumps, and
degenerate interfaces. Continuity alone would not control upward jumps;
the concave-infimum representation is essential. □

Let `H0` be the Hessian of `q0`. For global retained coordinate `i`, put

\[
 L_i=(H_0)_{ii}+\sum_{t:i\in E_t}\ell_{t,j(t,i)},\qquad
 L=\max_i L_i.                                           \tag{7}
\]

The reduced function `V(z)=q0(z)+sum_t phi_t(E_tz)` has upper coordinate
curvature `L_i`, even though different blocks may change regimes at
different parameters. The independent maxima in (7) are a safe bound;
they need not be jointly attainable. Computing them uses only the local
pieces. This avoids the potentially exponential global overlay.

## 3. Certified sparse optimization theorem

Suppose the original objective has a unique global optimizer and global
quadratic growth with constant `g>0` in all original variables, as in the
companion recourse notes. Let `p` be the maximum residual bag size.
If `L>0`, let `kappa=max(1,L/g)`.

**Theorem.** Validated local BSP certificates admit a deterministic
algorithm returning a rational original feasible point with a checkable
gap at most `2^-q` in `f(p,kappa)(S+q+1)^C` bit operations, and an exact
rational original optimizer in `f1(p,kappa)(S+1)^C1` bit operations.
The exponents are absolute. Neither `g` nor `kappa` is input. If every
`L_i<=0`, endpoint DP is exact without growth or uniqueness.

Proof: each reduced optimum lifts to an original optimum, and evaluating
the original growth inequality at a conditional optimizer gives
`V(z)-F*>=g||z-z*||^2`. The preceding lemma supplies the upper coordinate
curvature. A factor query traverses its BSP and evaluates one rational
quadratic; at a boundary either containing leaf is valid. Its feasible
response and KKT certificate are already available. The factor scopes
are unchanged, so the [sparse convex value factor theorem](../../../negative-curvature/sparse-convex-value-factors.md)
applies with (7) in place of the direct diagonal. It uses only upper
coordinate curvature, growth, finite sparse factor tables, and rational
bit bounds; it does not require a smooth or globally quadratic reduced
objective. Certificate replay checks the BSP/KKT package once and then
the finite-tree tables and full filtering history.

Exact output uses a denominator bound for the **original rational QP**,
not an unjustified rational-height argument for an arbitrary piecewise
function. Isolate its optimal value with the certified gap, reconstruct
retained coordinates in shrinking growth windows, lift through containing
leaves, and accept only original feasibility and exact equality to the
isolated value, precisely as in the companion theorem. All coordinates
are rational and all lifted values are exact. If `L_i<=0` for every `i`,
the reduced objective is separately concave; independent endpoint
rounding and finite-tree DP give the exact minimum. □

Any certified bound `L<=C0 beta`, where `nu<=beta<2nu` bounds the original
negative curvature and `C0` is class-wide constant, gives the same
width-plus-`nu/g` corollary as affine condensation. The condition is
substantive. This theorem does not establish it for arbitrary box QPs.

## 4. Recognition and finite construction

A single full-dimensional rational leaf `P` admits a **complete
polynomial-time affine-selector recognition test**, including singular
private Hessians. Choose a rational interior point `v0`, solve its exact
convex QP, and let `h=C y0+D v0+c`. Coordinates with `h_i>0` must be
fixed at their lower bounds by any affine selector; those with `h_i<0`
must be fixed at their upper bounds. Coordinates with `h_i=0` must have
identically zero affine gradient. The proof is the same as the existing
[box recognizer](../../../negative-curvature/adversary/affine-selector-recognition.md):
a feasible affine coordinate attaining a bound at an interior parameter
is constant; a one-signed affine gradient vanishing there is identically
zero. All central optimizers have the same gradient because `C` is PSD.

The remaining unknown affine coefficients satisfy linear stationarity
identities and global affine inequalities over `P`. The LP dual form
above converts every such inequality into a polynomial-size system of
linear equalities and inequalities in those coefficients and fresh
nonnegative dual variables. Feasibility gives the maps in (2)-(3);
infeasibility proves that no affine selector exists on that leaf.
This is a leaf recognizer, not a polynomial test for the existence of
a partition with at most a specified number of leaves.

For **positive-definite** `C`, a finite complete construction is simple,
although it can be exponential. Enumerate all `3^m` lower/free/upper
patterns of an `m`-variable private box. Every free principal submatrix
is invertible, so solve its stationarity equations for an affine response.
Its free-bound inequalities and active-gradient sign inequalities define
a rational critical polyhedron. Collect their nonconstant boundary
hyperplanes and successively split the attachment box along them,
retaining only genuine full-dimensional splits. Each resulting closed
leaf lies in at least one valid critical polyhedron: solve at an interior
point and use its optimal pattern; all signs for that pattern are
constant in the leaf interior and valid on its closure. Label each leaf
with that pattern's affine KKT map. There are at most `O(m 3^m)` candidate
hyperplanes, and in attachment dimension `k` the arrangement has at most
`sum_{j=0}^k binom(H,j)` full-dimensional regions. A BSP with `R` leaves
has `R-1` internal nodes. The construction and certificate bit lengths
are finite, but neither `H` nor `R` is polynomially bounded in `m`.

For a scalar attachment, intersections are rational intervals and all
of this can be done with exact rational linear algebra and comparisons.
The accompanying implementation enumerates patterns, assembles a covered
interval partition, checks KKT algebra and endpoints independently, and
computes (6). For singular blocks the verifier still accepts valid maps;
the included automatic constructor deliberately requires positive
definiteness. [The convex recourse engine](../../../solver/convex_recourse.py)
integrates this scalar constructor to tighten grid corrections, with a
default cap of 81 active patterns per private block. The model certificate
contains the local pieces; replay reconstructs each block from the
original model and checks the pieces independently. The general
polyhedral leaf recognizer and general BSP constructor remain proof-level
algorithms. Their broader implementation is not claimed by this component.

## 5. A separating family with three pieces per block

For `M>=1`, let `z in [0,3/4]`, `y1,y2 in [0,1]`, and define

\[
 f_M(y_1,y_2,z)=M(y_1+y_2-z)^2+(y_1-2z+1/2)^2.           \tag{8}
\]

The private Hessian is PD. Its unique optimal response and value are

| Parameter interval | `(y1,y2)` | `phi_M(z)` | Second derivative |
| --- | --- | --- | --- |
| `[0,1/4]` | `(0,z)` | `(1/2-2z)^2` | `8` |
| `[1/4,1/2]` | `(2z-1/2,1/2-z)` | `0` | `0` |
| `[1/2,3/4]` | `(((M+2)z-1/2)/(M+1),0)` | `M/(M+1)(z-1/2)^2` | `2M/(M+1)` |

These follow by direct stationarity and bound-gradient signs. In the
third interval the first response coordinate lies in `[1/2,1)` for all
`M>=1`; hence no omitted upper-bound region occurs. At both joins the
responses and first value derivatives agree. Because the response is
unique and its slope changes, no globally affine selector exists.
The direct retained Hessian entry is `2M+8`, whereas (6) is exactly `8`.

To obtain a growing nonconvex sparse family, take `m` such blocks, add
`v_i in [0,1]`, and put `a=1/5`, `eta=1/16`,

\[
 F=\sum_i\{z_i^2+f_M(y_{1i},y_{2i},z_i)-v_i^2+3v_i
                    -(z_i-a)v_i\}
   +\eta\sum_{i=1}^{m-1}[(z_{i+1}-z_i)^2+(v_{i+1}-v_i)^2].       \tag{9}
\]

The unique optimizer is `(z_i,v_i,y1_i,y2_i)=(a,0,0,a)` and
`F*=m/20`. To prove uniform growth, write
`t=z-a`, `u=y1`, `w=y2-a`, `r=u+w-t`, `s=u-2t`. Exact expansion gives

\[
 z^2+f_M-1/20=t^2+M r^2+s^2+u/5.                       \tag{10}
\]

Moreover `-v^2+3v-tv>=v^2`, because
`v(3-2v-t)>=0` for `v in [0,1]`, `t in [-1/5,11/20]`.
The elementary estimates

\[
 u^2\le2s^2+8t^2,\quad
 w^2\le3r^2+27t^2+6s^2
\]

yield `t^2+u^2+w^2<=36(t^2+M r^2+s^2)` for `M>=1`.
All path penalties are nonnegative and vanish at the stated optimizer.
Thus full-vector growth holds with `g=1/36`, independently of `M,m`.

Before adding PSD square and path terms, each `(z_i,v_i)` Hessian is
`[[2,-1],[-1,-2]]`, bounded below by `-sqrt(5) I`; the private rows
are initially zero. Hence the full negative curvature `nu<=sqrt(5)`.
The `v` principal subspace has Hessian `-2I+2eta L_path` and is negative
definite, so there are at least `m` negative eigenvalues. On `v=0` the
remaining Hessian is PSD; the dimension argument gives at most `m`.
Thus negative inertia is exactly `m` and `nu>=2` by the constant-`v`
direction. Each residual ladder has bags of size at most four. Equation
(7) gives `L<=10+4eta=41/4`, uniformly in `M,m`, while the original
retained diagonal grows as `2M+10`. There are just three certified pieces
per private block; their global overlay has `3^m` nonempty cells.

This is a strict extension of globally affine condensation and the
direct-curvature value-factor theorem: neither provides the same uniform
curvature bound on this fixed supplied partition. Other algorithms can
exploit this particular family's explicit nonnegative identity (10);
the example does not establish practical hardness or solver superiority.

## 6. Sources and verification scope

Affine optimizers on critical regions and piecewise-affine parametric-QP
solutions are classical. See Bemporad, Morari, Dua, and Pistikopoulos,
*The explicit linear quadratic regulator for constrained systems*,
[Automatica 38 (2002), 3–20](https://doi.org/10.1016/S0005-1098(01)00174-1),
and the [authors' paper](https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp.pdf).
The statements here are proved directly for the narrower fixed-private-box
model and do not rely on generic active-set assumptions from that paper.
No publication-priority claim is made.

The accompanying scalar constructor and checker provide executable
evidence for the KKT/coverage/curvature interface and the separating
family. JSON-safe piece serialization uses exact integer or fraction
strings, rejects approximate coefficients, and does not replace KKT
verification. Constructor and verifier support cooperative budget
callbacks. The scalar factor interface is integrated in the convex
recourse engine; that engine's own tests cover its solver integration.
The general BSP sparse complexity theorem remains a proof-level
composition beyond this implemented scalar special case. No
project-wide verification or CI inspection was run for this work.
