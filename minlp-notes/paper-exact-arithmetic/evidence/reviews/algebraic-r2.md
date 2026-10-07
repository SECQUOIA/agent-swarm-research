# Algebraic manuscript review, round 2

Date: 2026-10-05. Scope: the completed repairs to the actual
`sections/06-algebraic.tex` and `appendices/E-algebraic.tex`. I read the full
prior `evidence/reviews/algebraic-r1.md` and the full author response
`evidence/authoring/repair-points-constraints-algebraic-r1.md`, then checked
the changed statements against their proofs. Independent delegated checks
covered the cyclic/output-format changes and the retained degree-21 argument.
This review does not expand to Appendix L or another topic.

## Final inspected files

The final read includes the root's two small prose corrections made during
this review. SHA-256 hashes:

```text
sections/06-algebraic.tex  (700 lines)
add45cc7abe70cba732e2c35b0f77ada4391e4c9c04663fc8247d6cb2ab82967

appendices/E-algebraic.tex  (2061 lines; source-locator addendum included)
a55ecca962308f61f3bf882af9fde23ab8f736a830ac83f0290052a2644d1f43
```

The initial Section 06 hash was
`b14f683b56a2cb8dcc47f566b20106e521c7f3bf75d5bf6c4898f61a2b9c0cd5`.
The appendix hash for the original R2 proof review was
`f5ba83b498e1c190aa6ad6d0fa78eacada6c2685f8cb5e46fb6e795e2e22e191`.
The two root corrections changed only the main section's explanatory prose;
the proofs stayed intact. The later appendix source-locator update is checked
in the addendum below and accounts for its final hash.

## Verdict

Changed-scope mathematical review passes. Every mandatory finding from
algebraic R1 is closed. I found no remaining internal proof gap or mathematical
regression in the repaired text. The complete factor-n-free curvature proof
is now present, while the full Hessian Gram estimate retains n. The rational
singleton and graph-lift statements have the correct scope, and the full
sharp five-variable degree-21 proof is retained.

Source-citation verification and bibliography integration remain separate
work owned by the root and Luna. AG5's singular-lci source gate is cleared by
the supplied Luna primary-source result; it is no longer an open finding of
this review.

## R1 findings checked and closed

| Finding | Actual repaired text | Verification |
| --- | --- | --- |
| R1: p must be algebraic | Section 06:315–319 | Full-rank residual gradients select n rational equations with nonsingular Jacobian. A small rational box isolates p; real-algebraic transfer makes its coordinates algebraic. No representation of p is required by the construction. |
| R2: curvature without n needed a proof | Section 06:302–304; E:444–483 | The new remark supplies all degree-zero, degree-one and degree-two Hessian estimates and the exact scalar minimization. Details below. |
| R3: graph exposing quadratic's zero set | Section 06:664–674 | The text now claims exactly g_hatp(w_*)=f(p)=0 for every rational center. The inaccurate ellipsoid/singleton parenthetical is gone. |
| R4: real points at infinity and generic combinations | Section 06:492–497 and 533–543; E:1395–1464 | The introduction now includes elimination of flat directions. The detailed explanation allows common complex zeros at infinity and correctly uses rational linear combinations, chosen generically for the length-three residual. |
| R5: cyclic integer magnitudes | E:935–947 | The polynomial-magnitude claim is limited to the listed denominator-clearing and scaling integers. The exponential-magnitude d_n and e_i have O(n) bits and enter only through weights. |
| R6: normalization of P | Section 06:348–363; E:517–533 and 661–675 | The explanation uses monic P_1, including its residual equation and derivative. It therefore accepts negative rational multiples of the input polynomial without a sign error. |

Two minor omissions survived the author's repair but were corrected by the
root during this review: the residual determinant sentence still named
P'(alpha) instead of P_1'(alpha), and the introductory infinity sentence
named a rational coordinate change without elimination of flat directions.
Both corrections are verified in the final hash above. Neither affected the
appendix proofs.

