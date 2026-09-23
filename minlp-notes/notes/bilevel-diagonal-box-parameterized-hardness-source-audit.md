# Diagonal box followers: parameterized hardness is an existing ReLU consequence

Date: 2026-09-05. Status: direct primary-source overlap found. Do not claim
new W[1]-hardness or ETH lower bounds for the scope below.

The proposed boundary has an affine upper objective, `r` unit-box leader
variables, and a strictly convex diagonal quadratic follower over a unit box.
The follower has no coupling constraints, and the upper level has no constraints
beyond its box. Parameterized hardness in `r`, even with an identity follower
Hessian and a fixed additive decision gap, follows directly from an existing
shallow-ReLU construction. A new clique reduction can be useful as an alternative
proof, but does not establish a new complexity classification for this class.

## Exact primary predecessor

[Froese, Grillo, Hertrich, and Stargalla, Parameterized Hardness of Zonotope Containment and Neural Network Verification](https://arxiv.org/pdf/2509.22849v1),
September 2025, Proposition 3.1, constructs a two-layer ReLU function on `k`
inputs from Multicolored Clique. Its maximum is `C=k+binom(k,2)` in the yes
case and at most `C-1` otherwise. Theorem 4.2 and Corollary 4.3 establish
W[1]-hardness and the ETH exclusion of `rho(k) N^(o(k))` algorithms.
Appendix B.5 explicitly restricts witnesses to a polynomially bounded box.
The first-layer rows use at most two inputs and have polynomial-magnitude
rational data; output coefficients are signs. The
[September 3, 2026 version](https://arxiv.org/pdf/2509.22849v3)
retains the construction as Proposition 4.1 and gives the corresponding
results in Theorem 5.3 and Corollary 5.5. It identifies the ICLR 2026
conference version as its predecessor. The obstruction therefore predates
the present repository investigation; it is not only a recent new claim
in the expanded version.

## Explicit transfer to a diagonal strongly convex box follower

The following elementary translation explains why the bilevel restrictions do
not evade that predecessor. It is recorded as a corollary calculation, not as
an independent new hardness proof.

Write the constructed network, restricted to a rational box `[0,L]^k`, as

```
f(t)=sum_(i=1)^m sigma_i max(0,h_i(t)),
sigma_i in {-1,1},
```

where `h_i` is rational affine. Choose `L` to include all yes-instance
witnesses, and put `t=Lx` for `x in [0,1]^k`. There is no requirement that
all maximizers lie in this box: a yes witness lies there, while the no-instance
upper bound holds everywhere. Expand `h_i(Lx)=a_i^T x+beta_i`.

Take a positive integer

```
R >= 1+max_i (|beta_i|+sum_j |a_ij|).
```

The predecessor's polynomial coefficient magnitudes allow a polynomially
bounded choice of `R`. For each leader choice, use the follower

```
min_(y in [0,1]^m) (1/2) sum_i [y_i-h_i(Lx)/R]^2.
```

It has the unique response

```
y_i(x)=clip(h_i(Lx)/R,0,1)=max(0,h_i(Lx))/R.
```

The second equality holds because the positive affine range does not reach
the clipping upper bound. Its Hessian in `y` is exactly the identity.
Dropping terms depending only on `x` gives the conventional follower form
`(1/2)y^T y+(c+Dx)^T y`; retaining the squares also exhibits joint convexity
of an equivalent follower objective.

Choose the affine upper objective

```
C-R sum_i sigma_i y_i.
```

The bilevel minimum is zero in a yes instance and at least one in a no
instance. All feasible follower problems are strictly convex box problems;
there are no response-dependent upper constraints. The leader dimension
remains exactly `k`. Construction size and coefficient encoding remain
polynomial, so both the parameterized and ETH conclusions transfer.

## Extra numerical restrictions do not restore novelty

The normalized follower coefficients `a_ij/R` and `beta_i/R` have magnitude
at most one. Two-input sparsity of every nonconstant follower row is
preserved. If upper-objective coefficients must also have magnitude at most
one, replace every follower coordinate by `R` independent copies with the
same response and coefficient `-sigma_i` in the upper objective. This is
still polynomial size because `R` has polynomial numerical magnitude, not
merely polynomial bit length. The follower Hessian remains the identity.

If even the affine objective constant must be eliminated, add `C` independent
boxed follower coordinates minimizing `(u-1)^2/2` and give each coefficient
one in the upper objective. Their unique responses are one. Thus upper
coefficients in `{-1,1}`, coefficient magnitudes at most one in the follower
linear terms, unit boxes, polynomially bounded rational denominators, identity
Hessian, two-input coupling rows, and a `0` versus `>=1` gap are all available
through routine transformations of the same prior construction.

This is not a fixed finite numerical alphabet result: denominators and
coefficient values may vary with the input. Nor does constant *absolute*
gap imply constant gap after normalizing by the sum of all upper weights.
The duplication step can increase that sum polynomially. Those distinctions
matter when comparing normalized additive approximation guarantees.

## Consequences for this investigation

The proposed direct clipped-ramp reduction can be retained with explicit
attribution as an alternative proof or a convenient bilevel specialization.
Its use of simple coordinate labels and piecewise-linear edge penalties may
be easier to explain than the predecessor's encoding, but such a proof change
does not justify a new W[1]/ETH result. A claimed stronger theorem needs a
restriction or quantitative guarantee that the transfer above does not give.

The author retained that proof in
[the diagonal leader-dimension boundary note](bilevel-diagonal-leader-dimension-boundary.md).
A limited sanity check here found its half-grid distance formula, mixed-radix
edge interpolation, continuous rounding gap, identity-Hessian realization,
and difference-of-two-scaled-ReLUs normalization consistent. This is not a
substitute for a complete independent proof audit before reuse in a theorem.

The fixed-`r` arrangement algorithm and the `N^(O(r))` dependence remain
consistent with this known boundary. Hardness here concerns a variable number
of leaders; it does not contradict polynomial algorithms for each fixed `r`,
nor does it explain the separate single-leader hardness with a dense follower
Hessian. Neural-network *training* hardness is also not the relevant source:
the direct predecessor optimizes the input of an already specified shallow
network, exactly the setting represented by the diagonal follower response.

No further broad literature search is needed to establish this overlap.
The stronger recent papers about Lipschitz constants of input-convex networks
and zonotope norm maximization concern different functionals and are not
needed for the transfer. The exact restrictions above should be checked if
the candidate is retained, but plain novelty is already excluded by the
primary predecessor and this explicit reduction.
