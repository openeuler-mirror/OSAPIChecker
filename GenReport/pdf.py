#!/usr/bin/python3

from pdfmaker import PdfMaker
from reportlab.platypus import PageBreak
from reportlab.lib import colors  # 颜色模块
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet  # 样式
from reportlab.platypus import Paragraph
import json
import argparse
import os

total_width = 700
table_background_color = '#d5dae6'

g_env = "../Outputs/environments-info.json"
g_lib = "../Outputs/libchecker-output.json"
g_fs = "../Outputs/fs.json"
g_cmd = "../Outputs/cmd.json"
g_server = "../Outputs/service_result.json"
g_result = "./操作系统应用编程接口要求标准符合性测试报告.pdf"
g_isConform = "符合"

# 表格样式
# table_background_color = '#87CEEB'
default_table_style = [
    ['ALIGN', (0, 0), (-1, -1), 'CENTER'],  # 水平居中
    ['VALIGN', (0, 0), (-1, -1), 'MIDDLE'],  # 垂直居中对齐
    # ['ALIGN', (0, 1), (-1, -1), 'CENTER'],  # 第二行到最后一行左右左对齐
    ['VALIGN', (0, 0), (-1, -1), 'MIDDLE'],  # 所有表格上下居中对齐
    ['GRID', (0, 0), (-1, -1), 0.5, colors.black],  # 设置表格框线为grey色，线宽为0.5
]
default_para_style = getSampleStyleSheet()['Normal']
default_para_style.fontName = 'SimSun'
default_para_style.wordWrap = 'CJK'     # 设置自动换行
default_para_style.fontSize = 10
default_para_style.textColor = colors.darkslategray  # 设置表格内文字颜色
default_para_style.alignment = 1        # 居中对齐

# 首页样式
home_table_style = [
    ['ALIGN', (0, 0), (-1, -1), 'CENTER'],  # 第一行水平居中
    ['VALIGN', (0, 0), (-1, -1), 'MIDDLE'],  # 所有表格上下居中对齐
    ['ALIGN', (0, 0), (0, -1), 'RIGHT'],
    ['ALIGN', (1, 0), (1, -1), 'CENTER'],
]
home_para_style = getSampleStyleSheet()['Normal']
home_para_style.fontName = 'SimSun'
home_para_style.fontSize = 20
home_para_style.wordWrap = 'CJK'     # 设置自动换行
home_para_style.alignment = 1        # 居中对齐


