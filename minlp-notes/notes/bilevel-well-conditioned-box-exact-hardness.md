# Exact bilevel hardness with a uniformly well-conditioned box follower

Date: 2026-09-05. Status: reviewed predecessor; the final theorem is in
[the promoted result](../results/bilevel-well-conditioned-box-exact-hardness.md). This complements
[the conditioned additive algorithm](bilevel-conditioned-box-additive-algorithm.md).
The hardness gap becomes exponentially small; it does not contradict a
running time polynomial in inverse additive tolerance.

## 1. Candidate theorem

The leader is one scalar `x in [0,1]`. Its follower minimizes

```
(1/2)u^T Q u+(c+x d)^T u,   u in [0,1]^N,
```

and the upper objective is linear in `u`, with no other upper constraints.
All rational coefficient magnitudes can be bounded by two, and

```
(49/50)^2 I <= Q <= (51/50)^2 I.
```

Thus the follower is uniformly strongly convex, its spectral condition
number is less than two, and every leader has a unique response.

**Candidate theorem.** Exact upper-value threshold decision is NP-complete
under these restrictions. More precisely, a polynomial-time reduction from
3SAT produces a positive rational `delta` of polynomial binary encoding
length such that the upper optimum is at most `delta/8` in yes instances
and at least `15delta/8` in no instances. Consequently, additive upper-value
approximation in time polynomial in the input length and
`log(1/epsilon)` would imply `P=NP`, even for these uniformly conditioned
and bounded-magnitude instances.

This is ordinary binary-encoded hardness. Small rational data and an
exponentially small upper gap are allowed. It is not a constant-gap,
strong-NP-hardness, or fixed-coefficient-set result.

## 2. A bounded feedforward ReLU computation of the SAT score

Use a 3SAT formula with `n` variables and `m` clauses, each on three
distinct variables, as justified in
[the earlier box-hardness proof](../results/bilevel-scalar-leader-spd-box-np-completeness.md).
Write `ReLU(t)=max(0,t)`. For `i=1,...,n`, recursively define

```
t_i=3^(i-1)x-2 sum_(j<i)3^(i-1-j)y_j,
alpha_i=ReLU(3t_i-1),
beta_i=ReLU(3t_i-2),
y_i=alpha_i-beta_i.
```

For `t_i in [0,1]`, `y_i=clip_[0,1](3t_i-1)` and
`t_(i+1)=3t_i-2y_i` belongs to `[0,1]`. Indeed, its three affine pieces
map respectively `[0,1/3]`, `[1/3,2/3]`, and `[2/3,1]` into `[0,1]`.
Induction from `t_1=x` proves these bounds for every leader. In particular,
`alpha_i in [0,2]`, `beta_i in [0,1]`, and `y_i in [0,1]`.

Add readout coordinates

```
p_i=ReLU(2y_i-1),
v_a=ReLU(1-ell_a(y)),
```

where `ell_a` is the sum of the three continuous literal values in clause
`a`. These new coordinates belong to `[0,1]`. All `N=3n+m` ReLU
coordinates can be ordered as

```
h=(alpha_1,beta_1,...,alpha_n,beta_n,p_1,...,p_n,v_1,...,v_m)
```

so that their equations have the form

```
h=ReLU(Ah+b_0+x b_1),                               (1)
```

with strictly lower triangular rational matrix `A`. Here every entry of
`A,b_0,b_1` has magnitude at most `C=2*3^n`. All have polynomial bit
length. The coefficient bound follows from the displayed ternary formulas;
readout coefficients are at most two.

The exact network coordinates satisfy `0<=h_i<=2`. Its residual

```
rstar=h-Ah-b_0-x b_1
```

has coordinates between zero and two. For the two base ReLUs, the most
negative preactivation is respectively `-1` and `-2`; for a readout it is
at least `-2`. This explicit residual bound will control the quadratic
approximation below.

Define the linear score

```
Phi(h)=2 sum_i alpha_i-2 sum_i beta_i-2 sum_i p_i+2 sum_a v_a.
```

For `D(y)=sum_i min(y_i,1-y_i)`, the exact identities give

```
Phi(h)=2D(y)+2 sum_a max(0,1-ell_a(y))>=0.             (2)
```

For every Boolean vector `b`, the rational leader

```
x_b=sum_i 2b_i/3^i+1/(2*3^n)
```

makes the network output `y=b`, by the ternary remainder bounds in the
earlier proof. A satisfying Boolean vector therefore has network score
zero. If the formula is unsatisfiable, round any `y` at one half. A false
clause has each literal equal to its corresponding minority amount and
has distinct variables, hence `ell_a(y)<=D(y)`. Equation (2) then implies
`Phi(h)>=2D(y)+2max(0,1-D(y))>=2` for every leader.

The network itself is only an intermediate construction. The next step
replaces it by one well-conditioned convex quadratic program on a unit box.

## 3. Scaling makes the quadratic Hessian close to the identity

Put

```
M=(1+N*C)^N,
theta=1/(100*N*C*M),
s_0=1/(4*C),
s_i=s_0*theta^(i-1), i=1,...,N,
S=diag(s_i),
B=S A S^(-1).
```

The symbol `M` here is an explicit positive integer, not an asymptotic
constant. All these rationals have polynomial bit length; in particular
`log M=O(N log(NC))` and `log(1/s_N)=O(N^2 log(NC))`.

Consider the follower objective

