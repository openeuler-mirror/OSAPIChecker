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
parser.add_argument('-p', '--strategy', action='store', type=str, help='Choice OSAPIChecker strategy: base,onyl-expand,with-expand', default="base")

# --level:
#       l1
#       l2
#       l3
#       l1l2 (default)
#       l1l2l3
parser.add_argument('-l', '--level', action='store', type=str, help='Choice OSAPIChecker level: l1,l2,l3,l1l2,l1l2l3', default="l1l2")

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
def checker_call_handler():
    if (args.channel == "libchecker"):
        print("进入 LibChecker 处理程序 . . .")
        if (args.strategy == "with-expand"):
            if (args.level == "l1"):
                os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1')
            elif (args.level == "l2"):
                os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l2')
            elif (args.level == "l3"):
                os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l3')
            elif (args.level == "l1l2l3"):
                os.system('python3 LibChecker/lib_checker.py --strategy=with-expand --level=l1l2l3')
            else:
                os.system('python3 LibChecker/lib_checker.py --strategy=with-expand')
        elif (args.strategy == "base"):
            if (args.level == "l1"):
                os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1')
            elif (args.level == "l2"):
                os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l2')
            elif (args.level == "l3"):
                os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l3')
            elif (args.level == "l1l2l3"):
                os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1l2l3')
            else:
                os.system('python3 LibChecker/lib_checker.py --strategy=base')
        else:
            os.system('python3 LibChecker/lib_checker.py --strategy=base --level=l1l2') # defaulr --strategy=base --levle=l1l2

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


