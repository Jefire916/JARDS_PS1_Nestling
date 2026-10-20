# Segment engine report (as of 2026-10-20, FICTIONAL data)

Customers: 20 | Messaged: 13 | Not messaged: 7

By journey: REFILL 6, SIZE_UP 2, MILESTONE 2, WIN_BACK 3

Not messaged: No reminder consent 2, No rule matches 4, Cooldown: bot messaged on 2026-10-16 1

| Customer | Age (m) | Est. | Rules matched | Action | Offer | Reason |
|---|---|---|---|---|---|---|
| C01 | 10 | N | REFILL | SEND RF-DP3-UP-DP4 | DP-3->DP-4 | Matched REFILL |
| C02 | 2 | N | SIZE_UP | SEND SU-0-3M-TO-3-6M | BN-3-6 | Matched SIZE_UP |
| C03 | 12 | N | MILESTONE + WIN_BACK | SEND MS-12M | BN-12-18 | Matched MILESTONE + WIN_BACK; priority picks MILESTONE, others wait for next cycle |
| C04 | 14 | N | WIN_BACK | SEND WB-12-18M | BN-12-18 | Matched WIN_BACK |
| C05 | 9 | N | REFILL | NO MESSAGE | DP-3 | No reminder consent |
| C06 | 4 | Y | REFILL | SEND RF-DP2 | DP-2 | Matched REFILL |
| C07 | 4 | N | - | NO MESSAGE |  | No rule matches; FM-1 due but infant formula: no proactive message (SIFECS 6.1/6.3) |
| C08 | 15 | N | REFILL | SEND RF-GM3 | GM-3 | Matched REFILL |
| C09 | 8 | N | REFILL | NO MESSAGE | DP-3 | Cooldown: bot messaged on 2026-10-16 |
| C10 | 1 | N | SIZE_UP | SEND SU-NB-TO-0-3M | BN-0-3 | Matched SIZE_UP |
| C11 | 11 | N | REFILL | SEND RF-WP3PK | WP-3PK | Matched REFILL |
| C12 | 7 | N | - | NO MESSAGE |  | No rule matches |
| C13 | 23 | N | - | NO MESSAGE |  | No rule matches |
| C14 | 18 | N | WIN_BACK | SEND WB-12-18M | BN-12-18 | Matched WIN_BACK |
| C15 | 3 | N | REFILL + SIZE_UP | SEND RF-DP1-UP-DP2 | DP-1->DP-2 | Matched REFILL + SIZE_UP; priority picks REFILL, others wait for next cycle |
| C16 | 6 | N | MILESTONE | SEND MS-6M | BN-6-9 | Matched MILESTONE |
| C17 | 5 | N | - | NO MESSAGE |  | No rule matches |
| C18 | 13 | N | WIN_BACK | SEND WB-12-18M | BN-12-18 | Matched WIN_BACK |
| C19 | 9 | N | REFILL | SEND RF-DP3+WP80 | DP-3, WP-80 | Matched REFILL |
| C20 | 16 | N | WIN_BACK | NO MESSAGE | BN-12-18 | No reminder consent |

## Broadcast groups (one MantaGO message pack each)

| Message pack | Customers | Demo testers |
|---|---|---|
| MS-12M | C03 | Devanshi |
| MS-6M | C16 |  |
| RF-DP1-UP-DP2 | C15 |  |
| RF-DP2 | C06 |  |
| RF-DP3+WP80 | C19 |  |
| RF-DP3-UP-DP4 | C01 | Reyansh |
| RF-GM3 | C08 |  |
| RF-WP3PK | C11 |  |
| SU-0-3M-TO-3-6M | C02 | Adhvik |
| SU-NB-TO-0-3M | C10 |  |
| WB-12-18M | C04 C14 C18 | Shivangi |

## Most-bought items (excluding infant formula)

Diapers Size 3 (66) (14), Diapers Size 2 (70) (6), Water Wipes 3 Pack (240) (5), Diapers Size 4 (60) (4), Diapers Size 1 (70) (3)
