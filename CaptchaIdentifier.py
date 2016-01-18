#!/usr/bin/env python
#coding:utf-8
"""
  Author : Chaos--<chaosimpler@gmail.com>
  Purpose: 
  Created: 2016/1/15
"""
from PIL import Image
import os
import random
import urllib
import pickle


# CMCC-EDU 验证码的地址
captchaURL='http://218.200.239.185:8888/portalserver/user/randomimage'
randomMax=1000000
# 对已训练的分类器进行序列化后存储的文件
CLF_Dump='CLF_DUMP.dat'




#----------------------------------------------------------------------
def __downloadSomePics(picCount=50,filePath="pic/test"):
    """
    函数功能：
        下载一些验证码图片，存入指定路径
    """    
    for i in range(picCount):
        print "download", i
        pName="{0}/%04d.gif".format(filePath) % i
        file(pName, "wb").write(urllib.urlopen(captchaURL).read())   

#----------------------------------------------------------------------
def __splitSinglePic(pic="pic/0000.gif",path="pic/split"):
    """
    函数功能：
        （人工标记训练数据时使用）
        将单张图片先转换成二值化，然后切割成4个小图片，随机取名存储到指定的路径下；
        人工标记时，只需要将分割后的小图片分别放进不同的文件夹即可
    """
    img=Image.open(pic)
    for i in range(4):
        x=2+i*11
        y=2
        fName="{0}/%d.gif".format(path) % random.randint(1,randomMax)
        while os.path.exists(fName):
            fName="{0}/%d.gif".format(path) % random.randint(1,randomMax)
        img.crop((x,y,x+9,y+13)).convert("1").save(fName)    
    

#----------------------------------------------------------------------
def __getPicData(picFile):
    """
    函数功能：
        将指定（二值化后）图片的每个像素点的数值写入一个list并返回
    """
    t=Image.open(picFile)
    return list(t.getdata())
    

#----------------------------------------------------------------------
def __makeTrainData():
    """
    函数功能：
        获取训练数据和对应的标签信息
    """
    data=[]
    target=[]
    
    for i in range(10):
        path="pic\split\{0}".format(i)
        for f in os.listdir(path):
            pf=os.path.join(path,f)
            data.append(__getPicData(pf))
            target.append(str(i))
    
    return data,target

#----------------------------------------------------------------------
def __split_GetPicData(pic):
    """
    函数功能：
        对原始图片将其二值化，然后切割成四个图像，然后返回每个图像对应的数值
        返回值是一个list，包含切割后的四张图片的数据
    """
    data=[]
    img=Image.open(pic)
    for i in range(4):
        x=2+i*11
        y=2
        data.append(list(img.crop((x,y,x+9,y+13)).convert("1").getdata()))
    
    return data
    
#----------------------------------------------------------------------
def train(data,target,dumpFile=CLF_Dump):
    """
    函数功能：
        利用训练数据和其对应的标签训练一个分类器
    """
    
    from sklearn import neighbors
    clf=neighbors.KNeighborsClassifier(n_neighbors=1, p=2)
    clf.fit(data,target)
    
    #将训练好的分类器序列化
    pickle.dump(clf,open(dumpFile,'wb'))
        
    return clf

#----------------------------------------------------------------------
def __test():
    """
    函数功能：
        对该模块实现的主要功能进行测试
    """
    
    #获取训练数据
    data,target=__makeTrainData()
    #训练分类器    
    clf=train(data, target)
    
    
    testPath="pic\\test"
    for f in os.listdir(testPath):
        pf=os.path.join(testPath,f)
        
        #分割测试图片并获取切割后的四个图片的数据
        tdata=__split_GetPicData(pf)
        
        #利用机器学习进行预测
        fpredict=clf.predict(tdata).tostring()
        print fpredict
        
        #利用测试结果对测试图片进行重命名
        newName=os.path.join(testPath,"{0}.gif".format(fpredict))
        while os.path.exists(newName):
            newName=os.path.join(testPath,"{0}_{1}.gif".format(fpredict,random.randint(1,randomMax)))
        os.rename(pf,newName) 
    

#----------------------------------------------------------------------
def identifyCaptcha(pic):
    """
    函数功能：
        主要的对外接口
        对指定图片进行识别，返回识别后的字符串。
    """
    
    #如果没有训练好的分类器，则首先进行训练；否则，直接载入分类器
    if not os.path.exists(CLF_Dump):
        #获取训练数据
        data,target=__makeTrainData()
        #训练分类器    
        clf=train(data, target) 
    else:
        clf=pickle.load(open(CLF_Dump,'rb'))
    
    testdata=__split_GetPicData(pic)
    result=clf.predict(testdata).tostring()
    return result
    
if __name__ == '__main__':
    
   
    
    print 'over'
    
    