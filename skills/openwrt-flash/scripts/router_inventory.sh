#!/bin/sh
# Limited, read-only inventory. Review output before sharing it publicly.
set -u
if [ ! -r /etc/openwrt_release ]; then
    printf '%s\n' 'Not an identified OpenWrt environment; inventory stopped.' >&2
    exit 1
fi
printf '%s\n' '== Kernel =='
uname -sr
printf '%s\n' '== Board (allowlisted fields only) =='
if command -v ubus >/dev/null 2>&1 && command -v jsonfilter >/dev/null 2>&1; then
    board=$(ubus call system board 2>/dev/null) || board='{}'
    for field in model board_name; do
        printf '%s: ' "$field"
        printf '%s' "$board" | jsonfilter -e "@.$field"
    done
    for field in distribution version revision target; do
        printf '%s: ' "$field"
        printf '%s' "$board" | jsonfilter -e "@.release.$field"
    done
else
    printf '%s\n' 'Board information unavailable (ubus/jsonfilter missing).'
fi
printf '%s\n' '== Root filesystem =='
df -k /
printf '%s\n' '== Memory =='
if command -v free >/dev/null 2>&1; then free; fi
printf '%s\n' '== Available tools (presence is not service health) =='
for tool in apk opkg sysupgrade block lsblk findmnt dnsmasq nft iptables curl wget; do
    if command -v "$tool" >/dev/null 2>&1; then printf '%s\n' "$tool"; fi
done
printf '%s\n' 'No credentials, network configuration, or service changes were requested.'
