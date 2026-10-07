# Independent final review of Gaussian binary least squares

Disposition: **approved for integration within the stated mathematical scope**. The completed chapter contains full proofs of its selected nonstandard claims, either in the main section or in its reachable appendix. I found no unresolved mathematical blocker, missing proof dependency, or required author repair in the reviewed version. This is a mathematical and manuscript review; it does not certify the integrated LaTeX build or replace the literature lead's final source accounting.

The writer declared both TeX files complete before the full final read. I then reread the actual saved files and checked their hashes before and after the scoped consistency check. The section hash below includes the subsequently reviewed typesetting change described after the table:

| File | Reviewed SHA256 |
|---|---|
| `sections/binary-least-squares.tex` | `bd256b308009b27da0bf3bd01b6fff6bb4ac645b978bdfd54054aec1b3ed7043` |
| `appendices/bls-proofs.tex` | `8fb602516aba588cceee13ced87b89d2799ca05db1498cc1400c55405ffe8e6c` |

Narrow follow-up review: the root moved the final example `exp(Theta(N log log N/log N))` from inline mathematics to an unnumbered display to remove an overfull box. I inspected the saved paragraph at section lines 552–561. The formula, its fixed-positive-constant hypothesis, and the planted-recovery qualification are unchanged. The mathematical disposition remains approved, with no new findings. The original full-review section hash was `f0b331b43e3995a1f514825396acf28f832df0ab304c53af09b37d69591d232c`; the appendix hash is unchanged. The follow-up used only a scoped paragraph read and `sha256sum`, without repeating unchanged proofs or other checks. The root reports that the integrated PDF builds; that build was not run by this reviewer.

The review used `BRIEF.md`, `AUTHORING-CONVENTIONS.md`, `ARCHITECTURE-DECISION.md`, `ISSUES.md`, `INCOMING-AUDITS.md`, the BLS developments and scope corrections in `AUDIT-DISCRETE.md`, the complete `REVIEW-NNLS-R1.md`, the relevant original binary-least-squares note, the available `LITERATURE-KEYS.md`, and the final `AUTHOR-BLS.md`. The audit and earlier independent review supplied context; the disposition below follows a fresh reconstruction against the completed TeX. A read-only subreview independently checked the actual static upper and hard lower proofs and also found no blockers.

| Claim | Complete manuscript proof | Independent finding |
|---|---|---|
| Class number and convex-piece certificate interpretation | Main section, `bls:class-number`, lines 39–56 | Convex hulls give the semantic certificate, and every convex leaf containing assigned vertices contains their hull. The final text qualifies valid added cuts as convex. Removed vertices require augmented accounting. |
| Planted recovery and comparison with the true integer optimum | `app:bls-ml-proof`, appendix lines 110–178 | Gaussian integration gives the correct factor `(1+rho k/N)^(-M/2)`. The small-support recovery sum vanishes with the fixed logarithmic margin, and the large-support sum is exponentially small. The value-gap proof retains the binomial expression needed for its displayed logarithm. In particular it proves unique planted optimality at every fixed positive `rho=theta N`. |
| Planted versus global root exactness | `app:bls-root-exactness-proof`, appendix lines 180–214 | The planted probability is exactly `2^-N`. Strict convexity makes global value equality equivalent to a vertex root minimizer. The off-support sign probability and on-support Chernoff event are combined by conditioning, not by an unsupported independence claim. Rounding remains a separate event. |
| Finite sign-orbit invariant-event identity | Main `bls:sign-orbit`, lines 149–191 | The explicit nonzero OLS-coordinate and residual-product conditions ensure exactly one sign pattern selects each specified support. The event must be invariant under all column sign changes. The empty support is explicitly defined, and the Gaussian model satisfies every genericity condition almost surely. |
| Exact OLS Student density, selected NNLS coefficients, maximum CDF, and projection mixture | `app:bls-nnls-proofs`, appendix lines 216–299 | The matrix Jacobian and Gram determinant give exponent `(M+1)/2`; the gamma integral supplies the displayed normalized density. One common chi-square denominator governs the coefficient vector. Sign invariance transfers absolute coefficients and projection norms to a selected support. The binomial mixture and atom at zero are correct. No independence across nodes is inferred. |
| Finite maximum-coefficient tail | Main `bls:nnls-tail`, lines 244–282 | Fixed-support regression has `M-s+1` chi-square degrees. The two-sided normal bound has no missing factor two. The coordinate union bound and binomial derivative sum give exactly the stated upper bound, including square full-support regressions. |
| Simultaneous square/tall C1 threshold | Main `bls:c1-threshold`, lines 298–388; probability estimates in `app:bls-probability-lemmas` | At each wrong-fixing node, `w+2b_i` is independent of the free matrix and has variance `1+4theta`. The union over `N` nodes gives exponent `M-N+2` in the inactivity bound. The orthant value is defined before box equality is invoked. Explicit concentration choices give a uniform residual estimate and the correct gap `2theta(2beta-1)-1/2`. Fixed margins yield the stated `epsilon N/4` gaps. |
| Exact random root cutoff and logarithmic scale | Main `bls:root-threshold`, lines 393–477; `app:bls-root-threshold-proof`, appendix lines 301–361 | Scaling gives the pathwise cutoff `(max u°(1))^2/4`, including equality. The exact mixture gives the matching first-order scale `log N/(2beta_N-1)` on both sides. Both the normal maximum lower bound and chi-square concentration are supplied. Positive SNR, square/tall dimensions, and exact aspect-ratio notation are retained. |
| Static variable-order certificate upper bound | `app:bls-static-upper-proof`, appendix lines 363–443 | The exact one-node residual mixture permits a union over all possible nodes in the fixed order. The deterministic positive margin dominates the concentration errors. Counting possible parents gives `1+2 sum_{i=1}^K binom(N,i)`, and the weighted binomial bound and ceiling correction justify the stated leading logarithmic exponent. An optimum certificate uses an optimal incumbent; no planted-recovery assumption or adaptive-order claim enters the proof. |
| Entropy and barycenter certificate lower bound | `app:bls-overlap-entropy` and `app:bls-hard-lower-proof`, appendix lines 445–674 | The KL/entropy loss and elementary binomial mode/Chebyshev estimate are complete. The whole-matrix net bound avoids any selection-conditioning gap. The barycenter identity, optimum-gap allowance, overlap requirement, floor term, and final `log(8N)` correction check algebraically. The revised constants agree throughout the proof. |

