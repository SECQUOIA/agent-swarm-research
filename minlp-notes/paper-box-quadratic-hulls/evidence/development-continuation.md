# Continuation: removing the pair-minor hypothesis when vertices are positive

This is independently reviewed mathematical development. After mathematical
review found no substantive gap, the root authorized provisional TeX
integration: `sections/05b-contact-classification.tex` and
`appendices/E-contact-classification.tex` were updated, and
`appendices/F-facet-classification.tex` was added. No main input or build
was changed; final inclusion is gated on the exact Hildebrand source
receipt. No literature tool, KB check, experiment, sampler, or archived
verification script was run. The only external input
below is a precise source contract supplied by the existing literature lead
before that session was paused.

## Proposed strengthened classification

Let `q=q0+a^T x+x^T Qx` generate an extreme ray of `P3`, the cone of
quadratics nonnegative on `[0,1]^3`. Suppose:

1. `Qii>0` for all three coordinates;
2. `Q12 Q13 Q23>0`;
3. `q(v)>0` for all eight cube vertices.

Then `q` is either an affine square or a cube-symmetry copy of the strict
five-contact family. In particular, if at least one pair principal
determinant is nonnegative, `q` is an affine square and belongs to `D3`.

The previously proved contact classification establishes this conclusion
once all zeros are strict edge contacts. The new ingredient below excludes
stationary zeros of a PSD facet restriction among non-square extreme rays.
It handles both facet-interior zeros and edge zeros with zero derivative
into an adjacent facet. Consequently the pair-minor assumptions can be
removed when vertex values are positive. Vertex-zero rays remain outside
this argument.

## 1. External rank-one subtraction input and its cube transfer

The literature lead supplied the following exact contract from Hildebrand,
*Minimal zeros of copositive matrices*, arXiv:1401.0134v4, Lemma 4.3,
with irreducibility defined in Definition 2.1:

> For a copositive matrix `B` and a nonzero vector `w`, there exists
> `epsilon>0` such that `B-epsilon*w*w^T` is copositive if and only if
> `w^T u=0` for every zero `u>=0` of `B`.

Thus annihilating all zeros is sufficient. No extra support or critical
direction condition occurs in this rank-one subtraction criterion. The
exact source statement should still be checked against the already
available original before submission; this investigation does not launch
a new literature session. Hildebrand's theorem by itself does not classify
cube quadratics.

Here is the full transfer, including normalization. Let `A` be the
homogeneous symmetric `4x4` coefficient matrix of `q` and let `R` be the
`4x8` matrix whose columns are `(1,v)` for the eight cube vertices. The
polyhedral cone `K=cone{(1,x):x in cube}` equals `R R_+^8`. Therefore
`B=R^T A R` is copositive. The matrix `R` has rank four.

Suppose all zeros of `q` are contained in an affine plane `ell(x)=0`,
with nonzero homogeneous coefficient vector `l`. Set `w=R^T l!=0`.
For every nonzero zero `u>=0` of `B`, put `t=sum u_i>0`. Then
`Ru=t(1,x)` for a cube point `x`, and

`0=u^T B u=t^2 q(x)`.

Thus `w^T u=l^T Ru=t ell(x)=0`. The zero vector also satisfies this
identity. Hildebrand's rank-one criterion gives `B-epsilon w w^T` copositive.
Because every element of `K` has a nonnegative vertex representation,
this is equivalent to `q-epsilon ell^2>=0` on the cube. If `q` is extreme,
the decomposition

`q=(q-epsilon ell^2)+epsilon ell^2`

forces `q` to be an affine square. Hence a non-square extreme quadratic
must have zeros affinely spanning all of `R^3`.

## 2. Stationary PSD-facet lemma

**Lemma.** Suppose `q` is cube-nonnegative, its square coefficients and all
three mixed coefficients are positive, and all vertex values are positive.
Suppose a facet restriction has a PSD quadratic coefficient matrix and a
zero stationary in both facet coordinates. Then either `q` is not extreme
in `P3` or `q` is an affine square.

By simultaneous complementation of all three coordinates if necessary,
take the facet to be `z=0`. This preserves positivity of all mixed
coefficients. The stationary point `u0=(x0,y0)` is not a corner, because
vertex values are positive. It is allowed to be an edge point of the facet.
All zeros of `q` are shown below to be contained in an affine plane.

### 2a. Positive-definite facet block

Write

`q(u,z)=(u-u0)^T A(u-u0)+2z v^T(u-u0)+gamma z+t z^2`,

