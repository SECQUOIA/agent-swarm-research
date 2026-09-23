# Independent review: Stage 04, round 01, reviewer 1

Reviewer: `/root/paper_reviewer_1`. Date: 2026-09-07.

Frozen snapshot: `da3db325e0812991ad97d79560c4c8aeb99b83d7260ade75d6172d61d3b4aaa6`. I checked all twelve hashes in the manifest; all matched. I read the complete generic-fold section, its handoff, notation/claim changes, and the applicable accepted scalar-form, harmonic-bracketing, graded-design, and physical-transfer prerequisites. I did not read other reviewer reports or coordinator-checks, coordinate conclusions, edit sources, or delegate.

## Verdict

**Accept Stage 04. No major or minor issue found.** The hypotheses are explicit and sufficient for the uniform geometry and partitions used in the proof. The lower certificates remain valid for arbitrary integrable competing mobility, the upper construction protects additional ordinary roots, and each moment regime follows with its claimed logarithmic factor. The exact scalar-to-bulk ratio is justified even though only orders are proved for the generic scalar optimum.

This assessment does not extend the theorem to coincident folds, altered sampling exponents, or unknown fold locations; those cases are explicitly outside the statement.

## Independent checks

### 1. Compact root geometry and rate anchoring

The zero set is compact because g is continuous on the compact wall–parameter product. At a simple zero, a sufficiently small product chart has a fixed sign and positive lower magnitude for g_s, so each spatial slice has at most one zero. At a listed fold, g_ss has a fixed nonzero sign on a product chart, so strict convexity or concavity bounds the zero count on each slice by two. A finite subcover therefore supplies a uniform total zero count. This proof works also at the ends of the parameter interval for simple zeros; folds are explicitly interior.

After removing open product neighborhoods containing all folds, the remaining zero set is closed and compact and contains no multiple zero. Consequently |g_s| has a positive minimum there. Ordinary roots cannot have separation tending to zero on this closed set: compactness would give coincident limiting roots, and the spatial mean-value theorem would give g_s=0 at their common limit. That contradicts the uniform simple-root condition. Thus a common small radius gives disjoint ordinary-root intervals with uniform quadratic bounds.

The fold products can be chosen with uniformly nonzero g at their spatial ends for the active parameter interval. The two unfolding roots remain in a smaller interior interval after shrinking the parameter neighborhood. Ordinary-root intervals outside that active fold interval therefore can be used together with it in finite Neumann partitions. On the complement of all retained root intervals, a failure of a positive potential minimum would give an unretained limiting zero; compactness and the preceding cover rule this out. There is no hidden assumption that ordinary roots move with c.

The upper bound on k follows from compactness. The function `c -> int_Gamma g(s,c)^2 ds` is continuous. If its minimum were zero, continuity of g in s would make the entire realization zero. Then every spatial point would satisfy `g=g_s=0`, contradicting the assumed finite multiple-zero set. This proves the uniform positive anchor actually needed by the physical comparison theorem; pointwise nonzero integrals alone would not have been enough without compactness.

### 2. Regularity and geometry of the fold coordinate

Since g is C4, g_s is C3. The implicit equation `g_s(z(c),c)=0` and nonzero g_ss give a C3 critical-point curve. The integral Taylor coefficient b is C2 jointly in s and c, retains a fixed sign, and stays bounded away from zero on a small chart. Hence `x=(s-z(c))sqrt(|b(s,c)|)` is C2 and has nonzero spatial derivative at the fold. A smaller chart makes it a uniformly controlled spatial coordinate. No C4 normal-form coordinate is required.

The exact identity is `g=sigma(x^2-t)`, with `t=-sigma h(c)`. Differentiating h at the critical point gives `h'(c_j)=g_c(s_j,c_j)`, since the g_s term vanishes. Thus t is locally a valid parameter and `|t|` is comparable to `|c-c_j|`. Smoothness of z also gives its displacement from the fixed design site as O(|t|).

On the two-root side, x=±sqrt(t). Bounded spatial Jacobians and the O(t) center displacement make the distances of the two roots from the fold site, their separation, and the magnitude of their spatial slopes comparable to r=sqrt(t). On intervals of radius a fixed sufficiently small multiple of r, Taylor expansion or the exact normal form gives the stated quadratic rate bounds.

Alternatively, nonzero g_c gives the zero curve `c=C(u)`. Differentiating `g(u,C(u))=0` twice at the fold gives `C'=0` and `C''=-g_ss/g_c`, with the displayed sign and factor. On either fixed side of the site, |C'| is therefore comparable to the distance from the site. On a shell away from the site the map is monotone with derivative bounded below by a positive multiple of r, so an almost-everywhere lower density in c pulls back to an almost-everywhere lower bound in u. This validates the shell's parameter probability of order r squared even though the density is only measurable.

### 3. Arbitrary-design lower bounds

For a local mass m, the Fubini estimate for the translated bump gives mean derivative cost at most `C m/(r ell)`. The reaction contribution is at most `C r^2 ell^3`. Their balance is `ell^4` proportional to `m/r^3`, and the small-mass condition makes every test support stay in the spatial shell and within the local quadratic comparison. Jensen applies to the convex negative qth power for every q>0. Combining source, denominator, and parameter probability gives

`r^2 ell^(2q)[m/(r ell)+r^2 ell^3]^(-q)`,

which simplifies to `r^(2-5q/4)m^(-q/4)` as stated. If m=0, the same quotient with shrinking widths diverges, so this case is not excluded by an inverse-operator assumption.

