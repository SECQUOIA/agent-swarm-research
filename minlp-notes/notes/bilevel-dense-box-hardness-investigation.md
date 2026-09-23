# A scalar leader and a dense strictly convex box follower

Date: 2026-09-05. Status: reviewed predecessor of
[the stronger final result](../results/bilevel-scalar-leader-spd-box-np-completeness.md),
which removes all upper constraints and one redundant auxiliary block. This investigates the boundary of
[the fixed-block bilevel algorithm](../results/bilevel-fixed-block-response-algorithm.md).
The target is hardness with one continuous leader, a fixed positive-definite
follower Hessian, only box constraints at the lower level, and entirely
linear upper-level data. An exponential response path alone is not a
hardness proof; the reduction below gives an explicit constant objective gap.

## 1. Candidate theorem

Consider bilevel linear-quadratic programs

```
min F(x,z)
s.t. 0<=x<=1,  A z<=b,
     z=argmin{ (1/2)z^T Qz+(c+x d)^T z : 0<=z<=1 },
```

where the leader `x` is a single scalar, `Q` is rational positive definite
and independent of `x`, and the upper objective and constraints are affine.
The follower dimension is unrestricted. The follower is unique for every
leader, so optimistic and pessimistic conventions agree.

**Candidate theorem.** Deciding whether the optimal value is at most zero
is NP-complete, even on an always-feasible compact subclass for which the
optimal value is either zero or at least two. Thus approximating the
optimal value with absolute error strictly below one is NP-hard. The
constructed upper objective is nonnegative on every follower response.
Upper variable coefficients lie in `{-1,0,1}`; clause right-hand sides
are integers between `-1` and `2`, and the objective constant is `n`. The rational lower-level coefficients have polynomial bit
length but may have large condition numbers; no strong-NP-hardness or
well-conditioned hardness claim is made.

If a leader-only quadratic term is retained, the constructed lower
objective is a sum of positive weighted squares of affine functions of the
leader and followers. In that equivalent representation it is jointly
convex in all its variables, as well as strictly convex in the follower
vector. Removing the leader-only term yields the normalized displayed
model and preserves every follower response; the normalized expression
itself need not be jointly convex. The only coupling responsible for the construction lies
in its dense quadratic Hessian; there are no lower nonbox rows.

## 2. A quadratic response reaching every Boolean vector

For `n>=1`, choose

```
rho=1/(100*3^n),
w_i=rho^(i-1),  i=1,...,n,
eta=rho^n.
```

The leader is `x in [0,1]`. Introduce base follower coordinates
`y in [0,1]^n` and define affine residuals

```
r_i(x,y)=y_i-3^i x+2 sum_(j<i) 3^(i-j)y_j+1.
```

First consider the positive quadratic energy

```
f_0(x,y)=(1/2)sum_i w_i r_i(x,y)^2.
```

Its matrix of `y` coefficients is lower triangular with diagonal one:

```
L_ii=1, L_ij=2*3^(i-j) for j<i, L_ij=0 for j>i.
```

Therefore its follower Hessian is `L^T diag(w_i)L`, positive definite.

For every Boolean vector `b in {0,1}^n`, choose the rational leader

```
x_b=sum_(i=1)^n 2b_i/3^i + 1/(2*3^n).
```

It belongs to `(0,1)`. Define recursively the remaining ternary quantity

```
t_i=3^(i-1)x_b-2 sum_(j<i)3^(i-1-j)b_j
   =sum_(j=i)^n 2b_j/3^(j-i+1)+1/(2*3^(n-i+1)).
```

Then `r_i(x_b,b)=b_i-3t_i+1`. If `b_i=0`, this lies in
`[1/(2*3^(n-i)),1]`; if `b_i=1`, it lies in
`[-1,-1/(2*3^(n-i))]`. The endpoints follow by setting all remaining
bits to zero or one in the displayed formula for `t_i`.

The derivative with respect to `y_i` at this Boolean point is

```
G_i=w_i r_i + sum_(k>i) 2*3^(k-i) w_k r_k.
```

Since `|r_k|<=1`, the absolute value of the second term divided by `w_i`
is at most

```
2 sum_(ell>=1)(3rho)^ell = 6rho/(1-3rho)
                             < 1/(10*3^n).
```

The first term has the required box-normal sign and magnitude at least
`w_i/(2*3^(n-i))`, which is at least `3w_i/(2*3^n)`. Consequently

```
(1-2b_i) G_i > w_i/3^n.                              (1)
```

These are strict sufficient KKT signs for minimization on the box: at a
zero coordinate the derivative is positive; at a one coordinate it is
negative. Strict convexity therefore makes `b` the unique response at
`x_b`. The argument proves exact attainment of every Boolean vector,
not just proximity to a Boolean path.

