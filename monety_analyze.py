import os
import codecs

# Python开发工程师--西安深思信息科技有限公司--西安-高新技术...--0.8-1万/月--11-18--
class MoneyInfo:

    def __init__(self, file_path):
        self.path = file_path

    def get_info(self):
        my_file = codecs.open(self.path, "rb", "utf-8", "ignore")
        w_for_month_nums = 0;
        k_for_month_nums = 0
        y_for_day_nums = 0;
        w_for_year_nums = 0
        total_nums = 0
        # money_dict = {} # 每类数据公有多少行
        info_dict = {}  # 消息集合
        k_for_month = []  # 千/月
        w_for_month = []  # 万/月
        w_for_year = []  # 万/年
        y_for_day = []  # 元/天
        other_list = []
        for line in my_file:
            total_nums += 1
            if line.find("万/月") != -1:
                w_for_month_nums += 1
                type_list = line.split("万/月")[0].split("-")
                if len(type_list) == 2:
                    w_for_month.append(type_list[0])
                    w_for_month.append(type_list[1])
                elif len(type_list) == 1:
                    w_for_month.append(eval(type_list[0]) * 2)
            elif line.find("千/月") != -1:
                k_for_month_nums += 1
                type_list = line.split("千/月")[0].split("-")
                if len(type_list) == 2:
                    k_for_month.append(type_list[0])
                    k_for_month.append(type_list[1])
                elif len(type_list) == 1:
                    k_for_month.append(eval(type_list[0]) * 2)
            elif line.find("元/天") != -1:
                y_for_day_nums += 1
                type_list = line.split("元/天")[0].split("-")
                if len(type_list) == 2:
                    y_for_day.append(type_list[0])
                    y_for_day.append(type_list[1])
                elif len(type_list) == 1:
                    y_for_day.append(eval(type_list[0]) * 2)
            elif line.find("万/年") != -1:
                w_for_year_nums += 1
                type_list = line.split("万/年")[0].split("-")
                if len(type_list) == 2:
                    w_for_year.append(type_list[0])
                    w_for_year.append(type_list[1])
                elif len(type_list) == 1:
                    w_for_year.append(eval(type_list[0]) * 2)
            else:
                other_list.append(line)
        # print("总共" , total_nums)
        my_file.close()
        avg_w_month = self.get_count(w_for_month, "万/月") / 2 / w_for_month_nums
        avg_k_month = self.get_count(k_for_month, "千/月") / 2 / k_for_month_nums
        avg_y_day = self.get_count(y_for_day, "元/天") / 2 / y_for_day_nums
        avg_w_year = self.get_count(w_for_year, "万/年") / 2 / w_for_year_nums
        info_dict["avg"] = (avg_w_month + avg_k_month
                            + avg_y_day + avg_w_year) / 4
        info_dict["drop"] = len(other_list) / total_nums * 100
        return info_dict
        pass

    # 统一规格 万/月
    def get_count(self, type_list, type_code):
        money = 0
        if type_code == "万/月":
            for one in type_list:
                money += eval(str(one))
        elif type_code == "千/月":
            for one in type_list:
                money += eval(str(one))
            money = money / 10
        elif type_code == "元/天":
            for one in type_list:
                # print(one)
                money += eval(str(one))
            money = money * 30 / 10000
        elif type_code == "万/年":
            for one in type_list:
                money += eval(str(one))
            money = money / 12
        return money




if __name__=="__main__":

    path = os.path.abspath("./file/51jobs_北京_python_2018-11-27-17.16.money.txt")
    money_info = MoneyInfo(path)
    back_dict = money_info.get_info()
    print(back_dict)