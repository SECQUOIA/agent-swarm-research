# Author report: lower reductions (Section 04, Appendix B)

Date: 2026-10-05. Author: Opus main writing agent for `reductions`.

Files written:

- `sections/04-reductions.tex` (about 9.5 pages in a standalone build)
- `appendices/B-reductions.tex` (about 14 pages)
- this report

No other file was edited. No shared macro was added: the text uses
`\operatorname{...}`, `\mathbf`, `\vec` and `\overrightarrow` inline.
No literature research, computational experiment, or mathematical script was
run.

## 1. Scope after the root decisions

DECISIONS.md and the in-flight messages fixed the scope as follows, and the
files follow it.

- `lem:quartic-realization` (generic square/exposing assembly, tensor-Schur
  positivity, canonical full-Gram covariance) is owned by the algebraic
  author. My files cite it and never reprove it. Section 3 below gives the
  exact contract my applications need.
- I own both sign compilers, the gate-specific exposing constructions and
  weights, the min-sign perturbation, A1 and A4, `thm:quartic-complete`, and
  `thm:rational-optimizer`.
- M5 is owned by constraints (D10). Section 04 represents it only by a
  pointer to `cor:constraints-binary` after `thm:rational-optimizer`. The
  binary construction is not in my files.
- Taylor SOS and strict full-Gram spanning belong to heights (and/or the
  toolkit in 01); I cite them.

## 2. Coverage

| ID | Where | Status |
| --- | --- | --- |
| A1 | `prop:reductions-sums` plus the paragraph after it | Full proof (block sum via `thm:singleton-field`); stated as a distinct source contract. Shows the source problem reduces to PosSLP (via `thm:exact-upper`), and states that no reverse reduction is known or implied. Square Root Sum excluded for value-preserving encodings by the one-real-conjugate necessity. Records why the block sum has no PD full Gram. |
| A2 | `rem:reductions-monotone` | Special case of A3 with computable boxes `[1,A]`; one-line proof. |
| A3 | `thm:reductions-signed-root`; proof in `app:reductions-signed-root` | Full proof of all gate-specific parts: sign/scale normalization (signed boxes), residual Jacobian (explicit Frobenius bound), local tridiagonal exposing form, coupled weights, exact rational vanishing representation, certified root approximation, constants, complexity. Generic assembly cited. |
| A4 | `prop:reductions-box-baseline`; proof in `app:reductions-comparisons` | Short comparison with full proof. |
| A5 | `thm:reductions-root-circuit`; proof in `app:reductions-gadgets` and `app:reductions-root-compiler` | Full analytic constants (Cauchy estimate, axis vanishing), homogenization, absolute error induction (cancellation, zero values, repeated signals), parameter generation, near-one interval certificates, auxiliary signal. |
| A6 | `thm:reductions-root-language`; proof in `app:reductions-root-language` | Included because the architecture placed it in 04 (marked "may sit in 03"). Self-contained: integral scaling, conjugate bound, norm separation, Newton cube roots, propagation, five shifted predicates. Uses `lem:models-division`. Root may move or drop it if `upper` also writes it. |
| A7 | `thm:reductions-min-sign` (proof in main text); SOS consequences in `thm:quartic-complete`(iii) | Full proof, explicit cubic Gram, scale, sign analysis. |
| A10 | `thm:reductions-quaternion` (`app:reductions-quaternion-compiler`) and `prop:reductions-quaternion-realization` (`app:reductions-quaternion-realization`) | Full proofs: identities, generator, signal arithmetic with all four operations, homogenization, upper bound with unit-norm validity check; realization with repeated parents, conjugates, weights, rounding. |
| A11 | `thm:rational-optimizer` (proof in main text) and `rem:reductions-rational-length` | Composition proof; remark shows one optimizer coordinate has a reduced denominator with more than `64*4^T` bits, exponential in `N`. |
| M5 | pointer only | Per D10, owned by constraints. |
| Coverage 8.1 | `prop:reductions-obstacles`(ii) | Naive squared-residual counterexample with proof. |
| A1-note radius obstruction | `prop:reductions-obstacles`(i) | Radius bound with proof; explains bounded sign-only signals. |

