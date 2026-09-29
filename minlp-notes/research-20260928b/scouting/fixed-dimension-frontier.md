# Scout report: fixed-dimension frontier for integer and mixed-integer polynomial optimization

Date: 2026-09-28. Area: `fixed-dimension-frontier`. Status: scouting only.
The new-looking statements in Section 3 have proof sketches and targeted
computational checks. They have not had independent review. Novelty is not
established.

Scratch files are in `research-20260928b/scouting/fixed-dimension-frontier/`:
text extractions of the primary sources, `html2txt.py`, and three check
scripts described in Section 3.

## 0. Summary

- **Quadratic objectives are now settled in fixed dimension.** Ari–Hildebrand
  (arXiv 2609.18266v2, 23 Sep 2026) solve MIQP exactly over any rational
  polyhedron with an indefinite objective in time
  \(2^{O(N\log N)}(m+1)^{O(N)}\varphi_{\max}^{O(N)}(1+\varphi)^{O(1)}\).
  Wei's parallel preprint does the same for pure IQP. Under ETH, Herrmann's
  W[1]-hardness makes the \(O(N)\) exponent optimal.
- **Cubic objectives are settled only for bounded pure-integer problems.**
  The same paper handles cubics plus a concave quartic form, and more
  generally "curvature-concave" polynomials, on bounded polyhedra. It states
  that the mixed-integer and unbounded extensions are proved only for
  quadratics.
- **The suggested flagship question is already closed.** An indefinite
  quadratic objective over the integer points of an ellipsoid is NP-hard in
  dimension two. This essentially follows from Manders–Adleman and is recorded
  as Example 22 in Hildebrand–Göß. Section 3.1 adds a small strengthening: one
  ellipse, a concave objective, and no linear constraints. It was checked on
  14,875 instances.
- **First-pass result on the last open case of the Del Pia–Hildebrand–Weismantel–Zemmer (DHWZ) degree classification.**
  That case is cubic objectives over unbounded polyhedra with \(n\ge3\). The
  case \(n=2\) is polynomial by DHWZ Theorem 1.3. In dimension three:
  - (A) Deciding the optimal-value threshold is at least as hard as the
    **principal ideal problem** (PIP) for complex cubic fields, which has no
    known classical polynomial-time algorithm.
  - (B) Unconditionally, some instances have only optimal solutions of
    **exponential encoding length**.

  Both use the norm form of a complex cubic field, which is nonnegative on a
  rational cone. Checks with PARI/GP support both.
- **Best substantive open question:** bounded **mixed-integer cubic**
  minimization in fixed dimension (Section 3.3). An attack plan is given. It
  carries a high risk of being scooped: the Ari–Hildebrand group flagged this
  exact case.
- **Solver significance is low.** Fixed-dimension exact complexity has little
  direct solver value. **Score: 4/10** for this area as a main project. The
  Section 3.2 note is worth writing up as a short side result.

## 1. Frontier map

### 1.1 What is proved (exact assumptions)

