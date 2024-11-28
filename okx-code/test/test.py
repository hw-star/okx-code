# ---------------------------------------------------
# encoding: utf-8
# @author: HWS
# @contact: xxx
# @time: 2024/11/10 16:10
# @desc: AUTO
# ---------------------------------------------------

import requests
from lxml import html


class SessionBasedExtractor:
    def __init__(self, url, headers=None):
        """
        初始化提取器
        :param url: 目标 URL
        :param headers: 请求头信息
        """
        self.url = url
        self.session = requests.Session()  # 创建一个会话
        self.headers = headers if headers else {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }
        self.session.headers.update(self.headers)  # 设置默认请求头

    def fetch_page(self):
        """
        使用会话获取网页内容
        :return: 响应内容的文本形式
        """
        try:
            response = self.session.get(self.url)
            print(response)
            response.raise_for_status()
            print(response.content.decode('utf-8'))
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"请求失败：{e}")
            return None

    def extract_value(self, xpath):
        """
        使用 lxml 提取 HTML 中的值
        :param xpath: 用于定位目标值的 XPath 表达式
        :return: 提取的值列表
        """
        html_content = self.fetch_page()
        # print(html_content)
        if not html_content:
            return []

        tree = html.fromstring(html_content)
        try:
            # 使用 XPath 提取目标值
            values = tree.xpath(xpath)
            return [value.strip() for value in values if value.strip()]
        except Exception as e:
            print(f"提取失败：{e}")
            return []

    def close_session(self):
        """关闭会话"""
        self.session.close()


# 示例使用
if __name__ == "__main__":
    url = "https://www.okx.com/zh-hans/trade-spot/shib-usdt"  # 替换为实际 URL
    xpath = '//span[@class="last"]/text()'  # 定位到目标 span 标签的 XPath 表达式

    extractor = SessionBasedExtractor(url)
    extracted_values = extractor.extract_value(xpath)
    extractor.close_session()  # 关闭会话

    print("提取的值：", extracted_values)