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
parser.add_argument('-o', '--organize', action='store', type=str, help='Choice Company or Organize')
parser.add_argument('-j', '--json', action='store', type=str, help='Choice OSChecker Json templete file', required=False) # this line use for dect the json file.
args = parser.parse_args() # write arguments to struct

g_inputstrategy = args.strategy
g_inputlevel = args.level
g_inputostype = args.ostype
g_inputpkgmngr = args.pkgmngr
g_inputorganize = args.organize
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

def get_stdjsons_info(json_file_path):
    with open(json_file_path) as f:
        f_dict = json.load(f)

    global g_jsonfile_dict
    g_jsonfile_dict = f_dict
    lib_basedict = f_dict['libs']['category']['base']['packages']

    print("标准信息:")
    print("\t标准简要信息:")
    print("\t\t标准号: %s" % f_dict['std_description']['std_number'])
    print("\t\t文件名: %s" % f_dict['std_description']['std_name'])
    print("\t库检查器信息:")
    print("\t\t检查位置: %s" % f_dict['libs']['lib_location'])

    # print("Start Checking: .....: Chapter: %s Category: %s;" %(f_dict['libs']['category']['base']['description']['chapters_number'], f_dict['libs']['category']['base']['description']['chapters_Name']))

def libchecker_environment_init():
    global g_counter_flags
    # g_inputstrategy = args.strategy
    # g_inputlevel = args.level
    # g_inputostype = args.ostype
    # g_inputpkgmngr = args.pkgmngr
    
    g_counter_flags = {'pkg_counter': {'total': {'all' : 0, 'l1' : 0, 'l2' : 0, 'l3' : 0} , 'passed': {'all': 0, 'l1' : 0, 'l2' : 0, 'l3' : 0}, 'warning': {'all': 0, 'l1' : 0, 'l2' : 0, 'l3' : 0}, 'failed': {'all' : 0, 'l1' : 0, 'l2' : 0, 'l3' : 0} }, 'lib_counter': {'total': 0, 'passed': 0, 'warning': 0, 'failed': 0}}

    get_env_info()

    get_stdjsons_info('Jsons/lib_list.json')
    
    if (g_inputpkgmngr == "apt-deb"):
        apt_pkg.init_system()

def check_srcname(realname):
    if(len(g_storejsondict[realname]['alias']) == 0):
        return realname
    else:
        alias_list = g_storejsondict[realname]['alias'][0]['name'].split('/')
        if(realname not in alias_list):
            alias_list.append(realname)

        if (g_inputpkgmngr == "yum-rpm"):
            for alias_tmp in alias_list:
                l_1 = os.system('dnf info %s 2>/dev/null 1>/dev/null' %(alias_tmp))
                if(l_1 == 0):
                    break
            return alias_tmp
        else:
            for alias_tmp in alias_list:
                l_1 = os.popen('apt-cache showsrc %s 2>/dev/null | grep "^Version:"' %(alias_tmp)).read().split('\n')
                if(len(l_1) != 0):
                    break
            return alias_tmp

def check_per_pkg_info(src_pkgname):
    global g_notfind_set_flag
    global g_genresults_to_json
    global g_test_dict 

    if(g_inputostype == "desktop"):
        if (g_inputpkgmngr == "apt-deb"):
            p_srcpkgver = os.popen('apt-cache showsrc %s 2>/dev/null | grep \^Version | cut -d '"\ "' -f 2 ' %(src_pkgname))
        elif (g_inputpkgmngr == "yum-rpm"):
            p_srcpkgver = os.popen('yum list %s 2>/dev/null | awk \'{print $2}\' | sed -n \'3p\'  ' %(src_pkgname))
    elif(g_inputostype == "server"):
        if (g_inputpkgmngr == "apt-deb"):
            p_srcpkgver = os.popen('apt-cache showsrc %s 2>/dev/null | grep \^Version | cut -d '"\ "' -f 2 ' %(src_pkgname))
        elif (g_inputpkgmngr == "yum-rpm"):
            p_srcpkgver = os.popen('yum list %s 2>/dev/null | awk \'{print $2}\' | sed -n \'3p\'  ' %(src_pkgname))
    else:
        print("Please input --ostype=[desktop,server,embde,...] and --pkgmngr=[apt-deb,yum-rpm,src-bin,...]")

    srcpkgver = p_srcpkgver.read().rstrip('\n')
    p_srcpkgver.close()

    global g_counter_flags

    g_counter_flags['pkg_counter']['total']['all'] += 1

    print("\t\t系统实现: ")

    if (len(srcpkgver) == 0):
        print("\t\t\t\t没有发现")
        g_notfind_set_flag = 1
    else:
        print("\t\t\t\t实现包名 -> ", src_pkgname.ljust(20),"实现版本 -> ",srcpkgver)

        print("\t\t共享库信息:")

        g_counter_flags['pkg_counter']['passed']['all'] += 1    

