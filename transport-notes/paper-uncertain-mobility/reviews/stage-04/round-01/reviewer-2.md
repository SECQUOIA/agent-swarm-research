# Independent review: stage 04, round 01, reviewer 2

Date: 2026-09-07. Reviewed frozen snapshot `da3db325e0812991ad97d79560c4c8aeb99b83d7260ade75d6172d61d3b4aaa6`. Recomputed every manifest hash; all matched. Read the complete new generic-fold section, author handoff, supporting notation/claim/plan changes, and the accepted local and design estimates it invokes. No other reviewer report or coordinator-check file was read. No manuscript edits, delegation, or shared-output build was performed.

## Verdict

**Accept Stage 04. No major or minor issue found.** The theorem establishes the stated three optimized orders under its explicit sufficient assumptions. It does not claim the sharp cosine constants for a generic family, and the exact scalar-to-bulk ratio is supported by the earlier comparison theorem.

## Independent checks

### Uniform geometry and assumptions

The compact zero set admits a finite cover by neighborhoods where either g_s has fixed nonzero sign or g_ss has fixed nonzero sign. Each spatial slice of such a neighborhood has at most one or two roots respectively, so this does give a uniform finite root count. Outside open fold products the remaining closed zero set is compact and has no zero of g_s, giving a positive minimum ordinary-root slope. Any sequence of distinct ordinary roots with separation tending to zero would have a multiple-zero limit; excluding neighborhoods of the listed folds prevents that limit. Thus the uniform ordinary-root intervals used in the upper argument can be chosen sufficiently small and disjoint.

The assumptions also exclude an identically zero realization: that would create an entire circle of points with g=g_s=0. Continuity of c↦∫g² on compact I then gives a strictly positive rate anchor, while compact C⁴ regularity gives the uniform upper rate bound. These are sufficient for the physical transfer theorem later in the section.

The fold coordinate is justified directly by the implicit function theorem applied to g_s and by the integral Taylor remainder. The factor b_j has nonzero fixed sign near the fold, so its square-root coordinate has a nonzero spatial derivative after shrinking the neighborhood. Differentiating h_j(c)=g(z_j(c),c) at the fold eliminates the g_s z_j′ term, giving t′=-σ_j g_c≠0. The center shift is O(|c-c_j|)=O(|t|). Thus the two roots lie a distance comparable to sqrt(t) from the fixed fold site and have slopes comparable to sqrt(t); the drift of the critical center is smaller than that distance. Differentiating g(u,C_j(u))=0 twice gives C_j″=-g_ss/g_c at the fold. On one branch, its Jacobian is comparable to the distance r, so a root-position interval of length r has parameter probability of order r².

No nonzero g_c assumption is imposed at ordinary roots. The upper construction separately protects those roots, including stationary branches and ordinary roots occupying another fold's spatial site at a different parameter value. Distinct fold sites and parameters make the proof's spatial and active-parameter localization consistent.

### Arbitrary-design moving-shell lower bounds

On the shell u∈[r,3r/2], the lower density bound and |C_j′(u)|≈r give the root-position integration measure comparable to r du. The translated bump supports fit in the enlarged shell when ell=κ(m/r³)^(1/4) and m≤c*r⁷. Fubini bounds the average derivative cost by Cm/(r ell), while local Taylor control bounds reaction energy by Cr² ell³. The quotient numerator is of order ell². Jensen for x^(-q), valid for every q>0, therefore gives

`r² ell^(2q)[m/(r ell)+r² ell³]^(-q) ≍ r^(2-5q/4)m^(-q/4)`.

This calculation uses only the mobility mass m, not a representative value, regularity, or support shape. Zero m makes the shrinking-width lower bound infinite, as stated.

A fixed sampled shell proves M^(-q/4) below the threshold. For q=8/5, disjoint geometric spatial shells also have disjoint parameter images because C_j is monotone on the retained branch. Taking their smallest radius to be a sufficiently large multiple of M^(1/7) makes the small-mass condition valid even when an entire budget is concentrated in one shell. There are N≈log(1/M) such shells. The inequality `∑m_n^(-2/5)≥N^(7/5)M^(-2/5)` follows from their total mass constraint and the convex negative power.

For the supercritical lower bound, on a spatial radius R and parameter window of width R², Taylor expansion gives |g|≤CR², hence k≤CR⁴. The derivative and reaction costs are bounded by CM/R² and CR⁵, while the squared source is comparable to R². Choosing R=M^(1/7) yields J≥cR⁻³ on a window of probability at least cR². This proves the exponent (2-3q)/7 for every competitor. Additional roots cannot invalidate a compact local test.

