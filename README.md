# OSAPIChecker

#### 介绍
Operating system API compliance check tool.

#### 软件架构
软件架构说明


#### 安装教程

1.  xxxx
2.  xxxx
3.  xxxx

#### 使用说明

0. OSAPIChecker
![alpha](Docs/01-GUIs/alpha-01.png)

1. LibChecker

   1. 基本用法

      ```shell
      # 1. /etc/apt/source.list 下打开 deb-src.
      # 2. 执行 sudo apt update.
      # 3. (OSAPIChecker)/$: ./OSAPIChecker.py --channel=libchecker [--strategy=base --level=l1l2]
      # 4. LibChecker 执行的日志位于: (OSAPIChecker)/Logs 下, 输出结果存放于: (OSAPIChecker)/Outputs 下.
      ```
   2. 典型示例
      ```shell
      # 1. (OSAPIChecker)/$: ./OSAPIChecker.py --channel=libchecker --strategy=base --level=l1l2 --ostype=desktop --pkgmngr=apt-deb
      # 2. (OSAPIChecker)/$: ./OSAPIChecker.py --channel=libchecker --strategy=base --level=l1l2 --ostype=server --pkgmngr=yum-rpm
      ```

2. FsChecker

   1. 桌面版的使用

      ```shell
      # 对 U 系列
      # 1. /etc/apt/source.list 下打开 deb-src.
      # 2. 执行 sudo apt update.
      # 3. (OSAPIChecker)/$: ./OSAPIChecker.py --channel=fschecker
      ```

3. CmdChecker

   1. 桌面版的使用

      ```shell
      # 对 U 系列
      # 1. /etc/apt/source.list 下打开 deb-src.
      # 2. 执行 sudo apt update.
      # 3. (OSAPIChecker)/$: ./OSAPIChecker.py --channel=cmdchecker
      ```

      

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
