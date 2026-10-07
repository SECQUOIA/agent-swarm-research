# Audit of stable nonlinear dynamics and rational output

## Conclusion and required qualification

The stable scalar-dynamics theorem and the fixed-degree rational-polynomial
extension are sound under the stated structural promises. I found no fatal
flaw in the graph strips, forward repair, adjoint cancellation, contraction
constants, local LP implementation, rational-center resetting, or compressed
feasible output. The arguments below give complete proofs of the points that
need to remain explicit in the manuscript.

One claim requires qualification when the results are combined. The sharp
final leaf-plus-cell count applies to a run with a fixed sufficient grading
ratio. The unknown-growth bit-budget search may return a successful run with
an insufficient ratio and a final stage not bounded by the sufficient run's
analytical stopping stage. Its runtime and serialized output are still
polynomially bounded by the search budget. The sharp
`O(T log(T/epsilon))` final box count does not automatically apply to that
winning output. State the fixed-ratio box counts and the unknown-growth
polynomial runtime/output guarantee separately. This is a reporting repair;
no change to the sound stopping rule is needed.

The theorem must also retain its exact feasibility contract. The forward
repair preserves every choice of initial state and continuous controls only
because the entire input rectangle of each dynamics map is sent into the
next prescribed state interval. Additional state, endpoint, terminal, or
coupled control constraints are outside this contract unless a separate
repair-invariance proof is supplied.

Sources read in full:

- [Manuscript brief](BRIEF.md).
- [Stable nonlinear dynamics](../../research-20261002/new-direction/nonlinear-dynamics.md).
- [Rational certificates and compressed trajectories](../../research-20261002/new-direction/nonlinear-dynamics-bit.md).
- [Regridding theorem](../../research-20261002/regridded-certificates/note.md).
- [Certified inexact oracles](../../research-20261002/regridded-certificates/inexact-oracles.md).
- [Repository instructions](../../AGENTS.md).

## 1. Exact assumptions and output contracts

Use `S>0` for the largest interval width in the manuscript. This avoids the
source notes' collision between the width constant `s0` and the initial-state
variable `s_0`.

There are states `s_0,...,s_T` and continuous controls
`u_0,...,u_{T-1}`, with `T>=1`. Their domain `X` is a product of compact
nondegenerate intervals `I_t` and `U_t`. The feasible set is exactly

\[
 P=\{x\in X:s_{t+1}=\phi_t(s_t,u_t),\quad 0\le t<T\}.
\]

Each map is continuously differentiable on a neighborhood of its rectangle,
and the following bounds hold on the full rectangle:

\[
 \phi_t(I_t\times U_t)\subseteq I_{t+1},\qquad
 |\partial_s\phi_t|\le a<1,\qquad
 |\partial_u\phi_t|\le b,\qquad
 \operatorname{Lip}(\nabla\phi_t)\le H.
\]

All constants are nonnegative; `a<1`. Norms in the gradient-Lipschitz
conditions are Euclidean. The objectives are bag functions
`a_t(s_t,u_t,s_{t+1})`, with `F=sum_t a_t` and
`Lip(grad a_t)<=M` on their full bag boxes. Every leaf `B` has a supplied
continuous convex model `underline a_{t,B}` satisfying

\[
 0\le a_t(z)-\underline a_{t,B}(z)\le A_0\operatorname{width}(B)^2/4
 \quad(z\in B).
\]

Endpoint or vertex exactness is not required. The proof uses validity and
this uniform error bound. In particular, the affine Taylor model in the
rational implementation is admissible even though it is not vertex exact.

Assume there is `x* in P` and `g>0` such that

\[
 F(y)-F(x^*)\ge g\|y-x^*\|^2\quad(y\in P).
\]

This is feasible-set quadratic growth. It implies uniqueness of the
minimizer. It need not hold at infeasible points and does not follow from
stability alone. Boundary minimizers are allowed; no stationarity condition
is required.

For the exact-real algorithm, bound the global dependent-state derivatives
at its feasible centers by `|partial_{s_j}F(c)|<=G`, `1<=j<=T`.
For the rounded-center algorithm, this bound must hold at all ambient-box
centers. A full-box bound `G_b` on every bag-gradient component gives
`G=2G_b`. A feasible-center bound can also be extended: comparing to any
feasible trajectory and using at most two incident bags gives the ambient
bound `G_feas+2M sqrt(3) S`. A conservative rational upper bound suffices.

The path has bags `V_t={s_t,u_t,s_{t+1}}` and separators
`S_t={s_t}` for `1<=t<T`, rooted at bag zero. We may uniformly use
`N=T`, `p=3`, and `k=2`, including `T=1`. The actual separator dimension
is one; the source's factor `3^w` with `w=2` is a valid conservative bound.

The exact-real result outputs a valid lower certificate and a feasible
incumbent with gap at most `epsilon`. It counts exact local convex
optimization, function evaluation, gradient evaluation, and feasible
recurrence representation as oracle operations. It does not establish the
bit complexity of those oracles or of expanded trajectory coordinates.

