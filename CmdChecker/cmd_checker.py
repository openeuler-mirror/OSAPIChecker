# coding=utf-8
"""
@Project : OSChecker
@Time    : 2022/7/27 15:22
@Author  : wangbin
"""
import argparse
import sys
import os
import json
import time
import re
import logging
from subprocess import PIPE, Popen


def log_handler():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s][CmdChecker][%(levelname)s][%(message)s]')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    log_file_path = 'CmdChecker/logs/log_cmd_checker.txt'
    fh = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('[%(asctime)s][CmdChecker][%(filename)s:%(lineno)d]:[%(levelname)s][%(message)s]')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


logger = log_handler()


class Standard:
    """
    描述标准的类
    """
    def __init__(self, cmd_json):
        with open(cmd_json, 'r', encoding='utf-8') as f:
            self.cmd_list = json.load(f).get('system_cmds')

    def get_list(self):
        return self.cmd_list


class CMD:
    """
    cmd类
    """
    def __init__(self, cmd_path):
        """
        读取系统制定路径内的命令
        :param cmd_path:
        """
        with open(cmd_path, 'r', encoding='utf-8') as f:
            path_list = json.load(f).get('系统命令位置')
        self.cmd_list = []
        for path in path_list:
            for root, dirs, files in os.walk(path):
                for cmd in files:
                    self.cmd_list.append(cmd)
        with open(cmd_path, 'r', encoding='utf-8') as f:
            self.cmd_with_file = json.load(f).get('需要文件的命令')

    def is_exist(self, cmd):
        """
        cmd 存在性检查
        :param cmd:
        :return:
        """
        result = 'pass' if cmd in self.cmd_list else 'fail'
        return {
            'result': result
        }

    def check_run(self, cmd):
        """
        cmd  执行检查
        :param cmd:
        :return:
        """
        if cmd in self.cmd_with_file.keys():
            file = self.cmd_with_file.get(cmd)
            file = os.path.abspath(f"CmdChecker/testfiles/{file}")
            command = f'{cmd} {file}'
        else:
            command = f'{cmd} --version'
        re_str = 'not found'
        re_str_CN = '未找到'
        p = Popen(command, shell=True, stderr=PIPE, stdout=PIPE)
        stdout, stderr = p.communicate()
        error_by_stderr = re.search(re_str, stderr.decode('utf-8'))
        error_CN_by_stderr = re.search(re_str_CN, stderr.decode('utf-8'))
        if error_by_stderr or error_CN_by_stderr:
            return {
                'result': 'fail'
            }
        return {
            'result': 'pass'
        }

    @staticmethod
    def get_os_cmd_version(cmd):
        re_str = r'\b\d+\.[\d\.a-z]+'
        if cmd == 'sh':
            po = os.popen(f'echo $SHELL')
            cmd = po.readline()
            cmd = cmd[:-1]
        # if cmd == 'pax':
        #     po = os.popen(f'{cmd} --version')
        #     fetch = po.readline()
        #     version_by_version = re.search(re_str, fetch)
        #     if version_by_version:
        #         os_version = version_by_version.group()
        #         return os_version
        #
        # fetch = os.popen(f'{cmd} -V').readline()
        # version_by_V = re.search(re_str, fetch)
        # if version_by_V:
        #     os_version = version_by_V.group()
        #     return os_version
        for params in ['--version', '-V']:
            p = Popen(f'{cmd} {params}', shell=True, stderr=PIPE, stdout=PIPE)
            stdout, stderr = p.communicate()
            version_by_stdout = re.search(re_str, stdout.decode('utf-8'))
            version_by_stderr = re.search(re_str, stderr.decode('utf-8'))
            if version_by_stdout:
                os_version = version_by_stdout.group()
                return os_version
            if version_by_stderr:
                os_version = version_by_stderr.group()
                return os_version

        return 'not found'

    @staticmethod
    def get_os_cmd_path(cmd):
        if cmd == 'sh':
            shell_cmd = 'echo $SHELL'
        else:
            shell_cmd = 'which ' + cmd

        po = os.popen(f'{shell_cmd}')
        path = po.read().split('\n')[0]

        return path or 'not found'

    @staticmethod
    def compare_version(standard_version, os_version):
        ver1 = [int(x) for x in standard_version.split('.')]
        ver2 = [int(x) for x in os_version.split('.')]
        scenario_1 = ver1[0] > ver2[0]
        scenario_2 = ver1[0] == ver2[0] and ver1[1] > ver2[1]
        if len(ver1) > 2 and len(ver2) > 2:
            scenario_3 = ver1[0] == ver2[0] and ver1[1] == ver2[1] and ver1[2] > ver2[2]
        else:
            scenario_3 = False
        if scenario_1 or scenario_2 or scenario_3:
            logger.info(f'标准版本：{standard_version}， 系统中实际版本：{os_version}，标准测试 FAIL 。。。')
            return 'fail'
        logger.info(f'标准版本：{standard_version}， 系统中实际版本：{os_version}，标准测试 PASS 。。。')
        return 'pass'


