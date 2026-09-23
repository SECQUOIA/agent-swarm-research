# Literature audit: precision versus integer dimension for bilinear graphs

Date: 2026-09-05. Status: targeted novelty audit, not a proof review or a claim of exhaustive priority checking.

The candidate result under investigation concerns the vector graph

\[
\Gamma_G=\{(x,w):x\in[0,1]^V,\ w_{ij}=x_ix_j\quad(ij\in E)\}.
\]

An outer relaxation must contain every point of this graph and every projected feasible point must satisfy componentwise vertical error \(|w_{ij}-x_ix_j|\le\varepsilon\). The proposed minimum integer count, allowing arbitrary convex lifts and unbounded general integer variables, is

\[
\tau^*(G)\log_2(1/\varepsilon)+O_G(1),\qquad
\tau^*(G)=\min\{\textstyle\sum_i a_i:a_i\ge0,\ a_i+a_j\ge1\ (ij\in E)\}.
\]

No matching theorem was found in the targeted open-source search below. The upper-bound ingredients are established. The potentially new part is the universal lower bound, its matching fractional-cover coefficient for an arbitrary interaction graph, and the conclusion that choosing a more general convex formulation or unbounded integer variables cannot reduce that coefficient. The matching construction uses binary polyhedral lifts. The main theorem draft is in `results/bilinear-graph-binary-complexity.md`; despite its filename, the developed scope includes general integers.

## Closest results and exact scope differences

### Double discretization and shared binaries

