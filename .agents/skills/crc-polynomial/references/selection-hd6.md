# Selection: hd6.html

Source: https://users.ece.cmu.edu/~koopman/crc/hd6.html

Retrieved: 2026-11-15

Copyright 2015-2018 Philip Koopman, Carnegie Mellon University, CC BY 4.0 (http://creativecommons.org/licenses/by/4.0/)

Modification: HTML was reformatted into Markdown tables; layout whitespace and visual styling were normalized. Values were not calculated or completed. — means not supplied in the source.

> hd6.html: This work is copyright 2015 by Philip Koopman. Licensed under a Creative Commons Attribution 4.0 International License.

> Philip Koopman, Carnegie Mellon University

> Good /6sub8 Polynomials

> Good HD=3 Polynomials

> Good HD=4 Polynomials

> Good HD=5 Polynomials

> Good HD=6 Polynomials

> Pick an optimal HD=6 length.

> Note that alternate HD=6 choices can be found via the secondary property criteria for HD=3 and HD=4 polynomials.

> Notes: minimum dataword length evaluated is 4 bits. Yellow highlighted cells indicated work in progress/missing data. (**) indicates "good" but not necessarily "optimal" value due to limited computational resources for an exhaustive search.

> See the NOTES PAGE for interpreting this data. Last update 1/2019.

| CRC bits | Primary HD length | Polynomial (implicit; explicit) | Nickname / attributes | HD lengths | Source |
| --- | --- | --- | --- | --- | --- |
| 8 | 4 | (0x9b; 0x137) | CRC-8F/6 (*o) | {118,118,4,4} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 9 | 8 | (0x13c; 0x279) | CRC-9F/6.2 (*o) | {8,8,8,8} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 10 | 12 | (0x28e; 0x51d) | CRC-10F/6.2 (*o) | {95,95,12,12} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 11 | 22 | (0x532; 0xa65) | CRC-11K/6.1 (*o) | {22,22,22,22} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 12 | 27 | (0xb41; 0x1683) | CRC-12F/6.2 (*o) | {1773,1773,27,27} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 13 | 52 | (0x1e97; 0x3d2f) | CRC-13F/6.2 (*o) | {52,52,52,52,4,4,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 14 | 57 | (0x372b; 0x6e57) | CRC-14K/6 (*o) | {8176,8176,57,57,3,3,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 15 | 114 | (0x573a; 0xae75) | CRC-15F/6.2 (*o) | {114,114,114,114,7,7,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 16 | 135 | (0x9eb2; 0x13d65) | C1; CRC-16-DNP; CRC-16F/6.2 (*o) | {135,135,135,135,6,6,4,4} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 17 | 240 | (0x1724e; 0x2e49d) | CRC-17K/6 (*o) | {240,240,240,240,11,11,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 18 | 240 | (0x32c69; 0x658d3) | CRC-18K/6 (*o) | {496,496,240,240,20,20,3,3} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 19 | 494 | (0x5685a; 0xad0b5) | CRC-19K/6 (*o) | {494,494,494,494,16,16,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 20 | 494 | (0xe2023; 0x1c4047) | CRC-20K/6 (*o) | {1006,1006,494,494,20,20} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 21 | 1004 | (0x1edfb7; 0x3dbf6f) | CRC-21K/6 (*o) | {1004,1004,1004,1004,28,28,7,7,1,1,1,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 22 | 1004 | (0x395b53; 0x72b6a7) | CRC-22K/6 (*o) | {2028,2028,1004,1004,34,34,4,4,4,4,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 23 | 2026 | (0x6bc0f5; 0xd781eb) | CRC-23K/6 (*o) | {2026,2026,2026,2026,39,39,11,11,2,2,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 24 | 2026 | (0xbd80de; 0x17b01bd) | CRC-24/6.2 (*o) | {4074,4074,2026,2026,59,59,12,12,2,2,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 25 | 4072 | (0x1b9189d; 0x372313b) | CRC-25K/6 (*o) | {4072,4072,4072,4072,65,65,7,7,7,7,4,4} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 26 | 4072 | (0x2186c30; 0x430d861) | CRC-26K/6 (*o) | {8168,8168,4072,4072,74,74,6,6} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 27 | 8166 | (0x6c3ff0d; 0xd87fe1b) | CRC-27K/6 (*o) | {8166,8166,8166,8166,86,86,16,16,1,1,1,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 28 | 8166 | (0xd120245; 0x1a24048b) | CRC-28K/6 (*o) | {16358,16358,8166,8166,104,104,22,22} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 29 | 16356 | (0x1cf492f3; 0x39e925e7) | CRC-29K/6 (*o) | {16356,16356,16356,16356,66,66,26,26,12,12,3,3,3,3,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 30 | 16356 | (0x2ad4a56a; 0x55a94ad5) | CRC-30K/6 (*o) | {32740,32740,16356,16356,138,138,25,25,2,2,2,2,2,2} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 31 | 32738 | (0x74f9e7cb; 0xe9f3cf97) | CRC-31K/6 (*o) | {32738,32738,32738,32738,151,151,14,14,13,13,7,7,1,1,1,1,1,1,1,1} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
| 32 | 32738 | (0x9960034c; 0x132c00699) | CRC-32K/6.4 (*o) (**) | {65506,65506,32738,32738,193,193,31,31,17,17} | https://users.ece.cmu.edu/~koopman/crc/hd6.html |
