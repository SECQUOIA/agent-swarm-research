# Stage 4 literature evidence

The following primary passages were inspected for the vector arguments and their
prior-work positioning. Local summaries were used only to locate sources; PDF
text was read directly or freshly extracted. The audit is of the listed passages,
not a claim to have checked every result of each cited paper. Retrieval hashes
for newly downloaded material are in `stage4-retrievals.json`.

| Source and inspected version | Primary passage | Effect on manuscript |
| --- | --- | --- |
| Lyu, Hicks, Huchette, local arXiv:2304.14542v1, corresponding to Operations Research 74(1), 484–499 (2026) | [[lyu2026-building-formulations-for-piecewise-linear]] p.6-8, Section 3 and Proposition 1; original PDF title/version and merged SOS2 discussion | Shared-input breakpoint union and a common SOS2 encoding are explicitly prior work. Added version-specific locator note; the manuscript contribution remains the comparison against every convex integer lift and compact random access to potentially exponentially many knots. |
| Awerbuch–Kleinberg, author-hosted STOC 2004 paper | [Primary PDF](https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf), PDF p.4, Section 2.3, Propositions 2.2 and 2.4 and determinant replacement proof | Maximum-determinant exact spanners and determinant exchange with a linear optimizer are established. These remain credited; rational denominators and exact feasibility are proved locally for the graph compiler's interface. |
| Plevrakis–Hazan, published NeurIPS 2020 paper | [Proceedings PDF](https://proceedings.neurips.cc/paper_files/paper/2020/file/565e8a413d0562de9ee4378402d2b481-Paper.pdf), PDF p.8, Section 3.3; official proceedings BibTeX | The authors combine approximate optimization with the inherited spanner algorithm. Updated the bibliography to volume 33, pp.7637–7647, and changed the locator from preprint Section 3.2 to published Section 3.3. The manuscript does not claim a new general approximate-spanner principle. |
| Grötschel–Lovász–Schrijver, 1981 primary PDF cached locally | Published p.172, Definitions (5)–(7); p.177, Theorem (3.1); p.178, Corollaries (3.4)–(3.5) | Weak optimization compares with the actual body and permits distance error. The fixed-grid proof separately repairs that error. Polar and nonnegative anti-blocker equivalences are classical. Explicit inner balls, polynomial rational normals and the one-dimensional padding convention are retained. |
| Kelly–Maulloo–Tan, 1998 published PDF cached locally | Section 2, published p.239, the logarithmic NETWORK objective and proportional-fairness inequality (1) | The maximum-product first-order relation is established proportional fairness. The manuscript provides its elementary derivation for the stated unconditional body and does not claim that principle as new. |
| Ellenberg–Gijswijt, arXiv:1605.09223v1 cached locally, corresponding to Annals 2017 | PDF p.2-3, Theorem 4 and monomial-count proof | The imported bound is `3 m_((q-1)n/3)`. Substitution q=3 gives the stated cap estimate. Added exact version note for Theorem 4; the new application is only the graph-contact restriction. |
| Hartman, Pacific Journal of Mathematics 9(3), 1959, primary PDF cached locally | Published p.707, definition of a difference of convex functions; p.708, local/global framework | The convexification framework is classical. The manuscript proves its elementary quadratic domination and all graph-error and conditioning consequences without importing an unproved decomposition assertion. |
| Averkov–Weismantel, arXiv:1002.0948v2 cached locally, corresponding to Advances in Geometry 2012 | PDF p.1-2, definition of the mixed Helly number and Theorem 1.1 | The identity concerns finite convex-set intersection certificates, with explicit continuous-dimension factor. Added exact version note and retained the distinction from an error-preserving interval cover. |

The [Lyu publisher page](https://pubsonline.informs.org/doi/10.1287/opre.2023.0187)
confirms volume 74(1), 484–499 and January–February 2026 issue assignment (online
publication was April 24, 2025); the issue year is retained. The [Plevrakis–Hazan
proceedings page](https://proceedings.neurips.cc/paper/2020/hash/565e8a413d0562de9ee4378402d2b481-Abstract.html)
and its official BibTeX supplied the published metadata. The web text tool rejected
the BibTeX content type, but direct retrieval succeeded and is recorded. No
paywall or authentication barrier was bypassed.

Targeted online searches for `"curvature rank" "integer" convex graph
approximation` and `"noncommutative rank" "graph approximation" integer
dimension` produced no directly relevant new comparison theorem. Unrelated hits
were not cited, and absence from these searches is not evidence of priority.
Together with the earlier focused literature review, these checks support the
existing qualified nc-rank claim and the precise attribution of vector ingredients;
they do not certify exhaustive novelty.
