# Author report: upper comparisons (Section 3 and Appendix A)

Date: 2026-10-05. Author: Opus main writer `upper`.

Owned files: `sections/03-upper.tex`, `appendices/A-upper.tex`, and this
report. No other file was edited. No literature search, experiment, or
mathematical script rerun was performed.

## 1. Coverage

| Coverage ID | Where it is in the paper | Status |
| --- | --- | --- |
| A9 (and A8 as the fixed-degree case) | `thm:exact-upper` (promise form (a) and checked Hessian-certificate language (b), sparse unary degree, all six relations including `=` and `!=`) | Full proof in App. A.6-A.7 via `lem:newton-circuit`, `lem:separation`, `lem:denominator-clearing`, `lem:upper-shifted`. |
| A8 quartic certificate language | `thm:exact-upper`(b) with the general listed monomial vector `w(X,v)` containing every `v_i`; the full quartic basis `(v, X⊗v)` is the special case named in the text | Full proof (identity check, rational LDL test, `det/tr` bound via `lem:models-det-trace`, `||w||>=||v||`). Invalid certificates map to the circuit `0`. |
| A8 corollaries | `cor:upper-two-minima` (separable sum, difference observable, no joint full Gram needed), `prop:upper-circuit-witness` (short shared-circuit strict witness, no oracle, limits stated) | Full proofs in main text. |
| A12 | `thm:upper-monotone` (strongly monotone sparse polynomial maps of unary degree, which contains the cubic case; promise and checked Jacobian-Gram form), `ex:upper-nongradient` (constant skew example and the printed 4x4 certificate `Q_0` with leading minors 3, 47/16, 43/16, 65/16, recomputed by hand) | Existence by Brouwer, standalone rounded-cut warm start (`lem:upper-warm-start`, GLS Thm 3.2.1 + Remark 3.2.33, n=1 bisection), nonsymmetric Newton by elimination without pivoting (`lem:upper-pivots`). Completeness for certified cubic maps inherited from gradient lower bounds; equality upper bound only. |
| C2 | `prop:upper-slack-gap` | Full proof App. A.8. Extended to unary degree by working in the chart without expanding it; separation via the KKT formula in `(x, lambda)`; chart norm bound `||Z||<=2^{2L+1}` from Hadamard + Cramer fixed before the active set is known. The slack-gap promise is not checked; no general polyhedral deterministic `P^PosSLP` claim. Constraints section already cites this label. |
| A6 | Pointer subsection `sec:upper-roots` to `thm:reductions-root-language` | **Duplication resolved, see Section 4.** The reductions writer proves the same upper bound with the same constants in `app:reductions-root-language`. I removed my duplicate theorem/proof; fallback text is in Section 10 below. |
| A13 | `thm:posslp-closure`(c) | Derived from part (a). |
| A14 | `thm:posslp-closure`(a),(b) | Full error budget, positive-denominator pairs, explicit universal padded interpreter and machine unrolling, `P^PosSLP = {L : L <=_m PosSLP}`; restrained novelty wording ("We make no priority claim"). |
| D4 structured corollary | `cor:structured-single-sign` is defined by the constraints writer (`sections/05-constraints.tex`, proof `app:constraints-single-sign`) | **Duplication resolved, see Section 4.** My section now explains the application and cites their corollary. Fallback text in Section 10. |

Toolkit owned by `upper` per DECISIONS.md: `lem:separation` (common
algebraic separation), `lem:denominator-clearing` (rational denominator
clearing), `lem:newton-circuit` (shared Newton point, uniform in the
observable), `thm:posslp-closure` (adaptive sign compiler).

Not covered here by decision: degeneracy frontier, equality/uncertainty and
nullvector boundaries (Appendix K, contrast owner); `prop:upper-degenerate`
from the architecture is therefore not written.

## 2. Shared labels defined in my files and their exact contracts

- `lem:separation`. Absolute integer `c_0>=1`. Quantifier-free `Phi(y,z)`,
  `y` in `R^s`, `s>=1`, polynomials in `Z[y,z]` of degree `<= d` (`d>=2`) and
  coefficient bit size `<= tau` (`tau>=1`); if
  `{z : exists y Phi(y,z)} = {alpha}` then alpha is algebraic and
  (a) "polynomial-size formulas": if `s,d,tau <= L^c` (`L>=2`, `c>=1`), then
  `alpha=0` or `|alpha| >= 2^{-2^e}`, `e = c(c_0+2)L^{c+1}`;
  (b) "explicit form": `alpha != 0` implies `|alpha| >= 2^{-2 tau d^{c_0 s}}`
  (linear in `tau`, single exponential in `s` for fixed `d`).
  Inequalities and Boolean combinations are allowed, so KKT formulas with
  `lambda>=0` and complementarity are covered. The constraints writer's
  "first form" and "second form" correspond to (a) and (b).
