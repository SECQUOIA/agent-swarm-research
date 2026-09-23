# One scalar leader with a strictly convex quadratic box follower

Date: 2026-09-05. Status: independently reviewed theorem.
[First full audit](../notes/review-bilevel-dense-box-hardness.md) and
[second full audit](../notes/review-bilevel-dense-box-hardness-second.md).
The [source comparison](../notes/bilevel-dense-box-hardness-novelty.md)
found no matching complete theorem in a bounded search. Scalar-leader
bilevel hardness and exponential box-QP response paths have prior
antecedents; the precise restriction and explicit gap below are the target
contribution, not either broad phenomenon in isolation.

## 1. The restricted problem and theorem

The leader chooses one continuous scalar `x in [0,1]`. Its unique follower
response is

```
z(x)=argmin { (1/2)z^T Qz+(c+x d)^T z : z in [0,1]^N },
```

where the rational matrix `Q` is positive definite and independent of the
leader. The leader minimizes a linear function of `z(x)`. There are **no
upper constraints** beyond `x in [0,1]`, and no lower constraints beyond
the fixed unit box. Every leader is feasible. Follower uniqueness makes
optimistic and pessimistic conventions identical.

**Theorem.** Deciding whether the global upper optimum is at most zero is
NP-complete, even on a subclass with upper variable coefficients in
`{-2,0,2}` and upper optimum either zero or at least two. The upper
objective is nonnegative on every follower response. Thus approximating
the optimal value with absolute error strictly below one is NP-hard.

The construction has polynomial rational bit length. Its follower Hessian
contains a dense block and can be ill-conditioned; no strong-NP-hardness or bounded-
condition-number claim is made. If a leader-only quadratic term is
retained, the constructed lower objective is jointly convex in leader and
followers. Removing that harmless term gives the normalized display above
and preserves all responses, but the normalized expression itself need
not be jointly convex.

This gives a sharp scope boundary for
[the fixed-dimensional independent-block algorithm](bilevel-fixed-block-response-algorithm.md):
positive definiteness and box geometry alone do not replace bounded local
block dimension and bounded aggregate coupling.

## 2. Base quadratic and Boolean leaders

Take a 3SAT formula on `n>=1` variables with `m` clauses, each on three
distinct variables. This restriction remains NP-complete. To see this,
remove tautologies and repeated literals; replace `a OR b` by
`(a OR b OR t) AND (a OR b OR NOT t)` using fresh `t`, and replace a
singleton `a` by the four clauses `a OR (+/-t) OR (+/-u)` using two fresh
variables. An empty clause can be replaced by a fixed unsatisfiable set of
eight clauses on three variables. These changes have polynomial size and
preserve satisfiability.

Set

```
rho=1/(100*3^n),
w_i=rho^(i-1),  i=1,...,n,
eta=rho^n,
xi=eta/(m+1).
```

For `y in [0,1]^n`, define affine residuals

```
r_i(x,y)=y_i-3^i x+2 sum_(j<i)3^(i-j)y_j+1
```

and the base energy

```
f_0(x,y)=(1/2)sum_i w_i r_i(x,y)^2.
```

Its matrix of `y` coefficients is lower triangular:

```
L_ii=1,
L_ij=2*3^(i-j) for j<i,
L_ij=0 for j>i.
```

Thus the base follower Hessian `L^T diag(w_i)L` is positive definite.

For each Boolean vector `b in {0,1}^n`, choose

```
x_b=sum_(i=1)^n 2b_i/3^i + 1/(2*3^n) in (0,1).
```

Write

```
t_i=3^(i-1)x_b-2 sum_(j<i)3^(i-1-j)b_j
   =sum_(j=i)^n 2b_j/3^(j-i+1)+1/(2*3^(n-i+1)).
```

Then `r_i(x_b,b)=b_i-3t_i+1`. If `b_i=0`, this belongs to
`[1/(2*3^(n-i)),1]`; if `b_i=1`, it belongs to
`[-1,-1/(2*3^(n-i))]`. These bounds follow by setting the remaining bits
in `t_i` to zero or one.

