## Node counts and fitted slopes

| instance | pred. | setting | 1e-01 | 1e-02 | 1e-03 | 1e-04 | 1e-05 | 1e-06 | 1e-07 | tail slope | wide slope | nodes/decade |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| iso2 | log | default | 21 | 51 | 51 | 71 | 93 | 95* | 95* | 0.00 | 0.07 | 1 |
| iso2 | log | nopresolve | 21 | 51 | 51 | 71 | 93 | 95* | 95* | 0.00 | 0.07 | 1 |
| iso2 | log | noprop | 31 | 41 | 81 | 101 | 111 | 116* | 116* | 0.01 | 0.08 | 2 |
| iso2 | log | nocutoffprop | 31 | 41 | 81 | 101 | 111 | 116* | 116* | 0.01 | 0.08 | 2 |
| iso2 | log | noweakdual | 31 | 41 | 81 | 101 | 111 | 116* | 116* | 0.01 | 0.08 | 2 |
| iso2 | log | obbtoff | 21 | 51 | 51 | 71 | 93 | 95* | 95* | 0.00 | 0.07 | 1 |
| iso2 | log | obbtall | 11 | 21 | 31 | 41 | 51* | 51* | 51* | 0.00 | 0.07 | 0 |
| iso2 | log | lppoint | 11 | 21 | 141 | 167 | 169* | 169* | 169* | 0.00 | 0.14 | 0 |
| iso2 | log | midpoint | 41 | 137* | 137* | 137* | 137* | 137* | 137* | 0.00 | -0.00 | 0 |
| iso2 | log | widestbisect | 31 | 140 | 141* | 141* | 141* | 141* | 141* | 0.00 | 0.00 | 0 |
| iso2 | log | model | 15 | 25 | 33 | 45 | 55 | 63 | 75 | 0.06 | 0.09 | 9 |
| iso2 | log | modelnoprop | 23 | 35 | 49 | 55 | 73 | 79 | 93 | 0.05 | 0.08 | 9 |
| iso2 | log | toy | 55 | 65 | 81 | 93 | 101 | 117 | 157 | 0.10 | 0.07 | 28 |
| iso3 | log | default | 61 | 161 | 331 | 341* | 341* | 341* | 341* | -0.00 | 0.05 | 0 |
| iso3 | log | noprop | 91 | 191 | 471 | 591 | 661 | 861 | 881 | 0.05 | 0.10 | 90 |
| iso3 | log | model | 57 | 91 | 119 | 149 | 183 | 209 | 259 | 0.08 | 0.09 | 40 |
| iso3 | log | toy | 253 | 487 | 757 | 919 | 1125 | 1225 | 1335 | 0.04 | 0.08 | 103 |
| iso4 | log | default | 197 | 441 | 671 | 1191 | 2301 | 2921 | 3431 | 0.08 | 0.20 | 522 |
| iso4 | log | noprop | 239 | 491 | 1311 | 2181 | 3701 | 5331 | 7391 | 0.15 | 0.23 | 1802 |
| iso4 | log | model | 173 | 265 | 349 | 437 | 519 | 613 | 699 | 0.07 | 0.09 | 92 |
| iso4 | log | toy | 1433 | 2533 | 3223 | 3997 | 5165 | 5963 | 6637 | 0.05 | 0.09 | 727 |
| iso2c | log | default | 21 | 51 | 51 | 61 | 81 | 93* | 93* | 0.02 | 0.07 | 5 |
| iso2c | log | noprop | 21 | 31 | 108 | 109* | 109* | 109* | 109* | 0.00 | 0.08 | 0 |
| iso2c | log | model | 15 | 25 | 33 | 45 | 55 | 67 | 75 | 0.07 | 0.10 | 10 |
| iso2c | log | toy | 39 | 53 | 73 | 85 | 95 | 109 | 125 | 0.06 | 0.07 | 14 |
| isofbbt2 | n/a | default | 7 | 15* | 15* | 15* | 15* | 15* | 15* | 0.00 | -0.00 | 0 |
| isofbbt2 | n/a | nopresolve | 7 | 15* | 15* | 15* | 15* | 15* | 15* | 0.00 | -0.00 | 0 |
| isofbbt2 | n/a | noprop | 7 | 39* | 39* | 39* | 39* | 39* | 39* | -0.00 | -0.00 | 0 |
| isofbbt2 | n/a | nocutoffprop | 7 | 15* | 15* | 15* | 15* | 15* | 15* | 0.00 | -0.00 | 0 |
| isofbbt2 | n/a | noweakdual | 7 | 37* | 37* | 37* | 37* | 37* | 37* | 0.00 | -0.00 | 0 |
| isofbbt2 | n/a | obbtoff | 7 | 15* | 15* | 15* | 15* | 15* | 15* | 0.00 | -0.00 | 0 |
| isofbbt2 | n/a | obbtall | 7 | 9* | 9* | 9* | 9* | 9* | 9* | -0.00 | -0.00 | 0 |
| isofbbt2 | n/a | lppoint | 7 | 15 | 21 | 21 | 23 | 27* | 27* | 0.03 | 0.04 | 2 |
| isofbbt2 | n/a | midpoint | 7 | 15* | 15* | 15* | 15* | 15* | 15* | 0.00 | -0.00 | 0 |
| isofbbt2 | n/a | widestbisect | 9 | 13 | 13 | 13 | 13 | 23* | 23* | 0.14 | 0.06 | 6 |
| isofbbt2 | n/a | model | 7 | 15* | 15* | 15* | 15* | 15* | 15* | 0.00 | -0.00 | 0 |
| isofbbt2 | n/a | modelnoprop | 7 | 23 | 25 | 27 | 29 | 31 | 35 | 0.04 | 0.03 | 3 |
| isofbbt2 | n/a | toy | 13 | 35 | 37 | 39 | 45 | 49 | 51 | 0.03 | 0.04 | 3 |
| isofbbt2 | n/a | smallstreps | 7 | 15* | 15* | 15* | 15* | 15* | 15* | 0.00 | -0.00 | 0 |
| linediag2 | 0.5 | default | 97 | 741 | 3291 | 13751 | 25731 | 65701 |  | 0.33 | 0.46 | 24370 |
| linediag2 | 0.5 | nopresolve | 97 | 741 | 3291 | 13751 | 25731 | 65701 |  | 0.33 | 0.46 | 24370 |
| linediag2 | 0.5 | noprop | 131 | 1021 | 3431 | 14231 | 24541 | 65181 |  | 0.33 | 0.44 | 24404 |
| linediag2 | 0.5 | nocutoffprop | 131 | 941 | 3441 | 14001 | 25191 | 66661 |  | 0.33 | 0.44 | 25020 |
| linediag2 | 0.5 | noweakdual | 131 | 941 | 3441 | 14001 | 25191 | 66661 |  | 0.33 | 0.44 | 25020 |
| linediag2 | 0.5 | obbtoff | 97 | 741 | 3291 | 13751 | 25731 | 65701 |  | 0.33 | 0.46 | 24370 |
| linediag2 | 0.5 | obbtall | 69 | 193 | 961 | 4891 | 19521 | 43201 |  | 0.48 | 0.59 | 20104 |
| linediag2 | 0.5 | lppoint | 107 | 941 | 3531 | 12621 | 29531 | 67971 |  | 0.34 | 0.46 | 25772 |
| linediag2 | 0.5 | midpoint | 1011 | 3961 | 8131 | 19371 | 54161 |  |  | 0.42 | 0.39 | 22790 |
| linediag2 | 0.5 | widestbisect | 611 | 3291 | 15781 | 65951 |  |  |  | 0.62 | 0.66 | 50170 |
| linediag2 | 0.5 | model | 89 | 359 | 1115 | 3805 | 11893 | 38073 | >100000 | 0.50 | 0.51 | 29497 |
| linediag2 | 0.5 | modelnoprop | 111 | 383 | 1157 | 3821 | 11897 | 38089 | >100000 | 0.50 | 0.50 | 29419 |
| linediag2 | 0.5 | toy | 743 | 2729 | 9293 | 24475 | 79129 |  |  | 0.46 | 0.48 | 33406 |
| lineaxis2 | 0.5 | default | 267 | 788 | 3611 | 16541 | 35801 | >100000 |  | 0.36 | 0.53 | 25244 |
| lineaxis2 | 0.5 | nopresolve | 267 | 788 | 3611 | 16541 | 35801 | >100000 |  | 0.36 | 0.53 | 25244 |
| lineaxis2 | 0.5 | noprop | 270 | 834 | 12781 | 16471 | 35459 | >100000 |  | 0.34 | 0.49 | 24084 |
| lineaxis2 | 0.5 | nocutoffprop | 268 | 832 | 12751 | 16721 | 35482 | >100000 |  | 0.34 | 0.48 | 24192 |
| lineaxis2 | 0.5 | noweakdual | 268 | 832 | 12751 | 16721 | 35482 | >100000 |  | 0.34 | 0.48 | 24192 |
| lineaxis2 | 0.5 | obbtoff | 267 | 788 | 3611 | 16541 | 35801 | >100000 |  | 0.36 | 0.53 | 25244 |
| lineaxis2 | 0.5 | obbtall | 187 | 651 | 2324 | 8091 | 27484 | >100000 |  | 0.54 | 0.54 | 24637 |
| lineaxis2 | 0.5 | lppoint | 205 | 2051 | 3941 | 15271 | 39334 | >100000 |  | 0.45 | 0.44 | 32313 |
| lineaxis2 | 0.5 | midpoint | 441 | 2251 | 5391 | 22521 | 58771 |  |  | 0.54 | 0.51 | 27236 |
| lineaxis2 | 0.5 | widestbisect | 801 | 2871 | 14771 | 61151 |  |  |  | 0.62 | 0.63 | 46380 |
| lineaxis2 | 0.5 | model | 227 | 651 | 2427 | 7871 | 24349 | 88601 |  | 0.52 | 0.51 | 38128 |
| lineaxis2 | 0.5 | modelnoprop | 241 | 679 | 2659 | 8149 | 24853 | 90039 |  | 0.52 | 0.51 | 38718 |
| lineaxis2 | 0.5 | toy | 521 | 2351 | 9393 | 23253 | 78973 |  |  | 0.45 | 0.50 | 33154 |
| ring2 | 0.5 | default | 95 | 471 | 1761 | 5181 | 18291 | 56151 |  | 0.52 | 0.52 | 24870 |
| ring2 | 0.5 | nopresolve | 95 | 471 | 1761 | 5181 | 18291 | 56151 |  | 0.52 | 0.52 | 24870 |
| ring2 | 0.5 | noprop | 121 | 501 | 1561 | 6901 | 21231 | 67077 |  | 0.49 | 0.54 | 29096 |
| ring2 | 0.5 | nocutoffprop | 121 | 461 | 1518 | 6101 | 21331 | 66991 |  | 0.51 | 0.55 | 29290 |
| ring2 | 0.5 | noweakdual | 121 | 471 | 1561 | 6561 | 21214 | 67057 |  | 0.50 | 0.55 | 29160 |
| ring2 | 0.5 | obbtoff | 105 | 480 | 1751 | 5121 | 18097 | 56042 |  | 0.53 | 0.52 | 24950 |
| ring2 | 0.5 | obbtall | 121 | 401 | 1113 | 4403 | 14116 | 44872 | >100000 | 0.53 | 0.53 | 39923 |
| ring2 | 0.5 | lppoint | 99 | 438 | 1431 | 4881 | 18411 | 56675 |  | 0.53 | 0.53 | 25231 |
| ring2 | 0.5 | midpoint | 191 | 1681 | 6081 | 17181 | 51111 | >100000 |  | 0.46 | 0.48 | 37374 |
| ring2 | 0.5 | widestbisect | 361 | 1451 | 8991 | 31291 | >100000 |  |  | 0.58 | 0.65 | 38190 |
| ring2 | 0.5 | model | 99 | 353 | 1155 | 3769 | 11857 | 37439 | >100000 | 0.50 | 0.51 | 29236 |
| ring2 | 0.5 | modelnoprop | 111 | 341 | 1173 | 3777 | 11847 | 37261 | >100000 | 0.50 | 0.50 | 28916 |
| ring2 | 0.5 | toy | 221 | 1065 | 4241 | 12473 | 44705 | >100000 |  | 0.54 | 0.53 | 36849 |
| ring2 | 0.5 | noexpand | 1* | 1* | 1* | 1* | 1* | 1* | 1* | 0.00 | 0.00 | 0 |
| mccaxis2 | rule-dependent | default | 1 | 3 | 5 | 5 | 5 | 211 | 1041 | 1.34 | 0.47 | 528 |
| mccaxis2 | rule-dependent | nopresolve | 1 | 3 | 5 | 5 | 5 | 211 | 1041 | 1.34 | 0.47 | 528 |
| mccaxis2 | rule-dependent | noprop | 3 | 21 | 61 | 151 | 158 | 311 | 9141 | 0.85 | 0.40 | 3760 |
| mccaxis2 | rule-dependent | nocutoffprop | 1 | 3 | 19 | 69 | 621 | 1395 | 2795* | 0.33 | 0.61 | 1144 |
| mccaxis2 | rule-dependent | noweakdual | 3 | 21 | 61 | 221 | 221 | 401 | 9711 | 0.86 | 0.45 | 4341 |
| mccaxis2 | rule-dependent | obbtoff | 3* | 3* | 3* | 3* | 3* | 3* | 3* | -0.00 | -0.00 | 0 |
| mccaxis2 | rule-dependent | obbtall | 1 | 3 | 11 | 21 | 21 | 61 | 2521 | 0.94 | 0.44 | 1016 |
| mccaxis2 | rule-dependent | lppoint | 1 | 3* | 3* | 3* | 3* | 3* | 3* | -0.00 | -0.00 | 0 |
| mccaxis2 | rule-dependent | midpoint | 1 | 3 | 5* | 5* | 5* | 5* | 5* | -0.00 | 0.02 | 0 |
| mccaxis2 | rule-dependent | widestbisect | 1 | 3 | 5* | 5* | 5* | 5* | 5* | -0.00 | 0.02 | 0 |
| mccaxis2 | rule-dependent | model | 1 | 3 | 5 | 5 | 25 | 35 | 79 | 0.22 | 0.30 | 24 |
| mccaxis2 | rule-dependent | modelnoprop | 3 | 7* | 7* | 7* | 7* | 7* | 7* | -0.00 | -0.00 | 0 |
| mccaxis2 | rule-dependent | toy | 5 | 17 | 59 | 367 | 1363 | 4677 | 21191 | 0.58 | 0.62 | 9328 |
| mccaxis2 | rule-dependent | xprioexttoy | 5 | 11 | 17 | 25 | 31 | 37 | 45 | 0.08 | 0.12 | 7 |
| mccaxis2 | rule-dependent | smallstreps | 1 | 3 | 13 | 31 | 431 | 1231 | 2881 | 0.40 | 0.62 | 1171 |
| mccaxis2 | rule-dependent | xpriomidpoint | 1 | 3 | 5* | 5* | 5* | 5* | 5* | -0.00 | 0.02 | 0 |
| mccaxis2 | rule-dependent | xpriotoy | 5 | 17 | 59 | 367 | 1363 | 4677 | 21191 | 0.58 | 0.62 | 9328 |
| mccaxis2 | rule-dependent | withlocks | 1* | 1* | 1* | 1* | 1* | 1* | 1* | 0.00 | 0.00 | 0 |
| mccaxis2 | rule-dependent | exttoy | 7 | 27 | 91 | 379 | 1017 | 2803 | 10469 | 0.49 | 0.50 | 4445 |
| mccaxis2 | rule-dependent | xprio | 1 | 3 | 5 | 5 | 5 | 211 | 1041 | 1.34 | 0.47 | 528 |
| mccaxis2 | rule-dependent | xpriolppoint | 1 | 3* | 3* | 3* | 3* | 3* | 3* | -0.00 | -0.00 | 0 |
| mccdiag2 | 0.5 | default | 3 | 11 | 33 | 121 | 328 | 1504 | 4776 | 0.57 | 0.53 | 2124 |
| mccdiag2 | 0.5 | nopresolve | 3 | 11 | 33 | 121 | 328 | 1504 | 4776 | 0.57 | 0.53 | 2124 |
| mccdiag2 | 0.5 | noprop | 11 | 31 | 71 | 301 | 1481 | 4191 | 18351 | 0.53 | 0.57 | 7810 |
| mccdiag2 | 0.5 | nocutoffprop | 3 | 11 | 71 | 531 | 2281 | 6231 | 21681 | 0.48 | 0.64 | 9020 |
| mccdiag2 | 0.5 | noweakdual | 11 | 31 | 71 | 351 | 1151 | 4471 | 16131 | 0.56 | 0.56 | 7098 |
| mccdiag2 | 0.5 | obbtoff | 5 | 9 | 33 | 103 | 319 | 1395 | 4417 | 0.58 | 0.53 | 2019 |
| mccdiag2 | 0.5 | obbtall | 3 | 7 | 31 | 113 | 255 | 1023 | 4558 | 0.66 | 0.55 | 2233 |
| mccdiag2 | 0.5 | lppoint | 3 | 11 | 33 | 125 | 319 | 1516 | 4702 | 0.58 | 0.52 | 2124 |
| mccdiag2 | 0.5 | midpoint | 3 | 11 | 71 | 281 | 5101 | 7151 | 15591 | 0.23 | 0.68 | 4868 |
| mccdiag2 | 0.5 | widestbisect | 3 | 11 | 51 | 221 | 4121 | 8581 | 15731 | 0.28 | 0.70 | 5560 |
| mccdiag2 | 0.5 | model | 3 | 11 | 31 | 119 | 319 | 1025 | 3505 | 0.52 | 0.50 | 1547 |
| mccdiag2 | 0.5 | modelnoprop | 3 | 15 | 45 | 149 | 485 | 1483 | 4709 | 0.49 | 0.51 | 2040 |
| mccdiag2 | 0.5 | toy | 5 | 19 | 73 | 405 | 1377 | 4793 | 18351 | 0.56 | 0.59 | 8156 |
| mccdiag2 | 0.5 | smallstreps | 3 | 9 | 31 | 115 | 255 | 1023 | 4440 | 0.65 | 0.53 | 2179 |
| sphere3 | 1 | default | 81 | 980 | 11401 | >100000 |  |  |  |  | 1.10 |  |
| sphere3 | 1 | noprop | 91 | 1001 | 10517 | >100000 |  |  |  |  | 1.06 |  |
| sphere3 | 1 | model | 79 | 747 | 7475 | 76699 |  |  |  | 1.01 | 1.01 | 69224 |
| sphere3 | 1 | toy | 1606 | 14587 | >100000 |  |  |  |  |  |  |  |
| plane3 | 1 | default | 301 | 5251 | 53821 |  |  |  |  |  | 1.01 |  |
| plane3 | 1 | noprop | 301 | 5861 | 54401 |  |  |  |  |  | 0.97 |  |
| plane3 | 1 | model | 271 | 2857 | 31789 |  |  |  |  |  | 1.05 |  |
| plane3 | 1 | toy | 3689 | 43125 |  |  |  |  |  |  |  |  |
| qflat1 | 0.25 | default | 3 | 7 | 19 | 51 | 79 | 171 | 390 | 0.36 | 0.34 | 160 |
| qflat1 | 0.25 | noprop | 3 | 11 | 29 | 51 | 103 | 194 | 344 | 0.27 | 0.29 | 122 |
| qflat1 | 0.25 | model | 3 | 7 | 19 | 51 | 79 | 171 | 335 | 0.31 | 0.33 | 127 |
| qflat1 | 0.25 | toy | 13 | 21 | 39 | 63 | 105 | 197 | 331 | 0.25 | 0.24 | 114 |
| qflat2a | 0.25 | default | 21 | 45 | 109 | 381 | 501 | 931 | 1358 | 0.18 | 0.30 | 359 |
| qflat2a | 0.25 | nopresolve | 21 | 45 | 109 | 381 | 501 | 931 | 1358 | 0.18 | 0.30 | 359 |
| qflat2a | 0.25 | noprop | 43 | 63 | 411 | 581 | 751 | 1031 | 1337 | 0.14 | 0.21 | 316 |
| qflat2a | 0.25 | nocutoffprop | 41 | 63 | 281 | 621 | 801 | 1011 | 1338 | 0.12 | 0.22 | 291 |
| qflat2a | 0.25 | noweakdual | 41 | 63 | 281 | 621 | 801 | 1011 | 1338 | 0.12 | 0.22 | 291 |
| qflat2a | 0.25 | obbtoff | 21 | 45 | 109 | 381 | 501 | 931 | 1358 | 0.18 | 0.30 | 359 |
| qflat2a | 0.25 | obbtall | 17 | 40 | 61 | 122 | 271 | 454 | 823 | 0.24 | 0.27 | 274 |
| qflat2a | 0.25 | lppoint | 17 | 43 | 211 | 211 | 389 | 661 | 1601 | 0.29 | 0.27 | 561 |
| qflat2a | 0.25 | midpoint | 21 | 121 | 341 | 651 | 1531 | 2441 | 5501 | 0.28 | 0.31 | 1920 |
| qflat2a | 0.25 | widestbisect | 31 | 281 | 511 | 1281 | 3121 | 7521 | 51831 | 0.62 | 0.42 | 22546 |
| qflat2a | 0.25 | model | 25 | 45 | 89 | 189 | 339 | 625 | 1161 | 0.27 | 0.28 | 413 |
| qflat2a | 0.25 | modelnoprop | 37 | 65 | 115 | 195 | 371 | 599 | 1131 | 0.25 | 0.25 | 387 |
| qflat2a | 0.25 | toy | 91 | 181 | 321 | 511 | 843 | 1553 | 2487 | 0.24 | 0.23 | 832 |
| qflat2b | 0.5 | default | 63 | 175 | 603 | 1973 | 5897 | 22644 | 70627 | 0.54 | 0.52 | 32006 |
| qflat2b | 0.5 | noprop | 55 | 271 | 606 | 1757 | 6377 | 21370 | 66007 | 0.50 | 0.50 | 28600 |
| qflat2b | 0.5 | model | 63 | 175 | 497 | 1639 | 4707 | 15473 | 48307 | 0.51 | 0.49 | 21572 |
| qflat2b | 0.5 | toy | 149 | 659 | 2265 | 12453 | 45445 | >100000 |  | 0.53 | 0.61 | 29006 |
| qflat3 | 0.5 | default | 171 | 610 | 1861 | 6601 | 20107 | 67019 |  | 0.50 | 0.50 | 29030 |
| qflat3 | 0.5 | noprop | 241 | 575 | 2381 | 7071 | 17311 | 69515 |  | 0.50 | 0.49 | 29930 |
| qflat3 | 0.5 | model | 175 | 481 | 1553 | 4513 | 13583 | 45003 | >100000 | 0.50 | 0.49 | 34358 |
| qflat3 | 0.5 | toy | 5071 | 22265 | >100000 |  |  |  |  |  |  |  |
| condisk2 | 0.5 | default | 1* | 1* | 1* | 1* | 1* | 1* | 1* | 0.00 | 0.00 | 0 |
| condisk2 | 0.5 | noprop | 1* | 1* | 1* | 1* | 1* | 1* | 1* | 0.00 | 0.00 | 0 |
| condisk2 | 0.5 | model | 1* | 1* | 1* | 1* | 1* | 1* | 1* | 0.00 | 0.00 | 0 |
| condisk2 | 0.5 | toy | 1* | 1* | 1* | 1* | 1* | 1* | 1* | 0.00 | 0.00 | 0 |
| condisk2 | 0.5 | noexpand | 1* | 1* | 1* | 1* | 1* | 1* | 1* | 0.00 | 0.00 | 0 |
| condisk2soc | 0.5 | default | 1* | 1* | 1* | 1* | 1* | 1* | 1* | 0.00 | 0.00 | 0 |
| condisk2soc | 0.5 | noprop | 41 | 321 | 1151 | 4991 | 17311 | 53700 | >100000 | 0.49 | 0.55 | 39750 |
| condisk2soc | 0.5 | nocutoffprop | 1* | 1* | 1* | 1* | 1* | 1* | 1* | 0.00 | 0.00 | 0 |
| condisk2soc | 0.5 | noweakdual | 3* | 3* | 3* | 3* | 3* | 3* | 3* | -0.00 | -0.00 | 0 |
| condisk2soc | 0.5 | model | 1* | 1* | 1* | 1* | 1* | 1* | 1* | 0.00 | 0.00 | 0 |
| condisk2soc | 0.5 | toy | 147 | 899 | 3557 | 10945 | 39857 | >100000 |  | 0.54 | 0.54 | 31924 |
| condisk2soc | 0.5 | nonlprop | 31 | 226 | 1021 | 3018 | 13281 | 46041 | >100000 | 0.54 | 0.57 | 36764 |
| conexp2 | 0.5 | default | 7 | 21 | 63 | 229 | 736 | 2728 | 9768 | 0.55 | 0.54 | 4324 |
| conexp2 | 0.5 | nopresolve | 7 | 21 | 63 | 229 | 736 | 2728 | 9768 | 0.55 | 0.54 | 4324 |
| conexp2 | 0.5 | noprop | 7 | 25 | 69 | 225 | 738 | 2878 | 9567 | 0.54 | 0.53 | 4221 |
| conexp2 | 0.5 | nocutoffprop | 7 | 25 | 69 | 225 | 734 | 2876 | 9531 | 0.54 | 0.53 | 4207 |
| conexp2 | 0.5 | noweakdual | 7 | 25 | 69 | 225 | 734 | 2876 | 9531 | 0.54 | 0.53 | 4207 |
| conexp2 | 0.5 | obbtoff | 7 | 21 | 63 | 229 | 736 | 2728 | 9768 | 0.55 | 0.54 | 4324 |
| conexp2 | 0.5 | obbtall | 7 | 21 | 63 | 229 | 736 | 2728 | 9770 | 0.55 | 0.54 | 4324 |
| conexp2 | 0.5 | lppoint | 5 | 21 | 73 | 213 | 723 | 3258 | 9116 | 0.53 | 0.53 | 4003 |
| conexp2 | 0.5 | midpoint | 9 | 23 | 69 | 231 | 1021 | 3041 | 11641 | 0.54 | 0.55 | 5106 |
| conexp2 | 0.5 | widestbisect | 9 | 23 | 69 | 231 | 1021 | 3041 | 11641 | 0.54 | 0.55 | 5106 |
| conexp2 | 0.5 | model | 7 | 21 | 63 | 229 | 709 | 2047 | 7359 | 0.51 | 0.50 | 3220 |
| conexp2 | 0.5 | modelnoprop | 7 | 23 | 69 | 225 | 713 | 2193 | 7171 | 0.50 | 0.50 | 3131 |
| conexp2 | 0.5 | toy | 7 | 23 | 75 | 229 | 713 | 2251 | 7205 | 0.50 | 0.50 | 3148 |
| conexp4 | 1 | default | 46 | 448 | 4744 | 52021 |  |  |  | 1.04 | 1.03 | 47277 |
| conexp4 | 1 | noprop | 46 | 418 | 5520 | 51936 |  |  |  | 0.97 | 1.04 | 46416 |
| conexp4 | 1 | model | 43 | 387 | 3709 | 40381 |  |  |  | 1.04 | 1.01 | 36672 |
| conexp4 | 1 | toy | 583 | 5703 | 45599 |  |  |  |  |  | 0.90 |  |

