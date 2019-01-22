#coding=utf-8





import cPickle


'''
def ReadFile(ReadPath,index):
    ReslutDetection = cPickle.load(open('{1}/detection_data_{0}.pik'.format(index,ReadPath)))
    ReslutAnticipation = cPickle.load(open('{1}/anticipation_data_{0}.pik'.format(index,ReadPath)))
    #ReslutJoint = cPickle.load(open('{1}/joint_data_{0}.pik/'.format(index,ReadPath)))
    print ReslutDetection
    return ReslutDetection,ReslutAnticipation

def ReadTestFile(ReadPath,index):
    TestData = cPickle.load(open('{1}/test_data_{0}.pik'.format(index,ReadPath)))
    #print TestData['labels_human'],TestData['labels_objects']
    print TestData['labels_human']

'''

if __name__ == '__main__':
    testDataPat = '/home/yz/human_anticipation_data/CAD_120/features_cad120_ground_truth_segmentation/dataset2/fold_5'
    filePath = '/home/yz/human_anticipation_data/result'
    index = 502308

    print 'filepath={0}'.format(filePath)

    #ReadFile(filePath,index)
    #ReadTestFile(testDataPat,index)




