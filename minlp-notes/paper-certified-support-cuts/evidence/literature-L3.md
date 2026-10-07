# Literature lane L3: rigorous relaxations, safe cuts, certificates, Bernstein and ball bounds, expression domains

Date: 2026-10-03. Lane: L3. Claims in scope: C-SUP, C-BERN, C-SCREEN, N4, N6.
Notes on C-AGG, C-IMPL, N1–N3 and N5 appear only where an L3 source bears on them.

This is a targeted search, not a proof of novelty. "Not found" means not found in
the local knowledge base (KB) and in the web searches listed in Section 9.

## 1. Main conclusions

1. **N4 is partially anticipated. Each ingredient has direct prior art.**
   - A numerically chosen affine function followed by a rigorous final shift is
     explicit in Garloff, Jansson and Smith (2003, JCAM), Section 5. They state that
     the approximate LP solution "need not" be verified; only the shift must be
     rigorous.
   - Garloff and Smith (2008), Section 5, also run the bulk computation in plain
     floating point and only the first and last steps rigorously.
   - Neumaier and Shcherbina (2004, p. 294) choose cuts in floating point and then
     repeat the derivation rigorously. They note that the bound is valid "for the s
     actually used, independent of its construction".
   - Requiring the exact machine coefficients to be valid is Definition 2 of
     Borradaile and Van Hentenryck (safe estimators with floating-point slope and
     intercept).
   - Bound-corrected rounding after aggregation is in Neumaier–Shcherbina
     (pp. 292–293), Cook–Dash–Fukasawa–Goycoolea (2009, §3.3), and
     Eifler–Gleixner (2024, Lemma 1, Corollary 2).
   - Certificates checked against the original instance are VIPR
     (Cheung–Gleixner–Steffy 2017), as used in exact SCIP. Neumaier–Shcherbina
     (p. 289) already require that safe bounds be computed for the raw LP, not for a
     presolved one that contains unjustified rounded substitutions.
   - **What was not found** is the combination for nonlinear joint-support cuts
     inside a MINLP solver: (a) a whole-domain certificate for the exact exported
     binary64 row of a *vector* of nonlinear functions, (b) safe rounding after
     source-side elimination, and (c) fresh-process replay bound to the archived
     source model and to the row actually stored by SCIP.
   - The closest MINLP precedent, Liers et al. (2021), mentions only "safe rounding
     of coefficients" without specification (preprint p. 25; Appendix 7.2, step 5).
     SCIP 10's exact mode is restricted to MILP (Hojny et al. 2025, §3.1, p. 7).
   - **Framing:** present N4 as an integrated certification contract built from
     established safe-cut techniques, not as a new principle.
2. **N6 is partially anticipated.**
   - Neumaier (2004, Acta Numerica, §20) states the problem: modeling systems
     introduce uncontrolled rounding when they translate floating-point constants
     and presolve.
   - Schichl and Neumaier (2005, §3.1) warn that constant folding in a validated
     context must not introduce roundoff.
   - Domain-aware expression semantics exist: Vigerske (2013) Definition 7.6
     (`domerr`); IEEE 1788-2015 decorations.
   - The positivity hypothesis behind x^y = exp(y log x) is stated by Belotti et al.
     (2009): without it, points with x_j = 0 are excluded. SCIP 8's benchmark setup
     bounds the arguments of log and negative powers away from zero by 1e-9 and
     reports a bound for the modified problem (Bestuzheva et al., §3.2.1).
   - The witness du = 1 for d ≠ 0 is the classical Rabinowitsch device.
   - **Not found:** an MINLP importer that symbolically checks the solver-submitted
     expression DAG against exact binary64 source semantics, without tolerance, and
     preserves strict and nonzero domains through exact existential witnesses.
   - **Framing:** N6 is a modest implementation-level contribution. Present it as
     translation validation (Pnueli et al. 1998; Necula 2000) applied to model
     import.
3. **C-SUP and C-BERN are anticipated in substance.**
   - The support/hull duality is classical.
   - The final-row validity proposition is a direct specialization of Garloff,
     Jansson and Smith (2003, §5), Garloff and Smith (2008, §5), and Domes and
     Neumaier (2012, Theorem 6.1).
   - Exact rational Bernstein enclosures with fully covered subdivision exist in a
     formally verified, proof-producing form: Muñoz and Narkawicz (2013, PVS), and
     Kodiak (Smith et al. 2015).
   - Ball arithmetic is Arb (Johansson 2017).
   - The chord correction is the classical linear-interpolation remainder, the same
     quantity as the αBB maximum-separation bound with α = M/2.
   - The paper should claim the binding of exact expression, domain, partition,
     and exported row, not the enclosure methods.
4. **C-SCREEN is standard convex geometry.** Hölder's inequality and dual-norm
   distance (Mangasarian 1999, Theorem 2.2) give the bound. Tawarmalani's (2010)
   inclusion certificates are the conceptual relative. Using it as a checked skip
   test for cut separation was not found, but this is minor.
5. **Bibliography fixes are needed** (Section 6):
   - The key `GarloffJanssonSmith2003` in Reports A and B points to the
     *Computing* 70(2) paper (inclusion isotonicity). The "rigorous shift without
     verifying the LP" statement is in the *J. Comput. Appl. Math.* 157(1) paper.
   - Andrew Smith's thesis is from 2012, not 2009.
   - SCIP 8's journal volume is 2025, although the article appeared online in 2023.
6. **A concrete technical fact justifies C-IMPL's stored-row replay.**
   - In SCIP 10.0 (tag v10.0.0, matching the installed SCIP 10.0), `colAddCoef`,
     `colChgCoefPos`, `rowAddCoef` and `rowChgCoefPos` in `src/scip/lp.c` round a
     coefficient that is integral within epsilon when exact mode is off. They do not
     adjust the side (e.g., `lp.c` lines 1870–1872).
   - `rowprepCleanupIntegralCoefs` in `misc_rowprep.c` relaxes the side with a
     variable bound when one exists. Otherwise it "only round[s] coef (introduces an
     error)" (line 441).
   - The paper can cite this source code as the reason the submitted row must be
     re-read from SCIP and checked.

## 2. Method and read-scope legend

- Local KB: grep over `literature/index.md` and `papers/*/fulltext.md`, using about
  70 author names and phrases (safe, rigorous, directed rounding, VIPR, Bernstein,
  interval, domain, x/x, …). I read the relevant full-text passages. Page locators
  for KB texts are the `<!-- page N -->` markers, i.e. PDF pages of the stored
  version, unless a journal page is stated.
- Web: author pages, arXiv, Optimization Online, institutional repositories, the
  Crossref API for metadata, and the GitHub SCIP repository. Reading copies were
  extracted with `pdftotext -layout` into a temporary directory outside the
  repository. Hashes are in Section 9; the copies were deleted after this review.
- Read-scope tags:
  - **[FT]** full-text passages read (sections/pages given);
  - **[PT]** partial full text (keyword search plus short passages);
  - **[AB]** abstract or metadata only;
  - **[KB-S]** KB summary only (not re-read here).

Theorem numbers are given only where I read them. For preprints, numbering may
differ from the journal version; this is noted where relevant.

## 3. Works by topic

### 3.1 Safe LP/MILP bounds, safe cuts, exact MIP and certificates

**Neumaier, A., Shcherbina, O. (2004). Safe bounds in linear and mixed-integer linear programming. *Math. Program.* 99(2):283–296. doi:10.1007/s10107-003-0433-3.** [FT, KB `neumaier2004-safe-bounds-in-linear-and`; journal pagination]
- Establishes:
  - Rigorous LP lower bounds from approximate duals, using directed rounding and
    variable bounds (§3, pp. 286–288).
  - Certificates of infeasibility (§4, pp. 288–290).
  - Safe cuts (§5, from p. 290).
  - Safe aggregation: the computed aggregated row is shifted by a rigorously
    enclosed residual times the variable bounds (pp. 292–293).
  - Safe MIR and generalized Gomory cuts with a rigorous correction term
    (pp. 294–295).
  - p. 294: candidate cuts may be chosen in floating point and the derivation then
    repeated rigorously, since "the bounds are valid for the s actually used,
    independent of its construction".
  - p. 289: if presolve contains rounded substitutions, the bounds "must be applied
    to the raw linear program and not to the reduced version".
- Relation:
  - Foundational precedent for C-SUP (numerical choice, rigorous final check).
  - Foundational precedent for the C-AGG export rule (bound-corrected aggregated
    row; our Prop. elimination-round is its lower-row form).
  - Precedent for N4/N6 (bind the check to the raw model).
  - Linear rows only; no nonlinear support.
- Anticipates: partial (N4 ingredients; C-SUP principle).

**Jansson, C. (2004). Rigorous lower and upper bounds in linear programming. *SIAM J. Optim.* 14(3):914–935. doi:10.1137/S1052623402416839.** [AB; cited in Neumaier–Shcherbina p. 289 and Kearfott 2011 §4]
- Establishes: rigorous LP bounds, including problems with unbounded variables.
- Relation: background for safe LP bounds. Our row checks do not need LP bounds.
- Anticipates: none.

**Cook, W., Dash, S., Fukasawa, R., Goycoolea, M. (2009). Numerically safe Gomory mixed-integer cuts. *INFORMS J. Comput.* 21(4):641–649. doi:10.1287/ijoc.1090.0324.** [FT §§1–3, pp. 641–644, author PDF]
- Establishes:
  - Defines a safe cut-generation process (p. 641).
  - F-representable inequalities, i.e. rows whose coefficients are floating-point
    numbers.
  - Directed rounding via `fesetround`.
  - §3.3 "Safe row aggregation" (p. 643): with x ≥ 0, round the aggregated
    coefficients down; equalities with negative multipliers must first be relaxed
    to inequalities of the right sense.
- Relation:
  - Direct precedent for the requirement that the exact exported coefficients be
    valid (C-SUP Prop. round).
  - Direct precedent for safe aggregation and export (C-AGG). Linear MIP only.
- Anticipates: partial (rounding component of N4).

**Applegate, D., Cook, W., Dash, S., Espinoza, D. (2007). Exact solutions to linear programming problems. *Oper. Res. Lett.* 35(6):693–699. doi:10.1016/j.orl.2006.12.010.** [AB]
- Establishes: exact rational LP solving (QSopt_ex) by precision boosting.
- Relation: background for exact verification.
- Anticipates: none.

**Steffy, D. E., Wolter, K. (2013). Valid linear programming bounds for exact mixed-integer programming. *INFORMS J. Comput.* 25(2):271–284. doi:10.1287/ijoc.1120.0501.** [AB; described in Eifler–Gleixner 2023, p. 5]
- Establishes: the project-and-shift safe dual bound.
- Relation: background.
- Anticipates: none.

**Cook, W., Koch, T., Steffy, D. E., Wolter, K. (2013). A hybrid branch-and-bound approach for exact rational mixed-integer programming. *Math. Program. Comput.* 5(3):305–344. doi:10.1007/s12532-013-0055-6.** [AB; context from Eifler–Gleixner 2024 §1, KB p. 2]
- Establishes: the first general exact MIP solver for rational input. It combines
  symbolic and numeric computation with safe dual bounding.
- Relation: the exact-MIP paradigm whose nonlinear analogue the paper would partly
  provide.
- Anticipates: none (MILP only).

