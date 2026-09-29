# Scout report: mixed-integer centerpoints and information complexity

Date: 2026-09-28. Area: `mi-centerpoints`. Status: scouting only. The
new-looking statements in Section 3 have complete short proofs and targeted
numerical checks. They have not had independent review. Novelty is not
established: an unsuccessful search does not show that a result is new.

Scratch files are in `research-20260928b/scouting/mi-centerpoints/`:
PDFs and text extractions of the sources in `src/`, the depth code
`midepth.py`, and the check scripts and logs listed in Section 3.5.

## 0. Summary

- **Oertel's conjecture is still open as of September 2026.** Two 2026 papers
  (Cristi–Salas, v4 of July 2026, and Cheng–Basu, February 2026) prove it only
  for "wide" sets. Cheng–Basu write that the general case "seems to require
  fundamentally new ideas". The same holds for the information-complexity gap
  that the conjecture would close.
- **New-looking result for one integer variable (n = 1).** For every convex
  body \(C\subset\mathbb R^{1+d}\), some point of \(S=C\cap(\mathbb Z\times\mathbb R^d)\)
  has halfspace depth at least
  \(\tfrac{1}{2(1+e)}\big(\tfrac{d}{d+1}\big)^d\nu(S)\ge 0.049\,\nu(S)\). This constant
  does not depend on d. The previous general bound was
  \(\nu(S)/(2(d+1))\). The query point is explicit: it needs only the fiber
  volumes and the centroids of two fibers. The proof combines a
  Brunn–Minkowski concavity of fiber depth, a "lifting lemma", and a discrete
  layer-cake inequality (Section 3). Numerically, the best constant from this
  argument is about \(g_d/(2e)\ge 0.068\).
- **Consequence (proved, modulo the paper's model assumptions).** With one
  integer variable, the full-information first-order information complexity of
  mixed-integer convex optimization becomes
  \(\Theta\big(d\log\frac{MR}{\min\{\rho,1\}\varepsilon}\big)\). The previous upper
  bound was \(O(d^2\log\cdot)\). This closes the n = 1 case of the
  first-order query-count gap in open question 2 of Basu's survey (the
  response-size and other-oracle parts of that question are untouched).
- **Easy side result.** The strong conjecture holds for every n and d when
  each fiber is centrally symmetric about an affine function of z, for example
  when C is invariant under \((z,x)\mapsto(z,-x)\).
- **No counterexample in the smallest open case (n = 1, d = 2).** Searches over
  random and adversarial 3–5-fiber sets never went below the conjectured
  \(2/9\). The optimizer always drifted toward the known 2-fiber extremal
  \(\{0,1\}\times\text{triangle}\).
- **Practical MINLP significance is low.** Resolving the conjecture would
  change worst-case oracle-call counts by a factor of about d. No solver uses
  mixed-integer centerpoint cutting planes. Computing such points is itself
  hard for general n. The value is in complexity theory and discrete convex
  geometry.
- **Score: 3/10** under the brief's significance × feasibility × originality
  criterion. The n = 1 result is cheap to write up as a short note after an
  independent check. The general question is hard and has little solver payoff.

## 1. Frontier map

Notation: \(S=C\cap(\mathbb Z^n\times\mathbb R^d)\) for a convex body C;
\(\nu\) is the mixed-integer volume (the sum of the d-dimensional volumes of
the integer fibers); \(h_S(x)=\inf\{\nu(S\cap H): H \text{ a closed halfspace},\ x\in H\}\);
\(F(S)=\max_{x\in S}h_S(x)/\nu(S)\) (the "Oertel radius");
\(g_d=(d/(d+1))^d\in(1/e,1]\).

### 1.1 Conjecture and bounds