- `lem:denominator-clearing`. Syntactic pair construction, size `O(sigma+b)`,
  no sign tests; if all divisions are by nonzero values then `Q_v>0` and
  value `= N_v/Q_v` at every node; division rule
  `(N_a Q_b N_b, Q_a N_b^2)` (`eq:upper-division`). This replaces the
  architecture's proposed `lem:models-division`; see Section 5.
- `lem:newton-circuit`. Input of length `L`: `n>=1`, rational `mu>0`, and
  (a) explicit sparse `f` with `Hess f >= mu I` (then `T = grad f`) or
  (b) explicit sparse map `T` with strong monotonicity modulus `mu`. Given
  `L' >= L` in unary, time `poly(L')`, no oracle: a shared rational circuit
  `x_hat` with all divisions by nonzero values such that every explicit sparse
  `h` of encoding length `<= L'` has `h(p)=0` or `|h(p)| >= g_{L'}`, and
  `|h(x_hat)-h(p)| <= g_{L'}/8`, where `g_{L'} = 2^{-2^{e(L')}}`,
  `e(L') = (c_0+3)L'^2`; `g_{L'}` has a circuit by `e(L')` squarings of 1/2.
  Heights (`thm:circuit-gram`, witness families) and constraints
  (normal-cone test) use exactly this form.
- `thm:exact-upper`, `thm:upper-monotone`, `cor:upper-two-minima`,
  `prop:upper-circuit-witness`, `prop:upper-slack-gap`, `thm:posslp-closure`.
- Section label `sec:upper`; appendix `app:upper` with subsections
  `app:upper-bounds`, `app:upper-separation`, `app:upper-clearing`,
  `app:upper-newton`, `app:upper-warm`, `app:upper-newton-proof`,
  `app:upper-convex-proof`, `app:upper-monotone-proof`, `app:upper-slack`,
  `app:upper-closure`. Internal lemmas: `lem:upper-derivatives`
  (`Lambda = 2^{10L'^2}` on the ball of radius `2^{5L'}`), `lem:upper-shifted`,
  `lem:upper-pivots`, `lem:upper-local-newton`, `lem:upper-warm-start`,
  `rem:upper-explicit-separation`, `ex:upper-nongradient`.

## 3. Labels I reference from other writers

All exist in the current drafts except the two marked missing.

| Label | Owner | Use | Status |
| --- | --- | --- | --- |
| `sec:models` | framing | conventions | exists |
| `sec:points` | points | prior-work pointer for convex value optimization | **missing** (02-points.tex not yet written) |
| `lem:convex-value` | points | warm start in `lem:newton-circuit`(a) and `prop:upper-slack-gap` | **missing as a statement** (its proof is in `appendices/C-points.tex`) |
| `lem:models-det-trace` | framing | `mu = det M/(tr M)^{m-1} <= lambda_min(M)` | exists, matches |
| `lem:models-low-degree` | framing | (a) convex degree `<=3` is quadratic; (b) strongly monotone degree `<=2` map is affine | exists, matches |
| `lem:models-strong-convexity` | framing | gap-to-distance on closed convex `K`, radius from a feasible point | exists, matches |
| `sec:reductions`, `thm:quartic-complete`, `thm:reductions-root-language` | reductions | lower bounds, classification, root language | exist |
| `sec:constraints`, `thm:constraints-rank`, `cor:structured-single-sign` | constraints | open polyhedral case, Las Vegas exclusion, structured application | exist |
| `sec:heights`, `thm:circuit-gram` | heights | uniform Newton point consumer, circuit Gram | exist |
| `sec:fields` | fields | rational SOS at minimum zero is not decided by the sign | exists |
| `thm:singleton-field` | algebraic | irrational minimizer at minimum zero | exists |

