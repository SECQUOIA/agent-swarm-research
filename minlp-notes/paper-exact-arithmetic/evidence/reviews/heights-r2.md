# Second manuscript review: changed height scope

Date: 2026-10-05. Independent GPT Sol review. This round checks the repairs
to `heights-r1.md`, their actual manuscript implementation, and the changed
interfaces. It does not repeat the unchanged analytic calculations accepted
in round 1. No manuscript file was edited by this reviewer.

## Verdict

**The repaired height scope is mathematically ready for integration.** All
substantive R1 height findings are resolved. One missed notation replacement
was found during this round, corrected by the root, and reread in the actual
file. The new circuit claims follow from the existing formulas and preserve
the distinction between rational circuits and irrational exact outputs.

Bibliography integration, the written Luna source-checkpoint synchronization,
and the remaining prior-work locator checks are still pending. These are
attribution and submission-integration tasks, not failures of the internally
proved height theorems. This report does not give a verdict on the still-pending
independent Opus review or on the full manuscript.

## Files and SHA-256 hashes actually reviewed

These hashes were read after the root corrected Appendix F line 673.

| File | SHA-256 |
| --- | --- |
| `sections/07-heights.tex` | `d071e16a67f04ee1810b9d24a316e5a9c191e90a8e65ec5440cf4d220b40c135` |
| `appendices/F-heights.tex` | `523e1364bd3cc09c05d4f79d889826a1d4b010ead6276e8c1e71629b85d021d3` |
| `sections/08-fields.tex` | `80b9aa17f7c0048e8de8a0e48ffb0dac64dd12884364d8034d3033cb3a1fec25` |
| `sections/01-models.tex` | `865c317989deb9f4d54012727bdcbbe2b470b69b0f8e4076df75b1d86bb97382` |
| `evidence/literature-review.md` | `452741bfca1ef248858534400cda21096609c78608f39be86521ab4f4a3012aa` |
| `evidence/authoring/repair-heights-reductions-r1.md` | `f376093fe156f51f7ccf0c29696608e47ae2fee8240b427bea471368d25e6212` |

## Resolved findings and new-claim checks

1. **Rational-circuit summary scope — resolved.** Section 07 lines 39–50,
   58–62, and 742–754 now state the two generic output contracts only on
   their appropriate sides of zero: a strict feasible point when the minimum
   is negative and an interior Gram when it is positive. The circle objects
   are named separately. Lines 826–833 correctly explain that rational
   arithmetic circuits cannot output an irrational optimizer, a maximal-rank
   optimal Gram with that optimizer field, or a nonzero exposing matrix with
   that field. No theorem about root circuits is asserted.

2. **New short circuit for the circle maximal-rank Gram — verified.** Lines
   815–825 add the exact circuit for `T_p(A)`. The optimizer has a circuit
   using k complex squarings; the rescaled optimizer additionally uses the
   explicitly encoded powers of two. Each entry of `C_U(p)` and `C_V(p)` is
   an integer polynomial of degree at most two in p, and the Taylor Gram
   formula uses matrices of order polynomial in n. The supplied rational A
   has polynomial input length in k. Appending those fixed matrix products
   therefore constructs one shared rational circuit of polynomial size in k,
   with the exact identity and rank already proved in `thm:heights-moment`.
   Similarly, the entries of `ee^T` are monomials of degree at most four in
   p and have polynomial-size shared circuits. The paragraph claims a short
   circuit for `ee^T`, not for every arbitrary positive real rescaling of it.

3. **All-yes family hardness in the table — resolved.** The `g_k` and `h_k`
   table cells at lines 850–853 and 869–872 now report circuit size only.
   Lines 884–890 place PosSLP-completeness of the constructed witness's sign
   test and PosSLP-hardness of the constructed Gram's PD test over general
   certified quartic inputs. They explicitly state that both predicates are
   always true on the displayed families. The general equivalences at lines
   790–799 and the existing many-one reductions remain valid.

4. **Full-basis PSD example and field interface — resolved.** Section 07
   lines 208–213 identifies the full-basis Gram of `sqrt(2) X_1^2` as the
   matrix with only one nonzero diagonal entry, at `X_1`. It is PSD and
   singular. Section 08 lines 107–110 now also calls it positive
   semidefinite. The conjugation argument still excludes an unweighted SOS
   over `Q(sqrt(2))`; no full-basis PD claim remains in that interface.

5. **Gram dimension N — resolved after one correction during review.**
   Section 07 line 96 and Appendix F lines 6–9 define N consistently as
   `binom(n+2,2)`, leaving D for input degree in the shared models. The
   rank, kernel, determinant, trace, and matrix-size replacements preserve
   all formulas. The original repair missed `2^{DB}` in Appendix F line
   673. I reported it immediately; the root changed it to `2^{NB}`. The
   corrected row has N denominators, each at most `2^B`, so
   `pi_i <= 2^{NB}`. The next bound `2^{(N+1)B}`, the determinant exponent
   `(N+1)(N-1)=N^2-1`, and the theorem's lower bound then follow exactly as
   before. I reread lines 657–684 after the correction. No change to the
   mathematical constant was needed.

