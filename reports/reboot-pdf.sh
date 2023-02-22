#!/bin/bash

checker=$1
time_tmp=$2
if [ ${checker} = "" ];then
	echo "ERROR"
	return 2
elif [ ${time_tmp} = "" ];then
	echo "ERROR"
	return 2
fi

real_p=$(realpath $0)
dir=${real_p%/*}
dir_systemd=/usr/lib/systemd/system

function generator_enable_service() {
echo "[Unit]
Description=service verify reboot
After=verify_reboot.service

[Service]
Type=oneshot
ExecStart=${dir}/report-pdf.sh ${checker} ${time_tmp}

[Install]
WantedBy=multi-user.target" >${dir_systemd}/report_pdf.service

}

function config_sudo_passwd() {
	sed -i '$ a\%sudo ALL=(ALL:ALL) NOPASSWD:ALL' /etc/sudoers
	systemctl daemon-reload
	systemctl enable report_pdf.service
}
generator_enable_service
config_sudo_passwd
