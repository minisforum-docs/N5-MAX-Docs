# Linux SATA link power management issue

On any Linux distribution other than the pre-installed MinisCloud OS, the
five SATA links idle in a low-power state that the JMB585 controller cannot
always leave cleanly: while idle the HDD LEDs show a slow "breathing"
pattern, and the next access can fail with read/write and filesystem errors
(journaled filesystems can suffer severe corruption). Set the link policy to
`max_performance` — immediately and persistently.

## Fix

### Apply now (until next reboot)

```bash
echo max_performance | sudo tee /sys/class/scsi_host/host*/link_power_management_policy
```

Verify — all five hosts must report `max_performance`:

```bash
cat /sys/class/scsi_host/host*/link_power_management_policy
```

### Make it persistent: helper package (recommended)

The policy resets to the kernel default on every reboot.
[Tools/N5MAX-SATA-LPM-Fix](/Tools/N5MAX-SATA-LPM-Fix/README.md) provides a
small `.deb` package that applies the fix immediately and sets up both
persistence mechanisms automatically, without a reboot. Download
`n5max-sata-lpm-fix_1.0.0_all.deb` from its `dist/` directory, then:

```bash
sudo apt install ./n5max-sata-lpm-fix_1.0.0_all.deb
```

Verify:

```bash
cat /sys/class/scsi_host/host*/link_power_management_policy
```

All five hosts must report `max_performance`. Uninstall and build
instructions are in the
[package documentation](/Tools/N5MAX-SATA-LPM-Fix/README.md).

### Manual setup (advanced users)

If you prefer not to install the package, configure the persistence by hand —
pick **one** method. Both methods need a text editor; the examples use `nano`.
In `nano`, save with `Ctrl+O` followed by `Enter`, and exit with `Ctrl+X`
(in most terminals, paste text with `Ctrl+Shift+V` or a right-click).

**Option A — udev rule.** Open a new file in the editor:

```bash
sudo nano /etc/udev/rules.d/99-n5max-sata-lpm.rules
```

Paste this content:

```text
# N5 MAX: keep SATA link power management at max_performance
ACTION=="add|change", SUBSYSTEM=="scsi_host", ATTR{link_power_management_policy}="max_performance"
```

Save and exit `nano` (`Ctrl+O`, `Enter`, `Ctrl+X`), then load the rules:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=scsi_host --action=change
```

**Option B — systemd service.** Open a new file:

```bash
sudo nano /etc/systemd/system/n5max-sata-lpm-fix.service
```

Paste this content:

```ini
[Unit]
Description=N5 MAX: keep SATA link power management at max_performance
After=systemd-udev-settle.service
Wants=systemd-udev-settle.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/sh -c 'for f in /sys/class/scsi_host/host*/link_power_management_policy; do if [ -e "$f" ]; then echo max_performance > "$f"; fi; done'

[Install]
WantedBy=multi-user.target
```

Save and exit `nano` (`Ctrl+O`, `Enter`, `Ctrl+X`), then enable the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now n5max-sata-lpm-fix.service
```

## Background

SATA link power management parks an idle link in a low-power state and wakes
it on demand; this controller (`0000:35:00.0`, all five hosts) does not
negotiate the wake-up reliably with some drive models, so the link drops.
Disabling the feature has no measurable effect on power consumption.

## Notes

- MinisCloud OS already applies this fix; it is only needed on other Linux
  distributions.
- After the fix, the idle HDD LED breathing pattern disappears.