The C1 tree conclusion uses the correct dependency: `lattice:path`, exact box node values, and exactness at the remaining binary singleton. Weak C1 needs the optimal incumbent when off-path nodes are checked; strict C1 permits exact best-bound selection without an initial optimal incumbent. The chapter explicitly excludes a tree lower bound inferred solely from C1 failure and gives no claim at the critical parameter or in a shrinking critical window.

The hard-certificate conclusion has the safe audited scope. For divergent `rho=o(N)`, the subtractive logarithm is negligible compared with `(N/rho)log rho`. For each sufficiently large fixed `rho`, the exponent is linear in `N`, with constants allowed to depend on both `beta` and that fixed `rho`. The manuscript does not claim a matching rate throughout an arbitrary linear-SNR interval. The elementary net proof uses

`C_beta=2[sqrt(beta+1)+sqrt(2(log 5+1))]`

and

`c_beta=beta[Phi(-1)-Phi(-2)]/[256 e^2 C_beta^4]`.

The fixed-SNR existence choice for `rho_0` matches these conservative constants. The sharper source constants and its numerical threshold are not attached to the revised proof.

Four minor precision findings raised during this review were repaired and checked in the frozen files:

- The fixed-SNR statement now uses `Theta_{beta,rho}(N)`.
- The sign-orbit lemma defines the empty-support span and residual.
- The lower centered chi-square moment is stated for every nonnegative exponential parameter, with zero degrees treated separately.
- The certificate discussion explicitly restricts added cuts to convex cuts.

The final writer also made the C1 concentration choices and surviving-singleton exactness explicit. None of the review findings remains unresolved.

The exposition is suitable for optimization experts. It introduces the model and counted certificate first, explains the barycenter mechanism before its technical lower bound, and keeps long distribution and concentration arguments in the appendix. Planted recovery, planted root exactness, global vertex exactness, rounding, box/orthant equality, and C1 are consistently distinguished. The classical Gaussian cone mixture and Student regression density are described as classical; the finite tail is presented as the ingredient for the B&B application, without an unsupported novelty claim. Hu–Lu is a scope comparison and is not a proof dependency of simultaneous node claims.

All four chapter citation keys are present in the current bibliography. Their exact bibliographic identities and theorem locators remain the literature lead's responsibility. The only external manuscript theorem dependency used by the chapter is the reviewed one-path lemma; its required search and singleton hypotheses are stated in the BLS application. No proof depends on an internal audit, experiment, source note, or review file. `main.tex` directly inputs both reviewed TeX files.

Actual local verification consisted of scoped `pwd`, `rg --files`, `rg -n`, `cat`, and `nl -ba ... | sed -n ...` source reads; `sha256sum sections/binary-least-squares.tex appendices/bls-proofs.tex`; and one scoped `python -` consistency check over the two reviewed TeX files, `sections/lattice.tex`, `main.tex`, and `references.bib`. That check found 68 BLS labels, no duplicate BLS labels, no missing reviewed references, no missing chapter citation keys, and both inputs reachable. `apply_patch` wrote only this review report. No literature browsing, experiment rerun, numerical or symbolic experiment, project-wide verification, CI status/log inspection, or TeX build was performed. The root's integrated targeted build and final literature accounting are separate integration checks, not results of this review.
