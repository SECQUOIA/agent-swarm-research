# R2: mathematical correctness of the recourse sections

Key: `R2-math-recourse`. Files reviewed: `sections/recourse.tex`, `recourse-valuefn.tex`,
`recourse-local.tex`, `recourse-convex.tex`, `recourse-cuts.tex`, `recourse-mixed.tex`,
`recourse-balanced.tex`, `appendix-smoothed.tex`, plus the parts of `setting.tex`, `grids.tex`,
`growth.tex` and `exact.tex` that these files invoke. The compiled section is Section 7
(pp. 24-47 of `build/main.pdf`) and Appendix C (p. 96).

## 1. Verdict

No main claim in these files is false, and I found no invalid proof of a main result.
Every theorem, lemma, proposition and example listed in the brief was re-derived line by line;
the numerical examples were re-checked in exact arithmetic (Section 4).

Four major problems (M1-M4) and one minor correctness slip (m1) need fixing before submission:

1. **Certificate checking (M1; Theorem `thm:cv`(i), `recourse-convex.tex` l. 69, 348-349).**
   The text says that any leaf certificate can be checked in polynomial time. That is false for the
   general finite polytope families allowed by Definition `def:leaf`, because deciding whether
   the polytopes cover the box is coNP-hard. The claim holds once certificates are required
   to be binary space partitions, which is what Proposition `prop:cert-exist` builds and what
   Lemma `lem:cv-bits` already assumes.
2. **Exact output without growth (M2; Theorem `thm:cv`(iii), l. 388-411).** The acceptance test is
   claimed to be valid "independently of growth". Its validity rests on the denominator bound
   $\Omega_0$ for $\OPT$. Lemma `lem:cv-height` proves that bound only for a *unique* minimizer.
   The claim is true, but the paper does not prove it. A short extension of the lemma closes the gap.
3. **Theorem `thm:valuefn` overstates the running time (M3).** As stated, it inherits
   Theorem `thm:approx` with the exponent $(I+q+1)^5$, and the proof says that "the arithmetic
   bounds are unchanged". Neither holds for value factors, whose values have no common
   denominator. The paper's own Lemma `lem:cv-bits` gives bit length $m_0\poly(I+b)$, and
   the exponent depends on the evaluation oracle.
4. **Notation (M4).** The same private-block model is written in two incompatible notations in
   adjacent subsections, and several symbols have two or three meanings inside Section 7. The
   most damaging case is $\mathcal R$, which means *retained* in `recourse-convex.tex` but
   *residual* (eliminated) in `recourse-cuts.tex` and `recourse-mixed.tex`.
5. **Negative curvature bounds (m1).** In Theorem `thm:cv`, the $L_i$ of `eq:cv-L` can be
   negative, as for the $v_i$ of the ladder. Definition `def:curvature` requires
   $L_i\ge0$. Used as written in the corrections, a negative $L_i$ gives an invalid bound.
   Example: $V=-v^2$ on $[0,1]$, $L_v=-2$, grid $\{0,1\}$ gives
   $\beta=-1+\tfrac14=-\tfrac34>\OPT=-1$. Clip at zero.

The conclusion also misstates when Theorem `thm:cv` answers the $\nu/g$ question (M5).

## 2. Findings

Severity follows the brief: critical (false main claim or invalid proof), major (real gap, wrong
or misleading statement, missing necessary content, serious clarity problem), minor (local).

### Major

**M1. Leaf certificates are not polynomially checkable as defined.**
Location: `recourse-convex.tex` l. 53-67 (Definition `def:leaf`), l. 69-83, Theorem `thm:cv`(i)
l. 348-349 and proof l. 370-371.
Issue: Definition `def:leaf` allows any finite family of polytopes with union $\Pi$. Checking the
union condition is coNP-hard in the dimension $k$. Reduction from DNF tautology: map a term to
the box $\prod_iI_i$ with $I_i=[\frac12,1]$ for a positive literal, $[0,\frac12]$ for a negated
literal and $[0,1]$ otherwise. The boxes cover $[0,1]^k$ if and only if the DNF is a tautology.
Since $k\le p$, an arrangement-based check costs $(Rm)^{O(p)}$, which is not $\poly(I)$ and
not $f(p)\poly(I)$. The sentence at l. 79-82 notes that BSP leaves cover the root, but the
definition does not require a BSP.
Fix: In Definition `def:leaf`, replace "is a finite family of closed polytopes
$P_1,\ldots,P_R\subseteq\Pi$ with nonempty interiors and union $\Pi$" by "is a rational binary
space partition of $\Pi$ (each internal node splits its polytope by one rational hyperplane
into two closed halves with nonempty interiors) whose leaves $P_1,\dots,P_R$ each carry a
certificate". Then change l. 69 to "A certificate is checked exactly in time polynomial in its
encoding length: ..." and drop the conditional "When the leaves are produced by a binary space
partition". Proposition `prop:cert-exist` already produces such certificates, and
Lemma `lem:cv-bits` (l. 295) already descends "the partition tree".

