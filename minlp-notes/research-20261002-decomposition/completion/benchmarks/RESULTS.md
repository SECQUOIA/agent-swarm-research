# Phase-two benchmark results

Each run used a two-second cooperative solve budget, a five-second hard
worker deadline, a separate five-second proof replay deadline, one thread,
and a 512 MiB address-space cap. Full inputs, refusals, source snapshots,
and resource failures are retained. The initial baseline pilot is excluded.

| Lane | Runs | Completed certificates | Valid replays, including partial bounds | Exact reference enclosures |
| --- | ---: | ---: | ---: | ---: |
| baseline | 16 | 12 | 16 | 9 |
| completed_grid | 16 | 12 | 16 | 9 |
| completed_exact | 9 | 9 | 9 | 9 |
| completed_recourse | 11 | 10 | 11 | 8 |
| completed_constraints | 16 | 13 | 15 | 14 |
| completed_sets | 5 | 5 | 5 | 5 |

A valid replay at a resource limit certifies the reported bounds; it does
not mean that the requested gap or exact result was reached. Input screening
of the three continuous public QPLIB cases is separate from these run counts.

| Case | Lane | Method | Status | Gap | Solve + replay wall seconds | Peak solver/checker RSS, KiB |
| --- | --- | --- | --- | --- | ---: | ---: |
| fresh_path_5 | baseline | grid | certified | 0.000407 | 0.247 | 25920/21848 |
| fresh_width2_6 | baseline | grid | certified | 0.000366 | 0.245 | 25412/22112 |
| fresh_mixed_5 | baseline | grid | certified | 0.000651 | 0.256 | 25752/21924 |
| random_tree_7 | baseline | grid | certified | 0.000497 | 0.290 | 25468/22024 |
| fresh_path_5_shuffled | baseline | grid | certified | 0.000407 | 0.265 | 25988/21904 |
| fresh_path_16 | baseline | grid | certified | 0.000313 | 0.323 | 25752/22468 |
| fresh_path_32 | baseline | grid | certified | 0.00058 | 0.479 | 25796/23316 |
| fresh_path_64 | baseline | grid | certified | 3.08e-05 | 1.439 | 28468/27732 |
| random_tree_32 | baseline | grid | certified | 0.000387 | 0.446 | 25712/23276 |
| rational_face | baseline | grid | certified | 0 | 0.224 | 25520/21688 |
| mixed_rational | baseline | grid | certified | 0.000488 | 0.245 | 26084/21768 |
| flat_diagonal | baseline | grid | certified | 0 | 0.245 | 25800/21612 |
| affine_star_5_shuffled | baseline | grid | time_limit | 0.296 | 4.659 | 34500/33532 |
| affine_star_17_shuffled | baseline | grid | table_limit | 14.2 | 4.600 | 30356/31064 |
| QPLIB_3852 | baseline | grid | table_limit | 454 | 0.759 | 31188/25272 |
| QPLIB_5881 | baseline | grid | table_limit | 4.48e+04 | 0.461 | 26268/23116 |
| fresh_path_5 | completed_grid | grid | certified | 0.000407 | 0.256 | 26460/23740 |
| fresh_width2_6 | completed_grid | grid | certified | 0.000366 | 0.246 | 25764/22384 |
| fresh_mixed_5 | completed_grid | grid | certified | 0.000651 | 0.230 | 25744/22148 |
| random_tree_7 | completed_grid | grid | certified | 0.000497 | 0.209 | 25444/22272 |
| fresh_path_5_shuffled | completed_grid | grid | certified | 0.000407 | 0.239 | 25728/22168 |
| fresh_path_16 | completed_grid | grid | certified | 0.000313 | 0.344 | 25800/22824 |
| fresh_path_32 | completed_grid | grid | certified | 0.00058 | 0.492 | 25764/23616 |
| fresh_path_64 | completed_grid | grid | certified | 3.08e-05 | 1.268 | 28568/28140 |
| random_tree_32 | completed_grid | grid | certified | 0.000387 | 0.457 | 25760/23560 |
| rational_face | completed_grid | grid | certified | 0 | 0.215 | 25388/21784 |
| mixed_rational | completed_grid | grid | certified | 0.000488 | 0.254 | 25448/21912 |
| flat_diagonal | completed_grid | grid | certified | 0 | 0.246 | 25760/22004 |
| affine_star_5_shuffled | completed_grid | grid | time_limit | 0.296 | 4.914 | 33240/33768 |
| affine_star_17_shuffled | completed_grid | grid | table_limit | 14.2 | 4.254 | 29936/31404 |
| QPLIB_3852 | completed_grid | grid | table_limit | 454 | 0.730 | 34428/25732 |
| QPLIB_5881 | completed_grid | grid | table_limit | 4.48e+04 | 0.988 | 26792/24168 |
| fresh_path_5 | completed_exact | exact | exact | 0 | 0.537 | 26476/25904 |
| fresh_width2_6 | completed_exact | exact | exact | 0 | 1.143 | 28040/27916 |
| fresh_mixed_5 | completed_exact | exact | exact | 0 | 0.313 | 25892/23296 |
| rational_face | completed_exact | exact | exact | 0 | 0.249 | 25824/21892 |
| mixed_rational | completed_exact | exact | exact | 0 | 0.227 | 25492/22268 |
| flat_diagonal | completed_exact | exact | exact | 0 | 0.206 | 25404/22032 |
| clipped_response | completed_exact | exact | exact | 0 | 0.248 | 25752/22028 |
| false_growth_trap | completed_exact | exact | exact | 0 | 0.368 | 25768/22620 |
| rational_face | completed_exact | exact_no_convex | exact | 0 | 0.199 | 25780/21772 |
| clipped_response | completed_recourse | recourse_convex | certified | 0.000732 | 0.260 | 27796/23000 |
| piecewise_convex_1 | completed_recourse | recourse_convex | certified | 0.000412 | 0.205 | 26048/22636 |
| piecewise_convex_100 | completed_recourse | recourse_convex | certified | 0.000412 | 0.244 | 25756/22712 |
| affine_star_5_shuffled | completed_recourse | recourse | exact | 0 | 0.238 | 26308/22432 |
| affine_star_17_shuffled | completed_recourse | recourse | exact | 0 | 0.326 | 25948/22760 |
| singular_affine | completed_recourse | recourse | exact | 0 | 0.235 | 26060/22336 |
| clipped_response | completed_recourse | recourse | exact | 0 | 0.199 | 26012/22308 |
| dense_mincut_7 | completed_recourse | recourse | exact | 0 | 0.224 | 26084/22308 |
| dense_mincut_33 | completed_recourse | recourse | epsilon_optimal | 0.000977 | 0.451 | 25768/23664 |
| fresh_path_5 | completed_recourse | recourse | exact | 0 | 0.224 | 26308/22748 |
| QPLIB_3852 | completed_recourse | recourse | table_limit | 454 | 1.089 | 37892/35608 |
| disconnected_tu_optima | completed_constraints | constrained | epsilon | 0.000732 | 0.197 | 24888/23444 |
| disconnected_tu_optima | completed_constraints | constrained_union | epsilon | 0.000732 | 0.175 | 22568/22392 |
| disconnected_tu_optima | completed_constraints | constrained_exact | limit | 2.79e-09 | 1.199 | 34728/33660 |
| disconnected_tu_optima | completed_constraints | constrained_exact_union | exact | 0 | 0.248 | 23280/23064 |
| network_mixed_5 | completed_constraints | constrained | epsilon | 0.000977 | 0.164 | 22868/22520 |
| network_mixed_5 | completed_constraints | constrained_exact | exact | 0 | 0.500 | 24856/24560 |
| ordered_nonconvex_4 | completed_constraints | constrained | epsilon | 0.000977 | 0.168 | 22628/22384 |
| ordered_nonconvex_4 | completed_constraints | constrained_exact | exact | 0 | 0.616 | 23800/23460 |
| weighted_integer_column | completed_constraints | constrained | epsilon | 0.000488 | 0.164 | 22464/22244 |
| weighted_integer_column | completed_constraints | constrained_exact | exact | 0 | 0.188 | 22984/22660 |
| large_equality_energy_full | completed_constraints | constrained | epsilon | 0.000954 | 1.008 | 26944/23252 |
| large_equality_energy_full | completed_constraints | constrained_exact | limit | 2.27e-10 | 3.497 | 28816/24552 |
| large_equality_energy_projected | completed_constraints | constrained | epsilon | 0.000977 | 0.149 | 22344/22252 |
| large_equality_energy_projected | completed_constraints | constrained_exact | exact | 0 | 0.247 | 23128/22964 |
| infeasible_flow | completed_constraints | constrained | infeasible | — | 0.148 | 22364/22356 |
| invalid_tu_input | completed_constraints | constrained | input_rejected | — | 0.072 | 22148/— |
| flat_diagonal | completed_sets | diagonal_set | certified | 0 | 0.236 | 26488/21996 |
| tilted_disconnected | completed_sets | diagonal_set | certified | 0 | 0.215 | 25712/21900 |
| false_growth_trap | completed_sets | diagonal_set | certified | 0 | 0.336 | 25452/22008 |
| fresh_path_5 | completed_sets | diagonal_set | certified | 0 | 0.245 | 25820/21920 |
| endpoint_branch_8 | completed_sets | endpoint_set | certified | 0 | 0.193 | 25820/22080 |
