# Independent mathematical review: extinction under daughter dependence

Date: 2026-09-06. Reviewer: independently assigned proof agent. Reviewed `research/results/extinction-coupling.md` before the near-critical extension was added.

## Verdict and scope

The stated lower and upper bounds and stationary attainment proofs are correct under the stated finite-type, independently specified coupling sets. The lower-envelope theorem is an application of classical branching decision process reasoning; it should not be advertised as a new general fixed-point theorem. The rearrangement formula is also classical and is verified below without an external theorem. No counterexample to the stated claims was found.

The upper bound uses a special property that really is present here: the diagonal coupling maximizes the generating function at every vector. The warning about general upper Bellman envelopes is appropriate. Choosing a maximizing action at an upper-envelope fixed point only produces a fixed point of its generating function; it does not establish that it is the least fixed point.

## Detailed checks

1. Nonnegative coefficients make every generating function monotone on the cube. Taking an infimum preserves monotonicity. The compact feasible sets give attained minima, and uniform Lipschitz continuity gives continuity of the minimum map. Thus the monotone limits are fixed points and are the least fixed points.
2. Equal row and column marginals suffice for the identity involving squared differences. Symmetry is stronger than needed for that identity, but is natural for an exchangeable pair of daughters.
3. Selecting a minimizer at the lower-envelope fixed point is valid: least-fixed-point minimality gives one inequality and the already established universal comparison gives the other. The selected family works simultaneously for all starting types.
4. A single stationary coupling family is essential in the model interpretation, and the proof actually delivers one. It does not merely optimize separately for different initial types or generations.
5. The mean matrix and continuous-time expectation equation use consistent parent-row/child-column conventions. Positive finite rates on finitely many types give bounded individual rates and binary events, so explosion is excluded by domination by a linear-rate pure-birth process.
6. The lineage identifiability statement is correct for uniformly selected daughters, including death observations. Selection conditioned on future survival or other daughter attributes would be a different observation scheme.
7. Reducibility, zero death probabilities, and criticality do not invalidate Theorem 1. They do matter for expansions or spectral sensitivity arguments. Such extensions must state extra assumptions separately.

## Self-contained verification of the quantile formula

Fix a marginal probability vector p and values z_j in [0,1]. Let X and Y have this same scalar distribution. For any joint law and any s,t in [0,1], the elementary intersection bound gives

\[
 \Pr(X>s,Y>t)\geq
 \max\{0,\Pr(X>s)+\Pr(Y>t)-1\}.
\]

By the layer-cake identity and Tonelli's theorem,

\[
 E[XY]=\int_0^1\!\int_0^1\Pr(X>s,Y>t)\,ds\,dt.
\]

Let U be uniform on (0,1), set X=Q(U), Y=Q(1-U), and use the generalized increasing quantile Q. Apart from endpoints of measure zero, the two exceedance events are an upper interval in U and a lower interval in U. Their intersection has length exactly the lower bound above. This construction therefore minimizes E[XY] over all scalar couplings, and its value is

\[
 \int_0^1Q(u)Q(1-u)\,du.
\]

It remains to check feasibility as a *type* coupling, including ties. Sort the types in any order compatible with z, partition (0,1) into consecutive intervals I_j of lengths p_j, and define

\[
 C_{jk}=\operatorname{Leb}\{u:u\in I_j,\ 1-u\in I_k\}.
\]

The row and column sums are p, reflection gives C_{jk}=C_{kj}, and z_j on I_j is a quantile version. Hence this symmetric type coupling realizes the scalar minimum. Zero masses, tied values, and interval endpoints cause no problem. Reversing the full type order leaves the resulting antithetic matrix unchanged, because it reflects every interval.

## Follow-on result

The uniform near-critical expansion and exact optimal-coupling stability theorem are developed, with a full proof, in [extinction-near-critical.md](../results/extinction-near-critical.md). Those are derived here rather than independently reviewed here: they require a separate reviewer before being marked independently verified. Their novelty remains unresolved. In particular, the ordinary near-critical survival coefficient is classical in character; any contribution must be framed around the dependence optimization and its consequences.
