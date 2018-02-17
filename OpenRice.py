# coding: utf-8

# # Library


from urllib import request
import re
import requests
import sys
import csv


# # Functions


class func(object):
    def __init__(self):
        print ("Let's got this ....")

    # getsource

    def getsource(self, url):
        req = request.Request(url)
        req.add_header("user-agent",
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36")
        responese = request.urlopen(req)
        result = responese.read()
        return result

    # get restaurant all info
    def getallinfo(self, source):
        res = re.findall('<div class="content-cell-wrapper">(.*?)<!-- Start suggested restaurant list -->', source,
                         re.S)
        print (res)
        return res

    # get name info
    def getinfo(self, allinfo):
        info = {}
        info['res_name'] = re.search('value&quot;:null}]" >(.*?)</a>', allinfo, re.S).group(1)
        info['res_type'] = re.search('/en/hongkong/restaurants/cuisine(.*?)</a></li>', allinfo, re.S).group(1)
        a = re.search(
            '</a></li>\r\n            \r\n            <li><a href="/en/hongkong/restaurants(.*?)</a></li>\r\n            \r\n        </ul>\r\n',
            allinfo, re.S)
        if a == None:
            info['res_type2'] = 'None'
        else:
            info['res_type2'] = a.group(1)
        print (info)
        return info

    # save info
    def saveinfo(self, classinfo, save):
        f = open(save, 'a')
        for each in classinfo:
            f.writelines('res_name:' + each['res_name'] + ',res_type:' + each['res_type'] + ',res_type2:' + each[
                'res_type2'] + '\n')
        f.close()
        print('write file finished')




# # Main


if __name__ == '__main__':
    classinfo = []
    search = 'Harbourside'
    url = 'https://www.openrice.com/en/hongkong/restaurants?what=' + search
    testspider = func()
    html = testspider.getsource(url).decode('utf-8')



allinfo = testspider.getallinfo(html)

for key in allinfo:
    res_info = testspider.getinfo(key)
    classinfo.append(res_info)
testspider.saveinfo(classinfo, "testing.csv")


# # Add variable names


with open('testing.csv', newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]

with open('testing_final.csv', 'w', newline="") as f:
    w = csv.writer(f)
    w.writerow(['Res_Name', 'Res_type', 'Res_type2'])
    w.writerow(data)

