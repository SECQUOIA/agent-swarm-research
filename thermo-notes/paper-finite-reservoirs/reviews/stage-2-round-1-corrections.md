# Stage 2, round 1 — corrections

All accepted issues in the coordinator's adjudication have been addressed in `sections/microscopic.tex`. I read all five review reports and checked the relevant original primary-source text. The microscopic threshold theorem statements and their scope are unchanged. This report prepares the corrected stage for the required second round of five independent reviews; it does not close that review gate.

## 1. Major source-convention issue: use the original BCT objects throughout

The short-range input subsection now explicitly fixes every contour, interior/exterior, compatibility relation, phase event, restricted partition function, and activity to Borgs–Chayes–Tetali (BCT2012), Definitions 4.1–4.4 and 5.4, equations (6.1)–(6.5) and (6.13)–(6.22). It states the original exterior rule: use the component containing a compatible interface when one exists; otherwise use the larger component and the fixed tie rule. The exact positive partition decomposition and ordered factor `q` are cited directly to BCT (6.1)–(6.5), and the tunneling bound to its Lemma 6.1.

The inaccurate assertion that BCHPT2022 records identical finite-volume events has been removed. The paper now explicitly notes the modified exterior convention in BCHPT Definition 5 and does not import estimates between those conventions. The cluster convergence margin is grounded solely in BCT (A.5)–(A.6), eliminating the unnecessary “or equivalently” source transfer. The exact cap from BCT (A.3), `tau(beta) = beta/8 - beta/20 + 1`, is now supplied rather than left implicit.

### Stable-side identification in the same convention

The manuscript now gives the original-source reasoning instead of invoking BCHPT's differently defined metastable branches:

- BCT Lemma A.3 identifies positive spontaneous magnetization with `a_o = 0`. The physical definition of the transition thus gives `a_d = 0` below coexistence and `a_o = 0` above; continuity gives equality at coexistence.
- BCT Lemma A.1(ii) bounds each full-torus restricted partition function above by `exp[-N min_i f_i^tr + O(N exp(-bL))]`. The maximum in its estimate is at most one because all additional exponents are nonpositive. Equation (A.9) gives the matching lower bound for any minimizing phase.
- The original interface-network sum (6.26)–(6.27) bounds the tunneling contribution by `exp[-N min_i f_i^tr - b L^(d-1)]`. Its derivation needs Appendix A's bounds and large-`q` counting, not ordered-phase minimization. The paper explicitly permits shrinking the fixed neighborhood so `q <= exp(2d kappa + d)` there, retaining the inequality used by that derivation on both sides of coexistence.
- The exact positive decomposition therefore identifies `min_i f_i^tr` with the physical thermodynamic random-cluster free energy. The exact random-cluster/spin normalization and BKMS's stable physical branch then give `f_i^tr = psi_i + d beta` on the relevant stable side.

These steps avoid any identification of distinct finite-volume contour conventions or of their unstable metastable extensions.

## 2. General matching-label derivative estimate

The restricted-derivative proof now starts directly from BCT (6.13)–(6.14), with an explicit displayed summand logarithm:

`F_Gamma = -e_o n_o - e_d n_d - kappa M_Gamma + c_Gamma log q`.

The paper defines the two vertex counts, their sum as the interior vertex count, the total internal contour-intersection count, and the temperature-independent component/color exponent, including removal of the ordered multiplicity. It explains why the admissible families and these geometric quantities are temperature independent.

The local count is now explicit. BCT's boundaries lie in the fixed half-lattice construction; compatible contours are separated by at least one half. Each lattice edge can therefore support only a bounded number of intersections. Edges meeting an interior are bounded by its vertex count plus its outer contour-intersection count. Thus total internal contour size is at most `C_d (interior vertices + outer size)`, including for torus interiors.

The displayed positive-sum identities yield first logarithmic derivative `O(V_gamma)` and second logarithmic derivative `O(V_gamma + V_gamma^2)`. The original BCT geometric estimate gives `V_gamma = O(m_gamma^2)`, and the activity ratios consequently give the existing `O(m_gamma^2)` logarithmic first derivative and `O(m_gamma^4 K_gamma)` second activity derivative. No stability assumption has been added to this step.

The unrestricted ordinary-random-cluster interpretation and citation to BCHPT Section 3.8 have been removed from this proof. Its embedding and simple-connectivity restrictions are no longer being used implicitly.

## 3. Log-partition derivatives

In the bond-to-spin transfer proof, the sentence now expressly identifies
`F_{i,L}(beta) = log[exp(d beta N) Z_{i,L}(beta)]` and states that its derivatives with respect to bond fugacity are the conditional bond mean and variance. It no longer attributes these quantities to derivatives of the partition function itself. The subsequent, already correct chain-rule and moment calculations are unchanged.

## 4. Geometric explanation of the phase events

Before introducing their positive partition functions, the manuscript now explains the thickened occupied-bond geometry, the ordered/disordered regional labels, zero-winding contours versus nonzero-winding interfaces, the common-exterior label when no interfaces are present, and the tunneling event when interfaces are present. This explains the conditioning used later without requiring the reader to reconstruct all source topology.

## Validation and scope

Checked BCT's original Definitions 4.1–4.4 and 5.4, equation (4.5), equations (6.1)–(6.5), (6.13)–(6.27), Appendix A's opening assumptions, (A.3)–(A.9), Lemma A.1, and Lemma A.3 against the retained primary-source text. The corrections concern the exact scientific dependencies and an explicit elementary derivative derivation; finite numerical tests would not validate their uniform estimates.

Ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` from `paper-finite-reservoirs`. The final build succeeds and produces a 20-page PDF. The final log has no warnings or overfull/underfull box diagnostics. No workflow, other review report, later-stage content, bibliography entry, or theorem statement was modified.
