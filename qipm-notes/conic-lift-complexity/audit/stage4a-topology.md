# Stage 4A: general-cone topology author audit

Author scope: `sections/08a-general-topology.tex` only. The parent integrates the section and bibliography. Existing sections, literature packages, and source catalog were not edited.

## Result and source disposition

| Workbench source (all dated 2026-09-04) | Disposition and manuscript location |
|---|---|
| `global-smooth-saturation-topology` | **Verified and included.** The C2 Hessian-diagonal argument and Parseval equality produce the abstract tangent splitting before Proposition `abstract-splitting-ranks`. Adams, Euler, and parallelizability consequences are retained or directly subsumed by the stronger C1 joint-cover theorem. No inference from ordinary lift existence to global selectors is made. |
| `rank-two-curvature-summand-topology` | **Verified and included/subsumed.** Rank-one/rank-two budget is explicit in Proposition `abstract-splitting-ranks`; the full unstable clutching criterion is displayed. Bounds for counts of blocks of dimension at least five and the special congruence obstruction follow directly from the displayed budget and total-rank identity; exact global cone-factor conclusions are strictly subsumed by `general-joint-cover`. Stable KO commentary is not a separate mathematical result needed after the exact clutching criterion. |
| `steenrod-effective-curvature-capacity` | **Verified with an independent proof; included/subsumed.** Every subset-sum restriction, the near-full rank, the effective-capacity count, its abstract sharpness, and the Radon–Hurwitz exceptions are explicit. The plane-field implication is proved directly by clutching; the middle-rank endpoint is excluded separately by Euler class. This avoids reliance on inaccessible book wording. The logarithmic asymptotic cone-cap implications and source regularity-premium corollaries are subsumed by the exact general-cone frontier. |
| `saturated-factor-submersion-obstruction` | **Verified and included.** Nonzero factors, exact quotient derivative rank, constant-rank patches, invariance of domain, and radial transversality are all proved in `general-joint-cover`. The same proof for an individually saturated channel is stated explicitly before `sphere-product-submersions`. |
| `saturated-block-submersion-rigidity` | **Verified and included/subsumed.** Independent primal/polar charts and the bi-C1 body application are explicit. Proper C1 maps are handled by a uniformly close smooth approximation, avoiding the need for a separate Earle–Eells theorem. Its elementary dimension bound is subsumed by the exact sphere-submersion pairs. |
| `joint-saturated-block-covering-rigidity` | **Verified and included.** The full abstract compact-contact-manifold theorem, zero-capacity channels, common-kernel proof, finite covering, and sphere/product-sphere profiles are proved. The conclusion is extended from equal sphere dimensions to arbitrary dimensions at least two by cohomology indecomposables. No product splitting of the covering is claimed. |
| `sphere-submersion-curvature-gap` | **Verified and included.** Classical individual submersion classification is proved from Browder and the two-row Serre sequence. The exact general proper-cone factor/dimension/ambient-barrier frontier is explicit. Ambient barriers are distinguished from barriers on a feasible slice. Grouped Lorentz upper bounds refer to the already proved construction. |
| `product-sphere-submersion-dimension-rigidity` | **Verified, with strengthened proof of its delicate case.** Formula `product-submersion-dimensions` is proved by the standard simply connected elliptic formal-dimension identity for targets of dimension at least three. For target S2, an explicit acyclic path model proves exclusion for source sphere dimension at least four, so no degree-one extension of the formal-dimension theorem is assumed. Remaining rational candidates are described as undecided by this argument, not as globally open problems. The jointly nonsingular result and arithmetic consequences are subsumed by the joint-cover theorem and the displayed individual dimension restriction. |
| `sphere-submersions-balanced-real-grassmannians` | **Verified and included.** All real orders and connected finite covers are covered in `balanced-real-submersion`, including disconnected fibers before lifting, positive-dimensional fibers, zero-dimensional fibers, circles, and the point. Euler characteristic is computed from Schubert cells rather than relying on an unverified Hopf–Samelson citation. The rank-five quadric exception is excluded with an explicit affine paving and its integral square relation. |

