# Stage 4 author record

Date: 2026-09-07. Scope: global approximation in accuracy bits, complete inverse
and quantitative dependencies, and response-dependent polynomial upper data.
This author draft awaits five independent reviewers. No stage 5 authorship or
review delegation was performed.

## Manuscript files and coverage

- `sections/04-accuracy.tex`: complete diagonal, single-resource, fixed-resource,
  convex-aggregate and polynomial-upper results, with explicit rational recovery,
  exact-feasibility qualifications and negative examples.
- `appendices/b-inverse-approximation.tex`: the full signed monotone inverse
  construction and the sharper nonnegative-coefficient specialization.
- `appendices/c-quantitative-bounds.tex`: resource projection, explicit multiplier
  and Hoffman constants, uniform polynomial Bregman growth, both existing response
  moduli, and a new sharper leader-response modulus.
- `main.tex`, bibliography, README and source-to-label coverage were integrated.
  Accepted mathematical section and fixed-core appendix files are unchanged.
- `verification/stage04-author/` contains actual diagnostic outputs, build output,
  a focused additional check, and a command/input/artifact manifest.

The organization shares the general response-certificate interface while retaining
all distinct source developments. Diagonal powers have their elementary dyadic
construction; one equality has its sharper exact signed residual identity; multiple
resources retain their own repair/complementarity ledger; aggregate recovery handles
nonlinear branch crossings explicitly. Upper polynomials are handled by one common
Lipschitz/substitution argument, so their count does not enlarge the algebraic
optimization dimension.

## Substantive development: a sharp 1/P leader-response exponent

Root proposed strengthening the existing 1/(P+1) response modulus. I independently
rederived its tangent-cancellation argument, developed the complete proof in
`prop:accuracy-response-modulus`, and retained the original simpler bound as well.

On a common exact active pattern, a row-space correction of the moving active
right-hand sides has infinity norm at most K B_b times the leader displacement.
Subtracting that correction leaves a common tangent direction, orthogonal to both
optimal gradients. Combining this cancellation with the two Bregman inequalities
removes one response-distance power. The resulting same-pattern estimate has
Hölder exponent 1/P with explicit rational constants from gradient coefficient
bounds and the integer-minor repair bound.

The globalization is a bound, not an exponential algorithm. Along the straight
segment between two feasible leaders, a pattern has an existential polynomial KKT
description. Weak inequalities are lifted with squared slack variables and strict
inequalities with reciprocal-square equations. Summing their squares yields a real
hypersurface. Milnor's affine component bound, which does not assume compactness,
bounds the number of components after projection. Over all at most 3^N 2^k
patterns, the explicit Gamma bound has a polynomial-length binary encoding.
Their component endpoints give at most 2 Gamma + 1 consecutive intervals.
Continuity and summing the local estimates therefore yield a uniform 1/P bound
with a rational constant of polynomial bit length, without computing the intervals.

The independent scalar response x^(1/P) proves sharpness of the exponent. The
convex-anchor tightening theorem can consequently use numerical exponent P rather
than P+1. For N=0 the separate direct Lipschitz exponent is one. This is a
mathematical strengthening of the repository state; no claim of publication
priority is made. Root independently verified the proof and primary component
bound, recorded in its separate reading assessment.

## Critical proof checks and decisions

- Both inverse proofs are complete here. The signed proof projects the real parts
  of *all complex critical values*, includes repeated/nonreal values, pads their
  isolating intervals, and uses geometric rational target panels away from them.
  Properness and simple-root inverse neighborhoods justify a finite covering over
  a critical-value-free disk; simple connectivity yields the analytic branch.
- Centers are rational response values. Their exact forward images are rational
  Taylor centers, so no irrational Taylor coefficients are rounded. The formal
  recurrence, common denominator A1^(2n-1), Cauchy bounds and intermediate truncated
  convolution bounds establish bit complexity, not merely operation counts.
- The interpolation modulus works for signed strictly increasing marginals and
  interior derivative zeros. Positivity is used only in the sharper relative-disk
  construction and sharper positive Bregman constant.
- Resource feasibility is an exact rational leader polytope from support rays,
  including deficient rank and equality pairs. Integer Gram minors give explicit
  polynomial-bit multipliers and repair constants without Slater or strong
  curvature. Small numerical coefficients affect required bits, not an unstated
  inverse-condition-number factor in the runtime.
- The single-resource identity uses one multiplier and no cancellation among
  signed weighted response changes. It is never assumed for multiple resources.
- General aggregate candidates use realizable sign vectors and closed branch
  validity conditions, not arbitrary Cartesian branch products or unjustified
  nonlinear cell closures. All true responses have candidate lifts.