where `A=[[a,c],[c,b]]` is positive definite, `a,b,c>0`,
`v=(r,s)>0`, `t>0`, and `gamma>=0`. The latter is the inward derivative
at the zero. If the full `3x3` matrix is PSD, this is already a sum of
affine squares and a nonnegative multiple of `z`; an extreme ray with
positive square coefficients must be an affine square. Otherwise its
Schur complement

`S0=t-v^T A^{-1}v`

is negative.

For each `z in [0,1]`, let `u(z)` be the unique minimizer over `[0,1]^2`
and let `F(z)=q(u(z),z)`. Then `F>=0`, `F(0)=0`, and every zero of `q`
is of the form `(u(z),z)` with `F(z)=0`. The function `u` is continuous
and piecewise affine, and `F` is continuously differentiable and piecewise
quadratic. These facts follow directly from the active-set formulas below:
free gradients vanish, fixed coordinates have zero derivative, and the
formulas agree at each active-set transition, so `F'=partial_z q` agrees
there as well.

The unconstrained velocity is

`u'_1=(c s-b r)/(ab-c^2)`,

`u'_2=(c r-a s)/(ab-c^2)`.

Both components cannot be positive. If both are nonpositive, the minimizer
starts free, reaches a lower edge, and then reaches `00`; some phases can
be absent. Once coordinate 1 is fixed at zero, coordinate 2 decreases
with velocity `-s/b`, while the gradient of coordinate 1 increases with
velocity `r-cs/b>=0`. Hence that lower bound never releases. The other
coordinate choice is symmetric.

If coordinate 1 initially increases, then `cs>br`. Coordinate 2 decreases.
If coordinate 2 reaches zero first, coordinate 1 immediately decreases
with velocity `-r/a`, and the lower-bound gradient for coordinate 2
increases with velocity `s-cr/a>0`. The path is then a lower edge followed
by `00`. If coordinate 1 reaches one first, the path is

`free -> x=1 -> 10 -> y=0 -> 00`.

On `x=1`, coordinate 2 decreases with velocity `-s/b`, while the
upper-bound gradient for coordinate 1 decreases with velocity
`r-cs/b<0`, so it stays at one until coordinate 2 reaches zero. At `10`,
the lower-bound gradient for coordinate 2 increases with velocity `s>0`,
while the upper-bound gradient for coordinate 1 increases with velocity
`r>0`. The latter may reach zero and release coordinate 1. On the following
edge `y=0`, coordinate 1 decreases with velocity `-r/a`, and coordinate 2
stays at zero because `s-cr/a>0`. These inequalities use `ab>c^2`:
`cs>br` implies `s>br/c>cr/a`.

An initial stationary point on the boundary produces a truncation of
these same paths. If the unconstrained velocity points outward through a
lower bound, the free coordinate immediately decreases and that lower
bound remains active. If it points outward through an upper bound, the
path starts with the corresponding upper-edge phase. If it points inward,
the free phase starts immediately. No additional active-set path is
possible. Simultaneous transitions merely remove a phase.

On a free phase, `F''/2=S0<0`. On a phase with coordinate 2 free,
`F''/2=Sy=t-s^2/b`; with coordinate 1 free it is
`Sx=t-r^2/a`; at a corner it is `t>0`. In the upper-edge path above,

`Sx>Sy`,

because `cs>br` and `ab>c^2` imply `r^2/a<s^2/b`. Consequently the
curvature sequence is

`S0, Sy, t, Sx, t`, with `S0<0` and `Sx>Sy`.

The simple lower-edge path has sequence `S0, Sx, t` or `S0, Sy, t`.
These sequences show that the zeros of `F` for `z>0` are either at most
two isolated points or one interval:

- A strictly concave quadratic piece has no zero in its relative interior
  on which `F>=0`; a zero at `z=1` can only be the final zero.
  At an interior phase transition, any zero also has `F'=0` because `F`
  is differentiable and nonnegative. A neighboring piece with strictly
  negative curvature would then give negative values immediately on that
  side, so such a transition cannot be a zero. Thus phase endpoints do
  not introduce additional zeros beyond the counts below.
- If `Sy>=0`, every piece after the first upper-edge piece has nonnegative
  curvature. If `Sy<0` and `Sx>=0`, every piece after the first corner has
  nonnegative curvature. A nonnegative convex differentiable function has
  one connected zero set on such a tail.
- If `Sx<0`, both free edge pieces are strictly concave; only the two
  strictly convex corner pieces can contain interior zeros, and each has
  at most one. A final endpoint zero on a concave piece gives at most one
  additional zero after the first corner, for a total of two.
