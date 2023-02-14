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
parser.add_argument('-o', '--organize', action='store', type=str, help='Choice Organize or Company')
parser.add_argument('-j', '--json', action='store', type=str, help='Choice OSChecker Json templete file', required=False) # this line use for dect the json file.
parser.add_argument('-T', '--timetmp', action='store', type=str)
args = parser.parse_args() # write arguments to struct

g_inputstrategy = args.strategy
g_inputlevel = args.level
g_inputostype = args.ostype
g_inputpkgmngr = args.pkgmngr
g_inputorganize = args.organize
g_inputjson = args.json

g_time_stamp = args.timetmp
g_output_filename = "Outputs/libchecker-output_" + g_time_stamp + ".json"
g_output_logname = "Logs/libchecker_" + g_time_stamp + ".log"

# option module import
#if (g_inputpkgmngr == "apt-deb"):
#    import apt_pkg # import for apt-deb package management tools


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
g_ostype = g_inputostype        # global magic string for OS type
g_pkgmgr = g_inputpkgmngr       # global magic string for OS type
g_test_dict = {}
g_test_list = []

## 0.2 a recycle call function for user
def libchecker_over_jobs():
    #time_now = time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())
    #log_file_name = "Logs/libchecker-" + g_time_stamp + ".log"
    os.rename("Logs/libchecker-tmp.log", g_output_logname)

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

def libchecker_environment_init():
    global g_counter_flags

    g_counter_flags = {'pkg_counter': {'total': {'all' : 0, 'l1' : 0, 'l2' : 0, 'l3' : 0} , 'passed': {'all': 0, 'l1' : 0, 'l2' : 0, 'l3' : 0}, 'warning': {'all': 0, 'l1' : 0, 'l2' : 0, 'l3' : 0}, 'failed': {'all' : 0, 'l1' : 0, 'l2' : 0, 'l3' : 0} }, 'lib_counter': {'total': 0, 'passed': 0, 'warning': 0, 'failed': 0}}

    get_env_info()

    get_stdjsons_info('Jsons/lib_list.json')
    
#   if (g_inputpkgmngr == "apt-deb"):
#       apt_pkg.init_system()

##====获取别名信息字典====##
def get_alias_dcit(l_realname):
    
    l_dict_alias_info = {}
    l_dict_binary_name = {}
    l_dict_tmp = {}

    l_list_binary_name = []
    l_list_alias = []
    l_list_tmp = []

    
    if(len(g_storejsondict[l_realname]['alias']) == 0):
        l_list_binary_name.clear()
        
        if (g_inputpkgmngr == "yum-rpm"):
            l_list_binary_name = get_rpmpkg_from_srcpkg(l_realname)
        else:
            l_list_binary_name = get_debpkg_from_srcpkg(l_realname)

        if(len(l_list_binary_name) != 0):
            for i in range(0, len(l_list_binary_name)):
                l_dict_binary_name.update({l_list_binary_name[i]: '-'})
            l_dict_alias_info.update({l_realname: l_dict_binary_name})
        else:
            l_dict_alias_info.update({l_realname: "-"})
    else:
        l_list_alias.clear()
        l_list_tmp.clear()

        for i in range(0, len(g_storejsondict[l_realname]['alias'])):
            if "/" in g_storejsondict[l_realname]['alias'][i]['name']:
                l_list_tmp = g_storejsondict[l_realname]['alias'][i]['name'].split('/')
                for num in range(0, len(l_list_tmp)):
                    l_list_alias.append(l_list_tmp[num])
            else:
                l_list_alias.append(g_storejsondict[l_realname]['alias'][i]['name'])

        if l_realname not in l_list_alias:
            l_list_alias.append(l_realname)

        for k in range(0, len(l_list_alias)):
            l_list_binary_name.clear()
            l_dict_binary_name.clear()

            if (g_inputpkgmngr == "yum-rpm"):
                l_list_binary_name = get_rpmpkg_from_srcpkg(l_list_alias[k])
            else:
                l_list_binary_name = get_debpkg_from_srcpkg(l_list_alias[k])

            if(len(l_list_binary_name) != 0):
                for j in range(0, len(l_list_binary_name)):
                    l_dict_binary_name.update({l_list_binary_name[j]: '-'})

                l_dict_tmp = dict.fromkeys(l_dict_binary_name.keys(), None)
                l_dict_alias_info[l_list_alias[k]] = l_dict_tmp
            else:
                l_dict_alias_info[l_list_alias[k]] = "-"

    return l_dict_alias_info