A fixed shell has positive probability because the density is positive near the chosen fold. It yields the subcritical lower order using m<=M, without requiring sampling elsewhere. At criticality, a sufficiently separated geometric shell sequence has disjoint spatial enlargements and, on the selected monotone branch, disjoint parameter images. The smallest radius is a sufficiently large constant times `M^(1/7)`, guaranteeing the small-mass condition for every shell. There are order log(1/M) shells and total assigned mass at most M; convexity gives their aggregate `M^(-2/5) N^(7/5)`.

For the supercritical lower bound, on a spatial window of width R and parameter window of width order R squared about the fold, Taylor expansion gives |g|<=C R squared. Therefore reaction energy is at most C R fifth, derivative energy is at most `C M/R^2`, and squared source is of order R squared. Choosing `R=M^(1/7)` gives response at least `c R^(-3)` over probability at least c R squared. Additional roots cannot reduce any of these valid local lower tests.

### 4. One admissible upper design and ordinary-root protection

The grading exponent is nonnegative and below six. For each fixed positive M, the exact normalization gives a bounded field with positive lower bound. The use of max(0,alpha_q) for q<=2/3 is material: a negative exponent could reduce mobility at a site occupied by an ordinary root for another parameter value. The chosen global lower bound `D_M>=c a_R` protects that case, including stationary ordinary roots.

Near each distinct fold site, the distance to the finite fold set equals the distance to that site on a sufficiently small chart. Its normalization integral is bounded for alpha<1, logarithmic for alpha=1, and of order `R^(1-alpha)` for alpha>1. With the stated cutoffs, all three cases give `a_R` comparable to `R^(6+alpha)`.

For an ordinary root, using only mobility floor `c a_R` and a uniform positive quadratic coefficient is enough. The oscillator length tends to zero relative to the fixed root interval. The free-endpoint harmonic response is uniformly bounded after rescaling: compact ranges of positive interval lengths have anchored coercivity; longer intervals are handled by a central anchored interval and integrable reciprocal quadratic tails. Thus every ordinary root contributes at most `C a_R^(-1/4)` regardless of its parameter velocity or proximity to another fold's fixed site.

At a fold-side root of distance r>=C R, mobility is comparable to `a_R r^(-alpha)` and curvature to r squared. The oscillator-length/root-distance ratio is of order `(R/r)^((6+alpha)/4)`. The harmonic bound then gives `C a_R^(-1/4)r^(-3/2+alpha/4)`. The local complement's reciprocal response has order r inverse-cubed; divided by the root response it is bounded by a constant times the same scale ratio, so it is absorbed. These estimates do not need symmetry of the two root slopes.

In the central window, direct Taylor expansion with `s-s_j=R y` and `c-c_j=R^2 tau` gives `g/R^2=gamma_j y^2+beta_j tau+o(1)` uniformly on fixed rescaled intervals and compact tau ranges. Both coefficients are nonzero. The derivative coefficient has a positive lower bound, so any normalized sequence with energy tending to zero would converge to a nonzero constant; the limiting nonzero quadratic-square potential rules that out. This proves the needed uniform Neumann coercivity and hence response O(`R^(-3)`). The spatial center shift is only O(R squared), which is harmless at this scale. A sufficiently large fixed interval factor contains all roots in the window; outside it the local reciprocal integral is also O(`R^(-3)`).

On the rootless side, the exact normal form and bounded coordinate Jacobian reduce the reciprocal response to the integral of `(|t|+x^2)^(-2)`, giving order `|t|^(-3/2)`. The ordinary-root and positive-potential complements are retained in every case. Neumann bracketing and the uniform count of intervals justify summing all these contributions into the displayed global estimates.

### 5. Moment integration and physical transfer

The bounded sampling density and bounded parameter Jacobian give root-side integral `a_R^(-q/4) int_R r^(e-1) dr`, with `e=2-3q/2+alpha q/4`. For q<=2/3, alpha=0 and e is positive. Above that range, direct algebra gives `e=(8-5q)/(q+4)`. The sign changes precisely at 8/5.

The regular-root contribution is `O(a_R^(-q/4))`, while the core is `O(R^(2-3q))`. Their ratio is `R^e`; this proves the required comparison separately below and above criticality. The rootless integral is bounded below q=2/3, logarithmic at q=2/3, and of order `R^(2-3q)` above it. At criticality, `a_R` is of order `M/log(1/M)` and the root integral has one additional factor log(1/R), giving total logarithmic power 7/5. The core and rootless contributions have one fewer logarithmic factor. These checks cover all positive q, rather than presuming q>=1.

For the full-bulk problem, the compactness-derived upper rate bound and positive rate integral meet the accepted comparison theorem. Every proved scalar order grows faster than `[1+log(1/M)]^q`. Therefore the exact ratio `G_q^g/(chi^q P_q^g) -> 1` follows for the optima at fixed bulk data, even though the scalar value here is only known up to comparison constants. The text correctly does not replace that assertion by a generic sharp coefficient. Directly on the proposed trial, its minimum mobility gives only a logarithmic remainder bound; no unsupported bounded remainder is claimed.

## Verification and scope

Independent symbolic simplification checked the endpoint exponent, the core/root comparison identity, and the supercritical budget exponent; all residuals were zero. No scientific numerical result is asserted or needed for this order theorem. I did not run a build that could alter frozen build artifacts; the review is based on the unchanged sources and analytic arguments above.

The final discussion preserves the material limitations: known distinct fold sites and values, nonzero unfolding derivative, two-sided positive bounded sampling near folds, and no identically zero realization. It does not silently extend the conclusion to simultaneous folds or laws supported only on a rootless side. Literature synthesis and later observation-dependent results remain later-stage obligations.

**Findings requiring correction: none. No major issue found.**
