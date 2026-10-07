# R1-math-core: mathematical correctness of Sections 3–6 and Appendix A

Scope: `sections/setting.tex` (with `setting-growthcert.tex`), `grids.tex`,
`growth.tex` (with `growth-sharp.tex`), `exact.tex` (with the subsection
`exact-localized.tex`, which `main.tex` inputs directly after it and which
therefore renders as Section 6.6), `appendix-growth.tex`, and the proof of
Corollary 6.19 in `appendix-localized.tex`.

Several of these files changed on disk while I was reviewing them
(`growth-sharp.tex`, `setting-growthcert.tex`, `exact-localized.tex` and
`appendix-localized.tex` were added). Line numbers below refer to the snapshot
in `process/w2/R1-snapshot/`, taken at 01:20 on 2026-10-03. At the end of the
review the snapshot was byte-identical to `sections/`. Labels are given with the
numbers from `build/main.aux` built at 01:19.

## Verdict

No critical issue. I re-derived every lemma, proposition and theorem in scope.
Every main statement is correct under its stated hypotheses, and every
numerical constant holds.

Three findings are major:

- The roadmap of Section 6 is stale. Its scope sentence says that $F$ is a
  quadratic "Throughout Sections 6.1–9.1", which covers Sections 7 and 8.
- Corollary 6.19 (`cor:local`) shows only that $x^*$ would pass the
  localized test. The text claims that the test succeeds, but no candidate
  rule is shown to produce $x^*$.
- A quantitative claim in `growth-sharp.tex` cites a theorem that does not
  prove it.

The remaining findings are minor: imprecise wording, notation clashes, typos,
and one unstated variant whose constants I checked.

## What was re-derived and confirmed

- **Setting (Def. 3.1, 3.2, Lemma 3.3).**
  - $\bar\kappa\le\kappa$ holds.
  - Under rescaling $x_i=\alpha y_i$, $L_i$ scales by $\alpha^2$, so
    $\bar\kappa$ is invariant.
  - For the separable example, $\bar\kappa=2$ and
    $\kappa=2\max L_i/\min L_i$.
  - The supremum $\gamma^*$ is attained, because $\norm{x-x^*}_{\mathbf L}$
    depends only on $x^*_P$, which weighted growth makes unique.
  - Lemma `lem:growthcert`(a) is correct: on the box,
    $\zeta_id_i\ge\mu_id_i^2$ at the active coordinates.
  - Lemma `lem:growthcert`(b) is correct: $\zeta_S=0$ and
    $H_{SS}\succeq2gI$, hence $L\ge2g$ if $S\ne\emptyset$.
