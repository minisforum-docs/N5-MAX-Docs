# N5 MAX Known Issues and Solutions

This section lists the known issues of the N5 MAX and their fixes. Each issue
is documented on its own page.

- ⚠️ **Important** — affects every operating system installation other than
  the pre-installed MinisCloud OS; apply the fix before putting the machine
  into service.
- 🟡 **Optional** — fix only if you encounter the problem.

## Index

- ⚠️ [Linux storage corruption with AMD IOMMU](/Docs/English/N5-MAX-Known-Issues-IOMMU-Storage-Corruption.md) — drives can fail and corrupt data under load; kernel-parameter fix or kernel upgrade
- ⚠️ [Linux SATA link power management issue](/Docs/English/N5-MAX-Known-Issues-SATA-Link-Power-Management.md) — idle links fail to wake; install the helper `.deb` (recommended) or set it up manually
- 🟡 [Windows 3D rendering errors with small dedicated graphics memory](/Docs/English/N5-MAX-Known-Issues-Windows-3D-Rendering.md) — 3DMark Time Spy at 1–2 GB dedicated memory may occasionally render incorrectly; size the memory to the application's needs
