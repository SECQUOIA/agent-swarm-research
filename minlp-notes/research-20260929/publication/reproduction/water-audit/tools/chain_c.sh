#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Chain C (one process at a time): re-runs of chain-B items that failed because of
# this track's first path-fix bug; the implied_06 round test; then the bound audit's
# class (i) and emfl certificates and the two independent audit checks.
OUT="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/water-audit
R=$OUT/tools/run.sh
WD="${_PUBLIC_REPO}"-clean/research-20260929
W=$WD/open-instances-wave2/waterno2
CS=$W/cellslopes/logs
D=$W/data
V1=$WD/reviews/waterno2-verification
RC=$WD/reviews/waterno2-recheck
SR=$WD/reviews/waterno2-sepbranch-review-checks
CR=$WD/reviews/waterno2-cellslopes-review-checks
BA=$WD/bound-audit
BV=$WD/reviews/bound-audit-verification
BR=$WD/reviews/bound-audit-recheck
# --- waterno2 re-runs
$R w06_vimplied $V1 clean "python3 vimplied.py 6 2"
$R w06_ind_verify_cert3 $SR clean "python3 ind_verify.py $W/sepbranch/logs/cert3.pkl $V1/logs/my_implied_06.json logs/repro_ind_verify_cert3.json"
$R w06_terminal_allT $SR clean "python3 terminal_allT.py 2 3 4 6 9 12 18 24"
$R w06_point_check_cert3 $SR clean "python3 point_check.py $W/sepbranch/logs/cert3.pkl $D/waterno2_06.p1.sol $D/waterno2_06.p2.sol $D/waterno2_06.p3.sol $D/waterno2_06.p4.sol"
$R w06_ind_verify_certB $CR clean "python3 ind_verify_cs.py $CS/certB_cert.pkl.gz logs/repro_ind_verify_certB.json $CS/certB_verify.json"
$R w06_point_check_certB $CR clean "python3 point_check_cs.py $CS/certB_cert.pkl.gz logs/repro_ind_verify_certB.json $D/waterno2_06.p4.sol $D/waterno2_06.p3.sol $D/waterno2_06.p2.sol $D/waterno2_06.p1.sol"
$R wall_vsum $V1 clean "python3 vsum.py 6 9 12 18 24"
$R wall_vsum2 $RC clean "python3 vsum2.py 9 12 18 24"
$R w06_implied_r1 $W clean "python3 implied.py 6 logs/repro_implied_06_r1.json 1"
# --- bound audit (author code): evaluation and verification of the class (i) points
I_PTS="ghg_3veh.p2 glider100.p2 methanol50.p4 nuclear14.p3 smallinvDAXr1b150-165.p2 smallinvDAXr1b200-220.p2 smallinvDAXr2b150-165.p2 smallinvDAXr2b200-220.p2 sssd20-04persp.p3 sssd22-08persp.p3 sssd22-08persp.p4 sssd25-04persp.p3 sssd25-08persp.p3 sssd25-08persp.p4"
CERT_PTS="nd_netgen-2000-3-4-b-a-ns_7.p2 watercontamination0303.p2 topopt-cantilever_60x40_50.p4 topopt-cantilever_60x40_50.p5 emfl050_3_3.p2 emfl050_3_3.p4 emfl050_3_3.p5 emfl050_5_5.p4 emfl050_5_5.p5 emfl050_5_5.p6 emfl100_3_3.p3 emfl100_3_3.p4 emfl100_5_5.p2"
RMEVAL=""; for t in $I_PTS $CERT_PTS; do RMEVAL="$RMEVAL logs/eval/$t.json"; done
RMVER=""; for t in $I_PTS; do RMVER="$RMVER logs/verify/$t.json logs/verify/$t.center.sol"; done
$R audit_evaluate $BA clean "rm -f $RMEVAL && python3 audit.py evaluate --jobs 1"
$R audit_verify $BA clean "rm -f $RMVER && python3 audit.py verify --jobs 1"
$R audit_cert_linear $BA clean "python3 cert_linear.py watercontamination0303.p2"
$R audit_cert_ndnetgen $BA clean "python3 cert_ndnetgen.py nd_netgen-2000-3-4-b-a-ns_7.p2"
$R audit_cert_socp_emfl050_3_3 $BA clean "python3 cert_socp.py emfl050_3_3 emfl050_3_3.p2 emfl050_3_3.p4 emfl050_3_3.p5"
$R audit_cert_socp_emfl050_5_5 $BA clean "python3 cert_socp.py emfl050_5_5 emfl050_5_5.p4 emfl050_5_5.p5 emfl050_5_5.p6"
$R audit_cert_socp_emfl100_3_3 $BA clean "python3 cert_socp.py emfl100_3_3 emfl100_3_3.p3 emfl100_3_3.p4"
$R audit_cert_socp_emfl100_5_5 $BA clean "python3 cert_socp.py emfl100_5_5 emfl100_5_5.p2"
$R audit_cert_topopt_p4 $BA clean "python3 cert_topopt.py topopt-cantilever_60x40_50.p4"
$R audit_cert_topopt_p5 $BA clean "python3 cert_topopt.py topopt-cantilever_60x40_50.p5"
$R audit_sanity $BA clean "python3 sanity.py"
$R audit_classify $BA clean "python3 audit.py classify && python3 summarize.py > logs/summary.txt && python3 make_tables.py > logs/tables.md"
$R audit_check_display $BA clean "python3 check_display.py"
# --- first independent verification of the audit (own code; data fetched from minlplib.org)
$R auditv_fetch $BV clean "python3 fetch.py ghg_3veh:p1,p2 nd_netgen-2000-3-4-b-a-ns_7:p1,p2 watercontamination0303:p1,p2 glider100:p1,p2 topopt-cantilever_60x40_50:p4,p5 emfl050_3_3:p1,p2 && python3 fetch.py methanol50:p3,p4 nuclear14:p3 sssd20-04persp:p2,p3 smallinvDAXr1b150-165:p2 && python3 fetch.py smallinvDAXr1b200-220:p2"
$R auditv_evalpt $BV clean "python3 evalpt.py ghg_3veh.p1 ghg_3veh.p2 glider100.p1 glider100.p2 nd_netgen-2000-3-4-b-a-ns_7.p2 emfl050_3_3.p2 methanol50.p4 nuclear14.p3 sssd20-04persp.p3 smallinvDAXr1b150-165.p2 smallinvDAXr1b200-220.p2 topopt-cantilever_60x40_50.p4 topopt-cantilever_60x40_50.p5"
for t in ghg_3veh.p2 glider100.p2 methanol50.p4 nuclear14.p3 smallinvDAXr1b200-220.p2; do
  $R auditv_kraw_$t $BV clean "python3 run_kraw.py $t"
