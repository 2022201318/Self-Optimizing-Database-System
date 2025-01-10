import json


def extract_json_from_text(file_path):
    """
    从文本中提取 JSON 格式的内容
    :param file_path: 包含大模型输出的文件路径
    :return: 提取出的 JSON 数据
    """
    with open(file_path, 'r') as f:
        content = f.read()

    # 手动匹配大括号以提取 JSON
    stack = []
    json_start = -1
    json_end = -1

    for i, char in enumerate(content):
        if char == '{':
            if not stack:
                json_start = i
            stack.append(char)
        elif char == '}':
            stack.pop()
            if not stack:
                json_end = i
                break  # 找到第一个完整的 JSON

    if json_start != -1 and json_end != -1:
        json_str = content[json_start:json_end + 1]
        try:
            # 加载 JSON 数据
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError as e:
            print(f"JSON 解码错误: {e}")
            return None
    else:
        print("未找到 JSON 数据！")
        return None


def generate_pg_config_commands(json_data, output_file):
    """
    将 JSON 数据转换为 PostgreSQL 配置命令
    :param json_data: 提取的 JSON 数据
    :param output_file: 输出的 shell 命令文件路径
    """
    if not json_data:
        print("无有效 JSON 数据，无法生成配置命令。")
        return

    config_commands = []
    config_commands.append('echo "')

    for key, value in json_data.items():
        suggested_setting = value.get("suggested_setting")
        if suggested_setting:
            # 将字符串型参数加引号，数字型参数不加引号
            if isinstance(suggested_setting, str) and not suggested_setting.replace(".", "").isdigit():
                config_commands.append(f"{key} = '{suggested_setting}'")
            else:
                config_commands.append(f"{key} = {suggested_setting}")

    config_commands.append('" >> ~/tmp_master_dir_polardb_pg_1100_bld/postgresql.conf')

    # 添加 PostgreSQL 配置重新加载或重启命令
    config_commands.append('\n# Reload PostgreSQL configuration')
    config_commands.append('pg_ctl reload -D ~/tmp_master_dir_polardb_pg_1100_bld')  # 请替换数据目录路径
    config_commands.append('# 或者使用以下命令来重启 PostgreSQL')
    config_commands.append('pg_ctl restart -m fast -D ~/tmp_master_dir_polardb_pg_1100_bld')  # 请替换数据目录路径

    # 保存到 shell 脚本中
    with open(output_file, "w") as f:
        f.write("\n".join(config_commands))
    
    print(f"PostgreSQL 配置命令已保存到 {output_file}")


if __name__ == "__main__":
    input_file = "optimized_pg_settings.txt"  # 大模型输出文件
    output_file = "pg_settings_commands.sh"  # 输出的 PostgreSQL 配置命令文件

    # 提取 JSON 数据
    json_data = extract_json_from_text(input_file)

    # 生成 PostgreSQL 配置命令
    generate_pg_config_commands(json_data, output_file)


