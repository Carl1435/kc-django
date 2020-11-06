
import pandas as pd
import csv
import os
import xlrd
import tensorflow.examples.tutorials.mnist.input_data as input_data
import tensorflow as tf
import numpy as np
import MySQLdb
BPCNN_TEST=__import__("BPCNN_TEST")
BPCNN_TEST_1=BPCNN_TEST.BPCNN_TEST()
test_cnn = __import__("cnn_test")
Test_cnn=test_cnn.TestCNN()

def train(Code_ID,strategy_train_start,strategy_train_end,strategy_verify_start, strategy_verify_end,strategy_Model_choose, strategy_epoch_num_choose,if_open, if_high, if_low, if_vol, if_amo):

        #, strategy_verify_start, strategy_verify_end,
    # strategy_Model_choose, strategy_epoch_num_choose, if_open, if_high, if_low, if_vol, if_amo
    # 都数据库得到 daycode,,epoch_num,input,output,input_yanzheng, output_yanzheng,

    #从code_ID按strategy_train_start,strategy_train_end,strategy_verify_start,strategy_verify_end读if_open,if_high,if_low,if_vol,if_amo


    db = MySQLdb.connect("139.9.169.15", "huawei", "123456", "huawei", charset='utf8')
    cursor = db.cursor()


    sql_train_close="SELECT close FROM " + Code_ID + " where `index`> \'" + strategy_train_start + "\' AND  `index`< \'" + strategy_train_end + "\'"
    cursor.execute(sql_train_close)
    result = cursor.fetchall()
    output_train=np.array(result, dtype=float)

    if (if_low == 1):
        sql_train_low = "SELECT low FROM " + Code_ID + " where `index`> \'" + strategy_train_start + "\' AND  `index`< \'" + strategy_train_end + "\'"
        cursor.execute(sql_train_low)
        result = cursor.fetchall()
        input_train_low = np.array(result, dtype=float)
    else:
        input_train_low = np.zeros(output_train.shape, dtype=float)
    if (if_vol == 1):
        sql_train_vol = "SELECT vol FROM " + Code_ID + " where `index`> \'" + strategy_train_start + "\' AND  `index`< \'" + strategy_train_end + "\'"
        cursor.execute(sql_train_vol)
        result = cursor.fetchall()
        input_train_vol = np.array(result, dtype=float)
    else:
        input_train_vol = np.zeros(output_train.shape, dtype=float)
    if (if_amo == 1):
        sql_train_amo = "SELECT amount FROM " + Code_ID + " where `index`> \'" + strategy_train_start + "\' AND  `index`< \'" + strategy_train_end + "\'"
        cursor.execute(sql_train_amo)
        result = cursor.fetchall()
        input_train_amo = np.array(result, dtype=float)
    else:
        input_train_amo = np.zeros(output_train.shape, dtype=float)
    if (if_high == 1):
        sql_train_high = "SELECT high FROM " + Code_ID + " where `index`> \'" + strategy_train_start + "\' AND  `index`< \'" + strategy_train_end + "\'"
        cursor.execute(sql_train_high)
        result = cursor.fetchall()
        input_train_high = np.array(result, dtype=float)
    else:
        input_train_high = np.zeros(output_train.shape, dtype=float)
    if (if_open == 1):
        sql_train_open = "SELECT open FROM " + Code_ID + " where `index`> \'" + strategy_train_start + "\' AND  `index`< \'" + strategy_train_end + "\'"
        cursor.execute(sql_train_open)
        result = cursor.fetchall()
        input_train_open = np.array(result, dtype=float)
    else:
        input_train_open  = np.zeros(output_train.shape, dtype=float)
    db.close()

    input_train = np.append(input_train_amo,input_train_high, axis=1)
    input_train = np.append(input_train, input_train_low, axis=1)
    input_train = np.append(input_train, input_train_open,axis=1)
    input_train = np.append(input_train, input_train_vol,axis=1)
    for i in range(5):
        input_train = np.append(input_train,np.zeros(output_train.shape, dtype=float), axis=1)
    # print(input_train.shape)
    # print(output_train.shape)

    sql_verify_close = "SELECT close FROM " + Code_ID + " where `index`> \'" + strategy_verify_start + "\' AND  `index`< \'" + strategy_verify_end + "\'"
    cursor.execute(sql_verify_close)
    result = cursor.fetchall()
    output_verify = np.array(result, dtype=float)

    if (if_low == 1):
            sql_verify_low = "SELECT low FROM " + Code_ID + " where `index`> \'" + strategy_verify_start + "\' AND  `index`< \'" + strategy_verify_end + "\'"
            cursor.execute(sql_verify_low)
            result = cursor.fetchall()
            input_verify_low = np.array(result, dtype=float)
    else:
            input_verify_low = np.zeros(output_verify.shape, dtype=float)
    if (if_vol == 1):
            sql_verify_vol = "SELECT vol FROM " + Code_ID + " where `index`> \'" + strategy_verify_start + "\' AND  `index`< \'" + strategy_verify_end + "\'"
            cursor.execute(sql_verify_vol)
            result = cursor.fetchall()
            input_verify_vol = np.array(result, dtype=float)
    else:
            input_verify_vol = np.zeros(output_verify.shape, dtype=float)
    if (if_amo == 1):
            sql_verify_amo = "SELECT amount FROM " + Code_ID + " where `index`> \'" + strategy_verify_start + "\' AND  `index`< \'" + strategy_verify_end + "\'"
            cursor.execute(sql_verify_amo)
            result = cursor.fetchall()
            input_verify_amo = np.array(result, dtype=float)
    else:
            input_verify_amo = np.zeros(output_verify.shape, dtype=float)
    if (if_high == 1):
            sql_verify_high = "SELECT high FROM " + Code_ID + " where `index`> \'" + strategy_verify_start + "\' AND  `index`< \'" + strategy_verify_end + "\'"
            cursor.execute(sql_verify_high)
            result = cursor.fetchall()
            input_verify_high = np.array(result, dtype=float)
    else:
            input_verify_high = np.zeros(output_verify.shape, dtype=float)
    if (if_open == 1):
            sql_verify_open = "SELECT open FROM " + Code_ID + " where `index`> \'" + strategy_verify_start + "\' AND  `index`< \'" + strategy_verify_end + "\'"
            cursor.execute(sql_verify_open)
            result = cursor.fetchall()
            input_verify_open = np.array(result, dtype=float)
    else:
            input_verify_open = np.zeros(output_verify.shape, dtype=float)
    db.close()

    input_verify = np.append(input_verify_amo, input_verify_high, axis=1)
    input_verify = np.append(input_verify, input_verify_low, axis=1)
    input_verify = np.append(input_verify, input_verify_open, axis=1)
    input_verify = np.append(input_verify, input_verify_vol, axis=1)
    for i in range(5):
            input_verify = np.append(input_verify, np.zeros(output_verify.shape, dtype=float), axis=1)
    # print(input_verify.shape)
    # print(output_verify.shape)


    if(strategy_Model_choose==1):
        cnn_train(input_train,output_train,input_verify,output_verify,strategy_epoch_num_choose*250+250,strategy_name,Code_ID)
        cnn_verify()
    else:
        bp_train(input_train,output_train,input_verify,output_verify,strategy_epoch_num_choose*250+250,strategy_name,Code_ID)
        bp_verify()


