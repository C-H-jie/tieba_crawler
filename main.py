import time
import random
import requests
from bs4 import BeautifulSoup
from lxml import etree
import json


user_agent = [
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    ]


def change_ip():
    ip = requests.get( 此处填入代理IP网址  ).text.replace("\r","").replace("\n","")
    print(ip)
    proxies = {'http': ip,
               'https': ip
               }
    print(proxies)
    return proxies


def get_html(url,proxies):


    headers = {'User-Agent': random.choice(user_agent)}
    print(headers)
    try:
        response = requests.get(url, headers=headers,proxies = proxies,timeout=5).text
    except:
        proxies = change_ip()
        response = get_html(url,proxies)
    return response
    pass


if __name__ == '__main__':
        # i = 0
    proxies = change_ip()
    for i in range(0,274):
        trys = 0
        print("正在抓取第{}页".format(i))
        user_dict_list = []
        len_ = 0
        while len_ ==0:

            if trys>4:
                proxies = change_ip()
                trys=0

            html = get_html("https://tieba.baidu.com/p/7769616907?pn={}".format(i),proxies)
            trys +=1
            # print(html)
            # print()
            data = etree.HTML(html)
            # soup = BeautifulSoup(html, 'lxml')
            # user_list = soup.find_all(class_='l_post l_post_bright j_l_post clearfix  ')

            user_list = data.xpath('//*[@id="j_p_postlist"]/div')
            # data.id

            len_ = len(user_list)
            print(len(user_list))
            # time.sleep(2)

        for user in user_list:
            # user.get('data-field')
            # 抓取用户信息
            user_infr = user.get('data-field')
            print(user_infr)

            user_dict = json.loads(user_infr)

            # 抓取用户发言
            user_message = user.xpath('.//div[2]/div[1]/cc/div[2]/text()')
            # user_message =
            # user_message = user_message.replace('            ','')

            user_dict["user_message"] = user_message
            print(user_message)


            # 抓用户等级
            #                        .//div[1]/ul/li[4]/div/a/div[2]
            user_level = user.xpath('.//div[1]/ul/li[5]/div/a/div[2]/text()')
            if len(user_level)==0:
                user_level = user.xpath('.//div[1]/ul/li[4]/div/a/div[2]/text()')

            user_dict["user_level"] = user_level
            print(user_level)

            # 抓发帖时间
            #
            # user_time = user.xpath('.//span[@class="first"]/text()')
            # print(user_time)

            user_dict_list.append(user_dict)
        with open('json.txt','a',encoding='utf-8') as f:
            for user_dict in user_dict_list:
                user_dict = json.dumps(user_dict,ensure_ascii=False)
                f.write(user_dict)
                f.write("\n")

            # t = etree.tostring(user, encoding="utf-8", pretty_print=True)
            # print(t.decode("utf-8"))
        pass