### Exact-budget graded trial and all local upper bounds

The nonnegative exponent α=max(0,(6q-4)/(q+4)) produces a global floor ca_R. Its normalization integral is finite-order constant, logarithmic, or proportional to R^(1-α) in the three respective regimes. With the specified cutoffs, a_R≈R^(6+α) in every case. For each positive M the field is both bounded and strictly positive; no uniform-in-M positive floor is being presumed.

For a separated fold-side root, local mobility is comparable to a_R r^(-α), curvature to r², and the harmonic width divided by r is `(a_R/r^(6+α))^(1/4)≈(R/r)^((6+α)/4)`. At r≥CR the interval can contain a fixed number of harmonic widths uniformly. The Neumann harmonic bound therefore yields `Ca_R^(-1/4)r^(-3/2+α/4)`. The remaining local reciprocal-potential integral is O(r⁻³), whose ratio to that bound is at most C(R/r)^((6+α)/4), so it is absorbed.

In the central window, s-s_j=Ry and c-c_j=R²τ give

`R⁻² g(s,c) = γ_j y²+β_j τ+o(1)`

uniformly on a fixed interval in y and bounded τ. The scaled derivative coefficient has a fixed positive lower bound because D_M≈R⁶ there. Uniform Neumann coercivity follows by contradiction: vanishing derivative energy would force an L²-normalized sequence to approach a nonzero constant; after a parameter subsequence, the nonzero quadratic-square limiting potential prevents that constant from having zero reaction energy. This argument is sufficient even when the quadratic-square potential has roots. The source response scales as R⁻³. Taking the fixed interval sufficiently large contains all local roots, and the exterior local reciprocal integral has the same order.

On the rootless side the exact normal form and bounded Jacobians give ∫(|t|+x²)⁻² dx=O(|t|^(-3/2)). Ordinary roots use the independent global floor ca_R and their uniformly nonzero slope, giving O(a_R^(-1/4)) each. The finite root count and positive-potential remainder complete the Neumann partition. These terms are explicitly retained, rather than incorrectly treating the active fold as the only possible root.

### All moment ranges and endpoints

After changing from t to r=sqrt(t), the fold-side integral has endpoint exponent

`e=2-3q/2+αq/4`.

For q≤2/3, α=0 and e=2-3q/2>0. For q>2/3, independent symbolic simplification gives e=(8-5q)/(q+4). Thus it changes sign at exactly 8/5.

Below 8/5, a_R≈M and the fold integral is O(M^(-q/4)). The central term relative to a_R^(-q/4) is R^e, which tends to zero. The rootless integral is bounded for q<2/3, logarithmic at q=2/3, and of order R^(2-3q) above 2/3; in each case it is no larger than the desired subcritical order. In particular, the separate q=2/3 logarithm does not alter the theorem.

At q=8/5, a_R≈M/log(1/M), R≈[M/log(1/M)]^(1/7), and e=0. Hence the root integral is M^(-2/5)log(1/M)^(7/5). The central and rootless terms are only M^(-2/5)log(1/M)^(2/5), with one fewer logarithm.

Above 8/5, the lower endpoint dominates the root integral, giving a_R^(-q/4)R^e=R^(2-3q)=M^((2-3q)/7). The ordinary-root term divided by this order is R^(-e), which tends to zero because e<0. These comparisons cover every fixed q>0 and require only a bounded sampling density for upper estimates.

### Physical transfer, scope, and clarity

The compact rate anchor and upper bound verify the accepted transfer assumptions. Each proved polynomial scale dominates the logarithmic bulk moment. Therefore the generic full-bulk value is asymptotic to χ^q times the scalar optimum even though the scalar theorem supplies only comparison orders, not a sharp generic coefficient. The stated direct logarithmic bound for the explicit trial is also valid because its minimum mobility is at least ca_R and log(1/a_R)=O_q(log(1/M)).

The section clearly separates the single sampled fold needed for lower bounds from the collection of known fold sites needed for its upper trial. It retains stationary ordinary roots, finite-domain endpoints, and all q-dependent integrability cases. The excluded sampling, higher-degeneracy, simultaneous-fold, vanishing-bulk, and fabrication-constraint cases are not silently claimed. No proof-essential clarification or currently actionable editorial issue was identified.
