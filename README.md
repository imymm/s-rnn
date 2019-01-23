# SRNN Human-Object Activities Preadiction for ROS
=============

Summary
--------
This is a human motion detection and prediction of the demonstration program. Including the detection and prediction of human motion, as well as the detection and prediction of object behavior. So far we have tested this node with kinetic ROS under ubuntu16.04. If you have any questions about the code, please contact us.

Quickstart
-----------
It is recommended to install python reuirements in virtual envirnment created bu conda\
1、ROS(Kinetic Kame on ubuntu16.04)\
2、Python 2.7\
3、Theano(>=0.6)\
4、Neural Models [!Neural Models](https://github.com/asheshjain399/NeuralModels)   \

Environment setup\

conda create -n ros_srnn python=2.7 Theano matplotlib\
conda activate ros_srnn\
pip install rosinstall\
git clone https://github.com/asheshjain399/NeuralModels.git  \
cd NeuralModels\
git checkout srnn\
python setup.py develop \



Overview
-------
readData： This program can convert an array into SVN format \
activity-rnn-full-model： Model training \
activity_prediction_sharedrnn：Model to predict \
image：Display
video
--------




FAQ
--------



















