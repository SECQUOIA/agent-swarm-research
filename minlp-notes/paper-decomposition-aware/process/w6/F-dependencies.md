# F-dependencies: moved proofs and appendix dependencies (Appendices A, C-H)

Scope: every proof or result moved to Appendices A, C, D, E, F, G and H in W5
(diff of `process/w5/sections-before-w5/` against `sections/`), checked for
(i) symbols, definitions, equations and lemmas used before definition or
without reference, (ii) completeness of the moved proofs, (iii) an
informative opening sentence per appendix section. Changed steps were
re-derived. Sources were not edited.

## Verdict

No critical or major problem. Every moved proof is complete: a word-level
comparison of the old main-text proofs with the new appendix proofs
(`checks/Fdep-moved.py`) finds only the added "Proof of ..." headers, the
explicit reference to Definition `def:cert`, the name `J=[a,a']`, the
reference to the endpoint rounding now defined in Section 9.2, and the
checker sentence that moved back to the main text after Lemma
`lem:endpointid`. The ordering inside each appendix respects dependencies,
every main-text summary of a moved result matches the appendix statement,
and the build log has no undefined references. Six minor problems remain:
two notation slips, one inconsistency between Section 11 and Appendix H,
two appendix openings that do not describe their content, and a missing
opening sentence.

## Findings

### F-dependencies-1 (minor) Appendix A has no opening sentence
- Location: `sections/appendix-growth.tex:1-3`.
- Problem: the section heading "Proofs for Section 5" is followed directly by
  `\begin{proof}[Proof of Lemma~\ref{lem:graded}]`. The appendix also holds
  the calculus bound for Lemma `lem:states` (moved in W5), a bit-length
  paragraph, the proofs of Lemma `lem:commonmesh`, Proposition `prop:sharp`
  and Corollary `cor:uniformgrid`, and the claims of Examples `ex:family`
  and `ex:chain`. No sentence tells the reader what is there. Every other
  appendix in scope, C to H, opens with such a sentence. Appendix B has the
  same gap, but B is outside this report's scope.
- Fix: insert after line 1:
  "This appendix proves Lemma~\ref{lem:graded}, the bound $K(\theta,n_P)$ in
  Lemma~\ref{lem:states}, the bit-length claims in the proof of
  Theorem~\ref{thm:approx}, Lemma~\ref{lem:commonmesh},
  Proposition~\ref{prop:sharp}, Corollary~\ref{cor:uniformgrid}, and the
  claims of Examples~\ref{ex:family} and~\ref{ex:chain}."

### F-dependencies-2 (minor) Name clash $R_0$ in the proof of Corollary `cor:uniformgrid`
- Location: `sections/appendix-growth.tex:224-239`.
- Problem: W5 renamed the radius parameter of Proposition `prop:sharp` from
  $\rho$ to $R_0$, and the induction radii of this proof from $\rho_j$ to
  $R_j=\min\{1,2(k_0+1)h_j\}$. As a result, $R_0$ now means two things in
  one paragraph: the parameter of the proposition, and the $j=0$ term of the
  sequence, which equals 1. The phrase "Proposition~\ref{prop:sharp} with
  $h=h_j$ and $R_0=R_j$" (line 231) therefore reads as the equation
  $1=R_j$, which is false for large $j$. The parallel proof of Lemma
  `lem:tu-uniform` (`appendix-tu.tex:399`), which says "Induction, as in the
  proof of Corollary~\ref{cor:uniformgrid}", still calls the same sequence
  $\rho_j=\min\{1,2(k_0+1)h_j\}$.