def make_pdf_cover(content):
    # 添加标题
    content.append(Spacer(1, 30))
    content.append(PdfMaker.draw_title('《操作系统应用编程接口要求》\n标准符合性测试报告', 30))

    # 添加日期等内容
    content.append(Spacer(1, 50))

    if not os.path.exists(g_env):
        print("未发现测试环境结果文件")
        content.append(
            PdfMaker.draw_little_title(
                '未发现测试环境结果文件', 12, colors.red))
        return

    with open(g_env, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        data = [
            ['产品名称:', json_data["测试对象"]["系统名称"]],
            ['产品版本:', json_data["测试对象"]["版本"]],
            ['测试日期:', json_data["测试时间"]]
        ]

    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            data[i][j] = Paragraph(str(cell), home_para_style)

    content.append(
        PdfMaker.draw_table(
            home_table_style,
            data,
            totalWidth=550,
            rates=[2, 7],))

    # 添加检测机构
    content.append(Spacer(1, 100))

    unit = json_data["送测单位"]
    content.append(PdfMaker.draw_title(unit, 20))


def make_pdf_test_env(content):
    # 添加小标题
    content.append(PdfMaker.draw_little_title('一、测试环境'))

    if not os.path.exists(g_env):
        print("未发现测试环境结果文件")
        content.append(
            PdfMaker.draw_little_title(
                '未发现测试环境结果文件', 12, colors.red))
        return

    data = []
    with open(g_env, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        data = [
            ['测试对象', '系统名称', json_data["测试对象"]["系统名称"]],
            ['测试对象', '版本', json_data["测试对象"]["版本"]],
            ['送测单位', '送测单位', json_data["送测单位"]],
            ['系统环境', '内核版本', json_data["系统环境"]["内核版本"]],
            ['系统环境', '编译器版本', json_data["系统环境"]["编译器版本"]],
            ['系统环境', 'Python版本', json_data["系统环境"]["Python版本"]],
            ['环境配置', '机器型号', json_data["环境配置"]["CPU型号"]],
            ['环境配置', 'CPU指令集', json_data["环境配置"]["CPU指令集"]],
            ['环境配置', 'CPU型号', json_data["环境配置"]["CPU型号"]],
            ['环境配置', '内存', json_data["环境配置"]["内存"]],
            ['环境配置', '硬盘', json_data["环境配置"]["硬盘"]],
            ['环境配置', '固件', json_data["环境配置"]["固件"]],
            ['测试工具', '名称', json_data["测试工具"]["名称"]],
            ['测试工具', '版本', json_data["测试工具"]["版本"]],
            ['测试时间', '测试时间', json_data["测试时间"]],
        ]

    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            data[i][j] = Paragraph(str(cell), default_para_style)

    extra_style = default_table_style + [
        ['SPAN', (0, 0), (0, 1)],
        ['SPAN', (0, 2), (1, 2)],
        ['SPAN', (0, 3), (0, 5)],
        ['SPAN', (0, 6), (0, 11)],
        ['SPAN', (0, 12), (0, 13)],
    ]

    content.append(
        PdfMaker.draw_table(
            extra_style,
            data,
            totalWidth=total_width,
            rowHeight=27,
            rates=[1, 1, 3]))


def make_pdf_lib(content):
    content.append(Spacer(1, 10))
    # 1.运行库
    content.append(PdfMaker.draw_little_title('1.运行库', 15))
    content.append(Spacer(1, 10))

    if not os.path.exists(g_lib):
        print("未发现运行库检查结果文件")
        content.append(
            PdfMaker.draw_little_title(
                '未发现运行库检查结果文件', 12, colors.red))
        return

    # (1)库包检查
    content.append(PdfMaker.draw_little_title('(1)库包检查', 12))
    # 添加表格
    data = [
        ['包名', '检测信息', '--', '--', '--'],
        ['包名', '检测信息', '--', '--', '--'],
    ]

    with open(g_lib, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        row = 2
        for r in json_data:

            require_version = json_data[r]["Required version"]
            level = json_data[r]["Level"]
            data.append([r, '版本要求', '级别', '--', '--'])
            data.append([r, require_version, level, '--', '--'])
            data.append([r, '二进制包名', '当前版本', '--', '测试结果'])

        #     local_version = "-"
        #     status = ""
            for pack in json_data[r]["Binary package"]:
                if isinstance(json_data[r]["Binary package"][pack], dict):
                    for lib in json_data[r]["Binary package"][pack]:
                        local_version = json_data[r]["Binary package"][pack][lib]["version"]
                        status = json_data[r]["Binary package"][pack][lib]["status"]

                        if status == "compatible":
                            status = "通过"
                        elif status == "not installed":
                            continue
                        else:
                            status = "不通过"
                        data.append([r, lib, local_version, '--', status])

            data.append([r, '共享对象名', '存储路径', '归属包名', '测试结果'])
            if isinstance(json_data[r]["Shared library"], dict):
                for shared in json_data[r]["Shared library"]:
                    result = json_data[r]["Shared library"][shared]["status"]
                    if result == "compatible":
                        result = "通过"
                    else:
                        result = "不通过"

                    belongs = "-"

                    if json_data[r]["Shared library"][shared]["belongs"] != "None":
                        belongs = json_data[r]["Shared library"][shared]["belongs"]
                    path = json_data[r]["Shared library"][shared]["path"]
                    if len(path) > 65:
                        path_list = list(path)
                        path_list.insert(60, '\n')
                        path = ''.join(path_list)
                    data.append([r, shared, path, belongs, result])

    lib_table_style = default_table_style + [
        ['BACKGROUND', (0, 0), (-1, 0), table_background_color],  # 设置第一行背景颜色
        ['BACKGROUND', (0, 1), (-1, 1), table_background_color],  # 设置第二行背景颜色
        ['SPAN', (0, 0), (0, 1)],  # 合并第一列一二行
        ['SPAN', (1, 0), (-1, 1)],  # 合并第四列一二行
    ]

    is_merge = False

    for i, r in enumerate(data):
        if data[i][1] == "版本要求":
            lib_table_style.append(
                ['BACKGROUND', (1, i), (-1, i), table_background_color])
            lib_table_style.append(['SPAN', (2, i), (-1, i)])
            lib_table_style.append(['SPAN', (2, i + 1), (-1, i + 1)])
        if data[i][1] == "二进制包名":
            lib_table_style.append(
                ['BACKGROUND', (1, i), (-1, i), table_background_color])
            is_merge = True

        if data[i][1] == "共享对象名":
            lib_table_style.append(
                ['BACKGROUND', (1, i), (-1, i), table_background_color])
            is_merge = False

        if is_merge:
            lib_table_style.append(['SPAN', (2, i), (3, i)])

        if data[i][-1] == "不通过":
            c = default_para_style.textColor
            default_para_style.textColor = colors.red
            data[i][-1] = Paragraph(str(data[i][-1]),
                                    default_para_style)
            default_para_style.textColor = c

        for j, cell in enumerate(r):
            if not isinstance(data[i][j], Paragraph):
                s = default_para_style.fontSize
                if i == 0:
                    default_para_style.fontSize = 12
                data[i][j] = Paragraph(str(cell), default_para_style)
                default_para_style.fontSize = s

    content.append(
        PdfMaker.draw_mul_table(
            lib_table_style,
            data,
            totalWidth=total_width,
            rates=[2, 3, 7, 2, 1.2]))
    content.append(PageBreak())

    # (2)小计
    content.append(PdfMaker.draw_little_title('(2)小计', 12))

    with open(g_lib, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        result_map = {}
        for r in json_data:
            level = json_data[r]["Level"]

            if level not in result_map:
                level_map = {}
                level_map["pack_require_num"] = 0
                level_map["pack_no_pass_num"] = 0
                level_map["shard_require_num"] = 0
                level_map["shard_pass_num"] = 0
                result_map[level] = level_map

            result_map[level]["pack_require_num"] += 1
            status = ""

            for pack in json_data[r]["Binary package"]:
                if isinstance(json_data[r]["Binary package"][pack], dict):
                    pack_passed = True
                    for lib in json_data[r]["Binary package"][pack]:
                        status = json_data[r]["Binary package"][pack][lib]["status"]
                        if status == "incompatible":
                            pack_passed = False
                    if not pack_passed:
                        result_map[level]["pack_no_pass_num"] += 1

            if isinstance(json_data[r]["Shared library"], dict):
                for lib in json_data[r]["Shared library"]:
                    if json_data[r]["Shared library"][lib]["status"] == "compatible":
                        result_map[level]["shard_pass_num"] += 1
                    result_map[level]["shard_require_num"] += 1

    # 添加表格
    data = [
        ['级别', '类型', '要求数量', '符合数量', '比率'],
    ]
    i = 1
    result_style = default_table_style + [
        ['BACKGROUND', (0, 0), (-1, 0), table_background_color],  # 设置第一行背景颜色
    ]
    for level in result_map:
        pack_pass_num = result_map[level]["pack_require_num"] - \
            result_map[level]["pack_no_pass_num"]
        if result_map[level]["pack_require_num"] != 0:

            pack_rate = '{:.2f}%'.format(
                pack_pass_num / result_map[level]["pack_require_num"] * 100)
        else:
            pack_rate = 0

        # print(result_map[level]["shard_require_num"])
        if result_map[level]["shard_require_num"] != 0:
            shard_rate = '{:.2f}%'.format(
                result_map[level]["shard_pass_num"] /
                result_map[level]["shard_require_num"] *
                100)
        else:
            shard_rate = 0

        table_content = [
            level,
            "包",
            result_map[level]["pack_require_num"],
            pack_pass_num,
            pack_rate]
        data.append(table_content)

        table_content = [
            level,
            "共享对象",
            result_map[level]["shard_require_num"],
            result_map[level]["shard_pass_num"],
            shard_rate]
        data.append(table_content)

        result_style = result_style + [
            ('SPAN', (0, i), (0, i + 1)),  # 合并第一列一二行
        ]

        if level == 'L1' or level == 'L2':

            if pack_rate != "100.00%" or shard_rate != "100.00%":
                global g_isConform
                g_isConform = "不符合"

        i += 2

    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            s = default_para_style.fontSize
            if i == 0:
                default_para_style.fontSize = 12
            data[i][j] = Paragraph(str(cell), default_para_style)
            default_para_style.fontSize = s

    content.append(
        PdfMaker.draw_table(
            result_style,
            data,
            totalWidth=total_width,
            rates=[1, 1, 1, 1, 1]
        ))


def make_pdf_fs(content):
    content.append(Spacer(1, 10))
    # 2.文件系统层次结构
    content.append(PdfMaker.draw_little_title('2.文件系统层次结构', 15))
    content.append(Spacer(1, 10))
    if not os.path.exists(g_fs):
        print("未发现文件系统层次结构检查结果文件")
        content.append(
            PdfMaker.draw_little_title(
                '未发现文件系统层次结构检查结果文件',
                12,
                colors.red))
        return

    # (1)文件系统层次结构检查
    content.append(PdfMaker.draw_little_title('(1)文件系统层次结构检查', 12))
    # 添加表格
    data = [
        ['目录', '检查项', '', '测试结果'],
        ['', '存在', '权限', ''],
    ]

    require_num = 0
    pass_num = 0

    fs_table_style = default_table_style + [
        ['BACKGROUND', (0, 0), (-1, 0), table_background_color],  # 设置第一行背景颜色
        ['BACKGROUND', (0, 1), (-1, 1), table_background_color],  # 设置第二行背景颜色
        ['SPAN', (0, 0), (0, 1)],  # 合并第一列一二行
        ['SPAN', (1, 0), (2, 0)],  # 合并第一行二三列
        ['SPAN', (3, 0), (3, 1)],  # 合并第四列一二行
    ]

    with open(g_fs, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        json_result = json_data["result"]

        i = 2
        for r in json_result:
            if r["exist_check"]["result"] == "pass":
                exist = "通过"
            else:
                exist = "不通过"

            if r["result"] == "pass":
                result = "符合"
                pass_num += 1
            else:
                result = "不符合"

            table_content = [
                r["FS_name"],
                exist,
                r["file_permissions"],
                result]
            data.append(table_content)

            i += 1
            require_num += 1

    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            s = default_para_style.fontSize
            c = default_para_style.textColor
            if i == 0:
                default_para_style.fontSize = 12
            if j == len(row) - 1 and cell == "不符合":
                default_para_style.textColor = colors.red
            data[i][j] = Paragraph(str(cell), default_para_style)
            default_para_style.fontSize = s
            default_para_style.textColor = c

    content.append(
        PdfMaker.draw_table(
            fs_table_style,
            data,
            totalWidth=total_width,
            rates=[1, 2, 2, 1]))
    content.append(Spacer(1, 10))

    # (2)小计
    content.append(PdfMaker.draw_little_title('(2)小计', 12))
    # 添加表格
    rate = '{:.2f}%'.format(pass_num / require_num * 100)
    data = [
        ['要求数量', '符合数量', '比率'],
        [require_num, pass_num, rate]
    ]
    result_table_style = default_table_style + [
        ['BACKGROUND', (0, 0), (-1, 0), table_background_color],  # 设置第一行背景颜色
    ]
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            s = default_para_style.fontSize
            if i == 0:
                default_para_style.fontSize = 12
            data[i][j] = Paragraph(str(cell), default_para_style)
            default_para_style.fontSize = s

    content.append(
        PdfMaker.draw_table(
            result_table_style,
            data,
            totalWidth=total_width,
            rates=[1, 1, 1]))


def make_pdf_cmd(content):
    content.append(Spacer(1, 10))
    # 3.常用命令
    content.append(PdfMaker.draw_little_title('3.常用命令', 15))
    content.append(Spacer(1, 10))

    if not os.path.exists(g_cmd):
        print("未发现常用命令检查结果文件")
        content.append(
            PdfMaker.draw_little_title(
                '未发现常用命令检查结果文件', 12, colors.red))
        return

    # (1)常用命令检查
    content.append(PdfMaker.draw_little_title('(1)常用命令检查', 12))
    # 添加表格
    data = [
        ['命令', '检查项', '', '', '测试结果'],
        ['', '路径', '版本', '运行', ''],
    ]

    require_num = 0
    pass_num = 0

    cmd_table_style = default_table_style + [
        ['BACKGROUND', (0, 0), (-1, 0), table_background_color],  # 设置第一行背景颜色
        ['BACKGROUND', (0, 1), (-1, 1), table_background_color],  # 设置第二行背景颜色
        ['SPAN', (0, 0), (0, 1)],  # 合并第一列一二行
        ['SPAN', (1, 0), (3, 0)],  # 合并第一行二三四列
        ['SPAN', (4, 0), (4, 1)],  # 合并第五列一二行
    ]

    with open(g_cmd, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        json_result = json_data["result"]
        i = 2
        for r in json_result:
            if r["exist_check"]["result"] == "pass":
                exist = "通过"
            else:
                exist = "不通过"
            if r["run_check"]["result"] == "pass":
                check = "通过"
            else:
                check = "不通过"

            if r["result"] == "pass":
                result = "符合"
                pass_num += 1
            else:
                result = "不符合"

            table_content = [r["name"], "-", r["cmd_version"], check, result]
            data.append(table_content)

            i += 1
            require_num += 1

    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            s = default_para_style.fontSize
            c = default_para_style.textColor
            if i == 0:
                default_para_style.fontSize = 12
            if j == len(row) - 1 and cell == "不符合":
                default_para_style.textColor = colors.red
            data[i][j] = Paragraph(str(cell), default_para_style)
            default_para_style.fontSize = s
            default_para_style.textColor = c

    content.append(
        PdfMaker.draw_table(
            cmd_table_style,
            data,
            totalWidth=total_width,
            rates=[1, 4, 2, 2, 2]))

    # (2)小计
    content.append(PdfMaker.draw_little_title('(2)小计', 12))
    # 添加表格
    rate = '{:.2f}%'.format(pass_num / require_num * 100)
    data = [
        ['要求数量', '符合数量', '比率'],
        [require_num, pass_num, rate]
    ]
    result_table_style = default_table_style + [
        ['BACKGROUND', (0, 0), (-1, 0), table_background_color],  # 设置第一行背景颜色
    ]
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            s = default_para_style.fontSize
            if i == 0:
                default_para_style.fontSize = 12
            if j == len(row) - 1 and cell == "不符合":
                default_para_style.textColor = colors.red
            data[i][j] = Paragraph(str(cell), default_para_style)
            default_para_style.fontSize = s

    content.append(
        PdfMaker.draw_table(
            result_table_style,
            data,
            totalWidth=total_width,
            rates=[1, 1, 1]))


def make_pdf_service(content):
    # 4.服务检查
    content.append(Spacer(1, 10))
    content.append(PdfMaker.draw_little_title('4.服务检查', 15))
    content.append(Spacer(1, 10))

    if not os.path.exists(g_server):
        print("未发现服务检查结果文件")
        content.append(
            PdfMaker.draw_little_title(
                '未发现服务检查结果文件', 12, colors.red))
        return

    # (1)常用命令检查
    content.append(PdfMaker.draw_little_title('(1)常用服务检查', 12))
    # 添加表格
    data = [
        ['服务', '测试结果'],
    ]

    service_style = default_table_style + [
        ['BACKGROUND', (0, 0), (-1, 0), table_background_color],  # 设置第一行背景颜色
    ]

    with open(g_server, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        i = 1
        for r in json_data:
            result = json_data[r]["Check result"]
            if result == "pass":
                result = "通过"
            else:
                result = "不通过"
                service_style.append(
                    ['TEXTCOLOR', (0, i), (-1, i), colors.red])
            table_content = [r, result]
            data.append(table_content)
            i += 1

    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            s = default_para_style.fontSize
            c = default_para_style.textColor
            if i == 0:
                default_para_style.fontSize = 12
            if j == len(row) - 1 and cell == "不符合":
                default_para_style.textColor = colors.red
            data[i][j] = Paragraph(str(cell), default_para_style)
            default_para_style.fontSize = s
            default_para_style.textColor = c

    content.append(
        PdfMaker.draw_table(
            service_style,
            data,
            totalWidth=total_width,
            rates=[1, 1]))


def make_pdf_result(content):
    # 添加小标题
    content.append(PdfMaker.draw_little_title('二、测试结果'))
    make_pdf_lib(content)
    content.append(PageBreak())
    make_pdf_fs(content)
    content.append(PageBreak())
    make_pdf_cmd(content)
    content.append(PageBreak())
    make_pdf_service(content)


def make_pdf_conclusion(content):
    # 添加小标题
    content.append(PdfMaker.draw_little_title('三、测试结论'))

    if not os.path.exists(g_env):
        content.append(
            PdfMaker.draw_little_title(
                '未发现测试环境结果文件', 12, colors.red))
        return

    with open(g_env, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        print(g_isConform)
        text = '经测试，{}送测的{}-{}({}){}《操作系统应用编程接口要求》。'.format(
            json_data["送测单位"],
            json_data["测试对象"]["系统名称"],
            json_data["测试对象"]["版本"],
            json_data["环境配置"]["CPU指令集"][0],
            g_isConform)
        content.append(PdfMaker.draw_text(text, 12))


def make_api_pdf(pdfName):
    # 创建内容对应的空列表
    content = list()

    make_pdf_cover(content)
    content.append(PageBreak())
    make_pdf_test_env(content)
    content.append(PageBreak())
    make_pdf_result(content)
    content.append(PageBreak())
    make_pdf_conclusion(content)

    PdfMaker.create_pdf(pdfName, content)
    print("pdf生成完成, 路径: {}".format(os.path.abspath(g_result)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--result', type=str)
    parser.add_argument('-e', '--env', type=str)
    parser.add_argument('-l', '--lib', type=str)
    parser.add_argument('-f', '--fs', type=str)
    parser.add_argument('-c', '--cmd', type=str)
    parser.add_argument('-s', '--server', type=str)
    args = parser.parse_args()

    if args.result is not None:
        g_result = args.result

    if args.env is not None:
        g_env = args.env

    if args.lib is not None:
        g_lib = args.lib

    if args.fs is not None:
        g_fs = args.fs

    if args.cmd is not None:
        g_cmd = args.cmd

    if args.server is not None:
        g_server = args.server

    make_api_pdf(g_result)
