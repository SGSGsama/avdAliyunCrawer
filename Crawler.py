from time import sleep
from utility import init_driver, genRawDoc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def runCrawler(catalog: str, number: int = 0, debug: bool = 0, sleepSecond: float = 1):
    '''
    sleepSecond为每跳转一个页面的等待时长，过短可能会触发限流或反爬\n
    如果cve的命名不符合windows文件命名规范则会转换为url命名输出\n
    catalog为要爬取的漏洞库的按钮文本{"CVE 漏洞库","非CVE漏洞库","高危漏洞"}\n
    number为爬取的记录数量，若不指定则在调用函数时提示输入
    '''
    driver = init_driver("https://avd.aliyun.com/")
    Page = driver.find_element(by=By.LINK_TEXT, value=catalog)
    if debug:
        print("in "+driver.title+"  at "+driver.current_url)
        # input("continue")
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).click(
        Page).key_up(Keys.CONTROL).perform()  # 进入漏洞库列表
    sleep(sleepSecond*1.5)  # 等待加载
    if debug:
        print("sleep finished")

    driver.switch_to.window(driver.window_handles[-1])  # 切换至漏洞库窗口

    links = driver.find_elements(By.TAG_NAME, "a")
    # print(len(links))
    if debug:
        # print(driver.window_handles)
        print("in "+driver.title+"  at "+driver.current_url)
        # input("continue")
    total = driver.find_element(
        by=By.CSS_SELECTOR, value="div.py-3.bg-light > div.container.vuln-list-container > div.py-3 > div.d-flex.justify-content-between.align-items-center > span.text-muted").text
    if debug:
        print(total[total.find("总计 ")+3: total.find(" 条记录")])
    total = int(total[total.find("总计 ")+3: total.find(" 条记录")])
    print("正在爬取 {}".format(catalog))
    toDo = number
    if toDo == 0:
        toDo = int(input("输入要爬取的记录条数，范围为 <={}\n".format(total)))
    hasNextPage = 1
    cnt = 0
    while hasNextPage and cnt < toDo:
        if debug:
            print("in"+driver.current_url)
        for link in links:  # 遍历所有超链接
            if "detail" in link.get_attribute("href"):
                link.click()  # 进入cve
                sleep(sleepSecond)
                driver.switch_to.window(
                    driver.window_handles[-1])  # 切换至新窗口
                button = driver.find_elements(
                    by=By.CSS_SELECTOR, value=".btn.btn-link.text-muted")
                if len(button):
                    button[0].click()
                genRawDoc(driver, debug)
                cnt += 1
                print("进度 {} / {}".format(cnt, toDo))
                if debug:
                    print("in "+driver.title+"  at "+driver.current_url)
                    input("continue")
                driver.close()
                # input("closed")
                driver.switch_to.window(driver.window_handles[-1])
                if debug:
                    print("in "+driver.title+"  at "+driver.current_url)
                    # input("continue")
            if cnt == toDo:
                break
        nextPageButton = driver.find_elements(
            by=By.CSS_SELECTOR, value=".px-3.btn.btn-sm.btn-outline-secondary.btn-bd-primary:not(.disabled)")
        if debug:
            print(len(nextPageButton))
        hasNextPage = 0
        for button in nextPageButton:
            if "下一页" in button.text:
                actions.key_down(Keys.CONTROL).click(
                    button).key_up(Keys.CONTROL).perform()
                # driver.close()
                sleep(sleepSecond)
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])
                hasNextPage = 1
                break
    driver.quit()
