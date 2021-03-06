#!/usr/bin/env python
#coding=utf-8

import numpy as np
import os
import sys
import cPickle
from theano import tensor as T
from readData import sortActivities
#from neuralmodels.utils import permute, load, loadSharedRNN, loadSharedRNNVectors, loadSharedRNNOutput
from neuralmodels.utils import permute
from neuralmodels.loadcheckpoint import load, loadSharedRNN, loadSharedRNNVectors, loadSharedRNNOutput
from neuralmodels.costs import softmax_loss
from neuralmodels.predictions import OutputMaxProb, OutputSampleFromDiscrete
from neuralmodels.layers import softmax, simpleRNN, OneHot, LSTM, TemporalInputFeatures
from image import label_get,activate_get
from image import display
#from output import HumanAna,ObjectAna
import pdb



def predict_activitiy(index,fold,checkpoint,architecture='joint'):

	path_to_dataset = '/home/yz/human_anticipation_data/CAD_120/features_cad120_ground_truth_segmentation/dataset2/fold_5'
	path_to_checkpoints = '/home/yz/human_anticipation_data/checkpoint1/full_model_fold_1/'
	path_to_result = '/home/yz/human_anticipation_data/result/'

	print 'load test data'
	test_data = cPickle.load(open('{1}/test_data_{0}.pik'.format(index,path_to_dataset)))	
	print 'end load '

	Y_te_human = test_data['labels_human']
	Y_te_human_anticipation = test_data['labels_human_anticipation']
	X_te_human_disjoint = test_data['features_human_disjoint']
	X_te_human_shared = test_data['features_human_shared']

	Y_te_objects = test_data['labels_objects']
	Y_te_objects_anticipation = test_data['labels_objects_anticipation']
	X_te_objects_disjoint = test_data['features_objects_disjoint']
	X_te_objects_shared = test_data['features_objects_shared']

	print 'load checkpoint'
	sharedrnn = []
	if architecture in ['detection','anticipation']:
		sharedrnn = loadSharedRNN('{2}/{0}/checkpoint.{1}'.format(index,checkpoint,path_to_checkpoints))
	else:
		sharedrnn = loadSharedRNNOutput('{2}/{0}/checkpoint.{1}'.format(index,checkpoint,path_to_checkpoints))
	print 'end load checkpoint'

	predictions = []
	errors = 0
	errors_objects = 0

	N = 0
	N_objects = 0

	detection = np.array([])
	anticipation = np.array([])

	activate_list = activate_get()
	label_list = label_get()

	if architecture == 'detection':

		for xte_shared,xte,yte in zip(X_te_human_shared,X_te_human_disjoint,Y_te_human):
			prediction = sharedrnn.predict_output(xte_shared,xte,OutputMaxProb)
			predictions.append(prediction)
			t = np.nonzero(yte-prediction)
			errors += len(t[0])
			N += yte.shape[0]
			
		for xte_shared,xte,yte in zip(X_te_objects_shared,X_te_objects_disjoint,Y_te_objects):
			prediction = sharedrnn.predict_output(xte_shared,xte,OutputMaxProb,layer=2)
			predictions.append(prediction)
			t = np.nonzero(yte-prediction)
			errors_objects += len(t[0])
			N_objects += yte.shape[0]

		cPickle.dump(predictions, open('{1}/detection_data_{0}.pik'.format(index, path_to_result), 'wb'))
		detection = np.array([1.0-(errors*1.0/N),1.0-(errors_objects*1.0/N_objects)])

	elif architecture == 'anticipation':
		for xte_shared,xte,yte in zip(X_te_human_shared,X_te_human_disjoint,Y_te_human_anticipation):
			prediction = sharedrnn.predict_output(xte_shared,xte,OutputMaxProb)
			predictions.append(prediction)
			t = np.nonzero(yte[:-1]-prediction[:-1])
			errors += len(t[0])
			N += yte.shape[0] - 1
			#print '1 prediction={0}'.format(prediction)
		for xte_shared,xte,yte in zip(X_te_objects_shared,X_te_objects_disjoint,Y_te_objects_anticipation):
			prediction = sharedrnn.predict_output(xte_shared,xte,OutputMaxProb,2)
			predictions.append(prediction)
			t = np.nonzero(yte[:-1]-prediction[:-1])
			errors_objects += len(t[0])
			N_objects += yte.shape[0] - 1
			#print '2 prediction={0}'.format(prediction)
		cPickle.dump(predictions, open('{1}/anticipation_data_{0}.pik'.format(index, path_to_result), 'wb'))
		anticipation = np.array([1.0-(errors*1.0/N),1.0-(errors_objects*1.0/N_objects)])

	elif architecture == 'joint':
		for xte_shared,xte,yte in zip(X_te_human_shared,X_te_human_disjoint,Y_te_human_anticipation):
			prediction = sharedrnn.predict_output(xte_shared,xte,OutputMaxProb,1,'anticipation')
			predictions.append(prediction)
			t = np.nonzero(yte[:-1]-prediction[:-1])
			errors += len(t[0])
			N += yte.shape[0] - 1
		for xte_shared,xte,yte in zip(X_te_objects_shared,X_te_objects_disjoint,Y_te_objects_ant-icipation):
			prediction = sharedrnn.predict_output(xte_shared,xte,OutputMaxProb,2,'anticipation')
			predictions.append(prediction)
			t = np.nonzero(yte[:-1]-prediction[:-1])
			errors_objects += len(t[0])
			N_objects += yte.shape[0] - 1

		anticipation = np.array([1.0-(errors*1.0/N),1.0-(errors_objects*1.0/N_objects)])
		errors = 0
		errors_objects = 0
		N = 0
		N_objects = 0

		for xte_shared,xte,yte in zip(X_te_human_shared,X_te_human_disjoint,Y_te_human):
			prediction = sharedrnn.predict_output(xte_shared,xte,OutputMaxProb,1,'detection')
			predictions.append(prediction)
			t = np.nonzero(yte-prediction)
			errors += len(t[0])
			N += yte.shape[0]
		for xte_shared,xte,yte in zip(X_te_objects_shared,X_te_objects_disjoint,Y_te_objects):
			prediction = sharedrnn.predict_output(xte_shared,xte,OutputMaxProb,2,'detection')
			predictions.append(prediction)
			t = np.nonzero(yte-prediction)
			errors_objects += len(t[0])
			N_objects += yte.shape[0]
		cPickle.dump(predictions, open('{1}/joint_data_{0}.pik'.format(index, path_to_result), 'wb'))
		detection = np.array([1.0-(errors*1.0/N),1.0-(errors_objects*1.0/N_objects)])

	return {'detection':detection, 'anticipation':anticipation}

