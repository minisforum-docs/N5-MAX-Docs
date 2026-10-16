# N5 MAX Windows LLM 推理最佳实践

本指南介绍在安装 Windows 11（而非预装 MinisCloud OS）时，如何将 N5 MAX 配置用于
本地 LLM 推理。内容涵盖系统要求、显存管理以及推荐的推理引擎。

## 目录

- [第 1 步：系统要求](#第-1-步系统要求)
- [第 2 步：Windows 上的显存](#第-2-步windows-上的显存)
- [第 3 步：推理引擎](#第-3-步推理引擎)
- [第 4 步：性能预期](#第-4-步性能预期)
- [参考资料](#参考资料)

## 第 1 步：系统要求

- **Windows 11（25H2）**，并安装所有当前更新。
- **AMD Software: Adrenalin Edition**，驱动 **25.8.1 WHQL 或更新版本** —— 请从
  AMD 官网安装，不要使用 Windows Update 可能提供的基础显示驱动。旧版驱动可能无法
  加载大模型。
- 除[第 2 步](#第-2-步windows-上的显存)中的设置外，无需对 N5 MAX 固件做其它修改。

## 第 2 步：Windows 上的显存

Windows 将 GPU 可用内存划分为两个池：

- **专用 GPU 内存** —— 固件为 iGPU 预留的容量（即 BIOS 中的
  `UMA Frame buffer Size` 设置）；这部分内存会从 CPU 可用内存中扣除。
- **共享 GPU 内存** —— 由 Direct3D 从系统内存中分配的池，在当前 Windows 版本中其
  大小固定为 `(已安装内存 − 专用 GPU 内存) / 2`。

因此应用程序可用的总显存为
`专用显存 + (已安装内存 − 专用显存) / 2`。

要运行大尺寸 LLM，需要**调大专用显存** —— 下面两种方式修改的是同一个固件级设置：

1. **BIOS** —— `Setup` → `AMD CBS` → `NBIO Common Options` →
   `GFX Configuration` → `UMA Frame buffer Size`。
2. **AMD Software: Adrenalin Edition** —— `Performance` → `Tuning` →
   `Variable Graphics Memory`（AMD 推荐的方式；修改后系统会重启）。

Windows 不具备 Linux 那样的自定义共享显存分配能力（详见
[Linux LLM 推理最佳实践](/Docs/Chinese/N5-MAX-Linux-LLM-Inference-Best-Practices.md#第-4-步使用-amd-ttm-配置共享显存)）。

## 第 3 步：推理引擎

与 Linux 相同，推理引擎只是 **API 服务端**（OpenAI 兼容 HTTP 接口，无聊天界面）——
需要搭配独立客户端（聊天前端、编程助手或自研应用）使用。

- **llama.cpp —— 主线 Vulkan 版**：llama.cpp 官方提供的 Windows Vulkan 后端二进制
  即可很好地驱动 Radeon 8060S。从
  <https://github.com/ggml-org/llama.cpp/releases> 下载
  `llama-b<build>-bin-win-vulkan-x64.zip`，解压后对 GGUF 模型运行
  `llama-server.exe`。Vulkan 运行时随[第 1 步](#第-1-步系统要求)中的 AMD 驱动一同安装。
- **llama.cpp（ROCm）—— `lemonade-sdk/llamacpp-rocm`**：内置 AMD ROCm 7 运行时的
  每日构建，AMD 优化路线。Ryzen AI Max+ 395 请下载 **gfx1151** 资产（例如
  `llama-b<build>-windows-rocm-gfx1151-x64.zip`）：
  <https://github.com/lemonade-sdk/llamacpp-rocm>
- **Lemonade —— `lemonade-sdk/lemonade`**：AMD 的 Windows 本地 AI 方案 —— 安装
  服务、管理模型下载，并通过 AMD 调优的引擎提供 OpenAI、Anthropic 和 Ollama 兼容
  API（Ollama 的托管替代品）。安装程序与文档：<https://lemonade-server.ai> ·
  <https://github.com/lemonade-sdk/lemonade>

**不推荐在此平台使用 Ollama**，原因与 Linux 相同：其内置的 llama.cpp 落后于主线，
且其模型仓库提供的量化质量普遍低于当前社区量化。

## 第 4 步：性能预期

相同模型与引擎下，Windows 的 LLM 推理速度可能略低于 Linux —— 这是驱动栈之间的正常
差异，并非机器缺陷。如需最大吞吐量，请使用
[Linux LLM 推理最佳实践](/Docs/Chinese/N5-MAX-Linux-LLM-Inference-Best-Practices.md)。

## 参考资料

- AMD 驱动下载：<https://www.amd.com/en/support/download/drivers.html>
- AMD 常见问题：Variable Graphics Memory、VRAM 与 AI 模型大小：
  <https://www.amd.com/en/blogs/2025/faqs-amd-variable-graphics-memory-vram-ai-model-sizes-quantization-mcp-more.html>
- AMD："AI Unleashed: How Ryzen AI Max+ Makes Supercomputing Personal"
  （驱动与 VGM 建议）：
  <https://www.amd.com/en/blogs/2025/amd-ryzen-ai-max-personal-ai-supercomputing-guide.html>
