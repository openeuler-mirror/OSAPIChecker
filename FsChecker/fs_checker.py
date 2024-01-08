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
import logging
import time


def log_handler():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s][FsChecker][%(levelname)s][%(message)s]')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    log_file_path = 'FsChecker/logs/log_fs_checker.txt'
    fh = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('[%(asctime)s][FsChecker][%(filename)s:%(lineno)d]:[%(levelname)s][%(message)s]')
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
            self.cmd_list = json.load(f).get('FS')

    def get_list(self):
        """
        返回标准文件内的fs列表
        :return: list
        """
        return self.cmd_list


class Result:
    """
    结果类
    """
    def __init__(self):
        self.result = []

    def add(self, stand, exist_result, file_permissions):
        self.result.append({
            'FS_name': stand.get('FS_name'),
            'exist_check': exist_result,
            'file_permissions': file_permissions,
            'result': exist_result.get('result')
        })

    def stat(self):
        total = 0
        pass_count = 0
        for res in self.result:
            total += 1
            pass_count += 1 if res.get('result') == 'pass' else 0
        data = {
            'total': total,
            'pass': pass_count,
            'fail': total - pass_count
            }
        # logger.info(data)
        return data

    def export(self, timestamp=None, path=None):
        # pprint.pprint(self.result)
        data = {
            'handler': 'fs_checker',
            'result': self.result
        }
        path = path or 'Outputs'
        if not timestamp:
            result_file = path + '/fs_' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.json'
        else:
            result_file = path + '/fs_' + timestamp + '.json'
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        logger.info(f'FSChecker 测试完成，测试结果见 {path}')
        return path


class FSChecker:
    """
    fs的checker 类.
    """
    def __init__(self, cmd_json_path=None):
        logger.info('FSChecker 执行开始。。。')
        fs_json = cmd_json_path or os.path.abspath('Jsons/fs_list.json')
        self.standard = Standard(fs_json).get_list()
        self.result = Result()

    @staticmethod
    def _get_file_permissions(file):
        if os.path.exists(file):
            return oct(os.lstat(file).st_mode)[-4:]
        else:
            return "not found"

    def check(self):
        """
        fs的测试方法，遍历标准中的fs进行存在性检测
        :return:
        """
        # tmp = []
        for stand in self.standard:
            logger.info(f'fs checking...{stand}...')
            # 增加对普通文件和特殊文件（字符设备文件和链接文件）的判断
            if stand.get('type') == 'directory':
                exist_result = {
                    'result': 'pass' if os.path.isdir(stand.get('FS_name')) else 'fail'
                }
            elif stand.get('type') == 'file':
                exist_result = {
                    'result': 'pass' if os.path.isfile(stand.get('FS_name')) else 'fail'
                }
            else:
                exist_result = {
                    'result': 'pass' if os.path.exists(stand.get('FS_name')) else 'fail'
                }
            file_permissions = self._get_file_permissions(stand.get('FS_name'))
            self.result.add(stand=stand, exist_result=exist_result, file_permissions=file_permissions)
            logger.info(f"\ncmd: {stand.get('FS_name')},\n"
                        f"exist_check: {exist_result}\n"
                        f"file_permissions: {file_permissions}\n")

        # fs权限暂时不做处理
        #     permission = oct(os.stat(stand.get('FS_name')).st_mode)[-4:]
        #     tmp.append({
        #         "FS_name": stand.get('FS_name'),
        #         "type": 'directory',
        #         'permission': str(permission)
        #     })
        # path = 'FsChecker/report/fs_result_tmp.json'
        # with open(path, 'w', encoding='utf-8') as f:
        #     json.dump({'result': tmp}, f)

    def export(self, timestamp):
        """
        输出文件报告
        :return:
        """
        return self.result.export(timestamp)

    def stat(self):
        """
        对检查结果进行统计
        :return:
        """
        data = self.result.stat()
        logger.info(f'FSChecker 测试结果:{data}')
        return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="操作系统标准工具SIG FsChecker")
    parser.add_argument('-V', '--version', action='version', version='version 1.0 操作系统标准工具SIG FS Checker')
    parser.add_argument('-L', '--list', default=None, metavar='fs_list.json', help='fs_list的json文件')
    parser.add_argument('-T', '--timestamp', default=None, action='store', type=str)
    args = parser.parse_args()
    if args.list and not os.path.isfile(args.list):
        print('fs_list.json 文件不正确 ！！！')
        sys.exit(1)

    # main(args.list, args.path)
    checker = FSChecker()
    checker.check()
    checker.export(args.timestamp)
    checker.stat()

