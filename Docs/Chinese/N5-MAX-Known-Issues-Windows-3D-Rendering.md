# Windows 3D 渲染错误（专用显存过小）

N5 MAX 上的已知现象：专用显存设为 1 GB 或 2 GB 时，3DMark Time Spy 可能偶尔出现
渲染错误。此为可选修复 —— 仅当 3D 应用中出现错误时处理。

## 修复

将专用显存**调整到大于你所使用的 3D 软件/游戏所需的显存** —— 4 GB 只是我们在测试
中解决 3DMark Time Spy 的取值，其它软件可能需要更多。下面两种方式修改的是同一个
固件级设置：

1. **BIOS** —— `Setup` → `AMD CBS` → `NBIO Common Options` →
   `GFX Configuration` → `UMA Frame buffer Size`。
2. **AMD Software: Adrenalin Edition** —— `Performance` → `Tuning` →
   `Variable Graphics Memory`。

随后重启并重新运行出现问题的应用。

## 背景

在 N5 MAX 上以 1 GB 和 2 GB 专用显存运行 3DMark Time Spy 时曾偶发观察到该现象。
对于 LLM 工作负载，推荐设置远大于此，因此通常不会遇到该问题。