- Fix: in lines 224-239, replace $R_j$, $R_1$ and $R_{j+1}$ by $\rho_j$,
  $\rho_1$ and $\rho_{j+1}$. For example, line 224 becomes "Put
  $\rho_j=\min\{1,2(k_0+1)h_j\}$; we show by induction that
  $X^{(j)}\supseteq[-\rho_j,\rho_j]^n$." Line 231 becomes
  "Proposition~\ref{prop:sharp} with $h=h_j$ and $R_0=\rho_j$ retains every
  interval with an endpoint $kh_j$, where $|k|\le k_0$ and
  $|k|h_j\le\rho_j$." Line 228, "with $h=1$ and $R_0=1$", and the graded
  rule, "$R_0=R$", stay as they are.

### F-dependencies-3 (minor) Appendix H assigns $\kappa_{\mathrm{target}}=2$ runs to E3
- Location: `sections/appendix-computation.tex:80-83`.
- Problem: Appendix H says "On the separable instances of E3
  ($\kappa_{\mathrm{target}}=2$), ...". After the W5 merge, Section 11.2
  defines E3 with $\kappa_{\mathrm{target}}=4$ only (`computation.tex:145-147`)
  and mentions separable instances only for E2 (`computation.tex:143-145`).
  The pre-W5 text reported these runs as a side remark on E3. The cross-
  reference "Section~\ref{sec:comp-growth} reports the coupled case" therefore
  points to a section that never mentions a separable E3 case.
- Fix: replace lines 80-83 with:
  "E3 was also run with $\kappa_{\mathrm{target}}=2$, for which the generator
  makes the free coordinates separable (Section~\ref{sec:comp-growth}); on
  these instances filtered uniform grids used exactly
  $4(\lfloor\sqrt{n/4}\rfloor+1)+1$ nodes. Section~\ref{sec:comp-growth}
  reports only $\kappa_{\mathrm{target}}=4$ because the separable case does
  not test coupling."

### F-dependencies-4 (minor) Appendix H uses $J$ for the stage limit of CT
- Location: `sections/appendix-computation.tex:14-16`.
- Problem: item (b) defines the implementation's stage limit as "the least
  $J$ with $\frac78Lns^24^{-J}\le\varepsilon$ instead of
  $\frac9{16}Lns^24^{-J}\le\varepsilon$". Table `tab:notation`, CONVENTIONS
  section 7 and Lemma `lem:commonmesh` (`growth.tex:318`) call the stage limit
  of TRIAL and CT $j_{\max}$. They reserve $J$ for grid intervals and for the
  last level of CORE, TU-GRID and UC. The item compares directly with the
  lemma's definition, so the two names hide the fact that the same quantity
  is meant.
- Fix: "the stage limit is the least $j_{\max}$ with
  $\frac78Lns^24^{-j_{\max}}\le\varepsilon$ instead of
  $\frac9{16}Lns^24^{-j_{\max}}\le\varepsilon$, so a trial may run one stage
  longer."

### F-dependencies-5 (minor) The opening of Appendix D gives notation, not content, and does not cover D.3
- Location: `sections/appendix-recourse-cuts.tex:3-7`.
- Problem: the only opening sentence is "This appendix uses the notation of
  Section~\ref{sec:cuts}: ... a core of $k$ continuous coordinates with domain
  $[0,1]^k$ ...". It does not say what the appendix proves. Its last
  subsection, D.3 "Proofs for Section 7.5" (Lemma `lem:chaincut`, work
  bounds of Theorem `thm:balanced`), uses the notation of Section 7.5
  (grids $G_i$, signs $o_i$, $\chi_i$, $F_\chi$, no core), not the notation
  announced in the opening.
- Fix: replace lines 3-7 with:
  "This appendix proves the exact-output theorem for a cut residual
  (Theorem~\ref{thm:cr-exact}), the claims of Remark~\ref{rem:cr-mixed} on
  concave--convex residuals, and the results deferred from
  Section~\ref{sec:balanced}. The first two subsections use the notation of
  Section~\ref{sec:cuts}: $F(x)=\frac12x^{\T}Hx+b^{\T}x+c$ is a rational
  quadratic, $\mathcal K$ is a core of $k$ continuous coordinates with domain
  $[0,1]^k$, $\mathcal R$ is the residual, and $\alpha_i$, $\delta_i$ and
  $y(z)$ are as defined before Proposition~\ref{prop:cr-cut}; the last uses
  that of Section~\ref{sec:balanced}."