Beach, Burlacu, Bärmann, Hager, and Hildebrand, *Enhancements of Discretization Approaches for Non-Convex Mixed-Integer Quadratically Constraint Quadratic Programming: Part II*, arXiv:2302.01164, is the closest located construction paper. Section 4.1, pp. 9–10, explicitly discusses bilinear systems of the form \(x^TQy\), with \(x\in\mathbb R^n\), \(y\in\mathbb R^m\). Discretizing the smaller variable block with NMDT uses \(2L\min(m,n)\) binaries for maximum error \(2^{-2L-2}\) per product; the compared D-NMDT construction uses \(L(m+n)\). Thus sharing binary discretizations across many products and exploiting bipartite structure are already explicit. Propositions 1 and 2 give the single-product maximum errors \(2^{-L-2}\) and \(2^{-2L-2}\). Section 5.2, Theorem 1 proves optimal uniform breakpoint placement **within fixed-size Cartesian piecewise McCormick grids**, using average relaxation width as the objective. This is not optimization over arbitrary lifted formulations or a universal integer-count lower bound. [Open paper](https://arxiv.org/abs/2302.01164).

The proposed construction should therefore be described as a fractional-cover allocation of known discretizations. The bipartite complete-graph upper coefficient \(\min(m,n)\) is not new. The new assertion, if verified, is that it is unavoidable even outside the discretization family, and that \(\tau^*(G)\) gives the correct coefficient for every graph.

### Vertex covers already select variables in global optimization

Nagarajan, Lu, Wang, Bent, and Sundar, *An adaptive, multivariate partitioning algorithm for global optimization of nonconvex programs*, JGO 74 (2019), 639–675, develops adaptive partitioning and convergence results for MINLPs. Its computational tables distinguish partitioning every nonlinear variable from selecting variables in a minimum vertex cover. The associated Alpine documentation explicitly defines `min_vertex_cover` for the interaction graph of nonlinear terms. This is direct prior art for the variable-selection idea. It does not, in the material inspected, formulate fractional precision allocation or establish a universal lower bound on integer dimension. [Author paper](https://harshangrjn.github.io/pdf/JOGO_2018.pdf), [official Alpine documentation](https://lanl-ansi.github.io/Alpine.jl/latest/functions/).

Undercover and Undercover Branching are additional prior art for integer vertex covers of nonlinear co-occurrence graphs. Their role is variable fixing to obtain a linear subproblem. This further rules out claiming novelty merely for associating a vertex cover with a bilinear model. A full primary-source reading of those papers was not completed in this audit; this observation is a priority lead, not a complete comparison.

### Logarithmic encodings and formulations for prescribed disjunctions

Huchette's 2018 thesis, *Advanced mixed-integer programming formulations: Methodology, computation, and application*, Proposition 1, p. 45, proves that an irredundant combinatorial disjunctive constraint with \(d\) alternatives requires at least \(\lceil\log_2d\rceil\) binaries. Section 2.7 develops graph-product constructions for multilinear discretizations; Section 3.2 studies when general integers can use fewer variables than binary encodings. Its graph is a conflict graph for a prescribed disjunction. The candidate instead uses the original bilinear interaction graph and must lower-bound the number of needed convex pieces before selecting a disjunction. The elementary counting step is established; the proposed geometric precision bound is the distinction. [Author's thesis](https://www.joehuchette.com/files/phd-thesis.pdf).

Huchette and Vielma's *A Combinatorial Approach for Small and Strong Formulations of Disjunctive Constraints*, Mathematics of Operations Research 44 (2019), 793–820, is the related published formulation source. Its applications include outer approximations of multilinear terms. It should be cited for the encoding framework, not treated as unrelated because its graphs have a different interpretation. [Published paper](https://pubsonline.informs.org/doi/10.1287/moor.2018.0946).

### Midpoint obstruction and general integer variables

Lubin, Zadik, and Vielma, *Mixed-Integer Convex Representability*, Mathematics of Operations Research (2022), provides the essential general lower-bound mechanism. Definition 4.2 calls a set \(w\)-strongly nonconvex when it contains \(w\) points with every pairwise midpoint outside the set. Lemma 4.1, the Midpoint Lemma, gives MICP rank at least \(\lceil\log_2w\rceil\). Its parity argument applies to unbounded integer variables. The paper also characterizes binary MICP representability through finite unions of projections of closed convex sets. These facts substantially precede the present investigation. The candidate contribution must be the quantitative geometry for bilinear approximation, not the parity obstruction itself. [Open paper](https://arxiv.org/abs/1706.05135); local source: `literature/papers/lubin2022-mixed-integer-convex-representability/fulltext.md`.

**General-integer extension.** For a convex mixed-integer relaxation, group exact-graph lifts by parity of their integer vectors. The midpoint of two same-parity lifts is again integer feasible, so the vertical-error condition forces \(|(x_i-y_i)(x_j-y_j)|\le4\varepsilon\) for each edge. Applying the coordinate-width lemma to the closure of each parity-support set gives a box with edgewise width products \(O(\varepsilon)\). At most \(2^b\) such boxes cover the cube, avoiding any measurability assumption on support sets. This extension was identified independently by the main proof reviewer and this audit, and incorporated into the main draft. Its source mechanism is the established midpoint/parity argument above.

### Geometric approximation lower bounds already exist for one product

Bärmann, Burlacu, Hager, and Kleinert, *On piecewise linear approximations of bilinear terms: structural comparison of univariate and bivariate mixed-integer programming formulations*, JGO 85 (2023), 789–819, is especially relevant. Section 3.1.2, Lemma 7 gives the bilinear interpolation defect \(|\Delta x\Delta y|/4\) and credits earlier work including Pottmann et al. (2000) and Kutzer's 2020 thesis. Lemma 8 gives a lower bound of \(\lceil\operatorname{area}(D)/(2\sqrt5\varepsilon)\rceil\) triangles for an interpolating bivariate \(\varepsilon\)-triangulation of a rectangle. The proof bounds the area of each admissible triangle. Thus a volume-based precision lower bound for single-product triangulations is established prior art. The candidate differs by handling arbitrary convex lifted formulations, unbounded integers, and simultaneous products through \(\tau^*(G)\). [Published open paper](https://link.springer.com/article/10.1007/s10898-022-01243-y), [author preprint](https://optimization-online.org/wp-content/uploads/2021/08/8536.pdf).

The same source identifies earlier geometric work: Pottmann, Krasauskas, Hamann, Joy, and Seibold, *On piecewise linear approximation of quadratic functions*, Journal for Geometry and Graphics 4(1) (2000), 31–53. Its full text was not independently reviewed here. It is a priority lead for single-product constants and optimal triangle shapes, not currently evidence of the arbitrary-graph theorem.

### Latest located sequential bilinear formulation paper

Ploussard, Usis, Iwakin, and Pavičević, *When MILP Beats QP: Piecewise-Linear Reformulations of Sequentially Coupled Bilinear Programs*, arXiv:2608.27312, posted 2026-08-27, studies specific CPWL approximations and three associated formulations. Theorem 1 gives maximum error \(1/(16n^2)\) and average error \(1/(48n^2)\) for its chosen function. The conclusion explicitly leaves formal optimality of the number-of-pieces/error balance open. Inspection found no universal integer-dimension bound or fractional-cover theorem. This recent paper strengthens the motivation for a formulation-independent benchmark. [Open preprint](https://arxiv.org/abs/2608.27312).

### Other established upper-bound machinery

Beach, Hildebrand, and Huchette, *Compact mixed-integer programming relaxations in quadratic optimization*, constructs logarithmic-size approximations to univariate quadratics and combines them with diagonal perturbations. It establishes exponential precision improvement with the number of binary variables for particular formulations. No arbitrary-interaction-graph integer-dimension lower theorem was located in the inspected paper. [Open paper](https://arxiv.org/abs/2011.08823).

He and Tawarmalani, *MIP Relaxations in Factorable Programming*, SIAM Journal on Optimization 34 (2024), 2856–2882, obtains ideal formulations for discretized outer functions and composite expressions. Remark 7.3 uses logarithmic SOS2 encodings and gives \(d\lceil\log_2n\rceil\) binaries for the stated grid setting. This is additional prior art for the formulation side. [Open paper](https://arxiv.org/abs/2310.07168); local source: `literature/papers/he2024-mip-relaxations-in-factorable-programming/fulltext.md`.

Gupte, Ahmed, Dey, and Cheon, *Relaxations and discretizations for the pooling problem*, JGO 67 (2017), 631–669, Section 4, distinguishes finite-value variable restrictions from discretizing consistency at pools. It discusses unary and binary encodings and logarithmic SOS1 formulations. Its discretizations there are primarily restrictions for obtaining primal bounds, so they do not by themselves prove the candidate outer-approximation theorem. [Open author manuscript](https://www.pure.ed.ac.uk/ws/files/136877755/4883.pdf); local source: `literature/papers/gupte2017-relaxations-and-discretizations-for-the/fulltext.md`.

## Defensible positioning

Do not claim invention of logarithmic discretization, local McCormick errors, shared product encodings, interaction-graph vertex covers, or midpoint/parity obstructions. A defensible candidate claim is: **the fractional vertex-cover number exactly determines the leading integer-dimension cost of uniform approximation of a vector of bilinear products, even when arbitrary convex lifts are allowed.**

The vector-valued graph and componentwise error requirement are material. A scalar sum of bilinear terms can exhibit cancellation, so this claim must not be advertised as an unrestricted complexity formula for arbitrary scalar quadratic objectives. Likewise, this is representation complexity, not a running-time lower bound for global optimization.

The universal lower bound is more consequential than the allocation algorithm: grid allocation follows by taking logarithms of standard edgewise error requirements, whereas proving that arbitrary convex formulations cannot bypass the allocation law rules out a whole class of improvements. The parity extension strengthens that statement further by excluding compression through unbounded general integers.

## Search record and limitations

Queries included combinations of bilinear, fractional vertex cover, fractional matching, discretization, vertex cover, precision allocation, minimum binary variables, approximation error, convex covering number, Huchette thesis, approximate MICP representability, and epsilon/MICP rank. Searches located no direct match for the fractional-cover precision theorem. Primary full texts of Beach Part II, Beach–Hildebrand–Huchette, Huchette's thesis, Bärmann et al., and Ploussard et al. were downloaded to `/tmp/minlp-graph-novelty/` and searched. Repository full texts were inspected for He–Tawarmalani, Gupte et al., and Lubin–Zadik–Vielma. The last paper's approximation-related passages concern representability motivation or number-theoretic approximation, rather than quantitative bilinear relaxation rank. An RWTH engineering-discretization thesis appeared in searches, but its download returned an HTML challenge instead of a PDF; it was not treated as fully reviewed. Search absence is evidence for continued investigation, not proof of novelty.
