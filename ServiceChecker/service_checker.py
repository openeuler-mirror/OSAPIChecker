import logging
import os
import stat
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ServiceChecker.utils.shell import shell_cmd
from ServiceChecker.utils.logger import init_logger

logger = logging.getLogger('OSAPIChecker')


class ServiceChecker(object):

    @staticmethod
    def view_version():
        cmd = ["systemctl", "--version"]
        ret, out, err = shell_cmd(cmd)
        if not ret:
            if err:
                logger.debug(f"Systemd 版本检查信息失败！{err}")
            if out:
                logger.info(f"Systemd 版本检查信息为:\n{out.splitlines()[0]}")

    @staticmethod
    def registered_service():
        sh_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "service_verify.sh"))
        os.chmod(sh_path, stat.S_IXUSR)
        dir_path = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        log_path = os.path.join(dir_path, 'Logs/service_checker.log')
        try:
            os.system(f"{sh_path} 2>&1 | tee -a {log_path}")
            logger.info("service_checker 检测完成!")
        except Exception as err:
            logger.error(f"检测出错：{err}")


if __name__ == "__main__":
    init_logger()
    service_checker = ServiceChecker()
    # 测试systemd组件service、socket、path单元
    service_checker.registered_service()
    # 查看systemd版本信息
    service_checker.view_version()
