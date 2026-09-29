# Adversarial review of the singleton field prior audit

Date: 2026-09-28. Reviewed
[the prior audit](singleton-field-characterization-prior.md), with its
[arithmetic comparison](singleton-field-characterization-prior-independent.md)
and [pencil comparison](planar-corank-one-singletons-prior.md).
This review covers necessity and the stated source comparisons. It does
not repeat the three-quadratic construction proof or the separate
one-parameter classification review.

No mathematical gap was found in the necessity argument. The literature
assessment appropriately leaves priority unestablished. The explicit
qualifications identified below have been incorporated in Section 4 and
checked again. They make its intended argument precise rather than change
its conclusion.

## Necessity

The active inequalities alone define the singleton. A second point
satisfying them gives a segment satisfying every active inequality by
convexity. Continuity preserves each inactive strict inequality near
the singleton, and the finite family permits a common positive segment
length. This also works when only the active zero sublevels are convex.

The singleton coordinates are algebraic by real quantifier elimination
over the rationals. Every real embedding of their generated number field
preserves the active equalities, hence fixes the entire tuple and is the
identity. No preservation of inequality signs is assumed.

The passage to an individual coordinate is valid. A number field with
one real embedding has odd degree. Its extension over any subfield
therefore has odd degree. Transporting a primitive-element minimal
polynomial along any real embedding of that subfield produces an
odd-degree real polynomial with a real root. This extends that embedding
to a real embedding of the full field. Thus each coordinate field also
has exactly one real embedding. The odd-degree argument is essential;
extension to a real embedding is not automatic for arbitrary finite
extensions.

The claimed scope is also correct. Convexity of an intersection alone
does not suffice, as the rational description of the singleton
\(\{\sqrt2\}\) shows. General conic descriptions need not give
individual convex polynomial sublevels.

## The interpolation comparison and corrected wording

An independent reviewer checked Krick--Mourrain--Szanto, equations (4)
and (6), Proposition 2.2, Lemma 2.7 and Proposition 2.8. For squarefree
\(p\), setting the target to zero in the displayed interpolation
identities gives the claimed sum over nonreal conjugate pairs. The SOS
Gram matrix has kernel equal to the span of real-root evaluation
vectors: its coefficient vectors have rank equal to the number of
nonreal roots. Proposition 2.2 assumes strict positivity at real roots,
so the note correctly treats this specialization as an inference, not
as that proposition's conclusion. The positive-definite rounding
argument does not supply rounding inside the zero-target boundary
face. [Primary paper](https://arxiv.org/pdf/2112.00490)

The revised hypotheses are explicit: \(p\) is squarefree of degree \(d\)
in the interpolation argument; for the rational obstruction it is
irreducible and has a real root \(\alpha\), and
\(v(t)=(1,t,\ldots,t^{d-1})^T\). If rational symmetric \(B\)
is PSD and \(v(t)^TBv(t)\equiv0\pmod p\), then
\(Bv(\alpha)=0\), and power-basis independence forces \(B=0\).
The real-root hypothesis matters: \(p=t^2+1\), \(B=I_2\)
satisfies the congruence and is positive definite.

The revised obstruction concerns a **nonzero rational PSD matrix
satisfying the exact congruence**. Rational PSD approximations without that congruence do
exist. With this qualification, the distinction between positivity on
the nonreal-root subspace and global PSD, followed by the companion
sandwich, is correctly stated. This review checks that distinction,
not the full construction using it.

## Other primary comparisons

Direct inspection confirms that Slot--Steurer--Wiedmer, Example C.2,
already gives the rational globally convex sextic
\((t^3+t+1)^2\) with an irrational cubic singleton zero set. Lemma
C.3 has the stated rational-minimum hypothesis for a univariate convex
quartic. Thus irrational native polynomial singleton feasibility is
prior work, while these statements do not give the claimed general
representation. [Primary Appendix C](https://arxiv.org/html/2511.03440v1#A3)

The other inspected statements match the audit:

- Bodirsky--Jonsson--von Oertzen, Section 6, requires each polynomial
  inequality to define a convex set and explicitly distinguishes that
  class from general convex semialgebraic sets.
  [Primary paper](https://lmcs.episciences.org/1218/pdf)
- Liang--Li--Bai, Lemma 3.8(2), gives real finite eigenvalues for a PSD
  Hermitian pencil and includes singular pencils. The arithmetic
  consequence remains an additional inference.
  [Primary paper](https://web.cs.ucdavis.edu/~bai/publications/lianglibai13.pdf)
- Hillar's Theorem 1.5 and Scheiderer's Theorem 1.2 and Proposition 1.6
  concern descent of SOS or quadratic-module representations.
  Chua--Plaumann--Sinn--Vinzant, Remark 1.7, explicitly supplies the
  \(t^2+\sqrt2\) example distinguishing PSD at one embedding from
  an SOS over the field.
  [Hillar](https://arxiv.org/pdf/0704.2824),
  [Scheiderer](https://ems.press/content/serial-article-files/32129?nt=1),
  [Gram Spectrahedra](https://arxiv.org/pdf/1608.00234)

The older Laurent, Laplagne and SPECTRA comparisons were not re-audited
in this pass. Neither this bounded source check nor the earlier searches
establish originality of the characterization or construction.

## Verification

The necessity proof was checked directly, and the interpolation comparison
received a separate fresh review. An exact SymPy calculation checked the
sextic derivative identity, the cubic's irreducibility and real-root
count, and the no-real-root counterexample to an overbroad rational PSD
claim. These calculations verify those examples, not the general proof.
Two inline `python - <<'PY'` commands performed the exact symbolic checks
and the Markdown checks. `git diff --check --
research-20260927/singleton-field-characterization-prior-review.md` also
returned no diagnostics. Targeted Markdown checks covered this review's final newline, trailing
whitespace, control characters, display-math delimiters and relative
links. No project-wide checks or CI inspection were used.
