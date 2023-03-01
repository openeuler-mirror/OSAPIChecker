# CmdChecker

cmdchecker  是一款检查操作系统内置命令是否符合标准的快捷工具
## 环境要求
python 3.7+

## 使用方法
1. 进入OSChecker主目录  
cd OSChecker  
2. 使用python3执行cmdchecker检查工具   
python3 CmdChecker/cmd_checker.py  
3. 常用参数  
usage: cmd_checker.py [-h] [-V] [-L cmd_list.json] [-P config.json] [-T filetime]
    

    操作系统标准工具SIG CMDChecker  
    optional arguments:   
    -h, --help              show this help message and exit  
    -V, --version           show program's version number and exit  
    -L cmd_list.json, --list cmd_list.json
                            cmd_list的json文件
    -P config.json, --path config.json
                            cmd可能存在的路径配置文件  
    -T filetime, --timestamp filetime
                            文件时间戳

## 结果说明
    {
        "handler": "cmdchecker",            ——子工具名
        "result": [                         ——结果集合
            {
                "name": "ar",               ——检查命令
                "exist_check": {            ——命令存在性检查
                    "result": "pass"        ——检查结果
                },
                "run_check": {              ——命令运行检查
                    "result": "pass"        ——检查结果
                },
                "cmd_version": "2.34",      ——命令版本
                "cmd_path": "/usr/bin/ar",  ——命令实际路径
                "result": "pass"            ——综合测试结果
            },
            ……
        ]
    }