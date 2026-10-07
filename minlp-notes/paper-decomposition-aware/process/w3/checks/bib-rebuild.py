"""W3 rebuild of references.bib (bib group).

Input : process/w3/checks/bib-references-before-w3.bib (copy of references.bib before W3)
        process/w1/lit-core.bib, process/w1/lit-ext.bib (provenance comments directly above entries)
Output: references.bib, sorted by key, each entry preceded by its own provenance comment.
"""
import importlib.util
import re

spec = importlib.util.spec_from_file_location('prov', 'process/w3/checks/bib-provenance.py')
prov = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prov)

before = prov.bib_entries('process/w3/checks/bib-references-before-w3.bib')
core = prov.entries_with_comments('process/w1/lit-core.bib')
ext = prov.entries_with_comments('process/w1/lit-ext.bib')

# ---------------------------------------------------------------- deletions
DUPLICATES = {  # deleted key -> key that stays
    'BhathenaEtAl2026': 'BhathenaEtAl2026Graphs',
    'Khajavirad2026Poly': 'Khajavirad2026PolyBox',
    'Khajavirad2026SDP': 'Khajavirad2026SparseSDP',
    'ChervetGrappeRobert2018': 'ChervetGrappeRobert2021 (also deleted; uncited)',
}
UNUSED = [  # never cited and not proposed for citation by any W2 report
    'BajajHasan2020Dynamic', 'BertsimasIancuParrilo2010', 'Bodlaender1996', 'BonnansIoffe1995',
    'BurkeFerris1991', 'BurkeMore1988', 'ChervetGrappeRobert2021', 'FacchineiFischerKanzow1998',
    'HorstTuy1996', 'HuyJeyakumarLee2006', 'JeyakumarLeeDinh2004', 'KelnerNikolova2007',
    'Kolmogorov2006', 'Lasserre2001', 'Lovasz1983', 'Majthay1971', 'ParisotEtAl2014',
    'PicardRatliff1980', 'Pinar2004', 'Rockafellar1970', 'RoseTarjanLueker1976', 'Schrijver2000',
    'SpjotvoldEtAl2006', 'SpjotvoldTondelJohansen2005', 'StaibJegelka2020', 'SunEtAl2012',
    'Wright1993', 'Zhang2000', 'Zhang2005Schur',
]
DELETE = set(DUPLICATES) | set(UNUSED)

# ---------------------------------------------------------------- arXiv preprints
# key -> arXiv identifier as printed (version suffix where the paper cites numbered
# statements of the preprint or where the year refers to a revised version)
ARXIV = {
    'BhathenaEtAl2026Graphs': '2603.02103',
    'BienstockChen2024': '2411.11722',
    'BurerNatarajanWillemsen2026v3': '2504.03996v3',
    'DelPia2026Jacobi': '2607.29386',
    'DelPiaKhajavirad2026': '2609.35595v1',
    'DongLuo2018': '1811.08122',
    'GomezHan2025': '2209.13161v2',
    'Khajavirad2026PolyBox': '2604.25033v2',
    'Khajavirad2026SparseSDP': '2601.18545',
    'Lokshtanov2015': '1511.00310',
}


def fix_arxiv(key, text):
    text = re.sub(r'\n\s*primaryClass\s*=\s*\{[^}]*\},?', '', text)
    text = re.sub(r',?\n\s*note\s*=\s*\{[^}]*\}', '', text)
    text = text.rstrip()
    assert text.endswith('\n}'), key
    text = text[:-2].rstrip().rstrip(',')
    return text + ',\n  howpublished  = {arXiv:%s}\n}' % ARXIV[key]


entries = {k: v for k, v in before.items() if k not in DELETE}
for k in ARXIV:
    entries[k] = fix_arxiv(k, entries[k])

# arXiv lists the authors as Han, Gomez
entries['GomezHan2025'] = entries['GomezHan2025'].replace(
    'author        = {G{\\\'o}mez, Andr{\\\'e}s and Han, Shaoning}',
    'author        = {Han, Shaoning and G{\\\'o}mez, Andr{\\\'e}s}')