**Cheung, K. K. H., Gleixner, A., Steffy, D. E. (2017). Verifying integer programming results. In: IPCO 2017, LNCS 10328:148–160. doi:10.1007/978-3-319-59250-3_13. arXiv:1611.08832.** [AB (arXiv); VIPR rules as described in Hojny et al. 2025, KB p. 10]
- Establishes:
  - VIPR, a certificate format of sequentially checkable statements with a few
    inference rules: conic combinations, MIR-type rounding, and disjunction
    "unsplitting".
  - An independent checker.
- Relation:
  - The model for "replay against the original instance" (N4).
  - VIPR has no nonlinear derivation rule; our support certificates would need a
    new rule, "this row is valid on this domain for this expression".
- Anticipates: partial (replay concept of N4), MILP only.

**Eifler, L., Gleixner, A. (2023). A computational status update for exact rational mixed integer programming. *Math. Program.* 197(2):793–812. doi:10.1007/s10107-021-01749-5. arXiv:2101.09141.** [FT pp. 5–6, 8, 13, KB `eifler2023-…`]
- Establishes:
  - Rational input data with a floating-point approximation (p. 6).
  - Safe dual bounds by bound-shift, project-and-shift, or exact LP (pp. 5–6).
  - Running error analysis for safe feasibility checks (p. 8).
  - VIPR certificates (p. 13). Presolving must be disabled when certificates are
    written, because PaPILO does not produce certificates (p. 13).
- Relation:
  - The "rational source, float approximation" convention differs from ours, where
    the binary64 leaf *is* the source value.
  - The presolve exclusion parallels our statement that SCIP's later
    simplification and presolve lie outside the binding claim (N6).
- Anticipates: partial (N6 boundary concept), MILP only.

**Eifler, L., Gleixner, A. (2024). Safe and verified Gomory mixed-integer cuts in a rational mixed-integer program framework. *SIAM J. Optim.* 34(1):742–763. doi:10.1137/23M156046X. arXiv:2303.12365.** [FT §1, §2.2–2.3, §2.5, KB `eifler2024-…` arXiv PDF, pp. 2–3, 7–8, 10]
- Establishes:
  - Lemma 1 (p. 7): making a rational valid row F-representable by bound-dependent
    relaxation.
  - Corollary 2 (p. 8): safe aggregation of two F-representable rows with
    0 < λ ∈ F.
  - Safe slack back-substitution "exactly as an aggregation according to
    Corollary 2" (p. 10).
  - Lemma 3: safe scaling.
  - VIPR verification of MIR cuts, plus a completion tool for weakly dominated
    rows (§3).
- Relation: this is the closest precedent for C-AGG's safe export after
  elimination (Prop. elimination-round). That proposition is the lower-row form of
  Lemma 1 applied after exact elimination.
- Anticipates: partial (rounding/export component of N4; C-AGG export).

**Borst, S., Eifler, L., Gleixner, A. (2024). Certified constraint propagation and dual proof analysis in a numerically exact MIP solver. arXiv:2403.13567.** [PT, KB pp. 2–3]
- Establishes: safe-rounding activity-based bound propagation and dual proof
  analysis in exact SCIP, certified in VIPR.
- Relation: direct precedent for C-IMPL's "affine bound propagation with
  provenance" (Prop. affine-bounds). Our rule (row, side, target, previous and new
  bounds, replay) is the same activity argument, recorded outside VIPR.
- Anticipates: partial (C-IMPL bound provenance).

**Hojny, C., Besançon, M., Bestuzheva, K., Borst, S., et al. (2025). The SCIP Optimization Suite 10.0. arXiv:2511.18580.** [FT §3.1, KB pp. 7–10]
- Establishes:
  - SCIP 10 offers an exact solving mode "restricted to mixed-integer linear
    programs" (p. 7).
  - The exact readers parse all coefficients and bounds as rationals (p. 8).
  - Only Gomory mixed-integer cuts are separated in exact mode (p. 9).
  - VIPR certificates cover the B&B process "except presolving" (pp. 7, 10).
- Relation:
  - Confirms that no exact or certified nonlinear mode exists in SCIP 10. This is
    important context for N4.
  - The decimal-to-rational parsing convention differs from our binary64-exact
    convention for PySCIPOpt-submitted data.
- Anticipates: none for nonlinear cuts.

**Hoen, A., Gleixner, A. (2025). Analyzing the numerical correctness of branch-and-bound decisions for mixed-integer programming. In: CPAIOR 2025, LNCS 15763:35–50. doi:10.1007/978-3-031-95976-9_3.** [KB-S]
- Establishes: retrospective exact checks of floating-point B&B decisions in MIP.
- Relation: motivation (floating-point MIP decisions can be wrong).
- Anticipates: none.

### 3.2 Rigorous linear relaxations for nonlinear problems

**Borradaile, G., Van Hentenryck, P. (2005). Safe and tight linear estimators for global optimization. *Math. Program.* 102(3):495–517. doi:10.1007/s10107-004-0533-8.** [FT §§2–3 of Brown Univ. Tech. Report CS-03-11, June 2003; journal version not read]
- Establishes, in tech-report numbering:
  - Definition 2: a *safe* linear overestimator is a valid estimator m*x + b* whose
    coefficients m*, b* lie in the floating-point set F.
  - Rounding m and b outward naively is not safe in general (Fig. 1).
  - Theorem 1: class-1 safe estimators, by sign cases on the interval.
  - Theorem 2: class-2 safe estimators anchored at a tangency or secant point.
  - Tightness results (Theorems 3–6) and a multivariate combination.
- Relation:
  - Direct precedent for C-SUP Prop. round: validity must hold for the exact
    machine coefficients.
  - They derive safe coefficients analytically for univariate estimators. We
    certify arbitrary exported coefficients a posteriori, over the whole domain,
    for a vector of functions.
- Anticipates: partial (C-SUP Prop. round; N4 ingredient).

**Hongthong, S., Kearfott, R. B. Rigorous linear overestimators and underestimators. Technical report, Univ. of Louisiana at Lafayette (undated; cited by Kearfott 2011 as ref. [18]).** [AB (search abstract)]
- Establishes: rigorous estimation and rounding for powers, reciprocals, exp, log,
  sqrt, and uncertain scalar multiples in GlobSol.
- Relation: background for elementary-function relaxations.
- Anticipates: none.

**Kearfott, R. B., Hongthong, S. (2005). Validated linear relaxations and preprocessing: some experiments. *SIAM J. Optim.* 16(2):418–433. doi:10.1137/030602186.** (Erratum: *SIAM J. Optim.* 21(1):415–416, 2011.) [AB]
- Establishes: experiments with validated linear relaxations.
- Relation: background.
- Anticipates: none.

**Kearfott, R. B. (2011). Interval computations, rigour and non-rigour in deterministic continuous global optimization. *Optim. Methods Softw.* 26(2):259–279. doi:10.1080/10556781003636851.** [FT §4.1–4.5 of the 18 Jan 2010 preprint, pp. 11–13]
- Establishes:
  - Two places need rounding control in linear relaxations: (1) the coefficients of
    the estimators, via directed rounding so that the stored machine numbers give
    valid estimators (citing Borradaile–Van Hentenryck and Hongthong–Kearfott);
    (2) the LP bound, via Neumaier–Shcherbina.
  - Rigorous convex relaxations are "not yet actually documented or tried" (§4.3).
  - Interval constraint propagation is cheap to make rigorous.
- Relation: survey-level precedent for the overall rigour agenda. It states the
  exact-coefficient requirement behind C-SUP.
- Anticipates: partial (principle only).

**Lebbah, Y., Michel, C., Rueher, M., Daney, D., Merlet, J.-P. (2005). Efficient and safe global constraints for handling numerical constraint systems. *SIAM J. Numer. Anal.* 42(5):2076–2097. doi:10.1137/S0036142903436174.** and **Lebbah, Y., Michel, C., Rueher, M. (2005). A rigorous global filtering algorithm for quadratic constraints. *Constraints* 10(1):47–65. doi:10.1007/s10601-004-5307-7.** [AB; cited in Neumaier 2004 §20 and Domes–Neumaier 2010/2016]
- Establishes: QUAD, an RLT-style linear relaxation with safe (rounding-controlled)
  LP use for filtering quadratic systems.
- Relation: precedent for safe linear relaxations of quadratic constraints
  (C-POLY/C-STAR context; rigour component).
- Anticipates: none of N1–N6 directly.

**Domes, F. (2009). GloptLab — a configurable framework for the rigorous global solution of quadratic constraint satisfaction problems. *Optim. Methods Softw.* 24(4–5):727–747. doi:10.1080/10556780902917701.** [AB; described in Domes–Neumaier 2010, KB pp. 2–3]
- Establishes: a MATLAB environment for rigorous quadratic CSPs, with directed
  rounding throughout.
- Relation: system precedent for rigorous quadratic processing.
- Anticipates: none.

**Domes, F., Neumaier, A. (2010). Constraint propagation on quadratic constraints. *Constraints* 15(3):404–429. doi:10.1007/s10601-009-9076-1.** [FT, KB author manuscript, pp. 2–3, 15]
- Establishes:
  - Directed-rounding bounds for univariate quadratics and for bilinear
    elimination.
  - Coefficients are allowed to vary in narrow intervals, to account for
    "conversion errors from an original representation to our normal form, and
    rounding errors when creating new constraints by relaxation" (p. 15).
- Relation: precedent for N6's concern with conversion errors. Their remedy is
  interval coefficients; ours is exact binary64 semantics plus a symbolic check.
- Anticipates: partial (N6 problem statement).

**Domes, F., Neumaier, A. (2012). Rigorous filtering using linear relaxations. *J. Global Optim.* 53(3):441–473. doi:10.1007/s10898-011-9722-1.** [FT §1.4 and §6 of author preprint `linearcsp.pdf`; Theorem 6.1 at manuscript p. 17]
- Establishes: Theorem 6.1. If p(x) ∈ c implies h(x) ∈ d on a box, then
  h − p ∈ [d̲ − c̲, d̄ − c̄] there. Linear relaxations of quadratic constraints are
  then obtained from rigorous enclosures of the difference. All steps use directed
  rounding (§1.4).
- Relation: this is C-SUP's "choose a linear function, enclose the remainder
  rigorously over the box" for a single quadratic constraint.
- Anticipates: partial (C-SUP mechanism, single function).

**Domes, F., Neumaier, A. (2016). Constraint aggregation for rigorous global optimization. *Math. Program.* 155(1–2):375–401. doi:10.1007/s10107-014-0851-4.** [FT abstract, §1, §3, §3.1 eqs. (31)–(34) of the R2 manuscript MAPR-D-14-00182R2 from the author page, manuscript pp. 2–3, 12–14]
- Establishes:
  - An aggregator y (or (ν, y) with the objective) forms the redundant constraint
    uᵀF(x) ∈ yᵀb, with interval coefficient uncertainty bounded rigorously (32).
  - Approximate Lagrange multipliers from a local solve serve as aggregators.
  - The aggregate is then used for rigorous box filtering and for certificates of
    infeasibility (§3.1).
- Relation, for C-AGG and lane L2:
  - Nonnegative aggregation of *original nonlinear* constraints with numerical
    multipliers, made rigorous, is established.
  - Their output is box reduction, not a linear original-variable cut with a
    certified global lower bound of the aggregate.
  - They give no closure theorem.
