# N5 MAX 已知问题与解决方案

本节列出 N5 MAX 的已知问题及其修复方法，每个问题单独占一页。

- ⚠️ **重要** —— 影响除预装 MinisCloud OS 之外的所有操作系统安装；请在投入使用前
  完成修复。
- 🟡 **可选** —— 仅在遇到问题时修复。

## 索引

- ⚠️ [Linux 存储损坏（AMD IOMMU）](/Docs/Chinese/N5-MAX-Known-Issues-IOMMU-Storage-Corruption.md) —— 高负载下硬盘可能出错并损坏数据；通过内核参数或升级内核修复
- ⚠️ [SATA 链路电源管理问题](/Docs/Chinese/N5-MAX-Known-Issues-SATA-Link-Power-Management.md) —— 空闲链路无法可靠唤醒；安装辅助 `.deb`（推荐）或手动配置
- 🟡 [Windows 3D 渲染错误（专用显存过小）](/Docs/Chinese/N5-MAX-Known-Issues-Windows-3D-Rendering.md) —— 1–2 GB 专用显存下 3DMark Time Spy 可能偶尔渲染错误；按软件所需显存调整
