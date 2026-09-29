# Independent review of the three-variable rational-SOS comparison

Date: 2026-09-28. Status: comparison and geometric deductions passed;
the requested minor proof-wording clarification was applied and rechecked.

I independently read the full
[three-variable prior comparison](three-variable-rational-sos-descent-prior.md),
its linked earlier two-variable descent argument, and the primary
statements identified below. I did not develop the ternary counterexample
or this comparison. No blocking defect was found. This review does not
reprove the new counterexample's strict Hessian certificate or establish
publication priority.

## Dimensions and strongest relevant prior results

The comparison consistently distinguishes three affine variables from
four homogeneous variables. It does not misapply theorems about ternary
quartic forms to an affine polynomial in three variables. A homogeneous
quaternary quartic can of course be dehomogenized to three affine
variables; what the cited examples lack is the required convexity and
strict rational Hessian certificate, rather than merely the variable count.

I directly inspected the following primary sources:

- [Laplagne, arXiv:2312.16801](https://arxiv.org/pdf/2312.16801),
  Section 3.1, Proposition 3.1, and the subsequent positive construction.
  The reproduced four-variable quartic is real SOS over a cubic field
  and not rational SOS. The paper gives a rational projective zero
  and the approximate irrational point, and reports degree twelve for
  that point's coordinate field. The comparison correctly attributes
  this degree report and does not claim independently to verify it.
- The [Capco--Laplagne--Scheiderer 2019 abstract](https://www.union-matematica.org.ar/suma2019/files/00-1a-005.pdf)
  announces examples and families in the homogeneous $(3,6)$ and
  $(4,4)$ cases using degree-three coefficient fields, with uniqueness
  up to orthogonal transformations. It says the work is in progress.
  It does not assert convexity or prove the claimed properties in that
  one-page announcement. The comparison correctly treats it as prior
  announcement evidence, not a complete proof or a positive odd-degree
  descent theorem.
- [Capco--Scheiderer](https://www.impan.pl/shop/en/publication/transaction/download/product/113947),
  Theorem 3.11 and Section 3.13. The singular-boundary restriction is
  for strictly positive real-SOS forms with failed rational descent.
  The paper explicitly transfers its ternary-sextic discussion to
  quaternary quartics. It does not classify all quaternary quartics
  with real zeros.
- [Ahmadi--Blekherman--Parrilo](https://arxiv.org/html/2404.14440v1),
  Theorem 3.1 and Corollary 3.8, and
  [El Khadir](https://optimization-online.org/wp-content/uploads/2019/09/7380.pdf),
  Theorem 1.1. These are statements about convex homogeneous forms
  and real SOS or SOS-convexity. They are not rational-descent
  statements for arbitrary affine ternary quartics.
- [Blekherman--Iliman--Kubitzke](https://arxiv.org/pdf/1305.0642),
  Theorem 1.8. It uses real projective points in general linear
  position and compares ordinary and symbolic square dimensions.
  The dimensions ten and eleven for six points, and equality for at
  most five, are reported accurately. Those conclusions alone do not
  give either rational descent or a convex perturbation at the
  particular mixed real/nonreal Galois orbit.
- [Scheiderer's published classification](https://ems.press/content/serial-article-files/32129),
  Theorem 4.1. The linked two-affine-variable argument uses exactly
  this ternary homogeneous quartic result. The four distinct lines in
  general position must come in nonreal conjugate pairs for a
  nonnegative form; their two distinct real intersections contradict
  the single-projective-zero conclusion supplied by the strict Hessian
  Gram. Thus the dimension-minimality comparison is justified within
  the stated hypotheses.

This review did not locate or claim to read the full separately cited
Capco--Laplagne--Scheiderer preprint. It also did not independently
reprove the old example's non-rational-SOS certificate. Those limitations
are consistent with the comparison note.

## Projective changes do not supply the desired convex example

If the Hessian has a positive definite Gram matrix on
$(v,x\otimes v)$, its principal block $C$ on $x\otimes v$ is
positive definite. Comparing the highest-degree terms and applying
Euler's identity gives

\[
 12F_4(x)=x^{\mathsf T}\nabla^2F_4(x)x
        =(x\otimes x)^{\mathsf T}C(x\otimes x)>0
 \quad(x\ne0).
\]

Therefore the homogenization has no real zero at infinity. Strong
convexity and minimum zero give just one affine zero, hence exactly
one real projective zero. An invertible real projective map preserves
that count. The old form has at least the distinct rational and
irrational projective zeros identified in the source, so changing its
chart cannot give the requested properties. This argument needs neither
an exhaustive list of its zeros nor the reported degree-twelve fact.

The rational version is also correct. Rational projective changes
preserve rationality of a projective point and rational SOS of forms.
If such a transformed polynomial had the requested strict certificate,
its rational projective zero would have to be the unique affine zero.
Taylor integration of the rational Hessian Gram at that rational point
gives a rational positive semidefinite Gram for the polynomial. Rational
positive semidefinite Gram matrices yield rational SOS using rational
LDL and four-square decompositions, without requiring a rational
Cholesky factor. This contradicts the original failed rational descent.

The even-degree obstruction is valid as stated conditionally on the
reported coordinate-field degree. A number field of even degree with
a real embedding has at least two real embeddings, because its real
embedding count has the same parity as its degree. Distinct embeddings
give distinct tuples of its generating coordinates. Every rational
polynomial vanishing at the original tuple vanishes at all those real
tuples. Thus a perturbation preserving it cannot produce a nonnegative
strongly convex polynomial with a single zero. Perturbations moving
the zero are correctly left outside that conclusion.

## Homogeneous convexity obstruction

For a nonnegative convex homogeneous form $H$ and a zero direction
$p$, convexity applied to

\[
 x+tp=(1-\varepsilon)\frac{x}{1-\varepsilon}
           +\varepsilon\frac{tp}{\varepsilon}
\]

gives the inequality in the note. Homogeneity makes its right side
tend to $H(x)$ as $\varepsilon\downarrow0$. The reverse inequality
comes from applying the same result with base point $x+tp$ and shift
$-tp$. I requested this explicit wording in place of merely saying
"replace $t$ by $-t$". The author applied it, and I reread the corrected
passage. The proof is correct and this review has no outstanding issue.

The resulting zero set equals the translation-invariance subspace.
For rational $H$, this subspace is the kernel of rational linear
equations in the direction vector obtained from the coefficients of
its directional derivative. A one-dimensional such kernel has a
rational generator. Thus a rational homogeneous convex form cannot
have exactly one real projective zero on an irrational line. This
explains the scope distinction without assuming that homogenization
preserves affine convexity.

## Independent exact checks of the comparison's calculations

An inline `python - <<'PY'` command independently reconstructed the
three-variable monomial bases in total degree at most two and four,
used the exact representatives
$p=(a^4/2,a,a^2/2)$ modulo $a^5-2$, and formed the five quadratics
displayed in the comparison. It verified:

- the degree-at-most-two evaluation matrix has rank five;
- the fifteen quadratic products have coefficient rank fifteen;
- the rational first-jet matrix has rank twenty;
- the first-jet matrix annihilates the product coefficient matrix.

The dimensions are therefore $10-5=5$ for the quadratic vanishing
space and $35-20=15$ for the quartic first-jet kernel. The product
span equals the latter kernel, and the symmetric Gram on the five
quadratics is unique. None of this makes that Gram positive
semidefinite. Rational SOS summands vanish on the whole Galois orbit,
while real SOS summands need only vanish at the chosen real point;
the note correctly locates its arithmetic obstruction in that difference.

The same exact command reconstructed Laplagne's displayed affine
quartic from its primary formula. It verified its Hessian at the
origin, the principal minor $-512$, and invariance under simultaneous
sign reversal of the three affine variables. These checks prove
nonconvexity of that chart and the stated symmetry. They do not
classify all possible projective transformations; the preceding
projective-zero argument supplies the stronger obstruction.

The prospective significance assessment is therefore appropriately
limited: failed rational SOS descent with a strict rational Hessian
Gram, a unique nondegenerate irrational zero, and three affine
variables would add a combination not furnished by the inspected
prior examples. The construction and its explicit certificate still
need their own proof review. Neither this comparison nor an
unsuccessful literature search establishes novelty, optimization
hardness, or practical solver failure.

Only targeted source inspection and the exact checks described above
were performed. No project-wide verification, CI inspection, or Lean
checking was run.
