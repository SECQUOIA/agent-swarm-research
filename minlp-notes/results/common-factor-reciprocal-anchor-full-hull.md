# Exact reciprocal-anchor hull with arbitrarily many box-bounded leaves

Date: 2026-09-04.

Status: theorem with complete proof; the common-factor author independently reviewed the full proof on 2026-09-04 and found it sound. The final written theorem also passed [root review](../notes/review-common-factor-root.md). The construction was independently identified in discussions between the common-factor author and reviewer. Novelty is unchecked. The argument uses classical one-dimensional distribution ideas, and these ingredients must not be presented as new. The proposed application is an exact hull and rational separation oracle for an anchored common-factor bilinear block.

The [literature audit](../notes/common-factor-literature-audit.md) identifies prior foundations in convex-order lattices and lift zonoids, and records application-level overlap risks. Those attributions apply to the call-function envelope and submeasure arguments below; any novelty assessment must concern the specific optimization application and consequences.

The mathematical claims have [Lean verification](../formal/topics/13-many-leaf-reciprocal/README.md),
including the actual hull, rational algorithms, and explicit arithmetic and
schoolbook bit-work models. The package records coverage, independent review,
and targeted checks. This does not verify the Python implementation or novelty.

## 1. Statement

Fix real `0<a<b`. Consider

```
K_n = conv{(X,1/X,Y_1,...,Y_n,XY_1,...,XY_n):
              a<=X<=b, 0<=Y_j<=1 for every j}.
```

Write the hull coordinates as `(m,t,q,w)`. For each such point define the function of a scalar `s`

```
C_*(s) = max{0, m-s,
             w_j-q_j s,
             m-w_j-(1-q_j)s : j=1,...,n}.              (1)
```

Define the convex function

```
T_*(m,q,w) = 1/a - (m-a)/a^2
              + integral_a^b 2 C_*(s)/s^3 ds.          (2)
```

**Theorem.** A point belongs to `K_n` if and only if it satisfies

```
0<=q_j<=1,
a q_j<=w_j<=b q_j,
a(1-q_j)<=m-w_j<=b(1-q_j)              for every j,

T_*(m,q,w) <= t <= (a+b-m)/(ab).                       (3)
```

For `n=0`, include `a<=m<=b` explicitly; for `n>=1` these bounds follow from (3). They may also be included explicitly in every case. When the endpoints and candidate coordinates are rational, the lower bound in (3) admits exact polynomial-time evaluation and a rational linear separation oracle. An upper envelope of `2n+2` affine functions suffices. No enumeration of `2^n` leaf endpoint patterns is needed for membership or separation.

An anchor product `w_0=p>0` yields the coordinate `t=y_0/p`. A leaf box `[l_j,u_j]`, with `l_j<u_j`, is normalized by

```
q_j = (y_j-l_j)/(u_j-l_j),
v_j = (w_j-l_j m)/(u_j-l_j),
```

and `v_j` replaces `w_j` in (1)–(3). Fixed leaves contribute linear equations. The theorem does not allow additional product bounds or linking constraints on the original points without further convexification. If `a=b`, the hull is linear.

## 2. Proof

For a probability distribution `mu` on `[a,b]`, define its call function

```
C_mu(s) = E_mu[(X-s)_+].
```

This function is convex, equals `m-s` for `s<=a`, equals zero for `s>=b`, and has slopes between `-1` and zero. Conversely, a convex piecewise affine function with these two exterior pieces is a call function: put probability mass equal to each upward slope jump at its breakpoint. The total mass is one; evaluating at `a` gives its mean as `a+C_mu(a)=m`.

### Which leaf moments can a fixed common-factor distribution realize?

Given `mu` and a desired mass `q in [0,1]`, select a fractional submeasure by a function `theta(X) in [0,1]` with `E[theta]=q`. Its first moment is `E[X theta]`. The largest possible first moment is

```
U_mu(q) = inf_s {q s+C_mu(s)}.                        (4)
```

Indeed, pointwise `theta(X)(X-s)<=(X-s)_+` gives the upper bound for every `s`. Equality is attained by selecting the largest `X` values, with fractional selection of an atom at the threshold if needed. The smallest possible first moment is `m-U_mu(1-q)`, by applying the same argument to the complementary submeasure. All values between these endpoints occur by convex mixing of maximizing and minimizing selection functions.

Consequently `(q,w)` is realizable as `(E[Y],E[XY])`, with `0<=Y<=1`, if and only if

