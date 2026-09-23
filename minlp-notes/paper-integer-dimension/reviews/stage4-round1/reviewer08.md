Reviewer 08 — stage4-round1, separable vector theory

Major findings: 0
Minor findings: 0

I found no concrete error, missing material hypothesis, proof gap, or omitted substantive stage4 development requiring correction. There are no numbered findings or unresolved questions in this report. This is a bounded no-findings assessment, not formal verification, an exhaustive priority determination, or a guarantee of correctness.

I read all 1,297 lines of `sections/04-vector.tex`, the entire abstract, introduction and conclusion, the bibliography, coverage inventory, task/lens instructions, process and protocol. I independently reconstructed the proofs and compared all ten canonical stage4 results and eleven explicit supporting developments with their manuscript locations. I previously reviewed accepted01–03 in full; for this stage I checked the accepted03 correction diff and the relevant parity, finite disjunction, scalar packing, hybrid count/compiler and allocation-oracle interfaces. The accepted03 changes make rational tolerances and affine data explicit and do not alter these proofs.

All eleven source hashes match the snapshot frozen at `2026-09-05T20:05:45.273919+00:00`:

| File relative to paper-integer-dimension | SHA-256 |
| --- | --- |
| abstract.tex | `db2b95f525fdfc786c9c24b46f41693892131a8103f249d27dbc012d53e323a3` |
| coverage.md | `d8b2ed835cfcdfac31b48197cd7a4da7c0e9bac0f73b2dfab6a3571d34a8e1cf` |
| macros.tex | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| main.tex | `026577c84ea4f9c0ff19361708694be45ce88a5a4e911a9b902852f826d1ba9c` |
| references.bib | `60fd73a2eec8fd2bc999cf2c407c6a571c590b087786c78647cc1bb7a59a1693` |
| sections/00-introduction.tex | `6940bf7c1017d82a8ea00af76575aa88da76f2ef26290b4b3872fd0bba152b16` |
| sections/01-foundations.tex | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| sections/02-quadratic-finite.tex | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| sections/03-scalar-nonlinear.tex | `8e271531b4c705a1333b49f170b20e987359ed5e7d1b05866030bccb69040803` |
| sections/04-vector.tex | `d9369569aa0711c3652dcf28929ea4be5884c534f18e371038fbdfc7edb6252d` |
| sections/05-conclusion.tex | `2bfb1f16aaa317e5b49dd171ccd9648c7a320343f23ec13acbf6a38b1955ad6e` |

My primary-lens assessment concerns `lem:vector-product-packing` and `thm:separable-vector-rank`, including their one-input and oracle dependencies. The rank is correctly taken in a single direct sum of coordinate function spaces modulo affine functions. A basis of concatenated original output rows gives the same representation coefficients in every coordinate. Consequently the sum of the selected original convex outputs controls each original summand's nonnegative chord gap despite signed basis coefficients. If the selected scalar summand is affine, the domination forces every original summand in that coordinate to be affine. This justifies removing inactive coordinates without spending integer variables. The facet version uses compactness and nonnegative weights to recover the same conclusion; the oracle version uses the common positive-polar image and effective span.

The product packing is against the original vector lift. For ordered scalar packings, Jensen superadditivity gives `J_Psi > tau ||u-v||_1` for distinct product contacts. Exceeding `r` forces one selected normalized original output, facet function or feasible polar function to exceed its admissible midpoint value one. The integer lattice deletion radius is `qn`, where `q=r/(n tau)`; its generating-function bound is `[3(2q+1)]^n`. The packings and deleted code are existence devices, not inputs to the constructive algorithm. Local finite and hybrid binary capacities are respectively at most `12 P_i` and `5832 P_i`, including one-cell and zero-bit cases.

Recomputing all six comparisons gives the following factors before taking logarithms:

| Model | Local tolerance | Safe packing factor per input | Capacity times packing factor |
| --- | --- | --- | --- |
| Finite box | `1/n` | `9r` | `108r < 2^7 r` |
| Compiled box | `1/(2n)` | `15r` | `87480r < 2^17 r` |
| Finite facets | `1/(2n)` | `15r` | `180r < 2^8 r` |
| Compiled facets | `1/(4n)` | `27r` | `157464r < 2^18 r` |
| Finite unconditional body | `1/(2rn)` | `15r^2` | `180r^2 < 2^8 r^2` |
| Compiled unconditional oracle | `1/(36rn)` | `219r^2` | `1277208r^2 < 2^21 r^2` |

