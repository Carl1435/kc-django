import tensorflow as tf
import math
import os

import numpy as np
class TestCNN(object):

    def __init__(self):
        # # 定义占位符
        self.LearningRate=1e-4
        self.x = tf.placeholder('float', shape=[None, 10 * 10],name='InputData')
        self.y_true = tf.placeholder('float', shape=[None, 10],name='OutputData')
        #
        self.x_image = tf.reshape(self.x, [-1, 10, 10, 1])
        #
        # 1st layer: 第一次卷积加池化

        w_conv1 = self.weights([3, 3, 1, 6])#产生卷积核 用正态分布
        b_conv1 = self.bias([6])#[[0.1],[0.1],[0.1],[0.1],[0.1],[0.1],[0.1]]
        h_conv1 = tf.nn.relu(self.conv2d(self.x_image, w_conv1) + b_conv1)
        h_pool1 = self.max_pool_2x2(h_conv1)
        h_pool2_flat = tf.reshape(h_pool1, [-1, 150])




        # # 2nd layer: 第二次卷积加池化
        # w_conv2 = self.weights([5, 5, 6, 16])
        # b_conv2 = self.bias([16])
        # h_conv2 = tf.nn.relu(self.conv2d(h_pool1, w_conv2) + b_conv2)
        # h_pool2 = self.max_pool_2x2(h_conv2)
        # h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 16])

        w_fc1 = self.weights([150, 20])
        b_fc1 = self.bias([20])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)
        # 3rd layer: 全连接*3
        # w_fc1 = self.weights([7 * 7 * 16, 120])
        # b_fc1 = self.bias([120])
        # h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)

        # w_fc2 = self.weights([30, 84])
        # b_fc2 = self.bias([84])
        # h_fc2 = tf.nn.relu(tf.matmul(h_fc1, w_fc2) + b_fc2)

        w_fc3 = self.weights([20, 10])
        b_fc3 = self.bias([10])
        h_fc3 = tf.matmul(h_fc1, w_fc3) + b_fc3

        with tf.name_scope('mse'):
            self.mse = tf.reduce_mean(tf.square(self.y_true - h_fc3))
            self.mse_1=tf.summary.scalar('mse', self.mse)
        with tf.name_scope('loss-train'):
            self.loss = tf.losses.mean_squared_error(h_fc3, self.y_true)
            self.loss_train_1=tf.summary.scalar('loss-train', self.loss)

        with tf.name_scope('loss-yanzheng'):
            self.loss_yanzheng = tf.losses.mean_squared_error(h_fc3, self.y_true)
            self.loss_yanzheng_1=tf.summary.scalar('loss-yanzheng', self.loss_yanzheng)


        self.merged_summary_op = tf.summary.merge_all()
        self.train_step = tf.train.AdamOptimizer(1e-4).minimize(self.loss)  # 反向传播
        # 使用tf.summary.FileWriter(path, graph)将日志写入到文件中
        # path:日志文件保存路径， graph:需要保存的图
        tenboard_dir = 'D:\\tensorboard\\test1'
        self.writer = tf.summary.FileWriter(tenboard_dir, graph=tf.get_default_graph())

    def weights(self,shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    def bias(self,shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)
    # 卷积
    def conv2d(self,x, W):
        return tf.nn.atrous_conv2d(x,W, 2,'SAME', name=None)
        #return tf.nn.conv2d(input=x, filter=W, strides=[1, 1, 1, 1], padding='SAME')
    # 池化
    def max_pool_2x2(self,x):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    def step(self):
        global step
        global step1
        self.step = 1
        self.step1 = 0

    def train(self,saver,sess,a,b,c,strategy_id,codeID):
        #print(num,self.step)
        ckpt_dir = "D:/Save"
        for i in range(c-100):

            mse1,loss_train_1, = sess.run([self.mse_1,self.loss_train_1],feed_dict={self.x: a[i:i + 10, :], self.y_true: b[i:i + 10, :]})
            #mse1= sess.run(self.loss,feed_dict={self.x: a[i:i + 10, :], self.y_true: b[i:i + 10, :]})


            self.train_step.run(session=sess, feed_dict={self.x: a[i:i + 10, :],
                                                         self.y_true: b[i:i + 10, :]})
            if (i % 100 == 50) | (i == (c - 1)):
                self.step=self.step+1
                # #self.writer.add_summary(loss_train_1,self.step)
                self.writer.add_summary(mse1,self.step)
                saver.save(sess,  ckpt_dir + "/my_model_"+strategy_id+"_"+codeID, global_step=50)

    def setyanzheng(self, input, output, long):
        global input_yanzheng
        global output_yanzheng
        for i in range(long):
            if i < (long - 100):
                continue
            self.input_yanzheng = input[i:i+100,:]
            self.output_yanzheng = output[i:i+100,:]
            break
        print("setinput",self.input_yanzheng.shape)
        print("setoutput",self.output_yanzheng.shape)

    def putyanzheng(self,input,output,long):
        for i in range(long):
            if i<(long-100):
                continue
            self.input_yanzheng = np.vstack((self.input_yanzheng,input[i:i+100,:]))
            self.output_yanzheng = np.vstack((self.output_yanzheng,output[i:i+100,:]))
            break
        print("putinput", self.input_yanzheng.shape)
        print("putoutput", self.output_yanzheng.shape)

    def getyanzheng(self):
       return self.input_yanzheng,self.output_yanzheng

    def yanzheng(self,saver,sess,a,b,c,strategy_id,codeID):
        # 执行验证集

        saver.restore(sess=sess, save_path="D:/Save/"+"/my_model_"+strategy_id+"_"+codeID+"-50")


        for i in range(c):
            if i%100==0:
                loss_train_1, = sess.run([self.loss_yanzheng_1],
                                         feed_dict={self.x: a[i:i+30, :], self.y_true: b[i:i+30, :]})
                self.step1 = self.step1 + 1
                self.writer.add_summary(loss_train_1, self.step1)







    def test(self):
        saver.restore(sess=sess, save_path="D:/Save/" + "/my_model_" + strategy_id + "_" + codeID + "-50")

        for i in range(c):
            if i % 100 == 0:
                loss_train_1, = sess.run([self.y_true],
                                         feed_dict={self.x: a[i:i + 30, :]})
                return loss_train_1