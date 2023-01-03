#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author   : Wang Jinlong
# @Time     : 2022/11/09 16:00
# @File     : Alpha OSAPIChecker Tools Source Code

import argparse
import json
import os
import platform
import sys
import time

# -1. Inherit arguments from CUI
# there are some arguments match with main program 
    ## --strategy: 
    ## --level:
    ## --ostype:
    ## --pkgmngr:
    ## --json:
parser = argparse.ArgumentParser(description="This Progermm is a OSChecker", prog="OSChecker")
parser.add_argument('-s', '--strategy', action='store', type=str, help='Choice OSAPIChecker strategy: base,only-expand,with-expand', default="base")
parser.add_argument('-l', '--level', action='store', type=str, help='Choice OSAPIChecker level: l1,l2,l3,l1l2,l1l2l3', default="l1l2")
parser.add_argument('-t', '--ostype', action='store', type=str, help='OSType of current OS: desktop, server, embed，other', default="desktop")
parser.add_argument('-p', '--pkgmngr', action='store', type=str, help='Package Manager of current OS: apt-deb, yum-rpm, src-bin, other', default="apt-deb")
parser.add_argument('-j', '--json', action='store', type=str, help='Choice OSChecker Json templete file', required=False) # this line use for dect the json file.
args = parser.parse_args() # write arguments to struct

g_inputstrategy = args.strategy
g_inputlevel = args.level
g_inputostype = args.ostype
g_inputpkgmngr = args.pkgmngr
g_inputjson = args.json


# option module import
if (g_inputpkgmngr == "apt-deb"):
    import apt_pkg # import for apt-deb package management tools


# for logger handler
class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

    # print("Beginning check at [",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"")
sys.stdout = Logger("Logs/libchecker-tmp.log", sys.stdout)
#sys.stderr = Logger("Logs/a.log_file", sys.stderr)

# 0. Global Resources Initialized
## 0.1 init dict and list data structures
g_pkginfodict_from_json = {}    # read pkacage info from json file
g_libinfodict_from_json = {}    # read library info from json file
g_bind_pkglib_from_json = {}    # bing package and library info
g_liblist_from_json = {}        # bing package and library info
g_pkginfodict_from_os = {}      # dict buffer for package info from current os
g_libinfodict_from_os = {}      # dict buffer for library info from current os
g_liblist_from_os = {}          # dict buffer for library info from current os
g_libchecker_comp_status = {}   # dict for libchecker compare result
g_jsonfile_dict = {}            # a josn file struct
g_pkgstd_dict = {}              # a dict store json node mata-date
g_counter_flags = {}            # a conuter struct 
g_storejsondict = {}
g_pkgversiodict = {}
g_lib_location_path = " "
g_notfind_set_flag = 0          # bool flag for find source package status
g_chapter_dict = {}
g_genresults_to_json = {}
g_subresults_to_json = {}
g_pkgflag_dict = {}
g_ostype = "desktop"            # global magic string for OS type
g_pkgmgr = "apt-deb"            # global magic string for OS type
g_test_dict = {}
g_test_list = []

## 0.2 a recycle call function for user
def libchecker_over_jobs():
    time_now = time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())
    log_file_name = "Logs/libchecker-" + time_now + ".log"
    # os.system("cp Logs/libchecker-tmp.log Outputs/libchecker-output.txt")
    os.rename("Logs/libchecker-tmp.log", log_file_name)
## 0.3 platform info
def get_env_info():
    print("系统信息:")
    str1 = os.popen("cat /etc/os-release").read()
    str2 = str1.split("\n")
    for s1 in str2:
        print("\t", s1)

def get_platform_info():
    # global g_inputstrategy = args.strategy
    # global g_inputlevel = args.level
    # global g_inputostype = args.ostype
    # global g_inputpkgmngr = args.pkgmngr
    global g_ostype
    print("开始 LibChecker 检查")
    # p_platform_info = os.popen('uname -a')
    # print(p_platform_info)
    # p_platform_info.close()

    print("\t系统平台信息:")
    # print("\t\t 名称:",os.name)
    print("\t\t 系统:",platform.system())
    print("\t\t 架构:",platform.architecture())
    print("\t\t 机器:",platform.machine())
    print("\t\t 版本:",platform.release())

    # if "desktop" in platform.release():
        # g_ostype = "desktop"
    # else:
        # g_ostype = "server"
    g_ostype = g_inputostype
    # print(g_ostype)

def get_stdjsons_info(json_file_path):
    with open(json_file_path) as f:
        f_dict = json.load(f)

    global g_jsonfile_dict
    g_jsonfile_dict = f_dict
    lib_basedict = f_dict['libs']['category']['base']['packages']

    # print(type(f_dict.keys()))
    # print(f_dict)
    print("标准信息:")
    print("\t标准简要信息:")
    print("\t\t标准号: %s" % f_dict['std_description']['std_number'])
    print("\t\t文件名: %s" % f_dict['std_description']['std_name'])
    print("\t库检查器信息:")
    print("\t\t检查位置: %s" % f_dict['libs']['lib_location'])

    # print("Start Checking: .....: Chapter: %s Category: %s;" %(f_dict['libs']['category']['base']['description']['chapters_number'], f_dict['libs']['category']['base']['description']['chapters_Name']))

def libchecker_environment_init():
    # print("Enter function: libchecker_environment_init")
    global g_counter_flags
    # g_inputstrategy = args.strategy
    # g_inputlevel = args.level
    # g_inputostype = args.ostype
    # g_inputpkgmngr = args.pkgmngr
    
    # g_counter_flags = {'pkg_counter': {'total': 0, 'passed': 0, 'warning': 0, 'failed': 0, 'l1': 0, 'l2': 0, 'l3':0}, 'lib_counter': {'total': 0, 'passed': 0, 'warning': 0, 'failed': 0}}
    g_counter_flags = {'pkg_counter': {'total': {'all' : 0, 'l1' : 0, 'l2' : 0, 'l3' : 0} , 'passed': {'all': 0, 'l1' : 0, 'l2' : 0, 'l3' : 0}, 'warning': {'all': 0, 'l1' : 0, 'l2' : 0, 'l3' : 0}, 'failed': {'all' : 0, 'l1' : 0, 'l2' : 0, 'l3' : 0} }, 'lib_counter': {'total': 0, 'passed': 0, 'warning': 0, 'failed': 0}}

    #get_platform_info()

    get_env_info()

    # get_stdjsons_info('../Jsons/lib_list_1.0I-20220914-uos.json')
    # get_stdjsons_info('Jsons/lib_list_1.0I-20220914-uos.json')
    get_stdjsons_info('Jsons/lib_list.json')
    
    if (g_inputpkgmngr == "apt-deb"):
        apt_pkg.init_system()

    # gen_mainscrn_init()

