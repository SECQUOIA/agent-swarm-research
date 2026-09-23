# Stage 5, round 1 — independent review 11

**Verdict: PASS.** No major or minor defect found. In particular, the lifted order-one refinement is valid under the stated objective, graph-identity, and full-box quadratic-hull assumptions. The dimensional and order asymptotics retain the necessary restrictions.

## Coverage

I read all of the following frozen manuscript files, including every proof and scope paragraph:

- `process/snapshots/stage05-round01/sections/13-xor-quadratic-hulls.tex` (printed Section 16).
- `process/snapshots/stage05-round01/sections/14-monomial-reformulations.tex` (printed Section 17).
- `process/snapshots/stage05-round01/sections/15-finite-certificates-affine.tex` (printed Section 18).

The earlier dependencies inspected directly were the vertex-distribution and certificate-model portions of frozen `sections/01-foundations.tex`, all of frozen `sections/11-coordinate-domains-lifts.tex` and `sections/12-relative-blocks-cuts.tex`, frozen `macros.tex`, and the four new bibliography entries. In particular, I checked the incumbent/tolerance contract, the distinction between coordinatewise interpolation and multivariate monomial substitution, the clique-cut escape, and the treatment of discarded regions. Stage 5 adds no separate appendix proof requiring an additional dependency.

I read `process/review-protocol.md`, `process/stage-05-review-assignment.md`, `process/stage-05-author-assignment.md`, the complete author ledger `process/stage-05-author.md`, focus 11 in `process/stage05-reviewer-focus.json`, the Stage 5 scope rows, and `process/order-one-monomial-refinement.md`. I read all three mapped canonical sources and all four mapped correction/audit sources, in full, relative to the repository root:

- `results/spatial-bb-quadratic-cut-exponential-lower-bound.md`.
- `results/spatial-bb-monomial-lift-exponential-lower-bound.md`.
- `notes/spatial-bb-affine-branching-barrier.md`.
- `notes/review-spatial-bb-beyond-clique.md`.
- `notes/review-spatial-bb-beyond-clique-second.md`.
- `notes/review-spatial-bb-bounded-monomial-lift.md`.
- `notes/review-spatial-bb-affine-branching-barrier.md`.

These older audits supplied correction history, not proof authority. I read no peer report from this round, delegated no work, and edited no manuscript or literature file.

### Primary-source access account

I read `../literature/AGENTS.md` before inspecting originals. All four mapped primary originals were accessible. I checked their SHA-256 digests independently; they match `verification/stage05-primary-sources.json`. Exact digests are recorded in my `verification/reviewer11/stage05-round01/result.json`.

