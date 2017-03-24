#-*- coding: utf-8 -*-
#! /usr/bin/env python3
import requests,re,random,time
class whois():
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.8 Safari/537.36',
        'Accept-Language':'zh-CN,zh;q=0.8',
    }
    re = {
    'fkey':r'(?<=var pendingWhoisRefresh = ")[a-z0-9]+(?=")',\
    'makesure':r'(?<=var cacheTimeLeft = ")[0-9]+(?=")',\
    'jvjue':r'升级|频繁',\
    'bad' : r'重试|超时',\
    'success' : r'No Object Found|未被注册或被隐藏|object does not exist|No match for',\
    'not' : r'未知域名|域名不合法'
    }
    url_1 = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain='
    url_2 = 'http://whois.chinaz.com/'
    url_3 = 'https://who.is/whois/'
    k = 0
    #def __init__(self):
    def chinaz(self,domain):
        try:

            with open('daili.txt','r') as f:
                print('加载代理文件-------')
                ip = f.readlines()
            #print('加载成功，选择代理中')
            rip = random.choice(ip).split('\n')
            #print('选择成功')
            url = self.url_2+domain
            #print('正在连接'+url)
            f = requests.get(url,headers=self.headers,timeout=15,proxies={'http':rip[0]})
            #print('连接成功')
            find = re.findall(self.re['jvjue'],f.text)
            if find != []:
                #print('代理加载时间过长，正在重新选择')
                ip.remove(rip)
                exit(0)
            find = re.findall(self.re['bad'],f.text)
            if find !=[]:
                #print('网络连接超时，正在重试------')
                exit(0)
            find = re.findall(self.re['success'],f.text)
            find_=re.findall(self.re['bad'],f.text)
            if f1 != []:
                    if f2 == []:
                        print (domain+'   yes')
                        with open('domain.txt','a') as file:
                            file.write(domain+'\n')
                        return 1
                    else:
                        print('[-]域名后缀不存在，请查证后再进行查询')
                        return -1
            else:
                    if f2 == []:
                        print(domain+'   no')
                        return 0
                    else:
                        print('[-]域名后缀不存在，请查证后再进行查询')
                        return -1
        except:
            self.k = self.k + 1
            time.sleep(0.01)
            if self.k < 5:
                return self.chinaz(domain)
            else:
                return -1
    
    z = 0
    def who_is(self,domain):
        try:
            url = self.url_3+domain
            f = requests.get(url,headers=self.headers,timeout=15)
            fkey = re.search(self.re['fkey'],f.text)
            makesure = re.search(self.re['makesure'],f.text)
            if makesure.group(0) <= '86100':
                url =url+'?forceRefresh='+ fkey.group(0)
                f = requests.get(url,headers=self.headers,timeout=15)
            find = re.findall(self.re['success'],f.text)
            if find != []:
                print (domain+'   yes')
                with open('domain.txt','a') as file:
                    file.write(domain+'\n')
                return 1
            else:
                print(domain+'   no')
                return 0
        except :
            self.z = self.z + 1
            time.sleep(0.05)
            #print('我日 挂了  重来')
            if self.z > 5:
                print('失败次数过多，正在尝试连接到其他网站（不稳定）:')
                return self.chinaz(domain)
            else:
                return self.who_is(domain)
        
    
    s = 0
    def request(self,domain):
        try:
            url = self.url_1+domain
            f = requests.get(url,headers=self.headers,timeout=15)
            if self.r > 10:
                return -2
            if '210' in f.text:
                print (domain+'   yes')
                with open('domain.txt','a') as file:
                        file.write(domain+'\n')
                return 1
            elif '211' in f.text:
                print(domain+'   no')
                return 0
            elif '212' in f.text:
                exit(0)
            elif '500' in f.text:
                #peint('连接失败，等待重试')
                self.s = self.s + 1
                time.sleep(15)
                return self.request(domain)

            elif 'Maximum number of open connections reached.' in f.text:
                #print('当前查询量过大，等待重试')
                self.s = self.s + 1
                time.sleep(20)
                return self.request(domain)

            elif '213' in f.text:
                print('%s域名后缀错误' % tld)
                return -1
            else:
                #print('未知错误，等待重试')
                self.s = self.s + 1
                time.sleep(1)
                return self.request(domain)
        except:
            print('网络拥堵，正在尝试连接其他域名商')
            return self.who_is(domain)