**M2. Validity of the exact output of Theorem `thm:cv`(iii) without growth is unproven.**
Location: `recourse-convex.tex` l. 305-334 (Lemma `lem:cv-height`), l. 395-407.
Issue: The procedure accepts $\tilde z$ when its lifted value equals the unique rational of
denominator at most $\Omega_0$ in $[\beta,U]$. This is optimal only if $\OPT$ itself has
denominator at most $\Omega_0$. Lemma `lem:cv-height` proves that only when the slice problem
has a *unique* minimizer. Line 406-407 nevertheless says: "An accepted point is feasible with
optimal value, hence optimal, independently of growth." Without uniqueness, the paper gives
no reason why $[\beta,U]$ could not contain a rational $r>\OPT$ of small denominator equal to
some $V(\tilde z)$. For box QPs, Corollary `cor:height` has no uniqueness assumption, so the
paper's emphasis on certificates "valid without growth" makes this gap visible.
Fix: Prove the lemma without uniqueness, keeping the same constant. Replace the hypothesis "If $f$
has a unique minimizer $x^*$ on $P$, then $x^*=w/q$..." by "Some global minimizer $x^*$ of
$f$ on $P$ has $x^*=w/q$ with $1\le q\le\Lambda_0$; if the minimizer is unique, it is this
one." Proof change: "Among global minimizers choose $x^*$ whose active set $\mathcal E$ has
maximal cardinality. Optimality gives $\nabla f(x^*)\perp\mathcal T$ and $H\succeq0$ on
$\mathcal T$. If some $d\in\mathcal T\setminus\{0\}$ had $Hd\perp\mathcal T$, then
$d^\T Hd=0$ and $f$ would be constant on the line $x^*+td$. Moving $t$ until an inactive row
becomes active, which happens because $P$ is bounded, would give a minimizer with a strictly
larger active set. Hence the reduced Hessian on $\mathcal T$ is nonsingular and positive
semidefinite, so it is positive definite, and the saddle-matrix argument applies unchanged." The
statement "$\OPT$ has denominator at most $2D_f\Lambda_0^2$" then holds unconditionally, and
l. 406-407 becomes correct.

