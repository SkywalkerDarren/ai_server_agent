#!/usr/bin/env bash

TARGET_SERIAL="xxx"  # 目标序列号

# 函数：打印消息
echo_info() {
    echo "INFO: $1"
}

# 函数：打印错误消息并退出
echo_error() {
    echo "ERROR: $1" >&2
    exit 1
}

# 函数：查找并挂载分区
mount_partition() {
    disk_path="$1"
    first_partition=$(fdisk -l "$disk_path" 2>/dev/null | grep '^/' | awk '{print $1}' | head -n 1)

    if [ -z "$first_partition" ]; then
        echo_error "No partitions found on $disk_path"
    fi
    echo_info "First partition of $disk_path is: $first_partition"

    if [ ! -d /data ]; then
        echo_info "/data directory does not exist, creating it."
        mkdir /data
    else
        echo_info "/data directory exists."
    fi

    if mount | grep "on /data " > /dev/null; then
        echo_info "/data is already mounted."
    else
        echo_info "Attempting to mount $first_partition on /data."
        if mount "$first_partition" /data; then
            echo_info "/data mounted successfully."
        else
            echo_error "Failed to mount /data. Please check $first_partition and mount parameters."
        fi
    fi
}

# 主逻辑
for disk in $(lsblk -no NAME | grep -E '^vd[a-z]+$'); do
    serial=$(udevadm info --query=all --name=/dev/$disk | grep ID_SERIAL= | cut -d= -f2)
    if [ "$serial" == "$TARGET_SERIAL" ]; then
        echo_info "Found disk with serial $TARGET_SERIAL: /dev/$disk"
        mount_partition "/dev/$disk"
        exit 0
    fi
done

echo_error "Disk with serial $TARGET_SERIAL not found."
