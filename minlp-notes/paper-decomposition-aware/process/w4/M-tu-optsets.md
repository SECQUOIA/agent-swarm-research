# W4 review M-tu-optsets: mathematics of Sections 8 and 9 and Appendices E and F

Reviewer key: M-tu-optsets. Files reviewed: `sections/constraints.tex`
(Section 8), `sections/appendix-tu.tex` (Appendix E in the current build),
`sections/optsets.tex` (Section 9), `sections/appendix-proximal.tex`
(Appendix F). Line numbers refer to these sources. Cited results from other
sections were read in their current form: `def:curvature`, `def:growth`,
`def:corr`, `prop:cellwise` and its "Families of intervals" paragraph,
`lem:dp`, `def:filter`, `prop:filter`, `def:graded`, `lem:graded` and its
proof, TRIAL, CT, `lem:commonmesh`, `eq:logabsorb`, `prop:sharp`,
`cor:uniformgrid`, Section 6.1 constants, `lem:statpoly`, `cor:height`,
`prop:accept`, REC, `lem:snap`, `thm:transfer`, `rem:setgrowth`, EX,
`lem:intcurv`, `lim:prop:constraints`, `lim:prop:setgrowth`.

## Verdict

Every theorem, lemma, proposition, example and remark in the four files was
re-derived line by line. The small numerical claims were checked with exact
rational arithmetic. I found no error in a main result, a stated bound or a
proof. The revised constants of `prop:twocenters` are correct:
`beta <= -max{theta^2 M^2/379, h^2/20}`, more than `M/(48 sqrt eps)` x-nodes,
more than `M/(24 sqrt eps)` and `M/24` table entries, and the separate
stage-0 case. Earlier-round issues in these files are fixed: the
`prop:twocenters` consequences for CT, stage 0, "forced" uniform meshes, the
TU complexity claim, the `rem:falseguess` ties, and the no-growth table size.

Three minor problems remain:

1. Theorem `thm:tu-approx` covers explicit polynomial factors, but for
   non-quadratic factors the paper gives no checkable certificate of the
   curvature bound (8.2).
2. Two statements quantify over "every level reached" while referring to the
   next-level domain, which does not exist at the returning level.
3. The level count of Theorem `thm:tu-exact`(c) is off by one.

## Findings

### M-tu-optsets-1 (minor): no curvature certificate for polynomial factors under TU coupling

- **Where.** `constraints.tex:86-103` (Remark `rem:tu-curv`),
  `:320-323` (certificate record), `:410-421` (Theorem `thm:tu-approx`).
- **What.** Theorem `thm:tu-approx` allows "explicitly encoded rational
  polynomials of fixed degree" and says that the output is "certified as in
  Proposition `prop:tu-sound`". The certificate record lists "the curvature
  certificate for (8.2)". Parts (b) and (c) of `prop:tu-sound`, and so the
  checker claim at `:271-274`, rely on (8.2) for the supplied `\bar L`
  (through Lemma `lem:tu-allow`). Remark `rem:tu-curv` gives rational checks
  of (8.2) only for quadratics. Lemma `lem:intcurv` bounds only diagonal
  second derivatives, which is coordinate curvature; Example `ex:tu-fullcurv`
  shows that this is not enough. So for a non-quadratic polynomial the paper
  provides no certificate that a checker could verify. Exact verification of
  (8.2) is a polynomial optimization problem in general.
- **Fix.** Add a sufficient, polynomial-time check to Remark `rem:tu-curv`,
  after "Both checks are rational and change no factor scope.":
  > For explicit polynomial factors of fixed degree and
  > $\mathcal W=\R^{n_c}$, bound each $\lvert\partial_{ik}F\rvert$ on
  > $[\ell,u]\times\prod_k[\min Z_k,\max Z_k]$ by the sum of
  > $\lvert c_m\rvert\max\{\lvert\underline\mu_m\rvert,\lvert\overline\mu_m\rvert\}$
  > over its monomials, with monomial ranges as in Lemma~\ref{lem:intcurv}.
  > Every positive rational that is at least the largest row sum of these
  > bounds is a valid $\bar L$, because the spectral radius of
  > $\nabla^2_{xx}F(x,z)$ is at most its largest absolute row sum. The
  > checker recomputes this bound in time polynomial in $I$.

  Alternatively, restrict the certificate claim of Theorem `thm:tu-approx`
  to quadratic factors.

