# Polynomial-bit evaluation of a certified convex patch

Date: 2026-10-02. Status: the epigraph reduction, direct GLS Turing-model
source, and rational feasibility repair have been checked. This note uses
classical convex optimization; it makes no new solver claim.

A rational strongly convex patch supports arbitrary-precision evaluation
in time polynomial in its encoding length and requested accuracy bits.
An exponentially small strong-convexity constant causes only a logarithmic
cost. This conclusion does not require the earlier sparse grid algorithm
or a parameter-dependent bound in the numerical ratio `L/tau`.

## Lemma

Let `B` be a bounded rational box and let `f` be an explicitly encoded
rational polynomial of fixed degree. Substitute every fixed coordinate,
including all integer coordinates and zero-width continuous intervals.
Suppose the remaining polynomial has a supplied positive rational `tau`
and a valid certificate that

\[
                    \nabla^2 f(x)\succeq\tau I\quad(x\in B).
\]

Let `S` be the encoding length of this restricted polynomial, its box,
and `tau`. For every nonnegative integer `q`, a deterministic algorithm
returns a rational point `y in B` and rational numbers `a,b` such that

\[
 \|y-x^\star\|_2\le2^{-q},\qquad
 a\le f(x^\star)\le f(y)=b,\qquad b-a\le2^{-q},
\]

in `poly(S+q)` bit time, with an absolute polynomial exponent at fixed
degree. Here `x^star` is the unique constrained minimizer on `B`.
Its coordinates need not be rational or interior. If `tau` is supplied
as a dyadic lower bound `2^{-k}`, the dependence on this bound is
polynomial in `k`, not in `2^k`.

This is an evaluation lemma. Constructing the patch, certifying its
convexity, and proving that it contains the original global optimizer
are separate obligations. When those obligations hold, evaluating this
patch evaluates the original implicit optimizer. Expanded algebraic
coordinates, exact active-set decisions, and exact threshold comparisons
are not promised.

## A bounded epigraph removes global-oracle qualifications

If no coordinate remains, evaluate the fixed rational point directly.
Otherwise let `m` be the remaining dimension, `c` the midpoint of `B`,
and define the positive rational quantities

\[
 r=\tfrac12\min_i(u_i-\ell_i),\qquad
 D=\sum_i(u_i-\ell_i).
\]

Write `f(x)=sum_alpha a_alpha x^alpha` and put

\[
 R_0=\max\{1,\max_i|\ell_i|,\max_i|u_i|\},\qquad
 W=1+\sum_\alpha|a_\alpha|R_0^{|\alpha|}.
\]

Then `|f|<=W` on `B`. These quantities have polynomial encoding length.
Their numerical magnitudes need not be polynomially bounded.
The rational bound

\[
 G=1+\sum_\alpha |a_\alpha|\,|\alpha|\,
                         R_0^{\max\{|\alpha|-1,0\}}
\]

also has polynomial encoding length and satisfies
`G>=max(1,sup_B ||grad f||_2)`: the displayed sum bounds the gradient's
one-norm term by term.

Consider the capped epigraph

\[
 K=\{(x,t):x\in B,\ f(x)\le t\le W+2\}.
\]

It is a compact full-dimensional convex body. It contains the Euclidean
ball centered at `(c,W+1)` of radius

\[
                         r_K=\min\{r,1/2\},
\]

because every point of that ball has `x in B` and
`W+1/2<=t<=W+3/2`. It lies in the ball with the same center and radius

\[
                            R_K=D+2W+2.
\]

Both radii have polynomial rational encoding, even for very thin boxes.
The location of the optimizer within the box has no effect on these
body bounds.

Use the following rational strong separation oracle. A query outside
`B` has a violated box inequality as separator. A query with `t>W+2`
has the separator `t'<=W+2`. If those checks pass but `t<f(x)`, the
rational inequality

\[
             t'\ge f(x)+\nabla f(x)^T(x'-x)
\]

separates the query from `K`. Otherwise the query belongs to `K`.
Every separating normal is nonzero; divide it by its infinity norm
to obtain the rational normalization required for a GLS weak separation
oracle. A strong separator with this normalization satisfies that weak
oracle's requirements at every positive tolerance. Convexity is needed
only on `B`. Fixed-degree rational value and gradient evaluation,
comparison, and normalization have polynomial query and output bit
complexity.

## The precise GLS guarantee and rational feasibility repair

The primary source is Grötschel, Lovász, and Schrijver, *Geometric
Algorithms and Combinatorial Optimization* (1988), in the local
[full text](../../literature/papers/grotschel1988-geometric-algorithms-and-combinatorial-optimization/fulltext.md)
and [PDF](../../literature/papers/grotschel1988-geometric-algorithms-and-combinatorial-optimization/original.pdf).
Definition 2.1.10, printed p. 50, specifies weak optimization with
approximate feasibility and comparison against the eroded body.
Corollary 4.2.7, printed p. 106, obtains this weak optimization oracle
from weak separation for a circumscribed convex body; its ingredients
are Theorem 4.2.2 and Remark 4.2.5. Sections 1.2--1.3 specify oracle
Turing machines and binary rational arithmetic. Section 4.1, printed
pp. 102--104, states the composition with a polynomial-time separation
algorithm. Thus this is a bit-time result, including query and
intermediate precision, rather than just an arithmetic-operation count.
These source statements were read directly for this audit.

