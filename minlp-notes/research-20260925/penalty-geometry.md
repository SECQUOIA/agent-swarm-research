# Geometry of the smallest exact norm penalty

Date: 2026-09-25. Status: supporting derivations, independently reviewed.
These are consequences of convexification and elementary Lagrangian duality,
not a claim to a new general duality theory. Their purpose is to explain the
penalty encoding and complexity constructions in this research continuation.

## 1. Model and distinction between two thresholds

Let `X` be a nonempty compact set, let `f: X -> R` and
`r: X -> R^m` be continuous, and assume `F={x in X:r(x)=0}` is nonempty.
Write

```
v = min_F f,
L_rho(lambda) = min_X [f(x) + lambda^T r(x) + rho ||r(x)||],
D_rho = sup_lambda L_rho(lambda),       rho >= 0.
```

The norm is fixed. Exactness here means `D_rho=v`. This differs from
exactness with a specified multiplier, such as `L_rho(0)=v`, and from the
stronger requirement that every minimizing point satisfy `r=0`.

This is the definition used by Lefebvre and Schmidt in their
[December 15, 2025 manuscript](https://optimization-online.org/?p=27046).
Their Theorem 14 establishes finite exact penalties for convex continuous
slices under their compactness and slice Slater assumptions. The paper's
conclusion asks whether polynomial bit
length extends from mixed-integer quadratic objectives with linear
constraints to quadratically constrained problems.

## 2. Balanced finite mixtures characterize the dual

**Proposition 1.** For every `rho >= 0`,

```
D_rho = min sum_i theta_i [f(x_i) + rho ||r(x_i)||]
        subject to theta_i >= 0, sum_i theta_i = 1,
                   sum_i theta_i r(x_i) = 0, x_i in X.
```

There is a minimizing mixture with at most `m+1` points.

**Proof.** Let `K` be the convex hull of the compact set
`{(r(x), f(x)+rho||r(x)||):x in X}`. In a finite dimensional space this
convex hull is compact. Let `w=min{t:(0,t) in K}`. For every multiplier,
averaging its objective over a balanced mixture cancels its linear term,
so `D_rho <= w`.

For `a<w`, strictly separate `(0,a)` from `K`, with the orientation

```
u^T z + beta t > beta a    for every (z,t) in K.
```

Since `(0,w)` belongs to `K`, necessarily `beta>0`. Divide by `beta`.
The multiplier `u/beta` has `L_rho(u/beta)>a`. Taking `a` up to `w`
proves `D_rho=w`. This argument does not assume a maximizing multiplier
exists.

Caratheodory's theorem initially supplies a finite optimal mixture. If it
has more than `m+1` positive weights, the columns `(1,r(x_i))` are linearly
dependent. Perturb the weights in both directions along a nonzero
dependence until a weight vanishes. The objective derivative along the
dependence must be zero: otherwise one of the two sufficiently small
perturbations would improve an optimal mixture. Thus one can remove a
point without changing the objective or balance. Repetition gives the
stated bound. ∎

The penalty in this formula is `sum_i theta_i ||r(x_i)||`. Replacing it
by the norm of the average residual would remove the penalty entirely.

**Corollary 2.** Let `B` consist of balanced mixtures with at most `m+1`
points, and write `c_mu=sum theta_i f(x_i)` and
`s_mu=sum theta_i ||r(x_i)||`. The smallest exact dual penalty is

```
rho_* = max(0, sup_{mu in B, s_mu>0} (v-c_mu)/s_mu).
```

An empty supremum contributes no positive lower bound. An infinite
supremum means no finite penalty is exact. When the displayed number is
finite, exactness holds at the threshold itself.

Indeed, mixtures with `s_mu=0` use only feasible points and already have
`c_mu>=v`. Proposition 1 says exactness is precisely the remaining family
of scalar inequalities `rho s_mu >= v-c_mu`.

This explains why opposing residual witnesses are useful in lower-bound
constructions: their multipliers cancel, even when the multipliers have
arbitrarily large encoding length.

## 3. One dualized equality has an explicit threshold formula

Now let `m=1` and use absolute value. Assume both positive and negative
residuals occur. Define the extended real numbers

```
A_plus  = sup_{r(x)>0} (v-f(x))/r(x),
A_minus = sup_{r(x)<0} (v-f(x))/(-r(x)).
```

Each is a real number or positive infinity; neither is negative infinity.

**Proposition 3.** If both numbers are finite, then

```
rho_* = max(0, (A_plus+A_minus)/2).
```

For a given `rho`, a multiplier attains the exact value if and only if

```
A_plus-rho <= lambda <= rho-A_minus.
```

If either number is infinite, no finite `rho` has `D_rho=v`.

**Proof.** Points with zero residual already satisfy `f>=v`. For positive
residuals, `f+lambda r+rho|r|>=v` for all points is equivalent to
`lambda+rho>=A_plus`. For negative residuals the corresponding condition
is `rho-lambda>=A_minus`. These give the interval and threshold for an
attaining multiplier.

To rule out exactness merely as a supremum when the interval is empty,
fix one positive-residual and one negative-residual point. If
`L_rho(lambda_j)` tends to `v`, evaluating at these two fixed points bounds
`lambda_j` below and above. A subsequence converges. The function
`L_rho` is upper semicontinuous, being an infimum of continuous affine
functions of `lambda`, so the limit attains at least `v`, hence exactly
`v` by weak duality. The interval conditions therefore characterize dual
exactness as well. ∎

For comparison, the threshold at the fixed multiplier zero is
`max(0,A_plus,A_minus)`. Optimizing the multiplier can change the answer.

If residuals occur on only one side of zero, Proposition 1 instead gives
`D_0=v`: every balanced mixture uses only zero-residual points. A finite
maximizing multiplier need not exist. Thus the two-sign hypothesis is
essential for the assertion about multiplier attainment.

## 4. Why feasible-slice regularity is not enough for a bit bound

Consider finitely many integer assignments `z`, with compact nonempty
native sets `X_z`. Assume `f>=L` on their union and `v<=U`. Divide the
assignments into those with `r=0` feasible and those without such points.

Suppose every feasible assignment has an equality multiplier `lambda_z`
satisfying

```
f(x)+lambda_z^T r(x) >= v_z = min_{X_z intersect {r=0}} f,
||lambda_z||_* <= M,                 x in X_z,
```

where `||.||_*` is the dual norm. Suppose every infeasible assignment has
`min_{X_z} ||r|| >= delta > 0`. Then the zero-multiplier penalty is exact
for

```
rho >= max(M, (U-L)/delta).
```

On a feasible assignment, dual-norm Cauchy--Schwarz gives
`f+rho||r|| >= f+lambda_z^T r >= v_z >= v`. On an infeasible assignment,
`f+rho||r|| >= L+rho delta >= U >= v`. A feasible optimizer gives equality.
If there are no infeasible assignments, the second term can be omitted.

This is an elementary sufficient condition that separates two different
quantities. Slice Slater conditions can justify the feasible multipliers;
they do not give a numerical lower bound on the distance of an infeasible
slice to the equality. The quadratic-chain construction makes that latter
distance doubly exponentially small while all input coefficients remain
bounded and the feasible slices have strict quadratic slack.

This observation is explanatory, not an independent novelty claim. The
source theorem already distinguishes feasible and infeasible integer
assignments in its proof. The contribution under investigation is the
explicit bit-complexity obstruction and the associated minimum-penalty
hardness, not that partition of the proof.

## Verification scope

These arguments are mathematical proofs. The independent
[adversarial review](penalty-geometry-review.md) accepted them and their
classical positioning. No general-purpose optimization solver or
project-wide verification was run for this note. The neighboring
construction notes record their own exact computations and targeted formal
checks.

The review also derives a source correction, independently rechecked here:
Lefebvre--Schmidt's Example 13 has one-sided residuals, and consequently
exact dual value for every penalty, although no finite multiplier attains
that value. It therefore demonstrates nonattainment rather than a positive
optimized dual gap under their Definition 1. The correction does not
affect the stated sufficient theorem or the encoding question.
