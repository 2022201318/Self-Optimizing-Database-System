import psutil
import subprocess
import time
import json
from statistics import mean, stdev


def monitor_system(script_path, output_file, interval=1):
    """
    监控运行脚本过程中的 CPU、内存、磁盘、网络使用情况，并生成 JSON 文件。

    :param script_path: 要执行的脚本路径
    :param output_file: 输出 JSON 文件路径
    :param interval: 采样间隔（秒）
    """
    cpu_data = []
    memory_data = []
    disk_read_bytes = []
    disk_write_bytes = []
    network_sent = []
    network_recv = []

    # 获取初始的网络和磁盘数据
    initial_net_io = psutil.net_io_counters()
    initial_disk_io = psutil.disk_io_counters()

    # 定义输出的中间文件路径
    time_output_file = "output.txt"

    # 使用 Shell 内置 `time` 命令运行脚本并重定向输出
    time_command = f"bash -c 'time {script_path}' > {time_output_file} 2>&1"
    process = subprocess.Popen(time_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        while process.poll() is None:
            # 采集 CPU 和内存使用情况
            cpu_data.append(psutil.cpu_percent(interval=None))
            memory_data.append(psutil.virtual_memory().percent)

            # 磁盘 I/O
            disk_io = psutil.disk_io_counters()
            disk_read_bytes.append(disk_io.read_bytes)
            disk_write_bytes.append(disk_io.write_bytes)

            # 网络 I/O
            net_io = psutil.net_io_counters()
            network_sent.append(net_io.bytes_sent)
            network_recv.append(net_io.bytes_recv)

            time.sleep(interval)

    except KeyboardInterrupt:
        process.terminate()
        print("脚本被用户中断。")
    finally:
        stdout, stderr = process.communicate()
        if stderr:
            print("脚本错误输出:")
            print(stderr)

    # 从时间输出文件中提取时间统计信息
    time_stats = {}
    with open(time_output_file, 'r') as f:
        for line in f:
            if "real" in line:
                time_stats["real"] = line.split()[1]
            elif "user" in line:
                time_stats["user"] = line.split()[1]
            elif "sys" in line:
                time_stats["sys"] = line.split()[1]

    # 计算磁盘和网络的统计数据
    total_read_bytes = disk_read_bytes[-1] - initial_disk_io.read_bytes if disk_read_bytes else 0
    total_write_bytes = disk_write_bytes[-1] - initial_disk_io.write_bytes if disk_write_bytes else 0
    total_bytes_sent = network_sent[-1] - initial_net_io.bytes_sent if network_sent else 0
    total_bytes_recv = network_recv[-1] - initial_net_io.bytes_recv if network_recv else 0

    # 处理数据
    result = {
        "cpu_percent": {
            "average": mean(cpu_data),
            "max": max(cpu_data),
            "min": min(cpu_data),
            "stdev": stdev(cpu_data) if len(cpu_data) > 1 else 0
        },
        "memory_percent": {
            "average": mean(memory_data),
            "max": max(memory_data),
            "min": min(memory_data),
            "stdev": stdev(memory_data) if len(memory_data) > 1 else 0
        },
        "disk_io": {
            "total_read_bytes": total_read_bytes,
            "total_write_bytes": total_write_bytes,
            "average_read_time": mean(disk_read_bytes) if disk_read_bytes else 0,
            "average_write_time": mean(disk_write_bytes) if disk_write_bytes else 0,
            "max_read_bytes": max(disk_read_bytes) - initial_disk_io.read_bytes if disk_read_bytes else 0,
            "max_write_bytes": max(disk_write_bytes) - initial_disk_io.write_bytes if disk_write_bytes else 0
        },
        "network_io": {
            "total_bytes_sent": total_bytes_sent,
            "total_bytes_recv": total_bytes_recv
        },
        "time_statistics": time_stats
    }

    # 将结果写入 JSON 文件
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=4)

    print(f"监控数据已保存到 {output_file}")


if __name__ == "__main__":
    # 设置脚本路径和输出 JSON 文件路径
    script_to_run = "./tpch_copy.sh"
    output_json = "system_metrics.json"

    monitor_system(script_to_run, output_json)
