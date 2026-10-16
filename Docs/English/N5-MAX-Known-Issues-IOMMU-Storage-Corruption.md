# Linux storage corruption with AMD IOMMU

Under high I/O or memory load, the drives on any Linux distribution other
than the pre-installed MinisCloud OS can fail reads and writes and corrupt
data — copy-on-write filesystems such as ZFS usually stop with I/O errors
instead of damaging existing data, while journaled filesystems can suffer
severe corruption. Apply one of the solutions below before putting the
machine into service.

## Fix

### Current solutions

Add **one** of the following to the kernel command line and reboot:

1. `iommu=pt` — keeps the IOMMU enabled with passthrough mapping for host
   devices; virtualization and device passthrough keep working. Downside:
   DMA is not translated, weakening the memory protection the IOMMU
   normally provides.
2. `iommu=off` (equivalently `amd_iommu=off`) — disables DMA translation
   entirely; it also maximizes iGPU memory access performance. Trade-off:
   the integrated NPU and virtualization (device passthrough) become
   unavailable.
3. `amd_iommu=pgtbl_v2` — keeps the IOMMU translating with its v2 page
   tables; use this if you are concerned about the reduced DMA protection
   of `iommu=pt`.

**To add a parameter on Debian/Ubuntu:**

Open the GRUB configuration file with the `nano` editor:

```bash
sudo nano /etc/default/grub
```

Find the line starting with `GRUB_CMDLINE_LINUX_DEFAULT` and add the
parameter inside the quotes. For `iommu=pt`, the line should read:

```text
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash iommu=pt"
```

Save and exit `nano`: press `Ctrl+O`, then `Enter` to write the file, then
`Ctrl+X` to exit the editor.

Finally, regenerate the boot configuration and reboot:

```bash
sudo update-grub
sudo reboot
```

### Permanent solutions

- **Current BIOS + patched kernel** — upgrade to Linux 7.3 or newer, or to a
  distribution kernel that carries the backport. The kernel then disables
  the buggy feature itself, and no workaround is needed for data safety.
- **Updated BIOS + any kernel** — a future N5 MAX BIOS that integrates the
  fixed AMD AGESA PI resolves the issue at the firmware level, independent
  of the kernel version. That BIOS is not available yet: it depends on a
  new AGESA PI release from AMD, so until it ships, use one of the current
  solutions above (or the patched-kernel route).

Check whether your kernel carries the fix — on fixed kernels the kernel log
shows `pci 0000:00:00.0: enhanced atomics disabled` when the firmware has
the feature enabled:

```bash
sudo dmesg | grep "enhanced atomics"
```

## Background

The BIOS enables a PCIe root-port feature ("enhanced atomics") on ports whose
devices do not support it, corrupting DMA transfers that use high I/O
addresses — which is why the failure looks like an IOMMU problem. The
upstream fix (commit `4fde4482`) disables the feature on the affected AMD
NBIO 7.7/7.11 root ports at boot and on resume; the JMB585 SATA ports (five
HDD bays) and the M.2 NVMe slots are the devices most commonly hit.

Authoritative technical description — kernel mailing list thread:
<https://lore.kernel.org/linux-ide/20260908190600.226485-1-mario.limonciello@amd.com/>
