# Independent review: stage 06, round 01, reviewer 2

Date: 2026-09-07. Reviewed snapshot `fd49a0c7de991734f21f20428b8a74ba19e44a0ffa3204ed80a925056ab5fb2f`. Independently verified all hashes in its manifest; all matched. Read the entire finite-precision section, its author handoff, accepted local-response, measure-relaxation, placement and bulk-transfer prerequisites, and supporting notation/claim changes. No coordinator-check file or other reviewer report was read. No source edits, delegation, or shared-output build was performed.

## Verdict

**Accept Stage 06. No major or minor issue found.** The finite positive-ratio crossover is supported by variational localization and uniform recovery; the simultaneous coarse limit has a separate unrestricted proof. Neither is inferred merely by matching endpoint constants. This is a mathematical stage acceptance, not the final whole-paper or novelty verdict.

## Local uncertain-center problem

### Scaling and arbitrary-design lower certificates

The local change `ell=(m/a)^(1/5)`, `D=a ell⁴ d`, and `h=(a ell²)⁻¹f` gives mass `a ell⁵=m` and common response factor `(a ell)⁻¹=a^(-4/5)m^(-1/5)`. The center interval rescales by w/ell, yielding the stated local argument.

For the large-width lower certificate, the test amplitude is η^(1/2) and width η^(-1/4). Its source and reaction both scale as η^(1/4). The derivative squared amplitude is η^(3/2); averaging translations over a center interval of length η and extending that interval to the line bounds its kernel by `η^(3/2)η^(-1/4)/η=η^(1/4)` times Tψ. Integrating against any unit-mass field therefore gives the exact lower bound C0 η^(1/4), with no regularity or allocation assumption. The separate lower bound Cpl follows from permitting exact observation of the center.

The constant patch upper bound has unit padding on both sides of every possible center. For large η its harmonic length is (η+2)^(-1/4), so both endpoints recede in harmonic units uniformly over all centers. Asymmetric endpoint distances do not affect the oscillator limit: bracketing a centered interval at the smaller endpoint distance and integrating reciprocal quadratic tails proves the same uniform limit. The exterior reciprocal contribution is at most two. Thus the upper order and exact coefficient C0 at large η are justified.

### Rough-density endpoint lemma, continuity, and attainment

The quadratic source tail is correctly L^(-1/2), not the stronger quartic tail from Stage 3. A fixed-core lower mobility bound and a positive-potential anchor control the local H¹ norm, while the quadratic potential controls exterior L² mass weighted by x². These bounds supply uniformly bounded maximizing energies and make source integrals converge after local weak compactness.

On a unit interval near large x, the squared function and derivative norms are bounded by `C|x|⁻² E` and `C|x|^α E`. The one-dimensional interpolation estimate therefore gives `|f(x)|²≤C(|x|⁻²+|x|^(α/2-1))E`. Since α<2, the limit is bounded. This makes the cutoff derivative error vanish against an arbitrary integrable, possibly unbounded density d. The compact weighted-derivative approximation is valid because d has a positive lower bound on each compact interval: convergence in L²(d dx) implies L¹ convergence of derivatives, and an integral correction followed by integration gives uniform function convergence. The limiting finite-energy function is consequently in the smooth-test completion. This closes the natural-endpoint upper limit rather than assuming a maximal weighted domain equals the chosen minimal one.

For centers in a fixed compact set, the shifted-potential difference is bounded by `C|z-z′|(1+x²)` and that weighted norm is controlled by the original energy. Nearby forms therefore bound each other with multiplicative factors tending to one, proving the required fixed-profile continuity.

The singular-mass removal construction from Stage 3 applies because the quadratic potential is bounded on each fixed test support. Compact-test joint lower semicontinuity under vague measure convergence and center convergence gives the Fatou lower bound after the fixed parameterization z=ηv. Removing singular mass and adding a density to replace missing mass yields a unit-mass competitor without increasing cost. This proves attainment without an unproved tightness claim. The same argument proves lower continuity in η. The positive-tail mixture has the exact energy ordering needed for `T_z(d_epsilon)≤(1+epsilon)T_z(d)`. Its compact-center continuity proves upper continuity of the value. Reflection averaging is valid because the center interval is symmetric. No uniqueness or width monotonicity is used.