6. **Initial circle point versus dyadic rounded points — resolved.** Appendix
   F lines 448–452 correctly restrict dyadic parts to j >= 1 and retain
   constant bit length for the initial `3/5` and `4/5`. The added magnitude
   bound is justified by `|hat z_j| <= |z_j| + e_j <= 1 + eta <= 2`; thus
   the stated bit count follows from the dyadic mesh. The error induction and
   running-time bound are unchanged.

7. **Jiang parameter comparison — repaired to remove the unit claim.**
   Section 07 lines 415–419 no longer identify an external algorithm's
   parameter with `2^k log_2 5`. The statement that the least common
   denominator of the circle optimizer is `5^{2^k}` follows directly from
   the exact reduced denominators at every level: all divide the terminal
   power and the terminal coordinates attain it. The source's exact
   parameter convention remains an attribution check, not a proof dependency.

8. **Gärtner–Magron–Vallentin comparison — repaired to remove the runtime-unit
   claim.** Section 07 lines 723–728 no longer claim bit-polynomial recovery
   in an ambiguously encoded eigenvalue margin. The internal size inference
   is correct for the manuscript's ordinary expanded rational input model:
   a positive rational lower bound below `M_k^{-2^{k+1}}` has denominator
   exceeding `M_k^{2^{k+1}}`, so its encoding has more than
   `2^{k+1} log_2 M_k` denominator bits. The printed-Gram lower bound is
   independent of the recovery method. The exact Corollary 1.3 attribution
   remains a locator/source check.

9. **BPR strict rational sampling — mathematical source gate remains cleared.**
   The root reaffirmed Luna's primary-source verification of BPR 1996 JACM
   Theorem 4.1.2, printed pages 1031–1032, in package
   `basu1996-on-the-combinatorial-and-algebraic`: every connected component
   of a nonempty strict integer-polynomial sign set, with coefficient bits
   tau and degree at most d, contains a rational point whose reduced
   coordinate numerator and denominator lengths are `tau d^{O(n)}`. This
   exactly supports Appendix F lines 802–815 at degree at most six and the
   witness comparison at degree four. The hashed `literature-review.md`
   snapshot still contains only the general height/recovery summary at line
   42; its written synchronization and the vetted bibliography key remain
   integration work. No new search or independent literature claim is made
   by this reviewer.

## Remaining items

There is no unresolved mathematical finding in the changed height scope.
The following precise source/attribution items from R1 still need the written
Luna checkpoint or a narrower citation sentence before submission:

- `HeltonNie2010`, Lemmas 7–8, and `Lasserre2009`, Theorems 2.6 and 3.3:
  the credited Taylor-integral SOS principle, exact low-order SOS-convex
  moment relaxation, and first-moment extraction with their actual hypotheses.
  All stronger kernel, uniqueness, and field conclusions in this chapter
  have internal proofs.
- `GaertnerMagronVallentin2026`, Corollary 1.3: its actual margin-input and
  exact recovery statement/locator. The revised text no longer requires an
  interpretation of its runtime as polynomial in margin bit length.
- `Jiang2021`, Theorem 1.6/Definition 2.6: the exact denominator/vertex
  complexity parameter and its units. The revised circle denominator claim
  is independent of that convention.
- `PatakiTouzov2024`: the recalled Khachiyan chain and rank/height comparison;
  `Zhang2020`, Example 2.5.3: the nonconvex cubic local-minimizer comparison.
- `Laplagne2020`, Proposition 3.2/Section 3.2: real-zero and conjugate
  rational kernel relations; `ChuaPlaumannSinnVinzant2017`, Lemma 1.5:
  compactness of the declared Gram spectrahedra. The chapter's kernel and
  quantitative trace claims are proved internally.
- Complete active bibliography integration and final source-version/locator
  harmonization. Section 08's cited key is now the 2017 key. Citation absence
  during that integration is not treated as a proof failure here.

One optional precision edit remains at Section 07 line 883: “cheap to
construct but not to validate in general” sounds unconditional, whereas the
correct statements are the PosSLP classifications in the next sentence and
the explicit “unless PosSLP is” caveat at line 795. Prefer: “The circuits can
be constructed in polynomial time. Their validation over general certified
quartic inputs has the following complexity.” This is not a theorem blocker.

## Scope and targeted checks actually run

Read the actual repaired Section 07 and Appendix F passages and the complete
file diffs against the writer's preserved copies in `/tmp/hr-r1-orig`.
Read `heights-r1.md`, the repair response, the models/fields interfaces, and
the current vetted literature report; reread the corrected Appendix F proof
passage after the root's edit. The unchanged proof calculations retain the
round-1 assessment.

Commands actually run were scoped `nl -ba`/`sed`, `rg`, `diff -u`, and
`sha256sum` on the files listed above. A final direct document-integrity check
and a whitespace check apply only to this review file. No compilation,
computational experiment, mathematical script or historical checker rerun,
literature research, project-wide verification, or CI inspection was
performed. These results are local review evidence, not CI results.

The direct Python document check passed (final newline, trailing whitespace,
and control characters). `git diff --check --
paper-exact-arithmetic/evidence/reviews/heights-r2.md` exited 0 with no output;
the direct check covers the new file independently of Git tracking.
