import requests
from bs4 import BeautifulSoup
import time
import random



# print(label_container[1].find(attrs = {"class":"product_name"}).get_text())


# print(label_container[1].find(attrs = {"class":"product--label-container"}).get_text())


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def get_proxy_count():
    return requests.get("http://127.0.0.1:5010/count/").json()['count']


def getHtml(url):
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.get(url, proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    return None


req = getHtml("https://chiikawamarket.jp/collections/restock")
first_page = BeautifulSoup(req.text,features = "lxml")
page_num = list(first_page.find(attrs={"class":"pagination--numbers"}).children)
pages = int([i.get_text() for i in page_num][-2])

access_time = 0
update_count = 0
product_num_old = 0
while True:
    
    if update_count == 100:
        req = getHtml("https://chiikawamarket.jp/collections/restock")
        access_time += 1
        first_page = BeautifulSoup(req.text,features = "lxml")
        page_num = list(first_page.find(attrs={"class":"pagination--numbers"}).children)
        pages = int([i.get_text() for i in page_num][-2])
        update_count = 0
        time.sleep(30)

    product_num = 0
    for page in range(pages):
        time.sleep(random.randint(5,12))
        url = "https://chiikawamarket.jp/collections/restock?page=" + str(page)
        access_time += 1
        res = getHtml(url)
        if res.status_code == 200:
            bs_object = BeautifulSoup(res.text,features = "lxml")
            label_container = bs_object.find_all(attrs = {"class":"product--root"})
            product_num += len(label_container)
        else:
            print("connection error")
        proxy_count = get_proxy_count()
    print("访问次数: {}, 代理池数量: {}, 当前再入荷商品数量: {}".format(access_time, proxy_count, product_num))

    if product_num_old != product_num and update_count != 0:
        print("change")


    product_num_old = product_num
    update_count += 1

    