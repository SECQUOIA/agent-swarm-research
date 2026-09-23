# Stage 3 root proof investigation

Root read both complete canonical results on near-optimal response robustness
and dense-model surrogate screening. This records independent analysis during
authorship, not stage acceptance.

## Near-optimal projection

The threshold predicate needs a feasible stationary candidate on a measurement
fiber whose cost meets the budget. It does not need global comparison within
each measured fiber: existence of any qualifying point implies its global
fiber minimizer qualifies and has KKT multipliers; every accepted candidate
itself is feasible and under budget. Nominal v(x) still needs full global
comparison. This simplification is already present in the canonical source
and should be retained, not presented as new here.

A distinct arithmetic refinement follows from the stage 2 proof. Constant
local Q and local equality/inequality normals make local KKT inverses rational
constants. Shared normals may still depend polynomially on the leader, since
they enter the effective linear coefficient rather than the local KKT matrix.
In particular the criterion measurement equations T_j(x)z=t can move without
introducing variable local denominators. Local responses have bounded degree
independent of N/row counts at fixed input degree and structural dimensions.
Separate per-criterion QE gives polynomial-count families of bounded-degree
outputs, and a fixed number of subsequent QE/sampling steps preserves the
bound. The selected optimal leader and one adverse witness therefore share a
field of bounded degree. Many independently requested witnesses need not have
a bounded-degree common compositum. This is an algorithmic output-degree
statement, not an attainment claim. Author is independently assessing it.

## Dense screening

Checked the ellipsoid from the two variational inequalities: with p=Ey and
e=z-y, e'Qe+p'e<=0. Its signed output support gives the exact centers and
widths; substituting b=Qe_i gives gradient center ghat_i+p_i/2. The maximum
of p'Q^{-1}p on a fixed-dimensional compact cell occurs at vertices. The
strict gradient tests, weak coordinate tests, and relative-interior closure
refinements have the required signs and nonidentity conditions.

Exact recovery must use the true dense principal matrix Q_FF and every
original upper row. It solves at most M*3^t recovery LPs; preprocessing and
possible refinement are separate costs. A full guessed assignment can be
validated at cell vertices first, which resolves the source's conservative
ellipsoid example; a failed whole-cell check cannot exclude that assignment
on a smaller part of the cell.

For the perturbation neighborhood, root and author independently found the
same simplification: use the cover consisting of all affinely independent
subsets of at most r+1 cell vertices instead of constructing a triangulation.
Caratheodory proves coverage, overlaps are permitted by the main theorem, and
fixed r makes enumeration polynomial. Injective projection of the surrogate
response graph bounds the cell affine dimension by r. Each covering simplex
then has at most (r+1)q transition coordinates. The same positive vertex
margins and spectral norm bounds give the source radius and certificates.
This removes a construction dependency without making a new convexity claim.

## Primary-source comparison

Root directly opened Dantas--Gribonval arXiv v3
https://arxiv.org/html/1812.06635v3, including its introduction and Sections
II--III definitions. It explicitly combines fast structured approximate
dictionaries with screening safe for the original Lasso problem. The
nearby-model screening principle must therefore be attributed; the present
claim is the exact whole-cell bilevel recovery and its ambiguity parameter.
Also opened the primary Liu et al. proceedings record
https://proceedings.mlr.press/v32/liuc14.html and Arnström--Axehill
https://arxiv.org/abs/2003.07605 to confirm the cited antecedents and metadata.
These checks are bounded source comparison, not proof of novelty.

## Full draft reading

Root read the full stage 3 draft during authorship, including both positive-
budget nonattainment examples, the Max-Cut restriction, all enclosure signs,
the relative-interior closure proof, dense principal-matrix reconstruction,
explicit perturbation constants, simplex cover, and inner/outer value bounds.
The threshold proof, nominal/global comparison and per-criterion elimination
order are consistent. The one-witness field guarantee is properly limited.

Checked the positive-budget derivative lower bound on z<=a<1/3 and the
integral comparison establishing 4x+a_(rho+x)>a; the unconstrained infimum
therefore really is unattained. The convex fixed-normal proof repairs strict
sublevel points and uses the continuous unique nominal response at zero
budget, covering all boundary cases.

For screening, the advertised LP count excludes construction and screening.
Affine free-coordinate recovery uses true Q, and positive definiteness
handles a growing dense free set. Exact status overlap at zero-gradient
bounds loses no response. The perturbation radius bounds both response and
gradient changes by sigma/2 and has positive rational polynomial encoding.
The N=0 case is separately an upper LP. Both conservatism and moving-switch
examples support their stated limitations.

During authorship root sent three minor presentation requests: a missing
backslash before quad, clarify fixed depth of successive eliminations rather
than fixed total number of per-criterion calls, and say combining the two VI
inequalities instead of subtracting under the displayed signs. These do not
change a theorem. No additional substantive defect found in this reading.

## Additional bibliography finding during independent review

Minor root finding: the Arnström--Axehill work has a published journal version,
so the paper should cite that version rather than only the 2020 preprint.
Verified primary metadata: the author's publications page lists it in IEEE
Transactions on Automatic Control (2022), and the IEEE Control Systems Society
June 2022 contents digest, PDF page 3, confirms volume 67, issue 6, start page
2758 (next article starts 2771). The institutional postprint's search-indexed
cover supplies pp.2758--2770 and DOI 10.1109/TAC.2021.3090749. Direct institution
PDF access timed out and its record showed a bot challenge; no access is claimed
to that postprint. The accessible arXiv v2 supports the actual broad statement
used in our paper. Keep the inspected preprint provenance, but update the
bibliographic publication metadata after all five stage reviews are assessed.

Primary metadata URLs:
https://darnstrom.github.io/publications/
https://ieeecss.org/sites/ieeecss/files/documents/pcd/CSS_Publications_Content_Digest_062022_0.pdf
https://www.diva-portal.org/smash/get/diva2%3A1669297/FULLTEXT01.pdf