`thm:quartic-complete` assembles A5/A7/A10/A11 with the upper theorem: all
eight strict/weak value and coordinate tests are PosSLP-complete; equality
has only the upper bound; nonnegativity, real SOS, and existence of a
rational PD polynomial Gram are complete; rational SOS is hard. The lowest
possible degree is noted with `lem:models-low-degree`.

## 3. Labels I rely on from other authors (exact contracts used)

Please reconcile these names; the build with stubs resolves all of them.

1. `thm:exact-upper` (upper). For an explicit polynomial `f` with a checked
   full PD rational Hessian Gram (or supplied curvature `mu`), and an explicit
   polynomial observable `h` of degree at most four, each of `h(p)>0, >=0,
   <0, <=0, =0` at the unique minimizer reduces to one PosSLP instance. Used
   with `h=f-r`, `h=x_j-r`, and affine `h` in A1. A1 uses the promise version
   (supplied `mu=1`, true by construction).
2. `lem:quartic-realization` (algebraic; now written in `sections/06-algebraic.tex`).
   I checked its statement against my use. Hypotheses: `g, r_1..r_m` of degree
   at most two vanishing at `p`, `H >= mu I`, `||H|| <= Lambda`, `||T_j|| <= 1`,
   `||b_j|| <= beta`, `sum b_j b_j^T >= nu^2 I`, `eps=t^2 <= min{1, mu^2/(2m),
   nu^2 mu^2/(36 n (Lambda+m beta)^2)}`, `||ell|| <= eps`. Both applications
   use `n=m=N` and exactly these constants (my proofs now use the lemma's
   notation `mu`, `g`, `m`). Conclusions used: `m+1` rational quadratic
   squares, degree four, `Hessian >= (3/2)I`, unique zero and minimizer `p`,
   and part (c): the canonical Hessian Gram of the displayed representation
   is a rational positive definite full Hessian Gram computed by polynomially
   many rational operations. No approximation oracle or bound on `||p||` is
   needed, so my earlier fallback sentences about approximating `p` were
   removed.
3. `thm:singleton-field` (algebraic). Checked against its statement: for
   degree `d>=3` (with one real root) it gives in polynomial time, from a
   dense coefficient list, a quartic in `(d+1)/2` variables with zero
   `(alpha,...,alpha^n)`, `n+1` rational quadratic squares, `Hessian >= I`,
   and a PD rational Hessian Gram; for rational `alpha` it gives
   `(x-alpha)^2+(x-alpha)^4`; and (iii) implies (i) gives the necessity
   statement used for Square Root Sum. Its text already points to Section 4
   for the Square Root Sum remark, consistent with mine.
4. `lem:taylor-sos` (toolkit/heights). If `f` has a PSD real Hessian Gram on
   `(v,x⊗v)` and `grad f(p)=0`, then `f-f(p)` is a sum of squares of real
   polynomials.
5. `thm:interior-gram` (heights). Existence part: a certified quartic (full
   PD rational Hessian Gram) with `min f>0` has a rational PD Gram on all
   monomials of degree at most two.
6. `lem:models-det-trace`, `lem:models-gram-curvature` (part (b): affine
   changes of variables act by the congruence `S^T A S`; used for the fixed
   cube), `def:models-circuits` (positive-denominator rational circuits and
   division; replaces my earlier reference to a nonexistent division lemma),
   `lem:models-rational-squares`, `lem:models-low-degree`,
   `def:models-hessian-gram`, and `rem:models-gram-kinds` (block sums have no
   PD full Hessian Gram; my A1 paragraph now cites it instead of repeating the
   argument), all in `sections/01-models.tex`.
7. `cor:constraints-binary` (constraints): should take as input exactly the
   instances of `thm:rational-optimizer` (rational `p` in `[-1,1]^N`, `F>=0`
   with unique zero, `N+1` rational square factors, `Hessian >= (3/2)I`,
   checked PD Gram `Q`, `p_j != 0`, sign of `p_j` = sign of `2V-1`).
8. `thm:global-point` (points), `thm:rational-height` (heights),
   `ex:fields-ternary` (fields; the ternary minimum-zero example, SOS over
   `E` iff `2^(1/5)` in `E`; replaces my earlier `thm:fields-ternary`),
   `sec:constraints` (constraints section label).

All 17 external labels now resolve against the files on disk (checked
2026-10-05, see Section 8).

## 4. Labels I provide for other authors

