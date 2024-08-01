import os
from datetime import datetime 
import re
from utils_func import detect_encoding, query_source, get_latest_file
from collections import Counter
import json
# pyinstaller --onefile ipDisable.py

browser_dict = {}
ip_count_dict = {}

conf = open('path.conf', 'r')
conf_list = conf.read().split("\n")
iis_log_path = conf_list[0].split("=")[1]
start_line_num = int(conf_list[1].split("=")[1])
log_now_filename = conf_list[2].split("=")[1]
max_visit_one_day = int(conf_list[3].split("=")[1])
print(f"Read path.conf:\n{conf_list[0]}\n{conf_list[1]}\n{conf_list[2]}\n{conf_list[3]}")
conf.close()

history_disabled_ip_read = open("history_disabled_ip.conf","r+")
history_disabled_ip_list = history_disabled_ip_read.read().split("\n")
history_disabled_ip_read.close()

while "" in history_disabled_ip_list:
    history_disabled_ip_list.remove("")
print("history_disabled_ip_list:",history_disabled_ip_list)


# 定义一个函数来逐行读取日志文件并统计IP访问次数
def count_ip_visits(filename,temp_dict_ip_count):
    global browser_dict
    ip_counter = Counter(temp_dict_ip_count)  # 使用Counter来统计IP访问次数
    new_start_num = start_line_num
    with open(filename, 'r', encoding=ENCODING, errors='replace') as file:  # 打开文件
        for line in file.readlines()[start_line_num:]:  # 逐行读取
            parts = line.strip().split(' ')  # 去除行尾换行符并分割字符串
            if len(parts)>9:  # 确保分割后至少有一个元素
                ip_address = parts[8]  # 获取IP地址
                genjt = parts[4] #防止封锁掉自己的IP: 生成静态的那个IP地址
                if "/genjt" not in genjt:
                    ip_counter[ip_address] += 1  # 更新计数器
                if ip_address not in browser_dict.keys():
                    browser_dict[ip_address] = query_source(parts[9])
            new_start_num += 1
    
    update_conf_start_line_num(new_start_num)
    return ip_counter

    
def reset_conf(real_now_log):
    temp_f=open("path.conf","r+")
    temp_f_list = temp_f.readlines()
    temp_f_list[1] = "start_line_num=5\n"
    temp_f_list[2] = f"now_log_name={real_now_log}\n"
    temp_f.close()

    new_f = open("path.conf","w+")
    new_f.writelines(temp_f_list)
    new_f.close()

def update_conf_start_line_num(new_num):
    temp_f=open("path.conf","r+")
    temp_f_list = temp_f.readlines()
    temp_f_list[1] = f"start_line_num={new_num}\n"
    temp_f.close()

    new_f = open("path.conf","w+")
    new_f.writelines(temp_f_list)
    new_f.close()


# 获取最新修改的文件名
log_file_path = get_latest_file(iis_log_path)
print("iis_log_path",iis_log_path)
# 检测文件编码
ENCODING = detect_encoding(iis_log_path+log_file_path)

print("ENCODING",ENCODING)

# 记录每天日志到log文件
chars_to_remove = r'[^\w\s]'
orig_str = str(datetime.now())
# ip_log_date = orig_str[0:10]
if log_file_path!=log_now_filename:
    reset_conf(log_file_path)
    conf = open('path.conf', 'r')
    conf_list = conf.read().split("\n")
    iis_log_path = conf_list[0].split("=")[1]
    start_line_num = int(conf_list[1].split("=")[1])
    log_now_filename = conf_list[2].split("=")[1]
    max_visit_one_day = int(conf_list[3].split("=")[1])
    print(f"Config Reset!!! Read path.conf:\n{conf_list[0]}\n{conf_list[1]}\n{conf_list[2]}\n{conf_list[3]}")
    conf.close()


temp_str = re.sub(chars_to_remove, "_", orig_str)
print(temp_str,"ipDisable Running...")
if not os.path.exists("./log"):
    os.makedirs("./log")
f = open(f'./log/{log_file_path}_ip_disable.log', 'a', encoding=ENCODING)
# sys.stdout = f
# sys.stderr = f		# redirect std err, if necessary

#读取已有的.json格式文件的内容
if os.path.exists("./dict_json"):
    try:
        with open(f'./dict_json/browser_dict_{log_file_path}.json','r+') as file:
            browser_dict_json_read=file.read()
            browser_dict=json.loads(browser_dict_json_read)#将json格式文件转化为python的字典文件
        with open(f'./dict_json/ip_count_dict_{log_file_path}.json','r+') as file:
            ip_count_dict_json_read=file.read()
            ip_count_dict=json.loads(ip_count_dict_json_read)#将json格式文件转化为python的字典文件
    except FileNotFoundError:
        print("FileNotFoundError")
        pass
    except:
        print("Other Error")
        pass

# 调用函数并获取结果
ip_Visits = count_ip_visits(iis_log_path+log_file_path,ip_count_dict)

for ip, count in ip_Visits.items():
    ip_count_dict[ip] = count
    if ((count>=max_visit_one_day) and (browser_dict[ip]=="Others")) and (ip not in history_disabled_ip_list):
        f.writelines(f'{orig_str} {ip} {count} {browser_dict[ip]}\n')
        with open("history_disabled_ip.conf","a+") as history_disabled_ip:
            history_disabled_ip.writelines(f'{ip}\n')
        os.system(f"netsh advfirewall firewall add rule name=\"disabledIP[{ip}]({orig_str[0:10]})\" dir=in action=block remoteip=\"{ip}\"")
        # 命令：netsh advfirewall firewall add rule name="disabledIP" dir=in action=block remoteip=""

f.close()

#将字典结构数据保存为 .json 格式文件，并打开
browser_dict_json=json.dumps(browser_dict)#转化为json格式文件
ip_count_dict_json=json.dumps(ip_count_dict)#转化为json格式文件


if not os.path.exists("./dict_json"):
    os.makedirs("./dict_json")

#将json文件保存为.json格式文件
with open(f'./dict_json/browser_dict_{log_file_path}.json','w+') as file:
    file.write(browser_dict_json)


#将json文件保存为.json格式文件
with open(f'./dict_json/ip_count_dict_{log_file_path}.json','w+') as file:
    file.write(ip_count_dict_json)



        

