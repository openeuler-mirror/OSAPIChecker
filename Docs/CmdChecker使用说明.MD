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
usage: cmd_checker.py [-h] [-V] [-L cmd_list.json] [-P config.json]  

操作系统标准工具SIG CMDChecker  
optional arguments:   
  -h, --help            show this help message and exit  
  -V, --version         show program's version number and exit  
  -L cmd_list.json, --list cmd_list.json
                        cmd_list的json文件
  -P config.json, --path config.json
                        cmd可能存在的路径配置文件  