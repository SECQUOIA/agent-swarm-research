# Stage 4: root proof and source investigation

Stage 4 began only after stage 3 closed with all 15 second-round reports recording no findings. The sole author is `/root/stage04_author`. Root independently reads the proofs, checks sources and selected computational evidence, and builds the resulting draft before the mandated review round.

## Initial complete mathematical reads

Root read all three canonical results: the full fixed-core/block theorem, the bypass vertex-integrity/affine-quality-rank mapping, and the bounded polygon-path projection and attachment theorem. The source audit and fixed-core novelty note were also read. No mathematical defect has been identified in these initial reads; this is not a review verdict for the still-unwritten stage.

The general support construction fixes the joint core/support dimension, enumerates signs of local vertex validity and score comparisons, and avoids the exponential Cartesian product of bases. After selecting compatible bases, squared-denominator clearing creates degree growing linearly with the number of blocks. Fixed variable count keeps dense polynomial expansion and subsequent quantifier elimination polynomial in input length. Empty blocks, singular candidate bases, lower-dimensional leaves, and zero signs require explicit treatment. Recovery must take place in one common algebraic field of polynomial degree.

The structural mapping assigns every arc once. Covered output mass and quality-coordinate totals belong to the core, so growing output attribute counts add core rows rather than aggregate dimensions. Lower bounds and zero-throughput pools remain in scope. Bounded vertex integrity is distinct from bounded graph degree or treewidth.

The path result projects only a fixed number of actual boundary flow coordinates. It does not retain arbitrary dense costs or global aggregates. Balanced composition controls size and bit growth; reconstruction uses rational affine operations within the sampled common field. The multiple-pool extension must preserve external contracts when removing unusable pools. The degree-two/degree-three comparison concerns contracted feasibility.

## Computable compact-core boxes

Root proposed completing the slack-bound extension without an additional input-box assumption. For a nonempty compact rational semialgebraic core in fixed dimension, eliminate all but one coordinate at a time. Each projection is compact and has a polynomial-size univariate formula. Its finite endpoints are roots of nonconstant polynomials in that formula. Cauchy root bounds then give rational enclosing bounds of polynomial bit length. Constant or empty projections and zero-dimensional cores are treated separately. Interval arithmetic over the resulting box and supplied leaf boxes gives polynomial-bit aggregate slack bounds. The author is independently checking and developing this argument.

## Primary algebraic-LP source

Root read Adler–Beling's original article introduction, field-degree definitions, general-algebraic scaling discussion, and Section 5 Remark 1. Original PDF page 20 (printed p.455) was visually inspected. It explicitly states polynomial rational-machine time in LP dimension, common problem-field degree, and coefficient triplet bit lengths; it outlines the finite-precision construction and defers a full exposition. The common-field condition is essential. The bounded recovery LP contains box rows, so the paper's full-column-rank formulation causes no gap. The manuscript should cite this precise scope and not imply that many separately encoded radicals automatically have polynomial common degree.

The author initially reported two authors for the TVPI source from its package metadata. Root checked the actual original PDF and its page-1 extraction: it lists Axel Simon, Andy King, and Jacob M. Howe. Thus the older boundary note's three-author attribution is correct for the inspected artifact; the package metadata is not. The primary Kent publication page also lists all three and explicitly identifies the online revised manuscript as the preferred version after a publisher-version problem. Its displayed volume/page metadata is internally inconsistent, so it must not be copied unchecked. Root instructed the author to cite the inspected three-author revised manuscript (PDF footer 27 October 2010), with its own page locators and primary URL, rather than merging incompatible version metadata. Sources: `https://www.cs.kent.ac.uk/pubs/2010/3167/` and its `content.pdf`. Imported literature remains unchanged.

## Selected finite checks

The existing support-reduction, structural-mapping, and boundary-projection checkers were inspected and run independently by root. Their logs are retained under `verification/logs/`. The first mixes exact support/denominator arithmetic with numerical SciPy LP comparisons; the second checks exact symbolic ownership/residual identities; the third checks exact polygon compositions using Fourier–Motzkin elimination. None implements the complete real-algebraic optimization algorithm or proves the asymptotic description bound.

All passed: 1,971 exact support/denominator comparisons plus independent numerical LP and degeneracy checks; 15 symbolic structural mappings with 375 exact ownership/residual identities; and 70 exact polygon compositions with 480 lower/upper slice identities, including points and vertical/nonvertical segments. Logs are `fixed-core-support.txt`, `bypass-structure-mapping.txt`, and `boundary-projection-exact.txt`.

## Additional current source check

Root inspected the primary publisher text of Martin Brain and Jacob M. Howe, “Canonical Forms and Widening for Two Variables Per Inequality Systems,” Mathematics in Computer Science 20, article 2 (published 11 March 2026), DOI 10.1007/s11786-025-00612-6. Its abstract, introduction, closure definitions, and stated results concern canonical representations and widening in abstract interpretation. These inspected passages do not supply the balanced bounded-path projection size and bit-complexity argument used here. This is a scoped source comparison, not an exhaustive priority finding. Primary source: https://link.springer.com/article/10.1007/s11786-025-00612-6 .

Root also read the entire older vertex-cover precursor and confirmed its distinct specialization, recognition procedure, arbitrary signed linear arc costs, and bounds are represented by the stronger vertex-integrity/affine-rank mapping. Its old fixed-product open-case language must not survive: accepted stage 3 now resolves the two-pool/two-product branch negatively. The stage-4 author independently identified and corrected that cross-stage point.

## Full manuscript read before reviewer freeze

Root read the complete 1,024-line initial stage-4 draft. The general theorem, both basic pooling mappings, rank/vertex-integrity ownership and aggregate counts, planar envelope bound, balanced reconstruction, multiple-pool boundary map, restricted objectives, and degree-three contracted hardness mapping were checked. One local constructive-proof wording was sent to the author: redundant inequalities must be tested against the system with the candidate row removed, not merely against vertices of the original system. Exact planar LP supplies the required test. No change to the projection theorem is needed.

Root visually inspected original BPR PDF pages 3–4 (printed 1004–1005): the Section 1.3 well-behaved bit-size guarantee and Theorem 1.3.1 confirm polynomial input/output bit complexity when the total variable count is fixed, including polynomially growing degree. Root also read Hochbaum–Naor Section 2: its envelope/elimination methods are correctly described as antecedents, without assuming that its feasible-cell restriction preserves the full endpoint relation.

Root inspected the newly added Cslovjecsek et al. primary manuscript introduction and Theorem 1. Its fixed linear block LP and linking-row algorithm is distinguished accurately from global variation of the nonlinear core. The stage-4 initial build completed at 54 pages with no final LaTeX/BibTeX warnings or over/underfull boxes. Accepted sections 01–03 retain their hashes. PDF page 47, including the planar composition statement and envelope argument, was visually inspected and is legible without layout defects.