These prove the six displayed count bounds. For the compiled box, summing the coordinate gaps gives at most `13/16` and summing endpoint rounding gives at most `1/8`; the directed band contains the exact graph and admits at most `15/16` error. For facets the center error is in `15K/32`, and the half-body band admits at most `31K/32`. For the oracle case both spanners are shared across all input blocks. Effective-coordinate rounding at accuracy `1/(16nrL_B)` stays in the common nonlinear image and contributes at most `P/16` after summation. Together with the gap `13P/64`, this gives center error `17P/64` and admitted error `49P/64`. Each coordinate has one index and one continuous interpolation weight serving every output; no independent output selectors are introduced. The claimed polynomial complexity is in the supplied dense separated representation and oracle/radius encoding. It is not a sparse multivariate or mixed-coordinate claim.

The rest of the stage was checked independently as follows:

- `lem:level-refinement` and the finite output overlays: strict superlevel cuts, plateaus, singleton hulls and trimming a finite cover preserve the required gap. The bounds `2m+1`, `8q+1`, `4r-1` and `8r-1` retain their distinct mechanisms. Coupled budgets correctly use symmetric half-body bands.
- `lem:implicit-overlay` and the convex/arbitrary polynomial compilers: the canonical fixed bisection tree is ordered in the target even when approximate mass values at different nodes are not ordered. Reflections reverse indices. A product of polynomially many fixed endpoint denominators and one largest dyadic denominator gives a short common grid. Counting right endpoints with multiplicity gives exact order statistics and containing source cells, including duplicate endpoints and the terminal input one. Signed source-cell flags select the proper rounding and band offsets. Bracket cells use a derivative bound that survives restriction. All components interpolate at the same input; invalid codes are excluded by the external index computation.
- `lem:curvature-spanner`: maximum determinants give coefficient bound one; rational exchanges give bound two with polynomially many exchanges and bounded inverses because every basis uses original rows. The selected functions remain convex. Rank-zero facet systems force every original component affine because each column of a compact nonnegative-facet description has a positive entry.
- `prop:vector-log-product`: the exact support inequality follows from the feasible segment derivative of the log product. An `e^-1` product approximation gives the factor seven by a nonnegative product expansion, with dimension one treated separately. Scaling the scalar allocation oracle by `R I` loses no positive feasible body point. Reciprocal scales have polynomial bit length, and the final bands describe an inner box rather than the original oracle body.
- `lem:rational-spanner` and `thm:vector-oracle-rank`: seed determinants and cofactors bound objectives uniformly. One grid and fixed repair weights keep denominators bounded through all exchanges. Weak optimization, rounding and central-ball repair give exactly feasible points with objective loss at most one quarter; stopping yields coefficient bound `9/4`. The positive polar has explicit inner/outer balls and independent feasible image seeds. Support optimization plus repair supplies a valid weak separator without assuming strong polar access. Dimension-one padding matches the imported GLS convention. Effective body coordinates need not be unconditional; positivity is used in the original output coordinates. The two-spanner band and all constants through `49P/64` are consistent.
- Positive-power obstructions: midpoint errors are uniformly below `7/8`, every normalized signed scalarization has a two-rectangle finite linear upper, and the selected thirds combinations have gap `2177/2144 > 1`. Distinct residues and fixed binary sections yield the different lower counts. The cap-set reduction excludes all nontrivial zero-sum triples, and the generating-function minimizer and base are correct. The direct three-witness proof handles arbitrary labels through both far-separated labels and repeated convexification in the middle section. These results do not establish a growing binary/general-integer gap in the one-input box model.
- Exact convex box separation: the rational box inequalities hold, and the proof checks the entire middle integer section with weights `(t,1-2t,t)`, not only pairwise original chords. Oriented thirds combinations and product contacts give exactly `n` general integers and `ceil(n log2 3)` binaries. The rational upper constructions and their different continuous-size scopes are explicit. The hinge precursor, Bernstein convexity-preserving stability and affine monotonicity shear remain present as distinct supporting mechanisms.
- Nonconvex and tilted examples: Bernstein's variance estimate gives the uniform `1/32` approximation, with polynomial dense rational encoding. Period and orientation give two general integers; full convexity of binary sections separates the peaks. The actual degrees grow and remain at most `1024M^2`, so the stated worst-case logarithmic-degree order follows. The tilted error-body projection retains the scalar lower bound, while the common quadratic is absorbed by an explicit continuous band. Its second-difference estimate gives the claimed growing radius ratio `8+60M^2`.
- Conditioning and open boundaries: the box and Euclidean refinements and the sharper simplex band control every admitted error, including for a nonsymmetric convex body containing the given central ball. Axis normalization of an unconditional body yields the stated inner crosspolytope. Strict upper-violation sets and their projections are convex and lattice free; their union need not be convex. The Helly and Radon discussion correctly identifies missing implications rather than claiming an impossibility theorem.

