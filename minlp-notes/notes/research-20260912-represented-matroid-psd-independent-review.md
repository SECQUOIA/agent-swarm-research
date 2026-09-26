# Fresh independent review of the represented-matroid PSD approximation set

Date: 2026-09-12.

**The theorem and its stated design consequences pass fresh independent
mathematical review.** For fixed information dimension `p`, the
[candidate construction](research-20260912-represented-matroid-psd-approximation-set.md)
produces a polynomial-size set of actual bases of the supplied rationally
represented matroid. Every feasible information matrix has one representative
in the two-sided relative PSD sandwich, including singular matrices with
exactly the same kernel. The rank of the input matroid may grow. The running
time is polynomial in the supplied rational input length and `1/eta`.
No substantive theorem or algorithm correction was needed. During the
review, the author explicitly separated `q'=0` before the strict rounding
remainder bound; the algorithm already returned that case exactly. The
reviewer did not edit the author's source.

This is a correctness verdict. It does not establish priority, a useful
practical exponent, or a solver implementation. In particular, the exact
profile algorithm is established work of Berstein et al.; it must not be
presented as a new contribution. The candidate's unresolved priority and
representation qualifications remain necessary.

The review independently checked the following parts of the argument.

1. **The three ranks have distinct roles.** Redundant rows of the supplied
   representation may be removed once to leave a full-row-rank `q by m`
   rational matrix. Selecting independent rows preserves all column
   dependence relations. The information rank `r<=p` is unrelated to `q`.
   After filtering to `E'`, the test `rank(A_E')=q` is essential: a base
   of a restriction whose rank dropped is smaller than an original base.
   The same safeguard applies to the separate zero-information restriction.
   If `q=0`, returning the empty base is correct even when the prior is
   nonzero. An explicitly represented matroid always has a base, including
   a matroid consisting entirely of loops.

2. **Contraction forces the owners without changing the feasible family.**
   The selected nonprior factors have a set `F` of distinct owners, with
   `|F|<=r`. Testing `F subset E'` and independence of `A_F` is necessary.
   Since `E'` retains rank `q`, every independent `F` extends to a base in
   that restriction. The proposed basis matrix `D`, whose first columns
   are `A_F`, is therefore invertible. Multiplication by `D^(-1)` makes
   those columns the first coordinate vectors. Dropping their rows and
   columns realizes the quotient by `span(A_F)`, hence the contraction has
   exactly rank `q'=q-|F|`. Its bases lift precisely to the original bases
   contained in `E'` and containing `F`. Clearing denominators by a common
   nonzero factor preserves these dependence relations. When `q'=0`, the
   only possible lifted base is `F`; the stated special case is correct.

   There is no requirement that different selected factors have different
   owners. An element matrix includes each of its factors once when its
   owner is selected; forcing one owner therefore includes all its selected
   factors. Prior factors are already included. As an independent check,
   append one integer coordinate marking membership in `F` and retain
   original-base profiles with count `|F|`. Because a base is a set, that
   equality forces every owner. This alternative yields the same optional
   profile support as contraction. It even yields the same coefficients
   up to the common squared change-of-basis and denominator-clearing factor.

3. **Range normalization handles singular matrices exactly.** Rational PSD
   Schur elimination gives at most `p` positive weighted rational factors
   per summand, including singular summands. A PSD residual with zero
   diagonal is zero. The kernel of a sum of PSD matrices is the intersection
   of their kernels, so every factor of a target base and its prior lies
   in the target information range. These factors contain a basis of that
   range. Enumerating all independent label sets of size `r<=p` therefore
   enumerates a basis for every feasible range.

   For a selected rational factor matrix `V`, the stated `L` is a left
   inverse and `Pi=VL` is its orthogonal projector. The range test `Pi Q=Q`
   and symmetry give `Q Pi=Q` too. Thus `TK=I`, `KT=Pi`, and
   `K(TQT^T)K^T=Q` for every retained summand. The rectangular transform
   loses no information on the allowed range. The distinct selected
   factors, after dyadic normalization, contribute the diagonal matrix
   with entries `tau_i^2 w_i>=1`. Every accepted lifted base therefore
   has transformed information at least `I_r` and original range exactly
   `range(V)`. These conclusions do not require a positive definite prior.

