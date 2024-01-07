import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
service = Service("/usr/local/bin/chromedriver")

# Create ChromeOptions if needed
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_experimental_option("detach", True)
global driver

url_keyword = "https://timviec365.vn/tim-kiem?keyword=ai&page="

# Initialize the Chrome browser with the service and options
driver = webdriver.Chrome(service=service, options=chrome_options)
elems = []
links = []
salary = []
names = []
address = []
description = []
requirement = []
benefit = []
for number in range(1,10):
    url = url_keyword + str(number)
    print(url)
    driver.get(url)
    time.sleep(1)
    elems = driver.find_elements(By.CSS_SELECTOR, "div.img_cate.box_new_left a.logo_user_th" )
    for elem in elems:
        links.append(elem.get_attribute("href"))
        names.append(elem.get_attribute("title"))

for link in links:
    driver.get(link)
    time.sleep(1)
    request = driver.find_elements(By.CSS_SELECTOR, "span.tag_red")
    if request is not None and request:
        salary.append(request[0].text)
        print(request[0].text)
    else:
        salary.append("null")
    request = driver.find_elements(By.CSS_SELECTOR, "span.diachi")
    if request is not None and request:
        address.append(request[0].text)
        print(request[0].text)
    else:
        address.append("null")
    request = driver.find_elements(By.CSS_SELECTOR, "div.text_content.ctn_chung_pd")
    if request is not None and request:
        print(request[0].text)
        description.append(request[0].text)
    else:
        description.append("null")
    request = driver.find_elements(By.CSS_SELECTOR, "div.text_content.w_100.ycau_tdung")
    if request is not None and request:
        print(request[0].text)
        requirement.append(request[0].text)
    else:
        requirement.append("null")
    request = driver.find_elements(By.CSS_SELECTOR, "div.text_content.ctn_chung_pd")
    if len(request) > 1:
        print(request[1].text)
        benefit.append(request[1].text)
    else:
        benefit.append("null")


import pandas as pd

# Tạo DataFrame từ danh sách thông tin
data = {'Job Name': names, 'Job_url': links, 'Description': description, 'Requirement': requirement, 'Benefit' : benefit, "Address" : address, "Salary" : salary}
df = pd.DataFrame(data)

# Xuất DataFrame vào một tệp Excel
df.to_excel('job_ai.xlsx', index=False)