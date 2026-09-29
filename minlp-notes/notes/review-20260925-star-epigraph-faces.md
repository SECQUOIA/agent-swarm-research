# Independent review of the star epigraph exposed-face result

Date: 2026-09-25.

Reviewed: [A limit on face-based lower bounds for quadratic indicator
stars](research-20260925-star-epigraph-faces.md).

**Assessment:** the proposition, bounded-face corollary, and stated
limitation on face-based extension-complexity transfers are correct under
the stated assumptions. The result is a modest structural observation.
It does not give a compact
formulation, a lower bound, or a new optimization algorithm for the full
epigraph hull. Publication priority remains unresolved.

This review independently checked the closure argument, the scalar
minimizer count, the treatment of tied indicators, and the linear extended
formulation. A separate adversarial subreview checked the scalar argument
and tie degeneracies. No substantive proof gap was found. The wording
distinction between original root-off cube vertices and their convex hull
was corrected in the final draft. The final revised draft, including the
bounded-face lemma and rational four-minimum example, was read in full.

## Closure and exposed-face equality

Write `S_Q` for the original mixed-integer epigraph set and
`L=t-2c^T x+delta^T z`. For each binary support `z`, let `x^z` be its unique
continuous minimizer and `m_z` its minimum objective value. With
`m=min_z m_z`, stationarity on the active coordinates gives, for every
point of `S_Q`,

```
L(z,x,t)-m = (m_z-m) + (x-x^z)^T Q(x-x^z) + (t-x^T Qx).
```

All three terms are nonnegative. Consequently `L>=m` on the closed convex
hull, and equality is attained by some support minimizer.

For a convergent sequence of convex combinations with objective tending
to `m`, the total weight on nonoptimal supports tends to zero: there are
finitely many support values, so their strictly positive gaps have a
positive minimum when any such supports exist. If `mu=lambda_min(Q)>0`,
the average displacement from the corresponding `x^z` has norm at most
`sqrt((L-m)/mu)`. Thus the limiting `(z,x)` is a convex combination of
optimal support minimizers. Finally, `L=m` determines `t` affinely. This
rules out extra face points produced only by closure, including sequences
with small weights on unbounded original points.

This argument uses no star structure and is valid for every
positive-definite `Q`. It does not require first proving that `conv(S_Q)`
is closed.

## Scalar minimizers and ties

After fixing an active root at `r`, each leaf contributes

```
min{0, delta_i-(c_i-b_i r)^2/d_i}.
```

On each interval of fixed signs, the total objective is a quadratic with
leading coefficient at least `a-sum_i b_i^2/d_i>0`. The draft's argument
using at most `2n+1` closed intervals is valid even with repeated roots,
double roots, identically zero terms, and zero couplings. Counting closed
intervals does not accidentally double the number of possible minimizers:
each interval contains at most one distinct global minimizer, and their
union covers the real line.

An alternative argument removes ineffective roots. Only leaves with
`b_i!=0` and `delta_i>0` create actual switching points. At either endpoint
of their inactive interval, the one-sided derivative jump is

```
-2 |b_i| sqrt(delta_i/d_i).
```

All simultaneous jumps are downward. Such a point cannot be a local
minimum, because that would require the left derivative to be nonpositive
and the right derivative to be nonnegative. This also proves the stated
tie characterization:

- A coupled leaf can tie at a minimizing root only when `delta_i=0` and
  `c_i-b_i r=0`. Both choices then have continuous coordinate zero.
- An uncoupled leaf can tie identically when `delta_i=c_i^2/d_i`; its
  active continuous coordinate can be nonzero.

Each tied indicator is independent of the others at a fixed root. The
original minimizers are the vertices of the affine cube given by
`x_i=z_i(c_i-b_i r)/d_i`, together with the affine equation
`t=m+2c^T x-delta^T z`. Keeping the `z_i` coordinates ensures that the
cube directions remain independent even when a continuous coordinate is
zero. The root-off branch supplies the convex hull of one further group
of independent binary choices. A branch contributes only when its minimum
equals the global value `m`.

