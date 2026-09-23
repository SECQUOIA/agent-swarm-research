# Stage 4 round 1 — reviewer 11

Major findings: 0
Minor findings: 0

Reviewer lens: nonconvex scalar family and arbitrary polynomial overlay, including Bernstein error, dense degree/encoding, two-integer representation, binary lower bounds, root brackets and sign-directed bands.

I found no concrete major or minor issue in this frozen stage. This is a bounded mathematical review, not a guarantee of correctness, novelty, external acceptance, or implementation completeness. There are no numbered findings or unresolved review questions.

## Scope and snapshot

I read the entire `sections/04-vector.tex` (1,297 lines), abstract, introduction and conclusion; the stage task, protocol and process; the coverage inventory and relevant bibliography entries. I compared the ten canonical stage-4 result texts and eleven explicitly substantive supporting developments with their manuscript locations. Promoted pointer notes contain no additional theorem. The hinge example and Bernstein stability mechanism remain present; the weaker numerical degree-32 precursor does not add an omitted mechanism. Direct maximum-product allocation, elementary normalization/simplex bounds and the repeated-convexification argument remain present despite stronger companion bounds.

I reread the accepted dependencies used here: the model, affine invariance, parity/contact and finite-disjunction lemmas in section 01; the rational block log-determinant oracle and central repair in section 02; and the scalar chord/packing lemma, indexed endpoint compiler, hybrid curvature compiler and Jensen superadditivity in section 03. My previous stage-3 review covered its full scalar proofs; this review additionally checked the current versions of the dependencies above. I did not conduct a new full proof audit of every unrelated theorem in sections 01–03.

All eleven SHA-256 values matched the snapshot both at the initial check and immediately before writing this report:

