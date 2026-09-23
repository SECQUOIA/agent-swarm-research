# Stage 3 independent review: readability and mathematical completeness

I reviewed all of sections/last-event.tex, sections/daughter-comparison.tex, sections/critical-last-event.tex, appendices/product.tex, and the supplement script and saved JSON. I checked their use of the accepted Stage 1/2 framework, the current bibliography, README, and coverage map. I did not read other current Stage 3 review reports or communicate with other reviewers. All build and script execution occurred in an isolated copy at /tmp/stage3-readability-wq7r1sx1.

The mathematical results and proofs are clean. I found no major issue. The new sections explain the distinction between a first-event hazard along a fragmentation-only trajectory and the actual full-process compensator, correctly condition at ordinary jump stopping times rather than at the last event, and distinguish conditional size asymptotics from calendar-time asymptotics. The sharpness statements are backed by realizable positive finite-support population measures.

## Required minor corrections

### S3-RDB-01 — MINOR: specify coagulation when asserting a finite total event count

**Location:** sections/last-event.tex:95, the final sentence of the proof of Theorem 5.1. The same ambiguity appears in the Stage 2 integration at sections/auxiliary-process.tex:281.

**Reason:** “Finite-horizon nonexplosion now implies a finite total event count” is too broad: the conclusion is a finite total number of auxiliary coagulations. The allowed controls can have \(F(\infty)=\infty\), in which case the state-independent fragmentation clock has infinitely many events almost surely. This matters especially at criticality, where fragmentation continues after the finite last coagulation. The theorem statement correctly refers to \(K_\infty\); the proof's conclusion should preserve that distinction. Likewise “each path has only finitely many events” in the earlier section should specify which events.

**Fix:** Write “Finite-horizon nonexplosion now implies a finite total coagulation count.” Replace the earlier wording with “each path has only finitely many coagulation events.” These are wording corrections, not gaps in the proof.

### S3-RDB-02 — MINOR: reconcile the Stage 2 acceptance status

**Location:** development/COVERAGE.md:29 and 64, compared with README.md:7 and the supplied Stage 3 review scope.

**Reason:** The README says Stages 1 and 2 are accepted, while the coverage map still says Stage 2 coordinator verification is pending. The inconsistency makes it unclear which review gate the current manuscript has passed.

**Fix:** Update the two stale Stage 2 status statements to reflect its accepted state. This does not affect any scientific claim.

## Mathematical verification

