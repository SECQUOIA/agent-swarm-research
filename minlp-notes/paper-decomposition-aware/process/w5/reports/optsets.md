# W5 report: optsets (Section 9 and Appendix F)

Files edited: `sections/optsets.tex`, `sections/appendix-proximal.tex`.
New check scripts: `process/w3/checks/optsets-w5-pages.py` (page spans) and
`process/w3/checks/optsets-w5-diagtilt.py` (exact check of the moved example).

## Page spans (measured from builds)

Fractional spans come from `pdftotext -layout` positions (script above).

| Part | Before W5 (snapshot build) | After (private build) | Change |
|---|---|---|---|
| Section 9 | pp. 53-62, 8.44 pp | pp. 52-58, 6.20 pp | -2.24 pp |
| 9.1 | 2.95 pp | 2.24 pp | -0.71 |
| 9.2 | 2.59 pp | 1.91 pp | -0.68 |
| 9.3 | 2.61 pp | 1.81 pp | -0.80 |
| Appendix F | pp. 116-119, 2.31 pp | pp. 113-118, 5.23 pp | +2.92 |

The absolute page numbers after the change also reflect other groups'
concurrent edits; the spans measure only Section 9 and Appendix F. The
after-build was in `/tmp/w5-optsets`, and `main.aux` there gives
`sec:optsets` p. 52, `sec:limits` p. 58, `app:proximal` p. 113 and
`app:limits` p. 118.

## CUTPLAN items done

1. **Proofs moved to Appendix F.** These proofs now live in Appendix F, each
   opening with `\begin{proof}[Proof of ...]`:
   * the proof of `prop:twocenters`, in F.1;
   * the proofs of `lem:endpointid` and `cor:facecsp`, in F.2.

   The main text keeps every statement and adds "The proof is in
   Appendix~\ref{app:proximal}". After `lem:endpointid` it also keeps one
   sentence from the moved "Checking" paragraph, because Theorem
   `thm:endpointset` claims that the description is checkable: "a checker
   needs the tables $M_t$ and that assignment, not the minimization that
   produced them".
2. **Appendix F retitled** "Proofs for Section~\ref{sec:optsets}", with the
   label `app:proximal` kept. It has three subsections: F.1 one center and
   two minimizers; F.2 coordinatewise concave quadratics; F.3 the diagonal
   certificate and the proximal stage.
3. **Section 9.3.**
   * Kept: box KKT points, $\Lambda$, $\Psi$, and the statement of
     `lem:diagcert`.
   * The class $\mathfrak D$ is now defined in the text right after the
     lemma (see C-consistency-7).
   * `rem:shor` is shortened to membership (convex, plus a pointer to the
     indefinite example) and the credit sentences, which are unchanged.
   * PROX (`alg:prox`) and DISC (`alg:disc`) stay in the main text as
     precise algorithm environments, as CONVENTIONS section 2 requires. PROX
     is condensed: the two displays are now inline. DISC is unchanged
     (6 lines).
   * `lem:proximal` (statement) moved to F.3. In its place is a summary
     paragraph based on the C-writing-1 verifier fix. It states:
     - the node bound $K_\theta$;
     - the cost per stage, with its bit length;
     - $\dist(y^{(j)},\mathcal S)^2\le\frac{99}{256}\hat\kappa nh_j^2$ under
       set growth with $\kappa_S\le\hat\kappa$, with a pointer to the lemma.

     I made one correction to the verifier's text: it wrote "if
     $\kappa_S\le\hat\kappa$", and the summary now says "if $F$ has set
     growth with a constant $g_S$ such that $\kappa_S\le\hat\kappa$".
   * The discussion after `thm:diagdiscovery` is reduced to two sentences:
     the work limit, and that a failed guess certifies nothing
     (`rem:falseguess`). The table-size computation
     $K_\theta^p\le2(48p\sqrt{\hat\kappa})^p(n+2)\le2(68p\sqrt{\kappa_S})^p(n+2)$
     moved into the proof of Theorem `thm:diagdiscovery`(c). It adds the
     justification $48\sqrt2<68$.
   * `prop:sshard`, together with its credit sentence, its proof and the
     uniqueness discussion, moved to F.3. The main text keeps a 7-line
     summary covering:
     - the dual value equals OPT;
     - the Del Pia-Khajavirad reduction lies in $\mathfrak D$;
     - (i) and (ii) with the condition unless P=NP;
     - deciding whether a given minimizer is unique is coNP-hard;
     - `cor:facecsp` has no counterpart in $\mathfrak D$.

