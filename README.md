# N5 MAX

Advanced user documentation for the Minisforum N5 MAX (AMD Strix Halo) —
running Linux or Windows in place of the pre-installed MinisCloud OS and
avoiding the platform's known issues.

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

## Other language versions

The Chinese and English documentation is officially maintained. Community
translations into other languages are welcome.

| Language | Link                                         |
| -------- | -------------------------------------------- |
| Chinese  | [中文版](/Docs/Chinese/N5-MAX-BaseGuide.md)  |
| English  | [English](/Docs/English/N5-MAX-BaseGuide.md) |

## Contributing

- Fork the repo, create a branch, and open a PR.
- Keep changes focused (fix, add an example, or translate).
- Use clear headings and short sections; prefer code blocks for commands.
- For doc fixes, reference the file path in your PR description.

## Support & Issues

Open an issue for bugs, missing steps, or platform-specific problems. Include:

- OS / firmware version
- The exact command and output (copy/paste)
- Which guide you followed

## License

MIT License