- A zero interval requires one free-edge curvature to be zero. If `Sy=0`,
  then `Sx>0`, so the later pieces cannot have another zero. If `Sx=0`,
  the preceding corner meets the zero interval with value and derivative
  zero; its unique zero is that endpoint. Thus no other isolated zero or
  zero interval accompanies a flat interval. The lower-edge path has the
  same simpler property.

Across a zero interval, `u(z)` is affine on a single free-edge phase;
the neighboring strictly convex corners cannot extend the interval.
Thus the corresponding zeros of `q` form a straight segment. The zeros
on `z=0` consist only of `(u0,0)`. All zeros of `q` are therefore contained
in an affine plane: the base point and at most two points, or the base
point and one straight segment. The rank-one subtraction transfer proves
the lemma in this case.

### 2b. Rank-one facet block

The positive diagonal and mixed coefficients imply that the PSD block has
the form `[d1,d2]^T[d1,d2]`, with `d1,d2>0`. Its stationary zero gives

`q=(d1 x+d2 y-h)^2+2z(r x+s y+gamma)+t z^2`,

where `r,s,t>0` and `0<h<d1+d2`. The base zero set is the segment
`d1 x+d2 y=h`, `z=0`. Positive vertex values exclude the degenerate
endpoint choices `h=0,d1,d2,d1+d2`.

Set `lambda1=r/d1`, `lambda2=s/d2`, and first suppose
`lambda1<lambda2`. For fixed weighted sum `S=d1 x+d2 y`, the term
`r x+s y` is minimized by using coordinate `x` first. Its value is

`J(S)=lambda1 S` for `0<=S<=d1`,

`J(S)=lambda1 d1+lambda2(S-d1)` for `d1<=S<=d1+d2`.

For every `z>0`, this allocation is unique. The remaining minimization is

`F(z)=min_{0<=S<=d1+d2} (S-h)^2+2z[J(S)+gamma]+t z^2`.

If `h<d1`, the path is `y=0 -> 00`. If `h>d1`, it is

`x=1 -> 10 -> y=0 -> 00`,

with weighted-sum positions `S=h-lambda2 z`, `S=d1`,
`S=h-lambda1 z`, and `S=0`, respectively. The respective curvatures
`F''/2` are `t-lambda2^2`, `t`, `t-lambda1^2`, and `t`, and the second
free-edge curvature is strictly larger than the first. The preceding
zero-count argument gives at most two isolated outside zeros or one flat
interval. Two isolated outside zeros could occur only with the first
corner zero and a negative subsequent free-edge curvature. More explicitly,
with both free-edge curvatures negative, the first zero would have to be
in the `10` corner phase, and the second would have to follow the intervening
cheap-coordinate phase, in `00` or at the terminal boundary `z=1`.
If the cheap-coordinate curvature were nonnegative, the value function
would be convex from the first corner onward and these two zeros could
only belong to one connected zero set, not two isolated zeros.

That possibility is excluded by the corner's inward derivative. At a
zero `(1,0,zA)`, vertex positivity makes `zA` an interior edge position.
The vertical restriction is a nonnegative quadratic with a double zero,
so, with `d3=sqrt(t)`,

`zA=(h-d1)/d3`.

The derivative into the cube in coordinate `x` is nonnegative, giving

`d1(d1-h)+r zA<=0`, hence `lambda1<=d3`.

Thus the subsequent free-edge curvature is nonnegative, a contradiction.
There is at most one isolated outside zero, or one straight zero segment.

The base segment and an isolated point lie in an affine plane. An outside
zero segment on `y=0` requires its restriction to be an affine square:

`r=d1 d3`, `gamma=-h d3`,

and its zeros satisfy `d1 x+d3 z=h`. An outside zero segment on `x=1`
similarly requires

`s=d2 d3`, `r+gamma=-(h-d1)d3`,

and its zeros satisfy `d2 y+d3 z=h-d1`. In either case, the base segment
and outside segment are contained in the same plane

`d1 x+d2 y+d3 z=h`.

If `lambda2<lambda1`, interchange coordinates and apply the same proof.

Finally suppose `lambda1=lambda2=lambda`. The polynomial depends on
`x,y` only through `S`, and its minimizing weighted sum is
`S(z)=max(h-lambda z,0)`. On the free-sum phase,

`F(z)=2(gamma+lambda h)z+(t-lambda^2)z^2`.

An interior positive `z` zero on this phase forces that polynomial to
vanish identically, because `F>=0` and an interior zero has derivative
zero. Then `gamma=-lambda h`, `t=lambda^2`, and `q` itself is the affine
square `(S+lambda z-h)^2`. Otherwise the free-sum phase can have a zero
only at the final boundary `z=1`; all corresponding points lie in the
plane `S+lambda z=h`. After `S(z)` reaches zero, the minimizer is `00`
and the positive-curvature quadratic has at most one zero. There cannot
be both an upper-facet free-sum zero and a later corner zero within
`[0,1]`. Thus in the non-square case the base segment is accompanied by
one point, or by one coplanar upper-facet segment. This again puts every
zero in an affine plane and proves the lemma.

