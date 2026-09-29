# Independent review of the exact-penalty geometry note

Date: 2026-09-25. Reviewed file: [penalty-geometry.md](penalty-geometry.md).
Scope: the compact-set duality formula, support count, threshold formula,
scalar sign cases, slice bound, and their relationship to prior theory.

**Verdict.** The mathematical statements in the reviewed note are correct
under their stated assumptions. They are useful supporting results, with no
substantiated claim of new general duality theory. A material error was found
in a cited source's example: it distinguishes failure of finite multiplier
attainment from dual value exactness incorrectly. The source correction is
derived separately below and was independently rederived by the root agent.

## 1. Convexification and the support count

The proof of Proposition 1 works without convexity of `X`, `f`, or `r`, and
without dual attainment. Continuity and compactness make the image

```
S_rho = {(r(x), f(x)+rho||r(x)||): x in X}
```

compact. Its convex hull is compact in `R^(m+1)`, so the lowest point of its
intersection with the vertical line through zero exists. Strict separation
of `(0,a)` from that convex hull for `a<w` is justified. Evaluating the
separator at `(0,w)` gives `beta(w-a)>0`, which establishes the essential
sign `beta>0`. Division by `beta` is therefore valid. No constraint
qualification is being smuggled into this argument.

The `m+1` support count is also correct. Ordinary Caratheodory first gives
at most `m+2` points. An optimal combination with more than `m+1` positive
weights has a nonzero null vector for the columns `(1,r(x_i))`. Both signs
of a sufficiently small weight perturbation remain feasible. Optimality
forces zero objective derivative along that vector. Moving to the first
vanishing weight preserves value and removes a support point.

The support bound cannot be improved in general. Take a finite native set
with one feasible point having `(r,f)=(0,0)`, together with `m+1` points
whose residuals are

```
e_1, ..., e_m, -(e_1+...+e_m)
```

and whose costs are all `-1`. At `rho=0`, every optimal balanced mixture has
cost `-1`, places no mass on the feasible point, and uses all `m+1`
infeasible points. Their unique balanced weights are `1/(m+1)`.

