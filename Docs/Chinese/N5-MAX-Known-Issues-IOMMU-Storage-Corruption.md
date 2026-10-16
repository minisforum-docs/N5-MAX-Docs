# Linux 存储损坏（AMD IOMMU）

在高 I/O 或高内存负载下，除预装 MinisCloud OS 外的任何 Linux 发行版上，硬盘都可能
出现读写失败并损坏数据 —— ZFS 等写时复制（CoW）文件系统通常会以 I/O 错误中止而
不会破坏已有数据，日志式文件系统则可能遭到严重损坏。请在投入使用前应用以下任一
解决方案。

## 修复

### 当前解决方案

在内核命令行中添加**以下之一**并重启：

1. `iommu=pt` —— IOMMU 保持启用、对主机设备使用直通映射；虚拟化与设备直通正常
   工作。代价：DMA 不做地址转换，会削弱 IOMMU 通常提供的内存保护。
2. `iommu=off`（等价于 `amd_iommu=off`）—— 完全禁用 DMA 地址转换；同时最大化
   iGPU 内存访问性能。代价：集成 NPU 与虚拟化（设备直通）不可用。
3. `amd_iommu=pgtbl_v2` —— IOMMU 保持地址转换并使用 v2 页表；担心 `iommu=pt`
   削弱 DMA 保护的用户可选此项。

**在 Debian/Ubuntu 上添加参数：**

用 `nano` 编辑器打开 GRUB 配置文件：

```bash
sudo nano /etc/default/grub
```

找到以 `GRUB_CMDLINE_LINUX_DEFAULT` 开头的行，把参数加进引号内。以
`iommu=pt` 为例，该行应改为：

```text
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash iommu=pt"
```

保存并退出 `nano`：先按 `Ctrl+O`，再按 `Enter` 写入文件，然后按 `Ctrl+X`
退出编辑器。

最后重新生成引导配置并重启：

```bash
sudo update-grub
sudo reboot
```

### 彻底解决方案

- **当前 BIOS + 已打补丁的内核** —— 升级到 Linux 7.3 或更新版本，或使用包含该
  回移补丁的发行版内核。内核会自行禁用该缺陷特性，数据安全方面无需再使用任何
  临时方案。
- **更新后的 BIOS + 任意内核** —— 集成修复版 AMD AGESA PI 的未来 N5 MAX BIOS 可
  在固件层面解决该问题，不依赖内核版本。该 BIOS 尚未发布：它取决于 AMD 发布新版
  AGESA PI；在它推出之前，请使用上面的任一当前解决方案（或升级内核）。

检查你的内核是否已包含修复 —— 修复后的内核在固件启用该特性时，日志中会显示
`pci 0000:00:00.0: enhanced atomics disabled`：

```bash
sudo dmesg | grep "enhanced atomics"
```

## 背景

BIOS 在本不支持该特性的设备所连接的 PCIe 根端口上启用了 "enhanced atomics" 特性，
导致使用高位 I/O 地址的 DMA 传输数据被破坏 —— 这就是故障表现得像 IOMMU 问题的
原因。上游修复（commit `4fde4482`）在启动和恢复时禁用受影响的 AMD NBIO 7.7/7.11
根端口上的该特性；最常受影响的设备是 JMB585 SATA 端口（五个硬盘位）与 M.2 NVMe
插槽。

权威技术说明（内核邮件列表讨论串）：
<https://lore.kernel.org/linux-ide/20260908190600.226485-1-mario.limonciello@amd.com/>