if __name__ == "__main__":
	index = sys.argv[1]
	checkpoint = sys.argv[2]

	#architecture='joint'
	architecture = 'anticipation'
	#architecture = 'detection'

	checkpoints = [checkpoint,checkpoint,checkpoint,checkpoint]

	print "Using {0} architecture".format(architecture)
	print "************* Checkpoint {0} ************".format(checkpoint)

	folds = ['1','2','3','4']
	err_detection = []	
	err_anticipation = []

	#print "fold={0} checkpoint={1}".format(fold,checkpoint)
	#result = predict_activitiy(index,'fold_5',checkpoint,architecture)
	result = predict_activitiy(index, 'fold_5', checkpoint, architecture)

	detection = result['detection']
	anticipation = result['anticipation']

	if detection.shape[0] > 0:
		err_detection.append(detection)
	if anticipation.shape[0] > 0:
		err_anticipation.append(anticipation)
	if len(err_detection) > 0:
		print "Detection result"
		print err_detection
		err_detection = np.array(err_detection)
		print 'Activity: {0} ({1}); Affordance: {2} ({3})'.format(np.mean(err_detection[:,0]),np.std(err_detection[:,0]),np.mean(err_detection[:,1]),np.std(err_detection[:,1]))
		print ''

	if len(err_anticipation) > 0:
		print "Anticipation result"
		print err_anticipation
		err_anticipation = np.array(err_anticipation)
		print 'Activity: {0} ({1}); Affordance: {2} ({3})'.format(np.mean(err_anticipation[:,0]),np.std(err_anticipation[:,0]),np.mean(err_anticipation[:,1]),np.std(err_anticipation[:,1]))
		print ''







