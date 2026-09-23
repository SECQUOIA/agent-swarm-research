# Novelty audit: one pool with fixed qualities and unrestricted bypasses

Date: 2026-09-05. Status: bounded literature audit; no new hardness theorem or proof validation is asserted here. The [investigation](pooling-single-quality-bypass-investigation.md) is developing a direct-flow encoding with shared source capacities. The precise proposed variant permits lower flow bounds, fixed source contracts, fixed output demands, and exact output qualities.

The main finding is a distinction between **an existing hardness claim** and **an independently verified reduction**. Baltean-Lugojan and Misener already claim that restoring feed availability or pool capacity makes their one-pool, one-quality, bypass-containing class NP-hard. The inspected argument does not establish that precise assertion by a reduction. A correct new reduction could therefore fill a proof and model-specific classification gap, but should not be advertised as the first claim of this hardness boundary.

## Exact model boundaries in the sources

### Haugland and Boland–Kalinowski–Rigterink

Haugland's final paper excludes direct source-terminal arcs and replaces each by a new pool. It also explicitly counts a quality with both upper and lower bounds twice in its upper-bound-only convention. These transformations preserve unrestricted pooling but change the parameters relevant here. [[haugland2016-the-computational-complexity-of-the]] p.4

Its single-pool theorem solves the problem through the smaller of `(terminals+1)^qualities` and `2^terminals` compact LP families. It consequently gives polynomial time for fixed qualities or fixed terminal count **in that no-direct-arc model**. Its concluding bounded-pool questions concern that same model. [[haugland2016-the-computational-complexity-of-the]] p.7, p.16