def cnn_train(input_train,output_train,input_verify,output_verify,strategy_epoch_num_choose):
    with tf.Session() as sess:
        init = tf.initialize_all_variables()
        sess.run(init)
        tf.global_variables_initializer().run()
        saver = tf.train.Saver()
        Test_cnn.step()
        input_train = input_train.reshape(input_train.shape[0] // 10, 100)
        input_verify = input_verify.reshape(input_verify.shape[0] // 10, 100)
        for j in range(strategy_epoch_num_choose):
                Test_cnn.train(saver, sess,input_train, output_train, input_train.shape[0] - 10,strategy_name,Code_ID)
                Test_cnn.yanzheng(saver, sess, input_verify, output_verify, input_verify.shape[0] - 10,strategy_name,Code_ID)
        #Test_cnn.test()


def bp_train(input_train,output_train,input_verify,output_verify,strategy_epoch_num_choose,strategy_name,Code_ID):
   with tf.Session() as sess:
        init = tf.initialize_all_variables()
        sess.run(init)
        tf.global_variables_initializer().run()
        saver = tf.train.Saver()
        BPCNN_TEST_1.step()
        input_train = input_train.reshape(input_train.shape[0] // 10, 100)
        input_verify = input_verify.reshape(input_verify.shape[0] // 10, 100)
        for j in range(strategy_epoch_num_choose):
            BPCNN_TEST_1.train(saver, sess, i, input_train, output_train, input_train.shape[0]- 10,strategy_name,Code_ID)
            BPCNN_TEST_1.yanzheng(saver, sess, input_verify, output_verify, input_verify.shape[0] - 10,strategy_name,Code_ID)
        #BPCNN_TEST_1.test()




