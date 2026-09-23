# Spectral approximation sets for rationally represented matroid bases

Date: 2026-09-12. Lean verification completed on 2026-09-22.
Priority is unresolved. No practical performance claim is made.

All 37 frozen topic-22 claims are proved and independently reviewed. The
65 Lean modules passed the targeted build, the 1,680-declaration axiom audit,
three original-input execution checks, and individual kernel replays.
The implementation uses the owner-count variant below, cached Bird
arithmetic, and explicit tensor Lagrange interpolation. These preserve the
theorem and output bound while avoiding a contraction matrix. The complete
producer and polynomial charged bit-work bound start from the original
rational representation and PSD matrices, without a supplied profile oracle.
See the [coverage map](../formal/topics/22-represented-matroid-spectral/COVERAGE.md)
and [verification record](../formal/topics/22-represented-matroid-spectral/VERIFICATION.md).

The [independent review](research-20260912-represented-matroid-psd-independent-review.md)
accepted the theorem, Turing bit bound, and stated design consequences.
Its exact checker tests normalization, determinant profiles, interpolation,
contraction, and basis recovery on small instances. This is verification,
not a standalone polynomial-time solver implementation.

The construction replaces the DAG dynamic program in the
[reviewed PSD approximation-set construction](research-20260912-dag-psd-approximation-set.md)
with the exact profile algorithm of Berstein et al. (2008). It gives deterministic FPTAS consequences for D-, A-, and E-optimal design
over rationally represented matroid bases at fixed information dimension.
This is narrower than the independence-oracle matroid model in Brown,
Laddha, and Singh (2024). The profile-generating determinant and its
interpolation are established results, not proposed inventions here.

## 1. Input and theorem

Fix `p>=1`. Let `A in Q^(a by m)` explicitly represent a matroid on
`E={1,...,m}`: a set is independent exactly when its columns of `A` are
linearly independent. Write `q=rank(A)` for the matroid rank. Neither
`q` nor `a` is fixed. Each element has a rational symmetric PSD matrix
`Q_e` of order `p`; there is also a rational symmetric PSD matrix `Q0`.
For a matroid base `B`, put

```text
J(B) = Q0 + sum_(e in B) Q_e.                         (1)
```

**Candidate theorem.** For rational `0<eta<1`, one can deterministically
construct a set `C` of actual matroid bases such that, for every base `B`,
some `B_hat in C` satisfies

```text
(1-eta) J(B) <=_PSD J(B_hat) <=_PSD (1+eta) J(B).       (2)
```

The set size and Turing bit complexity are polynomial in the entire input
length and `1/eta` for fixed `p`. All singular matrices are included, and
the representative in (2) has the same kernel as its target. There is no
lower eigenvalue or Euclidean condition-number assumption.

An explicitly represented matroid always has a base. When `q=0`, its only
base is empty; return it. Otherwise use `N=q` as a uniform cardinality
bound. Remove redundant rows of `A` so it has full row rank `q`. Rational
row selection and denominator clearing preserve the column matroid and
have polynomial bit complexity. In what follows, keep the distinction
between matroid rank `q` and information rank `r<=p`.

The output is an approximation set, not necessarily a set of PSD-maximal
bases. Its two-sided property can be destroyed by discarding dominated
matrices. Complexity is measured in the supplied rational representation;
the statement does not provide a representation from an independence
oracle or from a finite-field representation.

## 2. Normalize each possible information range

Decompose every `Q_e` and `Q0` by exact rational pivoted LDL into at most
`p` nonzero terms `w_j v_j v_j^T`, with rational `w_j>0` and rational
`v_j`. Retain each factor's element or prior owner. There are at most
`M=p(m+1)` labels.

For every `r=1,...,p`, enumerate all `r` factor labels whose columns form
an independent rational `p by r` matrix `V_b`. Define

```text
L = (V_b^T V_b)^(-1) V_b^T,       Pi = V_b L,
1 <= tau_i^2 w_bi < 4,           tau_i a power of two,
T = diag(tau_i) L,               K = V_b diag(1/tau_i),
H_e = T Q_e T^T,                 H0 = T Q0 T^T.        (3)
```

