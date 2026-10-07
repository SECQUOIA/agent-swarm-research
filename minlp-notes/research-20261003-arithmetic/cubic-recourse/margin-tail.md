# Finite core noise avoids small bounded-height quadratic margins

Date: 2026-10-03. Status: proved probability lemmas, independently reviewed.
The [full theorem](theorem.md) supplies the certification and
optimizer-recovery algorithms.

Residual conditioning does not enter the probability estimates below.
The key fact is that the residual value function is semiconcave in the
core. At cores selected by linear perturbations, its contact gradient is
locally Lipschitz with the same upper-curvature constant. This controls
the distribution of optimal cores even when residual optimizers are
nonunique or change discontinuously.

## 1. Model and a finite family of margins

Let

\[
 F:[0,1]^k\times[0,1]^n\longrightarrow\mathbb R,
 \qquad V(v)=\min_{z\in[0,1]^n}F(v,z),
 \qquad V_\gamma(v)=V(v)-\gamma^Tv.
 \tag{1}
\]

Here `F` is an explicit rational polynomial of total degree at most three.
In the intended application every residual fiber is convex. The probability
proof itself only needs compact residual feasibility and a rational bound

\[
               F_{vv}(v,z)\preceq L I_k,\qquad L\ge0.
 \tag{2}
\]

Coefficient sums give such a bound with polynomial binary length. Let `I`
include the polynomial, dimensions, a supplied bound `L`, and a rational
noise half-width `sigma>0`. The case of no residual variables is allowed.

Fix an integer `R>=1` with `log(R+1)=poly(I)`. On a core face with `q`
free coordinates, put

\[
 s_q=(q+1)(q+2)/2,\qquad
 \mathcal P_{q,R}
 =\{p\in\mathbb Z[X_1,\ldots,X_q]:
       \deg p\le2,\ p\ne0,\ \|\operatorname{coeff}p\|_\infty\le R\}.
 \tag{3}
\]

Its size is `(2R+1)^{s_q}-1`. These families are used for counting, not
enumerated by the algorithm. They include integer multiples obtained by
clearing denominators in the rational minor polynomials of the
[residual-convex cubic structure theorem](../../research-20261002/new-direction/residual-convex-cubic-boundary.md).
That theorem gives a polynomial-bit common bound for the coefficient
heights after restriction to any original core face.

For `0<mu<1`, call a draw bad if there are an original core face `A`, a
global optimizer `a` of (1) in `relint A`, and a polynomial in the family
(3) for that face such that `|p(a)|<=mu`. Coordinates of `a` in this
condition are the free face coordinates. Exact zeros are included.
Zero-dimensional faces cannot be bad: their nonzero integer polynomials
are constants of absolute value at least one.

## 2. Contact gradients have a local Lipschitz bound

Fix a positive-dimensional core face, identify its closed free-coordinate
box with `K=[0,1]^q`, and restrict `V` to this box. The function

\[
                         V(v)-(L/2)\|v\|_2^2
 \tag{4}
\]

is concave. Indeed, the same assertion holds for each fixed residual
point by (2), and an infimum of concave functions is concave. Compactness
makes `V` finite and continuous.

Let `C` be the set of points `a in int K` admitting an affine lower
support on the whole box:

\[
        V(x)\ge V(a)+g_a^T(x-a)\quad\hbox{for every }x\in K.
 \tag{5}
\]

At such a point the vector `g_a` is unique and `V` is differentiable
with gradient `g_a`. To see this, take a supergradient of the finite
concave function (4) at the interior point. Its resulting quadratic
upper support, compared with (5) along both signs of each direction,
must have the same linear term `g_a`. Consequently

\[
 0\le V(x)-V(a)-g_a^T(x-a)
       \le (L/2)\|x-a\|_2^2\quad(x\in K).
 \tag{6}
\]

The map `a -> g_a` is locally `L`-Lipschitz on `C`. For the proof take
`a,b in C`, let `r=||a-b||`, and suppose the closed ball of radius `r`
about `a` lies in `K`. Write `d=g_b-g_a`. Combining the lower support
at `b` with the upper support at `a` gives

\[
 d^Th\le V(a)-V(b)-g_b^T(a-b)+(L/2)\|h\|_2^2
       \le (L/2)(r^2+\|h\|_2^2)
 \tag{7}
\]

whenever `a+h in K`. For `d!=0`, choose `h=r d/||d||`. Then (7)
implies `||g_b-g_a||<=L||a-b||`. The zero-distance and zero-vector
cases are immediate. Every interior point has a ball small enough that
this argument applies to every pair of contact points in that ball.

In particular, for a measurable subset `T` of `C`,

\[
            \operatorname{vol}_q\{g_a:a\in T\}
                 \le L^q\operatorname{vol}_q(T).
 \tag{8}
\]

