import copy
from  HAT.utils.VarRender import refresh
from HAT.core.globalContext import g_context
from HAT.parse.YamlCaseParser import load_yaml_files
from HAT.context.AppCaseContext import AppCaseContext
from HAT.extend.script import run_script
import pytest
import allure
from tqdm import tqdm
import os

class TestRunner:
    # load_context_from_yaml("./../examples/app-cases-yaml")
    # data=read_yaml("./examples/app-cases-yaml/login.yaml")
    data=load_yaml_files("../../examples/app-cases-yaml")
    print('执行用例需要用的数据',data)

    @pytest.mark.parametrize('caseinfo',data)
    def test_case_exceute(self,caseinfo):
        caseContext=None
        try:
            # keywords=Keywords()

            local_context=caseinfo.get("local_context",{})
            context=copy.deepcopy(g_context().show_dict())
            context.update(local_context)

            pre_script=refresh(caseinfo.get('前置条件',None),context)
            if pre_script:
                for script in eval(pre_script):
                    run_script.exec_script(script,g_context().show_dict())


            print('执行用例需要用的数据',caseinfo)

            base_info=caseinfo.get("基础配置",None)
            # print("基础配置数据",base_info)
            allure.dynamic.parameter("caseinfo","")
            allure.dynamic.feature(base_info.get("一级模块",""))
            allure.dynamic.story(base_info.get("二级模块",""))
            allure.dynamic.title(base_info.get("用例标题",""))
            case_type = base_info.get("用例类型")
            if case_type == "AppCase":
                caseContext = AppCaseContext()
                keywords = caseContext.init_keywords()
                caseContext.start()

            steps=caseinfo.get("用例步骤", None)
            # print("项目真正要操作的事情用例步骤", steps)

            with tqdm(total=len(steps), desc="用例执行进度") as pbar:
                for step in steps:
                    # print('项目具体操作挨个拿出来',step)
                    # print('键',list(step.keys())[0])
                    # print('值', list(step.values())[0])
                    step_name=list(step.keys())[0]
                    step_value=list(step.values())[0]
                    pbar.set_description(f"正在执行{step_name}")
                    pbar.update(1)

                    context=copy.deepcopy(g_context().show_dict())
                    step_value=eval(refresh(step_value,context))

                    with allure.step(step_name):
                        key = step_value['操作类型']
                    try:
                        key_func=keywords.__getattribute__(key)
                        key_func(**step_value)
                    except AttributeError:
                        if g_context.get_dict("keydir")is not NOne:
                            keywords.ex_invoke(key=key,step_value=step_value)
                        os.path.append()

            local_context=caseinfo.get("local_context",{})
            context=copy.deepcopy(g_context().show_dict())
            context.update(local_context)

            pre_script=refresh(caseinfo.get('后置条件',None),context)
            if pre_script:
                for script in eval(pre_script):
                    run_script.exec_script(script,g_context().show_dict())
        finally:
            if caseContext is not None:
                caseContext.release()