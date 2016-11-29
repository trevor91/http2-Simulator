import urllib
import json
import wpt_batch_lib
import time
import requests
import codecs
import shutil
import os
import requests
import re

def make_json(dirpath, hash_url):
    # Generate result for request & Extract hash_url
    arg_hash_url = hash_url

    # Make a directory
    if not os.path.exists("/Users/browsable/PycharmProjects/FEO-backend/static/wpt/"+dirpath):
        os.makedirs("/Users/browsable/PycharmProjects/FEO-backend/static/wpt/"+dirpath)

    # Check finishing test
    finishCheck(arg_hash_url)

    # Make waterfall.png / connection.png / screenshot.png
    make_img_file(dirpath, arg_hash_url)

    # Get a json data from wpt & Store json data
    """"
    url_resp = urllib.request.urlopen("http://www.webpagetest.org/jsonResult.php?test=" + hash_url)
    reader = codecs.getreader("utf-8")
    urls_json = json.load(reader(url_resp))
    urls_json = json.dumps(urls_json)
    urls_json = json.loads(urls_json)
    """
    url_resp = requests.get("http://www.webpagetest.org/jsonResult.php?test=" + arg_hash_url)
    url_resp = json.dumps(url_resp.text)
    urls_json = json.loads(url_resp)

    file_path = "/Users/browsable/PycharmProjects/FEO-backend/static/wpt/"+dirpath+"data.json"
    with open(file_path, "w") as my_file:
        my_file.write(urls_json)

def finishCheck(hash_url):
    url_list = []
    url_list.append(hash_url)

    batch_json = wpt_checker(url_list)
    cnt = 0
    while (int(batch_json[hash_url]) is not 200):
        #print("Not yet, Delay time : " + str(cnt)+"sec") # probe test
        cnt = cnt + 5
        batch_json= wpt_checker(url_list)
        time.sleep(5)
    else:   # Success ( Get 200 )
        #print("Complete !") # probe test
        pass

def wpt_checker(url):
    res = wpt_batch_lib.CheckBatchStatus(url)
    res = json.dumps(res)
    res = json.loads(res)
    return res

def make_img_file(dirpath, hash_url):
    arg_hash_url=hash_url

    with open("/Users/browsable/PycharmProjects/FEO-backend/static/wpt/"+dirpath+"waterfall.png", "wb") as waterfall_file:
        wf_response = requests.get("http://www.webpagetest.org/result/" + arg_hash_url + "/1_waterfall_thumb.png")
        waterfall_file.write(wf_response.content)

    with open("/Users/browsable/PycharmProjects/FEO-backend/static/wpt/"+dirpath+"screenshot.jpg", "wb") as screen_file:
        sc_response = requests.get("http://www.webpagetest.org/results/" + convert_hash(arg_hash_url) + "/1_screen.jpg")
        screen_file.write(sc_response.content)

    with open("/Users/browsable/PycharmProjects/FEO-backend/static/wpt/"+dirpath+"connection.png", "wb") as connection_file:
        cn_response = requests.get("http://www.webpagetest.org/waterfall.png?test=" + arg_hash_url +
                                "&run=1&width=930&type=connection&mime=1")
        connection_file.write(cn_response.content)

def convert_hash(hash):
    # ex) Convert Format, 161031_ZD_D6R to 16/10/31/ZD/D6R
    arg_hash=hash
    rec=re.compile(r'_')
    tmp=rec.split(arg_hash)
    tmp_date = int(tmp[0])
    tmp_date_str = str(tmp_date // 10000) + "/"+str(int((tmp_date % 10000 - tmp_date % 100)/100)) + "/" + str(tmp_date % 100)
    converted=arg_hash.replace("_","/")
    converted=converted.replace(tmp[0],tmp_date_str)
    return converted

#finishCheck("161031_ST_YBC")
#make_img_file("161110_39_25VF")