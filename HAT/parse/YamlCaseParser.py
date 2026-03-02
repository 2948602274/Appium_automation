import yaml
import os
from HAT.core.globalContext import g_context

def read_yaml(file_path):

    case_infos=[]
    with open(file_path,'r',encoding='utf-8')as file:
        data = yaml.safe_load(file)
        # print('yaml用例数据',data)
    case_infos.append(data)
    return case_infos

def load_context_from_yaml(folder_path):
    yaml_file_path=os.path.join(folder_path,"context.yaml")
    # print(yaml_file_path)
    with open(yaml_file_path,"r",encoding='utf-8') as file:
        data=yaml.safe_load(file)
        if data:g_context().set_by_dict(data)
        # print(data)

def load_yaml_files(folder_path):
    suite_folder=os.path.join(folder_path,)
    load_context_from_yaml(suite_folder)
    # 读取符合规则的yaml用例数据
    file_names = [(int(f.split("_")[0]), f) for f in os.listdir(suite_folder)
                  if f.endswith(".yaml") and f.split("_")[0].isdigit()]
    # print("文件符合规则的数据", file_names)
    file_names.sort()
    [f[-11]for f in file_names]


if __name__ == '__main__':
    # load_context_from_yaml("../../examples/app-cases-yaml")
    load_yaml_files("../../examples/app-cases-yaml")