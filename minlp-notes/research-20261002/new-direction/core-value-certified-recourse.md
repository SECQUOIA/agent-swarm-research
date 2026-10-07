# Fixed-law value output with a certified integer-recourse oracle

Date: 2026-10-02. Status: scoped corollary, passed
[fresh independent review](core-value-certified-recourse-independent-review.md).
Section 4's all-dimensional extension passed a separate actual-file
review recorded in the same report.
This composes the reviewed [core value oracle](core-only-noise-value-oracle.md)
with an existing certified conditional solver. It is not a new algorithm
for TU systems, integer flows, or arbitrary integer programs.

## 1. Concrete mixed-integer interface

Let `v in [0,1]^k`, with `k in {1,2}`, and let the residual domain be
the nonempty finite set

\[
 Y=\{z\in\mathbb Z^m:Az\le b,\quad\ell\le z\le u\},       \tag{1}
\]

where the linear data and finite integer bounds are rational/binary
encoded. Round any rational integer-coordinate bounds inward first.
Importantly, `Y` is fixed independently of `v`. Let `F_0(v,z)`
be an explicit rational polynomial of fixed degree. The base length `I`
includes these data, a rational noise half-width `sigma>0`, a rational
`L>=0`, and verified core-coordinate upper bounds

\[
                   (F_0)_{v_iv_i}\le L\quad
                        \text{on }[0,1]^k\times Y.         \tag{2}
\]

Suppose the residual class has a certified oracle with the following
contract. At every rational `v` and positive rational tolerance `eta`,
it returns `z_v in Y` and rational values

\[
 \ell_v\le\min_{z\in Y}F_0(v,z)
             \le u_v=F_0(v,z_v),\qquad u_v-\ell_v\le\eta,   \tag{3}
\]

with polynomial bit work and certificate verification in the input,
the core-coordinate lengths, and the requested accuracy bits. The
polynomial exponent is uniform over the specified residual class. The
oracle may instead solve the conditional problem exactly. Its correctness
and running time must already be proved for that class; they do not
follow merely because (1) is a rational integer polytope.

As in the main theorem, verification costs for (2) or additional
structural certificates must be polynomial in their encoded lengths
for the stated bound; otherwise add their actual cost separately.
For fixed `v`, a sampled linear core term is a rational constant, so
adding it to both endpoints of (3) preserves the oracle contract.

**Corollary.** Choose independent linear core noise on one finite
rational grid in `[-sigma,sigma]`, with its size fixed from base data
and logarithm polynomial in `I`. For every sample, the global optimal
value of

\[
                \min_{v\in[0,1]^k,\ z\in Y}
                              F_0(v,z)+\gamma^Tv           \tag{4}
\]

has a Cauchy evaluator. At accuracy `2^{-q}`, it returns a rational core
point, a feasible integer residual vector, and a rational global value
interval of width at most `2^{-q}`, with its upper endpoint attained by
that feasible pair. Its expected work and proof-record size are

\[
                     (1+L/\sigma)\operatorname{poly}(I+q).
                                                               \tag{5}
\]

The same sample is used at every precision. Correctness holds on every
draw; the expectation concerns cost. No stable optimal residual label,
label gap, unique residual optimum, or coordinate-distance approximation
is promised or needed.

## 2. Why the inherited proof applies

First, rounding the core holds the chosen residual vector fixed. Because
`Y` does not change with the core, that vector remains feasible at every
corner. Equation (2) therefore gives exactly the corrected-corner lower
bound and feasible upper bound used by the main proof. Its generated-cell
count, per-level cap, and near-linear bookkeeping are unchanged.

Second, the projected growth formula is still

\[
 \exists(a,z_0)\ \forall(v,z):\quad
 F_\gamma(v,z)-F_\gamma(a,z_0)\ge t\|v-a\|^2,              \tag{6}
\]

with membership in `[0,1]^k x Y` explicitly included. For the finite
section bound, integer membership can be expanded as disjunctions of
allowed labels and intersected with `Az<=b`. If `N_i=u_i-l_i+1`, then
`sum_i N_i` and `prod_i N_i` are at most `2^{poly(I)}`. All labels have
polynomial binary length. Thus this is a two-block formula with
exponential-in-polynomial base format and scalar-section complexity
`C_0=2^{poly(I)}` independent of noise heights and the threshold. The
continuous core value is the minimum of finitely many continuous
polynomials. The same proximal growth tail and finite-law transfer
therefore apply, including ties.

Third, there is an elementary same-draw fallback with the required
base-only exponential factor. Enumerate the integer bounding box,
discard labels violating (1), and for each remaining label solve the
fixed-dimensional polynomial core problem exactly. Dimension `k<=2`
and degree are fixed, so standard real-algebraic optimization has
polynomial coefficient-height cost for each label. Exact comparisons
select a globally optimal label and core value. Alternatively, the
two-block fallback construction in the main theorem applies directly.
The number of labels enters only a base factor
`B_0=2^{poly(I)}`; added noise bits and requested evaluation bits enter
polynomially. After selection, rationally approximating and clipping the
core coordinates preserves feasibility of the same integer label and
gives a feasible value approximation with certified global lower bound.