- `thm:quartic-complete`, `thm:rational-optimizer`: shared main labels.
- `thm:reductions-signed-root`: certified odd-root circuit (unary odd degrees,
  rational boxes not containing zero, Minkowski interval test
  `eq:reductions-interval-test`) gives in polynomial time `F` with `N+1`
  rational quadratic squares, `Hessian >= (3/2)I`, unique zero
  `p_{i,e}=(sigma_i kappa xi_i)^e`, rational PD Hessian Gram, with
  `kappa=max{1, max_i 1/min(|lower_i|,|upper_i|)}`. The fields tower (F4,
  degree five, boxes `[1,2]`) is a special case if `fields` wants to cite it.
  The heights author built a specialized cube-chain realization (their
  report, F.2) and does not depend on this theorem.
- `lem:reductions-small-signal`: for `Q>=1`, `delta_0=1000^{-(Q+3)}`,
  `w_i=1000^i delta_0`, any cube-root circuit with at most `Q` gates whose
  radicands are constants in `[1-2w_i,1+3w_i]`, affine
  `1+sum lambda_j (xi_j-1)` with `sum|lambda_j|<=6`, or square gates passes
  the direct interval test with boxes `[1-w_i,1+w_i]`; the square chain from
  `1+3 delta_0^2` gives `0<delta_r<=delta_0^(2^r)`. Currently used only in my
  appendix; heights uses its own chain.
- `thm:reductions-root-language` is cited by the upper author
  (`sections/03-upper.tex`, subsection on nested cube roots), who sketches
  the same upper bound and defers to my proof. No duplication of the full
  proof exists there.
- `def:reductions-root-circuit`, `def:reductions-quaternion-circuit`,
  `thm:reductions-root-circuit`, `thm:reductions-root-language`,
  `thm:reductions-min-sign`, `thm:reductions-quaternion`,
  `prop:reductions-quaternion-realization`, `cor:reductions-feasibility`,
  `prop:reductions-sums`, `prop:reductions-box-baseline`,
  `prop:reductions-obstacles`, `lem:reductions-generator`, and appendix
  labels `app:reductions-*`.

## 5. Citations

Keys used (all present in the current `references.bib`):
`AllenderEtAl2009`, `TarasovVyalyi2008`, `EY2010`, `SlotSteurerWiedmer2025`.

Statements for Luna to verify (each also marked by a `% LIT-REQUEST` comment
in the source):

1. `AllenderEtAl2009`: PosSLP is in the counting hierarchy, and
   `P^PosSLP` equals the Boolean part of constant-free polynomial-time BSS
   computation (`BP(P^0_R)`).
2. `EY2010`, Lemma 5: PosSLP reduces to comparison of bounded circuits over
   `+, *, /` with values in `(0,1)` (lemma number from a repository audit of
   the author PDF, pp. 22--23).
3. `SlotSteurerWiedmer2025`, version 1: polynomial-time approximation for
   convex polynomial programming; exact decision `exists x in P: f(x)<=0`
   for convex quartics left open (Table 1 / Section 1.3). Please confirm,
   and check later versions.
4. Requested new sources, currently uncited and only described in prose:
   Dawson--Nielsen, *The Solovay--Kitaev algorithm* (near-identity
   commutators, Secs. 4.1--4.2); Ben-Or--Cleve 1992 and König--Lohrey,
   *Evaluating matrix circuits* (group/matrix-circuit simulation of
   arithmetic). If vetted, add citations at the Solovay--Kitaev sentence in
   "Relation to earlier hardness results". Optional: Etessami--Yannakakis
   2009 (recursive Markov chains) for bounded `{avg, mul}` circuit
   comparison.

Novelty language is conservative: the stated contribution is the restriction
to one explicit certified quartic and the two compilers it needs. Exact SDP
hardness, bounded-circuit hardness and commutator multiplication are credited
as prior.

## 6. Responses to `prewrite-reductions.md` and the algebraic audit

- Encoding, sharing and gate-count conventions are stated before the
  reductions (Section 4.1 and the definitions); sizes are of shared DAGs.
- Full PD Hessian Gram: provided by `lem:quartic-realization`. My
  applications verify its hypotheses and the full-space PD property is not
  inferred from tensor vectors anywhere.
- Promise versus checked language: the certified class is checked;
  malformed inputs map to a fixed program with output `-1` (also for the
  root and quaternion languages, including unit-norm checks).