- Anticipates: partial (C-AGG mechanism); none for the N3 closure.

**Domes, F., Neumaier, A. (2015). Rigorous verification of feasibility. *J. Global Optim.* 61(2):255–278. doi:10.1007/s10898-014-0158-2.** [AB]
- Establishes: verified feasible points for upper bounds.
- Relation: background for "numerical incumbent checks are not exact
  certificates" (C-EXP wording).
- Anticipates: none.

**Ninin, J., Messine, F., Hansen, P. (2015). A reliable affine relaxation method for global optimization. *4OR* 13(3):247–277. doi:10.1007/s10288-014-0269-0.** [FT abstract and §4 of the Optimization Online preprint, 23 Oct 2012, pp. 10–12]
- Establishes:
  - Automatic linear relaxations from affine arithmetic forms (AF1/AF2;
    Propositions 3.1–3.2).
  - A reliable version uses rounded interval arithmetic ("reliable affine
    arithmetic"), so all rounding errors move into error variables.
  - The resulting LP is bounded rigorously with Neumaier–Shcherbina (p. 12).
  - Tested on 74 COCONUT problems.
- Relation:
  - Precedent for a fully automatic, rounding-safe relaxation pipeline over a
    factorable grammar (C-SUP/C-BERN context).
  - Different mechanism: per-operation affine forms, not joint support with a
    whole-domain certificate.
- Anticipates: partial (rigorous automatic relaxation), none for vector support
  or replay.

**Neumaier, A. (2004). Complete search in continuous global optimization and constraint satisfaction. *Acta Numerica* 13:271–369. doi:10.1017/S0962492904000194.** [FT §20, KB author manuscript pp. 63–64]
- Establishes, §20 "Rigorous verification and certificates":
  - "Rounding in the problem definition": translating problems with floating-point
    constants into internal formats, and presolve, introduce uncontrolled rounding.
    No modeling system then allowed control.
  - Rigorous LP via Neumaier–Shcherbina; certificates of infeasibility; certified
    upper bounds need existence proofs.
- Relation: the clearest prior statement of the problem N6 addresses, and of the
  N4 agenda.
- Anticipates: partial (problem statement for N6/N4).

**Neumaier, A., Shcherbina, O., Huyer, W., Vinkó, T. (2005). A comparison of complete global optimization solvers. *Math. Program.* 103(2):335–356. doi:10.1007/s10107-005-0585-4.** [AB (author page)]
- Establishes: testing of global solvers on more than 1000 problems. Reliability
  failures are documented (as summarized in Neumaier 2004 §20).
- Relation: motivation.
- Anticipates: none.

**Messine, F., Trombettoni, G. (2019). Reliable bounds for convex relaxation in interval global optimization codes. *AIP Conf. Proc.* 2070:020050. doi:10.1063/1.5090017.** [AB (metadata only)]
- Establishes: per the title, reliable bounds for convex relaxations in interval
  codes.
- Relation: possible precedent for rigorous non-LP relaxations; not read.
- Anticipates: unknown; low risk for N4 (different objects).

### 3.3 Bernstein enclosures and verified polynomial bounds

**Garloff, J., Jansson, C., Smith, A. P. (2003). Lower bound functions for polynomials. *J. Comput. Appl. Math.* 157(1):207–225. doi:10.1016/S0377-0427(03)00422-9.** [FT Theorem 3.1 and §5 "Verification", in Konstanzer Schriften Nr. 185, Feb 2003, pp. 3–4, 8–9]
- Establishes:
  - Theorem 3.1: affine lower bound functions from Bernstein control points via an
    LP. Section 4 gives error bounds.
  - §5: rigorous Bernstein coefficients (via Fischer and Rokne). For the affine
    bound, compute a rigorous lower bound δ of the minimum slack (32) by interval
    arithmetic and shift. "It is not necessary to verify the feasibility or
    optimality of the approximate solution ŝ of the linear programming problem …
    We have only to add the constant δ" (p. 9).
- Relation: the most direct precedent for C-SUP's "numerical direction, certified
  final bound" and for C-BERN's Bernstein certificate (single polynomial, one box).
- Anticipates: partial to full for the C-SUP principle in the polynomial case.

**Garloff, J., Jansson, C., Smith, A. P. (2003). Inclusion isotonicity of convex–concave extensions for polynomials based on Bernstein expansion. *Computing* 70(2):111–119. doi:10.1007/s00607-003-1471-7.** [AB; this is the entry under key `GarloffJanssonSmith2003` in Reports A/B]
- Establishes: inclusion isotonicity under domain shrinkage.
- Relation: less relevant to C-SUP than the JCAM paper above.
- Anticipates: none.

**Garloff, J., Smith, A. P. (2008). Rigorous affine lower bound functions for multivariate polynomials and their use in global optimisation. In: Proc. 1st Int. Conf. on Applied Operational Research, Lecture Notes in Management Science 1:199–211.** (Also Konstanzer Schriften 250.) [FT abstract and §5 of the author PDF, pp. 8–9]
- Establishes:
  - Least-squares affine bound functions from the Bernstein control points.
  - §5, rigorous version: interval Bernstein coefficients, then least squares on
    midpoints in plain floating point, then a rigorous downward shift. "Step 2 (the
    bulk of the computation) does not need to be performed rigorously" (p. 9).
- Relation: same principle as above (C-SUP, C-BERN).
- Anticipates: partial.

**Garloff, J., Smith, A. P. (2007). Guaranteed affine lower bound functions for multivariate polynomials. *PAMM* 7(1):1022905–1022906. doi:10.1002/pamm.200700501.** [AB]
- Relation: short version of the rigorous affine bound idea.
- Anticipates: partial (same as above).

**Muñoz, C., Narkawicz, A. (2013). Formalization of Bernstein polynomials and applications to global optimization. *J. Autom. Reasoning* 51(2):151–196. doi:10.1007/s10817-012-9256-3.** [PT, KB author draft: §2.3 pp. 7–8, completeness discussion p. 11, strategy input grammar pp. 36–38]
- Establishes:
  - A formal PVS development of multivariate Bernstein enclosures and recursive
    subdivision (subdivided coefficients computed from the parent).
  - Proof-producing strategies for polynomial inequalities over boxes with
    rational constants.
  - A subdivision procedure that is complete for strict inequalities under fair
    variable selection, but not for nonstrict ones (p. 11).
- Relation:
  - Covers C-BERN's "exact rational Bernstein with complete subdivision coverage"
    in a stronger, formally verified form. The PVS kernel checks coverage of the
    box.
  - Our contribution is the binding to the solver row and the exported coefficients.
- Anticipates: full for the Bernstein/subdivision core of C-BERN.

**Smith, A. P., Muñoz, C. A., Narkawicz, A. J., Markevicius, M. (2015). A rigorous generic branch and bound solver for nonlinear problems (Kodiak). In: SYNASC 2015, IEEE, pp. 71–78. doi:10.1109/SYNASC.2015.20.** [KB-S]
- Establishes: a C++ rigorous branch-and-bound with interval and Bernstein
  enclosures and formal-verification support.
- Relation: background.
- Anticipates: partial (C-BERN context).

**Narkawicz, A., Muñoz, C. (2014). A formally verified generic branching algorithm for global optimization. In: VSTTE 2013, LNCS 8164:326–343. doi:10.1007/978-3-642-54108-7_17.** [KB-S]
- Relation: formal soundness of generic branching (coverage).
- Anticipates: partial (C-BERN coverage argument).

**Ray, S., Nataraj, P. S. V. (2009). An efficient algorithm for range computation of polynomials using the Bernstein form. *J. Global Optim.* 45(3):403–426. doi:10.1007/s10898-008-9382-y.** [AB]
- Establishes: Bernstein range algorithms with cut-off, vertex, monotonicity, and
  concavity tests, plus subdivision rules.
- Relation: background, and possible acceleration ideas for C-BERN.
- Anticipates: none.

**Nataraj, P. S. V., Arounassalame, M. (2011). Constrained global optimization of multivariate polynomials using Bernstein branch and prune algorithm. *J. Global Optim.* 49(2):185–212. doi:10.1007/s10898-009-9485-0.** [AB]
- Relation: Bernstein branch-and-prune for constrained polynomial problems.
- Anticipates: none.

**Patil, B. V., Nataraj, P. S. V., Bhartiya, S. (2012). Global optimization of mixed-integer nonlinear (polynomial) programming problems: the Bernstein polynomial approach. *Computing* 94(2–4):325–343. doi:10.1007/s00607-011-0175-7.** [AB]
- Relation: Bernstein methods applied to MINLP. Background for C-BERN in an MINLP
  context.
- Anticipates: none.

**Smith, A. P. (2009). Fast construction of constant bound functions for sparse polynomials. *J. Global Optim.* 43(2–3):445–458. doi:10.1007/s10898-007-9195-4.** [AB]
- Relation: computes only the needed Bernstein coefficients for sparse polynomials.
- Anticipates: none.

**Smith, A. P. (2012). Enclosure methods for systems of polynomial equations and inequalities. Doctoral thesis, Univ. of Konstanz. http://kops.uni-konstanz.de/handle/123456789/20898.** [AB; the lane brief said "2009"; KOPS gives 2012]
- Relation: broad Bernstein and interval background.
- Anticipates: none.

**Leroy, R. (2009/2011). Certificates of positivity in the simplicial Bernstein basis (HAL preprint)** and **Boudaoud, F., Caruso, F., Roy, M.-F. (2008). Certificates of positivity in the Bernstein basis. *Discrete Comput. Geom.* 39(4):639–655. doi:10.1007/s00454-007-9042-x.** [KB-S]
- Relation: Bernstein positivity certificates with subdivision. Background for
  C-BERN certificates.
- Anticipates: partial (certificate notion).

### 3.4 Interval and ball arithmetic, domain semantics

**Johansson, F. (2017). Arb: efficient arbitrary-precision midpoint-radius interval arithmetic. *IEEE Trans. Comput.* 66(8):1281–1292. doi:10.1109/TC.2017.2690633. arXiv:1611.02831.** [AB (arXiv abstract)]
- Establishes: ball arithmetic for real and complex numbers, polynomials, and
  special functions, with error-bound strategies.
- Relation: the outward-enclosure engine used through python-flint (Report A
  `integration.tex`). Its function-level enclosure contract is a library
  assumption.
- Anticipates: none.

**Hart, W. B. (2010). Fast Library for Number Theory: an introduction. In: ICMS 2010, LNCS 6327:88–91. doi:10.1007/978-3-642-15582-6_18.** [AB]
- Relation: software citation for FLINT, which now contains Arb.
- Anticipates: none.

**Rump, S. M. (1999). INTLAB — INTerval LABoratory. In: T. Csendes (ed.), *Developments in Reliable Computing*, Kluwer, pp. 77–104. doi:10.1007/978-94-017-1247-7_7.** and **Rump, S. M. (2010). Verification methods: rigorous results using floating-point arithmetic. *Acta Numerica* 19:287–449. doi:10.1017/S096249291000005X.** [AB]
- Relation: standard references for verified floating-point computation.
- Anticipates: none.

**Moore, R. E., Kearfott, R. B., Cloud, M. J. (2009). *Introduction to Interval Analysis*. SIAM. doi:10.1137/1.9780898717716.** [AB]
- Relation: standard interval background.
- Anticipates: none.

