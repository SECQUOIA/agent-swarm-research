# Stage 2 coordinator investigation

This record supports the sole stage author's work; it is not a substitute for the five independent post-draft reviews.

## Primary input retrieved

Downloaded the open BCT preprint from https://arxiv.org/pdf/1011.3058 to `sources/borgs-chayes-tetali-2012.pdf` and extracted searchable text. The published paper is *Tight bounds for mixing of the Swendsen–Wang algorithm at the Potts transition point* (2012). Exact metadata will be checked in the manuscript bibliography.

Relevant source facts read directly:

- Printed p.28, Lemma 6.3: the contour activity bound applies when the metastable excess free energy times contour diameter is sufficiently small.
- Printed pp.39–41, Appendix A: its working range includes temperatures on both sides of the transition; this is broader than the main lemma's displayed stable-side restriction.
- Equation (A.8) gives the finite-volume truncated pressure estimate.
- Lemma A.1(i) makes actual and truncated activities equal under the diameter condition.
- Equations (5.5)–(5.7) bound contour diameter and enclosed volume; torus diameter is at most L.

The modern treatment https://arxiv.org/html/1909.09298v3 confirms a positive ordered/disordered/tunneling decomposition, including the ordered multiplicity q. Neither source licenses identifying a conditioned bond count with the physical spin energy.

## Proposed proof routes sent to the author

1. Under Edwards–Sokal, occupied bond count B conditional on spins is Binomial(M,p), where M is the number of equal-spin nearest-neighbor pairs and the physical spin energy is -M. Conditional binomial noise B-pM has a uniform sub-Gaussian moment bound on scale sqrt(N). Conditioning on a positive-probability phase costs only its reciprocal probability. Hölder can therefore transfer a phase moment bound for B to one for M without a false conditional-derivative identity.
2. Truncated contour activities have summable first-derivative Lipschitz bounds because their cap is exponentially small in contour size while logarithmic derivatives of the finite positive partition ratios grow polynomially. This can make the truncated pressures locally Lipschitz and open a temperature window of width eta/L in which every torus activity is untruncated. The author proposes differentiating the actual finite-volume expansion twice in that window; this avoids assuming the min-truncated infinite-volume pressures are C2.
3. The strengthened two-scale theorem requires a nondegenerate fluctuation limit in only one phase. Consequently the older claim that added kinetics are essential to the mean-field reservoir exponent is unnecessarily restrictive. The author confirmed that pure spins admit the same iff threshold, with kinetics needed only for the two continuous Gaussian peaks and the analytic continuous benchmark.

These routes must be stated completely and independently reviewed before being treated as manuscript theorems.

## Numerical verification

Ran `python research/verification/check_potts_finite_bath.py`. Explicit enumeration through eight spins agreed with occupation aggregation to less than 4e-16. Two direct energy-density checks at N=12 agreed with the Gamma/Beta CDF TV calculation to about 1e-11 or better. This confirms the existing finite-system formulas, not the new short-range proof.
