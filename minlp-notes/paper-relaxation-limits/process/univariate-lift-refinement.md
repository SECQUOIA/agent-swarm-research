# Candidate development: no degree loss for coordinatewise graph lifts

Root derivation, 2026-09-05. **Not yet an accepted manuscript theorem.** Stage 4 author and all Stage 4 reviewers must verify it. This strengthens the conservative rD pullback bound in `results/spatial-bb-product-domain-exponential-lower-bound.md`, using the same Boolean endpoint construction. It does not concern auxiliaries depending on several original coordinates.

## Statement to verify

For each original coordinate x_i in [0,1], introduce any finite number of real-valued functions y_(i,j)=psi_(i,j)(x_i), with finite values on their domains. A node imposes arbitrary restrictions on each local graph block (x_i,y_i), and its exact preimage is a nonempty set S_i. The functions need not be polynomial for this construction. Let the degree-2r node oracle use normalization; the original demand equality and its allowed polynomial multiples; polynomial equalities valid on each restricted local graph and all their multiples through lifted degree 2r; and every product of local polynomial inequalities valid on these restricted graphs times a square, subject to total lifted degree at most 2r. The global square polynomial may couple all lifted blocks. Coupled valid inequalities using several original coordinates are not supplied for free.

Assume the lifted objective is a polynomial of degree at most 2r and equals the intended quadratic fractional-cardinality objective (or its stated linear perturbation) on the full graph. In particular this includes the original quadratic objective, and the linear sum of penalty auxiliaries y_i=x_i(1-x_i).

Then the existing product-domain lower bound holds with **order r, not rD**:

q_r=min{k-2r+2,z-2r+2,m(1/2-2 epsilon)}.

The same perturbation and fixed-relative-gap block consequences should follow with their original order parameters. Polynomial degree D, or number of coordinatewise auxiliary variables, does not enter this bound. The existing rD statement remains a valid weaker consequence, but literal polynomial substitution is unnecessarily expensive for this particular endpoint-supported construction.

## Proof

Take a witness w=1_H+p 1_M in the preimage product domain, and partition coordinates into R={i:0 or 1 is absent from S_i} and U=[n] minus R. Assume |R|<q_r. Use the existing degree-2r fractional-cardinality functional E_(s,t) on Boolean formal variables u_i for i in U. Its hypotheses are satisfied exactly as in the original product-domain proof. Coordinates in R are fixed to their actual witness values.

Define a substitution Phi on lifted coordinates as follows:

- For i in R, map x_i to w_i and each y_(i,j) to psi_(i,j)(w_i).
- For i in U, map x_i to u_i and y_(i,j) to psi_(i,j)(0)+(psi_(i,j)(1)-psi_(i,j)(0))u_i.

Every lifted variable is replaced by an affine or constant polynomial. Hence a polynomial of lifted degree j has image of original degree at most j. Define L[P]=E_(s,t)[Phi(P)] for deg P<=2r, using Boolean reduction. This is normalized.

The image of the demand equality is sum_(i in U)u_i-t. Images of its multiplier polynomials have degree at most 2r-1, so the existing cardinality identity proves all required equality products.

For a local polynomial inequality g_i valid on the restricted graph, Phi(g_i) is a nonnegative constant if i is in R. If i is in U, its values at u_i=0 and 1 are nonnegative, because both endpoint graph tuples lie in the restricted graph. Modulo u_i^2=u_i, it therefore equals c_0(1-u_i)+c_1 u_i with c_0,c_1>=0. Products of such inequalities reduce to nonnegative combinations of assignment indicators. After grouping factors for a coordinate and removing constants, the number of involved coordinates is no more than the sum of their original lifted degrees. For any allowed square multiplier P, deg Phi(P)<=deg P. Lemma B from the original higher-SOS proof consequently proves L[(product g_i)P^2]>=0 with the original order r. This includes polynomials P coupling all blocks and repeated local factors.

