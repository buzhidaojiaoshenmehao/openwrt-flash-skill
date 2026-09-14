# OpenWrt Flash Skill | 软路由刷机、升级与恢复

[中文](#中文说明) | [English](#english) | [Contributing](CONTRIBUTING.md) | [MIT License](LICENSE)

Hardware-aware OpenWrt flashing, firmware verification, sysupgrade and recovery workflows for Codex AI agents. Covers SD/TF boards (NanoPi, Raspberry Pi), x86 soft routers and supported embedded routers, with backup and disk-safety checks.

## 中文说明

面向 Codex 的 OpenWrt 安装、升级与恢复 skill。根据设备证据选择流程，支持中文交互。

适配的是**刷机流程类别**，不代表列表中的任意型号都支持 OpenWrt：

| 设备类别 | 处理方式 |
| --- | --- |
| NanoPi / Raspberry Pi 等 SD、TF 卡启动设备 | 精确板型匹配、离线整盘镜像、写入后读回验证 |
| x86 / x86_64 软路由、工控机 | UEFI / BIOS、网卡驱动、磁盘与文件系统匹配 |
| 小米 / Redmi、GL.iNet、TP-Link、Linksys、Netgear、ASUS 等内置闪存设备 | 先查精确型号、地区和硬件修订版的官方安装方法；不提供通用 MTD 刷写命令 |
| 已运行 OpenWrt 的设备 | 备份、兼容性检查、sysupgrade 或适配的 Attended Sysupgrade |
| 虚拟机 | 平台官方支持的镜像导入、虚拟网卡和启动方式核对 |
| eMMC / NAND / NOR、双固件分区设备 | 仅按设备文档执行，区分启动介质、校准区和恢复流程 |

## 安装

将本仓库中的 `skills/openwrt-flash` 文件夹放到 `~/.codex/skills/openwrt-flash`。重新打开 Codex 对话后可显式使用：

```text
使用 $openwrt-flash 帮我给 NanoPi R2S 刷官方稳定版，先识别 TF 卡并核对固件。
使用 $openwrt-flash 检查我的小米路由器是否支持 OpenWrt，尚未确认型号。
使用 $openwrt-flash 升级现有 OpenWrt，先评估是否能保留配置。
```

skill 本身不会自动刷写。实际工作由 Codex 按现场证据和已授权范围完成；清空介质需要明确关联到当前设备的授权，旧对话的磁盘编号不能复用。

## 包含内容

- `SKILL.md`：设备识别、固件匹配、备份、执行和验收流程。
- `references/`：可移除介质、内置闪存与升级、联网排障、官方入口。
- `scripts/router_inventory.sh`：在已授权登录的 OpenWrt shell 中输出有限只读诊断，不打印 UCI、订阅、密码或 MAC。
- `scripts/verify_firmware.py`：校验普通文件的 SHA-256 和 gzip 完整性，计算解压后大小；拒绝符号链接和设备文件，不下载、不刷写。
- `tests/`：合成文件校验测试和人工场景验收标准。

脚本使用 Python 3.9+ 标准库或 POSIX shell，不依赖 SSH 密钥、浏览器插件或特定操作系统的 Python 第三方库。

## 验证

```sh
python3 -m unittest discover -s tests -v
sh -n skills/openwrt-flash/scripts/router_inventory.sh
```

已做离线脚本测试和流程审阅；没有对设备矩阵进行逐台实机认证。固件和安装资料必须在每次实际任务时重新核实。

仓库不包含固件、路由器备份、订阅地址、凭据、MAC、序列号或个人设备配置。

## English

**OpenWrt Flash Skill** is a reusable Codex skill for installing OpenWrt, upgrading existing installations and investigating post-flash networking problems. It is a hardware-aware workflow, not an unattended flasher or a firmware distribution.

### Device workflows

- **NanoPi R2S and other SD/TF boards:** identify the exact board, select its official image, verify checksums and read back written data.
- **Raspberry Pi:** match the exact generation, supported image and boot medium.
- **x86 / x86_64 soft routers and mini PCs:** check UEFI/BIOS, NIC support, disk identity and filesystem layout.
- **Supported embedded routers:** Xiaomi/Redmi, GL.iNet, TP-Link, Linksys, Netgear and ASUS are discovery categories, not blanket compatibility claims. Every model, hardware revision and regional variant needs an official installation procedure.
- **Existing OpenWrt installations:** backups, sysupgrade compatibility checks, configuration-retention decisions and recovery planning.
- **Virtual machines, eMMC, NAND/NOR and dual-slot devices:** follow the matching platform/device procedure; no universal raw flash commands.

### Install in Codex

Clone this repository and place `skills/openwrt-flash` inside your Codex skills directory (normally `~/.codex/skills/`). Do not overwrite an existing customized skill without reviewing it.

```sh
git clone https://github.com/buzhidaojiaoshenmehao/openwrt-flash-skill.git
```

Start a new conversation after installation and invoke it explicitly:

```text
Use $openwrt-flash to install official stable OpenWrt on my NanoPi R2S.
Identify the TF card and verify the exact firmware before any destructive step.

Use $openwrt-flash to check whether my router model supports OpenWrt.

Use $openwrt-flash to plan and perform a backed-up sysupgrade.
```

The core instructions currently use Chinese; ask the agent to explain its work in your preferred language. Other agents may adapt the Markdown instructions, but their skill loading and execution permissions are not tested here.

### Safety and testing

The included Python 3.9+ checksum tool and POSIX shell inventory tool are read-only. The skill requires exact hardware identification, trusted firmware sources, backups, explicit destructive-write authorization and post-install checks. It never treats checksum success as proof of device compatibility.

Run the tests from the repository root using the commands in the verification section above. Tests use synthetic files; supported workflow categories have **not** been individually certified on real hardware. Check current official support and installation documentation for every actual device. No firmware binaries, private configurations or credentials are included.

### Official starting points

[OpenWrt Firmware Selector](https://firmware-selector.openwrt.org/) · [Table of Hardware](https://openwrt.org/toh/start) · [Sysupgrade documentation](https://openwrt.org/docs/guide-user/installation/generic.sysupgrade)

This is an independent community skill, not an official OpenWrt or OpenAI project. GitHub discoverability is helped by descriptive documentation and accurate repository topics; search placement is not guaranteed.
