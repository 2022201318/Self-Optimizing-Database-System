import json
from zhipuai import ZhipuAI

# 初始化 ZhipuAI 客户端
client = ZhipuAI(api_key="ae569c6c31ac4c5c9aa03619d0013a89.ZbCV0v4L6OUpOwOc")

# 定义两个 JSON 文件路径
pg_settings_file = "pg_settings.json"  # 数据库配置文件路径
monitor_statistics_file = "system_metrics.json"  # 监控数据文件路径

# 读取 JSON 文件
def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# 加载数据
pg_settings = load_json(pg_settings_file)
monitor_statistics = load_json(monitor_statistics_file)

# 构造交互任务描述
task_description = f"""
你至少要给我返回10个更改的参数，不能是改前和改后都相同的。我需要更多的更改参数，同时，我希望你能够通过计算我给你的monitor_running.json的变化来优化参数。
我给你的pg_settings里面有几百个参数呢，我正在优化一个数据库导入数据的速度，
导入的是2G tpch 数据，需要你帮我优化参数，我的运行设备有着8核16GB内存，100G磁盘。
我的目的是极尽所能加快导入速度，其他的一概不管。
以下是相关的配置参数和模型运行时间信息：
1. PostgreSQL 配置 ({pg_settings_file}):
{json.dumps(pg_settings, indent=4)}

2. 数据库导入运行时间和其他信息 ({monitor_statistics_file}):
{json.dumps(monitor_statistics, indent=4)}

请根据这些信息，返回一个 JSON 格式的响应，包括需要更改的参数。

返回的 JSON 格式应为：
{{
    "参数名1": {{
        "suggested_setting": "新值",
        "current_value": "当前值"
    }},
    "参数名2": {{
        "suggested_setting": "新值",
        "current_value": "当前值"
    }},
    ...
}}

例如：
{{
    "shared_buffers": {{
        "suggested_setting": "256MB",
        "current_value": "128MB"
    }},
    "work_mem": {{
        "suggested_setting": "64MB",
        "current_value": "4MB"
    }},
    "maintenance_work_mem": {{
        "suggested_setting": "1GB",
        "current_value": "8MB"
    }}
}}

注意：
1. 返回的 JSON 必须干净整洁，不能包含注释或额外的无关内容。
2. short_desc 是描述，你可以根据这个调参数。
3、shared_buffers 的实际大小需要注意乘单位，例如1048576就是8GB，因为单位是8kB，
4、shared_buffers 实际大小不能大于 1GB，注意要乘单位
5、wal_size等内存相关的都是如此
"""

# 调用大模型 API
response = client.chat.completions.create(
    model="glm-4-plus",  # 使用 glm-4-plus 模型
    messages=[
        {
            "role": "user",
            "content": task_description,
        }
    ],
)

# 输出大模型的回复
response_text = response.choices[0].message.content

# 保存优化后的结果到 JSON 文件
optimized_settings_file = "optimized_pg_settings.txt"
with open(optimized_settings_file, "w") as f:
    f.write(response_text)

print(f"优化后的 PostgreSQL 配置已保存到 {optimized_settings_file}")