The base derivative at this point is

```
G_i=w_i r_i+sum_(k>i)2*3^(k-i)w_k r_k.
```

Since every `|r_k|<=1`, its second term has magnitude at most

```
w_i * 2 sum_(ell>=1)(3rho)^ell
 = w_i * 6rho/(1-3rho)
 < w_i/(10*3^n).
```

The signed first term is at least
`w_i/(2*3^(n-i))>=3w_i/(2*3^n)`. Hence

```
(1-2b_i)G_i > w_i/3^n.                              (1)
```

These are strict box optimality signs for minimization:
positive derivative at a zero coordinate and negative derivative at a one
coordinate. They leave room for the additional quadratic terms below.

## 3. Exact auxiliary responses and the full follower

For clause `a`, let `ell_a(y)` denote the sum of its three continuous
literal values: a positive literal contributes `y_i`, and a negative
literal contributes `1-y_i`. Add boxed follower variables

```
p in [0,1]^n,  v in [0,1]^m
```

and use the full objective

```
f(x,y,p,v)=f_0(x,y)
  +(eta/2)sum_i (p_i-2y_i+1)^2
  +(xi/2)sum_a (v_a-1+ell_a(y))^2.                    (2)
```

There are `N=2n+m` follower variables. The residual matrix, ordered by
`(y,p,v)`, is square block lower triangular with diagonal blocks `L,I,I`.
Every weight is positive, so its weighted Gram matrix is positive
definite. This is the fixed follower Hessian. All residuals are affine in
leader and followers, giving the stated jointly convex representation
when the leader-only term is retained.

For fixed `y`, every auxiliary coordinate appears only in its own square.
Thus every full follower optimum satisfies exactly

```
p_i=clip_[0,1](2y_i-1),
y_i-p_i=min(y_i,1-y_i),
v_a=clip_[0,1](1-ell_a(y))=max(0,1-ell_a(y)).          (3)
```

The last equality uses `ell_a(y)>=0`.

At a Boolean vector `b`, choose `p=b` and set `v_a` to one if clause `a`
is false under `b`, and zero otherwise. These are the conditional
minimizers in (3). The new `p_i` square contributes `-2eta` to the base
coordinate derivative if `b_i=0`, and zero if `b_i=1`.

A clause with `k` true literals has new residual zero for `k=0,1`, one for
`k=2`, and two for `k=3`. Distinctness of its variables means each base
coordinate coefficient is zero or `+/-1`. The total clause contribution
to any base derivative therefore has magnitude at most `2m xi<2eta`.
All auxiliary feedback together has magnitude less than `4eta`, whereas

```
4eta=4rho*w_n=w_n/(25*3^n)<w_n/3^n<=w_i/3^n.
```

The strict signs (1) survive at leader `x_b`. Auxiliary coordinates
already satisfy their box optimum conditions. Strict convexity therefore
proves that the unique full follower response at `x_b` is precisely this
Boolean/auxiliary point. This holds for every Boolean assignment,
regardless of satisfiability.

## 4. A linear upper objective with a constant gap

Use no upper constraints and the linear objective

```
F(y,p,v)=2 sum_i y_i-2 sum_i p_i+2 sum_a v_a.
```

For `D(y)=sum_i min(y_i,1-y_i)`, identities (3) give on every response

```
F=2D(y)+2 sum_a max(0,1-ell_a(y))>=0.                 (4)
```

If the formula is satisfiable, choose a satisfying Boolean vector `b` and
its leader `x_b`. Every clause shortfall is zero and `D(b)=0`, so the upper
value is zero.

If it is unsatisfiable, take any response and round `y_i` to one when
`y_i>=1/2`, and to zero otherwise. Some clause is false under the rounded
bits. Every continuous literal in that clause equals the corresponding
minority amount `min(y_i,1-y_i)`, including at ties. Its three variables
are distinct, so

```
ell_a(y)<=D(y).
```

Using its one shortfall term in (4) yields

```
F>=2D(y)+2 max(0,1-D(y))>=2.
```

