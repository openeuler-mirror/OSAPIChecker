# OSAPIChecker(主程序)

OSAPIChecker是测试工具的主程序,将各个子模块进行汇总处理。

## 环境要求
python 3.7+
golang 1.13+
python3-reportlab

## 使用方法
1. 进入OSChecker主目录  
./OSAPIChecker.py

2. 常用参数  
usage: OSChecker [-h] [-c CHANNEL] [-s STRATEGY] [-l LEVEL] [-t OSTYPE] [-p PKGMNGR] [-o ORGANIZE] [-R]
    
optional arguments:
  -h, --help            show this help message and exit
  -c CHANNEL, --channel CHANNEL
                        Choice OSAPIChecker channels:
                        libchecker,cmdchecker,fschecker,servicechecker,all
  -s STRATEGY, --strategy STRATEGY
                        Choice OSAPIChecker strategy: basic,expansion,with-
                        expand
  -l LEVEL, --level LEVEL
                        Choice OSAPIChecker level like: l1,l2,l3,l1l2,l1l2l3
  -t OSTYPE, --ostype OSTYPE
                        OSType of current OS: desktop, server
  -p PKGMNGR, --pkgmngr PKGMNGR
                        Package Manager of current OS: apt-deb, yum-rpm
  -o ORGANIZE, --organize ORGANIZE
                        Choice Organize  
  -R, --reports         Generate Reports

参数解析：
-h, --help:
    显示帮助信息
-c CHANNEL, --channel CHANNEL： 
    选择要测试子模块（libchecker,cmdchecker,fschecker,servicechecker）
    默认是all--全部测试
-s STRATEGY, --strategy STRATEGY:
    选择libchecker测试的库的类型（basic、expansion、with-expand）
    其中，with-expand是（basic+expansion）
    默认是basic
-l LEVEL, --level LEVEL:
    选择libchecker测试的级别（l1、l2、l3或者是三者组合）
    默认是l1l2
-t OSTYPE, --ostype OSTYPE:
    选择libchecker测试的OS类型（desktop、server）
    默认是desktop
-p PKGMNGR, --pkgmngr PKGMNGR:
    选择libchecker测试的软件包类别（apt-deb、yum-rpm）
    默认是apt-deb
-o ORGANIZE, --organize ORGANIZE
    送测单位名称
    默认是空
-R, --reports
    生成报告（默认不生成报告）


3. 注意
1) 在进行测试时，请根据需要填写必要的参数信息
2) 当前除libchecker外，其他子模块使用的默认配置，当前主程序不做单独配置处理（部分工具存在参数冲突）, 若有需要, 请单独运行子模块程序