```
f(x,u)=(1/2)||(I-B)u-S(b_0+x b_1)||_2^2,
             u in [0,1]^N.                          (3)
```

For `i>j`, `|B_ij|<=C theta^(i-j)`. Hence

```
||B||_infinity, ||B||_1 <= C theta/(1-theta)<=2C theta<=1/50,
||B||_2<=1/50.
```

Its follower Hessian is `Q=(I-B)^T(I-B)`, so

```
(49/50)^2 I<=Q<=(51/50)^2 I.                          (4)
```

This is a uniform absolute eigenvalue bound, not merely a bound on the
ratio of eigenvalues. The full square expression is jointly convex in
leader and follower variables. Its leader-only term can be dropped to
obtain the normalized model without changing responses.

The resulting `Q` entries have magnitude at most two. For each of `b_0`
and `b_1`, `||S b_j||_infinity<=1/4`, and
`||(I-B)^T||_infinity<=51/50`. Thus the normalized follower vectors `c,d`
have entries of magnitude less than one. Every remaining bound coefficient
is zero or one.

## 4. Uniform relative-coordinate approximation of the network

Let `u(x)` be the unique minimizer of (3), and let `h(x)` be the exact
network output (1). The scaled network point `S h` belongs to `[0,1]^N`,
since `h_i<=2` and `s_i<=1/(4C)`. It satisfies

```
S h=clip_[0,1](B S h+S(b_0+x b_1))
```

coordinatewise: the upper clip never changes its ReLU output.

Write

```
r=(I-B)u-S(b_0+x b_1),
e_i=|u_i/s_i-h_i|,
P=|A|,
U=S^(-1)|B|^T S=S^(-2)P^T S^2.
```

Box optimality of (3) is equivalent to the projected-gradient identity

```
u=clip_[0,1](u-(I-B)^T r)
 =clip_[0,1](Bu+S(b_0+x b_1)+B^T r).
```

The scalar clip is nonexpansive. Subtracting the scaled network identity
and dividing componentwise by `s_i` gives

```
e<=P e+U |S^(-1)r|.
```

The residual decomposition and the bound `|rstar|<=2` give

```
|S^(-1)r| <= (I+P)e+2*1,
e <= P e+U[(I+P)e+2*1].                              (5)
```

These are componentwise inequalities between finite nonnegative vectors.
No a priori small-error assumption is used.

Since `P` is strictly lower triangular,

```
T=(I-P)^(-1)=I+P+...+P^(N-1)>=0,
||T||_infinity<=(1+NC)^N=M.
```

Also `||P||_infinity<=NC`, and the upper triangular entries of `U`
satisfy `U_ik<=C theta^(2(k-i))` for `k>i`. Thus

```
||U||_infinity<=2C theta^2.
```

Multiplying (5), after moving `Pe` left, by the nonnegative matrix `T`
yields

```
e<=T U(I+P)e+2T U1.
```

Our parameter choice ensures

```
||T U(I+P)||_infinity
 <=2MC(1+NC)theta^2 < 1/2.
```

Taking the infinity norm therefore gives

```
||e||_infinity <= 8MC theta^2
 =1/(1250*N^2*C*M)
 <=1/(16N).                                         (6)
```

All estimates are uniform over the full leader interval. This proves
relative-coordinate approximation even for coordinates whose amplitudes
`s_i` are extremely small; an ordinary absolute Euclidean error estimate
would not suffice for the construction.

## 5. Bounded upper coefficients and an exponentially small gap

Let `ell` denote the coefficient vector of `Phi`, whose entries are
`+/-2` and whose one-norm is `2N`. Put `delta=s_N` and use the linear upper
objective

```
G(u)=delta*ell^T S^(-1)u.
```

Every coefficient has magnitude at most two, because `delta/s_i<=1`.
Equation (6) gives for every leader

```
|G(u(x))-delta*Phi(h(x))|<=delta/8.                   (7)
```

If the formula is satisfiable, its Boolean leader witness has network
score zero, so the QP-response upper value is at most `delta/8`. If it is
unsatisfiable, every network score is at least two, so every QP-response
upper value is at least `15delta/8`. The rational threshold `delta`
therefore decides satisfiability.

The follower box is fixed and compact, and its objective is uniformly
strictly convex. Its unique response is continuous, so the global upper
minimum is attained. NP membership follows from the exact active-face
certificate in the earlier theorem: after guessing lower/free/upper
statuses, the response and threshold inequalities reduce to a rational
interval in the one leader variable. All witness data have polynomial
bit length.

Finally, `log(1/delta)` is polynomial in the source formula length.
An additive-value algorithm polynomial in accuracy bits could be called
with `epsilon=delta/4` and would distinguish the two cases by threshold
`delta`. This proves the claimed precision dependence barrier. The
positive algorithm's polynomial dependence on `1/epsilon` remains fully
consistent with this result.

## 6. Source and scope audit still required

The ternary Boolean-score computation comes from the earlier investigated
construction and its explicitly credited scalar-leader bilevel and
regularization-path antecedents. The proposed new step here is the
relative-coordinate perturbation estimate (5)--(6), which realizes that
computation by a uniformly conditioned unit-box QP while moving hardness
into very small upper-value differences.

This note does not claim a general exact representation of feedforward
ReLU networks by these QPs. It proves a quantitative approximation for this
explicit bounded network, uniformly in the leader, and then transfers a
robust network score gap. No hardness is inferred from an exponential
number of path pieces alone. Independent proof and source audits are
required before promotion.
