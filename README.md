

#  OSAPIChecker

## 介绍

Operating system API compliance check tool. ----操作系统API符合性检查工具。

## 软件架构

支持全架构

## 安装教程

可以直接下载运行。

运行程序前，需要确定系统中有以下软件：

python 3.7+  
golang 1.13+  
python3-reportlab（或者使用pip安装reportlab）  
当系统使用的是RPM软件包格式时，需要安装rpmdevtools。

## 使用说明

程序包含1个主程序：OSAPIChecker，4个子程序：LibChecker、CmdChecker、FsChecker与ServiceChecker，以及一个PDF生成工具。使用方法如下:

### 1. 运行前环境准备：

1.1 检测的系统使用的软件包格式为deb，需要开启源码源：/etc/apt/source.list 下打开 deb-src，并更新：

```
sudo apt update
```

### 2. OSAPIChecker 主程序

OSAPIChecker是测试工具的主程序,将各个子模块进行汇总处理，并生成报告。

#### 2.1 运行方式

下载代码后，进入OSAPIChecker主目录，直接运行主程序：

```
cd OSAPIChecker
./OSAPIChecker.py
```

运行说明：

直接运行主程序，会使用默认的方式进行检测，默认参数如下（详细信息参见[1.2 参数解析]）：

```
--channel=all --strategy=basic  --level=l1l2 --ostype=desktop --pkgmngr=apt-deb    
```

#### 2.2 参数解析

```
./OSChecker.py [-h] [-c CHANNEL] [-s STRATEGY] [-l LEVEL] [-t OSTYPE] [-p PKGMNGR] [-o ORGANIZE] [-R]
```

解析：

 -h, --help:   
  显示帮助信息

 -c CHANNEL, --channel CHANNEL：   
  选择要测试子模块（libchecker,cmdchecker,fschecker,servicechecker）  
  默认是all：全部测试，依次调用4个子程序(Libchecker、CmdChecker、FsChecker与ServiceChecker)

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
  送测单位名称，默认是空

 -R, --reports  
  生成报告，默认不生成报告



### 3. LibChecker子程序

LibChecker是测试工具的中检测当前操作系统环境包含的动态库是否符合标准的工具。

#### 3.1 运行方式

运行子程序有两种方式，可以使用主程序单独调用，也可以单独运行子程序：

方式一：主程序调用子程序

