import re
def make(url):
    try:
        sitename = re.sub(u'(.*?//|www.)', "", url)
        sitename = re.sub(u'(/.*|:.*)', "", sitename)
    except Exception:
        print("url error: " + url)
    return sitename

if __name__=="__main__":
    print(make("http://www.naver.com"))
    print(make("http://www.koreatech.ac.kr:80"))