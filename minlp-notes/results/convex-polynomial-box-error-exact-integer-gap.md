# Exact binary and general-integer counts for convex polynomial graphs

Date: 2026-09-05. Status: proved and independently reviewed twice.
The mathematical results in this note, including the monotone affine shear,
are [formally verified in Lean 4](../formal/topics/00-exact-counts/README.md).
The [completion record](../formal/topics/00-exact-counts/VERIFICATION.md)
records the September 11 verification; the
[coverage record](../formal/COVERAGE.md) states the exact scope. This excludes
literature attribution, novelty, open-problem status and the historical
checker's experiment counts.
The restricted example and exact count law are a candidate new supporting
result; bounded source searches found no matching statement. The residue
argument, product construction, and finite disjunction are classical.

For every `n>=1`, define the polynomial map on `[0,1]^n`

```
F_n(x)=( (7/4)(1-x_i)^32, (7/4)x_i^32 )_(i=1,...,n).
```

Every component is convex. Approximate this graph with unit componentwise
vertical error: the projected feasible set must contain every
`(x,F_n(x))`, must have `x in [0,1]^n`, and every admitted `(x,w)` must
satisfy `|w_j-F_(n,j)(x)|<=1`.

Let `p_conv` be the minimum number of integer coordinates among all such
formulations obtained by intersecting a convex lifted set with integer
constraints and projecting out auxiliary variables. Let `p_bin` be the
corresponding minimum when those coordinates are binary. Arbitrary finite
continuous dimension and arbitrary integer ranges are allowed. The
convex set need not be polyhedral; imposing closedness does not change
the result below. Formulation size is unrestricted in these two minima.

**Theorem.** The exact counts are

```
p_conv(F_n)=n,       p_bin(F_n)=ceil(n log2 3).
```

Both upper bounds have rational MILP realizations. The general-integer
realization uses `3n` continuous auxiliaries and `13n` inequalities;
the binary realization used here may have exponentially many continuous
variables and rows. Polynomial degree, error tolerance, and numerical data
in the general-integer construction are fixed independently of `n`.
The linear size claim concerns variable and row counts; it does not assert
linear serialized bit length or a solver running-time bound.

## 1. A rational one-integer formulation for one coordinate

Put

```
A=7/4, c=1/48, L=A(1-c)^32, d=A c^32,
Q(x)=(A(1-x)^32,A x^32).
```

We use the inequalities

```
A-1<L<1,      d<1/4,      (A+d)/2<1.                 (1)
```

These have elementary rational proofs. Bernoulli's inequality gives
`(47/48)^16>=2/3`, so `L>=7/9>3/4=A-1`. The binomial expansion gives
`(48/47)^32>=1+32/47+496/47^2>7/4`, proving `L<1`.
Finally `d< (7/4)/48 <1/4`, proving the other two bounds.

Define three boxes in `(x,w_1,w_2)`:

```
B_0=[0,c]     x [L,A] x [0,d],
B_1=[c,1-c]   x [0,L] x [0,L],
B_2=[1-c,1]   x [0,d] x [L,A].
```

Each contains the graph over its designated input interval. Each is
already within unit graph error: on an outer interval the component
ranges have widths `A-L<1` and `d<1`, and on the middle interval both
true and admitted outputs belong to `[0,L]`.

Append labels zero, one, and two, respectively, and set

```
C=conv( (B_0 x {0}) union (B_1 x {1}) union (B_2 x {2}) ).
```

This is a rational polytope. Impose that its last coordinate `z` is
integer. At `z=0` and `z=2`, only the respective box is possible. At
`z=1`, consolidate the contribution from each box into one point of
that box. The weights must be `t,1-2t,t`, with `0<=t<=1/2`.
The smallest possible input is

```
(1-2t)c+t(1-c)=c+t(1-3c)>=c;
```

symmetry bounds the largest input by `1-c`. Every admitted output lies
between zero and

```
(1-2t)L+t(A+d) <= max(L,(A+d)/2)<1.
```

Every true output at the admitted input is in `[0,L] subset [0,1)`.
Thus the entire integer slice has strict unit error, including points
created by mixing different boxes. Every exact graph point belongs to
one of the three labeled boxes, so containment also holds.

For an explicit formulation, write `B_j=[ell_j,u_j]` coordinatewise in
`v=(x,w_1,w_2)`. Introduce three continuous weights and impose

```
lambda_j >= 0                 (j=0,1,2),
lambda_0+lambda_1+lambda_2 = 1,
z = lambda_1+2 lambda_2,
sum_j lambda_j ell_(j,k) <= v_k <= sum_j lambda_j u_(j,k)
                              (k=1,2,3).
```

For fixed weights, the weighted sum of the boxes is exactly the box with
these weighted endpoints: each coordinate ranges independently over the
sum of its weighted intervals. Thus projection onto `(v,z)` gives exactly
`C`. Only `z` is integer. There are nine inequalities and two equalities,
or thirteen inequalities after replacing each equality by two inequalities.
Products use `3n` continuous auxiliaries and `13n` inequalities, with all
rational coefficients drawn from a fixed finite set independent of `n`.

