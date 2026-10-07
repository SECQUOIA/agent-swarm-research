# Editorial referee report

Reviewed the current `main.tex`, `macros.tex`, `abstract.tex`, and all seven section files. This was a read-only review of the manuscript. No literature research, experiments, or mathematical verification beyond what was needed to assess wording was performed. Line numbers below refer to the draft read on 2026-10-06 and may move during revision.

## Assessment

The organization is sound. The manuscript explains the common exact-cover construction before transferring it to named families, then separates the algorithmic results from the gap-zero construction. The definitions make the distinction between hypermetric, rounded positive semidefinite, and gap inequalities clear. The strongest passages explain why family containment does not itself transfer hardness, why switching changes hypermetric coefficient sums, and why general integer rank-one examples are different from Boolean moment inputs.

The prose is generally precise and readable for a polyhedral optimization expert. No substantial reorganization is needed. The points below should be resolved before treating the prose as final. Most are local changes; the literature-status wording needs the literature lead's evidence.

## Required or strongly recommended revisions

### 1. Distinguish rational distance data from cut vectors

`sections/06-gap-zero.tex`, opening and Theorem `thm:gap-zero-hardness` (lines 4 and 29), calls arbitrary rational data a “rational cut vector.” In Section 2, a cut vector is a binary vertex `d^S`. Such a vector cannot violate a valid gap inequality. This terminology changes the apparent domain of the theorem.

Replace both occurrences with “rational distance vector.” For example:

```tex
For a rational distance vector $d$ on $n$ vertices, let
```

and

```tex
Deciding whether a rational distance vector violates a gap-$0$
inequality is $\NP$-complete.
```

### 2. State the restricted rank-one decision problem with an existential quantifier

Proposition `prop:restricted-rank-one-hardness` (`sections/05-algorithms.tex`, lines 348--351) says “deciding whether a split vector ... is violated.” Read literally, the vector is supplied as part of the input, and its slack can be evaluated directly. The intended problem searches over the restricted coefficient set.

Replace the statement with:

```tex
At rational rank-one general integer moment points, deciding whether
there exists a violated split with $v\in\{0,1\}^{n+2}$ is
$\NP$-complete, although unrestricted split separation is polynomial
there.
```

### 3. Qualify the rational Gram-factor statement

The opening of Section 5 says a rational positive semidefinite matrix need not have a rational Gram factor. The proof of `thm:rank-separation` later constructs a rectangular rational Gram factor. The opening should refer to a factor in the matrix's rank dimension.

Use:

```tex
A rational positive semidefinite matrix need not have a rational Gram
factor in its rank dimension. We therefore work first with a rational
quotient and its rational inner product.
```

### 4. Define X3C before its first use

Theorem `thm:relaxation-hardness` introduces “an X3C instance” without expanding the acronym. Define the source problem immediately before the theorem or in its opening.

```tex
We now restrict to exact cover by 3-sets (X3C), in which every set has
three elements and the universe has $p=3q$ elements.
```

The theorem can then start “Suppose the instance is X3C with $q\geq3$.” This is a small change, but it helps readers from lattice theory or semidefinite optimization who do not routinely use the complexity-problem acronym.

### 5. Make the parameterized-complexity terminology explicit

The introduction informally explains the exponent in the XP threshold bound, but Section 5 uses “XP” without a formal definition and discusses fixed-parameter tractability without stating its time-bound convention. A short definition makes the rank/support/threshold distinction easy to assess.

Insert near the start of the fixed-rank subsection:

```tex
A running time $f(k)\poly(L)$ is fixed-parameter tractable in $k$ when
the polynomial exponent is independent of $k$. An XP bound allows that
exponent to depend on $k$. Thus the rank bound below is
fixed-parameter tractable, whereas the support and threshold bounds
are XP bounds.
```

Here the threshold parameter can be taken to be the integer $B_\rho$ defined in Theorem `thm:threshold-separation`. The exact algorithm and displayed bound already establish the substantive distinction.

### 6. Reconcile the novelty wording with the literature audit

The opening “has remained unresolved in the literature” and the later claim that all listed unrestricted hardness results have not appeared in prior work are currently unqualified except for the final “To the best of our knowledge.” The literature lead has identified sources that assert hardness without a proof, while other primary sources call the question open. The revised introduction should state this distinction precisely, supported by the audited citations, instead of suggesting that all sources agree on open status.