assert 'Han, Shaoning and G' in entries['GomezHan2025']

# ---------------------------------------------------------------- corrected entries
entries['Bach2018Isotonic'] = r"""@inproceedings{Bach2018Isotonic,
  author    = {Bach, Francis},
  title     = {Efficient algorithms for non-convex isotonic regression through submodular optimization},
  booktitle = {Advances in Neural Information Processing Systems 31 (NeurIPS 2018)},
  publisher = {Curran Associates},
  year      = {2018},
  url       = {https://proceedings.neurips.cc/paper/2018/hash/6ea9ab1baa0efb9e19094440c317e21b-Abstract.html}
}"""

entries['Edmonds1970'] = r"""@incollection{Edmonds1970,
  author    = {Edmonds, Jack},
  title     = {Submodular functions, matroids, and certain polyhedra},
  booktitle = {Combinatorial Structures and Their Applications (Proceedings of the Calgary International Conference, Calgary, Alberta, 1969)},
  editor    = {Guy, Richard and Hanani, Haim and Sauer, Norbert and Sch{\"o}nheim, Johanan},
  pages     = {69--87},
  publisher = {Gordon and Breach},
  address   = {New York},
  year      = {1970},
  note      = {Reprinted in \emph{Combinatorial Optimization -- Eureka, You Shrink!}, Lecture Notes in Computer Science 2570, Springer, 2003, pp.~11--26, \doi{10.1007/3-540-36478-1_2}}
}"""

entries['Korhonen2021'] = r"""@inproceedings{Korhonen2021,
  author    = {Korhonen, Tuukka},
  title     = {A Single-Exponential Time 2-Approximation Algorithm for Treewidth},
  booktitle = {2021 IEEE 62nd Annual Symposium on Foundations of Computer Science (FOCS)},
  pages     = {184--192},
  year      = {2022},
  doi       = {10.1109/FOCS52979.2021.00026}
}"""

entries['GartnerJaggiMaria2012'] = r"""@article{GartnerJaggiMaria2012,
  author  = {G{\"a}rtner, Bernd and Jaggi, Martin and Maria, Cl{\'e}ment},
  title   = {An exponential lower bound on the complexity of regularization paths},
  journal = {Journal of Computational Geometry},
  volume  = {3},
  number  = {1},
  pages   = {168--195},
  year    = {2012},
  doi     = {10.20382/jocg.v3i1a9}
}"""

entries['Garloff1986'] = r"""@incollection{Garloff1986,
  author    = {Garloff, J{\"u}rgen},
  title     = {Convergent bounds for the range of multivariate polynomials},
  booktitle = {Interval Mathematics 1985},
  editor    = {Nickel, Karl},
  series    = {Lecture Notes in Computer Science},
  volume    = {212},
  pages     = {37--56},
  publisher = {Springer},
  address   = {Berlin},
  year      = {1986},
  doi       = {10.1007/3-540-16437-5_5}
}"""

entries['Topkis1998'] = r"""@book{Topkis1998,
  author    = {Topkis, Donald M.},
  title     = {Supermodularity and Complementarity},
  publisher = {Princeton University Press},
  address   = {Princeton, NJ},
  year      = {1998}
}"""

entries['HunkenschroderEtAl2026'] = re.sub(
    r',\n\s*note\s*=\s*\{[^}]*\}', '', entries['HunkenschroderEtAl2026'])
# plainnat lowercases the letter after the opening parenthesis; protect it
entries['HunkenschroderEtAl2026'] = entries['HunkenschroderEtAl2026'].replace(
    '{(Near)-Optimal', '{({Near})-Optimal')
assert '({Near})' in entries['HunkenschroderEtAl2026']