| Problem | Status | Source and exact scope |
|---|---|---|
| ILP, fixed \(n\) | P; FPT in \(n\) | Lenstra, Kannan; Reis–Rothvoss \((\log 2n)^{O(n)}\mathrm{poly}\), randomized (cited in 2609.18266 §1.2) |
| Convex / quasiconvex polynomial objective and constraints, fixed \(n\) | P; attained optimum has size \(ld^{O(k^4)}\) | Khachiyan–Porkolab 2000 (local `khachiyan2000-...`, Thm 1.1–1.2: linear objective over convex semialgebraic sets, unbounded allowed); Hildebrand–Köppe \(2^{O(n\log n)}\) |
| Concave objective over a polytope, fixed \(n\) | P | Integer-hull vertices (Cook–Hartmann–Kannan–McDiarmid bound, Hartmann enumeration); Köppe survey §6.3 |
| IQP, \(n=2\), any polyhedron | P | Del Pia–Weismantel SODA 2014 |
| Cubic, \(n=2\), any polyhedron (unbounded included) | P | DHWZ, MOR 2016 (arXiv 1408.4711v2), Thm 1.3, §6 treats unbounded \(P\) |
| Homogeneous polynomial of any fixed degree, \(n=2\), bounded | P | DHWZ Thm 1.6 |
| Homogeneous quartic, \(n=2\), unbounded | Smallest optimum can be exponential (Pell) | DHWZ §1 (\((x^2-Ny^2)^2\), \(N=5^{2k+1}\), Lagarias) |
| Quartic, \(n=2\), polytope | NP-hard | De Loera–Hemmecke–Köppe–Weismantel 2006 (Manders–Adleman) |
| MIQP (varying dimension) | In NP; polynomial-size optima | Del Pia–Dey–Molinaro 2017 |
| Indefinite quadratic forms, fixed \(n\) | FPTAS if \(Q\) has \(\le1\) positive or \(\le1\) negative eigenvalue; general for \(n=3\) | Hildebrand–Weismantel–Zemmer (local `hildebrand2016-...`) |
| IQP, parameter \((n,\max\lvert A\rvert,\max\lvert Q\rvert)\) | FPT | Lokshtanov 2015 (arXiv 1511.00310); Zemmer thesis 2017 |
| IQP with explicit parameter dependence | \((nL)^{O(n^2)}\mathrm{poly}(\varphi)\); MIQP over polytopes \((nL)^{O(n^2(q+1)^2)}\mathrm{poly}(\varphi)\); unboundedness test \((m+n)^{O(n)}\mathrm{poly}(\varphi)\); W[1]-hard with no \((m+\varphi)^{o(n)}\) algorithm under ETH for noncopositivity and unboundedness | Ari–Hildebrand, *Curvature batching*, arXiv 2604.04851v2 (15 Sep 2026), Thm 1.1, Table 1 |
| IQP, parameter \(n\) | W[1]-hard, even with a separable concave objective \(\sum(y_i-x_i^2)\), \(2k\) variables, \(O(k^2n^2)\) rows, coefficients \(O(n^2)\) | Herrmann, arXiv 2608.17818v1 (18 Aug 2026) |
| Pure IQP, fixed \(n\), any polyhedron | P | L. Wei, Optimization Online `?p=36744` (14 Sep 2026); only the abstract page was read |
| **MIQP, fixed \(N\), any rational polyhedron** | **P**: \(2^{O(N\log N)}(m+1)^{O(N)}\varphi_{\max}^{O(N)}(1+\varphi)^{O(1)}\); certifies unboundedness; ETH-optimal exponent \(O(N)\) | Ari–Hildebrand, *Hidden convexity via symmetric displacement covers*, arXiv 2609.18266v2 (23 Sep 2026), Thm 1.1; supersedes 2609.17889 |
| **Bounded pure-integer cubic, fixed \(n\)** | **P**, including cubic plus a concave quartic form, and all curvature-concave polynomials (Def. 7.4) | Same paper, Thm 1.2, Thm 7.7, Cor. 7.8–7.9 |
| Reverse-convex IP \(P\setminus\bigcup\operatorname{int}C_i\), fixed \(n\) | P, given a boundary hyperplane cover | Hildebrand–Göß, arXiv 2409.05308v2, Thm 44 |
| Convex constraint plus reverse-convex constraint, \(n=2\) | NP-hard (AN1) | Hildebrand–Göß, Example 22 |
| Integer cubic unboundedness | Rays do not suffice for \(n\ge3\); "thin rays" characterize it for every \(n\); degree \(\ge4\): no ray certificate | Del Pia, arXiv 2511.02983v2 (21 Sep 2026), Thm 2, Prop. 1–2. Prop. 2 uses \(2x_1^3+x_2^3+4x_3^3-6x_1x_2x_3\), which is the norm form of \(\mathbb Q(\sqrt[3]2)\) up to a coordinate permutation |
| Cubic, continuous | Irrational unbounded rays; rational-solution hardness; fixed-dimension polynomial feasibility in NP | Bienstock–Del Pia–Hildebrand 2023 (local), Prop. 2.11, Thm 2.8, Thm 3.6 |
| Approximate MIQP | Polynomial \(\epsilon\)-approximation when the number of integer variables and the number of negative eigenvalues are fixed; both conditions necessary unless P=NP | Del Pia, arXiv 2607.29386 (31 Jul 2026); earlier fixed-rank version (local `pia2023-...`). Rank-one QP is NP-hard (Pardalos–Vavasis); MIQP unboundedness is NP-complete at rank 3 with \(p=0\) |

