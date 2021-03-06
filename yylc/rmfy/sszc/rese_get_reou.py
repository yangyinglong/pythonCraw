'''
create by yangyinglong at 20180425
get_response（）发送请求并接受response,
resolution()解析出公告的url,name,time,title
打包成元组装入list返回
'''

import requests
import re

ERROR_RESPONSE = 0
URL = 'http://www1.rmfysszc.gov.cn/News/handler.aspx'
BAIDU_API_URL = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=%s&callback=showLocation'
ak = 'wPh1zq1a818gaVKpOsGQEhrCBevNuVyy'

formData = {
	'search': '',
	'fid1': '90',
	'fid2': '',
	'fid3': '',
	'time': '',
	'time1': '',
	'page': '2',
	'include': '0'
}

requestHeaders = {
	'Accept':'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9',
	'Connection':'keep-alive',
	'Content-Length':'57',
	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	'Host':'www1.rmfysszc.gov.cn',
	'Origin':'http://www1.rmfysszc.gov.cn',
	'Referer':'http://www1.rmfysszc.gov.cn/News/Pmgg.shtml?fid=90&dh=3&st=0',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
}

def get_response(data=formData):
    'post requests to the server with form data and headers, return response, str'
    try:
        response = requests.post(URL, data=data, headers=requestHeaders, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        content = response.text
        if len(content) < 500:
            return ERROR_RESPONSE
        return content
    except:
        return ERROR_RESPONSE


def resolution(content, id=0):
	'resolution response return url, notice title, court name, Release time'
	notice_regex = re.compile(r'<a href=\'(.*?)\' title=\'(.*?)\' target=\'_blank\'>.*?class=\'n_c_l\' title=\'(.*?)\'.*?color: #313131;\'>(.*?)</span>', re.IGNORECASE)
	notice = notice_regex.findall(content)
	return notice

def get_location(address):
	''' give a address return location lng and lat'''
	url = BAIDU_API_URL % (address, ak)
	#print(url)
	try:
		response = requests.get(url, timeout=30)
		location = response.text.split('"location":')[1].split(',"precise"')[0]
		#print(location)
		lng = location.split('"lng":')[1].split(',"lat":')[0]
		lat = location.split('"lat":')[1].split('}')[0]
		location = lng + ',' + lat
		return location
	except Exception as e:
		print(e)
		return None
if __name__ == "__main__":
	a = get_location('长兴县雉城镇新城丽景22幢2-102室房屋、望春小区5幢第4、5号营业房产')
	print(a)
