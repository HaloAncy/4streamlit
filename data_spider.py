from datetime import datetime, timedelta
import json
import pandas as pd
# import numpy as np
import pickle
import os
# import random
from curl_cffi import requests

url_format = "https://api.investing.com/api/financialdata/historical/{}?start-date={}&end-date={}&time-frame=Daily&add-missing-rows=false"
# WTIoil_url = "https://api.investing.com/api/financialdata/historical/8849?start-date={}&end-date={}&time-frame=Daily&add-missing-rows=false"
# LBoil_url = "https://api.investing.com/api/financialdata/historical/8833?start-date={}&end-date={}&time-frame=Daily&add-missing-rows=false"
# gold_url = "https://api.investing.com/api/financialdata/historical/8830?start-date={}&end-date={}&time-frame=Daily&add-missing-rows=false"
# silver_url = "https://api.investing.com/api/financialdata/historical/8836?start-date={}&end-date={}&time-frame=Daily&add-missing-rows=false"
# copper_url = "https://api.investing.com/api/financialdata/historical/8831?start-date={}&end-date={}&time-frame=Daily&add-missing-rows=false"
# natural_gas_url = "https://api.investing.com/api/financialdata/historical/8862?start-date={}&end-date={}&time-frame=Daily&add-missing-rows=false"
# SPX_url = "https://api.investing.com/api/financialdata/historical/166?start-date={}&end-date={}&time-frame=Daily&add-missing-rows=false"
id4url_list = ["8849", "8833", "8830", "8836", "8831", "8862", "166"]
dataname_list = [
    "WTIoil", "LBoil", "gold", "silver", "copper", "natural_gas", "SPX"
]
# url_list = [
#     WTIoil_url, LBoil_url, gold_url, silver_url, copper_url, natural_gas_url,
#     SPX_url
# ]
datafile_list = [
    "WTI原油期货历史数据.csv", "伦敦布伦特原油期货历史数据.csv", "黄金期货历史数据.csv", "白银期货历史数据.csv",
    "铜期货历史数据.csv", "天然气期货历史数据.csv", "美国标准普尔500指数历史数据.csv"
]

BROWSERS = ["chrome", "safari", "safari_ios"]

headers = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "authority":
    "api.investing.com",
    "accept":
    "application/json, text/plain, */*",
    "accept-language":
    "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6",
    "domain-id":
    "cn",
    "origin":
    "https://cn.investing.com",
    # "referer": "https://cn.investing.com/commodities/crude-oil-historical-data",
    "sec-ch-ua":
    "\"Chromium\";v=\"123\", \"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\"",
    "sec-ch-ua-mobile":
    "?0",
    "sec-ch-ua-platform":
    "\"Windows\"",
    "sec-fetch-dest":
    "empty",
    "sec-fetch-mode":
    "cors",
    "sec-fetch-site":
    "same-site",
    "Authorization":
    "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTE2MTc4NjgsImp0aSI6IjI1ODE0NzIwNyIsImlhdCI6MTcxMTYxNDI2OCwiaXNzIjoiaW52ZXN0aW5nLmNvbSIsInVzZXJfaWQiOjI1ODE0NzIwNywicHJpbWFyeV9kb21haW5faWQiOiI2IiwiQXV0aG5TeXN0ZW1Ub2tlbiI6IiIsIkF1dGhuU2Vzc2lvblRva2VuIjoiIiwiRGV2aWNlVG9rZW4iOiIiLCJVYXBpVG9rZW4iOiJOSG8lMkZmbVZxUGpabElXeHFaVFExTWpGb05teGtaMlpqTVRKdmJEYzNNeVUwSURZNFpUSXdkbVJyYWlSbFpqVXBaVE5sTkQ1dU5tQmxOVEpxTURBd01UUm5QMjVsT2o1clpXZHNhR1ZqTlRJeGFUWm9aR0ZtWXpFNGIyZzNOek5vTkdFMk5HVTFNREJrTUdvM1pXODFhV1YzWlhrJTJCZWpZblpUY3lZakJ4TUhjME96OSUyQlpUVSUyQlpHVXpiR0JsWXpVMk1XUTJaR1JxWm0weE1XOXROMlV6S3pSJTJGIiwiQXV0aG5JZCI6IiIsIklzRG91YmxlRW5jcnlwdGVkIjpmYWxzZSwiRGV2aWNlSWQiOiIiLCJSZWZyZXNoRXhwaXJlZEF0IjoxNzE0MTM0MjY4fQ.Sod0XmHvLcRyc7VbMQHGDTYf4LbBCg1Q3oiD8xeKQN4"  # noqa
}


# 获取页面信息(完整url)
def get_html(url):
    # cookies = {'Cookie': COOKIES}
    # random.choice(["chrome119", "chrome120", ...])
    print(f"正在爬取 {url}")
    for browser in BROWSERS:
        print("use: ", browser)
        response = requests.get(url, headers=headers, impersonate=browser)
        # print(response.cookies)
        print("响应状态码：", response.status_code)
        if response.status_code == 200:
            return response.text
        print("try next browser")
    # print("Crawling failed")
    # return ""


# 选择所需数据部分url及填补时间信息
def get_data(url_id, start_date, end_date):
    complete_url = url_format.format(url_id, start_date, end_date)
    return get_html(complete_url)


# 数据列日期标准化函数
def date_standardization(rawdate):
    return datetime.strptime(rawdate,
                             "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")


# +%
def addpercenttag(percent):
    return percent + "%"


