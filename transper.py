import requests, os, zipfile
import json
def transper (sitename):
    files_path = '/Users/browsable/Downloads/'+sitename+'_files'
    html_path = '/Users/browsable/Downloads/'+sitename+'.html'
    dest_file = 'web/'+sitename+'.zip'

    with zipfile.ZipFile(dest_file, 'w') as zf:
        rootpath = files_path
        for (path, dir, files) in os.walk(files_path):
            for file in  files:
                fullpath = os.path.join(path, file)
                relpath = sitename+'_files/'+os.path.relpath(fullpath, rootpath)
                zf.write(fullpath, relpath, zipfile.ZIP_DEFLATED)
                zf.write(fullpath, relpath, zipfile.ZIP_DEFLATED)
        zf.write(html_path, sitename+'.html', zipfile.ZIP_DEFLATED)
        zf.close()

    h1test = 'https://h1test.net/downloads'
    h2test = 'https://h2test.net/downloads'
    params = {'sitename': sitename}
    h1res = requests.get(h1test, params=params)
    h2res = requests.get(h2test, params=params)

    return h1res, h2res