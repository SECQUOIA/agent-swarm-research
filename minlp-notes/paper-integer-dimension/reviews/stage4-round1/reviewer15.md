# Reviewer 15: stage 4, round 1

Major findings: 0

Minor findings: 0

I found no concrete error, missing mathematical obligation, or materially misleading synthesis claim in the reviewed stage. The abstract, introduction and conclusion match the proved scope. In particular, they distinguish the exact growing-input product separation, the nonconvex scalar family, and the poorly conditioned tilted-body family from the unresolved one-input componentwise-convex box question. This is a bounded review verdict, not a guarantee of correctness or publication priority.

## Findings

None. I have not promoted optional changes in wording or organization to findings.

## Actual coverage

I read all 1,297 lines of `sections/04-vector.tex` and all of `abstract.tex`, `sections/00-introduction.tex`, and `sections/05-conclusion.tex`. I also read the task, protocol, process and lens instructions; checked the stage-4 coverage rows and final boundary inventory; inspected the bibliography additions against the previously reviewed bibliography; and checked `main.tex` and `macros.tex` for the actual assembly and notation.

The accepted sections 01–03 were dependencies rather than new review targets. I had reviewed each of those stages in full in the earlier rounds. For this round I revisited the definition of the two minima, the general-mixture and parity lemma, finite disjunction, scalar chord/packing bounds, indexed endpoint compilation, the mass-bisection implementation, the dense hybrid cell bound, Jensen superadditivity, and the scalar specialization of the rational block-logdet oracle. These are the interfaces used by stage 4. The accepted sections 01 and 02 retain the hashes from my prior reviews; section 03 has the accepted corrections.

I compared all ten canonical stage-4 results and all eleven explicitly substantive supporting developments listed in `coverage.md` with their manuscript locations. This included the original sources for the common overlay, box/facet/oracle rank transfer, unconditional allocation, both separable transfers, exact product counts, the nonconvex scalar family, arbitrary polynomial overlay, conditioning comparisons, finite separable companion, lattice investigation, hinge/Bernstein precursor, tilted body, positive-power refinement/scalarization obstruction and its source assessment, cap-set strengthening, three-witness argument, and rational polar-spanner oracle. The promoted nonconvex supporting pointer adds no distinct theorem. Alternate numerical constants for the same degree-32 mechanism are superseded, while the separate hinge and Bernstein stability mechanisms survive in the paper. I used the root audit as a list of issues to check, not as proof.

## Independent reconstruction

1. **Common partitions and the scalar interface.** The level-set argument yields at most $2H-1$ cells; strict levels, plateaus and singletons are compatible with its proof. Finite closed interval covers admit the stated farthest-reaching trimming procedure. Parity contacts provide endpoint midpoint bounds on their interval hulls by continuity, without requiring the original witness sets to be measurable or the lift to be closed. The resulting finite box and facet overlay constants follow.

2. **Implicit ordering and simultaneous containment.** Canonical mass evaluation at each fixed bisection node gives ordered target ranges for left, stop and right decisions. This proves monotonicity of that particular approximate inverse procedure, even if the approximate mass values themselves are not monotone. Reflection must reverse the local indices, as stated. A product of the polynomially many piece-endpoint denominators and one sufficiently large dyadic denominator provides a short common grid. Counting right endpoints at a grid numerator then gives exact order statistics with multiplicity. Every positive merged cell lies in a source cell of every array; repeated endpoints and the final endpoint have valid source-cell choices. All outputs use one input cell and interpolation weight.

3. **Original-output curvature bases.** Maximum determinants give coefficient bound one, and determinant-doubling exchange on rational original rows gives bound two with polynomial bit complexity. The signed coefficient bound works because the selected basis consists of convex original outputs with nonnegative chord gaps. I checked the finite factors $4r-1$ and $8r-1$, the compiled factors below $2^{12}r$ and $2^{13}r$, and the explicit facet band. Its center error is in $15K/32$, so its half-body band admits at most $31K/32$. Compact nonnegative-facet bodies have a positive entry in each column, which justifies the claimed affine rank-zero case.