def check_per_pkg_info(src_pkgname):
    global g_notfind_set_flag
    global g_genresults_to_json
    global g_test_dict 

    # p_srcpkgnam = os.popen('apt-cache showsrc %s | grep Package | cut -d '"\ "' -f 2 ' %(src_pkgname))
    # srcpkgnam = p_srcpkgnam.read().rstrip('\n')
    # p_srcpkgnam.close()

    if(g_inputostype == "desktop"):
        if (g_inputpkgmngr == "apt-deb"):
            p_srcpkgver = os.popen('apt-cache showsrc %s 2>/dev/null | grep \^Version | cut -d '"\ "' -f 2 ' %(src_pkgname))
        elif (g_inputpkgmngr == "yum-rpm"):
            p_srcpkgver = os.popen('yum list %s | awk \'{print $2}\' | sed -n \'3p\'  ' %(src_pkgname))
    elif(g_inputostype == "server"):
        if (g_inputpkgmngr == "apt-deb"):
            p_srcpkgver = os.popen('apt-cache showsrc %s 2>/dev/null | grep \^Version | cut -d '"\ "' -f 2 ' %(src_pkgname))
        elif (g_inputpkgmngr == "yum-rpm"):
            p_srcpkgver = os.popen('yum list %s | awk \'{print $2}\' | sed -n \'3p\'  ' %(src_pkgname))
    else:
        print("Please input --ostype=[desktop,server,embde,...] and --pkgmngr=[apt-deb,yum-rpm,src-bin,...]")

    # yum list gcc | awk '{print $2}' | sed -n '3p'

    srcpkgver = p_srcpkgver.read().rstrip('\n')
    p_srcpkgver.close()

    global g_counter_flags

    g_counter_flags['pkg_counter']['total']['all'] += 1

    print("\t\t系统实现: ")
    # print(g_pkgversiodict)

    if (len(srcpkgver) == 0):
        print("\t\t\t\t没有发现")
        # print("\t\t共享库信息:")
        g_notfind_set_flag = 1
    else:
        print("\t\t\t\t实现包名 -> ", src_pkgname.ljust(20),"实现版本 -> ",srcpkgver)

        # if(len(srcpkgver.split(':')) > 1):
        #       print("\t\t状态信息: L1L2 报错置位！", compare_version_serial_number(srcpkgver.split(':')[1], g_pkgversiodict[src_pkgname]))
        # else:
        #       print("\t\t状态信息: L1L2 报错置位！", compare_version_serial_number(srcpkgver, g_pkgversiodict[src_pkgname]))
#    vc = apt_pkg.version_compare(a,b)

 #       if(srcpkgver > g_pkgversiodict[src_pkgname]):
        if (apt_pkg.version_compare(srcpkgver,g_pkgversiodict[src_pkgname]) > 0):
            print("\t\t状态信息: ")
            print("\t\t\t\t兼容")
        else:
            if (apt_pkg.version_compare(srcpkgver,g_pkgversiodict[src_pkgname]) == 0):
                print("\t\t状态信息: ")
                print("\t\t\t\t兼容")
            else:
                print("\t\t状态信息: ")
                print("\t\t\t\t不兼容")
                g_counter_flags['pkg_counter']['warning']['all'] += 1

        print("\t\t共享库信息:")

        g_counter_flags['pkg_counter']['passed']['all'] += 1    

        # print("\t\tsections_number -->", g_jsonfile_dict[src_pkgname]['sections_number'])
        # print(l_tmp_dict[key]['alias'][0]['name'])
        # print(g_jsonfile_dict['libs']['category']['base']['packages'].keys())

        # for list_item in g_jsonfile_dict['libs']['category']['base']['packages'][src_pkgname]['share_objs']['desktop']
        # print("\t\t\t\tlib_soname -> ", list_item,";  " "location -> ",check_sharelib_info('/lib', list_item))

def check_pkginfo_for_desktop(src_pkgname):
    for src_pkgname in g_jsonfile_dict:
        check_per_pkg_info(g_jsonfile_dict['libs']['category']['base']['packages'][src_pkgname]['alias'][0]['name'])

        # print(g_jsonfile_dict['libs']['category']['base']['packages'][src_pkgname]['alias'][0]['name'])
        # print(g_jsonfile_dict['libs']['category']['base']['packages'].keys())
        # print(g_jsonfile_dict[src_pkgname]['libs']['alias'][0]['name'])
        # print(g_jsonfile_dict[src_pkgname])
        # print(type(g_jsonfile_dict['libs'][src_pkgname]))
        # print(g_jsonfile_dict['libs']['category']['base']['packages']['glibc']['alias'][0]['name'])
        # print(src_pkgname)
        # print(type(src_pkgname))


def check_sharelib_info(lib_soname):

    global g_lib_location_path
    global g_counter_flags
    g_lib_location_path = "0"

    global g_counter_flags
    g_counter_flags['lib_counter']['total'] += 1
    l_list = ["/lib", "/lib64", "/usr/lib"]

    for path_tmp in l_list:
        for realpath, dirs, files in os.walk(path_tmp):
            if lib_soname in files:
                full_path = os.path.join(path_tmp, realpath, lib_soname)
                g_lib_location_path = (os.path.normpath(os.path.abspath(full_path)))
        if g_lib_location_path != "0":
            break
        
    if g_lib_location_path == "0":
        return "not found"
    else:
        return g_lib_location_path

