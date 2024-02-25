from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# driver = webdriver.Edge()
path = r"C:\Users\zcy\Downloads\chrome-win64\chrome-win64\chromedriver.exe"
service = Service(executable_path=path)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors-yes')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(service=service, options=options)

url = r"http://www.fangdi.com.cn/old_house/old_house_list.html?district=9999a061b2bf2968&area=&verifyNo=&region=e5e5d9c5a207f8f8&blockName=%E6%A2%85%E5%B7%9D%E4%B8%80&check_input=&time=&location="

url = r"http://www.fangdi.com.cn"
# url = r"http://www.baidu.com"
# url = r"http://mi.com"
driver.get(url)
driver.maximize_window()

sleep(10)
driver.close()