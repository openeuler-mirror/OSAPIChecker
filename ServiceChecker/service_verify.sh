#!/bin/bash

dir_path=$(
  cd "$(dirname "$0")"
  pwd
)
. ${dir_path}/config/lib.sh
dir_systemd=/usr/lib/systemd/system
monitor_path=/opt/tem_monitor
apply_path=/usr/libexec/service_checker
path_file=${dir_path}/path
socket_file=${dir_path}/socket
timer_file=${dir_path}/timer
service_file=${dir_path}/service
swap_file=${dir_path}/swap

function generator_enable_service() {
echo "[Unit]
Description=service verify reboot

[Service]
Type=oneshot
ExecStart=python3 ${dir_path}/service_checker.py -m reboot
ExecStop=/bin/bash -c "echo Stop verify_reboot.servic"

[Install]
WantedBy=multi-user.target" >${dir_systemd}/verify_reboot.service

}

function mv_register_file() {
  log_info "开始注册所有systemd检测单元文件..."

  if [[ ! -d ${dir_systemd} ]]; then
    log_error "Have not found systemd service work directory: ${dir_systemd},please check your system."
  fi

  # 创建开机自启动reboot service单元配置文件
  generator_enable_service

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

  if [[ -d ${service_file} ]]; then
    cp ${service_file}/service_verify_disable.service ${dir_systemd}
  else
    log_warn "Service file directory not exist, can not copy register file."
  fi

  if [[ -d ${swap_file} ]]; then
    cp ${swap_file}/swapfile.swap ${dir_systemd}
  else
    log_warn "Service swap file directory not exist, can not copy register file."
  fi

  go version >/dev/null 2>&1
  if [ $? -ne 0 ]; then
    log_info "正在安装golang，请等待..."
    sudo yum install -y golang >/dev/null 2>&1
    if [ $? -ne 0 ]; then
      log_error "自动安装失败，请先安装golang。"
    fi
    log_info "golang 安装完成！"
  fi

  cd ${socket_file}
  # install go-systemd库 activation
  export GO111MODULE=auto
  # git clone https://github.com/coreos/go-systemd.git ~/go/src/github.com/coreos/go-systemd
  go get github.com/coreos/go-systemd/activation >/dev/null 2>&1
  if [ $? -ne 0 ]; then
    go env -w GOPROXY=https://goproxy.cn,direct
    go env -w GOPRIVATE=git.mycompany.com,github.com/my/private

    go get github.com/coreos/go-systemd/activation >/dev/null 2>&1
  fi

  go build service_client.go
  go build service_server.go

  if [[ ! -d ${apply_path} ]]; then
    mkdir -p ${apply_path}
  fi
  cp service_client ${apply_path}
  cp service_server ${apply_path}

  log_info "添加待测试systemd配置文件完成。"
}

function verify_service() {

  systemctl enable verify_reboot.service
  log_info "设置service_reboot服务开机自启动。"

  systemctl disable service_verify_disable.service
  log_info "设置service_disable服务禁止开机自启动。"

  # 添加或修改配置文件后，需要重新加载
  systemctl daemon-reload
  if [ $? -eq 0 ]; then
    log_info "'systemctl daemon-reload' 重新加载配置文件成功。\n"
  fi

  # 验证path服务功能
  verify_path
}

function verify_path() {
  # 启动目录监控服务
  log_info "***** 启动service_verify_path单元 *****"
  systemctl start service_verify_path.path
  if [ $? -ne 0 ]; then
    log_warn "path 单元启动失败。"
  fi
  log_info "查看path单元服务状态：\n`systemctl status service_verify_path.path`"
  if [[ ! -d $monitor_path ]]; then
    mkdir $monitor_path
  fi
  cd $monitor_path
  if [[ -f test_path.log ]]; then
    rm -f test_path.log
  fi

  touch tem_verify.txt
  log_info "在${monitor_path}目录下添加一个临时文件."

  sleep 2
  if [[ -f test_path.log ]]; then
    log_info "第一次查看path服务输出内容为：\n$(cat test_path.log)"
    sleep 5
    rm -f tem_verify.txt
    log_info "在${monitor_path}目录下删除该临时文件."
    sleep 2
    log_info "第二次查看path服务输出内容为：\n$(cat test_path.log)"
  else
    log_warn "***** path单元功能验证失败 *****\n"
  fi
  log_info "***** path单元功能验证成功 *****\n"

  # 验证socket服务功能
  verify_socket
}

function verify_socket() {
  # 启动客户端服务，强依赖服务端服务
  log_info "***** 启动service_verify_socket单元 *****"

  systemctl start service_verify_client.service
  if [ $? -ne 0 ]; then
    log_warn "socket 客户端服务启动失败。"
  fi
  log_info "查看客户端服务状态：\n`systemctl status service_verify_client.service`"

  log_info "请等待socket单元测试应用运行..."
  sleep 10
  log_info "显示客户端服务通信日志信息：\n$(journalctl -u service_verify_client.service -n 5)"
  log_info "显示服务端服务通信日志信息：\n$(journalctl -u service_verify_server.service -n 3)"

  journalctl -u service_verify_client.service -n 5 | grep "Verify socket server" >/dev/null 2>&1 &&
    journalctl -u service_verify_server.service -n 3 | grep "Verify socket client" >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    log_info "***** socket单元功能验证成功 *****\n"
  else
    log_warn "***** socket单元功能验证失败 *****\n"
  fi

  # 验证timer单元功能
  verify_timer
}

