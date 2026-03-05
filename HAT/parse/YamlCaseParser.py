import yaml
import os
import uuid
import copy
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
    yaml_caseInfos=[]
    suite_folder=os.path.join(folder_path)
    load_context_from_yaml(suite_folder)
    # 读取符合规则的yaml用例数据
    file_names = [(int(f.split("_")[0]), f) for f in os.listdir(suite_folder)
                  if f.endswith(".yaml") and f.split("_")[0].isdigit()]
    # print("文件符合规则的数据", file_names)
    file_names.sort()
    file_names=[f[-1]for f in file_names]
    print("用例文件列表",file_names)

    for file_name in file_names:
        file_path=os.path.join(folder_path,file_name)
        print("用例文件路径",file_path)
        with open(file_path,'r',encoding="utf-8") as rfile:
            caseinfo=yaml.safe_load(rfile)
            print("用例数据",caseinfo)
            yaml_caseInfos.append(caseinfo)
    return yaml_caseInfos

def yaml_case_parser(config_path):
    case_names=[]
    case_infos=[]
    yaml_caseInfos=load_yaml_files(config_path)
    print("符合规则的所有yaml用例数据",yaml_caseInfos)
    for caseinfo in yaml_caseInfos:
        ddts=caseinfo.get("数据驱动",[])
        # print("数据驱动", ddts)
        if len(ddts)>0:
            caseinfo.pop("数据驱动")
        if len(ddts)==0:
            case_name=caseinfo.get("基础配置").get("用例标题",uuid.uuid4().__str__())
            case_names.append(case_name)
            case_infos.append(caseinfo)
        else:
            for ddt in ddts:
                new_case=copy.deepcopy(caseinfo)
                new_case.update({"local_context":ddt})
                case_name = caseinfo.get("基础配置").get("用例标题", uuid.uuid4().__str__())
                case_name=f'{case_name}-{ddt.get("描述标题",uuid.uuid4().__str__())}'
                new_case.get("基础配置").update({"用例标题":case_name})
                case_names.append(new_case)
                case_infos.append(case_name)
    return {
        "case_infos":case_infos,
        "case_names":case_names
    }

if __name__ == '__main__':
    yaml_case_parser("../../examples/app-cases-yaml")