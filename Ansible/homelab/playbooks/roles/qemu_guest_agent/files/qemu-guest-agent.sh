#!/bin/sh

case "${1:-start}" in
    start)
        /usr/sbin/service qemu-guest-agent onestatus >/dev/null 2>&1 ||
            /usr/sbin/service qemu-guest-agent onestart
        ;;
    stop)
        if /usr/sbin/service qemu-guest-agent onestatus >/dev/null 2>&1; then
            /usr/sbin/service qemu-guest-agent onestop
        fi
        ;;
    restart)
        /usr/sbin/service qemu-guest-agent onerestart
        ;;
    *)
        exit 0
        ;;
esac