This is the classical finite moment problem geometry. For background,
[Winkler (1988)](https://doi.org/10.1287/moor.13.4.581) studies extreme
probability measures under finitely many moment conditions;
[Pinelis (2012/2016)](https://arxiv.org/abs/1204.0249) gives general atomic
representation results with a support bound determined by the number of
moment restrictions. The mass restriction accounts for the additional one
in this note's `m+1`. These sources' abstracts and bibliographic records
were checked; their full general theorems are not needed for the elementary
proof given here. Do not present this support reduction as a new result.

## 2. The smallest threshold

Corollary 2 is valid, including its endpoint claim. It is enough to require
the inequalities for mixtures with at most `m+1` points because, for each
fixed `rho`, Proposition 1 supplies an optimizer of that size. This does
not require one common mixture to be optimal for every penalty.

For `s_mu=0`, nonnegativity of all weights and of the norm implies that
every point of positive mass has zero residual. Hence `c_mu>=v`. For
`s_mu>0`, exactness is equivalent to

```
rho >= (v-c_mu)/s_mu.
```

If the supremum is finite, every one of these weak inequalities holds at
the supremum. No maximizing ratio or positive lower bound on `s_mu` is
needed. If the supremum is infinite, every finite candidate penalty is
violated by some balanced mixture. The empty supremum convention is stated
adequately in the note.

This remains a dual *value* threshold. In particular, its attainment as a
real number does not imply an attaining Lagrange multiplier. That
distinction is essential in Section 4 below.

## 3. Scalar residuals and the slice bound

With both signs present, neither `A_plus` nor `A_minus` can equal negative
infinity: each supremum is over a nonempty collection of finite real
numbers. Thus the sum is unambiguous even if one of them is positive
infinity.

The multiplier interval in Proposition 3 has the correct signs. Its
nonemptiness gives `2rho>=A_plus+A_minus`, including cases where either
finite `A` is negative. To check the concern about a nonattained dual
supremum independently, fix points with residuals `a>0` and `-b<0`. Any
sequence with `L_rho(lambda_j)` bounded below satisfies a lower bound on
`lambda_j` from the positive point and an upper bound from the negative
point. A convergent subsequence exists. Upper semicontinuity of `L_rho`
then proves attainment whenever its supremum equals `v`. The same argument
rules out exactness if either `A` is infinite.

There is also a direct check using the moment formula. The balanced pair
at these two residuals has weights `b/(a+b)` and `a/(a+b)`, and its ratio is

```
(v-c_mu)/s_mu
  = (1/2) [(v-f(x_plus))/a + (v-f(x_minus))/b].
```

The two points can be chosen independently. Taking the supremum therefore
recovers `(A_plus+A_minus)/2`, including the infinite cases. This derivation
does not depend on multiplier attainment.

The one-sided case is correct: a balanced mixture of nonnegative scalar
residuals uses only zero residuals, so `D_0=v` and hence `D_rho=v` for every
`rho>=0`. A concrete nonattainment example is

```
X=[0,1],  r(x)=x,  f(x)=-sqrt(x),  v=0.
```

For every finite `lambda` and `rho`, a sufficiently small positive `x`
makes `-sqrt(x)+(lambda+rho)x<0`. Nevertheless `D_rho=0`. Conversely,
`X=[-1,1]`, `r(x)=x`, `f(x)=-sqrt(abs(x))` has both `A` values infinite;
the equally weighted pair `x=t,-t` gives value
`-sqrt(t)+rho*t<0` for sufficiently small `t>0`, for every multiplier.

The feasible/infeasible slice bound has no missing factor. On a feasible
slice,

```
lambda_z^T r <= ||lambda_z||_* ||r|| <= M||r||,
```

and on an infeasible slice the cost is at least `L+rho*delta`. Taking the
maximum of `M` and `(U-L)/delta` is sufficient. It gives exactness for the
specified multiplier zero, which is stronger than dual value exactness.
The existence of the assumed global slice multipliers needs justification
in applications; slice Slater is sufficient in the convex setting, but the
note's abstract slice result explicitly assumes the multiplier inequality.

## 4. Separate correction to Lefebvre--Schmidt Example 13

The source is the [December 15, 2025
manuscript](https://optimization-online.org/wp-content/uploads/2024/07/exact-penalty-for-minlp-1.pdf),
Definition 1 and Example 13. Its dual value is a supremum over multipliers.
The example is described as having no finite exact penalty representation.
The following independent calculation shows that its dual value is exact
for every nonnegative penalty; finite multiplier attainment fails instead.

Write the example's native variables as `(u,s,z)`:

```
X = {(u,s,z) in [-1,1]^2 x {0,1}:
     u+2z<=1, u^2<=s},
f(u,s,z)=u-z/2,    r(u,s,z)=s.
```

The dualized equality is `s=0`. It forces `u=0` and then `z=0`, so `v=0`.
Throughout `X`, however, `s>=u^2>=0`. This is precisely the one-sided
setting of Proposition 1, so already `D_rho=0` for every `rho>=0`.

For a completely separate verification, set `t=lambda+rho`. Since `s>=0`,
the augmented objective is `u-z/2+t*s`. If `t>=1/2`, then:

* At `z=1`, the only native point is `(-1,1,1)`, of value `t-3/2`.
* At `z=0`, minimizing first over `s` gives `s=u^2`. Completing the square
  shows that the minimum is `-1/(4t)`, attained at `u=-1/(2t)`.

Consequently,

```
L_rho(lambda) = min(t-3/2, -1/(4t))       for t>=1/2.
```

In particular, for `t>=2` this equals `-1/(4t)`. Sending `lambda` to
positive infinity gives `D_rho>=0`; weak duality gives the reverse
inequality. On the other hand, for every finite `t` choose `0<epsilon<=1`
small enough that

```
-epsilon+t*epsilon^2<0.
```

The native point `(-epsilon,epsilon^2,0)` proves
`L_rho(lambda)<0`. Thus the exact supremum is never attained at a finite
multiplier, at any finite penalty. Lemma 3 of the source transports an
*attained* exact penalty from one fixed multiplier to another after
increasing the penalty; it cannot turn nonattainment into a positive dual
gap.

There is a smaller arithmetic error in the source's displayed value at
`lambda=0`. For `rho>=1/2`, the equality

```
min(rho-3/2, -1/(4rho)) = -1/(4rho)
```

holds only when `rho >= (3+sqrt(5))/4`. At `rho=1/2`, the two terms are
`-1` and `-1/2`. This error does not change its valid fixed-multiplier
nonattainment conclusion.

This correction does not refute the source's sufficient theorem under
slice Slater conditions. It invalidates this example's claim of a positive
dual gap at every finite penalty under the source's own value-based
definition. It also does not affect the neighboring bit-complexity
construction, which uses residuals of both signs. The root agent
independently rederived the two slice minima, the dual limit, and the
correct crossing value before this review was finalized.

## 5. Positioning and changes recommended

Keep the geometry note as supporting theory. A finite moment formulation,
its support bound, and the scalar elimination calculation are not by
themselves evidence of a substantial original contribution. The current
note already respects this limitation.

The broader distinction between exact penalty functions and existence of
augmented Lagrange multipliers is studied, under explicit additional
conditions, by [Dolgopolik, *Existence of augmented Lagrange multipliers:
reduction to exact penalty functions and localization
principle*](https://arxiv.org/abs/1802.03046). Its abstract and revision
record were checked. This is background rather than a checked theorem
equivalent to the scalar formula here. A novelty claim for the latter
would require a more precise literature comparison than this review.

Two small edits to the introductory source description would improve
precision:

1. Say that Theorem 14 works under **convexity of the continuous slices**,
   compactness, and its slice Slater assumptions. Convexity is stated in
   the surrounding source section and is used in its proof.
2. Replace “Its conclusion asks” with “The paper's conclusion asks” so
   that the open bit-complexity question is attributed to the paper's
   concluding discussion, not the statement of Theorem 14.

Preserve the one-sided paragraph and explicitly link the source correction
if the note discusses the necessity of slice regularity. Do not repeat
the source's Example 13 as a counterexample to finite dual value exactness.

## Verification record and limits

The principal verification was independent mathematical derivation,
including the separation sign, support reduction, pair-mixture ratio,
compactness of scalar maximizing sequences, and both slices in the source
example. No numerical optimizer, Lean proof, or project-wide verification
was used. CI status and logs were not inspected.

A targeted exact-arithmetic check was also run with Python's standard
`fractions.Fraction`, in an inline `python - <<'PY'` command. It evaluated
the two source-example slice values at
`t=1/2,1,2,10,100`, verified the stationary point lies in `[-1,1]`, and
checked `u+t*u*u=-1/(4t)` exactly. The respective minima were

```
-1, -1/2, -1/8, -1/40, -1/400.
```

Those checks establish exact arithmetic at the specified values; the
general optimization formula and limiting argument are established by the
proof above, not by this finite calculation. Local literature filenames
were searched for the relevant authors and penalty/duality terms; no
matching local version of the principal cited manuscript was found in
`literature/papers`, so its openly accessible primary PDF was used.
