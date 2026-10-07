# A pullback extension to overlapping polynomial graph constraints

Date: 2026-10-02. Status: derivation, targeted checks, and fresh independent
review complete.
This is a corollary of the expected exact sparse polynomial box theorem,
not a new algorithm for general coupled constraints. No priority claim is
made.

Some coupled polynomial equalities can be handled by a global, sparse
parameterization. The useful case retains independently perturbed free
coordinates as ambient coordinates. Conditioning on the other perturbations
then leaves exactly the product noise required by the box theorem. The
equalities may overlap throughout a connected graph; they need not separate
into disjoint blocks.

Two restrictions are essential to this argument. Curvature must be bounded
after substitution, and a bounded inverse alone does not preserve the
conditional noise law. Section 5 gives exact examples of both failures.

## 1. Model and corollary

Let `t in T` be a product of rational continuous intervals and bounded native
integer intervals. These are retained ambient coordinates, called the free
coordinates. Remove fixed free coordinates and suppose `m>=1` remain. Write
`w_i` for their widths and `w_max=max_i w_i`.

Additional continuous coordinates are determined by a polynomial acyclic
graph:

\[
 z_j=P_j(t,z_{<j}),\qquad j=1,\ldots,q.
 \tag{1}
\]

Each defining polynomial has degree at most a fixed `e>=1`, has at most `k`
parents, and the longest dependency path has length at most a fixed `D`.
Every dependency starts at a free coordinate. An output with no parents is
a constant and may be substituted directly. There are no additional
constraints on `t` or `z`; any displayed output bounds must be redundant.
In particular, restricting an output to an arbitrary interval is not covered.

Let `F_0(t,z)` be a sum of explicit rational polynomial factors of fixed
degree at most `d>=1`. Supply a tree decomposition of bag size at most `p`
containing every objective factor scope and every equality scope in (1).
The rational input length `I` includes this decomposition and `sigma>0`.

Substitution gives explicit polynomials `z_j=Psi_j(t)`. Their degree is at
most `E=e^D`, and each involves at most `a=max{1,k^D}` free coordinates.
The map `Phi(t)=(t,Psi(t))` is globally injective; its inverse on the
feasible set is coordinate projection. The substitution can be performed
in `poly_{d,e,D}(I)` bit work: all resulting degrees are fixed, so the number
of possible monomials in `m` variables is polynomial in `I`.

For a deterministic auxiliary coefficient vector `eta in [-sigma,sigma]^q`,
define

\[
 G_\eta(t)=F_0(t,\Psi(t))+\sum_j\eta_j\Psi_j(t).
 \tag{2}
\]

Supply a rational `L'>0` with

\[
 \partial_{ii}G_\eta(t)\le L'
 \quad\text{for every }t\text{ in the continuous hull of }T,
 \quad |\eta_j|\le\sigma,
 \quad i=1,\ldots,m.
 \tag{3}
\]

As in the box theorem, either treat (3) as a valid input premise or derive
it by rational termwise monomial bounds. A sharper independently verified
bound may be supplied, with its proof length and verification cost included
in `I`. Include `L'` in `I`.

There is a base-computed power of two `M`, with
`log M=poly_{d,e,D}(I)`, such that independently drawing every ambient linear
coefficient from the same `M` equally spaced points of `[-sigma,sigma]`
admits an exact optimizer of

\[
 F_0(t,z)+\gamma^Tt+\eta^Tz
 \quad\text{subject to }t\in T\text{ and (1)}
 \tag{4}
\]

on every draw. If `p'` is the maximum bag size after the expansion below,
then `p'<=ap`, and expected bit work is

