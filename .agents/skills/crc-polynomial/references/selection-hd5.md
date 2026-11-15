# Selection: hd5.html

Source: https://users.ece.cmu.edu/~koopman/crc/hd5.html

Retrieved: 2026-11-15

Copyright 2015-2018 Philip Koopman, Carnegie Mellon University, CC BY 4.0 (http://creativecommons.org/licenses/by/4.0/)

Modification: HTML was reformatted into Markdown tables; layout whitespace and visual styling were normalized. Values were not calculated or completed. — means not supplied in the source.

> hd5.html: This work is copyright 2015 by Philip Koopman. Licensed under a Creative Commons Attribution 4.0 International License .

> Philip Koopman, Carnegie Mellon University

> Good /6sub8 Polynomials

> Good HD=3 Polynomials

> Good HD=4 Polynomials

> Good HD=5 Polynomials

> Good HD=6 Polynomials

> Selection rules:

> Pick an optimal HD=5 length.

> Note that alternate HD=5 choices can be found via the secondary property criteria for HD=3 and HD=4 polynomials.

> Note: minimum dataword length evaluated is 4 bits. Yellow highlighted cells indicated work in progress/missing data.

> See the NOTES PAGE for interpreting this data. Last update 1/2019.

## Published source anomalies (verbatim; do not use as implementation parameters without verification)

| Anomalous cell | Source |
| --- | --- |
| 0(0x74f9e7cb; 0xe9f3cf97) | https://users.ece.cmu.edu/~koopman/crc/hd5.html |

| CRC bits | Primary HD length | Secondary property | Polynomial (implicit; explicit) | Nickname / attributes | HD lengths | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 7 | 4 | none | (0x72; 0xe5) | FT2; CRC-7-MVB; CRC-7F/5 ("345p") (*p) | {120,7,4} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 8 | 9 | none | (0xeb; 0x1d7) | CRC-8F/5 | {9,9,9,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 9 | 13 | none | (0x185; 0x30b) | CRC-9F/5 ("1413") | {96,16,13} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 10 | 21 | none | (0x2b9; 0x573) | CRC-10F/5 | {21,21,21,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 11 | 26 | none | (0x5d7; 0xbaf) | CRC-11F/5 (*p) | {2036,28,26,3,2,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 12 | 53 | HD=6@ 10 | (0xbae; 0x175d) | CRC-12F/5 | {53,53,53,10,2,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 13 | 52 | HD=6@ 52 | (0x1e97; 0x3d2f) | CRC-13F/6.2 (*o) | {52,52,52,52,4,4,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 14 | 113 | HD=6@ 21 | (0x212d; 0x425b) | CRC-14K/5 | {113,113,113,21,3} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 15 | 136 | HD=6@ 16 | (0x6a8d; 0xd51b) | CRC-15F/5 | {136,136,136,16,5,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 16 | 241 | HD=6@ 35 | (0xac9a; 0x15935) | C3; CRC-16F/5 | {241,241,241,35,10,8,3} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 17 | 240 | HD=6@ 240 | (0x1724e; 0x2e49d) | CRC-17K/6 (*o) | {240,240,240,240,11,11,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 18 | 493 | HD=6@ 61 | (0x39553; 0x72aa7) | CRC-18K/5 | {493,493,493,61,4,4,3,3,2} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 19 | 494 | HD=6@ 494 | (0x5685a; 0xad0b5) | CRC-19K/6 (*o) | {494,494,494,494,16,16,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 20 | 1005 | HD=6@ 105 | (0xc8a89; 0x191513) | CRC-20K/5 | {1005,1005,1005,105,28,10,4} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 21 | 1004 | HD=6@ 1004 | (0x1edfb7; 0x3dbf6f) | CRC-21K/6 (*o) | {1004,1004,1004,1004,28,28,7,7,1,1,1,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 22 | 2025 | HD=6@ 158 | (0x2a952a; 0x552a55) | CRC-22K/5 | {2025,2025,2025,158,2,2,2,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 23 | 2026 | HD=6@ 2026 | (0x6bc0f5; 0xd781eb) | CRC-23K/6 (*o) | {2026,2026,2026,2026,39,39,11,11,2,2,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 24 | 4073 | HD=6@ 228 | (0x98ff8c; 0x131ff19) | CRC-24/5.1 | {4073,4073,4073,228,13,9,9,9,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 25 | 4072 | HD=6 @ 4072 | (0x1b9189d; 0x372313b) | CRC-25K/6 (*o) | {4072,4072,4072,4072,65,65,7,7,7,7,4,4} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 26 | 8165 | HD=6@ 328 | (0x2c45446; 0x588a88d) | CRC-26K/5 | {8165,8165,8165,328,89,32,13,13,7} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 27 | 8166 | HD=6@8166 | (0x6c3ff0d; 0xd87fe1b) | CRC-27K/6 (*o) | {8166,8166,8166,8166,86,86,16,16,1,1,1,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 28 | 16357 | HD=6@488 | (0x9037604; 0x1206ec09) | CRC-28K/5 | {16357,16357,16357,488,35,35,8,8,3} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 29 | 16356 | HD=6@ 16356 | (0x1cf492f3; 0x39e925e7) | CRC-29K/6 (*o) | {16356,16356,16356,16356,66,66,26,26,12,12,3,3,3,3,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 30 | 32737 | HD=6@ 514 | (0x2adf3aaf; 0x55be755f) | CRC-30K/5 | {32737,32737,32737,514,237,74,23,23,16,5,2,2,2,2,2,2,2,2,1} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 31 | 32738 | HD=6@ 32738 | 0(0x74f9e7cb; 0xe9f3cf97) | CRC-31K/6 (*o) | {32738,32738,32738,32738,151,151,14,14,13,13,7,7,1,1,1,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
| 32 | 65505 | HD=6@ 1060 | (0xd419cc15; 0x1a833982b) | CRC-32/5.1 (**) | {65505,65505,65505,1060,81,58,27,27,21,17,3,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd5.html |
