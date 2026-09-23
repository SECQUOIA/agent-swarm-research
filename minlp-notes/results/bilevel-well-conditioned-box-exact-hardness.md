# Exact bilevel hardness with a uniformly well-conditioned box follower

Date: 2026-09-05. Status: complete proof, independently reviewed twice. This complements
[the conditioned additive algorithm](bilevel-conditioned-box-additive-algorithm.md).
The hardness gap becomes exponentially small; it does not contradict a
running time polynomial in inverse additive tolerance.

Independent audits: [first review](../notes/review-bilevel-well-conditioned-box-exact-hardness.md)
and [second review](../notes/review-bilevel-well-conditioned-box-hardness-second.md).
Their exact checks include [actual rational follower KKT verification](../code/bilevel_dense_box/check_conditioned_hardness_first_review.py)
and [independent matrix, network, and error-bound checks](../code/bilevel_response/check_conditioned_hardness_second.py).

## 1. Theorem

The leader is one scalar `x in [0,1]`. Its follower minimizes

```
(1/2)u^T Q u+(c+x d)^T u,   u in [0,1]^N,
```

and the leader minimizes a linear upper objective in `u`, with no other upper constraints.
All rational coefficient magnitudes can be bounded by two, and

```
(49/50)^2 I <= Q <= (51/50)^2 I.
```

Thus the follower is uniformly strongly convex, its spectral condition
number is less than two, and every leader has a unique response.

**Theorem.** Exact upper-value threshold decision is NP-complete
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

## 6. Source comparison and scope

The [bounded primary-source audit](../notes/bilevel-well-conditioned-box-hardness-novelty.md)
found no exact matching hardness theorem under all the restrictions above.
This is a qualified literature assessment, not a proof of priority.

The scalar ternary computation and SAT score build on the earlier
[box-hardness construction and source comparison](../notes/bilevel-dense-box-hardness-novelty.md),
including Sugishita and Carvalho's scalar-leader linear-follower hardness.
Diagonal scaling of positively homogeneous networks is established in
[El Ghaoui et al., *Implicit Deep Learning*, equations (2.6)–(2.7)](https://arxiv.org/pdf/1908.06315).
Approximation of feedforward ReLU computations by strictly convex squared-
residual energies with weak feedback is established in
[Zach and Estellers, *Contrastive Learning for Lifted Networks*, section 2](https://arxiv.org/pdf/1905.02507).
Neither diagonal scaling nor convex-energy emulation is claimed as new.

The specific contribution investigated here is the quantitative relative-
coordinate estimate (5)–(6), with explicit polynomial rational bit lengths,
and its use to prove scalar-leader NP-completeness for a near-identity
unit-box follower with bounded coefficient magnitudes. The small readout
scaling is essential: it bounds the upper coefficients while shrinking
the hardness gap exponentially.

The theorem does not represent arbitrary ReLU networks exactly by these
QPs. It proves uniform quantitative approximation for the explicit bounded
network above and transfers its score gap. It does not infer hardness from
an exponential number of response pieces. It gives neither constant-gap
hardness nor strong NP-hardness, and it is compatible with the additive
algorithm's polynomial dependence on inverse tolerance.

## 7. Arbitrarily small coupling and the exact diagonal boundary

This extension passed [the first review addendum](../notes/review-bilevel-well-conditioned-box-exact-hardness.md)
and [a separate second review](../notes/review-bilevel-near-identity-corollary-second.md).

For every rational `0<eta<=1`, the same reduction can additionally enforce

```
||Q-I||_1 < eta,   ||Q-I||_infinity < eta,   ||Q-I||_2 < eta.
```

The construction runs in time polynomial in the formula length and the
binary encoding length of `eta`, and all output rationals have polynomial
encoding length in those inputs. To see this, replace `theta` throughout
by

```
theta_new=min{theta, eta/(10C)}
```

and rebuild `S` and `delta=s_N`. The new matrix obeys
`||B||_1,||B||_infinity<=2C theta_new<=eta/5`. Since
`Q-I=-B-B^T+B^TB`, both induced norms are at most
`2eta/5+eta^2/25<eta`; the spectral norm has the same bound. Decreasing
`theta` only improves every estimate in the relative-coordinate proof.
In particular (6) remains valid as an upper bound, and the scaled SAT gap
and the threshold reduction remain valid with the new `delta`.

The matrix is strictly diagonally dominant because

```
Q_ii-sum_(j!=i)|Q_ij| >= 1-||Q-I||_infinity > 0.
```

Thus exact hardness persists with arbitrarily small coupling, including
an exponentially small rational `eta`. This does not produce a constant
value gap: decreasing `eta` can make the readout scale smaller still.

At an exactly diagonal positive-definite `Q`, each response coordinate is
an affine function of the leader clipped to `[0,1]`. For a fixed leader
dimension, its `2N` threshold hyperplanes have polynomially many cells;
on each closed cell the upper objective is affine, so exact linear
optimization gives a polynomial-time algorithm. The corollary therefore
separates exact diagonal structure from arbitrarily small general
coupling. The additive theorem remains stable under these perturbations.

A supplied fixed-rank decomposition gives a different exact tractability
condition: `Q=Diag(d)+UHU^T` with positive `d`, fixed column count of `U`,
and fixed leader dimension permits exact optimization through polynomially
many linear programs. This allows arbitrarily large coupling and affine
upper constraints involving the response. See the
[source-qualified corollary](../notes/bilevel-fixed-rank-quadratic-corollary.md)
and its independent review. No algorithm for discovering such a decomposition
is asserted.
