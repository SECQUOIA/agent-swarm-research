# Author report: algebraic singletons and degree (Section 06, Appendix E)

Date: 2026-10-05. Author: Opus main writer for the `algebraic` topic.
Files written (and only these, plus this report):

- `sections/06-algebraic.tex` (statements, motivation, proof outlines; about
  10 pages in a scoped test build)
- `appendices/E-algebraic.tex` (complete proofs; about 23 pages)

No shared macro, `main.tex`, `references.bib`, other author's file, or
historical note was edited.

## 1. Shared labels defined here

| Label | Content and contract |
| --- | --- |
| `lem:quartic-realization` | Generic assembly. Point `p` in R^n (arbitrary real, need not be known); rational quadratics `g, r_1..r_m` vanishing at `p`; expansions `g(p+u)=l'u+u'Hu`, `r_j(p+u)=b_j'u+u'T_ju`; positive rationals `mu, Lambda, beta, nu` with `H >= mu I`, `norm H <= Lambda`, `norm T_j <= 1`, `norm b_j <= beta`, `sum b_j b_j' >= nu^2 I` (eq. `eq:algebraic-realization-data`); rational `t>0`, `eps=t^2 <= min{1, mu^2/(2m), nu^2 mu^2/(36 n (Lambda+m beta)^2)}`, `norm l <= eps` (eq. `eq:algebraic-realization-eps`). Conclusions: `f=(g/(t nu))^2+sum (r_j/nu)^2` has degree exactly four, `m+1` rational squares, PD quartic form; Hessian `>= (3/2) I`; unique zero/minimizer `p`; canonical Hessian Gram `Gamma_f` rational with `Gamma_f >= gamma I`, `gamma = min{3/2, 2mu^2/(eps nu^2)} / (((1+theta)^2+1)(1+norm p)^2)`, `theta = 3 sqrt(n) eps (Lambda+m beta)/mu^2`. Computing `Gamma_f` uses `O(m(n+n^2)^2)` rational operations; **no approximation of `p` and no projection** (canonical Gram covariance). The factor `n` in the last eps bound is needed only for the Gram. |
| `thm:singleton-field` | Equivalence for real `alpha`: (i) one real conjugate; (ii) coordinate of the single real zero of some rational polynomial; (iii) coordinate of a singleton defined by finitely many rational convex inequalities; (iv) coordinate of the unique minimizer of a rational convex polynomial; (v) coordinate of the unique zero of a rational quartic with `n+1` rational quadratic squares, Hessian `>= I`, PD rational full Hessian Gram. Constructive in time polynomial in the dense coefficient list (via `thm:algebraic-dimension`, `n=(d+1)/2`). |
| `lem:one-real-conjugate` | (Architecture item E1.) Zero-set case and rational-convex-inequality case; complete embedding-extension argument (odd `[K:Q(p_j)]`). |
| `thm:sos-length` | Real SOS length `>= n+1` for globally convex degree-exactly-4 `f` with a zero and PD Hessian there; sharpness and necessity of each hypothesis. |
| `thm:quadratic-graph` | Certified quartic `(f,A)`, promised `min f = 0`; poly-time rational quadratics satisfying `lem:quartic-realization` at `(p,(p_i p_j)_{i<=j})` in `N=n+n(n+1)/2` variables; `N+1` squares (least real number). Uses `lem:convex-value` (points) once, for an approximate minimizer; no second approximation. |