### 1.2 How the Ari–Hildebrand mechanism works, and where it stops

The feasible integer points are covered by dyadic slack cells \(C\), each
with a symmetric displacement polytope \(D_C\) satisfying \(C-C\subseteq D_C\)
and \(C\pm D_C\subseteq P\). There are \((1+2r(M+2))^{n}\) cells, where
\(M\approx\log(\text{max slack})\).

- **Quadratics.** Suppose some integer \(d\in D_C\) has \(d^TQd<0\). The
  reflection identity \(f(x+d)+f(x-d)=2f(x)+2d^TQd\) then shows that no point
  of \(C\) is optimal. Otherwise \(f\) has supporting inequalities between the
  integer points of \(C\). This "lattice hidden convexity" allows exact
  minimization with an integer-query separation oracle (their Thm 3.5,
  credited to Basu and Hildebrand–Göß).
- **Cubics.** The Hessian is affine, so a negative direction gives a linear
  cut valid for every global minimizer in the cell.

The stated limits (2609.18266v2, Thm 1.2 remark and Remark 7.10) are:

- The mixed-integer and unbounded extensions are proved only for quadratics.
- The denominator-scaling reduction needs a constant Hessian. It fails for
  cubics, whose mixed-integer optima can be irrational (Bienstock–Del Pia–Hildebrand).
- For cubics, the right-hand side \(b\) stays in the dimension-dependent
  factor.
- General quartics need a restriction, since they are NP-hard at \(n=2\).

Discarding cells whose slack lies in \((0,1)\) uses integrality of slacks.
This step is what fails when continuous variables are present.

### 1.3 Open questions stated by the authors

- **Ari–Hildebrand, curvature batching §9:**
  1. Finite-value IQP in polynomial time for every fixed \(n\). Now solved by
     2609.18266 and Wei.
  2. The parameterized complexity of bounded IQP at inertia \((1,1,n-2)\),
     and of noncopositivity with a fixed negative index of at least two.
  3. Reducing the MIQP exponent \(O(n^2(q+1)^2)\).
  4. Constants in the recession test.
- **Herrmann §3:** Is IQP FPT in \(n+m\)? (Lokshtanov.) Is IQP polynomial for
  fixed \(n\)? The second is now solved.
- **DHWZ, line 75 of the extraction:** "an open question whether Problem (1)
  can be solved in polynomial time for \(n\ge3\) and \(d\in\{2,3\}\)." What
  remains is \(d=3\) with an unbounded polyhedron, or with mixed-integer
  variables.
- **Hildebrand–Göß §8:**
  - An FPT (rather than XP) bound for reverse-convex IP.
  - A mixed-integer version, listed as future work.
  - A conjecture that closed strictly convex sets can be removed.

### 1.4 Repository overlap check

- `research-20260927/fixed-integer-strong-quartic-fpt.md` and
  `integer-query-convex-oracle-prior.md` already use the Ari–Hildebrand
  Definition 3.4 / Theorem 3.5 interface for strongly convex quartics with a
  fixed number of integer variables.
- The Hessian-span files (`hessian-span-main-results.md`,
  `unbounded-integer-frontier.md`, `nonconvex-hessian-span-frontier.md`)
  treat convex MIQCQP and nonconvex quadratic certificates.
- `two-integer-pell-output-boundary.md` records Pell exponential outputs for
  nonconvex quadratic constraints in two integer variables.
- `results/fixed-parameter-linear-fibers-np-membership.md` is a fixed-parameter
  NP-membership lemma for linear fibers.

None of these treats cubic objectives, unbounded cubic minimization, number
fields, or mixed-integer cubics. Their candidate-list and integer-query
machinery is directly reusable for Q2.

### 1.5 Sources examined

- **arXiv 2609.18266v2:** full text extracted. Checked the abstract, §1–3,
  §6, §7.1–7.4 including Remark 7.10, §8 intro and the references.
- **arXiv 2609.17889:** abstract; confirmed superseded.
- **arXiv 2604.04851v2:** abstract, §1, Table 1, §9 open problems.
- **arXiv 2608.17818v1:** complete text, including the reduction and
  conclusion.