Dependencies of the moved proofs:
* The definitions they use stay in the main text before Appendix F:
  - $\pi_t$, $Y$, $M_t$, $r_t$, $B_t^\uparrow$, $\chi$, cube, face,
    $\Sigma_i$, $Z_t$ and $\mathrm{Adm}_t$;
  - PROX, $X'$, $\varrho$, $\omega$ and $Q_\omega$.
* The lemma `lem:proximal` precedes the proof of
  Theorem `thm:diagdiscovery` that uses it.
* `rem:falseguess` precedes `prop:sshard`.

## Adjudication of assigned findings

| id | verdict | reason | change |
|---|---|---|---|
| C-consistency-7 | ACCEPTED (modified placement) | $\mathfrak D$ was defined only inside Remark `rem:shor`, but Theorem `thm:diagdiscovery` and Proposition `prop:sshard` use it. | Sentence before the theorem: "We write $\mathfrak D$ for the class of continuous box QPs that satisfy the equivalent conditions (a)--(c) of Lemma~\ref{lem:diagcert}(iii), and call it the diagonal certificate class." `rem:shor` now starts with "Convex box QPs belong to $\mathfrak D$". I put the definition in the text after the lemma instead of inside the lemma statement (the task allows either); this keeps the lemma purely mathematical. |
| C-writing-19 | ACCEPTED (for my files) | "optimizer" and "minimizer" were mixed. | Every "optimizer" in `optsets.tex` and `appendix-proximal.tex` is now "minimizer" (0 occurrences remain), including the 9.2 title ("every minimizer at once"), the title of `thm:endpointset`, `cor:facecsp`(iii), `rem:shor`, `prop:sshard` and `rem:falseguess`. "Optimal set" and "optimal value" are unchanged. The intro uses were already removed by front. |
| C-consistency-5 | ACCEPTED (my part) | The proximal weight $\eta=L\theta^2/4$ was a third meaning of $\eta$. | Renamed to $\omega$ and $Q_\eta$ to $Q_\omega$, in PROX, the proof of `lem:proximal` and `rem:falseguess`. The stage denominator $\omega_j$ in proof (iv) is renamed to $\Gamma_j$, which matches the $\Gamma_X2^{\dots}$ denominators of Appendices A and B. The other items of this finding ($P$, $q$, $\nu$, ETH) are not in my files. |
| R-referee-4 | ACCEPTED (my part) | Overloads of $e_i$, $\eta$ and $r$. | $\eta$ as above. $e_i(v_i;x_i)$ is removed from 9.2: the endpoint rounding $Y$ is now defined first, with $\Pr(Y_i=\ell_i)=(u_i-x_i)/s_i$ and $\Pr(Y_i=u_i)=(x_i-\ell_i)/s_i$, and $\pi_t(v;x)=\Pr(Y_{B_t}=v)$. Theorem `thm:endpointset`(b) now reads "$\pi_t(v;x)=0$ for every bag $t$ and every $v\in E(B_t)$ with $r_t(v)>0$" (still factored polynomial equations of degree at most $p$), and its proof now says explicitly that the residual terms vanish iff (b) holds. No new symbol is needed. The exponent $e_i$ belongs to core. $r$: see C-consistency-4. |
| C-consistency-3 | ACCEPTED (my part) | In App F the nearest minimizer was called $s^*$, while $s$ (the width) appears in the same proof ($h_j=s2^{-j}$). The finding's $e_i(v_i;x_i)$ item points at optsets.tex 270-276. | $s^*$ is renamed to $x^\circ$ in the proof of `lem:proximal`(ii), following the finding's own convention for Section 6. $e_i(v_i;x_i)$ is removed (see R-referee-4). The Section 6 and App D items are not in my files. |
| C-consistency-4 | NO CHANGE NEEDED in my files | In Section 9, $r$ already means only the largest number of optimal values of a coordinate, and it is defined at its first use (optsets.tex 8-9) and in `thm:cells`. | The Table 2 entry for $r$ is in `setting.tex` (core); request below. |

