# Coordinator checks: Stage 04

Date: 2026-09-07. Stage03 was accepted before author assignment. These checks concern the current generic-fold stage only; no later-stage text is being authored.

## Geometry and proof checks

Read the complete generic-fold source note and independent review. Independently checked the following points.

A finite cover of the compact zero set by product neighborhoods with a fixed sign of g_s at simple roots and a fixed sign of g_ss at folds bounds the root count: at most one root in each first type and at most two in each second type for a fixed parameter. On the compact zero set outside retained open fold neighborhoods, |g_s| has a positive lower bound. A uniform positive lower bound on integral g² follows by continuity and the exclusion of identically zero profiles; such a profile would contradict the finite multiple-zero set.

The fold coordinate can be derived directly. Solve g_s(z(c),c)=0, write g(s,c)-g(z(c),c)=(s-z(c))² a(s,c) by Taylor's integral remainder, and set x=(s-z(c))sqrt(|a(s,c)|). The coefficient a is bounded away from zero and is C² under g in C⁴, so the coordinate is a local C² diffeomorphism with bounded Jacobian. The critical center differs from the fold site by O(|c-c_j|); h'(c_j)=g_c(s_j,c_j) is nonzero. This supplies all comparisons without an unproved normal-form regularity assertion.

The lower certificate requires only one positively sampled fold and one branch. The branch parameter c=C(u) has derivative of order |u-s_j|, giving a probability weight comparable to r on a spatial shell of length r. The arbitrary-mass shell and whole-budget fold tests from Stage03 retain their powers under bounded coordinate changes. Geometric shells can be separated in both space and parameter, so neither budget nor probability is counted twice.

For upper bounds, alpha=max(0,(6q-4)/(q+4)) supplies a global floor of order a_R. This is essential to permit ordinary roots fixed at another fold's spatial site. The fold estimates alone are insufficient when a realization also has ordinary roots; their total contribution O(a_R^(-1/4)) must remain explicit. Its qth moment fits all three target orders. The inner quartic family has a uniform natural-endpoint gap because derivative energy forces a hypothetical zero-energy limit to be constant, and a nonzero polynomial potential then forces that constant to vanish. Rootless local pieces are bounded by the reciprocal potential. A finite number of interval pieces gives a finite q-dependent sum constant for every positive q.

## Primary literature boundary

Inspected the author's openly accessible version of Berry, Keating and Schomerus (2000), *Universal twinkling exponents for spectral fluctuations associated with mixed chaology*, Proceedings of the Royal Society A 456, 1659–1668, DOI 10.1098/rspa.2000.0580:

https://michaelberryphysics.wordpress.com/wp-content/uploads/2013/07/berry320.pdf

Pages 1659–1660 and Section3, especially equations (3.3)–(3.6), already describe moment selection through singularity strength and the volume of its unfolding parameter region. That general mechanism is prior art. The current theorem adds a shared spatial mobility budget and matching unrestricted lower/graded upper bounds, giving its particular optimized threshold and logarithm. It should not present bifurcation-dominated moment scaling itself as new. The full final novelty audit remains Stage07. The Lancaster author PDF search result was found, but the web open failed; the Berry author-hosted PDF above was successfully inspected.

## First complete source pass

Read the first complete Section04 before the author declared it finished. The unrestricted lower tests, global ordinary-root term, all three integrals, and same-budget physical ratio check. Reported author-cleanup items before freeze: missing backslashes in spacing commands that would silently render as letters, a multiple-label eqref requiring cref, and explicit definition of the central scaled parameter and Taylor coefficients without reusing the earlier b_j function. These are author self-audit corrections before the independent snapshot, not post-review changes. No mathematical gap was identified in this pass.

## Frozen-source verification

After author completion, froze snapshot da3db325e0812991ad97d79560c4c8aeb99b83d7260ade75d6172d61d3b4aaa6 and dispatched five reviewers. The source incorporates the pre-freeze notation corrections. Recomputed hashes after dispatch: unchanged. Visually inspected compiled page28, including upper-response bounds, harmonic scale, and the central Taylor/coercivity proof; no clipping or overflow. Final complete-PDF inspection remains required.
