import asyncio
from pyppeteer import launch
from pyppeteer import navigator_watcher
from pyquery import PyQuery as pq


url = r"http://www.fangdi.com.cn/old_house/old_house_list.html?district=9999a061b2bf2968&area=&verifyNo=&region=e5e5d9c5a207f8f8&blockName=%E6%A2%85%E5%B7%9D%E4%B8%80&check_input=&time=&location="

# url = r"http://www.fangdi.com.cn"
#url = r"http://www.fangdi.com.cn"
# async def main():
#     browser = await launch()
#     page = await browser.newPage()
#     await page.goto(url)
#     doc = pq(await page.content())
#     print("开始")
#     print(doc)
#     print("结束")
#     await browser.close()

async def main():
    # await launch(headless=False)
    # await asyncio.sleep(5)

    # browser = await launch(headless=False, args=['--enable-automation','--disable-infobars','--window-size=1366,768','--no-sandbox', 'disable-setuid-sandbox'], userDataDic='./userdata')
    # page = await browser.newPage()
    # await page.setViewport({'width':1366, 'height':768})
    # await page.evaluate(
    #     '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }'''
    # )
    # await page.goto(url)
    # await asyncio.sleep(100)

    js1 = '''() =>{
 
    Object.defineProperties(navigator,{
    webdriver:{
        get: () => false
        }
    })
    }'''
    
    js2 = '''() => {
        alert (
            window.navigator.webdriver
        )
    }'''
    #browser = await launch({'headless':False, 'args':['--no-sandbox'],})
    browser = await launch(headless=False, args=['--enable-automation','--disable-infobars','--window-size=1366,768','--no-sandbox', 'disable-setuid-sandbox'], userDataDic='./userdata')
    
    page = await browser.newPage()
    await page.evaluateOnNewDocument(js1)
    await page.evaluate(js2)
    await page.goto(url)
    await page.evaluate(js2)

    await asyncio.sleep(100)

asyncio.get_event_loop().run_until_complete(main())