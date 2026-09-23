# Adversarial review of planar curvature and smoothed regions

Date: 2026-09-22. Reviewed source:
[higher-dimensional smoothing](research-20260922-higher-dimensional-smoothing.md).
The source was not edited during this review.

**Verdict:** I found no correctness gap in the stated planar theorem. The
piecewise-quadratic curvature argument, including its corner contribution,
is valid. The finite semialgebraic setting is important to the proof as
written. I recommend a stronger literature attribution and a broader quadratic
corollary below. This is an independent mathematical review, not a formal proof
or a claim that a literature search establishes novelty.

## Curvature measure and interface calculation

I independently checked the following parts of Section 3.

For a concave, globally `L`-Lipschitz function `g` on the square, its
distributional Hessian is a negative semidefinite matrix measure. Therefore
its nuclear-norm variation is the mass of `-Delta g`. On an inner parallel
square whose boundary avoids exceptional interface configurations, the
piecewise divergence theorem gives

```
|D^2 g|_*(D_epsilon)
  = - integral_(boundary D_epsilon) grad(g) dot n
  <= L perimeter(D_epsilon) <= LP.
```

Boundary traces have norm at most `L`. Monotone convergence of the positive
measure `-Delta g` establishes the claimed bound on the entire open square.
No lower bound on the gradient of `g` is used.

For `h=g_0-g_1`, refine the finitely many polynomial pieces to a finite
semialgebraic stratification. Its one-dimensional interfaces may be curved;
this causes no additional singular Hessian term. In tangent-normal coordinates,
continuity of `h` implies that its two gradient traces have the form
`(a,b_minus)` and `(a,b_plus)`. The singular Hessian is

```
(b_plus-b_minus) n tensor n times arc length,
```

whose nuclear-norm mass is `|b_plus-b_minus|` times arc length. The variation
of the normal direction along an interface does not enter this jump term.

At a transverse level crossing, `a` is nonzero. Both gradient directions lie
in the same open half-plane with prescribed tangential sign. Thus their
angular difference is the absolute difference of the appropriate continuous
arctangent branch. Since

```
|d/db atan(b/a)| = |a|/(a^2+b^2) <= 1/|a|,
```

the claimed bound `|a| alpha <= |b_plus-b_minus|` follows, even when the
normal components have opposite signs. The oriented level tangents have the
same angular difference: continuity through the interface prevents an
unaccounted reversal. One-dimensional coarea along the interface weights
each crossing by precisely `|a|`. The singular Hessian therefore pays for
the full integrated corner curvature.

Inside smooth cells, the level curvature formula and coarea give the stated
bound by the absolutely continuous nuclear-norm Hessian mass. Adding the two
contributions yields

```
integral TC(h^(-1)(y) intersect interior(D)) dy
 <= |D^2 h|_*(interior(D)) <= 2LP.
```

The finite exceptional set of stratum-critical values excludes zero
gradients, tangential interface contacts, constant restrictions, and
arrangement vertices. Away from those values the level is a one-dimensional
manifold with finitely many corners. A compact connected component is a
simple closed curve, so the total-curvature lower bound `2pi` proves
`integral C(y) dy <= LP/pi`.

This proof should not be silently extended to arbitrary Lipschitz functions.
Nor does the same proof automatically apply to every abstract DC function:
one would then need additional approximation and level-set regularity work.

## Charging loops and counting regions

The identity `{h_i=xi_i}` = the set where both bit classes attain the global
minimum is exact. It is stronger than a containment and is needed when
charging a junction-free tie loop to a whole connected level component.
Along such a loop the two active supports cannot change without creating a
third active support. Every additional branch of the class level set would
be an additional branch of the global tie set; it is excluded by regularity
of the fixed pairwise equality curve. Thus the loop charge is valid.

I also checked the junction and Euler arguments. Three distinct cube vertices
have affine rank two, and an invertible two-coordinate projection gives three
corners of a square. Choosing the elbow makes the two noise equations simple
class differences, with derivative row norms at most `2L`. The area formula
therefore gives the proposed `4 phi^2 L^2 A` bound per coordinate pair and
corner triple. The finite union bound has the stated constant.

