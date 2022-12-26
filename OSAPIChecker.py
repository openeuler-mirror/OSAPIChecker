#!/usr/bin/python3

import argparse
import os
import sys
import logging
#import tkinter # for graphical user interface

# import libchecker # import libhecker module
# import cmdchecker # import cmdchecker module
# import fschecker  # import fschecker  module

# 0. Global Init
parser = argparse.ArgumentParser(description="This Progermm is OSChecker", prog="OSChecker")

# --channel: 
#       cmdchecker (default)
#       libchecker 
#       fschecker
parser.add_argument('-c', '--channel', action='store', type=str, help='Choice OSAPIChecker channels: libchecker,cmdchecker,fschecker', default="cmdchecker")

# --strategy: 
#       base (default)
#       only-expand
#       with-expand
parser.add_argument('-s', '--strategy', action='store', type=str, help='Choice OSAPIChecker strategy: base,onyl-expand,with-expand', default="base")

# --level:
#       l1
#       l2
#       l3
#       l1l2 (default)
#       l1l2l3
parser.add_argument('-l', '--level', action='store', type=str, help='Choice OSAPIChecker level: l1,l2,l3,l1l2,l1l2l3', default="l1l2")

# --ostype:
#       desktop
#       service
#       embed
#       other
parser.add_argument('-t', '--ostype', action='store', type=str, help='OSType of current OS: desktop, server, embed，other', default="desktop")

# --pkgmngr:
#       apt-deb
#       yum-rpm
#       other
parser.add_argument('-p', '--pkgmngr', action='store', type=str, help='Package Manager of current OS: apt-deb, yum-rpm, othrr', default="apt-deb")

# --stdjson:
# 
#parser.add_argument('-j', '--stdjson', action='store', type=str, help='Choice OSAPIChecker standard json templete file', required=True)


args = parser.parse_args()


# 1. Input Valid Check
def input_valid_check():
    print("|************************ 操作系统软件兼容性应用编程接口检查工具 ************************|")
#    print('the options is', options)

    # Options check

    # Json check


# 2. Call Subchecker's Handler
    # --channel:    [cmdchecker,fschecker,libchecker]
    # --strategy:   [with-expand, base]
    # --level       [l1,l2,l3,l1l2,l1l2l3]
    # --ostype      [desktop,server,embed]
    # --pkgmngr     [apt-deb,yum-rpm,src-bin,other]