function verify_timer() {

  # 启动timer定时单元
  log_info "***** 启动service_verify_timer单元 *****"
  systemctl start service_verify_timer.timer

  if [ $? -eq 0 ]; then
    log_info "service_verify_timer.timer单元启动成功，等待定时服务启动..."
  else
    log_warn "service_verify_timer.timer单元启动失败。"
  fi

  log_info "查看timer单元服务状态：\n`systemctl status service_verify_timer.timer`"

  sleep 70
  if [[ -f ${monitor_path}/test_timer.log ]]; then
    log_info "service_verify_timer.service服务启动输出为：\n$(cat ${monitor_path}/test_timer.log)"
    log_info "***** timer单元功能验证成功 *****\n"
  else
    log_warn "***** timer单元功能验证失败 *****\n"
  fi

  # 创建交换文件作为交换分区
  verify_swap

}


function verify_swap() {
  log_info "***** 验证swap单元 *****"
  log_info "创建一个交换文件（swapfile）:"
  dd if=/dev/zero of=/swapfile bs=1M count=512 status=progress
  if [ $? -ne 0 ]; then
    log_warn "创建交换文件失败。"
  fi
  # 防止交换文件全局可读
  chmod 600 /swapfile

  mkswap /swapfile
  # 重启后会启动/swapfile交换分区
  # sed -i '$ a\# /etc/fstab\n/swapfile none swap defaults 0 0' /etc/fstab

  systemctl start swapfile.swap
  if [ $? -eq 0 ]; then
    log_info "成功启动swap单元。"
  else
    log_warn "启动swap单元失败"
  fi

  log_info "查看swap单元服务状态：\n`systemctl status swapfile.swap`"

  log_info "查看交换空间使用详细信息："
  swapon --show
  if [ $? -eq 0 ]; then
    log_info "***** swap单元功能验证成功 *****\n"
  else
    log_warn "***** swap单元功能验证失败 *****\n"
  fi

  # 测试及修改默认target
  verify_target
}

function verify_target() {
  log_info "***** 开始验证target单元 *****"
  log_info "查询所有运行级别传统runlevel与对应target信息如下：\n $(ls -al ${dir_systemd}/runlevel*.target | awk -F " " '{print $9 $10 $11}')"

  log_info "查看当前系统默认target为: $(systemctl get-default)"

  systemctl isolate rescue.target
  if [ $? -eq 0 ]; then
    sleep 2
    log_info "切换当前运行级别至单用户模式（rescue.target）成功，runlevel信息为：`runlevel`"
    log_info "***** target单元功能验证成功 *****"
  else
    log_warn "切换至单用户级别失败"
    log_warn "***** target单元功能验证失败 *****"
  fi

  # 重启系统
  log_info "请等待3秒后将重启系统...\n"
  sleep 3
  reboot
}



function verify_reboot_service() {
  log_info "***** 开机自启动服务单元（service_verify_reboot.service）执行成功！*****"

  log_info "查询service_disable服务设置开机启动状态为：`systemctl list-unit-files --type=service|grep service_verify_disable.service|awk -F " " '{print $2}'`"
  if [ -f ${monitor_path}/test_disable.log ]; then
    log_warn "***** 禁止开机自启动服务单元执行失败！*****"
  else
    log_info "***** 禁止开机自启动服务单元（service_verify_disable.service）执行成功！*****"
  fi

}


function clear_environment() {

  systemctl stop swapfile.swap
  systemctl stop service_verify_server.socket
  systemctl stop service_verify_server.service
  systemctl stop service_verify_timer.timer
  systemctl stop service_verify_path.path
  systemctl stop service_verify_disable.service

  # 删除交换文件
  rm -f /swapfile

  rm -rf ${monitor_path}
  rm -rf ${apply_path}
  rm -rf /run/service_checker
  rm -f ${socket_file}/service_client
  rm -f ${socket_file}/service_server
  find ${dir_systemd} -name "service_verify*" | xargs rm -f
  rm -f ${dir_systemd}/swapfile.swap

  export GO111MODULE=""

  systemctl stop verify_reboot.service &&
  rm -f ${dir_systemd}/verify_reboot.service

}

# 执行入口
case $1 in
start)
  # 将所有注册文件移动到指定工作目录下
  mv_register_file
  # 检测所有待测单元
  verify_service
  ;;
reboot)
  # 验证重启系统后部分功能
  verify_reboot_service
  ;;
clear)
  # 清理环境
  clear_environment
  ;;
*)
  echo 'unknown comand,try again start or reboot'
  ;;
esac
