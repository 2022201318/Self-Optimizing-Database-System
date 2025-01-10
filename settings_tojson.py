import csv
import json
import os

def csv_to_json(csv_file_path):
    """
    将指定路径的CSV文件转换为JSON文件，并保存在相同目录下。

    :param csv_file_path: 输入的CSV文件路径
    """
    # 获取CSV文件所在的目录和文件名
    directory, filename = os.path.split(csv_file_path)
    # 构建JSON文件的路径，文件名与CSV相同但扩展名为.json
    json_file_name = os.path.splitext(filename)[0] + '.json'
    json_file_path = os.path.join(directory, json_file_name)

    data = []

    try:
        # 读取CSV文件
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            # 遍历CSV中的每一行，将指定字段提取出来
            for row in csv_reader:
                entry = {
                    "name": row.get("name", ""),
                    "setting": row.get("setting", ""),
                    "unit": row.get("unit", ""),
                    "short_desc": row.get("short_desc", ""),
                    "reset_val": row.get("reset_val", "")
                }
                data.append(entry)
        
        # 将数据写入JSON文件
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        
        print(f"成功将 '{csv_file_path}' 转换为 '{json_file_path}'。")
    
    except FileNotFoundError:
        print(f"错误：文件 '{csv_file_path}' 未找到。请检查路径是否正确。")
    except Exception as e:
        print(f"转换过程中发生错误：{e}")

if __name__ == "__main__":
    # 定义CSV文件的路径
    csv_path = "/home/postgres/polardb_pg/PolarDB-for-PostgreSQL/pg_settings.csv"
    
    # 检查CSV文件是否存在
    if os.path.isfile(csv_path):
        csv_to_json(csv_path)
    else:
        print(f"错误：CSV文件 '{csv_path}' 不存在。请确保文件路径正确。")