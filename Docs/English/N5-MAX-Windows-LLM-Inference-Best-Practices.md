# N5 MAX Windows LLM Inference Best Practices

This guide describes how to configure the N5 MAX for local LLM inference when
you install Windows 11 instead of the pre-installed MinisCloud OS. It covers
the system requirements, graphics memory, and the recommended inference
engines.

## Table of Contents

- [Step 1: System requirements](#step-1-system-requirements)
- [Step 2: Graphics memory on Windows](#step-2-graphics-memory-on-windows)
- [Step 3: Inference engines](#step-3-inference-engines)
- [Step 4: Performance expectations](#step-4-performance-expectations)
- [References](#references)

## Step 1: System requirements

- **Windows 11 (25H2)** with all current updates.
- **AMD Software: Adrenalin Edition**, driver **25.8.1 WHQL or newer** —
  install it from AMD's website, not the basic display driver Windows Update
  may provide. Older drivers may fail to load large models.
- No further firmware changes are needed beyond the settings in
  [Step 2](#step-2-graphics-memory-on-windows).

## Step 2: Graphics memory on Windows

Windows splits the GPU memory into two pools:

- **Dedicated GPU memory** — reserved for the iGPU by the firmware (the BIOS
  `UMA Frame buffer Size` setting); it is subtracted from the RAM available to
  the CPU.
- **Shared GPU memory** — a pool that Direct3D allocates from system RAM; on
  current Windows versions its size is fixed at
  `(installed RAM − dedicated GPU memory) / 2`.

Total graphics memory available to applications is
`dedicated + (installed RAM − dedicated) / 2`.

To run large LLMs, increase the **dedicated graphics memory** — both methods
below set the same firmware-level value:

1. **BIOS** — `Setup` → `AMD CBS` → `NBIO Common Options` →
   `GFX Configuration` → `UMA Frame buffer Size`.
2. **AMD Software: Adrenalin Edition** — `Performance` → `Tuning` →
   `Variable Graphics Memory` (AMD's recommended path; the system restarts to
   apply).

Windows does not provide Linux-style custom shared-memory allocation (see
[Linux LLM Inference Best Practices](/Docs/English/N5-MAX-Linux-LLM-Inference-Best-Practices.md#step-4-shared-memory-configuration-with-amd-ttm)).

## Step 3: Inference engines

As on Linux, the engine is only the **API server** (OpenAI-compatible HTTP,
no chat interface) — pair it with a separate client (a chat UI, a coding
agent, or your own application).

- **llama.cpp — mainline Vulkan build**: the upstream Windows binaries with a
  Vulkan backend drive the Radeon 8060S well. Download
  `llama-b<build>-bin-win-vulkan-x64.zip` from
  <https://github.com/ggml-org/llama.cpp/releases>, unpack it, and run
  `llama-server.exe` against a GGUF model. The Vulkan runtime comes with the
  AMD driver from [Step 1](#step-1-system-requirements).
- **llama.cpp with ROCm — `lemonade-sdk/llamacpp-rocm`**: nightly builds with
  AMD's ROCm 7 runtime built in, the AMD-optimized path. For the Ryzen AI
  Max+ 395 download the **gfx1151** asset (for example
  `llama-b<build>-windows-rocm-gfx1151-x64.zip`):
  <https://github.com/lemonade-sdk/llamacpp-rocm>
- **Lemonade — `lemonade-sdk/lemonade`**: AMD's local-AI stack for Windows —
  installs a service, manages model downloads, and serves OpenAI-, Anthropic-
  and Ollama-compatible APIs with AMD-tuned engines (the managed alternative
  to Ollama). Installer and documentation: <https://lemonade-server.ai> ·
  <https://github.com/lemonade-sdk/lemonade>

**Ollama is not recommended** on this platform, for the same reasons as on
Linux: its bundled llama.cpp lags behind mainline, and its registry
quantizations are generally of lower quality than current community quants.

## Step 4: Performance expectations

LLM inference on Windows can be slightly slower than on Linux for the same
model and engine — a normal difference between the driver stacks, not a
defect. For maximum throughput, use
[Linux LLM Inference Best Practices](/Docs/English/N5-MAX-Linux-LLM-Inference-Best-Practices.md).

## References

- AMD driver downloads: <https://www.amd.com/en/support/download/drivers.html>
- AMD FAQ: Variable Graphics Memory, VRAM and AI model sizes:
  <https://www.amd.com/en/blogs/2025/faqs-amd-variable-graphics-memory-vram-ai-model-sizes-quantization-mcp-more.html>
- AMD: "AI Unleashed: How Ryzen AI Max+ Makes Supercomputing Personal"
  (driver and VGM recommendations):
  <https://www.amd.com/en/blogs/2025/amd-ryzen-ai-max-personal-ai-supercomputing-guide.html>
