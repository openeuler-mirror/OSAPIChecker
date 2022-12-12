import logging
import os
import stat
import sys
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ServiceChecker.utils.shell import shell_cmd
from ServiceChecker.utils.logger import init_logger

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
        self.sh_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "service_verify.sh"))
        self.dir_path = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.log_path = os.path.join(self.dir_path, 'Logs/service_checker.log')
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

    def service_register_check(self, model='start'):
        os.chmod(self.sh_path, stat.S_IXUSR)

        try:
            os.system(f"/bin/bash {self.sh_path} {model} 2>&1 | tee -a {self.log_path}")
            if model == "reboot":
                logger.info("service_checker 检测完成!")
                # 删除reboot.service配置文件
                self.clear_reboot_service()
        except Exception as err:
            logger.error(f"检测出错：{err}")

    def clear_reboot_service(self):
        try:
            os.system(f"rm -f {os.path.join(self.systemd_path, self.reboot)}")
        except Exception as err:
            logger.error(f"删除reboot.service错误：{err}")

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
    elif args.verify_model == "reboot":
        service_checker.service_register_check(model=args.verify_model)
    else:
        logger.error("参数输入有误。")