The bit result additionally assumes rational endpoints, rational polynomial
maps and costs of fixed numerical degree and fixed arity, rational valid
derivative bounds, and rational `epsilon>0`. Its output consists of:

- Rational initial state and rational controls in their exact intervals.
- The original recurrence, defining the exact feasible trajectory from those
  inputs.
- A rational lower certificate and rational feasible-objective upper bound
  with gap at most `epsilon`.

The recurrence is the feasible-solution representation. Outputting every
state as an expanded reduced rational is excluded. Certified finite-precision
state enclosures may be generated separately. A checker either trusts the
supplied global bounds and invariance promise or receives a separate proof
of them; the local LP certificate is not itself a proof of those promises.

## 2. Bounds used for soundness versus bounds used for rates

The distinction depends on the implementation.

| Data or promise | Exact-real algorithm with supplied valid lower models | Rational Taylor-LP/enclosure algorithm |
|---|---|---|
| Box invariance | Required for feasibility of the forward-repaired incumbent | Required for compressed exact feasibility and safe enclosure intersection |
| Graph curvature `H` | Required for graph-strip containment | Required for the rational graph strips |
| Objective-model validity | Required for every lower certificate | Obtained from the valid supplied curvature bound `M` |
| Objective curvature `M` and model error `A_0` | Used in rate analysis once model validity is supplied independently | `M` is also used to construct sound Taylor lower models |
| State contraction bound `a` | Used in repair-error and termination estimates; exact forward simulation itself does not use its numerical value | Also required for sound forward enclosures |
| Control derivative bound `b` | Used in the residual/drift rate estimate | Used in the rate estimate |
| Dependent-state derivative bound `G` | Used to bound exact multipliers and the rate constants | Used in the rate; `G_b` is also required for the objective upper enclosure |
| Growth `g>0` | Required for termination/rate, not for validity of an individual stage | Required for termination/rate, not used by unknown-growth trials |
| Grading smallness conditions | Required for the proved contraction, not for certificate validity | Same |

Thus a grading search may leave `g` and rate constants unknown. It cannot
repair underestimated graph curvature, invalid objective lower models,
invalid enclosure contraction, or failure of invariance. In the rational
algorithm the soundness-critical bounds `M,H,a,G_b` are supplied or
conservatively derived from the polynomial data as appropriate, rather than
guessed from successful stopping tests.

## 3. Graph strips and exact feasible repair

Let `B` be a leaf of width `w`, and let `m` be the midpoint of its two
input-coordinate intervals. Define

\[
 \ell(s,u)=\phi_t(m)+\nabla\phi_t(m)^T((s,u)-m),\qquad
 \tau=Hw^2/4,
\]

\[
 O_t(B)=\{z\in B:|z_{s_{t+1}}-\ell(z_s,z_u)|\le\tau\}.
\]

Since the two input deviations are each at most `w/2`, Taylor's integral
remainder gives

\[
 |\phi_t(s,u)-\ell(s,u)|\le(H/2)\|(s,u)-m\|^2\le Hw^2/4.
\]

Every true graph point in `B` therefore lies in `O_t(B)`. Every strip point
satisfies, with `q_t=s_{t+1}-phi_t(s_t,u_t)` and `K=H/2`,

\[
 |q_t(z)|\le |z_{s_{t+1}}-\ell(z_s,z_u)|
                 +|\ell(z_s,z_u)-\phi_t(z_s,z_u)|\le Kw^2.
\]

The strip is a compact polytope, possibly empty. Leaf strips need not agree
on common faces: containment of true graph points on each closed leaf is
the property used by the lower-bound induction. If `H=0`, the strip is the
exact affine graph; the proof permits its lower-dimensional domain.

Define `y=R(x)` by preserving `s_0` and all controls and recursively setting
`y_{s_{t+1}}=phi_t(y_{s_t},x_{u_t})`. Invariance proves by induction that
every generated state belongs to its prescribed interval. Hence `R:X->P`
and `R(y)=y` for `y in P`.

Let `e_t=y_{s_t}-x_{s_t}` and `r_t=q_t(x_{V_t})`. Then

\[
 e_0=0,\qquad |e_{t+1}|\le a|e_t|+|r_t|.
\]

Writing the error vector as a sum of lag shifts of the residual magnitude
vector, each shift has Euclidean norm at most one. The triangle inequality
and geometric sum give

\[
 \|R(x)-x\|\le\frac{\|q(x)\|}{1-a}.
\]

This proof uses both `x_{s_t}` and the generated `y_{s_t}` in `I_t` when
applying the derivative bound. Invariance is therefore part of both the
feasibility proof and this repair estimate. No extra state-constraint
conclusion follows.

## 4. Adjoint cancellation at feasible and infeasible centers

At any center `c in X`, define

\[
 d_j=\partial_{s_j}F(c),\quad A_t=\partial_s\phi_t(c_{s_t},c_{u_t}),
\]