def checker_call_handler():
    if (args.channel == "libchecker"):
        print("进入 LibChecker 处理程序 . . .")
        if (args.strategy == "with-expand"):
            if (args.level == "l1"):
                if (args.ostype == "desktop"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1 --ostype=desktop --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1 --ostype=desktop --pkgmngr=yum-rpm')
                    else: # desktop default use apt-deb
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1 --ostype=desktop --pkgmngr=apt-deb')
                elif (args.ostype == "server"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1 --ostype=server --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1 --ostype=server --pkgmngr=yum-rpm')
                    else: # server default use yum-rpm
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1 --ostype=server --pkgmngr=yum-rpm')
                else: # default desktop with apt-deb
                    os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1 --ostype=desktop --pkgmngr=apt-deb')
            # end "level l1"
            elif (args.level == "l2"):
                if (args.ostype == "desktop"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l2 --ostype=desktop --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l2 --ostype=desktop --pkgmngr=yum-rpm')
                    else: # desktop default use apt-deb
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l2 --ostype=desktop --pkgmngr=apt-deb')
                elif (args.ostype == "server"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l2 --ostype=server --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l2 --ostype=server --pkgmngr=yum-rpm')
                    else: # server default use yum-rpm
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l2 --ostype=server --pkgmngr=yum-rpm')
                else: # default desktop with apt-deb
                    os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l2 --ostype=desktop --pkgmngr=apt-deb')
            # end "level l2"
            elif (args.level == "l3"):
                if (args.ostype == "desktop"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l3 --ostype=desktop --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l3 --ostype=desktop --pkgmngr=yum-rpm')
                    else: # desktop default use apt-deb
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l3 --ostype=desktop --pkgmngr=apt-deb')
                elif (args.ostype == "server"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l3 --ostype=server --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l3 --ostype=server --pkgmngr=yum-rpm')
                    else: # server default use yum-rpm
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l3 --ostype=server --pkgmngr=yum-rpm')
                else: # default desktop with apt-deb
                    os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l3 --ostype=desktop --pkgmngr=apt-deb')
            # end "level l3"
            elif (args.level == "l1l2"):
                if (args.ostype == "desktop"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=desktop --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=desktop --pkgmngr=yum-rpm')
                    else: # desktop default use apt-deb
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=desktop --pkgmngr=apt-deb')
                elif (args.ostype == "server"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=server --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=server --pkgmngr=yum-rpm')
                    else: # server default use yum-rpm
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=server --pkgmngr=yum-rpm')
                else: # default desktop with apt-deb
                    os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=desktop --pkgmngr=apt-deb')
            # end "level l1l2"

            elif (args.level == "l1l2l3"):
                if (args.ostype == "desktop"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2l3 --ostype=desktop --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2l3 --ostype=desktop --pkgmngr=yum-rpm')
                    else: # desktop default use apt-deb
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2l3 --ostype=desktop --pkgmngr=apt-deb')
                elif (args.ostype == "server"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2l3 --ostype=server --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2l3 --ostype=server --pkgmngr=yum-rpm')
                    else: # server default use yum-rpm
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2l3 --ostype=server --pkgmngr=yum-rpm')
                else: # default desktop with apt-deb
                    os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2l3 --ostype=desktop --pkgmngr=apt-deb')
            # end l1l2l3
            else:
                # os.system('python3 LibChecker/lib_checker.py --strategy=with-expand')
                os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=desktop --pkgmngr=apt-deb')
        elif (args.strategy == "base"):
            if (args.level == "l1"):
                if (args.ostype == "desktop"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1 --ostype=desktop --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1 --ostype=desktop --pkgmngr=yum-rpm')
                    else: # desktop default use apt-deb
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1 --ostype=desktop --pkgmngr=apt-deb')
                elif (args.ostype == "server"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1 --ostype=server --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1 --ostype=server --pkgmngr=yum-rpm')
                    else: # desktop default use yum-rpm
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1 --ostype=server --pkgmngr=yum-rpm')
                else: # default desktop with apt-deb
                    os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1 --ostype=desktop --pkgmngr=apt-deb')
            # end l1
            elif (args.level == "l2"):
                if (args.ostype == "desktop"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l2 --ostype=desktop --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l2 --ostype=desktop --pkgmngr=yum-rpm')
                    else: # desktop default use apt-deb
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l2 --ostype=desktop --pkgmngr=apt-deb')
                elif (args.ostype == "server"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l2 --ostype=server --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l2 --ostype=server --pkgmngr=yum-rpm')
                    else: # server default use yum-rpm
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l2 --ostype=server --pkgmngr=yum-rpm')
                else: # default desktop with apt-deb
                    os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l2 --ostype=desktop --pkgmngr=apt-deb')
            # end l2
            elif (args.level == "l3"):
                if (args.ostype == "desktop"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l3 --ostype=desktop --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l3 --ostype=desktop --pkgmngr=yum-rpm')
                    else: # desktop default use apt-deb
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l3 --ostype=desktop --pkgmngr=apt-deb')
                elif (args.ostype == "server"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l3 --ostype=server --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l3 --ostype=server --pkgmngr=yum-rpm')
                    else: # server default use yum-rpm
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l3 --ostype=server --pkgmngr=yum-rpm')
                else: # default desktop with apt-deb
                    os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l3 --ostype=desktop --pkgmngr=apt-deb')
            # end l3
            elif (args.level == "l1l2"):
                if (args.ostype == "desktop"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=desktop --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=desktop --pkgmngr=yum-rpm')
                    else: # desktop default use apt-deb
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=desktop --pkgmngr=apt-deb')
                elif (args.ostype == "server"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=server --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=server --pkgmngr=yum-rpm')
                    else: # server default use yum-rpm
                        os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=server --pkgmngr=yum-rpm')
                else: # default desktop with apt-deb
                    os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2 --ostype=desktop --pkgmngr=apt-deb')
            # end "level l1l2"
            elif (args.level == "l1l2l3"):
                if (args.ostype == "desktop"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1l2l3 --ostype=desktop --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1l2l3 --ostype=desktop --pkgmngr=yum-rpm')
                    else: # desktop default use apt-deb
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1l2l3 --ostype=desktop --pkgmngr=apt-deb')
                elif (args.ostype == "server"):
                    if (args.pkgmngr == "apt-deb"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1l2l3 --ostype=server --pkgmngr=apt-deb')
                    elif (args.pkgmngr == "yum-rpm"):
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1l2l3 --ostype=server --pkgmngr=yum-rpm')
                    else: # server default use yum-rpm
                        os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1l2l3 --ostype=server --pkgmngr=yum-rpm')
                else: # default desktop with apt-deb
                    os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1l2l3 --ostype=desktop --pkgmngr=apt-deb')
            # end l1l2l3
            else:
                # os.system('python3 LibChecker/lib_checker.py --strategy=base')
                os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1l2 --ostype=desktop --pkgmngr=apt-deb')
        else:
            # os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1l2') 
            os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1l2 --ostype=desktop --pkgmngr=apt-deb') # default --strategy=base --levle=l1l2 --ostype=desktop --pkgmngr=apt-deb

        # For LibChecker:
        # import libcheck: input (json-file) (formated-json)

    elif (args.channel == "cmdchecker"):
        print("进入 CmdChecker 处理程序 . . .")

        os.system('python3 CmdChecker/cmd_checker.py')

        # For CmdChecker
        # import cmdcheck: input (json-file) (formated-json)

    elif (args.channel == "fschecker"):
        print("进入 FsChecker 处理程序 . . .")

        os.system('python3 FsChecker/fs_checker.py')
        
        # For FsChecker
        # import fscheck: input (json-file) (formated-json)

    elif (args.channel == "servicechecker"):
        print("进入 ServiceChecker 处理程序 . . .")

        os.system('python3 ServiceChecker/service_checker.py')

        # For CmdChecker
        # import cmdcheck: input (json-file) (formated-json)


    else:
        print("Invalid Options, please input --channel=[cmdchecker|fschecker|libchecker]")


# 3. Generate Output
#def generate_json_file():
#    print("This Label is generatejson ")
#    print('Label:', generate_json_file.__name__)

#def convert_json_to_txt():

#def convert_json_to_pdf():



# 4. Draw Graphics
def draw_main_gui():
    top = tkinter.Tk()
    top.mainloop()


# Main entry point
if __name__ == '__main__':
    try:
        input_valid_check()
        checker_call_handler()
#        generate_json_file()
#        draw_main_gui()
    except Exception as e:
        print(e)


