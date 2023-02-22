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

dir=$(echo $(realpath $0 | awk -F'reports' '{print $1}'))
dir_systemd=/usr/lib/systemd/system

s_arch=$(uname -m)
result_file="result_${checker}_${time_tmp}.pdf"
env_file="environments-info_${time_tmp}.json"
lib_file="libchecker-output_${s_arch}_${time_tmp}.json"
cmd_file="cmd_${time_tmp}.json"
fs_file="fs_${time_tmp}.json"
service_file="service_result.json"
cmd_line=""

function generate_reports() {
	echo "生成报告：result_${checker}_${time_tmp}.pdf"
	if [ -f ${dir}/Outputs/${env_file} ];then
		cmd_line="${cmd_line} -e $dir/Outputs/${env_file}"
	fi
	
	if [ -f ${dir}/Outputs/${lib_file} ];then
		cmd_line="${cmd_line} -l $dir/Outputs/${lib_file}"
	fi
	
	if [ -f ${dir}/Outputs/${cmd_file} ];then
		cmd_line="${cmd_line} -c $dir/Outputs/${cmd_file}"
	fi
	
	if [ -f ${dir}/Outputs/${fs_file} ];then
		cmd_line="${cmd_line} -f $dir/Outputs/${fs_file}"
	fi
	
	if [ "${checker}" == "all" ] || [ "${checker}" == "servicechecker" ];then
		if [ -f ${dir}/Outputs/${service_file} ];then
			cmd_line="${cmd_line} -s $dir/Outputs/${service_file}"
		fi
	fi
	if [ "${cmd_line}" == "" ];then
		echo "not found ${checker} output file" >> $dir/Logs/pdf_${time_tmp}.log 2>&1
	else
		cd $dir/GenReport
		echo "Generate reports" >> $dir/Logs/pdf_${time_tmp}.log 2>&1
		./pdf.py -r $dir/Outputs/${result_file} ${cmd_line} >> $dir/Logs/pdf_${time_tmp}.log 2>&1
	fi
}

function recovery_configure (){
	sed -i '/%sudo ALL=(ALL:ALL) NOPASSWD:ALL/d' /etc/sudoers
	systemctl disable report_pdf.service
	rm -f ${dir_systemd}/report_pdf.service
	systemctl daemon-reload
	systemctl stop report_pdf.service
}

if [ ${checker} == "libchecker" ] || [ ${checker} == "cmdchecker" ] || [ ${checker} == "fschecker" ] ;then
	generate_reports
elif [ ${checker} == "servicechecker" ] || [ ${checker} == "all" ];then
	while [ -e ${dir_systemd}/verify_reboot.service ]
	do
		str_status=$(systemctl status verify_reboot.service | grep Active | awk '{print $2}')
		if [ "${str_status}" == "failed" ] || [ "${str_status}" == "inactive" ];then
			break
		fi
		sleep 5
	done
	generate_reports
	recovery_configure
fi