# def libchecker_checking_loop():
def libchecker_checking_loop():
    global g_notfind_set_flag 
    global g_chapter_dict
    global g_genresults_to_json
    global g_subresults_to_json
    global g_storejsondict
    global g_test_list
    global g_test_dict
    global g_pkgflag_dict

    l_dict_to_json = {}
    l_pkgresult_to_json = {}

    del g_jsonfile_dict['libs']['category']['##章节名']
    print("")
    print("开始检查： ",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"")
    for chapter_class in g_jsonfile_dict['libs']['category']:
        if chapter_class == 'base':
            l_tmp_dict = g_jsonfile_dict['libs']['category']['base']['packages']
            del l_tmp_dict['##glibc']
        else:
            l_tmp_dict = g_jsonfile_dict['libs']['category'][chapter_class]['packages']
        for key in l_tmp_dict:
            g_chapter_dict.update({ key: l_tmp_dict[key]['sections_number']})
            if (args.level == "l1"):
                if (l_tmp_dict[key]['necessity'][g_ostype]['level'] == "L1"):
                    g_storejsondict[key] = l_tmp_dict[key]
            elif (args.level == "l2"):
                if (l_tmp_dict[key]['necessity'][g_ostype]['level'] == "L2"):
                    g_storejsondict[key] = l_tmp_dict[key]
            elif (args.level == "l3"):
                if (l_tmp_dict[key]['necessity'][g_ostype]['level'] == "L3"):
                    g_storejsondict[key] = l_tmp_dict[key]
            elif (args.level == "l1l2"):
                g_storejsondict[key] = l_tmp_dict[key]
                if (l_tmp_dict[key]['necessity'][g_ostype]['level'] == "L3"):
                    g_storejsondict.pop(key)
                elif (l_tmp_dict[key]['necessity'][g_ostype]['level'] == "L0"):
                    g_storejsondict.pop(key)
            elif (args.level == "l1l3"):
                g_storejsondict[key] = l_tmp_dict[key]
                if (l_tmp_dict[key]['necessity'][g_ostype]['level'] == "L2"):
                    g_storejsondict.pop(key) 
                elif (l_tmp_dict[key]['necessity'][g_ostype]['level'] == "L0"):
                    g_storejsondict.pop(key)
            elif (args.level == "l2l3"):
                g_storejsondict[key] = l_tmp_dict[key]
                if (l_tmp_dict[key]['necessity'][g_ostype]['level'] == "L1"):
                    g_storejsondict.pop(key) 
                elif (l_tmp_dict[key]['necessity'][g_ostype]['level'] == "L0"):
                    g_storejsondict.pop(key)
            elif (args.level == "l1l2l3"):
                g_storejsondict = l_tmp_dict
            else:
                g_storejsondict[key] = l_tmp_dict[key]
                if (l_tmp_dict[key]['necessity'][g_ostype]['level'] == "L3"):
                    g_storejsondict.pop(key)
                elif (l_tmp_dict[key]['necessity'][g_ostype]['level'] == "L0"):
                    g_storejsondict.pop(key)
                print("[Warnning]: Invalid input options, execute use default options \"--strate=base --levle=l1l2\"")

    for key4 in g_storejsondict:
        g_test_dict.update({key4 : "wwww"})
        l_dict_to_json={'Level': 'gen', 'Shared library':'gen', 'Required version': 'gen', 'Binary package':'gen'}
        g_genresults_to_json.update({ key4 : l_dict_to_json })
        
    with open("Outputs/libchecker-output.json","w") as f:
        json.dump(g_genresults_to_json,f)

    for last_key in g_storejsondict:
        l_pkgresult_to_json.clear()

        if (g_storejsondict[last_key]['necessity'][g_ostype]['level'] == "L1"):
            g_counter_flags['pkg_counter']['total']['l1'] += 1
        if (g_storejsondict[last_key]['necessity'][g_ostype]['level'] == "L2"):
            g_counter_flags['pkg_counter']['total']['l2'] += 1
        if (g_storejsondict[last_key]['necessity'][g_ostype]['level'] == "L3"):
            g_counter_flags['pkg_counter']['total']['l3'] += 1
        print("\t正在检查 ", '<',last_key,'>', "...")
        print("\t\t标准约定:")
        print("\t\t\t\t从属章节 -> ", g_chapter_dict[last_key].ljust(20), "兼容级别 -> ", g_storejsondict[last_key]['necessity'][g_ostype]['level'].ljust(20))
        print("\t\t\t\t标准包名 -> " ,last_key.ljust(20),"标准版本 -> ", g_storejsondict[last_key]['version'][g_ostype].ljust(20))
        g_pkgversiodict[g_storejsondict[last_key]['lib_name']] = g_storejsondict[last_key]['version'][g_ostype]
        if (len(g_storejsondict[last_key]['version'][g_ostype]) == 0):
            print("\t\t系统实现:")
            print("\t\t\t\t没有发现")
        else:
            check_per_pkg_info(g_storejsondict[last_key]['lib_name'])
            g_subresults_to_json.clear()
            if (g_notfind_set_flag == 1 ):
                g_counter_flags['pkg_counter']['failed']['all'] += 1
                g_notfind_set_flag = 0
            else:
                for list1_item in g_storejsondict[last_key]['share_objs'][g_ostype]:
                    print("\t\t\t\t名称 -> ",list1_item)
                    print("\t\t\t\t\t标准约定 -> ",list1_item, )
                    lib_result = check_sharelib_info(list1_item)
                    print("\t\t\t\t\t系统存在 -> ",lib_result, )
                    temp_libsoname = lib_result.split('/')[-1]
                    if (lib_result == "not found"):
                        print("\t\t\t\t\t检测结果 ->  未检测到存在")
                        g_subresults_to_json[list1_item] = "not found","-"
                        g_counter_flags['lib_counter']['failed'] += 1
                    else:
                        print("\t\t\t\t\t检测结果 -> ", compare_library_version(temp_libsoname, str(list1_item)))
                        if (compare_library_version(temp_libsoname, str(list1_item)) == "equal" ):
                            g_counter_flags['lib_counter']['passed'] += 1
                            g_subresults_to_json[list1_item] = "compatible",g_lib_location_path
                        elif (compare_library_version(temp_libsoname, str(list1_item)) == "smaller" ):
                            g_counter_flags['lib_counter']['failed'] += 1
                            g_subresults_to_json[list1_item] = "incompatible"
                        else:
                            g_counter_flags['lib_counter']['warning'] += 1
                            g_subresults_to_json[list1_item] = "compatible bigger"

        #Traverse the binary package of the source package
        if (g_inputpkgmngr == "yum-rpm"):
            binary_list = get_rpmpkg_from_srcpkg(last_key)
        else:
            binary_list = get_debpkg_from_srcpkg(last_key)

        for binary_name in binary_list:
            if (g_inputpkgmngr == "yum-rpm"):
                pkg_install_status = os.system('rpm -qi %s' %(binary_name))
                if (pkg_install_status == 0):
                    ver_required = g_storejsondict[last_key]['version'][g_inputostype] #获取要求的库包版本
                    ver_local = os.popen('rpm -qi %s | grep "Version\|Release" | awk -F" " \'{print $3}\' | sed \':label;N;s/\\n/-/;t label\'' %(binary_name)).read().rstrip('\n') #获取本地库包版本
                    if (get_rpmpkg_ver_contrast(ver_local, ver_required) == "compatible"):
                        l_pkgresult_to_json[binary_name] = "compatible", ver_local
                    elif (get_rpmpkg_ver_contrast(ver_local, ver_required) == "incompatible"):
                        l_pkgresult_to_json[binary_name] = "incompatible", ver_local
            else:
                pkg_install_status = os.popen('dpkg -l %s 2>/dev/null| grep %s 2>/dev/null | gawk -F" " \'{print $1}\' | head -n 1' %(str(binary_name), str(binary_name))).read().rstrip('\n')
                if (pkg_install_status == "ii"):
                    ver_required = g_storejsondict[last_key]['version'][g_inputostype] #获取要求的库包版本
                    ver_local = os.popen('dpkg -l %s 2>/dev/null| grep %s 2>/dev/null | gawk -F" " \'{print $3}\' | head -n 1' %(binary_name, binary_name)).read().rstrip('\n') #获取本地库包版本
                    if (get_debpkg_ver_contrast(ver_local, ver_required) == "compatible"):
                        l_pkgresult_to_json[binary_name] = "compatible", ver_local
                    elif (get_debpkg_ver_contrast(ver_local, ver_required) == "incompatible"):
                        l_pkgresult_to_json[binary_name] = "incompatible", ver_local
                else:
                    continue

        #向json文件写入库包级别
        with open("Outputs/libchecker-output.json", 'r') as fr:
            json_level = json.load(fr)
            json_level[last_key]['Level'] = g_storejsondict[last_key]['necessity'][g_inputostype]['level']
        with open("Outputs/libchecker-output.json", 'w+') as fw:
            json.dump(json_level,fw,ensure_ascii=False,indent=4)
        #向json文件写入库包需求版本
        with open("Outputs/libchecker-output.json", 'r') as fr:
            json_required_ver = json.load(fr)
            json_required_ver[last_key]['Required version'] = g_storejsondict[last_key]['version'][g_inputostype]
        with open("Outputs/libchecker-output.json", 'w+') as fw:
            json.dump(json_required_ver,fw,ensure_ascii=False,indent=4)
        #向json文件写入共享库兼容信息
        with open("Outputs/libchecker-output.json", 'r') as fr:
            json_so = json.load(fr)
            json_so[last_key]['Shared library'] = g_subresults_to_json
        with open("Outputs/libchecker-output.json", 'w+') as fw:
            json.dump(json_so,fw,ensure_ascii=False,indent=4)
        #向json文件写入库包本地版本
        with open("Outputs/libchecker-output.json", 'r') as fr:
            json_local_ver = json.load(fr)
            json_local_ver[last_key]['Binary package'] = l_pkgresult_to_json
        with open("Outputs/libchecker-output.json", 'w+') as fw:
            json.dump(json_local_ver,fw,ensure_ascii=False,indent=4)


    print("=============================================================================================================")
    print("结束检查 ",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    print("")
    print("\t检查策略：", "\"",  "--strategy =",args.strategy, "--level =",args.level, "--ostype =", args.ostype, "--pkgmngr =", args.pkgmngr, "\"")
    print("")
    print("\t软件包:")
    print("\t\t总计:", g_counter_flags['pkg_counter']['total']['all'], "{" ,"l1->",g_counter_flags['pkg_counter']['total']['l1'],";", "l2->", g_counter_flags['pkg_counter']['total']['l2'], ";", "l3->", g_counter_flags['pkg_counter']['total']['l3'],  "}")
    print("\t\t通过:", g_counter_flags['pkg_counter']['passed']['all'])
    print("\t\t警告:", g_counter_flags['pkg_counter']['warning']['all'])
    print("\t\t报错:", g_counter_flags['pkg_counter']['failed']['all'])
    # print("\t\tL1:", g_counter_flags['pkg_counter']['total']['l1'], "|警告：", g_counter_flags['pkg_counter']['warning']['l1'], "| 报错：", g_counter_flags['pkg_counter']['failed']['l1'])
    # print("\t\tL2:", g_counter_flags['pkg_counter']['total']['l2'], "|警告：", g_counter_flags['pkg_counter']['warning']['l2'], "| 报错：", g_counter_flags['pkg_counter']['failed']['l2'])
    # print("\t\tL3:", g_counter_flags['pkg_counter']['total']['l3'], "|警告：", g_counter_flags['pkg_counter']['warning']['l3'], "| 报错：", g_counter_flags['pkg_counter']['failed']['l3'])
    print("\t动态库:")
    # print("\t\t\ttotal:", g_counter_flags['lib_counter']['total'], "|  passed:", g_counter_flags['lib_counter']['passed'])
    print("\t\t总计:", g_counter_flags['lib_counter']['total'])
    print("\t\t通过:", g_counter_flags['lib_counter']['passed'])
    print("\t\t警告:", g_counter_flags['lib_counter']['warning'])
    print("\t\t报错:", g_counter_flags['lib_counter']['failed'])
    print("=============================================================================================================")

def get_debpkg_ver_contrast(ver_local, ver_required):
    # --compare-version ver_local op ver_required
    # op: lt le eq ne ge gt
    # sn:  < <= == != >= > 
    compare_result = os.system('dpkg --compare-versions %s ge %s' %(str(ver_local), str(ver_required)))
    if(compare_result == 0):
        return "compatible"
    else:
        return "incompatible"

def get_rpmpkg_ver_contrast(ver_local, ver_required):
    # compare ver_local op ver_required
    if ver_local < ver_required:
        return "incompatible"
    else:
        return "compatible"

def read_pkginfo_from_stdjson(json_file_path):
    # this function read package info from json file
    # input: 
    #           @ json_file_path
    # output:
    #           @ g_pkginfodict_from_json
    # return:
    #           @ pkginfo_dict
    print("Enter function: read_pkginfo_from_json(%s)" %(json_file_path))
    
    with open(json_file_path) as f:
        f_dict = json.load(f)

    lib_basedict = f_dict['libs']['category']['base']['packages']
#    lib_basedict = f_dict['libs']['category']['security']['packages']
#    lib_basedict = f_dict['libs']['category']['network']['packages']
#    lib_basedict = f_dict['libs']['category']['graphic']['packages']
#    lib_basedict = f_dict['libs']['category']['multimedia']['packages']
#    lib_basedict = f_dict['libs']['category']['print_scan']['packages']
#    lib_basedict = f_dict['libs']['category']['runtime_language']['packages']
#    lib_basedict = f_dict['libs']['category']['development']['packages']
#    lib_basedict = f_dict['libs']['category']['basic_calculation']['packages']
#    lib_basedict = f_dict['libs']['category']['storage']['packages']
#    lib_basedict = f_dict['libs']['category']['virtualization']['packages']
#    lib_basedict = f_dict['libs']['category']['high_availability']['packages']

    del lib_basedict['##glibc']

    temp_dict = {}

    for i in lib_basedict:
        l1 = lib_basedict[i]['alias']
        for i in range(len(l1)):
            temp_dict[l1[0]['name']] = l1[0]['version']['desktop']
    
    return temp_dict

## 2.1 read packages info from json file
def read_libinfo_from_stdjson(json_file_path):
    # this function read package info from json file
    # input: 
    #           @ json_file_path
    # output:
    #           @ g_pkginfodict_from_json
    # return:
    #           @ pkginfo_dict
    print("Enter function: read_pkginfo_from_json(%s)" %(json_file_path))
    
    with open(json_file_path) as f:
        f_dict = json.load(f)

    lib_basedict = f_dict['libs']['category']['base']['packages']
    # lib_basedict = f_dict['libs']['category']['security']['packages']
    # lib_basedict = f_dict['libs']['category']['network']['packages']
    # lib_basedict = f_dict['libs']['category']['graphic']['packages']
    # lib_basedict = f_dict['libs']['category']['multimedia']['packages']
    # lib_basedict = f_dict['libs']['category']['print_scan']['packages']
    # lib_basedict = f_dict['libs']['category']['runtime_language']['packages']
    # lib_basedict = f_dict['libs']['category']['development']['packages']
    # lib_basedict = f_dict['libs']['category']['basic_calculation']['packages']
    # lib_basedict = f_dict['libs']['category']['storage']['packages']
    # lib_basedict = f_dict['libs']['category']['virtualization']['packages']
    # lib_basedict = f_dict['libs']['category']['high_availability']['packages']

    del lib_basedict['##glibc']

    temp_dict = {}

    for i in lib_basedict:
        l1 = lib_basedict[i]['alias']
        d1 = lib_basedict[i]['share_objs']
        for i in range(len(l1)):
            temp_dict[l1[0]['name']] = d1['desktop']

    return temp_dict

def get_liblists_from_stdjson(json_file_path):
    print("Enter function: get_liblists_from_stdjson(%s)" %(json_file_path))
   
    global g_liblist_from_json 
    chapter_class = ['base', 'security', 'network', 'graphic', 'multimedia', 'print_scan', 'runtime_language', 'development', 'basic_calculation', 'storage', 'virtualization', 'high_availability']

    with open(json_file_path) as f:
        f_dict = json.load(f)

    temp_dict = {}  # Store dict={packages:sonames}
    temp_list = []  # Store list=[soanmes]
    for i in chapter_class:
        lib_basedict = f_dict['libs']['category'][i]['packages']
        if i == 'base':
            del lib_basedict['##glibc']
            for i in lib_basedict:
                l1 = lib_basedict[i]['alias']
                d1 = lib_basedict[i]['share_objs']
                for i in range(len(l1)):
                    temp_dict[l1[0]['name']] = d1['desktop']
        
    for key in temp_dict:
        temp_list.extend(temp_dict[key])

    g_liblist_from_json = temp_list

    return temp_list
        



## 2.2 read libraries info from json file
def read_libinfo_from_json(json_file_path):
    # this function read library info from json file
    # input: 
    #           @ json_file_path
    # output:
    #           @ g_libinfodict_from_json
    # return:
    #           @ libinfo_dict
    print("Enter function: read_libinfo_from_json(%s)" %(json_file_path))
    fobj = open(json_file_path)

    file_data = json.load(fobj)

    libinfo_dict = {}

    for i in file_data['libraries']:
        libinfo_dict[i['linkname']] = i['soname']

    fobj.close()

    return libinfo_dict

## 2.3 read metadata info from json file
def libchecker_read_stdjson(json_file_path):
    print("Enter function: libchecker_read_stdjson_file(%s)" %(json_file_path))

    global g_pkginfodict_from_json
    global g_libinfodict_from_json

    g_pkginfodict_from_json = read_pkginfo_from_stdjson(json_file_path)
    g_libinfodict_from_json = read_libinfo_from_stdjson(json_file_path)

#    print(g_pkginfodict_from_json)
#    print(g_libinfodict_from_json)

## 2.3 read metadata info from json file
def libchecker_read_std_json(json_file_path):
    print("Enter function: libchecker_open_std_json(%s)" %(json_file_path))
    fobj = open(json_file_path)

    file_data = json.load(fobj)
    objs_dict = {}


    for i in file_data['libs']['base']:
        print(i)
        print(type(file_data['libs']['base'][i]))
        #print(file_data['libs']['base'][i])
#        objs_dict = file_data['libs']['base'][i]
        objs_dict.update({ i : file_data['libs']['base'][i]})

#    print(objs_dict)
#    print(type(objs_dict))
#    print(len(objs_dict))
#    print(objs_dict.keys())

#    j = 'gcc'
#    print(objs_dict[j]['lib_name'])

    del objs_dict['##chapters_number']
    del objs_dict['chapters_number']
    del objs_dict['##glibc']


    for key in objs_dict:
        print(key)

        #g_pkginfodict_from_json[key['lib_name']] = key['version']    # write pkginfo to dict: g_pkginfodict_from_json
        aliasname = objs_dict[key]['aliasname']
        g_pkginfodict_from_json.update({ aliasname : objs_dict[key]['version']['desktop_version']}) # src package name : pkg version
        
#        print(objs_dict[key]['aliasname'])
        g_bind_pkglib_from_json.update({ key : objs_dict[key]['desktop-share_objs']}) # src package name : library soname

    print(g_pkginfodict_from_json)
    print(g_bind_pkglib_from_json)

    for i in g_bind_pkglib_from_json:
        print(g_bind_pkglib_from_json[i])

    fobj.close()


#    print(f_dict['libs']['base']['glibc']['necessity'].keys())
#    print(f_dict["libchecker"][1])
#    print(f_dict["libchecker"][1]['name'])

# 3. Find Meatdate Info from Current OS
## 3.1 get src package info
def get_srcname_from_os():
    # this function for get src package name from current os
    # input: 
    #           @ 
    # output:
    #           @
    # return:
    #           @
    print("Enter function: get_srcname_from_os")

def get_srcver_form_srcname(src_pkgname):
    # this function for get src pacgake version from package name in current os
    # input: 
    #           @ src_pkgname
    # output:
    #           @ 
    # return:
    #           @ srcpkgver
    print("Enter function: get_srcver_from_srcname(%s)" %(src_pkgname))
    p_srcpkgver = os.popen('apt-cache showsrc %s 2>/dev/null| grep \^Version | cut -d '"\ "' -f 2 ' %(src_pkgname))
    srcpkgver = p_srcpkgver.read().rstrip('\n')
    p_srcpkgver.close()

    return srcpkgver

def get_pkginfo_from_srcpkg(src_pkgname):
    # this function for get src pacgake info from package name in current os
    # input: 
    #           @ src_pkgname
    # output:
    #           @ 
    # return:
    #           @ srcpkg_info_dict
    print("Enter function: get_pkginfo_from_srcpkg(%s)" %(src_pkgname))
    p_srcpkgnam = os.popen('apt-cache show %s 2>/dev/null | grep Package | cut -d '"\ "' -f 2 ' %(src_pkgname))
    srcpkgnam = p_srcpkgnam.read().rstrip('\n')
    p_srcpkgnam.close()
    p_srcpkgver = os.popen('apt-cache show %s 2>/dev/null | grep Version | cut -d '"\ "' -f 2 ' %(src_pkgname))
    srcpkgver = p_srcpkgver.read().rstrip('\n')
    p_srcpkgver.close()

    srcpkg_info_dict = {} 
    srcpkg_info_dict = {srcpkgnam : srcpkgver}

    return srcpkg_info_dict
    
def compare_version_serial_number(ver1, ver2):
    # this function compare two version serial number only for number
    # input: 
    #           @ ver1, string [x.x.x.x],[x]:[0-999999] 
    #           @ ver2, string [x.x.x.x],[x]:[0-999999]
    # output:
    #           @ 
    # return:
    #           @ ret:  string: >
    #           @ ret:  string: =
    #           @ ret:  string: <
    list1 = str(ver1).split(".")
    list2 = str(ver2).split(".")
    for i in range(len(list1)) if len(list1) < len(list2) else range(len(list2)):
        if int(list1[i]) == int(list2[i]):
            pass
        elif int(list1[i]) < int(list2[i]):
            return "<"
        else:
            return ">"
    if len(list1) == len(list2):
        return "="
    elif len(list1) < len(list2):
        return "<"
    else:
        return ">"

def compare_library_version(str1, str2):
    # this function compare soname for number
    # input: 
    #           @ str1 
    #           @ str2
    # output:
    #           @ 
    # return:
    #           @ ret:  string: >
    #           @ ret:  string: =
    #           @ ret:  string: <
#    list1 = str(str1).split(".")
#    list2 = str(str2).split(".")


    if str1 == str2:
        return "equal"
    elif str(str1) < str(str2):
        return "smaller"
    else:
        return "bigger"

## 3.2 get deb package info 
def get_debpkg_from_srcpkg(src_pkgname):
    # this function for get deb pacgakes from package name in current os
    # input: 
    #           @ src_pkgname
    # output:
    #           @ 
    # return:
    #           @ debpkgs
    p_debpkgs = os.popen('apt-cache showsrc %s 2>/dev/null | grep Binary | cut -d '"\:"' -f 2- | cut -d '"\ "' -f 2- ' %(src_pkgname))
    debpkgs = p_debpkgs.read().split("\n")[0].split(", ")
    p_debpkgs.close()

    return debpkgs
    
def get_rpmpkg_from_srcpkg(src_pkgname):
    # this function for get rpm pacgakes from package name in current os
    # input: 
    #           @ src_pkgname
    # output:
    #           @ 
    # return:
    #           @ debpkgs

    p_rpmpkgs = os.popen('dnf info | grep -B 5 -E "%s.*.src.rpm" | grep "名称" | awk -F" " \'{ print $3 }\' | sort -n | uniq | sed \':label;N;s/\\n/ /;t label\'' %(src_pkgname))
    debpkgs = p_rpmpkgs.read().split("\n")[0].split(" ")
    p_rpmpkgs.close()

    return debpkgs

## 3.3 get libraries info 
    ################################################################################
    # RealName                                                                     # 
    # realname = libname.so.x.y.z                                                  #
    # x: major version number                                                      #
    # y: minor version number                                                      #
    # z: release version number                                                    #
    #------------------------------------------------------------------------------#
    # SoName                                                                       #
    # soname = libname.so.x                                                        #
    # x: major version number                                                      #
    #------------------------------------------------------------------------------#
    # LinkName                                                                     #
    # link = name                                                                  #
    ################################################################################
### 3.3.1 get libraries realname from deb pakcgae
def get_realname_from_debpkg(deb_pkgname):
    # this function for get all library realname from one deb in current os
    # input: 
    #           @ deb_pkgname
    # output:
    #           @ 
    # return:
    #           @ realnames
    print("Enter function: get_realname_from_deb(%s)" %(deb_pkgname))
    p_realnames = os.popen('apt-file list %s | rev | cut -d / -f 1 | rev | grep -e "\.so$" -e ".so\."' %(deb_pkgname))
    realnames = p_realnames.read().split('\n')
    del realnames[len(realnames)-1]
    p_realnames.close()

    return realnames

def compare_realname_version(realname1, realname2):
    # this function compare library realname
    # input: 
    #           @ realname1
    #           @ realname2
    # output:
    #           @ 
    # return:
    #           @ 
    print("Enter function: compare_soname_version")

### 3.3.2 get libraries soname from deb package
def get_soname_from_debpkg(deb_pkgname):
    # this function for get all library soname from one deb in current os
    # input: 
    #           @ deb_pkgname
    # output:
    #           @ 
    # return:
    #           @ sonames
    print("Enter function: get_soname_from_deb(%s)" %(deb_pkgname))
    # p_sonames = os.popen('apt-file list %s |rev | grep .os | cut -d / -f 1 | rev | sort | grep .so.[0-999]$' %(deb_pkgname))
    p_sonames = os.popen('apt-file list %s |rev | grep .os | cut -d / -f 1 | rev | sort | grep -e .so.[0-999]$ -e .so$' %(deb_pkgname))
    sonames = p_sonames.read().split('\n')
    del sonames[len(sonames)-1]
    p_sonames.close()

    return sonames

def compare_soname_version(soname1, soname2):
    # this function compare library soname
    # input: 
    #           @ soname1
    #           @ soname2
    # output:
    #           @ 
    # return:
    #           @ 
    print("Enter function: compare_soname_version")

### 3.3.3 get libraries linkname from deb package
def get_linkname_from_debpkg(deb_pkgname):
    # this function for get all library linkname from one deb in current os
    # input: 
    #           @ deb_pkgname
    # output:
    #           @ 
    # return:
    #           @ linknames
    print("Enter function: get_linkname_from_deb(%s)" %(deb_pkgname))
    p_linknames = os.popen('apt-file list %s | rev | cut -d / -f 1 | rev | grep -e "\.so$"' %(deb_pkgname))
    linknames = p_linknames.read().split('\n')
    del linknames[len(linknames)-1]
    p_linknames.close()

    return linknames

def compare_linkname_version(linkname1, linkname2):
    # this function compare library linkname
    # input: 
    #           @ linkname1
    #           @ linkname2
    # output:
    #           @ 
    # return:
    #           @ 
    print("Enter function: compare_linkname_version")

def pick_linkname_from_soname(soname):
    # this function pick up linkname from soname
    # input: 
    #           @ soname
    # output:
    #           @ 
    # return:
    #           @ a linkname
    print("Enter function: pick_linkname_from_soname(%s)" %(soname))

    return (soname.split(".")[0] + ".so")

### 3.3.4 get libraries realname from src package
def get_realname_from_srcpkg(src_pkgname):
    print("Enter function: get_realname_from_srcpkg(%s)" %(src_pkgname))
    # this function for get all library realname from src pkgname in current os
    # input: 
    #           @ src_pkgname
    # output:
    #           @ 
    # return:
    #           @ realnames_list
    debpkgs_list = get_debpkg_from_srcpkg(src_pkgname)
    realnames_list_orig = [] 
    realnames_list = [] 
    for i in debpkgs_list:
        realnames_list_orig.extend(get_realname_from_debpkg(i))

    for i in realnames_list_orig:
        if i not in realnames_list:
            realnames_list.append(i)

    realnames_list.sort()

    return realnames_list

### 3.3.5 get libraries soname from src package
def get_soname_from_srcpkg(src_pkgname):
    # this function for get all library soname from src pkgname in current os
    # input: 
    #           @ src_pkgname
    # output:
    #           @ 
    # return:
    #           @ sonames_list
    print("Enter function: get_soname_from_srcpkg(%s)" %(src_pkgname))
    debpkgs_list = get_debpkg_from_srcpkg(src_pkgname)
    sonames_list_orig = [] 
    sonames_list = [] 
    for i in debpkgs_list:
        sonames_list_orig.extend(get_soname_from_debpkg(i))

    for i in sonames_list_orig:
        if i not in sonames_list:
            sonames_list.append(i)

    sonames_list.sort()

    return sonames_list

### 3.3.6 get libraries linkname from src package
def get_linkname_from_srcpkg(src_pkgname):
    # this function for get all library linkname from src pkgname in current os
    # input: 
    #           @ src_pkgname
    # output:
    #           @ 
    # return:
    #           @ linknames_list
    print("Enter function: get_soname_from_srcpkg(%s)" %(src_pkgname))
    debpkgs_list = get_debpkg_from_srcpkg(src_pkgname)
    linknames_list_orig = [] 
    linknames_list = [] 
    for i in debpkgs_list:
        linknames_list_orig.extend(get_linkname_from_debpkg(i))

    for i in linknames_list_orig:
        if i not in linknames_list:
            linknames_list.append(i)

    linknames_list.sort()
    
    return linknames_list

### 3.3.7 get package info from current os
def get_pkginfo_from_os():
    # this function for get pkackage info in current os by g_pkginfodict_from_json
    # input: 
    #           @ g_pkginfodict_from_json
    # output:
    #           @ 
    # return:
    #           @ g_pkginfodict_from_os
    print("Enter function: get_pkginfo_from_os")
    print(g_pkginfodict_from_json)
    for key in g_pkginfodict_from_json:
        g_pkginfodict_from_os[key] = get_srcver_form_srcname(key)

    return g_pkginfodict_from_os

### 3.3.8 get libraries info from current os (don't call this function !!!)
def get_libinfo_from_os():
    # this function for get library info in current os by g_libinfodict_from_json
    # input: 
    #           @ g_libinfodict_from_json
    # output:
    #           @ 
    # return:
    #           @ g_libinfodict_from_os
    print("Enter function: get_libinfo_from_os")
    liblists = []
    g_libchecker_comp_status = g_libinfodict_from_json
    
    for key in g_pkginfodict_from_json:
        lib_linkname_lists = get_linkname_from_srcpkg(key)
        lib_soname_lists = get_soname_from_srcpkg(key)
        for i in g_libinfodict_from_json.keys():
            if i in lib_linkname_lists:
                g_libinfodict_from_os[i] = max([s for s in lib_soname_lists if i in s])
    return g_libinfodict_from_os

#print(g_pkginfodict_from_json)
#print(g_libinfodict_from_json)
#print(g_bind_pkglib_from_json)

def get_liblists_from_os():
    print("Enter function: get_liblist_from_os")
    global g_liblist_from_os 
    temp_list = []

    for key in g_pkginfodict_from_json:
        temp_list.extend(get_soname_from_srcpkg(key))
   

    g_liblist_from_os = temp_list

    return temp_list


def get_libinfo_from_os_by_srcpkg():
    print("Start Test")
    print(g_libinfodict_from_json)
    for key in g_pkginfodict_from_json:
        g_libinfodict_from_os[key] = get_soname_from_srcpkg(key)

    global g_libchecker_comp_status

    l2 = []
    for key in g_libinfodict_from_json:
        l2.extend(g_libinfodict_from_json[key])

    for i in l2:
        g_libchecker_comp_status[i] = "flase"

    print(l2)
    print(g_libchecker_comp_status)

    print("Overring Test")
    return g_libinfodict_from_os


#g_pkginfodict_from_os = {}
#g_libinfodict_from_os = {}

#g_libchecker_comp_status = {}
#print(get_realname_from_srcpkg('ncurses'))
#print(get_soname_from_srcpkg('ncurses'))
#print(get_linkname_from_srcpkg('ncurses'))
#print(read_pkginfo_from_json('std-lib.json'))
#print(read_libinfo_from_json('std-lib.json'))
#print(read_pkginfo_from_json('std-lib.json'))

#get_libinfo_from_os()
#print(get_libinfo_from_os())

#pick_linkname_from_soname('ncurses')
#print(get_soname_from_srcpkg('ncurses'))
#print(pick_linkname_from_soname('ncurses.so.1.9'))
#print(compare_version_serial_number("1.4.3", "2.4.3"))
#libchecker_compare_metainfo()

# 4. Compare Package and Libraries Info
## 4.1 comapre packages between os and json-dict g_pkginfodict_from_json
def get_pkg_compare_info():

    # it always not equla, ex: lib1-1.0 vs lib1-1.0+deb10u1, so give up!
    # only compare shared library object files ***.so
    
    print("Enter function: get_pkg_compare_info()")

## 4.2 comapre librarie between os and json-dict g_libinfodict_from_json
def get_lib_compare_info():

    # only compare soname by linkname
    # only compare lib***.so.X, 'X' is a key value for compare,
    # because for linkname:libc6.so, soname:libc.so.6, realname:libc-2.28
    # implement by function: libchecker_compare_metainfo()

    print("Enter function: get_lib_compare_info()")

## 4.3 generate libraries compare status to a global dict
def libchecker_compare_metainfo():
    # this function get the result of libchecker compare
    # input: 
    #           @ g_pkginfodict_from_json
    #           @ g_libinfodict_from_json
    # output:
    #           @ g_libchecker_comp_status
    # return:
    #           @ 
    print("Enter function: libchecker_compare_metainfo()")
    liblists = []
    global g_libchecker_comp_status

    # init the g_libchecker_comp_status[] to "false"
    for key in g_libinfodict_from_json:
        g_libchecker_comp_status[key] = "false"

    for key in g_pkginfodict_from_json:
        liblists = get_linkname_from_srcpkg(key)
        for i in g_libinfodict_from_json.keys():
            if i in liblists:
                if compare_library_version(g_libinfodict_from_os[i], g_libinfodict_from_json[i]) == ">" :
                    g_libchecker_comp_status[i] = "true"
                elif compare_library_version(g_libinfodict_from_os[i], g_libinfodict_from_json[i]) == "=" :
                    g_libchecker_comp_status[i] = "true"
                else:
                    g_libchecker_comp_status[i] = "false"

    return g_libchecker_comp_status

def libchecker_compare_liblist():

    global g_liblist_from_json
    global g_liblist_from_os
    
    liblist_json = g_liblist_from_json
    liblist_os = g_liblist_from_os
    
    print(liblist_json)
    print(liblist_os)

    compare_dict = {}

    for i in liblist_json:
        compare_dict[i] = "false"

    print(compare_dict)

    for i in liblist_json:
        for j in liblist_os:
#            if j >= i
            compare_dict[i] = compare_library_version(i, j)

    return compare_dict

# 5. Generate Output Result
## 5.1 generate a json file output
def gen_json_file():
    # this function generate a json file (for test)
    # input: 
    #           @ 
    # output:
    #           @ file: test.json
    # return:
    #           @
    print("Enter function: gen_json_file()")

    article_info = {}
    data = json.loads(json.dumps(article_info))

    data['cmdchecker'] = 'none'

    libchecker = {'title': 'Python-base', 'publish_time':'2019-4-1', 'write':{}}
    data['libchecker'] = libchecker

    sonames = {'name': 'lixiansheng', 'sex':'man', 'email':'xxx@gmail.com'}
    data['libchecker']['sonames'] = sonames

    oschecker = json.dumps(data, ensure_ascii=False)

    with open("test.json","w") as f:
        json.dump(oschecker,f,indent = 4)

def libchecker_output_json_file():
    # global g_chapter_dict
    # global g_jsonfile_dict

    # print("Enter function: libchecker_output_json_file()")
    output_info = {}
    output_data = json.loads(json.dumps(output_info))
    
    # mateinfo = {}
    # mateinfo_sections_number = {}
    # mateinfo_pkgcheck_result = {}
    # mateinfo_objcheck_result = {}
    # mateinfo_packages_dict = {}
    # mateinfo_share_libs = {}
    # mateinfo_all_info = {}
    out_data_deep = {}
    
    # result_dict = libchecker_compare_liblist()


    # for chapter_class in g_jsonfile_dict['libs']['category']: # chapter_class
        # print(chapter_class)
        # for key in g_jsonfile_dict['libs']['category'][chapter_class]['packages']: # package_class
            # print("\t", key)
            #mateinfo.update = { key : g_jsonfile_dict['libs']['category'][chapter_class][key]['packages']['sections_number'] }
            # for key1 in g_jsonfile_dict['libs']['category'][chapter_class]['packages'][key]: # sections_number class
                # print("\t\t", key1)
                # print("\t\t", key1)
                # print("\t\t\t",g_jsonfile_dict['libs']['category'][chapter_class]['packages'][key]['sections_number'])
#                print("\t\t\t", key1)
                # mateinfo_sections_number.update({ key :  g_jsonfile_dict['libs']['category'][chapter_class]['packages'][key]['sections_number']})
#            for key1 in g_jsonfile_dict['libs']['category'][chapter_class]['packages']:
#                mateinfo_pkgcheck_result.update({ key1 :  g_jsonfile_dict['libs']['category'][chapter_class]['packages'][key1]['version']['desktop']})
#            for key1 in g_jsonfile_dict['libs']['category'][chapter_class]['packages']:
#                mateinfo_objcheck_result.update({ key1 :  g_jsonfile_dict['libs']['category'][chapter_class]['packages'][key1]['share_objs']['desktop']})
            #, "Chapter " : g_jsonfile_dict['libs']['category'][chapter_class][key]['packages']['sections_number']}
            #, "Necessity" : chapter_class['packages']['necessity'], "Share Objs" : chapter_class['packages']['share_objs'], "Otherinfo" : "none"}
            # mateinfo = { "Package ":  g_jsonfile_dict['libs']['category'][chapter_class]['packages'][key]}i
                # mateinfo_sections_number.update({ key1 :  g_jsonfile_dict['libs']['category'][chapter_class]['packages'][key]['sections_number']})

            # mateinfo_packages_dict.update({key : mateinfo_sections_number})
            # mateinfo_packages_dict.update({key : mateinfo_sections_number})
            # mateinfo_sections_number.clear()
            
            # mateinfo_all_info.update({ key :  g_jsonfile_dict['libs']['category'][chapter_class]['packages'][key]['sections_number']})
        #mateinfo_packages_dict.update({key : "test"})

        # mateinfo_all_info.update({chapter_class : mateinfo_packages_dict})

        #out_data_deep.update({chapter_class : mateinfo_packages_dict})
        # out_data_deep.update({chapter_class : g_genresults_to_json})
        #mateinfo_packages_dict.clear()
        
    #output_data = {"LibChecker Result" : out_data_deep}
    output_data = {"LibChecker Result" : g_genresults_to_json}




    json_output = json.dumps(out_data_deep, ensure_ascii = False)

    with open("Outputs/libchecker-output.json","w") as f:
        json.dump(output_data,f)
        #json.dump(out_data_deep,f)


def libchecker_json_file_output():
    # this function generate a json file for libchecker
    # input: 
    #           @ g_libinfodict_from_os
    #           @ g_libchecker_comp_status
    # output:
    #           @ file: libchecker-output.json
    # return:
    #           @
    print("Enter function: gen_json_file_output()")
    # {
    #   "libchecker" {
    #       "linkname" : {
    #           "name" : "******"
    #           "version" : "******"
    #           "status" : "******"
    #           "category" : "******"
    #           "otherinfo" : "******"
    #       },
    # }
    output_info = {}
    output_data = json.loads(json.dumps(output_info))
    
    mateinfo = {}
    out_data_deep = {}

    for key in g_libchecker_comp_status:
        if key not in g_libinfodict_from_os:
            mateinfo = {"name" : key, "version" : "no exist", "status" : "no exist" , "category" : "exist", "otherinfo" : "no exist"}
        else:
            mateinfo = {"name" : pick_linkname_from_soname(key), "version" : key, "status" : g_libchecker_comp_status[key], "category" : "library", "otherinfo" : "none"}
        
        #out_data_deep = {key : mateinfo}
        out_data_deep.update({key : mateinfo})
        output_data = {"libchecker": out_data_deep}

    json_output = json.dumps(output_data, ensure_ascii = False)

    with open("Output/libchecker-output.json","w") as f:
        json.dump(output_data,f)

#print(get_realname_from_debpkg('libncurses5'))
#print(get_soname_from_debpkg('libncurses5'))
#print(get_linkname_from_debpkg('libncurses5'))
#print(get_debpkg_from_srcpkg('ncurses'))
#get_pkginfo_from_os('libc6')
#libchecker_read_json_file('std-lib.json')

#gen_json_file()
#read_json_file('std-lib.json')
#read_json_file('libchecker-out.json')
#libchecker_json_file_output()
#print(compare_library_version("lib.so.6", "lib.so.6"))
#test_function()

#for key in g_pkginfodict_from_json:
#        liblists = get_linkname_from_srcpkg(key)
#        for i in g_libinfodict_from_json.keys():

#read_json_file('../StdLists/lib_list_1.0I-20220826.json')

#print(read_pkginfo_from_stdjson('../StdLists/lib_list_1.0I-20220830-uos.json'))
#print(read_libinfo_from_stdjson('../StdLists/lib_list_1.0I-20220830-uos.json'))
#libchecker_read_stdjson('../StdLists/lib_list_1.0I-20220830-uos.json')i

##libchecker_read_stdjson('StdLists/lib_list_1.0I-20220830-uos.json')
#print(g_pkginfodict_from_json)
#print(g_libinfodict_from_json)
#print(g_bind_pkglib_from_json)

#g_pkginfodict_from_os = {}
#g_libinfodict_from_os = {}

#g_libchecker_comp_status = {}
#print(get_realname_from_srcpkg('ncurses'))
#print(get_soname_from_srcpkg('ncurses'))
#print(get_linkname_from_srcpkg('ncurses'))
#print(read_pkginfo_from_json('std-lib.json'))
#print(read_libinfo_from_json('std-lib.json'))
#print(read_pkginfo_from_json('std-lib.json'))

#get_libinfo_from_os()
#print(get_libinfo_from_os())

#pick_linkname_from_soname('ncurses')
#print(get_soname_from_srcpkg('ncurses'))
#print(pick_linkname_from_soname('ncurses.so.1.9'))
#print(compare_version_serial_number("1.4.3", "2.4.3"))
#libchecker_compare_metainfo()
#libchecker_read_std_json('stdlists/lib_list_1.0I.json')
#def read_pkginfo_from_json(json_file_path):
#print(get_pkginfo_from_os())
#print(get_libinfo_from_os())


#print(get_libinfo_from_os_by_srcpkg())
#print(g_libinfodict_from_json)
##get_liblists_from_os()
#print(get_liblists_from_stdjson('../StdLists/lib_list_1.0I-20220830-uos.json'))
##get_liblists_from_stdjson('StdLists/lib_list_1.0I-20220830-uos.json')

#print("g_liblist_from_json")
#print(g_liblist_from_json)
#print("g_liblist_from_os")
#print(g_liblist_from_os)

##libchecker_compare_liblist()
##libchecker_output_json_file()


libchecker_environment_init()
libchecker_checking_loop()
#print(get_env_info())
#get_env_info()

#libchecker_output_json_file()
libchecker_over_jobs()

#check_sharelib_info('/lib', 'libanl.so.1' )

#print(g_jsonfile_dict['glibc']['share_objs']['desktop'])
#        for list_item in g_jsonfile_dict['libs']['category']['base']['packages'][src_pkgname]['share_objs']['desktop']
 