4. **Each target has an accepted normalization trial.** Among the weighted
   factors of a target base and the prior, choose a maximum-volume basis.
   If another weighted factor has coordinate `x_i` in this basis, replacing
   its `i`th column changes the volume by `|x_i|`, proving `|x_i|<=1`.
   This argument applies in a proper subspace. The dyadic normalization
   scales each selected weighted column to magnitude in `[1,2)`, so every
   transformed factor coordinate has absolute value below 2. Each matrix
   has at most `p` factors and passes the diagonal threshold `4p`.
   The target base survives every range and magnitude filter. Its forced
   owners are a subset of that base and hence independent. The restriction
   still contains the whole target base and therefore retains rank `q`.
   Its optional part is a base of the contraction. The maximum-volume
   choice is an existence proof only; square roots need not be computed.

5. **Signed labels have exact support and controlled error.** For all
   retained matrices, PSD and the diagonal bound imply
   `|H_e,ij|<=4p`. Consequently

   ```text
   -ceil(4p/h) <= floor(H_e,ij/h) <= ceil(4p/h).
   ```

   The proposed common shift makes the labels nonnegative and bounds them
   by `2 Lmax`. Every optional base has exactly `q'` elements, so subtracting
   the common vector `q' Lmax 1` recovers its signed profile. Floor gives a
   remainder in `[0,h)` for negative entries as well as positive entries.
   For `q'>0`, two optional bases with the same signed profile have each
   summed-entry difference strictly below `q'h` in absolute value. The
   case `q'=0` is returned exactly before using this strict bound. The prior and forced
   contribution cancel exactly. Symmetry then gives the operator-norm
   bound `r q'h<=r qh=eta`. Together with `H(B)>=I_r`,

   ```text
   H(B_hat) >= H(B)-eta I_r >= (1-eta) H(B),
   H(B_hat) <= H(B)+eta I_r <= (1+eta) H(B).
   ```

   Congruence by `K` reconstructs both original matrices and proves the
   sandwich. Every zero-information base is covered by the separate
   rank-preserving zero-element restriction. There is no conditioning
   assumption hidden in the rounding error.

6. **The determinant test has no cancellation, and deletion recovers a
   base of the right size.** Cauchy–Binet expands
   `det(A_c diag(y^w_e) A_c^T)` as a sum of squared basis determinants
   times their profile monomials. Over the rationals, each basis contributes
   positively and different bases with the same profile add positively.
   A profile coefficient is positive exactly when that profile is feasible.
   All coordinate degrees are at most `Dmax=2 q' Lmax`.

   Starting from a feasible target coefficient, delete a column precisely
   when its removal preserves positivity of that coefficient. Keep the
   original `q'` rows. A rank-deficient remaining column set has identically
   zero determinant and cannot be accepted. A deletion infeasible earlier
   cannot become feasible after further deletions, since the feasible
   subsets only shrink. If the final set had a column outside one of its
   target-profile bases, deleting that column would preserve feasibility,
   a contradiction. Thus a single pass leaves exactly one actual
   `q'`-element base. Recomputing a smaller row rank during this process
   would break the argument; the candidate explicitly forbids it.

