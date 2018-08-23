# -*- coding:utf-8 -*-
import urllib2
import json
import argparse
import random
import datetime

def baidu_subdomains(url,UA):
    subdomains=[]
    request=urllib2.Request(url='http://ce.baidu.com/index/getRelatedSites?site_address=%s' % url)
    request.add_header('User-Agent',UA)
    ret=urllib2.urlopen(request)
    try:
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+u' 正在通过百度接口进行查询......'
        ret=json.loads(ret.read())
    except Exception, urllib2.HTTPError:
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+u' 警告：百度接口连接错误 ' + str(urllib2.HTTPError)
        return subdomains
    else:
        if ret.get('code')==0:
            for data in ret.get('data'):
                subdomains.append(data.get('domain'))
            print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+u' 百度接口查询结果返回中......'
        else:
            print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+u' 警告:'+ret.get('message')
        return subdomains

def virustotal_subdomains(url,UA):
    subdomains = []
    request = urllib2.Request(url="https://www.virustotal.com/ui/domains/%s/subdomains"%url)
    request.add_header('User-Agent', UA)
    try:
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+u' 正在通过Virustotal接口进行查询......'
        ret = urllib2.urlopen(request)
    except Exception, urllib2.HTTPError:
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+u' 警告：Virustotal接口连接错误 ' + str(urllib2.HTTPError)
        return subdomains
    else:
        ret=json.loads(ret.read())
        for data in ret.get('data'):
            subdomains.append(data.get('id'))
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+u' Virustotal接口查询结果返回中......'
        return subdomains

def random_ua():
    UA = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52", ]
    index=random.randint(0,15)
    return UA[index]


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='*********子域名查询工具*********')
    parser.add_argument('-u,--url',dest='url',help='需要查询的主域名',type=str)
    parser.add_argument('-f,--file',dest='file',help='查询结果保存文件名',type=str)
    args=parser.parse_args()
    url=args.url
    path=args.file
    if url !=None:
        ret=set()
        bd_ret=baidu_subdomains(url,random_ua())
        virustotal_ret=virustotal_subdomains(url,random_ua())
        ret_pre=bd_ret+virustotal_ret
        for i in ret_pre:
            if i not in ret:
                ret.add(i)
                print i
        if path !=None:
            with open(path,'wb+') as file:
                file.write('以下为%s的查询结果：\n'%url)
                for i in ret:
                    file.write(i+'\n')
            print '查询结果保存在当前脚本文件夹下的%s中'%path
    else:
        parser.print_help()
        exit()