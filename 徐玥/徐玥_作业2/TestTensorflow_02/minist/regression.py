import os
import input_data
import model
import tensorflow as tf

data = input_data.read_data_sets('MNIST_data', one_hot=True)

# 引入 建立模型
with tf.variable_scope("regression"):
    x = tf.placeholder(tf.float32, [None, 784])
    # 占位符，第一个是传进来的格式，第二个是张量
    y, variables = model.regression(x)

# 训练
y_ = tf.placeholder("float", [None, 10])
# 交叉熵
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
# 优化器 步长0.01
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
# 预测
correct_prediction = tf.equal(tf.arg_max(y, 1), tf.arg_max(y_, 1))
# 转换格式
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# 训练五部完成 下面是参数保存
saver = tf.train.Saver(variables)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    # 把所有参数进行全局初始化 放进来
    for _ in range(1000):
        batch_xs, batch_ys = data.train.next_batch(100)
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
        # feed_dict 往里面放参数
    print((sess.run(accuracy, feed_dict={x: data.test.images, y_: data.test.labels})))
    # 数据、参数，或者说模型存起来
    path = saver.save(
        sess, os.path.join(os.path.dirname(__file__),'data','regression.ckpt'),
        write_meta_graph=False,write_state=False)
    print("Saved:", path)