# ---------------------------------------------------------------- new entries (verified in W3)
NEW = {
'NagarajanEtAl2019': (r"""@article{NagarajanEtAl2019,
  author  = {Nagarajan, Harsha and Lu, Mowen and Wang, Site and Bent, Russell and Sundar, Kaarthik},
  title   = {An adaptive, multivariate partitioning algorithm for global optimization of nonconvex programs},
  journal = {Journal of Global Optimization},
  volume  = {74},
  number  = {4},
  pages   = {639--675},
  year    = {2019},
  doi     = {10.1007/s10898-018-00734-1}
}""", "% W3: Crossref; read by R7 (local package, Alg. 1 and 4, pp. 9--13)."),
'GupteKosterKuhnke2022': (r"""@inproceedings{GupteKosterKuhnke2022,
  author    = {Gupte, Akshay and Koster, Arie M. C. A. and Kuhnke, Sascha},
  title     = {An Adaptive Refinement Algorithm for Discretizations of Nonconvex {QCQP}},
  booktitle = {20th International Symposium on Experimental Algorithms (SEA 2022)},
  editor    = {Schulz, Christian and U{\c{c}}ar, Bora},
  series    = {Leibniz International Proceedings in Informatics (LIPIcs)},
  volume    = {233},
  pages     = {24:1--24:14},
  publisher = {Schloss Dagstuhl -- Leibniz-Zentrum f{\"u}r Informatik},
  year      = {2022},
  doi       = {10.4230/LIPIcs.SEA.2022.24}
}""", "% W3: DataCite record of the DOI (authors, title, LIPIcs 233, 24:1--24:14, editors); read by R7 (local package, pp. 5--8)."),
'KosterKuhnke2019': (r"""@article{KosterKuhnke2019,
  author  = {Koster, Arie M. C. A. and Kuhnke, Sascha},
  title   = {An adaptive discretization algorithm for the design of water usage and treatment networks},
  journal = {Optimization and Engineering},
  volume  = {20},
  number  = {2},
  pages   = {497--542},
  year    = {2019},
  doi     = {10.1007/s11081-018-9413-6}
}""", "% W3: Crossref; meta."),
'CifuentesParrilo2016': (r"""@article{CifuentesParrilo2016,
  author  = {Cifuentes, Diego and Parrilo, Pablo A.},
  title   = {Exploiting Chordal Structure in Polynomial Ideals: A {Gr{\"o}bner} Bases Approach},
  journal = {SIAM Journal on Discrete Mathematics},
  volume  = {30},
  number  = {3},
  pages   = {1534--1570},
  year    = {2016},
  doi     = {10.1137/151002666}
}""", "% W3: Crossref; read (arXiv:1411.1745v2, journal reference SIDMA 30(3), Example 1.1: Subset Sum as\n% quadratic equations on a path)."),
'EdmondsKarp1972': (r"""@article{EdmondsKarp1972,
  author  = {Edmonds, Jack and Karp, Richard M.},
  title   = {Theoretical Improvements in Algorithmic Efficiency for Network Flow Problems},
  journal = {Journal of the ACM},
  volume  = {19},
  number  = {2},
  pages   = {248--264},
  year    = {1972},
  doi     = {10.1145/321694.321699}
}""", "% W3: Crossref; meta (cited by the recourse group in W3)."),
'CookKochSteffyWolter2013': (r"""@article{CookKochSteffyWolter2013,
  author  = {Cook, William and Koch, Thorsten and Steffy, Daniel E. and Wolter, Kati},
  title   = {A hybrid branch-and-bound approach for exact rational mixed-integer programming},
  journal = {Mathematical Programming Computation},
  volume  = {5},
  number  = {3},
  pages   = {305--344},
  year    = {2013},
  doi     = {10.1007/s12532-013-0055-6}
}""", "% W3: Crossref; meta."),
'KordaMagronRiosZertuche2025': (r"""@article{KordaMagronRiosZertuche2025,
  author  = {Korda, Milan and Magron, Victor and R{\'\i}os-Zertuche, Rodolfo},
  title   = {Convergence rates for sums-of-squares hierarchies with correlative sparsity},
  journal = {Mathematical Programming},
  volume  = {209},
  number  = {1--2},
  pages   = {435--473},
  year    = {2025},
  doi     = {10.1007/s10107-024-02071-6}
}""", "% W3: Crossref; meta."),
'WangMagronLasserre2021': (r"""@article{WangMagronLasserre2021,
  author  = {Wang, Jie and Magron, Victor and Lasserre, Jean-Bernard},
  title   = {{TSSOS}: A Moment-{SOS} Hierarchy That Exploits Term Sparsity},
  journal = {SIAM Journal on Optimization},
  volume  = {31},
  number  = {1},
  pages   = {30--58},
  year    = {2021},
  doi     = {10.1137/19M1307871}
}""", "% W3: Crossref; meta."),
'KolmogorovPockRolinek2016': (r"""@article{KolmogorovPockRolinek2016,
  author  = {Kolmogorov, Vladimir and Pock, Thomas and Rolinek, Michal},
  title   = {Total Variation on a Tree},
  journal = {SIAM Journal on Imaging Sciences},
  volume  = {9},
  number  = {2},
  pages   = {605--636},
  year    = {2016},
  doi     = {10.1137/15M1010257}
}""", "% W3: Crossref; meta."),
'KuricAhmetspahicPock2024': (r"""@article{KuricAhmetspahicPock2024,
  author  = {Kuric, Muhamed and Ahmetspahic, Jan and Pock, Thomas},
  title   = {Total Generalized Variation on a Tree},
  journal = {SIAM Journal on Imaging Sciences},
  volume  = {17},
  number  = {2},
  pages   = {1040--1077},
  year    = {2024},
  doi     = {10.1137/23M1556915}
}""", "% W3: Crossref; meta."),
'Vorobev1962': (r"""@article{Vorobev1962,
  author  = {Vorob'ev, N. N.},
  title   = {Consistent families of measures and their extensions},
  journal = {Theory of Probability and Its Applications},
  volume  = {7},
  number  = {2},
  pages   = {147--163},
  year    = {1962},
  doi     = {10.1137/1107014}
}""", "% W3: Crossref; meta."),
'NeumaierShcherbina2004': (r"""@article{NeumaierShcherbina2004,
  author  = {Neumaier, Arnold and Shcherbina, Oleg},
  title   = {Safe bounds in linear and mixed-integer linear programming},
  journal = {Mathematical Programming},
  volume  = {99},
  number  = {2},
  pages   = {283--296},
  year    = {2004},
  doi     = {10.1007/s10107-003-0433-3}
}""", "% W3: Crossref; meta."),
'Kearfott1996': (r"""@book{Kearfott1996,
  author    = {Kearfott, R. Baker},
  title     = {Rigorous Global Search: Continuous Problems},
  series    = {Nonconvex Optimization and Its Applications},
  volume    = {13},
  publisher = {Kluwer Academic Publishers},
  address   = {Dordrecht},
  year      = {1996},
  doi       = {10.1007/978-1-4757-2495-0}
}""", "% W3: Crossref (title, author, year, series); series volume 13 from publisher and catalogue records; meta."),
'HojnyEtAl2025': (r"""@misc{HojnyEtAl2025,
  author        = {Hojny, Christopher and Besan{\c{c}}on, Mathieu and Bestuzheva, Ksenia and Borst, Sander and Dion{\'\i}sio, Jo{\~a}o and others},
  title         = {The {SCIP} {Optimization} {Suite} 10.0},
  year          = {2025},
  eprint        = {2511.18580},
  archivePrefix = {arXiv},
  howpublished  = {arXiv:2511.18580}
}""", "% W3: arXiv API record (v1, 2025-11-23; 34 authors, first five listed); meta."),
'Herrmann2026': (r"""@misc{Herrmann2026,
  author        = {Herrmann, Anton},
  title         = {Integer Quadratic Programming is {W[1]}-Hard Parameterized by the Number of Variables},
  year          = {2026},
  eprint        = {2608.17818},
  archivePrefix = {arXiv},
  howpublished  = {arXiv:2608.17818}
}""", "% W3: arXiv API record (v1, 2026-08-18); meta."),
'DellEtAl2014': (r"""@article{DellEtAl2014,
  author  = {Dell, Holger and Husfeldt, Thore and Marx, D{\'a}niel and Taslaman, Nina and Wahl{\'e}n, Martin},
  title   = {Exponential Time Complexity of the Permanent and the {Tutte} Polynomial},
  journal = {ACM Transactions on Algorithms},
  volume  = {10},
  number  = {4},
  pages   = {21:1--21:32},
  year    = {2014},
  doi     = {10.1145/2635812}
}""", "% W3: Crossref (pages 1--32); article number 21 from the publisher record; meta."),
'CyganEtAl2015': (r"""@book{CyganEtAl2015,
  author    = {Cygan, Marek and Fomin, Fedor V. and Kowalik, {\L}ukasz and Lokshtanov, Daniel and Marx, D{\'a}niel and Pilipczuk, Marcin and Pilipczuk, Micha{\l} and Saurabh, Saket},
  title     = {Parameterized Algorithms},
  publisher = {Springer},
  address   = {Cham},
  year      = {2015},
  doi       = {10.1007/978-3-319-21275-3}
}""", "% W3: Crossref; meta."),
'Novak1988': (r"""@book{Novak1988,
  author    = {Novak, Erich},
  title     = {Deterministic and Stochastic Error Bounds in Numerical Analysis},
  series    = {Lecture Notes in Mathematics},
  volume    = {1349},
  publisher = {Springer},
  address   = {Berlin},
  year      = {1988},
  doi       = {10.1007/BFb0079792}
}""", "% W3: Crossref; series volume from the publisher record; meta."),
'HornJohnson2012': (r"""@book{HornJohnson2012,
  author    = {Horn, Roger A. and Johnson, Charles R.},
  title     = {Matrix Analysis},
  edition   = {Second},
  publisher = {Cambridge University Press},
  address   = {Cambridge},
  year      = {2012},
  doi       = {10.1017/CBO9781139020411}
}""", "% W3: Crossref and publisher page (second edition, print publication 22 October 2012); meta.\n% Section 7.8 (determinant inequalities) not checked against the book."),
'BurgisserCucker2013': (r"""@book{BurgisserCucker2013,
  author    = {B{\"u}rgisser, Peter and Cucker, Felipe},
  title     = {Condition: The Geometry of Numerical Algorithms},
  series    = {Grundlehren der mathematischen Wissenschaften},
  volume    = {349},
  publisher = {Springer},
  address   = {Berlin},
  year      = {2013},
  doi       = {10.1007/978-3-642-38896-5}
}""", "% W3: Crossref; series volume from the publisher record; meta."),
'FullnerRebennack2022': (r"""@article{FullnerRebennack2022,
  author  = {F{\"u}llner, Christian and Rebennack, Steffen},
  title   = {Non-convex nested {Benders} decomposition},
  journal = {Mathematical Programming},
  volume  = {196},
  number  = {1--2},
  pages   = {987--1024},
  year    = {2022},
  doi     = {10.1007/s10107-021-01740-0}
}""", "% W3: Crossref; meta."),
}
for k, (text, _) in NEW.items():
    assert k not in entries, k
    entries[k] = text