- **arXiv 2409.05308v2:** contents, §1, §3.1 Examples 22–23, Thm 44, §8.
- **arXiv 1408.4711v2 (DHWZ):** abstract; Theorems 1.3 and 1.6, confirmed to
  include unbounded \(P\); the exponential example; the open question at
  line 75.
- **arXiv 2511.02983v2 (Del Pia):** abstract, introduction, Tables 1–2,
  proof of Prop. 2. A grep found no number-field or norm-form discussion.
- **arXiv 2607.29386:** abstract via the arXiv API.
- **Optimization Online `?p=36744` (Wei):** abstract page only.
- **Local literature:**
  - `koppe2012-on-the-complexity-of-nonlinear` §4.1: quadratic Diophantine
    hardness, and the remark that "for indefinite forms nothing seems known"
    as of 2012.
  - `khachiyan2000-...`: Thm 1.1–1.2.
  - `hildebrand2016-...`: abstract and introduction.
  - `pia2023-an-approximation-algorithm-for-indefinite`: introduction and
    Thm 1–2.
  - `bienstock2023-complexity-exactness-and-rationality-in`: abstract, §2.3,
    §5.
  - `herrmann2026-...`: matches the arXiv text.
- **arXiv API title/abstract searches, sorted by date:** "integer cubic",
  "integer quadratic programming", "fixed dimension ∧ quadratic ∧ integer",
  "displacement cover", "mixed-integer cubic", "norm form ∧ integer
  programming". Only the items above were relevant.
- **Web search:** the session's web-search budget ran out before the
  number-theory prior-art queries. Principal-ideal and norm-form connections
  to integer programming were therefore **not** searched on the open web.

## 2. Open questions after the search

An unsuccessful search does not establish novelty.

**Q0 (closed): indefinite or concave quadratic objective over integer points
of an ellipsoid or convex quadratic region.** This is NP-hard in dimension two.
Section 3.1 gives the proof and a one-ellipse strengthening. More broadly, in
fixed dimension, integer points of \(P\cap\{q\le0\}\) with one arbitrary
quadratic \(q\) are polynomial (Ari–Hildebrand, via the epigraph of the IQP
objective). Adding a second quadratic, even a convex one, gives NP-hardness at
\(n=2\). The "one nonconvex quadratic" boundary is sharp. A useful follow-up
along this line must therefore change the model, not merely add an ellipsoid.

**Q1: integer cubic minimization over unbounded rational polyhedra, fixed
\(n\ge3\), finite optimum.**

- *Why it is open:* DHWZ line 75; Ari–Hildebrand Thm 1.2 is restricted to
  bounded polyhedra ("essential to the scope"); Del Pia 2511.02983 gives only
  structural unboundedness certificates.
- *After the first pass:* lower bounds are in hand (Section 3.2). Upper bounds
  remain open:
  - decidability for fixed \(n\);
  - NP membership with succinct (for example power-product) certificates;
  - whether dimension-three instances reduce to unit, PIP, or norm-form
    computations in cubic fields.

**Q2: bounded mixed-integer cubic (or curvature-concave) minimization in fixed
dimension.** Is exact minimization over \(P\cap(\mathbb Z^{n_I}\times\mathbb
R^{n_C})\), \(P\) a polytope, polynomial for fixed \(N\)?

- *Why it is open:* Ari–Hildebrand Remark 7.10 says explicitly that the
  mixed-integer case is not covered and why. Earlier results give an FPTAS
  (De Loera et al.) but no exact algorithm.
- *Special case already covered:* the Ari–Hildebrand denominator scaling
  transfers verbatim when the continuous variables enter with a constant
  \(y\)-Hessian, meaning no monomials \(y_iy_jz_k\) or \(y^3\). Then
  \(t_Sy^*\) is integral and Thm 1.2 applies to the scaled grids. That case
  should be treated as essentially known.

**Q3: parameterized structure of IQP.**
- (a) Is IQP FPT in \(n+m\)? Lokshtanov 2015 asked this; Herrmann 2026 restates
  it. The Ari–Hildebrand bound is XP only through \(\varphi_{A,Q}^{O(n)}\).
  Herrmann's hardness needs \(m=\Theta(k^2n^2)\). The simplest unresolved
  instance is box-constrained IQP parameterized by \(n\).