- Section 1 of the audit: the complex-disk bound for `phi` is derived by
  integrating `phi'`; the `|xy|` factor and exact axis vanishing are
  stressed; zero values and repeated wires are covered by absolute bounds.
  The zero signal is a raw gate with radicand one, counted in the raw-gate
  bound `Q` (it is not an analytic macro and has exact value zero).
- Section 2: the `||J||_F <= beta` bound is stated explicitly before using
  the singular-value product; `T_alpha` indexing `j=0..n-1` is explicit;
  numerical sizes of `log A` and all precision exponents are polynomial.
- Section 3 (cube, tilt) and Section 5 (quaternions) are followed; the
  quaternion rounding uses Euclidean vector-approximation errors
  (`e_i <= h(3^i-1)`), as the October review asked.
- Canonical covariance (algebraic audit Section 4): adopted by citing the
  shared lemma; I removed every second rational projection from my
  constructions. The zero-preserving rational vanishing representation of
  the exposing form (`lem:reductions-vanishing-basis`) remains, as that audit says it must.

## 7. Deviations from the source notes

None changes a theorem statement. Changes are simplifications or repairs.

- Signed-root weights use `rho=(h_0/(4A))^2` with a row-sum argument
  (the source used `(h_0/(2NA))^2`); `gamma=h_0 rho^(k-1)/2`, `m=gamma`,
  approximation tolerance `tau<=min{1, gamma/(2kB_0), eps/(2A^N kB_0)}`,
  `B_0=A+1+32N^2(2A)^(2N)`. All bounds re-derived in `app:reductions-signed-root`.
- Signal error bounds are named `Theta_t` (cube: `2^30 Theta^3`,
  `log2 Theta_t=16*3^t-15`; quaternion: `2^20 Theta^4`).
- Quaternion operators renamed to avoid collisions with reserved symbols:
  `iota`, `rot`, `pr`, `add`, `prod`; generator `w_theta`, `theta=2^-20`.
- Box baseline: the geometric-series step is an inequality (finite sum
  bounded by the series).
- `cor:reductions-feasibility`(ii) states `Hessian >= 54 I` (from the
  `(3/2)I` realization; the source used `36 I` from `I`).
- The A1 proposition now also proves that the source comparison reduces
  to PosSLP via `thm:exact-upper`, which removes any reliance on the
  separate odd-radical upper-bound note.

## 8. Verification actually run

All checks were targeted to my two files; none is a CI or project-wide
check, and no mathematical script or experiment was run.

- A temporary harness outside the repository (`/tmp/red-check/harness.tex`)
  with the `main.tex` preamble, `macros.tex`, stub labels for the external
  references, my section and appendix, and `references.bib`: `pdflatex`
  (several runs) and `bibtex`. Final run: no errors, no undefined references
  or citations, no overfull boxes; 24 pages, of which about 9.5 are the
  section and about 14 the appendix (plus one stub page).
- An inline Python check on the two files, using the patterns of
  `verification/check_manuscript.py` on uncommented text: no unfinished-text
  pattern (after rewording "need to be supplied"), no repository paths, no
  duplicate labels among my 59 labels; no trailing whitespace; final
  newlines present.
- An inline Python resolution check of every `\ref`/`\eqref` in my two files
  against the labels in all `sections/*.tex` and `appendices/*.tex` now on
  disk: all resolve; all four cited keys exist in `references.bib`; none of
  my labels is duplicated elsewhere.
- `verification/check_manuscript.py` itself was not run: it builds the whole
  manuscript closure, whose other files are still being written by other
  authors, so it is not a check scoped to my files.

## 9. Open items for the root

1. Labels are reconciled with the files currently on disk; re-run the
   resolution check if other authors rename `lem:quartic-realization`,
   `thm:singleton-field`, `lem:taylor-sos`, `thm:interior-gram`,
   `def:models-circuits`, `rem:models-gram-kinds`, `ex:fields-ternary`, or
   `cor:constraints-binary`.
2. `thm:reductions-root-language` (A6) stays in Section 4; the upper author
   already cites it.
3. Length: main text slightly above the 7--9 page budget, appendix under the
   18--22 page budget. The min-sign and classification proofs are in the
   main text because each is under a page; they can move to Appendix B if
   the editor wants a shorter Section 4.
4. Literature: the four verification items and the requested commutator /
   matrix-circuit sources in Section 5.
