# -- coding:utf-8 --
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import os

import ListUtil
import CsvUtil
import GetDataJs as jsCode

url = r"http://www.fangdi.com.cn/old_house/old_house_list.html?district=9999a061b2bf2968&area=&verifyNo=&region=e5e5d9c5a207f8f8&blockName=%E6%A2%85%E5%B7%9D%E4%B8%80&check_input=luhv&time=&location="
path1 = r"http://www.fangdi.com.cn/old_house/"
target1 = r"../old_house/old_house_list_detail.html?id=12f5c6d19fa4159a"

resultDic = dict()
threadNum:int = 3

async def main():
    count = await fetchCount()
    if (count is None or count <= 0):
        print("Get count is fail.")
        return
    pages = list(range(1, count + 1))
    pages = ListUtil.chunk(pages, threadNum)
    groupNum = 1
    try:
        for pagesItems in pages:
            tasks = [fetchData(pageNum) for pageNum in pagesItems]
            print('===开始第%d组===' % groupNum)
            print(pagesItems)
            await asyncio.gather(*tasks)
            groupNum += 1
    except Exception as e:
        print("Get GroupNum %d Data have warnning" % groupNum)
        print(e)

    contentList:list = []
    for key, value in resultDic.items():
        contentList.append(['Page' + str(key)])
        print("Page %d" % key)
        for item in value:
            contentList.append(item)
            print(item)
    
    dataPath = os.getcwd()
    dataNameUtf8 = "dataUtf8.csv"
    dataNameGbk = "dataGbk.csv"
    fullPathUtf8 = os.path.join(dataPath, dataNameUtf8)
    fullPathGbk = os.path.join(dataPath, dataNameGbk)

    CsvUtil.SaveListToCsv(fullPathUtf8, contentList)
    CsvUtil.SaveListToCsv(fullPathGbk, contentList, True, 'gbk')

    # Directly fetch page 2 data
    # await fetchData(2)

async def fetchData(pageNum:int):
    await asyncio.sleep(pageNum)
    GetData = '''
    function GetData(){
        return receiveData;
    }
'''
    GetOldHouse = '''
function getOldHouse2(currentPage){
    receiveData = "ajax Start";
	$.ajax({
		type : "POST",
		contentType : "application/x-www-form-urlencoded;charset=utf-8",
		url : path+"/oldhouse/selectOldHouse.action",
		dataType : "json",
		data : {district:decodeURIComponent(vars.district),area:decodeURIComponent(vars.area),
		location:vars.location,price:decodeURIComponent(vars.price),region:decodeURIComponent(vars.region),
		blockName:vars.blockName,time:decodeURIComponent(vars.time),houseType:decodeURIComponent(vars.houseType),
		listingNo:decodeURIComponent(vars.listingNo),verifyNo:decodeURIComponent(vars.verifyNo),currentPage:currentPage},
	    success : function(data){
	    	var listdata = data.htmlView;
            receiveData = listdata;
	    }
	});
}
    '''
    # browser = await launch(headless=False, args=['--enable-automation','--disable-infobars','--window-size=50,50','--no-sandbox'], userDataDic=r'C:/Users/zcy/Downloads/userdata')

    browser = await launch(headless=False, args=['--enable-automation','--disable-infobars','--window-size=50,50'], userDataDic=r'C:\Users\zcy\Downloads\userdata')
    page = await browser.newPage()
    await page.setViewport({'width':1080, 'height': 1080})
    #await page.evaluateOnNewDocument(js1)
    await page.evaluateOnNewDocument(jsCode.webDriverOffJs)

    await page.goto(url)
    await page.waitForNavigation()
    # await page.goto(path1 + target1)
    await asyncio.sleep(1)

    await page.evaluate('receiveData = "Before";')
    await asyncio.sleep(0.2)
    print("start get %d" % pageNum)
    isSuccess = False
    for i in range(10):
        try:
            print("start %d" % i)
            await page.evaluate(GetOldHouse, pageNum)
            data = await page.evaluate(GetData)

            for i in range(30):
                data = await page.evaluate(GetData)
                print("page%d: try %dnd" % (pageNum, i + 1))
                if (data != "ajax Start"):
                    print("Page Number %d Content：" % pageNum)
                    pageDataList = ParseData(data)
                    resultDic[pageNum] = pageDataList
                    break
                await asyncio.sleep(1)
            isSuccess = True
            break
        except Exception as e:
            print("Encounter exception will to sleep 1s to continue try it.%d" % i)
            await asyncio.sleep(1)
    if (isSuccess):
        print('Get Page %d Finish.' % pageNum)
    else:
        print('Get data %d overtime.' % pageNum)
    print('获取内容%d结束' % i)
    await page.close()
    await browser.close()