The conditioned/approximate source `robust-saturated-block-submersion` remains assigned to Stage 4C, not covered by this exact global section.

## New development and independent proof checks

1. The normalized-base theorem is valid for initially nonsmooth proper cones. Rank-full image patches first make the image relatively open in the topological base boundary; compactness gives surjectivity; only then is the whole boundary declared C1. Radial transversality is proved using an interior base point.
2. The common-kernel implication uses only independent fixed-variable derivatives and does not differentiate the contact correspondence.
3. Lemma `proper-base-domain` is a reusable local version for Stage 4B face-sharing. Component derivative rank cannot exceed the boundary dimension even before smoothness; joint injectivity forces every component to attain its rank. Whole-sphere domain would yield the prohibited finite cover. A proper open phase domain has zero ordinary source top class.
4. The abstract plane-field implication is reconstructed by clutching. A decomposition with smaller rank r lets both clutching classes land in SO(n-r) after conjugation inside SO(n). Their sum therefore gives a reduction supplying r fields. This proves existence of a frame, **not** triviality of the originally supplied rank-r summand. Middle-rank even spheres are handled by Euler class separately.
5. For the product-source submersion theorem, r>=3 gives simply connected fibers. The exact homotopy rank algebra and both parity branches have been checked. For r=2 and q>=4, the S2 model generators x2 and y3 must map to zero. The path model obtained by adjoining u1,v2 with Du=x and Dv=y-ux is acyclic; pullback leaves a polynomial v2 class, contradicting compact fiber cohomology. This resolves the repository proof's otherwise delicate degree-one issue without making an unverified nilpotent extension claim.
6. The balanced real Grassmannian positive-fiber argument uses Browder for arbitrary compact manifold fibers, not an assumed sphere fiber. A finite covering is handled independently when fiber dimension is zero. Its quadric has the closed filtration given by z0=0, then z1=0 (which forces z2=0), and a point in the residual CP1; successive open strata are C3,C2,C1,C0. Integral cohomology and primitivity of the hyperplane class are explained.
7. The general proper-cone barrier bound restricts an arbitrary ambient barrier to the product of two-dimensional interior-crossing linear sections. This gives an orthant barrier and is valid even without logarithmic homogeneity. It does not lower-bound arbitrary barriers on an affine feasible slice.

## Literature verification

