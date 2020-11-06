import tensorflow as tf
import math
import os
import numpy as np
class BPCNN_TEST(object):
    def __init__(self):
        # # 定义占位符
        input_size=100
        output_size=10
        hide_size = 5
        self.x = tf.placeholder(tf.float32, shape=(None, 10*10),name='InputData')
        self.y = tf.placeholder(tf.float32, shape=(None, 10),name='OutputData')
        w_hidden = tf.Variable(tf.random_normal([input_size, hide_size], stddev=1, seed=1))
        b_hidden = tf.Variable(tf.zeros([1, hide_size], dtype=tf.float32))
        w_output = tf.Variable(tf.random_normal([hide_size, output_size], stddev=1, seed=1))
        # 定义前向传播过程
        h = tf.nn.tanh(tf.matmul(self.x, w_hidden) + b_hidden)
        y_pred = tf.nn.sigmoid(tf.matmul(h, w_output))
        self.y_pre=y_pred
        with tf.name_scope('mse'):
            self.mse = tf.reduce_mean(tf.square(self.y - y_pred))
            self.mse_1=tf.summary.scalar('mse', self.mse)
        with tf.name_scope('loss-train'):
            self.loss = tf.losses.mean_squared_error(y_pred, self.y)
            self.loss_train_1=tf.summary.scalar('loss-train', self.loss)
        with tf.name_scope('loss-yanzheng'):
            self.loss_yanzheng = tf.losses.mean_squared_error(y_pred, self.y)
            self.loss_yanzheng_1=tf.summary.scalar('loss-yanzheng', self.loss_yanzheng)


        self.merged_summary_op = tf.summary.merge_all()
        self.train_step = tf.train.AdamOptimizer(1e-4).minimize(self.mse)  # 反向传播

        tenboard_dir = 'D:\\tensorboard\\test1'
        self.writer = tf.summary.FileWriter(tenboard_dir, graph=tf.get_default_graph())


    def step(self):
        global step
        self.step = 1
        self.step1 = 0

    def train(self, saver, sess, a, b, c,strategy_id,codeID):
        # print(num,self.step)
        ckpt_dir = "D:/Save"
        for i in range(c - 100):

            mse1, loss_train_1, = sess.run([self.mse_1, self.loss_train_1],
                                           feed_dict={self.x: a[i:i + 10, :], self.y: b[i:i + 10, :]})
            # mse1= sess.run(self.loss,feed_dict={self.x: a[i:i + 10, :], self.y_true: b[i:i + 10, :]})

            self.train_step.run(session=sess, feed_dict={self.x: a[i:i + 10, :],
                                                         self.y: b[i:i + 10, :]})
            if (i % 100 == 50) | (i == (c - 1)):
                self.step = self.step + 1
                # #self.writer.add_summary(loss_train_1,self.step)
                self.writer.add_summary(mse1, self.step)
                saver.save(sess, ckpt_dir + "/my_model_"+strategy_id+"_"+codeID, global_step=50)

    def setyanzheng(self, input, output, long):
        global input_yanzheng
        global output_yanzheng
        for i in range(long):
            if i < (long - 30):
                continue
            self.input_yanzheng = input[i:i + 30, :]
            self.output_yanzheng = output[i:i + 30, :]
            break
        print("setinput", self.input_yanzheng.shape)
        print("setoutput", self.output_yanzheng.shape)

    def putyanzheng(self, input, output, long):
        for i in range(long):
            if i < (long - 30):
                continue
            self.input_yanzheng = np.vstack((self.input_yanzheng, input[i:i + 30, :]))
            self.output_yanzheng = np.vstack((self.output_yanzheng, output[i:i + 30, :]))
            break
        print("putinput", self.input_yanzheng.shape)
        print("putoutput", self.output_yanzheng.shape)

    def getyanzheng(self):
        return self.input_yanzheng, self.output_yanzheng

    def yanzheng(self, saver, sess, a, b, c,strategy_id,codeID):
        # 执行验证集

        saver.restore(sess=sess, save_path="D:/Save/"+"/my_model_"+strategy_id+"_"+codeID+"-50")




        loss_train_1, = sess.run([self.loss_yanzheng_1],
                                                 feed_dict={self.x: a[:c, :], self.y: b[:c, :]})


        self.step1 = self.step1 + 1
        self.writer.add_summary(loss_train_1, self.step1)

    def test(self, saver, sess, a, b, c,strategy_id,codeID):
        saver.restore(sess=sess, save_path="D:/Save/" + "/my_model_" + strategy_id + "_" + codeID)

        loss_train_1, = sess.run([self.y_pre],
                                 feed_dict={self.x: a[i:i + 30, :]})
        return loss_train_1
