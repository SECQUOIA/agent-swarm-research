# Independent audit of the proposed P-split Theorem 6 counterexample

Date: 2026-09-04. Reviewer: audit_mccormick, independently of common_factor.
Status: the counterexample passes the stated-assumption and formulation audit.
This identifies a failure of the universal nonexactness statement as written;
it does not question the validity of P-split relaxations or their useful behavior
on other nonlinear disjunctions. No literature priority is claimed.

## Source and scope checked

The local source is Kronqvist, Misener, and Tsay, *P-split formulations: a class
of intermediate formulations between big-M and convex hull for disjunctive
constraints*, DOI [10.1007/s10107-025-02232-1](https://link.springer.com/article/10.1007/s10107-025-02232-1).
The article appeared online in 2025 and is indexed in Mathematical Programming
218 (2026), 57–94. The local artifact is the Springer typeset open copy at
[the German National Library](https://d-nb.info/1373875933/34).
Theorem 6 and Definition 4 are on local PDF page 15, and the proof is on page 16.
The same statement and definition were independently found in the publisher's
current article HTML. This audit therefore concerns the journal article, rather
than an unverified preprint version.

I read the model assumptions, split construction, relevant relaxation-strength
statements, definition, theorem, and full proof in the local extraction. I also
visually checked the original PDF pages 6, 15, and 16, including the retained
box constraint in both formulation (5) and the displayed P-split formulation.
This is a targeted mathematical audit, not a claim to have reviewed the entire
computational study or every theorem in the article.

Definition 4 means pairwise empty intersection of the disjunct sets; it does not
mean disjoint variable scopes. The theorem asserts nonexactness under this
condition, additive bounds, and strictly convex constraint functions
[[kronqvist2026-p-split-formulations-a-class]] p.15-16.

## Assumptions checked individually

Let

```
X=[0,3]×[-1,1],
D_0={x∈X : x_1²+x_2²≤1},
D_3={x∈X : (x_1−3)²+x_2²≤1}.
```

Strictly speaking these sets are disks intersected with the common box; the
common-box intersections are exactly the disjuncts of source formulation (1).

- `X` is nonempty, full-dimensional, compact, and convex.
- Both disjuncts are nonempty, even with nonempty interior in `R²`.
- The two constraint functions are globally strictly convex, with Hessian `2I`.
  Every univariate component is also strictly convex and all components are
  bounded on the relevant box intervals.
- Disjointness holds: `D_0` has `x_1≤1`, and `D_3` has `x_1≥2`.
- Exact bounds are additive because the split components use distinct box
  coordinates. The component ranges are `[0,9]` for either shifted or unshifted
  first-coordinate square and `[0,1]` for the second-coordinate square. The
  complete constraint range is `[0,10]` in either disjunct.
- Minimal auxiliary variables cause no difficulty: the common `x_2²` component
  is represented by one shared auxiliary variable in the full split, as required
  by Assumption 3 and Remark 1.
- There is one constraint per disjunct. Assumption 4's preference for many more
  variables than constraints is explicitly described as technically unnecessary
  on page 4. It cannot exclude this example. An arbitrary-dimensional version
  below also meets that preference as strongly as desired.

These are the relevant assumptions and bound conventions in
[[kronqvist2026-p-split-formulations-a-class]] p.4-6, p.9.

## Exact hull and exact projected relaxation

Both vertices `(0,−1),(0,1)` lie in `D_0`; both vertices `(3,−1),(3,1)` lie in
`D_3`. Therefore

```
conv(D_0∪D_3)=X.
```

Let `R_P` be the continuous P-split relaxation projected onto the original
variables. It is convex, contains the original union, and retains `x∈X`.
Consequently

```
X=conv(D_0∪D_3) ⊆ R_P ⊆ X,
```

so equality holds. The projection terminology matches the source's stated
meaning of relaxation strength and sharpness, not an alternative assertion
about the hull of the extended auxiliary-variable or indicator formulation
[[kronqvist2026-p-split-formulations-a-class]] p.6-7, p.15.

An explicit full-split lift verifies this conclusion without relying solely on
that sandwich argument. Write `t=x_1`, `y=x_2`, and use shared lift coordinates
`a,b,c` for `t²,(t−3)²,y²`. The two vectors

```
q_0=(0,9,1),       q_3=(9,0,1)
```

lie in the bounded linearized disjuncts: `a+c≤1` for `q_0`, and `b+c≤1` for
`q_3`. For any `(t,y)∈X`, set

```
λ_0=1−t/3,        λ_3=t/3,
(a,b,c)=λ_0 q_0+λ_3 q_3=(3t,9−3t,1).
```

The linking inequalities hold because

```
t²≤3t,       (t−3)²≤9−3t,       y²≤1.
```

Thus this point has a valid full-split continuous lift with exactly the shared
auxiliary convention of Assumption 3. Summing the relevant coordinates gives a
valid coarser split as well. No optimization software or tolerance-based
objective comparison is needed.

## Where the proof fails

The proof chooses distinct points from different disjuncts whose joining segment
lies on the hull boundary and asserts strict Jensen inequalities for every
coordinate component. Distinct vectors need not differ in every coordinate.
For example, the endpoints `(0,1),(3,1)` satisfy its boundary-segment premise,
but the second-coordinate component is unchanged. Its midpoint has

```
h_2(1)=1=(h_2(1)+h_2(1))/2,
```

so the claimed strict inequality in that coordinate is false.

Independently, the claimed full feasible neighborhood about a hull-boundary
midpoint does not account for the retained constraint `x∈X`. In this example
all such neighborhoods contain points outside `X`. Slack in other linking
inequalities cannot make those points feasible. Both issues occur in the proof
on [[kronqvist2026-p-split-formulations-a-class]] p.16.

A condition ensuring a usable supporting boundary segment inside the interior
of `X`, together with strict slack in every linking component relevant to an
outward perturbation, might support a narrower nonexactness theorem. This audit
does not claim those conditions are necessary or a complete repair.

## Arbitrarily many variables with one constraint per disjunct

For any integer `n≥2`, take

```
X_n=[0,3]×[-1,1]^(n−1),
g_0(x)=x_1²+(1/(n−1))Σ_{i=2}^n x_i²,
g_3(x)=(x_1−3)²+(1/(n−1))Σ_{i=2}^n x_i²,
D_j={x∈X_n : g_j(x)≤1}.
```

Each function has a positive-definite diagonal Hessian. The disjuncts remain
nonempty, full-dimensional, and disjoint because their first-coordinate ranges
are separated by `[1,2]`. Every box vertex with first coordinate zero lies in
`D_0`, and every box vertex with first coordinate three lies in `D_3`. Hence
`conv(D_0∪D_3)=X_n`, and the identical relaxation sandwich proves exactness for
every allowed split. Box bounds are additive. Common coordinate squares can be
shared. Thus the phenomenon persists with arbitrarily many variables and only
one strictly convex constraint in each of two disjuncts.

## Audit outcome

The proposed two-dimensional counterexample is correct under the article's
stated assumptions. The independent algebraic lift and arbitrary-dimensional
extension reinforce the geometric proof. A targeted search for the DOI with
correction-related wording did not locate a correction; this limited search
does not establish that none exists. The conclusion is confined to the statement
and source version checked here.

## Addendum: local directional repair

I also independently checked the sufficient local criterion in
[common-factor-p-split-correction.md](common-factor-p-split-correction.md),
section 3. For a finite link set, holding the mixed auxiliary vector fixed
preserves every positive-slack link under a sufficiently short continuous step.
The explicit nonincrease condition preserves every zero-slack link. Domain
feasibility and a strictly positive supporting-normal displacement then give a
relaxation point outside the true hull. This argument is correct.

Two clarifications requested in review were incorporated: the link set must be
finite, and the quantitative step must lie within a common radius for domain
feasibility, zero-slack preservation, and the stated Lipschitz bounds. With those
conditions, `ε L_a≤Δ_a` for positive-slack links is sufficient and the supporting
inequality violation is exactly `ε cᵀd`. This is an elementary sufficient repair,
not a claim that the original assumptions imply its additional conditions.
