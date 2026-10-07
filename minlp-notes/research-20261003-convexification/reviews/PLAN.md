# Independent correctness review

This review covers the new implementation in this directory. The earlier
campaign and its frozen source remain unchanged. Review is internal agent
review, not external peer review or formal verification.

The review has four separate responsibilities:

1. Bind every admitted native model to the original expression trees,
   including domain conditions justified by original affine constraints.
2. Check exact quadratic support and the stated finite separation contract
   against independently derived analytic examples and adversarial domains.
3. Reconstruct each saved aggregate cut from original row sides and the
   support certificate, then verify its exact elimination, binary64 rounding
   correction, and actual inserted SCIP row.
4. Reconcile the final frozen experiment records with the verified source,
   preserve refusals and unknown logs, and distinguish cut validity from
   numerical solver bounds and performance evidence.

Implementation authors supply their own tests. Review tests must add distinct
confidence: exact known optima, preserved source-domain restrictions, boundary
cases, altered certificate fields, and independently reconstructed bindings.
Producer/checker agreement alone does not establish the underlying theorem.

The main experiment must wait until supported source semantics and cut
conversion pass review. Only topic-specific commands are run; CI and
project-wide verification remain outside this local work.
