import send_info
import monety_analyze
import money_bugs


if __name__ == '__main__':
    city = "中国"
    language = "python"
    start_time = money_bugs.datetime.datetime.now()
    processA_mutex = money_bugs.threading.Lock()
    file_path = money_bugs.main(city, language,
                                80, processA_mutex)
    end_time = money_bugs.datetime.datetime.now()
    print("共用时: " ,(end_time - start_time).seconds, "s")

    money_info = monety_analyze.MoneyInfo(file_path)
    back_dict = money_info.get_info()

    print(""+city+""+language+
          "行情: %.3f 万/月" % back_dict["avg"])
    print("数据丢弃率: %f " % back_dict["drop"], "%")

    # my_dicts = {"任旭": "13363630863"}
    # Send = send_info.SendMessage()
    # Send.test_send(my_dicts, "SMS_150736399")