This proves the gap for **every** leader in an unsatisfiable instance.
The fixed compact follower box supplies a unique response for every
leader. The response is continuous: any convergent sequence of leaders
has follower subsequences whose limiting defining objective inequalities
show optimality at the limiting leader, and uniqueness identifies the
limit. Hence the response graph is compact and the continuous upper
objective attains its global minimum. The constructed instances are
always feasible.

The reduction has polynomial bit size. Each `3^i` has `O(n)` bits; each
`rho^i` has `O(n^2)` bits; division by `m+1` adds polynomial encoding
length. Expanding (2) gives polynomially many rational coefficients with
polynomial bit lengths. The formula affects only its clause residuals;
all dimensions and coefficient lists are polynomial in its input size.
Omitting the leader-only term yields the normalized `Q,c,d` model.

## 5. NP membership

For a rational positive-definite box QP with affine scalar parameter,
guess which follower coordinates are at their lower bounds, free, or at
their upper bounds. Free-coordinate stationarity solves a principal
positive-definite subsystem of `Q`; its solution is affine rational in the
scalar leader. Rational Gaussian elimination gives polynomial-bit
coefficients.

The remaining bound feasibility and endpoint gradient-sign conditions
are affine inequalities in the leader. The linear upper objective
threshold is also affine. Thus a feasible guessed status gives a nonempty
rational interval within `[0,1]`, which has a rational point of polynomial
bit length. The follower vector then also has polynomial rational encoding
length. Non-strict tests permit degeneracies where a free coordinate
reaches a bound.

A verifier checks the leader bound, follower box, box KKT conditions, and
upper threshold in polynomial bit time. Strict convexity makes the KKT
conditions sufficient for the unique follower optimum. This establishes
NP membership and completes the theorem.

## 6. Prior work, validation, and limits

[Sugishita and Carvalho, Complexity of Bilevel Linear Programming with a
Single Upper-Level Variable, March 2026 version](https://arxiv.org/html/2510.21126)
already prove one-leader bilevel LP NP-completeness without upper
constraints, with a constant gap and a lexicographic ternary construction.
Their main theorem and Section 4 informed this investigation. Their
follower is linear over a coupled polyhedron. The restriction established
here is a unique positive-definite quadratic follower on a pure fixed box,
with entirely linear upper data and explicit polynomial-bit weights.
Scalar-leader hardness, digit extraction, and constant-gap constructions
are not new in isolation.

Exponential regularization paths are also classical, including
[Mairal and Yu's Lasso construction](https://icml.cc/2012/papers/202.pdf)
and [Gärtner, Jaggi, and Maria's SVM construction](https://arxiv.org/abs/0903.4817).
The independent [source audit](../notes/bilevel-dense-box-hardness-novelty.md)
derives a closer antecedent: normalizing the dual of Mairal--Yu's
full-rank construction gives a scalar-parameter SPD box QP visiting all
Boolean assignments in a subset of its coordinates. Therefore no first
exponential-path or Boolean-coverage claim is made here. Such path
behavior alone is not a reduction proving upper-level optimization hard.
The bounded search found no exact match for the complete restriction and
proof above; this is qualified novelty evidence.

The earlier symmetric auxiliary construction and its exact checks are
preserved in [the investigation](../notes/bilevel-dense-box-hardness-investigation.md).
The [constraint-removal note](../notes/bilevel-dense-box-no-upper-constraints-extension.md)
records the intermediate extension. Independent audits cover the final
simplification that removes the redundant symmetric coordinate. The
independent exact checker
[second_review_checks.py](../code/bilevel_dense_box/second_review_checks.py)
passed 510 base Boolean certificates, 1,008 clause-feedback certificates
covering both auxiliary variants, and 125 gap checks without upper
constraints. These finite checks support the general proof audits.

The follower matrix can be poorly conditioned because the proof uses
geometrically separated weights. The gap is for exact follower responses
and upper values; it does not automatically persist when follower
optimality is relaxed. No claim is made about polynomial condition
numbers, strong hardness, or robustness to arbitrary coefficient
perturbations. This does not contradict the positive fixed-block theorem:
the dense coupling lacks its bounded block/aggregate structure.