**IEEE Std 1788-2015, IEEE Standard for Interval Arithmetic. doi:10.1109/IEEESTD.2015.7140721.** [AB; decoration definitions checked in the GNU Octave interval package manual, "IEEE Std 1788-2015"]
- Establishes:
  - Decorations record whether an evaluation stayed inside the function's domain:
    com, dac, def, trv, ill.
  - For example, def means the input "is a nonempty subset of Dom(f)". sqrt over an
    interval containing negatives yields trv.
- Relation: standard semantics for "the enclosure is valid and the expression was
  defined on the whole input". This is the interval-level analogue of the N6 domain
  checks.
- Anticipates: partial (domain-tracking concept of N6).

**Pryce, J. D., Corliss, G. F. (2006). Interval arithmetic with containment sets. *Computing* 78(3):251–276. doi:10.1007/s00607-006-0180-4.** [AB]
- Relation: cset semantics for evaluation outside the natural domain.
- Anticipates: none.

**Goldberg, D. (1991). What every computer scientist should know about floating-point arithmetic. *ACM Comput. Surv.* 23(1):5–48. doi:10.1145/103162.103163.** [AB]
- Relation: background for "every finite binary64 number is an exact dyadic
  rational".
- Anticipates: none.

### 3.5 Expression DAGs, reformulation and domains in global solvers

**Schichl, H., Neumaier, A. (2005). Interval analysis on directed acyclic graphs for global optimization. *J. Global Optim.* 33(4):541–562. doi:10.1007/s10898-005-0937-x.** [FT §3.1, §7, §8.2 of the KB author manuscript, pp. 5–6, 14, 16–17]
- Establishes:
  - Reduced DAGs merge computationally equivalent subexpressions (Definition 3.1).
  - Constant evaluation: "in a validated computation context, however, you have to
    make very sure that no roundoff errors are introduced in this step" (p. 6).
  - Mathematical equivalences such as log rules may change the DAG layout.
  - Proposition 7.1: slope enclosures give valid linear under- and overestimators.
  - §8.2 handles rounding errors in slope centers.
- Relation:
  - Precedent for N6: exact constants and the caution about constant folding.
  - Background for shared subexpressions.
  - They do not discuss preserving the domains of removed subexpressions.
- Anticipates: partial (N6 constant-folding concern).

**Vu, X.-H., Schichl, H., Sam-Haroud, D. (2009). Interval propagation and search on directed acyclic graphs for numerical constraint solving. *J. Global Optim.* 45(4):499–531. doi:10.1007/s10898-008-9386-7.** [KB-S]
- Relation: DAG propagation (FBPD) background.
- Anticipates: none.

**Vigerske, S. (2013). Decomposition in multistage stochastic programming and a constraint integer programming approach to mixed-integer nonlinear programming. Dissertation, Humboldt-Universität zu Berlin. https://edoc.hu-berlin.de/18452/17356.** [FT §7.3 pp. 167–170, full PDF from edoc]
- Establishes:
  - An explicit domain for each SCIP operator: log on R>0; negative integer powers
    on R≠0; fractional powers on R≥0 or R>0 (p. 167).
  - Definition 7.6: expression-graph evaluation returns `domerr` if a child is
    `domerr` or the arguments lie outside dom f.
  - §7.3.1 simplification: constant folding, merging of signomial summands by
    adding coefficients, and substitution. log(∏) = Σ log is "not implemented, yet".
- Relation:
  - Precedent for domain-aware evaluation in SCIP's expression layer (N6).
  - The folding and coefficient-merging steps are the floating-point
    transformations that N6's symbolic check guards against.
- Anticipates: partial (N6 domain semantics).

**Vigerske, S., Gleixner, A. (2018). SCIP: global optimization of mixed-integer nonlinear programs in a branch-and-cut framework. *Optim. Methods Softw.* 33(3):563–593. doi:10.1080/10556788.2017.1335312.** [FT passages in the Optimization Online 2016 preprint; PDF pp. 7, 11, 12–13]
- Establishes:
  - Bound tightening with "roundingsafe extended interval arithmetic".
  - Nonlinear cuts are added if violated by more than 1e-4, or by the feasibility
    tolerance before branching.
  - "Interval gradient cuts" for indefinite functions use interval gradients from
    CppAD over intervals; no cut is generated if bounds are infinite.
- Relation:
  - Native SCIP uses mathematically valid (real-arithmetic) estimators for general
    functions. Their exported floating-point rows are not certified.
  - This is the baseline against which C-SUP's exact-row guarantee differs.
- Anticipates: none (no rounding-safe export).

**Bestuzheva, K., Chmiela, A., Müller, B., Serrano, F., Vigerske, S., Wegscheider, F. (2025). Global optimization of mixed-integer nonlinear programs with SCIP 8. *J. Global Optim.* 91(2):287–310. doi:10.1007/s10898-023-01345-1. arXiv:2301.00587.** [FT passages in KB arXiv v1, pp. 3, 4, 8, 22, 24]
- Establishes:
  - SCIP 8 keeps the original constraints and annotates an implicit extended
    formulation. This is because epsilon-feasible solutions of explicit
    reformulations were infeasible in the original problem (p. 3).
  - Expressions are DAGs with callbacks for simplification and common
    subexpression identification (p. 4). Common subexpressions share one
    auxiliary variable (p. 8).
  - In the benchmark setup, "SCIP ensures that a variable x in x^p, p < 0, or
    log(x) is bounded away from zero by 1e-9, and terminates with a lower bound for
    this modified problem" (§3.2.1, p. 22).
  - Of 41 SCIP failures, 16 were wrong optimal values and 23 infeasible solutions
    (p. 24).
- Relation:
  - Strong motivation for N6 (source-faithful model, no epsilon domain shifts) and
    for C-IMPL's separation of numerical incumbent checks from certificates.
  - The 1e-9 rule contrasts directly with N6's exact existential witnesses.
- Anticipates: none (it documents the gap).

**Belotti, P., Lee, J., Liberti, L., Margot, F., Wächter, A. (2009). Branching and bounds tightening techniques for non-convex MINLP. *Optim. Methods Softw.* 24(4–5):597–634. doi:10.1080/10556780903087124.** [FT §2 passage, Optimization Online 2008 preprint, PDF p. 6]
- Establishes: Couenne rewrites x_j^{x_i} as e^{x_k} with x_k = x_i log x_j. "This
  transformation gives an equivalent problem assuming that x_j > 0 was implied by
  the other constraints. Otherwise, all solutions x such that x_j = 0 are excluded."
  The recursive reformulation is an opt-reformulation.
- Relation: direct precedent for C-IMPL's variable-power rule and for its
  requirement that positivity be *proved*. Our rule refuses rather than silently
  excluding points.
- Anticipates: partial (N6 variable-power rule).

**Smith, E. M. B., Pantelides, C. C. (1999). A symbolic reformulation/spatial branch-and-bound algorithm for the global optimisation of nonconvex MINLPs. *Comput. Chem. Eng.* 23(4–5):457–478. doi:10.1016/S0098-1354(98)00286-5.** [AB]
- Relation: the origin of symbolic standard-form reformulation in spatial B&B.
- Anticipates: none.

**Liberti, L. (2009). Reformulations in mathematical programming: definitions and systematics. *RAIRO Oper. Res.* 43(1):55–85. doi:10.1051/ro/2009005.** [AB]
- Relation: formal notions of exact and opt-reformulation. These give vocabulary
  for N6's "the import is an exact reformulation".
- Anticipates: none.

**Rabinowitsch, J. L. (1930). Zum Hilbertschen Nullstellensatz. *Math. Ann.* 102:520. doi:10.1007/BF01782361.** [AB]
- Establishes: the extra-variable device behind d ≠ 0 ⇔ ∃u: du = 1.
- Relation:
  - The d ≠ 0 witness in C-IMPL is this device.
  - The d > 0 variant (du = 1, u ≥ 0) is an immediate consequence.
  - These witnesses should be credited, not presented as new.
- Anticipates: full for the witness constructions as mathematics.

**Ye, J., Scott, J. K. (2023). Extended McCormick relaxation rules for handling empty arguments representing infeasibility. *J. Global Optim.* 87(1):57–95. doi:10.1007/s10898-023-01315-7.** [KB-S]
- Relation: domain and emptiness handling in relaxation arithmetic. Different
  setting.
- Anticipates: none.

**SCIP source code (v10.0.0 tag; also master at commit 5675a33d, 2026-01-28): `src/scip/lp.c` and `src/scip/misc_rowprep.c`.** https://github.com/scipopt/scip [FT of the cited functions]
- Establishes:
  - With exact mode off, `colAddCoef`, `colChgCoefPos`, `rowAddCoef` and
    `rowChgCoefPos` replace a coefficient that is integral within epsilon by its
    rounded value. The comment reads "in case the coefficient is integral w.r.t.
    numerics we explicitly round the coefficient to an integral value"
    (v10.0.0 `lp.c` lines 1870–1872, 2011–2013, and the analogous lines in the row
    functions). No side correction is made there.
  - `rowprepCleanupIntegralCoefs` (v10.0.0 `misc_rowprep.c` around line 441)
    pre-rounds such coefficients. It adds (coef − round(coef))·bound(x) to the side
    when a finite bound exists. Otherwise it "only round[s] coef (introduces an
    error)". The documented `SCIPcleanupRowprep` also drops small coefficients "if
    this can be done by relaxing the row".
- Relation:
  - The bound-corrected rounding idea exists in SCIP, but in floating point with a
    documented unsafe fallback.
  - LP-row insertion can change submitted coefficients. This is concrete
    justification for C-IMPL's replay of the actual stored row and for the
    exporter's refusal rules.
- Anticipates: partial (bound-corrected coefficient change, non-rigorous).

### 3.6 Numerical-then-exact certificates and verified transformations

**Peyrl, H., Parrilo, P. A. (2008). Computing sum of squares decompositions with rational coefficients. *Theor. Comput. Sci.* 409(2):269–281. doi:10.1016/j.tcs.2008.09.025.** [AB (abstract via search); DOI checked with Crossref]
- Establishes: numeric SDP followed by rounding and projection to an exact rational
  SOS certificate, under strict feasibility.
- Relation: the same "numerical proposal, exact certificate" paradigm as C-SUP, in
  polynomial optimization.
- Anticipates: partial (paradigm only).

**Kaltofen, E., Li, B., Yang, Z., Zhi, L. (2008). Exact certification of global optimality of approximate factorizations via rationalizing sums-of-squares with floating point scalars. In: ISSAC 2008, pp. 155–164. doi:10.1145/1390768.1390792.** [AB]
- Relation: paradigm precedent.
- Anticipates: partial (paradigm).

**Magron, V., Allamigeon, X., Gaubert, S., Werner, B. (2015). Certification of real inequalities: templates and sums of squares. *Math. Program.* 151(2):477–506. doi:10.1007/s10107-014-0834-5.** [AB]
- Establishes: certified lower bounds for transcendental multivariate functions on
  boxes, via max-plus templates and SOS. Certificates are checked in Coq
  (companion: *J. Formaliz. Reason.* 8(1):1–24, 2015, arXiv:1404.7282, abstract
  only).
