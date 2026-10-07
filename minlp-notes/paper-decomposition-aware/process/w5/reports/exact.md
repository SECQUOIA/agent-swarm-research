# W5 report: group exact

Files: `sections/exact.tex`, `sections/exact-localized.tex`,
`sections/appendix-localized.tex`, `sections/appendix-boundary.tex`.
No labels were moved, renamed or deleted.

## Adjudication of assigned findings

| id | verdict | reason | change |
|---|---|---|---|
| M-exact-1 | ACCEPTED (wording extended) | REC and the acceptance comparison read $\hat x$ and $\beta$, whose bit lengths are $O((1+\mu2^\mu)(I+q+1))$ by App. A, not $\poly(I+q^*)$. The reviewer named only $\hat x$; $\beta$ (a table entry) has the same bound. The theorem's bound is unchanged. | Proof of `thm:exact`, "Bound under growth": the cost is now a polynomial in $I$ and in the bit lengths of $\hat x$ and $\beta$; these are $O((1+\mu2^\mu)(I+2q^*+1))$, where $\mu$ is the last trial of CT, with $2^\mu\le6\sqrt{\bar\kappa}\le6\sqrt\kappa$ (Thm `thm:approx`(b)); all factors that depend only on $\kappa$ are absorbed into $f_1$. |
| M-exact-2 | ACCEPTED (different letter) | $s,s_i$ are reserved for widths. I used $x^\circ$ rather than $\bar x$ because C-consistency-3 and C-writing-10 propose $x^\circ$, and `appendix-tu.tex` already uses $x^\circ$ for the same role. The optional rename $A_*\to T_*$ would clash with the reserved tree $T$, so I used $M_*$. | Def `def:statpoly`, Lemma `lem:statpoly` and its proof, the proof of Cor `cor:height`(a), Rem `rem:heights` and the proof of Lemma `lem:snap` now use $x^\circ$, $\mathcal P(x^\circ)$, $J_0(x^\circ)$; the auxiliary $s'$ in the proof of `lem:snap` is now the vertex $v$ itself. Proof of Thm `thm:boundary`(b): $A_*\to M_*$. |
| C-consistency-3 | ACCEPTED (my files) | Same clash as M-exact-2; $e_i$ also had three meanings in Section 6. | Minimizer $\to x^\circ$ (above). In the proof of `lem:snap`, the fixed endpoint $e_i\to\xi_i$. In the proof of `cor:poly`, the exponent is no longer named: "the exponents that define the meshes $h_{ij}$ (Section 5)". This stays correct whatever core does with $e_i$ (R-referee-4 proposes $\varpi_i$). $e_i$ now means only the unit vector in Section 6 (`lem:intcurv`). Also in App. B.2: $e_k\to\xi_i$ in the proof of `thm:boundary`(b), and $e=x-a\to z=x-a$ in the proof of `prop:margin`. |
| C-consistency-5 | ACCEPTED (my part only) | The phase index $q$ in App. B.2 clashed with the accuracy $2^{-q}$. I did not use $\phi$: it already names the linear function in `lem:snap`, the block objectives $\phi_t$, and the function in `lem:states`. | Procedure paragraph and proof of `thm:boundary`(b): phase $q\to k$, $q_*\to k_*$. The coordinate index in the same proof, formerly $k$, is now $i$. The other symbols ($\eta$, $P$, $\nu$, ETH) are not in my files. |
| C-consistency-6 | ACCEPTED (my part only) | $C_2$ was used at exact.tex:496 before its definition in App. B.2. | Last paragraph of Section 6.6: $C_2$ and $\lambda_A$ are defined in place (shared with C-writing-12). The $\Gamma_F$ part concerns growth.tex (core). |
| C-writing-6 | MODIFIED | Valid: Section 11 repeats the S1 numbers. The proposed "long before the certified gap reaches the threshold" is false on 2 of the 29 instances. On random_band2_n4_s7005 the face candidate is accepted at stage 0 and a single CT run reaches the threshold at stage 2; on random_path_n8_s7013 these are stages 0 and 1 (check script below). | exact-localized.tex: the S1 paragraph is one sentence. The face candidate was accepted within nine stages on 29 of 30 random mixed-integer instances, whereas one CT run needed up to 72 stages to reach the threshold of `prop:accept` with the constants of (6.1). The Neumaier sentence is kept. The 6.5 opener also shortens the duplicated E4 range to "as small as about $2^{-315}$". |
| C-writing-10 | ACCEPTED (my part only) | | Minimizer $s\to x^\circ$ (above). The proof of `cor:poly` no longer uses the stage limit $J$: it now says "$\alpha$ as in Appendix A but with $O(dI)$ in place of $O(I)$". Core's rename $J\to j_{\max}$ therefore needs nothing in my files. $f(p,\kappa)$ is defined in growth.tex (core); Section 6 only evaluates $f$ at $\kappa$, which stays correct. |
| C-writing-11 | ACCEPTED | The bracket notation conflicted with the Iverson bracket of Lemma 5.5. | Cor `cor:local`: $h^*=\omega^*/\sqrt{n\kappa}$, where $\omega^*$ is the smallest of $\frac12$ (if $I_Z\cap P\ne\emptyset$), $\delta_X/6$ (if $I_C\cup(I_Z\setminus P)\ne\emptyset$) and $\lambda_A/(5\Gamma)$ (if $A\ne\emptyset$). At least one of the first two conditions holds, because the two sets cover $[n]$. The App. B.1 proof now states $\omega_j\le\omega^*$. |
| C-writing-12 | ACCEPTED (reworded) | | exact.tex, last paragraph: "Besides $p$, $\kappa$ and $I$, the cost bound depends polynomially on $\log_2\max\{2,C_2/\lambda_A\}$, where $C_2$ bounds the absolute row sums of the second derivatives in the continuous coordinates on $\bar X$ and $\lambda_A$ is the smallest inward derivative at the active bounds (Theorem B.4)". This matches $f'_d(p,\kappa)\poly(I+B_\lambda)$. |
| C-writing-17 | MODIFIED | Valid. I avoided `\ref` in a section title, which would go into the PDF bookmarks. | App. B title: "Exact output: localized acceptance and polynomial boundary optima" (label `app:exact` kept). |
| C-writing-19 | ACCEPTED (my files) | | "optimizer" $\to$ "minimizer": exact.tex (2 occurrences in the intro) and all occurrences in appendix-boundary.tex. "optimal set/value" and "globally optimal" are kept. |
| C-literature-7 | NO CHANGE (not my file) | The fix belongs in related.tex (front). | None. If front adds the sentence, `lem:snap` keeps its label. |
| R-referee-4 | ACCEPTED (my part only) | | REC free set $J\to J_f$, as the referee asked. For consistency the same applies to the face-candidate free set (Def `def:facecand` and the text after `cor:local`, App. B.1) and to the free set of Lemma `lem:patch` and Thm `thm:boundary` (App. B.2). $J_f$ matches the pattern notation $(J_\ell,J_f,J_u)$ of appendix-recourse-convex.tex:221. The exponent $e_i$ is no longer named in Section 6 (see C-consistency-3). The height constant $R$ keeps its reserved meaning. |

