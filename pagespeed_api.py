def curl(url):
    import subprocess, json
    bashCommand = ['curl',
                   'https://www.googleapis.com/pagespeedonline/v2/runPagespeed?url=' + url + '&key=AIzaSyBRFX09gCpUvE_uQiLEPCeaY8ia75nLYho']

    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = ' '.join(str(output.decode('utf-8')).replace('\\n', '').replace('\'', '').split())

    # JSON parsing
    dict = json.loads(output)
    ## page state
    pageStats = {}
    keys = list(dict['pageStats'].keys())
    for i in keys:
        temp = {i: dict['pageStats'][i]}
        pageStats.update(temp)

    ## Rule
    rule = {}
    keys = list(dict['formattedResults']['ruleResults'].keys())
    for i in keys:
        temp = {i: dict['formattedResults']['ruleResults'][i]['ruleImpact']}
        rule.update(temp)
    result = []
    result.append(pageStats)
    result.append(rule)
    return (result)

    # print(curl("http://www.naver.com"))