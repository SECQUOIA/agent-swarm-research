# Independent whole-paper review 03

**Verdict: PASS.** No major or minor finding requiring repair.

Target: `process/snapshots/whole-round01/main.pdf`, 111 pages, SHA256
`912de166731f56368a8ee4db21294aa348b85364e85cd444e31265b29828d084`.
This is an independent final gate on that frozen version. Earlier acceptance
labels were not used as evidence of correctness. I did not read another
review from this round or delegate any part of this review.

## Coverage

I read the complete frozen manuscript, every proof and appendix, the printed
certificate programs, and the complete bibliography. Specifically, I read
`main.tex`, `macros.tex`, `references.bib`, and every file below under the
frozen `sections/` directory:

- `01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`,
  `04-incidence-interiority.tex`, `05-feedback-frequency.tex`,
  `06-treewidth-two.tex`, `07-positive-boxes.tex`, `08-exact-complexity.tex`.
- `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`,
  `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`,
  `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`,
  `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`,
  `17-synthesis.tex`.
- `appendix-finite-signings.tex`, `appendix-positive-couplings.tex`,
  `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`,
  `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`,
  `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`,
  `appendix-fbbt.tex`, `appendix-integer-comparison.tex`.

I also read the frozen review protocol, whole-paper assignment, reviewer-focus
file, scope proposal, complete claim-coverage ledger, stage-06 author record,
complete stage-06 correction log, and README. The additional structural,
physical-box, and algorithmic focus did not replace the whole-paper reading.
The scope ledger's supporting strands are present with their stated limits;
I found no required strand silently dropped or promoted from finite evidence
to a universal result.

I read `literature/AGENTS.md` before inspecting local originals. Primary-source
checks included the following precise inputs. These are checks of relevant
statements and passages, not claims to have re-proved every cited source.

