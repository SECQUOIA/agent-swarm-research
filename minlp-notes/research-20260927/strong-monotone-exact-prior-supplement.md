# Supplementary search for exact strongly monotone polynomial comparison

Date: 2026-09-28. This is a source-scope check, not a proof review or a
priority claim. It supplements
[the existing upper-bound prior audit](strong-convex-quartic-posslp-upper-prior.md).
The search target was exact rational-threshold comparison at the unique
root of a strongly monotone rational polynomial map, especially the
gradient of a globally strongly convex rational quartic with a supplied
rational curvature bound. No additional PosSLP upper-bound or completeness
theorem for that target was found in the sources inspected below.

**Finite convergence for convex polynomial optimization.**
De Klerk and Laurent,
[*On the Lasserre hierarchy of semidefinite programming relaxations of
convex polynomial optimization problems*](https://ir.cwi.nl/pub/18610/18610D.pdf),
SIAM Journal on Optimization 21 (2011), 824–832, Corollary 3.3, proves
finite convergence under convexity, Slater's condition, an Archimedean
quadratic module, and positive definite objective Hessian at the minimizer.
Section 4.2 gives an explicitly approximate ellipsoid guarantee in the
real-number model. Theorem 4.2 shows that the finite relaxation order has
no bound depending only on the dimensions, degrees, and number of nonzero
coefficients. Those parameters omit coefficient bit lengths and the
supplied curvature bound; the theorem therefore does not rule out a
bound depending on them. These statements provide neither a polynomial
exact-decision algorithm nor a PosSLP classification. The CWI final
version has Corollary 3.3; an earlier eight-page version has different
numbering and should not be silently substituted.

**Finite convergence for polynomial variational inequalities.**
Nie, Sun, Tang, and Zhang,
[*Solving polynomial variational inequality problems via Lagrange
multiplier expressions and Moment-SOS relaxations*,
arXiv:2303.12036v1](https://arxiv.org/html/2303.12036v1),
Theorem 3.4, bounds the number of outer loops by one plus the number of
KKT candidates that are not solutions, assuming this number is finite
and the constraining polynomial tuple is nonsingular. Theorem 3.5 gives
finiteness for generic polynomial data. Theorem 4.2 gives finite
convergence of a Moment-SOS subproblem hierarchy when its polynomial
equalities have finitely many real solutions, under the stated
Archimedean and generic-objective assumptions. The loops contain
polynomial optimization subproblems. The paper does not give a
polynomial bit-cost bound, an exact threshold complexity class, or a
special PosSLP theorem under strong monotonicity. Its finite-convergence
claim is therefore not the sought classification.

**Condition-dependent exact real-zero counting.**
Cucker, Krick, Malajovich, and Wschebor,
[*A Numerical Algorithm for Zero Counting. I: Complexity and Accuracy*,
arXiv:0710.4508v2](https://arxiv.org/pdf/0710.4508v2),
Theorem 1.1, counts real zero rays of a square homogeneous polynomial
system using finite-precision arithmetic. Its total arithmetic cost
contains a factor of the form
\((2(n+1)D^2\kappa(f)^2/\alpha_*)^{2n}\), even though the
number of refinement rounds is logarithmic in the condition number.
Remark 1.2 permits nontermination on ill-posed inputs with infinite
condition number. This is an exact finite-valued computation, but it
does not supply a polynomial-time root-threshold procedure for growing
dimension or a supplied strong-monotonicity modulus.

Searches combined `PosSLP`, `strongly monotone`, `strongly convex`,
`gradient`, `quartic`, `polynomial variational inequality`, `exact`,
`BSS`, and `condition number`. Searches also returned the already-audited
PPS, Hesse, and real-computation bridge results; they are not counted as
new evidence here. A separate agent checked the conditioning literature.
No absence-of-prior-work conclusion follows from these searches.

Targeted verification: a Python check of this file verified its final
newline, whitespace, control characters, and local Markdown link.
`git diff --check -- research-20260927/strong-monotone-exact-prior-supplement.md`
passed. No project-wide verification or CI inspection was run.
