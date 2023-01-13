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
1. 检查系统systemd版本；
2. 目前自定义service、path、socket、timer、swap、target等单元配置文件，检查目标检测单元的起停及自定义配置功能实现；
3. 自定义开机自启动服务（enable）及开机禁止启动服务(disable)，重启环境后验证其功能。


## 结果说明
1. 工具生成检测结果路径为：Outputs/service_result.json；
2. 目标单元检测通过为：'pass'，检测失败为：'fail'，检测结果示例如下：


    {
        "Path Unit": {				    --Path单元检测
            "Check result": "pass/fail"
        },
        "Socket Unit": {				    --Socket单元检测
            "Check result": "pass/fail"
        },
        "Timer Unit": {				    --Timer单元检测
            "Check result": "pass/fail"
        },
        "Swap Unit": {				    --Swap单元检测
            "Check result": "pass/fail"
        },
        "Target Unit": {				    --Target单元检测
            "Check result": "pass/fail"
        },
        "Service enable": {				    --自定义开机自启动服务
            "Check result": "pass/fail"
        },
        "Service disable": {				    --自定义开机禁止启动服务
            "Check result": "pass/fail"
        }
    }
