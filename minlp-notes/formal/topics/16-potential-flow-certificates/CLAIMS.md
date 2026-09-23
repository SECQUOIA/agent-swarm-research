# Deterministic potential-flow certificates: mathematical obligations

This frozen inventory covers the mathematical assertions of
[Appendix K, "Certified computation from rational witnesses"](../../../paper-potential-flow/complexity/sections/11-certified-computation.tex)
(`sec:a-cert`), together with its source result notes
[`potential-flow-envelope-bregman-certificates.md`](../../../results/potential-flow-envelope-bregman-certificates.md)
and [`potential-flow-envelope-rational-certificates.md`](../../../results/potential-flow-envelope-rational-certificates.md).

The already verified [potential-flow package](../03-potential-flow/README.md)
covers the model, the dual energy bound, the uniform cube-root flow radius,
and one saved rational example. Those statements are reused, not reproved.
This package covers the remaining mathematics of the same appendix:
separate-edge Bregman intervals, posterior endpoint-scenario recovery,
support certificates for linear goals with their completeness and
convergence, conservation-aware curvature certificates, the optimal
Laplacian factor with its zero-curvature obstruction, and the exact
two-path comparison example.

An obligation is discharged by an actual theorem with the stated hypotheses.
A numerically or symbolically plausible restatement does not discharge it.
`COVERAGE.md` maps every identifier below to Lean declarations and records
every difference between the source statement and the proved statement.
This inventory is not itself a completion claim.

Scope conventions, which apply to every entry:

- The network is the finite directed multigraph of `Formal/PotentialFlow/Network.lean`,
  including self-loops, parallel edges and disconnected graphs, with the
  asymmetric cubic energy `E_e(t) = c_e^{sgn t}|t|^3/3` and edge law
  `G_e(t) = c_e^{sgn t} t|t|`. All coefficients are strictly positive.
- `x*` always denotes the unique energy minimizer on `Ax = b`, equivalently
  the unique physical flow; its existence, uniqueness and potential
  characterization are the reused results of topic 3.
- Division and square roots are total in Lean. Hypotheses that the source
  leaves implicit (positive denominators, nonempty index sets, sign
  conventions at zero) must be stated explicitly where they are used.
- Boundary cases must be included: zero energy gap, zero flows, zero
  curvature edges, empty positive-curvature sets, `s_e = 0`, `C_* = 0`,
  ties, redundant conservation rows and singular potential gauges.
- A statement about supplied rational data is not a statement about a
  producer. Where the source asserts that data *can be constructed*, the
  construction itself must be exhibited and proved correct.

## Bregman intervals and enclosures

| ID | Required assertion | Source and material scope |
|---|---|---|
| CC01 | Define the edge divergence `D_e(y,z) = E_e(y) - E_e(z) - G_e(z)(y - z)` and prove it nonnegative, zero exactly at `z = y`, strictly decreasing in `z` on `(-inf, y]` and strictly increasing on `[y, inf)`. | `prop:a-cert-bregman` proof. The derivative `2 c_e^{sgn z}|z|(z - y)` vanishes at `z = 0`; strict monotonicity must still be proved on each side, including intervals containing zero. |
| CC02 | For feasible `y` and the physical flow `x*`, prove the exact identity `E(y) - E(x*) = sum_e D_e(y_e, x*_e)`, with every summand nonnegative, hence each summand at most any verified gap bound `delta`. | `eq:a-cert-bregman-sum`. Uses conservation and stationarity at `x*`, not an assumption that `y` is near `x*`. |
| CC03 | If `delta` bounds the energy gap, `l_e <= y_e <= u_e`, `D_e(y_e, l_e) >= delta` and `D_e(y_e, u_e) >= delta`, then `l_e <= x*_e <= u_e`. | `eq:a-cert-bregman-test`. Must hold per edge for arbitrary rational endpoints, including `l_e = u_e = y_e`. |
| CC04 | If the verified gap is zero then `x* = y`, so the singleton intervals are valid without any curvature hypothesis. | `prop:a-cert-bregman`, zero-gap case. |
| CC05 | The initial endpoints `y_e +- eta` from the verified uniform radius satisfy the endpoint test, so a bracket always exists. | `prop:a-cert-bregman` proof: `beta_L eta^3 / 6 >= delta`. |
| CC06 | Exhibit an exact rational bisection that, from a valid outer bracket, returns rational endpoints satisfying CC03 whose distance from the exact sublevel boundary is at most `eta 2^{-k}` after `k` steps, on each side. | `prop:a-cert-bregman` construction. Correctness and the accuracy recursion must be proved; the invariant that the retained outer endpoint keeps `D_e >= delta` is part of the obligation. |
| CC07 | The physical edge drop is enclosed by `[G_e(l_e), G_e(u_e)]` for verified intervals. | Paragraph after `prop:a-cert-bregman`. Monotonicity of the edge law. |
| CC08 | For a flow `q` with `Aq = a`, the potential objective satisfies `a^T pi = q^T G(x*)` for every potential vector `pi` of the physical state, so signed interval arithmetic over the support of `q` encloses it. | Same paragraph. The identity must be gauge independent. |
| CC09 | A nomination `a` admits some flow `q` with `Aq = a` exactly when `a` annihilates every potential vector with zero drops, which is the coordinate-free form of the componentwise zero-sum condition. | Same paragraph, "componentwise zero sums give the same statement". Disconnected graphs included. |

