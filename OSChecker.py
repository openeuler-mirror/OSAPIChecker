#!/usr/bin/python3

import argparse
import os
import sys
import logging


#import tkinter

# import libchecker # Import LibChecker module
# import cmdchecker # Import CmdChecker module
# import fschecker  # Import FsChecker  module

# 0. Global Init
parser = argparse.ArgumentParser(description="This Progermm is a OSChecker", prog="OSChecker")
parser.add_argument('-c', '--channel', action='store', type=str, help='Choice OSChecker channels: libchecker,cmdchecker,fschecker', default="all")
#parser.add_argument('-j', '--json', action='store', type=str, help='Choice OSChecker Json templete file', required=True)
#parser.add_argument('-j', '--json', action='store', type=str, help='Choice OSChecker Json templete file', required=True)
args = parser.parse_args()


# 1. Input Valid Check
def input_valid_check():

    print("|************************ 操作系统软件兼容性应用编程接口检查工具 ************************|")
#    print('the options is', options)

    # Options check

    # Json check


# 2. Call Subchecker's Handler
def checker_call_handler():
    if (args.channel == "all"):
        print("---> This is Default-ALL handler")

        # Whell-All

    elif (args.channel == "libchecker"):
        print("进入 LibChecker 处理程序 . . .")

        os.system('python3 LibChecker/lib_checker.py')

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

    else:
        print("Invalid Options")


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