# ---------------------------------------------------------------- provenance comments
COMMENT = {}
for k in entries:
    c = core.get(k) or ext.get(k)
    if c:
        COMMENT[k] = '\n'.join(c)
MERGED = {  # keys in both W1 files: keep both records
    'BienstockMunoz2018': ('% Crossref; read (arXiv:1501.00288v15 in the local package, titled "LP approximations to\n'
                           '% mixed-integer polynomial optimization problems": Theorems 4 and 15, Appendix A, pp. 24--25).\n'
                           '% The SIOPT text (also 30 pages) was not accessible; Appendix A there is not confirmed.'),
    'Rosenberg1972': '% Crossref; read (numdam scan, Lemma and Proposition 1, p. 96).',
    'WainwrightJaakkolaWillsky2005': '% Crossref; read (author PDF, Proposition 1 "tree agreement", p. 3702; Sec. V.A, pp. 3705--3706).',
    'Laurent2009': '% Crossref; read (author PDF, Section 8). Crossref year 2008 (online); the IMA volume is dated 2009.',
    'Vavasis1990': '% Crossref; read (Cornell TR 90-1099, Feb. 1990, Sec. 2, via OCR of the eCommons scan; see Vavasis1990TR).\n% Cited by Khajavirad (2026, Prop. 2) for the minimum-face positive-definiteness argument.',
    'Schrijver1986': '% Standard book record (publisher catalogue); meta. Section 6.1 (continued fractions); corollary number\n% not checked. Chapter 19 treats total unimodularity.',
}
COMMENT.update(MERGED)
R7_AUDIT = '% Crossref (R7 audit of cited DOIs, W2); meta.'
for k in ['BelottiEtAl2013', 'BestuzhevaEtAl2023', 'BodlaenderKoster2010', 'ChenEtAl2006',
          'FuriniEtAl2019', 'MisenerFloudas2014', 'QiuYildirim2024', 'TawarmalaniSahinidis2005',
          'VigerskeGleixner2018']:
    assert k not in COMMENT, k
    COMMENT[k] = R7_AUDIT
