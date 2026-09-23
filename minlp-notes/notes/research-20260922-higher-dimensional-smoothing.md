# Polynomial expected region count for two-dimensional quadratic messages

Date: 2026-09-22. Status: research theorem developed jointly with the coordinator;
two independent adversarial reviews found no mathematical gap. This extends the scalar
[smoothed-message investigation](research-20260922-next-frontier.md) at the level
of representation size. It does not establish a dynamic-programming algorithm.

## Statement

Let `Z` be a nonempty subset of `{0,1}^m`. For every `z`, let `q_z` be a
quadratic polynomial on the closed square `D=[-M,M]^2`, where `M>0`.
Suppose there is a common quadratic polynomial `p` such that every

```
r_z=q_z-p
```

is concave and has Euclidean gradient norm at most `L` on `D`. Let the
coordinates of `xi` be independent real random variables, each with a density
bounded by `phi`. Define

```
F_z(t)=q_z(t)+xi dot z,    V(t)=min_z F_z(t).
```

Let `R` count connected open regions of `interior(D)` on which the minimizing
support is unique. A support appearing in several disconnected regions is
counted repeatedly. Put `A=4M^2` and `P=8M`.

**Theorem.** Almost surely `R` is finite, and

```
E R <= 1 + (1+1/pi)m phi L P
           +96 binom(m,2) phi^2 L^2 A.                (1)
```

The constant is deliberately coarse. In particular, the expected number of
distinct necessary support quadratics is polynomial in `m,phi,L,M`, despite
the exponential number of possible supports. No independence between support
costs is assumed. Only the original coordinate penalties are independent.

Subtracting `p` preserves the minimizing supports. All proof steps below use
`r_z`; its common concave normalization supplies the curvature bound.

This is not a qualitative restriction for uniformly Lipschitz quadratics.
If instead every `q_z` has gradient norm at most `K` on the square, its
constant Hessian satisfies `||H_z||_op<=K/M`: evaluate the gradient at
`Mu` and `-Mu` for any unit vector `u`. Taking
`p(t)=K||t||^2/(2M)` makes every `q_z-p` concave with gradient norm at most
`(1+sqrt(2))K`. Thus (1) applies to any such quadratic family with
`L=(1+sqrt(2))K`. The support-elimination normalization below gives a
sharper bound for the optimization application.

## 1. Boundary crossings

Fix a coordinate `i` having two nonempty support classes and condition on all
noise except `xi_i`. Put

```
g_a(t)=min_(z_i=a) [r_z(t)+sum_(j!=i)xi_j z_j],
h_i(t)=g_0(t)-g_1(t).
```

Each `g_a` is concave and `L`-Lipschitz. Hence `h_i` is `2L`-Lipschitz.
The equation `h_i(t)=xi_i` says exactly that both coordinate classes attain
the global minimum. One-dimensional area/coarea on each of the four boundary
edges gives, for the number `B` of global tie points on the boundary,

```
E B <= 2m phi L P.                                  (2)
```

At fixed corners there is almost surely no tie. Pair equality curves meet
the interiors of the boundary edges transversely almost surely: tangency of a
fixed quadratic difference restricted to an edge requires its random constant
offset to take one of finitely many deterministic values. A restriction that
is constant is likewise almost surely nonzero.

## 2. Triple junctions: two independent coordinates suffice

Any three distinct binary vectors have affine rank two. Thus some two
coordinates project them onto three distinct corners of `{0,1}^2`.
Every choice of three corners has an elbow corner connected to each of the
other two by a unit coordinate edge.

Fix a coordinate pair `i,j` and condition on all other noise. Form the up to
four class minima

```
C_ab(t)=min_(z_i=a,z_j=b)
        [r_z(t)+sum_(k notin {i,j})xi_k z_k].
```

Ignore empty classes. For a choice of three corners, use the elbow corner
and its two neighbors. Equalities of the three class values take the form

```
(xi_i,xi_j)=H(t),
```