## Posterior endpoint-scenario recovery

| ID | Required assertion | Source and material scope |
|---|---|---|
| CC10 | Prove the scalar strong-monotonicity inequality `(G_e(u) - G_e(v))(u - v) >= beta_L|u - v|^3 / 2`, including opposite signs and zero. | `prop:a-cert-signs` proof; also stated in `prop:a-cert-energy`. |
| CC11 | With the selected endpoint coefficients `beta_e` chosen from the sign of `y_e`, verified intervals `[l_e, u_e]` containing `y_e` and `x*_e`, and `a_e` as defined in the source, prove the constitutive residual bound `|beta_e x*_e|x*_e| - G_e(x*_e)| <= r_e` with `r_e = (ubeta_e - lbeta_e) a_e^2`, where the envelope coefficients lie in `[lbeta_e, ubeta_e]`. | `prop:a-cert-signs` proof, first step. The envelope hypothesis enters only through coefficient membership and the selection rule; the envelope construction itself is out of scope. |
| CC12 | If `xhat` is the physical flow of the selected scenario law on the same nominations, then `||xhat - x*||_inf^2 <= (2/beta_L) sum_e r_e`. | `eq:a-cert-sign-error`. Both states are physical for their own laws; neither is assumed rational. |
| CC13 | Under the compatibility alternatives of `eq:a-cert-compatible`, prove exact equality `xhat = x*`, using uniqueness of the physical flow. | `prop:a-cert-signs`, exact-optimality case. All four alternatives, with non-strict signs and the zero-flow case. |

## Support certificates for linear goals

| ID | Required assertion | Source and material scope |
|---|---|---|
| CC14 | Define `S(y) = {x : Ax = b, E(x) <= E(y)}` and prove `x* in S(y)` for feasible `y`. | `thm:a-cert-support` preamble. |
| CC15 | For rational `lambda > 0`, `v`, `s = w - A^T v` and roots `R_e >= 0` with `R_e^2 lambda c_e^{sgn s_e} >= |s_e|^3`, prove `w^T x <= U_w` for every `x in S(y)`, with `U_w` as in `eq:a-cert-support`. | `thm:a-cert-support`, soundness. Real `x`, arbitrary graphs; no optimality of `y` assumed. |
| CC16 | Applying CC15 to `-w` gives the two-sided enclosure `[-U_{-w}, U_w]` of `w^T x*`. | `thm:a-cert-support`. |
| CC17 | For `lambda = 0`, prove that `w^T x` is constant, equal to `v^T b`, on `Ax = b` when `w = A^T v`; and conversely that `w^T x` is bounded above on `Ax = b` only if `w = A^T v` for some `v`. | `thm:a-cert-support`, `lambda = 0` case and the identification `(ker A)^perp = im A^T`. |
| CC18 | `S(y)` is nonempty, compact and convex, and `max_{x in S(y)} w^T x` is attained. | `thm:a-cert-support` completeness proof, coercivity. |
| CC19 | If `E(y) > E(x*)`, the infimum of the valid rational upper bounds `U_w` over all rational `(lambda > 0, v, R)` satisfying the checks equals `max_{x in S(y)} w^T x`. | `thm:a-cert-support`, completeness. Rational data and rational upward roots only; the real dual value must be shown attained and then approximated. |
| CC20 | If `w = A^T v` for rational `v`, the exact value is certified at `lambda = 0` with no roots. | `thm:a-cert-support`, constant-goal case. |
| CC21 | If `y_k` are feasible with `E(y_k) -> E(x*)`, then for every `rho > 0` the sets `S(y_k)` are eventually contained in the `rho`-ball about `x*`, and therefore the exact support intervals converge to `w^T x*` for every `w`. | `thm:a-cert-support`, final paragraph. Compactness and uniqueness argument, not a rate claim. |