## 3. Deduction of the strengthened classification

Take a non-square extreme ray with the three hypotheses in the proposed
theorem. Complement a coordinate to make all mixed coefficients positive.

An interior cube zero makes the full Hessian PSD; the Taylor expansion is
then a PSD quadratic form, contradicting non-square extremality. A
facet-interior zero makes its facet block PSD and is stationary in both
facet coordinates, contradicting the new stationary PSD-facet lemma.

Every zero therefore lies in an edge interior. If a derivative into an
adjacent facet vanished, that facet restriction would be stationary in
both its coordinates. Its `2x2` block must be PSD: the free edge coordinate
admits both signs, and any negative quadratic direction can be reversed
to point inward in the other coordinate. The new lemma again contradicts
non-square extremality. Thus every edge zero has strictly positive inward
derivatives.

The earlier perturbation argument now forces at least five edge contacts,
without any pair-minor hypothesis. Every step of its contact-graph
classification remains valid without that hypothesis:

- Two incident edge contacts force the local mixed coefficient to be at
  least `2 di dj`, so they still stay between adjacent Hamming levels.
- Three incident contacts decompose the quadratic into an affine square
  and nonnegative products; either it is the square or it is not extreme.
  Strict positivity of all three product coefficients is unnecessary.
- The central-cycle decomposition and the three impossible graph cases
  used only nonnegativity, positive mixed coefficients, and vertex positivity.
- The remaining family graph gives `k>0` directly from a strictly positive
  inward derivative, so every pair principal determinant is then negative.

Thus the non-square extreme ray is exactly a symmetry copy of the strict
five-contact family. A purported extreme ray in the nonnegative-pair-minor
regime with no vertex zero is therefore an affine square in `D3`.

For extreme rays of `P3+` with all square coefficients positive, the
existing manuscript bridge applies: they are also extreme in `P3`, because
small two-sided nonnegative decompositions retain positive diagonal
coefficients. The new reduction therefore applies to the completeness
question's extreme rays as well.

## 4. Remaining boundary

Vertex-zero extreme rays remain unclassified. The proved family boundary
strata account for many such rays, but the present argument does not show
they exhaust that regime. In particular, this continuation does not prove
the full capped-family completeness conjecture.

The active-set proof and zero-set geometry above are the new mathematical
content to review. Hildebrand supplies only rank-one subtraction, not the
parametric minimizer paths, zero counts, or cube-ray classification.

## 5. Targeted algebra actually checked

A one-off SymPy command verified both rank-one outside-flat restriction
identities and the aligned-cost free-sum value formula. It printed
`PSD-facet continuation identities: PASS`. This was symbolic coefficient
comparison for the new argument, not a rerun of any archived experiment.

## 6. All-sign extension from the already verified BNW theorem

The root identified a further short consequence of the existing BNW
exactness input. For a nonpositive mixed-product, complement coordinates
to make all mixed coefficients nonpositive. The BNW SDP
`M(m,Y)>=0, Yij<=mi` is compact: PSD and the diagonal inequalities imply
`0<=mi<=1`, and PSD bounds all second moments. The uniform cube moments
`mi=1/2,Yii=1/3,Yij=1/4` are strictly feasible. Hence Slater gives dual
attainment and the polynomial identity

`q=qmin+(1,x)^T Z(1,x)+sum_ordered(i,j) lambdaij xi(1-xj)`,

with `Z PSD`, `lambda>=0`, and `qmin>=0`. The ordered sum includes
diagonal caps; its mixed coefficient is `-lambdaij-lambdaji`, consistent
with the manuscript's full polynomial-coefficient convention.

For an extreme ray positive at every vertex, every product/cap summand
must be zero, since it vanishes at a vertex and cannot be proportional to
`q`. A nonzero constant cannot be proportional to a quadratic with all
positive square coefficients. Splitting the PSD term into affine squares
therefore makes `q` an affine square. Consequently the non-square ray
must have positive mixed-product, and the facet/contact proof applies.

The independent continuation reviewer confirmed compactness, strict
feasibility, dual signs, ordered multiplier convention, and the extremality
argument. `05b` now omits the mixed-product hypothesis entirely, and
Appendix E includes the full short SDP-dual proof. No main or build was
changed. This adds no new literature dependency.