These are precisely the three interfaces used by the cap-and-moment
proof. Its one choice `M>=C_0B`, with `B>=B_0`, works for every `q`.
The `L=0` branch again needs only the `2^k` core vertices and the
conditional oracle. No new probabilistic or combinatorial optimization
argument is required.

## 3. Use and limits

A structured integer recourse problem, such as a flow problem with an
already verified polynomial-time conditional optimizer and certificate,
can instantiate (3). This statement grants no oracle to general integer
linear optimization, and TU structure alone does not establish the
required oracle for an arbitrary nonlinear objective.

The result is useful even when the optimal integer labels tie or change
arbitrarily close to the optimal core: the returned label need only
support the certified requested objective gap. It is weaker than an
exact-label theorem but requires no certificate identifying a stable
optimal label. This distinction matters when comparing with the
separate [integer-flow completion theorem](smoothed-interior-core-flow.md).

For a broader fixed residual domain the same composition requires all
three interfaces explicitly: certified conditional value and feasible
output, the uniform finite-format projected growth tail, and a base-only
exact fallback. Compactness by itself does not supply them. In
particular, a residual domain `Y(v)` depending on the core would need
a new feasible-rounding or recourse-semiconcavity certificate; the present
argument does not cover it.

## 4. All core dimensions via the reviewed all-scale count

The reviewed [all-scale theorem](all-scale-core-value-oracle.md) removes
the restriction `k<=2` from this oracle composition. Keep the same fixed
integer domain (1), verified curvature (2), and polynomial-time certified
conditional oracle (3), but allow arbitrary `k>=1`. There is one finite
core-noise law with polynomial base bit length giving the same every-draw
value interval and feasible mixed point, with expected work and
proof/output size

```
f_d(k) (1+L/sigma)^k poly_d(I+q).                         (7)
```

The polynomial exponent is independent of the core and residual
dimensions. The sharper `(1+L/sigma) poly_d(I+q)` bound in (5) remains
available when `k<=2`. As before, this is a certified-oracle composition,
not a new conditional integer optimizer or an exact-label theorem.

The all-scale geometric proof applies to
`f(v)=min_{z in Y} F_0(v,z)`, which is continuous on the compact core box.
Its corrected-corner witnesses remain valid because `Y` is fixed.
The conjugacy, padded near-optimal hull, maximum-simplex volume estimate,
and covering argument require no residual convexity or residual topology.
They give the same weak first-moment tail for the all-scale count proxy.

For the finite-law transfer, use the actual two-block formula from
Section 5 of the all-scale theorem. It existentially chooses the
`(k+1)^2` near-optimal core points and their residual witnesses. Append
membership in (1) for each such witness. The shared universal competitor
is guarded by its own membership in `[0,1]^k x Y`. Expanding integer
membership into allowed-label disjunctions multiplies a base
`2^{poly(I)}` format size by only polynomially many witness copies.
The total number of variables is polynomial in `I`; the logarithm of
the atom count is polynomial in `I`; there are still two quantified
blocks. The reviewed quadratic QR and product-chain encoding of the
simplex determinant is unchanged. Fixed-block elimination therefore
gives a scalar-section bound `2^{poly_d(I)}`, independent of the
threshold, sampled heights, and requested accuracy. No conditional
independence of the residual witnesses is asserted or needed.

There is also an all-dimensional fallback with the required base budget.
Enumerate the residual bounding box and test its linear inequalities as
in Section 2. For each feasible integer label, invoke the reviewed
[generic polynomial-box fallback](polynomial-exact-fallback.md) on its
`k` continuous core variables. Unlike the fixed-dimensional argument in
Section 2, this invocation can cost `2^{poly_d(I)}` per label. Its
coefficient-height and evaluation-precision exponents are nevertheless
fixed, independent of `k`. The number of labels, all per-label base
budgets, and polynomial-time univariate comparisons of candidate values
can all be absorbed into one `B_0=2^{poly_d(I)}`. In particular, exact
comparisons of two candidate value representations have a base-only
degree factor and polynomial dependence on their coefficient heights;
no common field containing every candidate is constructed.

After choosing the best label, rational core approximation and clipping
give a feasible mixed point and a certified global value interval, as
before. The resulting fallback still costs
`B_0 poly_d(I+b+q)` with its exponential factor independent of noise
height and query precision. These two format checks are the only new
interfaces required by the all-scale cap proof. Its one law and one
random work factor then establish (7) simultaneously for all `q`.
For `L=0`, the `2^k` endpoint queries give the claimed parameterized
deterministic bound directly.

## Verification status

This is an interface substitution into the reviewed main proof. The
new checks concern fixed-domain feasibility, the integer membership
formula, and the coefficient-height cost of fallback. The fresh
actual-file review passed those interfaces, exact candidate comparisons,
and rational core repair. It also checked local links, mathematical
delimiters, and whitespace; no new mathematical fixtures were needed.
The separate actual-file review of Section 4 also passed its
all-dimensional integer-witness formula and fallback height bounds.
No index edits, project-wide tests, or CI checks were made.