Topic labels defined (selection others may cite): `lem:algebraic-gram`
(canonical Gram identity and translation covariance, matrix identity
`Gamma_S(g)=Psi_c' Gamma_S(g(.+c)) Psi_c`), `eq:algebraic-canonical`
(definition of `Gamma, Delta, Xi`), `lem:algebraic-block-bounds`,
`prop:algebraic-bivariate`, `cor:algebraic-three-quadrics`,
`thm:algebraic-dimension`, `thm:algebraic-cyclic`, `prop:algebraic-network`,
`thm:algebraic-degree-bounds`, `prop:algebraic-node-bound`,
`lem:algebraic-bivariate-descent`, `ex:algebraic-seven`,
`lem:algebraic-weighted-count`, `lem:algebraic-flat`,
`prop:algebraic-residual`, `prop:algebraic-positive-base`,
`thm:algebraic-univariate`, `lem:algebraic-roots`,
`lem:algebraic-cyclic-point`, `lem:algebraic-cyclic-data`,
`lem:algebraic-rank-one`, `rem:algebraic-cyclic-ellipsoids`,
`tab:algebraic-degrees`, `sec:algebraic*`, `app:algebraic*`.

Interfaces requested by other owners and now available:

- Fields: the minimal-dimension/bivariate descent interface is
  `lem:algebraic-bivariate-descent` (degree-four rational `f(x_1,x_2)`,
  nonnegative, one real zero, PD quartic form, hence rational SOS; every
  certified bivariate quartic with minimum zero qualifies). The fixed-field
  block padding can take the four-coordinate realization of
  `(a,a^2,a^3,a^4)`, `a=2^(1/5)`, from `thm:algebraic-dimension` with
  `d=5`, `n=4`. Covariance is `lem:algebraic-gram`(b).
- Reductions/heights/fields already cite `lem:quartic-realization`,
  `eq:algebraic-realization-data`, `eq:algebraic-realization-eps`,
  `eq:algebraic-canonical`, `lem:algebraic-gram` with exactly the parameter
  names above (checked by reading their current drafts).
- Contrast (Appendix J) may cite `cor:algebraic-three-quadrics` for the
  span-three singleton of unbounded degree.

## 2. Labels referenced from other owners

`sec:reductions`, `sec:heights`, `sec:fields`, `sec:upper` (section labels),
and `lem:convex-value` (points). Required contract of `lem:convex-value` for
`thm:quadratic-graph`: for an explicit rational convex polynomial on an
explicit rational box, a rational point in the box with value gap at most a
given rational `eta`, in time polynomial in input length and `log(1/eta)`.
Strong convexity with the explicit modulus `det A/(tr A)^(h-1)` then converts
the value gap into distance. All these labels resolve in the current tree.

## 3. Macros

No new macros are needed. The files use only `macros.tex` commands and
standard `\operatorname`, `\mathsf`, `\mathcal`, `\mathbb` (including
`\mathbb F` from amssymb), `\widetilde`, `\widehat`.

## 4. Citation keys needed (none are in `references.bib` except the first two)

Please have Luna verify each primary statement and theorem number; the exact
contract used is given in Appendix E.