## Cut-plan items

CUTPLAN assigns the exact group only its minor findings; it sets no page target.
Measured on isolated builds of the pre-W5 snapshot with only my four files swapped in
(`/tmp/w5-exact-iso-{before,after}`, fractional page positions taken from
pdftotext):

* Section 6: 7.81 pages before, 7.81 after. Removing the S1 paragraph and the E4 range saves about 5 lines. The added text uses about the same space: the M-exact-1 cost sentence, the definition of $C_2$, and the $h^*$ definition.
* Appendix B: 5.18 pages before, 5.17 after.

## Page span (build of the current repository state, `/tmp/w5-exact/main.aux`)

* Section 6 (`sec:exact`, including 6.5 `sec:localized` and 6.6 `sec:polynomial`): p. 23 to p. 31 (Section 7 starts on p. 31). Unchanged from the build before my edits.
* Appendix B (`app:exact`: B.1 `app:localized` p. 90, B.2 `app:boundary` p. 91): pp. 90-95 (Appendix C starts on p. 95). Before my edits it was pp. 93-98; the shift comes from other groups' concurrent changes to earlier appendices.

## Requests for other files

* computation: `exact-localized.tex` cites `sec:comp-exact` and `sec:comp-localized` (both exist in the merged Section 11.5) and quotes: the face candidate is accepted within nine stages on 29 of 30 instances; one CT run needs up to 72 stages to reach the threshold with the constants of (6.1); and the E4 thresholds are as small as about $2^{-315}$. If these numbers change, please tell the exact group.
* coreA/coreB: no change is needed for renaming $e_i$ or the stage limit $J$; exact.tex no longer names either. Optional: Table `tab:notation` may list $J_f$ (free coordinates of REC and of the face candidate) and $x^\circ$ (a minimizer, Section 6).
* recB: appendix-recourse-cuts.tex:73 already writes the minimizer as $v^\circ$, which is consistent with $x^\circ$.
* front: no change needed; `lem:snap` keeps its label (C-literature-7).

