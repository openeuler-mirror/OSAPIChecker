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
import subprocess 

# -1. Inherit arguments from CUI
# there are some arguments match with main program 
    ## --strategy: 
    ## --level:
    ## --ostype:
    ## --pkgmngr:
    ## --json:
parser = argparse.ArgumentParser(description="This Progermm is a OSChecker", prog="OSChecker")
parser.add_argument('-s', '--strategy', action='store', type=str, help='Choice OSAPIChecker strategy: basic,expansion,with-expand', default="basic")
parser.add_argument('-l', '--level', action='store', type=str, help='Choice OSAPIChecker level: l1,l2,l3,l1l2,l1l2l3', default="l1l2")
parser.add_argument('-t', '--ostype', action='store', type=str, help='OSType of current OS: desktop, server', default="desktop")
parser.add_argument('-p', '--pkgmngr', action='store', type=str, help='Package Manager of current OS: apt-deb, yum-rpm', default="apt-deb")
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
g_cpu_type = os.popen('uname -m').read().rstrip('\n')
g_output_filename = "Outputs/libchecker-output_" + g_cpu_type + "_" + g_time_stamp + ".json"
g_output_logname = "Logs/libchecker_" + g_time_stamp + ".log"

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

g_jsonfile_dict = {}            # a josn file struct
g_counter_flags = {}            # a conuter struct 
g_storejsondict = {}
g_genresults_to_json = {}

## 0.2 a recycle call function for user
def libchecker_over_jobs():
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

    print("标准信息:")
    print("\t标准简要信息:")
    print("\t\t标准号: %s" % f_dict['std_description']['std_number'])
    print("\t\t文件名: %s" % f_dict['std_description']['std_name'])
    print("\t库检查器信息:")
    print("\t\t检查位置: %s" % f_dict['libs']['lib_location'])

def libchecker_environment_init():
    global g_counter_flags

    #g_counter_flags = {'pkg_counter': {'total': {'all' : 0, 'l1' : 0, 'l2' : 0, 'l3' : 0} , 'passed': {'all': 0, 'l1' : 0, 'l2' : 0, 'l3' : 0}, 'warning': {'all': 0, 'l1' : 0, 'l2' : 0, 'l3' : 0}, 'failed': {'all' : 0, 'l1' : 0, 'l2' : 0, 'l3' : 0} }, 'lib_counter': {'total': 0, 'passed': 0, 'warning': 0, 'failed': 0}}
    g_counter_flags = {
            'pkg_counter': {
                'total': {
                    'all' : 0, 'l1' : 0, 'l2' : 0, 'l3' : 0
                    } , 
                'passed': {
                    'all': 0, 'l1' : 0, 'l2' : 0, 'l3' : 0
                    }, 
                'warning': {
                    'all': 0, 'l1' : 0, 'l2' : 0, 'l3' : 0
                    }, 
                'failed': {
                    'all' : 0, 'l1' : 0, 'l2' : 0, 'l3' : 0
                    }
                }, 
            'lib_counter': {
                'total': {
                    'all' : 0, 'l1' : 0, 'l2' : 0, 'l3' : 0
                    } , 
                'passed': {
                    'all': 0, 'l1' : 0, 'l2' : 0, 'l3' : 0
                    }, 
                'warning': {
                    'all': 0, 'l1' : 0, 'l2' : 0, 'l3' : 0
                    }, 
                'failed': {
                    'all' : 0, 'l1' : 0, 'l2' : 0, 'l3' : 0
                    }
                }
            }

    get_env_info()
    get_stdjsons_info('Jsons/lib_list.json')
    
