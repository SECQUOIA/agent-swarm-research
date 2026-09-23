# R1 independent review — reviewer 1

## Verdict

**No major issues and no valid minor issues identified.** The revised framing is clearer and preserves the mathematical guarantees, explicit assumptions, empirical distinctions, and restrained novelty claims. No correction is requested for R1.

I reviewed the current abstract, introduction, and discussion; read `PLAN.md` and `r1-author.md`; and checked relevant unchanged theorem, implementation, formalization, experimental, and table context. I did not read other R1 reviews, delegate, modify manuscript sources, or rerun unchanged tests, formal builds, numerical generation, or bulk replay. Updating the source archive belongs to R2 and is not an R1 defect.

## Findings from scrutiny

- **Research problem and guarantee.** The abstract and first introduction paragraphs now identify the two missing links between an exact MILP proof and a nonlinear bound before presenting the implementation. The objective-preserving feasible-set inclusion stated in the discussion is the actual mechanism proved in Section 3. The bound is conditional on satisfying the mathematical contracts and concerns the exact interpreted loaded model. Independence from numerical subproblem accuracy therefore means that numerical output is proposed evidence; it does not remove the support, enclosure, master-identity, or executable-correctness obligations.
- **Scope and assumptions.** The opening does not imply arbitrary convex-model admission or universal certificate existence. The introduction explicitly distinguishes the conditional validity theorem from completeness and states that neither Slater regularity nor attainment is needed for the transfer implication. Supported expressions, nonlinear equalities, nonconvex models, source-model interpretation, and the need for an original-model primal witness remain addressed. The abstract and contribution list explicitly preserve the limited Lean/software trust boundary.
- **Scientific contribution.** The early method/findings/validation/artifacts separation helps readers identify what the work contributes. The method is described as a concrete integration of established support and discrete-proof principles. The rewrite does not promote the 161 tests, selected Lean implications, 222-model collection, or absence of a Slater assumption into a new general optimization theorem. It does not claim first-system priority, general certificate-size superiority, or solver-performance superiority.
- **Prior work.** The comparison with Halbig retains the material distinction between solving continuous convex plane checks and recomputing rigorous enclosures at supplied support points before replaying a saved rational proof. Baes's certificate-point count remains qualified by the respective theorem hypotheses and separated from bit length. Established rigorous-bounding, exact MILP, and verified-software precedents retain their attribution. The shortened QIBEX-R passage is a description of the cited approach, not an independent validation of its interval implementation.
- **Empirical support.** The 203/289 abstract and introduction claim agrees with the uniform-artifact replay table and retains the separation from generation outcomes. The three externally accepted completed proofs agree with the saved exact audit summary: two incompatible-direction linear combinations and one integer disjunction with a gap of two. The discussion expressly distinguishes invalid supplied inferences from false final bounds, conservative sufficient-test failures from refutations, and solver-point infeasibility from objective discrepancies. The two exact optimality completions are the quadratic example and `clay0204m`, both supported in the unchanged experimental section.
- **Clarity and synthesis.** The abstract now follows problem, method, guarantee, evidence, and significance. The introduction states the result before the literature review and gives useful boundaries without repetitive priority disclaimers. The conclusion develops scientific lessons about consistent model interpretation, classification of failures, primal evidence, and representation costs; it does not merely repeat cohort chronology. Its claims are consistent with the retained limits on admission, proof size, live-row memory, shared-machine timing, and formal coverage.

## Compact checks

The three reviewed source hashes match the R1 author report:

- `main.tex`: `13f1381f1434aa843f79336f7960815b8e5b97b335ece14607d13bc7ee81fd49`.
- `sections/01-introduction.tex`: `4a3f4e07636d0c582dce7aefacea71657b507f40873a175b575a3c9f9c3f86ee`.
- `sections/07-discussion.tex`: `67332af75f4212c53b243858b824b81d130134cabf5435eae562618e15e17134`.

The saved R1 LaTeX log contains no warning, undefined-reference/citation, or overfull/underfull-box diagnostic. No substantive mathematical or experimental change was found that would justify repeating earlier executable or formal verification.
