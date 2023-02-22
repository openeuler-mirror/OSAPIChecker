#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import os
import json
import sys
import platform
import logging
import time
import getpass

timestamp = int(time.time())
#import tkinter # for graphical user interface

# import libchecker # import libhecker module
# import cmdchecker # import cmdchecker module
# import fschecker  # import fschecker  module

# 0. Global Init
parser = argparse.ArgumentParser(description="This Progermm is OSChecker", prog="OSChecker")

# --channel: 
#       cmdchecker
#       libchecker 
#       fschecker
parser.add_argument('-c', '--channel', action='store', type=str, help='Choice OSAPIChecker channels: libchecker,cmdchecker,fschecker,servicechecker,all', default="all")

# --strategy: 
#       base (default)
#       only-expand
#       with-expand
parser.add_argument('-s', '--strategy', action='store', type=str, help='Choice OSAPIChecker strategy: basic,expansion,with-expand', default="basic")

# --level:
#       l1
#       l2
#       l3
#       l1l2 (default)
#       l1l2l3
parser.add_argument('-l', '--level', action='store', type=str, help='Choice OSAPIChecker level like: l1,l2,l3,l1l2,l1l2l3', default="l1l2")

# --ostype:
#       desktop
#       service
#       embed
#       other
parser.add_argument('-t', '--ostype', action='store', type=str, help='OSType of current OS: desktop, server', default="desktop")

# --pkgmngr:
#       apt-deb
#       yum-rpm
#       other
parser.add_argument('-p', '--pkgmngr', action='store', type=str, help='Package Manager of current OS: apt-deb, yum-rpm', default="apt-deb")

# --stdjson:
# 
#parser.add_argument('-j', '--stdjson', action='store', type=str, help='Choice OSAPIChecker standard json templete file', required=True)

parser.add_argument('-o', '--organize', action='store', type=str, help='Choice Organize', default="")

parser.add_argument('-R', '--reports', action='store_true', help='Generate Reports')
# --ostype:
#       desktop
#       service
#       embed

args = parser.parse_args()

l_file_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(timestamp)) 
l_arch_name = os.popen("uname -m").read().rstrip("\n")

# 1. Input Valid Check
def input_valid_check():
    print("|************************ 操作系统软件兼容性应用编程接口检查工具 ************************|")

# 2. Check Environment Info
def gen_envinfo_json():
    l_organize = args.organize 
    l_osname = platform.system()
    l_osversion = platform.version()
    l_osmachine = platform.machine()
    l_osarchitecture = platform.architecture()
    l_osprocessor = platform.processor()
    l_kernel = os.popen("uname -r").read().rstrip("\n")
    l_compver = os.popen("gcc --version | awk 'NR==1'").read().rstrip("\n")
    l_pythonver = os.popen("python3 --version").read().rstrip("\n")
    l_meminfo = os.popen("free -g | grep Mem | awk '{print $2}'").read().rstrip("\n") + "G"
    l_firmwareinfo = os.popen("dmidecode -s bios-version").read().rstrip("\n")
    l_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)) 
    l_disk = os.popen("lsblk -d -n | awk '{print $4}'").read().rstrip("\n")

    #l_envinfodict = {"测试对象" : {"系统名称" : l_osname, "版本" : l_osversion}, "送测单位" : l_organize , "系统环境" : {"内核版本" : l_kernel , "编译器版本" : l_compver , "Python版本" : l_pythonver} , "环境配置" : {"机器型号" : l_osmachine , "CPU指令集" : l_osmachine , "CPU型号" : l_osprocessor , "内存" : l_meminfo , "硬盘" : l_disk, "固件" : l_firmwareinfo} , "测试工具" : {"名称" : "OSAPIChecker", "版本" : "1.0.0" } , "测试时间" : l_time }
    l_envinfodict = {"测试对象" : {"系统名称" : l_osname, "版本" : l_osversion}, "送测单位" : l_organize , "系统环境" : {"内核版本" : l_kernel , "编译器版本" : l_compver , "Python版本" : l_pythonver} , "环境配置" : {"CPU指令集" : l_osmachine , "CPU型号" : l_osprocessor , "内存" : l_meminfo , "硬盘" : l_disk, "固件" : l_firmwareinfo} , "测试工具" : {"名称" : "OSAPIChecker", "版本" : "1.0.0" } , "测试时间" : l_time }
    
    env_file_name = "Outputs/environments-info_%s.json" %(l_file_time) 
    #with open("Outputs/environments-info.json","w+") as fw:
    with open(env_file_name,"w+") as fw:
        json.dump(l_envinfodict,fw,ensure_ascii=False,indent=4)