async def fetchCount():
    js1 = '''() =>{
	    Object.defineProperties(navigator,{
		    webdriver:{
		        get: () => false
        }
	    })}
		'''
    GetData = '''
    function GetData(){
        return receiveData;
    }
'''
    GetOldHouse = '''
function getOldHouse2(currentPage){
    receiveData = "ajax Start";
	$.ajax({
		type : "POST",
		contentType : "application/x-www-form-urlencoded;charset=utf-8",
		url : path+"/oldhouse/selectOldHouse.action",
		dataType : "json",
		data : {district:decodeURIComponent(vars.district),area:decodeURIComponent(vars.area),
		location:vars.location,price:decodeURIComponent(vars.price),region:decodeURIComponent(vars.region),
		blockName:vars.blockName,time:decodeURIComponent(vars.time),houseType:decodeURIComponent(vars.houseType),
		listingNo:decodeURIComponent(vars.listingNo),verifyNo:decodeURIComponent(vars.verifyNo),currentPage:currentPage},
	    success : function(data){
	    	var listdata = data.htmlView;
            receiveData = listdata;
	    }
	});
}
    '''
    browser = await launch(headless=False, args=['--enable-automation','--disable-infobars','--window-size=50,50'], userDataDic=r'C:\Users\zcy\Downloads\userdata')
    page = await browser.newPage()
    await page.setViewport({'width':1000, 'height': 1000})
    await page.evaluateOnNewDocument(js1)

    gotoSuccess = False
    for i in range(5):
        try:
            await page.goto(url)
            await page.waitForNavigation()
            gotoSuccess = True
            break
        except Exception as e:
            print("等待1s再次请求,当前次数%d" % i)
            await asyncio.sleep(1)
    if (not gotoSuccess):
        print("数量请求超时，请检查网络")
        return

    await page.evaluate('receiveData = "Before";')

    isSuccess = False
    count:int = 0
    for i in range(30):
        try:
            if (count > 0):
                break
            await page.evaluate(GetOldHouse, 1)
            data = await page.evaluate(GetData)
            for i in range(30):
                data = await page.evaluate(GetData)
                print("Request Count Wait:%d" % (i + 1), end='\r')
                if (data != "ajax Start"):
                    count = GetDataCount(data)
                    isSuccess = True
                    break
                await asyncio.sleep(1)
        except Exception as e:
            print("Encounter exception will to sleep 1s to continue try it.%d" % i)
            await asyncio.sleep(1)
    if (isSuccess):
        print('Get Count Finish.')
    else:
        print('Get Count overtime.')
    print('获取页面Page结束')
    await page.close()
    await browser.close()
    return count



def ParseData(data:str, isLog:bool = False) -> list:
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find('table')
    # 提取表格数据
    rows = []
    for row in table.find_all('tr')[1:]:  # 跳过表头
        cells = []
        for cell in row.find_all('td'):
            # 如果有<a>标签，同时提取文本和href属性
            a_tag = cell.find('a')
            if a_tag:
                cell_data = path1 + a_tag.get('href')
            else:
                cell_data = cell.text
            cells.append(cell_data)
        rows.append(cells)

    if (isLog):
        # 打印表格数据
        for row in rows:
            print(row)

    return rows

    # paragraph = soup.find('input', id='PageCount')
    # print("\nPage Count:")
    # print(paragraph.attrs['value'])
    pass

def GetDataCount(data:str) -> int:
    "Get page count number"
    soup = BeautifulSoup(data, 'html.parser')
    paragraph = soup.find('input', id='PageCount')
    print("Page Count:")
    print(paragraph.attrs['value'])
    return int(paragraph.attrs['value'])




asyncio.get_event_loop().run_until_complete(main())