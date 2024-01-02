import socket, os


# 通过ip反查域名
def searchHostByDomain(domain):
    return socket.gethostbyname(domain)


# 查询域名的cdn
def searchCDNByDomain(domain):
    return os.popen('nslookup ' + domain).read()

