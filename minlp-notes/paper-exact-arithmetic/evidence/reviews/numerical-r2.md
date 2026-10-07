# Numerical R2: review of the final changed scope

Date: 2026-10-05. Independent GPT Sol review after the numerical R1
repair. This is an internal analytic review. I wrote only this report and
made no manuscript edit.

## Verdict and remaining gate

**PASS for the changed mathematical and comparison scope.** The actual
revisions resolve the Opus numerical findings without weakening a
load-bearing result. I found no unresolved mathematical objection, new
equality-hardness claim, incorrect reduction-format attribution, or defect
in the revised warm-start and nullvector interfaces.

**The six-file scope still has a bibliography integration gate.** A fresh
inventory of its 24 cited keys found the same 12 missing height-comparison
keys recorded by the repair writer. They are listed below. Their metadata
and final source wording belong to the Luna/root integration lane. This
review therefore passes the numerical revisions, but does not certify final
submission readiness or the full manuscript.

## Scope and prior-review context

I read `evidence/BRIEF.md`, `evidence/authoring/DECISIONS.md`, both
integration records, and the full files
`evidence/reviews/opus-numerical-r1.md` and
`evidence/authoring/repair-numerical-r1.md`. I inspected the complete four
manuscript diffs against the preserved baseline
`/tmp/numerical-r1-before-duym5tbf`, then read the actual revised passages
and adjacent proof contracts in all six named manuscript files. Appendix B
and Appendix F are byte-for-byte unchanged from that baseline.

The unchanged proofs retain their earlier independent review dispositions;
this round does not replace those full reviews with a fresh whole-paper
audit. The context is preserved as follows:

- `upper-r1.md` reconstructed the Newton, separation, monotone warm-start,
  slack-gap, and adaptive-sign proofs. Its rational derivative bounds,
  returned-cut encoding, and Horner findings were repaired and reread.
  Its remaining optional JPT citation and GLS acceptance questions are
  resolved here by removal of the optional remark and the supplied verified
  queried-center contract.
- `reductions-r1.md` found no theorem blocker. `reductions-r2.md` passed
  the repairs to the block-sum Gram scope, sufficient exposing-square
  explanation, first-radicand bit count, and arbitrary-generator accounting.
  The EY and commutator citations were subsequently reconciled in that
  lane. This round preserves those conclusions.
- `heights-r1.md` found no false theorem or internal proof gap.
  `heights-r2.md` passed the rational-circuit scope, general-input validation
  claims, full-basis PSD example, Gram-order notation, circle rounding, and
  narrowed recovery comparisons. Its corrected `2^{NB}` denominator bound
  remains in Appendix F. Bibliography integration remains separate.
- The independent Opus numerical R1 passed the mathematics of all three
  section/appendix pairs and requested the precise attribution and scope
  changes reviewed below. Its optional BPR replacement was not required;
  the retained BPR import has the accepted source contract.

I used the root-relayed Luna source clearances as the external contracts,
not the repair writer's assertions as proofs. I performed no independent
literature research. The internal changed reasoning was reconstructed by
hand. A delegated read-only second check of the minimum-sign changes also
found no objection.

## Changed claims reconstructed

### 1. Upper bounds and matching classifications — PASS

The contribution paragraph in Section 03 now gives a one-instance upper
bound for all six relations and arbitrary explicit polynomial observables
under the stated strong-convexity or strong-monotonicity hypotheses. It
claims matching completeness only for strict and weak value and coordinate
tests on certified quartics, and coordinate tests on their certified cubic
gradient maps.

This matches the actual proof interfaces. The shifted-comparison table in
`thm:exact-upper` handles equality through
`g^2/4-h(hat x)^2`, whose sign is positive exactly at zero given the gap and
the `g/8` error. The classification theorem supplies lower bounds only for
the four order relations. Those reductions produce nonzero values or
coordinates, so their strict/weak substitutions do not establish equality
hardness. A quartic's gradient is a cubic map with the same Hessian/Jacobian
certificate; its designated coordinate retains the coordinate lower bound.
The revised paragraph states exactly these consequences. Equality remains
an upper-bound statement throughout the affected summaries.

### 2. Square Root Sum attribution and adaptive compilation — PASS

Section 03 credits Allender et al. with a polynomial-time Turing upper
bound in `P^PosSLP`. The separate one-instance consequence is explicitly
attributed to `thm:posslp-closure`, rather than to that source.

