# A scalar leader with a diagonal strictly convex follower on a path

Date: 2026-09-05. Status: two independent written proof audits PASS;
exact lower-QP certificates also passed.

The Klee–Minty vertex certificate gives a precise obstruction to replacing
independent follower blocks by scalar blocks coupled along a path. The
leader has one scalar variable. The follower has a diagonal positive
definite quadratic objective and a fixed feasible path polytope described
by two-variable linear inequalities. The upper level retains one
**nonconvex quadratic constraint** and one scalar aggregate slab. The
restricted feasibility problem below is NP-complete. This is not an
all-linear-upper-level hardness theorem, and broad scalar-leader bilevel
hardness is already known.

## 1. The follower and its vertex responses

Use the notation of the
[reviewed Klee–Minty slab construction](klee-minty-rank-one-slab-hardness.md).
For positive integer weights `w_i`, let `W=sum_i w_i`,
`epsilon=1/(8W)`, and define the fixed follower polytope

```
P = { z : z_0=0,
      epsilon*z_(j-1) <= z_j <= 1-epsilon*z_(j-1), j=1,...,n }.
```

The convention `z_0=0` introduces no variable. Put

```
c_j=(1-epsilon)epsilon^(2(n-j)-1), j<n;  c_n=0,
L(z)=z_n-c^T z,
F(z)=L(z)-z_n^2.
```

The telescoping identity proves `F>=0` on `P`, with equality exactly
at its `2^n` vertices. Distinct vertices have distinct terminal
coordinates. Their coordinates have denominators dividing
`D=(8W)^(n-1)`, so distinct terminal values differ by at least `1/D`.
Define

```
Delta=D^(-2),       tau=Delta/(2n).
```

For a scalar leader decision `lambda in [-1,1]`, the follower solves

```
minimize   tau/2 * ||z||_2^2 - c^T z - lambda*z_n
subject to z in P.                                           (Q_lambda)
```

Its Hessian is `tau*I`, hence positive definite. Its feasible set is
nonempty and compact for every leader decision and is independent of
that decision. The unique follower response is consequently defined for
every `lambda`. The parameter occurs only in the linear coefficient of
the final coordinate; all lower constraints have at most two variables,
and their variable-interaction graph is a path.

**Vertex-response lemma.** Every vertex `v` of `P` is the unique
follower response at `lambda_v=2v_n-1`.

To prove it, first use the parabolic exposing identity. At every other
vertex `u`,

```
(c^T v+lambda_v*v_n)-(c^T u+lambda_v*u_n)
 = (u_n-v_n)^2 >= Delta.                                    (1)
```

For any `z in P`, choose a vertex decomposition
`z=sum_u alpha_u u`, and put `a=sum_(u!=v)alpha_u`. Linearity of
the score and (1) give score loss at least `Delta*a`. Since all
coordinates of all vertices lie in `[0,1]`,

```
||z-v||_infinity <= a,
||z||_2^2-||v||_2^2
 = 2v^T(z-v)+||z-v||_2^2 >= -2n*a.
```

The follower objective difference between `z` and `v` is therefore
at least

```
Delta*a-tau*n*a = Delta*a/2.
```

If `z!=v`, then `a>0`, proving uniqueness. The proof does not require
enumerating the vertices when constructing an instance.

The vertex persists on a nontrivial leader interval. If the parameter
changes by `h`, then the objective difference changes by
`-h(z_n-v_n)`, whose magnitude is at most `|h|a` in the same
decomposition. Therefore it remains strictly positive for `z!=v`
whenever `|h|<=Delta/4`. Each vertex is thus the constant unique
response on `[-1,1] intersect [lambda_v-Delta/4,lambda_v+Delta/4]`.
In particular, a diagonal strongly convex QP on a scalar 2VPI path
can have at least `2^n` distinct constant response pieces as one
linear objective parameter varies. The identity-Hessian normalization
below preserves this conclusion. For this response-complexity statement
alone, one may fix `epsilon=1/4` and use `D=4^(n-1)`; no upper-level
constraints or subset-sum data are needed. The interval widths shrink
with dimension, so no fixed numerical robustness is asserted.

Multiplying the entire follower objective by `1/tau` gives the
equivalent objective `||z||^2/2-(c/tau)^T z-(lambda/tau)z_n`.
Thus the follower Hessian may be the identity matrix, with condition
number exactly one. The large linear coefficients remain polynomially
encoded. This normalization is not a strong-hardness claim.

## 2. The upper-level decision problem

For an integer target `0<=B<=W`, ask whether there is `lambda in [-1,1]`
whose unique follower response satisfies

```
F(z) <= 0,
B-1/4 <= sum_i w_i*z_i <= B+1/4.                            (2)
```