## Curvature bounds and the constrained Laplacian

| ID | Required assertion | Source and material scope |
|---|---|---|
| CC22 | Define `h_e` by `eq:a-cert-curvature` from rational intervals `[l_e, u_e]` and prove the scalar Taylor bound `D_e(y_e, z) >= h_e (y_e - z)^2 / 2` whenever `y_e, z in [l_e, u_e]`. | `thm:a-cert-hessian` proof. The interval may straddle zero, in which case `h_e = 0`. |
| CC23 | With a verified gap `delta`, intervals containing `y_e` and `x*_e`, and any `v` with `s_Z = 0`, prove `(1/2) sum_e h_e (x*_e - y_e)^2 <= delta` and `|w^T(x* - y)| <= r` for every `r >= 0` with `r^2 >= 2 delta C(v)`, where `C(v) = sum_{e in P} s_e^2 / h_e`. | `thm:a-cert-hessian`, `eq:a-cert-quadratic-error`, `eq:a-cert-goal-radius`. Includes `P` empty and `delta = 0`. |
| CC24 | For `delta = 0` the goal is exact regardless of `h` and `s_Z`. | `thm:a-cert-hessian`, final sentence. |
| CC25 | The zero-edge condition `A_Z^T v = w_Z` is solvable exactly when `w_Z^T z = 0` for every `z in ker A_Z`, where `ker A_Z` means circulations supported on the zero-curvature edges. | `prop:a-cert-projection`, `eq:a-cert-zero-obstruction`. |
| CC26 | If that condition fails, the goal is unbounded on the quadratic error set `eq:a-cert-error-set`, for every `delta > 0`. | `prop:a-cert-projection`, obstruction case. Exhibit the unbounded family. |
| CC27 | When solvable, the minimum `C_*` of `C(v)` over admissible `v` is attained. | `prop:a-cert-projection`, least-norm argument. |
| CC28 | An admissible `v` attains `C_*` exactly when there is a circulation `d` with `Ad = 0` and `h_e d_e = s_e` on `P`; this is the matrix-free form of the stationarity system `eq:a-cert-kkt`, with `d_Z = -xi`. | `prop:a-cert-projection`, first-order optimality and its converse. The equivalence with `eq:a-cert-kkt` must be recorded in `COVERAGE.md`. |
| CC29 | With rational network data, `w` and `h`, some rational `v` attains `C_*`; singular gauges and redundant rows are allowed. | `prop:a-cert-projection`, rational exact elimination. Output rationality is the obligation; a bit-length model is not. |
| CC30 | For every `delta > 0` the supremum of `|w^T d|` over `eq:a-cert-error-set` equals `sqrt(2 delta C_*)`, and it is attained. | `prop:a-cert-projection`, sharpness. Includes `C_* = 0`, in which case every admissible circulation goal vanishes and `w = A^T v`. |

## Exact comparison on two long paths