def get_src_alias_list (dict_name, l_realname):
    l_list_src = []

    l_alias_version = '-'
    l_alias_name = '-'
    l_src_dict = {}
    
    l_src_dict.update({l_realname: {'version': dict_name[l_realname]['version'][g_inputostype]}})
    if(len(dict_name[l_realname]['alias']) >= 0):
        for i in range(0, len(dict_name[l_realname]['alias'])):
            l_alias_name = dict_name[l_realname]['alias'][i]['name']
            if (l_alias_name != l_realname):
                l_alias_version = dict_name[l_realname]['alias'][i]['version'][g_inputostype]
                l_src_dict.update({l_alias_name: {'version': l_alias_version}})

    return l_src_dict

def check_per_pkg_info(dict_name, l_src_name):
    global g_notfind_set_flag
    global g_counter_flags
    srcpkgver = []

    if (g_inputpkgmngr == "apt-deb"):
        l_search_pname = os.popen('apt-cache showsrc %s 2>/dev/null | grep ^Package: | awk -F": " \'{print $2}\'' %(l_src_name))
        l_pname = l_search_pname.read().split("\n")[0]
        l_search_pname.close()
        if(l_pname == l_src_name):
            p_srcpkgver = os.popen('apt-cache showsrc %s 2>/dev/null | grep \^Version | cut -d '"\ "' -f 2 ' %(l_src_name))
            srcpkgver = p_srcpkgver.read().rstrip('\n')
            p_srcpkgver.close()
    elif (g_inputpkgmngr == "yum-rpm"):
        cmd="rpm -qa --queryformat=\"%{SOURCERPM}\\n\" 2>/dev/null | grep ^" + l_src_name + " | uniq"
        p_srcpkgver = subprocess.getstatusoutput(cmd)
        src_list = p_srcpkgver[1].split('\n')
        if (len(src_list) != 0):
            for x in range(0, len(src_list)):
                s_str=l_src_name + "-"
                if (len(src_list[x].split(s_str)) > 1):
                    if (src_list[x].split(s_str)[1][0].isdigit()):
                        srcpkgver = src_list[x].split(s_str)[1].split('-')[0]
                        #srcpkgver = src_list[x].split(s_str)[1].split('.src.rpm')[0]
        else:
            srcpkgver = src_list


    print("\t\t系统实现: ")
    if (len(srcpkgver) == 0):
        print("\t\t\t\t未发现  -> ", l_src_name.ljust(20))
        return None
    else:
        print("\t\t\t\t实现包名 -> ", l_src_name.ljust(20),"实现版本 -> ",srcpkgver)
        return l_src_name

##====查询共享库路径信息====##
def check_sharelib_info(lib_soname):

    global g_lib_location_path
    g_lib_location_path = "0"

    l_list = ["/lib", "/lib64", "/usr/lib", "/usr/lib64"]

    for path_tmp in l_list:
        for realpath, dirs, files in os.walk(path_tmp):
            if lib_soname in files:
                full_path = os.path.join(path_tmp, realpath, lib_soname)
                g_lib_location_path = (os.path.normpath(os.path.abspath(full_path)))
                break

        if g_lib_location_path != "0":
            break
        
    if g_lib_location_path == "0":
        return "not found"
    else:
        return g_lib_location_path