One can apply the usual volume inequality for Lipschitz maps on each
member of a countable interior-ball cover. Partition `T` into disjoint
measurable pieces subordinate to that cover, apply the inequality with
constant `L` to each piece, and use subadditivity on their images.
All sets used below are semialgebraic, so measurability presents no
additional issue. This argument does not assert a Lipschitz residual
selector or differentiability of `V` away from the contact set.

If `a` minimizes `V(v)-gamma^T v` on `K` and lies in its interior,
then (5) holds with `g_a=gamma`. Thus for any semialgebraic
`T subset int K`, continuous uniform noise on `[-sigma,sigma]^q`
satisfies

\[
 \Pr\{\text{some interior minimizer belongs to }T\}
       \le \left(\frac{L}{2\sigma}\right)^q
                         \operatorname{vol}_q(T).
 \tag{9}
\]

The statement allows multiple minimizers. If `L=0`, the right side is
zero for positive-dimensional faces, as follows directly from (8).

## 3. An elementary quadratic sublevel estimate

For every nonzero integer polynomial `p` of degree at most two and
`0<mu<1`,

\[
 \operatorname{vol}_q\{x\in[0,1]^q:|p(x)|\le\mu\}
                     \le \min\{1,8\sqrt\mu\}.
 \tag{10}
\]

The estimate is independent of the coefficient upper bound `R`.

For a univariate quadratic with leading coefficient `a!=0`, completing
the square shows that its sublevel set on the entire line has length
at most `2 sqrt(2 mu/|a|)`, and therefore at most
`4 sqrt(mu/|a|)`. This includes the two-interval case: their total
length is largest when the inner endpoints meet.

If `p` has a nonzero square coefficient, slice the cube parallel to
that coordinate axis. The leading coefficient on every slice is the
same nonzero integer, so its absolute value is at least one. Fubini's
theorem proves the stronger bound `4 sqrt(mu)`.

If the quadratic part is nonzero but all square coefficients vanish,
choose a nonzero coefficient of `x_i x_j` and slice parallel to
`(e_i+e_j)/sqrt(2)`. Every univariate slice has quadratic leading
coefficient of absolute value at least `1/2`. The orthogonal projection
of the unit cube onto the perpendicular hyperplane has volume `sqrt(2)`:
only the two selected coordinates rotate. Fubini now gives
`sqrt(2) * 4 sqrt(2 mu)=8 sqrt(mu)`.

For a nonconstant linear polynomial, slicing along a nonzero integer
coefficient gives volume at most `2mu<=2sqrt(mu)`. For a nonzero
integer constant the sublevel set is empty. Taking the trivial bound
one proves (10).

For a fixed positive-dimensional face and a fixed member of (3),
(9)--(10) therefore imply

\[
 \Pr_{\rm cont}\{\text{some interior face minimizer has }|p(a)|\le\mu\}
       \le 8\left(\frac{L}{2\sigma}\right)^q\sqrt\mu.
 \tag{11}
\]

## 4. Uniform scalar sections transfer the bound to finite noise

Use the endpoint-inclusive uniform `M`-point grid on `[-sigma,sigma]`
independently in each core coordinate. We use exactly the two-block
elimination and marginal-replacement argument established in
[the finite-noise tail note, Sections 2--3](../../research-20261002/new-direction/polynomial-finite-noise-tails.md).
No algebraic tube theorem is needed here.

For a fixed face and polynomial, let `E` be the event in (11). Its exact
formula, with the fixed coordinates of the face substituted in `F`, is

\[
 \begin{split}
 \exists(a,z)\ \forall(w,y):\quad&
  a\in(0,1)^q,\ z\in[0,1]^n,\ |p(a)|\le\mu,\\
 &\bigl[(w,y)\notin[0,1]^{q+n}\bigr]\ \vee\\
 &\bigl[F(w,y)-\gamma^Tw
                   \ge F(a,z)-\gamma^Ta\bigr].
 \end{split}
 \tag{12}
\]

The last two lines are one disjunction, conjoined with all three
conditions on the first line. This is face minimization; every global
optimizer whose minimal core face is the chosen face satisfies it.
It makes no uniqueness or regularity assumption about the residual
optimizer.

Fix every noise coordinate except one. Formula (12) then has one free
scalar, two quantified blocks of at most `n+k` variables each, at most
`s_0=20(n+k+1)` polynomial atoms, and joint degree at most three.
The scalar-noise products have degree two. The threshold, fixed noise
coordinates, and coefficients of `p` are real coefficients; their
heights do not affect this format bound.

Using the effective universal constant `a_0` from the same fixed
quantifier-elimination bound as the predecessor, put

\[
 H=(3s_0)^{a_0(n+k+1)^2},\qquad C=2H^3+1.
 \tag{13}
\]

