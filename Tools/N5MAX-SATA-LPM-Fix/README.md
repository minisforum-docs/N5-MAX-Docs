# N5 MAX SATA LPM fix: helper package

This directory contains the source of `n5max-sata-lpm-fix`, a small `.deb`
package that applies the persistent fix for the
[SATA link power management issue](/Docs/English/N5-MAX-Known-Issues-SATA-Link-Power-Management.md).

On affected kernels the five SATA hosts default to the aggressive
`min_power_with_partial` link power management policy. With the JMicron JMB585
controller and some drives this leads to link wake-up failures, I/O errors and
potential filesystem corruption. This package sets
`link_power_management_policy = max_performance` for all SCSI hosts, reliably
and persistently.

## What gets installed

| File                                                 | Purpose                                                                         |
| ---------------------------------------------------- | ------------------------------------------------------------------------------- |
| `/usr/lib/udev/rules.d/99-n5max-sata-lpm.rules`      | Sets `max_performance` when a SCSI host is added (boot and hot-plug)            |
| `/usr/lib/systemd/system/n5max-sata-lpm-fix.service` | One-shot service that re-applies the setting to all existing SCSI hosts at boot |

The package's `postinst` script reloads the udev rules and starts the service,
so the fix applies immediately after installation, without a reboot.

## Install

```bash
sudo apt install ./dist/n5max-sata-lpm-fix_1.0.0_all.deb
```

(or `sudo dpkg -i ./dist/n5max-sata-lpm-fix_1.0.0_all.deb`)

## Verify

```bash
cat /sys/class/scsi_host/host*/link_power_management_policy
```

All hosts must report `max_performance`.

## Verification status

This package was tested end-to-end on an N5 MAX test unit (Ubuntu 26.04,
kernel 7.0.0-38): installation applies `max_performance` to all five SATA
hosts immediately, the udev rule re-applies it when the subsystem is
re-triggered, the systemd service re-applies it on restart, and removal leaves
no rule, unit file, or enabled service behind.

## Uninstall

```bash
sudo apt remove n5max-sata-lpm-fix
```

Notes on removal:

- The rule and the service are removed. The currently applied policy stays in
  effect until the next reboot; after that the kernel default returns
  (`min_power_with_partial` on affected kernels). To restore the default
  immediately as well, run `sudo systemctl reboot`.

- Removing the package does not touch your data or storage layout.

## Scope and caveats

- The rules apply `max_performance` to every SCSI host in the system, not only
  to the JMicron controller. On the N5 MAX all SATA hosts belong to the
  JMB585, so the scope is exactly the affected controller; on other systems
  this merely disables link power management for their SATA controllers too.
- Disabling SATA link power management has no measurable effect on system
  power consumption.
- The package is intended for Debian-based systems (Ubuntu, Proxmox VE,
  TrueNAS SCALE, ...).

## Build from source

```bash
./build.sh
```

The script only needs `dpkg-deb` (part of `dpkg`); it assembles the package
into `dist/`. No other build tools are required.

## License

MIT — same as the rest of this repository.
