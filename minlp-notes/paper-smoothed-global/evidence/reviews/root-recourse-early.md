# Root review of the first continuous-recourse section

Snapshot: first `sections/07-recourse.tex`, read 2026-10-05 before its proof
appendix and the complete manuscript existed. No experiments or literature
search were performed.

1. **Mathematical edge case.** The stated k=0 certified search queries with
   accuracy 4^{-j}, but defines E_j=kLh_j^2/8=0 and epsilon_j=2E_j=0.
   Proposition `prop:rec:search` then falsely promises U_j=f* for every
   admissible nonzero-width oracle answer. Give the empty-core case its own
   positive accuracy allowance (and propagate it through the proposition
   and stopping schedule), or separate it before stating the k>=1 search.
   The exact empty-core case is a direct recourse call. This is a local
   repair, not an obstruction to the positive-core theorem.
2. **Output clarity.** The summary table should explicitly say that quadratic
   fallback returns rational output too. Its current blanket phrase
   "every result returns an algebraic output" is unnecessarily ambiguous.
   Degree-one algebraic representations exist, but that obscures the stronger
   every-draw rational theorem.
3. **Input accounting.** A supplied curvature certificate's encoding belongs
   in I; its verification cost is charged to runtime, not to I itself.
4. **Convexity certificate.** An objective being a sum of squares does not
   prove its residual convexity. Specify a sum-of-squares certificate for the
   residual Hessian (or for the polynomial y^T H_RR(x)y), rather than an
   unspecified "explicit sum of squares". Sums of even powers of affine
   functions do supply the stated structural certificate.
5. **General oracle scope.** The k=0 case of the general certified-recourse
   theorem need not be convex. A certified global oracle is an assumption;
   convexity is a sufficient specialization. Qualify the following sentence
   accordingly: "For k=0 the problem is a convex polynomial on a box."

The exclusion certificate correctly uses global lower values, omits slabs at
clipped original bounds, and applies a full-width Lipschitz allowance. The
star example clearly explains why grid recourse cannot use a local rounding
budget. The model and count condition on residual noise before using core
independence.