4. **Direct unconditional allocation.** The maximum-product supporting inequality follows by differentiating a feasible segment. The approximate-product argument uses the nonnegative terms in the product expansion and treats dimension one separately; it supports the factor seven. The accepted scalar allocation oracle returns exactly feasible rational positive coordinates with polynomial reciprocal encoding. Thus the direct finite and compiled transfers have the stated $4m-1$ and $2^{14}m$ count factors, with an explicit inner box as the final band.

5. **Rational spanners and polar access.** I checked the seed determinant, cofactor and objective bounds, the fixed global grid, the central-ball repair and its additive objective loss. The repair gives exact feasibility; the fixed denominator prevents recursive coefficient growth over exchanges. Determinant growth bounds the number of exchanges, and stopping gives coefficient magnitude at most $9/4$. Support optimization followed by repair gives a feasible support point, from which the positive-polar procedure returns either a valid separator or a certified nearby feasible point. It does not assume a strong polar separator or exact polar membership. The positive polar has the required inner ball and spanning seeds. Pullback separation and the rational left inverse provide the stated effective-body radii. Padding to two dimensions handles the imported theorem's dimension convention.

6. **The band in the effective image.** Positive scalarizations control nonnegative vector gaps. The separate primal spanner provides $P\subset K\cap S\subset drP$. For exact bases the refinement factor gives $8r^2-1$. With the rational factor-three bases, scalar hybrid gaps lie in $13P/64$. Rounding effective coordinates adds only $P/16$, remains exactly in $S$, and gives center error $17P/64$. The explicit $P/2$ band contains the graph and admits $49P/64\subset K$. Affine terms are restored exactly. The count $486\cdot144r^2<2^{17}r^2$ and the compiler bounds are consistent.

7. **Separable vector reconstruction.** The concatenated basis uses the same representation coefficients in every input coordinate. Jensen superadditivity turns local index separation into a scalar midpoint gap, and a lattice-ball deletion argument compares the product packing with the original vector minimum. I independently recomputed the six per-coordinate capacity factors: $108r$, $180r$, $180r^2$, $87480r$, $157464r$, and $1277208r^2$. They imply the displayed finite and compiled constants. Total rounding is divided among active inputs, and every output shares each coordinate's index and interpolation weight. Removing affine-only coordinates is justified by nonnegative gap domination. No argument here silently substitutes multilinear interpolation for the supplied separated representation.

8. **Scalarization and cap-set limits.** For the positive powers, midpoint errors are below $7/8$, while the selected oriented thirds gap exceeds one by the stated rational lower bound. Modulo-three residues and equal binary assignments therefore give the two lower estimates. Range rectangles prove the finite upper and the separate signed-scalarization bound. Three zero-sum residues also force a forbidden average; the resulting cap-set reduction, monomial count and minimizing equation $4t^2+t-2=0$ are correct. The direct one-integer argument checks far-apart labels and then the entire middle section created by repeated convexification. None of these lower bounds is presented as a proved growing difference between the two optimum dimensions.

9. **Exact convex product counts and stability.** The three rational boxes contain the graph and satisfy their local errors. More importantly, every point in the middle integer section has weights $ (t,1-2t,t) $, a central input and outputs below one; this verifies all mixtures in that section. Oriented thirds incompatibility at the $3^n$ product contacts yields the exact general-integer and binary lower bounds. The rational upper constructions match them, with the unrestricted continuous size of the binary construction stated explicitly. The hinge precursor and Bernstein variance/second-difference proof preserve the distinct stability mechanism. Affine monotonicity shears preserve errors but do not make all monomial coefficients positive.

