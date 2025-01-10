
<div align="center">

# Self-Optimizing Database System

**A Tool for Automatic Parameter Optimization in PolarDB**

---

### [English](README.md) | [中文](README-CN.md)

[![github-license](https://img.shields.io/github/license/2022201318/Self-Optimizing-Database-System?style=for-the-badge&logo=github)](LICENSE)
[![github-issues](https://img.shields.io/github/issues/2022201318/Self-Optimizing-Database-System?style=for-the-badge&logo=github)](https://github.com/2022201318/Self-Optimizing-Database-System/issues)
[![github-stars](https://img.shields.io/github/stars/2022201318/Self-Optimizing-Database-System?style=for-the-badge&logo=github)](https://github.com/p2022201318/Self-Optimizing-Database-System/stargazers)

</div>

---

## What is the Self-Optimizing Database System?

The Self-Optimizing Database System is a tool based on **PolarDB for PostgreSQL**, designed to dynamically adjust database configuration parameters for performance optimization and monitor system resource usage during runtime. By iteratively improving the database, it is well-suited for high-performance needs in large-scale data environments.

---

## System Features

1. **Dynamic Database Parameter Adjustment**:
   - Automatically recommend parameter adjustments to improve database performance.
   - Supports multi-round iterative optimization, saving results for analysis.

2. **Performance Monitoring**:
   - Real-time monitoring of CPU, memory, disk, and network usage.
   - Records and saves system performance data during runtime.

3. **Result Storage**:
   - Saves optimization results into separate folders for each iteration, including database configurations, system performance data, and model feedback.

---

## Experiment Preparation

### 1. Tool Preparation

- A virtual machine or server with **8-core CPU**, **16 GB memory**, running **Ubuntu OS**, and at least **100 GB disk space**.
- Install and configure Docker, Git, and other common tools. Steps are omitted here.

### 2. Download Database Development Image, Start Container , Enter Container and pull the code

```bash
docker pull registry.cn-hangzhou.aliyuncs.com/polardb_pg/polardb_pg_devel:ubuntu20.04
docker run -d -it -P --shm-size=1g --cap-add=SYS_PTRACE --cap-add SYS_ADMIN --privileged=true --name my_new registry.cn-hangzhou.aliyuncs.com/polardb_pg/polardb_pg_devel:ubuntu20.04 bash
docker exec -ti my_new bash
cd polardb_pg
git clone https://github.com/2022201318/Self-Optimizing-Database-System
mv Self-Optimizing-Database-System PolarDB-for-PostgreSQL
```

### 3. Environment and Dependency Preparation

After moving the submitted code into the container, execute the following commands to configure the environment:

```bash
sudo apt update
sudo apt install python3
sudo apt install python3-pip
pip install psutil
pip install zhipuai
```

### 4. Data Preparation (Adjust the dataset size as needed)

```bash
cd ~/polardb_pg/PolarDB-for-PostgreSQL/tpch-dbgen
make -f makefile.suite
./dbgen -f -s 2
sudo mkdir /data
sudo chown -R postgres:postgres /data
sudo mv *.tbl /data/
```

---

## Running the Self-Optimizing System

### 1. Initialize the PolarDB Cluster

```bash
chmod 700 polardb_build.sh
./polardb_build.sh --without-fbl --debug=off
```

### 2. Run the System

```bash
cd ~/polardb_pg/PolarDB-for-PostgreSQL
chmod 700 auto.sh
./auto.sh
```

### 3. View Results

The results of the nth iteration of tuning are automatically saved in the `memory/backup_n` folder:

- `pg_settings_vi.json`: Database configuration for the ith iteration.
- `system_metrics_vi.json`: System performance data for the ith iteration.
- `optimized_pg_settings_vi.txt`: Feedback from the large model for the ith iteration.

### 4. Re-run the System

```bash
./tpch_copy.sh --clean
rm -rf backup*
./auto.sh
```

If you have any questions or suggestions, please contact: zhangbofei@ruc.edu.cn.

---

## File Structure

```plaintext
project/
├── auto.sh                      # Main script for the self-optimizing system
├── bigmodel.py                  # Interaction script with the large model
├── config/                      # Configuration files directory
├── memory/                      # Directory to store results of each iteration
│   ├── backup_1/                # Results of the first iteration
│   │   ├── pg_settings_v1.json  # Database configuration
│   │   ├── system_metrics_v1.json # System performance data
│   │   └── optimized_pg_settings_v1.txt # Recommended parameters
│   ├── backup_2/                # Results of the second iteration
│   │   ├── pg_settings_v2.json
│   │   ├── system_metrics_v2.json
│   │   └── optimized_pg_settings_v2.txt
├── polardb_build.sh             # Script to initialize the PolarDB cluster
├── settings_tocommand.py        # Script to convert optimized results into database commands
├── metrics_parser.py            # Script to parse system performance data
├── tpch_copy.sh                 # Data loading script
├── tpch-dbgen/                  # TPCH test data generation tool
├── README-CN.md                 # Project documentation in Chinese
├── README-CN.md                 # Project documentation in English
├── LICENSE                      # Open-source license
├── system_metrics.json          # System performance data
├── pg_settings.json             # Database configuration data
├── pg_settings_commands.sh      # Generated database configuration commands
```

---

## Notes

1. **System Requirements**: Ensure the server or VM running the project meets the following minimum requirements:
   - 8-core CPU
   - 16 GB memory
   - 100 GB disk space at least

2. **Container Permissions**: Privileged mode (`--privileged=true`) is required when starting the Docker container.

3. **Dependencies**: Ensure the following tools are installed:
   - Docker
   - Git
   - Python3
   - `psutil` and `zhipuai` (install via pip)

---

## Contribution and Support

We welcome suggestions and contributions to improve the self-optimizing database system. If you encounter any issues, feel free to submit an issue on GitHub.

---

## License

This project is based on **PolarDB for PostgreSQL 11**, modified from the repository provided by Digoal on GitHub. For more information, visit:  
[PolarDB-for-PostgreSQL on Gitee](https://gitee.com/digoal/PolarDB-for-PostgreSQL).

Special thanks to Professor Bian Haoqiong and Professor Zhang Jing from Renmin University of China and expert Digoal from Alibaba Cloud for their support and guidance.

This project is open-sourced under the Apache 2.0 License. See LICENSE for details.

