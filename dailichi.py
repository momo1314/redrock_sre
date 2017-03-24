#coding=utf-8
import requests
import re
import string
import random
import gevent
from time import *
from gevent.threadpool import ThreadPool
def get_ip(text):
	rex = r'''<td class="country"><img src=.*?/></td>\s*?<td>(.*?)</td>\s*?<td>(.*?)</td>\s*?<td>\s*.*\s*</td>\s*?.*\s*?<td>HTTPS</td>'''
	ip = re.findall(rex,text)
	return ip

url = [
	'http://www.xicidaili.com/nn/1',
	'http://www.xicidaili.com/nn/2',
	'http://www.xicidaili.com/nt/1',
	'http://www.xicidaili.com/nt/2',
	'http://www.xicidaili.com/wn/1',
	'http://www.xicidaili.com/wn/2',
	'http://www.xicidaili.com/wt/1',
	'http://www.xicidaili.com/wt/2',
]


def creat_pool(url):
	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		#'Accept-Encoding':'gzip, deflate, sdch',
		#'Accept-Language':'zh-CN,zh;q=0.8',
		'Connection':'keep-alive',
		'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTIxNDI1MzZlZTFlNjAzZmE2MThhOWUyMmJkMjhkZjhhBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTNYeU9ZWEpDeG5GWk9oOVhOcjladk9qczVSRGpWVDRFQVUzSlZaZ3UrQTQ9BjsARg%3D%3D--740e6e56cf503e3db454e101d0c62ed823fa07ac; CNZZDATA1256960793=250088865-1487378974-%7C1487381102',
		#'Host':'www.xicidaili.com',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'
	}
	data = []
	proxy_pool = []
	for i in url:
		r = requests.get(i,headers=headers)
		text = r.text
		ip = get_ip(text)
		data.extend(ip)

	for i in data:
		ip = i[0] +':'+ i[1]
		proxy_pool.append(ip)

	return proxy_pool


headers={
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	#'Accept-Encoding':'gzip, deflate, sdch',
	#'Accept-Language':'zh-CN,zh;q=0.8',
	'Cache-Control':'no-cache',
	#'Connection':'keep-alive',
	#'Cookie':'qHistory=aHR0cDovL3dob2lzLmNoaW5hei5jb20vK1dob2lz5p+l6K+i; CNZZDATA433095=cnzz_eid%3D1253356149-1487381892-%26ntime%3D1487381892; CNZZDATA5082706=cnzz_eid%3D340745156-1487381437-%26ntime%3D1487381437',
	#'Host':'www.mo-mo.party',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
}

def test_proxy(ip,proxy_pool,headers):
	try:
		kk = random.choice(string.ascii_letters+string.digits)
		r = requests.get('http://whois.chinaz.com/kk.gs',timeout = 3,proxies={'https':ip},headers=headers)
		if 'CopyRight 2002-2017' in r.text:
			pass
		else:
			proxy_pool.remove(ip)
	except:
		proxy_pool.remove(ip)
		pass

	return proxy_pool


def multi_thread_test(proxy_pool):
	n = len(proxy_pool)
	pool = ThreadPool(n)

	for ip in proxy_pool:
		pool.spawn(test_proxy,ip,proxy_pool,headers)
	gevent.wait()
	return proxy_pool

def main():
	t1 = time()
	print('正在扫描代理:')
	proxy_pool = creat_pool(url)
	proxy_pool = multi_thread_test(proxy_pool)
	with open('daili.txt','w+') as f:
		for ip in proxy_pool:
			f.write(ip+'\n')
	print('代理已获取,耗时：'+（time()-t1))

main()