The disjunctive formulation with `lambda_j>=0` and
`0<=w_ji<=lambda_j` is exact, including when `lambda_j=0`. With at most
`2n+2` cube images, each of dimension at most `n`, it uses at most
`(2n+2)(2n+1)` scalar inequalities as claimed.

## A sharper count and a counterexample to an overly strong count

The bound in the proposition can safely remain as written. A minor
sharpening is available. Let `I={i:b_i!=0, delta_i>0}` and let `B` be its
distinct switching endpoints. If `I` is empty, the scalar objective is a
single strictly convex quadratic and has one minimizing root. Otherwise,
the two unbounded intervals have the same quadratic formula and can
together contain at most one minimizer. There are therefore at most
`|B|<=2|I|<=2n` minimizing root values.

A bound of `n+1` is false. Take two leaves and set

```
Q = [[9/4,1,1], [1,1,0], [1,0,1]],
c_0=delta_0=0,
(c_1,delta_1)=(-2,36/5),
(c_2,delta_2)=(1,9/5).
```

The root-active support quadratics for leaf supports empty, `{1}`, `{2}`,
and `{1,2}` are respectively

```
(9/4)r^2,
(5/4)(r-8/5)^2,
(5/4)(r+4/5)^2,
(1/4)(r-4)^2.
```

They are all nonnegative and each attains zero at a different root. Their
lower envelope therefore has four distinct global minimizers. The matrix
is positive definite: its leading principal minors are `9/4,5/4,1/4`,
and its star Schur complement is `1/4`.

The following targeted exact check was run successfully:

```bash
python - <<'PY'
import sympy as s
r=s.symbols('r', real=True)
a=s.Rational(9,4)
actual=[a*r*r, a*r*r+s.Rational(36,5)-(-2-r)**2,
        a*r*r+s.Rational(9,5)-(1-r)**2,
        a*r*r+s.Rational(36,5)-(-2-r)**2+s.Rational(9,5)-(1-r)**2]
expected=[a*r*r,s.Rational(5,4)*(r-s.Rational(8,5))**2,
          s.Rational(5,4)*(r+s.Rational(4,5))**2,s.Rational(1,4)*(r-4)**2]
assert all(s.expand(x-y)==0 for x,y in zip(actual,expected))
Q=s.Matrix([[a,1,1],[1,1,0],[1,0,1]])
assert [Q[:i,:i].det() for i in range(1,4)]==[s.Rational(9,4),s.Rational(5,4),s.Rational(1,4)]
assert len({0,s.Rational(8,5),-s.Rational(4,5),4})==4
print('Exact rational identities passed: four distinct global minima and positive-definite Q.')
PY
```

This verifies the algebraic identities and the stated matrix test. The
nonnegativity and global-minimum conclusion follow from the displayed
squares. It does not verify the general theorem or establish novelty.
No project-wide tests or CI checks were run for this review.

The author's focused enumeration command,
`python code/check_star_epigraph_faces.py`, separately passed 77 cases and
3,232 exact support checks, as recorded in the research note. That
enumeration was not rerun in this review; the independent exact check
above verifies the rational four-minimum example directly.

## Independent check of the bounded-face strengthening

The author subsequently proposed extending the conclusion to every
nonempty bounded face, including nonexposed faces. This extension is
valid. A fresh adversarial subreview checked the argument independently.
The following proof avoids an unnecessary intermediate claim about the
closed convex hull of restricted supports.

First, for any positive-definite `Q`, every point of `H_Q` satisfies

```
x_i^2 <= z_i t / mu,    mu=lambda_min(Q)>0.
```

For a convex combination of original points, restrict the weighted sum
defining `x_i` to points with `z_i=1` and apply Cauchy--Schwarz. Their total
weight is the resulting `z_i`, and their weighted squared coordinates are
at most `t/mu`. The inequality passes to closure. In particular, `z_i=0`
still implies `x_i=0` throughout the closed hull. This fact is needed
below to describe which coefficients can affect a functional on a
coordinate face.