A source-neutral opening that does not prejudge the audit is:

```tex
We study the exact decision problem of whether a rational point
violates any hypermetric inequality. We prove that this problem is
strongly NP-complete.
```

Then explain the differing earlier assertions in the prior-work subsection. The appropriate novelty claim is a claim about the proof supplied here and its exact promises, qualified by what the reviewed sources establish. Do not invent a citation to complete this revision.

Delete the sentence that the review “does not establish that no unpublished or independently obtained proof exists.” The phrase “To the best of our knowledge” already expresses this limitation; the extra sentence distracts from the documented comparison.

### 7. Use one form of each established family name

The draft alternates between “rounded positive semidefinite,” “rounded psd,” and “rounded-psd”; between “gap-$1$,” “gap-1,” and “gap-one”; and between “gap-$0$” and “gap-zero.” The hyphenated form is especially concentrated in Section 4. Use the full name on first mention and “rounded psd” thereafter, consistently. Use “gap-$1$” and “gap-$0$” throughout. These are inequality classes, so stability of the name helps the reader compare results across representations.

The heading of Section 6 can be `\section{Gap-$0$ inequalities}`.

### 8. Avoid calling the unrestricted signed family finite

Section 1 calls the classes in Theorem `thm:finite-families` “finite Boolean quadric families.” Clique and cut inequalities have finite parameter sets at fixed dimension, but equation `eq:finite-BH` permits every integer $s$. Its direction coefficients are restricted to $0,\pm1$; the family as defined is not finite.

Use “signed-coefficient Boolean quadric families” for the collective reference, and reserve “finite” for the actual clique and cut subfamilies or for their direction set. In contribution item 2, for example:

```tex
We transfer this construction to the gap-$1$, rounded positive
semidefinite, Boros--Hammer, and signed-coefficient Boolean quadric
families ...
```

For the facet sentence, use “The witnesses for the clique, cut, pure hypermetric, and odd clique families define facets; we include a direct proof.” This also makes the scope of the facet claim more explicit than “the finite families.”

## Useful tightening

### 9. State the relaxation promise concretely in the opening

“Strictly satisfying the semidefinite relaxation” is less precise than the matrix statement proved in the paper. The finite list of gonality classes can also be stated as a fixed cutoff.

Suggested replacement for the last sentence of the opening paragraph:

```tex
The hardness persists at points satisfying all triangle and perimeter
inequalities, whose elliptope matrix is positive definite, and which
satisfy every inequality below any prescribed fixed gonality cutoff.
```

Use “at most” instead of “below” if matching the final cutoff convention exactly.

### 10. Remove the reference to an unspecified enumeration assumption

The prior-work paragraph at introduction lines 75--82 contrasts the new algorithms with “an assumption that bounded-radius enumeration has polynomial bit complexity,” without identifying who made that assumption. It reads like commentary on an earlier internal draft rather than a relation to published work.

Replace it with:

```tex
Integer-quadratic separation methods can exploit low rank and lattice
structure \citep{BuchheimTraversi2015}. Our algorithmic results give
an explicit reduction to exact closest-vector problems in a rational
lattice. Existing closest-vector algorithms then yield bounds in the
binary input model. We distinguish rank from support because they
lead to different parameter dependence.
```

### 11. Remove repeated scope paragraphs at the end

The final remark of Section 6 already explains why unrestricted gap separation is immediate outside the positive semidefinite cone, why it does not compute the exact gap of a prescribed vector, and why the current construction does not settle the full gap family at positive semidefinite inputs. Section 7 repeats these points at length. Keep the local remark, and shorten the corresponding discussion to the implication and remaining question.

Suggested replacement for the fourth and fifth paragraphs of Section 7:

```tex
Gap-$0$ separation concerns points outside the elliptope: these
inequalities have zero right-hand side in the $Z$ representation and
hold whenever $Z\succeq0$. The remaining classification problem is
full gap separation at positive semidefinite points. The present
reductions control violations with gap $1$ but do not exclude a
violator with gap at least $3$ on a no-instance. A reduction for the
full family must therefore control this larger right-hand side.
```

The final paragraph beginning “No computational performance claim is needed” also reads as an explanation of the writing process. It can be deleted. The paper presents theoretical results and need not defend the absence of experiments.

