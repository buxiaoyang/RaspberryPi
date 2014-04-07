#coding=utf-8
#! /usr/bin/python   
""" 
引入Python 块
"""
import weibo  
import os
import time
import urllib2
import random
import linecache
import urllib2
import urllib
from weibo import APIClient
""" 
授权需要的三个信息，APP_KEY、APP_SECRET为创建应用时分配的，CALL_BACK在应用的设置网页中 
设置的。【注意】这里授权时使用的CALL_BACK地址与应用中设置的CALL_BACK必须一致，否则会出 
现redirect_uri_mismatch的错误。 
"""  
  

#打招呼函数
#def hello():
#        count = len(open('hello.txt','rU').readlines())
#        hellonum=random.randrange(1,count, 1)
#        return linecache.getline('hello.txt',hellonum)
#网站监控函数
#def http_monitor():
#    try:
#        data = urllib2.urlopen('http://i.ice.gs/',timeout=30)
#        return '妥妥的！'
#    except:
#        return '妈蛋服务器进水啦！主人@GGICE 快去瞅瞅'

#获取DS18B20温度
def read_temperature():
    try:
        # Open the file that we viewed earlier so that python can see what is in it. Replace the serial number as before. 
        tfile = open("/sys/bus/w1/devices/28-00000332ef80/w1_slave") 
        # Read all of the text in the file. 
        text = tfile.read() 
        # Close the file now that the text has been read. 
        tfile.close() 
        # Split the text with new lines (\n) and select the second line. 
        secondline = text.split("\n")[1] 
        # Split the line into words, referring to the spaces, and select the 10th word (counting from 0). 
        temperaturedata = secondline.split(" ")[9] 
        # The first two characters are "t=", so get rid of those and convert the temperature from a string to a number. 
        temperature = float(temperaturedata[2:]) 
        # Put the decimal point in the right place and display it. 
        temperature = temperature / 1000 
        return temperature
    except:
        return 0.00

def login_getcilent():
    #模拟登陆
    APP_KEY = linecache.getline('/etc/grobot/db',1)
    APP_SECRET = linecache.getline('/etc/grobot/db',2)
    USERID = linecache.getline('/etc/grobot/db',3)
    PASSWD = linecache.getline('/etc/grobot/db',4)
    APP_KEY = APP_KEY.strip('\n')
    APP_SECRET = APP_SECRET.strip('\n')
    USERID = USERID.strip('\n')
    PASSWD = PASSWD.strip('\n')
    CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    referer_url = client.get_authorize_url()
    print "referer url is : %s" % referer_url
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    urllib2.install_opener(opener)
    postdata = {"client_id": APP_KEY,
             "redirect_uri": CALLBACK_URL,
             "userId": USERID,
             "passwd": PASSWD,
             "isLoginSina": "0",
             "action": "submit",
             "response_type": "code",
             }
 
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
               "Host": "api.weibo.com",
               "Referer": referer_url
             }
 
    req  = urllib2.Request(
                           url = referer_url,
                           data = urllib.urlencode(postdata),
                           headers = headers
                           )
    try:
        resp = urllib2.urlopen(req)
        print "callback url is : %s" % resp.geturl()
        print "code is : %s" % resp.geturl()[-32:]
        code=resp.geturl()[-32:]
        r = client.request_access_token(code)  
        #将access_token和expire_in设置到client对象  
        client.set_access_token(r.access_token, r.expires_in)
        return client
    except Exception, e:
        print e  
        
#主要函数
def run():
    client = login_getcilent()
    #获取时间    
    thetime=time.strftime('%M%S',time.localtime(time.time())) 
    #获取cup温度
    #float_temp = float(os.popen('vcgencmd measure_temp').readline().replace("temp=","").replace("'C\n",""))
    #获取DS18B20温度
    float_temp = read_temperature()
    #获取运行时间
    uptime = {}
    f = open("/proc/uptime")
    con = f.read().split()
    f.close()
    all_sec = float(con[0])
    MINUTE,HOUR,DAY = 60,3600,86400
    uptime['day'] = int(all_sec / DAY )
    uptime['hour'] = int((all_sec % DAY) / HOUR)
    uptime['minute'] = int((all_sec % HOUR) / MINUTE)
    uptime['second'] = int(all_sec % MINUTE)
    uptime['allminute']= int(all_sec / MINUTE)
    uptime['Free rate'] = float(con[1]) / float(con[0])
    #获取网站监控信息
    #wz=http_monitor()
    #整理微博信息
    text_temp = '喵喵~ 主人，我已经活动%d天%d小时啦。 现在室内温度是%.2f°C。' %(uptime['day'],uptime['hour'],float_temp)
    print text_temp  
    client.statuses.update.post(status=text_temp)  
    print "Send succesfully!"

if __name__ == "__main__":  
    run()  
