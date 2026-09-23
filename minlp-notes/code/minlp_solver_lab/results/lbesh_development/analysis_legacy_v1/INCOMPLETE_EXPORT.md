This export is incomplete. All 1,287 records passed the numerical audit with
zero warnings, and analysis.json was written, but CSV export then failed:
sorting an LP-exit dictionary containing both None and string keys raised
TypeError. Do not use the partial CSV files as a complete analysis package.
The repaired replay is analysis_legacy_v2. This directory is retained to
preserve the failed export and its recorded analyzer source hash.
