#!/usr/bin/env bash

# 设置要查找的磁盘标识符
disk_identifier="0x06254a8b"

# 查找具有指定磁盘标识符的硬盘
matching_disks=$(sudo fdisk -l 2>/dev/null | grep -B 10 "Disk identifier: $disk_identifier" | grep '^Disk /dev' | awk '{print $2}' | sed 's/://')

# 检查是否找到了匹配的硬盘
if [ -z "$matching_disks" ]; then
    echo "没有找到具有磁盘标识符 $disk_identifier 的硬盘。"
    exit 1
fi

echo "找到以下具有磁盘标识符 $disk_identifier 的硬盘："
echo "$matching_disks"

# 遍历所有匹配的硬盘
for disk in $matching_disks; do
    # 输出第一个分区
    first_partition=$(sudo fdisk -l $disk 2>/dev/null | grep '^/' | awk '{print $1}' | head -n 1)

    if [ -z "$first_partition" ]; then
        echo "在硬盘 $disk 上未找到分区。"
    else
        echo "硬盘 $disk 的第一个分区是 $first_partition"
    fi
done

if [ -d /data ]; then
    echo "/data 目录存在。"
else
    echo "/data 目录不存在，创建目录。"
    sudo mkdir /data
fi

if mount | grep "on /data " > /dev/null; then
    echo "/data 已经挂载。"
else
    echo "/data 未挂载，尝试挂载 /dev/vdb1 到 /data。"
    sudo mount "$first_partition" /data

    if mount | grep "on /data " > /dev/null; then
        echo "/data 挂载成功。"
    else
        echo "/data 挂载失败，请检查 /dev/vdb1 或者其他挂载参数。"
    fi
fi