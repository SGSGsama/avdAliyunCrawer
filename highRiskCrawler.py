from time import sleep
from utility import init_driver, genRawDoc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def runHighRiskCrawler(debug: bool = 0):
    driver = init_driver("https://avd.aliyun.com/")
    highRiskPage = driver.find_element(by=By.LINK_TEXT, value="高危漏洞")
    if debug:
        print("in "+driver.title+"  at "+driver.current_url)
        # input("continue")
    actions = ActionChains(driver)
    actions.move_to_element(highRiskPage)
    actions.key_down(Keys.CONTROL).click(
        highRiskPage).key_up(Keys.CONTROL).perform()  # 进入高危漏洞库列表
    sleep(1)  # 等待加载
    print("sleep finished")

    driver.switch_to.window(driver.window_handles[-1])  # 切换至漏洞库窗口
    links = driver.find_elements(By.TAG_NAME, "a")
    # print(len(links))
    if debug:
        # print(driver.window_handles)
        print("in "+driver.title+"  at "+driver.current_url)
        # input("continue")

    for link in links:  # 遍历所有超链接
        if "detail" in link.get_attribute("href"):
            link.click()  # 进入cve
            sleep(1)
            driver.switch_to.window(driver.window_handles[-1])  # 切换至新窗口
            button = driver.find_elements(
                by=By.CSS_SELECTOR, value=".btn.btn-link.text-muted")
            if len(button):
                button[0].click()
            genRawDoc(driver, debug)
            if debug:
                print("in "+driver.title+"  at "+driver.current_url)
                input("continue")
            driver.close()
            # input("closed")
            driver.switch_to.window(driver.window_handles[-1])
            if debug:
                print("in "+driver.title+"  at "+driver.current_url)
                # input("continue")
