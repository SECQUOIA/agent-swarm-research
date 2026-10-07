# Reproduction / eg_disc2_s check (helper agent; recorded by the lead reviewer)

The harness prevented the helper from writing this file; the lead copied its findings.
Scripts and logs are in this directory. The lead separately re-ran two of the three smoke
checks (`../lead-smoke/`) and confirmed 3b in `result-map.json`.

## Verdicts
1. **Mapping and counts: pass.** From the 38 `cert_p*_c*.log` logs and the NPZs (numpy only):
   1,114,361 certified leaves, 0 failures, 38 chunks (4,5,6,7,7,5,3,1); 1,152,830 processed boxes
   (matches `rec_disc2_p*.log` and `disc2_9_p*.log`); every leaf index in exactly one chunk; all
   `ok`, margins > 0; reviewer `leaves_p*.npz` boxes bit-identical to the certified boxes. Interval
   samples A/B/C = 3,890 + 5,184 + 1,400 = 10,474, 10,404 distinct, all in parts 0 and 2-7.
   All 159 path references in the eg_disc2_s map entry exist with matching hashes. The 54 EG
   command records have unique ids, matching output hashes and existing inputs; commands match
   `run_cert.out`, `run_record.sh` and the review. 50 are marked "historical expensive command;
   do not repeat for packaging"; 4 stored-evidence checks are marked "run only in a disposable copy".
   (`verify_eg_counts.log`: PROBLEMS: none.)
2. **Manifest:** scopes updated (`finish_paths.py` SCOPES; `rebuild_manifest.py` EXTRA_FILES).
   `manifest.json` is stale as declared: 0 eg-recheck entries, no `extra_files`, 14 changed hashes
   (`manifest_staleness.log`). Ownership is contradictory: reproduction/report.md:371 and
   README.md:274 hand the rebuild to "the integrating agent"; READINESS.md:196-200 hands it to the
   package owner/user.
3. **Displays: pass.** README primals ≥ saved `.retry.sol` objectives: eg_int_s +9.1e-17,
   eg_disc_s +9.4e-17, eg_disc2_s +4.4e-17; displayed relative gaps ≈ 9.997e-10 ≤ 1e-9; all 9
   fractions in `logs/integration-r1-displays.json` hold. The eg_disc_s dual is 2.38e-16 above
   the producer's binary64 bound (valid only via the retry review's exact-decimal certification,
   `verify_disc_p1.log` 40573/40573); the README does not state this caveat.
4. **Relocated smoke: pass.** All three checks in `/tmp/agent-repro-eg-r2-KeujILsM` (OSIL
   SHA-256 8849e06b…3289 = pin; bwrap hid the checkout and cache; strace: 0 source-tree opens;
   2 cores, 1 thread): summary 1,114,361 / 0 (1.49 s); part 7 `recheck_leaves.py` 29/29,
   coverage True (2.76 s); `indep_repro.py 8` 64/64 (3.28 s). Outputs match the recorded ones
   apart from timings (`compare_smoke.log`: ALL MATCH).
5. **Stale text:** README:257 "110,676 of 979,044" is labelled historical; no "1.67%".

## Minor issues
- 1a: `record-p{k}` records list only `egbb.py` as input (also needed: OSIL,
  `open-instances-wave3/sol/eg_disc2_s.p1.sol`, `ev.py`, `egfast`/`egtm`); interval-sample
  records omit the OSIL and the `minF_p*.npy` files sample C needs (also absent from the map).
- 1b (informational): the eight `disc2_9_p*.npz` saved inputs are byte-identical (1,792-byte final
  checkpoints with empty queues); a one-line note would prevent confusion.
- 3b: the eg_disc_s "lower bound" evidence in `result-map.json` cites `disc9_p0.log`
  5.7605396106949955 (non-binding part); the binding bound is `disc9_p1.log` 5.760539610694994.
- 4a: `check_eg_relocated.py` rewrites `reproduction/logs/integration-r1-eg/*` and
  `integration-r1-eg-smoke.json` on every run, leaves ~120 MB in /tmp
  (`/tmp/repro-eg-integration-r1-81qsbigg` still exists), and README:293 does not name its
  bwrap/strace prerequisites.