**M3. Theorem `thm:valuefn` claims the exact bound of Theorem `thm:approx` for value functions.**
Location: `recourse-valuefn.tex` l. 127-131 and proof l. 138-140.
Issue: "Theorem `thm:approx` holds with $\kappa_V$" includes the bound
$f(p,\bar\kappa)(I+q+1)^5$, and the proof says that "the arithmetic bounds are unchanged".
Theorem `thm:approx`'s bit analysis uses a common denominator $\Gamma_F\Gamma_X^24^\alpha$ for
all table entries. Value-factor values at grid points have unrelated denominators, such as
determinants of active blocks. The paper says so itself in Lemma `lem:cv-bits` ("No common
denominator across different active sets is needed") and bounds entries by
$m_0\poly(I+b)$ bits. The evaluation oracle is "polynomial" with an unspecified exponent, so
the exponent 5 cannot be inherited. The exact-output sentence (Theorem `thm:exact`, exponent
$C_1$) has the same problem. Also, a table entry is a sum of at most $|\mathcal A|+r+n$
values, not $|\mathcal A|+n$: the $r$ value factors are missing.
Fix: Statement: "...Then Theorem `thm:certificate` holds for $V$; if $F$ has quadratic growth,
Theorem `thm:approx` holds with $\kappa_V$ in place of $\kappa$ and with $(I+q+1)^5$ replaced by
$(I+q+1)^{C}$, where $C$ depends only on the exponent of the evaluation oracle; and if $F$ is a
rational quadratic and each recourse problem can be solved exactly, Theorem `thm:exact` holds
with $\kappa_V$ and such an exponent $C_1$." Proof: "...a table entry is a sum of at most
$|\mathcal A|+r+n$ exactly evaluated values, each of bit length $\poly(I+b)$, so it has bit
length $(|\mathcal A|+r+n)\poly(I+b)$ (Lemma `lem:cv-bits`)." Also add "of bit length
polynomial in $I$" to "rational upper coordinate curvatures $L_i^V$". The exact-output proof
uses $\log(1/g)\le\log\kappa_V+\log(1/L^V)$ and needs $\log(1/L^V)\le\poly(I)$. Finally, say
that the oracle returns a minimizer $y(v)$ and not only the value, since the theorem outputs
$(\hat v,y(\hat v))$.

**M4. Notation clashes across the recourse subsections.**
Locations and meanings:
- $\mathcal R$: retained set (`recourse-convex.tex` l. 14, 32, 656-664) versus residual,
  i.e. eliminated, set (`recourse-cuts.tex` l. 9-12, `recourse-mixed.tex` l. 4-7). $R$ is also
  the recourse set in `recourse-valuefn.tex` l. 3, the height constant $R$ in `exact.tex`, and
  the number of leaves in Definition `def:leaf`.
- Private-block model, written twice. `recourse-valuefn.tex` l. 105-118 has retained set $K$,
  blocks $y^{(t)}$, $t\le r$, scopes $E_t$, block objective $\phi_t(v,y)$ and value factor
  $\psi_t$. `recourse-convex.tex` l. 13-41 has retained set $\mathcal R$, blocks $y_t$,
  $t\le T$, scopes $S_t$, block objective $f_t(y,v)$ and value factor $\phi_t$. So $\phi_t$
  changes meaning, and $E_t$ is a scope set in one subsection and a selection matrix in the
  other (l. 267, 437).
- $K$: retained index set (valuefn), coupling matrix $K_t$ (convex), grid size $K$
  (Lemma `lem:dp`), cap $K_\mu$, index sets $K_l,K_u$ (Theorem `thm:cv-recog`), label count $K$
  (Corollary `cor:core`). $\mathcal K$: multiplier support (Lemma `lem:leaf`) and retained cells
  $\mathcal K_j$ (core search).
- $H_0$: Hessian of $q_0$ (convex) versus entry bound (Lemma `lem:cr-height`). $D_0$:
  denominator with $D_0H$ integral (Corollary `cor:cv-nu`) versus height bound
  (Lemma `lem:cr-height`).
- $g$: growth constant versus the set function $g(S)$ (`recourse-mixed.tex`), central
  gradient $g_0$ and grid points $g_{i,k}$ (Lemma `lem:chaincut`).
- $m_i$: min-marginal $m_i(v)$ versus $|G_i|-1$ in Lemma `lem:chaincut`, in the same subsection
  (`recourse-balanced.tex` l. 5 and l. 31).
- $k$: dimension of $v$ and constraint index in (eq. `leaf-comp`), inside one definition
  (`recourse-convex.tex` l. 51, 60).
- $\beta$: corrected minimum, entry bound in Lemma `lem:cv-height`, bit exponent in
  Lemma `lem:cv-bits`, eigenvalue bracket in Corollary `cor:cv-nu`, shifted coordinate in
  Proposition `prop:cv-limit`, LP variable in Proposition `prop:cr-greedy`, and the constant
  $mh^2/4-1-\epsilon$ in Proposition `prop:star`. The proof of Theorem `thm:cv`(iii) uses
  "$\beta$ ... of Lemma `lem:cv-height`" and "$U-\beta$" in the same paragraph (l. 392, 399).
- $M$: stiffness (examples), metric matrix (Corollary `cor:cv-affine`), number of atoms
  (Theorem `thm:cr-smoothed`). $\sigma$: step function, cancellation $\sigma_j$, KKT pattern
  (proof of Proposition `prop:cert-exist`), noise scale, signs of a balanced quadratic. $P$:
  $\{i:L_i>0\}$, polytope (Definition `def:leaf`, Lemma `lem:cv-height`), $\Delta H$, and
  $\mathcal P$ in `recourse-mixed.tex`. $L$ is also used for the final leaf in the proof of
  Proposition `prop:cert-exist` (l. 240-245).
- $b$: linear coefficient and pair index in Lemma `lem:chaincut` ($b_i$, $\sum_{a<b}$), and the
  greedy vector $b^\pi$ next to $q$'s linear term $b$ in `recourse-mixed.tex`.
- $l_i$ (recourse files) versus $\ell_i$ (Section `sec:setting`). `recourse-valuefn.tex` uses
  both, at l. 33 and l. 48.
- The core is $\mathcal C$ in `recourse-cuts.tex` but $C$ in Corollary `cor:core`, where $C$ is
  also a cell.
Fix: Use one model notation for both private-block descriptions. Suggested: retained $z$ (index
set $\mathcal K$), private blocks $y_t$, $t=1,\dots,T$, scopes $S_t$, block objective $f_t$,
value factor $\phi_t$. Rewrite `recourse-valuefn.tex` l. 105-120 in this notation. Reserve
$\mathcal R$ for the residual in Sections 7.4-7.5, write $E_t$ only for the selection matrix,
and rename the following: leaf count $R\to N_\Pi$; constraint index $k\to s$ in (`leaf-comp`);
$H_0$ in Lemma `lem:cr-height` $\to\bar h$; $D_0$ in Corollary `cor:cv-nu` $\to\Delta_H$;
$g(S)\to\gamma(S)$ or $\Phi(S)$; $m_i\to r_i$ in Lemma `lem:chaincut`; atom count
$M\to N_\gamma$; pattern $\sigma\to\pi$; final leaf $L\to\Lambda$; Lemma `lem:cv-height`'s
$\beta\to\beta_H$ and Lemma `lem:cv-bits`'s $\beta\to b'$; pair index $b\to a'$; core $C\to\mathcal C$.

**M5. The conclusion misstates the scope of Theorem `thm:cv`.**
Location: `conclusion.tex` l. 31-32 ("Theorem `thm:cv` answers this when the convex part can be
eliminated with certified responses whose pieces are small").
Issue: Theorem `thm:cv` gives the parameter $(H_0)_{ii}-\sum_t\sigma_{t,j}$, where $\sigma$ is the
*minimum* over all pieces. By Remark `rem:cv-unstable`, a single small piece without cancellation
destroys it. The size or number of pieces is irrelevant to the $\nu/g$ question. What matters
is $L\le C_0\nu$ (Corollary `cor:cv-nu`).
Fix: "Theorem `thm:cv` answers this when the convex part can be eliminated with certified
responses whose every piece cancels the stiff diagonal curvature, so that $L\le C_0\nu$
(Corollary `cor:cv-nu`); ..."

### Minor

**m1. Negative $L_i$ in Theorem `thm:cv`.** `recourse-convex.tex` l. 341-342, 380.
`eq:cv-L` can give $L_i<0$, as for the $v_i$ in Proposition `prop:cv-ladder`
($L_{v_i}=-2+2\eta\deg_i$). Definition `def:curvature` needs $L_i\ge0$. If a negative $L_i$ is
used in $d_i$, the bound is invalid (example in Section 1, item 5). Fix: "(iii) By (i), $V$ has
upper coordinate curvatures $L_i^+=\max\{L_i,0\}$" and use $L=\max_iL_i^+$ throughout.
Part (ii) is unaffected.

**m2. Lemma `lem:cr-semiconcave` duplicates Lemma `lem:valuefunction`(a) and splits the
discussion.** `recourse-valuefn.tex` l. 32-103. Lemma `lem:cr-semiconcave` is
Lemma `lem:valuefunction`(a) with $K=B$. The proof of Lemma `lem:cr-cell` (l. 78) cites
Lemma `lem:valuefunction`(a), not Lemma `lem:cr-semiconcave`. The paragraph "Part (a) explains
why..." (l. 97) refers to Lemma `lem:valuefunction`, but it comes after two other lemmas and their
discussion. Fix: delete Lemma `lem:cr-semiconcave`. Move the bag-cell material (l. 32-94) to the
start of Section `sec:local`, where it is used. Move l. 97-103 directly after the proof of
Lemma `lem:valuefunction`. Also define $V$ on $\bar X_K$ in (`eq:valuefn`), because the
curvature statement is about the continuous hull.

**m3. Which $L$ the bag-cell lemma uses.** `recourse-valuefn.tex` l. 38-48 use the global
$L=\max_iL_i$. The core search (`recourse-cuts.tex` l. 140-142) uses a core-only $L$ with an
arbitrary residual. The proofs use only coordinates in $B$. Fix: define
$e_B(C)=\frac{L_B}8\sum_{i\in B}w_i(C)^2$ with $L_B=\max_{i\in B}L_i$, and state
Lemma `lem:cr-cell` with $L_B$.

**m4. Lemma `lem:cv-height` uses the row form of Hadamard's inequality.** `recourse-convex.tex`
l. 330-332. The saddle matrix is indefinite, so Lemma `lem:hadamard` (positive-definite,
diagonal form) does not apply. Fix: "Hadamard's inequality $|\det A|\le\prod_i\norm{a_i}$ for
the rows $a_i$ bounds its determinant by $(\sqrt{2n}\,\beta)^{2n}$".

**m5. Theorem `thm:balanced` proof cites the wrong recovery step.** `recourse-balanced.tex`
l. 141-143. The proof of Theorem `thm:exact` uses snapping recovery REC, Proposition
`prop:accept` and Theorem `thm:transfer`, not rational reconstruction. Fix: "...which uses only
the approximation algorithm, the height bounds of Corollary `cor:height`, snapping recovery
(Lemma `lem:snap`, Gaussian elimination under growth) and the acceptance test of
Proposition `prop:accept`".

**m6. Leftover reference to "the report".** `recourse-balanced.tex` l. 163-165. Fix: "This
removes the sign restriction (R1) of Section `sec:cuts` at a price. Residual coordinates with
positive diagonal are gridded and filtered like the core, so their curvature now enters
$\kappa$. The residual graph may still be dense."

**m7. Example `ex:cr-star32` is not the smallest instance.** `recourse-local.tex` l. 222-239.
With $h=\frac12$, $m=17$ and $\epsilon=\frac1{64}$ (or $\frac1{32}$), family (A) already
satisfies its hypothesis, and the bag-local budget $\frac18$ already rejects the optimizer cell
(checked exactly). Also, "this instance refutes budgets depending on $(p,L)$ only" needs the
family, not one instance. Fix: title "An instance with $h=\frac12$". Last sentence: "Because
the growth constant of family (A) degrades as $m$ grows, family (A) refutes every budget that
depends only on $(p,L,h)$; family (B) refutes every budget that depends only on
$(p,\kappa,L,h)$."

**m8. "Essential requirement" claims necessity that is not proved.** `recourse-local.tex`
l. 94-98. Proposition `prop:cr-osc` proves only sufficiency. Fix: "For filtering alone,
Proposition `prop:cr-osc` shows that it suffices to control the oscillation of $W_B-\ell$ over
the compared bag states by $O(e)$; Example `ex:cr-star32` shows how the filter fails when this
oscillation grows with $m$."

**m9. "Separate concavity (R1) is essential."** `recourse-cuts.tex` l. 126. This is not proven.
Fix: "Separate concavity (R1) is needed for this oracle: ...".

**m10. Description of Del Pia and Khajavirad.** `recourse-cuts.tex` l. 129-133. Their
Theorem 4 / Corollary 1 do not require "few positive-diagonal variables". They require a
binary part of logarithmic treewidth with logarithmic interfaces, solvable continuous
components, and a low-dimensional coupling. Fix: "...and prove polynomial classes in which the
binary part has logarithmic treewidth and interfaces and couples to the continuous part through
a space of bounded dimension; their conditions concern the structure of the binary part rather
than its signs \cite{DelPiaKhajavirad2026}."

**m11. "Membership in this regime can be checked."** `recourse-convex.tex` l. 468-470. The
bracket $\nu\le\beta<2\nu$ decides $L\le C_0\nu$ only up to a factor 2. Fix: "Membership can
be tested up to a factor two: a rational $\beta$ with $\nu\le\beta<2\nu$ is computable in
polynomial time, and $L\le C_0\beta/2$ implies $L\le C_0\nu$."

**m12. Wrong attribution in the limits paragraph.** `recourse-convex.tex` l. 663-664: "By
Proposition `prop:vf-curv`(c), no certificate yields a parameter below
$L_{\mathcal R}/g_{\mathcal R}$." This follows from validity, Theorem `thm:cv`(i) together with
$g\le g_{\mathcal R}$ (Lemma `lem:cv-growth`), not from part (c). Part (c) is per factor, and the
certified $L_i$ for the sum can exceed $L_{\mathcal R}$. Fix: "Since every certified $L_i$ is
valid (Theorem `thm:cv`(i)) and $g\le g_{\mathcal R}$ (Lemma `lem:cv-growth`), no certificate
yields a parameter below $L_{\mathcal R}/g_{\mathcal R}$."

**m13. Remark `rem:cv-unstable`, last sentence.** l. 731: "The certified quantity is a maximum
over pieces". $\sigma$ is a minimum, and the certified curvature is a maximum. Fix: "The
certified curvature is a maximum over pieces, however small the piece."

**m14. Theorem `thm:cr-filter` and the remark after it.** `recourse-local.tex` l. 9-17, 49-58.
$\eta\ge0$ is used but never introduced. The conclusion "$\min\{\lambda,U\}$ is a certified
lower bound" also needs the top-level cells to cover $\bar X_B$. Fix: "...a number
$\eta\ge0$..." and "In a multilevel scheme whose top-level cells cover $\bar X_B$ and that
refines only retained cells, ...".

**m15. Prop `prop:star` preamble.** `recourse-local.tex` l. 116-118. "Every node has correction
$Lh^2/8$ in every coordinate" holds for a common $L$. With per-coordinate $L_i$, as in family (B),
where $L_y=2$, the correction is $L_ih^2/8$. Fix: "...with a common curvature bound $L$ every
node has correction $Lh^2/8$ ...".

**m16. Appendix C opening.** `appendix-smoothed.tex` l. 2: "remove this effect" has no
antecedent in the appendix and repeats `recourse-cuts.tex` l. 231. Fix: "Example `ex:cr-flat`
shows that without growth the deterministic count can be exponential in the number of levels.
Adding random linear terms to the core removes this effect in expectation." In
`recourse-cuts.tex` l. 232, "the core coefficients are drawn" should be "random linear terms
$\gamma_ix_i$, $i\in\mathcal C$, are added, with $\gamma_i$ drawn".

**m17. Duplicate network construction.** Proposition `prop:cr-cut` is the case $|G_i|=2$ of
Lemma `lem:chaincut`, and the two use $\operatorname{cap}(S)$ and $\operatorname{cut}(z)$ for the
same quantity. Lemma `lem:balance` repeats the BFS sign test of `recourse-cuts.tex` l. 18-20.
Fix: prove Lemma `lem:chaincut` once, before Section `sec:cuts`, derive Proposition
`prop:cr-cut` as its binary case, and use one name for the cut capacity.

**m18. Section structure.** Section 7.6 ("Corrected grids without a tree decomposition") is not
about recourse; only Corollary `cor:core` connects it to Section 7.4. Section 7 spans 23 pages.
Fix: move Section 7.6 to a short section of its own after Section `sec:exact`, or to the
end of Section `sec:growth`, and keep Corollary `cor:core` in Section 7.4 as a remark that
cites it.

**m19.** `recourse-valuefn.tex` l. 8: delete "Clearly". `recourse-convex.tex` l. 286-288: "a sum
of $m_0$ rationals with numerators and denominators at most $2^\beta$" should say "absolute
values of numerators".

## 3. What was re-derived and holds

- **Lemma `lem:valuefunction`.** (a) An infimum of concave functions over $y\in X_R$, with
  $(v+te_i,y)\in\bar X$, is concave. (b) Holds, using $V(v^*)=\OPT$ at the unique minimizer.
- **Lemma `lem:cr-cell`.** Jensen's inequality for $\varphi-\frac L2t^2$ gives
  $\E\varphi(Y)\le\varphi(\xi)+\frac L2\Var Y$. $\Var Y_i=(\xi_i-a_i)(b_i-\xi_i)\le(b_i-a_i)^2/4$,
  and $\Var Y_i=0$ on unit integer intervals. The sequential conditioning is valid because the
  $Y_i$ are independent. The final bound $W_B(\xi)\le F(x)$ uses the product structure of $X$.
- **Theorem `thm:valuefn`.** The certificate and growth parts hold. The exact part holds:
  under point growth, $g\|(\hat v,y(\hat v))-x^*\|^2\le V(\hat v)-\OPT$, and
  Theorem `thm:transfer` applies to the original box QP with $\varepsilon_S$ of $F$. The bit
  statement is corrected in M3.
- **Theorem `thm:cr-filter` (a)-(c) and Proposition `prop:cr-osc`.** Every inequality checked.
  Corners are feasible, which gives $W_B\ge\OPT$.
- **Proposition `prop:star`.** (A): $V(x)=(1-mh^2/4)x^2+\beta x$; $U_G=0$; the unique optimizer
  cell; the corner minimum $(1-h)(mh^2/4-h-\epsilon)$; the threshold; the limiting ratio
  $(1-h)^{-1}$; $g\le\epsilon/(1+mh^2/4)$. (B): $V_h(t)=2t^2-dh|t|+d^2h^2/4$;
  $U_G=\frac12-\frac{dh}2+\frac{d^2h^2}4$; the corner gap $dh(\frac12-h)+2h^2-\frac12$; the
  spectrum $\{3\pm\sqrt5,2\}$ and $\kappa=2(3+\sqrt5)$. All exact (Section 4).
- **Lemma `lem:leaf`, Proposition `prop:vf-curv`.** The KKT identity, $G_kB=0$ on the multiplier
  support, $\nabla^2q_P=-B^\T CB$ and the energy formula hold. In (b), the covering argument and
  the downward jumps of the concave $\phi$ give concavity. (c), optimality of the certified
  cancellation: interior points of each leaf force $\sigma'\le(B_r^\T CB_r)_{jj}$, so $\sigma_j$
  is the largest valid constant for that factor and is independent of the certificate.
- **Proposition `prop:cert-exist`.** The KKT pattern polyhedra have bounded multipliers for a box.
  The full-dimensional projections cover $\Pi$ by density and closedness. Barycentric
  interpolation stays in $\Omega_\sigma$ by convexity. Each final BSP leaf lies in one simplex.
- **Lemma `lem:cv-growth`, Corollary `cor:cv-affine`** ($H_{\rm red}=J^\T\nabla^2FJ$,
  $J^\T J=M$), **Corollary `cor:cv-nu`** (eigenvalue separation $\nu\ge D_0^{-d}\beta_0^{1-d}$).
- **Lemma `lem:cv-height`** (under uniqueness), and **Theorem `thm:cv`** (i), (ii), (iv), and
  (iii) under growth. The reconstruction windows $1/(4R_0^2)$ and the threshold
  $\min\{1/(4\Omega_0^2),g/(32R_0^4)\}$ hold. M2 is the only gap.
- **Theorem `thm:cv-recog`.** The common central gradient, the necessity argument through the
  "affine, nonnegative, zero at an interior point" fact, sufficiency through box KKT, and the LP
  encoding through Farkas multipliers all hold. For the example $(y_1+y_2-z)^2$, the selector
  $(z/2,z/2)$ is the *unique* affine optimal selector.
- **Example `ex:cv-fm`.** All three responses, values, KKT signs, $B^\T CB$ values and piece
  curvatures $8,0,2M/(M+1)$ hold symbolically in $M$. $\sigma=2M$ because
  $2(M+2)^2/(M+1)\ge2M$.
- **Proposition `prop:cv-ladder`.** The identity $z^2+f_M-\frac1{20}=t^2+Mr^2+s^2+\frac u5$, the
  growth $\frac1{12}$ via $u^2\le2s^2+8t^2$ and $w^2\le3(r^2+s^2+t^2)$, the negative inertia $m$
  (checked exactly for $m\le4$), $2\le\nu\le\sqrt5$, $L\le41/4$ and $g\le33/16$ all hold.
- **Proposition `prop:cv-limit`.** The SOS bound
  $\frac34(\alpha-\frac32\beta)^2+\frac1{16}\beta^2$, the eigenvalues $4M$ and $-\frac12$, the
  admissible sets, $y_c$, $x_c$, the clipped curvatures $2M-\frac14$, the concave interior piece
  ($V''=-2M/(2M-\frac14)$), $V(y_c)=\frac32-O(1/M)$ and the rescaling argument all hold.
- **Lemmas `lem:cv-energy`, `lem:cv-envelope`.** The weights $2g/(2g+c)$ and $c/(2g+c)$; the
  envelope growth $g\lambda/(2g+\lambda)$; the ratio $2+2\nu/g$.
- **Lemma `lem:cr-endpoint`, Proposition `prop:cr-cut`, Theorem `thm:cr-oracle`.** Expansion,
  $\omega_{ij}=c_{ij}d_id_j\le0$, and the cut identity (exact check, 1706 labels). Edmonds-Karp
  integrality holds after scaling.
- **Theorem `thm:cr-search`** (a)-(d), **Lemma `lem:cr-charge`** ($|\mathcal K_j|\le2^kN_j$ and
  $4^k$ corners per retained cell), **Proposition `prop:cr-growth`**, **Example `ex:cr-flat`**
  (diagonal products are children of diagonal products; $\Omega((L/\varepsilon)^{k/4})$ with
  $k$-dependent constants).
- **Lemma `lem:cr-height`, Theorem `thm:cr-exact`.** $T_0=\Lambda_c\Lambda_e^2$ clears every
  label-dependent coefficient; the fewest-interior minimizer has nonsingular $A_{SS}$; Leibniz
  and Cramer; separation by $D_0^{-2}$; $J=O(I^2)$. Exact check on 60 random instances.
- **Lemma `lem:cr-law`, Theorem `thm:cr-smoothed`.** The interval $I_i(v)$ is independent of
  $\gamma$; its length is $Lh+4e_j/h=Lh(1+k/2)$ by concavity at $t=-h,0,h$; the product bound
  follows by independence; summing coordinatewise uses $2^j-1<M$ for $j\le J-1$. In Remark
  `rem:cr-smoothed`, the comparison $(k^2L/\delta)^k$ versus $(kL/\delta)^{k/2}$ and the
  approximate-oracle variant $1+(1+a)k/2$ also hold.
- **Propositions `prop:cr-submod`, `prop:cr-greedy`.** The lattice submodularity of $\tilde q$
  (unary terms cancel; mixed-sign pairs give $(s_i-t_i)(s_j-t_j)\le0$ times a nonpositive
  coefficient) holds. So do the greedy inequality $b^\pi(T)\le h(T)$, Edmonds' min-max, and the
  LP and its dual (optimal value $-\min h$). The prefix decomposition of $(b^\pi)^\T y$ is a
  convex combination with weights summing to 1, using $h(\emptyset)=0$.
- **Lemma `lem:balance`, Lemma `lem:chaincut`, Theorem `thm:balanced`, Corollary `cor:core`.**
  The threshold encoding, $w=H_{ij}\delta_{i,k}\delta_{j,l}\le0$, the infinite chain arcs that
  force monotonicity, and the cut identity hold. Exact check on 120 random balanced instances with
  nonuniform grids and arbitrary unary terms, plus 871 min-marginals. The graph sizes and the
  polynomial dependence on $\kappa$ through $K_\mu=O(\sqrt\kappa\log n)$ hold.
- The literature statements in Remark `rem:cr-cut-prior` and in the remark after Corollary
  `cor:core` about Burer, Natarajan and Willemsen (tight for $n\le3$, Example 4 at $n=4$, open
  for $n\ge4$ in footnote 2; Kim and Kojima under $c\le0$; nonpositive diagonal via Padberg)
  match `literature/papers/burer2025-on-the-semidefinite-representability-of/fulltext.md`
  l. 39-67. The description of Del Pia and Khajavirad needs m10.

## 4. Targeted checks actually run

All checks are in `process/w2/checks/`, use exact `fractions.Fraction` or SymPy, and were run
one at a time with `python3 -B`. No project-wide verification was run and no CI was inspected.

- `r2_star.py` (passed): family (A) for $j\in\{1,2,3\}$, two values of $\epsilon$ and three
  values of $m$ each: $U_G=0$, $V(0)=0$, $V(1)=-\epsilon$, the corner minimum, the threshold
  identity, and corner minimum $=\min\{V_h(1-h),V_h(1)\}$. Family (B) for $j\in\{2,3,4\}$ and
  three $d$ each: the $V_h$ formula, $U_G$, both cells' corner gap. Exact spectrum of $H$ for
  $d=2,3,4$, with $\kappa=2(3+\sqrt5)$. All numbers of Example `ex:cr-star32`. A search shows
  $m=17$ already works at $h=\frac12$ (m7).
- `r2_recourse.py` (passed):
  1. `ex:cv-fm` symbolically in $M$, with KKT signs at $4\times21$ points per piece.
  2. Ladder identity, exact negative inertia by Descartes' rule on the characteristic
     polynomial, and $\lambda_{\min}$ bounds for $m=1,\dots,4$.
  3. `prop:cv-limit`: SOS identity, eigenvectors, $y_c$, $x_c$, piece formulas, interior
     concavity, the $V(y_c)$ expansion, and growth $\frac18$ on a $41\times41$ rational grid
     for $M\in\{1,2,5,50\}$.
  4. `prop:cr-cut`: 150 random (R1)-(R2) instances with integer and rational boxes; the cut
     identity on every label; own Fraction Edmonds-Karp versus brute force.
  5. `lem:chaincut`: 120 random balanced instances with nonuniform grids and random $\eta$;
     min cut versus brute force, plus 871 min-marginals.
  6. `lem:cr-height`: 60 random instances; every label optimum has denominator at most $D_0$.
