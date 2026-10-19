# Corrected quarterly-model disagreement review

All scores are offensive points/100. Season is the ending year. No new fits or model changes.

Screen: 247 season-five cases with >=500 retained possessions and >=20 games. Each quarter keeps its own prior-only forecast. These are only the retained benchmark quarters, not necessarily every possession that five played during the season.

Positive gap = larger structural absolute error on the averaged scoring rate. Ranking uses observed errors: selected cases have winner’s-curse bias and are not a new validation set. Early/late gaps use Q1–2 versus Q3–4, each requiring >=100 possessions. They are descriptive persistence checks, not independent fits or confidence intervals.

## Largest extra structural errors

| rank | season | lineup | possessions | games | quarters | actual | additive | structural | gap | early_gap | late_gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2025 | Russell Westbrook / Nikola Jokić / Jamal Murray / Michael Porter Jr. / Christian Braun | 749 | 27 | 3 | 126.97 | 124.44 | 118.83 | 5.61 | 6.45 | 5.10 |
| 2 | 2019 | Russell Westbrook / Paul George / Dennis Schröder / Steven Adams / Jerami Grant | 1045 | 63 | 4 | 115.60 | 114.40 | 109.80 | 4.60 | 2.22 | 4.90 |
| 3 | 2023 | DeMar DeRozan / Nikola Vučević / Zach LaVine / Patrick Williams / Ayo Dosunmu | 1188 | 44 | 3 | 112.71 | 112.28 | 117.59 | 4.45 | 3.94 | 5.44 |
| 4 | 2022 | Patrick Beverley / Karl-Anthony Towns / D'Angelo Russell / Jarred Vanderbilt / Anthony Edwards | 1078 | 43 | 4 | 119.29 | 118.21 | 113.86 | 4.35 | 4.02 | -4.46 |
| 5 | 2016 | Kyle Korver / Paul Millsap / Al Horford / Jeff Teague / Kent Bazemore | 2067 | 80 | 4 | 104.16 | 106.86 | 111.12 | 4.26 | 4.24 | 4.26 |
| 6 | 2016 | Kyrie Irving / LeBron James / J.R. Smith / Kevin Love / Tristan Thompson | 1564 | 57 | 3 | 119.12 | 116.81 | 112.61 | 4.20 | 5.43 | 3.99 |
| 7 | 2026 | Kevin Durant / Alperen Şengün / Jabari Smith Jr. / Tari Eason / Amen Thompson | 576 | 30 | 3 | 121.88 | 121.46 | 117.29 | 4.18 | — | -4.39 |
| 8 | 2018 | Carmelo Anthony / Russell Westbrook / Paul George / Steven Adams / Andre Roberson | 1052 | 31 | 3 | 113.78 | 114.51 | 109.53 | 3.52 | -1.62 | 4.90 |
| 9 | 2024 | DeMar DeRozan / Nikola Vučević / Alex Caruso / Coby White / Ayo Dosunmu | 919 | 31 | 2 | 109.25 | 115.57 | 118.98 | 3.41 | — | 3.41 |
| 10 | 2017 | Russell Westbrook / Taj Gibson / Victor Oladipo / Steven Adams / Andre Roberson | 575 | 20 | 1 | 113.04 | 110.97 | 107.63 | 3.34 | — | 3.34 |

## Accounting conventions

Player tables below are possession-weighted averages of quarter-specific coefficients, not one fixed season fit. Final contributions apply each quarter’s own calibration slope before averaging. Reference is the prior league-player mean; raw profile+career cannot be separated further from the saved fit. Player effects and conditional channel weights are accounting, not causal player values.

Structural anchor = L + a + b × (valuation intercept − L). Its other terms are b × valued opportunities, b × shooting surplus, and d × assist deficit. The negative conditional ORB coefficient is not a causal claim that rebounding hurts. The c3/ab3 categories are text-distance proxies, not tracking coordinates.

## 1. 2025: Russell Westbrook / Nikola Jokić / Jamal Murray / Michael Porter Jr. / Christian Braun

749 possessions / 27 games / 3 retained quarters. Actual **126.97**, additive **124.44**, structural **118.83**; extra structural error **+5.61**.

| origin | possessions | games | actual | additive | structural | gap |
| --- | --- | --- | --- | --- | --- | --- |
| 2025q2 | 280.00 | 9 | 129.64 | 124.96 | 118.51 | 6.45 |
| 2025q3 | 264.00 | 8 | 125.76 | 124.96 | 118.74 | 6.22 |
| 2025q4 | 205.00 | 10 | 124.88 | 123.07 | 119.40 | 3.67 |