Contract I rely on for `lem:convex-value` (stated in App. A.5): given an
explicit sparse convex polynomial `f` (unary degree), an explicit rational
polyhedron `P` contained in a box with rational bounds, and rational
`eta>0`, a deterministic algorithm returns, in time polynomial in the
encoding length and `log(1/eta)`, a rational `x in P` with
`f(x) <= min_P f + eta`. The proof in `C-points.tex` (capped epigraph,
weak separation, GLS weak optimization, exact feasibility) appears to
provide this; please make the statement in 02-points expose it.

## 4. Duplications found and how I resolved them

1. **Cube-root language upper bound (A6).** `thm:reductions-root-language`
   (04-reductions.tex) states completeness and equality upper bound, and
   `app:reductions-root-language` proves the upper bound with the same
   constants as my former `thm:upper-root-circuit` (norm separation
   `2^{-2^{6L}}`, `14L+6` cube-root Newton steps, propagation factor
   `2^{6L+3}`). I checked their proof line by line and found it complete. To
   keep one statement and one proof, I removed my theorem and appendix proof
   and replaced them with the pointer subsection `sec:upper-roots`. If the
   root prefers the upper half in Section 3, the fallback text in Section 10
   can be restored and the reductions appendix shortened to cite it.
2. **`cor:structured-single-sign`.** The constraints writer defined this label
   with a complete proof (`app:constraints-single-sign`) that uses
   `thm:posslp-closure`(b) and checks clocking, uniform operation bounds,
   query form, and promise violations. My version proved the same content.
   I removed mine (duplicate label) and kept an explanatory paragraph in
   `sec:upper-closure` citing theirs. Their statement and proof are
   consistent with my theorem's hypotheses (deterministic, worst-case
   polynomial time for every oracle answer sequence, integer-circuit
   queries). Fallback text in Section 10.

## 5. Problems found in other drafts (for root reconciliation)

- `appendices/B-reductions.tex` line 428 cites `lem:models-division`, which is
  defined nowhere. It should cite `lem:denominator-clearing` (DECISIONS.md
  assigns denominator clearing to `upper`).
- `sections/00-introduction.tex` (table near line 466) points the supplied
  slack gap result to Section 5; it is `prop:upper-slack-gap` in Section 3.
  The constraints section already cites the proposition, so either pointer is
  harmless, but the table should name the proposition.
- The introduction table describes the monotone result as "strongly monotone
  cubic map". `thm:upper-monotone` is stated for sparse maps of unary degree,
  which includes cubics; completeness is claimed only for certified cubic
  maps.

## 6. Bibliography

Existing keys used: `Basu2014` (Theorem 2.27; the October report's cited
version, September 4, 2014 arXiv v1), `AllenderEtAl2009`,
`EtessamiStewartYannakakis2012` (Appendix C), `TarasovVyalyi2008`,
`SlotSteurerWiedmer2025`, `GroetschelLovaszSchrijver1988` (Theorem 3.2.1,
Remark 3.2.33, Lemma 3.2.8; Section 3.2).

Proposed new key (used once, in `rem:upper-explicit-separation`, not needed
by any proof): `JeronimoPerrucciTsigaridas2013` = G. Jeronimo, D. Perrucci,
E. Tsigaridas, "On the minimum of a polynomial function on a basic closed
semialgebraic set and applications", SIAM J. Optim. 23(1):241-255, 2013,
doi 10.1137/110857751, arXiv 1112.0544. I read Theorem 1 in the local KB PDF
(`literature/papers/jeronimo2013-on-the-minimum-of-a/original.pdf` via
pdftotext): degrees bounded by an even `d`, coefficients `<= H`, compact
connected component `C`, `g` of degree `<= d` with coefficients `<= H_0 <= H`;
nonzero minimum has absolute value `>= (2^{4-n/2} H~ d^n)^{-n 2^n d^n}`,
`H~ = max{H, 2n+2m}`; Section 2 assumes `n>=2`. If Luna does not add the key,
delete the remark; nothing depends on it.

Sources for Luna to verify or supply (no proof depends on an unverified
source beyond these contracts):
- Basu2014 Theorem 2.27 coefficient-bit clause for `omega = 1`, `ell = 1`, and
  the reading that `d^{O(k)}` and `tau d^{O(k)O(ell)}` hide absolute
  constants. The 2011 survey version numbers it Theorem 2.16; the paper uses
  the bib entry's 2014 numbering.
- GLS Theorem 3.2.1 with Remark 3.2.33 (weaker oracle keeping a fixed subset
  `K_1`), Lemma 3.2.8 (polynomial encoding length of centers), and the
  chapter's `n>=2` convention (n=1 is handled by bisection).
