# Stage 4B balance-slice author audit

Owned manuscript file: `sections/09c-balance-slices.tex`.
Bibliography additions: `audit/stage4b-balance-bib.txt`.

## Source disposition

- `workbench/active/2026-09-04-hermitian-balance-slice-sharp-frontier.md`, Sections 1–5: covered by Theorem `thm:balance-slices` and Corollary `cor:balance-cap`, including heterogeneous simple Euclidean Jordan cones, Albert factors, path-connected extremes, factor essentiality and explicit nonconstant supporting slack, exact arbitrary coupled barrier values on the balance cone and base, and bounded-fiber transfer. The ambient product parameter rho is already classical in the manuscript; the new section proves the same exact value for its balance hyperplane section.
- The same source, Section 6: canonical exposed slack, central path, gap inversion, exact metric length and movement consequence are explicitly deferred to Stage 5. They are not claimed subsumed by the barrier parameter calculation here.
- `workbench/active/2026-09-04-psd-hermitian-cap-hard-connected-slices.md`, Sections 1–6: the resource/barrier frontiers are subsumed by the all-EJA theorem, but the alternate moment matrix has different signature. Corollary `cor:balance-alternate` therefore preserves its distinct family, sphere zero locus and explicit two-block extreme paths; it does not assert isomorphism with the off-diagonal-moment family.
- The second source's Section 7: matched-dimension comparison is included with explicit warning that the compared classical and Lorentz slices are different bodies. The precise ratio follows immediately from the displayed rL-1 and 2L-1 values; no claim about runtime is attached.

## Mathematical checks and improvements

The two-row minimal-face criterion is proved directly. Rank at least two has face dimension at least three in every simple EJA of rank at least two, so the exact extreme classification is one zero-height primitive block or two primitive blocks of opposite strict signs with unique weights. A two-block extreme point cannot use two primitive rays in the same block, since that gives a rank-two block.

The connectivity argument includes full cross-factor paths, including prescribed endpoints in disconnected real rank-two zero loci. Paths from either sign to zero are obtained using the connected sign regions; a balanced pair tends to the desired one-block endpoint because the opposite block weight tends to zero. This does not require any continuous selection for a competing lift.

For the Albert algebra the manuscript now gives the complete primitive-idempotent matrix P(x,y), not only diagonal entries. Artin's two-generator associativity checks P squared equals P. Positivity shows that the unique zero-height point outside the first chart is c3. The explicit path with fixed unit x and unbounded y tends to c3, as do paths with fixed |x| less or greater than one from the two sign regions. Thus there is no unsupported extension of an associative projective-space argument.

Every vanished frame coordinate defines a nonconstant support functional on the balance domain because a strictly feasible point exists. This proves boundary inheritance for the orthant and simplex sections, needed to restrict arbitrary barriers. The Hessian metric projection removes at least one unit after trace normalization; the extra balance equation can only decrease the gradient norm. The lower simplex bound makes rho-1 exact even among arbitrary coupled barriers. Bounded-fiber transfer is confined to the already proved closed-convex setting of Lemma `lem:bounded-fiber-barrier`.

The cap proof uses full-slack minimum-dimension rigidity, not a whole-row theorem. It therefore permits row splitting and discontinuous selections. With d at least three and L at least two, d is strictly less than dL-1. The gap yields total dimension at least dL and count at least L, both attained by the displayed relative-Slater slice.

No error invalidating either source was found. No new general extremality, barrier, or partial-minimization theorem is claimed. The contribution is the explicit sharp family and its combination of properties.

## Primary literature checked independently

- Henrion, Kružík and Weis, *Extreme points and faces in the moment problem*, arXiv:2606.21391v1, Theorem 2.6, read at https://arxiv.org/html/2606.21391v1 . Its injectivity criterion is explicitly attributed. The HTML has an August draft date but a June version stamp; the bibliography uses the stable version identifier without inventing publication metadata.
- Held, Stavrov and VanKoten, *(Semi-)Riemannian geometry of (para-)octonionic projective planes*, primary preprint https://arxiv.org/pdf/math/0702631 , Section 3, Definition 3.2 and Theorem 3.3: reduced homogeneous chart construction. Section 2 explicitly records two-generator associativity. Published metadata independently verified at https://www.sciencedirect.com/science/article/pii/S0926224509000205 : Differential Geometry and its Applications 27(4) (2009), 464–481, DOI 10.1016/j.difgeo.2009.01.007.
- Baez's author-hosted *The Octonions*, https://math.ucr.edu/home/baez/octonions/node12.html , was read for the Albert primitive-idempotent/projective-plane relationship. Existing bibliography entry reused.
- The known EJA identities and barrier theory use existing FK1994/GT1998 entries; the orthant/simplex lower bound uses the already checked NN1994 Section 2.3.4 and Proposition 2.3.6; bounded-fiber projection uses the manuscript's previously reviewed proof and Chares antecedent.

The section intentionally attaches no broad first-in-literature claim to the combined family. Its explicit result is stated precisely and the classical inputs are identified. The final manuscript-wide literature discussion can compare the synthesis with fixed-PSD-block and face-chain lower bounds without changing the quantifiers proved here.

## Build check

An isolated four-page driver in `/tmp/qipm-balance-check` compiled successfully with the qipm environment, BibTeX and two subsequent pdfLaTeX passes. No overfull/underfull boxes or undefined citations remained. The only undefined references were the three expected references to other manuscript sections omitted by the isolated driver: `lem:bounded-fiber-barrier`, `thm:minimal-dimension-rigidity`, and `lem:reduction`. The parent performs the integrated build. No test artifacts were added to the repository.

Integration addition by stage author: retained the long connected-extremes
source's failed coupled-log cancellation as a short final example.
Independently differentiated -log(1/9)-log(1/3-2h/3-h²)
+log(4/9-2h/3-h²): second derivative 10-27/4=13/4;
third derivative 52-27=25. A contemplated optional symbolic check found
SymPy absent from qipm; no package was installed and exact elementary
arithmetic suffices. This is not a numerical or CAS-based proof.
