# coding=utf-8
"""
@Project : 20220916-OSChecker
@Time    : 2022/9/20 14:24
@Author  : wangbin
"""

import json
import pprint

with open('cmdlist.txt') as f:
    data = f.readlines()


pprint.pprint(data)

result = []
for cmd in data:
    result.append({
        'name': cmd.replace('\n', '')
    })

result = {
    'std_name': '信息技术应用创新  操作系统应用编程接口要求',
    'system_cmds': result
}
# res = json.dumps(result)
# pprint.pprint(res)

with open('cmd_list.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
