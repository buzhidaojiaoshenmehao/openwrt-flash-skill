# 官方入口与执行记录

以下是查证入口，不是预先认证的型号清单。每次实际刷机应保存访问日期与相关设备专用页面，并重新核实目标固件；页面和下载索引可能不同时更新。

- [Table of Hardware](https://openwrt.org/toh/start)：精确机型、硬件修订和安装/恢复限制。
- [Firmware Selector](https://firmware-selector.openwrt.org/)：查 profile 和可用镜像。
- [官方稳定版下载目录](https://downloads.openwrt.org/releases/)：发布版本、target/subtarget、镜像和校验文件。
- [sysupgrade 说明](https://openwrt.org/docs/guide-user/installation/generic.sysupgrade)：已有 OpenWrt 升级与镜像检查；x86 的镜像命名是通用后缀规则的例外。
- [x86 安装](https://openwrt.org/docs/guide-user/installation/openwrt_x86)：磁盘和引导模式。
- [校验与签名](https://openwrt.org/docs/guide-user/security/signatures)：按实际发布版本核实签名与信任来源。
- [升级方式比较](https://openwrt.org/docs/guide-user/upgrading/comparing_upgrade_options)：常规升级、定制镜像与 Attended Sysupgrade 的选择。
- [OpenWrt 官方源码](https://github.com/openwrt/openwrt)：核对相应 release tag 下设备 image recipe；源码 profile 存在不等于安装流程已验证。

遇到反机器人页面时不要绕过限制或把拦截页当文档。可以使用用户提供的对应设备文档、可访问的官方发布说明和精确 release 源码补充证据；缺失关键步骤时停止实际刷写。

执行时在私有工作目录记录以下字段，供写入摘要和最终交接使用，不提交到公开仓库：

```text
设备完整型号 / 硬件修订 / 地区 / 当前固件:
板型证据及读取时间:
安装方式 / 官方设备专用页面 / 访问日期:
目标版本 / target / subtarget / profile:
镜像用途 / 引导方式 / 文件系统:
镜像 URL / SHA-256 / 清单来源与签名结果:
目标介质型号、容量、当前设备路径和排除系统盘的证据:
解压后字节数 / 介质容量:
备份位置、验证结果、回滚材料:
保留或重置配置的理由 / 用户授权范围:
写入与读回结果 / 重启后的板型和版本:
LAN/WAN/DNS/客户端测试及执行位置:
未验证项 / 临时权限清理结果:
```