Here `T K=I_r` and `K T=Pi`. Reject the trial unless `Pi Q0=Q0` and
every diagonal entry of `H0` is at most `4p`. Let `E'` consist of elements
with `Pi Q_e=Q_e` and every diagonal entry of `H_e` at most `4p`.
These are exact tests. Every retained matrix has range in `range(V_b)`,
can be reconstructed as `Q_e=K H_e K^T`, and has transformed entries
bounded in absolute value by `4p`.

Let `F` be the distinct element owners of the selected factors; selected
prior factors require nothing. There are at most `r<=p` forced elements.
Reject the trial if `F` is not a subset of `E'`, its columns in `A` are
dependent, or `rank(A_E')<q`. The last condition is essential: a base of
the lower-rank restriction would not be a base of the original matroid.

The implemented variant keeps the original `q` rows and enforces `F`
through one additional profile coordinate. Give element `e` the marker
`b_e=1` if `e in F`, and `0` otherwise. For every base `B`,

```text
sum_(e in B) b_e = |F| iff F is a subset of B.          (4)
```

This holds because a base is a set, so every forced element contributes
at most once. Restriction zeros columns outside `E'` without changing
row count; a positive profile coefficient therefore certifies an original
base contained in `E'`. A marker-complete profile also forces every owner.
The rank and owner rejection tests above may be implemented through these
exact support tests rather than as separate preliminary operations.

Write `q'=q-|F|` for the number of optional elements in every accepted
base. If `q'=0`, any accepted base is exactly `F`; this case has zero
approximation error. The producer may still use the same marker test.
Contraction is an equivalent mathematical construction, retained as an
independent cross-check in Section 8, not an operation of this producer.

Every original base accepted by this trial contains all selected factors.
Consequently its transformed information satisfies

```text
H(B) = H0 + sum_(e in B) H_e
     >=_PSD diag(tau_i^2 w_bi) >=_PSD I_r.             (5)
```

Its original information matrix has range exactly `range(V_b)`.

## 3. Enumerate rounded profiles by the established determinant method

For each positive-rank trial set

```text
h = eta/(r q),
z_e,ij = floor(H_e,ij/h),       1<=i<=j<=r,
d = r(r+1)/2.                                          (6)
```

The prior remains exact. All retained element labels can be rounded,
including forced elements: their common contribution cancels when two
accepted bases are compared. Floor includes negative entries. Put

```text
Lmax = ceil(4p/h),
w_e,ij = z_e,ij + Lmax in {0,...,2 Lmax}.               (7)
```

All original bases have cardinality `q`, so subtracting `q Lmax 1`
recovers their signed profile. For owner-complete bases, subtracting the
common forced-element profile leaves optional profiles with `q'` terms.

Let `A_ret` be the original full-row-rank representation with columns
outside `E'` zeroed. Use `d` information variables `y` and an owner
variable `t`, and define

```text
g(y,t) = det(A_ret diag_e(y^w_e t^b_e) A_ret^T)
       = sum_(B original base, B subset E')
           det(A_B)^2 y^(sum_(e in B) w_e) t^(|B intersect F|). (8)
```

This is the Cauchy–Binet determinant identity used by Berstein et al.
(2008), Lemma 4.3, with one extra bounded integer coordinate. Over the
rationals every coefficient is nonnegative and is positive exactly when
its profile is attained. Only coefficients of marker degree `|F|` are
retained. These characterize actual original bases containing every owner.
There is no cancellation among bases with the same profile. Arbitrary
reduction modulo a prime need not preserve coefficient nonzeroness.

The information degrees are at most `D=2qLmax`, and the marker degree is
at most `|F|<=q`. A uniform product grid `{1,...,Dbar+1}^(d+1)` with
`Dbar=max(D,q)` therefore suffices. The sharper rectangular grid is also
valid. At positive information rank, `Lmax>=1`, so `Dbar=D`.

Compute a requested coefficient by exact tensor Lagrange interpolation.
For nodes `1,...,Dbar+1`, form the univariate basis polynomials

```text
l_t(X) = product_(s != t) (X-s)/(t-s).
```

