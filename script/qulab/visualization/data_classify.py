


from qulab import get_report
import pickle
import os

# -----------配置常量---------------
save_root = './tmp/dataset'
cnt = 0


if __name__ == "__main__":
    for i in range(12104, 109860):
        if cnt % 100 == 0:
            print(f"Processing: {cnt}")

        try:
            report = get_report(i)
        except Exception as e:
            print(f"Error getting report for id {i}: {e}")
            continue

        flow_name = report.workflow
        print("flow_name: ", flow_name)

        if 'tmp' in flow_name:
            # save to path
            tmp_str = flow_name.split('_tmp')[0]
            tmp_root = save_root + '/' + tmp_str
            os.makedirs(tmp_root, exist_ok=True)

            filename_str = flow_name.split('.')[0]
            filename_str = filename_str.split('_')[-1]
            save_path = f"{tmp_root}/{filename_str}_{i}.npy"

            # print("report: ", report)
            print("~~~~~~~~~~~save path: ", save_path)

            # save report to pkl file
            tmp = report.other_infomation
            print("tmp: ", len(tmp), type(tmp))

            if len(tmp) == 0:
                print("tmp is empty, skip", report)
                continue

            if type(tmp) == dict:
                if 'image' not in tmp:
                    print("tmp has no image key, skip", tmp)
                    continue
                content = tmp['image']
                print("tmp is dict, content : ", content.keys())
            elif type(tmp) == tuple:
                tmp1 = tmp[0]
                content = tmp1['image']

            print("content: ", content.keys())

            final_content = {'image': content}

            with open(save_path, 'wb') as f:
                pickle.dump(final_content, f)

            cnt += 1
            # if cnt > 10:
            #     break
