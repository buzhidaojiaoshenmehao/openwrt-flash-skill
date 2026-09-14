# Contributing / 参与贡献

Contributions are welcome in Chinese or English. For a device workflow, include the exact model, hardware revision, region, current firmware, boot medium, official installation source and recovery prerequisites. Clearly distinguish a documentation review from a successful hardware test. Do not submit a universal flash command or firmware binaries.

欢迎补充设备流程和排障案例。请提供精确型号、硬件修订、地区、当前系统、启动介质、官方安装来源与恢复前提，并区分“文档核对”和“已实机测试”。不要提交通用强制刷写命令或固件文件。

Before submitting:

```sh
python3 -m unittest discover -s tests -v
sh -n skills/openwrt-flash/scripts/router_inventory.sh
```

Remove passwords, keys, serial numbers, MAC addresses, public/private IP addresses, subscription URLs, backups and identifying screenshots from issues and pull requests. Use synthetic reproductions. Preserve explicit write authorization, compatibility checks and recovery planning.
