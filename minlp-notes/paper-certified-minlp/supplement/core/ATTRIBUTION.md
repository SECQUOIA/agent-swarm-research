# Sources and attribution

The model files under `lab/instances/py`, the two source files under
`lab/instances/gms`, and `lab/instances/instancedata.csv` are from **MINLPLib: A
Library of Mixed-Integer and Continuous Nonlinear Programming Instances**,
maintained by Stefan Vigerske and the MINLPLib contributors:
https://www.minlplib.org/ and https://www.minlplib.org/download.html.

The official home and download pages were checked on 2026-09-13 and displayed
Creative Commons Attribution 4.0 International (CC BY 4.0):
https://creativecommons.org/licenses/by/4.0/ . Retain this attribution and the
notices embedded in individual source files when redistributing them. The source
files included here are unchanged from the locally frozen inputs identified by
the manifests. No claim is made that they match a future library download.
The model loader's documented dedenting operation acts in memory at load time.
GAMS scalar is the library's primary format; converted Pyomo expressions define
the exact loaded-tree semantics used for the bound certificates in this study.

The case-specific GAMS solver listings and compact output records are saved
outputs of the research runs. They are evidence, not vendor executables. The
checker and paper experiment scripts accompany the study for scientific review
and reproduction. External package licenses remain with those packages; install
them through their ordinary distribution channels. Gurobi, IPOPT, SCIP, GAMS,
or other solver binaries and licenses are not redistributed in these archives.

No local literature PDFs or proof-assistant dependency cache is included.