## 3. Linear upper objective through extra boxed follower coordinates

Add `p,q in [0,1]^n` and use the follower objective

```
f(x,y,p,q)=f_0(x,y)
  +(eta/2) sum_i [(p_i-2y_i+1)^2+(q_i+2y_i-1)^2].       (2)
```

For fixed `y`, the unique conditional minimizers are exactly

```
p_i=clip_[0,1](2y_i-1),
q_i=clip_[0,1](1-2y_i),
p_i+q_i=|2y_i-1|.                                    (3)
```

The full follower Hessian is positive definite. Indeed, the linear map
from `(y,p,q)` to all residuals in (2) is square and block lower triangular,
with diagonal blocks `L,I,I`; every weight is positive. Its weighted Gram
matrix is therefore positive definite. Equation (2) is also jointly convex
in `(x,y,p,q)` because every residual is affine.

At the point `(y,p,q)=(b,b,1-b)`, the added contribution to the base
coordinate derivative is `-2eta` if `b_i=0`, and `+2eta` if `b_i=1`.
The signs oppose the base margin, but

```
2eta=2rho*w_n < w_n/3^n <= w_i/3^n.
```

Thus the strict base signs (1) remain valid. The `p,q` coordinates obey
(3), so their box KKT conditions hold as well. Strict convexity proves
that the unique full follower response at `x_b` is exactly
`(b,b,1-b)`.

At the leader `x=1/2`, the point

```
y_i=1/2, p_i=q_i=0 for all i
```

makes every residual in (2) zero. For the base residual this uses
`sum_(j<i)3^(i-j)=(3^i-3)/2`. It is consequently the unique follower
response at that leader.

## 4. Constant-gap reduction from 3SAT

Use 3SAT with exactly three distinct variables in each clause. This is an
NP-complete restriction: remove tautological clauses and repeated literals;
a two-literal clause `a OR b` becomes `(a OR b OR t) AND (a OR b OR NOT t)`
with fresh `t`, while a singleton `a` becomes the four clauses
`a OR (+/-t) OR (+/-u)` with fresh distinct `t,u`. An empty clause can be
replaced by a fixed unsatisfiable set of eight clauses on three variables.
These transformations preserve satisfiability and have polynomial size.
For each resulting clause impose the upper linear inequality

```
sum_(positive literals i) y_i
  +sum_(negative literals i) (1-y_i) >= 1.
```

Use the affine upper objective

```
F(y,p,q)=n-sum_i(p_i+q_i).
```

On every follower response, (3) gives the exact identity

```
F=2 sum_i min(y_i,1-y_i) >= 0.                        (4)
```

The midpoint response from Section 3 satisfies every clause inequality
with left side `3/2`, so every constructed bilevel instance is feasible.
The response is continuous in the scalar leader: the follower objective
is continuous, the box is constant and compact, and its minimizer is
unique. This follows directly by taking convergent subsequences of
minimizers and passing their defining objective inequalities to the limit.
Therefore the feasible leader-response graph is compact and the upper
minimum is attained.

If the formula is satisfiable, take a satisfying Boolean vector `b` and
its leader `x_b`. Its follower response satisfies every upper clause and
has `F=0`.

Conversely, suppose the formula is unsatisfiable and take any feasible
follower response. Round `y_i` to `b_i=1` when `y_i>=1/2`, and to zero
otherwise. Some clause is false under `b`. For each of its three literals,
the corresponding continuous literal value equals `min(y_i,1-y_i)`;
this remains true at ties. Upper feasibility and distinctness of the
clause variables imply

```
sum_i min(y_i,1-y_i)
 >= sum_(three variables of the false clause) min(y_i,1-y_i)
 >= 1.
```

Equation (4) gives `F>=2`. This proves the gap `OPT=0` versus `OPT>=2`.
No claim about running through an exponentially long path is needed for
the hardness reduction.

All construction data have polynomial bit length. Powers `3^i` use `O(n)`
bits; each `rho^i` uses `O(n^2)` bits. Expanding (2) produces polynomially
many rational quadratic coefficients with polynomial bit lengths. The
leader-dependent constant term can be omitted without changing follower
responses, yielding the stated `Q,c,d` model. Joint convexity is asserted
for the original sum-of-squares representation, which retains this
leader-only quadratic term. The only dependence on the
3SAT clause list is in the upper linear inequalities.

## 5. Membership in NP