| ID | Required assertion | Source and material scope |
|---|---|---|
| CC31 | Construct the two-path network of `ex:a-cert-paths` for every `L >= 1` and prove that the physical flow is one on every edge, with the stated integral potentials, path drops `L`, and uniqueness. | `ex:a-cert-paths`. An actual network instance is required, not an abstract stand-in. |
| CC32 | Prove that the conserved flows are exactly the path-constant vectors with values `t` and `2 - t`, and that the energy along this family is strictly convex, symmetric about `t = 1` and strictly increasing in `|t - 1|`. | `ex:a-cert-paths`, flow-space description. Must be derived from conservation on the constructed graph. |
| CC33 | For rational `0 < eps < 1` and the candidate `y` of the example, prove the exact gap `delta = 2 L eps^2`, including that the integral potentials with their rational conjugate roots give exactly this dual value. | `eq:a-cert-path-gap`. |
| CC34 | Prove `S(y) = {path values in [1 - eps, 1 + eps]}` and hence that the exact support interval of a first-path edge is `[1 - eps, 1 + eps]`, of width `2 eps`. | `ex:a-cert-paths`. |
| CC35 | Exhibit the explicit rational dual data of the example, verify the support checks, and prove that it attains `U_w = 1 + eps`; the symmetric choice gives the lower endpoint. | `ex:a-cert-paths`, rational attainment. Includes the potential-consistency identity `1 - lambda L(1 + eps)^2 = -lambda L(1 - eps)^2`. |
| CC36 | Prove the expansion `D_e(y_e, y_e + a) = y_e a^2 + 2a^3/3` for `y_e + a > 0`, that the two exact boundary displacements exist and are unique, and that the Bregman width divided by `eps` tends to `2 sqrt(2L)` as `eps -> 0+`. | `eq:a-cert-path-bregman`. An asymptotic statement at fixed `L`. |
| CC37 | Prove that the circulation space is one dimensional, that the optimal factor for a first-path edge selector is `C_* = 1 / sum_e h_e`, and that the optimized Laplacian width `2 sqrt(2 delta C_*)` divided by `eps` tends to `2` as `eps -> 0+` for the interval endpoints of the example. | `eq:a-cert-path-hessian`. `C_* = 1/(4L)` is the limit of the endpoint curvatures, not a claim at fixed `eps`. |
| CC38 | For `L = 1` and `eps = 1/10`, prove `D_1(11/10, 9/10) = 29/750 > delta = 1/50`, so a point of `S(y)` can violate a separate-edge physical Bregman constraint. | `ex:a-cert-paths` warning. Exact rational arithmetic. |

## Rational construction support

| ID | Required assertion | Source and material scope |
|---|---|---|
| CC39 | For nonnegative rational `a/b`, `k in {2,3}` and precision `q`, define `j` as the least nonnegative integer with `j^k b >= a 2^{kq}` and prove that `j/2^q` is an upper enclosure of the `k`th root whose excess is less than `2^{-q}`. | `eq:a-cert-root`. Used for conjugate roots, `eta` and the rounded support roots; no algebraic-number arithmetic. |
| CC40 | Assemble the new witnesses into exact decidable rational acceptance conditions whose acceptance implies the corresponding real conclusions about `x*`, in the style of the existing `RationalNetwork.Accepted`. | Verifier-facing summary of `sec:a-cert`. Decidability of the checks is part of the obligation. |

## Explicit exclusions

These are outside the package and must not be described as verified:

- The envelope mapping from an original uncertainty instance: graph tests,
  resistance intervals, target selection, and the pipeline of
  `sec:a-cert`'s final two subsections. Topic 3 excluded these as well.
  CC11 assumes coefficient membership and the selection rule as hypotheses.
- The spanning-tree conservation repair and its rounding-convergence
  estimate, which are producer-side constructions.
- Machine-level bit-complexity claims: "polynomial-time verification",
  "polynomial bit time" and "polynomial output bit length". The verified
  content is correctness, termination and the exact accuracy or size
  recursions of the constructions in CC06 and CC39, following the scope
  already recorded for topic 3. No counted bit-cost model is claimed.
- The effective-resistance restatement `eq:a-cert-effective` and its
  Moore-Penrose form, which rewrite the verified `C_*` of CC27-CC30.
- Numerical producers, conic solvers, JSON parsers and the Python modules,
  and any claim that a solver attains its stopping tolerance.
- Bibliographic priority. The appendix itself credits Bregman divergences,
  Fenchel duality, primal-dual a posteriori bounds and the electrical
  cut/cycle projection as classical.