# 处理数字中的","分割符
def deal4num(strnum):
    return strnum.replace(',', '')


# 处理数据 获得合格格式的数据
def clean_data(data):
    data_dict = json.loads(data)
    datalist = data_dict['data']
    if datalist is None:  # 判断是否有新数据
        # print("无最新数据。")
        return
    # 获取
    newdata = pd.DataFrame()
    for each in datalist:
        newdata = pd.concat([newdata, pd.DataFrame([each])], ignore_index=True)
    # 去掉无用列
    newdata = newdata.drop([
        'direction_color', 'rowDate', 'rowDateRaw', 'volumeRaw',
        'last_closeRaw', 'last_openRaw', 'last_maxRaw', 'last_minRaw',
        'change_precentRaw'
    ],
                           axis=1)
    # 处理数据列格式
    newdata.loc[:, 'rowDateTimestamp'] = newdata['rowDateTimestamp'].apply(
        date_standardization)
    newdata.loc[:, 'change_precent'] = newdata['change_precent'].apply(
        addpercenttag)
    newdata.iloc[:, 1:5] = newdata.iloc[:, 1:5].apply(
        lambda column: column.apply(deal4num), axis=0)
    # 更换列名
    column_mapping = {
        'rowDateTimestamp': '日期',
        'last_close': '收盘',
        'last_open': '开盘',
        'last_max': '高',
        'last_min': '低',
        'volume': '交易量',
        'change_precent': '涨跌幅'
    }
    newdata = newdata.rename(columns=column_mapping)
    return newdata


data_start_date = "2015-1-1"
start_date = data_start_date
end_date = ""
data_update_flag = 2  # 0-first 1-update 2-updated
date_filename = 'endtime.pickle'  # 定义存取日期文件名

# 应优化为各个文件分别对应一个日期(存储日期列表)


# 保存最新日期
def save_date_file():
    with open(date_filename, 'w') as file:
        file.write(end_date.strftime("%Y-%m-%d"))


# 二进制存取
def save_date_file_byte():
    with open(date_filename, 'wb') as pkl_file:
        pickle.dump(end_date, pkl_file)


# with open(date_filename, 'rb') as pkl_file:
#     data = pickle.load(pkl_file)


# 获得标准起始日期 - datetime
def get_standardized_date():
    standardized_start_date = datetime.strptime(start_date, "%Y-%m-%d")
    standardized_end_date = datetime.strptime(end_date, "%Y-%m-%d")
    return standardized_start_date, standardized_end_date


def check_date_file():
    global start_date, end_date, data_update_flag  # change - use global
    # 获取当前日期
    current_date = datetime.now().strftime("%Y-%m-%d")
    print(f"当前日期为：{current_date}")

    print("读取日期文件：")
    # 检查文件是否存在
    if os.path.exists(date_filename):
        # 文件存在 读取
        with open(date_filename, 'r') as file:
            end_date = file.read().strip()  # strip()用于移除可能的空白字符
        if not end_date:  # 文件为空
            print("日期文件为空。")
            end_date = current_date
            data_update_flag = 0
        else:  # 文件非空
            print(f"日期文件存在，截止日期为：{end_date}")
            if current_date != end_date:
                data_update_flag = 1
                start_date = end_date  # 需+1
                end_date = current_date
    else:  # 文件不存在 用当前最新日期作为截止日期保存
        # 创建文件并写入当前的年月日
        # with open(filename, 'w') as file:
        #     file.write(current_date)
        # 爬取成功后更新日期
        print("日期文件不存在。")
        end_date = current_date
        data_update_flag = 0

    # +1
    start_date, end_date = get_standardized_date()
    if data_update_flag == 1:
        one_day = timedelta(days=1)
        start_date = start_date + one_day


# 获得标准起始日期 - str
def get_standardized_str_date():
    standardized_start_date = start_date.strftime("%Y-%m-%d")
    standardized_end_date = end_date.strftime("%Y-%m-%d")
    return standardized_start_date, standardized_end_date


# 具体操作
def script_select():
    # 判断+文件接口
    if data_update_flag == 2:
        print("数据已为最新。")
    else:
        print("数据可能需要更新。")
        start_date, end_date = get_standardized_str_date()
        print(f"start_date: {start_date}")
        print(f"end_date: {end_date}")

        for each in range(len(dataname_list)):
            each_name, each_id, each_filename = dataname_list[
                each], id4url_list[each], datafile_list[each]
            data = get_data(each_id, start_date, end_date)
            if data is not None:  # 判断爬取情况
                newdata = clean_data(data)
                if newdata is not None:  # 是否有新数据
                    # 判断数据文件是否存在
                    if data_update_flag == 0:
                        print("暂无数据文件。")
                        updated_data = newdata
                    if data_update_flag == 1:
                        print("数据文件存在。")
                        existing_data = pd.read_csv(each_filename)
                        updated_data = pd.concat([newdata, existing_data])
                    # 覆盖原始文件
                    updated_data.to_csv(each_filename, index=False, quoting=2)
                    save_date_file()
                else:
                    print(f"{each_name}无最新数据。")
            else:  # 爬取失败
                print(f"{each_name} crawling failed")
                # return


def main():
    # 改变当前工作目录
    # data_file_path = "C:\\baiduTB\\BaiduSyncdisk\\workspace\\workspace for py\\YCproject\\update\\"
    # os.chdir(data_file_path)
    check_date_file()
    script_select()


# if __name__ == "__main__":
main()
