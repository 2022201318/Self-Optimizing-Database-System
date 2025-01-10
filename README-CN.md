
<div align="center">

# 自优化数据库系统

**基于 PolarDB 的数据库参数自优化工具**

---

### [English](README.md) | 中文

[![github-license](https://img.shields.io/github/license/polardbpg/polardb-self-optimizer?style=for-the-badge&logo=github)](LICENSE)
[![github-issues](https://img.shields.io/github/issues/polardbpg/polardb-self-optimizer?style=for-the-badge&logo=github)](https://github.com/polardbpg/polardb-self-optimizer/issues)
[![github-stars](https://img.shields.io/github/stars/polardbpg/polardb-self-optimizer?style=for-the-badge&logo=github)](https://github.com/polardbpg/polardb-self-optimizer/stargazers)

</div>

---

## 什么是自优化数据库系统？

自优化数据库系统是一种基于 PolarDB for PostgreSQL 的工具，用于动态调整数据库配置参数以优化性能，并监控运行时的系统资源消耗。该工具通过迭代过程提升数据库的整体性能，适用于需要高效运行的大型数据环境。

---

## 系统功能

1. **数据库参数动态调整**：
   - 自动推荐参数调整，提升数据库性能。
   - 支持多轮迭代优化，保存每轮结果以供分析。

2. **性能数据监控**：
   - 实时监控 CPU、内存、磁盘、网络等系统资源。
   - 记录并保存系统运行时的性能数据。

3. **结果保存**：
   - 每轮优化结果保存到独立文件夹中，包括数据库配置、系统性能数据和大模型反馈。

---

## 实验准备

### 1. 工具准备

- 一台 8 核 16GB 内存的虚拟机或服务器，使用 Ubuntu 操作系统，磁盘容量不少于 100GB。
- 安装并配置 Docker、Git 等常用工具，具体步骤省略。

### 2. 下载数据库开发镜像, 启动容器, 进入容器

```bash
docker pull registry.cn-hangzhou.aliyuncs.com/polardb_pg/polardb_pg_devel:ubuntu20.04
docker run -d -it -P --shm-size=1g --cap-add=SYS_PTRACE --cap-add SYS_ADMIN --privileged=true --name my_new registry.cn-hangzhou.aliyuncs.com/polardb_pg/polardb_pg_devel:ubuntu20.04 bash
docker exec -ti my_new bash
```

### 3. 环境及安装包准备

在将我的提交代码移动到容器中后，执行如下命令配置环境：

```bash
sudo apt update
sudo apt install python3
sudo apt install python3-pip
pip install psutil
pip install zhipuai
```

### 4. 数据准备（可根据需要调整生成数据大小）

```bash
cd ~/polardb_pg/PolarDB-for-PostgreSQL/tpch-dbgen
make -f makefile.suite
./dbgen -f -s 2
sudo mkdir /data
sudo chown -R postgres:postgres /data
sudo mv *.tbl /data/
```

---

## 运行自优化系统

### 1. 初始化 PolarDB 集群

```bash
chmod 700 polardb_build.sh
./polardb_build.sh --without-fbl --debug=off
```

### 2. 运行系统

```bash
cd ~/polardb_pg/PolarDB-for-PostgreSQL
chmod 700 auto.sh
./auto.sh
```

### 3. 结果查看

调优后的第 n 次迭代生成信息自动保存于 `memory/backup_n` 文件夹中：

- `pg_settings_vi.json`：保存为第 i 次的数据库参数。
- `system_metrics_vi.json`：保存为第 i 次的运行时的系统参数。
- `optimized_pg_settings_vi.txt`：保存第 i 次的大模型回复信息。

### 4. 重新运行

```bash
./tpch_copy.sh --clean
rm -rf backup*
./auto.sh
```

如有疑问或指点可联系：zhangbofei@ruc.edu.cn

---

## 文件结构

```plaintext
project/
├── auto.sh                      # 自优化系统的主脚本
├── bigmodel.py                  # 基于大模型的交互脚本
├── config/                      # 配置文件目录
├── memory/                      # 保存每轮优化结果的目录
│   ├── backup_1/                # 第 1 轮优化结果
│   │   ├── pg_settings_v1.json  # 数据库参数配置
│   │   ├── system_metrics_v1.json # 系统性能数据
│   │   └── optimized_pg_settings_v1.txt # 大模型推荐参数
│   ├── backup_2/                # 第 2 轮优化结果
│   │   ├── pg_settings_v2.json
│   │   ├── system_metrics_v2.json
│   │   └── optimized_pg_settings_v2.txt
├── polardb_build.sh             # 初始化 PolarDB 集群的脚本
├── settings_tocommand.py        # 将优化结果转化为数据库命令的脚本
├── metrics_parser.py            # 解析系统性能数据的脚本
├── tpch_copy.sh                 # 数据加载脚本
├── tpch-dbgen/                  # TPCH 测试数据生成工具
├── README-CN.md                 # 项目中文说明文档
├── README.md                    # 项目英文说明文档
├── LICENSE                      # 开源协议
├── system_metrics.json          # 系统性能数据
├── pg_settings.json             # 数据库配置数据
├── pg_settings_commands.sh      # 生成的数据库配置命令脚本
```

---

## 注意事项

1. **系统资源**：确保运行该项目的服务器或虚拟机满足以下最低要求：
   - 8 核 CPU
   - 16 GB 内存
   - 至少 100 GB 磁盘空间

2. **权限设置**：在docker中运行时需保证各文件权限。

3. **依赖工具**：确认已安装以下工具：
   - Docker
   - Git
   - Python3
   - psutil 和 zhipuai（通过 pip 安装）

---

## 贡献与支持

我们欢迎您对自优化数据库系统的改进提出建议或贡献代码。如果您遇到问题，可以通过 GitHub 提交 issue。

---

## License

该项目基于 PolarDB for PostgreSQL 11，由德哥（Digoal）在 GitHub 上提供的仓库进行改动。更多信息请访问：  
[PolarDB-for-PostgreSQL on Gitee](https://gitee.com/digoal/PolarDB-for-PostgreSQL)。

特别感谢中国人民大学卞老师、张老师，阿里云专家德哥的支持与指导。

该项目遵循 Apache 2.0 协议开源。有关更多信息，请参阅 LICENSE。