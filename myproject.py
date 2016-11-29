from flask import Flask, render_template, request, jsonify, current_app, Response
from flask import send_from_directory
import extract_site
import h2checker, scraper, namesplit, operator, pagespeed_api, snapshot,os,redirecturl
from functools import wraps
import pymysql.cursors
# import gevent
# import gevent.monkey
# gevent.monkey.patch_all()

UPLOAD_FOLDER = '/Users/browsable/PycharmProjects/FEO-backend/web'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='1234',
                             db='feo',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
def event_stream(url):
    sitename=namesplit.make(url)
    fullurl = redirecturl.getURL(url).url
    if not os.path.isfile("/Users/browsable/PycharmProjects/FEO-backend/web/" + sitename +'.zip'):
        h1res,h2res = scraper.scraper(fullurl)
        if(h1res.status_code==200 and h2res.status_code==200):
            yield 'data: icon%s\n\n' % 3
    else:
        yield 'data: icon%s\n\n' % 3
    #page3
    if not os.path.exists("/Users/browsable/PycharmProjects/FEO-backend/static/wpt/" + sitename):
        h1url = 'https://www.h1test.net/web/'+sitename+'/'+sitename+'.html'
        h2url = 'https://www.h2test.net/web/'+sitename+'/'+sitename+'.html'
        originurl = redirecturl.getURL(sitename).url
        extract_site.generate_resouce_site(sitename,h1url,h2url,originurl)
    yield 'data: icon%s\n\n' % 5
    yield 'data: last-item\n\n'

@app.route('/my_event_source/<path:url>')
def sse_request(url):

    return Response(event_stream(url),mimetype='text/event-stream')

@app.route('/')
def main():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM feo.url_list ORDER BY cnt DESC LIMIT 0,4"
            cursor.execute(sql)
            url_list1 = cursor.fetchall()
            sql = "SELECT * FROM feo.url_list ORDER BY cnt DESC LIMIT 5,4"
            cursor.execute(sql)
            url_list2 = cursor.fetchall()
    finally:
        connection.commit()

    url = request.args.get('url')
    if (url == None or ""):
        return render_template('index.html', url_list1=url_list1, url_list2=url_list2)
    else:
        # h2scheck
        h2scheck = h2checker.checkH2S(url)
        if (h2checker.checkH2(url) == 2):
            return jsonify(url=url, notice='Failed to open URL')
        else:
            if (h2scheck == 3):
                return jsonify(url=url, notice='This domain supports HTTP/2')
            else: #not support http2
                try:
                    sitename = namesplit.make(url)
                    # make snapshot
                    imgname = sitename + ".png"
                    with connection.cursor() as cursor:
                        if os.path.isfile('static/images/' + imgname):
                            sql = "UPDATE `url_list` SET cnt=cnt+1 WHERE `sitename`=%s"
                            cursor.execute(sql, sitename)
                        else:
                            imgurl = 'images/' + imgname
                            sql = "INSERT INTO `url_list` (`sitename`, `imgurl`) VALUES (%s,%s)"
                            cursor.execute(sql, (sitename, imgurl))
                finally:
                    connection.commit()
                    # connection.close()
                return jsonify(url=url, notice='scraping')


@app.route('/scraping')
def scraping():
    url = request.args.get('url')
    fullurl = redirecturl.getURL(url).url
    sitename = namesplit.make(url)
    # if not os.path.isfile("/Users/browsable/PycharmProjects/FEO-backend/web/" + sitename +'.zip'):
    #     scraper.scraper(fullurl)
    imgurl = 'images/'+ sitename + ".png"
    # make snapshot
    pagespeed = pagespeed_api.curl(fullurl)
    red, orange, green = [], [], []

    pagespeed[1] = sorted(pagespeed[1].items(), key=operator.itemgetter(1))  # dictionary sorting
    for (key, val) in pagespeed[1]:
        if val == 0.0:
            green.append(key)
        elif val < 10:
            orange.append(key)
        else:
            red.append(key)
    return (render_template('page2.html', url=url,sitename=sitename,pagespeed=pagespeed[0], red=red, orange=orange, green=green, imgurl=imgurl))

@app.route('/iframe/<path:sitename>', methods=['GET', 'POST'])
def iframe(sitename):
    return render_template('iframe.html', sitename=sitename)

@app.route('/web/<path:filename>', methods=['GET', 'POST'])
def getzip(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)


@app.route('/result/<path:sitename>', methods=['GET', 'POST'])
def result(sitename):
    data_set = extract_site.get_data_list_comparison_site(sitename)
    return render_template("page3.html",sitename=sitename, data_set=data_set)

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data) + ')'
            return current_app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)

    return decorated_function


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
