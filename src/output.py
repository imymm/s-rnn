#coding=utf-8

from readresult import  ReadFile
from readresult import ReadTestFile


'''


def Trans(FilePath,Index):

    HumanIdentDict = {1:'reaching',2:'moving',3:'pouring',4:'eating',5:'drinking',6:'opening',7:'placing',8:'closing',9:'null'}
    ObjectIdentDict = {1:'movable',2:'stationary',3:'reachable',4:'pourable',5:'pourto',6:'containable',7:'drinkable',8:'openable',9:'placeable',10:'closeable'}

    ReslutDetection,ReslutAnticipation = ReadFile(FilePath,Index)

    print ReslutDetection



def HumanAna(ReslutDetection):
    HumanIdentDict = {1: 'reaching', 2: 'moving', 3: 'pouring', 4: 'eating', 5: 'drinking', 6: 'opening', 7: 'placing',8: 'closing', 9: 'null'}
    return HumanIdentDict[ReslutDetection]

def ObjectAna(ReslutDetection):
    ObjectIdentDict = {1: 'movable', 2: 'stationary', 3: 'reachable', 4: 'pourable', 5: 'pourto', 6: 'containable',7: 'drinkable', 8: 'openable', 9: 'placeable', 10: 'closeable'}
    return ObjectIdentDict[ReslutDetection]


def PathSend():
    pub = rospy.Publisher('ImagePath',String,queue_size=10)
    rospy.init_node('image',anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        path = '/home/yz/human_anticipation_data/person2/Subject3_rgbd_images/making_cereal/1204173536/RGB_406.png'
        pub.publish(path)
        rate.sleep()
'''



if __name__ == '__main__':
    filePath = '/home/yz/human_anticipation_data/result'
    testDataPat = '/home/yz/human_anticipation_data/CAD_120/features_cad120_ground_truth_segmentation/dataset2/fold_5'
    index = 502308

    #Trans(filePath,index)


