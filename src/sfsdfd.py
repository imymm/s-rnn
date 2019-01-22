#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Author: Jiongyu
E-mail: 35024339@qq.com
Description: display about the ground truth,detection,anticipation result.
Organization: GDUT
"""
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import pdb
import sys
import time
import cPickle

start_frame = []
end_frame = []
activity = '1204180344'  # you could choose another activity


def main():
    rospy.init_node("microwaving_food_{0}".format(activity), anonymous=True)
    image_pub = rospy.Publisher("microwaving_food_{0}".format(activity), Image, queue_size=1)
    bridge = CvBridge()

    while (image_pub.get_num_connections() < 1):
        print "the number of connections of the microwaving_food_{0} still less than 1.".format(activity)
        time.sleep(1)

    # CAD-120 dataset
    dataset_CAD120_path = './src/activity-anticipation/src/CAD_120'
    # microwaving_food which we can change to another is topper activity
    image_path = "{0}/person2/Subject3_rgbd_images/microwaving_food/{1}/".format(dataset_CAD120_path, activity)
    ground_truth_label_activity = '{0}/person2/Subject3_annotations/microwaving_food/labeling.txt'.format(
        dataset_CAD120_path)
    object1_location = '{0}/person2/Subject3_annotations/microwaving_food/{1}_obj1.txt'.format(dataset_CAD120_path,
                                                                                               activity)
    object2_location = '{0}/person2/Subject3_annotations/microwaving_food/{1}_obj2.txt'.format(dataset_CAD120_path,
                                                                                               activity)
    print "labeling.txt path:{0}".format(ground_truth_label_activity)
    ground_truth_label_interpreter(ground_truth_label_activity)

    point_object1_location = []
    point_object2_location = []
    object_location_interpreter(object1_location, point_object1_location)
    object_location_interpreter(object2_location, point_object2_location)

    # ground truth
    dic_ground_truth_label_human = {1: 'reaching', 2: 'moving', 3: 'pouring', 4: 'eating', 5: 'drinking', \
                                    6: 'opening', 7: 'placing', 8: 'closing', 9: 'null', 10: 'cleaning', 11: 'error',
                                    12: 'error'}

    dic_ground_truth_label_object = {1: 'mvable', 2: 'stationary', 3: 'reachable', 4: 'pourable', 5: 'pourto', \
                                     6: 'containable', 7: 'drinkable', 8: 'openable', 9: 'placeable', 10: 'closeable', \
                                     11: 'cleanable', 12: 'cleaner', 13: 'error', 14: 'error'}

    # also there could be fold_1 fold_2 fold_3
    ground_truth_path = './src/activity-anticipation/src/activity-anticipation/dataset/fold_4/'
    ground_truth_test_data = cPickle.load(open('{0}/grount_truth_test_data_579188.pik'.format(ground_truth_path)))
    ground_truth_label_human = ground_truth_test_data['labels_human']
    ground_truth_label_object = ground_truth_test_data['labels_objects']

    # prediction about human and object label
    prediction_human_and_object_path = './src/activity-anticipation/src/activity-anticipation/prediction/fold_4/'
    detection_human_data = cPickle.load(
        open('{0}prediction_detection_human_579188.pik'.format(prediction_human_and_object_path)))
    anticipation_human_data = cPickle.load(
        open('{0}prediction_anticipation_human_579188.pik'.format(prediction_human_and_object_path)))
    detection_object_data = cPickle.load(
        open('{0}prediction_detection_object_579188.pik'.format(prediction_human_and_object_path)))
    anticipation_object_data = cPickle.load(
        open('{0}prediction_anticipation_object_579188.pik'.format(prediction_human_and_object_path)))

    # some data about activity.
    # the number 4 is mean that the 5 line(a activity) of the fold3 file in the activity fold.
    # so following above change,you should to change the number.
    truth_human = ground_truth_label_human[26].T[0]
    detect_human = detection_human_data[26].T[0]
    anticipation_human = anticipation_human_data[26].T[0]
    truth_object = ground_truth_label_object[26].T[0]
    detect_object = detection_object_data[26].T[0]
    anticipation_object = anticipation_object_data[26].T[0]

    segement = 0
    point = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    while (segement < len(start_frame)):
        index = start_frame[segement]
        timer = rospy.Rate(20)
        # print "time{0}:".format(segement)
        # print 'ground truth human label:{0}'.format(dic_ground_truth_label_human[truth_human[segement]])
        # print 'ground truth object label:{0}'.format(dic_ground_truth_label_object[truth_object[segement]])
        while ((not rospy.is_shutdown()) and index <= end_frame[segement]):
            data = cv2.imread('{0}RGB_{1}.png'.format(image_path, index))
            cv2.putText(data, "time{0}:".format(segement), (30, 30), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(data,
                        'ground truth human label:{0}'.format(dic_ground_truth_label_human[truth_human[segement]]),
                        (30, 50), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(data,
                        'ground truth object label:{0}'.format(dic_ground_truth_label_object[truth_object[segement]]),
                        (30, 70), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

            cv2.rectangle(data, (point_object1_location[point], point_object1_location[point + 1]), \
                          (point_object1_location[point + 2], point_object1_location[point + 3]), (0, 255, 0), 2)
            cv2.putText(data, "microwaving", (point_object1_location[point], point_object1_location[point + 1] - 10),
                        font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)

            cv2.rectangle(data, (point_object2_location[point], point_object2_location[point + 1]), \
                          (point_object2_location[point + 2], point_object2_location[point + 3]), (0, 255, 0), 2)
            cv2.putText(data, "bowl", (point_object2_location[point], point_object2_location[point + 1] - 10), font,
                        0.75, (0, 255, 0), 1, cv2.LINE_AA)

            # print '{0}RGB_{1}.png'.format(image_path,index)
            # cv2.putText(data,'OpenCV',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
            cv2.putText(data, 'detect human label:{0}'.format(dic_ground_truth_label_human[detect_human[segement]]),
                        (30, 90), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(data, 'detect object label:{0}'.format(dic_ground_truth_label_object[detect_object[segement]]),
                        (30, 110), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(data, 'anticipation human label:{0}'.format(
                dic_ground_truth_label_human[anticipation_human[segement]]), (30, 130), font, 0.5, (0, 0, 0), 1,
                        cv2.LINE_AA)
            cv2.putText(data, 'anticipation object label:{0}'.format(
                dic_ground_truth_label_object[anticipation_object[segement]]), (30, 150), font, 0.5, (0, 0, 0), 1,
                        cv2.LINE_AA)
            cv_image = bridge.cv2_to_imgmsg(data, "bgr8")
            image_pub.publish(cv_image)
            index += 1
            point += 4
            timer.sleep()

            # print 'detect human label:{0}'.format(dic_ground_truth_label_human[detect_human[segement]])
        # print 'detect object label:{0}'.format(dic_ground_truth_label_object[detect_object[segement]])
        # print 'anticipation human label:{0}'.format(dic_ground_truth_label_human[anticipation_human[segement]])
        # print 'anticipation object label:{0}'.format(dic_ground_truth_label_object[anticipation_object[segement]])

        time.sleep(2)
        segement += 1


def ground_truth_label_interpreter(file):
    """
    following the CAD-120 dataset,this funcition can get the start,end frame of a activity.
    """
    # pdb.set_trace()
    global start_frame
    global end_frame
    f = open(file)
    line = f.readline()
    while line:
        s = line.split(',')
        if (s[0] == activity):
            start_frame.append(int(s[1]))
            end_frame.append(int(s[2]))
            # pdb.set_trace()
        line = f.readline()
    f.close()


def object_location_interpreter(file, point_object_location):
    """
    following the CAD-120 dataset,this funcition can get the object upper left,lower right corner in the picture.
    """
    # pdb.set_trace()
    f = open(file)
    line = f.readline()
    while line:
        s = line.split(',')
        point_object_location.append(int(s[2]))
        point_object_location.append(int(s[3]))
        point_object_location.append(int(s[4]))
        point_object_location.append(int(s[5]))
        # pdb.set_trace()
        line = f.readline()
    f.close()


if __name__ == "__main__":
# pdb.set_trace()
main()