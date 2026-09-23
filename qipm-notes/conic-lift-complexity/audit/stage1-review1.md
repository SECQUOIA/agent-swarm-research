# Stage 1 independent review 1

Scope: `main.tex`, `macros.tex`, both current section files, `bibliography.bib`, and the source-map and literature ledgers. I did not read any other review or modify the manuscript. Primary emphasis was the support-fiber invariant, minimal-face reduction, generic selection, lower-bound quantifiers, and the complete attainment argument.

## Verdict

**No major issue found.** The full-fiber rank theorem and its selection-free lower bound are mathematically sound on the stated hypotheses. Three small statement/scope corrections below should be made before proceeding. These do not require weakening the body theorems.

## Minor issues

1. **Abstract's local bound omits the zero/ray exception.** `main.tex:12–14` says that a proper cone of dimension `m` supplies mixed curvature bounded by `m-2`. For a ray (`m=1`), the actual rank is zero, which is not bounded by `-1`. The body correctly states the nonzero complementary-contact hypothesis and uses `max{m-2,0}` in its universal resource bound. **Remedy:** use `max{m-2,0}` in the abstract or explicitly restrict its sentence to nonzero complementary contacts in dimensions at least two.

2. **Abstract's exact rank formula needs its hypotheses.** `main.tex:15–20` omits `s >= 2` and the requirement that the dictionary contain a non-ray factor (`B>0`). Its unqualified formula would be zero for the interval, although the paper correctly proves the value one; an all-ray dictionary makes the denominator zero and has no ball lifts in dimensions at least two. **Remedy:** insert “For `s>=2` and a fixed repeatable dictionary containing a non-ray simple symmetric cone ...”. The theorem already contains these hypotheses through its setup.

3. **Make the contact-map definability hypothesis explicit in the selection lemma.** `sections/01-foundations.tex:131–133` currently says “a smooth primal–polar contact map,” whereas its cell-decomposition proof uses a definable composition. The actual normalized normal map of the definable `C^2` boundary patch is definable, so every application in the paper is covered; nevertheless the lemma should name that map or say “the definable normalized normal map.” **Remedy:** specify a definable `C^2` boundary patch and its normalized outward-normal contact map in the lemma statement, matching `:153–154`. This avoids appearing to claim generic regularity for arbitrary nondefinable compositions.

## Independent mathematical checks

- Free-variable elimination is legitimate because any equality-preserving free direction at fixed cone coordinates would otherwise project a feasible line into the compact body. The minimal face of a relative-interior feasible point contains every feasible point; its span gives relative Slater feasibility. The normalization proof obtains a certificate identity on the entire affine slice, not just on feasible lifts.
- The rank invariant is defined after reduction, and the manuscript explicitly avoids claiming existence of positive ambient certificates for a failed-Slater presentation. Integer-valued minima and maxima exist without compact certificate fibers.
- Each minimum-rank stratum and its nonempty fiber is semialgebraic. Choice followed by a common finite `C^1` decomposition is enough: no smooth global selector and no prior uniform certificate-rank bound are assumed. Minimum-norm selection is used only for convex primal/ordinary certificate fibers, not for the nonconvex minimum-rank fiber.
- At generic contacts, the overlap of the two derivatives is exactly contained in the `I x J` Peirce spaces. Differentiating Jordan complementarity yields the positive Gram expression with coefficient `mu_j/lambda_i`; there is no missing constant-rank hypothesis. This proves the stated rank bound even with a common kernel.
- The inequality `a_i p_i q_i <= a_i(r_i-1)q_i` is used only when `q_i>0`; zero certificates and reduced rays are handled correctly. Choosing the pointwise minimum rank first therefore proves the bound for every certificate in the full fiber at all supports of one dense open set. The order “fixed lift, then generic support, then all certificates” is preserved.
- The Peirce-perspective proof does not assume associative octonionic matrix multiplication. `P(w)c` is positive of rank at most one; its trace is `||w||^2/2`, yielding the rank-two subalgebra calculation. The `sqrt(2)` normalization and the completion trace `||g||^2/(4A)` are consistent.
- In the attaining lift, coefficient comparison gives the same positive tail trace in every block away from the north pole. Thus every full-fiber certificate really has at least one rank unit in each block, even for zero coordinate groups and groups that are proper subspaces of the half-Peirce space. The displayed certificates attain this count. The north-pole exception and the essential-infimum formula are correct for `s>=2`.
- The norm-tree counts use `s` leaves and `s-1` total branching surplus, have the advertised dimensions, and are strictly feasible. Symmetric reducible factors can be split without changing total Jordan rank, so the total-rank comparison remains valid.
- The quantifier-reversal example legitimately rotates the projection while keeping the cone dictionary fixed. It does not contradict the fixed-lift generic lower bound.

## Literature and staging

The present related-work paragraph makes a qualified and precisely scoped priority claim and distinguishes existing slack factorization/Jordan tools from the certificate-fiber objective. The source map correctly marks later products, topology, barriers, and movement statements as unverified stage candidates. The present draft does not improperly promote them to theorems. Broader novelty assessment and complete bibliographic verification remain part of the scheduled final synthesis; this review establishes no exhaustive priority guarantee.