7. **The size and Turing bounds allow growing matroid rank.** There are at
   most `sum_(r=1)^p binom(M,r)` normalization trials and at most
   `(2 q' Lmax+1)^(r(r+1)/2)` profiles per accepted trial. These quantities
   are polynomial for fixed `p`, because `q<=m` and
   `Lmax=ceil(4prq/eta)`. The stated output bound conservatively replaces
   `q'` by `q` and allows one zero-information representative. Recovering
   each output adds at most `m` coefficient tests. Even recomputing all
   coefficients at each test remains polynomial.

   Rational row selection, the `q by q` change of basis, and denominator
   clearing have polynomial bit complexity even when `q` grows. A common
   denominator's bit length is bounded by the sum of the input denominator
   bit lengths; the same reasoning applies after exact rational elimination.
   Selected factor weights and dyadic scales also have polynomial bit
   length. Extreme numerical scales increase bit length without increasing
   the normalized label bound.

   The interpolation bound is a bit bound, not just an arithmetic-operation
   bound. At a product-grid point, a monomial has bit length
   `O(d Lmax log(Dmax+1))`. The evaluated matrix entries and their
   `q' by q'` determinant therefore have polynomial bit length. The tensor
   Vandermonde system has polynomial dimension and polynomial-bit entries;
   exact rational linear algebra solves it in polynomial bit complexity.
   Alternatively, the source's moment-curve substitution has the same
   required polynomial guarantee. An integer coefficient is a sum of
   squared minors with at most exponentially many terms, but its bit
   length remains polynomial by determinant bounds and the logarithm of
   the number of subsets. Floating-point zero tests and arbitrary
   finite-field reductions are not justified by this reasoning.

The design consequences are correct with the qualifications inherited from
the [reviewed DAG theorem](research-20260912-dag-psd-approximation-set.md).
For determinant, choosing `eta=epsilon/p` and applying Bernoulli's inequality
gives ratio `1-epsilon`; determinants of rational fixed-size matrices can
be compared exactly. For minimum eigenvalue, `eta=epsilon` gives the same
ratio, and fixed-degree algebraic-number comparison is polynomial in the
rational coefficient length. If every base has singular information, the
ordinary determinant and minimum-eigenvalue optima are zero.

For positive definite information, inversion reverses the sandwich and
gives inverse-trace cost at most `1/(1-eta)` times optimum. Substituting
`eta=epsilon/(1+epsilon)` gives `1+epsilon`. Assigning infinite cost to
singular matrices detects the case with no finite A-optimality cost;
it does not make an infinite-cost ratio numerically meaningful. Restricting
each target and its representative to their common range proves the
corresponding Moore–Penrose inverse bounds and preserves estimability of a
specified contrast. This avoids a false pseudoinverse order rule across
different ranges. Adding a common PSD prior or applying a common congruence
preserves the sandwich directly. A nonnegative Loewner-nondecreasing
criterion homogeneous of positive degree `a` inherits factor `(1-eta)^a`,
subject to its evaluation/comparison procedure. Concavity is unnecessary;
monotonicity without scaling control is insufficient.

Uniform matroids have explicit rational Vandermonde representations, with
entries of polynomial bit length even when their rank grows. Direct sums
give partition matroids, and oriented (signed) incidence matrices give
graphic matroids.
Thus the stated fixed-cardinality, partition-quota, and spanning-tree or
spanning-forest base subclasses are valid. These examples do not supply a
rational representation for an arbitrary oracle or finite-field matroid.
Nor does the theorem cover simultaneous path and matroid constraints.