done
$R auditv_kraw_sssd20-04persp.p3 $BV clean "python3 run_kraw.py sssd20-04persp.p3 --snap 1e-12"
$R auditv_nd_netgen_exact $BV clean "python3 nd_netgen_exact.py p2"
$R auditv_water_exact $BV clean "python3 water_exact.py p2"
$R auditv_topopt_exact $BV clean "python3 topopt_exact.py p5 p4"
$R auditv_emfl_cert $BV clean "python3 emfl_cert.py emfl050_3_3 '' p2=10.40173793 p1=10.40173999 p3=10.40180127 BARON=10.40173793 LINDO=10.40173999 SCIP=10.40173999"
$R auditv_sanity $BV clean "python3 sanity.py"
# --- recheck of the audit (own code)
$R auditr_fetch $BR clean "python3 fetch.py sssd22-08persp:p2,p3,p4 sssd25-04persp:p2,p3 sssd25-08persp:p2,p3,p4 smallinvDAXr2b150-165:p2 smallinvDAXr2b200-220:p2 && python3 fetch.py emfl050_5_5:p1,p2,p3,p4,p5,p6 emfl100_3_3:p1,p2,p3,p4 emfl100_5_5:p1,p2 sssd20-04persp:p2,p3"
$R auditr_cmp $BR clean "for f in data/*.osil; do cmp \$f ~/.cache/minlplib/minlplib/osil/\$(basename \$f) && echo same \$f; done; for f in data/*.sol; do if [ -e ../../bound-audit/sol/\$(basename \$f) ]; then cmp \$f ../../bound-audit/sol/\$(basename \$f) && echo same \$f; fi; done; cp ~/.cache/minlplib/minlplib/osil/emfl050_3_3.osil data/ && echo 'copied cached emfl050_3_3.osil (undocumented step)'"
$R auditr_sssd_exact $BR clean "python3 sssd_exact.py sssd20-04persp.p3=347716.8909 sssd22-08persp.p4=508748.972 sssd22-08persp.p3=508748.972 sssd25-04persp.p3=300186.8048 sssd25-08persp.p4=472098.947 sssd25-08persp.p3=472098.947"
$R auditr_smallinv_exact $BR clean "python3 smallinv_exact.py smallinvDAXr2b150-165.p2=88.1049355 smallinvDAXr2b200-220.p2=156.604269"
$R auditr_emfl050_3_3 $BR clean "python3 emfl_bounds.py emfl050_3_3 p2=10.40173793 p1=10.40173999 p3=10.40180127 BARON=10.40173793 LINDO=10.40173999 SCIP=10.40173999 ANTIGONE=0.11605443 COUENNE=0.11888301 audit_LB_log=10.401752131628136 audit_UB_log=10.401752131870378 verifier_LB=10.40175213184103 verifier_UB=10.40175213184476"
$R auditr_emfl050_5_5 $BR clean "python3 emfl_bounds.py emfl050_5_5 p1=18.91343512 p2=18.91340776 p3=18.91351081 p4=18.90919208 p5=18.90550915 p6=18.91165289 BARON=18.91340776 LINDO=18.91340776 SCIP=18.91340776 ANTIGONE=0.11665436 COUENNE=0.11671129 audit_LB_text=18.9136329529 audit_LB_table=18.91363295295 audit_LB_log=18.913632952947218 audit_UB_log=18.91363295628119"
$R auditr_emfl100_3_3 $BR clean "python3 emfl_bounds.py emfl100_3_3 p1=18.13262446 p2=18.13265099 p3=18.13198244 p4=18.13236088 BARON=18.13262446 LINDO=18.13262446 SCIP=18.13262446 ANTIGONE=0.11740779 COUENNE=0.11813405 audit_LB_text=18.1326531194 audit_LB_table=18.13265311949 audit_LB_log=18.132653119485887 audit_UB_log=18.132653124322964"
$R auditr_emfl100_5_5 $BR clean "python3 emfl_bounds.py emfl100_5_5 p1=32.63818348 p2=32.63783605 BARON=32.63818348 LINDO=32.63818348 SCIP=32.63818206 ANTIGONE=0.10044302 COUENNE=0 audit_LB_text=32.6381903514 audit_UB_text=32.6381903547 audit_LB_table=32.63819035138 audit_LB_log=32.63819035137867 audit_UB_log=32.63819035472937"
$R auditr_crosseval $BR clean "python3 crosseval.py"
$R auditr_sanity $BR clean "python3 sanity.py"