### M-tu-optsets-2 (minor): "every level reached" also covers the returning level, where the next domain is undefined

- **Where.** `constraints.tex:260` (Prop `prop:tu-sound`, "for every level
  $j$ that is reached") with items (c) and (d), which concern
  $\mathcal D^{(j+1)}$; `constraints.tex:331-332` (Thm `thm:tu-states`, "For
  every level $j$ reached by TU-GRID"), all of whose items concern
  $\mathcal D^{(j+1)}$ or $\Lambda^{(j+1)}$.
- **What.** TU-GRID returns at step (2) at level $J$. Step (3) does not run
  there, so $\mathcal D^{(J+1)}$ is not defined, but the statements include
  $j=J$. Lemma `lem:tu-uniform` already uses the correct quantifier ("at
  which TU-GRID filters"). In TU-EXACT step (3) runs at every level, so the
  issue concerns TU-GRID only.
- **Fix.**
  - `prop:tu-sound`: "For TU-GRID and for its hull variant, for every level
    $j$ that is reached, (a), (b) and (e) hold, and (c) and (d) hold
    whenever step (3) is executed at level $j$:".
  - `thm:tu-states`: "For every level $j$ at which TU-GRID executes
    step (3):".

### M-tu-optsets-3 (minor): off-by-one in the level count of Theorem `thm:tu-exact`(c)

- **Where.** `constraints.tex:553-560`.
- **What.** The statement says that TU-EXACT "terminates by the first level
  $j$ with $E_j\le\dots$, hence after at most $J_{\rm ex}$ levels". The first
  such level is at most $J_{\rm ex}$ (the proof in `appendix-tu.tex:211-215`
  is correct). Levels are numbered from 0, so up to $J_{\rm ex}+1$ levels
  run. For $J_{\rm ex}=0$ the statement says "after at most 0 levels". The
  cost sentence, "as in Theorem `thm:tu-approx` with $J$ replaced by
  $J_{\rm ex}$", correctly sums over levels $0,\dots,J_{\rm ex}$.
- **Fix.** Replace "hence after at most" by "hence at the latest at level",
  so that it reads "hence at the latest at level
  $J_{\rm ex}=\max\{\dots\}=\poly(I)+O(\log\kappa_c)$."

## What was checked and found correct

### Section 8 (`constraints.tex`)

- **Definition `def:tu-model`, Prop `prop:tu-align`.** Both directions of
  `prop:tu-align` hold, including the count $1+\sum_k\lvert Z_k\rvert$.
- **Remark `rem:tu-curv`.** The kernel test with $\Xi_C$ and the projector
  row-sum test are correct. With $\mathcal W=\R^{n_c}$, (8.2) implies
  coordinate curvature.
- **Lemma `lem:tu-round`.** Checked:
  - the right side $(b-Bz-At)/h$ is integral;
  - appending unit rows preserves TU, so vertices of $\mathcal Q$ lie in
    $\{0,1\}^{n_c}$ and vanish on $\mathcal I_0$;
  - each fractional coordinate lies in a cell of $\mathcal D_i$;
  - $Y-x\in\mathcal W$ through the equality pairs;
  - $\E(Y_i-x_i)^2=(x_i-t_i)(t_i+h-x_i)\le h^2/4$.
- **Lemma `lem:tu-allow`.** The Taylor bound along $w\in\mathcal W$ and
  $E_j=n_c\bar Lh_j^2/8$ are correct.
- **Example `ex:tu-fullcurv`.** Correct, including that the allowance is
  attained.
- **Prop `prop:tu-sound`(a)-(e) and the checker claim.** All cases of (c)
  hold: discrete value; node that is a single-point component; node that is
  the endpoint of removed cells; fractional coordinate. The hull variant is
  covered a fortiori. In (d), $y^{(j)}$ is retained, which gives
  monotonicity of $U_j$.
- **Thm `thm:tu-states`.** $a_j^2=2E_j/g_S$; the lattice count
  $\lfloor4a_j/h_j\rfloor+5$; hull localization (c). The finite-projection
  remark: at least $(a'-a)/h_j-1$ nodes.
- **Example `ex:tu-union`.** Checked:
  - $\mathcal S_b$ and the growth constant $1/6$ in both halves;
  - Hessian rows and $\bar L=12$;
  - $216n_b$ and the hull grid of $2^j+1$ nodes.
- **Thm `thm:tu-approx`.** $J$ (with equality), $K_0$, $K_j$, denominators
  $\Delta_\eta2^j$, the table count, the no-growth bound
  $2^J<\eta\sqrt{n_c\bar L/(2\varepsilon)}$, and the claim paragraph.
- **Hardness paragraph.** After scaling, `lim:prop:constraints` has $p=3$,
  $K_Z=2$, $r=1$, $\kappa_c=1$, and $s/\eta=a_0/\gcd$ is the only
  unbounded quantity.
- **Not-FPT claim.** Lemma `lem:tu-uniform` has $\kappa_c=2$, $s/\eta=2$,
  $r=1$, $I=O(n_c\log n_c)$ and at least $n_c^{p/2}$ table entries, so no
  bound $f(p,\kappa_c)\poly(I+\log(1/\varepsilon))$ holds.
- **Section 8.6.** $\Delta$, $\hat H$, $c_z\in\Z^{n_c}$,
  $\hat b_z\in\Delta_\eta^{-1}\Z^{m'}$, the TU height constants, and
  TU-EXACT control flow.
- **Thm `thm:tu-exact`(a)-(c).** The $J_{\rm ex}$ thresholds
  $h_j\le\tau/(n_c\sqrt{\kappa_c})$ and
  $h_j\le 1/(\Omega\sqrt{n_c\bar L})\le 2/(\Omega\sqrt{n_c\bar L})$ are
  sufficient.
- **Prop `prop:tu-misaligned`.** Proof and both instances.
- **The sentence on aligned uniform grids.** It is correct; for $n_c=2$ the
  allowance $E_j$ equals $d_1+d_2$.
- **Example `ex:tu-sum`.** All values, and the triangle
  $(1,0,1),(0,1,1),(1,1,2)$.

### Appendix E (`appendix-tu.tex`)

- **Lemma `lem:tu-statpoly`(a)-(c).** Checked:
  - positive definiteness of $\hat H_{xx}$ on $\ker\hat A_{\mathcal E}$ via
    the vertex argument;
  - the saddle system and the nonsingularity of $\mathsf K$;
  - Cramer's rule with $\Delta_\eta\mid\rho$;
  - the Hadamard row bound
    $(2n_cC^2)^{n_c/2}n_c^{\lvert\mathcal E\rvert/2}\le(\sqrt2n_cC)^{n_c}\le R_{\rm TU}$.
- **Cor `cor:tu-height`.**
- **Lemma `lem:tu-snap`.** $\mathcal J_0\subseteq\mathcal J$; slack at most
  $3\tau/2$; $\psi(\tilde x)\le3/(8\Delta_\eta R)$; $\psi(x^\circ)=0$;
  optimality of all of $\mathcal P_z(\mathcal J)$.
- **The $x_1-x_1^2$ example.**
- **Proof of Thm `thm:tu-exact`.**
- **Remark `rem:tu-cf`.** The least-denominator argument, $a_j<1$, and the
  feasibility clause.
- **Lemma `lem:tu-uniform`.** Checked:
  - the instance is `prop:sharp` with $g=\bar L/2$, $\kappa=2$ and radius
    $h\sqrt{(n_c-2)/8}$;
  - the min-marginal comparison;
  - both induction cases, including $\nu=0$ and $j=0$;
  - $4\nu+5\ge\sqrt{2(n_c-2)}+1$ and
    $(\sqrt{2(n_c-2)}+1)^2\ge n_c$;
  - reachability $4^J\ge8n_c$, $h_{J-1}\le(2n_c)^{-1/2}$,
    $\nu+1\le\sqrt{2n_c}$; level $J-1$ filters by minimality of $J$.
- **The misaligned graded node lists, and the `ex:tu-sum` verification.**

### Section 9 (`optsets.tex`)

- **Prop `prop:twocenters`.**
  - The instance: $\mathcal S$, $\OPT$, curvatures, the symmetry, growth
    with $g_S=1/20$ in both cases, $\kappa_S\le40$.
  - The bound (9.1): case $k=1$; case $k\ge2$ with the
    $\alpha'^2\gtrless\alpha^2/5$ split; the recursion
    $\delta_{k-2}\ge(\delta_k-(2+\theta)h)/(1+\theta)^2\ge23M/100$ when
    $h\le M/16$; $0.23^2/20>1/379$.
  - Consequences: (a) TRIAL uses $G_z=\{0,M\}$, the $x$-interval stays
    $[0,M]$, $M\le h_{x0}<2M$, and stage 0 gives $-M^2/4$; for the common
    mesh, $h_0=M$. (b) $\sqrt{20}+\sqrt{379}<24$. (c) EX's test forces
    $\beta>-1$.
- **UC and the paragraph after it.** Nesting $\mathcal G_{i,j-1}\subseteq\mathcal G_{ij}$,
  cell lengths, spacing $\ge h_j/2$, at most one interior split point.
- **Lemma `lem:cells` and Theorem `thm:cells`.** Gap $\le\frac12nLh_j^2$;
  the count $3\cdot2r(4\sqrt{n\kappa_S}+2)=K_S$; bit lengths; the EX
  variant with $q\le\poly(I)+2\log_2\kappa_S$.
- **Remark `rem:grading`.**
- **Lemma `lem:endpointid`.** Telescoping, the expectation identity,
  trace-back by running intersection, the checking and cost claims.
- **Thm `thm:endpointset`, the $x+y-2xy$ example, Cor `cor:facecsp`(i)-(iii).**
  Including: the uniqueness criterion (an admissible $\ast$-pattern implies
  further admissible patterns); dimension; $\lvert\mathcal S\rvert$;
  distance with $\dist(y_i,X_i)^2$ for $\ast$; linear minimization over
  $\{\mathsf L,\mathsf U\}$ labels.
- **Remark `rem:endpointext`.** The two-value substitution, and "difference
  vanishes at an interior point iff $\psi_i$ is affine".
- **The Rosenberg correspondence.**
- **Lemma `lem:diagcert`(i)-(iii).** Including uniqueness of the maximizer
  of $\Psi$.
- **Remark `rem:shor`.** The example's diagonal, optimal segments, $\Lambda$
  and $H+\Lambda=2aa^\T$; the Shor equivalence (Slater holds for the primal
  SDP).
- **PROX.** $\mu$, $\theta$, $\eta$, $\varrho$.
- **Thm `thm:diagdiscovery`(a)-(c).** Including $K_\theta^p\le2(48p\sqrt{\hat\kappa})^p(n+2)\le2(68p\sqrt{\kappa_S})^p(n+2)$.
  I re-derived (`eq:logabsorb`) via $\sup_tt^pe^{-t}=(p/e)^p$ with $t=x\ln2$.
- **Prop `prop:sshard`.** Decomposition, $\mathcal S$, membership in
  $\mathfrak D$ ($H+\Lambda=H_{\rm sq}$, $\lambda=2$ on $x$), (i), (ii).
- **The zero-subset-sum uniqueness remark.**

### Appendix F (`appendix-proximal.tex`)

- **Proof of Lemma `lem:diagcert`.**
- **Proof of Lemma `lem:proximal`.**
  - Constants: $\theta^{-1}<\sqrt{32\hat\kappa}<6\sqrt{\hat\kappa}$.
  - (i): $\theta\varrho\le\sqrt{n/2}+\frac12$ and $7\theta^{-1}\lceil\log_2(n+2)\rceil$.
  - (ii): the cell chosen on the center side; Prop `prop:cellwise`(a)
    applied to $F+\eta\lVert\cdot-c\rVert^2$;
    $1+\frac12(1+\frac1{32})+\frac1{32}=\frac{99}{64}$.
  - (iii): the induction.
  - (iv): the $t_k$ formula, $\omega_j$, integrality of
    $8\Delta\omega_j^2d_i$ and $4^{\mu+1}\Delta\omega_j^2\eta\lVert y-c\rVert^2$.
- **Proof of Thm `thm:diagdiscovery`.** Including
  $\frac{99}{256}\cdot\frac{\tau^2}{4}<\frac{\tau^2}4$, Lemma `lem:snap`, and
  the guess count $2+\log_2\kappa_S$.
- **Proof of Prop `prop:sshard`.**
- **Remark `rem:falseguess`.** All numbers: $\OPT=-1/64$, $g_S\le1/128$,
  $\kappa_S\ge256$, $\Delta=128$, $R=2^{23}$, $\tau=2^{-26}$,
  $J_{\hat\kappa}=28,28,29$, eigenvalues $-1/64$ and $1/64$. The PROX runs
  are confirmed by exact computation (below).

## Checks run (targeted, exact rational arithmetic)

All scripts are in `process/w4/checks/`. All were run with
`python3 -B <script>` from that directory. All report PASS.

1. **`M-tu-optsets-grids.py`.**
   - Graded grids of `def:graded` with centers 3/10 and 7/10:
     - equal to the printed node list;
     - eleven nodes each, common nodes {0,1};
     - largest interval 3831/20480, $\delta=27/1280$;
     - (8.5) holds with $m=1/2$;
     - positive corrected minimum just above the $\lambda$ threshold.
   - Simple misaligned instance: $\delta=1/3$, threshold $75L/288$.
   - `ex:tu-sum`: grid, corrections, the seven points, $31L/64$,
     $53L/128$.
   - (9.1) of `prop:twocenters` by brute force on 1500 random instances
     (random $M$, $\theta\le1/4$, $h\le M$, center, $G_z\ni0,M$,
     $L_x\in\{2,3\}$). No violation; the largest ratio bound/$\beta$ was
     0.011.
2. **`M-tu-optsets-falseguess.py`.** Exact PROX runs on the instance of
   `rem:falseguess`:
   - $\hat\kappa=1,2$ ($\mu=2$, $\varrho=4$): the origin at stages 0-33,
     with no ties;
   - $\hat\kappa=4$ ($\mu=3$, $\varrho=6$): ties between $(0,0)$ and
     $(1,1)$ exactly at stages 0 and 1; the origin at stages 0-33 with ties
     broken towards the center;
   - $R$, $\tau$, $J_{\hat\kappa}$ and the two matrices as stated.
3. **`M-tu-optsets-endpoint.py`.** 300 random quadratics with
   $H_{ii}\le0$, on mixed boxes with integer coordinates of up to 4 values,
   with a path decomposition and ties (74 instances with several admissible
   patterns, 36 with a continuum of optimizers). Checked:
   - $M_{t_0}=\OPT$;
   - identity (`eq:endpointid`) at random rational points;
   - the characterization of `thm:endpointset` against brute force;
   - $\mathcal S$ as the union of admissible faces;
   - $\lvert\mathcal S\rvert$ from patterns when finite.
4. **`M-tu-optsets-prox.py`.** 27,707 proximal stages on random 2-D box QPs
   with exactly computed optimal sets, $\hat\kappa\in\{1,2,4,8,32\}$, and
   centers with $\dist(c,\mathcal S)^2\le4\hat\kappa nh^2$:
   - $F(y^+)-\OPT\le\frac{99}{256}Lnh^2$ always (largest ratio 0.57);
   - node counts at most $K_\theta$.
5. **`M-tu-optsets-uc.py`.** Exact UC on $F_M$ for $M\in\{8,64,1024\}$ and
   $\varepsilon\in\{2^{-4},2^{-10},2^{-16}\}$, with $z$ continuous or
   integer:
   - both minimizers always retained;
   - $\beta_j\le\OPT$ and $U-\beta_j\le\frac12nLh_j^2$;
   - at most 6 nodes per coordinate (bound $K_S\approx453$), independent of
     $M$. This confirms "Other methods solve this instance easily".
6. **`M-tu-optsets-tusim.py`** (log in `M-tu-optsets-tusim.log`). Exact
   TU-GRID (union and hull variants) and TU-EXACT on a mixed-integer
   instance in which the integer variable enters the coupling row
   ($x_1-x_2+z\le1$, $z\in\{0,1,2\}$), for four objectives, one with two
   minimizers at different $z$. Over 22 levels:
   - $\beta_j\le\OPT\le U_j\le\OPT+E_j$;
   - $\mathcal S\subseteq\mathcal D^{(j)}$;
   - Lemma `lem:tu-snap` at every level satisfying its hypothesis;
   - every TU-EXACT return is optimal.
   The union variant stayed at 5-8 nodes per coordinate. With two
   minimizers, the hull variant grew to $2^{21}+3$ nodes in $x_2$, as
   Example `ex:tu-union` predicts.

No project-wide verification was run, and CI status was not inspected.
