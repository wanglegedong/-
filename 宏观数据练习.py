from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
from selenium import webdriver
import time
import random
import csv

class hongguanshuju():
    def __init__(self):
        self.urls = ''  # 用来保存已爬取得url
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        self.iplist = [
            "123.163.96.88",
            "163.204.246.48",
            "183.129.244.16",
            "120.79.203.1",
            "114.113.222.131",
            "180.118.135.18",
            "120.25.203.182",
            "163.204.245.203",
            "59.37.33.62",
            "43.248.123.237",
            "175.44.156.198",
            "120.236.178.117",
            "183.158.202.222",
            "221.1.200.242",
            "61.176.223.7"
        ]  # 这是IP池
    def all_url(self,start_url):
        with open('shangshigongsi.csv', 'a', newline='') as csvfile:  # 保存到CSV列表里
            writer = csv.writer(csvfile)
            writer.writerow(['企业名称','英文名称', '曾用名' ,'所属地域' ,'所属行业', '公司网址', '主营业务', '产品名称','董事长','员工人数','联系电话','办公地址'])
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')   # 允许chrome使用自动化程序
        driver = webdriver.Chrome(options=option)  # 打开chrome浏览器
        driver.get(start_url)    #打开目标网址
        driver.maximize_window()  #全屏显示
        for i in range(1,571):
            self.geturl(driver)
            a=driver.find_element_by_xpath("//a[@title='下一页']").click()
            time.sleep(2)
            print('翻页成功')
            continue

    def geturl(self,driver):
        all_gupiaodaima = BeautifulSoup(driver.page_source, 'lxml').find('tbody').find_all('tr') # 解析网页
        for a in all_gupiaodaima:
            b=a.find_all('td')[1]
            print(b.get_text())
            url = 'http://s.askci.com/stock/summary/' + b.get_text()
            print(url)
            self.html(url)

    def html(self,url):
        html = self.request(url)
        try:
            qiyexinxi = BeautifulSoup(html.text, 'lxml').find('div',class_='right_f_c_table mg_tone').find_all('td')
        except:
            time.sleep(3)
            print(u'解析错误3S后重来')
            return self.html(url=url)
        print('爬取企业：',qiyexinxi[1].get_text())
        qiyemingcheng = qiyexinxi[1].get_text()
        yingwenmingcheng = qiyexinxi[3].get_text()
        cengyongming = qiyexinxi[5].get_text()
        suoshudiyu = qiyexinxi[7].get_text()
        suoshuhangye = qiyexinxi[9].get_text()
        gongsiwangzhi = qiyexinxi[11].get_text()
        zhuyingyewu = qiyexinxi[13].get_text()
        chanpinmingcheng = qiyexinxi[15].get_text()
        dongshizhang = qiyexinxi[23].get_text()
        yuangongrenshu = qiyexinxi[33].get_text()
        dianhua = qiyexinxi[35].get_text()
        bangongdizhi = qiyexinxi[41].get_text()
        with open('shangshigongsi.csv', 'a', newline='') as csvfile:  # 保存到CSV列表里
            writer = csv.writer(csvfile)
            writer.writerow([qiyemingcheng, yingwenmingcheng, cengyongming ,suoshudiyu ,suoshuhangye, gongsiwangzhi, zhuyingyewu, chanpinmingcheng,dongshizhang,yuangongrenshu,dianhua,bangongdizhi])

    def request(self,href):
        UA = random.choice(self.user_agent_list)          #随机选择请求头部
        headers = {'User-Agent': UA}
        try:
            content =requests.get(href, headers=headers,timeout=3)
            content.encoding = 'utf-8'  # 设置content为utf-8，否则会出现乱码
            return content
        except:
            print(u'开始使用代理')
            time.sleep(10)
            IP = ''.join(str(random.choice(self.iplist)).strip())  ##下面有解释哦
            proxy = {'http': IP}
            try:
                content =requests.get(href, headers=headers, proxies=proxy, timeout=3)
                content.encoding = 'utf-8'
                return content
            except:
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http': IP}
                    print(u'正在更换代理，10S后将重新获取')
                    print(u'当前代理是：', proxy)
                    return self.request(href=href)


shuju = hongguanshuju()
shuju.all_url("http://s.askci.com/stock/1/")