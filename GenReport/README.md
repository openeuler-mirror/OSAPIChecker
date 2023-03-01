# OSAPIChecker

#### 介绍
json结果转pdf工具

#### 依赖安装

1.  pip3 install reportlab==3.6.12

#### 使用说明
1. 基本用法，直接执行使用默认路径生成pdf
      ```shell
      cd Pdf
      ./pdf.py
      ```
      
2. 使用参数指定文件路径
   - -r : 指定pdf生成结果路径
   - -e : 指定环境检测结果路径
   - -l : 指定运行库检查结果文件路径
   - -f : 指定文件系统层次结构检查结果文件路径
   - -c : 指定常用命令检查结果文件路径
   - -s : 指定服务检查结果文件路径 

   ```shell
      cd Pdf
      ./pdf.py -r ./result.pdf -l ../Outputs/libchecker-output.json -f ../Outputs/fs.json -c ../Outputs/cmd.json -s ../Outputs/service_result.json 
   ```
