# N5 MAX

N5 MAX 是一台基于 AMD Ryzen™ AI Max+ 395（Strix Halo）平台打造的五盘位 AI NAS。
其核心特性是统一内存：CPU、GPU 与 NPU 共享同一组 LPDDR5X 内存，使 Radeon 8060S
无需独立显卡即可调用数十 GB 内存进行本地 LLM 推理。

本文档包含接口框图以及 N5 MAX 与 N5 系列其它机型的对比。

**在安装第三方操作系统之前，请先阅读
[已知问题与解决方案](/Docs/Chinese/N5-MAX-Known-Issues.md)：在 MinisCloud OS
之外的任何 Linux 发行版上，有两个问题必须手动修复。**

## 索引

- [N5 MAX 基础指南](/Docs/Chinese/N5-MAX-BaseGuide.md) —— 概览、接口框图、N5 系列对比
- [N5 MAX Linux LLM 推理最佳实践](/Docs/Chinese/N5-MAX-Linux-LLM-Inference-Best-Practices.md) —— 内核、BIOS、IOMMU、共享显存、推理引擎
- [N5 MAX Windows LLM 推理最佳实践](/Docs/Chinese/N5-MAX-Windows-LLM-Inference-Best-Practices.md) —— 显存、推理引擎、性能预期
- [N5 MAX 已知问题与解决方案](/Docs/Chinese/N5-MAX-Known-Issues.md) —— 必需的 Linux 修复与 Windows 注意事项
    - ⚠️ [Linux 存储损坏（AMD IOMMU）](/Docs/Chinese/N5-MAX-Known-Issues-IOMMU-Storage-Corruption.md) —— 内核参数修复
    - ⚠️ [SATA 链路电源管理问题](/Docs/Chinese/N5-MAX-Known-Issues-SATA-Link-Power-Management.md) —— 辅助 `.deb` 修复；手动方式仅供高级用户
    - 🟡 [Windows 3D 渲染错误（专用显存过小）](/Docs/Chinese/N5-MAX-Known-Issues-Windows-3D-Rendering.md) —— 遇到再修复

## 接口框图

![N5 MAX 接口框图](/Datasheet/N5-MAX-Block-Diagram.png)

## N5 系列对比

| 项目                | N5 MAX                                                                                       | N5 PRO                                                    | N5 Air                                                                                    |
| ------------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| CPU                 | AMD Ryzen™ AI Max+ 395（16C/32T，最高 5.1 GHz）                                              | AMD Ryzen™ AI 9 HX PRO 370 / 375（12C/24T，最高 5.1 GHz） | AMD Ryzen™ 7 255（8C/16T，最高 4.9 GHz）；可选 Ryzen™ 5 7640HS（6C/12T，最高 5.0 GHz）    |
| CPU 功耗模式        | Balance 90 W                                                                                 | 45 W                                                      | 45 W                                                                                      |
| GPU                 | Radeon 8060S，40 CU                                                                          | Radeon 890M                                               | Radeon 780M；可选 Radeon 760M                                                             |
| NPU                 | 最高 50 TOPS（整机 126 TOPS）                                                                | 最高 55 TOPS（PRO 375）                                   | 无                                                                                        |
| 内存                | LPDDR5X 统一内存（板载），64 / 128 GB，8000 MT/s                                             | DDR5 SO-DIMM ×2（ECC），最大 96 GB，5600 MT/s             | DDR5 SO-DIMM ×2（非 ECC），最大 96 GB，5600 MT/s                                          |
| 硬盘位              | 5 × 3.5"/2.5" SATA 3.0                                                                       | 5 × 3.5"/2.5" SATA 3.0                                    | 5 × 3.5"/2.5" SATA 3.0                                                                    |
| M.2 NVMe 插槽       | 共 5 个：A（PCIe 4.0 x4），B–E（PCIe 4.0 x1）                                                | 共 3 个；可选 U.2 适配器                                  | 共 3 个                                                                                   |
| PCIe 扩展           | 无 —— 为容纳更高功耗 CPU 的更大散热器，取消了 HHHL PCIe 插槽                                 | PCIe x16 插槽（PCIe 4.0 x4），半高半长                    | PCIe x16 插槽（PCIe 4.0 x4），半高半长                                                    |
| 以太网              | 2 × 10GbE RJ45                                                                               | 10GbE + 5GbE                                              | 10GbE + 5GbE                                                                              |
| USB4 端口           | 2 × USB4 v2（80 Gbps）后置 + 1 × USB4（40 Gbps）前置                                         | 2 × USB4（40 Gbps）                                       | 2 × USB4（40 Gbps）                                                                       |
| 视频输出            | HDMI 2.1 FRL（最高 8K@60 / 4K@144）+ USB4 Alt DP                                             | HDMI 2.1 FRL + USB4 Alt DP                                | HDMI 2.1 FRL + USB4 Alt DP                                                                |
| 电源                | 内置电源，AC 100–240 V，最大 250 W                                                           | DC 19 V / 280 W 适配器                                    | DC 19 V / 280 W 适配器                                                                    |
| 尺寸 / 重量         | 199 × 202.4 × 252.3 mm / 5.8 kg                                                              | 199 × 202 × 252 mm / 5 kg                                 | 199 × 202 × 252 mm / 4 kg                                                                 |

说明：

- N5 MAX 的 M.2 插槽 A 为 PCIe 4.0 x4，插槽 B–E 为 PCIe 4.0 x1。插槽 B 支持
  2230/2280 规格，出厂系统盘即安装于此。各插槽的物理位置请查阅用户手册。
