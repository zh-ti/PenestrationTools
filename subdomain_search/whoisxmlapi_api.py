import requests


class Api:
    base_url = "https://subdomains.whoisxmlapi.com/api/v1"
    apiKey = None

    def __init__(self, apiKey):
        self.apiKey = apiKey

    def search(self, domain):
        subdomains = set()
        params = {"apiKey": self.apiKey, "domainName": domain}
        try:
            res = requests.get(self.base_url, params=params)
            if res.status_code == 200:
                data = res.json()['result']['records']
                for item in data:
                    subdomains.add(item['domain'])
            else:
                print(f"请求错误，响应代码【{res.status_code}】, 原因【{res.reason}】")
        except Exception as e:
            print(f"请求失败：\n{e.args[0]}")
        return subdomains
