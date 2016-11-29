import time, namesplit,transper
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui
import selenium.webdriver.support.ui as ui
import os
# 서버용 from pykeyboard import PyKeyboard

def scraper(url):
    sitename = namesplit.make(url)
    imgname = sitename + ".png"
    print(sitename)
    print("start")
    # profile = webdriver.FirefoxProfile()
    # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'file/]unknown')
    #browser = webdriver.Firefox(firefox_profile=profile)
    browser = webdriver.Firefox()
    browser.set_window_size(1920, 1080)
    browser.get(url)
    imgurl = 'static/images/' + imgname
    browser.save_screenshot(imgurl)
    pageFirst = ui.WebDriverWait(browser, 15).until(lambda browser: browser.find_element_by_tag_name('body'))
    # 서버용
    # pageFirst.send_keys(Keys.CONTROL + 's')
    pageFirst.send_keys(Keys.COMMAND + 's')
    time.sleep(1)
    # 서버용
    # k = PyKeyboard()
    # k.type_string(sitename, interval=0.1)
    # k.press_key(k.enter_key)
    # k.release_key(k.enter_key)
    # 맥 로컬용
    path = sitename + ".html"
    pyautogui.typewrite(path, interval=0.1)
    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')
    print("download")
    #os.path.dirname("/Users/browsable/Downloads/")
    while 1:
        if os.path.isfile("/Users/browsable/Downloads/" + path):
            time.sleep(1)
            browser.close()
            break
        time.sleep(1)
        print("1")

    return transper.transper(sitename)