### Player accounting

| Player | raw_base | raw_carry | raw_experience | reference | centered_player_points | final_additive | structural_creation | structural_making |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Russell Westbrook | 5.846 | -0.349 | -0.680 | 3.111 | 1.706 | 1.178 | 3.318 | -2.051 |
| Nikola Jokić | 7.408 | 1.217 | 0.049 | 3.111 | 5.563 | 3.854 | 4.081 | 2.591 |
| Jamal Murray | 6.005 | 0.328 | 0.049 | 3.111 | 3.271 | 2.264 | 4.123 | 0.765 |
| Michael Porter Jr. | 4.281 | -0.077 | 0.152 | 3.111 | 1.245 | 0.860 | 3.884 | 1.240 |
| Christian Braun | 2.188 | 0.270 | -0.036 | 3.111 | -0.688 | -0.475 | 3.499 | -0.334 |

Additive = anchor **116.7603** + final player contributions **7.6807** = **124.4410**.

### Structural opportunity ledger

| Channel | events | conditional_weight | raw_points | final_points |
| --- | --- | --- | --- | --- |
| fga2_rim | 26.186 | 0.654 | 17.118 | 11.616 |
| fga2_paint | 17.392 | 0.254 | 4.414 | 2.995 |
| fga2_mid | 8.078 | 0.192 | 1.550 | 1.051 |
| fga2_longmid | 8.476 | 0.107 | 0.905 | 0.614 |
| fga3_c3 | 0.449 | 0.467 | 0.209 | 0.142 |
| fga3_ab3 | 30.214 | 0.418 | 12.619 | 8.563 |
| fta | 18.618 | 0.439 | 8.177 | 5.548 |
| orb | 11.534 | -0.426 | -4.912 | -3.333 |
| tov_ev | 14.096 | -0.867 | -12.219 | -8.291 |

Structural = anchor **97.7185** + channels **18.9053** + shooting **2.2106** + deficit **0.0000** = **118.8344**.

Averaged conditional weights × averaged events need not equal averaged raw points; each quarter’s product is formed before averaging.

### Opportunity forecasts versus observations

| Metric | predicted | actual |
| --- | --- | --- |
| fga | 90.797 | 92.523 |
| three_attempt | 30.664 | 30.040 |
| fta | 18.618 | 18.158 |
| turnover | 14.096 | 12.417 |

## 2. 2019: Russell Westbrook / Paul George / Dennis Schröder / Steven Adams / Jerami Grant

1,045 possessions / 63 games / 4 retained quarters. Actual **115.60**, additive **114.40**, structural **109.80**; extra structural error **+4.60**.

| origin | possessions | games | actual | additive | structural | gap |
| --- | --- | --- | --- | --- | --- | --- |
| 2019q1 | 151.00 | 10 | 111.26 | 115.02 | 108.67 | -1.17 |
| 2019q2 | 405.00 | 19 | 112.59 | 112.64 | 109.06 | 3.49 |
| 2019q3 | 173.00 | 13 | 127.17 | 114.28 | 109.53 | 4.75 |
| 2019q4 | 316.00 | 21 | 115.19 | 116.43 | 111.45 | 2.51 |

### Player accounting

| Player | raw_base | raw_carry | raw_experience | reference | centered_player_points | final_additive | structural_creation | structural_making |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Russell Westbrook | 4.710 | 0.089 | -0.520 | 0.929 | 3.350 | 2.490 | 4.470 | -1.330 |
| Paul George | 3.526 | 0.161 | -0.099 | 0.929 | 2.659 | 1.976 | 4.678 | 0.793 |
| Dennis Schröder | 2.222 | -0.040 | 0.079 | 0.929 | 1.332 | 0.991 | 4.106 | -0.671 |
| Steven Adams | -0.291 | 0.074 | 0.079 | 0.929 | -1.067 | -0.797 | 2.096 | 0.058 |
| Jerami Grant | -0.294 | -0.040 | 0.079 | 0.929 | -1.184 | -0.880 | 3.802 | -0.769 |

Additive = anchor **110.6196** + final player contributions **3.7805** = **114.4002**.

### Structural opportunity ledger

