# Bounded developments to verify during authoring

## A finite-dimensional coefficient-regularity corollary

This is a candidate synthesis for Stage 3, not yet an accepted manuscript theorem. It combines the existing coefficient-regularity argument in `notes/positive-box-rho-plus-two-proof.md` with the completed fixed-ambient balanced-orientation inequality in `notes/review-positive-box-balanced-orientation-closure.md`.

For ambient dimension N>=2, let beta_N be the reciprocal of the opposite-orientation probability of a uniformly chosen floor(N/2)-subset. For each local scope, restrict this same ambient law. The reviewed coefficient inequality is

    P_j - V_j <= beta_N (C_j - O_j) + (C_(j-1) - P_(j-1)).

For a discrete cardinality potential psi(k)=sum_j a_j binom(k,j), assume a_j>=0 and a_(j+1)<=L a_j for j>=2, with L>=0 and coefficients beyond the degree zero. Its multiaffine extension has upper, lower, independent, and orientation expectations C_psi,V_psi,P_psi,O_psi. Multiplication and summation give

    P_psi - V_psi <= beta_N (C_psi - O_psi) + L (C_psi - P_psi),

because independent deficiencies in orders zero and one vanish and all the others are nonnegative. Adding C_psi-P_psi yields

    C_psi - V_psi <= (L+1)(C_psi-P_psi) + beta_N(C_psi-O_psi).

One common mixture, with weights proportional to L+1 and beta_N, therefore gives factor L+1+beta_N for a sum of such entire local potentials with a common L. The full sum has a common upper extremizer because the nonnegative binomial expansions are supermodular. Each individual local potential has adjacent-cardinality lower attainment. These facts and the distinction between entire-factor gaps and expanded-monomial gaps must be proved or established by the preceding manuscript lemmas.

The algebra above strengthens the previously recorded L+3 by replacing 2 with beta_N. It does not determine the optimal gap constant. Stage 3 author and all stage reviewers must check its hypotheses and boundary conventions before promotion. This is a direct consequence of existing mechanisms, with no independent priority claim.

The coordinator's independent finite checker, `verification/check_cardinality_refinement.py`, passed 360 exact rational cases. It computes independent and orientation expectations directly from their distributions, including restrictions of a fixed ambient law, odd dimensions, deterministic coordinates, and L=0. It checks the proposed inequality on these cases; the universal coefficient argument remains the proof obligation.
