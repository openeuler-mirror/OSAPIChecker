#!/usr/bin/python3

import argparse
import json
import os

# 0. Global Resources Initialized
## 0.1 init dict and list data structures

g_pkginfodict_from_json = {}    # read pkacage info from json file
g_libinfodict_from_json = {}    # read library info from json file
g_bind_pkglib_from_json = {}    # bing package and library info
g_liblist_from_json = {}        # bing package and library info

g_pkginfodict_from_os = {}      # dict buffer for package info from current os
g_libinfodict_from_os = {}      # dict buffer for library info from current os
g_liblist_from_os = {}      # dict buffer for library info from current os

g_libchecker_comp_status = {}   # dict for libchecker compare result


## 0.2 init function was here
def libchecker_environment_init():
    print("Enter function: libchecker_environment_init")


# 1. Check Input Validity
## 1.1 check global variable and data structure
## 1.2 check os flag for other checker utlities


# 2. Get Meatdata Info from JSON File
## 2.1 read packages info from json file
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
def libchecker_read_stdjson_file(json_file_path):
    # this function read package and library info from json file
    # input: 
    #           @ json_file_path
    # output:
    #           @ g_pkginfodict_from_json
    #           @ g_libinfodict_from_json
    #           @ g_bing_pkglib_from_json
    # return:
    #           @ 
    print("Enter function: libchecker_open_json_file(%s)" %(json_file_path))
    fobj = open(json_file_path)

    file_data = json.load(fobj)

    for i in file_data['libraries']:
        g_pkginfodict_from_json[i['srcname']] = i['version']    # write pkginfo to dict: g_pkginfodict_from_json
        g_libinfodict_from_json[i['linkname']] = i['soname']    # write libinfo to dict: g_libinfodict_from_json
        g_bind_pkglib_from_json[i['srcname']] = i['linkname']   # write bindinfo to dict: g_bind_pkglib_from_json

    fobj.close()

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
    p_srcpkgver = os.popen('apt-cache showsrc %s | grep \^Version | cut -d '"\ "' -f 2 ' %(src_pkgname))
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
    p_srcpkgnam = os.popen('apt-cache show %s | grep Package | cut -d '"\ "' -f 2 ' %(src_pkgname))
    srcpkgnam = p_srcpkgnam.read().rstrip('\n')
    p_srcpkgnam.close()
    p_srcpkgver = os.popen('apt-cache show %s | grep Version | cut -d '"\ "' -f 2 ' %(src_pkgname))
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
    list1 = str(str1).split(".")
    list2 = str(str2).split(".")

    if str1 == str2:
        return "="
    elif str1 < str2:
        return "<"
    else:
        return ">"

## 3.2 get deb package info 
def get_debpkg_from_srcpkg(src_pkgname):
    # this function for get deb pacgakes from package name in current os
    # input: 
    #           @ src_pkgname
    # output:
    #           @ 
    # return:
    #           @ debpkgs
    print("Enter function: get_debpkg_from_srcpkg(%s)" %(src_pkgname))
    p_debpkgs = os.popen('apt-cache showsrc %s | grep Binary | cut -d '"\:"' -f 2- | cut -d '"\ "' -f 2- ' %(src_pkgname))
    debpkgs = p_debpkgs.read().split("\n")[0].split(", ")
    p_debpkgs.close()

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
    print("Enter function: libchecker_output_json_file()")
    output_info = {}
    output_data = json.loads(json.dumps(output_info))
    
    mateinfo = {}
    out_data_deep = {}
    
    result_dict = libchecker_compare_liblist()

    for key in result_dict:
        if result_dict[key] == 'false':
#            mateinfo = {"name" : key, "version" : "no exist", "status" : "not exist" , "category" : "exist", "otherinfo" : "no exist"}
            mateinfo = {"name" : pick_linkname_from_soname(key), "version" : key, "status" : 'not exist', "category" : "library", "otherinfo" : "none"}
        elif result_dict[key] == '<':
#            mateinfo = {"name" : key, "version" : result_dict[key], "status" : "incompatible", "category" : "library", "otherinfo" : "none"}
            mateinfo = {"name" : pick_linkname_from_soname(key), "version" : key, "status" : 'incompatible', "category" : "library", "otherinfo" : "none"}
        else:
#            mateinfo = {"name" : key, "version" : result_dict[key], "status" : "compatible", "category" : "library", "otherinfo" : "none"}
            mateinfo = {"name" : pick_linkname_from_soname(key), "version" : key, "status" : 'compatible', "category" : "library", "otherinfo" : "none"}
        
        #out_data_deep = {key : mateinfo}
        out_data_deep.update({key : mateinfo})
        output_data = {"libchecker": out_data_deep}

    json_output = json.dumps(output_data, ensure_ascii = False)

    with open("Outputs/libchecker-output.json","w") as f:
        json.dump(output_data,f)


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

print('========== Libchecker ==========')
libchecker_read_stdjson('StdLists/lib_list_1.0I-20220830-uos.json')
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
get_liblists_from_os()
#print(get_liblists_from_stdjson('../StdLists/lib_list_1.0I-20220830-uos.json'))
get_liblists_from_stdjson('StdLists/lib_list_1.0I-20220830-uos.json')

#print("g_liblist_from_json")
#print(g_liblist_from_json)
#print("g_liblist_from_os")
#print(g_liblist_from_os)

libchecker_compare_liblist()
libchecker_output_json_file()
