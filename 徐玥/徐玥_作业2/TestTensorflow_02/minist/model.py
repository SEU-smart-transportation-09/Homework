import tensorflow as tf

# 定义一个线性模型
# Y = W * x + b
def regression(x):
   W = tf.Variable(tf.zeros([784, 10]), name="W")
   b = tf.Variable(tf.zeros([10]), name="b")
   y = tf.nn.softmax(tf.matmul(x, W)+b)

   return y, [W, b]

# 定义一个卷积模型
def convolutional(x, keep_prob):

   # 定义一个卷积层
   def conv2d(x, W):
      return tf.nn.conv2d(x, W, [1, 1, 1, 1], padding='SAME')

   # 定义一个池化层
   def max_pool_2x2(x):
      return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME' )

   # 定义一个权重变量
   def weight_variable(shape):
      initial = tf.truncated_normal(shape, stddev=0.1)
      return tf.Variable(initial)

   def bias_variable(shape):
      initial = tf.constant(0.1, shape=shape)
      return tf.Variable(initial)

   x_image = tf.reshape(x, [-1, 28, 28, 1])
   W_conv1 = weight_variable([5, 5, 1, 32])
   b_conv1 = bias_variable([32])
   h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1)+b_conv1)
   h_pool1 = max_pool_2x2(h_conv1)
   # 第一层

   W_conv2 = weight_variable([5, 5, 32, 64])
   b_conv2 = bias_variable([64])
   h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2)+b_conv2)
   h_pool2 = max_pool_2x2(h_conv2)
   # 第二层

   # 全连接层
   W_fc1 = weight_variable([7*7*64, 1024])
   b_fc1 = bias_variable([1024])
   h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
   h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1)+b_fc1)
   # drop函数 随机扔掉一些值 为了防止过拟合
   h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

   W_fc2 = weight_variable([1024, 10])
   b_fc2 = bias_variable([10])
   y = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2)+b_fc2)

   return y, [W_conv1, b_conv1, W_conv2, b_conv2, W_fc1, b_fc1, W_fc2, b_fc2]