C-writing-1 (major; carried out through the CUTPLAN): I applied the verifier's
corrected fix (a) for Section 9. PROX and DISC stay in the main text. Beyond
fix (a), I moved the statement and proof of `prop:sshard` and shortened
`rem:shor`, as the CUTPLAN asks.

## Other corrections made while moving material

* `prop:sshard` assumed $\xi\in[-A,A]^m$, which is a degenerate box if all
  $a_i=0$; the paper requires $\ell_i<u_i$. The statement now requires
  $A\ge1$. In the proof, Subset Sum restricted to $A\ge1$ and $|a_0|\le A$
  stays NP-complete, because the other instances are decided trivially.
* `prop:sshard`(ii) used the letter $\pi$ for a polynomial, which clashes with
  $\pi_t$ in 9.2. It now reads "there is no polynomial bound
  $\kappa_S\le\poly(I)$ that holds, for a suitable set-growth constant, on
  every instance of this form in $\mathfrak D$".
* The uniqueness discussion said only that deciding uniqueness is "hard". It
  now states coNP-hardness and gives the proof: with $a_0=0$ the origin is a
  minimizer and the instance is in $\mathfrak D$, and it is the only minimizer
  iff no nonempty subset sums to zero. That problem is NP-complete because
  Subset Sum with positive items and target $T>0$ reduces to it by adding the
  item $-T$.
* The tilted, disconnected example of `rem:shor` became Example `ex:diagtilt`
  in F.3, with a full verification. The verification now also shows that $H$
  is indefinite ($w=(0,1,2)$, $w^\T Hw=-1$), which the old remark asserted
  without proof.

## Labels

* Moved to `appendix-proximal.tex`: `lem:proximal` (statement and proof) and
  `prop:sshard` (statement and proof). The proofs of `prop:twocenters`,
  `lem:endpointid` and `cor:facecsp` also moved; their statements and labels
  stay in `optsets.tex`.
* New label: `ex:diagtilt` (Appendix F).
* No label was deleted. I checked this by comparing all `\label`s of the
  snapshot files with the new files: none are missing and none are
  duplicated.
* External references to my labels remain valid: they point to labels that
  still exist (for example `prop:twocenters`, `thm:cells`, `lem:cells`,
  `alg:uc`, `lem:diagcert`, `thm:endpointset`, `cor:facecsp`,
  `thm:diagdiscovery`, `sec:endpointset`), and the final build reports no
  undefined reference to any of my labels.

## Requests for other files

* **front (intro.tex):** nothing is needed. The current intro.tex (checked
  at the end of this round) has no "optimizer" left and no reference to
  `app:proximal` or `sec:diagcert`. If the organization paragraph names
  Appendix F again, it should describe it as "Proofs for Section 9".
* **core (setting.tex, Table `tab:notation`):**
  - Add $r$ (C-consistency-4): "largest number of optimal values of a
    coordinate (Sections 8-10); in Section 7, the number of private blocks".
  - Optionally add $\omega$: "proximal weight $L\theta^2/4$ (Section 9.3,
    App. F)". $\omega$ also has local meanings in appendix-localized.tex
    ($\omega_j$), appendix-recourse-convex.tex ($\omega_A$) and
    constraints.tex (treewidth, in the Bienstock-Munoz comparison).
* **coordinator:** in CONVENTIONS section 4, the row "proximal objective
  P(y) -> Q_\eta(y)" is now $Q_\omega(y)$.

## Checks run (targeted, local; CI not consulted)

* Baseline build of the snapshot sections in `/tmp/w5-optsets-before`
  (`latexmk -pdf -interaction=nonstopmode main.tex`).
* Build of the current sections in `/tmp/w5-optsets`, with the same command,
  run three times while editing. My files produce no errors, no undefined
  references and no overfull boxes. The remaining warnings belong to other
  groups' work in progress:
  - `app:computation`, `tab:scip`, `tab:random` and `tab:recourse` are
    undefined (computation);
  - the citation `AbelloEtAl2001` is undefined (limits.tex);
  - one overfull box in appendix-tu.tex.
