# Reciprocal-anchor hulls and a joint separating inequality

Date: 2026-09-04.

Status: proved and independently reviewed; novelty is unchecked. The common-factor author independently checked the one-leaf proof and PSD congruence. The root reviewer independently checked the exact hull, the disjoint-support witness, the tangent-deficit coefficients, and all four strict rational lower bounds on 2026-09-04. These results concern box-bounded leaves without additional product bounds or linking constraints. Such extra restrictions require further convexification.

The exact one-leaf hull is closely related to standard disjunctive and perspective formulations; it should not be called a new general convexification method. The purpose of this note is to preserve the exact small-block formulation, a precise obstruction with two leaves, and a cut that resolves that obstruction. See the [algorithm investigation](../notes/common-factor-investigation.md) and [independent audit](../notes/review-common-factor.md) for context.

The [one-leaf Lean package](../formal/topics/05-reciprocal-anchor/README.md) verifies the actual graph hull, its PSD and two-SOC descriptions, the zero-mass and fixed-anchor cases, both individual witnesses, and joint nonmembership using the separating inequality with correction `1/400`. Its [coverage record](../formal/topics/05-reciprocal-anchor/COVERAGE.md) distinguishes these results from the unformalized congruence to the earlier moment-cut matrix and the four displayed radical calculations. The later [many-leaf package](../formal/topics/13-many-leaf-reciprocal/COVERAGE.md) also verifies affine leaf-box normalization and the equality-support argument used below. These proofs do not establish novelty or verify the separate numerical scripts.

## 1. Exact hull for an anchor and one unrestricted bounded leaf

Normalize the leaf to `Y in [0,1]`; any nondegenerate box `[l,u]` reduces to this by an affine change. Define

```
K = conv{(X,1/X,Y,XY): a<=X<=b, 0<=Y<=1},  0<a<b.
```

Write its coordinates as `(m,t,q,w)`. Then `K` is exactly the following set:

```
0 <= q <= 1,
a q <= w <= b q,
a(1-q) <= m-w <= b(1-q),
t <= (a+b-m)/(ab),

[ w,   0,    q   ]
[ 0,   m-w,  1-q ] >=PSD 0.                         (A)
[ q,   1-q,  t   ]
```

The linear inequalities are precisely the leaf's McCormick inequalities. The PSD condition is equivalent to the original reciprocal-anchor cut by an invertible congruence: starting with rows and columns ordered as `(sqrt(X),1/sqrt(X),sqrt(X)(2Y-1))`, replace the first and third functions by their half-sum and half-difference, and reorder. The diagonal entries become `w` and `m-w`, their cross entry becomes zero, and the reciprocal cross entries become `q` and `1-q`.

For positive denominators, (A) says

```
t >= q^2/w + (1-q)^2/(m-w).                         (B)
```

At zero denominators use the closed perspective convention: `0^2/0=0`; a nonzero numerator divided by zero is infeasible. The displayed PSD matrix incorporates these cases directly.

**Proof of sufficiency.** For any mass `rho>=0` and first moment `v` satisfying `a rho<=v<=b rho`, the possible inverse moments of a positive measure on `[a,b]` with that mass and first moment form exactly the interval

```
[rho^2/v, ((a+b)rho-v)/(ab)].                        (C)
```

For positive mass, Jensen gives the lower endpoint, attained by a point mass at `v/rho`. The reciprocal secant gives the upper endpoint, attained by the two endpoint masses with mean `v/rho`. Convex mixtures of these two measures retain mass and first moment and attain every intermediate inverse moment. Zero mass contributes zero moments.

Apply (C) to a first measure with mass `q` and first moment `w`, and a second measure with mass `1-q` and first moment `m-w`. The sum of their lower inverse-moment endpoints is the right side of (B); the sum of their upper endpoints is `(a+b-m)/(ab)`. Thus (A) and the secant inequality guarantee inverse moments for the two measures that sum to `t`. Set `Y=1` on the first measure and `Y=0` on the second. Their union is a probability measure representing `(m,t,q,w)`. Necessity follows from the original PSD proof and McCormick/secant validity. This proves equality. The case `a=b` is immediate and linear. ∎

