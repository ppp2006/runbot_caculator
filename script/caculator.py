#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#Python语言: 把用汉字表示的数字转换为阿拉伯数字
#coding=UTF-8
#用途：把用汉字表示的数字转换为阿拉伯数字
#用法：cn2dig(汉字数字)
#作者：马踏飞燕<honeyday.mj@gmail.com>
#日期：2008-07-18
import roslib; roslib.load_manifest('qbo_caculator')
import rospy
import math
from std_msgs.msg import String
#from neo_talk.srv import *
 
CN_NUM = {
u'〇' : 0,
u'一' : 1,
u'二' : 2,
u'三' : 3,
u'四' : 4,
u'五' : 5,
u'六' : 6,
u'七' : 7,
u'八' : 8,
u'九' : 9,
 
u'零' : 0,
u'壹' : 1,
u'贰' : 2,
u'叁' : 3,
u'肆' : 4,
u'伍' : 5,
u'陆' : 6,
u'柒' : 7,
u'捌' : 8,
u'玖' : 9,
  
u'幺' : 1,
u'貮' : 2,
u'两' : 2,
}
CN_UNIT = {
u'十' : 10,
u'拾' : 10,
u'百' : 100,
u'佰' : 100,
u'千' : 1000,
u'仟' : 1000,
u'万' : 10000,
u'萬' : 10000,
u'亿' : 100000000,
u'億' : 100000000,
u'兆' : 1000000000000,
}
NUM_SET = set([u'零', u'一', u'幺', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九'])
UNIT_SET = set([u'十', u'百', u'千', u'万', u'佰', u'仟', u'萬', u'亿', u'億', u'兆'])
#action_list = [u'加上', u'减去', u'乘以', u'除以', u'加', u'减', u'乘', u'除']
action_list = [u'加上', u'减去', u'乘以', u'除以']
def cn2dig_simple(cn):
    lcn = list(cn)
    print lcn
    unit = 0 #当前的单位
    ldig = []#临时数组
    while lcn:
        cndig = lcn.pop()
        print ldig
        dig = CN_NUM.get(cndig)
        ldig.append(dig)
    print "ldig=%s,len(ldig)=%s"%(ldig,len(ldig))
    n = 0
    value=0
    while n < len(ldig):
        value += pow(10,n)*ldig[n]
        n += 1
    print "value=%d"%value
     
    #return ret
def cn2dig(cn):
    lcn = list(cn)
    print lcn
    unit = 0 #当前的单位
    ldig = []#临时数组
    while lcn:
        cndig = lcn.pop()
#        print ldig
        if CN_UNIT.has_key(cndig):
            unit = CN_UNIT.get(cndig)
            if unit==10000:
                ldig.append('w')    #标示万位
                unit = 1
            elif unit==100000000:
                ldig.append('y')    #标示亿位
                unit = 1
            elif unit==1000000000000:#标示兆位
                ldig.append('z')
                unit = 1
            continue
        else:
            dig = CN_NUM.get(cndig)
            if unit:
                dig = dig*unit
                unit = 0
            ldig.append(dig)
    if unit==10:    #处理10-19的数字
        ldig.append(10)
    print ldig #uncomment this line to watch the middle var.
    ret = 0
    tmp = 0
    while ldig:
        x = ldig.pop()
        if x=='w':
            tmp *= 10000
            ret += tmp
            tmp=0
        elif x=='y':
            tmp *= 100000000
            ret += tmp
            tmp=0
        elif x=='z':
            tmp *= 1000000000000
            ret += tmp
            tmp=0
        else:
            tmp += x
    ret += tmp
    print "value=%d"%ret
    return ret
    #ldig.reverse()
    #print ldig
    #print CN_NUM[u'七']
 
def listen_callback(msg):
    sentence = msg.data
    sentence = sentence.upper()
    sentence=sentence.decode('utf8')
    sentence_list=[]
    first_list=[]
    second_list=[]
    sentence=sentence.replace(" ","")
    print sentence
    sentence_list=sentence
    if set(sentence_list) <= NUM_SET:
        print "num subset %s"%sentence
        cn2dig_simple(sentence_list) 
        return 
    elif set(sentence_list) <= (NUM_SET|UNIT_SET):
        print "num and unit subset %s"%sentence  
        cn2dig(sentence_list)
        return 
    #else:
    for action in action_list:
        if(sentence.find(action)) > -1:
            sentence_list = sentence.split(action)
#            print sentence_list[0]
#            print sentence_list[1]
            first_list = sentence_list[0]
            second_list = sentence_list[1]
	    print first_list
            print second_list
            first = cn2dig(first_list)
            second = cn2dig(second_list)
            if(action == u"加上" or action ==u"加"):
                result = first + second
            elif(action == u"减去" or action ==u"减"):
                result = first - second
            elif(action == u"乘以" or action ==u"乘"):
                result = first * second  
            elif(action == u"除以" or action ==u"除"):
                result = first/second  
            text="%s %s %s = %s"%(first, action, second, result )
            print text
 #           speak_this(text)
    if set(sentence_list) <= NUM_SET:
        print "set %s"%sentence 
#    print set(sentence_list)
#    print NUM_SET
if __name__ == '__main__':

    rospy.init_node('qbo_caculator')
    
#just for test
#    client_speak = rospy.ServiceProxy("/say", Text2Speach)
#    rospy.Subscriber("/system_lang", String, system_language)

    subscriber= rospy.Subscriber('recognizer/output', String, listen_callback)
    
    test_dig = [u'一千二百零三',               
                u'一百八十三', ]
    rospy.spin()

    for cn in test_dig:
        print cn,
        print cn2dig(cn)

