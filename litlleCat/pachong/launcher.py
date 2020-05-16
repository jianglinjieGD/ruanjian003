from flask_script import Command
import sys, argparse, importlib, traceback    # 需要读取命令参数


# job 同一入口文件
# 需要继承Command，才会默认执行run函数
# python manager.py runJob 加上：
# -m: path of model:
# default pre_fixed is "pachong/"

class Run_job(Command):
    # 不加下面一句，会提示参数太多
    capture_all_args = True

    def run(self, *args, **kwargs):
        # 读入参数
        args = sys.argv[2:]         # python manager.py runJob -m
        # 新建参数解析器
        parser = argparse.ArgumentParser(add_help=True)
        parser.add_argument("-m", "--name", dest="name",metavar="name", help="指定job名", required=True)
        # 可以通过才参数来执行 不同的动作
        parser.add_argument("-a", "--act", dest="act", metavar="act", help="Job动作", required=False)
        # 提供该参数来 增加传入的参数的数量； 其中  nargs="*" 表示无限制
        parser.add_argument("-p", "--param", dest="param", nargs="*", metavar="param", help="业务参数", required=False)
        # 使用参数解析器进行解析
        # 解析器的结果的对象，转化成dict
        params = parser.parse_args(args).__dict__
        if "name" not in params or params["name"] is None:
            return self.tips()

        try:
            '''
            from jobs.tasks.test import JobTask
            '''
            module_name = params['name'].replace("/", ".")      # 修改成 import语句
            import_string = "pachong.tasks.%s" % module_name    # 加上模块名
            target = importlib.import_module(import_string)     # 引入
            exit(target.Job_task().run(params))                 # 执行 不论哪个job模块 class都是 Job_task
            # Job_task() 该方法是在初始化
        except Exception as e:
            traceback.print_exc()

        return

    def tips(self):
        tip_msg = '''
            请正确调度job
            python manager.py runJob -m test
        
        '''
        return tip_msg



