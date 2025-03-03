from Crawler import runCrawler
from utility import genDetailDoc
# runCrawler("CVE 漏洞库", 2, 0, 2)
# runCrawler("非CVE漏洞库", 2, 0, 2)
# runCrawler("高危漏洞", 2, 0, 2)

enableAI = 1  # 是否开启AI生成报告功能

apiKey = "your-api-key"
apiUrl = "https://api.deepseek.com"
modelName = "deepseek-chat"

if enableAI:
    genDetailDoc(apiKey, modelName, apiUrl, 1)
