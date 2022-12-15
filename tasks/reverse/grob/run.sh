#!/bin/bash
/chal/hashcashed -c 28 timeout 45 qemu-system-i386 -monitor /dev/null -m 64M -nographic -drive  file=/chal/boot_prod.img,if=virtio,readonly=on,format=raw