Translate `K` by its rational center `a_0=(c,W+1)` when applying the
circumscribed-body theorem, so the supplied outer ball is centered at
zero with radius `R_K`. Translate the returned point back. Let
`K_{+epsilon}` denote the Euclidean `epsilon`-neighborhood of `K`,
and let `K_{-epsilon}` consist of points whose closed radius-`epsilon`
ball lies in `K`. Apply weak optimization to the linear objective
`-t`, with tolerance `epsilon>0`. Its returned rational point `(x,t)`
satisfies

\[
 (x,t)\in K_{+\varepsilon},\qquad
 t\le\min_{(z,s)\in K_{-\varepsilon}}s+\varepsilon,
\]

unless the algorithm correctly reports that `K_{-epsilon}` is empty.
The following choice of tolerance excludes that case and handles both
approximations in the source guarantee.

Define

\[
 A=1+\frac{2W+1}{r_K},\qquad
 C=G+2+\frac{2W+1}{r_K}.
\]

For a requested positive rational objective gap `eta`, choose

\[
                \varepsilon=\min\{r_K/2,\eta/C\}.
\]

Put `lambda=epsilon/r_K<=1/2` and
`z^star=(x^star,f(x^star))`. Convexity and the known inner ball give

\[
 (1-\lambda)z^\star+\lambda a_0\in K_{-\varepsilon}.
\]

Indeed, adding any vector of norm at most `epsilon` to this point
expresses it as a convex combination of `z^star` and a point in the
radius-`r_K` ball about `a_0`. The eroded body is therefore nonempty.
The last coordinate of this point is at most
`f(x^star)+epsilon(2W+1)/r_K`, because `f(x^star)>=-W`.
Consequently the returned coordinate satisfies

\[
                         t\le f(x^\star)+A\varepsilon.
\]

Project the returned vector `x` onto `B` by rational coordinatewise
clipping, and call the result `y`. Since `(x,t)` is within `epsilon`
of `K`, some `(bar x,bar t) in K` satisfies
`||x-bar x||_2<=epsilon` and `|t-bar t|<=epsilon`.
Projection onto the box is nonexpansive and fixes `bar x`, so
`||y-bar x||_2<=epsilon`. Both vectors lie in `B`, where the gradient
bound applies. Thus the exactly feasible rational point `y` satisfies

\[
 U:=f(y)\le f(\bar x)+G\varepsilon
              \le\bar t+G\varepsilon
              \le t+(G+1)\varepsilon.
\]

Return the rational objective interval

\[
                        [\,t-A\varepsilon,\ U\,].
\]

Its lower endpoint is at most `f(x^star)`, its upper endpoint is the
value of an exactly feasible point, and its width is at most
`C epsilon<=eta`. This argument does not assume that the weak
optimization output itself belongs to the epigraph.

Every constant and the tolerance have encoding length polynomial in
`S` and the encoding length of `eta`. The explicit separation oracle
and the cited Turing reduction therefore give a polynomial-bit
algorithm. An unrounded exact-real ellipsoid implementation would not
by itself establish this claim.

## Distance accuracy, including boundary minimizers

Constrained first-order optimality gives
`grad f(x^star)^T(x-x^star)>=0` for every `x in B`. Strong convexity
therefore gives

\[
 f(x)-f(x^\star)\ge\frac{\tau}{2}\|x-x^\star\|_2^2.
\]

Choose the rational tolerance

\[
          \eta=\min\{2^{-q},(\tau/2)2^{-2q}\}.
\]

Its encoding length is `O(S+q)`. The preceding objective enclosure
then proves both stated errors. Boundary optima require neither strict
complementarity nor discovery of the active face.

An equivalent direct sublevel argument also handles the boundary.
Choose rational `G>=max(1,sup_B ||grad f||_2)` and
`R>=max(1,diam B)`. For `delta>0`, set
`lambda=min(1,delta/(2GR))`. The homothetic box
`x^star+lambda(B-x^star)` lies in `B`, has objective at most
`f(x^star)+delta/2`, and contains a ball of radius `lambda r`.
The logarithm of its inverse radius is polynomial in the input and
accuracy lengths. Thus a boundary minimizer does not create a hidden
inverse-polynomial inradius assumption for ellipsoid sublevel methods.

## Scope and review

The rational patch and the polynomial must be explicitly encoded with
polynomial-time rational evaluation. A succinct arithmetic circuit of
unbounded degree does not inherit this statement merely from a small
circuit description. The supplied rational `tau` must be counted in
the input; writing a doubly exponentially small rational in ordinary
binary can itself require exponentially many bits. Approximation to
`q` bits does not expand a potentially exponential-degree minimal
polynomial and does not decide equality with a rational threshold.

A fresh independent audit confirmed the strong-convexity error bound,
the boundary sublevel ball, and the distinction between evaluating a
certified patch and obtaining its certificate. The coordinating
researchers independently checked the actual GLS weak-optimization
definition, the bit-model reduction, and the homothety and projection
repair above. The first version used Dadush's exact-feasible formulation
without a direct source for the full bit-model interface. This revision
instead invokes GLS directly and accounts for its near-feasible output
and comparison against the eroded body; it does not assume exact
epigraph feasibility. The evaluation conclusion is unchanged.

Targeted Python checks of this document's trailing whitespace, display
delimiters, and local links passed after the correction. No external
search, project-wide verification, or CI inspection was performed by
this audit.
