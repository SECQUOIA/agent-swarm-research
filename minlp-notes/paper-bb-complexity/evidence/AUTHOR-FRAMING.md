# Framing author report

Scope: `sections/abstract.tex`, `sections/introduction.tex`,
`sections/discussion.tex`, and this report only. Written under the root's
explicit Sol fallback after the Claude writing limit. No other file was
edited. The earlier introduction and discussion were read in full and
critically rewritten; sound distinctions and the source-supported narrative
were retained.

## Editorial result

The introduction now opens with solution versus proof and distinguishes
certificate size, search nodes, local checking work, and incumbent discovery.
Its result overview uses connected prose, three displayed structural
quantities, and the model map `intro:tab-models`. The duplicated informal
theorem environment and all former `intro:thm-*` promises were removed.
There is a separate focused decomposition paragraph and prior-work comparison.
The abstract is 220 words before final line edits; the introduction and
discussion were approximately 2,650 and 1,660 words at their first complete
revision. Submission sources contain no authoring-status or review history.

The discussion explains the consequences of each proved obstruction,
separates construction/checking/runtime from size, distinguishes statistical
events, interprets the finite-size computations, and states unresolved
questions. It makes no practical speedup claim.

## Evidence incorporated

Read in full: BRIEF, AUTHORING-CONVENTIONS, ARCHITECTURE-DECISION,
INCOMING-AUDITS, ISSUES, AUDIT-SPATIAL, AUDIT-DISCRETE, AUDIT-BRANCHING,
REVIEW-GEOMETRY-REPAIR-R1, REVIEW-NNLS-R1, REVIEW-SHARP-INDUCTION-R1,
REVIEW-PWE-R1, and ARCHITECTURE-BOUNDARY-NOTE. The latest issue/notification
files were reread after the first manuscript revision. The architecture
summary is superseded wherever it conflicts with these independently checked
results or actual chapter statements.

Also inspected the actual saved certificates, geometry, face, decomposition,
propagation, branching, lattice, regression, binary-least-squares and
experiments statements relevant to the overview. Technical authors supplied
stable hypotheses and labels directly. Framing uses the actual selected
results, rather than the architecture's preliminary list.

The Luna literature lead supplied the allowed comparison scope and stable
keys. No literature research was performed by this author. The 2018
Kannan–Barton source was removed from the introduction after the literature
lead restricted its inspected-source status. The corrected Chord Algorithm
key is `daskalakisDiakonikolasYannakakis2016ChordAlgorithm`. No barred
Dechter–Mateescu article key is used. The final `LITERATURE.md` was not yet
present at the last inspection; root integration must reread its completed
ledger for final source restrictions.

## Contribution and hypothesis map

This table records contribution wording, not universal priority claims. All
nonstandard mathematical proofs belong to the body/appendices, not this
internal report.