The consequence follows from the actual part (b) contract: a deterministic
oracle machine with a polynomial clock for every answer sequence compiles
to one instance. A polynomial-time oracle decision algorithm can be given
that clock without changing its correct run. The paper's padded interpreter
computes each answer bit within a shared integer arithmetic-and-threshold
circuit; part (a) then removes those internal thresholds. This changes the
reduction format and does not assert an ordinary polynomial-time PosSLP
algorithm. The revised prose preserves that distinction and the limitations
for randomness, nondeterminism, and multiple output bits.

### 3. Strongly convex box and queried-center warm start — PASS

The new prior-work paragraph accurately identifies the gradient warm
start's ingredients. From strong monotonicity between `p` and `0`,
`mu ||p||^2 <= -grad f(0)^T p`, hence
`||p|| <= ||grad f(0)||/mu`. The conservative input-length bound places
`p` in the explicit rational box used in Appendix A. The shared
`lem:convex-value` returns an exactly feasible point with objective gap at
most `eta=mu rho^2/2`; strong convexity then gives distance at most `rho`.
The box, requested accuracy, and evaluation bounds have polynomial encoding
length. I checked the actual shared value-lemma statement and proof
interface in Section 02/Appendix C. No unbounded-domain radius theorem is
needed in this warm start, and the Slot–Steurer–Wiedmer credit is now
separate.

For the nongradient warm start, the accepted source contract is GLS
Theorem 3.2.1 at printed pages 87–88: acceptance returns the queried current
center. Remark 3.2.33 preserves that alternative while allowing cuts valid
only on a fixed retained core. The revised Appendix A uses exactly that
contract. It does not infer acceptance merely from proximity to the target
set.

The unchanged internal argument still applies. Acceptance of
`||T(x)|| <= mu rho` implies `||x-p|| <= rho`. Rejection and the local
Jacobian bound give `||x-p|| > mu rho/Lambda`; with
`delta_0=mu^3 rho^2/(2 Lambda^3)`, the cut is strictly negative on
`B(p,delta_0)`. Thus every rejection retains the same ball. That ball
contains a cube of volume `(2 delta_0/n)^n`, which is larger than the
requested final volume `(delta_0/n)^n`, ruling out termination by a small
containing ellipsoid. The existing returned-vector encoding hypothesis and
GLS rounded-center contract account for ordinary bit complexity. In
dimension one, the revised word “rational” is correct: midpoint denominators
divide the endpoint denominator times a power of two, even when rational
`R_0` is not dyadic.

### 4. EY bounded-circuit comparison — PASS against cleared contract

The current Section 04 comparison gives exactly the supplied EY2010
Lemma 5 contract: a linear-size circuit over addition, multiplication, and
division, all gate values in `(0,1)`, and an order comparison of its output.
It does not invent a threshold, stronger output model, or additional gate
operation. The manuscript sentence matches the root-relayed Luna clearance
recorded in the integration/repair records. This source is comparison
credit; the internal sign compilers and realizations do not depend on it.
This is a manuscript-contract consistency check, not fresh primary-source
verification.

### 5. Nonzero auxiliary signal and minimum sign — PASS

The revised introductory statement and `eq:reductions-tilt-signals` use the
exact compiler promise. Write `s_o=xi_o-1` and `s_e=xi_e-1`. Appendix B's
auxiliary chain gives `0<s_e<=delta^{2^{T+1}}`, while the output signal has
order `d<=2^T` and `|s_o|>=delta^d/2`. Therefore

`s_e^2 <= delta^{2^{T+2}} <= delta^{d+3}
       <= 2 |s_o| delta^3 <= |s_o|/8`.

The exponent comparison holds even at `T=0`, and `delta<=2^{-30}` more
than suffices for the last inequality. Scaling by `1<=kappa<2` gives
`u_0!=0`, `v_0!=0`, `|v_0|<=1/8`, and
`u_0^2 <= (kappa/8)|v_0| <= |v_0|/2`. No sign of `u_0` is used.

For `v_0>0`, `G(p)=-u_0^2 v_0<0`. For `v_0=-t<0`, the modulus-one
strong-convexity bound gives

`G* >= u_0^2 (t-2t^2-u_0^2/2) >= u_0^2 t/2 > 0`,

because `t<=1/8` and `u_0^2<=t/2`. Thus both branches remain strict with
the weaker, exactly stated nonvanishing premise. The perturbation's printed
Gram also remains valid: its Frobenius norm squared is
`12 kappa^2+10<64`, so scaling the original Gram to margin at least nine
leaves `M_G>=I`. No certificate or reduction changes are needed.

### 6. Common kernel and Appendix K reference — PASS