## Conditional optimum: half budgets and exact-coordinate recovery

Reflection preserves each k_c, so it preserves a conditional ensemble even for an asymmetric offset bin. Convexity permits symmetric competitors, whose two half-circles have exactly m=M/2. Thus the paired factor is justified at the optimization level, not presumed in the unrestricted lower bound.

With `a_I=1-c_I²` and `ell_I=(m/a_I)^(1/5)`, expansion at the positive root gives

`(c+cos(r_I+ell_I x))/(sqrt(a_I)ell_I)=eta_I v-x+O_K(ell_I x²)`.

The uncertainty argument is therefore `eta_I=Delta/(sqrt(a_I)ell_I)=2^(1/5)(Delta/M^(1/5))a_I^(-3/10)`. Normalizing the pushed half-circle mass by m gives total mass one before passage to the vague limit. The source-test amplitude `(a_I ell_I²)⁻¹` makes each root's response factor `(a_I ell_I)⁻¹`. For the derivative term, the remaining prefactor is `m/(a_I ell_I⁵)=1`. Reflecting the compact test gives the total factor `2a_I^(-4/5)(M/2)^(-1/5)`. Fatou over v, singular removal, and mass completion give the local lower value for arbitrary original fields, including escaping mass and singular weak limits.

For recovery, the exact coordinate derivative is `dx/ds=1/(ell_I w_I)`. With `D=a_I ell_I⁴ w_I d_epsilon`, its two metric factors cancel the derivative transformation precisely. Source and reaction keep the bounded weight w_I, and the potential is exactly `(x-eta_I v)²` after scaling. The neighborhood mass is `m∫w_I² d_epsilon=m[1+o(1)]`, so a scalar factor tending to one restores the exact budget. The rough-density endpoint lemma applies on the two asymmetrically expanding coordinate intervals. All actual roots remain inside the fixed regular neighborhoods, making the exterior reciprocal response uniformly bounded. Its normalized contribution tends to zero.

The sequential compactness argument gives uniform localization on every compact regular offset set for bounded precision ratio. A finite cover of the compact local-width range by fixed regularized profiles makes this a deterministic bin policy with uniform error; there is no dependence on the unknown within-bin offset. Continuity of the local value also justifies the subtraction of Fctr(eta_I) in the displayed uniform conditional limit.

## Uniform estimates through bins containing folds

In a regular bin, the possible-root span is w≈Delta/sqrt(t) and padding is ell=(M/t)^(1/5). With mobility e≈M/(w+ell), its harmonic length `(e/t)^(1/4)` is at most a constant times ell. At t≥C(Delta+M^(2/7)), the patches lie in separated quadratic neighborhoods and every root has the necessary endpoint margin. Their interior response is `Ce^(-1/4)t^(-3/4)`. The exterior terms `C/(t ell)+Ct^(-3/2)` are no larger: e≤M/ell=t ell⁴ and ell≤C sqrt(t). Expanding (w+ell)^(1/4) produces exactly the two envelope powers 4/5 and 7/8.

For grouped fold bins, R≈sqrt(W), e≈M/sqrt(W), and W≥M^(2/7) imply W≥c e^(1/3). The quartic core integrated in the offset has size e^(-1/6); the separated-root part contributes `e^(-1/4)∫_{e^(1/3)}^{CW}t^(-3/4)dt`. Both are at most `Ce^(-1/4)W^(1/4)=CM^(-1/4)W^(3/8)`. The rootless tail is included in the e^(-1/6) estimate. Finite natural endpoints cause no missing large-parameter assumption because the patch retains a fixed relative margin beyond every possible root; harmonic root brackets and direct rootless reciprocal bounds supply the stated finite-interval estimates.

The exterior patch response integrated over the group is O(W^(-1/2)). Its ratio to the fold bound is `M^(1/4)W^(-7/8)≤1`. Remaining rootless bins have the same bound. A bin crossing a grouping boundary enlarges the group by at most Delta≤W, so the construction is independent of grid alignment.