## Checks run (local, targeted; not CI)

* `latexmk -pdf -interaction=nonstopmode main.tex` in `/tmp/w5-exact` (copy of the current repository): exit 0. My files produce no errors, undefined references or overfull boxes. The remaining overfull box (appendix-tu.tex) and the undefined citation `AbelloEtAl2001` (p. 61) come from other groups' files. An earlier build of the repository copy failed on in-progress edits in appendix-growth.tex (`\leR_j`, `\lek_0`), which are not my files; the final build is clean.
* Isolated builds `/tmp/w5-exact-iso-before` and `/tmp/w5-exact-iso-after` (pre-W5 snapshot, plus my four files in the after build): both 0 errors, 0 undefined references, 0 overfull boxes.
* `python3 process/w5/checks/exact-s1-stages.py`: PASS. It reads `experiments/results/S1_localized.csv` and confirms 29 of 30 accepted, a largest face-candidate stage index of 8, and a single-run threshold of at most 72 stages. It also lists the two instances on which acceptance is not much earlier than the threshold.
* By hand: the App. A bit-length bounds behind M-exact-1. Node denominators divide $\Gamma_X2^\alpha$, and table entries, including $\beta$, are $b=O((1+\mu2^\mu)(I+q+1))$-bit integers over $8\Gamma_F\Gamma_X^24^\alpha$. CT runs trials in increasing $\mu$ and keeps its incumbent, so all values come from trials $\mu\le$ the successful one. Setting.tex states that $\bar\kappa\le\kappa$ under point growth.
* Re-derived the renamed `lem:snap` proof. It shows $\frac32\abs{J'}\tau\le3/(8R)$, that $v$ agrees with the values REC fixes, and that $\nabla_{J_f}F(v)=0$ because $J_f\subseteq J_0$. Also re-derived the `prop:margin` estimate $\norm\rho\ge\frac34\norm z$ and the phase accounting with $k$: $\sum_{\mu=2}^k2^{k-\mu}<2^{k-1}$ and $k_*=\mu_*+\lceil\log_2M_*\rceil$.

## Unresolved

None in my files.

## Verification (W5 verifier for group exact)

I diffed the four files against `process/w5/sections-before-w5/`, checked each assigned finding in `process/w5/assign/exact.json` (none has a `verifier` field, so the reviewer fixes were the reference), re-derived every changed statement and proof, and rebuilt the paper.

### Findings

All 13 adjudications stand.

| id | verdict on the revision | notes |
|---|---|---|
| M-exact-1 | correct, made more precise | App. A gives node denominators dividing $\Gamma_X2^\alpha$ and table entries (including $\beta$) of $b\le c(1+\mu2^\mu)(I+q+1)$ bits. EX calls CT only with $q<2q^*$, and Thm `thm:approx`(b) gives $2^\mu\le6\sqrt{\bar\kappa}$ with $\bar\kappa\le\kappa$ (setting.tex). The final bound $f_1(p,\kappa)(I+1)^{C_1}$ is unchanged. CT keeps its incumbent across trials, so $\hat x$ may come from an earlier trial. "$\mu$ is the last trial of CT" is now "CT succeeds at trial $\mu$ (an incumbent kept from an earlier trial satisfies the smaller bound of that trial)". |
| M-exact-2, C-consistency-3, C-writing-10 (my part) | correct | No minimizer $s$, $s_i$ is left in Section 6. $x^\circ$ appears consistently in Def `def:statpoly`, Lemma `lem:statpoly`, Cor `cor:height`, Rem `rem:heights` and Lemma `lem:snap`. The re-derived proof of `lem:snap` holds with $v$ in place of $s'$: $\frac32\abs{J'}\tau\le\frac3{8R}<\frac1R$, $1/R=4n\tau>2\tau$, $v$ satisfies the fixed values of REC, $\nabla_{J_f}F(v)=0$, and $F(\tilde x)=F(v)$. $e_i$ now means only the unit vector (`lem:intcurv`, as in setting.tex:50). The name-free wording in the proof of `cor:poly` matches growth.tex, which now writes $\alpha=j_{\max}+O(I)+\mu K_\mu$ and names the exponents $\varpi_i$, $E$. $M_*$ is a sound choice ($T$ is the reserved tree). |
| C-consistency-5 (my part) | correct | Phase index $k$, $k_*$. Rechecked: $\sum_{\mu=2}^k2^{k-\mu}=2^{k-1}-1$; trial $\mu_*$ completes in phase $k_*=\mu_*+\lceil\log_2M_*\rceil$; the total is at most $2^{k_*}\le2\cdot2^{\mu_*}M_*$. Inside the proof, $k$ has no other meaning. |
| C-consistency-6, C-writing-12 | correct | $C_2$ and $\lambda_A$ are defined at the end of 6.6. "Depends polynomially on $\log_2\max\{2,C_2/\lambda_A\}$" matches $f'_d(p,\kappa)\poly(I+B_\lambda)$ in Thm `thm:boundary`(b). |
| C-writing-6 | correct (MODIFIED) | Checked against `experiments/results/S1_localized.csv`: 29 of 30 accepted, largest face-candidate stage index 8, largest single-run threshold 72 stages over all 30 instances. Per instance, acceptance is never later than the threshold. The rejection of "long before" is justified: on `random_band2_n4_s7005` and `random_path_n8_s7013` the threshold comes 1-2 stages after acceptance. The $2^{-315}$ in the 6.5 opener matches Section 11 ("21 to 315 bits"). |
| C-writing-11 | correct, one prose fix | The definition of $h^*$ is correct, and the cover argument holds because $(I_Z\cap P)\cup I_C\cup(I_Z\setminus P)=[n]$. The App. B.1 proof uses $\omega_j\le\omega^*$ correctly. The edit had dropped the "and put" of the old sentence, leaving a comma splice ("Put $\lambda_A$ \dots and $\Gamma$ \dots, let $\delta_X$ \dots"). This now reads "\dots, and let $\delta_X$ \dots". |
| C-writing-17 | correct (MODIFIED) | The title covers B.1 and B.2. Keeping `\ref` out of the section title is reasonable. |
| C-writing-19 | correct | No "optimizer" remains in the four files. |
| C-literature-7 | correct (no change) | The fix belongs in related.tex (front). |
| R-referee-4 (my part) | correct | REC, `thm:exact`, `def:facecand`, the text after `cor:local`, App. B.1, `lem:patch`, `thm:boundary` and `prop:margin` use $J_f$ consistently. No other file refers to the old free set $J$. |