| Framing claim | Exact manuscript support and material scope | Mathematical provenance | Prior-work comparison |
|---|---|---|---|
| Boundary-safe lower bounds after reduction | `cert:lem-events`, `cert:eq-work`, `cert:eq-eval`; rectangular ownership, retained boundaries, pointwise lower gap for removals, virtual probes charged, node conclusions only with bounded relevant rounds | AUDIT-SPATIAL §§2.3–2.4; independent REVIEW-GEOMETRY-REPAIR-R1 and ARCHITECTURE-BOUNDARY-NOTE | Finished-tree certificate observation is standard; contribution is the boundary-safe operation accounting, not that observation |
| Running-supremum profile comparison | `geom:thm-profile`, `geom:ass-upper`; positive bound gap, second-order objective and violation upper error, violation-to-full-feasible-distance error bound, Lipschitz objective, fixed instance; all raw minima separate | spatial-constrained note, audited §3; chapter gives complete proof | Du–Kearfott 1994, Wechsung–Schaber–Barton 2014, Kannan–Barton 2017 provide cluster/convergence antecedents; Bachoc–Cesari–Gerchinovitz 2021 counts Lipschitz-oracle evaluations. No identity between these cost models is asserted |
| Positive-dimensional manifold rate | `geom:prop-dimension`, `geom:prop-manifold`; quadratic growth plus compact regular manifold/chart cover, positive dimension | AUDIT-SPATIAL §3.3; actual chapter corollary | Rate is not claimed from optimal-set dimension alone |
| Nonlinear original-constraint tube transfer | `geom:thm-tube-kkt`; local C2 objective and compatible original exact/relaxed data, same violation function and KKT multipliers, combined LICQ, nonzero relaxed multiplier, positive-dimensional active stratum, inner tube, no original-feasibility reductions; all owners counted | Full repair AUDIT-SPATIAL §5 and independent REVIEW-GEOMETRY-REPAIR-R1 | Extends the selected original-model local proof beyond affine exact constraints; does not allow arbitrary feasible-set re-description |
| Root-face integral and analytic rates | `face:thm:characterization`, `face:rem:gap-scope`, `face:cor:analytic-rate`, `face:prop:full-box`, `face:ex:boundary`; unconstrained C1,1 objective, strictly positive quadratic vertex-gap lower and vertex-vanishing upper error; all positive-dimensional root faces; exact weighted oracle is the main theorem, sandwich extension is explicitly proved in the remark | RLCT note, AUDIT-SPATIAL §4, actual complete face proof | Lin 2017 supplies analytic sublevel/Laplace input; it does not supply a B&B theorem. The connection to the all-face certificate characterization is the manuscript contribution. Ordinary RLCT terminology excludes the separate identically-zero case |
| McCormick graph/placement dependence | Matching/transversality/fractional-cover body results; `geom:prop-aligned-two`, `geom:ex-aligned-three`; exact two-leaf result only for the stated unconstrained two-dimensional convex model and full optimal segment; three-dimensional aligned example has Theta(epsilon^-1/2) minima | face-exact source and AUDIT-SPATIAL §6; geometry author's full selected proofs | McCormick and Rikun formulas are classical. Contribution wording concerns certificate counts and exactness placement. No general aligned-stratum boundedness or McCormick characterization is claimed |
| Decomposition size under the same local oracle | `decomp:small-certificate`, `decomp:path-separation`; global quadratic growth, C1,1 bags, convex factor relaxations with vertex-vanishing error, controlled occurrence/branching/conditioning, exact center/slopes; fixed-width O(M log(M/epsilon)); clean c=0 path family uses separate convex unary and alphaBB bilinear factors | AUDIT-BRANCHING §6; full decomposition appendix, author checks | Marinescu–Dechter 2009, de Givry et al. 2006 establish conditioned reuse in discrete search; Bienstock–Munoz 2018 gives width-based approximate formulations. Present claim fixes the continuous local oracle and compares global-box versus affine-separator proof size. No later coordinate-grid, arbitrary-tree localization, or runtime theorem is imported |
| Objective-only cutoff propagation | `prop:fixed-point`, `prop:one-sided`, `prop:local-exactness`, `prop:cnd-transfer`; fixed finite continuous DAG and compact domains; distinct root-child coordinates; strict closed-cutoff emptiness/removal; CND derivative margin, C2 local bounds, specified objective-only phases, pointwise tests and ownership | cutoff note, AUDIT-SPATIAL §7, actual chapter/appendix | Schichl–Markot–Neumaier is known cutoff/exclusion context. Contribution is graph-dependent fixed-point/exactness/persistence analysis and distinct round accounting. No one-sided iff classification is claimed |
| Competitive branching and safeguards | `branching:four-competitive`, `branching:germ-obstruction`, `branching:recentring`, `branching:dimension-obstruction`, `branching:sharp-induction`; exact uniform-alpha oracle, unconstrained continuous f, fixed optimal incumbent; no convexity needed for 1D count; nonanalytic germ class; exponential coordinate-ambiguity result requires coordinatewise selection and no objective-dependent sibling information; safe zero-tolerance hitting versus finite-tolerance count; fixed coordinatewise sharp selection | AUDIT-BRANCHING §§2–5; independent REVIEW-SHARP-INDUCTION-R1; actual complete branching proofs | Daskalakis et al. 2016 is an oracle-competitive analogy in another problem. HJL 1991 full primary text remains unavailable, so no first/priority claim is made. General fixed-dimensional competitiveness remains open |
| Convex class number and random lattices | `lattice:class-number`, `lattice:operations`, `lattice:cvp`, `lattice:curvature-gadget`; fixed convex projected relaxation and required set P, finite kappa for attainment; semantic root allowed any convex set containing P; children need cover required integer points; cuts preserve P; Haar lattice plus uniform torus target; displayed exponent uses vanishing relative tolerance | integer-core note, AUDIT-DISCRETE, actual selected corrected lattice proofs | Dey–Dubey–Molinaro and Kaibel–Weltge supply conflict/hiding-set lower-bound antecedents. No efficient semantic construction, arbitrary split-tree characterization, Gaussian-basis lattice extrapolation, or universal novelty claim is made |
| Sparse root/C1/lift thresholds and hard certificates | `regression:easy-thresholds`, `regression:window`, `regression:lift-thresholds`, `regression:hard-theorem`; Gaussian unnormalized ridge model, easy-regime scaling and fixed margins; planted converses imply global failure only if planted support optimal; selected lift sandwich; separate low-total-signal regime; hard pairwise lift retains zero-fixed helpers | AUDIT-DISCRETE plus complete regression appendix | PWE, Xie–Deng, Dong–Chen–Linderoth are formulation antecedents. Wainwright 2009 is Lasso support recovery, a different certificate event. No universal stronger-lift or computational-hardness statement is made |
| Fixed-dimensional PWE limitation | `regression:pwe-theorem`; fixed 1<=k<d, fixed nonzero signal, fixed positive per-entry noise, lambda=sqrt(n), Gaussian design; planted support uniquely optimal whp but exactness probability has explicit limit below one | Independent REVIEW-PWE-R1, actual complete manuscript KKT/limit proof | Narrow comparison with PWE Theorem 2 under its printed normalization. Boolean reformulation and deterministic exactness identities are not rejected; no fixed-SNR or total-energy sharp-constant repair is asserted |
| Gaussian NNLS and BLS certificate transitions | `bls:nnls-tail`, `bls:nnls-law`, `bls:c1-threshold`, `bls:root-threshold`, `bls:certificate-law`; M>=N Gaussian model, independent standard Gaussian noise; C1 rho=theta N with fixed positive theta and fixed margin; root box equality iff rho>=random cutoff; exact beta_N in root threshold; certificate law rho->infinity and rho=o(N), 0<=epsilon_N<=rho_N, or sufficiently large fixed rho | New audit development and independent REVIEW-NNLS-R1; actual complete BLS chapter/appendix | Gaussian face-dimension and chi-square mixtures are classical Hug–Schneider/McCoy–Tropp material. Finite sign-invariant coefficient tail and B&B-specific simultaneous criterion/inactivity/certificate application are the selected contributions. Hu–Lu is per-decoder rounding, not all-node union bound. HHDX 2009 ML comparison is square and is not used to justify the manuscript's independently proved tall result |
| Archived computational interpretation | Actual experiments chapter and author's protocol message; controlled settings changed jointly; floating slopes descriptive; unclamping worsened recorded node counts; recentering uncertainty includes comparable performance; finite random tests outside easy asymptotic assumptions | Archived S1–S5 and exact historical reports; no reruns | Illustrates mechanisms and implementation effects. No asymptotic-constant measurement, formal epsilon-certificate claim for floating counts, generic solver gain, or practical speedup follows |

