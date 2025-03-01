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
                                                                    value=".card__content > .table-responsive > .table > tbody > tr >td")))  # CWE-ID行
    if debug:
        print("cwe info=", cweInfo)
    secProduct = list(map(lambda elem: elem.text, driver.find_elements(
        by=By.CSS_SELECTOR, value=".card.card--sidebar > .pl-3.pb-3 > .btn.btn-sm.btn-outline-success")))
    if debug:
        print("card info=", cardIntro, aliyunScore, secProduct)
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
    tableElemText = list(map(lambda elem: elem.text, driver.find_elements(
        by=By.CSS_SELECTOR, value=".pb-4.pt-3.table-responsive > .table > tbody > tr")))
    if debug:
        print(tableElemText)
    print("RawDocgend")
    affectDetail = []  # 类型	厂商	产品	版本	影响面
    for i in range(2, len(tableElemText), 2):
        affectDetail.append(tableElemText[i].split(' '))
        if debug:
            print(affectDetail[-1])
            print("类型= {}\n厂商= {}\n产品= {}\n版本= {}\n影响面= {}\n".format(
                affectDetail[-1][0], affectDetail[-1][1], affectDetail[-1][2], affectDetail[-1][3], " ".join(affectDetail[-1][4:])))

    # 生成md原始文档

    with open("./output_raw/{}.md".format(cveName), "w", encoding="utf-8") as rawFile:
        print("### {}".format(cveName), file=rawFile)
        print("#### 漏洞关键字\n{}".format(str(tags).replace(
            '[', '').replace(']', '').replace("'", "")), file=rawFile)
        print("#### 漏洞大致情况", file=rawFile)
        print("CVE编号: {}".format(briefIntro["CVE编号"]), file=rawFile)
        print("利用情况: {}".format(briefIntro["利用情况"]), file=rawFile)
        print("补丁情况: {}".format(briefIntro["补丁情况"]), file=rawFile)
        if len(cweInfo):
            print("CWEID: {}\n漏洞类型: {}".format(
                cweInfo[0], cweInfo[1]), file=rawFile)
        print("阿里云漏洞评分: {}".format(aliyunScore), file=rawFile)
        print(str(cardIntro).replace('{', '').replace(
            '}', '').replace("'", ""), file=rawFile)
        print("披露时间: {}".format(briefIntro["披露时间"]), file=rawFile)
        print("#### 漏洞描述及相关建议", file=rawFile)
        for text in detail:
            print(text, file=rawFile)
        print("#### 参考链接", file=rawFile)
        if len(refLink):
            for text in refLink:
                print(text, file=rawFile)
        else:
            print("无", file=rawFile)
        print("#### 影响面", file=rawFile)
        if len(affectDetail):
            for detail in affectDetail:
                print("类型: {}\n厂商: {}\n产品: {}\n版本: {}\n影响面: {}\n".format(
                    affectDetail[-1][0], affectDetail[-1][1], affectDetail[-1][2], affectDetail[-1][3], " ".join(affectDetail[-1][4:])), file=rawFile)
        else:
            print("未知", file=rawFile)

# 接入openAPi生成报告


def genDetailDoc():
    pass