| Key | Source | Contract used |
| --- | --- | --- |
| `SlotSteurerWiedmer2025` (exists) | Hesse's Redemption, arXiv v1 | Table 1 open rational-witness question for convex quartics; Appendix C sextic. **Version-specific; reconcile with STOC 2026 proceedings.** |
| `AhmadiChaudhryZhang2024` (exists) | Higher-order Newton | Prior Schur-complement / PD Hessian Gram technique for SOS-convex regularization (credit only). |
| `BasuPollackRoy2006` | Basu, Pollack, Roy, Algorithms in Real Algebraic Geometry, 2nd ed., Springer 2006 | Tarski-Seidenberg transfer to real algebraic numbers (cited as Thm 2.80, Cor 2.83; verify numbering). Heights uses `BasuPollackRoy1996`; root should unify. |
| `MehlhornSagraloffWang2015` | J. Symbolic Comput. 66 (2015) 34-69 | Theorem 5: certified isolation/refinement of all complex roots, polynomial bit complexity. |
| `Schonhage1982`, `Pan2002` | Schönhage 1982 preprint "The fundamental theorem of algebra in terms of computational complexity"; V. Pan, J. Symbolic Comput. 33 (2002) | Alternative sources for the same root-approximation contract. Optional. |
| `Hartshorne1977` | Algebraic Geometry, GTM 52 | Prop I.7.1, I.7.2, Thm I.7.7 (dimension and Bézout for hypersurface sections). |
| `Fulton1998` | Intersection Theory, 2nd ed. | Prop 8.4 / Ex 8.4.6 (zero-dimensional CI length), Prop 4.1 (Segre class of regular embedding), Ch. 9 (residual intersection). Verify numbers. |
| `EisenbudGreenHarris1996` | Cayley-Bacharach theorems and conjectures, Bull. AMS 33 (1996) 295-324 | CB5 (reduced CI) and CB7 (residual subschemes, nonreduced allowed). **Verify theorem labels and that CB7 covers arbitrary residual subschemes of a zero-dimensional CI.** The historical notes used EGH 1993 (Astérisque 218) pp. 195-197 for the same statements. |
| `Eisenbud1995` | Commutative Algebra, GTM 150 | Gorenstein duality of Artinian graded complete intersections (Ch. 21). |
| `EklundJostPeterson2013` | J. Algebra Appl. 12 (2013) 1250142 | Thm 3.2: generic residual count for a scheme defined by forms of one degree (unsaturated allowed), with lci Segre class. **Verify hypotheses (pure dimension, generation in degree 2).** |
| `Harris1992` | Algebraic Geometry: A First Course, GTM 133 | Def 18.1 (degree), Prop 18.9 / Cor 18.12 (minimal degree curves), Ex 1.16 (rational normal curve ideal by quadrics). Verify numbers. |
| `Hatcher2002`, `Milnor1965` | Algebraic Topology; Topology from the Differentiable Viewpoint | Degree: homotopy invariance, local degree formula (Hatcher Prop 2.30), Sard (Milnor §3). |
| `Tutte1948` | Proc. Cambridge Philos. Soc. 44 (1948) | Directed matrix-tree theorem. |
| `vanAardenneEhrenfestDeBruijn1951` | Simon Stevin 28 (1951) | BEST theorem (Euler circuits = tau times product of factorials), with loops/parallel arcs. |
| `ArratiaBollobasSorkin2004` | The interlace polynomial of a graph, JCTB 92 (2004) 199-233 | q_H(1)= number of Euler circuits of the 2-in 2-out digraph; q_H(2)=2^m; nonnegative integer coefficients, no constant term. **Verify loops are allowed and the circuit-counting convention.** |
| `BalisterBollobasCutlerPebody2002` | European J. Combin. 23 (2002) 761-767 | Thm 1: q(H;-1) = (-1)^rk 2^(m-rk), rk = rank over F_2 of A_H + I. Verify sign convention. |
| `EisenbudSturmfels1996` | Binomial ideals, Duke Math. J. 84 (1996) | Credit only: characters/lattice description of binomial solution sets. |
| `BorweinErdelyi1995` | Polynomials and Polynomial Inequalities, GTM 161 | Markov inequality on an interval (cited as Thm 5.1.8; verify). |
| `Scheiderer2016` | Sums of squares of polynomials with rational coefficients, JEMS 18 (2016) 1495-1513 | **Contract (Sch):** a nonnegative rational ternary quartic form that is not a sum of squares of rational quadratic forms is a product of four complex lines with no three concurrent. Only this is used (in `lem:algebraic-bivariate-descent`). The prewrite audits state the classification this way; it must be checked against the paper's exact theorem. |
| `KurdykaSpodzieja2015` | Convexifying positive polynomials and sums of squares approximation, SIAM J. Optim. 25 (2015) | Credit only: convexifying multipliers. |
| `LoncParolWojciechowski2001` | Networks 37 (2001) 129-133 | Credit only: grounded determinant of the directed square cycle. |

