# Prior audit: quartic nodes and the degree of a unique zero

Date: 2026-09-28. Here `n` is the number of affine variables, so the
homogenized hypersurface lies in complex projective space `P^n`.

The spectral node bound is useful only after checking its hypotheses. The
versions inspected require that all projective singularities be isolated;
strong convexity does not imply this. A direct application of the classical
Bézout theorem does give the unconditional bound

\[
[\mathbb Q(p):\mathbb Q]\le 2\,3^{n-1}
\]

for the unique zero `p` of a rational strongly convex quartic. The proof below
allows other positive dimensional singular components. This is an application
of classical intersection theory, not evidence of a new general node theorem.

1. **The spectral theorem and its indexing.** B. Castor,
   *Bounding Projective Hypersurface Singularities*,
   [arXiv:2110.12574](https://arxiv.org/pdf/2110.12574), Theorem 3.1,
   explicitly assumes that the degree-`d` hypersurface `Z` in `P^n` has only
   isolated singular points. If their local equations are `g_i` in `n`
   variables, its statement is

   \[
   \#\bigl((\alpha,\alpha+1)\cap
      \operatorname{Sp}(x_1^d+\cdots+x_n^d)\bigr)
   \ge \sum_i\#\bigl((\alpha,\alpha+1)\cap\operatorname{Sp}(g_i)\bigr).
   \]

   Multiplicities are counted. In the spectrum convention with values in
   `(-1,n-1)`, the Fermat spectrum consists of
   `sum(k_i/d)-1`, with `1 <= k_i <= d-1`, and a node has the single spectral
   number `n/2-1`. Other isolated singularities are permitted; their
   contributions do not invalidate the node count. Theorem 3.1 is a
   restatement of Varchenko's result, not its original proof.

2. **A primary computation of the quartic bound.** V. V. Goryunov,
   *Symmetric Quartics with Many Nodes*, *Advances in Soviet Mathematics*
   21 (1994), 147–161,
   [author's scanned paper](https://pcwww.liv.ac.uk/~goryunov/quartics.pdf).
   Pages 147–151 were inspected as rendered page images. Theorem 1, p. 149,
   states the bound for hypersurfaces whose singularities are all isolated
   Morse singularities. Its Arnold number is

   \[
   A_n(d)=\#\left\{(k_0,\ldots,k_n)\in\{1,\ldots,d-1\}^{n+1}:
        \sum k_i=\lfloor nd/2\rfloor+1\right\}.
   \]

   For quartics this equals

   \[
   A_n(4)=\#\left\{k\in\{1,2,3\}^{n}:
        2n-3<\sum k_i\le2n\right\}
       =[t^n](1+t+t^2)^{n+1}.
   \]

   Theorem 2, p. 150, proves

   \[
   A_n(4)\sim \frac{\sqrt3}{2}\,
                 \frac{3^{n+1}}{\sqrt{\pi n}}.
   \]

   Its table on p. 148 gives:

   | Ambient dimension `n` | 2 | 3 | 4 | 5 | 6 | 7 |
   | --- | ---: | ---: | ---: | ---: | ---: | ---: |
   | Spectral upper bound | 6 | 16 | 45 | 126 | 357 | 1016 |
   | Constructed node count | 6 | 16 | 45 | 120 | 336 | 938 |

   The first three upper bounds are attained by four general lines, a Kummer
   quartic, and the Burkhardt quartic. The constructed counts have asymptotic
   ratio `sqrt(3)/2` to the spectral bound. These are complex node counts;
   they do not provide degree lower bounds for a conjugacy orbit on a
   strongly convex rational quartic. No claim about the latest higher
   dimensional records is needed here.