def checker_call_handler(channel):
    if (channel == "libchecker"):
        print("进入 LibChecker 处理程序 . . .")
        s_str = args.strategy
        l_str = args.level
        os_str = args.ostype
        pkg_str = args.pkgmngr
        org_str = args.organize
        
        if ((s_str != "basic") and (s_str != "expansion") and (s_str != "with-expand")):
            print ("Error: -s or --strategy 参数指定错误")
            return 2

        level_list=['l1', 'l2', 'l3', 'l1l2', 'l1l3', 'l2l3', 'l1l2l3', 'l2l1', 'l3l1', 'l3l2', 'l1l3l2', 'l2l1l3', 'l2l3l1', 'l3l1l2', 'l3l2l1']
        if l_str not in level_list:
            print ("Error: -l or --level 参数指定错误")
            return 2

        if ((os_str != "desktop") and (os_str != "server")):
            print ("Error: -t or --ostype 参数指定错误")
            return 2

        if ((pkg_str != "apt-deb") and (pkg_str != "yum-rpm")):
            print ("Error: -p or --pkgmngr 参数指定错误")
            return 2

        os.system('python3 LibChecker/lib_checker.py --strategy=%s --level=%s --ostype=%s --pkgmngr=%s --organize=%s --timetmp=%s' %(s_str, l_str, os_str, pkg_str, org_str, l_file_time))        


    elif (channel == "cmdchecker"):
        print("进入 CmdChecker 处理程序 . . .")

        os.system('python3 CmdChecker/cmd_checker.py')
        
    elif (channel == "fschecker"):
        print("进入 FsChecker 处理程序 . . .")

        os.system('python3 FsChecker/fs_checker.py')
        

    elif (channel == "servicechecker"):
        print("进入 ServiceChecker 处理程序 . . .")

        login_name = getpass.getuser()
        if (login_name != "root"):
            os.system('sudo python3 ServiceChecker/service_checker.py')
        else:
            os.system('python3 ServiceChecker/service_checker.py')
        

    else:
        print("Invalid Options, please input --channel=[cmdchecker|fschecker|libchecker]")

def report_pdf_service(channel):
    os.system('sudo reports/reboot-pdf.sh %s %s' %(channel, l_file_time))

def report_pdf_shell(channel):
    os.system('reports/report-pdf.sh %s %s' %(channel, l_file_time))

# 3. PDF Report files
def generate_report(channel):
    if ((channel == "all") or (channel == "servicechecker")):
        print ("会重启（包含servicechecker模块）")
        report_pdf_service(channel)
    elif ((channel == "libchecker") or (channel == "cmdchecker") or (channel == "fschecker")):
        print ("不重启，单独程序：", channel)
        report_pdf_shell(channel)


def main_loop():
    gen_envinfo_json()
    if (args.channel == "all"):
        checker_call_handler("libchecker")
        checker_call_handler("cmdchecker")
        checker_call_handler("fschecker")
        if(args.reports):
            generate_report(args.channel)
        else:
            print ("NO Report Generation")
        checker_call_handler("servicechecker")
    else:
        if ((args.channel != "libchecker") and (args.channel != "cmdchecker") and (args.channel != "fschecker") and (args.channel != "servicechecker")):
            print ("Error: -c or --channel 参数指定错误")
            return 2
        if (args.channel == "servicechecker"):
            if(args.reports):
                generate_report(args.channel)
            else:
                print ("NO Report Generation")
            checker_call_handler(args.channel)
        else:
            checker_call_handler(args.channel)
            if(args.reports):
                generate_report(args.channel)
            else:
                print ("NO Report Generation")

# 4. Draw Graphics
def draw_main_gui():
    top = tkinter.Tk()
    top.mainloop()


# Main entry point
if __name__ == '__main__':
    try:
        input_valid_check()
        main_loop()
#        draw_main_gui()
    except Exception as e:
        print(e)


