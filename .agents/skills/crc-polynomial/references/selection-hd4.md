# Selection: hd4.html

Source: https://users.ece.cmu.edu/~koopman/crc/hd4.html

Retrieved: 2026-11-15

Copyright 2015-2018 Philip Koopman, Carnegie Mellon University, CC BY 4.0 (http://creativecommons.org/licenses/by/4.0/)

Modification: HTML was reformatted into Markdown tables; layout whitespace and visual styling were normalized. Values were not calculated or completed. — means not supplied in the source.

> hd4.html: This work is copyright 2015 by Philip Koopman. Licensed under a Creative Commons Attribution 4.0 International License .

> Philip Koopman, Carnegie Mellon University

> Good /6sub8 Polynomials

> Good HD=3 Polynomials

> Good HD=4 Polynomials

> Good HD=5 Polynomials

> Good HD=6 Polynomials

> Selection rules:

> Pick an optimal HD=4 length.

> Pick longest secondary property length available for that HD=4 length

> Note that all primitive polynomials times (x+1) annoted as (*op) have HD=4 up to length ((2**(k-1))-CrcSize-1). HD=3 secondary property was not selected because all such polynomials have the same length for HD=3 as for HD=4.

> Note: minimum dataword length evaluated is 4 bits. Yellow highlighted cells indicated work in progress/missing data.

> See the NOTES PAGE for interpreting this data. Last update 12/2017.

## Published source anomalies (verbatim; do not use as implementation parameters without verification)

| Anomalous cell | Source |
| --- | --- |
| 16777190,16777190,1059,1059,38,38,8,8,6,6,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |

| CRC bits | Primary HD length | Secondary property | Polynomial (implicit; explicit) | Nickname / attributes | HD lengths | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 10 | none | (0x15; 0x2b) | CRC-5; CRC-5-ITU; CRC-5F/4 (*op) | {10,10} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 6 | 25 | none | (0x23; 0x47) | CRC-6-CDMA2000-B (*op) | {25,25} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 7 | 56 | none | (0x5b; 0xb7) | CRC-7F/4.2 (*op) | {56,56,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 8 | 119 | none | (0x83; 0x107) | ATM-8; CRC-8P (*op) | {119,119} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 9 | 246 | HD=5,6@ 5 | (0x17d; 0x2fb) | CRC-9F/4.2 (*op) | {246,246,5,5,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 10 | 501 | HD=5,6@ 10 | (0x247; 0x48f) | CRC-10F/4.2 (*op) | {501,501,10,10} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 11 | 1012 | HD=5,6@ 17 | (0x583; 0xb07) | CRC-11F/4.2 (*op) | {1012,1012,17,17} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 12 | 2035 | HD=5,6@ 25 | (0x8f3; 0x11e7) | CRC-12F/4.2 (*op) | {2035,2035,25,25,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 13 | 4082 | HD=5,6@ 32 | (0x12e6; 0x25cd) | CRC-13F/4.2 (*op) | {4082,4082,32,32,4,4} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 14 | 8177 | HD=5,6@ 57 | (0x2322; 0x4645) | CRC-14K/4.2 (*op) | {8177,8177,57,57} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 15 | 16368 | HD=5,6@ 68 | (0x4306; 0x860d) | CRC-15F/4.2 (*op) | {16368,16368,68,68} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 16 | 32751 | HD=5,6@ 93 | (0xd175; 0x1a2eb) | C5; CRC-16F/4.2 (*op) | {32751,32751,93,93,11,11,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 17 | 65518 | HD=5,6@ 118 | (0x1165d; 0x22cbb) | CRC-17K/4 (*op) | {65518,65518,118,118,10,10,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 18 | 131053 | HD=5,6@ 167 | (0x25f53; 0x4bea7) | CRC-18K/4 (*op) | {131053,131053,167,167,10,10,5,5,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 19 | 262124 | HD=5,6@ 206 | (0x77b0f; 0xef61f) | CRC-19K/4 (*op) | {262124,262124,206,206,15,15,1,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 20 | 524267 | HD=5,6@ 294 | (0xc1acf; 0x18359f) | CRC-20K/4 (*op) | {524267,524267,294,294,24,24,3,3,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 21 | 1048554 | HD=5,6@ 370 | (0x10df8f; 0x21bf1f) | CRC-21K/4 (*op) | {1048554,1048554,370,370,26,26,1,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 22 | 2097129 | HD=5,6@ 509 | (0x248794; 0x490f29) | CRC-22K/4 (*op) | {2097129,2097129,509,509,26,26,12,12} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 23 | 4194280 | HD=5,6@ 601 | (0x400154; 0x8002a9) | CRC-23K/4 (*op) | {4194280,4194280,601,601} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 24 | 8388583 | HD=5,6@ 822 | (0x9945b1; 0x1328b63) | CRC-24/4 (*op) | {8388583,8388583,822,822,37,37,12,12,6,6} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 25 | 16777190 | HD=5,6@ 1059 | (0x10bba2d; 0x217745b) | CRC-25K/4 (*op) | 16777190,16777190,1059,1059,38,38,8,8,6,6,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 26 | 33554405 | HD=5,6@ 1493 | (0x278b495; 0x4f1692b) | CRC-26K/4 (*op) | {33554405,33554405,1493,1493,24,24,18,18,9,9,4,4} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 27 | 67108836 | HD=5,6@ 1785 | (0x745e8bf; 0xe8bd17f) | CRC-27K/4 (*op) | {67108836,67108836,1785,1785,45,45,10,10,6,6,2,2,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 28 | 134217699 | HD=5,6@ 2311 | (0xb67b511; 0x16cf6a23) | CRC-28K/4 (*op) | {134217699,134217699,2311,2311,92,92,24,24,8,8,4,4,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 29 | 268435426 | HD=5,6@ 2859 | (0x11c4dfb5; 0x2389bf6b) | CRC-29K/4 (*op) | {268435426,268435426,2859,2859,116,116,30,30,6,6,6,6,4,4,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 30 | 536870881 | HD=5,6@ 3769 | (0x2254329d; 0x44a8653b) | CRC-30K/4 (*op) | {536870881,536870881,3769,3769,99,99,44,44,10,10,6,6} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 31 | 1073741792 | HD=5,6@ 4957 | (0x52aa4332; 0xa5548665) | CRC-31K/4 (*op) | {1073741792,1073741792,4957,4957,157,157,35,35,9,9,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
| 32 | 2147483615 | HD=5,6@ 6167 | (0xc9d204f5; 0x193a409eb) | CRC-32K/4.2 (*op) | {2147483615,2147483615,6167,6167,148,148,44,44,25,25,8,8,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd4.html |
