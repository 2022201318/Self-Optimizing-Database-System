#!/bin/bash

n=10 #每个epoch迭代次数
for i in $(seq 1 $n); do
    echo "开始第 $i 次循环..."

    # 定义文件夹路径
    BACKUP_DIR="memory/backup_$i"
    
    # 创建备份文件夹
    mkdir -p $BACKUP_DIR

    # 执行任务命令
    echo "执行 psql 命令导出设置"
    psql -c "\copy (SELECT name, setting, unit, short_desc, reset_val FROM pg_settings) TO '/home/postgres/polardb_pg/PolarDB-for-PostgreSQL/pg_settings.csv' WITH CSV HEADER"

    echo "执行 settings_tojson.py"
    python3 settings_tojson.py

    echo "执行 monitor_running.py"
    python3 monitor_running.py

    echo "执行 bigmodel.py"
    python3 bigmodel.py

    echo "执行 settings_tocommand.py"
    python3 settings_tocommand.py

    echo "为 pg_settings_commands.sh 设置执行权限"
    chmod 700 pg_settings_commands.sh

    echo "执行 pg_settings_commands.sh"
    ./pg_settings_commands.sh

    echo "执行 tpch_copy.sh --clean"
    ./tpch_copy.sh --clean

    echo "第 $i 次循环完成"
    echo "-------------------------------"

        # 移动并重命名文件，避免覆盖
    if [ -f pg_settings.json ]; then
        mv pg_settings.json "$BACKUP_DIR/pg_settings_v$i.json"
        echo "文件 pg_settings.json 已移动并重命名为 pg_settings_v$i.json"
    fi

    if [ -f system_metrics.json ]; then
        mv system_metrics.json "$BACKUP_DIR/system_metrics_v$i.json"
        echo "文件 system_metrics.json 已移动并重命名为 system_metrics_v$i.json"
    fi

    if [ -f optimized_pg_settings.txt ]; then
        mv optimized_pg_settings.txt "$BACKUP_DIR/optimized_pg_settings_v$i.txt"
        echo "文件 optimized_pg_settings.txt 已移动并重命名为 optimized_pg_settings_v$i.txt"
    fi
done