3. **Primary spectral proof with an explicit isolation assumption.**
   J. H. M. Steenbrink, *The spectrum of hypersurface singularities*,
   *Astérisque* 179–180 (1989), 163–184,
   [open paper](https://www.numdam.org/article/AST_1989__179-180__163_0.pdf).
   Example 5 on pp. 169–170 discusses the projective node bound under an
   assumption of only isolated singularities, and derives the nodal case
   using Theorem 6.1 and formula (6.3). Theorem 6.1 itself assumes that the
   projective hypersurface has only isolated singularities. Thus the
   paper's treatment of spectra for nonisolated singularities does not by
   itself remove the global hypothesis needed here. The relevant text was
   read from the paper's extracted PDF text.

   D. van Straten's
   [*The Spectrum of Hypersurface Singularities*](https://arxiv.org/pdf/2003.00519),
   Section 5.4, makes the obstruction transparent: the Bruce deformation
   chooses a hyperplane avoiding the singular set, with smooth hyperplane
   section. Its cone then has an isolated singularity. That argument does
   not apply to an arbitrary positive dimensional singular set. Use the
   `n`-variable formula in Section 5.4 or Castor's Theorem 3.1; van Straten's
   Section 1.5 has inconsistent `n` versus `n+1` indexing in its displayed
   statement.

   The original reference is A. N. Varchenko, *Semicontinuity of the spectrum
   and an upper bound for the number of singular points of the projective
   hypersurface*, *Doklady Akademii Nauk SSSR* 270:6 (1983), 1294–1297,
   [Math-Net record](https://www.mathnet.ru/eng/dan10042). Its bibliographic
   record was checked, but its original full text was not obtained. This
   audit does not assert that a broader version is impossible; no inspected
   theorem established the needed extension.

The obstruction occurs even in a simple strongly convex example. Put
`s=x_1^2+...+x_n^2` and `f=s+s^2`. Its Hessian is
`(2+4s)I+8xx^T`, hence is at least `2I` on real space, and its only real zero
is the origin. Its degree-four homogenization is

\[
F=x_0^2s+s^2.
\]

All first derivatives vanish on `{x_0=0,s=0}`. For `n>=3` this set has
dimension `n-2`. This is a direct calculation, showing that the spectral
hypothesis cannot be inferred from strong convexity or a unique real zero.

4. **Bézout with other components present.** R. Lazarsfeld,
   *Excess intersection of divisors*, *Compositio Mathematica* 43:3 (1981),
   281–296,
   [open primary paper](https://www.numdam.org/article/CM_1981__43_3_281_0.pdf).
   The setting on p. 284 is `n` effective divisors on a smooth projective
   `n`-fold, each moving in a base-point-free linear system. Theorem 2.2 and
   Corollary 2.3, p. 289, decompose their intersection class into local
   limiting contributions. The following Remark, p. 290, states that an
   isolated intersection point of multiplicity `m_Q` contributes
   `m_Q[Q]` to every allowed limiting cycle. Pages 289–290 were also
   inspected visually. Consequently, the sum of isolated intersection
   multiplicities is at most the full intersection number, even if other
   components have positive dimension. On projective space this number is
   the product of the divisor degrees.

   For a compact explicit statement, J. Verschelde,
   [*Polynomial Homotopies for dense, sparse and determinantal systems*,
   Theorem 2.1](https://homepages.math.uic.edu/~jan/srvart/node3.html),
   bounds isolated complex solutions, counted with multiplicities, by the
   product of the equation degrees. This is an author-hosted exposition,
   citing Cox, Little, and O'Shea, not an original proof of Bézout's theorem.

Here is the resulting polar-intersection argument. Let `f` have degree `d`
and let `p_1,...,p_N` be its nondegenerate critical points lying on `f=0`.
These are isolated singularities, so there are finitely many. At each point
write `H_j` for the invertible Hessian. Choose an `(n-1)`-by-`n` matrix `A`
generically, and consider the `n` equations

\[
f=0,\qquad A\nabla f=0.
\]

At `p_j`, the last `n-1` equations have derivative matrix `AH_j` of rank
`n-1`. Their common zero set is locally a smooth curve. If `v_j` spans its
tangent, choose `A` also so that `v_j^TH_jv_j` is nonzero. Each requirement
is a nonempty Zariski open condition on `A`: invertibility of `H_j` allows
any tangent line, and the nondegenerate quadratic form does not vanish on
every line. Finitely many such conditions can hold simultaneously. Rational
matrices are Zariski dense, so `A` can be rational when desired.

On a local parameterization of that curve, `f` has zero constant and linear
terms and nonzero quadratic term. Its vanishing order, hence the local
intersection multiplicity of the displayed system, is exactly two.
Homogenizing the equations and applying the preceding isolated-component
Bézout inequality gives

\[
2N\le d(d-1)^{n-1}.
\]

The proof never requires the full intersection to be zero dimensional or
the hypersurface to be smooth at infinity. For `d=4` it gives
`N<=2*3^(n-1)`. It is weaker than the spectral counts when those apply:
for `n=2,3,4` it gives `6,18,54`.

For a rational strongly convex polynomial with zero `p`, the gradient
vanishes and the Hessian is positive definite at `p`. The gradient equations
therefore isolate `p` over the complex numbers, so its coordinates are
algebraic. Every embedding of `Q(p)` into `C` yields a distinct tuple
satisfying `f=0` and `grad(f)=0`; the Hessian determinant remains nonzero
under the embedding. Thus all conjugates are among the nodes counted above,
which proves the degree bound. This last passage and the polar argument are
our checked deductions from the cited results, not claims quoted from them.

Both the unconditional polar bound and the conditional spectral bound have
exponential base three as `n` grows. Moreover, Goryunov's general complex
examples already have that exponential base. A base-two bound for the
particular rational strongly convex problem would need additional structure
beyond a bound on arbitrary complex quartic nodes.

Local verification was limited to this audit. The script recorded below
computed coefficients of `(1+t+t^2)^(n+1)` and checked the displayed spectral
sequence. No project-wide verification or CI inspection was performed.

```sh
python - <<'PY'
expected = [6, 16, 45, 126, 357, 1016]
actual = []
for n in range(2, 8):
    coefficients = [1]
    for _ in range(n + 1):
        next_coefficients = [0] * (len(coefficients) + 2)
        for i, value in enumerate(coefficients):
            for j in range(3):
                next_coefficients[i + j] += value
        coefficients = next_coefficients
    actual.append(coefficients[n])
assert actual == expected, actual
print(actual)
PY
```

The script passed and printed `[6, 16, 45, 126, 357, 1016]`.
`git diff --no-index --check /dev/null research-20260927/quartic-node-bound-prior.md`
reported no whitespace diagnostics; its status was 1 because the file is new.