Section 07 retains the maximum-rank argument. For positive semidefinite
matrices, zero quadratic form is equivalent to annihilation, so
`ker(G_0+G)=ker G_0 intersect ker G`. Feasibility is convex. If some feasible
`G` failed to annihilate a vector in the kernel of a maximum-rank feasible
`G_0`, their feasible midpoint would have a strictly smaller kernel and
larger rank. Hence the maximum-rank kernel is the common kernel.

The replacement example reference resolves to the actual
`prop:bnd-nullvector` and `app:bnd-nullvector` in Appendix K. I checked its
matrices directly. The two blocks of `A(x)` are PSD respectively when
`|x|<=sqrt(2)` and `x>=sqrt(2)`, so together they force `x=sqrt(2)`.
`X(2,0)` is rational and positive definite. Imposing `X e_1=0` forces
`t=0`, leaving exactly the irrational feasible matrix `X(0,sqrt(2))`.
The revised Section 07 sentence describes restriction by annihilation,
which is the operation proved there. The common-kernel proof and the full
counterexample remain available without duplicate printing.

### 7. Removal of the optional explicit-bound remark — PASS

The optional JPT remark and its label/citation are absent from all six
files. Its deletion removes no dependency of the separation theorem or its
applications. The retained `lem:separation` still derives algebraicity and
the nonzero gap from the verified one-block elimination contract, then uses
the nonzero integer constant coefficient after removing a zero-root factor.
Its fixed absolute constant and explicit
`2^{-2 tau d^{c_0 s}}` bound still feed the shared Newton, slack-gap, and
parameterized uses. No load-bearing separation statement was lost.

## Outstanding bibliography integration

The scoped inventory still finds these keys missing from `references.bib`:

`GaertnerMagronVallentin2026`, `HeltonNie2010`, `Jiang2021`,
`KolmogorovNaldiZapata2024`, `Laplagne2020`, `Lasserre2009`,
`ODonnell2017`, `PatakiTouzov2024`, `PeyrlParrilo2008`,
`RaghavendraWeitz2017`, `SafeyElDinZhi2010`, and `Zhang2020`.

The earlier Basu/BPR/GLS/EY keys now resolve. The remaining list is a
submission integration obligation, not an unresolved internal mathematical
objection. The root was notified; this reviewer did not edit the bibliography
or independently research these sources.

## Reviewed SHA-256 hashes

These actual hashes match the numerical repair record:

```text
0db409d6a3b1e406e5e882d51311fb2df15ec345b23bea4667d61eaf7f6c2ee5  sections/03-upper.tex
e0a65e32b8d02c2b30d29882c71c37d8f781388a73aa53bbc13dba9fbad5269d  appendices/A-upper.tex
0673ebfc72cfd606b7ce7d3f35d6e027520fa59188f4540b5c657f69b7ebd50e  sections/04-reductions.tex
1c78b5cd28b75854390eac3d8f48ffa6c623ecb7061f3bc4142375d70a692b94  appendices/B-reductions.tex
59d80f97d0d99e05972c70ed37e1f56bf3effcb28621991db3f659bb6cd77901  sections/07-heights.tex
523e1364bd3cc09c05d4f79d889826a1d4b010ead6276e8c1e71629b85d021d3  appendices/F-heights.tex
```

## Targeted checks actually run

- `cat`, `sed -n`, `rg`, `rg --files`, and `wc -l` read the named evidence,
  current manuscript passages, shared value interface, and Appendix K
  construction. Some initial path lookups used incorrect baseline basenames
  or guessed contrast filenames; corrected paths were used for the actual
  comparisons and proof reading.
- `diff -u` compared each of the four edited manuscript files with its
  counterpart under `/tmp/numerical-r1-before-duym5tbf/{sections,appendices}`.
  Each returned 1 for the expected revisions, whose full diffs were inspected.
- Separate `cmp` commands compared Appendix B and Appendix F with those
  baseline copies; both returned 0.
- `sha256sum` on the six manuscript files supplied the hashes above; a final
  reread of those hashes checked snapshot stability.
- One inline Python document inventory extracted citation keys only from the
  six reviewed files and checked them against the active bibliography. It
  found 24 cited keys and the 12 missing entries above. The same scoped
  check found neither the removed optional label nor its JPT citation in
  any of the six files.
- This report was checked for a final newline, trailing whitespace, and
  control characters, and with `git diff --no-index --check /dev/null
  evidence/reviews/numerical-r2.md`. No hygiene diagnostic was produced;
  the no-index command returns 1 because this is a new file.

No computational experiment, mathematical script, symbolic calculation,
compilation, historical checker rerun, project-wide verification, CI
inspection, literature research, or KB mutation was performed. The findings
are local analytic and document-review evidence, not CI results.