## Final leaves against the Theorem B lower bound

Ratio = (open nodes at termination + processed leaves) / bound; min and max over eps, and the ratio at the smallest eps without a limit.

| instance | setting | min ratio | max ratio | ratio at smallest eps | eps |
|---|---|---|---|---|---|
| qflat1 | default | 1.59 | 4.18 | 4.10 | 1e-07 |
| qflat1 | noprop | 2.00 | 3.71 | 3.48 | 1e-07 |
| qflat1 | model | 1.59 | 3.68 | 3.68 | 1e-07 |
| qflat1 | toy | 3.20 | 5.00 | 3.46 | 1e-07 |
| iso2 | default | 9.32 | 17.81 | 11.13 | 1e-07 |
| iso2 | nopresolve | 9.32 | 17.81 | 11.13 | 1e-07 |
| iso2 | noprop | 11.81 | 20.32 | 13.44 | 1e-07 |
| iso2 | nocutoffprop | 11.81 | 20.32 | 13.44 | 1e-07 |
| iso2 | noweakdual | 11.81 | 20.32 | 13.44 | 1e-07 |
| iso2 | obbtoff | 9.32 | 17.81 | 11.13 | 1e-07 |
| iso2 | obbtall | 5.40 | 9.43 | 6.03 | 1e-07 |
| iso2 | lppoint | 5.59 | 30.79 | 19.70 | 1e-07 |
| iso2 | midpoint | 15.99 | 36.15 | 15.99 | 1e-07 |
| iso2 | widestbisect | 14.92 | 34.07 | 16.46 | 1e-07 |
| iso2 | model | 6.84 | 9.78 | 9.74 | 1e-07 |
| iso2 | modelnoprop | 9.95 | 11.79 | 11.59 | 1e-07 |
| iso2 | toy | 15.63 | 20.51 | 19.70 | 1e-07 |
| iso2c | default | 11.74 | 21.19 | 11.86 | 1e-07 |
| iso2c | noprop | 11.74 | 25.19 | 13.87 | 1e-07 |
| iso2c | model | 8.61 | 10.69 | 10.59 | 1e-07 |
| iso2c | toy | 16.20 | 19.87 | 16.65 | 1e-07 |
| linediag2 | default | 17.45 | 87.42 | 39.22 | 1e-06 |
| linediag2 | nopresolve | 17.45 | 87.42 | 39.22 | 1e-06 |
| linediag2 | noprop | 22.85 | 90.29 | 38.78 | 1e-06 |
| linediag2 | nocutoffprop | 22.85 | 89.00 | 39.71 | 1e-06 |
| linediag2 | noweakdual | 22.85 | 89.00 | 39.71 | 1e-06 |
| linediag2 | obbtoff | 17.45 | 87.42 | 39.22 | 1e-06 |
| linediag2 | obbtall | 12.73 | 42.78 | 29.90 | 1e-06 |
| linediag2 | lppoint | 18.82 | 85.63 | 40.66 | 1e-06 |
| linediag2 | midpoint | 104.63 | 342.10 | 104.63 | 1e-05 |
| linediag2 | widestbisect | 107.06 | 367.68 | 367.68 | 1e-04 |
| linediag2 | model | 15.88 | 23.65 | 23.53 | 3e-07 |
| linediag2 | modelnoprop | 19.02 | 23.67 | 23.44 | 3e-07 |
| linediag2 | toy | 107.84 | 145.36 | 124.42 | 1e-05 |
| lineaxis2 | default | 34.13 | 87.64 | 47.74 | 3e-06 |
| lineaxis2 | nopresolve | 34.13 | 87.64 | 47.74 | 3e-06 |
| lineaxis2 | noprop | 34.29 | 170.09 | 48.98 | 3e-06 |
| lineaxis2 | nocutoffprop | 34.47 | 169.79 | 49.16 | 3e-06 |
| lineaxis2 | noweakdual | 34.47 | 169.79 | 49.16 | 3e-06 |
| lineaxis2 | obbtoff | 34.13 | 87.64 | 47.74 | 3e-06 |
| lineaxis2 | obbtall | 24.82 | 43.88 | 43.88 | 3e-06 |
| lineaxis2 | lppoint | 27.49 | 85.38 | 58.90 | 3e-06 |
| lineaxis2 | midpoint | 53.48 | 93.78 | 75.61 | 1e-05 |
| lineaxis2 | widestbisect | 86.49 | 247.82 | 247.82 | 1e-04 |
| lineaxis2 | model | 27.87 | 40.73 | 40.73 | 1e-06 |
| lineaxis2 | modelnoprop | 27.86 | 41.59 | 41.59 | 1e-06 |
| lineaxis2 | toy | 61.38 | 128.79 | 95.78 | 1e-05 |
| qflat2a | default | 6.75 | 17.93 | 10.48 | 1e-07 |
| qflat2a | nopresolve | 6.75 | 17.93 | 10.48 | 1e-07 |
| qflat2a | noprop | 9.41 | 35.83 | 10.39 | 1e-07 |
| qflat2a | nocutoffprop | 9.41 | 28.55 | 10.51 | 1e-07 |
| qflat2a | noweakdual | 9.41 | 28.55 | 10.51 | 1e-07 |
| qflat2a | obbtoff | 6.75 | 17.93 | 10.48 | 1e-07 |
| qflat2a | obbtall | 5.00 | 7.43 | 6.55 | 1e-07 |
| qflat2a | lppoint | 5.62 | 17.07 | 12.95 | 1e-07 |
| qflat2a | midpoint | 7.23 | 36.30 | 34.92 | 1e-07 |
| qflat2a | widestbisect | 9.63 | 314.72 | 314.72 | 1e-07 |
| qflat2a | model | 6.76 | 9.41 | 9.38 | 1e-07 |
| qflat2a | modelnoprop | 8.80 | 11.24 | 8.99 | 1e-07 |
| qflat2a | toy | 19.71 | 25.79 | 19.71 | 1e-07 |
| qflat2b | default | 6.94 | 9.74 | 8.97 | 1e-07 |
| qflat2b | noprop | 7.26 | 11.08 | 8.16 | 1e-07 |
| qflat2b | model | 6.15 | 9.74 | 6.61 | 1e-07 |
| qflat2b | toy | 18.96 | 67.66 | 43.55 | 3e-06 |