```
w-q s <= C_mu(s),
m-w-(1-q)s <= C_mu(s)                    for every s. (5)
```

This includes `q=0` and `q=1`. For several leaves, each admissible selection function can be chosen on the same `mu`. They need not agree with each other. Set `Y_j=theta_j(X)` deterministically for each leaf. These continuous leaf values lie in `[0,1]` and realize all moments simultaneously.

### The least feasible call function exists explicitly

Every distribution with mean `m` that realizes all the leaves must satisfy `C_mu>=C_*`: (5) gives the leaf lines, and `C_mu>=max(0,m-s)` always holds.

Under the linear inequalities in (3), `C_*` is itself a valid call function. It is the maximum of affine functions and hence convex. Each line has slope in `[-1,0]`. For `s<=a`, the line `m-s` dominates every leaf line: for example,

```
(m-s)-(w_j-q_j s)
 = m-w_j-(1-q_j)s >= (1-q_j)(a-s) >= 0.
```

The other leaf line follows from `w_j>=a q_j`. For `s>=b`, both leaf lines are nonpositive by their upper McCormick bounds, as is `m-s`. Thus `C_*=m-s` to the left of `a` and `C_*=0` to the right of `b`.

Let `mu_*` be the finite distribution given by its slope jumps. It has support in `[a,b]`, mean `m`, and satisfies (5) for every leaf. Hence all the leaf moments can be realized on `mu_*`. Its support has at most `2n+1` points, since the upper envelope has at most `2n+2` affine pieces.

### The reciprocal moment is minimized by this distribution

For every twice continuously differentiable function `f` on `[a,b]`, the pointwise identity

```
f(X) = f(a)+f'(a)(X-a)
        + integral_a^b f''(s)(X-s)_+ ds
```

gives, for `f(X)=1/X`,

```
E_mu[1/X] = 1/a-(m-a)/a^2
              + integral_a^b 2 C_mu(s)/s^3 ds.         (6)
```

Since the integrand weight is positive and every feasible `C_mu` dominates `C_*`, (6) proves that the smallest possible reciprocal moment is exactly `T_*`, attained by `mu_*`.

The largest reciprocal moment for any distribution on `[a,b]` with mean `m` is `(a+b-m)/(ab)`, attained by the distribution `mu_end` on the endpoints with that mean. This follows from the reciprocal secant. Its call function dominates every call function supported on `[a,b]` with mean `m`: apply the secant inequality to the convex function `(X-s)_+`. In particular, `C_mu_end>=C_*`, so `mu_end` also permits every leaf in (3).

For any `t` between the stated extrema, a convex mixture of `mu_*` and `mu_end` has reciprocal moment `t`; its call function still dominates `C_*`. Therefore it permits all the leaf moments simultaneously by (5). If the two extrema coincide, simply use `mu_*`. The distributions have finite support, and setting `Y_j=theta_j(X)` yields a finite convex combination of original points with at most `2n+3` support points. This proves sufficiency. Necessity follows from the same arguments. ∎

## 3. Exact rational evaluation and separation

Throughout this section, assume that `a,b` are rational. The hull theorem above does not require this restriction.

At a rational candidate point satisfying the linear inequalities, construct the upper envelope (1) on `[a,b]`. Sort the line slopes, discard dominated parallel lines, and compute the upper envelope. There are `O(n)` segments, and a standard line-envelope construction uses `O(n log n)` rational arithmetic operations. Its breakpoints are rational intersections of lines with rational coefficients.

On an envelope interval `[alpha,beta]` whose active line is `U-V s`, integrate exactly:

```
integral_alpha^beta 2(U-V s)/s^3 ds
 = U(alpha^(-2)-beta^(-2))
    - 2V(alpha^(-1)-beta^(-1)).                       (7)
```

Here `U,V` are affine functions of the hull coordinates: `(0,0)`, `(m,1)`, `(w_j,q_j)`, or `(m-w_j,1-q_j)`. Formula (7) computes `T_*` using rational arithmetic. Intersections, interval endpoints, and coefficients have polynomial bit length; summing a polynomial number of rational quantities preserves a polynomial bit bound. Thus the algorithm has polynomial bit complexity, not merely an arithmetic-operation bound.

If a point violates a linear inequality in (3), that inequality separates it. Otherwise, if its `t` is smaller than `T_*`, retain the active lines and interval boundaries found at that point. Treat their boundaries as fixed rational constants, and form the affine function `L(m,q,w)` by replacing the integral in (2) with the sum (7) for those chosen lines. For every other point, each chosen line lies below its maximum in (1), so