| Channel | events | conditional_weight | raw_points | final_points |
| --- | --- | --- | --- | --- |
| fga2_rim | 33.139 | 0.578 | 19.140 | 14.778 |
| fga2_paint | 8.653 | 0.168 | 1.452 | 1.121 |
| fga2_mid | 9.902 | 0.134 | 1.326 | 1.024 |
| fga2_longmid | 11.426 | 0.087 | 0.997 | 0.770 |
| fga3_c3 | 1.131 | 0.479 | 0.542 | 0.419 |
| fga3_ab3 | 23.664 | 0.395 | 9.348 | 7.216 |
| fta | 23.451 | 0.420 | 9.844 | 7.600 |
| orb | 13.115 | -0.373 | -4.887 | -3.774 |
| tov_ev | 15.111 | -0.857 | -12.951 | -10.000 |

Structural = anchor **92.5691** + channels **19.1527** + shooting **-1.9192** + deficit **0.0000** = **109.8025**.

Averaged conditional weights × averaged events need not equal averaged raw points; each quarter’s product is formed before averaging.

### Opportunity forecasts versus observations

| Metric | predicted | actual |
| --- | --- | --- |
| fga | 87.914 | 86.794 |
| three_attempt | 24.795 | 31.292 |
| fta | 23.451 | 30.431 |
| turnover | 15.111 | 13.684 |

## 3. 2023: DeMar DeRozan / Nikola Vučević / Zach LaVine / Patrick Williams / Ayo Dosunmu

1,188 possessions / 44 games / 3 retained quarters. Actual **112.71**, additive **112.28**, structural **117.59**; extra structural error **+4.45**.

| origin | possessions | games | actual | additive | structural | gap |
| --- | --- | --- | --- | --- | --- | --- |
| 2023q1 | 399.00 | 15 | 108.02 | 111.38 | 117.37 | 5.99 |
| 2023q2 | 388.00 | 16 | 117.53 | 112.93 | 117.05 | -4.12 |
| 2023q3 | 401.00 | 13 | 112.72 | 112.53 | 118.35 | 5.44 |

### Player accounting

| Player | raw_base | raw_carry | raw_experience | reference | centered_player_points | final_additive | structural_creation | structural_making |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DeMar DeRozan | 2.620 | 0.750 | -0.921 | 1.209 | 1.240 | 0.876 | 4.524 | 1.483 |
| Nikola Vučević | -0.317 | -0.257 | -0.421 | 1.209 | -2.204 | -1.549 | 3.372 | 0.516 |
| Zach LaVine | 2.656 | 0.189 | 0.030 | 1.209 | 1.666 | 1.172 | 5.485 | 0.645 |
| Patrick Williams | -0.670 | -0.389 | 0.036 | 1.209 | -2.231 | -1.569 | 2.032 | 0.216 |
| Ayo Dosunmu | -0.109 | -0.264 | -0.178 | 1.209 | -1.760 | -1.238 | 2.355 | 0.130 |

Additive = anchor **114.5844** + final player contributions **-2.3088** = **112.2756**.

### Structural opportunity ledger

| Channel | events | conditional_weight | raw_points | final_points |
| --- | --- | --- | --- | --- |
| fga2_rim | 23.348 | 0.628 | 14.658 | 10.071 |
| fga2_paint | 11.846 | 0.219 | 2.593 | 1.782 |
| fga2_mid | 12.669 | 0.170 | 2.152 | 1.479 |
| fga2_longmid | 15.634 | 0.089 | 1.390 | 0.955 |
| fga3_c3 | 0.641 | 0.431 | 0.276 | 0.190 |
| fga3_ab3 | 27.449 | 0.390 | 10.717 | 7.364 |
| fta | 19.234 | 0.432 | 8.316 | 5.715 |
| orb | 7.264 | -0.394 | -2.862 | -1.967 |
| tov_ev | 13.116 | -0.868 | -11.380 | -7.822 |

Structural = anchor **96.8368** + channels **17.7684** + shooting **2.9891** + deficit **0.0000** = **117.5943**.

Averaged conditional weights × averaged events need not equal averaged raw points; each quarter’s product is formed before averaging.

### Opportunity forecasts versus observations

| Metric | predicted | actual |
| --- | --- | --- |
| fga | 91.586 | 86.700 |
| three_attempt | 28.090 | 27.525 |
| fta | 19.234 | 15.236 |
| turnover | 13.116 | 13.889 |

## 4. 2022: Patrick Beverley / Karl-Anthony Towns / D'Angelo Russell / Jarred Vanderbilt / Anthony Edwards

1,078 possessions / 43 games / 4 retained quarters. Actual **119.29**, additive **118.21**, structural **113.86**; extra structural error **+4.35**.