\[
 \mu_{T-1}=-d_T,\qquad \mu_{t-1}=A_t\mu_t-d_t\quad(T-1\ge t\ge1).
\]

At terminal state `s_T`, the derivative of
`G_c=F+sum_t mu_t q_t` is `d_T+mu_{T-1}=0`. At `s_j`,
`1<=j<T`, it is `d_j+mu_{j-1}-A_j mu_j=0`. Thus

\[
 \partial_{s_j}G_c(c)=0\quad(1\le j\le T).
\]

This algebra does not use `q(c)=0`. The center may be infeasible. Whenever
`|d_j|<=G`, backward induction gives

\[
 |\mu_t|\le G\sum_{r=0}^{T-1-t}a^r\le U:=G/(1-a).
\]

Write `A_t^c=a_t+mu_t q_t`. Since the gradient of `q_t` is
`(-partial_s phi_t,-partial_u phi_t,1)`, its Lipschitz constant is at most
`H`. Hence `Lip(grad A_t^c)<=Mbar:=M+UH`.

For `t>=1`, the state `s_t` occurs only in bag `t` within the subtree
rooted at that bag. Its separator slope is therefore

\[
 \lambda_t(c)=\partial_{s_t}a_t(c_{V_t})-\mu_t A_t.
\]

Every repair displacement `x-R(x)` has zero initial-state and control
coordinates. Consequently

\[
 \nabla G_c(c)^T(x-R(x))=0
\]

for every `x in X`. This is cancellation on the full dependent-coordinate
subspace, rather than on a tangent space. It neither requires a linear
repair nor differentiates the repair. This distinction is essential to the
nonlinear and rounded-center extensions.

At an infeasible center, an alternative Taylor construction of the full
multiplier-adjusted function would include the constant
`sum_t mu_t q_t(c)`. Dropping that constant would be an error. The audited
construction avoids it: it retains the original objective models and uses
adjusted gradients only to choose slopes.

## 5. Aggregate drift, telescoping, and complete error estimate

Consider a finite backtracked configuration with points
`z^t in O_t(B_t)`, own separator cells `D_t`, and the usual parent-leaf/
child-cell incidences. Let `x` take each coordinate from its top occurrence,
and let `y=R(x)`. Set

\[
 b_t=\operatorname{width}(B_t),\quad
 d_t=\operatorname{width}(D_t),\quad
 Q=\sum_t b_t^2+\sum_{t\ge1}d_t^2,
\]

\[
 E_x=\sum_t\|z^t-x_{V_t}\|^2,\qquad
 E_y=\sum_t\|z^t-y_{V_t}\|^2,\qquad C_0=k(k-1)p=6.
\]

The occurrence-subtree drift argument of the regridding theorem gives
`E_x<=C_0 Q`. On this path it can also be seen directly: the only mismatch
in bag `t>=1` is its input state, whose two copies differ by at most
`b_{t-1}+d_t`. Squaring and summing even gives the sharper `E_x<=2Q`;
the common constant `C_0=6` is valid and keeps the formulas uniform.

The full-box Lipschitz constant of `q_t` is at most
`L_q=sqrt(1+a^2+b^2)`. Since `b_t<=S`, the stacked residual vector obeys

\[
 \|q(x)\|\le L_q\sqrt{E_x}+K\sqrt{\sum_t b_t^4}
           \le(L_q\sqrt{C_0}+KS)\sqrt Q.
\]

Put

\[
 \rho=\frac{L_q\sqrt{C_0}+KS}{1-a},\qquad
 D=(\sqrt{C_0}+\sqrt{k}\rho)^2.
\]

Then `||y-x||<=rho sqrt(Q)`. Every global coordinate occurs in at most
`k` bags, so the triangle inequality on stacked bag vectors gives

\[
 \sqrt{E_y}\le\sqrt{E_x}+\sqrt{k}\|y-x\|\le\sqrt{DQ}.
\]

The term `KS` cannot be omitted: with one bag there is no copy mismatch,
but a strip point can still violate the nonlinear graph and require repair.

Let `Phi` be the configuration value with the original lower objective
models and adjusted separator slopes, and let
`err_t=a_t(z^t)-underline a_{t,B_t}(z^t)`. The subtree-gradient identity
gives

\[
 \Phi=\sum_t a_t(z^t)-\sum_t\operatorname{err}_t
          -\sum_t\nabla A_t^c(c_{V_t})^T(z^t-x_{V_t}).
\]

Adjoint cancellation permits replacing `x` by `y` in the final sum. Since
`q_t(y_{V_t})=0`, exact rearrangement yields

\[
 \Phi=F(y)+\sum_t T_t-\sum_t\operatorname{err}_t
                                  -\sum_t\mu_tq_t(z^t),
\]

\[
 T_t=A_t^c(z^t)-A_t^c(y_{V_t})
              -\nabla A_t^c(c_{V_t})^T(z^t-y_{V_t}).
\]

The multiplier residual is necessary because local copies satisfy strips,
rather than the nonlinear equalities. Its absolute value is at most
`UK sum_t b_t^2<=UKQ`.