def check_pkginfo_for_desktop(src_pkgname):
    for src_pkgname in g_jsonfile_dict:
        check_per_pkg_info(g_jsonfile_dict['libs']['category']['base']['packages'][src_pkgname]['alias'][0]['name'])

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
            check_per_pkg_info(check_srcname(last_key))
            g_subresults_to_json.clear()
            if (g_notfind_set_flag == 1 ):
                g_counter_flags['pkg_counter']['failed']['all'] += 1
                g_notfind_set_flag = 0
                with open("Outputs/libchecker-output.json", 'r') as fr:
                    json_so = json.load(fr)
                    json_so[last_key]['Shared library'] = "-"
                with open("Outputs/libchecker-output.json", 'w+') as fw:
                    json.dump(json_so,fw,ensure_ascii=False,indent=4)
                with open("Outputs/libchecker-output.json", 'r') as fr:
                    json_local_ver = json.load(fr)
                    json_local_ver[last_key]['Binary package'] = "-"
                with open("Outputs/libchecker-output.json", 'w+') as fw:
                    json.dump(json_local_ver,fw,ensure_ascii=False,indent=4)
                continue
            else:
                for list1_item in g_storejsondict[last_key]['share_objs'][g_ostype]:
                    print("\t\t\t\t名称 -> ",list1_item)
                    print("\t\t\t\t\t标准约定 -> ",list1_item, )
                    lib_result = check_sharelib_info(list1_item)
                    print("\t\t\t\t\t系统存在 -> ",lib_result, )
                    temp_libsoname = lib_result.split('/')[-1]
                    if (lib_result == "not found"):
                        print("\t\t\t\t\t检测结果 ->  未检测到存在")
                        g_subresults_to_json[list1_item] = {'status': 'not found', 'path':'-'}
                        g_counter_flags['lib_counter']['failed'] += 1
                    else:
                        print("\t\t\t\t\t检测结果 -> ", compare_library_version(temp_libsoname, str(list1_item)))
                        if (compare_library_version(temp_libsoname, str(list1_item)) == "equal" ):
                            g_counter_flags['lib_counter']['passed'] += 1
                            g_subresults_to_json[list1_item] = {'status': 'compatible', 'path':lib_result}
                        elif (compare_library_version(temp_libsoname, str(list1_item)) == "smaller" ):
                            g_counter_flags['lib_counter']['failed'] += 1
                            g_subresults_to_json[list1_item] = {'status': 'incompatible', 'path':lib_result}
                        else:
                            g_counter_flags['lib_counter']['warning'] += 1
                            g_subresults_to_json[list1_item] = {'status': 'compatible bigger', 'path':lib_result}

        #Traverse the binary package of the source package
        if (g_inputpkgmngr == "yum-rpm"):
            binary_list = get_rpmpkg_from_srcpkg(last_key)
        else:
            binary_list = get_debpkg_from_srcpkg(last_key)

        for binary_name in binary_list:
            if (g_inputpkgmngr == "yum-rpm"):
                pkg_install_status = os.system('rpm -qi %s 2>/dev/null 1>/dev/null' %(binary_name))
                if (pkg_install_status == 0):
                    ver_required = g_storejsondict[last_key]['version'][g_inputostype] #获取要求的库包版本
                    ver_local = os.popen('rpm -qi %s 2>/dev/null | grep "Version\|Release" | awk -F" " \'{print $3}\' | sed \':label;N;s/\\n/-/;t label\'' %(binary_name)).read().rstrip('\n') #获取本地库包版本
                    if (get_rpmpkg_ver_contrast(ver_local, ver_required) == "compatible"):
                        l_pkgresult_to_json[binary_name] = {'status': 'compatible', 'local version': ver_local}
                    elif (get_rpmpkg_ver_contrast(ver_local, ver_required) == "incompatible"):
                        l_pkgresult_to_json[binary_name] = {'status': 'incompatible', 'local version': ver_local}
            else:
                pkg_install_status = os.popen('dpkg -l %s 2>/dev/null| grep %s 2>/dev/null | awk -F" " \'{print $1}\' | head -n 1' %(str(binary_name), str(binary_name))).read().rstrip('\n')
                if (pkg_install_status == "ii"):
                    ver_required = g_storejsondict[last_key]['version'][g_inputostype] #获取要求的库包版本
                    ver_local = os.popen('dpkg -l %s 2>/dev/null| grep %s 2>/dev/null | awk -F" " \'{print $3}\' | head -n 1' %(binary_name, binary_name)).read().rstrip('\n') #获取本地库包版本
                    if (get_debpkg_ver_contrast(ver_local, ver_required) == "compatible"):
                        l_pkgresult_to_json[binary_name] = {'status': 'compatible', 'local version': ver_local}
                    elif (get_debpkg_ver_contrast(ver_local, ver_required) == "incompatible"):
                        l_pkgresult_to_json[binary_name] = {'status': 'incompatible', 'local version': ver_local}
                else:
                    continue

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
    print("\t检查策略：", "\"",  "--strategy =",args.strategy, "--level =",args.level, "--ostype =", args.ostype, "--pkgmngr =", args.pkgmngr, "--organize =", args.organize, "\"")
    print("")
    print("\t软件包:")
    print("\t\t总计:", g_counter_flags['pkg_counter']['total']['all'], "{" ,"l1->",g_counter_flags['pkg_counter']['total']['l1'],";", "l2->", g_counter_flags['pkg_counter']['total']['l2'], ";", "l3->", g_counter_flags['pkg_counter']['total']['l3'],  "}")
    print("\t\t通过:", g_counter_flags['pkg_counter']['passed']['all'])
    print("\t\t警告:", g_counter_flags['pkg_counter']['warning']['all'])
    print("\t\t报错:", g_counter_flags['pkg_counter']['failed']['all'])
    print("\t动态库:")
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

libchecker_environment_init()
libchecker_checking_loop()
libchecker_over_jobs()