def get_packages_binary_info (dict_name, key):
    l_src_list_update = []
    l_list_binary_name = []
    l_dict_alias_info = {}
    l_dict_src_info = {}

    global g_counter_flags

    l_dict_src_info = get_src_alias_list (dict_name, key)
    for l in l_dict_src_info:
        src_name_status = check_per_pkg_info(dict_name, l)
        if (src_name_status != None):
            l_list_binary_name = get_all_binary_list (l)
            if(len(l_list_binary_name) != 0):
                l_dict_binary_name = {}
                for j in range(0, len(l_list_binary_name)):
                    l_local_version = {} 
                    l_dict_binary_name.update({l_list_binary_name[j]: {'status':'-','version':'-'}})
                    if (g_inputpkgmngr == "yum-rpm"):
                        l_local_version = get_rpmpkg_local_version(l_list_binary_name[j], l_dict_src_info[l]['version'])
                    else:
                        l_local_version = get_debpkg_local_version(l_list_binary_name[j], l_dict_src_info[l]['version'])
                    l_dict_binary_name.update({l_list_binary_name[j]: l_local_version})
                l_dict_alias_info[l] = l_dict_binary_name

    old_failed_num = g_counter_flags['pkg_counter']['failed']['all']
    for p_a in l_dict_alias_info:
        for p_b in l_dict_alias_info[p_a]:
            if (l_dict_alias_info[p_a][p_b]['status'] == "incompatible"):
                g_counter_flags['pkg_counter']['failed']['all'] += 1
                if (dict_name[key]['necessity'][g_inputostype]['level'].lower() == "l1" ):
                    g_counter_flags['pkg_counter']['failed']['l1'] += 1
                elif (dict_name[key]['necessity'][g_inputostype]['level'].lower() == "l2" ):
                    g_counter_flags['pkg_counter']['failed']['l2'] += 1
                elif (dict_name[key]['necessity'][g_inputostype]['level'].lower() == "l3" ):
                    g_counter_flags['pkg_counter']['failed']['l3'] += 1
                break
        new_failed_num = g_counter_flags['pkg_counter']['failed']['all']
        if (new_failed_num > old_failed_num): 
                break

    with open(g_output_filename, 'r') as fr:
        json_alias_info = json.load(fr)
        json_alias_info[key]['Binary package'] =  l_dict_alias_info
    with open(g_output_filename, 'w+') as fw:
        json.dump(json_alias_info,fw,ensure_ascii=False,indent=4)