where each component of `H`, up to a sign, is the difference of two class
minima. Therefore each row of `DH` has norm at most `2L` almost everywhere,
and `|det DH|<=4L^2`. The two-dimensional area formula and the conditional
density bound `phi^2` give

```
E #{t in interior(D): H(t)=(xi_i,xi_j)} <=4phi^2 L^2 A.
```

At a point with three distinct globally minimizing supports, one coordinate
pair and one choice of three corners witness this event. There are four
corner triples for each coordinate pair. If `J` is the number of interior
points with at least three globally minimizing supports, then

```
E J <=16 binom(m,2) phi^2 L^2 A.                     (3)
```

This argument does not assert that every solution of the class equality is
a global triple tie; the extra solutions only strengthen the upper bound.
The finite expectation also excludes an infinite global triple locus almost
surely. Restricted to a boundary edge, the same Lipschitz map `H` has an
image of two-dimensional measure zero. Thus almost surely there are no
triple ties on the boundary. No enumeration of support triples appears in
the estimate.

## 3. Compact tie loops: a planar curvature estimate

We need a precise special case of a bounded-Hessian level-set estimate.
It is proved here for finite piecewise-quadratic functions, so no general
regularity theorem for arbitrary difference-of-convex functions is needed.

**Lemma.** Suppose `h=g_0-g_1`, where `g_0,g_1` are concave, continuous,
finite piecewise-quadratic functions and `L`-Lipschitz on `D`. For almost every
real `y`, its level set in the interior is a finite union of regular arcs
with finitely many corners. Let `C(y)` count its compact connected components.
Then

```
integral_R C(y) dy <= L P/pi.                       (4)
```

Here components are counted only at regular levels. The exceptional levels
have measure zero. A finite semialgebraic stratification of the quadratic
arrangement supplies finitely many smooth cells, interface arcs, and vertices.
The restrictions to these strata have only finitely many critical values;
constant restrictions contribute their one constant value. Removing these
values makes the level curves regular and transverse to interfaces.

For completeness, use the nuclear norm for matrix-valued Hessian measures.
On a smooth cell, write `tau` for a unit tangent to a regular level curve.
Its absolute curvature is

```
|kappa|=|tau^T (Hess h) tau|/||gradient h||.
```

Coarea therefore bounds the integral over levels of their smooth-arc
curvature by `integral ||Hess h||_* dt` on these cells.

There is an additional corner whenever a level curve crosses an interface.
Choose unit tangent and normal coordinates to that interface. Continuity of
`h` makes the two one-sided gradients `(a,b_-)` and `(a,b_+)`, with the same
tangential derivative `a`. At a transverse level crossing, `a!=0`. The
absolute corner angle `alpha` satisfies

```
|a| alpha <= |b_+-b_-|.                             (5)
```

Indeed the angle between the two gradients is the difference of their
arctangents in the half-plane with tangential coordinate of the fixed sign
of `a`; the derivative of this angle with respect to `b` has absolute value
at most `1/|a|`. The level tangents turn by the same angle. One-dimensional
coarea along the interface now bounds its integrated corner contribution
by `integral |b_+-b_-| ds`. This is exactly the nuclear-norm mass of the
singular Hessian there: continuity makes the gradient jump normal to the
interface. Arrangement vertices belong only to the excluded finite set of
level values.

Consequently, writing `TC` for total absolute curvature including corners,

```
integral_R TC({h=y} intersect interior(D)) dy
    <= |D^2 h|_*(interior(D)).
```

For a concave `L`-Lipschitz function `g`, the measure `-D^2g` is positive
semidefinite. Its nuclear-norm mass equals `-Delta g(D)` and is at most
`L P`, by integration of the outward gradient flux. This can be justified
on inner parallel squares with generic boundaries and then by a monotone
limit; the finite piecewise-smooth divergence theorem already suffices here.
Thus

```
|D^2 h|_* <= |D^2g_0|_*+|D^2g_1|_* <=2LP.
```