\[
 C_0^{p'}
 \left[4+(1+m/2)\frac{L'w_{\max}}{2\sigma}\right]^{p'}
 \operatorname{poly}_{d,e,D}(I).
 \tag{5}
\]

The exact output and arbitrary-precision evaluation contracts are inherited
from the [sparse polynomial box theorem](smoothed-sparse-polynomial.md).
The usual output is the unique minimizer of a rational strongly convex
patch in the free coordinates, followed by `z=Psi(t)`. Exceptional draws
use the same-draw exact algebraic fallback. This is an expected polynomial
bound for fixed `p'` under polynomial numerical width/noise bounds, not an
FPT claim in `p'`.

## 2. Substitution preserves a bounded-width decomposition

For a free coordinate `t_i`, let `Lambda(t_i)={i}`. For a dependent
coordinate `z_j`, let `Lambda(z_j)` be all of its free ancestors, whether
or not a polynomial cancellation later removes a dependence. Replace each
original bag `B` by

\[
                         B'=\bigcup_{v\in B}\Lambda(v).
 \tag{6}
\]

Every substituted objective factor and every term `eta_j Psi_j` has its
scope in one expanded bag. The latter assertion uses a bag containing
the defining equality of `z_j`, hence `z_j` itself.

For running intersection, fix a free coordinate `t_i`. The expanded bags
containing it form the union of the original occurrence subtrees of `t_i`
and all its dependent descendants. Every parent-child pair along a
dependency path occurs together in a constraint bag. Their occurrence
subtrees therefore intersect. The union is connected, because every such
descendant has a path back to `t_i`. Thus (6) is a valid tree decomposition.
Its bag size is at most `a p`; duplicate free coordinates are counted once.

This argument requires the decomposition to include the equality scopes.
An objective-only decomposition does not by itself justify the bound.

## 3. One finite noise law, chosen before every draw

It is not sufficient to sample `eta` and then apply the box theorem using
`G_eta` as a fresh base instance: doing so could choose the noise precision
after seeing part of the draw. Instead choose common constants for the
entire bounded polynomial family (2).

First, derive uniform rational first-, second-, and third-derivative bounds
on the free box with `|eta_j|<=sigma`. Their encoding lengths are polynomial
in `I`, and their magnitudes enter the cutoff only through polynomially
many precision bits, except for the explicit `L'` in (5).

The [finite polynomial noise-tail theorem](polynomial-finite-noise-tails.md)
gives a common scalar-section constant directly. Its formula
`C=2[(s_0 d_0)^{a_0(m+1)^2}]^3+1` depends only on free dimension, mixed-box
atom count, and composed degree, where `a_0` is its fixed elimination
constant. Each fixed `eta` is merely a vector of real polynomial
coefficients. The section bound is explicitly independent of those
coefficients and their heights. Thus the same `C` works for every `eta`,
without adding auxiliary parameters to the quantified variables.

The active-gradient root bound also depends only on free dimension,
integer label count, and composed degree. Use, for example,

\[
 K=\max\{1,m_c3^{m_c}R_Z\max(1,dE-1)^{m_c}\},
 \tag{7}
\]

where `m_c` is the number of continuous free coordinates and `R_Z` the
number of free integer assignments.

Finally the [exact fallback construction](polynomial-exact-fallback-construction.md)
separates degree/format costs from coefficient-height costs. Uniformly in
`eta` sampled with `b=log_2 M` bits, its work and precision evaluation
cost have the form

\[
                    B(I+b+q_{\rm eval}+1)^c,
 \qquad B=2^{\operatorname{poly}_{d,e,D}(I)},
 \tag{8}
\]

with fixed exponent `c`. Here `q_eval` is requested evaluation precision,
not the number of outputs. The composed coefficients are affine in `eta`.
All auxiliary sampled coefficients share denominator `M-1`, up to the
base denominator of `sigma`; hence their contribution to coefficient
length is polynomial in `I+b`. No exponential function of the new sampling
bits is hidden in `B`. Choose a single base bound `B` large enough for the
whole polynomial family and both fallback tasks.

With `W=sum_i w_i`, choose

\[
 \rho=(4B)^{-1},\qquad
 g_0=\rho\sigma/(2W),\qquad
 \tau=\rho\sigma/(2K).
 \tag{9}
\]

Choose the uniform cutoff level `J` by the box theorem's localization and
patch inequalities using these constants and the uniform derivative
bounds. Then choose the least power of two satisfying

\[
                M\ge\max\{2,2^J,4mC/\rho,2K/\rho\}.
 \tag{10}
\]

All of this precedes sampling both `gamma` and `eta`.

Conditional on any complete auxiliary draw `eta`, the free coefficients
`gamma_i` remain independent uniforms on this same grid. The conditional
bag value function is formed on the unchanged product free domain, and
its coordinate semiconcavity follows from (3). Therefore the cell-count
proof, tail bounds, and patch stopping argument apply with common
constants. The conditional fallback probability is at most `1/(2B)`.
Averaging over `eta` proves (5), and bounds the expected fallback work and
output size. There is no resampling and no conditioning on a good-growth
event.

## 4. Exact constrained output and a connected nonlinear example

On a usual draw the box algorithm fixes integer free coordinates and active
continuous free bounds, and returns a rational box `C` on the others with
a verified positive Hessian modulus for `G_eta+gamma^Tt`. Its box KKT system
has exactly one primal solution `t*`. Add the polynomial equations (1) to
specify the ambient optimizer `Phi(t*)` exactly. This produces an exact
constrained patch even when the ambient objective is nonconvex and the
feasible graph is nonlinear.

For a one-layer graph `z_j=P_j(t)`, the equality multiplier in the original
Lagrangian is `lambda_j=-partial_{z_j}F_gamma`. Substituting it into the
`t` stationarity equations gives the gradient of the pulled-back objective.
Thus the patch KKT equations agree with constrained stationarity, while
their uniqueness comes from the verified reduced Hessian. For a deeper
acyclic graph, the same statement follows by reverse substitution and the
chain rule. No positive ambient Hessian is required.

Polynomial evaluation of `Psi(t*)` supplies ambient coordinates to any
requested precision. Bounds on its derivatives have polynomial encoding
length, so choosing the extra free-coordinate precision costs only
polynomially many bits. A rational feasible free-coordinate approximation
`t_hat` maps to the rational point `(t_hat,Psi(t_hat))`, which satisfies
every graph equality exactly. Compute the output coordinates by polynomial
evaluation rather than rounding them independently. The free objective-gap
certificate is unchanged by this map. The rare branch returns the same
exact algebraic output type as the box fallback and applies the same
polynomial map.

For a concrete connected family, let `t_i in [0,1]`, allowing some free
coordinates to be binary, and impose

\[
 z_i=t_it_{i+1}\quad(i=1,\ldots,m-1),\qquad
 F_0(t,z)=\sum_{i=1}^{m-1}(z_i-a_i)^2+\lambda\sum_{i=1}^m t_i^2,
 \qquad\lambda\ge0.
 \tag{11}
\]

The constraint graph is a connected chain of triangles with bags
`{t_i,t_{i+1},z_i}`. The substituted objective has degree four and path
bags `{t_i,t_{i+1}}`. Each interior free coordinate contributes at most
four to its own second derivative from the two adjacent squared products,
so `L'=4+2lambda` is valid, independently of the chain length and the
numbers `a_i`. The auxiliary perturbation term
`sum_i eta_i t_i t_{i+1}` has zero pure coordinate second derivative and
does not increase this bound. All ambient coordinates can receive the same
independent finite perturbation law. The constraints overlap along the
entire chain; they are not a product of disjoint low-dimensional blocks.

## 5. What the parameterization assumptions do not give

A bounded local inverse does not preserve the conditional noise lemma.
Consider the linear map

\[
 (x_1,x_2)=\Phi(t_1,t_2)=(t_1+t_2,t_1+2t_2),\qquad t\in[0,1]^2.
 \tag{12}
\]

It has determinant one and inverse infinity-norm at most three. Its image
is the coupled parallelogram
`0<=2x_1-x_2<=1`, `0<=x_2-x_1<=1`. Independent ambient coefficients
`gamma_1,gamma_2` pull back to

\[
                      c_1=\gamma_1+\gamma_2,
 \qquad c_2=\gamma_1+2\gamma_2.
\]

For the finite endpoint-inclusive noise law, conditioning on the outside
coefficient `c_2=3sigma` forces both original coefficients to equal `sigma`.
Thus `c_1=2sigma` is conditionally deterministic. A singleton interval has
conditional probability one, rather than the `1/M` atomic term required
for an independent uniform coefficient. Under continuous noise, nearby
outside values leave arbitrarily thin conditional support. This disproves
the unchanged conditional-count argument, not the possibility of a
different algorithm for the parallelogram.

Nor does a bounded inverse preserve the original coordinate-curvature
parameter. Under the equality `z=t`, the ambient polynomial

\[
                  F_0(t,z)=Htz+\varepsilon(t^2+z^2)
\]

has both ambient diagonal second derivatives equal to `2epsilon`, but its
pullback is `(H+2epsilon)t^2`, with second derivative `2H+4epsilon`.
The graph and inverse are linear, local, and uniformly well conditioned.
An arbitrarily large ambient cross derivative still becomes free-coordinate
curvature. Formula (5) therefore uses `L'` from (3), not an unqualified
ambient diagonal bound.

The positive result is a sparse global-parameterization corollary. It does
not cover arbitrary order constraints, TU systems, inequalities cutting
the graph, or implicit algebraic inverse charts. Those classes need a
different feasible rounding, conditional-noise, or exact-arithmetic argument.

## 6. Targeted verification

The author ran
`python research-20261002/new-direction/check_polynomial_graph_constraints.py`.
The [exact diagnostic](check_polynomial_graph_constraints.py) passed 1,125
coupled quartic rounding and uniform-curvature cases, checked running
intersection after substitution in an overlapping depth-two graph, and
checked the conditional-noise obstruction on three finite laws. It also
checks the independent-anchor escape and the ambient-curvature obstruction.
These fixtures do not implement the finite-law budget, exact fallback,
or convex-patch evaluator; those are inherited proof interfaces. No
project-wide verification or CI inspection was performed. The
[independent actual-file review](../reviews/smoothed-polynomial-graph-review.md)
approved the stated parameterization corollary, including the common
pre-draw noise law and coefficient-height separation. The reviewer read
the diagnostic and separately ran
`python3 research-20261002/new-direction/check_polynomial_graph_constraints.py`
with the same passing results.
