# N5 MAX Linux LLM 推理最佳实践

本指南介绍在自行安装的 Debian、Ubuntu 或基于 Debian/Ubuntu 的系统上，如何将
N5 MAX 配置为本地 LLM 推理服务器。内容涵盖内核版本要求、BIOS 设置、最大化 GPU
性能的内核参数、共享显存配置、GPU 访问权限以及推荐的推理引擎。

第三方 Linux 安装中需要手动修复的硬件问题，请参阅单独的
[已知问题与解决方案](/Docs/Chinese/N5-MAX-Known-Issues.md)。

## 目录

- [第 1 步：Linux 内核版本要求](#第-1-步linux-内核版本要求)
- [第 2 步：BIOS 设置](#第-2-步bios-设置)
- [第 3 步：内核参数（IOMMU）](#第-3-步内核参数iommu)
- [第 4 步：使用 amd-ttm 配置共享显存](#第-4-步使用-amd-ttm-配置共享显存)
- [第 5 步：GPU 访问权限](#第-5-步gpu-访问权限)
- [第 6 步：推理引擎](#第-6-步推理引擎)
- [第 7 步：验证配置](#第-7-步验证配置)
- [参考资料](#参考资料)

## 第 1 步：Linux 内核版本要求

Radeon 8060S（`gfx1151`）需要内核中的 AMD KFD 驱动修复；缺少这些修复时，GPU 计算
负载可能无法初始化或行为异常。

- **Ubuntu 26.04 LTS** 自带的内核已包含全部所需修复，也是我们在 N5 MAX 测试机上
  验证过的配置。
- **Ubuntu 24.04 LTS**：请使用 OEM 内核 **6.14.0-1018 或更新版本** —— 默认的 HWE
  内核低于此要求。
- **内核 6.18.4 及更新版本**已包含 KFD 修复；请保持内核更新，以持续获得后续修复。

官方仅支持 Debian、Ubuntu 及其衍生版本。

## 第 2 步：BIOS 设置

进入 BIOS 设置界面（开机时按对应按键，参见用户手册）。有一个设置与 LLM 推理有关：

**专用显存（iGPU 预分配）** —— `Setup` → `AMD CBS` → `NBIO Common Options` →
`GFX Configuration` → `UMA Frame buffer Size`。

将其设为**最小值**。Linux 下 GPU 不需要大量固件预分配内存 —— GPU 显存由系统动态
管理，并通过[第 4 步](#第-4-步使用-amd-ttm-配置共享显存)中的 `amd-ttm` 工具配置。
不要将此设置保留为 "Auto"：视固件版本不同，它可能预留非常大的内存，导致这部分内存
对操作系统不可见。

## 第 3 步：内核参数（IOMMU）

为获得最大 GPU 内存访问性能，请在内核命令行中添加 `iommu=off`。厂商文档显示，
在此平台上禁用 IOMMU 后提示处理（prompt processing）吞吐量最多可提升约 15%。

如果这台机器还要运行带 PCIe 直通的虚拟机（例如 Proxmox VE），请改用 `iommu=pt`：
它保持 IOMMU 开启，并对主机设备使用直通映射。此时 GPU 性能提升幅度较小，并请注意
`iommu=off` 会禁用设备直通。

在 Debian/Ubuntu 上添加该参数：编辑 `/etc/default/grub`，将其追加到
`GRUB_CMDLINE_LINUX_DEFAULT`。修改后的示例：

```text
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash iommu=off"
```

保存文件后重新生成引导配置并重启：

```bash
sudo update-grub
sudo reboot
```

## 第 4 步：使用 amd-ttm 配置共享显存

默认情况下 GPU 共享显存上限约为系统内存的 50%，这会限制可加载的模型大小。AMD 的
`amd-ttm` 工具可以提升该上限。

安装（Ubuntu/Debian）：

```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
pipx install amd-debug-tools
```

打开新的终端，查看当前上限：

```bash
amd-ttm
```

设置可用的共享显存，建议的起始值：

| 已安装内存 | 建议值  |
| ---------- | ------- |
| 128 GB     | 112–120 |
| 64 GB      | 48–56   |

```bash
sudo amd-ttm --set 120
```

请为操作系统预留数 GB 内存。该内存池与 CPU 共享，且只有在模型实际占用时才会被消耗。

重启后生效。如需恢复内核默认值：执行 `sudo amd-ttm --clear`，然后重启。

## 第 5 步：GPU 访问权限

推理引擎需要访问 GPU 设备节点（`/dev/kfd`、`/dev/dri/`）。这些设备属于 `render`
和 `video` 组，请将当前用户加入这两个组 —— 否则引擎会因权限错误而无法启动：

```bash
sudo usermod -aG render,video "$USER"
```

注销并重新登录（或重启）使新的组成员关系生效；之后 `groups` 命令应列出 `render`
和 `video`。

## 第 6 步：推理引擎

AMD 为 Radeon 8060S 上的 LLM 推理维护了两个推荐组件。两者都是 **API 服务端**
（OpenAI 兼容的 HTTP 接口），不带聊天界面 —— 需要搭配 Open WebUI 等聊天前端、
编程助手或自研客户端使用。

- **llama.cpp（ROCm）—— `lemonade-sdk/llamacpp-rocm`**（仅引擎）：内置 ROCm 的
  llama.cpp 每日构建。Ryzen AI Max+ 395 请下载 **`gfx1151`** 资产（例如
  `llama-b<build>-ubuntu-rocm-gfx1151-x64.zip`）；仓库同时提供其它目标平台的构建，
  选错会报 "no compatible device" 错误。下载与用法见仓库 README：
  <https://github.com/lemonade-sdk/llamacpp-rocm>
- **Lemonade —— `lemonade-sdk/lemonade`**（模型管理器 + 服务端）：安装服务、下载
  并提供量化模型（类似 Ollama 的模型管理器），对外提供 OpenAI、Anthropic 和
  Ollama 兼容 API。按官方文档安装：<https://lemonade-server.ai> ·
  <https://github.com/lemonade-sdk/lemonade>

针对 Strix Halo 做过专门优化、值得关注的其它引擎（独立项目 —— 用于生产环境前请先
阅读其文档）：

- **charlie12345/ROCmFPX** —— 增加 AMD 专属权重格式（ROCmFP2/3/4/6/8）的 llama.cpp
  分支：<https://github.com/charlie12345/ROCmFPX>
- **gufo-org/gufo** —— 专为 `gfx1151` 编写的推理引擎，以容器镜像形式分发：
  <https://github.com/gufo-org/gufo>
- **peonist-ai/halogen-flash-server** —— 面向 Strix Halo 上 Qwen3.8-Flash-Next 模型
  系列的容器化引擎：<https://github.com/peonist-ai/halogen-flash-server>

**不推荐在此平台使用 Ollama**：其内置的 llama.cpp 落后于主线，缺少最新特性与
Strix Halo 优化，且其模型仓库提供的量化质量普遍低于当前社区量化（例如上述引擎所
使用的 Unsloth GGUF 量化方案）。

如果大模型加载时报显存不足而系统内存看起来还有余量，请回到
[第 4 步](#第-4-步使用-amd-ttm-配置共享显存) —— 共享显存上限通常是原因。

## 第 7 步：验证配置

重启后，确认内核参数已生效：

```bash
cat /proc/cmdline        # 应显示 iommu=off（或 iommu=pt）
ls /sys/class/iommu/     # 禁用 IOMMU 时该目录为空
```

固件预分配应较小（约 512 MB 至 2 GB）：

```bash
sudo dmesg | grep "VRAM memory ready"
```

共享显存应与 `amd-ttm` 的设置一致：

```bash
amd-ttm
sudo dmesg | grep "GTT memory ready"
```

## 参考资料

- AMD：在 Radeon Ryzen 上安装 ROCm（原生 Linux）：
  <https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html>
- AMD：Strix Halo 系统优化：
  <https://rocm.docs.amd.com/en/docs-7.2.0/how-to/system-optimization/strixhalo.html>
- AMD：各 ROCm 版本的 Linux 兼容性矩阵：
  <https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityryz/native_linux/native_linux_compatibility.html>
- AMD：Ryzen 平台的 llama.cpp 预编译二进制：
  <https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/advanced/advancedryz/linux/llm/llamacpp.html>