The integral gradient remainder gives

\[
 |T_t|\le\overline M\|y_{V_t}-c_{V_t}\|\|z^t-y_{V_t}\|
                +(\overline M/2)\|z^t-y_{V_t}\|^2.
\]

With `r=||y-c||` and
`B_0=Mbar D/2+A_0/4+UK`, Cauchy--Schwarz therefore gives

\[
 |F(y)-\Phi|\le\overline M\sqrt{kD}\,r\sqrt Q+B_0Q.
\]

Shell grading at scale `h` and ratio `theta` implies, for each bag and
separator, a width bound by `h` plus `theta` times a center-distance term
and a local-copy error term. Summing the squared bounds gives

\[
 Q\le6Nh^2+3(2k-1)\theta^2r^2+6\theta^2E_y.
\]

The bag-plus-separator center-distance sum is bounded by
`(2k-1)r^2`. The corresponding copy-error sum is at most `2E_y`.
Equality of these copy-error sums, valid before repair in the unconstrained
case, is not required after repair because private top-bag states may move.
If `12D theta^2<=1`, absorption gives

\[
 Q\le12Nh^2+12k\theta^2r^2.
\]

Choose a dyadic `theta<=1/2` with `eta=g/20` and

\[
 12D\theta^2\le1,\qquad
 \sqrt{12}\,k\sqrt D\,\overline M\theta\le\eta/4,\qquad
 12kB_0\theta^2\le\eta/4.
\]

Substitution gives a mixed term
`sqrt(12kD) Mbar sqrt(N) h r`, whose Young bound is
`eta r^2/2+6kD Mbar^2 Nh^2/eta`. The other two `r^2` terms together are
at most `eta r^2/2`. Thus, with

\[
 C=12B_0+6kD\overline M^2/\eta,
\]

every configuration satisfies

\[
 |F(y)-\Phi|\le(g/20)\|y-c\|^2+CNh^2.
\]

All comparisons take place in full original bag boxes; the repaired point
need not lie in the selected leaf. Full-box gradient-Lipschitz assumptions
are therefore necessary. This proof also covers `T=1`, with no separators.

## 6. Lower-certificate validity, flags, and exact-center contraction

Every local convex inequality is imposed on
`O_t(B) intersect {z_{S_t} in D}`, with the root separator condition
omitted. Because these domains contain every true graph point on their
leaves, the usual bottom-up separator-minorant induction remains valid on
the true feasible set.

Empty domains and unavailable messages require explicit flags. A leaf is
unusable if all intersecting cells of some child are flagged; otherwise its
child intercept is the minimum over the unflagged intersecting cells. An
own state is flagged only if every incident leaf is unusable or has an
empty local domain. A true feasible subtree assignment cannot be flagged:
its own graph point belongs to its leaf strip and own cell, and its true
child state selects an intersecting unflagged child cell by induction.
Consequently every true trajectory induces an available consistent
configuration, and its value is no greater than its objective. The root
bound satisfies `LB<=F(x*)`, and a finite root configuration exists.
Infinite intercepts are never treated as finite affine minorants.

Continuous local convex models on compact nonempty domains attain their
minima. The exact oracle must return an attaining point and value, or a
certified empty-domain decision. Backtracking then yields a finite
configuration with `Phi=LB` and all local points in their strips.

For exact feasible centers `c=y_{j-1}`, let
`h_j=S 2^{-j}`, `e_j=||y_j-x*||^2`, and
`B=max{p,2C/g}`. Feasible growth, the preceding estimate, and
`LB_j<=F(x*)` give

\[
 ge_j\le(g/20)\|y_j-y_{j-1}\|^2+CNh_j^2
       \le(g/10)(e_j+e_{j-1})+CNh_j^2,
\]

\[
 e_j\le e_{j-1}/9+(10C/(9g))Nh_j^2.
\]

The initial error is at most `pNh_0^2`. For later stages,
`h_{j-1}=2h_j` and `B>=2C/g` close the induction
`e_j<=BNh_j^2`. The stage-zero bound also follows directly from
`B>=p` and `B>=2C/g`.

For `j>=1`, `||y_j-y_{j-1}||^2<=10BNh_j^2`; stage zero has the stronger
bound `4BNh_0^2`. Updating the incumbent with the feasible value `F(y_j)`
therefore gives

\[
 0\le\operatorname{UBD}-\operatorname{LB}_j
       \le(gB/2+C)Nh_j^2\le gBNh_j^2.
\]

The stopping test is valid for every ratio, while these estimates establish
termination for sufficient ratios by

\[
 J=\max\{0,\lceil\log_2(S\sqrt{gBN/\epsilon})\rceil\}.
\]

For `m=4/theta`, the final leaves plus cells number at most
`2N m^p(J+1)`, total created boxes at most
`N m^p(J+1)(J+2)`, and total local convex calls at most

\[
 N3^w m^p(J+1)(J+2)(2J+3)/6.
\]

