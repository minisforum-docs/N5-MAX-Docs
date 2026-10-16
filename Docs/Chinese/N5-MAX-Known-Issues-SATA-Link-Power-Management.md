# Linux SATA 链路电源管理问题

除预装 MinisCloud OS 外的任何 Linux 发行版上，五条 SATA 链路会进入低功耗空闲状态，
而 JMB585 控制器并不总能可靠地退出该状态：空闲时硬盘指示灯呈缓慢 "呼吸" 状态，
下次访问可能以读写错误和文件系统错误告终（日志式文件系统可能严重损坏）。请将链路
策略设为 `max_performance` —— 立即执行并使其持久化。

## 修复

### 立即生效（重启前有效）

```bash
echo max_performance | sudo tee /sys/class/scsi_host/host*/link_power_management_policy
```

验证 —— 全部五个 host 都必须报告 `max_performance`：

```bash
cat /sys/class/scsi_host/host*/link_power_management_policy
```

### 持久化：辅助包（推荐）

该策略在每次重启后会恢复为内核默认值。
[Tools/N5MAX-SATA-LPM-Fix](/Tools/N5MAX-SATA-LPM-Fix/README.md) 提供了一个小型
`.deb` 包，安装后立即生效，并自动配置持久化机制，无需重启。从该目录的 `dist/`
下载 `n5max-sata-lpm-fix_1.0.0_all.deb`，然后：

```bash
sudo apt install ./n5max-sata-lpm-fix_1.0.0_all.deb
```

验证：

```bash
cat /sys/class/scsi_host/host*/link_power_management_policy
```

全部五个 host 都必须报告 `max_performance`。卸载与构建说明见
[包文档](/Tools/N5MAX-SATA-LPM-Fix/README.md)。

### 手动配置（高级用户）

如果不想安装上述包，也可以手动配置持久化 —— 二选一。两种方式都需要文本编辑器，
下文以 `nano` 为例：在 `nano` 中按 `Ctrl+O` 再按 `Enter` 保存，按 `Ctrl+X` 退出
（多数终端中可用 `Ctrl+Shift+V` 或右键粘贴文本）。

**方式 A —— udev 规则。** 用编辑器打开新文件：

```bash
sudo nano /etc/udev/rules.d/99-n5max-sata-lpm.rules
```

粘贴以下内容：

```text
# N5 MAX: keep SATA link power management at max_performance
ACTION=="add|change", SUBSYSTEM=="scsi_host", ATTR{link_power_management_policy}="max_performance"
```

保存并退出 `nano`（`Ctrl+O`、`Enter`、`Ctrl+X`），然后加载规则：

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=scsi_host --action=change
```

**方式 B —— systemd 服务。** 用编辑器打开新文件：

```bash
sudo nano /etc/systemd/system/n5max-sata-lpm-fix.service
```

粘贴以下内容：

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

保存并退出 `nano`（`Ctrl+O`、`Enter`、`Ctrl+X`），然后启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now n5max-sata-lpm-fix.service
```

## 背景

SATA 链路电源管理会让空闲链路进入低功耗状态并在需要时唤醒；本控制器
（`0000:35:00.0`，全部五个 host）与部分硬盘型号的唤醒协商不可靠，导致链路掉线。
禁用该特性对整机功耗没有可测量的影响。

## 说明

- MinisCloud OS 已应用此修复；仅其它 Linux 发行版需要。
- 修复后，空闲时硬盘指示灯的 "呼吸" 现象将消失。