- **Schoenebeck, author full version of the FOCS 2008 paper:** `/tmp/minlp-relaxation-limits-sources/schoenebeck-full.pdf`. I read the complete 19-page extracted original, with separate reads of pages 6–11 and 12–19 to avoid truncated output. I directly inspected original renders of printed pages 7, 8, 10, and 11. The relevant source ingredients are the random distinct-variable model, Definition 10, Theorems 11–12, Lemma 13, and the appendix width proof. The source explicitly displays the unit constant vector and then prints an inconsistent norm-zero sentence; the manuscript correctly uses normalization one. The positive width constant is supplied by Theorem 11. The chosen denominator is positive. [Author full version](https://schoeneb.people.si.umich.edu/papers/LasserreNew.pdf).
- **Ahmadi–Dash–Hua–Stellato, arXiv 2605.28674v1:** local original `../literature/papers/ahmadi2026-disjunctive-sum-of-squares/original.pdf`. I read printed pages 1–4, 8, and 30–34 and visually inspected printed page 32. These cover the definitions, main fixed-degree theorem statement, cone/sphere and simplex region models, node bounds, and both positive-tolerance termination statements. I did not audit all proofs or experiments in that paper. [Inspected version](https://arxiv.org/abs/2605.28674v1).
- **Beame et al., arXiv 1710.03219v3:** `/tmp/stage05-author-sources/stabbing.pdf`. I read its abstract and introduction through printed page 4, including the integer-negation branching rule and Theorem 1, and visually inspected printed page 3. The theorem says quasipolynomial size for Tseitin, as reported here. [Inspected version](https://arxiv.org/abs/1710.03219v3).
- **Fleming et al., arXiv 2102.05019v2:** `/tmp/stage05-author-sources/branch-cut.pdf`. I read its abstract and introduction through printed page 4, including Theorems 1.1–1.4, and visually inspected printed page 4. The CNF-encoding qualification in Theorem 1.3 and the coefficient restriction in Theorem 1.4 are retained in the manuscript. [Inspected version](https://arxiv.org/abs/2102.05019v2).

I also opened the author PDF and the three version-specific arXiv pages on the web. No access control was bypassed. No source was missing. The original PDF renders I inspected are confined to my assigned verification directory. Two initial attempts to render with Python failed because `fitz` was unavailable; `pdftoppm` then succeeded. I did not independently rebuild the full paper or audit the author's claimed finite-run counts. The independent checks below are my own.

## Findings

None. No repair is required for acceptance of this stage within its stated model.

## Independent verification

### Transfer, positivity, and quadratic realizability

For Section 13's transfer, I reconstructed the functional by fixing the endpoint-excluding coordinates at the witness and marginalizing the remaining variables. This does not require a conditioning event of positive mass. If the sum of generator degrees is `a` and the square multiplier has degree `d`, then `a+2d<=2r` implies `a+d<=2r`. After endpoint interpolation, each nonzero product is a nonnegative multiple of an idempotent indicator `I` of degree at most `a`. Thus `I P^2=(I P)^2` in the Boolean quotient requires at most degree `4r`. Repeated factors and conflicting indicators satisfy the same identity. Constant factors consume no indicator degree. Every allowed local equality vanishes after reduction, also with its permitted multiplier.

The original actual quadratic law can be marginalized and fixed, preserving all required means, diagonal moments, and cross moments. Its finite endpoint support is inside the node even for nonclosed coordinate sets. This proves actual hull membership, which need not equal the intersection of valid closed halfspaces for a nonclosed domain. For compact boxes the stated separation equivalence is correct. Nothing in this proof supplies arbitrary products or localizers of coupled quadratic cuts.

The signed-moment realization lemma correctly includes the constant Gram vector. Signed classes are mutually orthogonal; orienting its class to have deterministic value one and assigning independent unbiased signs to the other classes realizes every augmented matrix entry. Treating the constant class as another unbiased sign would lose first moments, but the manuscript does not make that error.

For the width lemma, absence of opposite derived signs gives well-defined moments. On characters of size at most `floor(w/2)`, transitivity stays within width because the resulting symmetric difference has size at most `2 floor(w/2)`. The signed class vectors give the Gram identity and positivity for an arbitrary sum of monomials. Defining top-degree moments directly by the closure rule handles odd `w`. The two actual source requirements remain `4r<=w` and `4rD<=w`.

The affected-clause bound uses valid squares of degree at most six, and untouched clause means remain exact. The restriction count is region-dependent, whereas the chosen signs may depend on its witness; this suffices to bound every witness-containing region uniformly. The union bound requires no disjointness of regions and also treats graph-empty or witness-empty regions. The cover convention charges feasible regions discarded by propagation.

### Lifted order one and parity rank

In Section 14, literal pullback of a lifted polynomial of degree `s` costs at most `Ds`. For localizer data `a+2d<=2r`, the pulled-back indicator times multiplier has degree at most `D(a+d)<=2rD`; its square uses at most `4rD`. Both sides of the quotient identity remain available. Every multiplied polynomial graph identity pulls back to zero within degree `2rD`. Objective equality is a real polynomial identity, so it survives deterministic substitution.

The augmented lifted quadratic matrix is PSD because a lifted linear square pulls back to square degree at most `D`. Its entries use signed characters of degree at most `2D`, and its diagonal is one. The signed-class law therefore applies even with repeated or overlapping supports. Endpoint means force restricted lifted coordinates to their endpoints almost surely. The resulting law can leave the nonlinear graph, exactly as allowed by the full-box hull contract.

The affected-clause square degree is at most three before squaring. Integer `rD>=2` gives `2rD>=4>=3`; no additional `r>=2` premise occurs. At `r=1,D=3`, the objective is linear, both defining equations are quadratic, and source degree 12 suffices. The unlifted general cubic objective still needs node degree at least three, hence integer order at least two.

The witness equations form a consistent binary affine system. A basis selected from its actual rows has the same support union as all rows: a column absent from that basis cannot occur anywhere in its span. Consequently `|C|<=D rank(A_R)`, and its exact witness fraction is `2^(-rank(A_R))`. This handles arbitrary finite `N`, duplicate supports, auxiliary signs, and nonclosed coordinate sets. Counting restricted lifted coordinates without rank would not justify the result, but the proof uses rank throughout.

### Constants and asymptotics — focus 11

I independently obtained the fixed-assignment tail `exp(-2nt+nt^2)` and its value `exp(-n)` at `t=1`. The assignment union bound vanishes because `log(2)<1`. Differentiating the binomial generating function gives `48(1+3/n)^(8n-1)` for `E[D_i 2^D_i]`. The displayed deletion estimate and the integer comparison `384*3^24<2^64` are valid. Markov needs no independence between occurrence counts. Intersecting its success event with the two events of probability `1-o(1)` works for every sufficiently large integer `n`, not only for a subsequence.

Deletion leaves `7n<=m<=8n`, occurrence at most 64, and at least `n` violated clauses at every assignment. Multiaffinity extends the vertex optimum to the continuous cube, giving `OPT>=1/8`. Each best-incumbent target is at least `1/16`; worse incumbents cannot weaken either target. The exponents are exactly `7n/1024`, `7n/(1024D)`, and for `D=3`, `7n/3072`.

The pair-plus-clause representation has exactly `N=n+2m` coordinates and `2m` displayed quadratic equations, whether or not some equations are redundant. Thus `15n<=N<=17n`, and `7n/3072>=7N/52224`. Repeated clauses do not spoil equivalence or alter the degree bound. For arbitrary lifts no corresponding linear relation between `N` and `n` exists, and the manuscript correctly keeps its general exponent in original dimension.

One selected high-width functional can be restricted to every smaller required degree. Thus the family can be chosen before the node order, and the same instances work simultaneously for all admissible orders; lifts satisfying `4rD<=an` use that same input. The fixed-`D` linear-order constant may depend on `D`, as it must. The condition for a polynomial bound `C n^k` gives `7n/(1024D)<=log2(C)+k log2(n)`, hence the asserted necessary `D=Omega(n/log n)` within the available-degree regime. It is neither a sufficiency assertion nor a polynomial-in-arbitrary-`N` assertion. In particular, large `D` and large order cannot be increased independently under the source-width restriction.

The sensitivity calculation counts one first derivative and two mixed second derivatives per incident clause; the diagonal Hessian vanishes. Its symmetric absolute-row-sum bound proves the claimed spectral norm estimate.

### Both upper certificates and affine scope

For the Bernstein certificate, `M=ceil(3/epsilon)` is a positive integer for every `epsilon>0`, including `epsilon>3`; `h=2/M<=2epsilon/3` remains valid. Each clause oscillates by at most `3h/2`, so averaging separate clause minima loses at most that quantity. The eight-corner interpolation is an exact polynomial identity with nonnegative coefficients and three bound-slack factors. Order two supplies these cubic products and the degree-three graph-transfer identity. Only originals need subdivision.

For the separate order-one proof, I reconstructed `L[v]-a_i a_j a_k` by adding and subtracting `a_k L[u]`. The first difference is the expectation of `u(x_k-a_k)`, bounded by `h`; the second uses `L[u]=L[x_i x_j]` and is bounded by `2h`. All expectations have degree at most two. Neither graph equation is assumed pointwise under the realizing law. The displayed quadratic cut is nonnegative on the entire lifted box by those same pointwise bounds, and its exact identity uses only constant graph multipliers. It is therefore a direct valid order-one certificate, not a hidden cubic or graph-hull argument. At `epsilon=1/16`, both upper counts equal `48^n`; `OPT>=1/8` gives the stated relative certificate too.

For the affine examples, zero mean of a nonnegative `S` forces zero second moment, contradicting `E[S^2]=n`. The affine-coordinate cut gives the same contradiction. For the substitution localizer, `t<ceil(n/2)` supplies at least `t+1` free coordinates. If the fixed sum is nonnegative, the selected negative indicator has degree `a+1<=r-1` and yields exactly `-2^(-(a+1))`; negative fixed sum is already excluded by the constant multiplier. The `r=1` conclusion is correctly vacuous. These establish only the failure of the displayed preservation/substitution method.

The literature comparison retains continuous covering versus integer-negation branching, source-specific region and oracle types, coefficient restrictions, and quasipolynomial rather than polynomial upper bounds. A perfect-satisfiability refutation alone gives one violation and hence normalized `1/m`, not the fixed target. The text makes no unsupported transfer of those refutations or the disjunctive SOS convergence statements to the present constant-gap region count.

### Reproducible checks

Run:

```
/home/sgusev/miniconda3/envs/minlp-notes/bin/python verification/reviewer11/stage05-round01/check.py
```

The checker passes. It verifies three identities symbolically (Bernstein interpolation with denominators cleared, the cubic graph transfer, and the order-one quadratic certificate), 6,540 permitted finite degree-budget cases including order one, 2,048 exact rational full-box vertex cut evaluations on unequal and degenerate intervals, and the displayed constant arithmetic. Output is `verification/reviewer11/stage05-round01/result.json`. The symbolic identities are exact algebraic checks. The finite evaluations test their stated cases only; they do not establish asymptotic source existence or replace the universal arguments reconstructed above.

## Remaining limits

This review does not establish priority, computational tractability of the exact quadratic-hull oracle, or lower bounds for arbitrary affine branching, graph hulls, or products of coupled cuts. Those remain correctly separated from the claims. I did not audit all proofs of the three comparison papers, every earlier manuscript theorem, or a full rendered build. No unverified dependency needed for the Stage 5 transfer or its stated comparisons remains within that coverage.