- Relation: certified bounds for an elementary-function grammar on compact
  domains. Closest to C-SUP and C-BERN for transcendental functions, with stronger
  formal guarantees, but no solver row export.
- Anticipates: partial (C-SUP/C-BERN bounding component).

**Solovyev, A., Hales, T. C. (2013). Formal verification of nonlinear inequalities with Taylor interval approximations. In: NFM 2013, LNCS 7871:383–397. doi:10.1007/978-3-642-38088-4_26.** [KB-S]
- Relation: certificate trees over box subdivisions replayed in HOL Light. The
  formal analogue of complete-coverage replay.
- Anticipates: partial (C-BERN coverage; N4 replay concept).

**Davis, M. M., Papp, D. (2022). Dual certificates and efficient rational sum-of-squares decompositions for polynomial optimization over compact sets. *SIAM J. Optim.* 32(4):2461–2492. doi:10.1137/21M1422574.** [KB-S]
- Relation: rational lower-bound certificates from numerical dual points.
- Anticipates: partial (paradigm).

**Gleixner, A., Steffy, D. E. (2020). Linear programming using limited-precision oracles. *Math. Program.* 183:525–554.** [KB-S]
- Relation: an exactness paradigm from floating-point oracles.
- Anticipates: none.

**Halbig, K., Hümbs, L., Rösel, F., Schewe, L., Weninger, D. (2024). Computing optimality certificates for convex mixed-integer nonlinear problems. *INFORMS J. Comput.* 36(6):1579–1610. doi:10.1287/ijoc.2022.0099.** [KB-S]
- Relation: optimality certificates for convex MINLP, in the sense of Baes et al.
  A different object (whole-problem optimality), not cut validity.
- Anticipates: none.

**Füllner, C., Kirst, P., Otto, H., Rebennack, S. (2024). Feasibility verification and upper bound computation in global minimization using approximate active index sets. *INFORMS J. Comput.* 36(6):1737–1756. doi:10.1287/ijoc.2023.0162.** [KB-S; author list from the KB record]
- Relation: verified upper bounds. Supports the paper's distinction between
  numerical incumbent checks and certificates.
- Anticipates: none.

**Bentkamp, A., Fernández Mir, R., Avigad, J. (2023). Verified reductions for optimization. In: TACAS 2023, LNCS 13994:74–92. doi:10.1007/978-3-031-30820-8_8.** [KB-S]
- Relation: CvxLean proves reformulations in Lean. Precedent for proving that a
  model transformation is exact (N6). It does not deal with binary64 source
  semantics or MINLP domains.
- Anticipates: partial (N6 concept).

**Bhattacharyya, S., Baranwal, M. (2026). SOVER: formal certification of optimization reformulations via LLM-assisted SMT verification. arXiv:2609.00728.** [KB-S]
- Relation: SMT checks of feasible-set equivalence of reformulations (N6 concept).
- Anticipates: partial (concept).

**Pnueli, A., Siegel, M., Singerman, E. (1998). Translation validation. In: TACAS 1998, LNCS 1384:151–166. doi:10.1007/BFb0054170.** and **Necula, G. C. (2000). Translation validation for an optimizing compiler. In: PLDI 2000, pp. 83–94. doi:10.1145/349299.349314.** [AB]
- Relation: the general method of checking each translation output against its
  source, instead of verifying the translator. N6's "symbolic check of the
  submitted DAG" is translation validation for model import.
- Anticipates: partial (method).

**McConnell, R. M., Mehlhorn, K., Näher, S., Schweitzer, P. (2011). Certifying algorithms. *Comput. Sci. Rev.* 5(2):119–161. doi:10.1016/j.cosrev.2010.09.009.** [AB]
- Relation: vocabulary for "producer output plus independently checkable witness"
  (N4).
- Anticipates: partial (concept).

### 3.7 Screening geometry and simultaneous-convexification numerics

**Mangasarian, O. L. (1999). Arbitrary-norm separating plane. *Oper. Res. Lett.* 24(1–2):15–23. doi:10.1016/S0167-6377(98)00049-2.** [FT §§1–2, UW-Madison Math. Prog. Tech. Report 97-07]
- Establishes: Theorem 2.2. The arbitrary-norm distance from q to the plane
  {x: wᵀx = γ} is |wᵀq − γ| / ‖w‖′, with ‖·‖′ the dual norm. The generalized
  Cauchy–Schwarz inequality is (2).
- Relation: the dual-norm normalization behind C-SCREEN, where the max-coefficient
  and sum normalizations pair with R1 and R∞. It also underlies the L1 distance
  identity in C-SEP.
- Anticipates: full for the mathematics of C-SCREEN; partial for C-SEP's distance
  identity (cone coordinates and finite nets are not in it).

**Tawarmalani, M. (2010). Inclusion certificates and simultaneous convexification of functions. Optimization Online.** [KB-S; read in Report A]
- Relation: measures that represent a point as a convex combination of other
  points. This is the conceptual relative of C-SCREEN's sample mixture.
- Anticipates: partial (concept).

**Liers, F., Martin, A., Merkert, M., Mertens, N., Michaels, D. (2021). Solving mixed-integer nonlinear optimization problems using simultaneous convexification: a case study for gas networks. *J. Global Optim.* 80(2):307–340. doi:10.1007/s10898-020-00974-0.** [PT, KB Optimization Online revision: p. 25 and Appendix 7.2–7.3, pp. 36–37]
- Establishes:
  - The separation problem is solved by a subgradient method over directions α.
  - The convex-envelope values are convex combinations Σλ_i g_α(x_i)
    (Appendix 7.3, step 3).
  - "Several standard methods to avoid numerical issues, such as … safe rounding of
    coefficients" (p. 25); Appendix 7.2 step 5 "Numeric rounding". No
    specification is given.
- Relation:
  - The closest simultaneous-convexification implementation. Its numerical
    safety is asserted, not specified or certified.
  - This is the strongest evidence that C-SUP/N4's certified export adds something
    in this application area.
- Anticipates: partial (mentions safe rounding), not N4.

**Ballerstein, M. (2013). Convex relaxations for mixed-integer nonlinear programs. Diss. ETH No. 21024. doi:10.3929/ethz-a-009959194.** [PT. Full PDF obtained via the ETH Research Collection DSpace API (bitstream `eth-7354-02.pdf`, SHA-256 in §9). Keyword search only.]
- Establishes (search scope only):
  - Convex envelopes in Chapters 3 and 5 are computed "numerically" (extracted
    lines 653, 2994, 3833).
  - Interval arithmetic appears only for bound tightening (Chapter 2).
  - No discussion of rounding-safe cut export was found.
- Relation: negative check for N4 in the simultaneous-convexification literature.
  Also resolves the download failure recorded in Report A's manifest.
- Anticipates: none found.

### 3.8 The chord (curvature) correction in C-BERN

**Adjiman, C. S., Dallwig, S., Floudas, C. A., Neumaier, A. (1998). A global optimization method, αBB, for general twice-differentiable constrained NLPs — I. Theoretical advances. *Comput. Chem. Eng.* 22(9):1137–1158. doi:10.1016/S0098-1354(98)00027-1.** [PT §3.2, p. 1140; the formula did not survive text extraction]
- Establishes: the maximum separation distance between f and its αBB
  underestimator is proportional to α and the squared box widths. The text
  attributes this to Maranas and Floudas (1994b). The standard value is
  (1/4)Σα_i(x_i^U − x_i^L)², stated here from general knowledge; check it in the
  PDF before quoting.
- Relation:
  - C-BERN's bound min p ≥ min{p(a), p(b)} − max{0, M}(b − a)²/8 is the
    linear-interpolation remainder p − chord = p''(ξ)(t − a)(t − b)/2. Equivalently
    it is the αBB maximum separation with α = M/2 applied to the concave function
    p − Mt²/2.
  - It is classical; credit it as such, e.g. any numerical-analysis text on linear
    interpolation error, plus αBB.
- Anticipates: full (the inequality itself).

## 4. Novelty assessment

| Claim | Verdict | Evidence |
|---|---|---|
| **C-SUP**, Prop. support (hull = intersection of support halfspaces) | Classical | Convex separation; Liers et al. 2021 Prop. 1; Tawarmalani 2010 (Report B already cites these). |
| **C-SUP**, Prop. round (validity of exact exported binary64 coefficients via a checked bound for the final direction) | Anticipated in principle; the vector-F version is an immediate extension | Garloff–Jansson–Smith 2003 JCAM §5, p. 9 ("not necessary to verify … ŝ"); Garloff–Smith 2008 §5; Neumaier–Shcherbina 2004 p. 294; Borradaile–Van Hentenryck Def. 2; Domes–Neumaier 2012 Thm 6.1. |
| **C-BERN** (exact rational Bernstein, complete subdivision coverage, ball arithmetic, chord correction) | Anticipated; the contribution is the binding and implementation | Muñoz–Narkawicz 2013 (formal PVS Bernstein subdivision, rational constants); Smith et al. 2015; Garloff et al.; Johansson 2017; αBB / interpolation remainder. |
| **C-SCREEN** | Mathematically standard; the use as a checked skip certificate was not found but is minor | Mangasarian 1999 Thm 2.2 (dual norm); Hölder; Tawarmalani 2010 inclusion certificates. |
| **N4** (numerical direction + whole-domain certificate of the exported row + safe rounding after elimination + replay bound to the source model) | Partial: every ingredient is anticipated; the integrated contract for nonlinear joint-support cuts in an MINLP solver was not found | Ingredients: GJS03/GS08/NS04/BVH05 (validation of final row); NS04 pp. 292–293, CDFG09 §3.3, EG24 Lemma 1/Cor. 2 (safe aggregation and export); VIPR (CGS17), EG23, SCIP 10 §3.1 (replay against the instance; MILP only); NS04 p. 289 (raw-model binding); Muñoz–Narkawicz, Solovyev–Hales, Magron et al. (formal replay of nonlinear bounds, no solver rows). Gaps: Liers et al. 2021 unspecified "safe rounding"; Ballerstein no rounding discussion; SCIP 8/10 no certified nonlinear cuts; SCIP's own coefficient rounding (lp.c, misc_rowprep.c). |
| **N6** (source-faithful import: exact binary64 semantics, symbolic whole-row check, exact domain witnesses, proved-positive variable powers) | Partial: the problem and each device are known; the combined, tolerance-free importer check was not found | Problem: Neumaier 2004 §20; Schichl–Neumaier 2005 §3.1; Domes–Neumaier 2010 p. 15. Semantics: Vigerske 2013 Def. 7.6; IEEE 1788. Devices: Rabinowitsch 1930 (witness); Belotti et al. 2009 (positivity assumption for x^y); SCIP 8 1e-9 rule (counter-example of practice); exact readers in SCIP 10 (decimal → rational, different convention). Method: translation validation (Pnueli et al. 1998; Necula 2000); CvxLean. |
| **C-IMPL** affine-bound provenance | Anticipated (certified propagation) | Borst–Eifler–Gleixner 2024 (VIPR-certified propagation in exact MIP); NS04 (rigorous presolve bounds). |
| **C-AGG** (for lane L2) | Mechanism partly anticipated in rigorous global optimization | Domes–Neumaier 2016 §3.1 (aggregation of original nonlinear constraints with approximate Lagrange multipliers, rigorous, used for filtering). Export rule: EG24, NS04, CDFG09. No L3 source gives the N3 closure theorem or the x² = 1/4 gap. |
| **N1, N2, N5** | Out of L3 scope | No L3 source bears on stars or pair-hull gluing. For N5, Mangasarian 1999 covers only the dual-norm distance to a single hyperplane. |

