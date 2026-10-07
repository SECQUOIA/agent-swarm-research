# First independent audit of conditioned box-follower exact hardness

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](bilevel-well-conditioned-box-exact-hardness.md) transfers a Boolean score gap through a uniformly well-conditioned box QP using a valid componentwise error estimate. The SAT gap, polynomial encoding, bounded coefficient magnitudes, and NP-membership argument all hold. Novelty of the strengthened restriction is separate from this correctness audit.

## 1. Exact intermediate network

The displayed recursion for `t_i` satisfies `t_(i+1)=3t_i-2y_i`. On its three consecutive subintervals, this is respectively `3t_i`, `2-3t_i`, and `3t_i-2`; all map into `[0,1]`. Hence every leader in `[0,1]` produces `t_i,y_i in [0,1]`. The ReLU difference is exactly `clip(3t_i-1)`, and the individual coordinate bounds are `alpha_i<=2`, `beta_i<=1`, `p_i<=1`, and `v_a<=1`.

The preactivations for the two base coordinates are at least `-1` and `-2`. Readout preactivations are at least `-1` for `p_i` and at least `-2` for a three-literal clause. Thus the exact network residual `h-Ah-b0-xb1` is coordinatewise in `[0,2]`. This bound is uniform over the full leader interval, not only Boolean witnesses.

The ordering makes `A` strictly lower triangular. Expanding `3t_i` gives coefficients at most `2*3^n` in magnitude; the leader coefficients are at most `3^n`, and the readout coefficients at most two. Dimension and rational data size are polynomial in the formula size.

The score identity follows from `y_i-p_i=min(y_i,1-y_i)`. At the rational leader for a Boolean word, each ternary remainder lies strictly below `1/3` for a zero bit and strictly above `2/3` for a one bit. This verifies Boolean coverage without needing any QP representation to be exact. A satisfying assignment gives score zero. For an unsatisfiable formula, rounding any continuous `y` makes some clause false; its literal values are the corresponding minority amounts. Distinct variables ensure their sum is at most `D(y)`. The resulting lower bound `2D+2max(0,1-D)>=2` is valid, including ties at one half. The earlier proof's preprocessing to three distinct variables is sound.

## 2. Scaling, conditioning, and data size

All scales are positive and satisfy `s_i=s_1 theta^(i-1)`. The similarity transform has entries `B_ij=A_ij theta^(i-j)` below the diagonal. Both its row and column absolute sums are bounded by `C theta/(1-theta)`, and the parameter choice is more than sufficient to bound these by `1/50`. Therefore `||B||_2<=sqrt(||B||_1 ||B||_infinity)<=1/50`.

The singular values of `I-B` lie in `[49/50,51/50]`. Squaring yields the claimed absolute eigenvalue bounds for `Q=(I-B)^T(I-B)`. In particular its condition number is at most `(51/49)^2<2`. Entry magnitudes of `Q` are bounded by its spectral norm and are below two.

After omitting the leader-only term in the square objective, the normalized coefficients are `c=-(I-B)^T S b0` and `d=-(I-B)^T S b1`. Their infinity norms are at most `(51/50)/4<1`. The upper coefficients are also bounded by two by the final scaling. The normalized objective is the bounded-coefficient model in the theorem; the optional full residual-square expression explains joint convexity without changing responses.

Writing `L=log(NC)`, the integer `M=(1+NC)^N` has `O(NL)` bits; `theta` has a denominator with `O(NL)` bits; and each `s_i` and its inverse have `O(N^2 L)` bits. Dense rational matrix multiplication and expansion involve only polynomially many such operations and preserve polynomial encoding length. Small amplitudes therefore do not create an exponentially long output instance.

## 3. Uniform relative-coordinate bound

The scaled exact network is in the unit box and satisfies its stated clipped fixed-point equation. Its upper clipping never changes the ReLU output because `s_i h_i<=1/(2C)<1`. For the true QP minimizer, box KKT conditions are exactly equivalent to the projected-gradient equation with step one. This equivalence does not require step one to define a convergent optimization iteration.

Set `z=S^-1 u-h`. Nonexpansiveness of the scalar clip and positivity of the scales give

```
|z|<=|A||z|+S^-1 |B|^T S |S^-1 r|.
```

The transpose contribution is

```
U=S^-1 |B|^T S=S^-2 |A|^T S^2,
U_ik=|A_ki| theta^(2(k-i))  for k>i.
```

The square on the scale ratio is essential and is correct. The residual decomposition is exact:

```
S^-1 r=(I-A)z+rstar.
```

Using `|rstar|<=2` gives the candidate's inequality (5), with no prior assumption on the size of `z` or on QP active sets.

For `P=|A|`, nilpotence makes `T=(I-P)^-1` a finite nonnegative matrix. Multiplying the componentwise inequality `(I-P)e<=U[(I+P)e+2*1]` by this nonnegative matrix preserves its direction even though `(I-P)e` need not itself be nonnegative. The norm estimates are

