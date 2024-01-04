import requests
import re

headerStr = '''
:authority: subdomains.whoisxmlapi.com
:method: POST
:path: /api/web
:scheme: https
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: no-cache
Content-Length: 96
Content-Type: application/json
Origin: https://subdomains.whoisxmlapi.com
Pragma: no-cache
Referer: https://subdomains.whoisxmlapi.com/api
Sec-Ch-Ua: "Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
X-Csrf-Token: 6egrfhnOSqyfEbZfUPtwShSF5HrO0bSY3vNCjBZp
X-Requested-With: XMLHttpRequest
'''

headers = {}
for header in headerStr.split('\n'):
    if len(header) > 0:
        name, value = header.split(': ')
        headers[name] = value


class Api:
    base_url = "https://subdomains.whoisxmlapi.com/api/web"
    headers = None
    data = None
    cookies = None

    def __init__(self):
        self.headers = headers
        self.data = {'g-recaptcha-response': 'null', 'web-lookup-search': 'true'}
        self.cookies = {'whoisxmlapi-privacy-cookie': 'true', 'cf_12389_id': 'db1618d4-d657-4f24-ad20-bbe268c5e16c',
                        'cf_12389_person_last_update': '1704368419264'}

    def search(self, domain):
        subdomains = set()
        if not self.get_page_cookie():
            print('Set page_cookie is failed!')
        else:
            self.data['domainName'] = domain
            self.data['search'] = domain
            try:
                res = requests.post(self.base_url, headers=self.headers, data=self.data, cookies=self.cookies)
                if res.status_code == 200:
                    data = res.json()['result']['records']
                    for item in data:
                        subdomains.add(item['domain'])
                else:
                    print(f"请求错误，响应代码【{res.status_code}】, 原因【{res.reason}】: {res.content}")
            except Exception as e:
                print(f"请求失败：\n{e.args[0]}")
        return subdomains

    def get_page_cookie(self):
        params = {
            ':authority': 'subdomains.whoisxmlapi.com',
            ':method': 'GET',
            ':path': '/api',
            ':scheme': 'https',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        res = requests.get('https://subdomains.whoisxmlapi.com/api', params=params)
        if res.status_code == 200:
            cookie_str = res.headers['Set-Cookie']
            matched = re.findall('emailverification_session=[\w%]+|XSRF-TOKEN=[\w%]+', cookie_str)
            for cookie in matched:
                key, value = cookie.split('=')
                self.cookies[key] = value
            return True
        return False


api = Api()
arr = api.search('zh-ti.top')
print(arr)