class Result:
    def __init__(self):
        self.result = []

    def add(self, stand, exist_result, run_result, cmd_version, cmd_path):

        if run_result.get('result') == 'pass':
            result = 'pass'
        elif run_result.get('result') == 'skip':
            result = 'pass'
        elif run_result.get('result') == 'fail':
            result = 'fail'
        else:
            result = 'warning'

        self.result.append({
            'name': stand.get('name'),
            'exist_check': exist_result,
            'run_check': run_result,
            'cmd_version': cmd_version,
            'cmd_path': cmd_path,
            'result': result
        })

    def stat(self):
        total = 0
        pass_count = 0
        warn_count = 0
        for res in self.result:
            total += 1
            pass_count += 1 if res.get('result') == 'pass' else 0
            warn_count += 1 if res.get('run_check').get('result') == 'warning' else 0
        data = {
            'total': total,
            'pass': pass_count,
            'warning': warn_count,
            'fail': total - pass_count - warn_count
            }
        # logger.info(data)
        return data

    def export(self, timestamp=None, path=None):
        # pprint.pprint(self.result)
        data = {
            'handler': 'cmdchecker',
            'result': self.result
        }
        path = path or 'Outputs'
        if not timestamp:
            result_file = path + '/cmd_' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.json'
        else:
            result_file = path + '/cmd_' + timestamp + '.json'
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        logger.info(f'CmdChecker 测试完成，测试结果见 {path}')
        return path


class CmdChecker:
    def __init__(self, cmd_json_path=None, cmd_path_conf_path=None):
        logger.info('CmdChecker 执行开始。。。')
        cmd_json = cmd_json_path or os.path.abspath('Jsons/cmd_list.json')
        cmd_config_path = cmd_path_conf_path or os.path.abspath('Config/cmd_config.json')
        self.standard = Standard(cmd_json).get_list()
        self.os_cmd = CMD(cmd_config_path)
        self.result = Result()

    def check(self):
        # tmp = []
        for stand in self.standard:
            logger.info(f'cmd running...{stand}...')
            exist_result = self.os_cmd.is_exist(stand.get('name'))
            run_result = self.os_cmd.check_run(stand.get('name'))
            cmd_version = CMD.get_os_cmd_version(stand.get('name'))
            cmd_path = CMD.get_os_cmd_path(stand.get('name'))

            self.result.add(stand=stand, exist_result=exist_result, run_result=run_result, cmd_version=cmd_version, cmd_path=cmd_path)
            logger.info(f"\ncmd: {stand.get('name')}\n"
                        f"exist_check: {exist_result}\n"
                        f"run_result: {run_result}\n"
                        f"cmd_version: {cmd_version}\n"
                        f"cmd_path: {cmd_path}\n")
            # tmp.append({
            #     "name": stand.get('name'),
            #     "version": os_V
            # })
        # path = 'CmdChecker/report/cmd_result_tmp.json'
        # with open(path, 'w', encoding='utf-8') as f:
        #     json.dump({'result': tmp}, f)

    def export(self, timestamp=None):
        return self.result.export(timestamp)

    def stat(self):
        data = self.result.stat()
        logger.info(f'CmdChecker 测试结果:{data}')
        return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="操作系统标准工具SIG CMDChecker")
    parser.add_argument('-V', '--version', action='version', version='version 1.0 操作系统标准工具SIG CMDChecker')
    parser.add_argument('-L', '--list', default=None, metavar='cmd_list.json', help='cmd_list的json文件')
    parser.add_argument('-P', '--path', default=None, metavar='cmd_config.json', help='cmd可能存在的路径配置文件')
    parser.add_argument('-T', '--timestamp', default=None, action='store', type=str)
    args = parser.parse_args()
    if args.list and not os.path.isfile(args.list):
        print('CmdList.json 文件不正确 ！！！')
        sys.exit(1)
    if args.path and not os.path.isfile(args.path):
        print('cmd_config.json 文件不正确 ！！！')
        sys.exit(1)

    # main(args.list, args.path)
    checker = CmdChecker()
    checker.check()
    checker.export(args.timestamp)
    checker.stat()