##====检查源码包仓库是否存在====##
def check_per_pkg_info(src_pkgname):
    global g_notfind_set_flag
    global g_genresults_to_json
    global g_test_dict 
    global g_counter_flags

    srcpkgver = []

    if g_inputostype == "desktop" or g_inputostype == "server":
        if (g_inputpkgmngr == "apt-deb"):
            l_search_pname = os.popen('apt-cache showsrc %s 2>/dev/null | grep ^Package: | awk -F": " \'{print $2}\'' %(src_pkgname))
            l_pname = l_search_pname.read().split("\n")[0]
            l_search_pname.close()
            if(l_pname == src_pkgname):
                p_srcpkgver = os.popen('apt-cache showsrc %s 2>/dev/null | grep \^Version | cut -d '"\ "' -f 2 ' %(src_pkgname))
                srcpkgver = p_srcpkgver.read().rstrip('\n')
                p_srcpkgver.close()
        elif (g_inputpkgmngr == "yum-rpm"):
            p_srcpkgver = os.popen('yum list %s 2>/dev/null | awk \'{print $2}\' | sed -n \'3p\'  ' %(src_pkgname))
            srcpkgver = p_srcpkgver.read().rstrip('\n')
            p_srcpkgver.close()
    else:
        print("Please input --ostype=[desktop,server,embde,...] and --pkgmngr=[apt-deb,yum-rpm,src-bin,...]")

    g_counter_flags['pkg_counter']['total']['all'] += 1

    print("\t\t系统实现: ")
    if (len(srcpkgver) == 0):
        print("\t\t\t\t未发现  -> ", src_pkgname.ljust(20))
    else:
        print("\t\t\t\t实现包名 -> ", src_pkgname.ljust(20),"实现版本 -> ",srcpkgver)
        g_counter_flags['pkg_counter']['passed']['all'] += 1   
        g_notfind_set_flag = 1 

##====查询共享库路径信息====##
def check_sharelib_info(lib_soname):

    global g_lib_location_path
    global g_counter_flags
    g_lib_location_path = "0"

    global g_counter_flags
    g_counter_flags['lib_counter']['total'] += 1
    l_list = ["/lib", "/lib64", "/usr/lib", "/usr/lib64"]

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