For completeness, the zero-threshold problem belongs to NP for general
rational instances of the displayed model with affine upper data and a
positive-definite box follower. Guess each follower coordinate's active
status: lower bound, free, or upper bound. On that status, free-coordinate
stationarity solves a principal positive-definite subsystem of `Q`, so
all free coordinates are affine rational functions of the scalar leader.
All box feasibility and endpoint gradient-sign tests then become affine
inequalities in that leader. Upper affine constraints and the objective
threshold do as well.

If a leader satisfying the guessed status exists, these finitely many
rational affine inequalities have a rational solution of polynomial bit
length. Equivalently, clear the polynomial-bit denominators from the
principal linear solve and take a rational endpoint of the resulting
nonempty interval in `[0,1]`. The follower vector then also has polynomial
rational encoding length. A verifier checks primal feasibility, the box
KKT signs, and upper feasibility/objective in polynomial bit time. Free
coordinates may reach bounds; non-strict tests include these degeneracies.
Strict convexity makes the verified KKT point the unique follower optimum.
This establishes NP membership and completes the candidate theorem.

## 6. Relation to known results and current limitations

[Sugishita and Carvalho, Complexity of Bilevel Linear Programming with a
Single Upper-Level Variable, March 2026 version](https://arxiv.org/html/2510.21126)
already prove one-leader bilevel LP NP-completeness and use a lexicographic
ternary construction. The present investigation was informed by reading
their main theorem and Section 4. Their follower has coupled polyhedral
constraints and a linear objective. The proposed distinction here is a
strictly convex fixed-Hessian follower on a pure box, with a direct
weighted-quadratic realization and an explicit constant upper-value gap.
One-scalar-leader bilevel hardness itself is not claimed as new.

Exponential one-parameter regularization paths are also established:
[Mairal and Yu (2012)](https://icml.cc/2012/papers/202.pdf) for Lasso and
[Gärtner, Jaggi, and Maria](https://arxiv.org/abs/0903.4817) for SVM.
Those path results must be distinguished from hardness of optimizing a
specified upper objective. The independent
[source audit](bilevel-dense-box-hardness-novelty.md) derives a particularly
close antecedent: normalizing the dual of Mairal--Yu's full-rank Lasso
construction gives a scalar-parameter positive-definite box QP whose
response visits all Boolean assignments in a subset of its coordinates.
Thus neither exponential paths nor their Boolean-vertex coverage is
claimed as new. The target contribution is the explicit polynomial-bit
construction and the all-affine-upper constant-gap bilevel hardness under
the stated restrictions. The bounded source search found no exact combined
match; this is qualified novelty evidence, not proof of first publication.

The lower Hessian is dense and has no fixed-dimensional independent-block
representation asserted here. Positive definiteness alone does not meet
the structure of the repository's positive theorem. The construction uses
geometrically separated weights, so it does not establish hardness under
a polynomial condition-number bound, bounded coefficient magnitudes after
normalization, or robust perturbations of the lower objective. The
constant gap concerns exact follower responses and upper objective values;
it does not automatically transfer to approximate follower optimality.

## 7. Exact validation

[check_dense_box_path.py](../code/bilevel_response/check_dense_box_path.py)
passed 510 full Boolean-response KKT checks through `n=8`, including the
auxiliary feedback gradients. It also verified four expanded Hessian/Gram
identities and positive rational LDL pivots, and 129 feasible rational-grid
points for the gap argument on an unsatisfiable three-variable formula.
The midpoint residual identity is checked at every tested dimension. These
finite tests support fragile signs and indexing; independent proof review
is required for the general theorem.

## 8. Elementary positive-objective approximation consequence

For the final no-upper-constraints result, write `F` for its linear upper
objective, whose exact-response optimum is zero or at least two. Replacing
it by `1+F` gives strictly positive optimum one versus at least three.
Thus any polynomial-time algorithm returning an exactly bilevel-feasible
solution with multiplicative ratio strictly less than three would imply
`P=NP`.

More generally, let `s=n+m` for the encoded SAT formula and replace the
objective by `1+2^s F`. The coefficient `2^s` has only `s+1` binary bits,
and the constructed input length `L` stays polynomial in `s`. The yes
optimum is one while the no optimum is at least `1+2^(s+1)`. Every fixed
polynomial in `L` is eventually smaller than `2^s`; finite small sizes
can be handled separately. Consequently a polynomial-time algorithm with
any polynomially bounded multiplicative approximation ratio would also
imply `P=NP`, under the exact bilevel-feasibility convention.

This is a conventional numerical-scaling consequence of the proved gap,
not a stronger hardness mechanism or a strong-NP-hardness assertion. The
constant-coefficient, constant-additive-gap theorem is the main structural
result. No claim is made for relaxed follower optimality or relaxed
bilevel feasibility.
