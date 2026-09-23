# Stage 3 independent review 2

Date: 2026-09-13. Scope: the shared rational normalization and DAG spectral
cover, their criterion and locality consequences, with a broader read of the
represented-matroid proof, weighted-trace scheme, and stated prior boundaries.
I read `sections/03-approximation.tex`, `appendices/approximation.tex`, the
relevant accepted locality dependencies, the coverage map, and the indicated
primary-source passages. I did not read another review or use the author's
checker.

## Findings and verdict

**MAJOR: none. MINOR: none.** I recommend accepting this stage within its
specified scope. I found no mathematical or scientific correction to request.
This review does not certify completeness of the later certification,
computational, or whole-paper stages.

## Main proof checks

- `lem:spectral-normalization`, source lines 221–290: the rational LDL
  decomposition accommodates singular atoms. The independent labeled factors
  determine a rational range projector and left inverse. The dyadic weights
  yield both the forced floor and reversible congruence. For a target object,
  maximum volume is needed only for existence: replacing a basis column proves
  the coordinate bound, and enumeration of rational labels includes that basis
  without computing irrational weighted volumes. Each owner contributes every
  one of its factors once, including when several basis labels share an owner.
  Consequently the atom-level magnitude filter and forced-owner floor are
  compatible. I found no dependence on an unprovided positive eigenvalue or
  condition-number promise.
- `thm:dag-spectral-set`, source lines 292–337: a DAG continuation depends on
  the current vertex, profile and forced-owner mask; previously visited edges
  cannot become available later. Thus merging states preserves the required
  reachability. Floor, rather than truncation toward zero, gives residuals in
  the asserted common interval even for negative off-diagonal entries and
  paths of different lengths. Equal signed profiles give absolute symmetric
  error at most `r*N*h`, and the floor converts this to relative error. The
  number of possible accumulated coordinates is bounded by the stated `C_r`:
  the endpoint interval has length at most `8*p*N/h + N`. Range preservation,
  the separate zero-information subgraph, and the `s=t` boundary cover all
  ranks. Label enumeration, inverse/projector arithmetic, dyadic scaling and
  profile arithmetic have polynomial bit length for fixed `p`.
- `subsec:spectral-consequences` and `cor:true-spectral-cover`, source lines
  349–416: D uses determinant ratios, E comparison can use fixed-degree exact
  algebraic arithmetic, and inverse criteria are restricted to positive
  definite information or a common estimable range as required. Singular
  information does not accidentally receive a finite nonestimable contrast
  cost. Common congruences and common PSD additions preserve the sandwich.
  The two applications of the locality bound give the stated factors. The
  `17*xi/28` bound is valid for `0<xi<1`; an independent symbolic check gives
  its slack as `6*xi*(1-xi)/(7*(8-xi))`.
- `app:matroid-proof`: restricting to full original rank, contracting an
  independent forced-owner subset, and keeping that rank during deletion are
  sufficient to return original bases. Positive squared minors ensure exact
  characteristic-zero profile detection. Shifted integer profiles preserve
  signed sums because all optional bases have the same size. The tensor
  interpolation and deletion algorithm has polynomial bit complexity with
  input-sized matroid rank and fixed information dimension. The zero-rank
  and zero-information cases are separately covered. I found no unstated
  extension to arbitrary oracle matroids, finite fields, intersections, or
  correlated-history restrictions.
- `thm:trace-fptas`: the accepted locality results supply the stated envelopes.
  Their fixed promise constants are essential, and are stated explicitly.
  Choosing a complete-history cap preserves the polynomial bound because the
  preceding window failed the accuracy test. The cooldown counter handles
  spacing even when the covariance window has forgotten the last selected
  time. The true/surrogate objective inequalities include nonnegative common
  priors and zero optima. The hardness example concerns individual channels,
  rather than contradicting complete-packet selection.

## Independent exact checks

I wrote and ran
`verification/stage03-review2/check_spectral.py` using SymPy rational arithmetic.
It independently implements rational factorization, range/magnitude filtering,
dyadic normalization, owner forcing, and signed-profile DAG state merging.
Every returned matrix sandwich is checked using exact principal minors.

Three instances each contain 20 feasible paths with zero atoms, variable path
lengths, parallel edges, negative off-diagonal entries, nearly coincident but
distinct rank-one ranges, and rational eigenvalue scales down to `2^-120`.
The prior is respectively zero, rank one, and positive definite. Across those
instances the test checked 91 independent-label trials, 76 forced-owner
floors, and 62 actual state merges. Each instance returned 19 representatives
and covered all 20 target paths; every successful sandwich had the same exact
kernel. The tests therefore exercise nontrivial state merging as well as the
singular cases. Results are stored beside the script in `results.json`.
These finite checks supplement the proof audit; they are not a general proof.

## Primary-work comparison

I independently inspected the primary Berstein et al. author report,
[Nonlinear Matroid Optimization and Experimental Design](https://optimization-online.org/wp-content/uploads/2007/07/1725.pdf),
Theorems 1.1/1.3 and Lemmas 4.3–4.4. Those passages establish the squared-minor
identity and exact bounded-profile interpolation. The manuscript attributes
that machinery correctly and distinguishes fixed distinct weight values in
the oracle theorem from its growing rounded-label family.

I also read Theorem 3 and the normalization/guessing argument on printed
pages 2–5 of Brown, Laddha and Singh's final publisher PDF, available from
[the NSF primary archive](https://par.nsf.gov/servlets/purl/10548928).
The browser retrieval timed out, so I used the already downloaded original
PDF and its extraction under `/tmp/correlated-stage03-sources`. The source
has the broader independence-oracle matroid setting, objective-specific
concave monotone homogeneous optimization, and randomized runtime whose
exponent depends on accuracy. The manuscript's comparison explicitly credits
the guessed normalization and forced-subset method. Its qualified claim is
the complete two-sided all-target integral cover with exact ranges and
deterministic polynomial accuracy dependence under explicit representations;
it does not claim to subsume Brown et al.'s oracle model. This is an
appropriately narrow boundary relative to the sources I checked, rather than
an assertion that the literature search proves absolute priority.

The coverage map points to the actual Stage 3 theorem and appendix labels.
Later computational construction of a full spectral set is not promised as
a practical solver: the text explicitly identifies the large exponents and
keeps that theorem separate from the certification methods to come.