| origin | possessions | games | actual | additive | structural | gap |
| --- | --- | --- | --- | --- | --- | --- |
| 2022q1 | 175.00 | 10 | 134.86 | 118.09 | 114.49 | 3.60 |
| 2022q2 | 96.00 | 3 | 150.00 | 117.45 | 112.67 | 4.78 |
| 2022q3 | 365.00 | 13 | 113.70 | 118.39 | 113.24 | -4.24 |
| 2022q4 | 442.00 | 17 | 111.09 | 118.27 | 114.39 | -3.88 |

### Player accounting

| Player | raw_base | raw_carry | raw_experience | reference | centered_player_points | final_additive | structural_creation | structural_making |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Patrick Beverley | 3.439 | 0.069 | 0.492 | 2.573 | 1.427 | 1.009 | 2.249 | 0.044 |
| Karl-Anthony Towns | 4.637 | 0.163 | 0.487 | 2.573 | 2.714 | 1.922 | 4.519 | 1.529 |
| D'Angelo Russell | 3.797 | 0.168 | 0.487 | 2.573 | 1.879 | 1.329 | 4.212 | 0.181 |
| Jarred Vanderbilt | 1.159 | 0.440 | 0.465 | 2.573 | -0.508 | -0.361 | 1.308 | -0.433 |
| Anthony Edwards | 3.136 | 0.138 | 0.253 | 2.573 | 0.954 | 0.674 | 5.539 | -1.268 |

Additive = anchor **113.6377** + final player contributions **4.5727** = **118.2103**.

### Structural opportunity ledger

| Channel | events | conditional_weight | raw_points | final_points |
| --- | --- | --- | --- | --- |
| fga2_rim | 26.001 | 0.609 | 15.824 | 11.214 |
| fga2_paint | 12.794 | 0.198 | 2.529 | 1.792 |
| fga2_mid | 5.945 | 0.159 | 0.947 | 0.671 |
| fga2_longmid | 6.299 | 0.084 | 0.532 | 0.377 |
| fga3_c3 | 0.453 | 0.432 | 0.196 | 0.139 |
| fga3_ab3 | 38.408 | 0.385 | 14.803 | 10.491 |
| fta | 19.277 | 0.430 | 8.297 | 5.880 |
| orb | 13.314 | -0.385 | -5.125 | -3.631 |
| tov_ev | 14.813 | -0.868 | -12.854 | -9.106 |

Structural = anchor **95.9847** + channels **17.8269** + shooting **0.0525** + deficit **0.0000** = **113.8641**.

Averaged conditional weights × averaged events need not equal averaged raw points; each quarter’s product is formed before averaging.

### Opportunity forecasts versus observations

| Metric | predicted | actual |
| --- | --- | --- |
| fga | 89.900 | 92.950 |
| three_attempt | 38.861 | 38.868 |
| fta | 19.277 | 20.315 |
| turnover | 14.813 | 14.935 |

## 5. 2016: Kyle Korver / Paul Millsap / Al Horford / Jeff Teague / Kent Bazemore

2,067 possessions / 80 games / 4 retained quarters. Actual **104.16**, additive **106.86**, structural **111.12**; extra structural error **+4.26**.

| origin | possessions | games | actual | additive | structural | gap |
| --- | --- | --- | --- | --- | --- | --- |
| 2016q1 | 306.00 | 13 | 103.27 | 106.66 | 111.89 | 5.23 |
| 2016q2 | 375.00 | 18 | 102.40 | 107.79 | 111.23 | 3.44 |
| 2016q3 | 564.00 | 20 | 104.79 | 107.06 | 111.26 | 4.19 |
| 2016q4 | 822.00 | 29 | 104.87 | 106.38 | 110.69 | 4.31 |

### Player accounting

| Player | raw_base | raw_carry | raw_experience | reference | centered_player_points | final_additive | structural_creation | structural_making |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kyle Korver | 3.069 | 0.109 | -0.445 | 1.831 | 0.902 | 0.761 | 2.114 | 2.260 |
| Paul Millsap | 2.805 | 0.165 | 0.032 | 1.831 | 1.172 | 0.993 | 4.041 | -0.052 |
| Al Horford | 0.999 | 0.072 | 0.032 | 1.831 | -0.727 | -0.615 | 2.781 | 1.980 |
| Jeff Teague | 2.926 | -0.188 | 0.055 | 1.831 | 0.962 | 0.819 | 3.935 | -0.307 |
| Kent Bazemore | 0.138 | 0.075 | 0.229 | 1.831 | -1.389 | -1.173 | 3.647 | -0.860 |