The first row is a nonconvex quadratic upper-level constraint whose
Hessian is `-2 e_n e_n^T`; its linear part is dense. The second line
is one dense aggregate with two bounds. Neither row belongs to the
follower feasible set. Equivalently, minimize `F(z)` at the upper level
subject to the slab and ask whether the optimum is at most zero.
In this optimization version, all upper feasible-set constraints are
linear and the upper objective is the nonconvex quadratic `F`.
For the stated target range its induced feasible set is nonempty, as
shown below. Continuity of the unique follower response and compactness
of `[-1,1]` ensure that this upper minimum is attained.

If the original subset-sum instance has a yes bit vector, its associated
path vertex lies in the slab by the reviewed `1/8` rounding bound. The
vertex-response lemma supplies a leader decision inducing that vertex,
which also has `F=0`.

Conversely, (2) and nonnegativity of `F` force the response to be a
path vertex. Its endpoint bits have weighted sum differing from the
target by at most `1/4+1/8<1`, so their integer weighted sum equals
`B`. This proves NP-hardness.

Membership in NP for this explicitly parameterized family is direct.
Give the endpoint bit vector, construct the rational vertex and
`lambda_v`, and check the slab. The vertex-response lemma proves lower
optimality of the constructed witness. Every yes instance has such a
witness, and its bit length is polynomial. Thus this restricted
feasibility problem is NP-complete. A broader bilevel NP-membership
claim is not needed for this conclusion. Optimistic and pessimistic
semantics agree because the follower response is unique.

The lower polytope and all coefficients have polynomial rational
encoding length; powers have exponents `O(n)` and base encoding
`O(log W)`. The reduction proves ordinary hardness. It does not give
strong hardness, a fixed numerical precision gap, or approximation
hardness. The upper-level nonconvex row is essential to this statement.

In fact, deleting `F<=0` makes the displayed slab feasible for every
target `0<=B<=W`. The unique response of the strongly convex follower
on a fixed compact polytope is continuous in `lambda`. It visits the
zero vertex and the all-one-bit vertex, whose weighted total is at
least `W-1/8`. The intermediate value theorem supplies every integer
target below `W`; the all-one-bit vertex itself satisfies the slab for
`B=W`. Thus the single linear slab does not carry the hardness on its
own. This is a useful negative control on attempts to claim an
all-linear-upper-level result from this construction.

## 3. Interpretation and prior work

This is a concrete limit on extending the repository's
[independent-block bilevel algorithm](../results/bilevel-fixed-aggregate-response-algorithm.md).
Diagonal curvature alone does not create independent follower blocks:
the path constraints couple them. The leader dimension and the number
of upper aggregates are fixed, but the coupled path grows. The example
does not contradict the positive theorem's independence assumptions.

Scalar-leader bilevel hardness and unique follower responses are already
known. [Sugishita and Carvalho](https://arxiv.org/pdf/2510.21126),
Sections 3–4, construct scalar-leader linear bilevel instances using a
chain of constant-size blocks and a unique follower response. Their
displayed chain has several variables per block and some three-variable
equalities; it is not the scalar two-variable-per-row follower described
here. The paper also proves an exponential union-of-polyhedra lower
bound for its response geometry. These established boundaries must not
be advertised as new consequences of the present construction.

[Ketkov and Prokopyev](https://arxiv.org/pdf/2511.15592), introduction
and Lemma 2, discuss this scalar-leader boundary and give a separate
route through parametric minimum-cost flow. Both primary texts were
inspected during a bounded source comparison. A full priority audit for
the precise diagonal-Hessian/path-2VPI/nonconvex-upper-row combination
has not been completed. The main purpose here is to preserve an explicit
short obstruction with fully stated hypotheses.

Exponential response complexity for parametric convex QPs is also
established prior work: [Gärtner, Jaggi and Maria (2012)](https://arxiv.org/abs/0903.4817)
prove an exponential regularization-path construction for support vector
machines. The response lemma here should be distinguished by its explicit
scalar path constraints, diagonal Hessian and quantitative vertex
intervals. It does not establish a new broad exponential-QP-path boundary.

## 4. Verification status

Two independent written audits passed:

- [First audit](review-klee-minty-diagonal-follower-bilevel.md) checks
  the full quantitative vertex-response argument, constant response
  intervals, NP certificate, uniqueness, nonempty attained upper
  optimization, and the essential upper nonconvexity.
- [Second audit](review-klee-minty-diagonal-follower-second.md)
  independently checks the same mathematics and the identity-Hessian
  normalization. Its
  [exact checker](../code/parametric_path_lp/exact_diagonal_follower_check.py)
  verifies 1,530 strictly positive normal-cone KKT certificates through
  dimension eight and 3,060 objective-gap inequalities on convex
  combinations. All calculations use rational arithmetic.

The previously reviewed path identity and slab reduction are linked
above. The new global convex-combination proof establishes the
quantitative strictly convex perturbation for all dimensions; the
finite exact checks provide additional independent validation.
