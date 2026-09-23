# Stage 2, round 1: independent review 2

Verdict: **revision required for the source conventions identified below**. I found no counterexample to the microscopic threshold theorems and no failure in the new cutoff-removal, cluster-differentiation, or bond-to-spin argument when all objects use the BCT2012 construction consistently. One central source-convention claim is inaccurate; a second source-scope claim needs qualification.

I reviewed `sections/microscopic.tex`, `main.tex`, `refs.bib`, the Stage 1 dependencies, and `stage-2-author.md`. I consulted the original local primary-source texts `bkms1991.txt`, `bct2012.txt`, and `bchpt2022.txt`. I did not consult other current reviews, edit the manuscript, or delegate work.

## Findings

### R2.1 — The two contour references do not use identical phase-event definitions

**Location:** `sections/microscopic.tex`, lines 371–374, and subsequent uses of BCHPT2022 as though it described the same finite-volume contour objects.

**Severity:** Major source-convention issue under the review protocol's criterion for incorrect source attribution. The likely remedy is local, and I do not regard this as evidence that the threshold theorem is false.

**Claim:** “The exact event definitions and multiplicity ... are also recorded” in BCHPT2022 Sections 3.3–3.4, equations (44)–(46).

**Primary evidence:** BCHPT2022, printed p.16, Definition 5 and the immediately following Remark, explicitly states that its definition of exterior differs from BCT2012. BCHPT selects the larger of the two components, with a tie-breaking point. BCT2012 Definition 4.4, printed p.16, first uses the component containing a compatible interface when one exists and only otherwise uses size and a tie-breaker. The ordered/disordered events are defined from these exteriors. BCHPT2022 itself cautions that transfer of results between these definitions requires checking applicability. Its Lemma 3.9 likewise explains its volume estimate by comparing its smaller interior with the BCT interior.

**Consequence:** The ordered multiplicity `q` and the positive decomposition structure are supported by both references, but this does not establish equality of their finite-volume phase events. The new proof must fix one contour convention before using the inactivity criterion, volume bound, partition derivative, and conditional phase law. In particular, the reader should not be invited to substitute BCHPT's definitions into BCT Appendix A without an argument.

**Exact remedy:** State explicitly that every contour, interior, exterior, phase event, and restricted partition function in the proof uses BCT2012 Definitions 4.4 and 5.4 and equations (6.1)–(6.5), (6.13)–(6.22). Cite those equations for the exact positive events and multiplicity. Replace the claim of identical definitions in BCHPT with a note that it uses a modified exterior convention and is cited only for the separately identified general cluster estimates or stable-side discussion. Alternatively prove the transfer of all used inputs to the modified convention, but that is unnecessary here.

### R2.2 — Section 3.8 does not give unrestricted random-cluster interpretations of every contour interior

**Location:** `sections/microscopic.tex`, opening paragraph of the proof of Lemma `lem:sr-restricted-derivatives`, especially lines 537–547.

**Severity:** Minor clarification of source scope, because the manuscript also supplies the correct general route through BCT's matching-label representation.

**Claim:** The positive interior partition sums are described as random-cluster sums, followed by the statement that their “exact random-cluster interpretations are given in Section 3.8” of BCHPT2022.

**Primary evidence:** The opening paragraph of BCHPT2022 Section 3.8, printed p.22, expressly says that general contour partition functions do not correspond to random-cluster partition functions because interfaces are excluded. It then restricts the ordinary free/wired interpretation to interiors that embed in `Z^d`; Proposition 3.14 imposes a simply connected finite-region construction. That proposition cannot by itself justify unrestricted use for every torus interior, including the contours of diameter comparable to `L` used in the cutoff-removal argument.

**Exact remedy:** Base the general derivative estimate directly on BCT2012 equations (6.13)–(6.14). For a matching contour configuration write its log weight as the explicit ordered/disordered ground terms plus `−kappa` times its total internal contour size and a temperature-independent color factor. Explain that the sum of internal sizes is bounded by a constant times the interior vertex count plus the bounding contour size: each nearby lattice bond contributes only a bounded number of intersections. Therefore each summand has first and second logarithmic derivatives of order `|Int gamma| + m_gamma`. Positive-sum differentiation gives a second logarithmic derivative of order `(|Int gamma| + m_gamma)^2`, which yields the displayed `m_gamma^2` and `m_gamma^4 K_gamma` activity estimates. Qualify or remove the Section 3.8 citation rather than asserting its unrestricted applicability.

This small expansion would also make the new derivative argument easier to verify without reconstructing a contour-to-bond correspondence.

## Source claims verified

- **BKMS1991 Theorem 1:** The source states `d >= 2`, sufficiently large `q`, six-times differentiable phase free energies, stable ordered/disordered branches, positive latent heat, and the periodic partition expansion with ordered multiplicity `q` and error `O(q^(-bL))`. Its equations (6)–(8) use precisely the negative monochromatic-bond Hamiltonian with unit coupling. The paper's conversion `psi_i = beta f_i` and its real-temperature use are correct. No complex-temperature continuation is needed for the arguments here.

