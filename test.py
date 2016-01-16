#!/usr/bin/env python
#coding:utf-8
"""
  Author : Chaos--<chaosimpler@gmail.com>
  Purpose: 
  Created: 2016/1/16
"""
import CaptchaIdentifier as ci
import urllib


#----------------------------------------------------------------------
def showExecuteTime(func):
    """
    装饰器，显示函数时间信息
    """
    import time,datetime 
    ISOFORMAT='%Y-%m-%d %X'
    def _deco():
        tStart=datetime.datetime.now()
        
        print 'start at :' +time.strftime(ISOFORMAT,time.localtime())
        func()
        print 'end at   :' +time.strftime(ISOFORMAT,time.localtime())
        
        tEnd=datetime.datetime.now()
        print 'Running {0} seconds!'.format((tEnd-tStart).seconds)
    return _deco
    
#----------------------------------------------------------------------
@showExecuteTime
def test():
    """
    测试下载并识别一个验证码
    """
    pic='test.gif'
    file(pic, "wb").write(urllib.urlopen(ci.captchaURL).read())
    print ci.identifyCaptcha(pic)    

if __name__ == '__main__':
    test()
    
    
    