## 2. Three pairwise incompatible exact contacts

Consider exact graph contacts at inputs `0,1/2,1`. Every pair admits a
convex combination with weights `1/3,2/3` that violates unit error.
For the pair `0,1/2`, give weight `2/3` to zero. At input `1/6`, the
first-component chord error is

```
g=(2/3)A+(1/3)A/2^32-A(5/6)^32>1.                 (2)
```

Indeed `4*5^8<6^8`, hence `(5/6)^32<1/256`, and
`g>7/6-7/1024>1`. The pair `1/2,1` has the symmetric obstruction in
component two, with weight `2/3` on one. For the pair `0,1`, give weight
`2/3` to zero; the first-component error at `1/3` is

```
(2/3)A-A(2/3)^32 >7/6-7/1024>1.                  (3)
```

These are errors of convex combinations of exact contacts. Therefore
they invalidate any admissible projected convex fiber containing the
two contacts, regardless of its auxiliary dimension.

## 3. Exact general-integer count

Taking the product of the one-coordinate formulations gives
`p_conv(F_n)<=n`.

For the reverse bound, take the `3^n` exact contacts with inputs in
`{0,1/2,1}^n`. In any admissible convex lift with `p` integer coordinates,
choose one lifted representative of each contact and its integer code.
If two codes agree modulo three, both combinations with weights
`1/3,2/3` have integer codes and lie in the convex lifted set.
The two inputs differ in some coordinate. Equations (2)--(3), choosing
the required orientation, show that one of those combinations violates
unit error in that coordinate's output pair. This is impossible.

The `3^n` chosen integer codes must therefore have distinct residues in
`(Z/3Z)^p`. Consequently `3^n<=3^p` and `p>=n`. The argument places no
bound on the magnitude of any integer coordinate.

## 4. Exact binary count

Two exact contacts with the same binary code have every convex
combination in the same feasible binary fiber. The pairwise obstruction
above therefore forces distinct binary codes for all `3^n` contacts.
Thus `p_bin(F_n)>=ceil(log2(3^n))`.

For equality, choose one of the `3^n` products of the three boxes with
distinct codes in `{0,1}^p`, where `p=ceil(log2(3^n))`. Take the convex
hull of the coded product boxes and impose integrality of the code.
A binary vector is an extreme point of the unit cube, so a convex
combination producing that vector can use only boxes with that same
code. Every admitted integer slice is precisely its selected product
box. This is a finite rational polyhedral formulation, contains the
graph, and has unit error. It proves the matching upper bound.

## 5. Meaning and limits

Already for one input and two convex polynomial outputs, one general
integer suffices while two binaries are necessary. Products give the
linear gap

```
p_bin-p_conv=ceil(n log2 3)-n.
```

This shows that an additive allowance proportional to input dimension
cannot always be removed when comparing binary constructions with the
best general-integer convex lift, even for fixed-degree componentwise
convex polynomials and an ordinary box error body. It does **not**
establish an unbounded gap with one input and a growing number of
outputs. That more specific question remains open in this repository.

If componentwise monotonicity is desired, add the affine function `56x_i`
to each first output. Its derivative then becomes
`56[1-(1-x_i)^31]>=0`. An invertible affine shear of `(x,w)` preserves
the error differences and all count arguments, including the closed-lift
minima. Substituting the shear in the displayed formulation preserves its
`3n` auxiliary and `13n` inequality counts. This does not produce nonnegative
monomial coefficients in the original input coordinates: the first output's
cubic coefficient is `-8680`. These statements are included in the completed
Lean verification (`monotone_exact_box_counts` and
`monotoneLeftPoly_coeff_three`).

## 6. Attribution and verification

Residue counting extends the classical midpoint obstruction of Lubin,
Vielma, and Zadik, [*Mixed-integer convex representability*](https://optimization-online.org/wp-content/uploads/2017/06/6082.pdf),
Lemma 4.1. The same source's binary representability discussion gives
the finite-convex-fiber viewpoint. No novelty is claimed for replacing
parity by modulus three, taking products, or encoding finite disjunctions.
The proposed contribution is the explicit fixed-degree convex graph
family with fixed box error and both exact minimum counts. The bounded
comparison is in
[the source note](../notes/convex-polynomial-box-gap-exact-counts-novelty.md).

Independent proof reviews:

- [Binary formulation reviewer](../notes/review-convex-vector-one-bit-box-gap.md),
  including the final constants and modulo-three product lower bound.
- [Root review](../notes/review-convex-vector-box-gap-root.md), including
  the full mixed middle slice and both exact product counts.

The [independent exact checker](../code/positive_vector_obstruction/check_box_gap_root.py)
passed the constant inequalities, 72 middle-slice candidate vertices,
2,048 rational mixtures, and 390 product-contact pairs. The proofs above
cover all real mixtures and all dimensions; these finite checks are
supplementary. Earlier hinge and polynomial variants remain in
[the investigation note](../notes/convex-vector-one-bit-box-gap-investigation.md).
