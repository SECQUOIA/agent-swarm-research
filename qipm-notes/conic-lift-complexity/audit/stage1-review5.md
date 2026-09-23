# Stage 1 independent referee report 5

## Verdict

**No major mathematical issue found.** The Stage 1 claims survive my independent reconstruction and edge-case checks. In particular, I find no counterexample to the certificate-fiber minimax theorem, its dense-open quantifier, or its exceptional-cone construction. This verdict concerns the current foundations, curvature results, and certificate-rank theorem; it does not certify the later barrier claims or the full eventual paper.

I read `main.tex`, `macros.tex`, both current section files, and `bibliography.bib`. I did not read other reviewers' reports. I inspected the existing compilation log without rebuilding shared outputs; it records a nine-page PDF and no undefined-reference, citation, or box warnings.

## Independent mathematical checks

1. **Whole-slice certificates.** Slater duality with the affine offset retained gives `M*lambda-T*v` and `b.lambda=1-t.v`, exactly the identity used in the manuscript. Compactness is needed for the output body, not the lifted feasible set. The free-variable elimination argument correctly kills an output direction by a feasible line. Minimal-face reduction avoids silently assuming ambient dual attainment.
2. **Universal mixed rank.** The relevant restricted pairing has domain `b-perp` and annihilator `span(a)`, giving dimension `m-2`. At a pointed-cone vertex, a two-sided derivative is zero. Dimension-two factors therefore cannot contribute, and rays are correctly harmless.
3. **Jordan mixed rank.** Two-sided positivity eliminates the entire kernel Peirce subalgebra in each derivative. The only common components are the `I x J` cross spaces. Differentiating Jordan complementarity gives the stated positive weights `mu_j/lambda_i`. No constant-rank hypothesis is hidden in this reasoning. The inner-derivation coefficient four in the local attainment paragraph is correct.
4. **Generic minimum rank.** The rank-minimizing fibers are semialgebraic, and a selected certificate need only be differentiable on the common full-dimensional locus. At each such support its minimum rank lower bound transfers to every certificate in that fiber. This justifies the strong order of quantifiers; it does not mistakenly interchange a certificate selector with the entire fiber. The lower-dimensional exceptional set is surface-null.
5. **Perspective construction.** I recomputed `P(w)c=w^2-(||w||^2/2)c`, its trace, and the rank-one conclusion from approximation by invertible quadratic representations. The resulting two-idempotent subalgebra proves the determinant formula independently of associativity. The factors `sqrt(2)` in the primal embedding and `1/sqrt(2)` in the dual completion are consistent with the trace norm. Thus the Albert case is supported by the actual proof rather than a matrix analogy.
6. **Fiber coefficients and degeneracies.** The common tail trace is `(1-eta)/2`, the head coefficients sum to `(1+eta)/2`, and these equations still hold when there is only one group. Non-full half-Peirce coordinate groups leave additional certificates, but positive tail trace forces every block nonzero, which is all the lower argument needs. Zero groups, the south pole, the north pole, and `q=1` all behave as claimed. The separate interval construction has the necessary rank-two reduced face and valid rank-one support certificates.
7. **Dimension resources.** The norm tree has exactly `s` leaves, `k` non-ray factors, and ambient dimension `s-1+2k`. Decomposing a reducible symmetric factor preserves total rank and never violates the dimension cap. Thus the stated ambient-rank lower bound follows even if the original factors are reducible. It is correctly distinguished from restricted barrier complexity.

## Minor issues and proposed remedies

### R5-1 — Minor: attribution of the Lorentz norm-tree construction

**Location:** `sections/01-foundations.tex`, Corollary `cor:dimension-resources` and its proof; relationship-to-earlier-work subsection.

**Justification:** The new exact lower bounds and simultaneous resource accounting should be distinguished explicitly from the established representation of a higher-dimensional Lorentz cone using a tree of lower-dimensional Lorentz cones. The construction is currently presented without an attribution. This is not an incorrect theorem or a demonstrated novelty conflict, but adding the attribution would make the careful novelty policy visible at the point where the familiar construction enters.

**Evidence:** Fawzi's published article *On representing the positive semidefinite cone using the second-order cone* expressly states that higher-dimensional second-order cones admit representations using three-dimensional cones and refers to an earlier source, Section 2. Publisher record: https://doi.org/10.1007/s10107-018-1233-0 . The paper's reference should be followed to the original construction, or an appropriate standard SOCP reference already in the local literature can be checked.

**Remedy:** Add one sentence and an appropriate primary citation crediting the standard recursive norm representation; reserve originality for the lower bounds and their exact resource match. Do not claim this search establishes priority for every variable-arity resource formula.

### R5-2 — Minor: state definability of the contact data explicitly

**Location:** `sections/01-foundations.tex`, Lemma `lem:selection`, especially the phrase “a smooth primal--polar contact map,” and the beginning of the curvature argument.

**Justification:** The proof uses cell decomposition of the composed maps, so its immediate hypothesis is definability of those maps. In the actual application this follows: the body is a projection of the definable lift, and the normalized normal on a definable `C^2` boundary patch is definable. A reader should not need to infer this restriction from the final sentence of the proof or interpret the lemma as covering arbitrary additional smooth contact data.

**Remedy:** Say “the normalized normal contact map on a definable `C^2` boundary patch” (or explicitly require a definable smooth contact map), and note that definable local coordinates may be chosen. This is a clarification of the proof's already valid application, not a change to either headline theorem.

## Literature and scope assessment

The current novelty sentence is appropriately qualified and names a precise invariant rather than claiming novelty for slack factorization or Jordan machinery. My targeted search did not identify an earlier support-fiber minimax formula. That search is not an exhaustive priority certification. The final synthesis should preserve the distinction between original sharp bounds, classical norm-tree/Schur-type constructions, and standard algebraic background. The eventual complete paper still needs the later-stage results and the corresponding expanded literature review; their absence is not a defect in this bounded Stage 1 delivery.
