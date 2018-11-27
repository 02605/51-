import re
import urllib.request
import os
import threading
import datetime

class Bugs(threading.Thread):
    # i_start, i_end, web_path_list, file_path
    def __init__(self, _file, web_path_list, i_start, i_end, _mutex):
        threading.Thread.__init__(self)
        self._file = _file # 写入的文件
        self.web_path_list = web_path_list # 网址列表
        self.i_start = i_start
        self.i_end = i_end
        self._mutex = _mutex # 写锁

    def run(self):
        list_all = []  # 每个线程的所有数据集合
        for i in range(self.i_start, self.i_end):
            data = get_page_data(self.web_path_list[i]) # 获取页面源代码
            #print(self.web_path_list[i])
            if data:  # 处理每页有效信息
                data_list = get_job_info(data)
                list_all.append(data_list)
                with self._mutex:
                    write_info(data_list, self._file)
                    #print(data_list)
            else:
                print("页面源代码获取失败")
# 获取页面源代码
def get_page_data(web_url):
    try:
        return urllib.request.urlopen(web_url).read().decode("gbk", "ignore")
    except:
        return None

# 获取总页数
def get_page_nums(page_data):
    if page_data:
        job_regex = "<span class=\"td\">共(\d+?)页"
        job_type = re.compile(job_regex, re.S)
        if len(job_type.findall(page_data))!=0:
            return eval(job_type.findall(page_data)[0])
        return 0
    return 0

# 获取每页的有效信息
def get_job_info(page_info):
    all_info_regex = "<div class=\"el\">(?:.*?)class=\"t4\">(.*?)</s"
    type_regex = re.compile(all_info_regex, re.S)
    return type_regex.findall(page_info)

# 根据页数拼接网址
def back_each_path(nums, type_city, type_lan):
    web_path_list = []
    for i in range(1, nums+1):
        each_path = "https://search.51job.com/list/"+type_city+",000000,0000,00,9,99,"+type_lan+",2,"+str(i)+".html"
        web_path_list.append(each_path)
    return web_path_list

# 根据一个city&language拼接一个base_path
def get_base_path(type_city, type_lan):
    return "https://search.51job.com/list/"+type_city+",000000,0000,00,9,99,"+type_lan+",2,1.html"

# 返回拼接地址
def get_path_list(type_city, type_lan):
    base_path = get_base_path(type_city, type_lan)
    page_info = get_page_data(base_path)
    all_page_num = get_page_nums(page_info)
    if all_page_num: # 搜索到总页数
        # 拼接每页地址
        web_path_list = back_each_path(all_page_num, type_city, type_lan)
        if len(web_path_list)!=0:
            return web_path_list
        else:
            return None
    else:
        return None

# 写文件函数
def write_info(data_list, _file):

    for i in range(len(data_list)):
        if data_list[i] != "":
            _file.write((data_list[i] + "\n").encode("utf-8"))
    _file.flush()

    # finally:
    #     my_file.close()

#  _file, web_path_list, i_start, i_end
def the_start(web_path_list, thd_num, write_file, _mutex):
    # 假设有十个线程，先创建九个
    thd_list = []
    base = len(web_path_list)//(thd_num-1)
    for i in range(thd_num-1):
        my_thd = Bugs(write_file, web_path_list,
                      i*base, (i+1)*base, _mutex)
        my_thd.start()
        thd_list.append(my_thd)

    # 处理最后一个线程
    my_thd = Bugs(write_file, web_path_list,
                  (thd_num-1) * base, len(web_path_list), _mutex)
    my_thd.start()
    thd_list.append(my_thd)

    # 线程运行等待
    for my_thd in thd_list:
        my_thd.join()
'''
xian 200200
beijing 010000
all 000000
'''
def main(city, language, thd_num, _mutex):
    city_code = ""
    if city=="北京":
        city_code = "010000"
    elif city=="西安":
        city_code = "200200"
    elif city=="天津":
        city_code = "050000"
    elif city=="中国":
        city_code = "000000"
    now = datetime.datetime.now()
    now_str = now.strftime(r"%Y-%m-%d-%H.%M.")
    file_path = os.path.abspath("./file/51jobs_"+city+"_"+language+"_"+now_str+"money.txt")
    path_list = get_path_list(city_code, language)
    my_file = open(file_path, "ba")
    the_start(path_list, thd_num, my_file, _mutex) # 开启多少个线程
    my_file.close()
    return file_path

if __name__=="__main__":
    start_time = datetime.datetime.now()
    processA_mutex = threading.Lock()
    main("西安", "python", 6, processA_mutex)
    end_time = datetime.datetime.now()
    print(end_time - start_time)  # 0:00:03.000466