- Hassin–Tamir, Theorem 3.1 and the series-parallel definitions (original
  printed page 381); Cornuéjols, Theorems 6.5, 6.6 and 6.13. The scanned
  Hassin–Tamir page and original Camion page were inspected visually.
  The authoritative [Hassin–Tamir PDF](https://www.math.tau.ac.il/~hassin/sp.pdf)
  and [Cornuéjols notes](https://www.andrew.cmu.edu/user/gc0v/webpub/notes.pdf)
  were also opened directly.
- Deza–Onn, Theorem 1.2 and the Section 3 matching construction, in the
  [author version](https://arxiv.org/html/1908.09278v1); Grötschel–Lovász–Schrijver,
  Theorem 6.4.9 and its well-described rational-polyhedron setting.
- Davidson–Donsig, the projective/Grothendieck discussion and original
  pages 6–7 containing the weighted Schur-multiplier statement; Luedtke–
  Namazifar–Linderoth, the author-version Conjecture 1; Sherali, original
  printed pages 252–253, formula (13) and Theorem 3.
- Altschuler–Boix-Adserà, Theorem 7.4, its accuracy discussion and Corollary
  7.5, including the original page and the arithmetic-model passage.
- Schoenebeck's full author version, Definition 10, Theorems 11–12,
  and the complete Lemma 13 signed-character construction; Potechin's
  stated symmetry/cardinality lower-bound input.
- Kronqvist–Misener–Tsay, retained-domain setup, Assumptions 1–4,
  Definition 4, Theorem 6 and its proof. The manuscript's correction
  addresses the actual retained-domain and componentwise strictness issues.
- Fawzi–Parrilo, original page 3, Theorem 1 and the Lorentz-cone conversion;
  Braun et al., the hard pair and Theorem 6(i); Lee–Raghavendra–Steurer,
  original pages 23, 32 and 34, Theorems 3.8, 5.3 and 5.4, including
  equation (3.11).
- Stewart–Etessami–Yannakakis, Section 4.1 and original equation (18).
  The manuscript correctly labels its Kleene-iteration consequence as an
  inference and proves that inference separately.

## Findings

None. I found no demonstrable defect in theorem truth, proof completeness,
necessary assumptions, central attribution, required coverage, or the
reader's ability to verify a main argument. The following records the
substantive challenges made to the manuscript rather than relying on that
negative conclusion alone.

## Independent verification

### Proof reconstruction and attempts to falsify the claims

**Widths and structural bounds.** I reconstructed the vertex-law reduction,
common upper attainment for positive terms, and the resulting deficiency
formulation. I checked the induced bilinear cell argument and polarization
constants. For the dyadic and variable-radix examples, I followed both the
upper-tail resource inequality and the attaining count mixtures, including
digit-reversal marginal restoration. The simple radix formula is used only
in its stated parameter range. The elimination order and complete-bipartite
minor establish the claimed incidence width.

The incidence orientation proof correctly allocates high variables to
disjoint owners; its polynomial-level estimate supports the outgoing-degree
alternative. The floor choices in the joint interiority/width lower bound
preserve the claimed asymptotic range. The feedback proof's residual
domination and conditional forest gluing work at degenerate means. Its
generic-payoff sharpness example does not purport to prove the corresponding
positive-monomial sharpness for arbitrary feedback number.

For frequency two, I checked the active-column rank argument forcing
vertex-disjoint odd half-cycles, the retained baseline in the coverage
bound, and the odd-girth constant. For incidence width two, I reconstructed
the active/blocking series-parallel invariant for the terminal types and
parallel combinations. Cycle decomposition followed by Camion gives TU
for all Eulerian square submatrices. The width-three all-ones obstruction
is correctly distinguished from a TU obstruction. The finite experiments
about stronger partitions remain explicitly finite evidence.

**Physical boxes and algorithms.** I checked the finite balanced-orientation
coefficient calculation and the spreading argument: moving a global minimum
and maximum preserves the needed constraints. Restricting the ambient
balanced law retains the ambient coefficient. Nonnegative expansion and
positive affine transfer justify the unequal-box bound without claiming
that expansion preserves incidence structure.

I reconstructed the edge-cover and convex-degree matching reductions with
signed costs. Negative edge costs in the coverage case are handled before
the nonnegative reduction. In the convex-degree gadget, the two mandatory
endpoints enforce an all-or-nothing edge choice, the cheapest slots telescope
to the degree cost, and the bonus exceeds every possible cost difference.
The scalar-envelope dual has bounded rational vertices by Cramer's rule;
the separation-to-optimization invocation therefore has polynomial encoding
length, including boundary means. This does not establish a small explicit
formulation for all factor values, and the manuscript does not claim one.

For exact hardness, I checked the PARTITION reduction's product expansion,
the epsilon choice, remainder bound, and the positive NO-instance variance
gap, as well as the polynomial-size rational law certificate. Common-aspect
tractability and arbitrary narrow unequal-box hardness have distinct
hypotheses. The rank-one transport comparison distinguishes logarithmic
accuracy complexity from inverse-accuracy algorithms.

**Spatial certificates and strengthened local relaxations.** I reconstructed
the cardinality Gram decomposition and its positive coefficient range,
homogenization degree, and full indicator-product localizers. Endpoint
substitution uses actual witness membership on restricted coordinates and
actual membership of both endpoints on unrestricted coordinates. The argument
allows arbitrary nonclosed coordinate domains without taking closures or
using approximation; the local graph maps preserve the information that the
argument needs. Objective agreement on the full graph is used.
The tensor construction restricts to the appropriate total-degree principal
submatrix. Relative block arguments use the translated perturbation
correctly, and the component/clique-cut escape witnesses remain valid.

For XOR, I checked closure under the allowed width, the signed-character
Gram representation, and deterministic substitutions. The local quadratic
moments have actual signed-class realizations on the full box. The bounds
on pulled-back degree, support union, and rank supply all the required
squares and localizers. The low-order monomial reformulation and the
separate Bernstein/full-quadratic-hull upper certificates respect their
different oracle conventions.

**Supporting strands and cross-section consistency.** I followed the
point-packing covariance/secant calculations, endpoint scaling hull and
perspective distinctions, repaired rectangular catalogue membership, retained-
box P-split counterexample and directional escape criterion, rational
rotation and exact auxiliary-image restrictions, correlation-face exposure
and stability estimates, FBBT least-fixed-point and arithmetic-circuit
constructions, every-schedule primitive iteration lower bound, and integer
parity cover. The approximate PSD transfer retains the logarithmic factor
arising from the quoted pseudo-density estimate. Local width, scalar
optimization, node strength, spatial cover size, and global lift size remain
distinct throughout the synthesis.

### Exact finite checks

All independent check artifacts are under
`verification/reviewer03/whole-round01/`. The main program is
`check_independent.py`; its SHA256 is
`47528d849e57110e3bf5c5b0381b3b4c0b482e61d46ffef41c9a8194b5794efd`.
Results are in `independent-results.json`.

- Exact rational integration of balanced-orientation laws tested 1,294
  coefficient inequalities on seeded rational cases with 2–7 coordinates,
  including zero and one means and orders exceeding the support size.
  All passed.
- Exhaustive enumeration of all 4,096 labeled bipartite graphs with sides
  of sizes 3 and 4, followed by degree-at-most-two elimination with fill,
  identified 3,845 graphs of treewidth at most two. Each admitted a factor
  two-coloring with no monochromatic cycle having an odd number of factors.
  All passed. This is an exact bounded-size falsification attempt, not a
  proof of the universal series-parallel invariant.
- On 120 seeded multigraph instances with signed integer edge costs and
  convex integer degree tables, the matching gadget agreed with exhaustive
  enumeration of all original edge subsets. Integer matching arithmetic
  was used. This validates finite behavior, not the polynomial-time theorem.
- I extracted and executed the actual printed programs from
  `appendix-finite-signings.tex` and `appendix-cubic-certificates.tex`.
  Both passed their complete stated enumerations using integers and
  `Fraction`. Saved program text and outputs make the replay inspectable.

These checks use no floating-point optimizer or tolerance-based certificate.
Their independence lies in the additional law, graph, and gadget checks;
executing the printed programs is a reproducibility check, not independent
discovery of their certificates.

### Build and visual inspection

I built from my own copies of the frozen inputs under
`verification/reviewer03/whole-round01/build/` with `latexmk -pdf
-interaction=nonstopmode -halt-on-error`. The build succeeded and produced
111 pages. Its layout-preserving text extraction is byte-identical to the
frozen PDF's extraction. The build has three underfull-hbox notices, with
no overfull boxes or unresolved-reference failures; I found no resulting
reader-facing defect.

I rendered every frozen PDF page and visually inspected all 111 pages in
contact sheets. I additionally inspected pages 25, 29, 33, 37, 41, 86, 101
and 111 at a larger scale, covering dense formulas, structural and algorithmic
arguments, a printed checker, the correlation face and bibliography. I saw
no clipped equations, overlapping content, missing pages or broken code
layout. The complete mathematical reading was from the source; the all-page
thumbnail inspection is a layout check, not a claim to have read every glyph
at that resolution.

## Remaining limits

This is a mathematical review, not a formal proof-assistant verification.
The finite checks do not establish unbounded theorems. I did not rerun every
historical structural experiment or independently regenerate all reported
search data, and those experiments are not used as proofs in the paper.

I checked the relevant primary-source passages above but did not audit the
complete proofs of deep external results such as random-XOR width lower
bounds, ellipsoid equivalence, Grothendieck's inequality, or the global
nonnegative/PSD-rank theorems. I did not independently inspect every original
behind all 41 bibliography entries or settle publication identity/priority
questions for anonymous or unpublished supporting material. A scanned Karp
source did not yield usable extracted text; classical PARTITION
NP-completeness is an accepted external input here. These limitations do not
identify a false or unsupported application in the frozen manuscript.

The paper's explicitly open higher-width partition questions, sharp planar
constants, and extensions beyond the stated oracle, domain, and encoding
models remain open. This PASS does not enlarge those claims.
