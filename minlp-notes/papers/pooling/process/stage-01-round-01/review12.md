# Stage 1 review, round 1 — reviewer 12

Focus: mathematical exposition, definitions, quantifiers, proof completeness, and notation. I independently read all of `sections/01-foundations.tex` and checked its arguments. I did not read other review reports or edit the manuscript.

## Findings

### 1. Major: endpoint formulation omits the upper-quality-only hypothesis

**Location:** `sections/01-foundations.tex`, lines 641–672, especially the claimed equivalence at lines 647–658.

The model allows both lower and upper product quality specifications (lines 36–39). The endpoint paragraph restricts input qualities to `[0,1]` and product **upper** bounds to `{0,1}`, but does not remove lower quality bounds or additional polyhedral product inequalities. Consequently its stated equivalence and exact MILP do not follow under its written assumptions.

A concrete example has one input of quality zero, one pool, one product, unit arc and node capacities, and zero lower flow bounds. Let the product quality interval be `[1/2,1]`. Routing one unit satisfies the displayed support disjunction: `D=0` and `S=0`. There are no bypasses to delete. Nevertheless its product mass is zero, violating the lower quality requirement. Thus the proposed formulation accepts a physically infeasible flow. The example satisfies every explicitly listed endpoint restriction.

**Fix:** State explicitly that the only product quality restrictions in this special case are the upper coordinate bounds `m_jk <= overline(mu)_jk t_j`, with `overline(mu)_jk in {0,1}` (equivalently allow only redundant lower bounds at most zero), and that no other polyhedral quality restrictions are imposed. Retain arbitrary lower **flow** bounds as intended. Under this added hypothesis the disjunction proof, MILP, integrality, and NP-certificate arguments check out. This is a missing essential hypothesis, although the textual repair is short.

### 2. Minor: the same symbol denotes a polyhedral right-hand-side vector and a scalar demand

**Location:** `sections/01-foundations.tex`, lines 42–43 and 51–53.

The first use makes `b_j` the vector in `A_j u <= b_j`; nine lines later `b_j` is the scalar exact delivery demand in `t_j=b_j` and `m_j=b_j B_j`. Both modeling options are retained in the section, so readers cannot consistently assign a type to `b_j` when the options coexist.

**Fix:** Use, for example, `d_j` for exact demand and keep `b_j` for the polyhedral right-hand side, or use a different symbol for the latter. This does not affect the results.

## What was checked

- Standard and generalized balance equations, zero-flow conventions, affine-rank substitution, and the rank-one/margins identity.
- Destination decomposition, including head-based disaggregation, physical quality preservation, capacity domination, and the averaging inequalities.
- Single-product reconstruction, aggregate quality conservation, rational encoding reasoning, the shortest-path criterion and its `K+1` support bound.
- All stated conic-hull containments, the capacity counterexample, cyclic SCC reconstruction, the absorption decomposition, and the negative-cycle criterion.
- Facial sufficiency and necessity, network integrality, the forbidden-input faciality LP, face-state enumeration, and the endpoint formulation under the repaired upper-quality-only hypothesis.

The main proof sequence is coherent and unusually explicit about active versus inactive pools, exact certificates, restrictions on cost functions, and the distinction between threshold hardness and feasibility. I found no other mathematical error in these arguments.

## Verdict and limits

**Verdict: major findings present**, specifically the omitted endpoint-specification hypothesis. One additional minor notation issue is listed.

This is a mathematical and exposition review of the assigned stage, not a verification of novelty or of the cited articles' complete contents. I consulted the endpoint development in `results/pooling-facial-quality-integrality.md` for context; its intended upper-bound-only formulation is consistent with the proposed repair. I did not check unassigned later stages, run compilation, or audit external bibliographic metadata. This review cannot guarantee exhaustive correctness or journal acceptance.
