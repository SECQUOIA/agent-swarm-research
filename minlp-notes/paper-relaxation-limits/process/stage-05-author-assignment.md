# Stage 5 author assignment (after Stage 4 is accepted)

Write all Stage 5 rows of scope-proposal.md with full fresh proofs and primary-source attribution. Read the complete three canonical sources and corrections, accepted oracle conventions and Stage 4's escape-cut discussion. One author owns this stage; 15 independent full-stage reviewers follow. Preserve earlier mathematics.

- State the general signed 3XOR transfer with three distinct coordinates per clause, repeated clauses permitted, m>0 and occurrence Delta, normalized objective, r>=2, original pseudo-degree 4r, and exact quadratic moment realization. The node hull is the hull of the full coordinate domain, not of the constrained feasible graph. Its quadratic inequalities enter linearly on moments; their arbitrary products/localizers are not granted.
- Prove deterministic substitution followed by marginalization, not conditioning, all repeated bound-slack preordering terms, affected-clause costs in [0,1], exact quadratic realization in the node and the 2^(mT_*/Delta) witness-cover count. Include arbitrary coordinate sets, every local univariate valid polynomial and equality through degree, and sensitivity/Hessian bounds.
- Prove the signed {0,+1,-1} moment realization lemma including the constant Gram vector's class. Then directly verify the Schoenebeck full original, Theorem11/12 and Lemma13, signed-character construction and width/degree convention. The original width w supplies moments through w and positivity of squares through floor(w/2); require 4r<=w, later 4rD<=w. Cite the construction as classical. Source files and root's direct visual/source audit are recorded in verification/primary-source-checks.md. At density8 use delta=gamma=1/4 and epsilon=0; avoid the source formula's gamma=1/2 boundary denominator. Root did not equate a source typographical v_empty norm-zero line with the intended normalized construction.
- Give the full elementary density8 random-sign union bound, occurrence>64 deletion estimate 48 exp(24)/2^64<1/8, intersection of events, retained7n<=m<=8n, OPT>=1/8 and all-sufficiently-large-n quantifier. State the original linear-order regime and absolute1/16/relative1/2 exponent7n/1024.
- Bounded monomial lifts include all original coordinates, signed nonempty supports of size<=D, arbitrary repeated/overlapping supports and arbitrarily many auxiliaries. Require exact polynomial pullback of the available-degree objective, all available graph identities, original pseudo-degree4rD and all signed character moments. Prove the lifted preordering and the actual quadratic moment distribution, explicitly allowing the latter to leave the graph. Prove parity-rank counting: a support union is contained in a basis-row union, so |C|<=D rank, giving 2^(mT_*/(Delta D)). The simple count of restricted lifted coordinates would be insufficient.
- Treat arbitrary lifted coordinate sets, including nonclosed sets, using endpoint-supported distributions. Prove the pair-plus-clause factorable formulation, linear objective,2m quadratic equalities,N=n+2m<=17n, exponent7n/3072 and order regime. Show the degree-three identity transferring the Bernstein upper certificate to the linear objective. At r=2, ceil(3/epsilon)^n regions suffice, giving48^n at the fixed tolerance. Distinguish original dimension n from arbitrary lifted dimension N.
- State the D-versus-region tradeoff only within4rD<=an. Polynomial region count requires D=Omega(n/log n) there. Do not extend Stage4's coordinatewise endpoint interpolation result to these multivariable auxiliaries without a new proof.
- Give both affine-branching obstructions from the canonical note: a balanced halfspace rejects the preserved first/second moments of an actual uniform distribution while retaining at least half the witnesses; order r forces at least min(r-1,ceil(n/2)) deterministic substitutions in that construction. The example is a method obstruction, not a short affine certificate for the constant-gap XOR objective. Explain why short refutations of perfect satisfiability yield only normalized1/m rather than1/16.
- Check relevant primary literature on disjunctive SOS and Stabbing Planes/branch-and-cut; distinguish continuous subdivisions from integer-negation disjunctions. Limit comparisons to source statements actually inspected. Keep no-priority-guarantee access records in the process documentation, not repetitive agent-history disclaimers in the manuscript.

Supply process/stage-05-author.md with source-to-label coverage, proof/source checks, finite symbolic verification where meaningful, and clean build evidence. Do not use prior internal PASS labels as proof. No edits to snapshots/literature/other paper folders. Do not return until the whole stage is written and compilable.

## New bounded candidate to check before fixing the stage hypotheses

Read `process/order-one-monomial-refinement.md`. Root found that the
lifted transfer may require only r>=1 and rD>=2; the unlifted cubic
objective still requires r>=2. For the pair-plus-clause D=3 formulation
this would strengthen the lower bound to lifted order one. A separate
full-quadratic-box-moment argument also gives the48^n upper certificate
at order one. Verify both proofs independently. If valid, develop them
fully and adjust the earlier blanket r>=2 instruction for the lifted
theorem only. Retain the canonical order-two Bernstein proof as a
distinct developed certificate. Record the new hypotheses, constants,
source-width requirement and this completed candidate in your ledger.
All15reviewers must scrutinize the refinement; do not promote it solely
because root proposed it.
