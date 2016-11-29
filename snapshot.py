def urlpageshot(url, name):
    from selenium import webdriver
    shot = webdriver.Firefox()
    shot.set_window_size(1920,1080)
    shot.get(url)
    imgurl = 'static/images/'+name
    shot.save_screenshot(imgurl)
    shot.close()
    shot.quit()
    return 'images/'+name

if __name__ == "__main__":
    urlpageshot("http://www.naver.com", "naver.png")