The strip constraints do not change shell incidences. Empty local domains
remove feasible choices and still count as oracle calls. Touching leaf-cell
pairs must remain in the incidence lists. For uniformly bounded
`a,b,H,G,M,A_0,g,S`, with `1-a` and `g` uniformly positive, these bounds are
`O(T(1+log_+(T/epsilon)))`, its squared logarithm for created boxes, and
its cubed logarithm for local calls. They count geometric boxes and oracle
calls, not serialized proof bits. Each additional map, objective, and
gradient evaluation must be charged; an unbounded list of factors per bag
is not covered by a bag-count-only evaluation bound.

## 7. Certified inexact local work: what transfers and what does not

The lower-DP and backtracking-error arguments of the inexact-oracle note
apply on the strip polytope without alteration. If a local oracle returns
a certified lower value, an exactly feasible strip point, and objective gap
at most `d h_j^2`, then only one chosen local gap per bag is added during
backtracking:

\[
 0\le\widehat\Phi-\operatorname{LB}\le dNh_j^2.
\]

For approximate separator slopes, the same edge-copy inequality gives
`H_edge<=C_1Q`, with `C_1=2p max{k-1,1}`. If their aggregate error from
the exact adjusted reference slopes is at most `zeta sqrt(N) h_j`, then

\[
 |\widehat\Phi-\Phi|\le(\eta/4)\|y-c\|^2+K_sNh_j^2,
\]

\[
 K_s=\sqrt{12C_1}\zeta+12kC_1\zeta^2\theta^2/\eta.
\]

This follows by substituting the repaired-point grading bound into
`|widehat Phi-Phi|<=nu sqrt(C_1Q)` and applying Young's inequality.
For feasible centers and exact feasible forward repair, these budgets and
an objective upper error `omega Nh_j^2` give the same `1/7` contraction as
the inexact note, with the dynamics constant `C` substituted there:

\[
 K=C+K_s+d+\omega,\qquad B_{\rm in}=\max\{p,8K/(3g)\}.
\]

This observation does not license box clipping as a strip-feasibility
procedure. Clipping to coordinate intervals preserves a box intersection,
but may leave its affine strip. Exact local feasibility must be certified
on the full polytope. Nor does the unconstrained bag-gradient perturbation
bound by itself bound errors in nonlinear adjoints; an implementation using
approximate dynamics derivatives must separately establish the aggregate
adjusted-slope error above. The rational extension avoids both issues with
exact LPs and exact rational adjoints at reset centers.

Most importantly, the unconstrained reconstruction argument does not make a
rounded nonlinear trajectory exactly feasible. The rational extension
retains exact recurrence semantics and rounds only enclosures and the next
center, as proved below.

## 8. Rational affine LPs and all degenerate boundaries

At a leaf midpoint `m_B` in all `p=3` coordinates, define

\[
 \underline a_{t,B}(z)=a_t(m_B)+\nabla a_t(m_B)^T(z-m_B)
                                         -Mp\,w_B^2/8.
\]

Because `||z-m_B||^2<=p w_B^2/4`, the absolute Taylor remainder is at most
`Mp w_B^2/8`. Therefore

\[
 0\le a_t(z)-\underline a_{t,B}(z)\le Mp w_B^2/4,
\]

so `A_0=pM` is valid. Its coefficients and those of the graph strip are
rational at rational leaf midpoints. The adjusted slopes are rational at
rational centers.

Merge the leaf and own-separator coordinate bounds exactly. A nonempty
local domain then has at most six coordinate inequalities and two strip
inequalities. The objective is affine, including separator slopes; child
intercepts are constants. Thus each task is an LP with at most three
variables and eight inequalities.

Exact active-basis enumeration is sufficient, including lower-dimensional
domains. A nonempty bounded polyhedron has a vertex. At a vertex, the
active row normals span the entire ambient space: otherwise there is a
nonzero vector annihilating them, and sufficiently small positive and
negative displacements along that vector preserve all inactive inequalities
as well, contradicting extremality. Enumerating all independent triples of
rows, solving their rational systems, and testing all inequalities therefore
finds every possible vertex candidate. An affine minimum is attained at a
vertex. Finding no feasible candidate proves emptiness. There are at most
`binom(8,3)=56` triples.

One may instead eliminate coordinates whose intersected bounds are equal,
then enumerate independent bases in the remaining dimension. In dimension
zero, exactly test all constraints and evaluate the objective. These rules
cover touching separator faces, exact graph equalities when `H=0`, and
empty strips. Floating-point feasibility tolerances are unnecessary.
Fixed-coordinate elimination is convenient, but ambient active-basis
enumeration is already sound even on lower-dimensional domains.

Exact LP points give rational retained controls and initial state in their
intervals. They also provide the local feasible points needed for finite
backtracking. The implicit recurrence, rather than these potentially
inconsistent state copies, defines the feasible incumbent.

## 9. Forward enclosures, objective upper bounds, and center reset

Fix the rational initial state and controls of one incumbent. Define its
exact states by the original recurrence; invariance already proves
feasibility. Suppose a certified state interval lies in `I_t`, with rational
midpoint `m_t` and radius `r_t`. Its midpoint is in the domain on which
`|partial_s phi_t|<=a`, so exact rational evaluation gives the enclosure