## New curvature proof: complete constants and scope

For q(p+u)=c^T u+u^T S u, the displayed Hessian identity in E:452–456 is

    v^T Hessian(q^2)(p+u) v
      = 2(c^T v+2u^T S v)^2
        +4(c^T u+u^T S u)(v^T S v).

For s=||u||, its terms of degree zero in u are 2(c^T v)^2. The degree-one
terms have absolute value at most 12||c||||S||s||v||^2: the two contributions
have bounds 8||c||||S||s||v||^2 and 4||c||||S||s||v||^2. For g, positive
definiteness of H gives a degree-two contribution at least
4 mu^2 s^2||v||^2. For each residual, the squared term is nonnegative and
the remaining product is at least -4s^2||v||^2, because ||T_j||<=1.

Adding the weighted factors in Phi=g^2+epsilon sum_j r_j^2 therefore gives

    v^T Hessian Phi(p+u) v
      >= [2 epsilon nu^2 - 12 epsilon (Lambda+m beta)s
          + (4 mu^2-4 epsilon m)s^2] ||v||^2
      >= [2 epsilon nu^2 - 12 epsilon (Lambda+m beta)s
          + 2 mu^2 s^2] ||v||^2.

The last inequality uses epsilon<=mu^2/(2m). The scalar minimum occurs at
s=3 epsilon (Lambda+m beta)/mu^2 and equals

    2 epsilon nu^2 - 18 epsilon^2 (Lambda+m beta)^2/mu^2.

It is at least (3/2)epsilon nu^2 under
epsilon<=nu^2 mu^2/[36(Lambda+m beta)^2]. Dividing by epsilon nu^2 proves
the stated global Hessian bound. Nonnegativity and vanishing at p then give
the unique zero and minimizer. Every condition used is printed in the remark
or retained from the lemma.

This is a bound at tensors w(u,v). The separate full-matrix proof E:387–403
still uses ||Delta||<=6 sqrt(n) epsilon (Lambda+m beta), and hence keeps n in
the epsilon condition for the Schur complement. The remark does not assert
that n is mathematically necessary for all full Gram constructions.

## Output formats and cyclic construction

Section 06:113–127 now correctly separates rational circuits from root
circuits. Rational arithmetic alone returns rational numbers; a root circuit
also has positive-root gates with the root index written in binary. No cheap
exact evaluation algorithm is asserted for these gates.

For the cyclic point, e_(i+1)=-2e_i-1 follows exactly from
e_i=((-2)^i-1)/3. Thus one gate for a=2^(1/d_n), followed by p_1=1/a and
p_(i+1)=1/(a p_i^2), computes the optimizer using O(n) arithmetic gates and
an O(n)-bit root index. Every division is by a positive nonzero number. The
translated first coordinate needs one additional addition. The univariate
realization's rational circuit is explicitly a circuit with input T for the
polynomial G, not a rational circuit for an irrational coordinate.

The retained exact degree d_n, primitive translated polynomial
2(T-1)^(d_n)-1, all-nonzero coefficient list of length Theta(d_n^2), rational
rank-one compression to n+1 squares, integer full Hessian Gram, and optimizer
condition number below 65600 n^2 remain valid. The certified input still
counts full exponent vectors and the dense Gram of order n+n^2, giving
L=O(n^4 log n) and the stated superpolynomial output bound with exponent 1/4.

The denominator clearing is consistent: multiplying the printed L_varrho by
D_0 gives entries

    S_0(S_0 b_1^2-a_1^2 Q_1^2) delta_ij
      +2 a_1^2 Q_1^2 z_i z_j,

which are integers of polynomial magnitude. The coefficients of 2r_j are
fixed small integers, so the resulting s_i coefficients have O(log(n+1))
bits as claimed.

## Retained sharp degree bounds and imported statements

- AG3 at E:1247–1261 still restricts the residual identity to N>=3 and
  0<=t<=s. All actual uses have the required range: reduced Cayley–Bacharach
  for n>=3, and the nonreduced residual identity with t=2 and n-3>=1.