### Cut plan, labels, references

* CUTPLAN gives group exact only its minor findings; no moves or cuts were required, and none were made.
* The label lists of all four files equal those of the snapshot, and `sections/*.tex` has no duplicate labels.
* Cross-file uses of `lem:snap`, `alg:rec`, `lem:statpoly`, `def:facecand` and `cor:local` (computation, appendix-proximal, appendix-recourse-*, optsets, constraints, recourse-*) still match the statements.

### Verifier edits (all in my group's files)

* `sections/exact-localized.tex` (Cor `cor:local`): fixed the comma splice ("and let $\delta_X$").
* `sections/exact.tex` (proof of `thm:exact`): $\mu$ is now "the trial at which CT succeeds", with the note on incumbents from earlier trials.
* `sections/exact.tex` (end of 6.6, proof of `lem:snap`) and `sections/appendix-boundary.tex` (proof of `thm:boundary`(b)): reflowed source lines; no change in content.

### Checks run (local, targeted; not CI)

* `python3 process/w5/checks/exact-verify-renames.py`: PASS. It checks that the labels equal the snapshot and that none of the old notation is left (minimizer $s$, $H_{JJ}$, $\nabla_J$, $e_k$, $A_*$, $q_*$, "optimizer", the bracket form of $h^*$). It also checks in exact arithmetic the `lem:snap` constants, the phase accounting with $k$, and the cover claim for $h^*$.
* `python3 process/w5/checks/exact-s1-stages.py`: PASS.
* Build of the current repository in `/tmp/w5-exact-verify` (`latexmk -pdf -interaction=nonstopmode main.tex`): exit 0, 0 errors, 0 overfull boxes, 0 undefined references. The only warning is the undefined citation `AbelloEtAl2001` (p. 60), which comes from `sections/limits.tex` (not this group's file; the key is missing from references.bib).
* Page spans from `/tmp/w5-exact-verify/main.aux`: Section 6 pp. 22-30 (6.5 p. 27, 6.6 p. 29; Section 7 starts on p. 30). Appendix B pp. 87-92 (B.1 p. 87, B.2 p. 88; Appendix C starts on p. 92). The shift from the revision agent's build (pp. 23-31, pp. 90-95) comes from other groups' cuts.

### Unresolved

None in this group's files. Outside them: `AbelloEtAl2001` is cited in limits.tex and is missing from references.bib (limits/coordinator).