Suggested additional comparisons for Luna/root (not cited in my prose):
Scheiderer's work on SOS length of forms (for `thm:sos-length`); prior
irrational convex singletons and root-interpolation constructions (for
`thm:singleton-field`); Motzkin-Straus style complex-root degree obstructions
(for `thm:algebraic-univariate`(c)). No novelty claim is made in the files.

## 5. Coverage (coverage map rows)

| Row | Where |
| --- | --- |
| S1 | `prop:algebraic-bivariate`: integer quartic, analytic `4124 I`, zero set, printed integer canonical Hessian Gram `Gamma_F` (6x6) proved PD by covariance and an explicit Schur bound, and the printed 21-square `4096 I` certificate (`N_F` and margins). |
| S2 | `lem:one-real-conjugate`, `thm:singleton-field` (necessity with active constraints and the odd-degree extension step; sufficiency); `cor:algebraic-three-quadrics` (three rational ellipsoids in `d-1` variables, polynomial time). Remark on `sqrt 2` for constrained optimizers; unconstrained convex minimizers included as (iv). |
| S3 | `lem:quartic-realization` + `thm:algebraic-dimension` with `n=d-1`. |
| S4 | `thm:algebraic-dimension` for every `(d+1)/2 <= n <= d-1`, with the converse `k >= (d+1)/2` for the prescribed power point only. |
| S5 | `thm:algebraic-cyclic` (field degree, `(1/2,2)^n`, `O(log n)` bits, `O(n^2)` monomials, integer PD canonical Gram, local condition number `<= 65600 n^2`, translated minimal polynomial with all `d_n+1` coefficients nonzero and `Theta(d_n^2)` length); `rem:algebraic-cyclic-ellipsoids`. |
| S6 | `lem:algebraic-rank-one` and the `n+1` integer squares in `thm:algebraic-cyclic`; `thm:sos-length`. |
| S7 | `prop:algebraic-network` (lattice count, non-Eulerian bound, interlace bound, weighted energy, minimal-binomial normal form). |
| S8 | `thm:algebraic-degree-bounds`(a),(b); `ex:algebraic-seven` (with a hand-checkable F_2 squaring table). Also the new `prop:algebraic-node-bound` (`2*3^(n-1)-1` without square factors) and the bivariate `D<=3` for convex quartics via `lem:algebraic-bivariate-descent`. |
| S9 | `thm:algebraic-degree-bounds`(c) via `prop:algebraic-residual` and `prop:algebraic-positive-base`, with external contracts (AG1)-(AG7) listed in `app:algebraic-imports`. |
| S10 | `thm:algebraic-univariate`(a),(b) and the fixed-centre counterexample remark. |
| S11 | `thm:algebraic-univariate`(c),(d), including the finite-system and unconstrained-objective versions and the quasiconvex contrast. |
| B3 | `thm:quadratic-graph`. |

Not written here by decision: A1 (`prop:reductions-sums` exists in 04),
P9 (points), Q4 and other Q rows (Appendix J). The architecture's
`cor:algebraic-sums` is therefore not defined.

## 6. Response to prewrite audits

`prewrite-algebraic.md`:
- §1 Necessity: full embedding-extension argument included; constrained
  `sqrt 2` caution included; unconstrained minimizers handled as a separate
  item (iv) through the gradient zero set.
- §2 Bivariate: analytic proof reproduced and rechecked by hand (all numeric
  bounds, `d_1,d_2` intervals, the `1031/6250000` constant, the coefficient
  bound `755983876 < 2^30`). The 4096 certificate is printed as `N_F` with its
  margins (D6); in addition I added a new full canonical Hessian Gram
  `Gamma_F`, whose entries I computed by hand and cross-checked against all
  18 Hessian coefficients recorded in the historical rational-certificate
  note, with an analytic positivity proof.
- §3/§4 Lemma with `m` residuals and the `n` versus `m` factors kept
  distinct; negative `T_j (x) T_j` retained. Covariance proved as a matrix
  identity (three contraction identities) in `lem:algebraic-gram`; the
  approximation/projection route is not used anywhere.