for k in ['GareyJohnson1979', 'KollerFriedman2009', 'NemirovskiYudin1983']:
    assert k not in COMMENT, k
    COMMENT[k] = '% Standard book record (no DOI); meta.'
COMMENT['Korhonen2021'] = '% Crossref (pages 184--192; the FOCS 2021 proceedings appeared in February 2022); meta.'
COMMENT['Bach2018Isotonic'] = ('% [KB] NeurIPS 2018 proceedings (Section 4.3, p. 5). The proceedings BibTeX at\n'
                               '% proceedings.neurips.cc has an empty page field, so no pages are given.')
COMMENT['Edmonds1970'] = ('% Original publication: pp. 69--87, Gordon and Breach 1970 (MR 0270945); editors from a library\n'
                          '% catalogue record. The LNCS 2570 reprint (pp. 11--26) was checked on Crossref.')
COMMENT['GartnerJaggiMaria2012'] = ('% [META] DOI and volume from the DOAJ record (Crossref has no record for this DOI).\n'
                                    '% Pages 168--195 from the arXiv journal reference of 0903.4817 and jocg.org (R7).')
COMMENT['GomezHan2025'] = ('% [AX][PDF] Author order as in the arXiv record (Han, Gomez); the title page of the PDF lists\n'
                           '% Gomez first. No journal version found on Crossref (2026-10-03).')
