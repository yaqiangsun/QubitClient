import os
import shutil

# 原始路径
source_root = "data"
# 目标路径
target_dir = os.path.join("tmp", "convert")

# 如果目标路径不存在，创建它
os.makedirs(target_dir, exist_ok=True)

# 遍历 data 目录下的所有文件夹
for folder_name in os.listdir(source_root):
    folder_path = os.path.join(source_root, folder_name)

    # 跳过 convert 文件夹或非文件夹项
    if folder_name == "convert" or not os.path.isdir(folder_path):
        continue

    # 遍历该文件夹中的所有 .npz 文件（你也可以限制只处理 Q 开头的）
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".npz") and file_name.startswith("Q"):
            src_file_path = os.path.join(folder_path, file_name)
            new_file_name = f"{folder_name}_{file_name}"
            dst_file_path = os.path.join(target_dir, new_file_name)

            shutil.copy2(src_file_path, dst_file_path)
            print(f"已复制: {src_file_path} -> {dst_file_path}")