### 12. Avoid reusing $W$ for both the vertex set and a lattice basis

The vertex set $W$ is a central notation throughout Sections 2--4. Section 5 reuses $W$ as a rational lattice-basis matrix and writes $W^{-1}t$. This reuse is local and technically readable, but avoidable. A distinct name such as $R_\Lambda$ for the lattice basis would make the rank proof easier to follow. The existing integer Hermite basis $H$, Gram matrix $F$, and rectangular Euclidean factor $C$ can keep their names.

### 13. Give the exact-cover theorem a direct verbal statement

The phrase “integer vectors of negative hypermetric correlation slack” in Theorem `thm:exact-cover` is dense despite being correct. Prefer:

```tex
The matrix $M$ in \eqref{eq:cover-matrix} is positive definite. For
every integer vector $z$, the following equivalence holds:
```

followed by the existing displayed equivalence. The defined function $g_M$ already identifies the slack.

## Organization and presentation

The current section order should be retained. Polynomial certificates occur after the hardness constructions, but the forward references in the corollary are explicit, so this does not obstruct the proof. The separate gap-zero section is justified: its inputs lie outside the elliptope, its reduction is only weak hardness, and its role is different from the main construction.

A compact classification table would be useful but is optional. It could group the strong-NP-complete families with their common relaxation promises, show gap-$0$ as NP-complete outside the elliptope, and show full gap separation at psd inputs as unresolved. The definitions table already occupies this function partly, and the introduction's contribution list is sufficient if the manuscript is kept concise.

I did not inspect a compiled PDF, citation resolution, bibliography completeness, or final page layout. Those checks remain with the root task's build and literature review. No general-purpose stylistic rewriting is needed after the targeted revisions above.

## Editorial closure on the revised draft

Read the revised abstract and Sections 1, 2, 5, 6, and 7, and checked the X3C definition in Section 3. The substantive accuracy objections from the first review are resolved: rational distance data are named correctly; the restricted search has an existential quantifier; the Gram-factor statement specifies the rank dimension; X3C is expanded; XP and fixed-parameter tractability are defined; the signed family is no longer called finite; the lattice basis is now `R_\Lambda`; and the exact-cover theorem uses a direct statement. The introduction documents the differing earlier complexity assertions, and its novelty claim is qualified. Literature verification remains with the Luna lead.

The abstract and conclusion have coherent scope. The abstract need not list the raw-approximation corollary as another headline result: it is a consequence of the exact classification, and the conclusion identifies it accurately. The new corollary explicitly covers the zero optimum in its multiplicative definition, uses the instance-dependent strict additive error, and disclaims hardness at a fixed additive tolerance. I found no editorial overclaim in that corollary.

Four small clarifications remain advisable; none calls for reorganizing or broadly rewriting the manuscript:

1. In the opening of Section 1, “satisfy every inequality up to any prescribed fixed gonality cutoff” should name the family. Use “satisfy every rounded positive semidefinite inequality up to any prescribed fixed gonality cutoff.” This matches the abstract and prevents “every inequality” from being read as including full gap inequalities, whose complexity the paper leaves open.
2. In the prior-work comparison of moment inputs, qualify the common-sphere statement by the positive definite setting. Use “At positive definite moment points, these identities place the origin and the lattice generators on a common sphere in the hypermetric representation.” The current unqualified sentence could be read as a statement about every ambient Boolean moment matrix, including indefinite or singular inputs.
3. In Lemma `lem:best-split-offset`, define the fractional-part notation at its first use: “For $t=w\trans x$, write $\{t\}=t-\lfloor t\rfloor$ for its fractional part and put $\phi(t)=\{t\}(1-\{t\})$.” Before Lemma `lem:primitive-split-domination`, a sentence “An integer direction is primitive if the greatest common divisor of its coefficients is one” would similarly make the remaining lattice terminology explicit.
4. Standardize the two remaining display-name variants in Section 6: change the heading `Gap-0 inequalities` to `Gap-$0$ inequalities` and the proof phrase “a gap-zero violator” to “a gap-$0$ violator.” Internal labels can retain `gap-zero`.

With those local clarifications, I have no remaining concrete editorial objection. The revised conclusion is concise and ends on the precise full-gap question. I did not inspect the reported warning-free PDF build or independently audit sources during this closure round.