- Rational recovery preserves only the enclosing rational polytope for nonlinear
  branches. Error comparisons use p(v*) at its valid original point and continuous
  true clipped responses at both points. Complementarity transfer includes a
  bound on the *absolute* inactive slack, not only positive violations.
- The aggregate mismatch refinement retains its 1/P exponent when feasibility
  and complementarity residuals vanish. It is distinct from the new global
  leader-response modulus and from the weaker certificate used for the main ledger.
- Polynomial upper derivatives are bounded on the enlarged response box [-1,2]^N.
  Listed upper monomials are substituted and expanded only in fixed compressed
  dimension. Numerical upper degree, rather than sparse binary exponent length,
  remains a complexity parameter.
- Outer feasibility and objective estimates have their exact stated meaning.
  An outer point may be truly infeasible and have objective below V(0). Inner
  emptiness says the positively tightened problem is empty, not that the original
  problem is infeasible. The posterior interval uses a true feasible inner point.
- A strict point alone does not yield tightening convergence. Convex reduced rows
  or uniform reserve headroom are explicit additional promises. Anchors are not
  silently certified by an exact radical oracle. Reserves are actual controls and
  must leave the entire follower, including its aggregate, unchanged.
- N=0 with polynomial upper data is not automatically an LP. A response-independent
  objective does not justify the LP shortcut if an upper row depends on response.
  The anchor and reserve corollaries state their boundary/nonemptiness conditions.

No defect requiring a change to canonical source files was identified. Existing
source statements are extended and reorganized in the paper, not overwritten.

## Sources and primary checks

Read all five canonical accuracy results, both complete inverse notes, their
focused source assessments and relevant dependency reviews, including the signed
transfer addenda, nonlinear-boundary discussion and polynomial-upper second audit.
Read `literature/AGENTS.md`; no literature packages, generated metadata or originals
were changed or redistributed. Earlier accepted real-algebra and fixed-core proofs
remain the manuscript's shared supporting tools.

Primary sources checked for this stage:

- Basu–Pollack–Roy's established fixed-variable elimination/sampling interface is
  the already verified foundation. Our formulas explicitly keep dimension fixed
  and track growing numerical degree and expanded coefficient bits.
- DLMF Section 1.10: Taylor/Cauchy framework, analytic continuation, Rouché theorem,
  and inverse functions. The displayed quantitative disk constants are proved in
  the appendix rather than attributed to an unspecified inverse condition bound.
  https://dlmf.nist.gov/1.10
- Farouki (2000), CAGD 17(2):179–196, DOI 10.1016/S0167-8396(99)00046-1:
  the primary publisher indexed abstract verifies the direct polynomial-inverse
  approximation precedent. Direct publisher fetch failed; no detailed theorem
  or full-text scope claim is made from that abstract.
  https://www.sciencedirect.com/science/article/abs/pii/S0167839699000461
- Walsh (2000), Mathematics of Computation 69(231):1167–1182, DOI
  10.1090/S0025-5718-00-01246-1: publisher PDF fetch failed, but the reproduced
  published primary text was readable. Theorem 1 on printed p.1170 gives a
  polynomial bit bound for the Puiseux singular part; the following paragraph
  discusses subsequent terms while omitting their further analysis. Our rational
  recurrence has its own complete proof and does not rely on that omission.
  https://paperzz.com/doc/7111378/a-polynomial-time-complexity-bound-for-the-computation-of...
- Patriksson–Strömberg: local/open primary preprint, inverse response formula (17)
  and Section 6/Remark 9 on dual versus primal error. Published metadata was
  independently verified at Chalmers: EJOR 243(3):703–722 (2015), DOI
  10.1016/j.ejor.2015.01.029. The bibliography cites the published version; the
  inspected text was arXiv:1501.07035.
  https://arxiv.org/html/1501.07035
  https://research.chalmers.se/publication/216160
- Hochbaum–Shanthikumar (1990), local primary full text, Theorem 1.1 and accuracy
  discussion. Logarithmic inverse-accuracy dependence for convex allocation is
  credited, without transferring its subdeterminant-dependent complexity to this
  independently signed upper optimization problem.
  https://hochbaum.ieor.berkeley.edu/html/pub/Hochbaum-Shanthi-JACM90.pdf
- Jeyakumar–Lasserre–Li–Pham (2016), local primary revised manuscript, abstract,
  Hölder/SDP-relaxation context and Theorem 3.5. General convergent polynomial
  bilevel relaxation is credited; no claim that it lacks a bit model was made.
  https://arxiv.org/abs/1506.02099