| Reviewed file | SHA-256 |
| --- | --- |
| `abstract.tex` | `db2b95f525fdfc786c9c24b46f41693892131a8103f249d27dbc012d53e323a3` |
| `coverage.md` | `d8b2ed835cfcdfac31b48197cd7a4da7c0e9bac0f73b2dfab6a3571d34a8e1cf` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `026577c84ea4f9c0ff19361708694be45ce88a5a4e911a9b902852f826d1ba9c` |
| `references.bib` | `60fd73a2eec8fd2bc999cf2c407c6a571c590b087786c78647cc1bb7a59a1693` |
| `sections/00-introduction.tex` | `6940bf7c1017d82a8ea00af76575aa88da76f2ef26290b4b3872fd0bba152b16` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/03-scalar-nonlinear.tex` | `8e271531b4c705a1333b49f170b20e987359ed5e7d1b05866030bccb69040803` |
| `sections/04-vector.tex` | `d9369569aa0711c3652dcf28929ea4be5884c534f18e371038fbdfc7edb6252d` |
| `sections/05-conclusion.tex` | `2bfb1f16aaa317e5b49dd171ccd9648c7a320343f23ec13acbf6a38b1955ad6e` |

## Specialist reconstruction

**Nonconvex family (`thm:nonconvex-gap`).** For the triangular wave with M periods, the slope bound is 2M. With N=1024M², the binomial variance estimate gives M/sqrt(N)=1/32 uniformly, including the endpoints. Bernstein positivity keeps the polynomial in [0,1]. The rational samples and binomial expansion have polynomial total encoding in numerical N and log M. This is a dense input family; it makes no polynomial-time construction claim in log M alone.

The period index z in [0,M−1] and orientation bit give exactly the triangular wave with x=(z+t)/M. Both branches are bounded rational polyhedra and their two-branch formulation does not require an extra integer beyond the orientation bit. The last period contains x=1, and adjacent periods agree at their boundary troughs. Thickening outputs by 1/32 contains the entire polynomial graph and admits error at most 1/16, below the fixed 1/4 tolerance. Both the unrestricted period integer and the binary orientation count toward the claimed two general integers.

At every peak the polynomial is at least 31/32; every trough is at most 1/32. Any two distinct peak contacts in the same binary section admit a chord crossing an intermediate trough, with error at least 30/32. This lower bound applies to arbitrary convex binary lifts, hence to the manuscript's binary linear minimum. Replacing the bounded period index with ceil(log2 M) bits, explicitly excluding unused codes, proves the upper count. Alternating endpoint troughs and peaks force at least 2M distinct crossings of 1/2, so actual degrees grow. Combined with degree at most 1024M², the binary/general-integer difference is Omega(log degree) along this family. The theorem does not claim the general-integer optimum is exactly two.

Restriction to convexity pieces and negation on concave pieces preserve the comparator count. Each piece has at most 3·2^p finite chord bands. The D−2 upper bound on distinct second-derivative roots gives at most D−1 pieces for D≥2; affine functions are handled separately. Thus the finite logarithmic-degree upper and the example's lower have compatible scope.

**Arbitrary polynomial overlay (`thm:arbitrary-vector-overlay`).** The coefficient sum M_j bounds the absolute derivative on [0,1]. Squarefree isolation of each distinct interior root of f_j'' permits disjoint rational nonroot bracket endpoints at the stated polynomial precision. Endpoint roots need no bracket. At most D_j−2 brackets and their complements give fewer than 2D_j pieces. On each complement the curvature has one sign; rational input normalization and possible output negation preserve the local comparator. Applying the dense hybrid therefore gives fewer than 2^(p+11) cells per shape piece. A root bracket's 2M_j h bound controls every subinterval even when curvature changes sign. The resulting 4096D_j·2^p count is sufficient, including degree two and no-root cases.

The common denominator is built from polynomially many piece endpoints and the maximum dyadic precision, not from exponentially many individual knots. Multiset order statistics retain duplicates, and a positive merged cell cannot cross a source knot. The last source knot at most the left endpoint identifies a containing source cell; at repeated endpoints and at one a containing cell may be chosen without ambiguity for validity. Sign metadata is computed separately for each output and stays fixed within the chosen cell.

In units of epsilon_j, the rounded-center residual ranges are [-1/16,13/16] for convex cells, [-13/16,1/16] for concave cells and [-1/8,1/16] for brackets. Adding the stated band offsets contains zero in every case. Extreme admitted residuals have magnitude at most 15/16. This verifies exact graph containment as well as admitted error, including singleton cells. The sign flags are forced Boolean circuit wires; choosing offsets linearly does not require new integer declarations. All outputs share the same input segment and interpolation weight. Summing actual counts and excluding invalid indices yields exactly the asserted logarithmic-total-degree comparison, with affine outputs represented exactly.

## Full-stage reconstruction

- **Finite and implicit overlays.** The arbitrary-level refinement has at most 2H−2 cuts; plateaus and coincident cuts only decrease the count. The interval-cover argument applies to the closed chord intervals used throughout. The component overlay gives 2m+1 pieces, and the twice-refined facet overlay gives 8q+1. Coupled budgets use a symmetric half-body band, avoiding an invalid difference of two arbitrary points in K. Canonical approximate-mass evaluations at a fixed search-tree node give ordered target branches, so the monotonicity argument does not require a monotone approximate oracle. Fixed common-grid searches handle exponentially long arrays and duplicate endpoints. The directed compiled vector band gives error 15/16 and the 1458m count is below 2048m.

- **Original-output and facet rank.** Maximum-determinant row replacement proves coefficient bound one; determinant doubling among rational original submatrices gives the polynomial factor-two construction. Signed coefficients are safe because every selected chord gap is nonnegative. I recomputed the finite 4r−1 and 8r−1 factors and compiled constants 12 and 13. Compactness of the nonnegative-facet body ensures every output coordinate is measured, making rank zero force an affine graph. The weighted l1 specialization has the stated rank-one scope.

- **Product allocation and rational oracle.** Differentiating log product gives sum v_j/b_j≤m. For an e^(-1)-approximate product, expansion of the feasible point (1−1/m)b+v/m gives the factor seven; m=1 is covered separately. Scaling by the coordinate outer radius makes the accepted scalar block-oracle specialization applicable without dropping any positive feasible point. The 486·28m factor is below 2^14 m.

- **Feasible spanners and effective image.** I checked the inner/outer radii, nonzero pullback normal, inverse/cofactor bound from the seed determinant, and the uniform objective bound. The fixed dyadic grid and fixed central repair give exact feasibility and additive objective loss at most 1/4. A returned coefficient exceeding two doubles the determinant; termination gives coefficient bound 9/4. Fixed denominators prevent successive oracle calls from causing uncontrolled encoding growth. Positive-polar support uses repaired points in K, so its separating cuts are valid for the exact polar. Its membership branch only claims proximity and explicitly constructs a nearby feasible point. Axis seeds span the image, and the one-dimensional product embedding addresses the imported oracle's dimension convention.

- **Oracle graph bands.** Positive-polar scalarizations dominate nonnegative gaps, while the feasible primal basis gives P⊂K∩S⊂drP. The finite tolerances give 8r²−1 cells per parity hull. The rational constants c=d=3 and tau=1/(36r) yield gap in (13/64)P. Rounding effective coordinates contributes P/16, restoring the affine term exactly. The center error is (17/64)P and the final band admits (49/64)P. The compiler adds no oracle constraint, and arbitrary comparator errors outside S are not incorrectly restricted.

- **Separable vector comparisons.** The single concatenated basis gives the same coefficients across all input blocks. Jensen superadditivity makes index-distance gaps additive. Deleting lattice l1 balls yields the denominator [3(2q+1)]^n; the strict midpoint obstruction compares against the original vector lift. I recomputed the six finite/compiled factors: 108r, 87480r, 180r, 157464r, 180r² and 1277208r². Their logarithms justify every listed overhead. Summed rounding respects the coupled body, and inactive coordinates and rank-zero cases reduce to affine equations.

- **Positive-power and cap-set boundaries.** The midpoint bound is strictly below 7/8 everywhere, while the oriented thirds error is at least 2177/2144>1. The scalarization quantifier allows each signed direction its own partition and uses its correct induced tolerance. Modulo-three witnesses and same-binary-section witnesses give their distinct lower bounds. Three distinct zero-sum residues give the same forbidden barycenter. The generating-function minimum solves 4t²+t−2=0. The direct one-integer argument covers arbitrary label differences and then repeated convexification within the middle label. None of these arguments is advertised as a growing optimum binary/general-integer gap.

- **Exact convex box counts and stability.** The rational inequalities for A,c,L,d hold. At label one, weights t,1−2t,t keep the input in [c,1−c] and every output below one, proving validity of the entire integer section. Product contact residues give n general integers; binary sections require 3^n assignments. The potentially exponential binary upper size is stated. The hinge precursor has middle-section error at most 3/4; Bernstein thickening adds at most 2delta and preserves all strict chord obstructions. The affine monotonicity shear preserves error without claiming positive monomial coefficients.

- **Conditioning and open boundaries.** The common quadratic convexifies both tilted outputs, the scalar difference projection preserves the binary obstruction, and the broad common-direction band contains the exact graph. The centered second difference gives max|q_M''|≥(15/2)M² and radius ratio at least 8+60M². Infinity and Euclidean conditioning factors, the nonnegative simplex estimate, and unconditional normalization have the stated constants. Only outer bounds on comparator midpoint vectors and inner bounds on admitted errors are used, so the nonsymmetric extension is justified. Strict upper-violation sets are convex and lattice-free in integer projection; their union need not be convex. The Helly/Radon discussion correctly states missing implications rather than asserting a solution to the one-input constant-gap problem.

The abstract, introduction and conclusion distinguish fixed inputs from growing input dimension, dense from binary-exponent encoding, integer count from total encoding, and finite existence from construction. Their open-question statements agree with the proved separations.

## Primary-source checks and verification limits

I inspected the cached primary passages for GLS Definition (5) and Theorem (3.1): the weak objective comparison is indeed against all of the body, as used here. I also inspected Ellenberg–Gijswijt Theorem 4, Sagraloff–Mehlhorn Theorem 36 and its squarefree scope, Lyu–Hicks–Huchette Section 3 Proposition 1, Plevrakis–Hazan Section 3.2, Kelly–Maulloo–Tan Section 2 and Averkov–Weismantel Theorem 1.1. Their quoted mathematical scope matches the applications. The manuscript supplies its own Bernstein and elementary convexification proofs. This was not an exhaustive literature or bibliographic-priority search, and I did not independently retrieve every cited publication or verify every metadata field.

After inspecting their implementations, I ran these existing checks successfully:

| Checker | Result |
| --- | --- |
| `code/quadratic_rank/check_polynomial_binary_integer_gap.py` | 12 exact Bernstein values at degrees 4096/9216, four peak-chord violations, 90 periodic branch checks |
| `code/quadratic_rank/check_implicit_knot_overlay.py` | 2,304 ordered-search checks, 60 exact order statistics, 180 source-cell containments, eight large implicit-grid rank queries, 99 directed-band checks |
| `code/quadratic_rank/check_rational_polar_spanner_second.py` | 16 generic systems, 93 repaired calls, 11 exchanges, 120 full-image vertex checks, 347 positive-polar cases |
| `code/positive_vector_obstruction/check_box_gap_root.py` | 72 middle-slice vertices, 2,048 exact mixtures, 390 product contact-pair obstructions |

These finite checks supplement the written reconstruction. They do not prove uniform Bernstein approximation, implement a general GLS oracle, implement the entire certified root/curvature compiler, or certify all possible instances. I did not run a shared LaTeX build, inspect the complete frozen PDF, or conduct a solver-performance experiment. No manuscript, bibliography, coverage, research source, literature entry or other review was edited.
