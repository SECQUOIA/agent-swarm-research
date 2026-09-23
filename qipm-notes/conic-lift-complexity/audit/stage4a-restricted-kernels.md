# Stage 4A author audit: restricted kernels

Authored `sections/08c-restricted-kernels.tex`. No changes to main.tex,
macros.tex, or bibliography.bib. The standalone section compiles to seven
pages with system pdflatex; its isolated build has only expected unresolved
cross-references/citations, which the integrated build must resolve.

## Source dispositions

1. `workbench/active/2026-09-04-projective-contact-q3-embedding-bound.md`:
   verified and incorporated in Theorem `thm:projective-phase`. Includes
   nowhere-zero hypothesis, phase lifting using integral rather than
   mod-two H1, injectivity from strict diagonal, characteristic-class
   staircase, product bound, sharp four-channel projective-plane count,
   explicit normalized Veronese/stereographic construction, and full-cone
   nonrepresentability scope distinction. The characteristic-class facts
   are classical; the factorization-to-embedding step is identified as
   the additional step. No literature-wide priority claim is made.
2. `workbench/active/2026-09-04-product-q3-near-saturation-boundaries.md`:
   all four distinctive results verified and included. Local chart and
   finite-sample saturation, partition-separated exact singleton/pair
   count, functional-inertia bound, overlapping positive block-additive
   chordal class, and a constructive all-source-dependent channel are
   retained. The text explicitly corrects a potentially overbroad reading
   of the source sentence that the paired count is optimal in the whole
   multiscale chordal class: the inertia bound depends on e, and the exact
   paired optimality theorem requires the positive block-additive
   summand condition. No unrestricted k>=3 exact count is asserted.
3. `workbench/active/2026-09-04-q1-curvature-flat-residual-nullity.md`:
   orientation theorem, exact squared-kernel column rank, factor-count
   penalty, standard-slice barrier implication, and canonical-splitting
   limitation all verified and incorporated. The old globally persistent
   saturated-row extraction consequence b+j is subsumed by the earlier
   manuscript's unrestricted global full-row product selected-rank
   theorem giving 2b in this critical real-PSD cap; since j<=b, it is not
   repeated as a separate weaker theorem. The flat-residual theorem itself
   is NOT subsumed, since it needs only continuity and concerns kernels
   with zero mixed contact curvature.

## Additional development completed

Theorem `thm:rado-nullity` proves a stronger general criterion in terms of
actual column ranks rho_a. It needs no continuity and works on arbitrary
nonempty product index sets. For every nonempty J require

  1 + sum_{a in J}(rho_a-1) > (R+1)(|J|-1)/2.

Then some simultaneous primal tuple has total nullity at least b. The
proof includes the independent-transversal ingredient by induction,
including its reduction from infinite vector sets. This also makes clear
that individual dual columns need not all be nonzero; each source merely
has nonzero column rank. Under a uniform rho lower bound the sufficient
condition is (R+3)(b-1)<2b rho. For squared slack rho=s(s+3)/2, so the
improved condition is (R+3)(b-1)<b s(s+3), strictly stronger than using
only Borsuk--Ulam's rho>=s. The b=1 condition is automatic.

Checks performed:
- Exact direct-sum identity for block-supported ranges in Rado proof.
- Column-space relation dimension at most j-1 (not a pairwise-intersection
  shortcut); exact product rank for squared kernels since constants occur.
- Odd/even squared-kernel rank s+s(s+1)/2.
- Uniform cap arithmetic at both endpoints j=1 and j=b.
- Characteristic-class maximal index j*=2^ceil(log2 r)-r; product monomial.
- Veronese scale, chord-map inner product, and nowhere-zero property.
- Finite evaluation matrix supplies a precise functional-inertia proof.
- All-source dependence shown by a tangent variation, avoiding an
  unexplained assertion about a generic basis.
- Labels and citations use existing macros; isolated LaTeX build succeeds.

## Literature and BibTeX suggestions

Primary browsing performed on 2026-09-20:
- Publisher full article for Fawzi (2019),
  https://link.springer.com/article/10.1007/s10107-018-1233-0 ; confirms
  Math. Program.175 (2019),109--118 (online year2018), and full-cone
  nonrepresentability. arXiv https://arxiv.org/abs/1610.04901 also checked.
- Primary full text https://arxiv.org/html/1407.4095 and publisher
  https://link.springer.com/article/10.1007/s10107-015-0922-1 for ordinary
  rank versus PSD rank. The workbench link 1407.4308 is not the correct
  identifier for this paper; use 1407.4095.
- Rado publisher metadata
  https://academic.oup.com/qjmath/article-abstract/os-13/1/83/1520949
  verifies author, title, volume, pages and DOI. Full original article is
  paywalled; our proof is self-contained and does not claim inspection of
  inaccessible theorem text.
- Milnor--Stasheff original book scan at
  https://people.math.harvard.edu/~dafr/M392C-2012/Readings/MilnorStasheff.pdf
  opens as an excerpt; full MIT and Rochester mirrors failed in browser.
  No unverified page/theorem locator is cited. The tangent identity and
  inverse total class used here are derived in the proof.
- Hatcher2002 already in bibliography supplies covering-space and
  Borsuk--Ulam background. Targeted searches for the projective Lorentz
  factorization/embedding bridge did not identify a matching prior
  theorem, but this alone is not treated as proof of novelty.

Please add these entries (or reconcile keys with other authors' entries):

```bibtex
@book{MilnorStasheff1974,
 author={Milnor, John W. and Stasheff, James D.},
 title={Characteristic Classes},
 series={Annals of Mathematics Studies}, volume={76},
 publisher={Princeton University Press}, year={1974}
}
@article{Rado1942,
 author={Rado, Richard}, title={A theorem on independence relations},
 journal={The Quarterly Journal of Mathematics},
 volume={os-13}, number={1}, pages={83--89}, year={1942},
 doi={10.1093/qmath/os-13.1.83}
}
@article{Fawzi2019SOC,
 author={Fawzi, Hamza},
 title={On representing the positive semidefinite cone using the second-order cone},
 journal={Mathematical Programming}, volume={175},
 pages={109--118}, year={2019}, doi={10.1007/s10107-018-1233-0}
}
@article{FGPRT2015,
 author={Fawzi, Hamza and Gouveia, Jo{\~a}o and Parrilo, Pablo A. and
         Robinson, Richard Z. and Thomas, Rekha R.},
 title={Positive semidefinite rank},
 journal={Mathematical Programming}, volume={153},
 pages={133--177}, year={2015}, doi={10.1007/s10107-015-0922-1}
}
```

The user-required five independent reviews remain the next stage-level
step; this author audit is not a substitute for them.
