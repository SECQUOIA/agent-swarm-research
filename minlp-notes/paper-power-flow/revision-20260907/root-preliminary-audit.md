# Root preliminary mathematical reading

Read in full: foundations, ordinary reduction, AC encoding and transfers, structural transformations, algebraic results, numerical results, bounded-arithmetic appendix, verification appendix.

The following four existing suites were freshly executed with python3; all exited zero: check_resistive_exact.py (12,751 profiles), check_ac_exact.py (2,112 pairs and 177,168 cycles), check_developments_exact.py (structural and residual checks), check_arithmetic_exact.py (1,681 composed profiles and full disk circuit). Finite checks supplement proofs.

No immediate counterexample to a central statement found during this reading. Particular independent checks: rectangular complex-power signs; crossing-rule axis cases; real-angle energy positivity below pi; one-sided reactive cancellation; subdivision current scaling by 1/(4L); three-quadrant basic-closedness obstruction; uniqueness and ranges in shifted reciprocal arithmetic; residual-transfer constant; tiny-residual recurrence; rational rounding with exact singleton clamping; Laplacian energy constants.

Stage 2 candidate improvement: replace explicit fundamental-cycle equations in the existential encoding by real vertex variables a_i with a_root=0 and a_i-a_j=k_ij on oriented edges. Since each k_ij is in {-1,0,1}, tree propagation makes a_i integer automatically, and such potentials exist exactly when all cycle sums vanish. This gives O(V+E) variables/constant-size predicates and O(V+E) monomials without an integer quantifier; complete bit encoding still includes graph indices and rational input lengths. It is an elementary incidence-potential compression, not a proposed novelty claim. Author must verify signs and disconnected cases before adoption.

Literature concern forwarded to Stage 1: cite closest angle-recovery and winding predecessors, especially local Farivar–Low and loop-flow work. The zero-winding criterion itself should not be presented as new. The version-specific Dynamic Toolbox claim and rational-equivalence definition were located in local fulltext.

## Primary-source cross-check

Opened local literature/papers/jeronimo2013-on-the-minimum-of-a/original.pdf pp.1–2 through pdftotext -layout. Theorem 1 has base 2^(4-n/2) Htilde d^n and exponent -n 2^n d^n, agreeing with manuscript specialization d=2. The local original carries arXiv v1 and its locator differs from the journal Theorem 1.1 currently cited; forwarded to Stage 1 author.

Root supplemental web searches on power-flow existential-real completeness/universality and the Dynamic Toolbox correction found no matching classification, but their absence is not evidence of priority. Author's separate source audit records the bounded novelty evidence.

Reviewer 4 located the published JPT original at https://ri.conicet.gov.ar/bitstream/handle/11336/14866/CONICET_Digital_Nro.18274.pdf?isAllowed=y&sequence=1 . Root opened it independently: journal p.242 Theorem 1.1 gives the exact cited bound with n>=2 and Htilde=max(H,2n+2m). The manuscript locator is correct; earlier uncertainty is resolved without changing the mathematical citation.