- A primary source for the classical inverse Newton sign iteration
  `x -> 2x/(1+x^2)` and its scaled variants; the text calls it classical
  without a citation.
- Prior-work comparison for `thm:posslp-closure`: Allender et al.
  Proposition 1.1 (oracle characterization), Balaji's 2016 thesis
  (`PosSLP^O` with internal sign gates; Luna is checking extended-basis
  predecessors), Etessami-Stewart-Yannakakis SICOMP 2017 Corollary 6.6
  (many-one PPS reductions with Newton circuits). Current text: "the oracle
  characterization of P^PosSLP is known; the statement proved here is the
  uniform compilation ... We make no priority claim for it."

## 7. Macros and notation

No new macro is required. Optional: `\newcommand{\PPosSLP}{\mathrm P^{\PosSLP}}`;
the text currently writes `\mathrm P^{\PosSLP}`.

Notation: `L` total binary length (n and exponents unary, so `n, D <= L`);
`n` dimension; `D` numerical degree; `mu` curvature lower bound; `Lambda`
derivative/Lipschitz upper bound (`2^{10L'^2}`); `e(L')` separation exponent;
`g` gap; `p` minimizer or zero; `f` objective; `h` observable; `T` map;
`s` quantified variables in `lem:separation`; `c_0` the elimination constant;
local symbols `sigma` (compressor scale), `kappa = 3B` (error amplification),
`B = 2^{2^S}` (magnitude), `varepsilon` (compiler error budget). `q` and `k`
are not used except `k` as gate count in `sec:upper-roots` and parameter in
the FPT remark of the constraints section.

## 8. Responses to the prewrite reductions audit and composition audit