##====主函数====##
def libchecker_checking_loop():
    global g_genresults_to_json
    global g_storejsondict

    l_strategy_list = ['basic', 'expansion', 'with-expand']
    
    del g_jsonfile_dict['libs']['category']['##章节名']
    print("")
    print("开始检查： ",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"")
    for chapter_class in g_jsonfile_dict['libs']['category']:
        l_tmp_dict = {}
        if chapter_class == 'base':
            l_tmp_dict = g_jsonfile_dict['libs']['category']['base']['packages']
            del l_tmp_dict['##glibc']
        else:
            l_tmp_dict = g_jsonfile_dict['libs']['category'][chapter_class]['packages']
        for key in l_tmp_dict:   
            l_level = l_tmp_dict[key]['necessity'][g_inputostype]['level'].lower()
            l_strategy = l_tmp_dict[key]['necessity'][g_inputostype]['options'] 
            if (l_level in g_inputlevel):
                if (g_inputstrategy == "with-expand") or (g_inputstrategy == l_strategy):
                    g_storejsondict[key] = l_tmp_dict[key]

    for key4 in g_storejsondict:
        l_dict_to_json={'Level': 'gen', 'Shared library':'gen', 'Required version': 'gen', 'Binary package':'gen'}
        g_genresults_to_json.update({ key4 : l_dict_to_json })

    with open(g_output_filename,"w") as f:
        json.dump(g_genresults_to_json,f)

    for last_key in g_storejsondict: 
        print("=============================================================================================================")
        print("\t正在检查 ", '<',last_key,'>', "...")
        print("\t\t标准约定:")
        print("\t\t\t\t从属章节 -> ", g_storejsondict[last_key]['sections_number'].ljust(20), "兼容级别 -> ", g_storejsondict[last_key]['necessity'][g_inputostype]['level'].ljust(20))
        print("\t\t\t\t标准包名 -> " ,last_key.ljust(20),"标准版本 -> ", g_storejsondict[last_key]['version'][g_inputostype].ljust(20))

        with open(g_output_filename, 'r') as fr:
            json_level = json.load(fr)
            json_level[last_key]['Level'] = g_storejsondict[last_key]['necessity'][g_inputostype]['level']
            json_level[last_key]['Required version'] = g_storejsondict[last_key]['version'][g_inputostype]
        with open(g_output_filename, 'w+') as fw:
            json.dump(json_level,fw,ensure_ascii=False,indent=4)

        g_counter_flags['pkg_counter']['total']['all'] += 1
        if (g_storejsondict[last_key]['necessity'][g_inputostype]['level'].lower() == "l1" ):
            g_counter_flags['pkg_counter']['total']['l1'] += 1
        elif (g_storejsondict[last_key]['necessity'][g_inputostype]['level'].lower() == "l2" ):
            g_counter_flags['pkg_counter']['total']['l2'] += 1
        elif (g_storejsondict[last_key]['necessity'][g_inputostype]['level'].lower() == "l3" ):
            g_counter_flags['pkg_counter']['total']['l3'] += 1

        get_packages_binary_info (g_storejsondict, last_key)

        print("\t\t共享库信息:")
        l_subresults_to_json = {}
        for list1_item in g_storejsondict[last_key]['share_objs'][g_inputostype]:
            print("\t\t\t\t名称 -> ",list1_item)
            print("\t\t\t\t\t标准约定 -> ",list1_item)
            lib_result = check_sharelib_info(list1_item)
            print("\t\t\t\t\t系统存在 -> ",lib_result)
            temp_libsoname = lib_result.split('/')[-1]
            if (lib_result == "not found"):
                print("\t\t\t\t\t文件所属 -> ", None)
                print("\t\t\t\t\t检测结果 ->  未检测到存在")
                l_subresults_to_json.update({list1_item: {'status': 'not found', 'path':'-', 'belongs':'None'}})
                if (g_storejsondict[last_key]['necessity'][g_inputostype]['level'].lower() == "l1" ):
                    g_counter_flags['lib_counter']['failed']['l1'] += 1
                elif (g_storejsondict[last_key]['necessity'][g_inputostype]['level'].lower() == "l2" ):
                    g_counter_flags['lib_counter']['failed']['l2'] += 1
                elif (g_storejsondict[last_key]['necessity'][g_inputostype]['level'].lower() == "l3" ):
                    g_counter_flags['lib_counter']['failed']['l3'] += 1
            else:
                if (g_inputpkgmngr == "yum-rpm"):
                    l_file_belongs = get_rpm_file_belongs_package(lib_result)
                else:
                    l_file_belongs = get_deb_file_belongs_package(lib_result)
                print("\t\t\t\t\t文件所属 -> ", l_file_belongs)
                l_check_version = compare_library_version(temp_libsoname, str(list1_item))
                if (l_check_version == "equal") or (l_check_version == "bigger"):
                    #g_counter_flags['lib_counter']['passed'] += 1
                    l_subresults_to_json.update({list1_item: {'status': 'compatible', 'path':lib_result, 'belongs':l_file_belongs}})
                    if (g_storejsondict[last_key]['necessity'][g_inputostype]['level'].lower() == "l1" ):
                        g_counter_flags['lib_counter']['passed']['l1'] += 1
                    elif (g_storejsondict[last_key]['necessity'][g_inputostype]['level'].lower() == "l2" ):
                        g_counter_flags['lib_counter']['passed']['l2'] += 1
                    elif (g_storejsondict[last_key]['necessity'][g_inputostype]['level'].lower() == "l3" ):
                        g_counter_flags['lib_counter']['passed']['l3'] += 1
                else:
                    #g_counter_flags['lib_counter']['failed'] += 1
                    l_subresults_to_json.update({list1_item: {'status': 'incompatible', 'path':lib_result, 'belongs':l_file_belongs}})
                    if (g_storejsondict[last_key]['necessity'][g_inputostype]['level'].lower() == "l1" ):
                        g_counter_flags['lib_counter']['failed']['l1'] += 1
                    elif (g_storejsondict[last_key]['necessity'][g_inputostype]['level'].lower() == "l2" ):
                        g_counter_flags['lib_counter']['failed']['l2'] += 1
                    elif (g_storejsondict[last_key]['necessity'][g_inputostype]['level'].lower() == "l3" ):
                        g_counter_flags['lib_counter']['failed']['l3'] += 1

                print("\t\t\t\t\t检测结果 -> ", l_check_version)

            with open(g_output_filename, 'r') as fr:
                json_so = json.load(fr)
                json_so[last_key]['Shared library'] = l_subresults_to_json
            with open(g_output_filename, 'w+') as fw:
                json.dump(json_so,fw,ensure_ascii=False,indent=4)

    ## 软件包
    g_counter_flags['pkg_counter']['passed']['all'] = g_counter_flags['pkg_counter']['total']['all'] - g_counter_flags['pkg_counter']['failed']['all']
    g_counter_flags['pkg_counter']['passed']['l1'] = g_counter_flags['pkg_counter']['total']['l1'] - g_counter_flags['pkg_counter']['failed']['l1']
    g_counter_flags['pkg_counter']['passed']['l2'] = g_counter_flags['pkg_counter']['total']['l2'] - g_counter_flags['pkg_counter']['failed']['l2']
    g_counter_flags['pkg_counter']['passed']['l3'] = g_counter_flags['pkg_counter']['total']['l3'] - g_counter_flags['pkg_counter']['failed']['l3']

    ## 动态库
    g_counter_flags['lib_counter']['passed']['all'] = g_counter_flags['lib_counter']['passed']['l1'] + g_counter_flags['lib_counter']['passed']['l2'] + g_counter_flags['lib_counter']['passed']['l3']
    g_counter_flags['lib_counter']['failed']['all'] = g_counter_flags['lib_counter']['failed']['l1'] + g_counter_flags['lib_counter']['failed']['l2'] + g_counter_flags['lib_counter']['failed']['l3']
    g_counter_flags['lib_counter']['total']['l1'] = g_counter_flags['lib_counter']['passed']['l1'] + g_counter_flags['lib_counter']['failed']['l1']
    g_counter_flags['lib_counter']['total']['l2'] = g_counter_flags['lib_counter']['passed']['l2'] + g_counter_flags['lib_counter']['failed']['l2']
    g_counter_flags['lib_counter']['total']['l3'] = g_counter_flags['lib_counter']['passed']['l3'] + g_counter_flags['lib_counter']['failed']['l3']
    g_counter_flags['lib_counter']['total']['all'] = g_counter_flags['lib_counter']['passed']['all'] + g_counter_flags['lib_counter']['failed']['all']

    print("=============================================================================================================")
    print("结束检查 ",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    print("")
    print("\t检查策略：", "\"",  "--strategy =",args.strategy, "--level =",args.level, "--ostype =", args.ostype, "--pkgmngr =", args.pkgmngr, "--organize =", args.organize, "\"")
    print("")
    print("\t软件包:")
    print(("\t\t总计: %s" %(g_counter_flags['pkg_counter']['total']['all'])).ljust(10), ("(L1--->%s," %(g_counter_flags['pkg_counter']['total']['l1'])).ljust(10), ("L2--->%s," %(g_counter_flags['pkg_counter']['total']['l2'])).ljust(10), ("L3--->%s)" %(g_counter_flags['pkg_counter']['total']['l3'])).ljust(10))
    print(("\t\t通过: %s" %(g_counter_flags['pkg_counter']['passed']['all'])).ljust(10), ("(L1--->%s," %(g_counter_flags['pkg_counter']['passed']['l1'])).ljust(10), ("L2--->%s," %(g_counter_flags['pkg_counter']['passed']['l2'])).ljust(10), ("L3--->%s)" %(g_counter_flags['pkg_counter']['passed']['l3'])).ljust(10))
    print(("\t\t报错: %s" %(g_counter_flags['pkg_counter']['failed']['all'])).ljust(10), ("(L1--->%s," %(g_counter_flags['pkg_counter']['failed']['l1'])).ljust(10), ("L2--->%s," %(g_counter_flags['pkg_counter']['failed']['l2'])).ljust(10), ("L3--->%s)" %(g_counter_flags['pkg_counter']['failed']['l3'])).ljust(10))
    print("\t动态库:")
    print(("\t\t总计: %s" %(g_counter_flags['lib_counter']['total']['all'])).ljust(10), ("(L1--->%s," %(g_counter_flags['lib_counter']['total']['l1'])).ljust(10), ("L2--->%s," %(g_counter_flags['lib_counter']['total']['l2'])).ljust(10), ("L3--->%s)" %(g_counter_flags['lib_counter']['total']['l3'])).ljust(10))
    print(("\t\t通过: %s" %(g_counter_flags['lib_counter']['passed']['all'])).ljust(10), ("(L1--->%s," %(g_counter_flags['lib_counter']['passed']['l1'])).ljust(10), ("L2--->%s," %(g_counter_flags['lib_counter']['passed']['l2'])).ljust(10), ("L3--->%s)" %(g_counter_flags['lib_counter']['passed']['l3'])).ljust(10))
    print(("\t\t报错: %s" %(g_counter_flags['lib_counter']['failed']['all'])).ljust(10), ("(L1--->%s," %(g_counter_flags['lib_counter']['failed']['l1'])).ljust(10), ("L2--->%s," %(g_counter_flags['lib_counter']['failed']['l2'])).ljust(10), ("L3--->%s)" %(g_counter_flags['lib_counter']['failed']['l3'])).ljust(10))
    print("")
    print("=============================================================================================================")

##====deb查询文件所属二进制包====##
def get_deb_file_belongs_package(l_deb_file_name):
    # this function for get deb pacgakes to which the file belongs
    # input: 
    #           @ l_deb_file_name
    # return:
    #           @ l_deb_binary_name
    # 真实路径（排除链接文件）
    #l_deb_realpath = os.path.realpath(l_deb_file_name)
    #l_file_belongs_deb = os.popen('dpkg -S %s 2>/dev/null | awk -F": " \'{print $1}\'' %(l_deb_realpath))
    #l_belongs_deb = l_file_belongs_deb.read().rsplit('\n')[0]
    #l_file_belongs_deb.close()
    # 查询到的路径（查询到的第一个） + 真实路径
    l_deb_realpath = os.path.realpath(l_deb_file_name)
    l_file_belongs_status = subprocess.getstatusoutput('dpkg -S %s 2>/dev/null | awk -F": " \'{print $1}\'' %(l_deb_file_name))
    l_belongs_status = l_file_belongs_status[0]
    l_belongs_info = l_file_belongs_status[1]
    if (len(l_belongs_info) == 0):
        l_real_belongs_status = subprocess.getstatusoutput('dpkg -S %s 2>/dev/null | awk -F": " \'{print $1}\'' %(l_deb_realpath))
        if (len(l_real_belongs_status[1]) != 0):
            l_belongs_info = l_real_belongs_status[1]
    #print("status:", l_belongs_status , "info:" , l_belongs_info)
    #print("len(info):", len(l_belongs_info))

    l_belongs_deb = l_belongs_info

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
    l_rpm_realpath = os.path.realpath(l_rpm_file_name)
    l_file_belongs_rpm = subprocess.getstatusoutput('rpm -qf %s 2>/dev/null ' %(l_rpm_realpath))

    if (l_file_belongs_rpm[0] != 0):
        l_belongs_rpm = "None"
    else:
        l_belongs_rpm = l_file_belongs_rpm [1]
    
    return l_belongs_rpm 

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
    compare_result = subprocess.getstatusoutput('rpmdev-vercmp  %s %s 2>/dev/null ' %(str(l_local_ver), str(l_required_ver)))
    if (compare_result[0] == 0):
        return "compatible"
    elif (compare_result[0] == 11):
        return "compatible"
    else:
        return "incompatible"
    
    #if l_local_ver < l_required_ver:
    #    return "incompatible"
    #else:
    #    return "compatible"

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

def get_all_binary_list (l_srcname):
    if (g_inputpkgmngr == "yum-rpm"):
        l_list_binary_name = get_rpmpkg_from_srcpkg(l_srcname)
    else:
        l_list_binary_name = get_debpkg_from_srcpkg(l_srcname)
    return l_list_binary_name

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
    #l_rpmpkgs = os.popen('dnf info | grep -B 5 -E "%s.*.src.rpm" | grep "Name" | awk -F" " \'{ print $3 }\' | sort -n | uniq | sed \':label;N;s/\\n/ /;t label\'' %(l_rpm_srcname))
    #l_list_rpmpkgs = l_rpmpkgs.read().split("\n")[0].split(" ")
    #l_rpmpkgs.close()
    l_rpmpkgs = subprocess.getstatusoutput("dnf repoquery -q --queryformat \"%%{sourcerpm} %%{name}\"| grep -E \"^%s-[0-9]\" | awk '{print $2}'" %(l_rpm_srcname)) 
    l_list_rpmpkgs = l_rpmpkgs[1].split("\n")
    #print (l_list_rpmpkgs)

    return l_list_rpmpkgs

##====deb获取二进制包版本====##  
def get_debpkg_local_version(l_deb_binary_name, l_req_version):
    # this function for get deb pacgakes local verison
    # input: 
    #           @ l_deb_binary_name
    # return:
    #           @ l_ver_local
    l_ver = "-"
    l_status = "-"
    binary_info = {}

    l_file_deb_install_status = os.popen('dpkg -l %s 2>/dev/null| grep %s 2>/dev/null | awk -F" " \'{print $1}\' | head -n 1' %(l_deb_binary_name, l_deb_binary_name))
    l_deb_install_status = l_file_deb_install_status.read().rstrip('\n')
    l_file_deb_install_status.close()

    if(l_deb_install_status != "ii"):
        l_status = "not installed"
        l_ver = "-"
    else:
        l_file_ver_local = os.popen('dpkg -l %s 2>/dev/null| grep %s 2>/dev/null | awk -F" " \'{print $3}\' | head -n 1' %(l_deb_binary_name, l_deb_binary_name))
        l_ver = l_file_ver_local.read().rstrip('\n')
        l_file_ver_local.close()
        l_status = get_debpkg_ver_contrast(l_ver, l_req_version)
    binary_info = {'status':l_status, 'version': l_ver}

    return binary_info

##====rpm获取二进制包版本====##  
def get_rpmpkg_local_version(l_rpm_binary_name, l_req_version):
    # this function for get rpm pacgakes local verison
    # input: 
    #           @ l_rpm_binary_name
    # return:
    #           @ l_ver_local
    l_ver_local = "-"
    l_status = "-"
    binary_info = {}

    l_rpm_install_status = os.system('rpm -qi %s 2>/dev/null 1>/dev/null' %(l_rpm_binary_name))
    if (l_rpm_install_status == 0):
        #l_file_ver_local = os.popen('rpm -qi %s 2>/dev/null | grep "Version\|Release" | awk -F" " \'{print $3}\' | sed \':label;N;s/\\n/-/;t label\'' %(l_rpm_binary_name))
        l_file_ver_local = os.popen('rpm -qa --queryformat="%%{VERSION}\n" %s 2>/dev/null ' %(l_rpm_binary_name))
        l_ver = l_file_ver_local.read().rstrip('\n')
        l_file_ver_local.close()
        l_status = get_rpmpkg_ver_contrast(l_ver, l_req_version)
    else:
        l_status = "not installed"
        l_ver = "-"
    binary_info = {'status':l_status, 'version': l_ver}

    return binary_info


libchecker_environment_init()
libchecker_checking_loop()
libchecker_over_jobs()
