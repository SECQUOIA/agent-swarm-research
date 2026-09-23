# Second review: scalar leader and diagonal strongly convex path follower

Date: 2026-09-05. Verdict: PASS for the mathematical construction in
[the bilevel draft](klee-minty-diagonal-follower-bilevel.md). The
nonconvex upper-level constraint is essential to the stated result.
This review does not establish separate literature priority.

## Exact regularization bound

At every Klee–Minty vertex, `c^T u=u_n-u_n^2`. Thus the linear
score at `lambda_v=2v_n-1` has loss exactly `(u_n-v_n)^2` relative
to vertex `v`. Every coordinate at depth `j` has denominator dividing
`(8W)^(j-1)`. Distinct vertex terminal values therefore differ by at
least `1/D`, for `D=(8W)^(n-1)`, giving squared loss at least
`Delta=D^(-2)`. This remains valid at dimension one.

For an arbitrary point, use a finite vertex decomposition and let `a`
be the total coefficient on vertices other than `v`. The linear score
loss is at least `Delta*a`. Coordinate bounds in `[0,1]` give
`||z-v||_infinity<=a`, hence

```
||z||^2-||v||^2
 =2v^T(z-v)+||z-v||^2 >= -2n*a.
```

Multiplication by the regularizer coefficient `tau/2`, with
`tau=Delta/(2n)`, loses at most `Delta*a/2`. The total objective
increase is at least `Delta*a/2`, strictly positive for `z!=v`.
This proves the stated unique vertex response without any limiting
argument or numerical perturbation assumption. No vertex enumeration
is required to construct the instance.

The follower Hessian is positive definite, its feasible set is nonempty
and compact, and its response exists uniquely for every parameter.
Scaling its objective by `1/tau` preserves that response and makes the
Hessian exactly the identity. This fixes the Hessian condition number;
it does not bound all numerical sensitivity, because the rescaled linear
coefficients can be large. Their bit lengths remain polynomial.

## Bilevel equivalence and encoding

The upper condition `F(z)<=0`, together with the follower's membership
in the path polytope, forces an original path vertex. Its bits then
satisfy the source subset-sum condition by the reviewed `1/8` rounding
bound and `1/4` slab width. Conversely every satisfying bit vector gives
a vertex satisfying both upper rows, and the displayed leader value
induces that vertex exactly.

The direct certificate is valid for this explicit instance family:
guess the bits, recursively compute their rational vertex, construct
`lambda_v`, and verify the slab. The proved response lemma establishes
lower-level optimality for that witness. A yes instance always has such
a certificate because its upper quadratic row forces a vertex. The
certificate and all constructed coefficients have polynomial encoding
length, including `Delta`, `tau`, and `1/tau`. Thus ordinary
NP-completeness is justified for this restricted feasibility problem.
Unique follower responses eliminate any optimistic/pessimistic
selection distinction.

The upper quadratic inequality has a dense linear part and is nonconvex.
The slab is one aggregate with two bounds. Neither is a lower-level
constraint, whose rows remain two-variable inequalities on a path.
Diagonal objective curvature does not make that path's coordinates
independent. This is consequently consistent with the existing positive
results for independent follower blocks. It does not establish strong
hardness, all-linear upper-level hardness, a fixed precision gap, or
hardness of solving an individual follower problem.

Indeed, deleting the upper quadratic condition would make this particular
slab-feasibility reduction uninformative. The strongly convex response is
a continuous function of the leader parameter: it is Euclidean projection
onto a fixed compact convex polytope after affine rescaling of the linear
score. It visits zero and the all-one-bit vertex, whose weighted sum is
at least `W-1/8`. Along the parameter interval between these two visits,
continuity reaches each integer target `B<W`; the all-one-bit response
itself meets the slab when `B=W`. Thus every target in the stated range
would pass the slab alone.

## Additional response-interval observation

The same estimates yield a finite interval around every exposing leader
value. For any other vertex `u`,

```
grad phi_(lambda_v)(v)^T(u-v) >= Delta-tau*n = Delta/2.
```

Changing the leader by `h` changes this directional derivative by
`-h(u_n-v_n)`, whose magnitude is at most `|h|`. Therefore every
leader value with `|lambda-lambda_v|<=Delta/4`, restricted to the
allowed interval, still has `v` as its unique response. Nonnegativity
of these directional derivatives extends from vertices to the whole
polytope; strict convexity then gives uniqueness. In particular the
response has at least `2^n` distinct constant pieces. These intervals
shrink with input size and do not establish a fixed robustness radius.
This is an elementary consequence of the same proof, not a claim that
exponential regularization paths are new.

## Independent exact KKT checks

[exact_diagonal_follower_check.py](../code/parametric_path_lp/exact_diagonal_follower_check.py)
checks the actual strongly convex quadratic's normal-cone optimality
conditions at every endpoint pattern in dimensions one through eight
for three independently generated weight vectors per dimension. Each
active path row has a diagonal sign and a predecessor coefficient
`epsilon`; backward exact substitution constructs multipliers satisfying

```
B^T mu = c+lambda_v e_n-tau*v,    mu>0.
```

All 1,530 exact KKT certificates passed. Positive multipliers and the
strictly convex objective certify unique global follower optimality.
Another 3,060 rational convex-combination tests verified the complete
objective-gap inequality and its strictness away from the target vertex.
No floating-point tolerance was used. These tests support, rather than
replace, the quantitative proof above.