10. **Nonconvex family and signed overlay.** Bernstein approximation of the triangular wave gives the uniform $1/32$ error at degree $1024M^2$; the period integer and orientation binary encode the wave, including period boundaries. Peak contacts force distinct binary sections, and alternating peaks/troughs force actual degree to grow. The finite convexity-piece argument and rational root-bracket construction give the degree-dependent upper bounds. For the arbitrary vector overlay I checked all three source-cell gap ranges, the directed rounding, sign-dependent offsets, repeated endpoints and computed type flags. The flags are conditional Boolean wires, so they add no declared integers. The count remains bounded by $4096(\sum_j D_j)2^p$.

11. **Conditioning and the remaining boundary.** The tilted-body projection retains the scalar obstruction while the common output interval absorbs the convexifying quadratic. The second-difference identity forces the asserted radius ratio to grow at least as $8+60M^2$. The finite conditioning comparisons use only an outer bound on nonnegative midpoint errors and an inner ball for the final band. The Euclidean simplex estimate and unconditional normalization are valid, including the explicitly announced nonsymmetric extension. Strict upper-violation sets and their integer-coordinate projections are convex and lattice free; their union need not be. The discussion correctly separates mixed Helly certificates, integral Radon partitions and input ordering, rather than claiming these tools resolve the one-input question.

## Synthesis and source checks

The introduction's quadratic precision coefficient and finite covariance description agree with the accepted preceding stages. Its scalar discussion keeps the finite two-bit theorem separate from the dense rational eleven-bit theorem, and its power/sparse language does not extend the dense stage-4 oracle constructions to binary huge-degree inputs. The result roadmap refers to the appropriate statements. The conclusion preserves the open smooth, vector and encoding boundaries rather than claiming a full characterization.

I directly inspected the cached primary GLS text at Definition (5), Theorem (3.1), and Corollaries (3.4)–(3.5). The weak objective comparison is indeed with all of the exact body, with an explicit inner/outer-ball interface. I also inspected Ellenberg–Gijswijt Theorem 4, Averkov–Weismantel Theorem 1.1, and Lyu–Hicks–Huchette Proposition 1. They support the cap-set, mixed-Helly and shared-breakpoint attributions used here. The paper proves the new graph-transfer steps rather than relying on those sources to supply them. I did not independently re-audit every historical citation or undertake an exhaustive external priority search.

## Executed checks and limitations

The following existing checkers all exited successfully:

- `python code/quadratic_rank/check_implicit_knot_overlay.py`: 2,304 ordered-search checks, 60 exact order statistics, 180 source-cell containments, eight large implicit-grid rank queries and 99 directed-band checks.
- `python code/quadratic_rank/check_rational_polar_spanner_second.py`: 16 generic systems, 93 exact repaired optimizer calls, 11 exchanges, 120 full-image vertex checks and 347 positive-polar cases.
- `python code/quadratic_rank/check_separable_oracle_rank_precision.py`: 96 exact lattice-ball bounds and 1,536 separable rounding/band checks.
- `python code/positive_vector_obstruction/check_box_gap_root.py`: 72 middle-slice vertices, 2,048 exact integer-slice mixtures and 390 product contact-pair obstructions.
- `python code/quadratic_rank/check_polynomial_binary_integer_gap.py`: 12 exact Bernstein values at degrees 4,096 and 9,216, four peak-chord violations and 90 periodic MILP branch checks.
- `python code/quadratic_rank/check_coupled_separable_rank_review.py`: 24 shared bases, 31 determinant exchanges, 39 negative representation entries, 540 gap dominations, 300 box bands and 600 coupled-body errors.

These checks corroborate the reconstruction; finite examples do not prove the general oracle, quadrature or asymptotic statements. I did not run a shared LaTeX build or independently inspect every rendered page. This report assesses mathematical content and standalone source exposition, not final typography. It also does not replace the mandatory later whole-paper review. No manuscript, bibliography, coverage, research-source or other-reviewer file was edited.

## Snapshot verification

All eleven SHA-256 values were recomputed and matched the assigned snapshot. Paths are relative to `paper-integer-dimension`.

| File | SHA-256 |
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
