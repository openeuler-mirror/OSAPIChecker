# FsChecker
fschecker  是一款检查操作系统文件系统是否符合标准的快捷工具
## 环境要求
python 3.7+

## 使用方法
1. 进入OSChecker主目录  
cd OSChecker  
2. 使用python3执行fschecker检查工具  
python3 FsChecker/fs_checker.py 
3. 常用参数  
usage: fs_checker.py [-h] [-V] [-L fs_list.json]  


    操作系统标准工具SIG FsChecker
    optional arguments:  
      -h, --help            show this help message and exit  
      -V, --version         show program's version number and exit  
      -L fs_list.json, --list fs_list.json
                            fs_list的json文件  

## 结果说明
    {
        "handler": "fs_checker",                ——子工具名
        "result": [                             ——结果集合
            {
                "FS_name": "/",                 ——检查目录或文件名
                "exist_check": {                ——存在性检查
                    "result": "pass"            ——检查结果
                },
                "file_permissions": "0775",     ——目录或文件权限
                "result": "pass"                ——综合检查结果
            },
            ……
        ]
    }