- §5 Both routes: I replaced the companion route for the quartic by the
  `(T-alpha)P(T)(1+T^2)^e` Gram route for every `n` in `[(d+1)/2, d-1]`
  (covers `d-1`), and use the companion pencil only for the three-ellipsoid
  corollary, with a self-contained margin on `U = ker l_alpha'`. Corrected
  separation exponent `d-1` in `nu` and division of every residual by `kappa`
  are used. Certified root approximation is an imported lemma
  (`lem:algebraic-roots`).
- §6-§8 Cyclic family: uniform proofs; `O(n^2)` conditioning; `Theta(d^2)`
  translated length; sparse caution (auxiliary primitive element) kept in the
  prose as "short circuit or radical output is not excluded".
- §9 Network: included with the exact conditions (all `m` equations, full
  lattice index, odd index).
- §10 Conditioning: cyclic part included; circle part belongs to heights.
- §12-§13 Degree bounds and five variables: reconstructed in full; the
  residual-scheme parity argument keeps nonreduced factors; positive-base case
  list complete (including combinations, handled by choosing one sub-base).
- §14 SOS length: full proof with the uniform properness estimate.
- §15 Univariate: index renamed `k`; constants renamed to avoid clashes.
- §16 Graph lift: covariance simplification adopted; approximate minimizer via
  `lem:convex-value` instead of a direct external SSW import.
- §17 Node bound and bivariate classification: included as
  `prop:algebraic-node-bound` and `lem:algebraic-bivariate-descent`. I proved
  the node bound by splitting each double point into two simple points with a
  small constant perturbation, so only the isolated-point weighted Bézout count
  is needed (no multiplicity version of refined Bézout). The bivariate degree
  bound is stated under global convexity (or a PD quartic form), which needs
  only the no-three-concurrent part of Scheiderer's classification; the
  stronger unconditional `n=2` statement in the audit would need the Galois
  `A_4/S_4` part of the classification and is not claimed.

`prewrite-descent-criterion.md`: `thm:sos-length` matches its Theorem 1. The
descent criterion itself and its finite cyclic stationary-space diagnostics
belong to fields; nothing in my files claims `J_4 = W` for the cyclic family.

`prewrite-sos-fields.md` §5, §10: covariance and the shorter graph proof are
implemented as described.

## 7. Response to the fresh Sol R1 findings (relayed by root)

1. Graph lift wording (06, graph subsection): the claim that `g_hat p`
   "vanishes exactly at `w_*`" read as a zero-set statement and was wrong
   (the zero set is an ellipsoid). Now: `g_hat p(w_*)=f(p)=0` exactly for
   every rational `hat p`, which is what the assembly lemma uses; the gradient
   at `w_*` is bounded by a constant multiple of `norm(hat p - p)`. The
   appendix proof already used only the value.
2. Cyclic input length (06, after `thm:algebraic-cyclic`): replaced
   `L=O(n^2 log n)` and `2^Omega((L/log L)^(1/2))` by the safe certified-input
   accounting `L=O(n^4 log n)` (dense exponent vectors and the full canonical
   Hessian Gram of order `n+n^2` included), giving list length
   `2^Omega(n)=2^Omega((L/log L)^(1/4))`, superpolynomial but not exponential
   in `L`; the construction is stated as polynomial time in `n`.
3. (AG3) restricted: `N>=3`; residual identity only for integers
   `0<=t<=s`; `h^1(I_R(k))=length(R)-H_R(k)` only for `k>=0`, with its
   one-line cohomological proof; usage recorded (reduced form for `n>=3`,
   residual form only for `n>=4` with `t=2`, `s-t=n-3>=1`).