The direct attribution to [Berstein, Lee, Maruri-Aguilar, Onn, Riccomagno,
Weismantel, and Wynn (2008)](https://optimization-online.org/wp-content/uploads/2007/07/1725.pdf)
was checked against the full preprint, locally available as
`/tmp/minlp-berstein-2008.txt`. Its Lemma 4.1 shifts signed weights;
Proposition 4.2 characterizes attainable profiles by positive squared-minor
coefficients; Lemma 4.3 gives the determinant identity; and Lemma 4.4
evaluates and interpolates the polynomial in time polynomial in the
representation length and maximum integer weight at fixed profile dimension.
Lemma 2.1 gives deletion recovery with an explicit original-rank test.
Theorem 1.3 permits an arbitrary objective supplied by a comparison oracle.
These are the precise established ingredients used here. The candidate's
Section 7 names and numbers them correctly.

[Brown, Laddha, and Singh (2024)](https://par.nsf.gov/servlets/purl/10548928)
was also checked in full-text extraction at
`/tmp/minlp-brown-laddha-singh-2024.txt`. Theorem 3 explicitly permits an
independence-oracle matroid and a concave monotone homogeneous criterion
given with value and first-order oracles, with randomized running time
`n^(O(p log(p)/epsilon^2))`. Its underlying data are information vectors;
its proof already guesses and forces vectors and filters others after
normalization. Its statement is over independent sets, which can be
extended to bases for its monotone maximization objectives. The candidate's
improved accuracy dependence is restricted to supplied rational
representations and does not subsume the broader oracle guarantee.

This review does not certify the rest of the priority landscape. In
particular, Onn's monograph chapter remains outside this review's read
full text. The candidate's explicit mixed-determinant cancellation and
finite-field lifting examples are algebraically correct, but neither is
a hardness theorem for the proposed PSD problem.

The fresh [exact checker](../code/research_20260912/review_represented_matroid_psd.py)
imports no author implementation and no earlier reviewer implementation.
It enumerates all bases of tiny input matroids for independent ground
truth, performs its own rational PSD factorization and all normalization
trials, and checks every target's maximum-volume witness. It computes the
generating determinant using sparse polynomial matrix entries and the
Leibniz formula, independently compares its coefficients with exhaustive
squared minors, and runs fixed-row deletion recovery. The owner-count
construction checks the contraction coefficients through a separate
original-rank determinant.

The checker deliberately uses exponential verification routines on tiny
instances. It is not the theorem's polynomial-time solver. A separate
three-variable bounded-degree fixture checks the actual numerical
determinant evaluations and tensor Vandermonde interpolation, including
zero output after rank loss; it does not run the potentially huge full
interpolation grid in every normalized trial.

The [saved exact results](../code/research_20260912/results/represented-matroid-psd-independent-review.json)
record 15 fixtures, 121 independent factor trials, and 80 original bases,
all covered by 62 output bases in total. They include:

- 74 maximum-volume target witnesses and 198 same-profile sandwiches;
- 33 sparse determinant/support checks and exact owner-count versus
  contraction coefficient comparisons, including 30 with nonempty `F`;
- 110 recovered bases, 495 deletion coefficient tests, and 99 rejections
  caused by rank loss with the original determinant rows retained;
- 23 restriction-rank-loss rejections, 15 dependent-owner rejections,
  12 trials with a filtered forced owner, six repeated-factor-owner trials,
  and 20 contractions of rank zero;
- 91 profile collisions, including 71 between different information
  matrices, and 18 trials with multiple distinct attainable profiles;
- signed off-diagonal floors, nontrivial rational contraction denominators,
  redundant representation rows, loops, parallel elements, graphic
  dependence, and matroid ranks three and four above information dimension;
- empty and rank-zero matroids, zero information, mixed singular ranges,
  distinct nearly parallel rank-one ranges separated by `2^-80`, and a
  proper oblique rank-two range with a `2^-60` coordinate;
- 54 exact determinant evaluations for tensor interpolation, an explicit
  false acceptance witness from recomputing a smaller row rank, and a
  positive characteristic-zero coefficient that vanishes modulo a prime;
- exact D-, A-, and E-criterion checks, together with 80 checks each of
  same-range pseudoinverse bounds, estimable contrasts, added priors, and
  common rectangular congruences.

All checks passed. Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_represented_matroid_psd.py
```

## Later Lean verification

On 2026-09-22, [topic 22](../formal/topics/22-represented-matroid-spectral/README.md)
completed all 37 frozen claims, independent reviews, and targeted Lean
checks. Its producer uses the equivalent owner-count variant, cached Bird
determinants, and tensor Lagrange interpolation. The original mathematical
review and small contraction checker above remain historical evidence; the
[Lean verification record](../formal/topics/22-represented-matroid-spectral/VERIFICATION.md)
records the implemented variant and the complete original-input cost proof.
