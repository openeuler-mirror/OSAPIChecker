import json
import logging
import os
import stat
import sys
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ServiceChecker.utils.shell import shell_cmd
from ServiceChecker.utils.logger import init_logger
from ServiceChecker.constants import K_TEST, k_VERIFY, VERIFY_PATH_TYPE, PASS, CHECK_RESULT, FAIL, TARGET_UNIT, \
    START_MODEL_TYPE, REBOOT_MODEL_TYPE, MODEL_REBOOT, MODEL_START

logger = logging.getLogger('OSAPIChecker')


def init_args():
    """
    init args
    :return:
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--model", type=str, dest="verify_model", default="", help="service verify model")

    return parser.parse_args()


class ServiceChecker(object):

    def __init__(self):
        self.systemd_path = "/usr/lib/systemd/system"
        self.dir_path = os.path.realpath(os.path.join(os.path.dirname(__file__)))
        self.sh_path = os.path.join(self.dir_path, "service_verify.sh")
        self.log_path = os.path.join(os.path.dirname(self.dir_path), 'Logs/service_checker.log')
        self.reboot = "verify_reboot.service"

    @staticmethod
    def verify_service():
        cmd = ["systemctl", "--version"]
        ret, out, err = shell_cmd(cmd)
        if not ret:
            if err:
                logger.debug(f"Systemd 版本检查信息失败！{err}")
            if out:
                logger.info(f"Systemd 版本检查信息为:\n{out.splitlines()[0]}")

    @staticmethod
    def export_verify_result(path, result):

        with open(path, "w", encoding='utf-8') as f:
            json.dump(result, f, indent=4)

    @staticmethod
    def verift_cmd_unit(cmd, result, unit, target_result):
        ret, out, err = shell_cmd(cmd.split())
        if not ret:
            if out:
                if unit == TARGET_UNIT:
                    result.get(unit)[CHECK_RESULT] = PASS
                elif target_result in out:
                    result.get(unit)[CHECK_RESULT] = PASS
        else:
            logger.debug(f"验证检测单元{unit}输出信息错误：{err}")

    def service_register_check(self, model='start'):
        result_path = os.path.join(os.path.dirname(self.dir_path), 'Outputs/service_result.json')
        os.chmod(self.sh_path, stat.S_IXUSR)

        try:
            os.system(f"/bin/bash {self.sh_path} {model} 2>&1 | tee -a {self.log_path}")
            if model == MODEL_START:
                result = {}
                start_result = self.verify_all_item(model, result)

                self.export_verify_result(result_path, start_result)

                # 重启系统
                os.system("reboot")

            elif model == MODEL_REBOOT:
                logger.info("service_checker 检测完成!")
                with open(result_path, "r") as f:
                    start_result = json.load(f)

                final_result = self.verify_all_item(model, start_result)
                self.export_verify_result(result_path, final_result)

                self.clear_environment('clear')
        except Exception as err:
            logger.error(f"检测过程出现错误：{err}")

    def clear_environment(self, clear):
        """
        关闭并删除测试单元自定义配置文件，恢复测试环境初始配置
        """
        try:
            os.system(f"/bin/bash {self.sh_path} {clear}")
        except Exception as err:
            logger.error(f"删除reboot.service错误：{err}")

    def get_verify_result_config(self):
        verify_path = os.path.join(self.dir_path, 'config/verify_result.json')
        with open(verify_path, "r") as rf:
            verify_config = json.load(rf)

        return verify_config

    def verify_all_item(self, model, result):
        """
        根据model来对所有systemd的待检测单元进行检测结果校验，输出汇总结果。
        @param model: 区分重启前（start）及重启后(reboot)检测的Unit.
        @param result: 检测结果
        @return: 检测结果
        """
        v_config = self.get_verify_result_config()
        for unit, verify_content in v_config.items():
            verify_cmd = verify_content.get(K_TEST)
            target_result = verify_content.get(k_VERIFY)
            if model == MODEL_START:
                result.setdefault(unit, {CHECK_RESULT: FAIL})
                if unit not in START_MODEL_TYPE:
                    continue
                elif unit in VERIFY_PATH_TYPE:
                    if os.path.exists(verify_cmd):
                        result.get(unit)[CHECK_RESULT] = PASS
                else:
                    self.verift_cmd_unit(verify_cmd, result, unit, target_result)
            elif model == MODEL_REBOOT:
                if unit not in REBOOT_MODEL_TYPE:
                    continue
                self.verift_cmd_unit(verify_cmd, result, unit, target_result)

        return result

    def collect_runlevel_target(self):
        run_level_cmd = ['find', self.systemd_path, '-name', "runlevel*.target"]
        ret, out, err = shell_cmd(run_level_cmd)
        if not ret:
            if err:
                logger.debug("systemd所有运行级别target文件查询失败")
            if out:
                run_level_contents = ''
                for line in out.split('\n'):
                    if not line:
                        continue
                    target_file = os.readlink(line)
                    run_level_contents += f"{os.path.dirname(line)} -> {target_file}\n"
                logger.info(f"查询运行级别传统runlevel与对应target信息如下：\n{run_level_contents.rstrip()}")
        else:
            logger.debug("没有查询到systemd运行级别信息")


if __name__ == "__main__":
    init_logger()

    args = init_args()
    service_checker = ServiceChecker()
    # 首次调用该模块执行部分
    if not args.verify_model:
        service_checker.verify_service()
        service_checker.service_register_check()
    # 系统重启后检测待测功能
    elif args.verify_model == MODEL_REBOOT:
        service_checker.service_register_check(model=args.verify_model)
    else:
        logger.error("参数输入有误。")