- Boyd–Vandenberghe, *Convex Optimization*, Section 5.6, printed pp.249 onward
  (PDF p.262 onward), on perturbed inequalities and value sensitivity. We use the
  established perturbation viewpoint, with our additional nonconvex-objective
  continuity and explicit tightening guarantees proved separately.
  https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf
- Milnor (1964), *On the Betti numbers of real varieties*, printed p.275,
  Theorem 2, DOI 10.1090/S0002-9939-1964-0161339-9. Root verified the original
  affine real-algebraic theorem visually: total Betti number at most
  d(2d-1)^(n-1), without compactness. The author independently checked its
  application to the strict/weak polynomial lift and projection count.
  https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Milnor1.pdf

The bibliography adds these new entries and converts Patriksson–Strömberg to
verified published metadata. A pre-existing BibTeX warning for Liu et al.'s PMLR
volume/part was removed by storing its volume as `32(2)` rather than incompatible
volume and number fields; the factual volume/part is unchanged. The DLMF entry
uses `n.d.` and an access date rather than inventing a publication year.

## Actual verification

All commands below completed with exit code 0 from the repository root, unless
noted. Logs are actual stdout, not reconstructed results.

| Diagnostic script | Result and distinct confidence |
| --- | --- |
| `code/bilevel_bounded_power/check_dyadic_approximation.py` | 900 certified dyadic approximation values, truncation/tail bounds and sparse-output constants. `dyadic.txt`. |
| `code/bilevel_bounded_power/check_positive_inverse_second.py` | 159 rational centers, 1,119 denominator/Cauchy checks, 477 independently enclosed inverse values. `positive-inverse.txt`. |
| `code/bilevel_bounded_power/check_monotone_inverse_second.py` | 15,504 rational panels, 20 Taylor centers, 236 denominator/Cauchy checks, 60 inverse enclosures, 80 modulus checks, three nonreal critical-value pairs. `monotone-inverse.txt`. |
| `code/bilevel_one_resource/check_signed_balance.py` | 7,200 exact signed balance/error certificates across 160 instances. `signed-balance.txt`. |
| `code/bilevel_bounded_power/check_fixed_resource_first_review.py` | 512 primal/ray comparisons, 288 approximate-dual/repair cases, 5,408 directed power Bregman and 3,380 signed modulus/Bregman cases. `resource.txt`. |
| `code/bilevel_reopened/nonlinear_aggregate_review.py` | Five irrational boundaries, ten recoveries on opposite sides, twenty complementarity transfer terms and twenty singular quartic cases. `aggregate-boundaries.txt`. |
| `code/bilevel_reopened/nonlinear_aggregate_checks.py` | 240 quadratic-local/quartic cases, 561 flat-curvature signed-resource equalities, 72 complementarity ledger cases. `aggregate-certificates.txt`. |
| `code/bilevel_reopened/response_constraints_review.py` | 10,091 exact cases: moving-resource and zero-curvature moduli, convex-service tightening, isolated-optimum gap sequence, posterior signs and enlarged-box upper-polynomial bounds. `upper-constraints.txt`. |
| `paper-structured-bilevel/verification/stage04-author/check_sharp_modulus.py` | 192 original-coordinate KKT endpoint certificates; 96 each tangent cancellation, monotonicity and gradient estimates; 48 fixed-resource division cases; 48 moving-resource row-space corrections; 15 exact sharp-root cases. `sharp-modulus.txt`. |

The new check targets the risky new common-active-pattern argument. It independently
constructs exact KKT optima with bound coordinates, redundant resource normals,
signed flat marginals of degrees 1/3/5, and convex quartic aggregates including
leader-dependent coefficients. It verifies true stationarity and tangent identities,
not an approximate optimizer. It does not test the all-input Milnor theorem or
compute a full global response decomposition. The old diagnostics test other
specific proof obligations and do not implement general quantifier elimination.
No aggregate count is presented as formal verification of the universal theorems.

The final command from the paper folder is:

```
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The combined PDF has 45 pages. Final LaTeX and BibTeX logs have no warnings,
undefined references/citations, or overfull/underfull boxes. A first integration
attempt used a repository-relative path from the paper directory and failed before
writing; it was rerun using absolute paths. The successful first build exposed
two overfull lines, corrected before the final build. Intermediate citation-change
warnings during the necessary reruns are harmless and absent from the final log.
The manifest records final hashes and command outcomes; accepted mathematical
files are compared with `stage03-accepted`.

## Remaining scope

All assigned stage 4 developments and their supporting proofs are written.
The author has identified no unresolved mathematical dependency within their
stated scope. Five independent reviews remain required, especially for the new
sharp modulus. Stages 5–7 and the final integrated review remain unchanged.
No claim is made that wider exact-feasibility, sparse-degree, growing-dimension,
or implementation questions have been solved by these theorems.