\[
 [\phi_t(m_t,u_t)-ar_t,\ \phi_t(m_t,u_t)+ar_t].
\]

Round its endpoints outward on a dyadic mesh of size `q` and intersect it
with `I_{t+1}`. Both operations preserve containment. Each endpoint moves
by less than or equal to `q` during rounding, and intersection cannot
increase diameter. Hence

\[
 r_{t+1}\le ar_t+q,\qquad r_0=0,\qquad r_t\le q/(1-a).
\]

Intersection also ensures the next midpoint remains in the derivative-bound
domain. Natural polynomial interval arithmetic alone does not prove this
contraction rate because repeated occurrences of the state can inflate its
width.

Let `G_b` bound every cost-gradient component on full boxes. Put

\[
 \widetilde F=\sum_t a_t(m_t,u_t,m_{t+1}),\qquad
 W=G_b\sum_t(r_t+r_{t+1}),\qquad U=\widetilde F+W.
\]

Integrating each cost along the segment joining its midpoint tuple to the
true tuple gives `|F(y)-tilde F|<=W`. Thus

\[
 F(y)\le U\le F(y)+2W\le F(y)+4G_bNq/(1-a).
\]

Repeated appearances of one state cause no difficulty; the bound sums the
separate bag uncertainties and assumes no independence. For any fixed
rational `omega>0`, taking
`q<=omega(1-a)h_j^2/(4 max{1,G_b})` gives upper error at most
`omega Nh_j^2`.

The next center must reset every coordinate. Also impose
`q<=(1-a)h_{j+1}/4`, and round each state midpoint, exact rational initial
state, and exact rational control to a dyadic mesh at most `h_{j+1}/2`.
Clip each result to its exact interval. A state midpoint has error at most
`h_{j+1}/4`, and nearest-mesh rounding adds at most `h_{j+1}/4`; the
retained inputs have only the latter rounding error. Clipping to an interval
cannot increase distance from any point in that interval. The loose bound

\[
 \|c_{j+1}-y_j\|^2\le pNh_{j+1}^2
\]

therefore holds. The reset center can be infeasible; Section 4 proves why
this is harmless for cancellation.

Store the incumbent's retained rational inputs separately from its reset
center. An upper bound belongs to the trajectory defined by those exact
retained inputs. When updating the minimum upper bound, retain its matching
inputs. Rounded center inputs must not silently replace incumbent inputs.

Let `c_0` be the rational box midpoint and let `y_{-1}` be its implicit
forward repair for the proof. Since both are in `X`, the center-distance
bound holds at stage zero with `h_0=S`; no expanded reference trajectory is
needed. Put `e_j=||y_j-x*||^2`. The three-vector inequality gives

\[
 \|y_j-c_j\|^2\le3(e_j+e_{j-1}+pNh_j^2).
\]

The single-stage estimate remains valid at the ambient-box center, so
growth gives

\[
 e_j\le\frac3{17}e_{j-1}
           +\frac{20C/g+3p}{17}Nh_j^2.
\]

Define

\[
 B_{\rm round}=\max\{p,4(C+\omega)/g+3p/5\}.
\]

For `j>=1`, the induction closes because
`12B_round+20C/g+3p<=17B_round`. At stage zero, the initial error bound
`e_{-1}<=pNh_0^2` gives
`e_0<=(20C/g+6p)Nh_0^2/17<=B_round Nh_0^2`; the last inequality follows
from `B_round>=p` and `5B_round>=20C/g+3p`. Therefore
`e_j<=B_round Nh_j^2` at every stage.

For `j>=1`, the center distance is at most
`(15B_round+3p)Nh_j^2`; the same bound covers initialization. Adding the
upper-evaluation error gives

\[
 0\le\operatorname{UBD}-\operatorname{LB}_j
 \le[3gB_{\rm round}/4+3gp/20+C+\omega]Nh_j^2
 \le gB_{\rm round}Nh_j^2.
\]

Thus the fixed-ratio stopping bound follows with `B_round` substituted for
`B`. The contraction factor `3/17<1/4` is essential: it leaves enough
margin to halve `h_j` despite center reset.

## 10. Bit growth and the conditioned runtime claim

Let `I` be the binary input length, including rational bounds, interval
endpoints, and the encoded tolerance; alternatively charge the tolerance's
encoding length separately. Numerical polynomial degree and local dimension
are fixed. Let `theta=2^{-mu}`. Reset center coordinates have
`O(I+j)` bits because they are dyadic mesh points or clipped original
endpoints. Fresh shell endpoints have `O(I+j+mu)` bits. They do not retain
arbitrary denominators from prior LP points.

