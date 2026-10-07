# A finite certificate counterexample to unrestricted tree localization

Date: 2026-10-02. Status: complete argument with an
[independent adversarial review](../reviews/tree-localization-adversary.md).

This note addresses property `(Loc_T)` in Remark 3.3 of
[`adaptive-matching.md`](../../research-20260929/theory-decomposition/adaptive-matching.md),
using the certificate and configuration model of Definition 1.2 and Lemma
1.5 in
[`decomposition-certificates.md`](../../research-20260929/theory-decomposition/decomposition-certificates.md).
It does not address only a generic objective perturbation: Section 5 realizes
the perturbation as actual finite dyadic certificate partitions, with the
standard convex envelope of a concave quadratic as the only inexact factor
relaxation.

## 1. Conclusion and scope

**Theorem.** There is a family with fixed `k = 3`, `w = 1`, `Delta = 2`,
`M_a = 3`, `alpha' A = 1/2`, and fixed positive quadratic-growth constant
`c_g`, satisfying `(QG)`, `(L^{1,1})`, `(U^q)` and `(S)`, with this property:
for every finite `K`, some member has finite dyadic leaf and separator
partitions and exact slopes `lambda = lambda(x*) = 0` such that

- every leaf and cell has width at most `W`;
- every minimizing configuration has a root copy farther than `K W` from
  the true minimizer `x* = 0`.

Thus the size-independent property `(Loc_T)` is false for the unrestricted
class of bounded-branching, uniformly conditioned problems. This failure
occurs at `theta = 0` and zero slope error, so neither a smaller positive
grading threshold nor the fixed-point condition on slope errors repairs it.

Conjecture 7 explicitly leaves room for an additional relation between
branching and conditioning. The theorem rules out its unconditional reading;
it does not rule out such a restricted version. It also does not show that
GR itself reaches these partitions, or rule out a different adaptive
algorithm with the desired certificate count. The construction uses a
large refinement difference between different bags; `(Loc_T)` explicitly
quantifies over such certificates.

## 2. Uniformly conditioned quadratic and bounded-width decomposition

Fix `a = 7/20` (the argument works for every
`1/3 < a < 1/(2 sqrt(2))`). Let `B_d` be the complete binary graph tree of
depth `d >= 1`, with `n = 2^(d+1)-1` vertices, adjacency matrix `A_d`, root
`o`, and graph-leaf set `L`. Put

```
H = I - a A_d,
delta_0 = 1 - 2 sqrt(2) a > 0,
F(x,y) = (1/2) x^T H x + (1/2) sum_{v in L} y_v^2,
X0 = [-1,1]^(n + |L|).
```

The adjacency norm is at most `2 sqrt(2)`. One elementary proof applies
`2 |u v| <= u^2/sqrt(2) + sqrt(2) v^2` on each directed parent-child edge
and counts the at most two children and one parent of each vertex. Hence

```
delta_0 I <= H <= (1 + 2 sqrt(2) a) I.
```

Consequently `(QG)` holds with the same
`c_g = delta_0/2` in every dimension, the unique minimizer is `(0,0)`, and
`(S)` holds. The Hessian condition number is uniformly bounded by
`(1+2 sqrt(2)a)/delta_0`.

Use a root bag `{x_o}`; for every nonroot graph vertex `v`, use a bag
`{x_parent(v), x_v}` attached to its parent's bag. At each graph leaf `v`,
attach a final bag `{x_v,y_v}`. No bag is contained in its parent.
Every separator has one coordinate. Internal graph variables occur in
their own bag and their two children's bags; graph-leaf variables occur in
their own bag and their final bag. Thus `k=3`, `w=1`, and `Delta=2`.

## 3. Factorization and legitimate per-factor relaxations

Let

```
s = sqrt(1 - 8 a^2),
lambda_plus = (1+s)/2.
```

Eliminate `H + diag(1_L)` from the graph leaves upward. Define

```
p_v = 2                                      (graph leaves),
p_v = 1 - sum_{u child of v} a^2/p_u          (other vertices).
```

All `p_v` lie in `[lambda_plus,2]`: the interval is preserved by
`p -> 1 - 2a^2/p`, whose value at `lambda_plus` is `lambda_plus`.
The exact factorization is

```
F(x,y) = (p_o/2) x_o^2
       + sum_{v != o} (p_v/2) (x_v - (a/p_v)x_parent(v))^2
       + sum_{v in L} [-(1/2)x_v^2 + (1/2)y_v^2].
```

Assign the root unary factor to the root bag, each convex square to its
edge bag, and the two final unary factors to the corresponding final bag.
Keep every convex factor exact. Relax `f(z)=-z^2/2` on `[l,u]` by its
chord,

```
f_[l,u](z) = -z^2/2 - (1/2)(z-l)(u-z).
```