## Numerical checks

| instance | setting | min(primal-f*) | max(dual-f*) | #optimal | limit at eps | max SoPlex warnings/run | min true f(sol)-f* |
|---|---|---|---|---|---|---|---|
| condisk2 | default | -5.3e-10 | -5.3e-10 | 13 |  | 0 | -9.3e-10 |
| condisk2 | model | 1.0e-15 | 1.0e-15 | 13 |  | 0 | 0.0e+00 |
| condisk2 | noexpand | -5.3e-10 | -5.3e-10 | 13 |  | 0 | -9.3e-10 |
| condisk2 | noprop | -1.8e-09 | -1.8e-09 | 13 |  | 0 | -1.0e-09 |
| condisk2 | toy | 1.0e-15 | 1.0e-15 | 13 |  | 0 | 0.0e+00 |
| condisk2soc | default | -2.7e-09 | -2.7e-09 | 13 |  | 0 | -1.8e-09 |
| condisk2soc | model | 1.0e-15 | 1.0e-15 | 13 |  | 0 | 0.0e+00 |
| condisk2soc | nocutoffprop | -2.7e-09 | -2.7e-09 | 13 |  | 0 | -1.8e-09 |
| condisk2soc | nonlprop | -2.9e-09 | -2.2e-07 | 0 | 1.0e-07 | 0 | -2.0e-09 |
| condisk2soc | noprop | -3.0e-09 | -2.3e-07 | 0 | 1.0e-07 | 0 | -2.0e-09 |
| condisk2soc | noweakdual | -2.7e-09 | -2.7e-09 | 13 |  | 0 | -1.8e-09 |
| condisk2soc | toy | -1.9e-09 | -1.3e-06 | 0 | 1.0e-06 | 0 | -2.0e-09 |
| conexp2 | default | -3.3e-09 | -1.0e-07 | 0 |  | 0 | -2.5e-09 |
| conexp2 | lppoint | -2.8e-09 | -1.0e-07 | 0 |  | 0 | -2.0e-09 |
| conexp2 | midpoint | -3.0e-09 | -1.0e-07 | 0 |  | 0 | -2.1e-09 |
| conexp2 | model | 1.0e-15 | -1.0e-07 | 0 |  | 0 | 0.0e+00 |
| conexp2 | modelnoprop | 1.0e-15 | -1.0e-07 | 0 |  | 0 | 0.0e+00 |
| conexp2 | nocutoffprop | -3.3e-09 | -1.0e-07 | 0 |  | 0 | -2.5e-09 |
| conexp2 | nopresolve | -3.3e-09 | -1.0e-07 | 0 |  | 0 | -2.5e-09 |
| conexp2 | noprop | -2.5e-09 | -1.0e-07 | 0 |  | 0 | -2.5e-09 |
| conexp2 | noweakdual | -3.3e-09 | -1.0e-07 | 0 |  | 0 | -2.5e-09 |
| conexp2 | obbtall | -3.2e-09 | -1.0e-07 | 0 |  | 0 | -2.4e-09 |
| conexp2 | obbtoff | -3.3e-09 | -1.0e-07 | 0 |  | 0 | -2.5e-09 |
| conexp2 | toy | 1.0e-15 | -1.0e-07 | 0 |  | 0 | 0.0e+00 |
| conexp2 | widestbisect | -3.0e-09 | -1.0e-07 | 0 |  | 0 | -2.1e-09 |
| conexp4 | default | -5.1e-09 | -4.8e-05 | 0 | 3.2e-05 | 0 | -4.2e-09 |
| conexp4 | model | 1.0e-15 | -3.7e-05 | 0 | 3.2e-05 | 0 | 0.0e+00 |
| conexp4 | noprop | -5.5e-09 | -4.8e-05 | 0 | 3.2e-05 | 0 | -4.8e-09 |
| conexp4 | toy | 1.0e-15 | -5.3e-04 | 0 | 3.2e-04 | 0 | 0.0e+00 |
| iso2 | default | -9.2e-10 | -9.2e-10 | 4 |  | 0 | 3.7e-24 |
| iso2 | lppoint | -8.9e-10 | -8.9e-10 | 5 |  | 56 | 3.7e-24 |
| iso2 | midpoint | -8.9e-10 | -8.9e-10 | 11 |  | 0 | 1.8e-20 |
| iso2 | model | 1.0e-15 | -7.6e-08 | 0 |  | 0 | 0.0e+00 |
| iso2 | modelnoprop | 1.0e-15 | -5.9e-08 | 0 |  | 0 | 0.0e+00 |
| iso2 | nocutoffprop | -9.1e-10 | -9.1e-10 | 4 |  | 1 | 3.9e-21 |
| iso2 | nopresolve | -9.2e-10 | -9.2e-10 | 4 |  | 0 | 3.7e-24 |
| iso2 | noprop | -9.1e-10 | -9.1e-10 | 4 |  | 1 | 3.9e-21 |
| iso2 | noweakdual | -9.1e-10 | -9.1e-10 | 4 |  | 1 | 3.9e-21 |
| iso2 | obbtall | -8.9e-10 | -8.9e-10 | 5 |  | 0 | 3.7e-24 |
| iso2 | obbtoff | -9.2e-10 | -9.2e-10 | 4 |  | 0 | 3.7e-24 |
| iso2 | toy | 1.0e-15 | -8.3e-08 | 0 |  | 0 | 0.0e+00 |
| iso2 | widestbisect | -8.9e-10 | -8.9e-10 | 9 |  | 0 | 1.8e-20 |
| iso2c | default | -8.9e-10 | -8.9e-10 | 4 |  | 0 | 3.7e-24 |
| iso2c | model | 1.0e-15 | -9.2e-08 | 0 |  | 0 | 0.0e+00 |
| iso2c | noprop | -9.1e-10 | -9.1e-10 | 8 |  | 0 | 2.4e-24 |
| iso2c | toy | 1.0e-15 | -9.7e-08 | 0 |  | 0 | 0.0e+00 |
| iso3 | default | -9.3e-10 | -9.3e-10 | 8 |  | 0 | 2.2e-16 |
| iso3 | model | 1.2e-15 | -9.9e-08 | 0 |  | 0 | 2.2e-16 |
| iso3 | noprop | -9.5e-10 | -6.9e-08 | 0 |  | 1050 | 2.2e-16 |
| iso3 | toy | 1.2e-15 | -1.0e-07 | 0 |  | 0 | 2.2e-16 |
| iso4 | default | -9.1e-10 | -9.8e-08 | 0 |  | 1602 | 2.2e-16 |
| iso4 | model | 1.2e-15 | -8.9e-08 | 0 |  | 0 | 2.2e-16 |
| iso4 | noprop | -9.9e-10 | -9.8e-08 | 0 |  | 12181 | 2.2e-16 |
| iso4 | toy | 1.2e-15 | -1.0e-07 | 0 |  | 0 | 2.2e-16 |
| isofbbt2 | default | -8.2e-10 | -8.2e-10 | 12 |  | 0 | 5.2e-19 |
| isofbbt2 | lppoint | -8.9e-10 | -8.9e-10 | 4 |  | 3 | 7.9e-25 |
| isofbbt2 | midpoint | -7.5e-10 | -7.5e-10 | 12 |  | 0 | 2.7e-18 |
| isofbbt2 | model | 1.0e-15 | 1.0e-15 | 12 |  | 0 | 0.0e+00 |
| isofbbt2 | modelnoprop | 1.0e-15 | -1.8e-08 | 0 |  | 0 | 0.0e+00 |
| isofbbt2 | nocutoffprop | -8.4e-10 | -8.4e-10 | 12 |  | 0 | 2.6e-21 |
| isofbbt2 | nopresolve | -8.2e-10 | -8.2e-10 | 12 |  | 0 | 5.2e-19 |
| isofbbt2 | noprop | -8.4e-10 | -8.4e-10 | 11 |  | 0 | 2.6e-21 |
| isofbbt2 | noweakdual | -9.0e-10 | -9.0e-10 | 11 |  | 0 | 5.0e-23 |
| isofbbt2 | obbtall | -7.8e-10 | -7.8e-10 | 12 |  | 0 | 2.4e-18 |
| isofbbt2 | obbtoff | -8.2e-10 | -8.2e-10 | 12 |  | 0 | 5.2e-19 |
| isofbbt2 | smallstreps | -8.2e-10 | -8.2e-10 | 12 |  | 0 | 5.2e-19 |
| isofbbt2 | toy | 1.0e-15 | -2.4e-08 | 0 |  | 0 | 0.0e+00 |
| isofbbt2 | widestbisect | -8.3e-10 | -8.3e-10 | 3 |  | 5 | 1.1e-22 |
| lineaxis2 | default | -9.0e-10 | -1.5e-06 | 0 | 1.0e-06 | 0 | 3.2e-21 |
| lineaxis2 | lppoint | -9.0e-10 | -1.3e-06 | 0 | 1.0e-06 | 0 | 2.0e-21 |
| lineaxis2 | midpoint | -8.9e-10 | -3.7e-06 | 0 | 3.2e-06 | 0 | 3.5e-22 |
| lineaxis2 | model | 1.0e-15 | -5.5e-07 | 0 | 3.2e-07 | 0 | -7.2e-43 |
| lineaxis2 | modelnoprop | 1.0e-15 | -7.4e-07 | 0 | 3.2e-07 | 0 | -7.2e-43 |
| lineaxis2 | nocutoffprop | -8.9e-10 | -1.5e-06 | 0 | 1.0e-06 | 0 | 2.2e-26 |
| lineaxis2 | nopresolve | -9.0e-10 | -1.5e-06 | 0 | 1.0e-06 | 0 | 3.2e-21 |
| lineaxis2 | noprop | -8.9e-10 | -1.5e-06 | 0 | 1.0e-06 | 0 | 2.2e-26 |
| lineaxis2 | noweakdual | -8.9e-10 | -1.5e-06 | 0 | 1.0e-06 | 0 | 2.2e-26 |
| lineaxis2 | obbtall | -9.0e-10 | -1.3e-06 | 0 | 1.0e-06 | 0 | 3.2e-21 |
| lineaxis2 | obbtoff | -9.0e-10 | -1.5e-06 | 0 | 1.0e-06 | 0 | 3.2e-21 |
| lineaxis2 | toy | 1.0e-15 | -6.3e-06 | 0 | 3.2e-06 | 0 | -7.2e-43 |
| lineaxis2 | widestbisect | -9.0e-10 | -6.3e-05 | 0 | 3.2e-05 | 0 | 1.3e-23 |
| linediag2 | default | -9.4e-10 | -3.6e-07 | 0 | 3.2e-07 | 1 | 1.0e-21 |
| linediag2 | lppoint | -9.4e-10 | -4.3e-07 | 0 | 3.2e-07 | 9 | 1.0e-21 |
| linediag2 | midpoint | -9.9e-10 | -3.9e-06 | 0 | 3.2e-06 | 4 | 1.0e-18 |
| linediag2 | model | 1.0e-15 | -1.4e-07 | 0 | 1.0e-07 | 0 | 0.0e+00 |
| linediag2 | modelnoprop | 1.0e-15 | -1.4e-07 | 0 | 1.0e-07 | 0 | 0.0e+00 |
| linediag2 | nocutoffprop | -9.6e-10 | -3.5e-07 | 0 | 3.2e-07 | 7 | 6.5e-19 |
| linediag2 | nopresolve | -9.4e-10 | -3.6e-07 | 0 | 3.2e-07 | 1 | 1.0e-21 |
| linediag2 | noprop | -9.6e-10 | -3.4e-07 | 0 | 3.2e-07 | 7 | 6.5e-19 |
| linediag2 | noweakdual | -9.6e-10 | -3.5e-07 | 0 | 3.2e-07 | 7 | 6.5e-19 |
| linediag2 | obbtall | -1.0e-09 | -4.4e-07 | 0 | 3.2e-07 | 30533 | 1.0e-21 |
| linediag2 | obbtoff | -9.4e-10 | -3.6e-07 | 0 | 3.2e-07 | 1 | 1.0e-21 |
| linediag2 | toy | 1.0e-15 | -5.9e-06 | 0 | 3.2e-06 | 0 | 0.0e+00 |
| linediag2 | widestbisect | -9.9e-10 | -5.2e-05 | 0 | 3.2e-05 | 0 | 2.8e-21 |
| mccaxis2 | default | -9.9e-10 | -9.5e-08 | 0 |  | 0 | 0.0e+00 |
| mccaxis2 | exttoy | 1.0e-15 | -5.3e-08 | 0 |  | 0 | 0.0e+00 |
| mccaxis2 | lppoint | 0.0e+00 | 0.0e+00 | 11 |  | 0 | 0.0e+00 |
| mccaxis2 | midpoint | 0.0e+00 | 0.0e+00 | 10 |  | 0 | 0.0e+00 |
| mccaxis2 | model | 1.0e-15 | -9.9e-08 | 0 |  | 0 | 0.0e+00 |
| mccaxis2 | modelnoprop | 1.0e-15 | 1.0e-15 | 12 |  | 0 | 0.0e+00 |
| mccaxis2 | nocutoffprop | -2.5e-10 | -2.5e-10 | 1 |  | 0 | 0.0e+00 |
| mccaxis2 | nopresolve | -9.9e-10 | -9.5e-08 | 0 |  | 0 | 0.0e+00 |
| mccaxis2 | noprop | 0.0e+00 | -1.0e-07 | 0 |  | 0 | 0.0e+00 |
| mccaxis2 | noweakdual | -9.9e-10 | -1.0e-07 | 0 |  | 0 | 0.0e+00 |
| mccaxis2 | obbtall | -9.6e-10 | -9.6e-08 | 0 |  | 0 | 0.0e+00 |
| mccaxis2 | obbtoff | 0.0e+00 | 0.0e+00 | 13 |  | 0 | 0.0e+00 |
| mccaxis2 | smallstreps | -1.0e-09 | -1.0e-07 | 0 |  | 0 | 0.0e+00 |
| mccaxis2 | toy | 1.0e-15 | -5.3e-08 | 0 |  | 0 | 0.0e+00 |
| mccaxis2 | widestbisect | 0.0e+00 | 0.0e+00 | 10 |  | 0 | 0.0e+00 |
| mccaxis2 | withlocks | 0.0e+00 | 0.0e+00 | 13 |  | 0 | 0.0e+00 |
| mccaxis2 | xprio | -9.9e-10 | -9.5e-08 | 0 |  | 0 | 0.0e+00 |
| mccaxis2 | xprioexttoy | 1.0e-15 | -5.3e-08 | 0 |  | 0 | 0.0e+00 |
| mccaxis2 | xpriolppoint | 0.0e+00 | 0.0e+00 | 11 |  | 0 | 0.0e+00 |
| mccaxis2 | xpriomidpoint | 0.0e+00 | 0.0e+00 | 10 |  | 0 | 0.0e+00 |
| mccaxis2 | xpriotoy | 1.0e-15 | -5.3e-08 | 0 |  | 0 | 0.0e+00 |
| mccdiag2 | default | -9.9e-10 | -1.0e-07 | 0 |  | 0 | 1.1e-16 |
| mccdiag2 | lppoint | -9.7e-10 | -1.0e-07 | 0 |  | 0 | 1.1e-16 |
| mccdiag2 | midpoint | -1.0e-09 | -1.0e-07 | 0 |  | 1 | 0.0e+00 |
| mccdiag2 | model | 1.1e-15 | -1.0e-07 | 0 |  | 0 | 1.0e-16 |
| mccdiag2 | modelnoprop | -9.9e-10 | -1.0e-07 | 0 |  | 0 | 2.4e-17 |
| mccdiag2 | nocutoffprop | -1.0e-09 | -1.0e-07 | 0 |  | 3 | 3.2e-17 |
| mccdiag2 | nopresolve | -9.9e-10 | -1.0e-07 | 0 |  | 0 | 1.1e-16 |
| mccdiag2 | noprop | -1.0e-09 | -1.0e-07 | 0 |  | 0 | 0.0e+00 |
| mccdiag2 | noweakdual | -1.0e-09 | -1.0e-07 | 0 |  | 4 | 0.0e+00 |
| mccdiag2 | obbtall | 1.1e-16 | -1.0e-07 | 0 |  | 0 | 1.1e-16 |
| mccdiag2 | obbtoff | -9.0e-10 | -1.0e-07 | 0 |  | 0 | 1.1e-16 |
| mccdiag2 | smallstreps | 1.1e-16 | -1.0e-07 | 0 |  | 0 | 1.1e-16 |
| mccdiag2 | toy | -9.5e-10 | -1.0e-07 | 0 |  | 0 | 5.0e-17 |
| mccdiag2 | widestbisect | -1.0e-09 | -1.0e-07 | 0 |  | 2 | 1.1e-17 |
| plane3 | default | -9.2e-10 | -4.3e-04 | 0 | 3.2e-04 | 0 | 6.2e-21 |
| plane3 | model | 1.0e-15 | -3.2e-04 | 0 | 3.2e-04 | 0 | 0.0e+00 |
| plane3 | noprop | -9.0e-10 | -4.3e-04 | 0 | 3.2e-04 | 0 | 3.2e-26 |
| plane3 | toy | 1.0e-15 | -7.1e-03 | 0 | 3.2e-03 | 0 | 0.0e+00 |
| qflat1 | default | -8.9e-10 | -9.5e-08 | 0 |  | 0 | 2.1e-12 |
| qflat1 | model | 1.0e-15 | -9.5e-08 | 0 |  | 0 | 0.0e+00 |
| qflat1 | noprop | -8.9e-10 | -9.0e-08 | 0 |  | 0 | 1.2e-12 |
| qflat1 | toy | 1.0e-15 | -1.0e-07 | 0 |  | 0 | 0.0e+00 |
| qflat2a | default | -8.9e-10 | -1.0e-07 | 0 |  | 0 | 2.9e-12 |
| qflat2a | lppoint | -9.0e-10 | -1.0e-07 | 0 |  | 4 | 1.7e-12 |
| qflat2a | midpoint | -9.2e-10 | -8.7e-08 | 0 |  | 2210 | 2.5e-12 |
| qflat2a | model | 1.0e-15 | -9.9e-08 | 0 |  | 0 | 0.0e+00 |
| qflat2a | modelnoprop | 1.0e-15 | -9.8e-08 | 0 |  | 0 | 0.0e+00 |
| qflat2a | nocutoffprop | -8.9e-10 | -1.0e-07 | 0 |  | 0 | 2.1e-12 |
| qflat2a | nopresolve | -8.9e-10 | -1.0e-07 | 0 |  | 0 | 2.9e-12 |
| qflat2a | noprop | -8.9e-10 | -1.0e-07 | 0 |  | 0 | 2.1e-12 |
| qflat2a | noweakdual | -8.9e-10 | -1.0e-07 | 0 |  | 0 | 2.1e-12 |
| qflat2a | obbtall | -9.0e-10 | -1.0e-07 | 0 |  | 0 | 2.3e-12 |
| qflat2a | obbtoff | -8.9e-10 | -1.0e-07 | 0 |  | 0 | 2.9e-12 |
| qflat2a | toy | 1.0e-15 | -1.0e-07 | 0 |  | 0 | 0.0e+00 |
| qflat2a | widestbisect | -9.8e-10 | -9.9e-08 | 0 |  | 33456 | 2.5e-12 |
| qflat2b | default | -9.0e-10 | -1.0e-07 | 0 |  | 0 | 3.3e-12 |
| qflat2b | model | 1.0e-15 | -1.0e-07 | 0 |  | 0 | 0.0e+00 |
| qflat2b | noprop | -9.0e-10 | -1.0e-07 | 0 |  | 0 | 3.7e-12 |
| qflat2b | toy | 1.0e-15 | -1.4e-06 | 0 | 1.0e-06 | 0 | 0.0e+00 |
| qflat3 | default | -9.0e-10 | -5.3e-07 | 0 | 3.2e-07 | 0 | 1.2e-12 |
| qflat3 | model | 1.0e-15 | -1.8e-07 | 0 | 1.0e-07 | 0 | 0.0e+00 |
| qflat3 | noprop | -9.0e-10 | -4.3e-07 | 0 | 3.2e-07 | 0 | 2.6e-12 |
| qflat3 | toy | 1.0e-15 | -1.3e-03 | 0 | 1.0e-03 | 0 | 0.0e+00 |
| ring2 | default | -9.0e-10 | -3.2e-07 | 0 | 3.2e-07 | 24 | 2.4e-23 |
| ring2 | lppoint | -9.0e-10 | -3.2e-07 | 0 | 3.2e-07 | 0 | 1.4e-22 |
| ring2 | midpoint | -9.0e-10 | -2.4e-06 | 0 | 1.0e-06 | 40 | 1.4e-18 |
| ring2 | model | 1.0e-15 | -1.4e-07 | 0 | 1.0e-07 | 28 | 0.0e+00 |
| ring2 | modelnoprop | 1.0e-15 | -1.4e-07 | 0 | 1.0e-07 | 36 | 0.0e+00 |
| ring2 | nocutoffprop | -9.5e-10 | -4.5e-07 | 0 | 3.2e-07 | 91 | 9.1e-19 |
| ring2 | noexpand | -8.8e-10 | -8.8e-10 | 13 |  | 0 | 7.3e-23 |
| ring2 | nopresolve | -9.0e-10 | -3.2e-07 | 0 | 3.2e-07 | 24 | 2.4e-23 |
| ring2 | noprop | -9.7e-10 | -4.5e-07 | 0 | 3.2e-07 | 201 | 1.7e-22 |
| ring2 | noweakdual | -9.5e-10 | -4.4e-07 | 0 | 3.2e-07 | 95 | 1.7e-22 |
| ring2 | obbtall | -1.0e-09 | -2.8e-07 | 0 | 1.0e-07 | 380 | 1.5e-15 |
| ring2 | obbtoff | -9.4e-10 | -3.2e-07 | 0 | 3.2e-07 | 18 | 2.7e-12 |
| ring2 | toy | 1.0e-15 | -1.7e-06 | 0 | 1.0e-06 | 136 | 0.0e+00 |
| ring2 | widestbisect | -9.0e-10 | -1.7e-05 | 0 | 1.0e-05 | 44 | 3.5e-22 |
| sphere3 | default | -9.5e-10 | -1.5e-04 | 0 | 1.0e-04 | 906 | 4.5e-21 |
| sphere3 | model | 1.0e-15 | -7.6e-05 | 0 | 3.2e-05 | 166 | 0.0e+00 |
| sphere3 | noprop | -9.6e-10 | -1.2e-04 | 0 | 1.0e-04 | 0 | 2.6e-21 |
| sphere3 | toy | 1.0e-15 | -2.3e-03 | 0 | 1.0e-03 | 164 | 0.0e+00 |