A local polynomial equality vanishing on the restricted graph has image zero at the chosen witness tuple (i in R), or at both endpoint tuples (i in U). Its Boolean reduction is zero. Multiplication by any allowed polynomial preserves that reduction and total degree remains at most 2r, so all required equality products vanish. More generally, any polynomial identity of the full graph through the available degree also vanishes under this substitution on the Boolean cube and is respected. This does not cover additional inequalities using the demand constraint.

At every Boolean assignment of u_U, Phi maps to an actual full-graph tuple with x_R=w_R and x_U=u_U. Therefore the image of the lifted objective and the original quadratic objective agree at every such Boolean point. Both have degree at most 2r; uniqueness of the multilinear representation on the Boolean cube shows their Boolean reductions agree. Thus L evaluates the objective exactly as in the existing proof: only middle witness coordinates in R contribute to the quadratic penalty. The objective estimate and endpoint-avoidance counting argument are unchanged, yielding the claimed lower bound.

The crucial distinction is that Phi is an endpoint interpolation used to construct a moment functional. It is **not** an identity between psi_i(x_i) and its chord at every continuous x_i. All actual graph equations are checked after Boolean reduction or deterministic evaluation, which is what the constructed functional uses.

## Review obligations and limits

Root finite check `verification/check_univariate_lift_refinement.py` passed 36 exact rational cases: orders1–3, power auxiliaries of degrees2,3,7,21, square-root auxiliaries with polynomial graph equality z_i^2=x_i, and zero, one or two middle coordinates fixed at1/16. It checked 2,880 demand-times-monomial identities and 5,760 localizer/square combinations, all available graph identities, and the original objective estimate. The square-root endpoint and fixed values were rational, so no floating-point arithmetic was used. These are finite checks of the endpoint interpolation and degree bookkeeping, not a proof of the universal theorem.

- Check the oracle's degree definition and every equality/localizer under Phi, especially nonpolynomial maps and arbitrary local restrictions.
- Require the objective's available lifted degree and exact graph agreement explicitly.
- Keep original coordinate x_i available so the original demand is still affine. Eliminating x_i through a nonlinear inverse is not covered.
- No arbitrary coupled cuts, auxiliary functions involving multiple original coordinates, or exact hull of the coupled feasible graph are granted.
- The resulting exponent uses original dimension. Arbitrarily many auxiliaries do not make it exponential in arbitrary lifted dimension.
- The transfer improves this existing proof; no independent literature-priority claim is made.

## Stage 4 author validation after resumption

The replacement sole author independently checked the complete candidate
and promoted it to manuscript `thm:local-graph-lift`, with the global
relative-block consequence in `thm:relative-cover`. This is author
validation pending the required 15-reviewer round, not coordinator stage
acceptance. Full details and source coverage are in `stage-04-author.md`.

The manuscript explicitly defines every auxiliary on all of [0,1] with
finite values, preserves original coordinates and affine balances, and
requires available lifted degree at most 2r and full-graph objective
agreement. It defines graph covers by exact preimages to avoid a false
compactness assumption for discontinuous auxiliary functions. The proof
checks all global equality multipliers, repeated local inequality
products with globally coupled squares, and the objective after Boolean
reduction. The relative consequence includes tensor positivity and does
not assume that the written lifted objective is block-separable.

The original 36 exact checks were replayed successfully. New supplemental
checks in `verification/check_stage04_author.py` include nine three-block
configurations through order three with discontinuous finite-valued
auxiliaries, 774 equality products, 360 localizer/square checks, and
coupled graph-identity objective representations. They support the degree
bookkeeping; the manuscript proofs establish the universal statements.
The literal rD proof remains as `prop:literal-lift`, a valid coarser
comparison. No separate literature-priority conclusion is asserted.

## Accepted 2026-09-06

Stage 4 round 1 completed with 15 independent PASS reports and no findings.
The coordinator read all reports and accepted the refinement and its relative
extension. See stage04-round01-adjudication.md.