**Recommended wording** for the paper: "We assemble established safe-cut
techniques — a posteriori validation of a numerically chosen affine function
[GJS03, GS08, NS04], validity of the exact machine coefficients [BVH05, CDFG09],
and bound-corrected rounding after aggregation [NS04, CDFG09, EG24] — into a
checked contract for joint-support cuts of nonlinear expressions in a MINLP solver.
The contract binds each certificate to the exact binary64 source model and to the
row actually stored by SCIP, and it is replayed independently [in the spirit of
VIPR, CGS17]." Do not write "first certified nonlinear cuts". Write "to our
knowledge, no published MINLP implementation certifies the exported rows of
nonlinear joint-support cuts", qualified by the search scope.

## 5. Must-cite list

Core (needed for an expert referee):

1. Neumaier and Shcherbina 2004 (safe bounds, safe cuts, raw-model binding).
2. Cook, Dash, Fukasawa and Goycoolea 2009 (safe aggregation, F-representable rows).
3. Eifler and Gleixner 2024 (safe aggregation, back-substitution, verified cuts;
   Lemma 1 / Corollary 2).
4. Cheung, Gleixner and Steffy 2017 (VIPR).
5. Cook, Koch, Steffy and Wolter 2013, and Eifler and Gleixner 2023 (exact MIP).
6. Hojny et al. 2025, SCIP 10 (exact mode limited to MILP; exact readers).
7. Borradaile and Van Hentenryck 2005 (safe estimators with machine coefficients).
8. Kearfott 2011 (rigour survey).
9. Domes and Neumaier 2012 (rigorous linear relaxations, Theorem 6.1).
10. Domes and Neumaier 2016 (rigorous constraint aggregation; also for C-AGG).
11. Ninin, Messine and Hansen 2015 (reliable affine relaxations).
12. Neumaier 2004, Acta Numerica §20 (rounding in problem definition).
13. Garloff, Jansson and Smith 2003, *JCAM* (rigorous shift without verifying the
    LP). Cite this in addition to, or instead of, the *Computing* 2003 paper.
14. Garloff and Smith 2008.
15. Muñoz and Narkawicz 2013 (formal Bernstein subdivision).
16. Johansson 2017 (Arb).
17. Schichl and Neumaier 2005 (DAGs, validated constant folding).
18. Vigerske 2013 thesis (§7.3 domains, `domerr`, simplification).
19. Vigerske and Gleixner 2018 (SCIP MINLP; interval gradient cuts).
20. Bestuzheva et al. 2025, SCIP 8 (original-constraint retention; 1e-9 domain
    rule; failure counts).
21. Belotti et al. 2009 (x^y → exp(y log x) positivity assumption).
22. Liers et al. 2021 (closest application; unspecified safe rounding).

Recommended:

- Jansson 2004.
- Lebbah, Michel and Rueher 2005 / Lebbah et al. 2005.
- Domes and Neumaier 2010.
- Ray and Nataraj 2009; Nataraj and Arounassalame 2011.
- Smith et al. 2015 (Kodiak).
- Solovyev and Hales 2013.
- Magron et al. 2015.
- Peyrl and Parrilo 2008.
- IEEE 1788-2015.
- Rump 2010.
- Moore, Kearfott and Cloud 2009.
- Rabinowitsch 1930.
- Mangasarian 1999.
- Adjiman et al. 1998 (αBB).
- Translation validation: Pnueli et al. 1998; Necula 2000.
- Bentkamp et al. 2023.
- Borst, Eifler and Gleixner 2024.
- SCIP source (lp.c / misc_rowprep.c, v10.0.0) as a software reference for the
  stored-row argument.
- Ballerstein 2013.

## 6. Corrections and cautions for the paper

1. **`GarloffJanssonSmith2003`** in both report bibliographies is
   *Computing* 70(2):111–119 (inclusion isotonicity). Report A's text describes
   it correctly ("inclusion under domain shrinkage"). Report B's `foundations.tex`
   cites it with Garloff–Smith 2008 for the Bernstein enclosure. For the
   numerical-direction-plus-rigorous-shift principle, cite *J. Comput. Appl.
   Math.* 157(1):207–225 (2003), §5. Add a separate key, e.g.
   `GarloffJanssonSmith2003JCAM`.
2. **Garloff and Smith 2008** has no DOI (Lecture Notes in Management Science 1).
   The existing bib entry and URL are fine. The PAMM 2007 note
   (doi:10.1002/pamm.200700501) can serve as a DOI-bearing companion.
3. **Smith's thesis** is from 2012 (KOPS handle 123456789/20898), not 2009. The
   2009 item is the *JOGO* 43:445–458 paper.
4. **SCIP 8 article**: *JOGO* 91(2):287–310 (2025 issue, online 2023). Page and
   section locators in this note refer to arXiv:2301.00587v1, as in Report A's
   manifest.
5. **Eifler and Gleixner 2024 locators**: Lemma 1 at p. 7, Corollary 2 at p. 8,
   and back-substitution at p. 10 refer to the arXiv PDF in the KB. Report B's bib
   note says "version 2". Confirm the version before quoting page numbers.
6. **Borradaile and Van Hentenryck**: theorem numbers here are from the Brown
   tech report CS-03-11 (2003). The journal version may renumber.
7. **Witnesses**: present du = 1 (d ≠ 0) and du = 1, u ≥ 0 (d > 0) as the
   classical Rabinowitsch device applied to domain preservation, not as new
   constructions.
8. **Chord correction**: present it as the classical linear-interpolation error
   bound.
9. **Safe rounding wording**: our row export requires two finite bounds for any
   changed coefficient. That is stricter than EG24 Lemma 1 and NS04, which need
   only the bound in the error's direction. Report B already states this. Keep the
   distinction when citing them.
10. **SCIP behavior claims**: quote the v10.0.0 source lines (Section 3.5) rather
    than paraphrasing documentation. The SCIP version installed with the project
    venv is 10.0 (checked: `pyscipopt 6.2.1`, `SCIP 10.0`).

## 7. Draft related-work paragraph (for adaptation)

> Floating-point cut generation can be made safe by validating the final row
> rather than the computation that produced it. Neumaier and Shcherbina [NS04]
> derive rigorous LP bounds and safe aggregated and Gomory cuts with directed
> rounding, and they note that the cut parameters may be chosen in ordinary
> floating point. Cook et al. [CDFG09] and Eifler and Gleixner [EG24] give safe
> aggregation, back-substitution, and VIPR-verifiable cuts for (exact) MIP
> [CGS17, EG23]. In nonlinear global optimization, safe linear estimators with
> machine coefficients [BVH05], rigorous relaxations [Kea11, DN12, NMH15], and
> rigorously shifted affine Bernstein bounds [GJS03, GS08] follow the same pattern.
> Bernstein subdivision has even been formalized in PVS [MN13]. Our cuts use these
> principles for joint supports of several nonlinear functions. The new element is
> the binding of the certificate to the exact binary64 source model, the
> elimination of auxiliary coordinates with a bound-corrected export, and
> inspection of the row SCIP actually stores. The last point matters because SCIP
> rounds near-integral coefficients on insertion. Existing MINLP implementations
> of simultaneous convexification mention safe rounding without specifying it
> [LMMMM21], and SCIP's exact mode covers only MILP [SCIP10].

## 8. BibTeX entries for new references

Keys follow the style of Report B. Entries were checked against Crossref
metadata, except where noted.