The ten canonical result files were all compared directly. The eleven explicitly substantive supporting notes were also read: finite separable rank; fixed-conditioning comparisons; the lattice investigation; the one-bit investigation; tilted-body gaps; the promoted nonconvex pointer; vector-refinement source assessment and obstruction; cap-set restriction; three-witness obstruction; and rational polar-spanner oracle. The alternate numerical constants in the one-bit investigation are legitimately superseded by the exact degree-32 product result; the separate hinge and Bernstein mechanisms survive. I did not reread every historical audit or predecessor derivation in the full dependency index, and old review verdicts were not used as proof.

The abstract, introduction and conclusion match the proved scope. They distinguish unrestricted convex integer minima from binary linear minima, finite existence from polynomial rational construction, and construction from solution complexity. The exact quadratic coefficient, finite covariance benchmark, scalar compiler guarantees and root-encoding separation agree with the accepted stages. The synthesis does not claim that the one-input convex box constant-gap question is solved by a growing-input product, a nonconvex scalar family, or a poorly conditioned tilted body. The mixed-coordinate vector and rank-changing smooth boundaries remain explicitly open.

For source verification, I directly inspected these primary passages:

- [Awerbuch–Kleinberg, Section 2.3, Propositions 2.2/2.4 and Observation 2.3](https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf): maximum-determinant spanners and determinant exchange are correctly credited. The manuscript supplies its own rational finite-row and repaired weak-oracle complexity arguments rather than silently importing an exact optimization oracle.
- Cached GLS1981, printed p172 Definitions (5)–(7), Theorem (3.1), and Corollaries (3.4)/(3.5): the weak optimizer compares its objective with every exact feasible point and gives Euclidean distance proximity under known inner/outer balls. The polar/anti-blocker predecessor scope matches the discussion.
- Cached Ellenberg–Gijswijt, Theorem 4 and Corollary 5: with field size three and coefficients all one, the theorem gives the monomial count used in the cap-set restriction. The manuscript derives its finite generating-function bound separately.
- Cached Averkov–Weismantel, Theorem 1.1, equation (3): the mixed Helly identity and its scope match the stated limitation of a proposed cover argument.
- Cached Lyu–Hicks–Huchette, Section 3, Proposition 1 and equation (4): the shared explicit breakpoint union and common SOS2 weights support the predecessor attribution; they do not supply the implicit-array bit-complexity theorem here.
- Cached Kelly–Maulloo–Tan, NETWORK and equations (1)/(2), and Plevrakis–Hazan, Section 3.2: these support proportional-fair allocation and approximate-optimization spanner credit. They are not used as proofs of the manuscript's complete graph-count comparisons.

These were targeted primary checks, not exhaustive publication-priority research. I did not independently retrieve every older source cited in the synthesis or verify every bibliographic field externally.

Executed checks:

| Command | Result |
| --- | --- |
| `python code/quadratic_rank/check_coupled_separable_rank_review.py` | PASS: 24 shared bases, 31 determinant exchanges, 39 negative representation entries, 540 gap dominations, 300 box bands and 600 coupled-body errors |
| `python code/quadratic_rank/check_separable_oracle_rank_precision.py` | PASS: 96 exact lattice-ball bounds and 1,536 coupled separable rounding/band checks |
| `python paper-integer-dimension/verification/check_manuscript.py --snapshot reviews/stage4-round1/snapshot.json` | PASS: 258 labels, 39 bibliography entries; no duplicate labels/keys, unresolved references/citations, or snapshot mismatches |

I inspected both focused checker implementations. They use exact rational arithmetic for the reported geometry and bands, but neither implements the complete quadrature/compiler or abstract convex-body optimization algorithm. Their passes supplement the proofs. Checker SHA-256 hashes, in table order, are `b1040a6701deb4cf0dce97754c3945ed73bf04253c0a5bd6200411fb9623bf6d`, `63b3e646cfa78ad0b60899d23637473fd28727b6964d09209aa5bcdb07484a68`, and `8c4f9ee8268c185f488a8b7fa1a72427791d47ecdd4441e5ed388d577d01fcbe`.

I did not run a shared LaTeX build, inspect every page of the frozen PDF, generate a complete compiled MILP, or perform formal proof verification. I edited only this assigned report and used no subagents.