```
L(m,q,w) <= T_*(m,q,w).
```

Equality holds at the candidate. Therefore

```
t >= L(m,q,w)                                        (8)
```

is a globally valid rational linear inequality and strictly separates that candidate. The upper reciprocal secant handles a reciprocal moment that is too large. This proves an exact rational separation oracle.

For a rational feasible point, the proof also constructs an explicit rational convex decomposition into at most `2n+3` original graph points. The slope jumps of `C_*` give rational probabilities at rational locations; the endpoint mixing weight is rational. For each leaf, sort this finite support and select its lower and upper `q_j` tails, splitting a boundary atom fractionally if needed. Convex interpolation between these two selection functions attains `w_j`. All calculations have polynomial bit complexity.

The cut family consists of partitioning `[a,b]` at finitely many rational endpoints, assigning one of the lines in (1) to each interval, and integrating those lines as in (7), with the affine initial term from (2). Every such cut is valid. At a rational candidate, choosing its upper envelope gives exact separation.

The family also characterizes the lower bound at real candidate coordinates satisfying `0<=q_j<=1`. To prove this, partition `[a,b]` into `N` equal intervals of rational length `delta=(b-a)/N`. On each interval `[alpha,beta]`, retain a line `ell` active at its left endpoint. All lines in (1) have slopes in `[-1,0]`, so, for `alpha<=s<=beta`,

```
0 <= C_*(s)-ell(s) <= s-alpha <= delta.
```

Indeed, every other line starts below `ell` at `alpha` and can gain on it at rate at most one. The affine expression `L` formed from these selected lines therefore satisfies

```
0 <= T_*-L <= 2 delta (b-a)/a^3.
```

If `t<T_*`, choose `N` large enough that this error is smaller than `T_*-t`; then `t<L`. The knots and the chosen line indices define rational affine coefficients even when the candidate coordinates are real. Thus these cuts, together with the linear bounds and reciprocal secant, describe the hull at all real candidates for rational `a,b`. This approximation argument proves completeness; the polynomial-time separation algorithm above takes rational input. No polynomial-size explicit formulation is asserted. The [Lean proof](../formal/Formal/ReciprocalAnchor/ManySeparation.lean) records the approximation and completeness as `exists_rationalCut_approx` and `all_rationalCuts_iff_lowerMoment`.

## 4. Relationship to the one-leaf hull and two-leaf obstruction

For one leaf, the least feasible distribution has the two conditional-mean locations `w/q` and `(m-w)/(1-q)`, with masses `q` and `1-q`, omitting zero-mass cases. Thus

```
T_* = q^2/w+(1-q)^2/(m-w),
```

which recovers the exact two-SOC hull in [the small-block note](common-factor-reciprocal-anchor-hulls.md).

For the rational two-leaf example `m=2`, `(q_1,w_1)=(2/3,5/3)`, `(q_2,w_2)=(14/29,40/29)`, on `[1,3]`, exact envelope construction gives

```
T_* = 31/50,
mu_* = (1/3) delta_1 + (16/87) delta_(25/16)
                       + (14/29) delta_(20/7).
```

Thus its proposed reciprocal moment `3/5` misses the exact hull by `1/50`.

For multiple leaves, separately satisfying the one-leaf lower bounds need not satisfy the full-envelope lower bound. The rational two-leaf example in that note has incompatible individual equality distributions, and the full envelope combines their necessary call-function inequalities into a strictly larger reciprocal lower bound. The explicit rational joint cut there is one concrete manifestation of this distinction.

## 5. Validation and remaining checks

[The verification script](../code/common-factor-anchor-verify.py) uses exact rational arithmetic to construct envelopes and their slope-jump distributions. It passed 150 seeded comparisons, with one through ten leaves, against an independently formulated shared-measure LP. That LP uses a finite scalar grid enriched with the derived distribution atoms and enforces each selected leaf submeasure between zero and the common measure. LP comparisons use floating-point HiGHS; the moment identities, envelope integrals, and displayed counterexample value are checked exactly. These are implementation cross-checks and do not replace the continuous-support proof. The verification implementation uses all pairwise line intersections, rather than implementing the faster envelope algorithm.

1. Final root review of the written theorem and construction completed; no unresolved mathematical issue found (see the linked review).
2. Literature comparison with convex-order lattices, call-function envelopes, zonoids, perspective/disjunctive formulations, and the common-variable bilinear convexification literature. No publication novelty claim is justified before this comparison.
