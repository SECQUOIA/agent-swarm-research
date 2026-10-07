# Review r2 recomputation of full-solve tables (own parser, node mode last)

off: runs 120 solved 75 timelimit 44 rc {'0': 119, '255': 1} missing-status 1
scip: runs 120 solved 75 timelimit 45 rc {'0': 120} missing-status 0
corner: runs 120 solved 76 timelimit 44 rc {'0': 120} missing-status 0
eff: runs 120 solved 76 timelimit 44 rc {'0': 120} missing-status 0
stock: runs 120 solved 77 timelimit 43 rc {'0': 120} missing-status 0

node pairs with nodes in all settings: 119; missing: [('ex5_4_2', 1)]

| seed | setting | solved/runs | CPU sgm | nodes sgm | common-solved (5 settings) | CPU sgm there | nodes sgm there |
|---|---|---|---|---|---|---|---|
| 1 | off | 37/60 | 18.490 | 4739.2 | 36 | 2.170 | 617.6 |
| 1 | stock | 38/60 | 16.066 | 5444.3 | 36 | 1.992 | 623.5 |
| 1 | scip | 38/60 | 18.028 | 4609.9 | 36 | 2.537 | 624.7 |
| 1 | corner | 38/60 | 17.814 | 4563.0 | 36 | 2.554 | 627.6 |
| 1 | eff | 38/60 | 17.071 | 4280.1 | 36 | 2.366 | 572.3 |
| 2 | off | 38/60 | 16.959 | 4447.1 | 37 | 2.127 | 616.0 |
| 2 | stock | 39/60 | 15.858 | 5057.4 | 37 | 1.864 | 604.8 |
| 2 | scip | 37/60 | 17.930 | 4315.9 | 37 | 2.391 | 616.0 |
| 2 | corner | 38/60 | 16.815 | 3890.1 | 37 | 2.117 | 515.4 |
| 2 | eff | 38/60 | 17.260 | 3868.8 | 37 | 2.319 | 530.6 |
| 1+2 | off | 75/120 | 17.709 | 4589.6 | 73 | 2.148 | 616.8 |
| 1+2 | stock | 77/120 | 15.962 | 5245.7 | 73 | 1.926 | 614.0 |
| 1+2 | scip | 75/120 | 17.979 | 4459.3 | 73 | 2.462 | 620.3 |
| 1+2 | corner | 76/120 | 17.308 | 4210.6 | 73 | 2.325 | 568.4 |
| 1+2 | eff | 76/120 | 17.166 | 4067.6 | 73 | 2.342 | 550.8 |

excl ex5_4_2 s1: off solved 75/119 CPU sgm 17.277
excl ex5_4_2 s1: stock solved 76/119 CPU sgm 16.361
excl ex5_4_2 s1: scip solved 74/119 CPU sgm 18.443

stock only vs off: ex5_4_2 s1 (0.06 s, 133 nodes), gabriel01 s2 (256.83 s, 97603 nodes)
off only vs stock: 
stock only vs scip: blend852 s1 (172.64 s, 84509 nodes), blend852 s2 (172.68 s, 96144 nodes), gabriel01 s2 (256.83 s, 97603 nodes)
scip only vs stock: tln7 s1 (283.04 s, 308290.0 nodes; stock status solving was interrupted [time limit reached], 584309.0 nodes)

stock vs off: all-pair CPU ratio 0.9066 p 0.0033150686331899154 (n inst 60, nonzero 38); common CPU 0.9296 p 0.00792397891483607; common nodes 0.9960 p 0.12074384978041053 (nonzero 34); pair-solved n 75 CPU 0.9236 p 0.0051307978702927835 nodes 1.0034 p 0.0902152419439517 (nonzero 35)
scip vs stock: all-pair CPU ratio 1.1189 p 1.6661120241653274e-07 (n inst 60, nonzero 39); common CPU 1.1832 p 2.3552764271002914e-07; common nodes 1.0088 p None (nonzero 3); pair-solved n 74 CPU 1.1807 p 2.3552764271002914e-07 nodes 1.0087 p None (nonzero 3)
scip vs off: all-pair CPU ratio 1.0144 p 0.04016004380176795 (n inst 60, nonzero 38); common CPU 1.0999 p 0.04601302621478742; common nodes 1.0048 p 0.10871651535853744 (nonzero 34); pair-solved n 73 CPU 1.0999 p 0.04601302621478742 nodes 1.0048 p 0.10871651535853744 (nonzero 34)
stock vs off excl ex5_4_2 s1: CPU ratio 0.9499 p 0.0034734444135781474
stock vs off seed 1: all-pair CPU ratio 0.8756 p 0.05442629212127532
stock vs off seed 2: all-pair CPU ratio 0.9387 p 0.012049870365868067

stock vs patched scip: both solved 74; signature differs on 51 / 120; on both-solved: 5
  ('blend531', 2, 21287.0, 37747.0, (56092, 598741), (98505, 1044426))
  ('carton9', 1, 4349.0, 4798.0, (9558, 229801), (10447, 252724))
  ('carton9', 2, 4722.0, 4774.0, (9892, 246435), (10127, 241583))
  ('edgecross14-039', 1, 805.0, 771.0, (2059, 275337), (2040, 276597))
  ('edgecross14-039', 2, 1049.0, 1051.0, (2681, 300424), (2691, 301909))
pairs with first LP and root dual in both: 117; first LP differs: 0; root dual differs: 0

median wall/CPU (> 5 CPU s) off: 1.2207 (n 68), max 1.451
median wall/CPU (> 5 CPU s) scip: 1.2054 (n 70), max 1.435
median wall/CPU (> 5 CPU s) corner: 1.2125 (n 69), max 1.611
median wall/CPU (> 5 CPU s) eff: 1.2052 (n 69), max 1.428
median wall/CPU (> 5 CPU s) stock: 1.2047 (n 67), max 1.423

stock reference flags: []