- **Prop. 4.2 (cellwise).**
  - (a) The concavification argument is correct, including integer
    coordinates and unit intervals.
  - (b) The bijection between pairs $(C,y)$ with $y\in\mathrm{vert}(C)$ and
    independent interval choices gives $\beta=\min_C\beta(C)$.
  - (c) The formula
    $\beta_i(I)=\min_{v\in\{a,a'\}}(m_i(v)+d_i(v))-L_i\Delta_i(I)^2/8\ge\min m_i$
    holds.
  - The independent-rounding remark (lines 104–108) is also correct: Jensen's
    inequality applied coordinatewise gives
    $\E F(Y)\le F(x)+\sum_iL_i\Var(Y_i)/2$.
- **Lemma 4.3 (DP).** The message recursion, the formula for $A_t$, the count
  $O((|\mathcal A|+n+N)K^p)$ and the outgoing messages via $A_t-M_{u\to t}$
  are all correct.
- **Prop. 4.5, Def. 4.6, Thm 4.7 (filter, path certificate).** Each is
  correct. The paragraph at lines 214–223, which says that filtering records
  are valid certificates, is also correct. It needs $U_j\ge\OPT\ge\beta$ and
  that the next grid spans exactly the filtered box; Algorithm 1 satisfies
  both.
- **Lemma 5.2 (graded grids).**
  - (a) Holds, including integer steps
    $\max\{1,\lfloor h+\theta t\rfloor\}$.
  - (b) The recurrence $t_{k+1}+H/\theta\ge(1+\theta/3)(t_k+H/\theta)$ holds,
    as does the split at $\theta t=2$ for integer coordinates with $h<1$.
    With $\ln(1+x)\ge\frac{23}{24}x$ this gives
    $m\le\lceil\frac{72}{23\theta}\ln(\cdot)\rceil\le\lceil\frac4\theta\ln(\cdot)\rceil$.
  - (c) Holds.
- **Dyadic meshes.** $\frac14<L_ir_i^2\le1$, $h_{i0}\ge s_i$, and $h_{ij}$ is
  a power of two.
- **Lemma 5.3 (invariants).** The energy bound (5.2) holds, and (i)–(v) hold
  with the stated constants. Exact algebra gives (iii)
  $Y\le\frac4{15}(\gamma^{-1}+\bar\kappa)a\le\frac8{15}\bar\kappa a$,
  (iv) $\frac14+\frac5{16}=\frac9{16}$, and (v)
  $Z\le(\frac{13}{15}\gamma^{-1}+\frac4{15}\bar\kappa)a\le\frac{17}{15}\bar\kappa a$.
- **Lemma 5.4 (localization and cap).**
  - $\sqrt{L_i}>1/(2r_i)$ holds.
  - The radius constant is $3+2\sqrt{17/15}+(2+\sqrt{17/15})/\sqrt2=7.2961<7.3<8$.
  - $\theta R_{ij}/H\le\theta+16\theta\rho\le\frac14+4\sqrt{2n_P}$.
  - $\varphi(1)=16.21$, $\varphi(2)=18.547$, and
    $\varphi'(m)\le4/m\le7.2/m\le\frac{d}{dm}10\log_2(m+2)$ for $m\ge2$.
  - So the cap is $10\theta^{-1}\lceil\log_2(n_P+2)\rceil$, and stage 0 has
    at most 3 nodes.
- **Common-mesh variant (lines 155–158).** The same proof gives the radius
  constant $2+\sqrt{17/15}+(2+\sqrt{17/15})/\sqrt8=4.148<4.2$, plus 1 for
  integer coordinates. The cap $8\theta^{-1}\lceil\log_2(n+2)\rceil$ holds,
  with $\varphi_v(1)=12.27\le16$.
- **Theorem 5.7.**
  - (a) Termination holds. Because $h_{ij}$ is dyadic,
    $\lfloor h_{ij}\rfloor=h_{ij}$ when $h_{ij}\ge1$, so $3+2/\theta<K_\mu$
    nodes is correct for integer coordinates as well. At stage $J$,
    $D\le a_J/2\le\frac89\varepsilon$.
  - (b) $\mu^*$ gives $8\bar\kappa\theta^2\le1$. The bound
    $2^{\mu^*}\le4\sqrt2\sqrt{\bar\kappa}\le6\sqrt{\bar\kappa}$ holds; the
    observed supremum is 5.6566. Also $\mu^*\le3(1+\log_2\bar\kappa)$.
  - The geometric sum of caps and (5.4),
    $\lceil\log_2(n_P+2)\rceil^p\le2p^p(n+2)$, both hold. I checked (5.4) for
    $p\le40$ and $n\le10^{15}$; the proof via $e\ln2>1$ is correct.
  - The denominator invariant $\Gamma_X2^\alpha$ holds: centers and box
    endpoints are earlier nodes, and offsets are
    $2^{E-j-e_i}((2^\mu+1)^k-2^{\mu k})/2^{\mu(k-1)}$. The common table
    denominator is $8\Gamma_F\Gamma_X^24^\alpha$.
  - The exponent count is $(J+1)\cdot I^2\cdot b^2\le(I+q+1)^5$. The $I^2$
    comes from $(|\mathcal A|+n+N)(n+2)$. Factor evaluations give the same
    order.
  - $f(p,\kappa)=c_0(c_1p\sqrt\kappa)^p\kappa(1+\log_2\kappa)^2$ follows,
    with $(1+\mu2^\mu)^2=O(\kappa\log^2\kappa)$.
- **Example 5.10.** All four claims hold:
  - the lower bound $\frac34(d_1^2+d_2^2)$ and
    $(\rho-\frac12)^2\le2(\rho-\frac u2)^2+\frac12d_1^2$, giving growth
    $\frac12$;
  - $L\le\frac{21}8$;
  - the strict local minima, from $\delta/8-\delta^2>0$;
  - $p=\max\{w+1,3\}$.
- **Example 5.11.** I re-derived $g=1/8$ and $L=10$ from the proof of
  Prop. 10.8. The unit-box Euclidean $\kappa$ is $\Theta(4^m)$.
- **Prop. 5.5 and Cor. 5.6 (sharpness).**
  - The completed square gives $q_1(a,v_a)\le\frac{\Lambda^2-\sigma^2}{2\Lambda}a^2$
    and $(\Lambda^2-\sigma^2)/(2\Lambda)=2g(\Lambda-g)/\Lambda$, so
    $a^2\le(n-2)\kappa h^2/16$ suffices.
  - In the uniform-rule induction, the claim $w_i(v)\le w_i(0)$ holds and the
    node count $4r+5$ is correct.
  - I confirmed all of this by exact simulation (below).
- **Section 6 (exact output).**
  - The Hadamard proof is correct.
  - Lemma 6.3 (a)–(c) holds: the kernel argument gives $H_{TT}\succ0$, and
    Cramer's rule with $\Delta^2$-scaled rows gives
    $v\in(\Delta\det P_{TT})^{-1}\Z$ and $\Delta\det P_{TT}\le R$.
  - Cor. 6.4 and Prop. 6.6 hold.
  - Lemma 6.7 (snapping) holds:
    - $1/\Delta\ge4n\tau=1/R>2\tau$;
    - $J\subseteq J_0$;
    - $\phi(s)\le\frac32n\tau=\frac3{8R}$;
    - $\phi(v)\in\rho^{-1}\Z$ forces $\phi(v)=0$;
    - every solution is optimal without nonsingularity.
  - Thm 6.8 holds, with $\tau^2/4=1/(64n^2R^2)$ and the existential
    $\varepsilon_0$ by compactness.
  - Lemma 6.10 (uniqueness implies growth) holds.
  - Thm 6.11 holds. It is stated, as it must be, under Euclidean point
    growth (3.2). Under weighted growth only $x_P^*$ is localized, and the
    transfer needs $g_S$ in the Euclidean distance. The proof's
    nonsingularity argument for $H_{J_0J_0}$ under uniqueness is correct.
  - Lemma 6.13 holds: a monomial's range on a box is the interval product.
  - Prop. 6.14 holds:
    $2^{-(1+\lceil\log_2Q_0\rceil)}\le1/(2Q_0)<1/Q_0$.
  - Cor. 6.15 holds.
  - Ex. 6.16 holds:
    $x^3-6x+4\sqrt2=(x-\sqrt2)^2(x+2\sqrt2)$, and the denominator is
    $2^{2^k+1}$.
- **Section 6.6.** Lemma 6.17, Prop. 6.18 and the computations in the proof
  of Cor. 6.19 are correct. These are the node-exclusion constants
  $\frac14+\frac14+\frac78=\frac{11}8$ and $\frac{15}{22}$, with
  $\frac12<\frac45<\sqrt{15/22}$; the integer-step argument; and the Schur
  complement bound. They are correct as proofs that $x^*$ passes the test
  (see M2).
- **Cross-references.** All `\ref`s in the scope files resolve. Two point to
  the wrong place for their content: `sec:exact-nonunique` (M1) and
  `thm:cells` (M3).

## Findings

### Major

**M1. Section 6 roadmap and scope sentence are stale.**
`exact.tex` lines 10–15 and 19.

- **Issue.** The opening paragraph says that this section shows "unions of
  uniform cells restore a rate that is polynomial for fixed bag size". It also
  says "The last subsection treats explicit polynomial factors."
  - The unions-of-cells result is Theorem 9.3 (`thm:cells`) in Section 9.
  - The last subsection of Section 6 is now 6.6, "Localized acceptance",
    which treats quadratics.
- **Issue.** Line 19 reads "Throughout Sections 6.1–9.1, $F$ is a quadratic"
  (`sec:exact-data`–`sec:exact-nonunique`). In the PDF, page 18, this spans
  Sections 7 (recourse) and 8 (coupling constraints), whose objectives are
  not of this form.
- **Issue.** Subsection 6.6 is about quadratics but comes after the
  polynomial subsection 6.5.
- **Fix.**
  - Replace lines 10–15 after "...the *set* of minimizers." with: "Under
    quadratic growth at a unique minimizer this yields exact output in
    $f_1(p,\kappa)\poly(I)$ bit operations (Theorem 6.11). Subsection 6.5
    treats explicit polynomial factors, and Subsection 6.6 gives an
    acceptance test that uses the filtering history. Several minimizers are
    treated in Section 9."
  - Replace line 19 with "Throughout Sections 6.1–6.4, $F$ is a quadratic
    with rational data,".
  - Either move `exact-localized.tex` before `\subsection{Explicit polynomial
    factors}`, or have it restate that $F$ is a quadratic; its line 6 already
    does this.

**M2. Corollary 6.19 (`cor:local`) proves acceptance of $x^*$ only; no
candidate rule is shown to produce $x^*$.**
`exact-localized.tex` lines 70–74 and 76–93; `appendix-localized.tex`.

- **Issue.** Prop. 6.18 tests a supplied candidate $\hat x$. Cor. 6.19 shows
  that at every stage with $h_j\le h^*$ the test accepts $\hat x=x^*$. The
  algorithm does not know $x^*$, and the text calls the candidate "arbitrary,
  for example the stationary point of the face of a feasible incumbent".
- **Issue.** Lines 72–74 and the corollary's last sentence ("this happens
  after $\poly(I)+O(\log\kappa)$ stages") read as a termination guarantee for
  a procedure. What is proved is a property of $x^*$. The stationary point of
  an incumbent's face need not be $x^*$: the incumbent can sit on a wrong
  face, and nothing ties it to $B'$.
- **Fix, option 1.** Specify a candidate and prove it equals $x^*$ under the
  corollary's hypotheses. For example:
  > $\hat x$: fix $\hat x_i$ to the single point of $B'_i$ for $i\notin W$;
  > for continuous $i\in W$ fix $\hat x_i$ at the endpoint of $B'_i$ nearest
  > to $y_j$ if $|y_{j,i}-\ell_i|$ or $|u_i-y_{j,i}|$ is below a threshold,
  > else leave it free; solve $\nabla_{\mathrm{free}}F=0$.
  
  Then show that, for $h_j\le h^*$ (possibly with an extra factor using the
  height separation $1/R$ between interior coordinates and bounds), this
  candidate is $x^*$ because $H_{SS}\succ0$.
- **Fix, option 2.** Weaken the text to what is proved:
  > "...at every stage $j$ with $h_j\le h^*$ the minimizer $x^*$ passes the
  > test of Proposition 6.18; hence a candidate rule that returns $x^*$ once
  > the face of $x^*$ is identified succeeds after
  > $\poly(I)+O(\log\kappa)$ stages."
  
  Also replace "the test succeeds after a number of stages governed by a
  geometric margin" (lines 72–74) by "the minimizer passes the test after a
  number of stages governed by a geometric margin".

**M3. The bound "(2+√2)√(nκ)+7 labels" is attributed to a theorem that does
not prove it.** `growth-sharp.tex` lines 45–49.

- **Issue.** The text says filtered uniform grids "have at most
  $(2+\sqrt2)\sqrt{n\kappa}+7$ labels per coordinate at every stage ...
  (Theorem 9.3 with a single minimizer)".
- **Issue.** Theorem 9.3 (`thm:cells`) bounds a different algorithm: UC,
  with unions of cells, no hulls, and a lattice anchored at $\ell$. Its
  bound is $K_S=12r(2\sqrt{n\kappa_S}+1)$, which is $24\sqrt{n\kappa}+12$ for
  $r=1$.
- **Issue.** A direct argument for centered uniform grids gives about
  $2\sqrt2\sqrt{n\kappa}+O(1)$ for continuous coordinates. With
  $\theta=0$, $Z\le\kappa nh^2/2$, so retained nodes lie within
  $\sqrt{n\kappa/2}\,h$ of $x^*$. So the claim is plausible, but it is not
  proved anywhere, and integer coordinates add terms.
- **Fix, option 1.** Replace with:
  > "Filtered uniform grids also have $O(\sqrt{n\kappa})$ nodes per
  > coordinate at every stage, without any condition on a grading; for
  > example the uniform-cell algorithm of Theorem 9.3 has at most
  > $12(2\sqrt{n\kappa}+1)$ (case $r=1$), so..."
- **Fix, option 2.** Add a three-line proof for centered hull grids with
  $\theta=0$ and state the constant it gives:
  > "with $\theta=0$, (5.2) has no $\theta$ term, so
  > $\norm{z-x^*}^2\le\kappa nh_j^2/2$ for every retained witness; the hull
  > lies within $\sqrt{n\kappa/2}\,h_j+h_j+[i\in I_Z]$ of $x^*$..."

### Minor

**m1. The common-mesh variant is used but not stated.** `growth.tex`
lines 155–158.

- **Issue.** Cor. 6.19 and its proof ((G1)–(G4) in Appendix G) and the
  implementation (Section 11) rely on this variant. The paper supports it
  only by "the same proof gives".
- **Issue.** The stated radius omits the integer term $+[i\in I_Z]$, which
  (G4) uses.
- **Issue.** No stage limit $J$ is given for the variant.
- **Fix.** State the variant as a short lemma:
  > "With $h_j=s2^{-j}$ in every coordinate, $8\kappa\theta^2\le1$ and
  > $a_j=Lnh_j^2$: (ii) $\norm{c-x^*}^2\le4\kappa nh_j^2$, (iii)
  > $\norm{y-x^*}^2\le\kappa nh_j^2$, (iv) $U-\beta_j\le\frac9{16}Lnh_j^2$,
  > (v) $\norm{z-x^*}^2\le\frac{17}{15}\kappa nh_j^2$; the filtered interval
  > lies within $4.2\sqrt{n\kappa}\,h_j+[i\in I_Z]$ of $y_i$; the cap is
  > $8\theta^{-1}\lceil\log_2(n+2)\rceil$. The proof is that of
  > Lemmas 5.3–5.4 with $L_i$ replaced by $L$ and $\norm\cdot_{\mathbf L}$ by
  > $\sqrt L\norm\cdot$."
  
  I checked the constants: $4.148<4.2$, and the cap holds with
  $\varphi_v(1)=12.27\le16$.

**m2. Weighted growth does not require a unique minimizer.**
`setting.tex` line 70. The same wording appears in `abstract.tex`
lines 15–16.

- **Issue.** "The running-time analysis uses a growth condition at a unique
  minimizer" contradicts lines 93–95: weighted growth allows minimizers that
  differ outside $P$.
- **Fix.** Use "The running-time analysis uses a growth condition at a
  minimizer." In the abstract, use "If the objective grows quadratically
  away from a minimizer, in the coordinate-curvature metric, ...".

**m3. The claim "$g$ can be exponentially small in $I$" says nothing.**
`setting.tex` line 104 and `exact.tex` line 290.

- **Issue.** This is trivially true by scaling $F$, and the paper never shows
  it. The meaningful quantity is $\kappa$.
- **Fix.** Use "but $\kappa$ can be exponential in $I$ (Example 5.11, unit-box
  version, and Proposition 10.1)". Delete exact.tex line 290 or replace it
  with the same sentence.

**m4. The meaning of "(at least $F(\ell)$)" is ambiguous.** `growth.tex`
lines 43–44.

- **Issue.** It reads as $U\ge F(\ell)$; the intended meaning is
  $U\le F(\ell)$.
- **Fix.** Use "and $U$ the smallest objective value of a feasible point
  known so far, so $U\le F(\ell)$."

**m5. The symbol $\bar\kappa$ is reused as a free parameter.** `growth.tex`
lines 63–64.

- **Issue.** In Lemma 5.3, "let $\bar\kappa\ge\max\{1,1/\gamma\}$" reuses the
  symbol defined in Def. 3.2 as $\max\{1,1/\gamma^*\}$.
- **Fix.** Use a different symbol, for example "let
  $k\ge\max\{1,1/\gamma\}$ with $8k\theta^2\le1$", and in Lemma 5.4 and
  Thm 5.7 apply it with $k=\bar\kappa$.

**m6. The inequality $\varphi(m)\le10\log_2(m+2)$ fails at $m=1$.**
`growth.tex` lines 148–150.

- **Issue.** "hence $\varphi(m)\le10\log_2(m+2)$" is false at $m=1$:
  $\varphi(1)=16.21>10\log_23=15.85$. Only the ceiling version holds there.
- **Fix.** Use "hence $\varphi(m)\le10\log_2(m+2)$ for $m\ge2$, and
  $\varphi(m)\le10\lceil\log_2(m+2)\rceil$ for all $m\ge1$."

**m7. The termination argument does not say why $3+2/\theta$ holds for
integer coordinates.** `growth.tex` lines 197–204.

- **Issue.** The bound $3+2/\theta$ for integer coordinates with
  $h_{ij}\ge1$ uses $\lfloor h_{ij}\rfloor=h_{ij}$. This is true because
  $h_{ij}$ is a power of two, but the text does not say so.
- **Issue.** The parenthetical about $h_{ij}<1$ is attached to the wrong
  sentence.
- **Fix.** After "...(integer)," insert "and $\lfloor h_{ij}\rfloor=h_{ij}$
  when $h_{ij}\ge1$ because $h_{ij}$ is a power of two; for integer
  coordinates with $h_{ij}<1$ the grid has at most $s_i+1<1/\theta+1$
  nodes". Delete the trailing parenthetical.

**m8. "All numbers" overstates the denominator bound.** `growth.tex`
lines 219–223.

- **Issue.** "all numbers have denominators dividing $\Gamma_X2^\alpha$" is
  true for grid nodes only. Table entries have denominators dividing
  $8\Gamma_F\Gamma_X^24^\alpha$.
- **Fix.** Use "all grid nodes have denominators dividing $\Gamma_X2^\alpha$
  ... and all table entries are integers over the common denominator
  $8\Gamma_F\Gamma_X^24^\alpha$".

**m9. The term count is wrong for factors with several monomials.**
`appendix-growth.tex` lines 44–45.

- **Issue.** "a sum of at most $|\mathcal A|+n$ terms of the form coefficient
  times a product of at most two nodes" fails when a factor has several
  monomials. The bound $b=O(I+\alpha)$ is unaffected.
- **Fix.** Use "a sum of at most $I+n$ terms".
- **Also.** On line 50, $\mu K_\mu\le10\mu2^\mu(I+1)$ already holds; the
  factor 20 is harmless.

**m10. Example 5.10 needs an edge.** `growth.tex` lines 260–266.

- **Issue.** $\frac1{16\Delta}$ is undefined if $\Gamma$ has no edges.
- **Issue.** $\Delta$ also denotes the effective width (Section 4) and the
  common denominator (Section 6).
- **Fix.** Use "for a graph $\Gamma$ on the blocks with maximum degree
  $\Delta_\Gamma\ge1$". Alternatively, write the coupling as
  $\frac1{16\max\{1,\Delta_\Gamma\}}$.

**m11. Prop. 5.5's hypothesis does not match its proof or its use.**
`growth-sharp.tex` lines 20–21.

- **Issue.** The hypothesis says "both grid intervals at 0 of length at least
  $h$". The proof (`appendix-growth.tex` line 99) uses only $w_i(0)\ge h$,
  and Cor. 5.6 (graded rule) assumes only $w_i(0)\ge h_j$. As stated, the
  corollary does not meet the proposition's hypothesis.
- **Fix.** Use "whose grids $G_i$ all contain $0$ with $w_i(0)\ge h$".

**m12. Cor. 5.6 runs outside the definitions it relies on.**
`growth-sharp.tex` lines 31–42.

- **Issue.** "Uniform grids (slope $\theta=0$)" lies outside Def. 5.1, which
  requires $0<\theta\le1/4$.
- **Issue.** "Slope", "grading", "labels" and "nodes" are used for the same
  objects.
- **Issue.** The meshes $h_j=2^{1-j}$ and the start at the center $0$ (not
  $\ell$) appear only in the proof.
- **Fix.** Use "...run the filtered algorithm with common meshes
  $h_j=2^{1-j}$ and uniform grids (Definition 5.1 with $\theta=0$), with
  initial center $0$...". Use "grading" and "nodes" throughout Section 5.

**m13. Typo and notation clashes in Lemma 3.3.** `setting-growthcert.tex`
lines 3–4 and 25.

- **Issue.** The proof writes "$F(x)-F(x^*)=\ell^{\T}d+\frac12d^{\T}Hd$";
  $\ell$ is the lower-bound vector. It should be $\zeta^{\T}d$.
- **Issue.** $S$ (interior index set) and $A$ (active set) clash with
  $\mathcal S$ (minimizer set) and $\mathcal A$ (factor set).
- **Fix.** Replace $\ell^{\T}d$ by $\zeta^{\T}d$. Rename $S$ and $A$ to
  $I_{\rm int}$ and $I_{\rm act}$, here and in Cor. 6.19.

**m14. The approximation and exact bounds are conflated.** `exact.tex`
lines 10–11.

- **Issue.** "this yields exact output within the bound of Theorem 5.7" is
  inaccurate. The exact bound is $f_1(p,\kappa)(I+1)^{C_1}$ (Thm 6.11), not
  Theorem 5.7's $f(p,\bar\kappa)(I+q+1)^5$.
- **Fix.** See M1. Use "in $f_1(p,\kappa)\poly(I)$ bit operations".

**m15. Notation clashes with Sections 4–5, which Section 6 invokes.**
`exact.tex` line 31 and the rest of Section 6.

- **Issue.** $P=\Delta H$ clashes with $P=\{i:L_i>0\}$, which CT uses inside
  EX.
- **Issue.** $R$ (height) clashes with $R$ and $R_{ij}$ (radius).
- **Issue.** $\Delta$ (denominator) clashes with $\Delta_i$ (effective
  width).
- **Issue.** $E,J$ in Lemma 6.7 clash with the dyadic exponent $E$ and the
  stage limit $J$.
- **Issue.** In Section 6.6, $W$ is an index set, while Prop. 6.6 uses $W$
  for a denominator.
- **Issue.** $S=\argmin$ is written $\mathcal S$ in Section 3.
- **Fix.**
  - Rename the matrix to $\tilde H=\Delta H$ and the height bound to
    $R_{\rm ht}$ (or $\Theta$).
  - Note that $I_C^+=I_C\cap P$.
  - Use $\mathcal S$ consistently.
  - Rename $W$ in Section 6.6 to $V$.

**m16. "=" should be "≤" in Remark 6.9.** `exact.tex` lines 257–258.

- **Issue.** "$\log_2(1/\varepsilon_S)=\poly(I)+\log_2(1/g_S)$" is an
  inequality, and it should hold for $g_S\ge1$ too.
- **Fix.** Use
  "$\log_2(1/\varepsilon_S)\le\poly(I)+\max\{0,\log_2(1/g_S)\}$".

**m17. The proof of Thm 6.11 needs $L>0$.** `exact.tex` lines 324–326.

- **Issue.** "$\log(1/L)$ ... polynomial" needs $L>0$. The case $L=0$ is
  handled in Algorithm EX but is not mentioned in the proof.
- **Fix.** Insert "If $L=0$, EX stops after one call (see Algorithm EX);
  otherwise" before "Since $g\ge L/\kappa$".

**m18. Remark 6.12 misstates which recovery needs less accuracy.**
`exact.tex` lines 338–345.

- **Issue.** "Snapping recovery needs only $g/(64n^2R^2)$" suggests a weaker
  requirement than the rounding threshold $g/(32R^4)$. It is weaker only
  when $R^2\ge2n^2$; for example $n=10$, $R=2$ gives $1/25600<1/512$.
  Certification by Prop. 6.6 needs gap $<1/\Omega^2$ in both cases.
- **Fix.** Use "Snapping recovery needs $g/(64n^2R^2)$, which is weaker when
  $R^2\ge2n^2$; it does not need uniqueness and returns a minimizer even when
  $S$ is a continuum. Both routes still need gap below $1/(2\Omega^2)$ for
  the acceptance test."

**m19. Symbols in Cor. 6.15's proof differ from Appendix A.** `exact.tex`
lines 405–412.

- **Issue.** $A_j$ and $\Delta_F$ are not defined. Appendix A uses
  $\Gamma_X2^\alpha$ and $\Gamma_F$.
- **Fix.** Use "nodes with denominators dividing $\Gamma_X2^\alpha$ ...
  denominator dividing $\Gamma_F(\Gamma_X2^\alpha)^d$ ... common denominator
  $8\Gamma_F(\Gamma_X2^\alpha)^d$". Also note that $|e_i|=O(dI)$.

**m20. Ex. 6.16(a) states $g$ and $\kappa$ as if exact.** `exact.tex`
lines 418–420.

- **Issue.** "so it has growth $g=3$ and $\kappa=4$" is imprecise. The best
  constant is $1+2\sqrt2$, which gives $\kappa\approx3.13$.
- **Fix.** Use "so $g=3$ is a growth constant and $\kappa\le4$".

**m21. Unused and clashing notation in Section 6.6.**
`exact-localized.tex` line 7.

- **Issue.** "with gradient $\ell(x)=\nabla F(x)$" is never used, and $\ell$
  is the lower-bound vector.
- **Fix.** Delete it. The proposition already uses $\zeta=\nabla F(\hat x)$.

**m22. Defects in the proof of Cor. 6.19.** `appendix-localized.tex`
lines 20, 29 and 53.

- **Issue.** Line 53, "$x^*\in B$ by (F)", is a dangling label.
- **Issue.** Line 29 writes $l_i$ instead of $\ell_i$.
- **Issue.** Line 20 applies Lemma 3.3(b), stated for continuous boxes, to a
  mixed box.
- **Fix.**
  - Use "by Proposition 4.5".
  - Write $\ell_i$.
  - Use "the argument of Lemma 3.3(b), which uses only directions $e_i$ with
    $i\in S\subseteq I_C$, gives $H_{ii}\ge2g$".
- **Also.** In Cor. 6.19, define $h^*=+\infty$ when $Z=C=A=\emptyset$. Note
  that the stage count also uses $\log\Gamma\le\poly(I)+\log\kappa$.

**m23. Degenerate grids and an imprecise condition in Section 4.**
`grids.tex` lines 10–13 and 186–197.

- **Issue.** Subboxes may be degenerate ($\ell'_i=u'_i$), in which case there
  are no grid intervals or cells, although "$w_i(v)=0$ if there is none"
  anticipates single-node grids. Filtering never produces them.
- **Issue.** (C1) says "not contained in $B_i^{(j+1)}$", which for integer
  coordinates should refer to the interval hull.
- **Fix.** Add "with $\ell'_i<u'_i$" to the definition of subbox and delete
  the clause "($w_i(v)=0$ if there is none)". Alternatively, allow the
  degenerate interval $[a,a]$. In (C1), use "not contained in the interval
  $[\ell_i^{(j+1)},u_i^{(j+1)}]$".

**m24. The rounding remark cites the correlated proof.** `grids.tex`
lines 106–108.

- **Issue.** The remark on independent rounding cites the correlated proof
  (Lemma 8.5). The independent version is proved in Lemma 9.2
  (`lem:cells`).
- **Fix.** Use "(see the proof of Lemma 9.2; Lemma 8.5 gives the correlated
  version used with constraints)".