* `python3 process/w3/checks/optsets-w5-pages.py main.pdf` on both PDFs
  (numbers above).
* `python3 process/w3/checks/optsets-w5-diagtilt.py`: exact rational check
  of Example `ex:diagtilt`. It checks:
  - the Hessian diagonal and indefiniteness;
  - $F\ge0$ on a 1/16 grid, with zero set equal to the two segments;
  - the KKT signs and $\Lambda=\diag(0,0,\frac14)$ at every minimizer on the
    grid;
  - $H+\Lambda=2aa^\T$.

  Result: passed.
* Re-derived by hand:
  - the $99/64$ constant of `lem:proximal`(ii) after the $\eta\to\omega$
    rename;
  - the denominators in proof (iv) with $\Gamma_j$;
  - $48\sqrt2<68$;
  - the zero-sum reduction;
  - Theorem `thm:endpointset` with $\pi_t$ in place of $e_i$.

## Unresolved

* None in my files.
* The cross-file requests above are for core and the coordinator.

## Verification

Verifier for group optsets. Files checked and edited:
`sections/optsets.tex` and `sections/appendix-proximal.tex`. The task named
`process/w5/assign/optsets-verify.json`, which does not exist, so I used the
group's assignment file `process/w5/assign/optsets.json` (6 findings). I also
used the C-writing-1 verifier `corrected_fix` in `process/w4/all-results.json`.

### Outcome

The revision is correct and complete. I found no mathematical error. I made
four small precision fixes, listed below.

### 1. Assigned findings

| id | agent's verdict | verification |
|---|---|---|
| C-consistency-3 | ACCEPTED (my part) | Confirmed. $s^*$ is now $x^\circ$ in the proof of `lem:proximal`(ii), and $e_i(v_i;x_i)$ is gone from Section 9.2. The Section 6 and App D items belong to exact/tu. |
| C-consistency-4 | NO CHANGE NEEDED | Confirmed. In Section 9, $r$ means only the largest number of optimal values of a coordinate (defined in the section intro and in `thm:cells`). The residual tables $r_t(v)$ of 9.2 are a separate, subscripted symbol. The Table 2 entry is a request to core. |
| C-consistency-5 | ACCEPTED (my part) | Confirmed. No $\eta$ is left in my files. The proximal weight is $\omega$ and the objective is $Q_\omega$. The old stage denominator $\omega_j$ is now $\Gamma_j$, which matches $\Gamma_X$ in Apps A and B. $\omega$ occurs in my files only as the proximal weight. |
| C-consistency-7 | ACCEPTED | Confirmed. $\mathfrak D$ is defined in the text right after `lem:diagcert`, before every use (`thm:diagdiscovery`, `prop:sshard`, `ex:diagtilt`). `rem:shor` starts with "Convex box QPs belong to $\mathfrak D$". No other file uses $\mathfrak D$. |
| C-writing-19 | ACCEPTED | Confirmed. `grep -i optimizer` finds nothing in my files, and the 9.2 title is "every minimizer at once". |
| R-referee-4 | ACCEPTED (my part) | Confirmed: there is no $\eta$ and no $e_i(\cdot;\cdot)$ in my files. In my files $J_i$ is a grid interval and $J$, $J_{\hat\kappa}$ are stage limits, both allowed by CONVENTIONS section 4. $R$ is only the height constant. |

### 2. CUTPLAN items

All items for optsets are done. I checked them in the diff against
`process/w5/sections-before-w5/`.

* **Moved proofs.** The proofs of `prop:twocenters`, `lem:endpointid` and
  `cor:facecsp` are in Appendix F, each starting with
  `\begin{proof}[Proof of ...]`. Their statements and labels stay in
  Section 9, each followed by a pointer.
* **Appendix F.** It is titled "Proofs for Section~\ref{sec:optsets}" and
  keeps the label `app:proximal`.