```
||T||_infinity<=M,
||U||_infinity<=2C theta^2,
a:=||TU(I+P)||_infinity<=2MC(1+NC)theta^2<1/2.
```

Hence `(1-a)||e||_infinity<=4MC theta^2` and

```
||e||_infinity<=8MC theta^2
              =1/(1250 N^2 C M)
              <=1/(16N).
```

All constants and inequalities check out. This controls relative-coordinate errors even in the final extremely small coordinates. A bound only on `||u-Sh||` would not justify the readout; the proof does supply the stronger bound needed.

## 4. Upper gap and exact decision membership

With `delta=s_N`, each readout coefficient is `delta ell_i/s_i` and has magnitude at most two. Since `||ell||_1=2N`, the preceding bound yields uniform readout error at most `delta/8`. At a satisfying Boolean leader, the actual QP readout is therefore at most `delta/8`. In an unsatisfiable instance, it is at least `2delta-delta/8=15delta/8` at every leader. Threshold `delta` preserves the SAT yes/no direction for upper **minimization**. Nonnegativity of the approximate readout is unnecessary and is not used.

The unique minimizer of a continuous strictly convex objective on the fixed compact box depends continuously on the scalar leader, by a compact-subsequence optimality argument. Thus the global upper minimum is attained. For any yes threshold instance, choose the lower/free/upper statuses at a qualifying response. The principal free-coordinate matrix is positive definite; its inverse gives a rational affine response as a function of the leader. Box feasibility, endpoint gradient signs, and the linear upper threshold then define a nonempty closed rational interval in `[0,1]`. Its endpoints and a contained rational leader have polynomial bit size by determinant bounds. The resulting rational follower also has polynomial bit size.

These data form a polynomial certificate checked by exact rational box KKT conditions and the upper inequality. Degenerate active statuses are allowed through non-strict inequalities. This proves NP membership in the restricted class. If the eigenvalue and coefficient restrictions are treated as language conditions rather than promises, their rational semidefinite comparisons and entry bounds are also decidable in polynomial time.

Finally, `log(1/delta)` is polynomial in the source length. Calling an additive value algorithm at tolerance `delta/4` leaves both yes and no values strictly separated by threshold `delta`. Polynomial dependence on accuracy bits would therefore imply `P=NP`. Polynomial dependence on inverse tolerance is consistent with this exponentially small gap; no fixed-gap or strong-hardness conclusion follows.

## 5. Independent exact checks

The independently written [rational checker](../code/bilevel_dense_box/check_conditioned_hardness_first_review.py) constructs the normalized QP, solves rational principal active systems, and accepts a follower only after checking the full exact box KKT conditions. It then verifies the relative-coordinate bound and the readout error with exact fractions. Cases include endpoints, ReLU breakpoints, Boolean leaders, and a three-variable unsatisfiable formula containing all eight sign clauses. Floating-point conditioning is not used to validate coordinates of tiny amplitude.

Run with `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/bilevel_dense_box/check_conditioned_hardness_first_review.py`. It passed 42 exact follower/KKT/error/gap checks using 390 rational active systems, with follower dimensions up to 17. These finite checks complement the uniform proof and do not establish the complexity claim by themselves.

## 6. Near-identity and strict diagonal dominance addendum

The author's subsequent corollary also passes. For a rational input `0<eta<=1`, replace the original scaling ratio by `theta'=min(theta,eta/(10C))`, then rebuild every scale and `delta`. Both absolute row and column norms of `B` are at most `2C theta'<=eta/5`. Since `Q-I=-B-B^T+B^T B`, submultiplicativity gives

```
||Q-I||_1, ||Q-I||_infinity
    <=2eta/5+eta^2/25<eta.
```

The spectral norm is bounded by the geometric mean of these two norms and hence is also below `eta`. The original cap on `theta'` retains every original conditioning and coefficient bound. All relative-coordinate estimates improve when the ratio decreases, so the same SAT gap proof holds with the rebuilt smaller `delta`.

In particular, `||Q-I||_infinity<1` implies `Q_ii-sum_(j!=i)|Q_ij|>0` on every row. The Hessian is strictly diagonally dominant with positive diagonal. This establishes the stated stronger exact-hardness restriction, without a fixed-gap assertion.

Using `eta` directly gives polynomial construction time and output size in the source length **plus the binary encoding length of the rational eta**. It does not automatically give a bound depending only on `log(1/eta)` for arbitrary rational encodings. The author agreed to state the former bound. If an output-size bound in `log(1/eta)` is wanted instead, use the dyadic lower approximation `2^(-ceil(log2(1/eta)))` in the cap; reading and computing from the original eta still takes time polynomial in its input encoding. No encoding concern remains with the agreed statement.
