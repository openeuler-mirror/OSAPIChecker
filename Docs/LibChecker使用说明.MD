# CmdChecker

libchecker  是一款检查操作系统当前环境多包含的动态库是否符合标准的快捷工具
## 环境要求
python 3.7+

## 使用方法

#### 1. 运行方式

运行子程序有两种方式，可以使用主程序单独调用，也可以单独运行子程序：

方式一：主程序调用子程序

```
./OSChecker.py --channel=libchecker
或者
./OSChecker.py -c libchecker
```

方式二：单独运行子程序

```
python3 LibChecker/lib_checker.py
```

运行说明：

上述两种运行方式都是使用默认的方式进行检测，默认参数如下（详细信息参见[3.2 参数解析]）：

```
--strategy=basic  --level=l1l2 --ostype=desktop --pkgmngr=apt-deb    
```


#### 2 参数解析

```
python3 LibChecker/lib_checker.py [-h] [-s STRATEGY] [-l LEVEL] [-t OSTYPE] [-p PKGMNGR] [-o ORGANIZE] [-j JSON] [-T TIMETMP]
```

 解析：

 -h, --help:  
  显示帮助信息

 -s STRATEGY, --strategy STRATEGY:  
  选择测试的库的类型（basic、expansion、with-expand）  
  其中，with-expand是（basic+expansion）  
  默认是basic

 -l LEVEL, --level LEVEL:  
  选择测试的级别（l1、l2、l3或者是三者组合）  
  默认是l1l2  

 -t OSTYPE, --ostype OSTYPE:  
  选择测试的OS类型（desktop、server）  
  默认是desktop

 -p PKGMNGR, --pkgmngr PKGMNGR:  
  选择测试的软件包类别（apt-deb、yum-rpm）  
  默认是apt-deb

 -o ORGANIZE, --organize ORGANIZE  
  送测单位名称，默认是空

 -T TIMETMP, --timetmp TIMETMP  
  测试时间，默认会自动获取当前时间，也可以自己指定时间信息。


#### 3 日志

LibChecker 执行的日志位于: OSAPIChecker/Logs 下, 输出结果存放于: OSAPIChecker/Outputs 下.