Let `F` be a nonempty bounded face and choose `u` in its relative interior.
Let `A` and `B` be the indicator coordinates at which `u` has value zero
and one, respectively. Define

```
p(z)=sum_(i in A) z_i + sum_(i in B)(1-z_i),
G=H_Q intersect {p=0}.
```

Because `p>=0` on `H_Q` and `u` is in the relative interior of `F`, the
entire face `F` lies in `G`. The set `G` contains upward vertical rays and
is unbounded. If `u` were in the relative interior of `G`, the face
property would force `F=G`, contradicting boundedness. Therefore `u` is
on the relative boundary of the closed convex set `G`, and there is a
supporting affine functional `h`, nonconstant on the affine hull of `G`,
that attains its minimum at `u`.

Its coefficient on `t` cannot be negative, because of the vertical rays.
Suppose that coefficient were zero. The original support with all
indicators outside `A` set to one allows arbitrary continuous values in
all coordinates outside `A`; hence their coefficients in `h` must vanish.
The coordinates in `A` have continuous value zero throughout `G`, by the
inequality above. The indicator projection of `G` is the full cube with
the coordinates in `A` and `B` fixed: all its binary vertices occur with
`x=0,t=0`. Every free indicator of `u` is strictly between zero and one.
Thus a linear indicator objective minimized there must have zero
coefficient on every free indicator. The functional would be constant on
`G`, a contradiction. Its `t` coefficient is therefore positive; scale it
to one.

For every binary support `z`, let `m_z` be the minimum of `h` on that
support. All these minima are finite and attained by positive
definiteness. Let

```
m_A=min{m_z:p(z)=0}.
```

Choose a finite `M>=0` such that `m_z+M p(z)>=m_A` for every binary
support. This is possible because there are finitely many supports and
`p(z)>=1` whenever it is positive. Then `h+Mp>=m_A` on the original set
and, by continuity, on `H_Q`. It agrees with `h` on `G`, and an allowed
support attains `m_A`. Therefore `min_G h=m_A=h(u)`. The exposed face of
`H_Q` minimizing `h+Mp` has positive `t` coefficient and contains `u`;
since `u` is in the relative interior of `F`, it contains all of `F`.

The containment lemma holds for every positive-definite `Q` with
unconstrained indicators. For a star, the containing exposed face is a
polytope with the proved quadratic-size LP extended formulation. The
original `F` is a face of that polytope and inherits such a formulation
by adding a face equality. This also shows that these bounded faces are
closed polytopes, even if closedness was not included in the initial
definition of a face.

## Scope and significance

The positive coefficient on `t` is necessary in the exposed-face statement.
Faces exposed with zero `t` coefficient can retain a curved quadratic
epigraph and need not be polytopes. The bounded-face lemma covers
nonexposed bounded faces by placing them inside positive-weight exposed
faces; it does not claim that every face is exposed. Additional constraints on the
indicators can invalidate the independent leaf choices. The note
correctly avoids claiming either extension to positive-semidefinite
matrices or a single formulation covering every exposed face at once.

The result blocks a particular transfer of a hard polytope through these
exposed faces and their affine images. It does not block a different
reduction, a hard affine section, or another route to a lower bound for
the full hull. Small formulations of individual faces need not combine
into a small global formulation.

The literature comparison is appropriately cautious. The
[2025 tree optimization paper](https://doi.org/10.1007/s10107-025-02222-3)
already establishes polynomial optimization on arbitrary trees, so the
elementary star minimization is not itself a new algorithmic result. The
full text of [Choi et al., Section 7.2](https://arxiv.org/html/2608.22815v1#S7.SS2)
was independently checked: its tree formulation has size `O(n^(k+1))`
with `k` leaves, and its remark explicitly identifies stars as a case
where that bound is exponential. Neither source check establishes that
the present exposed-face statement is new.