Increasing `a_0` once if necessary covers the displayed coarse atom
count. Every scalar section of `E` is a union of at most `C` interval
or point components. This is uniform in the threshold and every fixed
real value of the other noise coordinates, including the hybrid
continuous/discrete marginals used during replacement. The sampler
computes the format bound and does not perform quantifier elimination.

The endpoint-inclusive grid and continuous uniform distribution differ
by at most `1/M` in their cumulative distribution functions. An interval
or point therefore has discrepancy at most `2/M`, with any endpoint
convention. Replace the `q` marginals successively and condition on
the other coordinates at each step. It follows that

\[
 \Pr_{\rm grid}(E)
     \le8\left(\frac{L}{2\sigma}\right)^q\sqrt\mu
                  +\frac{2qC}{M}.
 \tag{14}
\]

This includes atoms at exact polynomial zeros. In particular the event
that an interior minimizing core lies on the zero set of `p` has grid
probability at most `2qC/M`, by decreasing `mu` to zero. All estimates
concern the same fixed grid; no noise resampling depends on a requested
optimizer accuracy.

## 5. Simultaneous margin and a polynomial-bit rare-event budget

For `k>=1`, define the following computable upper bounds:

\[
 \begin{split}
 N&=3^k(2R+1)^{s_k},\\
 A&=8N\max\{1,L/(2\sigma)\}^k,\\
 D&=2kNC.
 \end{split}
 \tag{15}
\]

There are at most `N` face/polynomial pairs. Their number is used only
in a union bound. Original core faces are fixed before sampling. Apply
(14) to their free-coordinate noise subvectors and sum, without
conditioning on the face chosen by the optimizer. Then

\[
                  \Pr\{\text{bad draw}\}
                         \le A\sqrt\mu+D/M.
 \tag{16}
\]

The binary lengths of `N,A,D` are polynomial in `I+log(R+1)`. For
`k=0` the bad event is empty and all this sampling work is omitted.

Let `B>=2` be any separately justified fallback-cost factor with
`log B=poly(I)`. Choose a positive dyadic number and a power-of-two grid
size by rounding the following thresholds by at most a factor of two:

\[
             \mu\le(2AB)^{-2},\qquad
             M\ge\max\{2,2DB\}.
 \tag{17}
\]

Then (16) is at most `1/B`. Both `log(1/mu)` and `log M` are polynomial
in the base input. These choices may also be made smaller/larger,
respectively, to satisfy other already proved polynomial-bit rare-event
budgets.

Outside the event in (16), every nonzero polynomial from the family
on the minimal face of any global optimizer has absolute value greater
than `mu`. This is stronger than bounding only the minors that are
nonzero at that optimizer: it excludes zeros of every nonzero member
of the tested family. Identically zero minor polynomials are omitted
when applying the assertion. If a rational minor is represented as
`P/d`, where `P` belongs to the integer family and `1<=d<=D_*`, its
absolute value is greater than `mu/D_*`. Polynomial-bit coefficient
height estimates supply a base bound `D_*` without enumerating minors.

The coordinate polynomials `x_i` and `1-x_i` also belong to (3). Thus,
on a good draw, every free coordinate of the optimal core is more than
`mu` from the two boundaries of its exact face. Coordinates fixed by
that face remain fixed; the probability argument does not identify them.

Equation (17) supplies a rare-event budget, not a sound stopping rule.
The separate [lattice certificate](lattice-certificate.md) must certify
the required margin, and the face must be certified separately. If a
bounded-work certification attempt fails, a correct fallback can be
charged to (16) only after proving that the attempt succeeds on every
draw outside the stated event. The present note does not assume success
merely because margins are likely, and does not replace finite atoms
with an almost-sure assertion.

## 6. Verification and attribution

The contact-gradient and quadratic-sublevel estimates are proved above.
The finite-law transfer uses the already audited Renegar two-block
format bound and scalar-grid discrepancy argument in the linked
predecessor. No new lattice theorem or external-source claim is needed
for this probability note.

A fresh independent review checked the actual file, including the local
contact-gradient estimate, image-volume inequality, both quadratic
slicing cases, the quantified event, marginal replacement, and the final
union and rare-event constants. It found no substantive mathematical gap.
Its clarification that the dyadic threshold and grid size must be chosen
near the displayed bounds, rather than arbitrarily beyond them, is
incorporated above.

The targeted inline command `python3 - <<'PY'` checked trailing whitespace,
paired display and split delimiters, the 17 sequential equation tags, and
all local links in this file. It passed. The scoped command
`git diff --check -- research-20261003-arithmetic/cubic-recourse/margin-tail.md`
also passed; the inline whitespace check covers this new untracked file.
These document checks do not constitute numerical or formal verification
of the mathematical claims. No project-wide verification or CI inspection
was performed.
