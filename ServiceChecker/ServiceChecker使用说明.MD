# ServiceChecker
Servicechecker  是一款检查操作系统管理软件systemd是否符合标准的快捷工具
## 环境要求
python 3.7+
golang 1.13+


## 使用方法
1. 使用root用户执行该模块

2. 进入ServiceChecker主目录  
cd ServiceChecker

3. 使用python3执行ServiceChecker检查工具  
python3 service_checker.py

## 检查内容
1. 检查systemd版本；
2. 目前检查系统service、path、socket、timer等单元的起停及基本功能。
