#!/bin/bash

dir_path=$(cd "$(dirname "$0")"; pwd)
. ${dir_path}/config/lib.sh
dir_systemd=/usr/lib/systemd/system
monitor_path=/tmp/tem_monitor
apply_path=/usr/libexec/service_checker

function mv_register_file()
{
  log_info "开始注册所有systemd检测单元文件..."
  path_file=${dir_path}/path
  socket_file=${dir_path}/socket
  timer_file=${dir_path}/timer
  if [[ ! -d ${dir_systemd} ]]; then
    log_error "Have not found systemd service work directory: ${dir_systemd},please check your system."
  fi
  if [[ -d ${path_file} ]]; then
    cp ${path_file}/service_verify_path.service ${dir_systemd} &&
    cp ${path_file}/service_verify_path.path ${dir_systemd}
  else
    log_warn "Service path file directory not exist, can not copy register file."
  fi

  if [[ -d ${socket_file} ]]; then
    cp ${socket_file}/service_verify_client.service ${dir_systemd} &&
    cp ${socket_file}/service_verify_server.service ${dir_systemd} &&
    cp ${socket_file}/service_verify_server.socket ${dir_systemd}
  else
    log_warn "Service socket file directory not exist, can not copy register file."
  fi
  if [[ -d ${timer_file} ]]; then
    cp ${timer_file}/service_verify_timer.service ${dir_systemd} &&
    cp ${timer_file}/service_verify_timer.timer ${dir_systemd}
  else
    log_warn "Service timer file directory not exist, can not copy register file."
  fi

  go version >/dev/null 2>&1
  if [ $? -ne 0 ]; then
    log_info "正在安装golang，请等待..."
    sudo yum install -y golang >/dev/null 2>&1
    if [ $? -ne 0 ]; then
      log_error "自动安装失败，请先安装golang。"
    fi
    log_info "golang 安装完成！"
  else
    log_info "已安装 golang。"
  fi
  cd ${socket_file}
  # install go-systemd库 activation
  export GO111MODULE=auto
  go get github.com/coreos/go-systemd/activation

  # git clone https://github.com/coreos/go-systemd.git ~/go/src/github.com/coreos/go-systemd

  go build service_client.go
  go build service_server.go

  if [[ ! -d ${apply_path} ]];then
    mkdir -p ${apply_path}
  fi
  cp service_client ${apply_path}
  cp service_server ${apply_path}
  # 添加或修改配置文件后，需要重新加载
  systemctl daemon-reload
  if [ $? -eq 0 ]; then
    log_info "'systemctl daemon-reload' 添加待测试systemd配置文件成功。"
  fi
}

function verify_path()
{
    # 设置开机自启动
  systemctl enable service_verify_path.path
  # 启动目录监控服务
  systemctl start service_verify_path.path

  if [[ ! -d $monitor_path ]]; then
    mkdir $monitor_path
  fi
  cd $monitor_path
  if [[ -f test_path.log ]]; then
    rm -f test_path.log
  fi
  log_info "查询path服务启动状态为: \n`systemctl status service_verify_path.path`\n"

  touch tem_verify.txt
  log_info "在${monitor_path}目录下添加一个临时文件."
  sleep 2
  if [[ -f test_path.log ]]; then
    log_info "第一次查看path服务输出内容为：\n`cat test_path.log`"
    sleep 5
    rm -f tem_verify.txt
    log_info "在${monitor_path}目录下删除该临时文件."
    sleep 2
    log_info "第二次查看path服务输出内容为：\n`cat test_path.log`"

  else
    log_warn "***** path单元功能验证失败！*****"
  fi
  log_info "***** path单元功能验证成功！*****"
}

function verify_socket()
{
  # 启动客户端服务，强依赖服务端服务
  systemctl start service_verify_client.service
  if [ $? -ne 0 ]; then
    log_warn "socket 客户端服务启动失败。"
  fi
  log_info "请等待socket单元测试应用运行..."
  sleep 10
  log_info "显示客户端服务通信日志信息：\n`journalctl -u service_verify_client.service -n 10`"
  log_info "显示服务端服务通信日志信息：\n`journalctl -u service_verify_server.service -n 5`"

  journalctl -u service_verify_client.service -n 10 | grep "The client is starting" >/dev/null 2>&1 &&
  journalctl -u service_verify_server.service -n 5 | grep "service server start" >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    log_info "***** socket单元功能验证成功！*****"
  else
    log_warn "***** socket单元功能验证失败！*****"
  fi
}

function verify_timer() {
  # 启动timer定时单元
  systemctl start service_verify_timer.timer
  if [ $? -eq 0 ]; then
    log_info "service_verify_timer.timer单元启动成功，等待定时服务启动..."
  else
    log_warn "service_verify_timer.timer单元启动失败。"
  fi
  sleep 80
  if [[ -f ${monitor_path}/test_timer.log ]]; then
    log_info "service_verify_timer.service服务启动输出为：\n`cat ${monitor_path}/test_timer.log`"
    log_info "***** timer单元功能验证成功！*****"
  else
    log_warn "***** timer单元功能验证失败！*****"
  fi
}

function clear_environment()
{
  systemctl stop service_verify_server.socket
  systemctl stop service_verify_server.service
  systemctl stop service_verify_timer.timer
  systemctl stop service_verify_path.path

  rm -rf ${monitor_path}
  rm -rf ${apply_path}
  rm -rf /run/service_checker
  find ${dir_systemd} -name "service_verify*" | xargs rm -f
}

# 执行入口
function main() {
  # 将所有注册文件移动到指定工作目录下
  mv_register_file
  # 验证path服务功能
  verify_path
  # 验证socket服务功能
  verify_socket
  # 验证timer单元功能
  verify_timer
  # 清理环境
  clear_environment
}

main