### F-dependencies-6 (minor) The coNP-hardness claim cited from Section 9.3 is hard to locate in Appendix F
- Location: `sections/appendix-proximal.tex:3-6` and `:432`;
  `sections/optsets.tex:469-470`.
- Problem: W5 replaced a main-text argument with the sentence "Deciding
  whether a given minimizer of an instance of $\mathfrak D$ with bag size
  three is the only one is coNP-hard (Appendix~\ref{app:proximal})". The
  argument now sits in an unlabeled closing paragraph after the proof of
  Proposition `prop:sshard`. The opening sentence of Appendix F lists the
  proofs for Section 9, Lemma `lem:proximal` and Proposition `prop:sshard`,
  but not this claim and not Example `ex:diagtilt`, which W5 also moved
  here. The argument itself is correct. With $a_0=0$ the origin is a
  minimizer, so the instance lies in $\mathfrak D$; adding the item $-T$ to
  positive items with target $T$ gives a zero-sum instance, so uniqueness is
  coNP-hard.
- Fix: replace lines 3-6 with:
  "This appendix contains the proofs for Section~\ref{sec:optsets},
  Example~\ref{ex:diagtilt} of tilted and disconnected optimal sets in
  $\mathfrak D$, the lemma on proximal stages used by DISC
  (Algorithm~\ref{alg:disc}), Proposition~\ref{prop:sshard} on the hardness
  of discovery within $\mathfrak D$, and, in its last paragraph, the proof
  that deciding uniqueness of a given minimizer in $\mathfrak D$ is
  coNP-hard."
  Insert `\paragraph{Uniqueness in $\mathfrak D$ is coNP-hard.}` before line
  432, and in `optsets.tex:470` write "(last paragraph of
  Appendix~\ref{app:proximal})".

## Checked and found correct (no change needed)

- **Appendix A.**
  - The calculus bound for $K(\theta,n_P)$ re-derived: $\varphi(1)=16.21$,
    $\varphi(2)=18.55$, $\varphi'\le4/m$, and the slope of
    $10\log_2(m+2)$ is at least $7.2/m$ for $m\ge2$. A brute-force check of
    $\varphi(m)\le10\lceil\log_2(m+2)\rceil$ for $m<2\cdot10^5$ passes.
  - The (G5) constant $\psi$ checks the same way.
  - The node formula $h_{ij}((1+\theta)^k-1)/\theta
    =2^{E-j-\varpi_i}((2^\mu+1)^k-2^{\mu k})/2^{\mu(k-1)}$ is correct.
  - The renames $\varpi_i$, $j_{\max}$, $k_0$ and $\omega_b$ are consistent
    with the main text.
- **Appendix C.**
  - Proposition `prop:star` (A) and (B) re-derived: $V(x)$; the corner
    values $(1-h)(mh^2/4-h-\epsilon)$ and the excess $h^3$; the eigenvalues
    $3\pm\sqrt5$; $V^G(t)=2t^2-dh|t|+d^2h^2/4$; the stated difference.
  - Example `ex:cr-star32` values verified: $23/32$, $27/32$, $31/16$,
    $1/8$, $33/16$ and $m/16$.
  - Proposition `prop:cr-osc` re-derived.
  - The multilevel paragraph and the "clipped piece" discussion are
    complete relative to the pre-W5 text.
  - Theorem `thm:cv-recog` has all its notation ($Y$, $\Pi$, $w_0$, $\phi$)
    defined locally.
- **Appendix D.**
  - The rewritten step (a) of Proposition `prop:cr-greedy` re-derived:
    submodularity with $A=S_{<i}\cup\{i\}$ and $B=S^\pi_{l-1}$ gives
    $A\cap B=S_{<i}$ and $A\cup B=S^\pi_l$, and the sum telescopes.
  - The deletion of the "same holds after subbox/fixing" sentence breaks no
    dependency: no file uses it.