* **Section 9.3** keeps:
  - box KKT points, $\Lambda$ and $\Psi$;
  - the statement of `lem:diagcert`;
  - the definition of $\mathfrak D$;
  - `rem:shor` (membership and credit);
  - PROX and DISC in algorithm environments (`alg:prox`, `alg:disc`);
  - the summary of `lem:proximal`, which states the set-growth hypothesis;
  - the statement of `thm:diagdiscovery`;
  - a summary of `prop:sshard`.
* **Moved to Appendix F:** `lem:proximal`, `prop:sshard` with its proof and
  discussion, and the table-size computation, now in the proof of
  `thm:diagdiscovery`(c).
* **No text lost.** A sentence-level comparison of the snapshot with the
  current files shows no lost sentence. Every snapshot sentence that does
  not occur verbatim is one of:
  - a rename (optimizer, $\eta$, $s^*$, $\omega_j$, $e_i$);
  - the condensed PROX;
  - a summary or rewrite listed in the agent's report.
* **Dependencies.** The moved proofs use only objects defined before them:
  - $Y$, $\pi_t$, $M_t$, $r_t$, $B_t^\uparrow$, $\chi$, cube, face,
    $\Sigma_i$, $Z_t$ and $\mathrm{Adm}_t$ are in 9.2;
  - $X'$, $\varrho$, $\omega$, $Q_\omega$ and $K_\theta$ are in PROX, and
    $K_\theta$ is restated in the statement of `lem:proximal`;
  - $\mathfrak D$ is in 9.3.

  Inside Appendix F, `lem:proximal` precedes the proof of
  `thm:diagdiscovery`, which precedes `prop:sshard`. External references to
  these labels (intro.tex, limits.tex, related.tex) point to labels that
  still exist.
* **Labels.** None is missing and none is duplicated in the paper (`grep` and
  `main.log`). The only new label is `ex:diagtilt`.

### 3. Mathematics re-derived

I re-derived each item below by hand. The script
`process/w5/checks/optsets-verify-exact.py` (exact rational arithmetic) checks
items 1, 4, 5 and 6.

1. **New $\pi_t$ in 9.2.** The definition
   $\pi_t(v;x)=\Pr(Y_{B_t}=v)$ equals the old $\prod e_i/(u_i-\ell_i)$, and
   $\pi_t(v;x)>0$ if and only if $v\in\operatorname{cube}(\chi(x)_{B_t})$.
   - In `thm:endpointset`(b) and its proof, $r_t(v)\pi_t(v;x)=0$ for all
     $v$ if and only if (b) holds, because both factors are nonnegative.
   - Script: identity `eq:endpointid` and $M_{t_0}=\OPT$ on 200 random
     coordinatewise concave quadratics on a path, at 5 rational points each.
2. **`ex:diagtilt`.** Checked:
   - $H=2aa^\T-\diag(0,0,\frac14)$ and its diagonal;
   - indefiniteness, with $w=(0,1,2)$ giving $w^\T Hw=-1$;
   - the optimal set;
   - the KKT signs $\pm\frac18$, $\Lambda=\diag(0,0,\frac14)$ and
     $H+\Lambda=2aa^\T$.

   I also re-ran the agent's `process/w3/checks/optsets-w5-diagtilt.py`
   (passed).
3. **`lem:proximal`(ii) after the rename.** The bound is
   $1+\frac12(1+\frac1{32})+\frac1{32}=\frac{99}{64}$, and the bound
   $d_i(v)\le\frac L4h^2+\omega|v-c_i|^2$ uses $\omega=L\theta^2/4$.
4. **`prop:sshard`.** The new hypothesis $A\ge1$ is needed, because $A=0$
   gives a degenerate box. Subset Sum stays NP-complete on the restricted
   instances.
   - Script, on 99 random instances: at every zero of $F$ the box KKT
     multiplier is $2$ on $x$ and $0$ on $\xi$, and $H+\Lambda=H_{\mathrm{sq}}$
     is PSD (exact $LDL^\T$).
5. **coNP-hardness of uniqueness.** With $a_0=0$ the origin is a minimizer.
   The zero-sum reduction (add the item $-T$) is correct.
   - Script: brute force on 3000 random instances.
