# Stage 1 independent review 5

Reviewed the current introduction, model section, bibliography, both evidence maps, and current author report on 2026-09-13. I also checked the local Halbig full text around the certificate definition and Section 4.3, the checker source's domain/curvature organization, and current primary records for Coey et al., Szeider, and Borst et al. This review concerns Stage 1, not the still unwritten proofs and experiments.

## Verdict

**No major issues found in Stage 1.** The mathematical contract is coherent and substantially clearer than a generic claim of certified MINLP. In particular, the treatment of infima, empty feasible sets, epigraph extensions, objective constants, conservative box domains, support at boundary points, and primal witnesses is correct. The exact binary64 coefficient example is mathematically correct. The text distinguishes certificate soundness from certificate existence and distinguishes replay from formal verification. These distinctions prevent the main foreseeable overclaims.

The contribution has credible scope as a methods/software and reliability paper. The closest prior convex-MINLP certificate work appears prominently, and the description of its continuous plane-checking and discrete integer-freeness obligations agrees with the inspected source. The contribution description does not need a priority sentence. Publication strength will depend on the detailed evidence promised in later stages; absence of that future content is not a current-stage defect.

## Valid minor corrections

1. **Minor — ambiguous use of “complete” for a proof language.** At `sections/01-introduction.tex:33`, “a restricted complete VIPR language” can be read as a logical completeness assertion for the admitted proof system. The intended point appears to be complete consumption and checking of each accepted derivation, rather than support for all VIPR syntax or a proof-system completeness theorem. Replace with, for example, “a separate, unmechanized checker that replays complete derivations in a restricted subset of VIPR.” This preserves the intended substantive claim without suggesting an unproved one. The inventory uses similar shorthand and should be made consistent where practical.

2. **Minor — incomplete established journal metadata.** The Coey et al. entry at `references.bib:124` lacks volume and page numbers even though the final journal record is available. Add volume `12` and pages `249--293` (and issue `2` if following the issue-number convention elsewhere). The [publisher record](https://link.springer.com/article/10.1007/s12532-020-00178-3) confirms volume 12 and pages 249–293. This is a bibliographic completeness correction, not a problem with the literature comparison. The current Borst preprint citation remains supported by the authors' publication listing; I found no reason to require a different publication status. Szeider's [publisher record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2026.52) agrees with the supplied citation.

## Future-stage obligations, not Stage 1 defects

- The formal safe-cut section must prove the finite-box and one-sided/free-coordinate rules under exactly the stated support conditions, and the implementation section must explain how its accepted derivatives meet those conditions.
- The complete manuscript must give operational definitions of accepted, rejected, and missing historical attempts and identify the 299-to-289 cohort selection. The introduction's arithmetic is consistent: 188 + 92 + 9 = 289.
- “Reproducible reliability study” ultimately requires an accessible supplement or sufficient reproducible procedure; internal paths and hashes alone do not provide artifact access. The inventory already recognizes this obligation.
- The exact loaded-tree interpretation must remain visible in experimental comparisons and primal case studies. The present section correctly prevents an unqualified claim of equivalence to a source decimal model.
- Any later Lean claim needs to replace the introduction's conditional wording with the actual coverage, while retaining the executable-checker trust distinction.

I made no manuscript or code changes and did not rerun the full proof campaign. No finding from this review invalidates the topic or requires repeating a five-reviewer cycle for mathematical repairs.