- (b) Is bounded IQP with inertia \((1,1,n-2)\) FPT in \(n\)? This is from
  Ari–Hildebrand §9.

## 3. First-pass mathematics

### 3.1 Q0 closure: one ellipse suffices for NP-hardness in the plane

**Proposition.** Minimizing a concave quadratic over the integer points of a
single ellipse in \(\mathbb R^2\), with no other constraints, is NP-hard.

*Reduction.* Start from Manders–Adleman AN1: given \((a,b,c)\) with
\(b\nmid a\), is there \(x\in[1,c-1]\) with \(x^2\equiv a\pmod b\)?

1. Put \(c'=c-1\) and \(u=\lceil(a-c'^2)/b\rceil\).
2. Choose an integer \(Y\ge\max(1,(a/b-u)/2)\). Put \(t=-Y-u\) and
   \(N=a+bt\).
3. For integers with \(X^2+by=N\), the condition \(|X|\le c'\) is then
   equivalent to \(y\ge-Y\). Moreover \(y\le N/b\le Y\) holds automatically.
4. The instance is: minimize \(f=N-X^2-by\) (Hessian \(\operatorname{diag}(-2,0)\))
   over integer points of the ellipse
   \(E:\ X^2+by+y^2/(2Y^2)\le N+\tfrac12\) (Hessian positive definite).

*Correctness.*
- On \(E\), \(f\ge y^2/(2Y^2)-\tfrac12>-1\). Since \(f\) is integer-valued at
  integer points, \(f\ge0\).
- \(f=0\) exactly when \(X^2+by=N\) and \(|y|\le Y\). By step 3 this is
  exactly a YES instance.

*Verification.* `check_ellipse_manders_adleman.py` checked all \(2\le b\le35\),
\(1\le a<b\), \(2\le c\le b+2\): 14,875 instances, 4,769 of them YES. In every
case \(\min f=0\) exactly on YES instances, and \(f\ge0\) on the integer points
of \(E\).

The parabola form (convex \(\{y^2\le ax-b\}\) plus a box) is Hildebrand–Göß
Example 22, and Köppe's survey records the same objective-value hardness. Only
the single-ellipse strengthening might be new, and it is minor.

### 3.2 Q1: norm forms make unbounded integer cubics number-theoretic in dimension three

**Setup.** Let \(K\) be a cubic field with one real embedding \(\sigma\) and a
complex pair \(\tau,\bar\tau\).

- Write \(y\in\mathbb Z^3\) for the coordinates of \(\alpha\in\mathcal O_K\)
  in an integral basis.
- The norm form is \(N(y)=\sigma(\alpha)|\tau(\alpha)|^2\in\mathbb Z[y]\), a
  cubic form. The map \(y\mapsto(\sigma,\tau)\in\mathbb R\times\mathbb C\) is
  a linear isomorphism.
- Let \(\tilde d\) be the real direction with \(\tau=0,\sigma>0\). It is
  irrational, and it is an isolated zero of \(N\) (an acnode of the cubic
  curve).
- Let \(Q\) be the rational polyhedral cone
  \(\{\sigma'(y)\ge2(\pm\operatorname{Re}\tau'(y)\pm\operatorname{Im}\tau'(y))\}\),
  with four rows, built from rational approximations \(\sigma',\tau'\). For
  good enough approximations, \(Q\) is pointed, \(Q\setminus0\subseteq\{\sigma>0\}\),
  and \(\tilde d\in\operatorname{int}Q\).
- Let \(\ell\) be an integral linear form that is positive on \(Q\setminus0\).

**Facts.**
1. On lattice points of \(Q\setminus0\), \(N\ge1\).
2. For a nonzero ideal \(I\) and \(\alpha\in I\), \(\operatorname{Norm}(I)\)
   divides \(N(\alpha)\).
3. For a unit \(\varepsilon\) with \(\sigma(\varepsilon)>1\) (rank-one unit
   group), \(|\tau(\varepsilon)|=\sigma(\varepsilon)^{-1/2}<1\). Hence
   \(\pm\alpha\varepsilon^k\to\tilde d\) in direction, so every nonzero
   \(\alpha\) has a unit multiple in \(\operatorname{int}Q\).

**Theorem A (sketch, unreviewed).** Let
\(\mu(I)=\min\{N(y):y\in I\cap Q,\ \ell(y)\ge1\}\), with \(I=B\mathbb Z^3\)
substituted as \(y=Bw\). This is a 3-variable integer cubic minimization over
a rational polyhedron. Then:
- \(\mu(I)\ge\operatorname{Norm}(I)\), and the minimum is attained;
- \(\mu(I)=\operatorname{Norm}(I)\) if and only if \(I\) is principal.

*Proof.*
- If \(I=(\alpha)\), a unit multiple \(\pm\alpha\varepsilon^k\) lies in \(Q\)
  and has norm \(\operatorname{Norm}(I)\).
- Conversely, \(N(y)=\operatorname{Norm}(I)\) with \(y\in I\) gives
  \((y)\subseteq I\) with equal norm, so \((y)=I\).
- The construction is polynomial in the field and ideal input.

Consequences:
- The threshold problem for integer cubic minimization over rational
  polyhedra in \(\mathbb R^3\) is at least as hard as the PIP for complex cubic
  fields, even with a homogeneous objective and a simplicial cone plus one row.
- To my knowledge, no classical polynomial-time PIP algorithm is known. The
  best known methods are subexponential under GRH (Buchmann), and quantum
  polynomial for fixed degree (Hallgren; Schmidt–Vollmer). These attributions
  come from memory and still need a source check.
- PIP has compact certificates in fixed degree, as I recall (Thiel), so this
  is number-theoretic hardness, not NP-hardness.
- For fixed \(K\) the PIP is easy. The hardness uses fields that vary with the
  input.

**Theorem B (unconditional exponential size, sketch).**
- Take \(K=\mathbb Q(\sqrt[3]2)\), \(\varepsilon=1+\theta+\theta^2\) (norm 1,
  \(\sigma(\varepsilon)\approx3.85\)), and a prime \(p\ge5\).
- Minimize \(N(e_1+p^jw)\) over \(w\in\mathbb Z^3\) with \(e_1+p^jw\in Q\).
  This is dimension three, with input length \(O(j\log p)\).
- Norms of points \(\equiv1\pmod{p^j}\) are \(\equiv1\), and \(N\ge1\) on
  \(Q\). So the minimum is 1, and the minimizers are exactly the units
  \(\varepsilon^k\), \(k\ge1\), with \(\varepsilon^k\equiv1\pmod{p^j}\).
- By the binomial lifting-the-exponent argument,
  \(\operatorname{ord}_{p^j}(\varepsilon)=\operatorname{ord}_{p^t}(\varepsilon)\,p^{j-t}\).
- Hence every optimal solution has at least
  \(\approx p^{j-t}\log_2 3.85\) bits: exponential in the input length.

This contrasts with MIQP, where polynomial-size optima exist
(Del Pia–Dey–Molinaro; Ari–Hildebrand), and with \(n=2\) cubics (DHWZ,
polynomial). **Dimension three is therefore the threshold for exponential
cubic optima.** The quartic Pell example of DHWZ needs degree four.

**Verification (targeted; PARI/GP via `cypari2`, installed with pip into the
user Python for this check):**

- `check_pip_cubic_cone.py` enumerates every lattice point of \(I\cap Q\) with
  \(1\le c\le C_{\max}\). It asserts that \(N>0\) and
  \(\operatorname{Norm}(I)\mid N\) at every point, and that the extreme rays
  of \(Q\) satisfy \(\sigma>0\) and \(c>0\). Results:
  - \(\mathbb Q(\sqrt[3]2)\): \(\mathcal O_K\) gives \(\min=1\) at \((1,1,1)\);
    the ideal \((3+\theta^2)\) gives 31.
  - \(\mathbb Q(\sqrt[3]{11})\), \(h=2\):
    - \(\mathcal O_K\): min 1 at the unit \((89,40,18)\).
    - \((2+\theta)\): 19.
    - \(P_3\), principal: 3.
    - \(P_2^2\), principal: 4.
    - \(P_2\), non-principal: **4 > 2**.
    - \(P_5\), non-principal: **10 > 5**.

  The minimum equals \(\operatorname{Norm}(I)\) exactly for the principal
  ideals.
- `check_unit_congruence_growth.py`: \(\operatorname{ord}_{p^j}(\varepsilon)\)
  for \(p=5\) is \(8,40,200,1000,5000\); for \(p=7\) it is
  \(19,133,931,6517,45619\). The ratio is exactly \(p\) at each level.

**What remains for Q1.**
- Upper bounds:
  - Is the dimension-three threshold problem in NP with compact
    representations?
  - Is it decidable for every fixed \(n\)?
  - Can Del Pia's thin-ray analysis plus norm-form structure classify all
    finite-value instances?
- The classification of cubic forms that are nonnegative on a rational cone
  and have irrational zeros. In \(\mathbb R^3\) these zeros appear to be
  exactly acnodes from complex cubic fields. In \(\mathbb R^2\) they are
  impossible, which is consistent with DHWZ.
- An independent review of Theorems A–B.
- A number-theory prior-art check. The link between norm forms, PIP, and
  lattice minimization is classical in computational number theory. The
  optimization-side statement may be folklore there.

### 3.3 Q2 attack plan: bounded mixed-integer cubic in fixed dimension

The Ari–Hildebrand certificate idea appears to survive continuous variables
if the cells are refined to scales \(2^{-K}\).

1. **Algebraic slack gap (key new lemma).** For a polytope and a cubic \(f\)
   in fixed \(N\), show that some global optimizer \(x^*\) has every nonzero
   row slack at least \(2^{-K}\), with \(K=\mathrm{poly}(\varphi)\). Take
   \(z^*\) optimal. Pick a fiber minimizer on the smallest face containing
   one. Use fixed-dimension real-algebraic separation bounds and a
   Hoffman-type bound for inactive rows.
2. **Refined dyadic cells in \(\mathbb R^N\).** Use slack levels
   \(0,2^{-K},\dots,2^{M}\) and discard \((0,2^{-K})\). This gives at most
   \((1+4r(M+K+2))^N\) cells, and \(C-C\subseteq D_C\), \(C\pm D_C\subseteq P\)
   holds for real points exactly as in their Theorem 2.2.
3. **Mixed admissibility.** Let
   \(A_C=\{x\in\bar C:v^TH(x)v\ge0\ \forall v\in D_C\cap(\mathbb Z^{n_I}\times\mathbb R^{n_C})\}\).
   - It is convex, being an intersection of halfspaces, and contains
     \(x^*\) by the reflection identity for real \(v\).
   - Its separation oracle is a homogeneous MIQP in fixed dimension, which
     Ari–Hildebrand Thm 1.1 solves with a rational witness.
4. **Mixed supporting inequalities.** Their Lemma 7.1 holds for real
   displacements. For mixed points \(x_1,x_2\in A_C\):
   - \(f(x_2)\ge f(x_1)+\nabla f(x_1)^T(x_2-x_1)\);
   - the slices \(f(z,\cdot)\) are convex on \(A_C\);
   - with KKT multipliers of the linear rows of \(A_C\), the slice-minimum
     function \(g(z)\) gets the cut
     \(g(z)\ge g(z_0)+(\nabla_zf+\sum\lambda_ia_{i,z})^T(z-z_0)\);
   - integer points of \(\operatorname{conv}\{z:g(z)\le\tau\}\) are exactly the
     good \(z\) (averaging argument).
5. **Exact optimization over \(z\).** Use Basu-style candidate retention with
   the repository's "cuts preserving strictly better points" (fixed-integer
   quartic note), without bisection. Handle algebraic \(\gamma\) with rational
   approximations inside a root-separation margin. Finish with exact
   algebraic comparisons of the candidates.

*Risks:*
- Step 5 needs slice minima and multipliers of a semi-infinite convex program
  to \(2^{-\mathrm{poly}}\) accuracy. Its active constraints come from an MIQP
  oracle that requires rational queries, so approximate admissibility and an
  error-tolerant supporting inequality are needed.
- Step 1 needs a careful quantitative citation.
- **Scoop risk is high.** The authors named this exact gap.
- *Estimate:* 2–4 weeks for a careful proof. Success probability about 50%.
  The main uncertainty is exactness bookkeeping, not the core identities.

### 3.4 Q3

No progress was attempted. Two structural observations:

- Herrmann-type reductions need many rows. With \(m\) fixed, the only non-FPT
  factor in Ari–Hildebrand is \(\varphi_{A,Q}^{O(n)}\), which comes from the
  dyadic depth.
- Proving W[1]-hardness in \(n+m\) would need number-theoretic encodings with
  large coefficients. An FPT algorithm would need a Lenstra-style replacement
  for the dyadic cells.

Feasibility looks low.

## 4. Significance

**Proved or near-proved (Section 3, pending review):**

- *The Q0 boundary.* Fixed-dimension polynomiality stops exactly at one
  nonconvex quadratic. A nonconvex objective with a single convex ellipsoid is
  already NP-hard with two integer variables.
- *Theorems A–B.* In fixed dimension, bounded cubic is polynomial
  (Ari–Hildebrand) and unbounded cubic in the plane is polynomial (DHWZ). In
  dimension three, the unbounded case has exponential-size optima and is
  PIP-hard. The degree-by-dimension classification is thus complete up to
  number-theoretic hardness.
- *Contrast with quadratics.* Quadratic minimization is polynomial on
  unbounded polyhedra and has small optimal solutions, so this contrast is new
  in kind.

**Plausible solver relevance (indirect, modest):**

- Finite bounds on general-integer variables are essential, not cosmetic, for
  exact cubic MINLP theory from three variables on. Unbounded cubic presolve
  or unboundedness logic must handle Diophantine phenomena.
- The reflection rule could give valid disjunctions for B&B on
  general-integer nonconvex MIQPs:
  - For integer \(d\) with \(d^TQd<0\), every optimum has
    \(x+d\notin P\) or \(x-d\notin P\).
  - On boxes: some \(j\) has \(x_j<l_j+|d_j|\) or \(x_j>u_j-|d_j|\).
  - The rule is useless for binaries and needs a computational test.
- Surviving cells admit nonconvex outer-approximation (OA) cuts that are valid
  on integer points.

**Speculative:**

- An exact mixed-integer cubic algorithm (Q2) would complete the
  fixed-dimension theory. It has no foreseeable solver impact: the
  dependence \(2^{O(N\log N)}\varphi^{O(N)}\) is prohibitive, and structured
  MINLPs are not fixed-dimensional.

For practical value, the missing pieces are empirical evidence that
reflection disjunctions prune real general-integer MIQP instances
(QPLIB-like), and an implementation of cheap negative-displacement search on
small boxes.

## 5. Recommendation

**Score: 4/10** (significance 3, feasibility 7, originality 6).

This area has just been largely settled for quadratics by Ari–Hildebrand and
Wei, and the most prominent next question (mixed-integer cubic) is named by
the same active group. It is pure complexity theory with weak routes to better
solvers, so it should not be a main direction.

The cheap, high-yield item is a short note on Theorems A–B. That note should
include:
- the norm-form cone;
- PIP-hardness and unconditional exponential-size optima for 3-variable
  integer cubic minimization over unbounded polyhedra, which settles the
  hardness side of the DHWZ \(n\ge3,d=3\) question;
- an independent proof review;
- a computational-number-theory prior-art audit, since the web search budget
  was exhausted.

Q2 is worth pursuing only if a fixed-dimension paper is wanted, and quickly,
given the scoop risk.

## Commands run (targeted checks only)

- `python3 check_ellipse_manders_adleman.py`: PASS, 14,875 instances.
- `python3 check_pip_cubic_cone.py`: PASS. It covers \(m=2\) with two ideals
  and \(m=11\) with six ideals. One unoptimized first version was stopped
  after exceeding the time limit.
- `python3 check_unit_congruence_growth.py`: PASS; ratios exactly \(p\).
- Source extraction: `curl` of arXiv HTML/PDF plus `html2txt.py` and
  `pdftotext`; arXiv API queries.
- `pip install cypari2` added PARI/GP to the user Python environment. This
  changed the local environment outside the repository.

No project-wide checks were run and CI was not inspected.
