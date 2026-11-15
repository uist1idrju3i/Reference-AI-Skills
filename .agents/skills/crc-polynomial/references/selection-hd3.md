# Selection: hd3.html

Source: https://users.ece.cmu.edu/~koopman/crc/hd3.html

Retrieved: 2026-11-15

Copyright 2015-2018 Philip Koopman, Carnegie Mellon University, CC BY 4.0 (http://creativecommons.org/licenses/by/4.0/)

Modification: HTML was reformatted into Markdown tables; layout whitespace and visual styling were normalized. Values were not calculated or completed. — means not supplied in the source.

> hd3.html: This work is copyright 2015-2017 by Philip Koopman. Licensed under a Creative Commons Attribution 4.0 International License .

> Philip Koopman, Carnegie Mellon University

> Good /6sub8 Polynomials

> Good HD=3 Polynomials

> Good HD=4 Polynomials

> Good HD=5 Polynomials

> Good HD=6 Polynomials

> Selection rules:

> Pick an optimal HD=3 length.

> Pick longest secondary property length available for that HD=3 length; in case of tie, pick one with lowest HW at that secondary HD.

> Note that all primitive polynomials annoted as (*p) have HD=3 up to length ((2**k)-CrcSize-1). Any primitive polynomial is generally good for longer lengths than that.

> See the NOTES PAGE for interpreting this data. Last update 1/2019.

## Published source anomalies (verbatim; do not use as implementation parameters without verification)

| Anomalous cell | Source |
| --- | --- |
| (0x5b3ca4; xb67949) | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| (0x306fe75; 0x60dfceb | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 0xbd07453; 0x17a0e8a7) | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| .(0x81620e5; 0x102c41cb) | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| (0x16dfbf51; 0x2dbf7ea3)) | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| (0x31342a2f; 0x6268545f)) | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| (0x4a3ed66b; 0x947dacd7 | https://users.ece.cmu.edu/~koopman/crc/hd3.html |

| CRC bits | Primary HD length | Secondary property | Polynomial (implicit; explicit) | Nickname / attributes | HD lengths | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 4 | none | (0x5; 0xb) | CRC-3K; FP-3 (*p) | {4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 4 | 11 | none | (0x9; 0x13) | CCITT-4; FP-4 (*p) | {11} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 5 | 26 | none | (0x12; 0x25) | CRC-5-EPC; CRC-5-USB; FP-5 (*p) | {26} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 6 | 57 | HD=4@ 5 | (0x33; 0x67) | CRC-6-CDMA2000-A; CRC-6F/3 (*p) | {57,5} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 7 | 120 | HD=4@ 14 | (0x65; 0xcb) | CRC-7F/2 (*p) | {120,14,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 8 | 247 | HD=4@ 19 | (0xe7; 0x1cf) | CRC-8F/3 (*p) | {247,19,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 8 | 247 | HD=5@ 6 | (0xa6; 0x14d) | CRC-8K/3 (*p) | {247,15,6} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 9 | 502 | HD=4@ 52 | (0x119; 0x233) | CRC-9F/3 (*p) | {502,52,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 9 | 502 | HD=5@ 10 | (0x143; 0x287) | CRC-9K/5 | {502,10,10} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 9 | 502 | HD=6@ 4 | (0x137; 0x26f) | CRC-9K/6.1 | {502,4,4,4,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 10 | 1013 | HD=4@ 73 | (0x327; 0x64f) | CRC-10F/3 (*p) | {1013,73,10,5,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 10 | 1013 | HD=5@ 16 | (0x2fd; 0x5fb) | CRC-10F/8.1 (*p) | {1013,16,16,5,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 10 | 1013 | HD=6@ 6 | (0x2c7; 0x58f) | CRC-10F/6.1 (*p) | {1013,7,7,6,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 11 | 2036 | HD=4@ 132 | (0x5db; 0xbb7) | \| CRC-11F/3 (*p) | {2036,132,16,2,2,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 11 | 2036 | HD=5@ 26 | (0x5d7; 0xbaf) | CRC-11F/5 (*p) | {2036,28,26,3,2,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 11 | 2036 | HD=6@ 9 | (0x473; 0x8e7) | CRC-11K/3.3 (*p) | {2036,46,9,9,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 11 | 2036 | HD=7@ 5 | (0x62b; 0xc57) | CRC-11K/3.2 (*p) | {2036,53,17,5,5} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 12 | 4083 | HD=4@ 159 | (0x987; 0x130f) | CRC-12F/3 (*p) | {4083,159,17,8,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 12 | 4083 | HD=5@ 33 | (0xbdf; 0x17bf) | CRC-12K/5.2 (*p) | {4083,59,33,6,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 12 | 4083 | HD=6@ 15 | (0x83e; 0x107d) | CRC-12F/6.1 (*p) | {4083,22,15,15,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 12 | 4083 | HD=7@ 6 | (0xa33; 0x1467) | CRC-12K/7 (*p) | {4083,149,10,6,6} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 13 | 8178 | HD=4@ 324 | (0x1abf; 0x357f) | CRC-13F/3 (*p) | {8178,324,31,6,2,2,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 13 | 8178 | HD=5@ 50 | (0x1877; 0x30ef) | CRC-13F/5 (*p) | {8178,50,50,7,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 13 | 8178 | HD=6@ 16 | (0x112d; 0x225b) | CRC-13K/6.2 (*p) | {8178,75,49,16,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 13 | 8178 | HD=7@ 9 | (0x1495; 0x292b) | CRC-13K/7 (*p) | {8178,108,21,15,9} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 13 | 8178 | HD=8@ 7 | (0x1747; 0x2e8f) | CRC-13F/8.1 ("27217p") (*p) | {8178,233,34,7,7,7,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 14 | 16369 | HD=4@ 459 | (0x27cf; 0x4f9f) | CRC-14F/3 (*p) | {16369,459,17,5,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 14 | 16369 | HD=5@ 69 | (0x37ef; 0x6fdf) | CRC-14F/11 (*p) | {16369,260,69,19,1,1,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 14 | 16369 | HD=6@ 26 | (0x2769; 0x4ed3) | CRC-14K/3.1 (*p) | {16369,134,32,26,4,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 14 | 16369 | HD=7@ 13 | (0x28a9; 0x5153) | CRC-14F/7 (*p) | {16369,317,46,14,13} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 14 | 16369 | HD=8@ 6 | (0x2a4f; 0x549f) | CRC-14K/3.2 (*p) | {16369,24,24,8,7,6,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 15 | 32752 | HD=4@ 786 | (0x4f23; 0x9e47) | CRC-15F/3 (*p) | {32752,786,45,12,9,8,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 15 | 32752 | HD=5@ 94 | (0x4d3c; 0x9a79) | CRC-15K/5 (*p) | {32752,190,94,10,10,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 15 | 32752 | HD=6@ 36 | (0x4bf9; 0x97f3) | CRC-15K/6 (*p) | {32752,195,36,36,9,6,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 15 | 32752 | HD=7@ 16 | (0x5b57; 0xb6af) | CRC-15F/7 (*p) | {32752,270,52,18,16,2,2,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 15 | 32752 | HD=8@ 8 | (0x54d6; 0xa9ad) | CRC-15K/3 (*p) | {32752,54,47,10,8,8,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 15 | 32752 | HD=9@ 5 | (0x4f51; 0x9ea3) | CRC-15F/9 ("117243p") (*p) | {32752,361,48,10,5,5,5} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 16 | 65519 | HD=4@ 1149 | (0x8d95; 0x11b2b) | CRC-16F/3 (*p) | {65519,1149,62,19,9,5,5} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 16 | 65519 | HD=5@ 119 | (0x9627; 0x12c4f) | CRC-16K/5 (*p) | {65519,390,119,15,11,4,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 16 | 65519 | HD=6@ 40 | (0x86f2; 0x10de5) | CRC-16K/6 (*p) | {65519,83,53,40,6,6,5} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 16 | 65519 | HD=7@ 18 | (0xb82d; 0x1705b) | CRC-16K/7.2 (*p) | {65519,221,22,18,18,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 16 | 65519 | HD=8@ 11 | (0x88f9; 0x111f3) | CRC-16F/8.1 ("210763p") (*p) | {65519,96,88,20,15,11,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 16 | 65519 | HD=9@ 6 | (0xc7ab; 0x18f57) | CRC-16K/3 (*p) | {65519,474,52,16,6,6,6,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 17 | 131054 | HD=4@ 1976 | (0x16fa7; 0x2df4f) | CRC-17/K3.1 (*p) | {131054,1976,63,16,16,10,6,4,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 17 | 131054 | HD=5@ 164 | (0x1b85b; 0x370b7) | CRC-17/K3.2 (*p) | {131054,440,164,23,5,2,2,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 17 | 131054 | HD=6@ 59 | (0x19f57; 0x33eaf) | CRC-17K/3.3 (*p) | {131054,420,70,59,7,7,3,3,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 17 | 131054 | HD=7@ 26 | (0x10c29; 0x21853) | CRC-17K/3.4 (*p) | {131054,358,55,28,26} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 17 | 131054 | HD=8@ 15 | (0x15583; 0x2ab07) | CRC-17K/3.5 (*p) | {131054,722,122,15,15,15,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 17 | 131054 | HD=9@ 8 | (0x123bd; 0x2477b) | CRC-17K/3.6 (*p) | {131054,8,8,8,8,8,8,4,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 17 | 131054 | HD=10@ 5 | (0x19d17; 0x33a2f) | CRC-17K/3.7 (*p) | {131054,824,17,17,10,10,5,5,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 18 | 262125 | HD=4@ 2807 | (0x23979; 0x472f3) | CRC-18K/3.1 (*p) | {262125,2807,85,9,9,9,6,3,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 18 | 262125 | HD=5@ 207 | (0x2bed6; 0x57dad) | CRC-18K/3.2 (*p) | {262125,781,207,10,10,5,2,2,2,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 18 | 262125 | HD=6@ 69 | (0x2ee49; 0x5dc93) | CRC-18K/3.3 (*p) | {262125,635,93,69,10,3,3,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 18 | 262125 | HD=7@ 31 | (0x21bab; 0x43757) | CRC-18K/3.4 (*p) | {262125,936,75,43,31,9,6,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 18 | 262125 | HD=8@ 16 | (0x238be; 0x4717d) | CRC-18K/3.5 (*p) | {262125,1081,142,34,19,16,5,5,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 18 | 262125 | HD=9@ 10 | (0x2d09f; 0x5a13f) | CRC-18K/3.6 (*p) | {262125,994,104,12,12,12,10,5,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 18 | 262125 | HD=10@ 6 | (0x287b9; 0x50f73) | CRC-18K/3.7 (*p) | {262125,59,59,53,7,7,7,6,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 18 | 262125 | HD=11@ 5 | (0x26a3d; 0x4d47b) | CRC-18K/11 (*p) | {262125,417,109,9,5,5,5,5,5} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 19 | 524268 | HD=4@ 4165 | (0x6fb57; 0xdf6af) | CRC-19K/3.1 (*p) | {524268,4165,44,44,20,10,6,2,2,2,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 19 | 524268 | HD=5@ 295 | (0x409ba; 0x81375) | CRC-19K/3.2 (*p) | {524268,1170,295,51,25,5,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 19 | 524268 | HD=6@ 88 | (0x4bacc; 0x97599) | CRC-19K/3.3 (*p) | {524268,373,98,88,23,12,10,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 19 | 524268 | HD=7@ 40 | (0x4f6a2; 0x9ed45) | CRC-19K/3.4 (*p) | {524268,596,88,41,40,4,4,4,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 19 | 524268 | HD=8@ 20 | (0x4809f; 0x9013f) | CRC-19K/3.5 (*p) | {524268,1207,174,48,31,20,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 19 | 524268 | HD=9@ 13 | (0x7573f; 0xeae7f) | CRC-19K/3.6 (*p) | {524268,838,187,49,30,15,13,6,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 19 | 524268 | HD=10@ 8 | (0x45f1c; 0x8be39) | CRC-19K/3.7 (*p) | {524268,975,182,18,10,9,9,8,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 19 | 524268 | HD=11@ 7 | (0x6d133; 0xda267) | CRC-19K/3.8 (*p) | {524268,1061,121,40,23,7,7,7,7} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 20 | 1048555 | HD=4@ 5061 | (0xb5827; 0x16b04f) | CRC-20K/3.1 (*p) | {1048555,5061,195,50,18,11,8,4,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 20 | 1048555 | HD=5@ 371 | (0xaf56f; 0x15eadf) | CRC-20K/3.2 (*p) | {1048555,1080,371,51,27,8,2,2,2,2,2,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 20 | 1048555 | HD=6@ 113 | (0xcdef9; 0x19bdf3) | CRC-20K/3.3 (*p) | {1048555,766,272,113,20,10,10,4,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 20 | 1048555 | HD=7@ 48 | (0xa88c9; 0x151193) | CRC-20K/3.4 (*p) | {1048555,285,146,68,48,16,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 20 | 1048555 | HD=8@ 27 | (0xb46b7; 0x168d6f) | CRC-20K/3.5 (*p) | {1048555,2629,72,46,29,27,9,2,2,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 20 | 1048555 | HD=9@ 15 | (0xba24b; 0x174497) | CRC-20K/3.6 (*p) | {1048555,625,157,41,29,15,15,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 20 | 1048555 | HD=10@ 11 | (0xc4d87; 0x189b0f) | CRC-20K/3.7 (*p) | {1048555,1845,281,29,22,11,11,11,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 20 | 1048555 | HD=11@ 7 | (0xafcdb; 0x15f9b7) | CRC-20K/3.8 (*p) | {1048555,429,85,29,12,12,8,7,7,2,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 21 | 2097130 | HD=4@ 8525 | (0x1707ea; 0x2e0fd5) | CRC-21K/3.1 (*p) | {2097130,8525,222,68,25,15,2,2,2,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 21 | 2097130 | HD=5@ 510 | (0x1c7d73; 0x38fae7) | CRC-21K/3.2 (*p) | {2097130,2478,510,25,25,16,13,7,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 21 | 2097130 | HD=6@ 137 | (0x1d3b83; 0x3a7707) | CRC-21K/3.3 (*p) | {2097130,1077,223,137,36,3,3,3,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 21 | 2097130 | HD=7@ 57 | (0x16ae33; 0x2d5c67) | CRC-21K/3.4 (*p) | {2097130,1188,94,89,57,12,12,6,5,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 21 | 2097130 | HD=8 @ 29 | (0x113ab8; 0x227571) | CRC-21K/3.5 (*p) | {2097130,916,76,76,40,29,4,4,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 21 | 2097130 | HD=9 @ 19 | (0x12ca8e; 0x25951d) | CRC-21K/3.6 (*p) | {2097130,3088,241,52,19,19,19,5,5} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 21 | 2097130 | HD=10 @ 11 | (0x1ab344;0x356689) | CRC-21K/3.7 (*p) | {2097130,439,194,65,27,15,11,11,7} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 21 | 2097130 | HD=11 @ 10 | (0x138517; 0x270a2f) | CRC-21K/3.8 (*p) | {2097130,2605,266,66,24,12,11,10,10} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 21 | 2097130 | HD=12 @ 6 | (0x132b7a; 0x2656f5) | CRC-21K/3.9 (*p) | {2097130,440,364,92,16,16,12,8,6,6,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 22 | 4194281 | HD=4@ 12077 | (0x308fd3; 0x611fa7) | CRC-22K/3.1 (*p) | {4194281,12077,186,100,39,9,9,5,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 22 | 4194281 | HD=5@ 632 | (0x3bc316; 0x77862d) | CRC-22K/3.2(*p) | {4194281,2153,632,70,14,14,14,6,5,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 22 | 4194281 | HD=6@164 | (0x25ef7d; 0x4bdefb) | CRC-22K/3.3 (*p) | {4194281,715,197,164,50,4,4,4,3,3,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 22 | 4194281 | HD=7@ 69 | (0x3ef8b1; 0x7df163) | CRC-22K/3.4 (*p) | {4194281,1986,300,78,69,17,12,4,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 22 | 4194281 | HD=8@ 37 | (0x36e400; 0x6dc801) | CRC-22K/3.5 (*p) | {4194281,6553,67,67,45,38,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 22 | 4194281 | HD=9@ 21 | (0x38b0d2; 0x7161a5) | CRC-22K/3.6 (*p) | {4194281,641,292,110,37,22,21,9,7} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 22 | 4194281 | HD=10@ 15 | (0x294d54; 0x529aa9) | CRC-22K/3.7 (*p) | {4194281,4583,195,31,31,19,15,15,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 22 | 4194281 | HD=11@ 12 | (0x36e098; 0x6dc131) | CRC-22K/3.8 (*p) | {4194281,577,387,65,35,12,12,12,12} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 22 | 4194281 | HD=12@ 8 | (0x2729b5; 0x4e536b) | CRC-22K/3.9 (*p) | {4194281,3089,394,44,41,12,8,8,8,8,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 22 | 4194281 | HD=13@ 5 | (0x3915e9; 0x722bd3) | CRC-22K/3.10 (*p) | {4194281,3745,6,6,6,6,6,6,6,5,5} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 23 | 8388584 | HD=4@ 18926 | (0x540df0; 0xa81be1) | CRC-23K/3.1 (*p) | {8388584,18926,420,96,36,7,7,7,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 23 | 8388584 | HD=5@ 823 | (0x424f3b; 0x849e77) | CRC-23K/3.2 (*p) | {8388584,3180,823,62,38,28,13,6,6,3,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 23 | 8388584 | HD=6@ 208 | (0x46b1ab; 0x8d6357) | CRC-23K/3.3 (*p) | {8388584,3590,301,208,28,14,13,4,4,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 23 | 8388584 | HD=7@ 81 | (0x4b5858; 0x96b0b1) | CRC-23K/3.4 (*p) | {8388584,6142,374,83,81,15,10,10,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 23 | 8388584 | HD=8@ 42 | (0x4297b0; 0x852f61) | CRC-23K/3.5 (*p) | {8388584,3560,487,130,47,42,5,5,5} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 23 | 8388584 | HD=9@ 26 | (0x5b3ca4; xb67949) | CRC-23K/3.6 (*p) | {8388584,5982,134,106,27,27,26,8,3,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 23 | 8388584 | HD=10@ 14 | (0x5e7b23; 0xbcf647) | CRC-23K/3.7 (*p) | {8388584,3015,312,77,28,28,17,14,14,3,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 23 | 8388584 | HD=11@ 14 | (0x5e7b23; 0xbcf647) | CRC-23K/3.7 (*p) | {8388584,3015,312,77,28,28,17,14,14,3,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 23 | 8388584 | HD=12@ 10 | (0x673171; 0xce62e3) | CRC-23K/3.8 (*p) | {8388584,5142,435,86,42,11,11,10,10,10,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 23 | 8388584 | HD=13@ 10 | (0x673171; 0xce62e3) | CRC-23K/3.8(*p) | {8388584,5142,435,86,42,11,11,10,10,10,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 24 | 16777191 | HD=4@ 22868 | (0x8f90e3; 0x11f21c7) | CRC-24K/3.2 (*p) | {16777191,22868,599,47,37,33,12,10,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 24 | 16777191 | HD=5@ 1060 | (0x93cb4f; 0x127969f) | CRC-24K/3.3 (*p) | {16777191,8880,1060,52,39,19,9,9,7,4,3,3,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 24 | 16777191 | HD=6@ 248 | (0xa2e4ce; 0x145c99d) | CRC-24K/3.4 (*p) | {16777191,2562,457,248,70,30,11,9,9,6,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 24 | 16777191 | HD=7@ 97 | (0x8d3c72; 0x11a78e5) | CRC-24K/3.5 (*p) | {16777191,415,415,135,97,16,11,11,9,4,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 24 | 16777191 | HD=8@ 48 | (0x941356; 0x12826ad) | CRC-24K/3.6 (*p) | {16777191,7497,179,127,60,48,18,11,6} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 24 | 16777191 | HD=9@ 30 | (0xb75eab; 0x16ebd57) | CRC-24K/3.7 (*p) | {16777191,8310,368,111,29,29,29,8,2,2,2,2,2,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 24 | 16777191 | HD=10@ 19 | (0xbda4d5; 0x17b49ab) | CRC-24K/3.8 (*p) | {16777191,10152,323,146,43,33,19,19,7,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 24 | 16777191 | HD=11@ 15 | (0xa735a7; 0x14e6b4f) | CRC-24K/3.9 (*p) | {16777191,5954,259,135,29,17,15,15,15,3,3,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 24 | 16777191 | HD=12@ 12 | (0xb87515; 0x170ea2b) | CRC-24K/3.10 (*p) | {16777191,4821,432,88,40,31,18,12,12,12,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 24 | 16777191 | HD=13@ 6 | (0xa35677; 0x146acef) | CRC-24K/3.11 (*p) | {16777191,3349,531,72,6,6,6,6,6,6,6,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 25 | 33554406 | HD=4@ 38912 | (0x101690c; 0x202d219) | CRC-25K/3.1 (*p) | {33554406,38912,604,128,72,13,13} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 25 | 33554406 | HD=5@ 1494 | (0x1d7938c; 0x3af2719) | CRC-25K/3.2 (*p) | {33554406,13554,1494,115,25,22,19,13,10,4,4,3,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 25 | 33554406 | HD=6@ 297 | (0x1a4072f; 0x3480e5f) | CRC-25K/3.3 (*p) | {33554406,7699,422,297,86,28,21,11,4,4,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 25 | 33554406 | HD=7@ 115 | (0x161d083; 0x2c3a107) | CRC-25K/3.4 (*p) | {33554406,7613,612,157,115,29,16,12,9} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 25 | 33554406 | HD=8@ 60 | (0x173877d; 0x2e70efb) | CRC-25K/3.5 (*p) | {33554406,4640,707,203,92,60,12,5,5} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 25 | 33554406 | HD=9@ 34 | (0x15b20e9; 0x2b641d3) | CRC-25K/3.6 (*p) | {33554406,11629,334,166,43,34,34,6,6,6,6} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 25 | 33554406 | HD=10@ 22 | (0x1519353; 0x2a326a7) | CRC-25K/3.7 (*p) | {33554406,8849,563,185,64,35,23,22,8,5,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 25 | 33554406 | HD=11@ 16 | (0x1685921; 0x2d0b243) | CRC-25K/3.8 (*p) | {33554406,7086,569,136,59,36,22,16,16} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 25 | 33554406 | HD=12@ 13 | (0x1cb9e8f; 0x3973d1f) | CRC-25K/3.9 (*p) | {33554406,11039,795,155,56,28,14,14,13,13,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 25 | 33554406 | HD=13@ 8 | (0x1b4562f; 0x368ac5f) | CRC-25K/3.10 (*p) | {33554406,15206,8,8,8,8,8,8,8,8,8,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 25 | 33554406 | HD=14@ 6 | (0x17448fb; 0x2e891f7) | CRC-25K/3.11 (*p) | {33554406,3930,362,120,56,45,21,12,7,7,6,6,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 25 | 33554406 | HD=15@ 4 | (0x13db8a9; 0x27b7153) | CRC-25K/3.12 (*p) | {33554406,5940,681,103,64,35,20,10,10,7,6,4,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 26 | 67108837 | HD=4@ 51801 | (0x33c19ef; 0x67833df) | CRC-26K/3.1 (*p) | {67108837,51801,451,97,75,35,7,7,1,1,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 26 | 67108837 | HD=5@ 1765 | (0x364aacb; 0x6c95597) | CRC-26K/3.2 (*p) | {67108837,11792,1765,155,82,24,9,8,8,3,3,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 26 | 67108837 | HD=6@ 374 | (0x2d83b9f; 0x5b0773f) | CRC-26K/3.3 (*p) | {67108837,5825,871,374,67,39,23,23,6,6,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 26 | 67108837 | HD=7@ 135 | (0x294f79e; 0x529ef3d) | CRC-26K/3.4 (*p) | {67108837,6915,299,255,135,25,18,4,4,3,3,3,2,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 26 | 67108837 | HD=8@ 68 | (0x3b61467; 0x76c28cf) | CRC-26K/3.5 (*p) | {67108837,11347,647,194,69,68,24,7,5,5,5,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 26 | 67108837 | HD=9@ 41 | (0x3a66e4f; 0x74cdc9f) | CRC-26K/3.6 (*p) | {67108837,18147,510,115,65,44,41,7,7,3,3,3,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 26 | 67108837 | HD=10@ 26 | (0x290a2fa; 0x52145f5) | CRC-26K/3.7 (*p) | {67108837,14375,405,169,72,48,26,26,2,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 26 | 67108837 | HD=11@ 19 | (0x2e80fa7; 0x5d01f4f) | CRC-26K/3.8 (*p) | {67108837,6451,226,207,71,30,23,19,19,3,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 26 | 67108837 | HD=12@ 17 | (0x306fe75; 0x60dfceb | CRC-26K/3.9 (*p) | {67108837,2120,763,155,43,20,17,17,17,17,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 26 | 67108837 | HD=13@ 9 | (0x3a4be4f; 0x7497c9f) | CRC-26K/3.10 (*p) | {67108837,3754,757,105,83,9,9,9,9,9,9,3,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 26 | 67108837 | HD=14@ 7 | (0x27eb7b3; 0x4fd6f67) | CRC-26K/3.11 (*p) | {67108837,15247,210,163,71,48,11,10,7,7,7,7,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 26 | 67108837 | HD=15@ 5 | (0x3e9912b; 0x7d32257) | CRC-26K/3.12 (*p) | {67108837,8355,809,230,89,12,12,12,10,9,6,5,5} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 27 | 134217700 | HD=4@ 75090 | (0x5e04635; 0xbc08c6b) | CRC-27K/3.1 (*p) | {134217700,75090,1050,204,43,41,28,16,11,4,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 27 | 134217700 | HD=5@ 2312 | (0x43cdaed; 0x879b5db) | CRC-27K/3.2 (*p) | {134217700,30670,2312,256,93,45,25,8,8,2,2,2,2,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 27 | 134217700 | HD=6@ 446 | (0x638e897; 0xc71d12f) | CRC-27K/3.3 (*p) | {134217700,27260,653,446,91,54,29,20,8,8,5,4,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 27 | 134217700 | HD=7@ 161 | (0x6ae846d; 0xd5d08db) | CRC-27K/3.4 (*p) | {134217700,24977,391,172,161,41,16,16,15,2,2,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 27 | 134217700 | HD=8@ 83 | (0x4f2e9e6; 0x9e5d3cd) | CRC-27K/3.5 (*p) | {134217700,22817,853,244,87,83,30,20,5,3,3,3,3,3,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 27 | 134217700 | HD=9@ 48 | (0x4429686; 0x8852d0d) | CRC-27K/9 (*p) | {134217700,27028,624,270,112,48,48,17,11} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 27 | 134217700 | HD=10@ 30 | (0x4f70bd9; 0x9ee17b3) | CRC-27K/3.6 (*p) | {134217700,9144,804,39,39,39,37,30,5,5,5,3,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 27 | 134217700 | HD=11@ 20 | (0x7464427; 0xe8c884f) | CRC-27K/3.7 (*p) | {134217700,21092,1450,185,79,30,21,21,20,5,5} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 27 | 134217700 | HD=12@ 15 | (0x472d41c; 0x8e5a839) | CRC-27K/3.8 (*p) | {134217700,10790,1042,207,95,54,24,16,16,15,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 27 | 134217700 | HD=13@ 11 | (0x6986313; 0xd30c627) | CRC-27K/13 (*p) | {134217700,3942,1156,223,84,52,11,11,11,11,11} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 27 | 134217700 | HD=14@ 8 | (0x6a21e4f; 0xd443c9f) | CRC-27K/3.9 (*p) | {134217700,30200,399,192,66,50,18,14,8,8,8,8,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 27 | 134217700 | HD=15@ 7 | (0x4cbaf41; 0x9975e83) | CRC-27K/3.10 (*p) | {134217700,14634,713,274,70,54,24,17,7,7,7,7,7} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 27 | 134217700 | HD=16@ 5 | (0x46569fb; 0x8cad3f7) | CRC-27K/3.11 (*p) | {134217700,5364,969,185,69,40,34,10,6,5,5,5,5,5,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 28 | 268435427 | HD=4@ 112011 | (0x91dc1e3; 0x123b83c7) | CRC-28K/3.1 (*p) | {268435427,112011,851,283,116,48,41,23,4,4,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 28 | 268435427 | HD=5@ 2997 | (0x8ba3d6b; 0x11747ad7) | CRC-28K/3.2 (*p) | {268435427,32665,2997,151,123,62,7,7,7,7,5,4,2,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 28 | 268435427 | HD=6@ 551 | (0x95afd3e; 0x12b5fa7d) | CRC-28K/3.3 (*p) | {268435427,19899,1143,551,111,59,19,19,9,6,2,2,2,2,2,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 28 | 268435427 | HD=7@ 192 | 0xbd07453; 0x17a0e8a7) | CRC-28K/3.4 (*p) | {268435427,40233,1065,282,192,32,23,16,14,10,4,3,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 28 | 268435427 | HD=8@ 92 | .(0x81620e5; 0x102c41cb) | CRC-28K/3.5 (*p) | {268435427,44913,1217,92,92,92,10,10,10} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 28 | 268435427 | HD=9@ 53 | (0xb628899; 0x16c51133) | CRC-28K/3.6 (*p) | {268435427,15847,745,295,81,60,53,7,7,7,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 28 | 268435427 | HD=10@ 33 | (0xde00a27; 0x1bc0144f) | CRC-28K/3.7 (*p) | {268435427,10170,1075,147,115,34,34,33,16,4,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 28 | 268435427 | HD=11@ 22 | (0x895065e; 0x112a0cbd) | CRC-28K/3.8 (*p) | {268435427,25515,2004,95,57,42,24,24,22,6,6} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 28 | 268435427 | HD=12@ 19 | (0xcf69197; 0x19ed232f) | CRC-28K/3.9 (*p) | {268435427,35900,1724,210,116,42,34,21,19,19,5,4,4,4,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 28 | 268435427 | HD=13@ 9 | (0xb4ec80f; 0x169d901f) | CRC-28K/3.10 (*p) | {268435427,22683,1002,306,86,36,22,21,13,10,9,9,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 28 | 268435427 | HD=14@ 9 | (0xb4ec80f; 0x169d901f) | CRC-28K/3.10 (*p) | {268435427,22683,1002,306,86,36,22,21,13,10,9,9,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 28 | 268435427 | HD=15@ 8 | (0x86b655c; 0x10d6cab9) | CRC-28K/3.11 (*p) | {268435427,23240,485,217,90,31,25,19,11,9,9,8,8} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 28 | 268435427 | HD=16@ 6 | (0xb73e919; 0x16e7d233) | CRC-28K/3.12 (*p) | {268435427,17941,1299,326,6,6,6,6,6,6,6,6,6,6,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 29 | 536870882 | HD=4@ 156945 | (0x16dfbf51; 0x2dbf7ea3)) | CRC-29K/3.1 (*p) | {536870882,156945,1567,280,67,62,43,19,15,5,5,5,2,2,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 29 | 536870882 | HD=5@ 3770 | (0x12e77cc7; 0x25cef98f) | CRC-29K/3.2 (*p) | {536870882,14946,3770,283,100,76,45,23,11,9,7,3,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 29 | 536870882 | HD=6@ 656 | (0x11f54062; 0x23ea80c5) | CRC-29K/3.3 (*p) | {536870882,11794,1940,656,116,40,25,13,13,8,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 29 | 536870882 | HD=7@ 226 | (0x1310728d; 0x2620e51b) | CRC-29K/3.4 (*p) | {536870882,34201,1867,240,226,55,44,15,13,11,7} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 29 | 536870882 | HD=8@ 108 | (0x17505831; 0x2ea0b063) | CRC-29K/3.5 (*p) | {536870882,28734,1199,265,118,108,23,23,10,10,10} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 29 | 536870882 | HD=9@ 62 | (0x10e70676; 0x21ce0ced) | CRC-29K/3.6 (*p) | {536870882,83259,1264,145,80,77,62,27,7,7,7,3,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 29 | 536870882 | HD=10@ 39 | (0x121b9bfb; 0x243737f7) | CRC-29K/3.7 (*p) | {536870882,11272,2280,343,108,41,40,39,9,9,6,5,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 29 | 536870882 | HD=11@ 27 | (0x173f6f21; 0x2e7ede43) | CRC-29K/3.8 (*p) | {536870882,15530,1383,312,137,46,32,28,27,10,7,7,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 29 | 536870882 | HD=12@ 20 | (0x1a4a9ced; 0x349539db) | CRC-29K/3.9 (*p) | {536870882,16252,1219,302,61,59,41,22,20,20,4,3,3,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 29 | 536870882 | HD=13@ 13 | (0x142507bb; 0x284a0f77) | CRC-29K/3.10 (*p) | {536870882,17116,1150,288,106,67,21,17,15,13,13,6,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 29 | 536870882 | HD=14@ 10 | (0x112b95a9; 0x22572b53) | CRC-29K/3.11 (*p) | {536870882,43878,1996,298,109,68,38,27,18,10,10,10,5} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 29 | 536870882 | HD=15@ 9 | (0x1057c91b; 0x20af9237) | CRC-29K/3.12 (*p) | {536870882,19053,1463,288,100,45,45,20,12,9,9,9,9} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 29 | 536870882 | HD=16@ 5 | (0x1234acfb; 0x246959f7) | CRC-29K/3.13 (*p) | {536870882,69997,1050,423,102,51,34,12,12,12,9,8,6,5,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 30 | 1073741793 | HD=4@ 212811 | (0x31342a2f; 0x6268545f)) | CRC-30K/3.1 (*p) | {1073741793,212811,1604,318,78,78,41,28,16,15,11,7,6} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 30 | 1073741793 | HD=5@ 4958 | (0x31107331; 0x6220e663) | CRC-30K/3.2 (*p) | {1073741793,55080,4958,457,158,77,36,21,10,9,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 30 | 1073741793 | HD=6@ 786 | (0x2a5b919d; 0x54b7233b) | CRC-30K/3.3 (*p) | {1073741793,81187,1579,786,104,68,44,22,13,6,6,6,6,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 30 | 1073741793 | HD=7@ 267 | (0x2efb42ab; 0x5df68557) | CRC-30K/3.4 (*p) | {1073741793,19534,1765,342,267,56,47,23,16,9,2,2,2,2,2,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 30 | 1073741793 | HD=8@ 125 | (0x3d60199f; 0x7ac0333f) | CRC-30K/3.5 (*p) | {1073741793,32233,1633,385,158,125,29,23,3,3,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 30 | 1073741793 | HD=9@ 71 | (0x35b8d0bf; 0x6b71a17f) | CRC-30K/3.6 (*p) | {1073741793,32573,2019,450,96,76,71,24,18,9,4,4,4,2,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 30 | 1073741793 | HD=10@ 44 | (0x22322571; 0x44644ae3) | CRC-30K/3.7 (*p) | {1073741793,5271,614,272,146,58,44,44,19,5,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 30 | 1073741793 | HD=11@ 30 | (0x20b33c48; 0x41667891) | CRC-30K/3.8 (*p) | {1073741793,66878,1308,558,121,76,36,32,30,12,8} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 30 | 1073741793 | HD=12@ 19 | (0x24916855; 0x4922d0ab) | CRC-30K/3.9 (*p) | {1073741793,55553,1243,361,114,74,49,27,19,19,12} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 30 | 1073741793 | HD=13@ 15 | (0x26d31d3c; 0x4da63a79) | CRC-30K/3.10 (*p) | {1073741793,38136,1617,463,123,81,44,24,16,15,15,3,3,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 30 | 1073741793 | HD=14@ 12 | (0x3452a9a3; 0x68a55347) | CRC-30K/3.11 (*p) | {1073741793,71125,2113,328,112,41,29,25,12,12,12,12,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 30 | 1073741793 | HD=15@ 10 | (0x236982e3; 0x46d305c7) | CRC-30K/3.12 (*p) | {1073741793,49379,869,444,118,72,33,25,19,15,11,10,10} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 30 | 1073741793 | HD=16@ 8 | (0x2897f865; 0x512ff0cb) | CRC-30K/3.13 (*p) | {1073741793,54065,2555,395,143,58,24,24,19,9,9,9,8,8,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 30 | 1073741793 | HD=17@ 4 | (0x2728fbad; 0x4e51f75b) | CRC-30K/3.14 (*p) | {1073741793,18343,1383,383,166,46,35,24,9,8,8,7,7,5,4,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 31 | 2147483616 | HD=4@ 335041 | (0x737e312b; 0xe6fc6257) | CRC-31K/3.1 (*p) | {2147483616,335041,2609,214,140,55,45,30,7,7,7,5,4,4,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 31 | 2147483616 | HD=5@ 6168 | (0x474e03ac; 0x8e9c0759) | CRC-31K/3.2 (*p) | {2147483616,24098,6168,510,149,98,45,22,22,15,9,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 31 | 2147483616 | HD=6@ 1019 | (0x4bf43ae9; 0x97e875d3) | CRC-31K/3.3 (*p) | {2147483616,68274,2788,1019,147,73,35,21,21,8,8,8,4,3,2,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 31 | 2147483616 | HD=7@ 319 | (0x66cd3537; 0xcd9a6a6f) | CRC-31K/3.4 (*p) | {2147483616,89836,2279,363,319,88,45,30,11,11,3,3,3,2,2,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 31 | 2147483616 | HD=8@ 147 | (0x49f2f2b5; 0x93e5e56b) | CRC-31K/3.5 (*p) | {2147483616,79707,2486,574,147,147,36,23,21,13,6,3,3,3,3,3,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 31 | 2147483616 | HD=9@ 81 | (0x4a30cfd6; 0x94619fad) | CRC-31K/3.6 (*p) | {2147483616,39591,1518,320,139,90,81,18,18,14,9,7,5,5,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 31 | 2147483616 | HD=10@ 51 | (0x59b51725; 0xb36a2e4b) | CRC-31K/3.7 (*p) | {2147483616,38610,1932,386,143,52,52,51,11,11,11,7,6,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 31 | 2147483616 | HD=11@ 35 | (0x460ee3bf; 0x8c1dc77f) | CRC-31K/3.8 (*p) | {2147483616,58790,1420,452,84,52,45,39,35,13,1,1,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 31 | 2147483616 | HD=12@ 24 | (0x4fea6a3a; 0x9fd4d475) | CRC-31K/3.9 (*p) | {2147483616,23848,2157,339,40,40,40,26,25,24,10,3,2,2,2,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 31 | 2147483616 | HD=13@ 18 | (0x705a39ab; 0xe0b47357) | CRC-31K/3.10 (*p) | {2147483616,54608,826,327,130,91,65,26,18,18,18,6,4,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 31 | 2147483616 | HD=14@ 13 | (0x40d5e985; 0x81abd30b) | CRC-31K/3.11 (*p) | {2147483616,57299,1437,158,132,42,42,31,15,15,13,13,6} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 31 | 2147483616 | HD=15@ 10 | (0x4a59e381; 0x94b3c703) | CRC-31K/3.12 (*p) | {2147483616,69278,1131,554,124,76,47,43,22,11,11,10,10} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 31 | 2147483616 | HD=16@ 9 | (0x41df2a47; 0x83be548f) | CRC-31K/3.13 (*p) | {2147483616,24992,2361,279,160,67,46,20,12,11,9,9,9,9,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 31 | 2147483616 | HD=17@ 5 | (0x4a3ed66b; 0x947dacd7 | CRC-31K/3.14 (*p) | {2147483616,101769,2646,450,6,6,6,6,6,6,6,6,6,6,5,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=4@ 427053 | (0xad0424f3; 0x15a0849e7) | CRC-32K/3.1 (*p) | {4294967263,427053,817,522,149,63,27,19,19,19,9,9,6} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=5@ 8162 | (0x9d9947fd; 0x13b328ffb) | CRC-32K/3.2 (*p) | {4294967263,146826,8162,361,145,60,56,33,16,16,6,6,4,4,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=6@ 1199 | (0x8e2371ef; 0x11c46e3df) | CRC-32K/3.3 (*p) | {4294967263,118103,2438,1199,201,66,45,38,24,14,10,6,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=7@ 356 | (0x80fcb077; 0x101f960ef) | CRC-32K/3.4 (*p) | {4294967263,47729,3343,519,356,68,41,31,17,9,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=8@ 163 | (0x8741c726; 0x10e838e4d) | CRC-32K/3.5 (*p) | {4294967263,93289,2083,725,249,163,58,30,13,13,7,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=9@ 90 | (0xd2c0ef07; 0x1a581de0f) | CRC-32K/3.6 (*p) | {4294967263,50057,971,625,153,91,90,39,11,11,5,5,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=10@ 58 | (0xb338add6; 0x166715bad) | CRC-32K/3.7 (*p) | {4294967263,40931,1969,224,198,63,63,58,25,11,11,5,4,2,2,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=11@ 38 | (0x945d045d; 0x128ba08bb) | CRC-32K/3.8 (*p) | {4294967263,184268,3603,526,136,100,48,38,38,10,10,10,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=12@ 27 | (0x8ee5368f; 0x11dca6d1f) | CRC-32K/3.9 (*p) | {4294967263,82664,2704,489,145,86,30,27,27,27,10,6,6,4,4,3,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=13@ 20 | (0x93b39b1b; 0x127673637) | CRC-32K/13 (*p) | {4294967263,41385,1745,515,210,71,67,32,29,20,20,8,4,4,4,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=14@ 15 | (0x81d7e747; 0x103afce8f) | CRC-32K/3.10 (*p) | {4294967263,27933,2311,664,199,70,58,33,18,18,16,15,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=15@ 14 | (0x87496166; 0x10e92c2cd) | CRC-32K/3.11 (*p) | {4294967263,126795,2098,272,103,103,52,35,21,15,15,14,14} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=16@ 10 | (0x8c746ed4; 0x118e8dda9) | CRC-32K/3.12 (*p) | {4294967263,116655,1682,490,102,76,67,42,22,15,10,10,10,10,4} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=17@ 6 | (0x8efd4bcd; 0x11dfa979b) | CRC-32K/3.13 (*p) | {4294967263,115159,1173,469,157,96,6,6,6,6,6,6,6,6,6,4,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
| 32 | 4294967263 | HD=18@ 4 | (0xe47b4c57; 0x1c8f698af) | CRC-32K/3.14 (*p) | {4294967263,58599,3333,722,232,107,59,27,6,6,6,6,6,6,6,4,1} | https://users.ece.cmu.edu/~koopman/crc/hd3.html |