- **Local catalog read:** packages for Steenrod 1951, Dibag 1976, Adams 1962, and Browder 1962 were metadata-only/unread; they were not treated as inspected full text and were not edited.
- **Adams 1962:** primary article scan retrieved at https://www.math.drexel.edu/~tyu/Math538/CH7.pdf. Theorem 1.1 and preceding Radon–Hurwitz formula inspected. Annals 75(3), 603–632; DOI 10.2307/1970213. This is the full article, not the distinct Topology or Bulletin announcement with the same title.
- **Steenrod:** book metadata and DOI verified, but full text was not accessible. The accessible original Steenrod–Whitehead article https://webhomes.maths.ed.ac.uk/~v1ranick/papers/steewhit.pdf, printed pp.58–59, states the plane-field consequence and cites book Theorems 27.16 and 40.11. We do not depend on its exact endpoint wording: the manuscript supplies the clutching proof and treats equality with Euler class. The manuscript cites the book generally, without pretending that the book theorem text was inspected.
- **Browder 1962:** author-uploaded primary full text at https://www.researchgate.net/publication/251964661_Fiberings_of_spheres_and_H-spaces_which_are_rational_homology_spheres inspected. Theorem 1 explicitly states homotopy types S1,S3,S7 for a connected polyhedral fiber in a sphere-total-space bundle. This published two-page announcement has a proof sketch and references the longer work; our use is clearly attributed.
- **Félix–Halperin–Thomas:** Springer author/title/year/series/DOI metadata verified at https://link.springer.com/book/10.1007/978-1-4613-0105-9. The formal-dimension identity is independently available in Kathryn Hess's author lecture notes https://homepages.math.uic.edu/~bshipley/Hess.Chicago.pdf, Theorem 2.4.3(1), printed p.21, explicitly citing FHT Theorem32.6. Hess Theorems2.2.1 and2.2.2, pp.13–15, state the fiber and fiber-square models and explicitly cite FHT Propositions15.5 and15.8. Those exact statements were inspected. The manuscript's r2 proof uses an explicit model rather than invoking a hidden degree-one extension.
- **Ehresmann:** primary NUMDAM record and scan https://www.numdam.org/item/SB_1948-1951__1__153_0/ verified. The accessible Bourbaki version is **1952**, Exposé24, pp.153–168. The often cited 1950 colloquium text is a different publication. Use the exact 1952 record below.
- **Grassmannian cells / Euler:** classical Schubert cell indexing is attributed to Milnor–Stasheff Section6; the signed-subset recurrence and resulting Euler formula are independently supplied. The quadric cell ranks are proved by explicit filtration, not assigned an unverified locator. The real homogeneous-space homotopy sequence uses the same standard SO facts already used in Section5.
- **Aubrun–La Piana–Müller-Hermes 2026:** primary https://arxiv.org/html/2606.27825v1 read. It asks for factorization of all positive linear maps through finite direct sums of Lorentz cones; those quantifiers differ from a single nonlinear smooth slack factorization with capacity equality. Existing parent key `ALM2026Lorentz` is used. No broad claim of literature priority is made.

## Suggested bibliography additions

Only keys not already added by the parent should be merged. Use published records below; the source URL accompanying Adams is an accessible scan.

```bibtex
@book{Steenrod1951,
 author={Steenrod, Norman}, title={The Topology of Fibre Bundles},
 series={Princeton Mathematical Series}, volume={14},
 publisher={Princeton University Press}, year={1951},
 doi={10.1515/9781400883875}}
@article{Adams1962,
 author={Adams, J. F.}, title={Vector Fields on Spheres},
 journal={Annals of Mathematics}, volume={75}, number={3},
 pages={603--632}, year={1962}, doi={10.2307/1970213},
 url={https://www.math.drexel.edu/~tyu/Math538/CH7.pdf}}
@article{Browder1962,
 author={Browder, William},
 title={Fiberings of spheres and {$H$}-spaces which are rational homology spheres},
 journal={Bulletin of the American Mathematical Society},
 volume={68}, number={3}, pages={202--203}, year={1962},
 doi={10.1090/S0002-9904-1962-10747-2}}
@book{FHT2001,
 author={F{\'e}lix, Yves and Halperin, Stephen and Thomas, Jean-Claude},
 title={Rational Homotopy Theory}, series={Graduate Texts in Mathematics},
 volume={205}, publisher={Springer}, year={2001},
 doi={10.1007/978-1-4613-0105-9}}
@incollection{Ehresmann1952,
 author={Ehresmann, Charles},
 title={Les connexions infinit{\'e}simales dans un espace fibr{\'e} diff{\'e}rentiable},
 booktitle={S{\'e}minaire Bourbaki : ann{\'e}es 1948/49--1950/51},
 series={S{\'e}minaire Bourbaki}, number={1}, note={Expos{\'e} 24},
 pages={153--168}, publisher={Soci{\'e}t{\'e} math{\'e}matique de France},
 year={1952}, url={https://www.numdam.org/item/SB_1948-1951__1__153_0/}}
@book{MS1974,
 author={Milnor, John W. and Stasheff, James D.},
 title={Characteristic Classes}, series={Annals of Mathematics Studies},
 volume={76}, publisher={Princeton University Press}, year={1974},
 doi={10.1515/9781400881826}}
```