For the unrestricted coarse-order lower bound, bump width b=(M/Delta)^(1/4) is much smaller than a regular root arc when Delta≥L M^(1/5). Source minus reaction is of order b⁻¹, while the averaged derivative kernel times the full mass is also O(b⁻¹); a small fixed amplitude gives a positive bound for every design. The exact-observation lower bound covers the complementary precision range. The upper envelope is integrable, and

`M^(-1/4)W^(3/8)≤C[M^(-1/7)+M^(-1/4)Delta^(3/8)]`

is smaller than the sum of the two desired scales at every joint rate. The separate fixed-N statement is also valid: a positive-length regular piece supplies the lower bound, and a single predetermined mean design supplies the upper bound.

## Finite-ratio crossover and all constants

The per-bin conditional value has leading factor `2^(6/5)a_I^(-4/5)M^(-1/5)Fctr(eta_I)`. Multiplying by the bin probability Delta/4 produces exactly the coefficient density in H. Uniform conditional localization and continuity justify Riemann sums on a regular compact set despite the changing number of policies.

The omitted normalized regular contribution is bounded by an integrable combination of t^(-4/5) and t^(-7/8). For bounded Delta/M^(1/5), the fold estimate after normalization is bounded by terms of order M^(2/35) and M^(1/40), both vanishing. Thus extending the compact set to the full root-containing interval proves the exact finite-ratio limit, including zero. The same envelope proves continuity and finiteness of H. At zero its integral is `2^(6/5)Cpl B(1/2,1/5)/4=Kobs`.

Independent high-precision arithmetic recovered Kobs≈22.404628230749138 and Kcoarse≈25.723827388763291. The symbolic finite-ratio fold exponent is `-1/20+(3/8)(1/5)=1/40`.

## Separate simultaneous coarse limit

The separate proof is necessary and supplied. On a regular compact set, let w be one root arc's length, e=M/(2w), and b=(e/a_I)^(1/4). The coarse assumption is exactly b/w→0 there. A paired harmonic test has averaged source minus reaction `2z0(2Iψ-Uψ)+o(z0)`, where z0=e^(-1/4)a_I^(-3/4). The conditional density along each arc is `(1+o(1))/w`. Because the two arcs are spatially separated, the pointwise sum of their derivative kernels is bounded by one full-arc kernel, not twice that kernel. Multiplying by total mass M=2ew gives the derivative penalty `2z0 Tψ[1+o(1)]`. This is the critical paired-root factor and yields the unrestricted lower coefficient 2C0 z0 without an assumed allocation.

For recovery, equal mass on the two arcs padded by p=sqrt(bw) changes e only by 1+o(1). Every root is many harmonic lengths from the endpoints, while the total arc width still tends to zero, so frozen curvature and natural-endpoint localization are uniform. The exterior reciprocal contribution divided by z0 is O(b/p)→0. Consequently

`V(M,I)∼2^(5/4)C0 a_I^(-7/8)M^(-1/4)Delta^(1/4)`.

Here a_I^(-7/8) follows from a_I^(-3/4) times w^(1/4)≈Delta^(1/4)a_I^(-1/8). The joint coarse condition implies W∼Delta, so the normalized fold contribution is O(Delta^(1/8)) and vanishes. Integrating with density 1/4 gives `2^(-3/4)C0 B(1/2,1/8)`. Independently inserting the local large-width limit into H gives the same factor: `2^(6/5)/4 × 2^(1/20)=2^(-3/4)`, and its curvature exponent is `-4/5-3/40=-7/8`. This consistency check is additional to the simultaneous proof, as the text correctly states.

## Physical and informational interpretation

The finite policy set avoids measurable selection issues, and every recovery normalization preserves the per-bin budget. The accepted observation-uniform bulk comparison applies to all these changing partitions, so it transfers the scalar results with the stated dimension conversion. The bits statement follows from Delta=4·2^(-B); one additional bit remains within a joint coarse sequence and changes its leading scale by 2^(-1/4). The text correctly restricts monotonic information ordering to nested partitions and distinguishes noiseless quantization from general noise or measurement-channel optimization.

No currently actionable mathematical gap, normalization error, unsupported interpretation, or proof-essential clarity issue was identified.
