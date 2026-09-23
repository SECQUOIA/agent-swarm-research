# Stage 5, round 1: independent review 5

**Verdict: no major issues identified. Three minor wording and scope corrections are requested.**

I read the Stage 5 author handoff, new abstract, introduction, numerical section, conclusions, revised main-text short-range guide, reproduction README, coverage audit, bibliography, figure code, and numerical records. I checked the synthesis against the theorems reviewed in earlier stages and sampled the relevant primary-source passages. I did not consult other current-round review reports, edit the manuscript, or delegate.

## Minor findings

### 1. Qualify the comparison of total variation with unbounded averages

**Location:** `sections/introduction.tex`, lines 17–20, especially “It is stronger than agreement of thermodynamic potentials, energy density, or any specified finite set of averages.”

The preceding statement about bounded measurements is correct. The next sentence can be read as claiming that TV convergence implies convergence of all the listed unbounded averages or thermodynamic quantities. That implication requires additional assumptions. A probability of order `1/N` at an energy of order `N^2` can vanish in TV while contributing a nonvanishing change to the mean energy per particle. This distinction matters because the weak-support theorem deliberately requires no moments.

**Fix:** State the intended implication directly: agreement of those quantities alone does not establish full-state TV convergence. Retain the bounded-measurement claim and, if needed, add that unbounded moments require separate integrability control. This is a prose qualification; no theorem is invalidated.

### 2. The short-range proof guide should name logarithmic derivatives

**Location:** `sections/microscopic.tex`, lines 325–327, newly added main-text proof guide.

The guide says that the positive phase partition functions have bounded second derivatives. The proved useful estimate is `|(log Z_{i,L})''| <= C N`; it is not a comparable bound on the second derivative of `Z_{i,L}` itself. The distinction is particularly relevant to readers learning why the estimate supplies fluctuation moments.

**Fix:** Say that their **logarithms** have second derivatives of order at most `N` throughout the stated window. The relocated appendix already has the correct estimate.

### 3. Add the stronger boundary hypotheses to the early summary

**Location:** `main.tex` abstract sentence beginning “At the N^(3/2) boundary,” and `sections/introduction.tex`, lines 113–116.

The introduction correctly states the general convergence threshold for short-range models in every fixed dimension at least two. Its immediately following summary of the boundary law omits the stronger finite-tilt integrability and exceptional-mass requirements. A reader who stops at the abstract or overview could infer that the boundary formula is proved for all positive coefficients in the two-dimensional short-range model. The conclusions and the boundary section correctly state the restricted range.

**Fix:** Add a short qualifier such as “Under the stronger finite-tilt tail bounds” to the abstract and overview boundary statement. In the overview, either mention the sufficiently-large-coefficient restriction in two dimensions or point explicitly to the microscopic range of the boundary theorem. No change to the theorem or result table is needed.

## Structure and reader assessment

The paper now has a clear physical route: what is compared, how the exact reservoir reweights it, why the required size changes with energy support, microscopic examples, shared-bath correlations, and boundary errors. The introduction's explanation of endpoint slopes connects the mathematical product of gap and fluctuation width to a concrete thermodynamic mechanism. The table is useful and correctly distinguishes an energy phase from several symmetry-related ordered phases at one energy.

Moving the technical contour proof into an appendix materially improves readability for a chemical-engineering reader while retaining the proof in the same document. Its main-text guide identifies the real technical issue, namely transferring a positive bond-phase moment bound to the exchanged spin energy. The shared-bath section remains prominent and consistently distinguishes the prescribed balanced canonical reference from the original unbalanced temperature. Gaussian geometry and the stated capillarity model are appropriately separated from microscopic physical theorems.

Notation is adequately scoped. The heat-capacity exponent is consistently distinguished from the canonical `c+1` convention. The numerical section defines its standardized boundary tilt before using the symbol, and the captions distinguish finite-size data from a limiting formula. I found no unresolved label, duplicate label, or missing citation key after relocation. The existing LaTeX log contains no undefined-reference/citation or box-warning matches.

The coverage audit accounts for the relevant reservoir notes and explains the independent directions excluded from this paper. It records the resolved short-range sufficiency question, the removal of the mean-field kinetic requirement, completed global optimization arguments, and remaining restrictions that are actual theorem hypotheses. I found no missing result needed for the current main argument. The root status updates distinguish the stopped exploratory pass from the continuing manuscript review rather than presenting internal reviews as external publication acceptance.

## Mathematical and numerical verification performed

The summary's three support-based scales, the shared-bath window and one-bit information limit, the two microscopic threshold claims, and the physical boundary optimization agree with their theorem statements, subject to minor finding 3 about early qualification. The new deterministic formulas also agree with the previously reviewed mathematics.

I independently reran the small numerical checks without invoking their result-file-writing entry points:

- Explicit labeled-spin enumeration for `N=1,...,8`: maximum energy-mass discrepancy `3.3306690738754696e-16`.
- Independent direct density integration at `N=12`: discrepancies from the Gamma/Beta CDF TV calculation approximately `9.19e-12` for kinetic shape 6 and `1.16e-14` for shape 12.
- The standalone Stage 4 checks all passed, including weighted Gaussian TV/root comparisons, physical compensation, and the square-torus inequality.
- Recomputed the archival SHA-256: `93fed9507ceaf9126feb93e79ae5bbb295be185a56f9a84dabe0608e55aab2c1`, matching the README.
- Compared parsed Python function bodies with the earlier algorithm: both `canonical_energies` and `finite_bath` are unchanged.
- Compared the saved fresh `N=300` values to their archived counterparts: maximum full-TV difference `1.1102230246251565e-16`.

I read the plotting code and visually inspected both PNG figures. Figure 1 uses `energy_tv`, the full spin–momentum distance justified by the energy likelihood identity, rather than the separately reported configuration marginal distance. Its boundary slopes, phase weights, and variances give the quoted limits `0.15739182188178924` and `0.0379859806585022`. Figure 2 evaluates the proved equal-variance limiting formula and does not masquerade as a finite-size simulation. Both plots are readable, with clear axes and legends.

The README accurately separates the 18 archived exact-enumeration points, fresh smaller checks, optional full recomputation, and formula-derived figures. It makes the ordinary floating-point status explicit. I did not repeat the expensive large-size enumeration or independently test every declared minimum dependency version.

## Literature and bibliography checks

All manuscript citation keys resolve in `refs.bib`; the source formats provide primary URLs and DOI identifiers where supplied. The synthesis credits established ensembles, two-phase Gaussian descriptions, supporting-quadratic geometry, conditional-limit methods, and phase correlations rather than presenting those mechanisms as discoveries here.

I directly checked representative retained primary passages:

- Griffin–Matty–Swendsen equation (23) is the Euclidean norm of energy-probability differences, and their discussion describes fitting the comparison temperature. The stated distinction from prescribed-target TV is supported.
- The Riera–Gogolin–Eisert text and its bath construction support the entropy-remainder/strong-distance comparison and squared subsystem-energy-scale sufficient size.
- Campisi explicitly relates finite reservoir capacity to power-law ensembles.
- The previously checked Ramírez-Hernández–Larralde–Leyvraz result supports the credited opposite-phase assignments; the shared-information source addresses ensemble dependence and phase contributions.

I did not treat the inaccessible full text of the 1990 review as evidence of absence. Its limited role in the manuscript and the source-access qualification in the author/reproduction records are appropriate. This is not an exhaustive new priority search or a rereading of every bibliography entry.

This verdict concerns the Stage 5 synthesis. The separate whole-manuscript review still remains necessary under the requested workflow.