Audit requirements (prewrite-reductions.md, "requirements for a complete
manuscript"):
1. Encoding, sharing and gate-count conventions are stated in
   `sec:upper-conventions` before any reduction; circuits are DAGs; the
   compiler counts every node including inputs, constants and control logic.
2. Full PD Hessian Gram proof for the lower constructions belongs to
   reductions/algebraic; my checked language tests `M succ 0` directly by
   rational elimination, so tensor-restricted positivity is never used.
3. Promise versus checked language is explicit in both theorems; invalid
   certificates map to the circuit `0`, for every relation including equality.
4. Polynomially bounded degree is retained; binary exponents without a degree
   bound are excluded with the reason.
5. The elimination constant `c_0` is fixed once; the Newton count
   `e(L')+1 = (c_0+3)L'^2 + 1` depends only on `L'`. Explicit constants are
   available through the JPT remark for equation-only singletons.
6. The bounded universal SLP interpreter is proved in App. A.10 part (b);
   Boolean closure is derived as part (c), not used for adaptivity.

Section-specific points: the complex critical curve example is included; the
`B`-cancelling accuracy bound `2 mu 2^{-6*2^e}` is used; the nonsymmetric
Newton step uses elimination without pivoting justified by
`lem:upper-pivots` (positive leading minors of matrices with positive definite
symmetric part), with the normal-equation alternative mentioned and the
warning not to apply symmetric elimination to `J_T`; the retained fixed ball
`B(p, delta_0)` with `delta_0 = mu^5/(32 Lambda^5)` is proved; outer cube cuts
run before map bounds are used; the threshold zero case is on the negative
side; magnitudes count scratch products of the interpreter.

composition-sign-closure.md: its content is reflected in
`thm:posslp-closure`(b) (clock, padding, malformed queries, integer values,
address enumeration rather than transcripts) and in the paragraph citing
`cor:structured-single-sign`; Las Vegas, UP/NP and multi-bit outputs are
excluded explicitly.

## 9. Checks actually run (targeted; no project-wide checks, no CI)

- Targeted LaTeX compile of only my two files: a wrapper in `/tmp/upper-check`
  (outside the repository) inputs `macros.tex`, `sections/03-upper.tex`,
  `appendices/A-upper.tex`, the shared `references.bib`, and stub targets for
  the other writers' labels; `pdflatex` (three passes) and `bibtex`.
  Final result: no LaTeX errors, no overfull boxes, no undefined references;
  one undefined citation, the proposed key `JeronimoPerrucciTsigaridas2013`.
  Two overfull boxes found earlier were fixed.
- Scoped grep of my two files for unfinished-text and repository-path
  patterns used by `verification/check_manuscript.py` (`TODO`, `FIXME`,
  `companion`, `pending review`, `to be supplied`, `/home/`, `../research-`,
  and similar): no matches.
- Mathematical checks were analytic, by hand: derivative-bound exponents,
  Newton contraction and accuracy, separation exponent arithmetic, the
  warm-start cut inequality, Hadamard/Cramer chart bound, the 4x4 certificate
  minors, the compressor/refinement inequalities and error budget. No script
  or experiment was run.

## 10. Fallback text removed from my files (not in the manuscript)

Kept here only so the root can restore the Section 3 placement if preferred.
It was compiled and proofread before removal.

```latex
% ---- Section 3 text: certified cube-root circuits ----
\subsection{Certified cube-root circuits}
\label{sec:upper-roots}

The reductions of Section~\ref{sec:reductions} pass through a language of
nested cube roots. Its comparison problem has an upper bound with a more
elementary proof: algebraic integers and norms replace quantifier
elimination, and scalar Newton steps from an explicit start replace the warm
start.

A \emph{certified cube-root circuit} consists of rational numbers $c_i$ and
$a_{ij},b_{ij}$ ($1\le j<i\le n$), rational intervals
$[\ell_i,u_i]$ with $0<\ell_i\le u_i$, and an output index $o$. It defines
real numbers by
\begin{equation}
 \xi_i^3=c_i+\sum_{j<i}\bigl(a_{ij}\xi_j+b_{ij}\xi_j^2\bigr),
 \qquad i=1,\ldots,n,
 \label{eq:upper-root-gates}
\end{equation}
with real cube roots. It is \emph{valid} if, for every $i$, the interval
obtained by evaluating the right-hand side of~\eqref{eq:upper-root-gates}
with interval arithmetic, using $\xi_j\in[\ell_j,u_j]$ and
$\xi_j^2\in[\ell_j^2,u_j^2]$, lies in $[\ell_i^3,u_i^3]$. Validity is checked
by rational arithmetic, and by induction it implies
$\xi_i\in[\ell_i,u_i]$ for all $i$.

\begin{theorem}[Comparison in certified cube-root circuits]
\label{thm:upper-root-circuit}
Given a certified cube-root circuit, a rational $r$ and a relation
${\bowtie}$, deciding whether the circuit is valid and $\xi_o\bowtie r$
reduces to one $\PosSLP$ instance.
\end{theorem}

The proof is in Appendix~\ref{app:upper-roots}. After multiplication by the
common denominator $\Delta$ of the gate coefficients and $r$, the numbers
$\Delta\xi_i$ are algebraic integers in a field of degree at most $3^n$, and
every conjugate of every $\xi_i$ has absolute value at most $2^{3L}$. The norm of the nonzero
algebraic integer $\Delta(\xi_o-r)$ is a nonzero integer, which gives
$|\xi_o-r|\ge2^{-2^{6L}}$ whenever $\xi_o\ne r$. Newton's iteration for the
cube root, started at $2^{L+1}$, converges after $14L+6$ steps to accuracy
$2^{L+1-2^{10L}}$, and the error grows by a factor at most $2^{6L+3}$ per
gate. Together with the reduction of $\PosSLP$ to this language in
Theorem~\ref{thm:reductions-root-circuit}, the theorem shows that the strict
and weak comparisons in valid certified cube-root circuits are
$\PosSLP$-complete. The reduction there produces outputs different from the
threshold, so it gives no equality lower bound. The upper bound itself is a
tailored instance of the classical approximation-and-separation argument and
is not a new general result about radical circuits.


% ---- Section 3 text: structured corollary ----
\begin{corollary}[Structured constrained comparisons with one sign test]
\label{cor:structured-single-sign}
Consider the structured boxes of Corollary~\ref{cor:constraints-boxes} and the
separable network flows of Corollary~\ref{cor:constraints-flows}, under the
same encoding, curvature and structural assumptions. For each explicit
observable $h$ of the fixed degree allowed there and each relation
${\bowtie}$, deciding $h(p)\bowtie0$ at the constrained minimizer $p$ reduces
to one $\PosSLP$ instance. The same holds for deciding whether a given
original bound is active at $p$, and for every polynomial-size Boolean
combination of such predicates.
\end{corollary}

The proof (Appendix~\ref{app:upper-structured}) checks that the procedures
behind Theorem~\ref{thm:constraints-transfer} are deterministic oracle
algorithms with a worst-case polynomial bound in the original input length.
Their warm start is an ordinary computation with polynomially many bits.
Every later step is a rational operation on shared circuits or a sign test of
such a circuit, and the number of steps is bounded by a polynomial in $L$
that does not depend on the expanded sizes of the circuit values. A clock
makes the procedure total on inputs that violate the promises.
Theorem~\ref{thm:posslp-closure}(b) then compiles each Boolean predicate. The
corollary asserts no hardness for these structured classes, and the complete
active set is again a list of instances. The randomized constraint-rank
algorithm of Theorem~\ref{thm:constraints-rank} is not covered, since its
running time is bounded only in expectation.


% ---- Appendix A text: proof of cube-root theorem ----
\subsection{Proof of Theorem~\ref{thm:upper-root-circuit}}
\label{app:upper-roots}

\emph{Encoding and validity.} Let $L\ge2$ be the input length. Then $n\le L$,
every printed numerator and denominator has absolute value at most $2^L$, and
the product $\Delta$ of the denominators of all $c_i,a_{ij},b_{ij}$ and of
$r$ satisfies $1\le\Delta\le2^L$. For a rational $a$ and an interval
$[x,y]$, put $a[x,y]=[\min(ax,ay),\max(ax,ay)]$, and add intervals
endpointwise. Let
\[
 I_i=[c_i,c_i]+\sum_{j<i}\Bigl(a_{ij}[\ell_j,u_j]+b_{ij}[\ell_j^2,u_j^2]\Bigr).
\]
The input is valid if $0<\ell_i\le u_i$ and $I_i\subseteq[\ell_i^3,u_i^3]$ for
all $i$; this is checked by rational arithmetic in polynomial time. An
invalid input is mapped to the circuit $0$. On a valid input, induction on $i$
shows $\xi_i\in[\ell_i,u_i]$: if this holds for $j<i$, then the right-hand
side of~\eqref{eq:upper-root-gates} lies in $I_i\subseteq[\ell_i^3,u_i^3]$, and
the real cube root is increasing. Hence
\begin{equation}
 2^{-L}\le\xi_i\le2^L\qquad(i=1,\ldots,n).
 \label{eq:upper-root-range}
\end{equation}

\emph{Separation.} Put $\alpha_i=\Delta\xi_i$. Then
\[
 \alpha_i^3=\Delta^3c_i+\sum_{j<i}\bigl(\Delta^2a_{ij}\alpha_j
 +\Delta b_{ij}\alpha_j^2\bigr),
\]
and $\Delta^3c_i$, $\Delta^2a_{ij}$ and $\Delta b_{ij}$ are integers. By
induction each $\alpha_i$ is a root of a monic cubic whose other coefficients
lie in the ring generated by algebraic integers, so every $\alpha_i$ is an
algebraic integer. The field $\mathbb K=\Q(\xi_1,\ldots,\xi_n)$ has degree at
most $3^n$ over $\Q$. Let $\phi$ be a complex embedding of $\mathbb K$. We
claim $|\phi(\xi_i)|\le M_0:=(2L+1)2^L\le2^{3L}$. If this holds for all
$j<i$, then
\[
 |\phi(\xi_i)|^3\le2^L\bigl(1+LM_0+LM_0^2\bigr)\le2^L(2L+1)M_0^2=M_0^3 ,
\]
because the coefficients have absolute value at most $2^L$, there are at
most $L$ indices $j$, and $M_0\ge1$. Now suppose $\xi_o\ne r$. Then
$\beta=\Delta(\xi_o-r)=\alpha_o-\Delta r$ is a nonzero algebraic integer in
$\mathbb K$, and its norm $\prod_\phi\phi(\beta)$ is a nonzero integer. Every
factor satisfies
$|\phi(\beta)|\le\Delta(M_0+|r|)\le2^L(2^{3L}+2^L)\le2^{4L+1}$, and the
identity embedding is one of the factors. Hence
\[
 |\xi_o-r|=\frac{|\beta|}{\Delta}
 \ge2^{-L-(4L+1)(3^L-1)}\ge2^{-2^{6L}}=:g ,
\]
where the last step uses $L+(4L+1)(3^L-1)\le(4L+2)3^L\le2^{2L}2^{2L}$ for
$L\ge2$. The bound uses no information about the conjugates beyond $M_0$; in
particular, conjugates need not lie in the supplied intervals.

\emph{Newton's iteration for one cube root.} Let $z>0$ have real cube root
$\eta\in[2^{-(L+1)},2^{L+1}]$, and iterate
$x_{k+1}=(2x_k+z/x_k^2)/3$ from $x_0=2^{L+1}$. Write $x_k=\eta(1+\epsilon_k)$.
A direct computation gives
\[
 x_{k+1}-\eta=\frac{(x_k-\eta)^2(2x_k+\eta)}{3x_k^2},\qquad
 \epsilon_{k+1}=\frac{\epsilon_k^2(3+2\epsilon_k)}{3(1+\epsilon_k)^2}.
\]
Since $\epsilon_0\ge0$, all $\epsilon_k\ge0$ and all iterates are positive.
Moreover $\epsilon_{k+1}\le\epsilon_k^2$, because $3+2\epsilon\le3(1+\epsilon)^2$,
and $\epsilon_{k+1}\le\frac23\epsilon_k$, because
$\epsilon(3+2\epsilon)\le2(1+\epsilon)^2$. From $\epsilon_0\le2^{2L+2}$ and
$(2/3)^2<1/2$, after $4L+6$ steps $\epsilon\le2^{-(2L+3)}2^{2L+2}=1/2$; after
$10L$ further steps $\epsilon\le2^{-2^{10L}}$. Hence $14L+6$ steps give
\begin{equation}
 |x_{14L+6}-\eta|\le2^{L+1-2^{10L}}=:\varepsilon_0 .
 \label{eq:upper-root-newton}
\end{equation}

\emph{Propagation.} Define $\hat\xi_i$ in order: compute
$\hat z_i=c_i+\sum_{j<i}(a_{ij}\hat\xi_j+b_{ij}\hat\xi_j^2)$ and apply $14L+6$
Newton steps with $z=\hat z_i$. Let
$E_i=\max_{j\le i}|\hat\xi_j-\xi_j|$ and $E_0=0$. Suppose
$E_{i-1}\le2^{-7L-1}$. Then $|\hat\xi_j|\le2^{L+1}$ for $j<i$, and
\[
 |\hat z_i-\xi_i^3|\le\sum_{j<i}\Bigl(|a_{ij}|+|b_{ij}|\,
 |\hat\xi_j+\xi_j|\Bigr)E_{i-1}
 \le L\bigl(2^L+3\cdot2^{2L}\bigr)E_{i-1}\le2^{4L}E_{i-1}\le2^{-3L-1}.
\]
By~\eqref{eq:upper-root-range}, $\xi_i^3\ge2^{-3L}$, so
$\hat z_i\ge2^{-3L-1}>0$ and $\hat z_i\le2^{3L}+1\le2^{3L+3}$; its cube root
lies in $[2^{-(L+1)},2^{L+1}]$, and~\eqref{eq:upper-root-newton} applies. On
the segment between $\hat z_i$ and $\xi_i^3$ the derivative of the cube root
is at most $\frac13(2^{-3L-1})^{-2/3}\le2^{2L+2}$. Therefore
\[
 E_i\le\varepsilon_0+2^{6L+2}E_{i-1},\qquad\text{hence}\qquad
 E_i\le\varepsilon_0\,(2^{6L+2}+1)^i\le2^{(6L+3)i}\varepsilon_0 .
\]
For $i\le n\le L$ the exponent of the last bound is at most
$6L^2+4L+1-2^{10L}$. Since $2^{10L}-2^{6L}\ge6L^2+11L+5$ for $L\ge2$, this
exponent is at most $-7L-1$ and at most $-2^{6L}-3$. So the hypothesis
$E_{i-1}\le2^{-7L-1}$ holds at every gate, and $E_n\le g/8$.

\emph{The circuit.} Put $\alpha=\xi_o-r$ and $\hat\alpha=\hat\xi_o-r$. Then
$\alpha=0$ or $|\alpha|\ge g$, and $|\hat\alpha-\alpha|\le g/8$. The number
$g=2^{-2^{6L}}$ is obtained from $1/2$ by $6L$ squarings.
Lemma~\ref{lem:upper-shifted} selects the rational expression for ${\bowtie}$,
and Lemma~\ref{lem:denominator-clearing} converts it into an integer circuit;
all divisions are by the positive iterates $x_k^2$ and by constants. The
rational circuit has $O(L^2)$ Newton steps and $O(L^2)$ gates for the
radicands, so the construction takes polynomial time. \qed


% ---- Appendix A text: proof of structured corollary and FPT remark ----
\subsection{Proof of Corollary~\ref{cor:structured-single-sign}}
\label{app:upper-structured}

Call a deterministic algorithm with a $\PosSLP$ oracle \emph{uniformly
bounded} if there is a polynomial $\pi$ such that on every input of length
$L$ and for every sequence of oracle answers it halts after at most
$\pi(L)$ steps, and each of its queries is an integer circuit, written in the
encoding above, of length at most $\pi(L)$. A step is an ordinary bit
operation, the creation of a circuit node, or a query. A uniformly bounded
algorithm is implemented by an oracle Turing machine whose running time is
polynomial in $\pi(L)$ for every sequence of oracle answers, as required in
Theorem~\ref{thm:posslp-closure}(b). Hence
every Boolean predicate that it decides on the promised inputs reduces to one
$\PosSLP$ instance. It remains to check that the procedures for the
structured classes are uniformly bounded. We use the procedures constructed
in Section~\ref{sec:constraints} for Theorem~\ref{thm:constraints-transfer}
and Corollaries~\ref{cor:constraints-boxes} and~\ref{cor:constraints-flows}.

\begin{enumerate}[label=(\roman*)]
\item \emph{Preprocessing.} Feasibility, the substitution of fixed
coordinates, the replacement of infinite endpoints by finite ones that keep
the minimizer strictly inside, and the rational bounds on derivatives are
ordinary computations with polynomially many bit operations.
\item \emph{Warm start.} The starting point is computed by convex value
optimization (Lemma~\ref{lem:convex-value}) with an accuracy whose encoding
length is polynomial in $L$. It is an ordinary computation, and its output
has polynomially many bits.
\item \emph{Newton phase.} The number of constrained Newton steps is a fixed
polynomial in $L$, chosen from the separation exponent and the derivative
bounds of the original input, not from the iterates. Each step solves one
exact quadratic program whose data are shared rational circuits. For boxes,
the solver uses at most $2n$ pivots, each with polynomially many rational
operations and comparisons; for flows, the strongly polynomial solver uses a
number of elementary operations and comparisons polynomial in the graph
size, and no rounding or root operation. In both cases the number of
operations is bounded by a polynomial in the dimensions alone, independently
of the encoding lengths of the circuit values. By
Lemma~\ref{lem:denominator-clearing}, every rational operation adds $O(1)$
nodes to the pair circuits, and every comparison of $N_a/Q_a$ with $N_b/Q_b$
is the query $N_aQ_b-N_bQ_a>0$, or its negative for the reverse order;
equality is the conjunction of two failed strict tests. Each query is a
circuit with polynomially many nodes.
\item \emph{Final test.} The sign of the observable is decided by one
query on the shifted expression of Lemma~\ref{lem:upper-shifted}; an active
bound $x_i=\ell_i$ is the predicate $h(p)=0$ for $h=X_i-\ell_i$, and
similarly for upper bounds and flow capacities.
\item \emph{Totality.} Let $\pi$ be the polynomial obtained from these
counts and run the procedure with a clock $\pi(L)$. On inputs that violate
the curvature or structure promises, a division can be by zero, and then a
pair receives the denominator $0$; the formulas of
Lemma~\ref{lem:denominator-clearing} still produce integer circuits, every
query is still well formed, and the clock bounds the running time. On
promised inputs every division is by a nonzero value and the procedure
follows the proved algorithm.
\end{enumerate}
Thus the procedures are uniformly bounded, and
Theorem~\ref{thm:posslp-closure}(b) compiles each predicate, and each
polynomial-size Boolean combination of predicates, into one $\PosSLP$
instance. The vector of all active bounds is a list of such instances, one
for each original finite bound. \qed

\begin{remark}
\label{rem:upper-fpt-compilation}
The construction in part~(b) of Theorem~\ref{thm:posslp-closure} only uses a
bound on the running time and query length. A deterministic oracle algorithm
with worst-case bound $F(k)L^{C}$, for a parameter $k$ and an absolute
constant $C$, is compiled in the same way into one $\PosSLP$ instance of size
$F_1(k)L^{C_1}$ with an absolute $C_1$; this is a parameterized many-one
reduction, not a polynomial-time one when $k$ grows with the input. A Las
Vegas algorithm with an expected time bound does not meet the hypothesis: a
truncated run may fail to produce an answer, and the compiler neither removes
the random bits nor selects good ones.
\end{remark}
```
