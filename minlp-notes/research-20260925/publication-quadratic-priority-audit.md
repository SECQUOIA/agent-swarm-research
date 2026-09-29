# Publication priority audit: the three-variable quadratic family

Date: 2026-09-25. Reviewer: `family_priority_audit`, separate from the
construction and the current proof audit. Scope: the accepted results in
[the counterexample note](three-positive-disjoint-counterexample.md) and
[the family SDP note](three-positive-family-sdp.md). This is a fresh source
and significance audit, not a new research direction or a proof of priority.

**Verdict.** The strongest defensible contribution is a negative answer to a
specific current exactness question, accompanied by a family of exposed
nonnegative quadratics and a compact SDP that enforces a broader valid
parameter domain. Its rational separating point also survives the inspected
extended-triangle SOC system. This is a coherent, self-contained candidate for
a focused theoretical publication. It is not a new tractability result for
three-variable quadratic optimization, the first separator for its moment
hull, or a demonstrated computational improvement. No equivalent explicit
parameter family was identified in the sources examined, but publication
priority remains qualified.

## 1. Current versions of the two recent comparison sources

The following checks were made on the audit date, including current author
and repository links rather than only the previously cited versions.

| Source | Version evidence inspected | Relevant conclusion |
|---|---|---|
| Khajavirad, *Tight semidefinite programming relaxations for sparse box-constrained quadratic programs* | [Current arXiv history](https://arxiv.org/abs/2601.18545) lists v2, 12 February 2026. The [author's publication page](https://coral.ise.lehigh.edu/aida/publications/) links that arXiv record. The [current Optimization Online entry](https://optimization-online.org/2026/02/tight-semidefinite-programming-relaxations-for-sparse-box-constrained-quadratic-programs/) is dated 15 February 2026; its PDF and [Lehigh report 26T-003](https://engineering.lehigh.edu/sites/engineering.lehigh.edu/files/_DEPARTMENTS/ise/pdf/tech-papers/26/26T_003.pdf) both display 12 February 2026. | All inspected copies retain the complete-three-node, three-positive-loop question and the same relevant matrix system. |
| Anstreicher–Puges, *Extended Triangle Inequalities for Nonconvex Box-Constrained Quadratic Programming* | [Current arXiv history](https://arxiv.org/abs/2501.09150) lists only v1, submitted 15 January 2025. Its [pinned PDF](https://arxiv.org/pdf/2501.09150v1) displays 17 January 2025. The [current Optimization Online entry](https://optimization-online.org/2025/01/extended-triangle-inequalities-for-nonconvex-box-constrained-quadratic-programming/) is dated 12 January 2025; its [PDF](https://optimization-online.org/wp-content/uploads/2025/01/QPB3.pdf) displays 10 January 2025. | Equations (14)–(16), their switching conventions, and Lemmas 4–5 agree in the inspected versions. |

The [arXiv HTML for Anstreicher–Puges](https://arxiv.org/html/2501.09150v1)
displays a manuscript date of 24 August 2026 despite identifying itself as v1.
This differs from both PDFs. It does not establish a later submission or a
later mathematical version. The comparison is therefore pinned to the
explicit formulas and identified artifacts. The current author page reached
through Anstreicher's former Iowa URL did not supply a newer linked
manuscript; the current available CV still lists the work under review as a
January 2025 manuscript. An unadvertised author revision is not excluded.

No newer resolution was found by title, author, arXiv identifier, and
counterexample searches. That finding is limited to the inspected public
records; it is not evidence that no other resolution exists.

## 2. The source-specific negative answer is supported

For Khajavirad, Section 3, equation (17), specialize to all three vertices in
the positive set and no other vertices. The free set has sizes zero through
three; conditioning each complementary coordinate to either bound gives
eight scalar blocks, twelve order-two blocks, six order-three blocks, and one
order-four block. These are exactly the 27 matrices used by the repository's
rational witness. Example 3 ends with the relevant unresolved exactness
question. The counterexample's positive square coefficients make its
inequality valid also for the author's diagonal-epigraph hull. The conclusion
is about that relaxation, not failure of SDP representability.
[Inspected source, Sections 3 and 6](https://arxiv.org/html/2601.18545v2).

For Anstreicher–Puges, Section 4, equation (14) describes the trilinear moment
polytope using eight scalar inequalities. Equations (15) and (16) add rotated
SOC inequalities involving one common trilinear variable. Permutations and
coordinate complements give the instances checked in the repository. Lemmas
4–5 establish implication of ETRI1, ETRI2, and ETRI3. Since the same extended
rational point satisfies these conditions and has family-cut value `−1/40`,
intersecting this system with the family SDP is a strict strengthening. It
does not follow that the family SDP by itself contains or dominates that
system. The authors already report nonzero worst-case gaps for their SOC
system; merely showing that it is not exact is not the new contribution.
[Inspected source, Sections 4 and 5](https://arxiv.org/pdf/2501.09150v1).

This audit inspected the source formulas and existing verification records.
The separate mathematical audits establish the actual rational inequalities;
this source audit does not substitute for them.

## 3. Stronger classical comparators that must be acknowledged

### Exact formulation of the entire three-variable hull

Anstreicher and Burer's Theorem 7 gives an exact DNN formulation over any
triangulated polytope of dimension at most three. The three-cube example uses
six tetrahedra and hence six order-four DNN blocks; the paper also mentions
a five-tetrahedron triangulation. Consequently every cut in the present
family is already implied by a classical finite SDP formulation. The useful
comparison is selective family enforcement versus this complete formulation,
not representability versus nonrepresentability.
[Primary manuscript, Theorem 7 and ensuing example](https://optimization-online.org/wp-content/uploads/2007/02/1586.pdf).

### Complete separation was also known

Burer and Dong, *Separation and relaxation for cones of quadratic forms*,
Mathematical Programming 137 (2013), 343–370, provide a boundary-based
separation algorithm. Section 5.3, Corollary 3 applies it to the homogenized
three-cube; Corollary 4 extends separation to the four-cube using the earlier
three-dimensional exact formulation. The method generates general valid
quadratic cuts, rather than only the present parameter family. Therefore
“a tractable way to separate three-variable quadratic moments” would be an
overclaim. What is additional here is exact simultaneous enforcement of this
specified family by an explicit order-five LMI with six nonnegative
auxiliaries. Section 5.2 also contains a parametric class of points outside
PSD+RLT+TRI, so a parameterized gap for that older relaxation alone would not
be new.
[Author-hosted published article, Sections 3 and 5](https://sburer.github.io/papers/032-recurse.pdf).

### Earlier box inequalities

Burer and Letchford's 2009 Sections 6.3–6.4 already provide recursive
boundary checking for indefinite quadratic inequalities and an explicit
three-variable PSD+RLT+TRI counterexample. Their displayed example, written
as a nonnegative quadratic, has square-coefficient signs `(+ ,0,−)`; the
strict family here has `(+,+,+)`. Thus those two displayed examples cannot
be identified by positive scaling, variable permutation, or complementation.
This limited distinction does not exclude a more general derivation from
their framework.
[Published paper](https://doi.org/10.1137/080729529), inspected using the
[existing local full text](extreme-prior-sources/burer-letchford-2009.txt).

Galli and Letchford's *Valid inequalities for quadratic optimisation with
domain constraints* studies a more general product of univariate domains.
Sections 4.1–4.5 cover McCormick, PSD, gap, stretched Boolean-quadric, and
internal Boolean-quadric inequalities. On the full unit interval there are
no internal domain gaps; the stretching construction gives the usual
Boolean-quadric inequalities. These inspected constructions do not identify
the present five-contact family. In particular, conclusions requiring
discrete or gapped domains cannot be transferred to the full continuous
cube.
[Author manuscript, Section 4](https://www.lancaster.ac.uk/staff/letchfoa/articles/qpdc.pdf).

The earlier [family priority review](three-positive-family-priority-review.md)
also checks Lambert's Proposition 9: her named General Triangle inequalities
reduce to ordinary triangle inequalities on the unit box. This audit did not
repeat that complete proof inspection and relies on the specifically
identified earlier review for that comparison.

## 4. Alternative formulations and terminology

The same object can be described as a cone of nonnegative quadratics on the
cube, valid linear inequalities for its quadratic moment hull, or a
set-copositive cone over the homogenized cube. Priority searches must cover
all three descriptions. Copositive cut generation and low-dimensional
copositive representations are established tools, not new methods supplied
by the present result.

Dong and Anstreicher's *Separating Doubly Nonnegative and Completely Positive
Matrices* develops transformed Horn cuts and other copositive separation
procedures, including a BoxQP application in Section 5. This is a relevant
ancestor of nonlinear parameterized cut generation. Its inspected formulas
do not exhibit the present five-contact cube family or its order-five SDP
enforcement. No proof is claimed that the family cannot be obtained from a
more general copositive construction. The present proof uses the classical
identity `COP_4 = PSD_4 + N_4`; applying that identity and a Schur complement
is not itself a new cone theorem.
[Primary manuscript, Sections 2–5](https://optimization-online.org/wp-content/uploads/2010/03/2562.pdf).

The exposed-ray argument also uses established geometry: nonnegative
evaluation functionals expose faces, and contact derivatives constrain
quadratic coefficients. The candidate contribution is the particular family
and its verified properties, not that general proof technique. The validity
identity places the entire family in the full degree-four box preordering.
It therefore provides no obstruction to unrestricted SOS hierarchies or to
higher-degree certificates.

Targeted searches included the exact titles and identifiers above and the
terms `quadratic cube extreme rays nonnegative`, `box quadratic five zeros
copositive`, `quadratic programming parameterized triangle inequalities`,
`nonnegative quadratic polyhedral cones`, `valid inequalities quadratic
domain constraints`, and `set-copositive box separation`. No source located
in these searches supplied an identified equivalent parameter formula.
General copositive and recursive descriptions do encompass the valid
inequalities abstractly. An unsuccessful formula search cannot establish
priority.

## 5. Publication framing and limits

The results support a focused contribution with this order of emphasis:

1. An exact rational three-variable obstruction to the specified 27-block
   relaxation, resolving its explicitly stated exactness question.
2. The five-contact family, its exclusion proof, and its exposed-ray
   property under the strict contact assumptions.
3. A larger valid parameter domain and its exact compact SDP enforcement,
   together with strict improvement of the inspected recent systems.

These claims do not require solving the remaining completeness problem or
demonstrating a numerical speedup. Those are extensions, not holes in the
stated results. Conversely, the current evidence does not support claiming
that this is the best triple strengthening, smaller than every exact lift,
complete after symmetry closure, or practically advantageous. Applying all
symmetry orientations can use substantially more blocks than a classical
exact triple lift. A proposed implementation should compare selected family
blocks, individual cuts, the classical exact formulation, and general
separation methods.

The broader parameterization has five scalar parameters but has positive
scaling redundancy. It should not be described as five independent
dimensions of rays. Exposed extreme rays of the nonnegative-polynomial cone
should not be called facets of the moment hull without a separate dimension
argument.

I consider the explicit negative answer plus structural family adequate
material for potential theoretical publication, subject to normal external
priority checking and peer review. The compact enforcement is a useful
constructive addition, but its classical cone ingredients and the stronger
existing exact formulations make broad algorithmic or foundational claims
unwarranted.

## 6. Reproducibility of this audit

Six downloaded PDFs and their `pdftotext -layout` extractions are retained in
[publication-quadratic-sources](publication-quadratic-sources/). The
[source manifest](publication-quadratic-sources/README.md) records URLs,
retrieval date, and SHA-256 hashes. The older Burer–Letchford copy was already
present and was read in place. Other linked artifacts were inspected through
their live primary-source pages.

This audit ran only targeted source retrieval, text extraction, text search,
source-hash and local-link checks, and an exploratory exact linear-algebra comparison with a particular
five-slack copositive pullback. That last calculation did not identify an
equivalence and is not used as a theorem or as evidence of novelty. No
mathematical checker was rerun merely to duplicate the independent proof
audit. No project-wide checks, CI inspection, or Lean build was run.
The six recorded SHA-256 hashes and this note's local links passed their
targeted Python checks.
