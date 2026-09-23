# Investigation: beyond quadratic integer precision

Date: 2026-09-05. The resulting [smooth-map theorem](../results/smooth-map-local-rank-integer-complexity.md) has passed the two proof audits linked there. This note records the reasoning boundaries and source search; the general gap between its two rank invariants remains unresolved.

## What transfers and what does not

A direct Taylor perturbation of the quadratic covariance determinant
proof is unsafe. A bound of the form `eta ||x-y||²` for the Hessian
variation can dominate the determinant term on sets with a large aspect
ratio. Small Euclidean neighborhoods alone do not fix this issue.

The useful replacement is an oscillatory-integral bound. If a contact
set has small midpoint defects, a phase built from those defects stays
small on the Cartesian square of that set. A nondegenerate mixed
Hessian gives an L² operator norm bound at frequency `1/ε`. Applying
it to the set indicator bounds the set's volume, without assuming a
particular shape. For several outputs, an invertible matrix evaluation
of the Hessian pencil makes a scalar phase on Cartesian powers; taking
a root cancels the matrix-evaluation dimension from the final exponent.

This proves a lower bound with coefficient half the largest pointwise
noncommutative Hessian rank. An upper bound with half the rank of the
global Hessian span follows from the constant shrinking decomposition
of that span and anisotropic Taylor cells. The two ranks need not agree.
When they agree, they give an exact leading integer precision law.
A fixed-degree polynomial admits a compact upper encoding using exact
products of input bits and at most one continuous residual per term.

## A global Hessian span is not automatically exact

Consider `f(x,y)=sqrt(x²+y²)` on `[1,2]²`. Its Hessian has rank one at
every point, while the Hessians at varying directions span the full
space of two-by-two symmetric matrices. Thus the global Hessian span
has noncommutative rank two, while the pointwise rank is one.

The actual leading coefficient is one half. The lower bound follows
from a curved one-dimensional slice. For the upper bound, use angular
sectors of width `h` and the corresponding supporting linear forms
`ell(x)=u^T(x,y)` with unit vectors `u` at sector centers. Throughout a
sector, `0<=f-ell<=R(1-cos(h/2))<=Rh²/8`, with a fixed bound `R` on
the radius. Each sector intersected with the original box is a polytope.
Affine output bands give graph relaxations with `O(ε^(-1/2))` members,
encodable by `(1/2)log2(1/ε)+O(1)` binaries. Hence the rank of the global
span is only an upper bound outside the quadratic setting.

For completeness, the Hessian is a positive multiple of
`[y²,-xy;-xy,x²]`. Three distinct ratios `x/y` give three linearly
independent coefficient vectors by the Vandermonde determinant, proving
the full three-dimensional span. No false claim is made that this cone
example disproves the pointwise-rank formula; it disproves substituting
the global span as an exact invariant.

The gap between the local-rank lower and global-span upper remains
open in the general smooth or polynomial setting. In particular,
nonlinear coordinate changes do not preserve the class of convex
linear lifts and cannot simply be treated as free transformations.

## Primary sources and attribution

Hörmander's *Oscillatory integrals and multipliers on FL^p*, Arkiv för
Matematik 11 (1973), Theorem 1.1, supplies the exact mixed-Hessian
operator estimate used at `p=2`:
[open original](https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7179-11512_2006_Article_BF02388505.pdf).
The independent novelty reviewer located and checked that statement.
Wolff's revised March 2002 *Lectures in Harmonic Analysis*, Theorem A,
printed pages 50–51, independently states the smooth compact-support
version and its TT* argument:
[editor-hosted notes](https://personal.math.ubc.ca/~ilaba/wolff/notes_march2002.pdf).
The Wolff pages were downloaded and read directly. The 1971 Acta
Mathematica publisher page returned no useful full text in this search;
we do not claim to have verified that original text.

GGOW2020 Theorem 1.4 supplies the full noncommutative rank/matrix-
evaluation equivalence. Choosing real matrix evaluations follows from
the elementary fact that a nonzero real polynomial does not vanish on
all real points. The Hermitian principal-restriction and symmetric
shrinking lemmas are proved in the preceding quadratic result.

Initial searches also located prior piecewise-affine approximation and
curvature literature. The familiar `ε^(-n/2)` cell scale, the analytic
operator estimate, noncommutative rank, parity, and binary products are
established ingredients. The candidate novelty is their combination
into a lower bound for arbitrary convex lifts and a matching compact
polynomial construction under the stated rank condition. No matching
result was found in the searches so far; priority remains unestablished.

## Constant-rank scalar continuation

The rotating-kernel gap can be closed for scalar functions whose Hessian
rank is constant on a neighborhood of the whole box. The candidate
`results/constant-hessian-rank-smooth-precision.md` proves exact coefficient
`r/2`, using local partial Legendre coordinates and polyhedral tubes
around the affine gradient fibers. It passed separate review in
`notes/review-constant-hessian-rank-smooth-precision.md`.

The geometric ingredient has close primary precedent: Fabio Nicola,
*Boundedness of Fourier integral operators on Fourier Lebesgue spaces
and affine fibrations*, [arXiv:0805.4122](https://arxiv.org/pdf/0805.4122),
Definition 1.1 and its following paragraph, printed page 3, explicitly
state the affine-gradient-fiber property under constant Hessian rank.
Pages 6–8 use transverse half-scale localization. These facts and scales
are established; the candidate formulation consequence must be scoped
accordingly. The new proof writes each local fiber as
`u(p,v)=-Db(p)^T v-∇c(p)`, making its thickened cell a genuine polytope.
It does not assume that a nonlinear coordinate change can be encoded
without cost.

## A representation-dependent computational barrier

For polynomial systems given by arithmetic circuits, determining the
exact asymptotic precision coefficient already subsumes polynomial
identity testing. This is a reduction, not an unconditional lower bound
on computational running time.

Given an arithmetic circuit with rational constants computing a polynomial `g(z)` in `d`
variables, form on `[-1,1]^(d+2)`

```
F(x,y,z)=(xy g(z), z_1²,...,z_d²).
```

The new arithmetic circuit has polynomial size in the original circuit
and the explicitly listed variables. If `g` is identically zero, the
quadratic system has coefficient `d/2`. If `g` is not zero, it is nonzero
at some interior `z_0`; at `(0,0,z_0)`, the Hessian of
`xyg(z)+sum_i z_i²` is

```
[ 0       g(z_0)   0 ]
[ g(z_0)  0        0 ]
[ 0       0      2I_d].
```

This is invertible, so the reviewed smooth theorem gives coefficient
`(d+2)/2`. Therefore an algorithm returning the exact coefficient, or
an additive approximation with error strictly smaller than one half,
decides whether `g` is the zero polynomial. No claim is made that this
obstacle applies when the full polynomial coefficient list is explicit:
in that representation identity testing is immediate.

Polynomial identity testing and its role in symbolic rank are established
algorithmic background; see GGOW2020 Sections 1.1–1.3. The new observation
here is this elementary reduction to the polynomial graph precision
coefficient. It cautions against transferring the deterministic rational
quadratic preprocessing theorem to succinct polynomial circuits without
additional argument.