- **A fixed interval around coexistence is available:** BCT2012 equation (1.5) gives `beta_c = (log q)/d + O(q^(-1/d))`; Appendix A assumes `beta >= max{C1 log(dC), (log q)/d - 1}`. For fixed `d` and sufficiently large fixed `q`, these conditions hold on a fixed real neighborhood on both sides of coexistence. Appendix A explicitly says that it proves Lemma 6.3(i),(ii) whether or not `beta >= beta_0`. Thus using this interval is justified, even though the main-text lemma is phrased on the ordered side.

- **Exact truncation and inactivity:** BCT2012 equation (A.3) defines a minimum of the original positive activity and a smooth exponential cap; its displayed cap has exponent `beta/8 - c beta + 1`. Lemma A.1(i) states equality of original and truncated activities under `a_i diam(gamma) <= c beta`. The manuscript has not replaced this equality by merely an activity upper bound. The original diameter and volume bounds are exactly BCT2012 Lemma 5.7.

- **Finite-volume pressure error:** BCT2012 equations (A.7)–(A.8) give the infinite-volume truncated pressures and the exponentially small finite-torus error. The manuscript's `O(N exp(-bL))` bound follows. On the stable branch the cutoff is inactive; the restricted contribution and the positive decomposition give the physical thermodynamic pressure. BCT2012 Lemma 6.3(iii), Appendix A.4, and BCHPT2022 Appendix B.1 support the phase identification on the two stable sides. Equating stable pressures does not require equating the two different metastable extensions.

- **Positive phase probabilities and tunneling:** BCT2012 equations (6.1)–(6.5) give genuine positive events and the exact factor `q`; Lemma 6.1 gives the tunneling bound and the coexistence weights. These inputs suffice without transferring the modified BCHPT exterior definition.

- **Cluster summability:** BCT2012 (A.5)–(A.6) provide the convergence margin needed to retain a positive exponential factor in total cluster size by increasing the fixed lower bound on `q`. The corresponding anchored estimate is explicit in BCHPT2022 Lemma 2.1 and equation (19). Summing over the bounded-degree contour embedding gives the asserted volume factor. Polynomial first- and second-derivative factors can be absorbed by this margin.

## Mathematical checks of the new short-range closure

1. From `|partial_beta log K| <= C m^2`, the minimum-truncated activity is absolutely continuous and satisfies the required derivative bound almost everywhere. The cluster majorant justifies the integrated first-derivative argument. Uniform Lipschitz continuity passes to its infinite-volume pressure, so `a_i(beta) <= C|beta-beta_c|` follows from coexistence equality. No differentiability of the minimum cutoff is assumed.

2. For the BCT diameter, `diam(gamma) <= L` holds even for wrapping geometry. Thus all finite-torus cutoffs are inactive on a sufficiently small `eta/L` interval. On that interval the original activities are smooth positive functions; their first two derivatives and the majorant justify the `O(N)` bound on the restricted second derivative.

3. The stable-side finite difference uses displacement of order `N^(-1/2)`, which lies inside `eta/L` for every fixed `d >= 2`. Dividing the exponentially small pressure error by that displacement remains negligible, while the Taylor remainder is `O(sqrt N)`. This gives the center accuracy needed for a standardized exponential moment.

4. The fugacity conversion is exact: `exp(d beta N) Z_i` is the fixed-event sum of `(exp(beta)-1)^B q^k`, up to the constant ordered multiplicity. Its derivatives in `lambda` are the conditional bond mean and variance. The chain rule retains an `O(N)` second derivative.

5. Conditional on spins, the Edwards–Sokal bond count is Binomial(`M,p`). Its centered noise has the stated uniform exponential moment on scale `sqrt N`. Conditioning on a bond phase costs only a bounded inverse phase probability; it need not preserve conditional binomial independence. The manuscript correctly uses the unconditional noise bound followed by conditioning. The Cauchy–Schwarz transfer to spin energy and its factors of `p` are correct.

6. The resulting positive spin-energy phase measures have the moment control required by Stage 1. The exceptional exponent `-b L^(d-1)` dominates the bath gain `o(sqrt N)` because `d-1 >= d/2`. Projection of the correctly reweighted joint law gives the exact physical spin marginal.

7. The separate necessity argument correctly obtains midpoint-conditioned weak CLTs from one-sided real Laplace limits. The positive lower bound on spin variance passes through strong convexity of the stable thermodynamic pressure, rather than through the total coexistence variance. Its independent-set and conditional-color calculation is valid for fixed sufficiently large `q > 2d`.

## Remaining stagewide checks

The mean-field stationary-point classification, Hessians, Gaussian phase weights, ordered-phase spin variance, and degenerate disordered spin-energy limit are consistent. The ordered phase alone supplies the required nondegenerate local scale when `a=0`, so the pure-spin extension is justified. The global occupation bound deals with the simplex boundary and yields the needed positive conditional moment bounds. Kinetic smoothing supplies the stated continuous local limits and interior envelope when `a>0`.

Direct integration gives occupation exponent `A+c`, conditional Beta parameters `(A,c+1)`, and the stated Gamma/Beta CDF formulas. Strict concavity of the likelihood yields the single interval used for continuous total variation; the separate discrete prescription avoids a shape-zero distribution. These calculations are exact, and I found no algebraic correction needed.

The stage clearly separates positive contour measures from midpoint energy events, and the definitions of the model and heat-capacity exponent remain consistent with Stage 1. This report does not certify literature novelty, assess later stages, or claim that numerical tests establish the contour theorem. I performed analytic and primary-source checks, not a new numerical computation.
