from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# 初始化浏览器


def init_driver(url: str):
    options = webdriver.ChromeOptions()
    options.add_argument("disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

# 生成未经ai处理的原始数据


def genRawDoc(driver: webdriver.Chrome, debug: bool = 0):
    # 收集tag
    tags = list(map(lambda tag: tag.text, driver.find_elements(
        by=By.CSS_SELECTOR, value=".breadcrumbs__list-item-last.CMSBreadCrumbsLink")))

    if debug:
        print("tags =", tags)
    # 收集编号等基本信息
    cveName = driver.find_element(
        by=By.CSS_SELECTOR, value=".header__title__text").text
    briefIntroElem = driver.find_elements(
        by=By.CSS_SELECTOR, value=".col-6.col-lg-3.pl-0")
    briefIntro = {}
    for elem in briefIntroElem:
        briefIntro[elem.find_element(by=By.CSS_SELECTOR, value=".metric-label").text] = elem.find_element(
            by=By.CSS_SELECTOR, value=".metric-value").text
    if debug:
        print("briefIntro =", briefIntro, cveName)
    # 右侧窗口中信息
    aliyunScore = driver.find_element(
        By.CSS_SELECTOR, value=".cvss-breakdown__score.cvss-breakdown__score--high").text
    cardIntroElem = driver.find_elements(
        by=By.CSS_SELECTOR, value=".cvss-breakdown__item")
    cardIntro = {}  # 卡片信息
    for elem in cardIntroElem:
        cardIntro[elem.find_element(by=By.CSS_SELECTOR, value=".cvss-breakdown__title").text] = elem.find_element(
            by=By.CSS_SELECTOR, value=".cvss-breakdown__desc").text
    cweInfo = list(map(lambda elem: elem.text, driver.find_elements(by=By.CSS_SELECTOR,
                                                                    value=".card.card--sidebar > .table-responsive > .table > tbody > tr >td")))  # CWE-ID行
    secProduct = list(map(lambda elem: elem.text, driver.find_elements(
        by=By.CSS_SELECTOR, value=".card.card--sidebar > .pl-3.pb-3 > .btn.btn-sm.btn-outline-success")))
    if debug:
        print("card info=", cardIntro, aliyunScore, cweInfo, secProduct)
    # 漏洞描述 & 解决建议
    detail = list(map(lambda elem: elem.text, driver.find_elements(
        by=By.CSS_SELECTOR, value=".text-detail.pt-2.pb-4")))
    if debug:
        print("detail= ", detail)
    # 参考链接
    refLink = list(map(lambda elem: elem.text,
                   driver.find_elements(by=By.CSS_SELECTOR, value=".text-detail.pb-3.pt-2.reference > .table.table-sm.table-responsive > tbody > tr > td > a")))
    if debug:
        print("refLink =", refLink)
    # 受影响软件情况
    print("RawDocgend")
