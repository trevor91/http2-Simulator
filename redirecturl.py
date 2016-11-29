import requests

headers = {'Accept': '*/*', \
           'user-agent': 'h2-check/1.0.1', \
           'Connection': 'Upgrade, HTTP2-Settings', \
           'Upgrade': 'h2c', \
           'HTTP2-Settings': '<base64url encoding of HTTP/2 SETTINGS payload>'}

def getURL(domain):
    r = requests.get('http://' + domain, headers=headers, allow_redirects=True)
    return r