4. Quadric surface: (AG6) now states the general minimal-degree bound for
   irreducible nondegenerate varieties of any dimension (`deg >= r-k+1`,
   Harris Cor. 18.12), and the case analysis derives "spans a real P^3 and is
   a quadric there" from it; smoothness is proved from rank three versus four
   (a rank-three quadric has a unique, hence real, vertex). The conic case also
   cites (AG6) for spanning a plane. Luna should confirm Cor. 18.12 is stated
   for varieties of arbitrary dimension.
5. (AG5) rewritten: reduced pure-dimensional local complete intersection,
   explicitly not necessarily smooth (example: reduced singular curves that
   are complete intersections of type (1,1,2,2)), `I_Y(2)` globally
   generated; the count of points outside `Y` (local lengths) equals
   `32 - integral of (1+2H)^5 cap s(Y,P^5)`, with `s(Y,P^5)=c(N)^-1 cap [Y]`
   for lci `Y`. Luna is verifying the exact Fulton/EJP contract.
6. Intro item (iv) now carries the single-real-zero and PD-Hessian hypotheses.

Scope is unchanged: every S row, B3 and E1 remain fully covered.

## 8. Corrections and deviations from the historical notes

1. No second approximation/projection for rational Grams anywhere
   (power, cyclic, graph); the canonical Gram is computed from the factors.
2. Generic lemma uses one Schur argument for both the Hessian bound and the
   Gram (the Hessian bound follows from the Schur complement).
3. Power realization generalized to all `(d+1)/2 <= n <= d-1` by padding with
   `(1+T^2)^e`; the historical `d-1` companion construction is replaced.
4. Three ellipsoids now reuse the rational vanishing matrix of the power
   construction and a direct margin estimate on `ker l_alpha'`.
5. Weighted Bézout count stated once (`lem:algebraic-weighted-count`) with the
   strengthened form `#isolated + sum over positive components <= initial
   weight`, which gives the weight-four argument directly.
6. Univariate (a) is derived from the effective (b).
7. The cyclic theorem is stated for the compressed `n+1`-square quartic; the
   `n+2` baseline appears as the representation before compression.

No error was found in the audited historical results.

## 9. Open items for root

- External contracts in §4 must be vetted (especially Scheiderer, EGH CB7,
  EJP Thm 3.2, ABS with loops). If any contract differs, the affected results
  are: `lem:algebraic-bivariate-descent` and the `n=2` clause of
  `prop:algebraic-node-bound` (Scheiderer); `thm:algebraic-degree-bounds`(b)
  second bound and (c) (EGH, EJP, Harris); `prop:algebraic-network` Eulerian
  bound (interlace identities).
- Unify `BasuPollackRoy1996` (heights) and `BasuPollackRoy2006` (mine).
- Small overfull boxes (< 4pt) remain at four places in Appendix E.

## 10. Checks actually run (targeted; not CI)

- Scoped compile: a test document in `/tmp/algtest` inputting `macros.tex`,
  `sections/06-algebraic.tex`, `appendices/E-algebraic.tex`, compiled twice
  with `pdflatex -interaction=nonstopmode` (rerun after each revision,
  including the R1 repairs). Result: no LaTeX errors; 34 pages;
  four overfull boxes under 4pt; undefined citations (keys above) and, before
  the other files existed, the five external section/lemma labels.
- `python3 verification/check_manuscript.py` (read-only): no undefined
  references, duplicate labels, unfinished-text or repository-path findings
  involving my files; the global errors are missing bibliography keys of all
  authors (pending Luna's `literature.bib`).
- `grep` scans of my files for review/repository/checker/Lean wording: none
  in prose.
- Inspection of a recorded exact diagnostic: the Lean source
  `formal/ConvexQuarticIrrationalZero.lean` (`hessianGapSOS`,
  `hessian_sos_identity`) to confirm the exact form of the printed 21-square
  identity. I did not rerun Lean, any checker script, or any experiment.
- All mathematical verification in this report is analytic, by hand.