- **Controlled tails and path laws:** The fragmentation-only process has the correct mean \(xe^{-[F(s)-F(t)]}\). Multiplication by the count factor cancels fragmentation activity, giving expected first-event hazard \(q u_{t,T}\). Conditional exponential survival and Jensen give the stated bound, including the infinite horizon. The two cases for total coagulation activity prove the vanishing last-event tail. Common clocks and innovations preserve each process's daughter law after divergence, and the coupling inequality applies to the whole finite or infinite future path.
- **Time moments and rare counts:** The exponential-moment formula follows from the tail integral. Fixed-window counts have mean \(b\ell\) despite their almost-sure eventual disappearance. Conditioning and Hölder give the stated lower bounds, including possibly infinite higher moments. The scalar factor \(c_p\) and its optimizer equation are correct. The Borel generating-function calculation gives \(h(t)\sim\sqrt2 e^{-bt/2}\); its status as a deduction from a classical solution is clear.
- **Daughter comparisons:** Both benchmark hazards have first moment one, even when a second moment is unavailable. The drift, fragmentation, and killing terms in both benchmark equations have the correct signs. Jensen and the chord inequality yield the two supermartingale/submartingale directions. The terminal comparison uses \(\mathbb E Y_s=qe^{-bs}\) and bounded survival factors, so it does not assume pathwise monotonicity of normalized size. The positive \(\varepsilon\)-daughter approximation controls both the pre-reset hazard and the remaining hazard in \(L^1\), proving the claimed limiting sharpness.
- **Overlap and product constants:** Concavity gives the overlap lower coefficient at the correct point \(q=1\), and monodispersity realizes it. The mean-one two-point construction establishes upper sharpness without using an inadmissible zero-size atom. At criticality, the holding-time normalization gives \(S=\sum_{k\ge1}2^{-k}E_k\), with mean one and variance one third. Its recurrence and displayed Taylor coefficients agree. The constants \(1/2\) and \(1-\Psi(1)\) have the stated distinct scopes.
- **Critical density and Laplace identities:** The recurrence cancels the loss in the bounded test \(\Psi\). The resulting pair integrand \(q\Psi(q+v)\) is bounded, so total-variation continuity supplies a continuous equal-split density without a higher size moment. The Laplace PDE and mixture identities have the correct derivatives and signs, including at Laplace argument zero.
- **General daughters and lower time tail:** Projecting the no-successor event at each genuine coagulation stopping time, then using the compensator, proves the general density. The rational envelope gives \(j(t)\le bh(t)\), hence the stated lower calendar-time tail. The small-state/high-state initial preparation proves instantaneous sharpness of \(b\). Positivity of \(h(0)\) makes the exponential moment diverge even at the endpoint \(r=b\). The unknown interval for the exact threshold is stated explicitly.
- **Scalar obstruction:** The proposed two-point laws are strictly positive, have mean one, and have every positive moment finite individually. Their tail probability is asymptotic to \(\varepsilon\), whereas the dissipation is bounded by \(\delta_\varepsilon+\Psi(R_\varepsilon)\). The finite-product estimate decays faster than any prescribed inverse power, proving the advertised obstruction for every fixed positive exponent. The result does not overclaim an obstruction to all scalar inequalities.
- **Product appendix:** Splitting the product at \(\lfloor\log_2q\rfloor\) gives the displayed quadratic logarithmic term, periodic correction, and positive remainder with the stated signs. The endpoint values of the periodic function match. The refined remainder coefficients follow from the geometric sums of the first three powers. The finite-product certificate and the exact rational endpoint assertions are valid.

## Exposition, integration, references, and reproduction

The presentation is sufficiently detailed for a mathematical chemical-engineering reader. It explains the zero-reset benchmark as a limiting comparison rather than an admissible physical split. It also distinguishes conditional envelope sharpness, uniform overlap sharpness, instantaneous time-tail sharpness, and an exact long-time exponent. The latter remains unclaimed, as it should. The large-\(q\) product appendix explicitly concerns size and cannot be mistaken for an asymptotic formula for \(h(t)\).

The dependence on Stage 1/2 is sound: fractional affinities require only the finite-count mass-conserving class, the jump construction is nonexplosive in that class, and all new sharpness preparations fall within the finite-second-moment existence theorem. The Stage 2 explanation of atomic versus lattice logarithmic laws is now accurate. The new sections do not reintroduce an independence assumption for adaptive daughter marks.

The product normalization and its precise cited equation numbers agree with [Bertoin–Biane–Yor, equations (1.3), (1.6), Theorem 1.1(i)](https://monge.univ-eiffel.fr/~biane/q_poisson.pdf): the manuscript's \(S\) has law \(I^{(1/2)}/2\). The contextual description of generator comparisons is consistent with [Rüschendorf–Schnurr–Wolf](https://arxiv.org/abs/1505.02925); the manuscript independently proves the particular comparison it uses.

The isolated make completed successfully and produced a thirty-page PDF. The final log had no undefined citations, unresolved references, label-rerun warnings, or overfull/underfull boxes. A representative new page was visually legible. Running the copied supplement script succeeded and reproduced the saved JSON exactly. I also executed the appendix's rational assertions independently; both strict decimal inequalities passed. The supplement correctly labels the overlap interval as certified and the counterexample values as illustrative floating-point evaluations.

**MAJOR count: 0. MINOR count: 2. Recommendation: accept Stage 3 after the two minor corrections. The mathematical proofs are clean.**
