# Independent review: two pools and two outputs are enough for hardness

Date: 2026-09-05. Reviewer: independent `benders_review` agent.

The reduction in [the investigation draft](pooling-two-pools-two-outputs-investigation.md) is mathematically correct. This approval includes the author's subsequent simplification using only one distinguished upper-quality constraint, rather than enforcing its equality with a duplicate negative quality. The construction proves ordinary NP-hardness with exactly two pools and two outputs, no bypass arcs, arbitrarily many inputs and quality attributes, and flow capacities in `{1,2}`. It also yields one-pool/two-output hardness with exactly one bypass by suppressing the anchor pool.

This is a correctness audit. It does not certify literature novelty, strong NP-hardness, an approximation lower bound, or membership in NP for general pooling.

## 1. The source problem is the required positive-product problem

The primary [Matsui report METR95-13](https://www.keisu.t.u-tokyo.ac.jp/data/1995/METR95-13.pdf) was independently read. Section 3, Theorem 3.1, reduces a binary set-partition feasibility problem to deciding whether a product of two strictly positive affine functions on a bounded rational polytope is at most a specified positive rational threshold. The underlying independent variables are in `[0,1]`; the remaining displayed variables are affine functions of them. The proof explicitly bounds the encoding length of its large coefficients and threshold polynomially. Thus boundedness, positivity, rational input, and exact threshold comparison all match the proposed reduction. This is an NP-hardness source, not a merely local-optimization or approximation statement.

## 2. Normalization and simplex representation are polynomial

An empty source polytope is detectable by rational LP and can be mapped to a fixed no instance. On a nonempty compact rational polytope, the strictly positive affine function `U` has a positive rational minimum `u_min`, computable with polynomial encoding by rational LP. Replacing

\[
U\leftarrow 2U/u_{\min},\qquad V\leftarrow u_{\min}V/2
\]

preserves their product and makes `U≥2`. Their coefficient encodings remain polynomial. Adding `V≤K` cannot remove a yes witness: `UV≤K` and `U≥2` imply `V≤K/2`. It may remove non-witness points, which is allowed. The resulting polytope remains compact and rational, and its emptiness can again be checked by LP.

For the bounded source family in `[0,1]^s`, the mapping `z_i=w_i/s`, with dummy coordinate `z_0=1−Σ_i w_i/s`, is an affine injection into the probability simplex. Adding `z_i≤1/s` and the transformed source inequalities gives an exact description of the same feasible points. Affine functions become homogeneous linear functions of `z` by using `Σ_i z_i=1`. The number of inputs and quality rows and their rational encodings are polynomial.

The use of the simplex does not enumerate vertices of the original polytope. Its generator points generally lie outside the original polytope, and no proof step assumes otherwise.

## 3. Individual source coefficients may have either sign

The constructed source coefficients satisfy

\[
a(z)=\sum_i a_i z_i=U(z)-1\ge1,
\qquad b(z)=\sum_i b_i z_i=K-V(z)\ge0
\]

for `z` in the enforced polytope. These bounds need not hold at individual simplex generators. This causes no defect: the proof first forces every active variable-pool mixture into that polytope and only then uses the bounds on `a(z)` and `b(z)`. Signed inlet costs are allowed in the stated linear-cost model.

For example, let two simplex coordinates have `U` coefficients `(-2,4)`, `V` coefficients `(6,1)`, and `K=5`. Restrict the first coordinate to at most `1/3`. Then `a_i=(-3,3)` and `b_i=(-1,4)` include negative entries, but all allowed mixtures have `a≥1` and `b≥0`. At first-coordinate weight `1/4`, `a=3/2`, `b=11/4`, and the construction achieves profit `55/12`; the product is `45/8>5`, correctly placing this mixture below the profit threshold. Negative generator coefficients do not invalidate either direction.

If nonnegative qualities and bounds are desired, choose a separate common shift for each attribute, large enough to make every source quality and both output bounds nonnegative. Apply it to the anchor as well. Since incoming quality mass and the bound both acquire the same shift times total output flow, all output inequalities are unchanged. A positive rescaling can additionally put every attribute and its bounds in `[0,1]`. These operations have polynomial rational encoding.

There is also a standard nonnegative-cost/revenue representation. Choose rational `B≥0` with `B≥max_i b_i`. Give each variable input cost `B−b_i`, the anchor input cost `B`, and both outputs revenue `B` per unit. Mass conservation makes net profit exactly `Σ_i b_i x_i`. All input costs and output revenues are then nonnegative. This does not change the feasible region or any capacity.

## 4. The extra qualities enforce every polytope row

Take any physical pooling solution with positive variable-pool throughput `T`, and let its input proportions be `z_i=x_i/T`. For a row `A_r z≤d_r`, the variable inputs have quality `A_ri` and the anchor has quality `d_r`. At output 1 the upper-bound condition cancels the anchor contribution and becomes

\[
(A_rz-d_r)y_1\le0.
\]

At output 2, which receives only variable-pool flow, it becomes

\[
(A_rz-d_r)y_2\le0.
\]

At least one of `y_1,y_2` is positive because their sum is `T`. Consequently every row holds for `z`. This includes the normalization-related box inequalities and the safe `V≤K` row. An anchor at the row bound cannot conceal a violated row at a positive-flow output; it merely contributes zero to the row residual.

Rows must be imposed at both outputs. Omitting them at an output could allow the variable pool to avoid enforcing the source polytope by serving that output alone.

## 5. One upper-quality inequality gives the exact maximum

Write `D_1=y_1+h` and `D_2=y_2`. With distinguished variable-pool quality `a(z)`, anchor quality zero, and output-1 upper bound one, feasibility gives

\[
a(z)y_1\le D_1.
\]

For an active variable pool, Section 4 gives `z∈P`, hence `a≥1` and `b≥0`. Because the output capacities are one,

\[
\operatorname{profit}=b(z)(y_1+D_2)
\le b(z)\left(D_1/a(z)+D_2\right)
\le b(z)(1+1/a(z)).
\]

There is no need to force equality in the distinguished-quality constraint. The single upper bound already proves the required upper bound on profit.

Conversely, for any `z∈P`, set

\[
y_1=1/a(z),\quad y_2=1,\quad h=1-1/a(z),
\quad T=1+1/a(z),\quad x_i=Tz_i.
\]

Both outputs have throughput one. Since `a≥1`, the anchor flow is in `[0,1]`, both variable-pool outgoing arcs respect capacity one, variable-pool throughput is at most two, and every variable input and its intake arc carries at most two. The anchor input, intake arc, and pool respect capacity one. All row qualities hold by construction, and the distinguished upper bound is attained. The output-2 distinguished bound is chosen redundant for every possible mixture and imposes no extra condition.

Thus the maximum profit equals

\[
\max_{z\in P}(K-V(z))(1+1/(U(z)-1)).
\]

When the variable pool is inactive, anchor-only flow may be feasible under the single upper bound. Its profit is zero. Since the displayed maximum is nonnegative and the decision target `K` is strictly positive, these inactive points affect neither the identity nor the decision equivalence. Compactness and `a≥1` ensure the displayed maximum is attained.

## 6. Threshold equivalence, counts, and limitations

For every `z∈P`, multiplication by the positive `a=U−1` gives

\[
(K-V)(1+1/(U-1))\ge K
\quad\Longleftrightarrow\quad UV\le K.
\]

The reduction therefore preserves the exact decision answer. There are exactly two pools and two outputs. One pool has one input and one outgoing arc, so eliminating it produces exactly one direct input-to-output arc and leaves one mixing pool. All positive flow capacities are one or two; the growing data are input count, quality count, costs, and rational quality encodings. The designated no instances can retain this topology, have zero profit on all feasible flows, and use a positive target.

Matsui's coefficients may be very large in numerical magnitude, so this proof does not establish strong NP-hardness despite the small flow capacities. It does not contradict fixed-pool/fixed-quality polynomial algorithms because its number of attributes grows. The one-bypass consequence also does not contradict the fixed-pool/fixed-quality result allowing a bounded number of bypass arcs for the same reason.

The initial draft had a duplicate negative distinguished attribute to force equality. That version was also correct. The final single-upper-bound argument is strictly simpler and retains the exact objective identity; the inactive-flow paragraph must use the updated zero-profit argument rather than claiming that anchor-only flow is infeasible.

## 7. Independent numerical cross-check

The author's original-pooling verification script was independently rerun with a different random seed using the project's `minlp-notes` Python environment: `--seed 1 --trials 8`. All 28 original-model solves passed their comparisons with exact rational reference values. This includes shifted-quality and bypass versions. The negative control correctly distinguished the model enforcing source rows at both outputs from the invalid version omitting output-1 rows. The [independent run log](../code/pooling_two_pools_two_outputs/independent_review_output.txt) records the result.

These solver checks support the algebraic reduction and catch formulation mistakes; they are not the proof of NP-hardness. The reference maximum-at-a-vertex argument is valid because, on `a≥1,b≥0`, the sublevel condition `b(1+1/a)≤t` is the convex hypograph `b≤ta/(a+1)` for `t≥0`, so the objective is quasiconvex.

The result has subsequently been promoted to [the result note](../results/pooling-two-pools-two-outputs-hardness.md). The stated undirected-tree topology and attribute normalization to `[0,1]` were also checked and are valid.

## 8. Approximation lemma for the reduced objective

The separate [positive-product subfamily approximation note](pooling-positive-product-subfamily-approximation.md) was independently checked. For `0<ε<1`, let `N=ceil(1/ε)` and solve the `N+1` LPs maximizing `b` over `P∩{a≤1/g}` for `g=k/N`, omitting that bound when `g=0` and skipping empty LPs. For an optimal point, put `t*=1/a*` and choose `g=floor(Nt*)/N`. This LP contains that point and returns `b_g≥b*`, while its point has `1/a_g≥g`. Its true objective is at least `b*(1+g)`, which is at least `OPT−b*/N≥(1−ε)OPT`. All LPs have polynomial rational encoding. Thus the lemma is correct, with `O(1/ε)` LPs and no coefficient-ratio dependence. Its scope is the displayed reduced objective on a rational polytope, not every two-pool/two-output instance; no novelty was asserted for this elementary consequence.
