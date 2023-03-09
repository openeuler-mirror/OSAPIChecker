# OSAPIChecker(主程序)

OSAPIChecker是测试工具的主程序,将各个子模块进行汇总处理。

## 环境要求

python 3.7+  
golang 1.13+  
python3-reportlab


## 使用方法  

1. 进入OSChecker主目录  

&emsp;&emsp;./OSAPIChecker.py

2. 常用参数  

&emsp;&emsp;usage: OSChecker [-h] [-c CHANNEL] [-s STRATEGY] [-l LEVEL] [-t OSTYPE] [-p PKGMNGR] [-o ORGANIZE] [-R] 
   
&emsp;&emsp;optional arguments:  
&emsp;&emsp;&emsp;-h, --help  
&emsp;&emsp;&emsp;&emsp;&emsp;show this help message and exit  
  
&emsp;&emsp;&emsp;-c CHANNEL, --channel CHANNEL  
&emsp;&emsp;&emsp;&emsp;&emsp;Choice OSAPIChecker channels:  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;libchecker,cmdchecker,fschecker,servicechecker,all  
  
&emsp;&emsp;&emsp;-s STRATEGY, --strategy STRATEGY  
&emsp;&emsp;&emsp;&emsp;&emsp;Choice OSAPIChecker strategy: basic,expansion,with-expand
  
&emsp;&emsp;&emsp;-l LEVEL, --level LEVEL  
&emsp;&emsp;&emsp;&emsp;&emsp;Choice OSAPIChecker level like: l1,l2,l3,l1l2,l1l2l3  
  
&emsp;&emsp;&emsp;-t OSTYPE, --ostype OSTYPE  
&emsp;&emsp;&emsp;&emsp;&emsp;OSType of current OS: desktop, server  
  
&emsp;&emsp;&emsp;-p PKGMNGR, --pkgmngr PKGMNGR  
&emsp;&emsp;&emsp;&emsp;&emsp;Package Manager of current OS: apt-deb, yum-rpm  
  
&emsp;&emsp;&emsp;-o ORGANIZE, --organize ORGANIZE  
&emsp;&emsp;&emsp;&emsp;&emsp;Choice Organize    
  
&emsp;&emsp;&emsp;-R, --reports         
&emsp;&emsp;&emsp;&emsp;&emsp;Generate Reports  
  
&emsp;&emsp;参数解析：  
  
&emsp;&emsp;&emsp;-h, --help:  
&emsp;&emsp;&emsp;&emsp;&emsp;显示帮助信息  
  
&emsp;&emsp;&emsp;-c CHANNEL, --channel CHANNEL：     
&emsp;&emsp;&emsp;&emsp;&emsp;选择要测试子模块（libchecker,cmdchecker,fschecker,servicechecker）  
&emsp;&emsp;&emsp;&emsp;&emsp;默认是all--全部测试  
  
&emsp;&emsp;&emsp;-s STRATEGY, --strategy STRATEGY:  
&emsp;&emsp;&emsp;&emsp;&emsp;选择libchecker测试的库的类型（basic、expansion、with-expand）  
&emsp;&emsp;&emsp;&emsp;&emsp;其中，with-expand是（basic+expansion）  
&emsp;&emsp;&emsp;&emsp;&emsp;默认是basic  
  
&emsp;&emsp;&emsp;-l LEVEL, --level LEVEL:  
&emsp;&emsp;&emsp;&emsp;&emsp;选择libchecker测试的级别（l1、l2、l3或者是三者组合）  
&emsp;&emsp;&emsp;&emsp;&emsp;默认是l1l2  
  
&emsp;&emsp;&emsp;-t OSTYPE, --ostype OSTYPE:  
&emsp;&emsp;&emsp;&emsp;&emsp;选择libchecker测试的OS类型（desktop、server）  
&emsp;&emsp;&emsp;&emsp;&emsp;默认是desktop  
  
&emsp;&emsp;&emsp;-p PKGMNGR, --pkgmngr PKGMNGR:  
&emsp;&emsp;&emsp;&emsp;&emsp;选择libchecker测试的软件包类别（apt-deb、yum-rpm）  
&emsp;&emsp;&emsp;&emsp;&emsp;默认是apt-deb  
  
&emsp;&emsp;&emsp;-o ORGANIZE, --organize ORGANIZE  
&emsp;&emsp;&emsp;&emsp;&emsp;送测单位名称，默认是空    
  
&emsp;&emsp;&emsp;-R, --reports    
&emsp;&emsp;&emsp;&emsp;&emsp;生成报告，默认不生成报告  
  
3. 注意   
&emsp;1) 在进行测试时，请根据需要填写必要的参数信息   
&emsp;2) 当前除libchecker外，其他子模块使用的默认配置，当前主程序不做单独配置处理（部分工具存在参数冲突）, 若有需要, 请单独运行子模块程序