## Concrete scope corrections from root and chapter synchronization

- The opening does not claim that node processing dominates runtime.
- Covers, rectangular partitions, trees, owned event families, and successful
  source-evaluation covers remain distinct.
- A bound-gap lower bound does not by itself handle removed pieces; those
  require the pointwise hypothesis.
- Unbounded tightening and propagation rounds do not yield actual-node lower
  bounds; virtual probes and distinct-solve charging remain explicit.
- Original C2 objective and exact/relaxed constraint data are kept together.
- McCormick alignment alone does not imply bounded certificates.
- Class-number cuts preserve the required set P. Cuts preserving only a
  smaller feasible set do not preserve a class number formed on larger P.
- Semantic attainment permits a root containing P and does not promise
  efficient actual solver disjunctions or checking.
- Weak C1 requires the optimal incumbent at off-path tests; exact best-bound
  search without it needs strict wrong-node bounds above OPT, exact fully
  fixed projected bounds, and recovery of an optimal feasible extension.
- BLS C1 has fixed positive theta and fixed margin. Its failure is not a tree
  lower bound. Root inactivity includes equality at the random cutoff.
- The abstract says divergent sublinear SNR, with sufficiently large fixed
  SNR as a separate body regime.
- Tall SDP threshold, universal nD competitiveness, generic cancellation
  dichotomy, general McCormick characterization, general tree localization,
  coordinate-grid algorithms, and empirical decomposition are omitted.
- Coordinate ambiguity was checked against its subsequently saved theorem
  `branching:dimension-obstruction` and full proof `app:branching-dimension`
  before its narrowly qualified overview was restored. The restriction to
  nonanalytic node-local information, coordinatewise minimizer selection,
  and no objective-dependent sibling state is explicit. A broad claim that
  the selected manuscript gives a quantitative class-versus-midpoint-clique
  separation was removed because no supporting KL/midpoint-blindness result
  was selected.

## Verification and integration requests

Targeted commands actually run were `pwd`, `rg --files`, `cat`, `sed -n`,
`wc -l`, `wc -w`, `rg -n`, and `ls` to inspect the assigned documents, source
keys, and relevant saved theorem statements. These document reads and scope
comparisons passed except for missing files during concurrent drafting;
subsequent reads found the saved technical files. `LITERATURE.md` was still
missing at last inspection. The framing sources were written with scoped
Python `Path.write_text` calls; no experiment or mathematical computation
was executed. No project-wide verification, CI query, TeX build, experiment
rerun, or commit was performed. Root owns the targeted standalone build.

Remaining integration requests are concrete:

1. Root/literature lead must finalize the allowed-source ledger and ensure
   every cited stable key is in the final bibliography; framing makes no
   priority claim dependent on unavailable HJL or barred editions.
2. Root's independent final manuscript review must recheck the final framing
   against any theorem changes made after this report. Coordinate ambiguity
   is now included with its exact information-class qualification.
3. Root must compile the integrated sources and check line breaks of the
   introduction's long comparison display and model table. The framing
   author did not compile or run project-wide checks.
