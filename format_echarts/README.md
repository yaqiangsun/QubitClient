# Quantum Data Transformation Tool

# 项目概述‌ 
这是一个量子数据及其处理结果格式转换可视化工具包。下面以s21vflux为例介绍。

# 代码架构‌

1. main()函数

    ```python
        def main():
        from config import API_URL, API_KEY
        base_dir = "./tmp/s21_peak"
        file_names = os.listdir(base_dir)
        file_path_list = []
        for file_name in file_names:
            if file_name.endswith('.npy'):
                file_path = os.path.join(base_dir, file_name)
                file_path_list.append(file_path)
        if len(file_path_list) == 0:
            return
        dict_list = []
        for file_path in file_path_list:
            content = load_npy_file(file_path)
            dict_list.append(content)
        trans_all_npy = transform_s21peak_npy_and_processed_data(API_URL, API_KEY, dict_list)  # trans_all_npy的数据格式参考format_s21vflux.json
    ```
   
        
# 注意事项！！！！！
1. trans_all_npy = transform_s21peak_npy_and_processed_data(API_URL, API_KEY, dict_list)  # trans_all_npy的数据格式参考format_s21vflux.json  
该函数的参数只有API_URL, API_KEY, dict_list。
2. 返回值trans_all_npy的格式参考format_s21vflux.json
3. 先确定格式，生成format_****.json,后完成数据转换。