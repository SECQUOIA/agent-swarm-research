# Licence-row check (helper agent; recorded by the lead reviewer)

The helper fetched each cited source with curl/WebFetch on 2026-10-04 and saved copies in
`sources/` (hashes in `sources/SHA256SUMS`). The harness prevented the helper from
writing this file; the lead copied its findings here and spot-checked the MATPOWER
LICENSE/manual 8.1 text, the Bitbucket SIF LICENSE, the MINLPLib footer and the control
`sources/MANIFEST.md` provenance lines 40-43.

| READINESS row | verdict | evidence |
|---|---|---|
| MINLPLib (R:159) | match | download.html footer: `License: CC-BY 4.0` (same footer on every page; no narrower scope). Saved earlier copy `minlplib-status/pages/site/download.html` is byte-identical. CC BY 4.0 s.3(a)(1) gives the attribution/change-notice duties. |
| QPLIB (R:160) | match | doc.html footer: "Website © 2017-2025 by Zuse Institute Berlin and GAMS. All rights reserved. … QPLIB is licensed under CC-BY 4.0." index.html adds a citation request ("When using QPLIB, please cite the article above"). |
| CUTEst/SIF (R:161) | cited files match; incomplete for our files | ralna/CUTEst and ralna/SIF LICENSE: 3-clause BSD, © 2000 Gould, Orban, Toint. But the four control SIF files (DTOC5, LUKVLE10, OPTCDEG2, OPTCNTRL) were downloaded from bitbucket.org/optrove/sif (control MANIFEST.md:40-43), whose LICENSE is "MIT License, Copyright (c) 2022 Nick Gould, Dominique Orban, Philippe Toint". The files are byte-identical to the ralna/SIF copies. HVYCRASH.SIF came from ralna/SIF. "Preserve problem-source credits" is a recommendation, not a licence term. |
| MATPOWER (R:162) | software matches; case-data sentence overstated | matpower.org/license: "3-clause BSD … beginning with MATPOWER 5.1". LICENSE and manual Section 1.2 (8.0b1 and 8.1 identical): "The MATPOWER case files … are not covered by the BSD license. In most cases, the data has either been included with permission or has been converted from data available from a public source." READINESS drops "In most cases". 8.0b1 is a beta; manual 8.1 (2025-07-12) is current. Section 1.3 asks publications using MATPOWER or its data files to cite MATPOWER. Saved case30/case39 headers credit their data sources but contain no licence/permission statement. |

Integration evidence: `integration/commands.md:95-107` names the URLs read but saved no copies or hashes of the licence pages.