| Statement | Source | What was checked |
|---|---|---|
| Helly-type bound \(F(S)\ge 1/(2^n(d+1))\) for every convex body; \(F\ge g_d\) when n = 0 (Grünbaum) | Basu survey arXiv 2110.06172, Thm 4.5 (`/tmp/basu_survey.txt` lines 640–660); Basu–Oertel arXiv 1511.08609 Cor. 16 (`src/plain_1511.txt` l. 820) | Exact form confirmed: \(1/(2^n(d+1))\). It comes from the Helly number \(2^n(d+1)\) of \(\mathbb Z^n\times\mathbb R^d\). |
| **Strong conjecture** (Oertel thesis Conj. 4.1.20 = Basu–Oertel Conj. 17 = survey Conj. 4.6): \(F(S)\ge 2^{-n}g_d\) | same | Tight for \(\{0,1\}^n\times\Delta_d\). Known cases: n = 0 (Grünbaum), d = 0 (Doignon, \(2^{-n}\)), and **d = 1**, where \(2^{-n}g_1=2^{-n}/2\) equals the Helly bound (also noted by Cristi–Salas, l. 170). The smallest open case is **(n, d) = (1, 2)**: \(2/9\) is conjectured and \(1/6\) is known. |
| **Weak conjecture** \(F(S)\ge 2^{-n}/e\) | Cheng–Basu arXiv 2603.00286 Conj. 2.3; Cristi–Salas arXiv 2411.11864 abstract | This is the form stated in the 2024–2026 papers. For complexity purposes, any d-independent \(c\,2^{-n}\) suffices. |
| "Thin" case: at most \(C^n\) nonempty fibers gives \(F\ge g_d/C^n\), so the strong conjecture holds with at most \(2^n\) fibers | Basu–Oertel Remark 19 (l. 888–900) | Checked. For n = 1 this means the 2-fiber case is settled. |
| Wide case I: lattice width of \(\mathrm{proj}_{\mathbb R^n}C\ge 2cn(n+d)^{5/2}\alpha n^{n+1}\) gives \(F\ge e^{-1/c-1}+e^{-2/c}-1\) | Basu–Oertel Thm 18 (Cristi–Salas Thm 1.1) | Threshold is exponential in n. |
| Wide case II: the projection contains a Euclidean ball of radius \(\ge\alpha d^2n^{3/2}\) (1178 is the constant quoted by Cheng–Basu); lattice-width version \(\ge\alpha' d^2 n^5\); **n = 1: width \(\ge\alpha'' d\) suffices for the strong form** | Cristi–Salas, IPCO 2025; Math. Program. 2026 (DOI 10.1007/s10107-026-02391-9); arXiv v4 of 9 Jul 2026 | Read the abstract, intro, the n = 1 section (Thm 3.4) and the partial-results paragraph. They still describe the conjecture as open. |
| Wide case III: the projection contains \(z_0+kB_\infty^n\) with \(k\ge\frac{3e}{2}(n+d)\), giving \(h\ge(1/e-3(n+d)/(2k))\nu\); if \(k\ge 3e(n+d)\) then \(F\ge 1/(2e)\). **Sharpness:** no \(k=o(n+d)\) threshold alone gives a dimension-free constant (Thm 5.1 and Cor. 5.2; the construction needs \(n\ge 2\) and \(n\) growing) | Cheng–Basu arXiv 2603.00286v1 (27 Feb 2026) | Read in full (`src/plain_2603.txt`). Conclusion: "the conjecture remains open in its full generality … seems to require fundamentally new ideas". It also asks for a poly-time constant-fraction cutting-plane step. |

### 1.2 Information complexity (full-information first-order oracle, class \(I_{n,d,R,\rho,M}\))

| Bound | Source |
|---|---|
| Upper \(O(2^n d(n+d)\log\frac{MR}{\min\{\rho,1\}\varepsilon})\): centerpoint cutting planes at depth \(1/(2^n(d+1))\) | Oertel thesis; Basu–Oertel Thm 6; Basu–Jiang–Kerger–Molinaro, Math. Program. 210 (2025), Table 1 and Thm 28 (local `literature/papers/basu2025-information-complexity-of-mixed-integer/fulltext.md` l. 124, 650) |
| Lower \(\Omega(2^n d\log\frac{MR}{\min\{\rho,1\}\varepsilon})\) (Cor. 8, obtained by transfer); older \(\Omega(2^n d\log(R/\rho))\) | same, l. 144; survey §4.1 |
| Remaining gap is a factor linear in dimension. Basu et al. state that the convex-geometry conjecture "would resolve this" | same, l. 214 |
| Bit and inner-product oracles: lower \(\Omega(2^n d^2\log\cdot)\), upper \(O(2^n d(n+d)^2\log^2\cdot)\) | Basu–Kerger–Molinaro arXiv 2511.02082 (v2, Jul 2026) |
| Function-value-only oracle: \(\tilde\Omega(2^n d^2)\) | Kerger arXiv 2607.13335 (Jul 2026), abstract only |

Survey open question 2 (Basu, arXiv 2110.06172 §6) asks to close the n, d ≥ 1
gap and calls Conjecture 4.6 "a very interesting question in pure
convex/discrete geometry".

### 1.3 Other sources examined

- arXiv 2607.02400 (Brandenburg–De Loera–Meroni, Jul 2026): exact
  semialgebraic algorithms for centerpoints of polytopal measures in fixed
  dimension. Abstract only. It could serve as a tool for exact
  small-dimension computation; it does not cover mixed-integer measures.
- arXiv 2411.01482 (Gupta–Narayanan): approximating halfspace depth in a
  convex body. Abstract only. Not mixed-integer.
- arXiv 2608.01721 (Jiao–Zhu) and 2606.19865 (Wang–Xiong–Yang): barycentric
  sections (Grünbaum–Loewner problems). Checked; not relevant.
- arXiv 1711.00998 ("Grünbaum's inequality for sections"). Seen in search
  results only; not read. It is related to the fiber-depth lemma below.
- Oertel's ETH thesis (2014): **not examined.** The ETH Research Collection
  blocked access. Its content on the conjecture (Thm 4.1.19 = Helly bound,
  Conj. 4.1.20) is known only from Cristi–Salas and Basu–Oertel. It may
  contain unlisted partial results.
- Repository: `literature/topics/complexity-and-tractability.md` and
  `literature/index.md` contain only the Basu et al. 2025 entry. No other local
  paper treats centerpoints.
- Web searches used: Basu–Oertel centerpoints; mixed-integer centerpoint
  conjecture; discrete Grünbaum lattice; "Oertel's conjecture" 2026;
  mixed-integer halfspace depth 2025; information complexity 2025–2026. The
  web-search budget ran out before searches for "Helly number mixed integer
  quantitative" and the Oertel thesis could run, so those were not done.

## 2. Open questions (after the search)

Q1. **Case n = 1.** Is \(F(S)\ge\frac12 g_d\) (strong), or at least
\(\ge\frac1{2e}\) (weak), for every convex body \(C\subset\mathbb R^{1+d}\)?
Evidence that it is open: both 2026 papers call the conjecture open. The
n = 1 results known before this report need width \(\ge\alpha d\)
(Cristi–Salas) or \(\ge 3e(1+d)\) (Cheng–Basu, weak form), or at most 2 fibers.
Section 3 proves a d-independent constant \(g_d/(2(1+e))\), a factor
\(1+e\) below the strong form.

Q2. **Fixed n ≥ 2, d-independent constant.** Is there \(c_n>0\) with
\(F(S)\ge c_n\) for all d and C? This is equivalent in effect to
\(\mathrm{icomp}=\Theta_n(d\log\cdot)\) for each fixed n. Evidence that it is
open: every known bound for n ≥ 2 either decays like 1/d or needs width
growing with d. Cheng–Basu Cor. 5.2 rules out width-only hypotheses with
sublinear width, but their construction has n growing, so it does not refute
Q2.

Q3. **Uniform version.** Is \(F(S)\ge c\,2^{-n}\) with an absolute c? This
would give the upper bound \(O(2^n(n+d)\log\cdot)\) and close the linear gap
whenever \(d\gtrsim n\). Stated as open in Basu et al. 2025 and in
Cheng–Basu 2026.

Q4. **Algorithmic.** Is there a poly-time computable query point that removes
a constant fraction of mixed-integer volume (Cheng–Basu's closing question)?
For n = 1, the point of Theorem C needs only fiber volumes and two fiber
centroids, which randomized volume algorithms approximate. A full check of the
robustness and of the pseudo-polynomial number of fibers remains to be done.
General n is open.

## 3. Best question, first-pass progress, and attack plan

### 3.1 Lemmas (all n, d ≥ 1)

For \((z,x)\in C\) define the **fiber depth**
\(D(z,x)=\inf_{a\ne 0}\mathrm{vol}_d\big(C_z\cap\{w: a\cdot w\ge a\cdot x\}\big)\),
where \(C_z\) is the fiber at \(z\in\mathbb R^n\). The value is unnormalized,
and D = 0 outside C.

**Lemma A (concavity).** \(G=D^{1/d}\) is concave on C.
*Proof.* Take \((z_i,x_i)\in C\), \(\lambda\in[0,1]\) and a unit vector a. Let
\(A_i=C_{z_i}\cap\{a\cdot w\ge a\cdot x_i\}\); each is nonempty and compact.
Convexity of C gives \((1-\lambda)A_0+\lambda A_1\subseteq C_{z_\lambda}\cap\{a\cdot w\ge a\cdot x_\lambda\}\).
Brunn–Minkowski then gives \(\mathrm{vol}^{1/d}\ge(1-\lambda)G(z_0,x_0)+\lambda G(z_1,x_1)\).
Take the infimum over a. ∎
This is likely folklore; it generalizes the concavity of \(\mathrm{vol}(C_z)^{1/d}\).

**Lemma B (lifting).** Let \(x_z\in C_z\) be any selection over
\(z\in\mathbb Z^n\cap\mathrm{proj}\,C\), and let k be a lattice point. Every
closed halfspace H containing \((k,x_k)\) satisfies
\(\nu(S\cap H)\ge\sum_{z:(z,x_z)\in H}D(z,x_z)\).
*Proof.* Write \(H=\{b\cdot z+a\cdot w\ge c\}\). If \((z,x_z)\in H\), then the
fiber section \(H_z=\{w: a\cdot w\ge c-b\cdot z\}\) contains \(x_z\), so
\(H_z\supseteq\{a\cdot w\ge a\cdot x_z\}\), or \(H_z=\mathbb R^d\) if a = 0.
Hence \(\mathrm{vol}(C_z\cap H_z)\ge D(z,x_z)\). ∎
For an affine selection \(x_z=\ell(z)\), the right side is at least the
lattice Tukey depth of k in \(\mathbb Z^n\) under the weights
\(\omega(z)=D(z,\ell(z))\). By the Doignon–Helly argument, some k has depth
\(\ge 2^{-n}\sum_z\omega(z)\).

**Corollary (easy).** Suppose every fiber \(C_z\) is centrally symmetric about
\(\ell(z)\), with ℓ affine; this holds, for example, when C is invariant under
\((z,x)\mapsto(z,-x)\). Then \(\omega=\mathrm{vol}(C_z)/2\), so
\(F(S)\ge 2^{-n-1}\ge 2^{-n}g_d\) and the strong conjecture holds. The same
argument works whenever the fiber centroids depend affinely on z. (This covers
the bodies in the Cheng–Basu sharpness construction.)

### 3.2 Theorem C (n = 1)

Let \(V_j=\mathrm{vol}_d(C_j)\) for \(j\in\mathbb Z\) and \(N(\sigma)=\#\{j: V_j\ge\sigma\}\).
Choose \(\sigma^*\) to maximize \(\sigma\lceil N(\sigma)/2\rceil\). Because
\(V^{1/d}\) is concave, \(\{j:V_j\ge\sigma^*\}=\{a,\dots,b\}\) is an integer
interval. Let \(k=\lfloor(a+b)/2\rfloor\), and let y be the point at level k on
the segment joining \((a,c(C_a))\) and \((b,c(C_b))\), where \(c(\cdot)\)
denotes the centroid. Then
\[
h_S(k,y)\ \ge\ g_d\,\sigma^*\lceil N(\sigma^*)/2\rceil\ \ge\ \frac{g_d}{2(1+e)}\,\nu(S),
\qquad\text{so}\qquad F(S)\ge\max\Big\{\frac1{2(d+1)},\ \frac{g_d}{2(1+e)}\Big\}\ge\frac{1}{2e(1+e)}\approx0.0495 .
\]
*Proof.*
1. Grünbaum gives \(D(j,c(C_j))\ge g_dV_j\ge g_d\sigma^*\) at \(j=a,b\).
2. By Lemma A, \(D(j,\ell(j))\ge g_d\sigma^*\) for every integer j in
   \([a,b]\) along the segment ℓ.
3. Apply Lemma B with this affine selection on \([a,b]\). The selection may
   be arbitrary elsewhere, since weights there are ≥ 0. For n = 1 a
   "halfspace" of \(\mathbb Z\) through k is \(\{j\ge k\}\) or \(\{j\le k\}\),
   and each contains at least \(\lceil N/2\rceil\) indices of \([a,b]\).
4. The last inequality is Lemma D applied to the log-concave sequence
   \((V_j)\). ∎

The first inequality is tight for \(\{0,1\}\times\Delta_d\), where it gives
\(g_d/2\).

**Lemma D (discrete layer cake).** For every finitely supported log-concave
sequence \(V_j\ge0\),
\(\sum_jV_j\le 2(1+e)\max_\sigma\sigma\lceil N(\sigma)/2\rceil\).
*Proof.* Normalize \(\max V=1\) and set \(g_j=-\log V_j\), a convex sequence.
Let g also denote its piecewise-linear interpolation. The sublevel set
\(\{g\le u\}\) is an interval of length \(n(u)\), and n is concave and
nondecreasing on \([0,\infty)\). Also \(N(e^{-u})\) counts the integers in
that interval, so \(n(u)-1\le N(e^{-u})\le n(u)+1\). Then
\[
\sum_jV_j=\int_0^\infty e^{-u}N(e^{-u})\,du\le1+\int_0^\infty e^{-u}n(u)\,du\le1+n(1).
\]
The last step uses a supergradient at \(u=1\) and
\(\int_0^\infty e^{-u}(u-1)\,du=0\). So \(\sum_jV_j\le2+N(e^{-1})\). Finally,
\(\max_\sigma\sigma\lceil N/2\rceil\ge\max\{1,\,N(e^{-1})/(2e)\}\). ∎

The sharp constant appears to be \(2e\): the continuous analogue gives
exactly \(2e\), and the search in `kappa.py` found 5.399 against
\(2e=5.437\). With \(2e\) the bound would be \(F\ge g_d/(2e)\ge 1/(2e^2)\approx0.068\).
Using only 1/d-concavity, the numerical worst ratios \(\kappa_d\) are
3.99, 4.48, 4.94, 5.14, 5.25 and 5.33 for d = 1, 2, 5, 10, 20, 50. The bound
\(g_d/\kappa_d\) beats Helly from about d = 6. With the rigorous constant
\(2(1+e)\) it beats Helly for d ≥ 9. For small d, Helly remains better.

**Corollary E (information complexity, n = 1).** Theorem 28 and Algorithm 1
of Basu et al. (2025) use only the depth guarantee of the query point.
Substituting the constant depth fraction \(c=1/(2e(1+e))\) for
\(1/(2(d+1))\) gives \(O\big(c^{-1}(1+d)\log\frac{MR}{\min\{\rho,1\}\varepsilon}\big)\)
queries. With Cor. 8 of that paper, this yields
\(\mathrm{icomp}_\varepsilon(I_{1,d,R,\rho,M})=\Theta\big(d\log\frac{MR}{\min\{\rho,1\}\varepsilon}\big)\).
Plausibly the same substitution improves the n = 1 bit/inner-product upper
bound to \(\tilde O(d^2)\), which would match Basu–Kerger–Molinaro's
\(\Omega(d^2)\) up to logarithms. This needs a check that the
approximate-cut analysis (their Thm 10) uses only the depth.

### 3.3 Why this does not extend directly to n ≥ 2 (Q2)

The n = 1 proof needs an affine selection through the convex superlevel set
\(W^\tau=\{D\ge\tau\}\) over all lattice points of its projection. For n = 1 a
segment always works. For n ≥ 2 it can fail. Take small fibers at the four
corners of a unit square with \(x_{00}+x_{11}\ne x_{01}+x_{10}\): no affine
map passes through all four. Non-affine selections lift to points in convex
position, which a halfspace can isolate.

### 3.4 Attack plan and difficulty

1. **Q1, improve the n = 1 constant toward \(g_d/2\).** Lemma B discards the
   far side of the rotated halfspace. A refined version would count the
   "rotation gain": the far side grows when the adversary tilts the
   hyperplane to kill the near side. That gain is large for exactly the
   geometric profiles that make Lemma D tight. For wide sets (width
   \(\ge 3e(1+d)\)), combine with Cheng–Basu, which leaves O(d) fibers. The
   d = 2 numerics suggest the worst case is the 2-fiber degeneration, so a
   proof might reduce to "a third fiber never hurts". Difficulty: moderate for
   the weak form \(1/(2e)\), high for the exact \(g_d/2\).
2. **Q2, fixed n ≥ 2.** Twisting (the 4-corner obstruction) forces central
   fibers to be large. For a \(3\times3\) lattice patch, the center fiber
   contains the midpoints of all opposite pairs. Try a dichotomy: either an
   approximately affine selection exists over a positive fraction of the
   lattice points of \(\mathrm{proj}\,W^\tau\), or the central fibers carry
   enough depth on their own. Combine it with flatness (few lattice
   hyperplanes) and with Cheng–Basu for fat projections. Difficulty: high.
   A d-independent \(c_n\), even one exponentially small in n, would give
   \(\Theta_n(d\log\cdot)\) for every fixed n.
3. **Q3** needs \(c_n\ge c\,2^{-n}\). This is the full weak conjecture; the
   risk is very high.

### 3.5 Computations (targeted; d = 2, n = 1)

Code: `mi-centerpoints/midepth.py`. It computes the exact area of a polygon
cut by a halfplane, the depth of \((k,y)\) by minimizing over a grid of
normals (\(\theta\), b) plus local Nelder–Mead refinement, including the
\(b\to\pm\infty\) limits and horizontal halfspaces, and maximizes over y by
Nelder–Mead in each fiber. The computed depth is an upper bound up to
refinement error, and the maximization over y can miss the global maximum.
These are therefore evidence, not certificates.

- `test_basic.py`: \(\{0,1\}\times\)triangle gives 0.22222 (= 2/9, exact);
  one triangle and a 3-layer prism give 0.44444.
- `search_random.py 340`: random hulls with 3–5 integer fibers. Minimum
  0.2309, 1% quantile 0.243, median 0.372. All near-minimal instances are
  2-fiber degenerations with other fibers ≤ 0.13% of ν (`inspect_seed.py`).
- `adversarial.py` ((1+34) evolution strategy, each fiber holding at least
  the given share of ν):

  | fibers | minimum share | best F |
  |---|---|---|
  | 3 | 0.20 | 0.3615 (0.3615 on the fine grid; shares 0.406/0.394/0.200) |
  | 3 | 0.05 | 0.2423 (shares 0.545/0.405/0.050) |
  | 4 | 0.10 | 0.2890 (shares 0.105/0.383/0.413/0.100) |

  The share constraint was binding in every run, so the optimizer pushes
  toward 2 fibers. No value below 2/9 was found.
- `check_line_lemma.py`: 400 random instances. The guarantee
  \(\tau\lceil N/2\rceil\) from the max-depth-point variant held up to
  \(4\times10^{-5}\) relative grid error. Minimum guaranteed fraction 0.162.
- `check_theorem_c.py`: 150 random instances. The explicit point of Theorem C
  had no violations; the minimum actual/guaranteed ratio was 1.0005, so the
  bound is nearly attained. The minimum guaranteed fraction was 0.158.
- `kappa.py`: the numerical \(\kappa_d\) values quoted in Section 3.2.

All commands were run locally in the scratch directory. No project-wide
checks were run.

## 4. Significance

**Proved (Section 3, pending independent review).**
- For n = 1 and every convex body \(C\), \(F(S)\ge 0.049\). This is the first
  d-independent bound for mixed-integer depth that does not need a width
  assumption, for any \(n\ge1\), as far as the search found.
- With one integer variable, first-order information complexity is
  \(\Theta(d\log\frac{MR}{\min\{\rho,1\}\varepsilon})\). This closes the
  n = 1 case of the query-count gap in the survey's open question 2.
- The strong conjecture holds for fiberwise-symmetric families.

**Plausible.**
- The n = 1 bit-oracle upper bound improves to \(\tilde O(d^2)\), which would
  be tight.
- The n = 1 query point is computable in randomized polynomial time from
  approximate volumes and centroids (Q4 for n = 1).

**Speculative, or low value for solvers.**
- MINLP solvers (outer approximation, extended cutting plane, NLP-based
  branch and bound, spatial branch and bound) do not use mixed-integer
  centerpoints. Their iteration counts depend on MILP master solves, not on
  oracle-query lower bounds.
- A full resolution changes worst-case query counts by a factor of about d
  inside a bound already exponential in n. Computing mixed-integer
  centerpoints requires solving mixed-integer subproblems (Basu–Oertel give
  fixed-dimension algorithms only).
- The honest assessment: this is discrete and convex geometry with a clean
  complexity-theoretic consequence. A route from it to better solvers is not
  visible. For practical value one would need (i) cheap approximate
  mixed-integer centerpoints and (ii) evidence that volume-reduction cutting
  planes beat outer approximation on some instance class. Neither is on the
  horizon.

## 5. Recommendation

The area is well defined and active: three 2025–2026 papers from the
Basu/Cristi–Salas groups. It is still open in general, and a first-pass
result came quickly. Theorem C gives a d-independent depth constant for one
integer variable. It closes the n = 1 information-complexity gap. Its proof
is short and checked numerically, but it is not independently reviewed, and
it may be folklore or already in Oertel's unexamined thesis. The natural next
target, a d-independent constant for fixed n ≥ 2, faces a concrete
obstruction (twisted affine selections) and would still carry little solver
value. Recommendation: spend a small, bounded effort to verify Theorem C
independently, check the Oertel thesis, and write it up as a short note. Do
not make this area the main direction for a solver-relevant MINLP
contribution. **Score: 3/10** (significance 2, feasibility of the n = 1 note
8 but of the general question 2, originality 5).