Additive = anchor **106.0797** + final player contributions **0.7852** = **106.8649**.

### Structural opportunity ledger

| Channel | events | conditional_weight | raw_points | final_points |
| --- | --- | --- | --- | --- |
| fga2_rim | 29.295 | 0.524 | 15.355 | 12.260 |
| fga2_paint | 11.231 | 0.141 | 1.575 | 1.259 |
| fga2_mid | 7.405 | 0.099 | 0.730 | 0.582 |
| fga2_longmid | 13.455 | 0.073 | 0.980 | 0.783 |
| fga3_c3 | 1.599 | 0.485 | 0.776 | 0.620 |
| fga3_ab3 | 27.101 | 0.380 | 10.294 | 8.214 |
| fta | 18.532 | 0.388 | 7.187 | 5.744 |
| orb | 8.320 | -0.328 | -2.730 | -2.181 |
| tov_ev | 15.372 | -0.877 | -13.480 | -10.764 |

Structural = anchor **91.5810** + channels **16.5177** + shooting **3.0214** + deficit **0.0000** = **111.1201**.

Averaged conditional weights × averaged events need not equal averaged raw points; each quarter’s product is formed before averaging.

### Opportunity forecasts versus observations

| Metric | predicted | actual |
| --- | --- | --- |
| fga | 90.085 | 89.937 |
| three_attempt | 28.699 | 31.592 |
| fta | 18.532 | 13.401 |
| turnover | 15.372 | 15.046 |

## 6. 2016: Kyrie Irving / LeBron James / J.R. Smith / Kevin Love / Tristan Thompson

1,564 possessions / 57 games / 3 retained quarters. Actual **119.12**, additive **116.81**, structural **112.61**; extra structural error **+4.20**.

| origin | possessions | games | actual | additive | structural | gap |
| --- | --- | --- | --- | --- | --- | --- |
| 2016q2 | 235.00 | 9 | 121.70 | 117.47 | 112.04 | 5.43 |
| 2016q3 | 440.00 | 17 | 117.05 | 116.74 | 112.13 | 4.61 |
| 2016q4 | 889.00 | 31 | 119.46 | 116.68 | 113.00 | 3.68 |

### Player accounting

| Player | raw_base | raw_carry | raw_experience | reference | centered_player_points | final_additive | structural_creation | structural_making |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kyrie Irving | 5.661 | -0.086 | 0.141 | 1.787 | 3.930 | 3.304 | 4.170 | 1.020 |
| LeBron James | 9.269 | 0.028 | -0.391 | 1.787 | 7.119 | 5.975 | 5.204 | 1.398 |
| J.R. Smith | 3.755 | -0.173 | -0.391 | 1.787 | 1.403 | 1.176 | 3.318 | 0.795 |
| Kevin Love | 3.683 | -0.101 | -0.003 | 1.787 | 1.793 | 1.509 | 3.596 | 0.484 |
| Tristan Thompson | 0.179 | -0.008 | 0.141 | 1.787 | -1.475 | -1.236 | 1.545 | -0.652 |

Additive = anchor **106.0873** + final player contributions **10.7267** = **116.8140**.

### Structural opportunity ledger

| Channel | events | conditional_weight | raw_points | final_points |
| --- | --- | --- | --- | --- |
| fga2_rim | 27.624 | 0.523 | 14.453 | 11.416 |
| fga2_paint | 12.043 | 0.142 | 1.714 | 1.351 |
| fga2_mid | 8.364 | 0.099 | 0.831 | 0.655 |
| fga2_longmid | 12.448 | 0.074 | 0.917 | 0.724 |
| fga3_c3 | 1.135 | 0.488 | 0.554 | 0.437 |
| fga3_ab3 | 29.499 | 0.379 | 11.185 | 8.835 |
| fta | 22.009 | 0.388 | 8.546 | 6.752 |
| orb | 13.335 | -0.328 | -4.379 | -3.459 |
| tov_ev | 12.816 | -0.876 | -11.230 | -8.879 |

Structural = anchor **91.7305** + channels **17.8323** + shooting **3.0465** + deficit **0.0000** = **112.6093**.

Averaged conditional weights × averaged events need not equal averaged raw points; each quarter’s product is formed before averaging.

### Opportunity forecasts versus observations

| Metric | predicted | actual |
| --- | --- | --- |
| fga | 91.112 | 95.396 |
| three_attempt | 30.634 | 34.847 |
| fta | 22.009 | 19.246 |
| turnover | 12.816 | 12.404 |