An equivalent lifted SOCP formulation introduces `tau_1,tau_0>=0` with

```
q^2 <= w tau_1,
(1-q)^2 <= (m-w) tau_0,
tau_1+tau_0 <= t,
```

and retains the displayed linear inequalities. This formulation has two rotated SOC constraints. The construction is closely related to convexifying a union of the two leaf-endpoint reciprocal graphs, so standard disjunctive or perspective formulations are a likely source of prior overlap.

## 2. Individual anchor-leaf hulls fail with two leaves

Take `a=1`, `b=3`, `m=2`, and `t=3/5`, with two leaves in `[0,1]`. The following two leaf moment pairs each satisfy the exact one-leaf hull above:

```
(q_1,w_1) = (2/3, 5/3),
(q_2,w_2) = (14/29, 40/29).
```

The first pair is represented by `X=1` with probability `1/3` and `X=5/2` with probability `2/3`, with its leaf equal to one exactly at the upper point. The second pair is represented by `X=6/5` with probability `15/29` and `X=20/7` with probability `14/29`, with its leaf equal to one exactly at the upper point. Both give `E[X]=2`, `E[1/X]=3/5`.

Yet no common distribution represents both leaves. For any representing distribution and any `Y in [0,1]`, weighted Cauchy--Schwarz gives

```
E[Y/X] >= (E[Y])^2 / E[XY],
E[(1-Y)/X] >= (E[1-Y])^2 / E[X(1-Y)].
```

For both displayed leaf pairs the sum of these lower bounds is exactly `3/5`, so both inequalities must be equalities. Equality forces `X=w/q` wherever `Y>0` and `X=(m-w)/(1-q)` wherever `1-Y>0`. Consequently the first leaf forces all mass onto `{1,5/2}`, and the second forces all mass onto `{6/5,20/7}`. These supports are disjoint, which is impossible.

All rational identities in this example were checked with exact symbolic arithmetic. This is a strict obstruction to intersecting even the exact individual anchor-leaf hulls, rather than merely a weakness of the moment cut. It also identifies why further coupling information is needed: the individually permitted distributions of the common factor may disagree.

### An explicit rational separating inequality

The incompatible point can be excluded by a linear cut that is valid for the true two-leaf hull. Define

```
g_1 = 2 - m - (6/5)q_1 + (21/25)w_1,
g_2 = 5/3 - (25/36)m - (29/30)q_2 + (2059/3600)w_2.
```

Then the strengthened inequality

```
2t >= g_1 + g_2 + 1/400                              (D)
```

is valid for `1<=X<=3`, `Y_1,Y_2 in [0,1]`. At the incompatible point, `g_1=g_2=t=3/5`, so (D) cuts it off by `1/400`.

To verify validity, choose the reference levels `(L_1,H_1)=(1,5/2)` and `(L_2,H_2)=(6/5,20/7)`. At any original point, the individual tangent deficit is

```
1/X - g_j(X,Y_j,XY_j)
 = (1-Y_j)(X-L_j)^2/(X L_j^2)
   + Y_j(X-H_j)^2/(X H_j^2).
```

The sum of the two deficits is a convex combination of the four functions

```
2/X + (1/A^2+1/B^2)X - 2/A - 2/B,
       A in {1,5/2}, B in {6/5,20/7}.
```

Each such function is bounded below on all positive `X` by `2 sqrt(2(1/A^2+1/B^2))-2/A-2/B`. The four resulting lower bounds are

```
(sqrt(122)-11)/3,
(sqrt(898)-27)/10,
(sqrt(1538)-37)/15,
(sqrt(226)-15)/10.
```

Each exceeds `1/400`, as direct squaring of positive rational quantities verifies. This proves (D) pointwise and hence for every convex combination. The inequality illustrates a useful strengthening principle: tangent inequalities whose equality supports are incompatible admit a strictly positive common-deficit correction. Its general novelty has not been assessed.