6. **Table-size bound** in the proof of `thm:diagdiscovery`(c):
   - $48^2\cdot2=4608<68^2=4624$;
   - `eq:logabsorb` with $n$ in place of $n_P$ holds for every $n$, since it
     reduces to $1/e\le\ln2$; the script checks $p\le40$ and $n$ up to
     $10^{12}$.

### 4. Changes made by the verifier

* **optsets.tex, last paragraph of 9.3 (precision).**
  - The summary now says the Del Pia-Khajavirad reduction is "written with
    unscaled partial sums", as the appendix credit sentence says. Before,
    the main text attributed membership in $\mathfrak D$ to the reduction as
    published.
  - "$\kappa_S$ is not bounded by a polynomial in $I$" is now "no choice of
    set-growth constants bounds $\kappa_S$ by a polynomial in $I$", which
    matches `prop:sshard`(ii), where $\kappa_S$ depends on the chosen $g_S$.
  - The uniqueness claim now says "with bag size three", points to
    Appendix F, and adds "unless $\mathrm P=\mathrm{NP}$" before "Corollary
    `cor:facecsp` has no counterpart". The contrast with the $2^{O(p)}$
    algorithm of `cor:facecsp` needs fixed $p$, and it holds only under
    $\mathrm P\ne\mathrm{NP}$.
* **appendix-proximal.tex, paragraph after the proof of `prop:sshard`.** The
  same two qualifiers ("Unless P=NP", "with bag size three").
* **appendix-proximal.tex, proof of `lem:endpointid`.** The "Checking"
  paragraph no longer repeats the checker sentence that the main text keeps.
  It now states only the extra claim: any tables with nonnegative residuals
  and one zero-residual endpoint assignment give `eq:endpointid`.

### 5. Build and pages

I built a private copy (`/tmp/w5-optsets-verify`,
`latexmk -pdf -interaction=nonstopmode main.tex`) after my edits:
* no errors;
* no undefined references;
* no overfull or underfull boxes from my files.

Remaining warnings from other files:
* the citation `AbelloEtAl2001` is undefined (limits);
* two overfull boxes in intro.tex in an earlier build of this session (not
  present in the final build).

Page spans, measured with `process/w3/checks/optsets-w5-pages.py`
(`main.aux`: `sec:optsets` p. 51, `sec:limits` p. 57, `app:proximal` p. 111,
`app:limits` p. 116):

| Part | Before W5 (snapshot build) | After verification | Change |
|---|---|---|---|
| Section 9 | pp. 53-62, 8.44 pp | pp. 51-57, 6.23 pp | -2.21 pp |
| 9.1 | 2.95 pp | 2.24 pp | |
| 9.2 | 2.59 pp | 1.91 pp | |
| 9.3 | 2.61 pp | 1.83 pp | |
| Appendix F | pp. 116-119, 2.31 pp | pp. 111-116, 5.16 pp | |

Absolute page numbers also reflect other groups' concurrent edits. My
precision fixes added 0.02 pp to Section 9.

### 6. Checks run (targeted, local; CI not consulted)

* `diff -u` of both files against `process/w5/sections-before-w5/`.
* Sentence-level comparison of the snapshot with the current files (inline
  Python).
* Label comparison and a duplicate-label scan over `sections/*.tex`.
* `grep` for leftover symbols ($\eta$, $\omega_j$, $s^*$, $e_i(\cdot)$,
  "optimizer").
* Two `latexmk` builds in `/tmp/w5-optsets-verify` (before and after my
  edits), with inspection of `main.log`.
* `python3 process/w3/checks/optsets-w5-pages.py` on the verifier build and
  the agent's snapshot build.
* `python3 process/w3/checks/optsets-w5-diagtilt.py` (passed).
* `python3 process/w5/checks/optsets-verify-exact.py` (all checks passed).

### 7. Unresolved

Nothing in my files. The agent's cross-file requests remain open:
* core: add $r$, and optionally $\omega$, to Table `tab:notation`;
* coordinator: update CONVENTIONS section 4 from $Q_\eta$ to $Q_\omega$.

One minor point, left unchanged: the constant term $c$ of
$F=\frac12x^\T Hx+b^\T x+c$ and the proximal center $c$ share a letter in
9.3. Context separates them, and no reviewer flagged it.
