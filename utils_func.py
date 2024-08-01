import chardet
import os
def detect_encoding(file_path):
    # 以二进制模式打开文件
    with open(file_path, 'rb') as file:
        # 读取一定数量的字节，这里读取前10000字节
        raw_data = file.read(10000)
        # 使用chardet检测编码
        result = chardet.detect(raw_data)
        # 返回编码结果
        return result['encoding']
    
def query_source(query):
    if 'baidu.com' in query:
        return 'Baidu'
    elif 'sogou.com' in query:
        return 'Sogou'
    elif 'zhanzhang.toutiao.com' in query:
        return 'ZhanzhangToutiao'
    elif 'bing.com' in query:
        return 'Bing'
    elif 'ahrefs.com' in query:
        return 'Ahrefs'
    elif 'semrush.com' in query:
        return 'Semrush'
    elif 'google.com' in query:
        return 'Google'
    elif 'facebook.com' in query:
        return 'Facebook'
    elif 'apple.com' in query:
        return 'Apple'
    elif ('Spider' in query) or ('spider' in query):
        return 'Spider'
    else:
        return 'Others'
    

def get_latest_file(folder_path):
    # 初始化最新时间戳和最新文件名
    latest_time = 0
    latest_file = None

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件是否以.log结尾
        if filename.endswith('.log'):
            file_path = os.path.join(folder_path, filename)
            
            # 确保是文件而不是文件夹
            if os.path.isfile(file_path):
                # 获取文件的最后修改时间
                file_modified_time = os.path.getmtime(file_path)
                
                # 检查是否是最新的文件
                if file_modified_time > latest_time:
                    latest_time = file_modified_time
                    latest_file = filename
    return latest_file