Write `B_j=O(I+j+mu+log(T+1))`. Fixed-degree, fixed-arity polynomial
values and derivatives at such points have `O(B_j)` bits. The adjoint step
`mu_{t-1}=A_t mu_t-d_t` multiplies the previous rational by a new
`O(B_j)`-bit rational and adds another such rational. Numerator and
denominator lengths therefore increase additively by `O(B_j)` per step,
yielding `O(TB_j)` bits. There is no repeated squaring of the preceding
multiplier.

Each local LP has fixed dimension and a constant number of rows. Cramer's
rule or rational elimination gives vertices and local affine contributions
of polynomial bit length; `O(TB_j)` is a conservative bound. In fact,
constraint coefficients do not depend on long adjoint values, so primal
vertices admit a sharper bound, but that improvement is unnecessary.

The message-size argument should be written explicitly. Once a minimizing
leaf, cell, and vertex are selected, a message equals its chosen local
affine contribution plus the selected child message. Expanding this
recurrence along the path yields a sum of at most `T` local contributions.
Taking a minimum selects a sum; it never adds all alternative sums or
multiplies child messages. The bit length of a rational sum is at most a
constant times the sum of its summands' bit lengths. Hence
`O(T^2B_j)` bits is a valid conservative message bound, independent of the
number of grid tasks. Exact comparisons have polynomial bit cost as well.

For enclosure generation, select `q` as the largest dyadic number satisfying
the prescribed accuracy and reset bounds, using rational comparisons.
Likewise select the largest reset mesh below its prescribed bound. This
rules out arbitrary overprecision. The required precision satisfies

\[
 \log_+(1/q)=O\bigl(I+j+\log(1+G_b)+\log(1/(1-a))
                                      +\log(1+1/\omega)\bigr).
\]

Each exact polynomial evaluation may temporarily involve the retained LP
input denominators, but its fixed degree keeps that bit cost polynomial.
Outward rounding removes the newly formed state denominator before the
next step. Endpoints remain at the prescribed dyadic/input precision;
objective sums have polynomial bit length.

Consequently a sufficient fixed-ratio run uses bit work bounded by

\[
 N(4/\theta)^3(J+1)^3\operatorname{poly}(T,I,J,\mu).
\]

All grid construction, incidence generation, gradients, exact LP basis
solves, adjoints, message comparisons, enclosures, resets, and output must
be charged. This is polynomial in numerical conditioning parameters, not
uniformly polynomial in their binary encoding lengths. In particular,
the first sufficient dyadic reciprocal ratio is polynomially bounded by
the displayed numerical constants and their inverse growth/stability
margins. For an arbitrary excessively small sufficient ratio, retain the
explicit `theta` dependence in the work bound; polynomial conditioning
alone does not bound that run's chosen overrefinement.

No algebraic arithmetic is necessary for choosing a sufficient ratio when
a rational growth lower bound is supplied. Use the rational majorants

\[
 \overline L_q=1+a+b,\qquad
 \overline\rho=\frac{3(1+a+b)+(H/2)S}{1-a},\qquad
 \overline D=(3+2\overline\rho)^2,
\]

which dominate `L_q,rho,D`. The grading inequalities can be tested with
rational arithmetic, squaring their nonnegative sides when needed, and
halving a dyadic ratio until they hold. The analytical `J` can likewise be
bounded by rational comparisons against `gB_round NS^2 4^{-J}`.

The expanded-state obstruction is real even under contraction. For
`phi(s)=s^2/4` on `[0,1]` and initial state `1/2`,

\[
 s_t=2^{-(3\cdot2^t-2)}.
\]

The derivative bound is `1/2`, but the reduced denominator requires
exponentially many bits. The recurrence and seed have a short description;
the polynomial enclosure argument does not expand that denominator.

A complete serialized lower proof may include a local check for each
touching leaf-cell pair, as well as intercepts, flags, coordinates, and
their numeric entries. At the final stage there are
`O(N3^w m^p(J+1)^2)` local pairs, compared with
`O(Nm^p(J+1))` boxes. The polynomial work bound covers this serialization;
the bare leaf-plus-cell count does not bound proof bits.

## 11. Unknown growth: complete budget proof and count caveat

Each trial uses `theta=2^{-mu}`, the same input-sized rational initial
center, rational Taylor LPs, exact adjoints, prescribed enclosures, and
complete center reset. None of these operations needs `g`, the analytical
constant `C`, `B_round`, or `J`. Each trial stops only on its computed
sound gap.

At round `r`, restart all trials `1<=mu<=r`, each with a budget `2^r` of
elementary bit-level machine steps. Setup, counters, arithmetic, grids,
control logic, and output are inside the budget. A time-bounded execution
may interrupt an arithmetic routine; stopping only between arbitrarily
expensive rational operations would not establish this bit bound.

Let `mu*` be any sufficient index, and let `W*>=1` bound its successful
unbudgeted bit work. Set

\[
 r^*=\max\{1,\mu^*,\lceil\log_2W^*\rceil\}.
\]

Unless an earlier trial has already produced a valid answer, this round
finishes trial `mu*`. Further,

\[
 \sum_{r=1}^{r^*}r2^r\le2r^*2^{r^*}
              \le4r^*\max\{2^{\mu^*},W^*,2\}.
\]