```
./OSChecker.py --channel=libchecker
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



#### 3.2 参数解析

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

注：使用主程序单独调用子程序时，使用的参数与子程序基本一致，除了“-T TIMETMP”， 主程序中自己会获取当前的时间，并传入子程序中，不需要单独输入“-T TIMETMP”参数。

#### 3.3 日志

LibChecker 执行的日志位于: OSAPIChecker/Logs 下, 输出结果存放于: OSAPIChecker/Outputs 下.

### 4. CmdChecker

CmdChecker是一款检查操作系统内置命令是否符合标准的快捷工具

#### 4.1 运行方式

运行子程序有两种方式，可以使用主程序单独调用，也可以单独运行子程序：

方式一：主程序调用子程序

```
./OSChecker.py --channel=cmdchecker
```

方式二：单独运行子程序

```
python3 CmdChecker/cmd_checker.py
```

运行说明：

上述两种运行方式都是使用默认的json文件进行检测

#### 4.2 参数解析

```
usage: cmd_checker.py [-h] [-V] [-L cmd_list.json] [-P config.json] [-T filetime]
```

 解析：

 -h, --help:  
  显示帮助信息

 -V, --version:  
  显示当前程序版本信息

 -L cmd_list.json, --list cmd_list.json:  
  cmd_list的json文件  
  默认使用程序自带的json文件

 -P config.json, --path config.json :  
  cmd可能存在的路径配置文件  
  默认使用程序自带的json文件

 -T filetime, --timestamp :  
  filetime 文件时间戳  
  默认会自动获取当前时间，也可以自己指定时间信息。

注：使用主程序单独调用子程序时，使用的是默认的参数，不对此子程序做参数解析。

#### 4.3 日志

CmdChecker 输出结果存放于: OSAPIChecker/Outputs 下.

### 5. FsChecker

FsChecker是款检查操作系统文件系统是否符合标准的快捷工具

#### 5.1 运行方式

运行子程序有两种方式，可以使用主程序单独调用，也可以单独运行子程序：

方式一：主程序调用子程序

```
./OSChecker.py --channel=fschecker
```

方式二：单独运行子程序

```
python3 FsChecker/fs_checker.py
```

运行说明：

上述两种运行方式都是使用默认的json文件进行检测

#### 5.2 参数解析

```
usage: fs_checker.py [-h] [-V] [-L fs_list.json] [-T filetime]
```

 解析：

 -h, --help:   
  显示帮助信息

 -V, --version:   
  显示当前程序版本信息

 -L fs_list.json, --list fs_list.json:   
  fs_list的json文件    
  默认使用程序自带的json文件

 -T filetime, --timestamp :   
  filetime 文件时间戳    
  默认会自动获取当前时间，也可以自己指定时间信息。

注：使用主程序单独调用子程序时，使用的是默认的参数，不对此子程序做参数解析。

#### 5.3 日志

CmdChecker 输出结果存放于: OSAPIChecker/Outputs 下.

### 6. ServiceChecker

ServiceChecker 是一款检查操作系统管理软件systemd是否符合标准的快捷工具

#### 6.1 运行方式

运行子程序有两种方式，可以使用主程序单独调用，也可以单独运行子程序（注：子程序需要root权限）：

方式一：主程序调用子程序

```
sudo ./OSChecker.py --channel=servicechecker
```

方式二：单独运行子程序

```
sudo python3 ServiceChecker/service_checker.py
```

运行说明：

此项子程序无特殊配置项，故直接运行即可。

#### 6.2 日志

ServiceChecker 执行的日志位于: OSAPIChecker/Logs 下,输出结果存放于: OSAPIChecker/Outputs 下.

### 7. PDF生成工具

GenReport里存放的是json结果转pdf工具

#### 7.1 运行方式

```
cd GenReport
./pdf.py 
```

运行说明：

基本用法，直接执行使用默认路径生成pdf。

#### 7.2 参数解析

```
usage: pdf.py [-h] [-r RESULT] [-e ENV] [-l LIB] [-f FS] [-c CMD] [-s SERVER]
```

参数解析：
   
 -h, --help   
  显示帮助信息

 -r RESULT, --result RESULT   
  指定pdf生成结果路径

 -e ENV, --env ENV   
  指定环境检测结果路径

 -l LIB, --lib LIB   
  指定运行库检查结果文件路径
 	  	
 -f FS, --fs FS   
  指定文件系统层次结构检查结果文件路径

 -c CMD, --cmd CMD   
  指定常用命令检查结果文件路径

 -s SERVER, --server SERVER   
  指定服务检查结果文件路径

####  7.3 日志

ServiceChecker 执行的日志位于: OSAPIChecker/Logs 下,输出结果存放于: OSAPIChecker/Outputs 下.



## 常用举例说明

1、当我们想要检测桌面、DEB格式软件包、basic类型、L1L2级别的libchecker，以及其他三项子项目并需要生成检测报告时，可以运行以下命令：

```
./OSAPIChecker.py -R
或者
./OSAPIChecker.py --channel=all --strategy=basic --level=l1l2 --ostype=desktop --pkgmngr=apt-deb -R
```

以上两条命令输出结果一致。

2、当我们需要检测服务器、RPM格式软件包、basic类型、L1L2级别的libchecker，以及其他三项子项目并需要生成检测报告时，可以运行以下命令：

```
./OSAPIChecker.py --channel=all --strategy=basic --level=l1l2 --ostype=server --pkgmngr=yum-rpm -R
```

3、当我们需要检测服务器、RPM格式软件包、basic+expansion类型、L1L2级别的libchecker,可以运行以下命令：

```
./OSAPIChecker.py --channel=libchecker --strategy=with-expand --level=l1l2 --ostype=server --pkgmngr=yum-rpm
```

4、当我们需要检测服务器、RPM格式软件包、expansion类型、L1L2级别的libchecker,并单独生成报告时，可以运行以下命令：

```
./OSAPIChecker.py --channel=libchecker --strategy=expansion --level=l1l2 --ostype=server --pkgmngr=yum-rpm -R
```