The coefficient of multi-index `z` is the sum over all grid points of
`g(t)` times the product of the corresponding coefficients of these
univariate basis polynomials. This is an explicit inverse of the tensor
Vandermonde system. The implementation constructs each univariate product
by multiplying coefficient vectors; it does not enumerate subsets of its
factors. Each grid determinant is evaluated by a cached version of
[Bird's division-free recurrence](https://www.cs.ox.ac.uk/publications/publication5398-abstract.html)
after exact denominator clearing. The preceding matrix is
stored once at each step. Determinant work is polynomial in variable `q`,
rather than a permutation expansion with factorial work.

Recover one actual base for each positive marker-complete profile by
one-pass column deletion. Start with all retained columns. Delete a column
if its removal preserves positivity of the requested coefficient. Keep
all original `q` rows in every test: a rank drop gives the zero polynomial.
The target remains feasible; a deletion infeasible earlier cannot become
feasible after more columns disappear. If the final set contained an extra
column outside one of its target-profile bases, that column could have
been deleted, a contradiction. Thus at most `m` tests leave exactly one
original base with that profile. No contraction or lifting is needed.

There are at most

```text
R = (2q'Lmax+1)^d                                     (9)
```

positive owner-complete profiles after subtracting the common forced
profile. Enumerating the larger full information grid `(D+1)^d` before
coefficient tests is still polynomial. The extra marker coordinate affects
interpolation work, not the number of retained profiles.

For information rank zero, if `Q0=0`, restrict to elements with `Q_e=0`.
Add one base only if the restriction retains the original `q`; its support
test again keeps all original rows. This covers all zero-information
bases. A nonzero prior excludes information rank zero.

## 4. Approximation proof

Fix any base `B` with information rank `r>0`. The factor vectors in its
elements and prior span `S=range J(B)`. Choose a maximum-volume set of
`r` weighted factor vectors `u_j=sqrt(w_j)v_j` within this collection.
If their matrix is `U_b`, every other factor vector in the collection has
coordinates `u=U_b x` with `|x_i|<=1`: otherwise replacing column `i`
would increase its volume.

The algorithm enumerates the rational labels of this basis. Its range
test preserves every element in `B` and the prior. Its dyadic normalization
gives `T U_b=diag(tau_i sqrt(w_bi))` with diagonal entries in `[1,2)`.
Every transformed factor coordinate therefore has absolute value below
`2`; each individual matrix has at most `p` factors, so its diagonal is
at most `4p`. Thus the prior and all elements of `B` survive all filters.

The forced owner set is a subset of `B`, so it is matroid independent;
the filtered elements retain rank `q` because they contain `B`. Hence
this trial is not rejected, and the full profile of `B` with owner
marker `|F|` has a positive coefficient in (8). Let `B_hat` be the
recovered original base for that profile. If `q'=0`, both bases equal
`F` and are represented exactly. Otherwise subtract the common forced
profile to obtain equal optional signed profiles.

The optional parts have the same signed integer sums. For every matrix
entry, each optional sum differs from `h` times its integer sum by a
number in `[0,q' h)`. The shared forced and prior matrices cancel.
Therefore

```text
|H(B_hat)_ij-H(B)_ij| < q' h <= q h,
||H(B_hat)-H(B)||_2 <= r q h = eta.                  (10)
```

Together with `H(B)>=_PSD I_r`, this gives the two-sided relative
sandwich in transformed coordinates. Congruence by `K` reconstructs the
original matrices and proves (2). The range tests and forced factors give
the same exact range. The separate rank-zero step completes the proof.

The proof does not identify an optimal design or use a scalar objective.
It proves coverage separately for every base by its own maximum-volume
trial. Square roots appear only in the proof; every algorithmic operation
can use rational arithmetic.

## 5. Polynomial bit complexity

There are at most `sum_(r=1)^p binom(M,r)` trials. For rank `r`,

```text
Lmax = ceil(4 p r q/eta),
D = 2 q ceil(4 p r q/eta),
R <= [2 q ceil(4 p r q/eta)+1]^(r(r+1)/2).             (11)
```

Each trial needs polynomially many operations for range tests, exact
profile support, owner enforcement, and original-rank preservation.
No contraction matrix is constructed. At most `R` representatives are
recovered, each with at most `m` further profile tests. The deliberately simple implementation
may recompute all coefficients for each test; even this is polynomial
in input length and `1/eta` for fixed `p`.

The output count is bounded by

```text
|C| <= 1 + sum_(r=1)^p binom(M,r)
       [2 q ceil(4 p r q/eta)+1]^(r(r+1)/2).           (12)
```

Here the initial `1` allows a zero-information representative. The
matroid-rank-zero case was handled before the enumeration.

For clarity, interpolation does not hide exponential bit lengths.
At a product-grid point, `y^w_e t^b_e` has bit length
`O((d Lmax+1) log(Dbar+1))`. Entries of the evaluated matrix therefore
have polynomial bit length. Clear their rational denominators by a common
product; its bit length is bounded by the sum of denominator lengths.
Bird's stored integer matrices perform polynomially many arithmetic
operations, and degree-growth bounds keep their operand lengths
polynomial even when `q` grows. A final exact division by the denominator
raised to `q` recovers the rational determinant.

The univariate Lagrange products and their nonzero integer denominators
have polynomial degree and encoding length. Their tensor products and
finite grid sums therefore have polynomial bit complexity at fixed `d+1`.
The implementation may recompute grid values for each coefficient and each
deletion test; these nested finite loops remain polynomial. Representation
row selection and normalization have separate polynomial bit bounds.
Large numerical coefficient values are permitted; their encodings, rather
than their magnitudes, are bounded. No factorial determinant execution or
unit-cost real arithmetic is used in this claim.

The Lean cost model charges schoolbook arithmetic and explicit finite scans,
storage, and copies. Row reduction, factorization, and each trial's shifted
labels are cached; rejected trials and rejected atoms are charged too.
Construction of proof and cost-observer transcripts is outside the measured
arithmetic algorithm. These bounds do not predict Lean wall-clock runtime.

This does not imply that floating determinant/interpolation tests can
certify zero coefficients. Exact arithmetic is part of the theorem.

## 6. Consequences and useful subclasses

The same consequences as for the DAG approximation set follow:
determinant ratio `1-epsilon` using `eta=epsilon/p`; minimum-eigenvalue
ratio `1-epsilon` using `eta=epsilon`; and inverse-trace minimization
ratio `1+epsilon` using `eta=epsilon/(1+epsilon)`. Determinants and
inverse traces are rational; minimum-eigenvalue comparisons use exact
fixed-degree algebraic-number operations. The common-range contrast,
additional-prior, and common-congruence deductions are unchanged.

For any nonnegative Loewner-monotone homogeneous criterion of degree
`a>0`, coverage gives factor `(1-eta)^a`, subject to availability of a
suitable evaluation/comparison procedure. Neither concavity nor an
objective-specific profile construction is required for this deduction.
Monotonicity alone does not supply a multiplicative objective bound.

Useful explicit representations include uniform matroids (rational
Vandermonde columns), partition matroids (direct sums of such
representations), and graphic matroids (vertex-edge incidence matrices).
Thus the result includes fixed-size experiment selection, quotas by
experiment group, and additive information design over spanning trees or
spanning forests. Vandermonde entries have polynomial encoding length;
the representation does not require bounded integer entries.

The theorem concerns additive element information matrices. It does not
automatically combine Markov-history path constraints with an additional
matroid constraint, nor cover arbitrary correlated observations without
an appropriate additive formulation.

## 7. Direct prior audit and boundaries

**The exact profile algorithm is already known.** Berstein, Lee,
Maruri-Aguilar, Onn, Riccomagno, Weismantel, and Wynn (2008),
[Nonlinear Matroid Optimization and Experimental Design](https://optimization-online.org/wp-content/uploads/2007/07/1725.pdf),
SIAM Journal on Discrete Mathematics 22(3):901–919,
DOI `10.1137/070696465`, supplies the exact-profile identity, interpolation
strategy, and deletion reduction used in Section 3.
In the read preprint, Lemma 4.1 shifts signed weights, Proposition 4.2
identifies feasible profiles through positive squared-determinant
coefficients, Lemmas 4.3–4.4 evaluate/interpolate the generating polynomial,
and Lemma 2.1 supplies deletion recovery. Theorem 1.3 solves arbitrary
nonlinear fixed-dimensional profile optimization in time polynomial in
representation bit length and maximum absolute integer weight. The
proposed addition is a relative PSD normalization that makes those weights
polynomially bounded despite arbitrary conditioning, while preserving all
singular ranges. Neither interpolation nor nonlinear matroid optimization
should be presented as a new capability.

**A stronger accuracy dependence comes with a narrower matroid model.**
Brown, Laddha, and Singh (2024),
[Fast algorithms for maximizing the minimum eigenvalue in fixed dimension](https://par.nsf.gov/servlets/purl/10548928),
Operations Research Letters 57:107186, DOI `10.1016/j.orl.2024.107186`,
Theorem 3, permits a matroid supplied by an independence oracle and a
concave monotone homogeneous objective supplied by value and first-order
oracles. Its randomized PTAS has an accuracy-dependent exponent,
`n^(O(p log(p)/epsilon^2))`. The proposed deterministic FPTAS improves
that dependence on the explicitly rationally represented subclass; it
does not subsume their broader oracle guarantee. Their proof already
normalizes, filters, and forces guessed information vectors, so those
ingredients individually are not new.

**Projected vertices do not suffice for these criteria.** The existing
local source [Onn and Rothblum (2004), Convex Combinatorial
Optimization](../literature/papers/onn2004-convex-combinatorial-optimization/paper.md)
gives strongly polynomial fixed-dimensional convex maximization through
projected-polytope vertices and linear optimization. Its introduction and
Theorem 2.6 were checked. D- and E-optimal maxima may occur at an interior
profile instead: for the rank-one uniform matroid on three elements with
information matrices `diag(1,3)`, `2I`, and `diag(3,1)`, the middle
profile is interior to the projected segment and uniquely best for both
determinant and minimum eigenvalue. Thus enumerating projected vertices
does not replace the attainable-profile enumeration here.

**Dimension-dependent general approximations are different guarantees.**
Brown, Laddha, Pittu, Singh, and Tetali (2022),
[Determinant Maximization via Matroid Intersection Algorithms](https://ieee-focs.org/FOCS-2022-Papers/pdfs/FOCS2022-4Bu7jGV9xIcveUWYj3oWoi/551900a255/551900a255.pdf),
FOCS, DOI `10.1109/FOCS54457.2022.00031`, Theorem I.1 gives a
deterministic dimension-dependent determinant approximation under an
oracle matroid constraint; related statements handle lower-rank volumes.
Its all-rank complement, Brown, Laddha, Pittu, and Singh (2022),
[Efficient Determinant Maximization for All Matroids](https://arxiv.org/abs/2211.10507),
Theorem 1, gives a constructive `p^(O(p))` approximation when the
matroid rank is at least `p`; that theorem and its technical overview
were read. Neither result states a fixed-information-dimension FPTAS. The recent
Bansal–Xu (2026) partition A/E-design hardness, arXiv `2608.05468`, uses
growing information dimension and therefore does not contradict the
candidate's fixed-`p` qualification.

**Objective-independent spectral coresets are also established.**
Mahabadi and Vuong (2026),
[Composable Coresets for Constrained Determinant Maximization and Beyond](https://proceedings.mlr.press/v300/mahabadi26a.html),
PMLR 300:1432–1440, Theorem 26 gives determinant coresets for partition
and laminar constraints. For example, its partition result for `k>=p`
has size `O(kp)` and approximation factor `p^(2p)`. Theorem 26 and
Appendix C were read in the publisher-linked full text. Appendix C uses
spectral spanners to replace each selected vector by a distribution over
retained vectors, then applies rounding for particular design criteria.
That intermediate object is a fractional information matrix with a
dimension-dependent approximation factor. It is not a single integral
design within `1+-eta` of every target matrix.

Its predecessor, Indyk, Mahabadi, Oveis Gharan, and Rezaei (2020),
[Composable Core-sets for Determinant Maximization Problems via Spectral Spanners](https://doi.org/10.1137/1.9781611975994.103),
already explicitly makes its spectral construction independent of the
objective. The introduction, Proposition 6.2, and Section 6.2 were read
in arXiv `1807.11648v2`. Proposition 6.2 first treats fractional budgeted
optimization; Section 6.2 obtains design consequences for multisets using
rounding and a budget sufficiently large relative to dimension. Thus objective independence
by itself is not a priority claim. These coresets retain input elements
and support distributed composition; our proposed output retains feasible
bases, may have much larger size, and has no distributed-composition
guarantee.

**Fixed objective dimension is not fixed decision dimension.**
De Loera, Hemmecke, Köppe, and Weismantel (2008),
[FPTAS for optimizing polynomials over the mixed-integer points of polytopes in fixed dimension](../literature/papers/loera2008-fptas-for-optimizing-polynomials-over/paper.md),
Theorem 1, fixes the total number of continuous and integer variables.
Its model and theorem were checked in the local full text. Projecting a
large matroid base set to a fixed number of profile coordinates does not
by itself supply that hypothesis: integer points of a projected polytope
can include unattainable profiles. Even `U_(1,2)` with scalar information
values `1` and `3` has projected interval `[1,3]`, whose integer point `2`
does not belong to any base. Exact feasible-profile recovery is therefore
a substantive requirement of the present reduction.

**Do not silently extend the polynomial identity to arbitrary matroids.**
The positive det-squared support test uses a rational representation.
Berstein et al.'s oracle result, Theorem 1.1, requires a fixed number of
distinct weight values; our rounded labels have a number of possible
values that grows with input size and `1/eta`. Substitution into that
oracle result does not preserve a polynomial exponent. This is an
obstruction to that proof route, not a hardness proof for the PSD problem.

For two represented matroids, a mixed determinant contains products of
two different basis determinants, which may have opposite signs. The
single-matroid noncancellation argument no longer applies: with row
representations `[1,1]` and `[1,-1]` and identical zero profiles, the mixed
determinant is zero although both singleton sets are common bases.
Berstein, Lee,
Onn, and Weismantel, [Nonlinear optimization for matroid intersection and
extensions](https://arxiv.org/abs/0807.3907), give a randomized algorithm
for arbitrary fixed-dimensional unary profiles over common bases of two
represented matroids. Section 3 of the preprint was read: separate
element indeterminates prevent formal cancellation, then random
substitution and a polynomial identity bound recover profiles with high
probability. The published title is *Parametric nonlinear discrete
optimization over well-described sets and matroid intersections*,
Mathematical Programming 124:233–253 (2010), DOI
`10.1007/s10107-010-0358-6`. That distinct randomized extension is not
claimed here. Finite-field representations likewise cannot be
reinterpreted as rational representations without potentially changing
independence relations. For example, the columns of the matrix with rows
`[1,1,0]`, `[1,0,1]`, `[0,1,1]` are dependent over `F_2` but have
nonzero rational determinant `-2`.

Onn's 2010 monograph,
[Nonlinear Discrete Optimization](https://ems.press/books/zlam/84),
DOI `10.4171/093`, is another priority source, particularly Chapter 6.
Its official abstract and contents were read; that chapter's full text
remains unretrieved and unread for this audit. Identified missing works
were sent to the shared literature agent, including this source request.

The bounded audit has not established that the normalized all-matrix
approximation set, or its fixed-dimensional design consequences, is new.
The candidate is a specific combination of a reviewed normalization
argument with established exact-profile machinery. Correctness, priority,
and practical impact must be assessed separately.

## 8. Equivalent contraction cross-check

The original version of this note contracted `F` after the rank-preserving
restriction. Extend its independent columns to a retained basis matrix
`D`, with `F` first, apply `D^(-1)`, and remove the first `|F|` rows and
forced columns. The resulting rational representation has rank
`q'=q-|F|`. Its bases are exactly the optional parts of original bases
contained in `E'` and containing `F`. Clearing denominators preserves them.

This contracted construction and the implemented owner-count construction
have the same optional profile support. Their coefficients agree up to
the common squared change-of-basis and denominator-clearing factor. The
historical exact checker compared both on small examples. That is an
independent check of owner handling; the present Lean producer uses the
owner-count construction and makes no contraction-implementation claim.