COMMENT['Garloff1986'] = ('% [CR][META] W3: editor from the Crossref book record; LNCS volume 212 from the publisher\n'
                          '% and catalogue records.')
COMMENT['Topkis1998'] = ('% [META] 1998 print edition, which has no DOI (10.1515/9781400822539 is the 2011 e-book).\n'
                         '% Theorem 2.7.6 cited via Bunton--Tabuada (2022, Theorem 4, p. 9).')
COMMENT['HunkenschroderEtAl2026'] = ('% Crossref (online 2026-03-18; volume and pages not assigned on 2026-10-03);\n'
                                     '% read (arXiv:2505.22212 version).')
for k, (_, c) in NEW.items():
    COMMENT[k] = c
missing = [k for k in entries if k not in COMMENT]
assert not missing, missing

HEADER = """\
% references.bib -- bibliography of "Decomposition-aware global optimization".
%
% Each entry is preceded by a comment recording how its metadata and content were checked.
% Two notations occur (from the two W1 literature reviews):
%   "Crossref; read (...)" / "meta" / "abstract": source of the metadata; "read" means the
%     primary text was read for the cited statement, "abstract" only the abstract, "meta"
%     metadata only.
%   "[CR]" Crossref, "[AX]" arXiv record, "[KB]" local knowledge-base text read, "[PDF]" PDF read,
%   "[META]" metadata only, "[SEC: ...]" content known only from the secondary source named.
% "W3" marks entries added or corrected in the third revision round (checked 2026-10-03).
%
% arXiv preprints are misc entries with howpublished = {arXiv:<id>}, because plainnat does not
% print the eprint field. A version suffix (vN) is given where the paper cites numbered
% statements of the preprint or where the year is that of a revised version.
"""

out = [HEADER]
for k in sorted(entries, key=str.lower):
    out.append(COMMENT[k] + '\n' + entries[k].strip() + '\n')
open('references.bib', 'w').write('\n'.join(out))
print('entries written:', len(entries), '| deleted:', len(DELETE), '| new:', len(NEW))