[Boland, Kalinowski, and Rigterink, *A polynomially solvable case of the pooling problem*](https://optimization-online.org/wp-content/uploads/2015/08/5059.pdf), inspected 2015 preprint, PDF p.2, explicitly makes the same exclusion and subdivision convention. Section 3 proves the fixed-input, single-pool result; Table 2 summarizes no-bypass cases. This does not settle a single original pool with an unbounded number of direct arcs. Nor should the table be used without its model assumptions to contradict a bypass hardness result.

The earlier MAGO 2014 two-pool/one-quality claim is not a reliable substitute: the [existing source-discrepancy audit](pooling-fixed-pools-qualities-source-audit.md) checks its mismatch with the final Haugland paper.

### Baltean-Lugojan and Misener

[*Piecewise parametric structure in the pooling problem: from sparse strongly-polynomial solutions to NP-hardness*](https://doi.org/10.1007/s10898-017-0577-y) is the closest prior claim. Its general model includes bypass flows, feed availability intervals, output demand intervals, and upper/lower quality specifications. Figure 1 explains that a feed may supply both a pool and outputs. [[lugojan2018-piecewise-parametric-structure-in-the]] p.3-4

Assumption 2.2 drops feed and pool capacities, fixes positive output demands, and uses one quality. Under those restrictions, Theorem 4.4/Corollary 4.5 give the single-pool/multiple-output algorithm. Remark 4.6 claims NP-hardness when capacities are restored, qualities added, or demands made variable. Its capacity argument invokes a bivariate rational polynomial and cites Garey–Johnson; the other bullets similarly invoke polynomial systems. No explicit reduction, admissible-system encoding, or relevant coefficient/degree complexity bound is supplied there. Therefore record these as the authors' assertions, not independently established classifications. [[lugojan2018-piecewise-parametric-structure-in-the]] p.5, p.22-24

Our assessment: obtaining a nonlinear polynomial system is insufficient to prove hardness of this pooling subclass. A reduction must show that a known hard family embeds into precisely the obtainable systems with polynomial input growth.

## Related nonlinear optimization: useful distinctions

[Matsui, *NP-hardness of Linear Multiplicative Programming and Related Problems*](https://www.keisu.t.u-tokyo.ac.jp/data/1995/METR95-13.pdf), inspected METR95-13 preprint, Theorem 3.1/PDF p.7, proves NP-hardness of minimizing a product of two positive variables over linear constraints. The proof uses growing-dimensional auxiliary polytopes and explicitly bounds binary encoding length. This supplies an established source problem; representing its polytope through direct blending and capacity constraints remains a separate task. It also shows why two scalar nonlinear coordinates alone do not ensure tractability when unrestricted linear coupling is allowed. Do not infer strong NP-hardness from this reduction's polynomial bit length: its numerical coefficients grow rapidly.

[Yajima and Konno, *Outer Approximation Algorithms for Lower Rank Bilinear Programming Problems*](https://orsj.org/wp-content/or-archives50/pdf/e_mag/Vol.38_02_230.pdf), *JORSJ* 38(2), 230–239 (1995), studies low-rank bilinear objectives on products of polytopes. Section 2 reduces to a fixed-dimensional projected outcome space; the paper offers practical approximate and finitely convergent exact algorithms. Its introduction distinguishes empirical efficiency and average-polynomial parametric behavior from general complexity. It does not provide a worst-case polynomial theorem that resolves the present pooling target.

[Punnen, Sripratak, and Karapetyan, *The bipartite unconstrained 0–1 quadratic programming problem: Polynomially solvable cases*](https://doi.org/10.1016/j.dam.2015.04.004), Section 2.2, gives polynomial algorithms for fixed-rank bilinear objectives on independent boxes. Its theorem relies on that box structure. Shared source capacities and bypass-output constraints produce a different feasible set, and pooling also has bilinear constraints. Thus neither fixed objective rank nor that result gives an immediate pooling classification.

A precise comparison must distinguish the number of qualities, the number of nonlinear variables, the rank of one objective matrix, the ranks of all constraint matrices, and the structure of the linear feasible region. These are different parameters. In particular, a small number of quality variables may multiply an unbounded number of output flows in separate constraints.

## What a successful direct-flow encoding would contribute

The author is investigating a means to copy bounded continuous variables between different source-quality labels using only direct-flow outputs, exact quality requirements, and fixed material contracts. If verified, the central contribution would be an explicit polynomial-size representation of a sufficiently rich linear feasible set inside a blending network. The one-pool nonlinear construction could then act on that represented set.

This is more informative than observing that a scalar-quality parametric LP has many bases. It would identify which physical-looking linear couplings carry the complexity. The bare existence of a large parametric basis family is neither a hardness proof nor a polynomial algorithm obstruction by itself.

The final theorem should state these scope details explicitly:

- One physical quality with lower and upper specifications is distinct from one upper-only quality in Haugland's counting convention; the corresponding upper-only encoding uses two coordinates.
- Fixed source outflow contracts and fixed output demands use lower as well as upper flow bounds. They must not disappear from the theorem statement.
- Bypass arcs, sources, outputs, and source-output incidence can grow. Artificially counting their degree-one subdivisions as additional pools would obscure the contribution.
- State whether hardness is feasibility or objective-threshold hardness, whether all constructed instances are feasible, and whether an approximation gap is proved. None follows automatically from another.
- Polynomially many variable copies must be established in binary encoding length. Repeating a gadget once per unit of a binary-encoded coefficient is not a polynomial-size reduction unless those coefficients are separately bounded.

Suggested wording after proof acceptance:

> We give an explicit reduction establishing [precise hardness statement] for one mixing pool with unrestricted direct source-output flows and [precise quality and flow-bound conventions]. The result makes rigorous a boundary previously asserted by Baltean-Lugojan and Misener and identifies direct-flow capacity sharing as a mechanism that can encode [verified source-polytope class].

No universal-polytope representation claim is justified until its construction and representation size are independently reviewed. Ordinary blending without a mixing pool is an LP; representing hard objective geometry through a projection is compatible with that fact.

## Search scope and remaining limitations

The audit inspected the local Haugland and Baltean-Lugojan–Misener sources, the open Boland–Kalinowski–Rigterink preprint, Matsui's original preprint, and primary low-rank bilinear algorithms. Targeted open-web searches combined pooling with `one pool`, `single pool`, `one quality`, `two qualities`, `bypass`, `direct arcs`, `feed availability`, `lower bounds`, `fixed supply`, and `Matsui`. No independently checked reduction for the exact one-pool/fixed-quality/shared-capacity bypass variant was found beyond the prior Remark 4.6 assertion.

This is a bounded search, not certification of first publication. Once a candidate theorem exists, repeat forward-citation checks using its exact lower-flow-bound and quality conventions. Its potential novelty is strongest in the explicit encoding mechanism and a sharply delimited theorem, rather than an unqualified claim that this broad hardness boundary has never been stated.