The sufficient-ratio inequalities bound `2^{mu*}` polynomially in numerical
conditioning parameters, and Section 10 bounds `W*` polynomially in those
parameters, horizon, input length, and accuracy. Counters and simulation
add at most logarithmic/polynomial logarithmic overhead. This proves
polynomial unknown-growth bit complexity without guessing any
soundness-critical bound.

However, the winning trial can use a coarser ratio and a stage `j_win`
that has no proved comparison to the sufficient trial's `J`. It is safe to
state the structural box count at its actual parameters
`2N(4/theta_win)^p(j_win+1)`, and to bound its complete output by the
global bit budget. It is not justified to substitute the sufficient
trial's `J` into that winning trial's count. The simplest manuscript repair
is to reserve the sharp horizon/logarithm box count for sufficient
fixed-ratio runs and give the unknown-growth search its polynomial
runtime/output guarantee. The unknown-constant search's overhead is a
search-work statement, rather than preservation of every sharp individual
run count.

## 12. Example and manuscript organization

The source example
`phi(s,u)=s/4+u/2+s^2/8` on `[-1,1]^2` is consistent with its claims.
The image is `[-5/8,7/8]`, state derivative lies in `[0,1/2]`, and
`H=1/4`. Its objective
`s_0^2+sum_t(s_{t+1}^2+u_t^2-u_t^4/4)` is at least
`3||x||^2/4` on the entire box. Thus the zero trajectory is its unique
feasible minimizer with `g=3/4`; `G=2`, `M=2`, and the source's
multiplier/drift constants follow. The quartic convexifier with parameter
`1/2` gives `A_0=1/2`. Varying only the final control leaves a feasible
curve with second derivative `5/2-3v^2`, negative at `v=15/16`.
It is a valid nonconvex example with horizon-uniform constants, rather than
evidence that the promises hold for general stable control problems.

Recommended manuscript structure:

1. Present the general constructive regridding theorem and certified
   inexact-oracle contract first, including geometric versus serialized
   certificate size.
2. Give the scalar stable-dynamics theorem as a constrained extension,
   with explicit full-rectangle invariance and no additional constraints.
   Prove graph strips, dependent-coordinate adjoint cancellation, repair
   drift, and the multiplier-residual configuration identity before quoting
   the general aggregate-contraction algebra.
3. State the fixed-degree rational-polynomial result with its compressed
   output contract. Prove exact local LP feasibility, contraction-aware
   enclosures, complete center reset, and additive bit growth. Do not imply
   that the unconstrained rational-clipping lemma preserves nonlinear
   equality feasibility.
4. State unknown-growth search separately, with its bit-budget bound and
   the final-count qualification above. A brief soundness/rate distinction
   prevents the reader from treating `H`, `M`, or enclosure promises as
   parameters that can safely be guessed.
5. Keep the uniform nonlinear example short. Explain the limits once:
   continuous controls, exact box invariance, feasible quadratic growth,
   supplied bounds, and compressed rather than expanded trajectory output.

The first-order cancellation and strip residual are the mathematical bridge
to the main certificate theorem; the LP/enclosure/reset proof is the bridge
to the Turing model. These are sufficient for a coherent paper without a
general nonlinear-constraint or state-constrained-control claim.

## 13. Verification performed for this audit

This audit used complete source reads and independent algebraic derivations.
A delegated read-only review independently checked exact LP degeneracies,
adjoint and message denominator growth, enclosure propagation, all-coordinate
reset, rounded-center constants, compressed trajectory feasibility, and
unknown-growth budgeting. It agreed with the proof and the final-count
qualification above.

Read commands actually run were `pwd`, targeted `rg --files`, `wc -l`, and
`cat` on the listed source files. This report is
`paper-separator-certificates/evidence/AUDIT-DYNAMICS.md`. A subsequent
authoring assignment produced `sections/dynamics.tex` and
`sections/dynamics-bit.tex`; their proofs follow this report, use states
`sigma_t` to preserve the manuscript's width notation `s_0`, and explicitly
qualify mesh and grading-ratio selection as described above.

The targeted typesetting invocation actually run was
`pdflatex -halt-on-error -interaction=nonstopmode -output-directory
/tmp/separator-dynamics-check-y94s8qva
/tmp/separator-dynamics-check-y94s8qva/dynamics-check.tex`, twice, through
an inline Python driver. The temporary harness included only the two authored
sections and their model, regridding, and limitations dependencies. Both
final passes exited successfully and produced a 28-page PDF with no overfull
box diagnostics. An initial dependency failure identified a `split`
environment with multiple alignment pairs in the regridding constants;
that file's author corrected it before the successful passes.

The same targeted inline Python driver checked both authored sections and
this report for control characters and trailing whitespace; all checks
passed. It checked the authored sections' references against the manuscript
labels and the report's local Markdown links against existing files; none
were missing. No computational
experiments were rerun, no literature discovery or knowledge-base writes
were performed, and no project-wide verification or CI inspection was used.
