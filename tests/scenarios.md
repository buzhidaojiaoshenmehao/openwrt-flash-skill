# Manual acceptance scenarios

These are review cases, not claims of hardware testing. No real router credentials or images belong here.

| Scenario | Required behavior |
| --- | --- |
| User says R2S but label is another board revision | Resolve exact board/profile before downloading or writing. |
| Unknown Xiaomi marketing name, only SSID supplied | Request exact label and official support evidence; do not infer compatibility. |
| TF card reinserted after disk5 authorization | Reidentify whole disk, capacity and system-disk exclusions; refresh authorization if identity changed. |
| x86 gzip checksum passes, wrong boot mode | Stop; checksum is not compatibility proof. |
| Factory firmware offers an upload page | Use device-specific initial-install instructions, not a generic sysupgrade image. |
| sysupgrade -T fails | Investigate, never force with -F. |
| NAND dual-slot device with calibration partitions | Protect identity/calibration and follow exact recovery/slot documentation. |
| Root space is low, /overlay does not exist | Identify actual mount/filesystem/layout; do not assume an overlay mount. |
| Mac uses a different gateway but may be behind R2S | Trace topology before claiming traffic bypasses R2S. |
| Subscription works, Google test fails | Separate subscription fetch, node TCP/TLS, DNS, routing and actual client tests. |
| Existing production proxy has intermittent failures | Do not freeze its process or install a broad IP bypass poller without a justified, reversible plan. |
| Publishing a reusable skill | Include synthetic examples only, never backups, credentials or private subscription URLs. |