- AG6 at E:1286–1290 still states the general minimal-degree inequality,
  including surfaces. Its use at E:1701–1712 correctly puts a degree-two
  integral surface in P^3 and excludes rank three by its real singular point.
- The rational flat-direction reduction preserves the coordinate field and
  rational square representation. Generic rational combinations produce
  the complete intersection needed for the length-three residual. The
  real-versus-complex distinction at infinity is correctly preserved.
- The finite odd-residual proof E:1586–1651 retains its filtered Gorenstein
  pairing, totally isotropic linear subspace, bounds 2v<=ell<=2^(v-1), and
  real parity contradiction for residual lengths 1,3,5,7,9.
- The positive-base proof E:1653–1771 retains every low-degree configuration,
  quadratic sheaf generation, the singular reduced complete-intersection
  curve cases, all excess values e>=10, and persistence of the D simple zeros
  under generic perturbation. AG5 yields D<=22, contradicting D>=23.
- E:1773–1792 then makes the full base finite, obtains a length-32 complete
  intersection, and applies the finite-residual argument. D<=21 and its
  attainment by the cyclic five-variable example remain fully developed.

The supplied Luna clearance verifies AG5 via EJP Theorem 3.2 and Remark 3.3
for the residual count with degree-two generators, d=5, in P^5, including
arbitrary closed subschemes. Fulton Proposition 4.1 supplies the lci Segre
formula for singular as well as smooth embeddings. The current E:1268–1285
uses those locators and limits the lci assumption to the normal-bundle formula.
This closes the prior singular-lci source gate.

Per the root's task, exact source-location checks for AG3, AG6 and the
network imports N2–N4 remain with Luna. Their statements and internal applications
show no mathematical defect in this review. Bibliography integration and
any locator updates belong to that source work, rather than an unresolved
internal algebraic proof.

## Optional clarity only

Section 06:421 could give the recurrence range 1<=i<n. Its intended use to
build p_1,...,p_n is clear, but the cyclic subsection also has modulo-(n+1)
indexing elsewhere. This is not needed for correctness of the construction.

## Checks actually run

Read-only scoped inspection used `cat` on the two review/repair reports,
`rg -n` to locate changed claims in 06/E, and `sed` with `nl -ba` to inspect
their complete proof neighborhoods. `wc -l` and
`sha256sum sections/06-algebraic.tex appendices/E-algebraic.tex` recorded and
reconfirmed the actual files. The curvature constants, determinant sign,
cyclic recurrence and integer clearing were checked analytically by hand.

No manuscript edit, mathematical script, computational experiment,
literature search, compilation, project-wide verification or CI check was
performed. Only this review artifact was written.

## Source-locator addendum: N1 primary source cleared

The root subsequently added Tutte1948 Theorem 3.6 to N1 and the elementary
loop extension at E:1128–1132. I reread those lines and their unchanged
L=2I-A convention at E:1123–1126. The extension is correct: a loop is never
an arborescence edge; deleting it reduces both the diagonal degree term and
the corresponding adjacency entry by one. Thus L and its rooted minors
are unchanged, as are the arborescence counts. The loopless source theorem
therefore supplies exactly the loop-allowed contract used here.

Luna's supplied primary-source check identifies Theorem 3.6 on printed page
470 of the original Tutte1948 scan, with arborescences directed toward the
root. Luna read that actual scan. The image-only PDF remains unread in the KB
because text extraction failed; that ingestion status does not replace or
undo the direct primary-source check. N1's source gate is now closed.

Scoped commands for this addendum were `sed`/`nl` on E:1120–1160, `wc -l`,
and `sha256sum` on 06/E. No new mathematical computation, manuscript edit,
source browsing or verification run was performed. The final appendix hash
is a55ecca962308f61f3bf882af9fde23ab8f736a830ac83f0290052a2644d1f43;
the Section 06 hash is unchanged.
