# Source records for the aggregation audit

Access date: 2026-10-03. This records retrieval and reading scope; the
mathematical comparisons appear only in
[`aggregation-prior.md`](aggregation-prior.md). Web retrieval provided the
listed full text or publisher metadata. This subtask did not save additional
PDF copies or compute archival hashes.

| Suggested key | Publication/version metadata | Primary URL and inspected scope |
|---|---|---|
| `BoydVandenberghe2004` | Stephen Boyd and Lieven Vandenberghe, *Convex Optimization*, Cambridge University Press, 2004 | [Author's PDF](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf): §§5.1.2–5.1.3 and 5.2.2, printed pp. 216–217 and 225; [author's book page](https://web.stanford.edu/~boyd/cvxbook/) for metadata/access provenance. |
| `DeyMunozSerrano2022` | SIAM J. Optim. 32(2), 659–686, published online 2022-04-28 | [Author's published PDF](https://www2.isye.gatech.edu/~sdey30/AggQuadratics.pdf): introduction, §2.3, Proposition 2.5, and conclusion; [publisher metadata](https://doi.org/10.1137/21M1428583). |
| `BlekhermanDeySun2024` | SIAM J. Optim. 34(1), 98–126, published online 2024-01-05 | [Publisher page](https://doi.org/10.1137/22M1528215): abstract and metadata only. No theorem-by-theorem full-text audit. |
| `GleixnerEtAl2017` | J. Global Optim. 67, 731–757 (2017); online 2016-06-17 | [Author preprint dated 2016-03-07](https://optimization-online.org/wp-content/uploads/2016/03/5356.pdf): §2, Theorem 1, Remarks 2–3; [publisher metadata](https://doi.org/10.1007/s10898-016-0450-4). |
| `MisenerFloudas2012` | Math. Program. 136, 155–182 (2012); online 2012-05-24 | [Publisher abstract and metadata](https://doi.org/10.1007/s10107-012-0555-6); [author's project description](https://wp.doc.ic.ac.uk/rmisener/project/global-optimisation-of-mixed-integer-nonlinear-programs/). Full paper not audited. |
| `GarloffSmith2008` | Konstanzer Schriften in Mathematik und Informatik 250, June 2008; existing bibliography entry also gives conference publication | [Institutional deposited report](https://d-nb.info/1097267482/34): title page, introduction, §5. Existing bibliography key can be reused. |
| `CookEtAl2009SafeCuts` | INFORMS J. Comput. 21(4), 641–649, published online 2009-06-29 | [Publisher page](https://doi.org/10.1287/ijoc.1090.0324): abstract and bibliographic metadata only. Detailed safe-row formulas are attributed to the Eifler–Gleixner text below. |
| `EiflerGleixner2024` | SIAM J. Optim. 34(1), 742–763, online 2024-02-16; inspected preprint arXiv:2303.12365v2, submitted 2023-07-25 | [Versioned full text](https://arxiv.org/html/2303.12365v2): §§2.1–2.5, especially Lemmas 1 and 3 and Corollary 2; [publisher metadata](https://doi.org/10.1137/23M156046X). The HTML rendering also displays a later manuscript header date; version and journal dates above follow the arXiv version label and publisher record. |

Suggested exact BibTeX additions follow. `GarloffSmith2008` already exists and
should not be duplicated. These records are supplied for the bibliography
owner; this file is not an additional bibliography loaded by the paper.

```bibtex
@book{BoydVandenberghe2004,
  author = {Stephen Boyd and Lieven Vandenberghe},
  title = {Convex Optimization},
  publisher = {Cambridge University Press},
  year = {2004},
  url = {https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf}
}

@article{DeyMunozSerrano2022,
  author = {Santanu S. Dey and Gonzalo Mu{\~n}oz and Felipe Serrano},
  title = {On Obtaining the Convex Hull of Quadratic Inequalities via Aggregations},
  journal = {SIAM Journal on Optimization},
  volume = {32},
  number = {2},
  pages = {659--686},
  year = {2022},
  doi = {10.1137/21M1428583},
  url = {https://www2.isye.gatech.edu/~sdey30/AggQuadratics.pdf}
}

@article{BlekhermanDeySun2024,
  author = {Grigoriy Blekherman and Santanu S. Dey and Shengding Sun},
  title = {Aggregations of Quadratic Inequalities and Hidden Hyperplane Convexity},
  journal = {SIAM Journal on Optimization},
  volume = {34},
  number = {1},
  pages = {98--126},
  year = {2024},
  doi = {10.1137/22M1528215}
}

@article{GleixnerEtAl2017,
  author = {Ambros M. Gleixner and Timo Berthold and Benjamin M{\"u}ller and Stefan Weltge},
  title = {Three enhancements for optimization-based bound tightening},
  journal = {Journal of Global Optimization},
  volume = {67},
  pages = {731--757},
  year = {2017},
  doi = {10.1007/s10898-016-0450-4},
  url = {https://optimization-online.org/wp-content/uploads/2016/03/5356.pdf},
  note = {Theorem locators refer to the March 7, 2016 author manuscript}
}

@article{MisenerFloudas2012,
  author = {Ruth Misener and Christodoulos A. Floudas},
  title = {Global optimization of mixed-integer quadratically-constrained quadratic programs ({MIQCQP}) through piecewise-linear and edge-concave relaxations},
  journal = {Mathematical Programming},
  volume = {136},
  pages = {155--182},
  year = {2012},
  doi = {10.1007/s10107-012-0555-6}
}

@article{CookEtAl2009SafeCuts,
  author = {William Cook and Sanjeeb Dash and Ricardo Fukasawa and Marcos Goycoolea},
  title = {Numerically Safe {Gomory} Mixed-Integer Cuts},
  journal = {INFORMS Journal on Computing},
  volume = {21},
  number = {4},
  pages = {641--649},
  year = {2009},
  doi = {10.1287/ijoc.1090.0324}
}

@article{EiflerGleixner2024,
  author = {Leon Eifler and Ambros Gleixner},
  title = {Safe and Verified {Gomory} Mixed-Integer Cuts in a Rational Mixed-Integer Program Framework},
  journal = {SIAM Journal on Optimization},
  volume = {34},
  number = {1},
  pages = {742--763},
  year = {2024},
  doi = {10.1137/23M156046X},
  eprint = {2303.12365},
  archivePrefix = {arXiv},
  url = {https://arxiv.org/html/2303.12365v2},
  note = {Theorem locators refer to version 2}
}
```