- **Appendix E** (`checks/Fdep-tu.py`, exact arithmetic).
  - The graded grids around $3/10$ and $7/10$ have eleven nodes each, only
    $0$ and $1$ in common, largest interval $3831/20480$ and
    $\delta=27/1280$.
  - The misaligned example gives $13/288$, $25/288$ and $\lambda$-threshold
    $75/288\,L$.
  - In Example `ex:tu-sum`, the seven feasible points have the stated
    values, and the allowance $75/128\,L$ against $\min F=L$ checks.
  - Example `ex:tu-union` re-derived: $g_S=1/6$, $\bar L=12$ and
    $2(5+\lfloor2\sqrt{216n_b}\rfloor)$.
  - Remark `rem:tu-curv` (i) checks: Gershgorin with absolute row sums.
  - TU-EXACT's notation ($\hat A_{\mathcal J}$) is now defined in the E.3
    preamble.
  - Lemma `lem:tu-snap` and the proof of Theorem `thm:tu-exact`(c)
    re-derived.
- **Appendix F.**
  - Proposition `prop:twocenters` re-derived:
    $0.23^2/20=0.002645>1/379$, $\sqrt{20}+\sqrt{379}<24$, and
    $M\le h_{x0}<2M$ from $\varpi_x=1$.
  - Lemma `lem:proximal` re-derived: the bracket equals $99/64$, and
    $3/4+8\ln(n+2)\le7\lceil\log_2(n+2)\rceil$.
  - Example `ex:diagtilt` re-derived: $H=2aa^{\T}-\diag(0,0,\frac14)$, and
    $w=(0,1,2)$ gives $-1$.
  - The constants of Remark `rem:falseguess` check: $R=2^{23}$,
    $\tau=2^{-26}$, $J_{\hat\kappa}=28,28,29$.
  - The proof of Proposition `prop:sshard` (ii) and the coNP argument are
    complete.
- **Appendix G.**
  - All four moved proofs are word-identical to the pre-W5 text, apart from
    the added references.
  - The new last paragraph of the proof of Proposition `prop:lbproduct`
    re-derived: $(1+\log_2\kappa)^2\le4\kappa$, $(I+2)^5\le3^5I^5$, and
    $\psi'$ is computable, nondecreasing and unbounded.
- **Appendix H.**
  - The SCIP numbers are consistent with Section 11.5: $9\cdot10^{-7}$
    epigraph part plus a 51-94% bound part gives a shortfall of
    $1.8\cdot10^{-6}$ to $1.5\cdot10^{-5}$; the run counts are
    $27=9+9+9$ and $39=9+9+21$.
  - The E6 numbers are consistent: 11 growth instances with smallest lower
    end 4.5, and nodes 8 to 18.
  - The recourse table matches Section 11.7.
  - The gap ratio $0.16/(9/16)=0.28$ matches Section 11.2.

## Commands run (targeted, local)

- `diff process/w5/sections-before-w5/<file> sections/<file>` for every
  appendix file and for `growth.tex`, `recourse-local.tex`,
  `recourse-convex.tex`, `recourse-cuts.tex`, `constraints.tex`,
  `optsets.tex`, `limits.tex`.
- `python3 process/w6/checks/Fdep-tu.py`: exact check of the TU-appendix
  examples (all values as stated).
- `python3 process/w6/checks/Fdep-constants.py`: numeric constants of the
  moved proofs. My first $J_{\hat\kappa}$ line used a wrong $4s^2$ factor;
  recomputed by hand, it confirms 28, 28, 29.
- `python3 process/w6/checks/Fdep-moved.py`: word-level comparison of the
  moved proofs.
- `grep` of `/tmp/dpaper/out/main.log` (no undefined references) and of
  `main.aux` (appendix numbering).

No project-wide build or CI check was run.
