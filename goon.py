#-*- coding: utf-8 -*-
#! /usr/bin/env python3
import optparse,gevent,string
from my_whois import whois


with open('dailichi.py','r') as f:
        code = compile(f.read(), 'dailichi.py', 'exec')
        exec(code)
# with open('daili.txt','r') as f:
#         ip = f.readlines()
# def creat(domain):
#     tld = domain.split('\n')[-1]
#     list =  [x + y + '.' + tld for x in string.ascii_lowercase for y in string.ascii_lowercase ]+[x + y + z + '.' + tld for x in string.ascii_lowercase for y in string.ascii_lowercase for z in string.ascii_lowercase] + [x + y + z + w + '.' + tld for x in string.ascii_lowercase for y in string.ascii_lowercase for z in string.ascii_lowercase for w in string.digits]
#     return list
def creat(tld):
    list =  [x + y + '.' + tld for x in string.ascii_lowercase for y in string.ascii_lowercase ]+[x + y + z + '.' + tld for x in string.ascii_lowercase for y in string.ascii_lowercase for z in string.ascii_lowercase] + [x + y + z + w + '.' + tld for x in string.ascii_lowercase for y in string.ascii_lowercase for z in string.ascii_lowercase for w in string.digits]
    return list

def _pool(tld):#协程池
    from gevent.pool import Pool#协程池
    from gevent import monkey
    monkey.patch_all()
    fun = whois()
    with open('domain.txt','a') as file:
        file.write('there is some domain you can choose:\n')
    domains = creat(tld)
    n = len(domains)
    pool = Pool(n)
    pool.map(fun.request,domains)
    print('please go to see the domain.txt')

def _pool_(tld):#线程池
    from gevent.threadpool import ThreadPool#线程池
    fun = whois()
    with open('domain.txt','a') as file:
        file.write('there is some domain you can choose:\n')
    domains = creat(tld)
    n = len(domains)
    pool = ThreadPool(n)
    for domain in domains:
        pool.spawn(url_status,domain)
        time.sleep(0.01)
    gevent.wait()
    print('please go to see the domain.txt')

def pool_(tld):#进程池,并行查询
    from multiprocessing import Pool
    from multiprocessing.dummy import Pool as ThreadPool
    fun = whois()
    with open('domain.txt','a') as file:
        file.write('there is some domain you can choose:\n')
    domains = creat(tld)
    pool = ThreadPool(20)
    res = pool.map(fun.request,domains)
    pool.close()
    pool.join()
    print('please go to see the domain.txt')

def only(domain):
    fun = whois()
    req = fun.request(domain)
    if req == 1:
        print('this domain haven\'t been registered')
    elif req == 0:
        print('this domain can\'t be registered.')
    elif req == -1:
        print('the tld does not exist')
    else:
        print('网络连接故障（或过慢），请手动调试后重试')
def main():#使用进程池 其他未测试
    parser = optparse.OptionParser("-H <domain> 请输入你想要的域名，如49.gs \t -t <tld> 请输入想要遍历的域名后缀")
    parser.add_option('-H', dest = 'domain', type = 'string', help = 'specify domain')
    parser.add_option('-t',dest = 'tld',type = 'string',)
    (options,args) = parser.parse_args()
    domain = options.domain
    tld = options.tld
    if domain == None and tld == None:
        key = input('please choose a option:\n1:check a domain whether can be use.\n2:enter a tld to see any else domains haven\'t been register.\n')
        if key == '1':
            domain = input('please enter a domain:')
            print('正在查询，等待回馈:')
            only(domain)
        elif key == '2':
            tld = input("pleas input a tld:")
            print('正在查询，等待回馈:')
            pool_(tld)
        else:
            print('invalid input!')
            exit(0)
    elif domain == None and tld != None:
        print('正在查询，等待回馈:')
        pool_(tld)
    elif domain != None and tld == None:
        print('正在查询，等待回馈:')
        only(domain)

if __name__ == '__main__':
    main()
