
import subprocess


def shell_cmd(cmd_list, inmsg=None):
    """
    :param cmd_list:
    :param inmsg:
    :return:
    """
    p = subprocess.Popen(cmd_list, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if inmsg:
        p.stdin.write(inmsg)
    out, err = p.communicate()

    return p.returncode, out.decode("utf-8", errors="ignore"), err.decode("utf-8", errors="ignore")