## Checks run

All checks are targeted, use exact arithmetic or 60-digit mpmath, and were
run locally from `process/w2/checks/`. These are not CI checks.

- `python3 r1_constants.py` checks:
  - the 7.3 and 4.2 radius constants;
  - $\varphi(1)$ and $\varphi(2)$, and the comparison of $\varphi$ with
    $10\log_2(m+2)$ (holds for $m\ge2$; fails at $m=1$ without the ceiling,
    see m6);
  - the derivative claims;
  - the common-mesh cap;
  - $\ln(1+x)\ge\frac{23}{24}x$;
  - $\mu^*$, including $2^{\mu^*}\le6\sqrt{\bar\kappa}$ (supremum 5.6566)
    and $\mu^*\le3(1+\log_2\bar\kappa)$;
  - (5.4) for $p\le40$ and $n\le10^{15}$;
  - the geometric sum of caps;
  - the algebra of Lemma 5.3;
  - the constants of Section 6.6 and Appendix G;
  - $\tau$ and $\phi(s)$;
  - the threshold comparison in m18.
  
  Every check passes except the $m=1$ case recorded in m6.
- `python3 r1_trial_sim.py <seed> <count> <magmax>` (runs with seeds 1, 7,
  11 and 23; 66 instances in total) does the following:
  - implements Def. 5.1, the dyadic meshes, Algorithm 1 and filtering
    literally, using brute-force grid enumeration and `Fraction`;
  - builds planted mixed continuous/integer box QPs with indefinite $H$;
  - certifies a weighted-growth constant exactly via
    $H+2M-2\gamma\,\mathrm{diag}(L)\succeq0$ (exact LDL);
  - at every stage, asserts:
    - Prop. 4.2(b) (cells, for $n=2$);
    - Prop. 4.2(c) at random points;
    - Lemma 5.3 (i)–(v);
    - the radius $R_{ij}$ of Lemma 5.4;
    - the cap $K(\theta,n_P)$.
  
  All assertions held on all 66 instances. Logs:
  `r1_trial_sim_seed11.log`, `r1_trial_sim_seed23.log`.
- `python3 r1_sharp.py` runs Prop. 5.5 and Cor. 5.6 on $n=4,6,10,16$ with
  $\kappa=40,80,32,40$, using filtered uniform grids centered at $0$ and
  $h_j=2^{1-j}$. It confirmed the following at every stage:
  - $0$ is the unique corrected minimizer;
  - every node with $|a|\le\min\{\rho,h\sqrt{(n-2)\kappa/16}\}$ has
    $m_i(a)\le U$;
  - the retained box contains $[-(r+1)h_j,(r+1)h_j]^n$ when
    $(r+1)h_j\le1$;
  - the next grid has at least $4r+5$ nodes.