This is its exact convex envelope and the minimal-parameter alphaBB
relaxation. It satisfies `(U^q)` with equality and `alpha'=1/2`.
Only one unary factor per final bag is relaxed, so `A=1`.

The edge-bag Hessian has norm `p_v+a^2/p_v < 3`; the root Hessian norm is
at most 2, and the final-bag Hessian is `diag(-1,1)`. Thus the common
choice `M_a=3` is valid. All factors have zero gradient at 0, and therefore
all exact subtree slopes at the true minimizer are zero.

## 4. An auxiliary objective with a unique amplified global minimizer

For a dyadic number `0 < W <= 1`, define the continuous function

```
h_W(z) = z(W-z)       if 0 <= z <= W,
         0            otherwise,
G_W(x,y) = F(x,y) - (1/2) sum_{v in L} h_W(x_v).
```

First minimize over unrestricted interior graph variables, holding the
leaf vector `z` fixed. Write `I` for the interior graph vertices and

```
B = -H_II^(-1) H_IL,
S = H_LL - H_LI H_II^(-1) H_IL.
```

Then

```
G_W(x,y) = (1/2)(x_I-Bz)^T H_II (x_I-Bz)
         + (1/2)z^T S z - (1/2)sum h_W(z_v)
         + (1/2)||y||_2^2.
```

`S` has nonpositive off-diagonal entries, because `H_II^(-1)` is
entrywise nonnegative (its convergent Neumann series has nonnegative
terms). By tree symmetry its row sums are equal. Write that row sum as
`q_d`. Direct solution of the radial recurrence gives

```
r_plus  = (1+s)/(4a),
r_minus = (1-s)/(4a),
gamma = r_minus/r_plus,
q_d = lambda_plus (1-gamma^(d+2))/(1-gamma^(d+1)).
```

Thus `lambda_plus < q_d <= 1`. With `b_ij=-S_ij >= 0` for distinct
leaves, the reduced objective equals

```
sum_i psi(z_i) + (1/2)sum_{i<j} b_ij (z_i-z_j)^2,
psi(z) = (q_d/2)z^2 - (1/2)h_W(z).
```

The unique scalar minimizer is

```
t_d = W/[2(q_d+1)].
```

Indeed, inside `[0,W]`,
`psi(z)-psi(t_d) = (q_d+1)(z-t_d)^2/2`. Outside that interval,

```
psi(z)-psi(t_d) - (q_d/4)(z-t_d)^2
    = (q_d/4)(z+t_d)^2 + t_d^2/2 >= 0.
```

It follows that the unique global minimizer of the unrestricted auxiliary
objective has every leaf equal to `t_d`, every dummy variable zero, and
interior coordinates equal to their harmonic extension. Its value at level
`j`, including the root at `j=0`, is

```
xbar_j = t_d (r_plus^(j+1)-r_minus^(j+1))
                 /(r_plus^(d+1)-r_minus^(d+1)).
```

The root equation is `xbar_0=2a xbar_1`, the internal equation is
`xbar_j=a xbar_(j-1)+2a xbar_(j+1)`, and the leaf value is `t_d`, which
verify the formula. Since `a>1/3`, `r_plus<1`; consequently

```
xbar_0/W = (1-gamma) r_plus^(-d)
            /[2(q_d+1)(1-gamma^(d+1))] -> infinity.
```

For each fixed depth choose `W` dyadic and small enough that every
`xbar_j` is strictly inside `[-1/2,1/2]`. This scaling does not change the
ratio `xbar_0/W`. The unrestricted minimizer then belongs to `X0` and is
also the unique minimizer of `G_W` on `X0`.

We will use an explicit uniform growth bound. Set

```
b0 = 2 sqrt(2) a / delta_0,
C_Q = 4/delta_0 + 4(2 b0^2+1)/lambda_plus.
```

The scalar inequality above, `H_II >= delta_0 I`, and `||B||_2 <= b0`
give, with `E = G_W(x,y)-G_W(xbar,0)`,

```
E >= (delta_0/2)||x_I-Bz||_2^2
       + (q_d/4)||z-t_d 1||_2^2 + (1/2)||y||_2^2,
||(x,y)-(xbar,0)||_2^2 <= C_Q E.
```

For the second inequality use
`||x_I-xbar_I||^2 <= 2||x_I-Bz||^2 + 2b0^2||z-t_d1||^2`
and add the leaf and dummy terms. Here `C_Q>=2`, so it also covers the
dummy variables.

## 5. Finite dyadic certificates realizing the auxiliary objective

Choose a dyadic mesh `0 < h <= W`, with `h` dividing `W`.

1. Partition every original root or edge bag uniformly into cubes of
   width `h`.
2. Partition every separator uniformly into intervals of width `h`.
3. In each final bag `{x_v,y_v}`, use width-`W` squares on the slab
   `[0,W] x [-1,1]` and width-`h` squares on the remaining two slabs.

