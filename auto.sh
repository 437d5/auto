#!/bin/bash

FILE_URL="https://raw.githubusercontent.com/437d5/auto/main/clear.py"
MOUNT_POINT="/mnt/ssd"
TARGET_DIR="home/user/Desktop"

echo "Доступные диски:"
lsblk -lnpo NAME,MOUNTPOINT,SIZE,MODE | grep -E '^/dev/sd[b-z]'

read -p "Введите путь к диску: " DISK

if [ ! -b "$DISK" ]; then
    echo "Диск $DISK не найден!"
    exit 1
fi

sudo mount "$DISK" "$MOUNT_POINT"
if [ $? -ne 0 ]; then
    echo "Mount error"
    exit 1
fi

cd "$MOUNT_POINT/$TARGET_DIR"
if [ $? -eq 0 ]; then
    wget -q "$FILE_URL"
    echo "Running clear.py"
    python3 clear.py
    rm clear.py
else
    echo "$TARGET_DIR not found"
fi

cd /
sudo umount -l "$MOUNT_POINT"
echo "Disk $DISK is ready"