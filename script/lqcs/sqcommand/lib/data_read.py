import h5py
import os



def get_hdf5_content(hdf5_file_path):
    """
    读取你的hdf5文件
    """
    print(hdf5_file_path)
    abs_path = os.path.abspath(hdf5_file_path)
    result = {}
    if not os.path.exists(abs_path):
        print(f"❌ hdf5文件不存在：{abs_path}")
        return None
    with h5py.File(hdf5_file_path, 'r') as f:
        # 主数据
        dv = f['DataVault']
        title = dv.attrs.get('Title', '').split(':')[0]
    
        if isinstance(dv, h5py.Dataset):
            data = dv[()]  # 获取所有数据

            result[title]=data
            return result
        



def get_latest_content(root_folder, task_type = 's21'):

    max_num = -1
    latest_file_name = None

    for filename in os.listdir(root_folder):
        if not filename.endswith('.hdf5'):
            continue

        number_id = int(filename.split(' - ')[0])

        if number_id > max_num and task_type in filename.lower():
            max_num = number_id
            latest_file_name = filename

    if latest_file_name is not None:
        print("find latest file: ", latest_file_name)
    else:
        return

    hdf5_path = os.path.join(root_folder, latest_file_name)
    pure_name = latest_file_name.split('.')[0]

    # 加载hdf5
    print("hdf5_path: ", hdf5_path)
    data = get_hdf5_content(hdf5_path)

    return data, pure_name