##====主函数====##
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
    l_dict_alias_info = {}      #存储写入json文件Binary package信息的字典
    l_dict_binary_list = {}

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
                g_storejsondict[key] = l_tmp_dict[key]
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
        
    if ( g_inputstrategy == "base" ):
        print(g_genresults_to_json)
        print(g_storejsondict)
        for l_name in list(g_genresults_to_json.keys()):
            if ( g_storejsondict[l_name]['necessity'][g_inputostype]['options'] != "basic" ):
                del g_genresults_to_json[l_name]
                g_storejsondict.pop(l_name)
    elif( g_inputstrategy == "with-expand" ):
         for l_name in list(g_genresults_to_json.keys()):
            if ( len(g_storejsondict[l_name]['necessity'][g_inputostype]['options']) == 0 ):
                del g_genresults_to_json[l_name]
                g_storejsondict.pop(l_name)
    elif( g_inputstrategy == "only-expand" ):
        for l_name in list(g_genresults_to_json.keys()):
            if ( g_storejsondict[l_name]['necessity'][g_inputostype]['options'] != "expansion" ):
                del g_genresults_to_json[l_name]
                g_storejsondict.pop(l_name)
    else:
        print("Error： --strategy 参数指定错误")
        exit()

    with open(g_output_filename,"w") as f:
        json.dump(g_genresults_to_json,f)

    for last_key in g_storejsondict:
        l_pkgresult_to_json.clear()

        l_dict_alias_info = get_alias_dcit(last_key)
        l_require_version = g_storejsondict[last_key]['version'][g_inputostype]  #源码包需求版本

        ###向json文件写入'Level'信息
        with open(g_output_filename, 'r') as fr:
            json_level = json.load(fr)
            json_level[last_key]['Level'] = g_storejsondict[last_key]['necessity'][g_inputostype]['level']
        with open(g_output_filename, 'w+') as fw:
            json.dump(json_level,fw,ensure_ascii=False,indent=4)
        ###向json文件写入'Required version'信息
        with open(g_output_filename, 'r') as fr:
            json_required_ver = json.load(fr)
            json_required_ver[last_key]['Required version'] = l_require_version
        with open(g_output_filename, 'w+') as fw:
            json.dump(json_required_ver,fw,ensure_ascii=False,indent=4)

        if (len(g_storejsondict[last_key]['version'][g_ostype]) != 0):
            for l_src_name in list(l_dict_alias_info.keys()):
                l_src_status = 0

                if (l_dict_alias_info[l_src_name] != "-"):
                    l_dict_binary_list.clear()
                    l_dict_binary_list = l_dict_alias_info[l_src_name]
                    for l_binary_name in list(l_dict_binary_list.keys()):
                        if (g_inputpkgmngr == "yum-rpm"):
                            l_rpm_local_version = get_rpmpkg_local_verison(l_binary_name)
                            if (l_rpm_local_version == "-"):
                                del l_dict_alias_info[l_src_name][l_binary_name]
                            else:
                                l_src_status += 1
                                l_binary_version_status = get_rpmpkg_ver_contrast(l_rpm_local_version, l_require_version)
                                l_dict_binary_list[l_binary_name] = {'status': l_binary_version_status, 'local version': l_rpm_local_version}
                        else:
                            l_deb_local_version = get_debpkg_local_version(l_binary_name, l_src_name)
                            if (l_deb_local_version == "-"):
                                del l_dict_binary_list[l_binary_name]
                            else:
                                l_src_status += 1
                                l_binary_version_status = get_debpkg_ver_contrast(l_deb_local_version, l_require_version)
                                l_dict_binary_list[l_binary_name] = {'status': l_binary_version_status, 'local version': l_deb_local_version}

                    if (l_src_status == 0):
                        l_dict_alias_info[l_src_name] = "Don`t find installed packages"
                    else:
                        l_dict_alias_info[l_src_name] = l_dict_binary_list
                else:
                    l_dict_alias_info[l_src_name] = "None"
        else:  
            l_dict_alias_info[l_src_name] = "None"

        ###向json文件写入'Binary package'信息
        with open(g_output_filename, 'r') as fr:
            json_alias_info = json.load(fr)
            json_alias_info[last_key]['Binary package'] =  l_dict_alias_info
        with open(g_output_filename, 'w+') as fw:
            json.dump(json_alias_info,fw,ensure_ascii=False,indent=4)

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
            g_subresults_to_json.clear()

            g_notfind_set_flag = 0
            for l_alias_name in list(l_dict_alias_info.keys()):
                check_per_pkg_info(l_alias_name)  #待修改

            print("\t\t共享库信息:")
            if (g_notfind_set_flag == 0):
                g_counter_flags['pkg_counter']['failed']['all'] += 1

                ###向json文件写入'Shared library'信息
                with open(g_output_filename, 'r') as fr:
                    json_so = json.load(fr)
                    json_so[last_key]['Shared library'] = "-"
                with open(g_output_filename, 'w+') as fw:
                    json.dump(json_so,fw,ensure_ascii=False,indent=4)
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
                        g_subresults_to_json[list1_item] = {'status': 'not found', 'path':'-', 'belongs':'None'}
                        g_counter_flags['lib_counter']['failed'] += 1
                    else:
                        if (g_inputpkgmngr == "yum-rpm"):
                            l_file_belongs = get_rpm_file_belongs_package(lib_result)
                        else:
                            l_file_belongs = get_deb_file_belongs_package(lib_result)

                        print("\t\t\t\t\t检测结果 -> ", compare_library_version(temp_libsoname, str(list1_item)))
                        print("\t\t\t\t\t文件所属 -> ", l_file_belongs)
                        if (compare_library_version(temp_libsoname, str(list1_item)) == "equal" ):
                            g_counter_flags['lib_counter']['passed'] += 1
                            g_subresults_to_json[list1_item] = {'status': 'compatible', 'path':lib_result, 'belongs':l_file_belongs}
                        elif (compare_library_version(temp_libsoname, str(list1_item)) == "smaller" ):
                            g_counter_flags['lib_counter']['failed'] += 1
                            g_subresults_to_json[list1_item] = {'status': 'incompatible', 'path':lib_result, 'belongs':l_file_belongs}
                        else:
                            g_counter_flags['lib_counter']['warning'] += 1
                            g_subresults_to_json[list1_item] = {'status': 'compatible bigger', 'path':lib_result, 'belongs':l_file_belongs}

        ###向json文件写入'Shared library'信息
        with open(g_output_filename, 'r') as fr:
            json_so = json.load(fr)
            json_so[last_key]['Shared library'] = g_subresults_to_json
        with open(g_output_filename, 'w+') as fw:
            json.dump(json_so,fw,ensure_ascii=False,indent=4)

    print("=============================================================================================================")
    print("结束检查 ",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    print("")
    print("\t检查策略：", "\"",  "--strategy =",args.strategy, "--level =",args.level, "--ostype =", args.ostype, "--pkgmngr =", args.pkgmngr, "--organize =", args.organize, "\"")
    print("")
    #print("\t软件包:")
    #print("\t\t总计:", g_counter_flags['pkg_counter']['total']['all'], "{" ,"l1->",g_counter_flags['pkg_counter']['total']['l1'],";", "l2->", g_counter_flags['pkg_counter']['total']['l2'], ";", "l3->", g_counter_flags['pkg_counter']['total']['l3'],  "}")
    #print("\t\t通过:", g_counter_flags['pkg_counter']['passed']['all'])
    #print("\t\t警告:", g_counter_flags['pkg_counter']['warning']['all'])
    #print("\t\t报错:", g_counter_flags['pkg_counter']['failed']['all'])
    #print("\t动态库:")
    #print("\t\t总计:", g_counter_flags['lib_counter']['total'])
    #print("\t\t通过:", g_counter_flags['lib_counter']['passed'])
    #print("\t\t警告:", g_counter_flags['lib_counter']['warning'])
    #print("\t\t报错:", g_counter_flags['lib_counter']['failed'])
    print("=============================================================================================================")

##====deb查询文件所属二进制包====##
def get_deb_file_belongs_package(l_deb_file_name):
    # this function for get deb pacgakes to which the file belongs
    # input: 
    #           @ l_deb_file_name
    # return:
    #           @ l_deb_binary_name
    l_deb_realpath = os.path.realpath(l_deb_file_name)
    l_file_belongs_deb = os.popen('dpkg -S %s 2>/dev/null | awk -F": " \'{print $1}\'' %(l_deb_realpath))
    l_belongs_deb = l_file_belongs_deb.read().rsplit('\n')[0]
    l_file_belongs_deb.close()

    if (len(l_belongs_deb) == 0):
        l_belongs_deb = "None"

    return l_belongs_deb 

##====rpm查询文件所属二进制包====##
def get_rpm_file_belongs_package(l_rpm_file_name):
    # this function for get rpm pacgakes to which the file belongs
    # input: 
    #           @ l_deb_file_name
    # return:
    #           @ l_rpm_binary_name
    print("makeing")


##====deb对比版本大小====##
def get_debpkg_ver_contrast(l_local_ver, l_required_ver):
    # --compare-version ver_local op ver_required
    # op: lt le eq ne ge gt
    # sn:  < <= == != >= > 
    compare_result = os.system('dpkg --compare-versions %s ge %s' %(str(l_local_ver), str(l_required_ver)))
    if(compare_result == 0):
        return "compatible"
    else:
        return "incompatible"

##====rpm对比版本大小====##
def get_rpmpkg_ver_contrast(l_local_ver, l_required_ver):
    # compare ver_local op ver_required
    if l_local_ver < l_required_ver:
        return "incompatible"
    else:
        return "compatible"

##====比较共享库版本大小====##
def compare_library_version(l_local_ver, l_required_ver):
    # this function compare soname for number
    # input: 
    #           @ l_local_ver
    #           @ l_required_ver
    # return:
    #           @ ret:  string: >
    #           @ ret:  string: =
    #           @ ret:  string: <
    if l_local_ver == l_required_ver:
        return "equal"
    elif str(l_local_ver) < str(l_required_ver):
        return "smaller"
    else:
        return "bigger"

## 3.2 get deb package info 
##====apt获取二进制包列表====##
def get_debpkg_from_srcpkg(l_deb_srcname):
    # this function for get deb pacgakes from package name in current os
    # input: 
    #           @ l_deb_srcname
    # return:
    #           @ l_list_debpkgs
    l_list_debpkgs = []
    l_list_debpkgs.clear()

    l_package_name = os.popen('apt-cache showsrc %s 2>/dev/null | grep ^Package: | awk -F": " \'{print $2}\'' %(l_deb_srcname))
    l_pname = l_package_name.read().split("\n")[0]
    l_package_name.close()
    if(l_pname == l_deb_srcname):
        l_debpkgs = os.popen('apt-cache showsrc %s 2>/dev/null | grep Binary | cut -d '"\:"' -f 2- | cut -d '"\ "' -f 2- ' %(l_deb_srcname))
        l_list_debpkgs = l_debpkgs.read().split("\n")[0].split(", ")
        l_debpkgs.close()

    return l_list_debpkgs
    
##====yum获取二进制包列表====##    
def get_rpmpkg_from_srcpkg(l_rpm_srcname):
    # this function for get rpm pacgakes from package name in current os
    # input: 
    #           @ l_rpm_srcname
    # return:
    #           @ l_list_rpmpkgs
    l_rpmpkgs = os.popen('dnf info | grep -B 5 -E "%s.*.src.rpm" | grep "名称" | awk -F" " \'{ print $3 }\' | sort -n | uniq | sed \':label;N;s/\\n/ /;t label\'' %(l_rpm_srcname))
    l_list_rpmpkgs = l_rpmpkgs.read().split("\n")[0].split(" ")
    l_rpmpkgs.close()

    return l_list_rpmpkgs

##====deb获取二进制包版本====##  
def get_debpkg_local_version(l_deb_binary_name, l_deb_src_name):
    # this function for get deb pacgakes local verison
    # input: 
    #           @ l_deb_binary_name
    # return:
    #           @ l_ver_local
    l_ver_local = "-"

    l_file_deb_install_status = os.popen('dpkg -l %s 2>/dev/null| grep %s 2>/dev/null | awk -F" " \'{print $1}\' | head -n 1' %(l_deb_binary_name, l_deb_binary_name))
    l_deb_install_status = l_file_deb_install_status.read().rstrip('\n')
    l_file_deb_install_status.close()

    if(l_deb_install_status == "ii"):
        l_file_src_name = os.popen('dpkg --status %s 2>/dev/null|grep ^Source:|awk -F": " \'{print $2}\'' %(l_deb_binary_name))
        l_src_name = l_file_src_name.read().rstrip('\n')
        l_file_src_name.close()

        if (len(l_src_name) == 0):
            l_file_src_name = os.popen('dpkg --status %s 2>/dev/null|grep ^Package:|awk -F": " \'{print $2}\'' %(l_deb_binary_name))
            l_src_name = l_file_src_name.read().rstrip('\n')
            l_file_src_name.close()
            if(l_src_name == l_deb_src_name):
                l_file_ver_local = os.popen('dpkg -l %s 2>/dev/null| grep %s 2>/dev/null | awk -F" " \'{print $3}\' | head -n 1' %(l_deb_binary_name, l_deb_binary_name))
                l_ver_local = l_file_ver_local.read().rstrip('\n')
                l_file_ver_local.close()
            else:
                l_ver_local = "-"
        else:
            if(l_src_name == l_deb_src_name):
                l_file_ver_local = os.popen('dpkg -l %s 2>/dev/null| grep %s 2>/dev/null | awk -F" " \'{print $3}\' | head -n 1' %(l_deb_binary_name, l_deb_binary_name))
                l_ver_local = l_file_ver_local.read().rstrip('\n')
                l_file_ver_local.close()
    else:
        l_ver_local = "-"

    return l_ver_local

##====rpm获取二进制包版本====##  
def get_rpmpkg_local_verison(l_rpm_binary_name):
    # this function for get rpm pacgakes local verison
    # input: 
    #           @ l_rpm_binary_name
    # return:
    #           @ l_ver_local
    l_ver_local = "-"

    l_rpm_install_status = os.system('rpm -qi %s 2>/dev/null 1>/dev/null' %(l_rpm_binary_name))
    if (l_rpm_install_status == 0):
        l_file_ver_local = os.popen('rpm -qi %s 2>/dev/null | grep "Version\|Release" | awk -F" " \'{print $3}\' | sed \':label;N;s/\\n/-/;t label\'' %(l_rpm_binary_name))
        l_ver_local = l_file_ver_local.read().rstrip('\n')
        l_file_ver_local.close()

    return l_ver_local


libchecker_environment_init()
libchecker_checking_loop()
libchecker_over_jobs()