Every compact regular level component is a simple closed curve. Its total
absolute curvature, including its corner angles, is at least `2pi`, by the
classical turning theorem (or Fenchel's theorem). Dividing by `2pi` proves
(4).

Apply this lemma conditionally to each `h_i`. Since `xi_i` has density at
most `phi`, the expected number of compact components of `{h_i=xi_i}` is
at most `phi L P/pi`.

Let `W` count connected components of the global tie set that are compact
loops having no triple junction. On each such loop the same two supports
minimize throughout: changing either support would create a triple tie.
Choose any bit on which these two supports differ. The loop is then an
entire compact connected component of `{h_i=xi_i}`. It cannot acquire an
additional branch without creating a triple junction. Hence

```
E W <=m phi L P/pi.                                 (6)
```

## 4. A finite planar graph bounds the regions

Two elementary genericity facts give a uniform degree bound.

First, the zero set of every pairwise difference `F_z-F_w` is almost surely
a regular affine zero set of a polynomial of degree at most two, or is
empty. This includes lines and pairs of parallel lines. The nonconstant part is a fixed quadratic;
a singular zero requires its random constant offset to equal a critical
value of this quadratic. A quadratic has at most one critical value when
its critical set is nonempty. A constant difference is almost surely
nonzero. The random offset has a density because `z!=w`.

Second, there are almost surely no five co-minimizing supports anywhere in
the square. Any five binary vectors have affine rank at least three: a
rank-two affine subspace has an injective projection onto two suitably
chosen coordinates and hence contains at most four binary vectors. Choose
four affinely independent vectors from any rank-three subset and three
noise coordinates making the associated difference matrix nonsingular.
Conditioning on all remaining noise, their three equality equations force
these three coordinates to belong to the image of a polynomial map from
the square to `R^3`. That image has three-dimensional Lebesgue measure zero.
A finite union over support choices proves the assertion.

Away from the `J` triple junctions and the `B` boundary points, the global
tie set is locally a smooth arc involving exactly two supports. At a triple
junction there are at most four supports and hence at most six smooth pair
zero curves, each with two incident half-arcs. Its graph degree is at most twelve.
There are no isolated tie points, because a regular equality curve between
two minimizers crosses locally while the other supports remain strictly
higher. The triple points already cover any remaining isolated possibilities.

Split the tie set into arcs at the junctions and boundary points; retain
junction-free compact loops separately. Its number of arcs is at most
`6J+B/2`, because each arc has two ends and the total degree is at most
`12J+B`. There are finitely many arcs by semialgebraicity. Adding one arc
or one closed loop to a planar disk can increase the number of complementary
regions by at most one. Equivalently, the planar graph Euler formula gives

```
R <=1+6J+B/2+W.                                    (7)
```

Isolated junctions do not increase the region count. Every complementary
region has one fixed unique minimizing support, by continuity. Equations
(2), (3), and (6) prove (1).

## Indicator quadratic programs satisfy the normalization

Consider a positive definite quadratic objective with two fixed boundary
coordinates `t` and internal coordinates `x`, restricted to a support `S`:

```
x_S^T Q_SS x_S +2t^T Q_BS x_S +c_S^T x_S
   +t^T Q_BB t+c_B^T t+lambda(S).
```

After eliminating `x_S`, subtract the common boundary polynomial
`p(t)=t^T Q_BB t+c_B^T t`. The remaining branch is

```
r_S(t)=lambda(S)
 -1/4 (c_S+2Q_SB t)^T Q_SS^(-1)(c_S+2Q_SB t),
```

which is concave. If the original matrix satisfies

```
0<d<=Q_ii<=D_0,
sum_(j!=i)|Q_ij|<=rho Q_ii,    rho<1,
|c_i|<=C,
```

then the coordinate maximum principle gives an invariant box with
`M=C/[2d(1-rho)]`. Every conditional internal minimizer has coordinates
in `[-M,M]` when `t` belongs to that box. Each coordinate of `gradient r_S`
is `2 sum_(j in S)Q_bj x_j`, so its absolute value is at most
`2rho D_0 M`. We may therefore take

```
L=2sqrt(2)rho D_0 M.
```

Independent noise in the internal indicator penalties now gives (1), with
constants independent of the number of eliminated continuous variables.
Deterministic support intercepts, including the original indicator
penalties, cause no difficulty. Boundary indicators can be fixed separately.

This is a bound for exact regions and retained support quadratics for a
two-dimensional separator. It does not construct those formulas efficiently,
bound products of dependent message sizes, or supply a bit-complexity theorem.
Those are separate obstacles to an algorithm for general bounded-treewidth
indicator QPs. The result also does not automatically extend to separator
dimension three: compact level surfaces require a different curvature measure
and the planar graph argument is unavailable.

## Sources examined and novelty limits

The estimate combines classical geometric measure theory with coordinate
isolation. None of the area formula, coarea formula, planar graph Euler
formula, or total-curvature inequality is a new ingredient.

- [Brunsch and Roeglin, *Improved Smoothed Analysis of Multiobjective
  Optimization*](https://arxiv.org/abs/1111.1546) studies several independently
  perturbed linear objectives and one arbitrary objective. Here there is one
  perturbed penalty vector, while both deterministic parameter directions
  and all support-dependent quadratic coefficients remain unperturbed.
  An equivalence has not been established.
- [Ambrosio and Bertrand, *DC Calculus*](https://arxiv.org/abs/1505.04817)
  develops measure-valued Hessians for differences of convex functions in
  a substantially broader setting. This note uses only the elementary
  finite piecewise-quadratic case and does not claim new DC calculus.
- [Bourgain, Korobkov, and Kristensen, *On the Morse–Sard property and level
  sets of Sobolev and BV functions*](https://ems.press/journals/rmi/articles/11727),
  Theorem 6.1, Corollary 6.2, and their proof, give a closer antecedent:
  almost every planar bounded-Hessian level has finite-turn components,
  using Hessian variation, coarea, and closed-curve curvature. The
  [curvature review](review-20260922-planar-curvature.md) records the full-text
  comparison. These mechanisms and level regularity are established theory;
  the precise bound above is derived for the finite piecewise-quadratic case.
- [Sullivan, *Curves of Finite Total Curvature*](https://arxiv.org/abs/math/0606007),
  including its Theorem 2.4, supplies the classical closed-curve curvature
  inequality in a form allowing corners. The inequality can also be obtained
  directly from the planar turning theorem.
- [Hajlasz, differential-geometry lecture notes](https://sites.pitt.edu/~hajlasz/Notatki/Undergraduate_Differential_Geometry.pdf)
  were inspected for the classical smooth Fenchel statement and its treatment
  of piecewise-smooth curves.
- [Ghaffari Hadigheh, Romanko, and Terlaky, *Sensitivity analysis in convex
  quadratic optimization*](https://optimization-online.org/2005/02/1070/)
  treats deterministic parameter changes in continuous QPs. It does not
  establish a penalty-only smoothed support-region bound.

Searches for smoothed multiparametric quadratic programming, random lower
envelopes, and planar difference-of-convex level-set complexity did not locate
an equivalent theorem. That unsuccessful search does not establish novelty.
The strongest direct comparison remains the scalar message theorem and its
primary-source audit. A broader source audit is needed before publication.

## Verification and next questions

The coordinator independently derived the two-coordinate area bound and
rechecked the normalization corollary. Fresh independent reviews checked the
[curvature and interface argument](review-20260922-planar-curvature.md) and
[coordinate conditioning, genericity, topology, and prior work](review-20260922-planar-topology.md).
Neither found a mathematical gap. The second review includes exact examples
showing that four-way junctions can persist and that the separate loop term
is necessary. No computation or Lean check proves the analytic theorem, and
no project-wide verification was run. Positive reviews are evidence, not a
correctness or novelty guarantee.

The most consequential next question is whether an exact message
construction can use this first-moment representation bound without requiring
uncontrolled products or second moments. Finite-grid noise would also require
a fresh atomic-level analysis; the scalar monotone-arc proof cannot simply be
reused in two dimensions.