Five co-minimizing supports would include four affinely independent supports.
Conditioning off three suitable coordinates then places three independent
continuously distributed noises in a two-dimensional polynomial image. Its
three-dimensional measure is zero. Hence there are at most four active
supports almost surely. Every pairwise conic is regular almost surely because
its random offset cannot equal its single possible critical value. Six pairs
give at most twelve incident half-arcs at a junction. Boundary tie points have
degree one: pair tangencies and boundary triple ties are null events.

After removing isolated vertices, the number of nonclosed edges is at most
`6J+B/2`. Adding these edges and the junction-free loops gives
`R <= 1+6J+B/2+W`. This bound tolerates tangencies between different regular
pair curves at an interior junction; no unproved transversality between all
pair curves is needed. In fact, finiteness of `R` alone holds for every noise
realization by semialgebraicity. The substantive claim is its expected bound.

## Stronger scope for the quadratic theorem

The source says common concave normalization is essential. It is essential
to this particular curvature budget, but it is not a qualitative restriction
for a family of quadratics with uniformly bounded gradients on the square.

Suppose directly that `||grad q_z|| <= K` on `[-M,M]^2`. For any unit vector
`u`, both `Mu` and `-Mu` belong to the square. Since the Hessian `H_z` is
constant,

```
2M ||H_z u||
 = ||grad q_z(Mu)-grad q_z(-Mu)|| <= 2K.
```

Consequently `||H_z||_op <= K/M`. The common polynomial

```
p(t)=K ||t||^2/(2M)
```

makes every `q_z-p` concave, and

```
||grad(q_z-p)|| <= (1+sqrt(2))K.
```

The stated theorem therefore implies the same polynomial expected region
bound for arbitrary `K`-Lipschitz quadratic families after substituting
`L=(1+sqrt(2))K`. The Schur-complement normalization remains useful because
it supplies a sharper, subtree-independent gradient bound for indicator QPs.
This extension is an elementary corollary, not a separate novelty claim.

## Primary literature examined

The strongest additional antecedent found during this review is
[Bourgain, Korobkov, and Kristensen, *On the Morse–Sard property and level sets
of Sobolev and BV functions*](https://ems.press/journals/rmi/articles/11727),
Rev. Mat. Iberoam. 29 (2013), 1–23. I inspected the
[published full text](https://ems.press/content/serial-article-files/38407?nt=1),
especially Theorem 6.1, Corollary 6.2, and the proof on pages 20–21. They show
that almost every level of a planar `BV_2` function is a finite family of
finite-turn curves. Their proof combines coarea, Hessian variation, and the
closed-curve curvature lower bound. Its displayed estimates use level subsets
with gradient bounds. I did not find the source note's precise global
`LP/pi` inequality there. This is nevertheless a direct and important
antecedent for the analytic mechanism; general DC calculus is a less precise
comparison. No novelty should be claimed for finite-turn level regularity.

I also checked the primary arXiv records for
[Ambrosio and Bertrand, *DC Calculus*](https://arxiv.org/abs/1505.04817),
which develops measure-valued Hessians, and
[Sullivan, *Curves of Finite Total Curvature*](https://arxiv.org/abs/math/0606007),
which treats smooth and polygonal curves in a common framework. These records
support the existing attribution but do not establish priority for the
smoothed optimization theorem.

Searches used “bounded Hessian level curvature,” “difference of convex level
sets curvature,” and “Bourgain Korobkov Kristensen level curves bounded
variation total curvature BV2.” This was a targeted analytic-source audit,
not a comprehensive audit of smoothed multiparametric optimization.

## Verification limits

The checks above were symbolic mathematical checks of the proof and its
constants. No numerical experiment or Lean check was used, since neither
would directly verify the coarea and genericity arguments. No project-wide
verification or CI inspection was run. A separate source and significance
review should still assess the complete smoothed representation result and
its distinction from prior smoothed multiobjective bounds.
