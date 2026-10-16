# N5 MAX Linux LLM Inference Best Practices

This guide describes how to configure the N5 MAX as a local LLM inference
server on Debian, Ubuntu, or a Debian/Ubuntu-based system you install
yourself. It covers the kernel version requirements, the BIOS settings, the
kernel parameters for maximum GPU performance, the shared-memory
configuration, GPU access permissions, and the recommended inference engines.

Hardware issues that require manual fixes on third-party Linux installations
are documented separately in
[Known Issues and Solutions](/Docs/English/N5-MAX-Known-Issues.md).

## Table of Contents

- [Step 1: Linux kernel version requirements](#step-1-linux-kernel-version-requirements)
- [Step 2: BIOS settings](#step-2-bios-settings)
- [Step 3: Kernel parameters (IOMMU)](#step-3-kernel-parameters-iommu)
- [Step 4: Shared memory configuration with amd-ttm](#step-4-shared-memory-configuration-with-amd-ttm)
- [Step 5: GPU access permissions](#step-5-gpu-access-permissions)
- [Step 6: Inference engines](#step-6-inference-engines)
- [Step 7: Verify your configuration](#step-7-verify-your-configuration)
- [References](#references)

## Step 1: Linux kernel version requirements

The Radeon 8060S (`gfx1151`) needs kernel fixes to the AMD KFD driver; without
them GPU compute workloads may fail to initialize or behave unpredictably.

- **Ubuntu 26.04 LTS** ships a kernel with all required fixes and is the
  configuration validated on the N5 MAX test unit.
- **Ubuntu 24.04 LTS**: use the OEM kernel **6.14.0-1018 or newer** — the
  default HWE kernel is below the requirement.
- **Kernel 6.18.4 or newer** includes the KFD fixes; keep the kernel updated
  so that future fixes arrive.

Only Debian, Ubuntu and their derivatives are officially supported.

## Step 2: BIOS settings

Enter the BIOS setup utility (press the BIOS entry key during boot; see your
manual). One setting matters for LLM inference:

**Dedicated graphics memory (iGPU carve-out)** — `Setup` → `AMD CBS` →
`NBIO Common Options` → `GFX Configuration` → `UMA Frame buffer Size`.

Set it to its **minimum value**. On Linux the GPU does not need a large
firmware carve-out — GPU memory is managed dynamically and configured with the
`amd-ttm` tool in
[Step 4](#step-4-shared-memory-configuration-with-amd-ttm). Do not leave this
setting on "Auto": depending on the firmware it can reserve very large amounts
of memory, hiding it from the operating system.

## Step 3: Kernel parameters (IOMMU)

For maximum GPU memory access performance, add `iommu=off` to the kernel
command line. Vendor documentation reports up to roughly 15% higher
prompt-processing throughput on this platform with the IOMMU disabled.

If this machine also runs virtual machines with PCIe passthrough (for example
Proxmox VE), use `iommu=pt` instead: it keeps the IOMMU enabled with
passthrough mapping for host devices. GPU performance does not improve as
much, and note that `iommu=off` disables device passthrough and the
integrated NPU.

To add the parameter on Debian/Ubuntu, edit `/etc/default/grub` and append
it to `GRUB_CMDLINE_LINUX_DEFAULT`. Example result:

```text
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash iommu=off"
```

Then save the file, regenerate the boot configuration and reboot:

```bash
sudo update-grub
sudo reboot
```

## Step 4: Shared memory configuration with amd-ttm

By default the GPU shared-memory pool is limited to approximately 50% of
system RAM, which limits how large a model can load. AMD's `amd-ttm` tool
raises this limit.

Install it (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
pipx install amd-debug-tools
```

Open a new terminal and check the current limit:

```bash
amd-ttm
```

Set the usable shared memory. Suggested starting values:

| Installed memory | Suggested value |
| ---------------- | --------------- |
| 128 GB           | 112–120         |
| 64 GB            | 48–56           |

```bash
sudo amd-ttm --set 120
```

Leave several GB for the operating system. The pool is shared with the CPU
and is only consumed when a model actually uses it.

Reboot for the change to take effect. To revert to the kernel default:
`sudo amd-ttm --clear`, then reboot.

## Step 5: GPU access permissions

The LLM engines must open the GPU device nodes (`/dev/kfd`, `/dev/dri/`).
These belong to the `render` and `video` groups, so add your user to both —
otherwise the engines fail to start with permission errors:

```bash
sudo usermod -aG render,video "$USER"
```

Log out and back in (or reboot) for the new group membership to take effect;
`groups` should then list `render` and `video`.

## Step 6: Inference engines

AMD maintains two recommended components for running LLMs on the Radeon
8060S. Both are **API servers** (OpenAI-compatible HTTP APIs) without a chat
interface — pair them with a chat UI such as Open WebUI, a coding agent, or
your own client.

- **llama.cpp with ROCm — `lemonade-sdk/llamacpp-rocm`** (engine only):
  nightly llama.cpp builds with ROCm built in. For the Ryzen AI Max+ 395
  download the **`gfx1151`** asset (for example
  `llama-b<build>-ubuntu-rocm-gfx1151-x64.zip`); the repository also ships
  builds for other targets, and picking the wrong one produces
  "no compatible device" errors. Follow the repository README for download
  and usage steps: <https://github.com/lemonade-sdk/llamacpp-rocm>
- **Lemonade — `lemonade-sdk/lemonade`** (model manager + server): installs a
  service, downloads and serves quantized models (similar to Ollama's model
  manager) through OpenAI-, Anthropic- and Ollama-compatible APIs. Install it
  per the official guide: <https://lemonade-server.ai> ·
  <https://github.com/lemonade-sdk/lemonade>

Alternative engines with Strix Halo-specific optimizations, worth tracking
(independent projects — check their documentation before production use):

- **charlie12345/ROCmFPX** — llama.cpp fork that adds AMD-focused weight
  formats (ROCmFP2/3/4/6/8): <https://github.com/charlie12345/ROCmFPX>
- **gufo-org/gufo** — inference engine written specifically for `gfx1151`,
  distributed as container images: <https://github.com/gufo-org/gufo>
- **peonist-ai/halogen-flash-server** — containerized engine specialized for
  the Qwen3.8-Flash-Next model family on Strix Halo:
  <https://github.com/peonist-ai/halogen-flash-server>

**Ollama is not recommended** on this platform: its bundled llama.cpp lags
behind mainline and misses recent features and Strix Halo optimizations, and
its model registry's quantizations are generally of lower quality than
current community quants (for example the Unsloth GGUF recipes used by the
engines above).

If a large model fails to load with an out-of-memory error while system memory
appears free, revisit
[Step 4](#step-4-shared-memory-configuration-with-amd-ttm) — the shared-memory
limit is the usual cause.

## Step 7: Verify your configuration

After rebooting, check that the kernel parameter took effect:

```bash
cat /proc/cmdline        # should show iommu=off (or iommu=pt)
ls /sys/class/iommu/     # empty when the IOMMU is disabled
```

The firmware carve-out should be small (roughly 512 MB to 2 GB):

```bash
sudo dmesg | grep "VRAM memory ready"
```

The shared memory should match your `amd-ttm` value:

```bash
amd-ttm
sudo dmesg | grep "GTT memory ready"
```

## References

- AMD: Install ROCm on Radeon Ryzen (native Linux):
  <https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/native_linux/install-ryzen.html>
- AMD: Strix Halo system optimization:
  <https://rocm.docs.amd.com/en/docs-7.2.0/how-to/system-optimization/strixhalo.html>
- AMD: Linux compatibility matrices by ROCm version:
  <https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityryz/native_linux/native_linux_compatibility.html>
- AMD: llama.cpp pre-built binaries for Ryzen:
  <https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/advanced/advancedryz/linux/llm/llamacpp.html>
