# Selection: 6sub8.html

Source: https://users.ece.cmu.edu/~koopman/crc/6sub8.html

Retrieved: 2026-11-15

Copyright 2015-2018 Philip Koopman, Carnegie Mellon University, CC BY 4.0 (http://creativecommons.org/licenses/by/4.0/)

Modification: HTML was reformatted into Markdown tables; layout whitespace and visual styling were normalized. Values were not calculated or completed. — means not supplied in the source.

> 6sub8.html: This work is copyright 2018 by Philip Koopman. Licensed under a Creative Commons Attribution 4.0 International License.

> Philip Koopman, Carnegie Mellon University

> Good /6sub8 Polynomials

> Good HD=3 Polynomials

> Good HD=4 Polynomials

> Good HD=5 Polynomials

> Good HD=6 Polynomials

> Selection rules:

> Consider only polynomials with bits set in the bottom 8 bits (in addition to the topmost bit). This can help speed up computation and reduce lookup table sizes for CRC calculations in application programs.

> Pick the polynomial with the longest length for HD=6. In case of a tie consider high HD values and if a further tie, select the smallest polynomial value numerically.

> Note that all primitive polynomials annoted as (*p) have HD=3 up to length ((2**k)-CrcSize-1). Any primitive polynomial is generally good for longer lengths than that.

> See the NOTES PAGE for interpreting this data. Last update 1/2019.

## Published source anomalies (verbatim; do not use as implementation parameters without verification)

| Anomalous cell | Source |
| --- | --- |
| (0x200e7; 0x401cf | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| (0x200053; 0x4000a7 | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| (0x800004d; 0x1000009b | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |

| CRC bits | Primary HD length | Polynomial (implicit; explicit) | Nickname / attributes | HD lengths | Source |
| --- | --- | --- | --- | --- | --- |
| 8 | 4 | (0x9b; 0x137) | CRC-8F/6 (*o) | {118,118,4,4} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 9 | 8 | (0x13c; 0x279) | CRC-9F/6.2 (*o) | {8,8,8,8} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 10 | 12 | (0x28e; 0x51d) | CRC-10F/6.2 (*o) | {95,95,12,12} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 11 | 20 | (0x433; 0x867) | CRC-11K/6sub8 (*o) | {20,20,20,20} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 12 | 25 | (0x8f3; 0x11e7) | CRC-12F/4.2 ("10747") (*op) | {2035,2035,25,25,1,1} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 13 | 32 | (0x1036; 0x206d) | CRC-13K/6sub8 (*o) | {3924,3924,32,32} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 14 | 50 | (0x20ee; 0x41dd) | CRC-14K/6sub8 (*o) | {112,112,50,50,3,3} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 15 | 60 | (0x404b; 0x8097) | CRC-15K/6sub8 (*op) | {16368,16368,60,60} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 16 | 99 | (0x808d; 0x1011b) | C4 (*o) | {28642,28642,99,99} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 17 | 113 | (0x10055; 0x200ab) | CRC-17K/6sub8 (*o) | {364,364,113,113} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 18 | 141 | (0x200e7; 0x401cf | CRC-18K/6sub8 (*o) | {4077,4077,141,141,1,1} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 19 | 236 | (0x400f0; 0x801e1) | CRC-19K/6sub8 (*o) | {236,236,236,236} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 20 | 229 | (0x80071; 0x1000e3) | CRC-20K/6sub8 (*o) | {393193,393193,229,229} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 21 | 261 | (0x100077; 0x2000ef) | CRC-21K/6sub8 (*o) | {262122,262122,261,261,1,1} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 22 | 412 | (0x200053; 0x4000a7 | CRC-22K/6sub8 (*o) | {680063,680063,412,412} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 23 | 425 | (0x40007b; 0x8000f7) | CRC-23K/6sub8 (*o) | {1653517,1653517,425,425,1,1} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 24 | 667 | (0x80009a; 0x1000135) | CRC-24K/6sub8 (*op) | {8388583,8388583,667,667} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 25 | 719 | (0x100001b; 0x2000037) | CRC-25K/6sub8 (*o) | {2097126,2097126,719,719} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 26 | 1041 | (0x2000033; 0x4000067) | CRC-26K/6sub8 (*o) | {11173180,11173180,1041,1041} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 27 | 1084 | (0x4000074; 0x80000e9) | CRC-27K/6sub8 (*o) | {67067881,67067881,1084,1084} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 28 | 1403 | (0x800004d; 0x1000009b | CRC-28K/6sub8 (*o) | {100663265,100663265,1403,1403} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 29 | 2193 | (0x100000f5; 0x200001eb) | CRC-29K/6sub8 (*o) | {89478456,89478456,2193,2193,4,4} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 30 | 2533 | (0x2000005c; 0x400000b9) | CRC-30K/6sub8 (*op) | {536870881,536870881,2533,2533} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 31 | 3122 | (0x400000bb; 0x80000177) | CRC-31K/6sub8 (*o) | {1073215458,1073215458,3122,3122,3,3} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 32 | 4113 | (0x80000072; 0x1000000e5) | CRC-32K/6sub8 (*o) | {1761607438,1761607438,4113,4113} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 33 | 4997 | (0x10000004e; 0x20000009d) | CRC-33K/6sub8 (*o) | {4294434784,4294434784,4997,4997} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 34 | 8164 | (0x2000000e1; 0x4000001c3) | CRC-34K/6sub8 (*o) | {114640,114640,8164,8164} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 35 | 7167 | (0x40000001b; 0x800000037) | CRC-35K/6sub8 (*o) | {1145044684,1145044684,7167,7167} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 36 | 9486 | (0x8000000fc; 0x10000001f9) | CRC-36K/6sub8 (*o) | {12884901846,12884901846,9486,9486,1,1} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 37 | 11832 | (0x1000000065; 0x20000000cb) | CRC-37K/6sub8 (*o) | {60129542093,60129542093,11832,11832} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 38 | 16597 | (0x2000000074; 0x40000000e9) | CRC-38K/6sub8 (*o) | {27380416423,27380416423,16597,16597} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 39 | 21986 | (0x400000005c; 0x80000000b9) | CRC-39K/6sub8 (*o) | {715773231,715773231,21986,21986} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 40 | 26722 | (0x80000000f3; 0x100000001e7) | CRC-40K/6sub8 (*o) | {515396075465,515396075465,26722,26722,1,1} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 44 | 58116 | (0x800000000d1; 0x1000000001a3) | CRC-44K/6sub8 (*o) | {8778913152469,8778913152469,58116,58116} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
| 48 | 156398 | (0x8000000000ed; 0x10000000001db) | CRC-48K/6sub8 (*o) | {27214007884029,27214007884029,156398,156398,2,2} | https://users.ece.cmu.edu/~koopman/crc/6sub8.html |