```bibtex
@article{NeumaierShcherbina2004,
  author = {Arnold Neumaier and Oleg Shcherbina},
  title = {Safe bounds in linear and mixed-integer linear programming},
  journal = {Mathematical Programming}, volume = {99}, number = {2},
  pages = {283--296}, year = {2004}, doi = {10.1007/s10107-003-0433-3}}

@article{Jansson2004,
  author = {Christian Jansson},
  title = {Rigorous Lower and Upper Bounds in Linear Programming},
  journal = {SIAM Journal on Optimization}, volume = {14}, number = {3},
  pages = {914--935}, year = {2004}, doi = {10.1137/S1052623402416839}}

@article{ApplegateEtAl2007,
  author = {David Applegate and William Cook and Sanjeeb Dash and Daniel G. Espinoza},
  title = {Exact solutions to linear programming problems},
  journal = {Operations Research Letters}, volume = {35}, number = {6},
  pages = {693--699}, year = {2007}, doi = {10.1016/j.orl.2006.12.010}}

@article{SteffyWolter2013,
  author = {Daniel E. Steffy and Kati Wolter},
  title = {Valid Linear Programming Bounds for Exact Mixed-Integer Programming},
  journal = {INFORMS Journal on Computing}, volume = {25}, number = {2},
  pages = {271--284}, year = {2013}, doi = {10.1287/ijoc.1120.0501}}

@article{CookKochSteffyWolter2013,
  author = {William Cook and Thorsten Koch and Daniel E. Steffy and Kati Wolter},
  title = {A hybrid branch-and-bound approach for exact rational mixed-integer programming},
  journal = {Mathematical Programming Computation}, volume = {5}, number = {3},
  pages = {305--344}, year = {2013}, doi = {10.1007/s12532-013-0055-6}}

@inproceedings{CheungGleixnerSteffy2017,
  author = {Kevin K. H. Cheung and Ambros Gleixner and Daniel E. Steffy},
  title = {Verifying Integer Programming Results},
  booktitle = {Integer Programming and Combinatorial Optimization (IPCO 2017)},
  series = {Lecture Notes in Computer Science}, volume = {10328},
  pages = {148--160}, year = {2017}, publisher = {Springer},
  doi = {10.1007/978-3-319-59250-3_13}, eprint = {1611.08832}, archivePrefix = {arXiv}}

@article{EiflerGleixner2023,
  author = {Leon Eifler and Ambros Gleixner},
  title = {A computational status update for exact rational mixed integer programming},
  journal = {Mathematical Programming}, volume = {197}, number = {2},
  pages = {793--812}, year = {2023}, doi = {10.1007/s10107-021-01749-5},
  eprint = {2101.09141}, archivePrefix = {arXiv}}

@misc{BorstEiflerGleixner2024,
  author = {Sander Borst and Leon Eifler and Ambros Gleixner},
  title = {Certified Constraint Propagation and Dual Proof Analysis in a Numerically Exact {MIP} Solver},
  year = {2024}, eprint = {2403.13567}, archivePrefix = {arXiv}, primaryClass = {math.OC}}

@misc{HojnyEtAl2025SCIP10,
  author = {Christopher Hojny and Mathieu Besan{\c{c}}on and Ksenia Bestuzheva and Sander Borst and others},
  title = {The {SCIP} Optimization Suite 10.0},
  year = {2025}, eprint = {2511.18580}, archivePrefix = {arXiv}, primaryClass = {math.OC},
  note = {Full author list: see arXiv record}}

@inproceedings{HoenGleixner2025,
  author = {Alexander Hoen and Ambros Gleixner},
  title = {Analyzing the Numerical Correctness of Branch-and-Bound Decisions for Mixed-Integer Programming},
  booktitle = {Integration of Constraint Programming, Artificial Intelligence, and Operations Research (CPAIOR 2025)},
  series = {Lecture Notes in Computer Science}, volume = {15763}, pages = {35--50},
  year = {2025}, doi = {10.1007/978-3-031-95976-9_3}}

@article{BorradaileVanHentenryck2005,
  author = {Glencora Borradaile and Pascal {Van Hentenryck}},
  title = {Safe and tight linear estimators for global optimization},
  journal = {Mathematical Programming}, volume = {102}, number = {3},
  pages = {495--517}, year = {2005}, doi = {10.1007/s10107-004-0533-8},
  note = {Tech. report CS-03-11, Brown University, 2003}}

@article{KearfottHongthong2005,
  author = {R. Baker Kearfott and Siriporn Hongthong},
  title = {Validated Linear Relaxations and Preprocessing: Some Experiments},
  journal = {SIAM Journal on Optimization}, volume = {16}, number = {2},
  pages = {418--433}, year = {2005}, doi = {10.1137/030602186}}

@article{Kearfott2011,
  author = {R. Baker Kearfott},
  title = {Interval computations, rigour and non-rigour in deterministic continuous global optimization},
  journal = {Optimization Methods and Software}, volume = {26}, number = {2},
  pages = {259--279}, year = {2011}, doi = {10.1080/10556781003636851}}

@article{LebbahEtAl2005,
  author = {Yahia Lebbah and Claude Michel and Michel Rueher and David Daney and Jean-Pierre Merlet},
  title = {Efficient and Safe Global Constraints for Handling Numerical Constraint Systems},
  journal = {SIAM Journal on Numerical Analysis}, volume = {42}, number = {5},
  pages = {2076--2097}, year = {2005}, doi = {10.1137/S0036142903436174}}

@article{LebbahMichelRueher2005,
  author = {Yahia Lebbah and Claude Michel and Michel Rueher},
  title = {A Rigorous Global Filtering Algorithm for Quadratic Constraints},
  journal = {Constraints}, volume = {10}, number = {1}, pages = {47--65},
  year = {2005}, doi = {10.1007/s10601-004-5307-7}}

@article{Domes2009,
  author = {Ferenc Domes},
  title = {{GloptLab}---a configurable framework for the rigorous global solution of quadratic constraint satisfaction problems},
  journal = {Optimization Methods and Software}, volume = {24}, number = {4--5},
  pages = {727--747}, year = {2009}, doi = {10.1080/10556780902917701}}

@article{DomesNeumaier2010,
  author = {Ferenc Domes and Arnold Neumaier},
  title = {Constraint propagation on quadratic constraints},
  journal = {Constraints}, volume = {15}, number = {3}, pages = {404--429},
  year = {2010}, doi = {10.1007/s10601-009-9076-1}}

@article{DomesNeumaier2012,
  author = {Ferenc Domes and Arnold Neumaier},
  title = {Rigorous filtering using linear relaxations},
  journal = {Journal of Global Optimization}, volume = {53}, number = {3},
  pages = {441--473}, year = {2012}, doi = {10.1007/s10898-011-9722-1}}

@article{DomesNeumaier2016,
  author = {Ferenc Domes and Arnold Neumaier},
  title = {Constraint aggregation for rigorous global optimization},
  journal = {Mathematical Programming}, volume = {155}, number = {1--2},
  pages = {375--401}, year = {2016}, doi = {10.1007/s10107-014-0851-4}}

@article{DomesNeumaier2015,
  author = {Ferenc Domes and Arnold Neumaier},
  title = {Rigorous verification of feasibility},
  journal = {Journal of Global Optimization}, volume = {61}, number = {2},
  pages = {255--278}, year = {2015}, doi = {10.1007/s10898-014-0158-2}}

@article{NininMessineHansen2015,
  author = {Jordan Ninin and Fr{\'e}d{\'e}ric Messine and Pierre Hansen},
  title = {A reliable affine relaxation method for global optimization},
  journal = {4OR}, volume = {13}, number = {3}, pages = {247--277},
  year = {2015}, doi = {10.1007/s10288-014-0269-0}}

@article{Neumaier2004,
  author = {Arnold Neumaier},
  title = {Complete search in continuous global optimization and constraint satisfaction},
  journal = {Acta Numerica}, volume = {13}, pages = {271--369},
  year = {2004}, doi = {10.1017/S0962492904000194}}

@article{NeumaierEtAl2005,
  author = {Arnold Neumaier and Oleg Shcherbina and Waltraud Huyer and Tam{\'a}s Vink{\'o}},
  title = {A comparison of complete global optimization solvers},
  journal = {Mathematical Programming}, volume = {103}, number = {2},
  pages = {335--356}, year = {2005}, doi = {10.1007/s10107-005-0585-4}}

@article{GarloffJanssonSmith2003JCAM,
  author = {J{\"u}rgen Garloff and Christian Jansson and Andrew P. Smith},
  title = {Lower bound functions for polynomials},
  journal = {Journal of Computational and Applied Mathematics}, volume = {157},
  number = {1}, pages = {207--225}, year = {2003},
  doi = {10.1016/S0377-0427(03)00422-9}}

@article{GarloffSmith2007PAMM,
  author = {J{\"u}rgen Garloff and Andrew P. Smith},
  title = {Guaranteed affine lower bound functions for multivariate polynomials},
  journal = {PAMM}, volume = {7}, number = {1}, pages = {1022905--1022906},
  year = {2007}, doi = {10.1002/pamm.200700501}}

@article{MunozNarkawicz2013,
  author = {C{\'e}sar Mu{\~n}oz and Anthony Narkawicz},
  title = {Formalization of {Bernstein} Polynomials and Applications to Global Optimization},
  journal = {Journal of Automated Reasoning}, volume = {51}, number = {2},
  pages = {151--196}, year = {2013}, doi = {10.1007/s10817-012-9256-3}}

@inproceedings{SmithEtAl2015Kodiak,
  author = {Andrew P. Smith and C{\'e}sar A. Mu{\~n}oz and Anthony J. Narkawicz and Mantas Markevicius},
  title = {A Rigorous Generic Branch and Bound Solver for Nonlinear Problems},
  booktitle = {17th International Symposium on Symbolic and Numeric Algorithms for Scientific Computing (SYNASC)},
  pages = {71--78}, year = {2015}, publisher = {IEEE}, doi = {10.1109/SYNASC.2015.20}}

@article{RayNataraj2009,
  author = {Shashwati Ray and P. S. V. Nataraj},
  title = {An efficient algorithm for range computation of polynomials using the {Bernstein} form},
  journal = {Journal of Global Optimization}, volume = {45}, number = {3},
  pages = {403--426}, year = {2009}, doi = {10.1007/s10898-008-9382-y}}

@article{NatarajArounassalame2011,
  author = {P. S. V. Nataraj and M. Arounassalame},
  title = {Constrained global optimization of multivariate polynomials using {Bernstein} branch and prune algorithm},
  journal = {Journal of Global Optimization}, volume = {49}, number = {2},
  pages = {185--212}, year = {2011}, doi = {10.1007/s10898-009-9485-0}}

@article{PatilNatarajBhartiya2012,
  author = {Bhagyesh V. Patil and P. S. V. Nataraj and Sharad Bhartiya},
  title = {Global optimization of mixed-integer nonlinear (polynomial) programming problems: the {Bernstein} polynomial approach},
  journal = {Computing}, volume = {94}, number = {2--4}, pages = {325--343},
  year = {2012}, doi = {10.1007/s00607-011-0175-7}}

@article{Smith2009,
  author = {Andrew Paul Smith},
  title = {Fast construction of constant bound functions for sparse polynomials},
  journal = {Journal of Global Optimization}, volume = {43}, number = {2--3},
  pages = {445--458}, year = {2009}, doi = {10.1007/s10898-007-9195-4}}

@phdthesis{Smith2012thesis,
  author = {Andrew Paul Smith},
  title = {Enclosure Methods for Systems of Polynomial Equations and Inequalities},
  school = {Universit{\"a}t Konstanz}, year = {2012},
  url = {http://kops.uni-konstanz.de/handle/123456789/20898}}

@incollection{Rump1999,
  author = {Siegfried M. Rump},
  title = {{INTLAB} --- {INTerval LABoratory}},
  booktitle = {Developments in Reliable Computing}, editor = {Tibor Csendes},
  publisher = {Kluwer}, pages = {77--104}, year = {1999},
  doi = {10.1007/978-94-017-1247-7_7}}

@article{Rump2010,
  author = {Siegfried M. Rump},
  title = {Verification methods: Rigorous results using floating-point arithmetic},
  journal = {Acta Numerica}, volume = {19}, pages = {287--449}, year = {2010},
  doi = {10.1017/S096249291000005X}}

@book{MooreKearfottCloud2009,
  author = {Ramon E. Moore and R. Baker Kearfott and Michael J. Cloud},
  title = {Introduction to Interval Analysis}, publisher = {SIAM},
  year = {2009}, doi = {10.1137/1.9780898717716}}

@misc{IEEE1788,
  author = {{IEEE}},
  title = {{IEEE} Standard for Interval Arithmetic},
  howpublished = {IEEE Std 1788-2015}, year = {2015},
  doi = {10.1109/IEEESTD.2015.7140721}}

@article{PryceCorliss2006,
  author = {John D. Pryce and George F. Corliss},
  title = {Interval Arithmetic with Containment Sets},
  journal = {Computing}, volume = {78}, number = {3}, pages = {251--276},
  year = {2006}, doi = {10.1007/s00607-006-0180-4}}

@inproceedings{Hart2010FLINT,
  author = {William B. Hart},
  title = {Fast Library for Number Theory: An Introduction},
  booktitle = {Mathematical Software -- ICMS 2010},
  series = {Lecture Notes in Computer Science}, volume = {6327},
  pages = {88--91}, year = {2010}, doi = {10.1007/978-3-642-15582-6_18}}

@article{SchichlNeumaier2005,
  author = {Hermann Schichl and Arnold Neumaier},
  title = {Interval Analysis on Directed Acyclic Graphs for Global Optimization},
  journal = {Journal of Global Optimization}, volume = {33}, number = {4},
  pages = {541--562}, year = {2005}, doi = {10.1007/s10898-005-0937-x}}

@phdthesis{Vigerske2013,
  author = {Stefan Vigerske},
  title = {Decomposition in Multistage Stochastic Programming and a Constraint Integer Programming Approach to Mixed-Integer Nonlinear Programming},
  school = {Humboldt-Universit{\"a}t zu Berlin}, year = {2013},
  url = {https://edoc.hu-berlin.de/18452/17356}}

@article{VigerskeGleixner2018,
  author = {Stefan Vigerske and Ambros Gleixner},
  title = {{SCIP}: global optimization of mixed-integer nonlinear programs in a branch-and-cut framework},
  journal = {Optimization Methods and Software}, volume = {33}, number = {3},
  pages = {563--593}, year = {2018}, doi = {10.1080/10556788.2017.1335312}}

@article{BelottiEtAl2009,
  author = {Pietro Belotti and Jon Lee and Leo Liberti and Fran{\c{c}}ois Margot and Andreas W{\"a}chter},
  title = {Branching and bounds tightening techniques for non-convex {MINLP}},
  journal = {Optimization Methods and Software}, volume = {24}, number = {4--5},
  pages = {597--634}, year = {2009}, doi = {10.1080/10556780903087124}}

@article{SmithPantelides1999,
  author = {Edward M. B. Smith and Constantinos C. Pantelides},
  title = {A symbolic reformulation/spatial branch-and-bound algorithm for the global optimisation of nonconvex {MINLPs}},
  journal = {Computers \& Chemical Engineering}, volume = {23}, number = {4--5},
  pages = {457--478}, year = {1999}, doi = {10.1016/S0098-1354(98)00286-5}}

@article{Liberti2009,
  author = {Leo Liberti},
  title = {Reformulations in Mathematical Programming: Definitions and Systematics},
  journal = {RAIRO -- Operations Research}, volume = {43}, number = {1},
  pages = {55--85}, year = {2009}, doi = {10.1051/ro/2009005}}

@article{Rabinowitsch1930,
  author = {J. L. Rabinowitsch},
  title = {Zum {Hilbertschen} {Nullstellensatz}},
  journal = {Mathematische Annalen}, volume = {102}, pages = {520},
  year = {1930}, doi = {10.1007/BF01782361}}

@article{MagronEtAl2015,
  author = {Victor Magron and Xavier Allamigeon and St{\'e}phane Gaubert and Benjamin Werner},
  title = {Certification of real inequalities: templates and sums of squares},
  journal = {Mathematical Programming}, volume = {151}, number = {2},
  pages = {477--506}, year = {2015}, doi = {10.1007/s10107-014-0834-5}}

@inproceedings{KaltofenEtAl2008,
  author = {Erich Kaltofen and Bin Li and Zhengfeng Yang and Lihong Zhi},
  title = {Exact certification of global optimality of approximate factorizations via rationalizing sums-of-squares with floating point scalars},
  booktitle = {Proceedings of ISSAC 2008}, pages = {155--164}, year = {2008},
  doi = {10.1145/1390768.1390792}}

@article{PeyrlParrilo2008,
  author = {Helfried Peyrl and Pablo A. Parrilo},
  title = {Computing sum of squares decompositions with rational coefficients},
  journal = {Theoretical Computer Science}, volume = {409}, number = {2},
  pages = {269--281}, year = {2008}, doi = {10.1016/j.tcs.2008.09.025}}

@inproceedings{SolovyevHales2013,
  author = {Alexey Solovyev and Thomas C. Hales},
  title = {Formal Verification of Nonlinear Inequalities with {Taylor} Interval Approximations},
  booktitle = {NASA Formal Methods (NFM 2013)},
  series = {Lecture Notes in Computer Science}, volume = {7871}, pages = {383--397},
  year = {2013}, doi = {10.1007/978-3-642-38088-4_26}}

@inproceedings{PnueliSiegelSingerman1998,
  author = {Amir Pnueli and Michael Siegel and Eli Singerman},
  title = {Translation Validation},
  booktitle = {Tools and Algorithms for the Construction and Analysis of Systems (TACAS 1998)},
  series = {Lecture Notes in Computer Science}, volume = {1384}, pages = {151--166},
  year = {1998}, doi = {10.1007/BFb0054170}}

@inproceedings{Necula2000,
  author = {George C. Necula},
  title = {Translation validation for an optimizing compiler},
  booktitle = {Proceedings of PLDI 2000}, pages = {83--94}, year = {2000},
  doi = {10.1145/349299.349314}}

@article{McConnellEtAl2011,
  author = {Ross M. McConnell and Kurt Mehlhorn and Stefan N{\"a}her and Pascal Schweitzer},
  title = {Certifying algorithms},
  journal = {Computer Science Review}, volume = {5}, number = {2},
  pages = {119--161}, year = {2011}, doi = {10.1016/j.cosrev.2010.09.009}}

@inproceedings{BentkampEtAl2023,
  author = {Alexander Bentkamp and Ramon {Fern{\'a}ndez Mir} and Jeremy Avigad},
  title = {Verified reductions for optimization},
  booktitle = {Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2023)},
  series = {Lecture Notes in Computer Science}, volume = {13994}, pages = {74--92},
  year = {2023}, doi = {10.1007/978-3-031-30820-8_8}}

@article{Mangasarian1999,
  author = {O. L. Mangasarian},
  title = {Arbitrary-norm separating plane},
  journal = {Operations Research Letters}, volume = {24}, number = {1--2},
  pages = {15--23}, year = {1999}, doi = {10.1016/S0167-6377(98)00049-2}}

@article{AdjimanEtAl1998,
  author = {Claire S. Adjiman and Stefan Dallwig and Christodoulos A. Floudas and Arnold Neumaier},
  title = {A global optimization method, {$\alpha$BB}, for general twice-differentiable constrained {NLPs} --- {I}. Theoretical advances},
  journal = {Computers \& Chemical Engineering}, volume = {22}, number = {9},
  pages = {1137--1158}, year = {1998}, doi = {10.1016/S0098-1354(98)00027-1}}

@misc{SCIPsource10,
  author = {{The SCIP Optimization Suite developers}},
  title = {{SCIP} source code, files src/scip/lp.c and src/scip/misc\_rowprep.c, tag v10.0.0},
  howpublished = {\url{https://github.com/scipopt/scip/tree/v10.0.0}},
  year = {2025}, note = {Accessed 2026-10-03}}
```

