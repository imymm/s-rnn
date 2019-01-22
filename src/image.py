#!/usr/bin/env python
#coding=utf-8
import rospy
import cv2
from std_msgs.msg import String
from std_msgs.msg import Int32

import roslib
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import re
from os import listdir
import random
import sys
import os
import cPickle
import pdb
import numpy as np

index = 502308

HumanIdentDict = {1: 'reaching', 2: 'moving', 3: 'pouring', 4: 'eating', 5: 'drinking', 6: 'opening', 7: 'placing',8: 'closing', 9: 'null'}
ObjectIdentDict = {1: 'movable', 2: 'stationary', 3: 'reachable', 4: 'pourable', 5: 'pourto', 6: 'containable',7:'drinkable', 8: 'openable', 9: 'placeable', 10: 'closeable'}
picture_file = '/home/yz/human_anticipation_data/person2/Subject3_rgbd_images/having_meal'
filePath = '/home/yz/human_anticipation_data/result'
testDataPath = '/home/yz/human_anticipation_data/CAD_120/features_cad120_ground_truth_segmentation/dataset2/fold_5'

#获取label中数据
def label_get():
    picture_order_path = '/home/yz/human_anticipation_data/person2/Subject3_annotations/having_meal/labeling.txt'
    line_list = []
    lines = open(picture_order_path).readlines()
    for line in lines:
        line = line.strip()
        if line > 0:
            activate_list = line.split(",")
            line_list.append(activate_list)
    return line_list

#获取活动列表
def activate_get():
    picture_file = '/home/yz/human_anticipation_data/person2/Subject3_rgbd_images/having_meal/'
    activate_path = '/home/yz/human_anticipation_data/CAD_120/features_cad120_ground_truth_segmentation/segments_svm_format/fold5.txt'

    activates = open(activate_path).readlines()
    activate_list = []

    for activate in activates:
        activate = activate.strip()
        if activate > 0:
            activate_list.append(activate)
    #print  activate_list
    return activate_list


def Imageshow(path,human_dete,obj_dete,hum_anti,obj_anti,human_true,obj_true):

    str_truth = 'hum_tru={0},obj_tru={1}'.format(human_true,obj_true)
    str_detec = 'hum_det={0},obj_det={1}'.format(HumanIdentDict[human_dete],ObjectIdentDict[obj_dete])
    str_anti =  'hum_ant={0},obj_anti={1}'.format(HumanIdentDict[hum_anti],ObjectIdentDict[obj_anti])

    img = cv2.imread(path,cv2.IMREAD_COLOR)
    image_pub = rospy.Publisher('ImagePath',Image,queue_size=10)
    brideg = CvBridge()
    cv2.putText(img,str_truth,(5,25),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
    cv2.putText(img,str_detec,(5,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
    cv2.putText(img,str_anti,(5,75),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)

    image_pub.publish(brideg.cv2_to_imgmsg(img,'bgr8'))


def display():
    rospy.init_node('image', anonymous=True)
    rate = rospy.Rate(50)

    ReslutDetection = cPickle.load(open('{1}/detection_data_{0}.pik'.format(index,filePath)))                   #获得的结果
    ReslutAnticipation = cPickle.load(open('{1}/anticipation_data_{0}.pik'.format(index,filePath)))

    Feature_dete = []           #改变形状
    Feature_dete_list = []
    for DeteList in ReslutDetection:
        for Dete in DeteList:
            Feature_dete.append(Dete[0])
        Feature_dete_list.append(Feature_dete)
        Feature_dete=[]
    humanFeature_Dete = [Feature_dete_list[0], Feature_dete_list[1], Feature_dete_list[2]]
    ObjFeature_dete = [Feature_dete_list[3], Feature_dete_list[4], Feature_dete_list[5]]

    Feature_anti = []
    Feature_anti_list = []
    for Anti in ReslutAnticipation:
        for Anti in Anti:
            Feature_anti.append(Anti[0])
        Feature_anti_list.append(Feature_anti)
        Feature_anti=[]

    humanFeature_Anti = [Feature_anti_list[0], Feature_anti_list[1], Feature_anti_list[2]]
    ObjFeature_Anti = [Feature_anti_list[3], Feature_anti_list[4], Feature_anti_list[5]]

    label_list = label_get()                #获取标签
    activate_list = activate_get()          #获取活动

    for activate,detec in zip(activate_list,range(3)):
        label_number = 0
        for x in label_list:
            start = int(x[1])
            end = int(x[2])
            num = int(0)
            cnt = int(0)
            if activate == x[0]:
                while ((not rospy.is_shutdown()) and  cnt < end):
                    cnt = int(start) + int(num)
                    num = num + 1
                    picture_path = '{2}/{1}/RGB_{0}.png'.format(cnt,activate,picture_file)
                    Imageshow(picture_path, humanFeature_Dete[detec][label_number],
                              ObjFeature_dete[detec][label_number], humanFeature_Anti[detec][label_number],
                              ObjFeature_Anti[detec][label_number], x[3], x[4])
                    rate.sleep()
                label_number = label_number + 1

if __name__ == '__main__':
    try:
        display()
    except KeyboardInterrupt:
        pass