These are finite dyadic cube partitions of the full bag domains. The
mixed partition in step 3 can also be obtained by recursive dyadic splits:
first reach width `W`, then further refine all cubes outside the indicated
slab. Every leaf and cell has width at most `W`, so `(W_theta)` holds
with `theta=0`, for the entire partition.

Use slopes zero, the prescribed affine child bounds, and maximal
intercepts from Lemma 1.5. This is a valid finite certificate, and its root
bound is the minimum configuration value `Phi`.

For any configuration, form a consistent point by taking each graph
variable from its own original bag and each dummy variable from its final
bag. The parent copy in an original edge bag differs from that consistent
coordinate by at most `2h`: its separator cell has width `h` and meets
the parent bag's width-`h` interval. The copied graph leaf in a final bag
also differs by at most `2h`. Each graph variable's top bag is its own
original bag, so there is no longer chain to consider here.

For a convex edge factor, this copy change alters its value by at most
`12h`, using its gradient Lipschitz constant at most 3 on `[-1,1]^2` and
its zero gradient at zero. For the final bag define

```
phi_W(z) = -z^2/2 - h_W(z)/2.
```

This function is 1-Lipschitz on `[-1,1]`: its derivative is `-z` outside
the special interval and `-W/2` inside it. On a coarse final-bag square
the relaxed unary factor is exactly `phi_W(z)`; on a fine square it is
`phi_W(z)-e` with `0 <= e <= h^2/8`. Thus its discrepancy from evaluation
at the consistent coordinate is at most `2h+h^2/8`. The dummy factor and
root factor use their consistent coordinates exactly. Summing, for
`h<=1`,

```
|Phi(c) - G_W(x(c),y(c))| <= 15 n h.                 (5.1)
```

The bound is deliberately loose. It is uniform over all configurations,
including configurations using boxes that only touch. The construction
therefore uses Definition 1.2 as stated, without the optional omission of
touching pairs.

There is also a consistent configuration at `(xbar,0)`. Each graph leaf
lies strictly in `[0,W]`, so choose its coarse final-bag square; choose
the remaining boxes and cells to contain the common coordinates. At this
configuration all convex factors are exact and each leaf factor has
exactly the auxiliary well error. Hence

```
min_c Phi(c) <= G_W(xbar,0).
```

For every minimizing configuration `c`, (5.1) and the growth bound give

```
||(x(c),y(c))-(xbar,0)||_2^2 <= 15 C_Q n h.
```

Choose `h` dyadic, dividing `W`, so small that

```
15 C_Q n h < xbar_0^2/4.
```

Then every minimizing configuration has its root coordinate greater than
`xbar_0/2`. Given any proposed finite localization constant `K`, first
choose depth `d` with `xbar_0/W>2K`, then choose `W` to fit the domain,
and finally choose `h` as above. Every minimizing configuration violates
`rho_root <= K W`.

All constants in `(Loc_T)` remain fixed throughout. The exact slopes meet
every slope-error bound, including the bound that depends on the proposed
`K_T`. Since `theta=0` meets every positive proposed `theta_T`, this proves
the theorem.

## 6. What this does and does not establish

The obstruction is already present at width one, fixed bag multiplicity,
fixed branching, and fixed spectral conditioning. Exponential growth in
the number of boundary leaves outweighs decay of the influence of one
leaf. Per-factor, vertex-vanishing relaxation error does not prevent this
when the partition is permitted to concentrate its width-`W` errors near
one side of every graph leaf.

The true objective is strongly convex, but its chosen factorization
includes a concave unary factor at each graph leaf. This is part of the
certificate model: the conjecture fixes assumptions on assigned bag
functions and per-factor models, and does not require all factors to be
convex. Keeping globally convex factors exact would of course remove this
particular relaxation mechanism.

The counterexample does not prove a size lower bound for certificates,
does not refute the known centered certificate upper bound, and does not
prove poor complexity of GR on its own reachable partitions. It identifies
a false sufficient localization statement. A positive extension needs an
additional assumption, such as a suitable influence contraction, or a
weaker localization property tailored to the actual algorithm's partitions.

## 7. Targeted verification

See `check_counterexample.py` and its output `check_counterexample.json`.
The script checks the exact factorization, bounded bag Hessians, Schur
row sums and signs, the harmonic formula, auxiliary minimizers and growth,
and the divergence of the localization ratio with fixed coefficients.
These are floating-point checks supporting the proof, not replacements
for it. The targeted command actually run was:

```
python research-20261002/tree-localization/check_counterexample.py
```

Result: passed on all seven explicit trees of depths 1 through 7, with
50 random global-growth checks per tree and scalar-growth checks on
10,001 points per depth. The closed-form root ratios are approximately
2.0846 at depth 16, 54.3039 at depth 32, 37,378.64 at depth 64, and
58,234,046.95 at depth 100. The script does not enumerate finite
certificate dynamic programs. No project-wide verification or CI checks
were used.