## 9. Provenance and checks run

Searches:

- KB: grep over `literature/index.md` for about 70 author names and topic words.
- KB: grep over `papers/*/fulltext.md` for: Borradaile, Ninin, Kearfott, VIPR,
  Cheung, Goycoolea, Garloff, Nataraj, Johansson, Rump, GloptLab, Lebbah,
  Shcherbina, Vigerske, Jansson, "directed rounding", "safe bound",
  "safe linear", "reliable affine", "affine arithmetic", Messine, "x/x",
  "domain of definition", "x^y", "exp(…log".
- Web search queries:
  - Borradaile–Van Hentenryck; Ninin–Messine–Hansen; Domes–Neumaier.
  - MINLP certificates and proof checkers.
  - Numerically safe nonlinear cuts.
  - Exact MINLP / SCIP exact mode.
  - Domain simplification in global solvers.
  - IEEE 1788 decorations; Rabinowitsch trick.
  - Kearfott 2011; Vigerske thesis; Hongthong–Kearfott; Lebbah et al.
  - Formally verified relaxations; Magron et al.; Peyrl–Parrilo; Stoutemyer.
  - Bernstein-related queries; Smith thesis; Luenberger minimum-norm duality.

Primary documents downloaded (temporary reading copies, deleted after review):

| Source | URL | SHA-256 | Read |
|---|---|---|---|
| Borradaile–Van Hentenryck TR CS-03-11 | https://cs.brown.edu/research/pubs/techreports/reports/03/cs03-11.pdf | `c57f905f7f374c8c6f116522889c5de958d25e2fedcfea9a50cebb42087ac20f` | §§2–3 |
| Ninin–Messine–Hansen preprint | https://optimization-online.org/wp-content/uploads/2012/10/3650.pdf | `1818673dbf2530f5ce0d732d5b41c29a65bbd03bee1e9091fb9464a041b6bda2` | abstract, §4 |
| Domes–Neumaier, constraint aggregation (R2 manuscript) | https://arnold-neumaier.at/ms/Aggregate.pdf | `cc50e02cdfa8f83062931350fb8481e8f1d5ab1f57c8115e69c23db87ee8fe0b` | abstract, §1, §3.1 |
| Domes–Neumaier, rigorous filtering | https://arnold-neumaier.at/ms/linearcsp.pdf | `bff346d3db5e3f46ff9a989ad84745fe6e361fe9bd95980ad816b93e092fe182` | §1.4, §6 (Thm 6.1) |
| Kearfott 2011 preprint | https://www.reliable-computing.org/archive/preprints/2009-verified-vs-non-verified.pdf | `8977a32ab68d5fda3543cd1b89c6ff6254d0ce74d4b59cd47421f328a3e2fa7f` | §4 |
| Garloff–Smith 2008 | https://www-home.htwg-konstanz.de/~garloff/rigorous.pdf | `7d2069beda207fdd61fc8bc394d0a715a6c467e7786d0f2c399d6592a899cefd` | abstract, §5 (hash matches Report A's manifest) |
| Garloff–Jansson–Smith 2003 (Konstanz report 185) | https://kops.uni-konstanz.de/server/api/core/bitstreams/b9a15d62-61bb-4417-a076-151d28cc5544/content | `36ba5efb457d8d9908d6f6317199e9d8edb7be0bec8cf09e0f1c38441311e6b9` | Thm 3.1, §5 |
| Cook–Dash–Fukasawa–Goycoolea 2009 | https://www.math.uwaterloo.ca/~bico/papers/safe_mir.pdf | `f6323601ed18dbbba31c6225e48f8c289fff24d232a1df55f224eded5684eded` | §§1–3 |
| Mangasarian TR 97-07 (PostScript) | https://ftp.cs.wisc.edu/math-prog/tech-reports/97-07.ps | `9b59468cba1aba9f8602eb150abe84e6005a477f5efbac90c80272ddb18dc3c3` | §§1–2 |
| Vigerske 2013 thesis | https://edoc.hu-berlin.de/bitstreams/4c446f58-566f-4e15-8e6a-12dcc691ab2e/download | `9efbd9b2570eb9def2aae4cf7705a958c98b03f2286cd576b3499402a35ea85b` | §7.3 |
| Ballerstein 2013 thesis | https://www.research-collection.ethz.ch/server/api/core/bitstreams/1c9a2cc7-1ec4-4440-9a62-375dd23dfcfd/content | `90b7c598cee8e48d49760de0f122c39e7afcc2d56e979d7bd3967217ed28c68c` | keyword search, TOC |
| SCIP `lp.c` v10.0.0 | https://raw.githubusercontent.com/scipopt/scip/v10.0.0/src/scip/lp.c | `3fab5cca375432cd17bcd07fcdbc8988edb4c8560b025b3a74bc69f96c1a1bed` | functions listed in §3.5 |
| SCIP `misc_rowprep.c` v10.0.0 | https://raw.githubusercontent.com/scipopt/scip/v10.0.0/src/scip/misc_rowprep.c | `ef27818694bd9790bdb74305700350e46afcd60bfd4b029ae3f4ad4af0089ada` | `rowprepCleanupIntegralCoefs` |

Not obtained:

- Stoutemyer (2011) PDF: the mirror returned HTML. Not cited.
- The SCIP online doxygen page returned HTTP 429. The source code was read instead.

Metadata: Crossref API queries (`api.crossref.org/works?query.bibliographic=…`)
for all journal and proceedings entries in Section 8; Füllner et al.'s author list
comes from the KB record. arXiv API for the abstracts of
1611.02831, 1611.08832, 2101.09141, 2303.12365 and 2403.13567. One local
targeted check printed `pyscipopt 6.2.1`, `SCIP 10.0`:
`.venv/bin/python -c "import pyscipopt; …"`.

BibTeX check: the Section 8 block was extracted to a temporary `l3.bib` and run
through `bibtex` with `\citation{*}` and `plain`. Result: 56 entries, no duplicate
keys, no warnings, exit code 0.

No project-wide verification, test suite, or CI inspection was run. Nothing under
`literature/` or `research-2026100*-convexification/` was modified.
