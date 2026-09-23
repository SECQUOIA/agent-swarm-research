# Stage 3 independent review 3

Scope: `sections/03-approximation.tex`, especially Lemma
`lem:spectral-normalization` and Theorem `thm:matroid-spectral-set`, and
`appendices/approximation.tex`, especially `app:matroid-proof`. I also read
the entire approximation section and scalar-predecessor appendix for broader
consistency. Missing later certification, computation, and integration stages
are outside this review. I did not read other reviewer reports or change the
manuscript.

## Verdict

**No MAJOR findings. No MINOR corrections identified.** The represented-matroid
theorem and shared normalization are mathematically sound within their stated
rational-representation, fixed-information-dimension scope. I recommend
acceptance of this part of Stage 3.

## Main mathematical checks

1. **Normalization and ranges.** Rational LDL factors remain labeled by their
   original owners. The maximum-volume argument applies to weighted factor
   vectors only in the existence proof; the implemented trials use rational
   labels and dyadic scaling. Cramer's replacement argument bounds every
   selected factor coordinate by one before scaling. At most `p` factors per
   atom then justify the `4p` diagonal filter. The projector tests and
   rectangular reconstruction preserve an oblique singular range exactly.
   Keeping all distinct owners of the selected factor basis supplies the
   identity lower bound, including multiple factors with one owner and labels
   belonging to the common prior. No unjustified square-root computation or
   minimum-eigenvalue promise enters the algorithm.

2. **Restriction and contraction.** The appendix correctly rejects dependent
   forced owners and restrictions whose column rank falls below the original
   `q`. Extending forced columns first to a retained original base, applying
   the inverse basis matrix, and deleting the first forced directions gives
   the represented contraction. Thus all lifted outputs are actual original
   bases. The `q'=0` case returns exactly the forced base. A target base's
   surviving normalization trial passes every feasibility filter.

3. **Signed profiles and positive coefficients.** The shift by
   `ceil(4p/h)` covers negative floor labels, and the fixed optional cardinality
   makes the shift reversible. Cauchy--Binet gives positive squared-minor
   coefficients over the rationals, so coefficient support equals profile
   attainability. The manuscript correctly warns that reduction modulo one
   prime cannot replace the exact zero test.

4. **Interpolation and growing matroid rank.** The degree bound
   `2q' ceil(4p/h)` is polynomial in `q` and `1/eta`. The tensor grid has
   polynomial size for fixed `p`, whose upper-triangular coordinate count is
   fixed. Grid evaluations, determinants of growing order, Vandermonde
   inversion, and denominator clearing all have polynomial bit complexity;
   no fixed-matroid-rank assumption is hidden in this reasoning. Repeating a
   polynomial interpolation per deletion and per positive profile is large
   but remains polynomial.

5. **Witness recovery.** Retaining the original row count during deletion
   tests is essential and is explicitly required. A failed deletion remains
   infeasible after subsequent deletions. Any extra surviving element outside
   one target-profile base could therefore have been deleted, proving the
   final surviving set is a base. Equal optional profiles cancel the exact
   common forced/prior sum; entry error less than `q'h` gives the claimed
   spectral error, and the normalization floor converts it to a relative
   sandwich. Rank-zero information receives a separate correct treatment.

6. **Scope and consequences.** The common-kernel requirement justifies
   contrast pseudoinverse comparisons and prevents falsely covering different
   singular ranges. The stated D, E, and A consequences follow with their
   different homogeneity/inverse factors. The true-memory sandwich composition
   has the correct orientation. The appendix's cancellation, finite-field,
   and unattainable integer-profile examples are exact. The text does not
   extend the additive matroid theorem to arbitrary correlated histories,
   independence-oracle inputs, or intersections. It describes a polynomial
   approximation theorem rather than a practical runtime improvement.

## Independent exact computation

New standalone script:
`verification/stage03-review3/check.py`; results:
`verification/stage03-review3/results.json`. It imports no archived author or
review helper, and changes no historical output.

- Three integer/rational representations of ranks 2, 3, and 4: enumerate all
  29 actual bases; match 18 exact profile coefficients computed independently
  by exhaustive squared minors, symbolic determinants, and tensor-grid
  interpolation.
- Perform 103 coefficient-based deletion tests and verify every recovered
  witness is an original base with its prescribed profile.
- For every fixture base and every prefix size of its forced set, check
  represented contraction against every candidate completion, including the
  empty optional base.
- Six normalizations of oblique rank-two PSD information embedded in dimension
  three, with a common prior, multiple factors per owner, signed coordinates,
  and dyadic scales spanning large bit ranges: verify range filters,
  reconstruction, atom diagonal bounds, forced-owner inclusion, and exact
  positive-semidefinite identity floors.
- Verify mixed-minor cancellation, the determinant `-2` finite-field witness,
  and an explicit rank-drop example where retaining the original rows gives
  the zero profile polynomial while incorrectly shrinking the row basis gives
  a positive coefficient.

Command completed successfully:

```
code/research_20260912/.venv/bin/python paper-correlated-measurements/verification/stage03-review3/check.py
```

These are finite exact proof checks, not performance benchmarks or a substitute
for the general proofs.

## Primary-source check

Read `literature/AGENTS.md` first. Independently opened the primary Berstein et
al. author report at
<https://optimization-online.org/wp-content/uploads/2007/07/1725.pdf>.
Theorem 1.3 and Proposition 4.2/Lemmas 4.3--4.4 support the existing exact
profile, squared-minor, and interpolation machinery; Theorem 1.1 has the
fixed-distinct-weight assumption described in the appendix. The manuscript
properly credits these algorithms and identifies its tensor interpolation as
an equivalent implementation.

Also inspected the available publisher PDF extraction of Brown--Laddha--Singh
2024, especially Theorems 2--3 and their general-matroid discussion. The
manuscript accurately distinguishes their randomized fixed-dimensional PTAS
and broader oracle model from its rationally represented deterministic
accuracy dependence. The qualified combined-cover novelty statement does
not claim invention of normalization, profile interpolation, or general
matrix-objective approximation.
