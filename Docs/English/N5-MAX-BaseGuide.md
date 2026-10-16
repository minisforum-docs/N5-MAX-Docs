# N5 MAX

The N5 MAX is a five-bay AI NAS built on the AMD Ryzen™ AI Max+ 395
(Strix Halo) platform. Its defining feature is unified memory: the CPU, GPU and
NPU share a single LPDDR5X memory pool, which allows the Radeon 8060S to
address tens of gigabytes of memory for local LLM inference without a discrete
graphics card.

This document shows the interface block diagram and compares the N5 MAX with
the rest of the N5 series.

**Before installing a third-party operating system, read
[Known Issues and Solutions](/Docs/English/N5-MAX-Known-Issues.md) first: two
Linux issues require manual fixes on any Linux distribution other than
MinisCloud OS.**

## Index

- [N5 MAX Base Guide](/Docs/English/N5-MAX-BaseGuide.md) — overview, interface block diagram, N5 series comparison
- [N5 MAX Linux LLM Inference Best Practices](/Docs/English/N5-MAX-Linux-LLM-Inference-Best-Practices.md) — kernel, BIOS, IOMMU, shared memory, engines
- [N5 MAX Windows LLM Inference Best Practices](/Docs/English/N5-MAX-Windows-LLM-Inference-Best-Practices.md) — graphics memory, engines, performance expectations
- [N5 MAX Known Issues and Solutions](/Docs/English/N5-MAX-Known-Issues.md) — mandatory Linux fixes and Windows notes
    - ⚠️ [Linux storage corruption with AMD IOMMU](/Docs/English/N5-MAX-Known-Issues-IOMMU-Storage-Corruption.md) — kernel parameter fix
    - ⚠️ [SATA link power management issue](/Docs/English/N5-MAX-Known-Issues-SATA-Link-Power-Management.md) — helper `.deb` in [Tools](/Tools/N5MAX-SATA-LPM-Fix/README.md); manual setup for advanced users
    - 🟡 [Windows 3D rendering errors with small dedicated graphics memory](/Docs/English/N5-MAX-Known-Issues-Windows-3D-Rendering.md) — fix only if encountered

## Interface block diagram

![N5 MAX interface block diagram](/Datasheet/N5-MAX-Block-Diagram.png)

## N5 series comparison

| Item                | N5 MAX                                                                                       | N5 PRO                                                    | N5 Air                                                                                    |
| ------------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| CPU                 | AMD Ryzen™ AI Max+ 395 (16C/32T, up to 5.1 GHz)                                              | AMD Ryzen™ AI 9 HX PRO 370 / 375 (12C/24T, up to 5.1 GHz) | AMD Ryzen™ 7 255 (8C/16T, up to 4.9 GHz); option: Ryzen™ 5 7640HS (6C/12T, up to 5.0 GHz) |
| CPU power mode      | Balance 90 W                                                                                 | 45 W                                                      | 45 W                                                                                      |
| GPU                 | Radeon 8060S, 40 CU                                                                          | Radeon 890M                                               | Radeon 780M; option: Radeon 760M                                                          |
| NPU                 | up to 50 TOPS (126 TOPS overall)                                                             | up to 55 TOPS (PRO 375)                                   | none                                                                                      |
| Memory              | LPDDR5X unified (onboard), 64 / 128 GB, 8000 MT/s                                            | DDR5 SO-DIMM ×2 (ECC), up to 96 GB, 5600 MT/s             | DDR5 SO-DIMM ×2 (non-ECC), up to 96 GB, 5600 MT/s                                         |
| HDD bays            | 5 × 3.5"/2.5" SATA 3.0                                                                       | 5 × 3.5"/2.5" SATA 3.0                                    | 5 × 3.5"/2.5" SATA 3.0                                                                    |
| M.2 NVMe slots      | 5 total: A (PCIe 4.0 x4), B–E (PCIe 4.0 x1)                                                  | 3 total; optional U.2 adapter                             | 3 total                                                                                   |
| PCIe expansion      | none — the HHHL PCIe slot was removed so the larger heatsink of the higher-power CPU can fit | PCIe x16 slot (PCIe 4.0 x4), HHHL                         | PCIe x16 slot (PCIe 4.0 x4), HHHL                                                         |
| Ethernet            | 2 × 10GbE RJ45                                                                               | 10GbE + 5GbE                                              | 10GbE + 5GbE                                                                              |
| USB4 ports          | 2 × USB4 v2 (80 Gbps) rear + 1 × USB4 (40 Gbps) front                                        | 2 × USB4 (40 Gbps)                                        | 2 × USB4 (40 Gbps)                                                                        |
| Video out           | HDMI 2.1 FRL (up to 8K@60 / 4K@144) + USB4 Alt DP                                            | HDMI 2.1 FRL + USB4 Alt DP                                | HDMI 2.1 FRL + USB4 Alt DP                                                                |
| Power               | internal PSU, AC 100–240 V, max 250 W                                                        | DC 19 V / 280 W adapter                                   | DC 19 V / 280 W adapter                                                                   |
| Dimensions / weight | 199 × 202.4 × 252.3 mm / 5.8 kg                                                              | 199 × 202 × 252 mm / 5 kg                                 | 199 × 202 × 252 mm / 4 kg                                                                 |

Notes:

- On the N5 MAX, M.2 Slot A is PCIe 4.0 x4 and Slots B–E are PCIe 4.0 x1.
  Slot B accepts 2230/2280 modules and is where the factory system disk is
  installed. Consult the user manual for the physical slot locations.
